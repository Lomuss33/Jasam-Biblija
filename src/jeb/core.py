"""Strict local IO, configuration and schema helpers."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import unicodedata
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

BOOKS = ("GEN", "MAT", "MRK", "LUK", "JHN")
SCHEMA_VERSION = "1.0"
MAX_DOCUMENT = 8 * 1024 * 1024


class JebError(ValueError):
    """Actionable validation failure; never a successful partial ingest."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise JebError(message)


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate key: {key}")
        result[key] = value
    return result


def json_loads(text: str) -> Any:
    def bad_number(value: str) -> None:
        raise JebError(f"Non-finite JSON number: {value}")

    try:
        return json.loads(text, object_pairs_hook=unique_pairs, parse_constant=bad_number)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise JebError(f"Invalid JSON: {exc}") from exc


class UniqueLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader: UniqueLoader, node: yaml.MappingNode) -> dict:
    return unique_pairs(
        [(loader.construct_object(k), loader.construct_object(v)) for k, v in node.value]
    )


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)


def read_bytes(path: Path, limit: int = MAX_DOCUMENT) -> bytes:
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    require(len(data) <= limit, f"File exceeds {limit} bytes: {path}")
    return data


def read_json(path: Path) -> Any:
    return json_loads(read_bytes(path).decode("utf-8", errors="strict"))


def read_yaml(path: Path) -> Any:
    # Reject aliases, including cyclic or exponentially expanding YAML documents.
    text = read_bytes(path).decode("utf-8", errors="strict")
    try:
        require(
            not any(isinstance(t, yaml.tokens.AliasToken) for t in yaml.scan(text)),
            "YAML aliases are unsupported",
        )
        return yaml.load(text, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise JebError(f"Invalid YAML in {path}: {exc}") from exc


def canonical(data: Any) -> bytes:
    return (
        json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(data: Any) -> str:
    return sha256(canonical(data))


def atomic_write(path: Path, data: bytes, *, replace: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.is_symlink(), f"Refusing symlink output: {path}")
    if path.exists():
        if read_bytes(path, max(MAX_DOCUMENT, len(data))) == data:
            return
        require(replace, f"Existing artifact differs; choose a new ID/path: {path}")
    handle, temporary = tempfile.mkstemp(prefix=".jeb-", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def write_json(path: Path, data: Any, *, replace: bool = True) -> None:
    atomic_write(path, canonical(data), replace=replace)


def inside(root: Path, relative: str | Path) -> Path:
    root = root.resolve()
    path = root / relative
    require(path.resolve().is_relative_to(root), f"Path escapes project: {relative}")
    current = path
    while current != root:
        require(not current.is_symlink(), f"Symlink path forbidden: {current}")
        current = current.parent
    return path


def identifier(value: str) -> str:
    require(bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,119}", value)), f"Unsafe ID: {value}")
    # Colons are legal in logical IDs, but never use these directly as filenames on Windows.
    return value


def file_id(value: str) -> str:
    identifier(value)
    require(":" not in value and ".." not in value, f"Unsafe filename ID: {value}")
    require(
        value.split(".")[0].upper()
        not in {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            *[f"COM{i}" for i in range(10)],
            *[f"LPT{i}" for i in range(10)],
        },
        f"Reserved Windows filename: {value}",
    )
    return value


def latin(text: str, context: str = "authored text") -> None:
    for char in text:
        category = unicodedata.category(char)
        require(not category.startswith("C") or char in "\n\t\r", f"Control character in {context}")
        require(
            not category.startswith("L") or "LATIN" in unicodedata.name(char, ""),
            f"Unsupported display-script character U+{ord(char):04X} in {context}",
        )


def latin_tree(value: Any, context: str = "authored metadata") -> None:
    if isinstance(value, str):
        latin(value, context)
    elif isinstance(value, dict):
        for key, item in value.items():
            latin(str(key), context)
            latin_tree(item, context)
    elif isinstance(value, list):
        for item in value:
            latin_tree(item, context)


def validate_schema(name: str, value: Any) -> None:
    schema = json_loads(files("jeb").joinpath(f"schemas/{name}.json").read_text("utf-8"))
    try:
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
            key=lambda e: str(list(e.absolute_path)),
        )
    except RecursionError as exc:
        raise JebError(f"Excessive nesting in {name}") from exc
    require(
        not errors,
        f"{name} schema: "
        + "; ".join(f"{'/'.join(map(str, e.absolute_path))}: {e.message}" for e in errors[:6]),
    )


class Project:
    def __init__(self, root: Path, *, synthetic: bool = False):
        self.root = root.resolve()
        self.edition = read_yaml(inside(self.root, "config/edition.yaml"))
        self.collection = read_yaml(inside(self.root, "config/collection.yaml"))
        validate_schema("edition", self.edition)
        validate_schema("collection", self.collection)
        require(
            tuple(self.collection["books"]) == BOOKS,
            "Collection must be exactly GEN, MAT, MRK, LUK, JHN in approved order",
        )
        self.synthetic = self.edition["corpus_kind"] == "synthetic"
        require(not self.synthetic or synthetic, "Synthetic workspace requires --synthetic")
        latin_tree(self.edition)
        latin_tree(self.collection)

    def path(self, relative: str | Path) -> Path:
        return inside(self.root, relative)

    def config(self, name: str) -> Any:
        value = read_yaml(self.path(f"config/{file_id(name)}.yaml"))
        latin_tree(value)
        return value

    def policy_hash(self) -> str:
        paths = [
            "docs/EDITORIAL_POLICY.md",
            "config/edition.yaml",
            "config/collection.yaml",
            "config/terminology.yaml",
            "config/name_registry.yaml",
            "config/modernization_rules.yaml",
        ]
        return digest({path: sha256(read_bytes(self.path(path))) for path in paths})
