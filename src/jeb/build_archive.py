"""Bounded local build-input ZIPs; never releases or general workspace backups."""

from __future__ import annotations

import io
import os
import re
import stat
import tempfile
import zipfile
from importlib.resources import files
from pathlib import Path, PurePosixPath

from jeb import __version__
from jeb.core import (
    Project,
    atomic_write,
    canonical,
    digest,
    file_id,
    inside,
    json_loads,
    latin_tree,
    native_path,
    read_bytes,
    read_json,
    require,
    sha256,
    validate_schema,
)
from jeb.corpus import ingest, load_corpus
from jeb.export import export, reader
from jeb.fetch import MAX_DOWNLOAD, MAX_EXPANDED, MAX_MEMBERS, archive_members
from jeb.knowledge import validate_knowledge
from jeb.knowledge_curation import read_receipts as curation_receipts
from jeb.knowledge_review import read_receipts as review_receipts
from jeb.review import all_decisions, heads
from jeb.sources import admitted, audit, registry

MAX_MANIFEST = 128 * 1024
REQUIRED = {
    "config/edition.yaml",
    "config/collection.yaml",
    "config/terminology.yaml",
    "config/name_registry.yaml",
    "config/modernization_rules.yaml",
    "docs/EDITORIAL_POLICY.md",
    "sources/registry.yaml",
    "sources/lock.json",
}
OPTIONAL = {
    "docs/RIGHTS_POLICY.md",
    "NOTICE.md",
    "LICENSES/MIT.txt",
    "LICENSES/CC0-1.0.txt",
    "LICENSES/README.md",
}
SAFE_ID = r"[A-Za-z0-9][A-Za-z0-9_.-]{0,119}"
HASH = r"[a-f0-9]{64}"


def engine_identity() -> str:
    def walk(resource, prefix=""):
        result = {}
        for child in resource.iterdir():
            name = prefix + child.name
            if child.is_dir() and child.name != "__pycache__":
                result.update(walk(child, name + "/"))
            elif child.name.endswith(".py") or (
                prefix == "schemas/" and child.name.endswith(".json")
            ):
                result[name] = sha256(child.read_bytes())
        return result

    return digest(walk(files("jeb")))


def _safe_path(name: str) -> None:
    path = PurePosixPath(name)
    require(
        name == path.as_posix() and not path.is_absolute() and len(path.parts) > 1,
        "Noncanonical archive input path",
    )
    for part in path.parts:
        file_id(part)
        require(not part.endswith((".", " ")), "Unsafe archive filename ending")


def _allowed(name: str, source_id: str) -> bool:
    _safe_path(name)
    if name in REQUIRED | OPTIONAL:
        return True
    patterns = (
        rf"sources/assessments/{SAFE_ID}\.json",
        rf"data/raw/{re.escape(source_id)}/{HASH}\.txt",
        rf"data/proposals/{SAFE_ID}\.json",
        rf"data/batches/{SAFE_ID}/input\.json",
        rf"data/approved/{SAFE_ID}\.json",
        rf"data/knowledge/{SAFE_ID}\.jsonl",
        rf"data/knowledge-reviews/{SAFE_ID}/{HASH}\.json",
        rf"data/knowledge-curation/{SAFE_ID}/{HASH}\.json",
    )
    return any(re.fullmatch(pattern, name) for pattern in patterns)


def _paths(project: Project, source_id: str) -> list[str]:
    _, lock = admitted(project, source_id)
    require(
        lock["format"] == "jeb-transcript-v1",
        "Build archives require the audited transcript adapter",
    )
    paths = set(REQUIRED)
    paths.update(path for path in OPTIONAL if native_path(project.path(path)).is_file())
    require(
        project.synthetic or "docs/RIGHTS_POLICY.md" in paths,
        "Historical build archive needs its project rights policy",
    )
    paths.add(f"data/raw/{source_id}/{lock['sha256']}.txt")
    for source in registry(project)["sources"]:
        path = f"sources/assessments/{file_id(source['source_id'])}.json"
        if native_path(project.path(path)).is_file():
            paths.add(path)
    for folder, pattern in (
        ("data/proposals", "*.json"),
        ("data/approved", "*.json"),
        ("data/knowledge", "*.jsonl"),
        ("data/knowledge-reviews", "*/*.json"),
        ("data/knowledge-curation", "*/*.json"),
    ):
        directory = native_path(project.path(folder))
        for path in directory.glob(pattern):
            relative = f"{folder}/{path.relative_to(directory).as_posix()}"
            project.path(relative)  # Recheck every file and parent, including symlinks.
            paths.add(relative)
    for relative in sorted(paths.copy()):
        if relative.startswith("data/proposals/"):
            proposal = read_json(project.path(relative))
            validate_schema("proposal", proposal)
            batch_id = file_id(proposal["response"]["batch_id"])
            packet = f"data/batches/{batch_id}/input.json"
            packet_value = read_json(project.path(packet))
            validate_schema("batch-packet", packet_value)
            require(
                packet_value["source_id"] == source_id,
                "Multiple-source proposal archives are not supported",
            )
            paths.add(packet)
    require(len(paths) < MAX_MEMBERS, "Too many build archive inputs")
    require(all(_allowed(path, source_id) for path in paths), "Unsupported build archive input")
    return sorted(paths)


def _proposal_history(project: Project) -> None:
    decisions = all_decisions(project)
    heads(decisions)
    directory = native_path(project.path("data/proposals"))
    proposals = {}
    for path in directory.glob("*.json"):
        proposal = read_json(project.path(f"data/proposals/{path.name}"))
        validate_schema("proposal", proposal)
        latin_tree(proposal)
        require(path.stem == proposal["proposal_id"], "Archived proposal filename/ID mismatch")
        response = proposal["response"]
        packet = read_json(project.path(f"data/batches/{file_id(response['batch_id'])}/input.json"))
        validate_schema("batch-packet", packet)
        latin_tree(packet)
        require(
            packet["batch_id"] == response["batch_id"]
            and packet["packet_sha256"]
            == digest({k: v for k, v in packet.items() if k != "packet_sha256"}),
            "Archived batch packet binding changed",
        )
        require(
            proposal["response_sha256"] == digest(response)
            and proposal["packet_sha256"] == response["packet_sha256"] == packet["packet_sha256"]
            and proposal["policy_sha256"] == packet["policy_sha256"],
            "Archived proposal/response/packet binding changed",
        )
        require(
            [i["segment_id"] for i in response["items"]] == packet["coverage_manifest"]
            and [i["segment_id"] for i in proposal["items"]] == packet["coverage_manifest"],
            "Archived proposal coverage changed",
        )
        proposals[proposal["proposal_id"]] = proposal
    for decision in decisions.values():
        require(decision["proposal_id"] in proposals, "Missing historical decision proposal")
        require(
            decision["proposal_sha256"] == digest(proposals[decision["proposal_id"]]),
            "Historical decision proposal hash changed",
        )


def _materialize(directory: Path, payloads: dict[str, bytes]) -> None:
    directory.mkdir(parents=True, exist_ok=False)
    for name, payload in sorted(payloads.items()):
        atomic_write(inside(directory, name), payload, replace=False)


def _rebuild(directory: Path, source_id: str, synthetic: bool) -> tuple[Project, dict]:
    project = Project(directory, synthetic=synthetic)
    audit(project)
    ingest(project, source_id, normalized=False)
    ingest(project, source_id, normalized=True)
    books = load_corpus(project, source_id)
    _proposal_history(project)
    knowledge = validate_knowledge(project, books)
    artifact = reader(project, source_id, "preview")
    markdown = export(project, source_id, "preview", "markdown", "exports/reader.md", "five-book")
    export(project, source_id, "preview", "json", "exports/reader.json", "five-book")
    return project, {
        "corpus_sha256": digest(books),
        "reader_sha256": digest(artifact),
        "markdown_sha256": markdown["sha256"],
        "policy_sha256": project.policy_hash(),
        "knowledge_records": len(knowledge),
        "text_decisions": len(all_decisions(project)),
        "review_receipts": len(review_receipts(project)),
        "curation_receipts": len(curation_receipts(project)),
    }


def _manifest_identity(manifest: dict, project: Project, identity: dict) -> None:
    require(
        project.edition["edition_id"] == manifest["edition_id"]
        and project.edition["corpus_kind"] == manifest["corpus_kind"],
        "Archive edition/corpus kind changed",
    )
    require(
        all(manifest["build"][key] == value for key, value in identity.items()),
        "Archive rebuilt corpus, reader or review identity differs",
    )


def _read(path: Path, synthetic: bool) -> tuple[dict, dict[str, bytes], str]:
    payload = read_bytes(path, MAX_DOWNLOAD)
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            require(
                all(not m.is_dir() and m.orig_filename == m.filename for m in archive.infolist()),
                "Archive directory entries or altered filenames are unsupported",
            )
    except zipfile.BadZipFile as exc:
        raise ValueError("Invalid build ZIP") from exc
    members = archive_members(payload)
    require(
        "manifest.json" in members and len(members["manifest.json"]) <= MAX_MANIFEST,
        "Missing or oversized build archive manifest",
    )
    manifest = json_loads(members.pop("manifest.json").decode("utf-8", errors="strict"))
    validate_schema("build-archive-manifest", manifest)
    latin_tree(manifest)
    file_id(manifest["archive_id"])
    file_id(manifest["source_id"])
    require(
        manifest["corpus_kind"] != "synthetic" or synthetic,
        "Synthetic archive requires --synthetic",
    )
    require(
        manifest["package_version"] == __version__
        and manifest["engine_sha256"] == engine_identity(),
        "Archive needs its exact compatible package/schema engine; no automatic migration",
    )
    paths = [entry["path"] for entry in manifest["files"]]
    require(
        paths == sorted(set(paths)) and len({p.casefold() for p in paths}) == len(paths),
        "Duplicate, reordered or filename-case archive inputs",
    )
    require(
        set(paths) == set(members) and REQUIRED <= set(paths),
        "Missing or unexpected archive members",
    )
    require(
        all(_allowed(path, manifest["source_id"]) for path in paths),
        "Archive input outside the build allowlist",
    )
    for entry in manifest["files"]:
        data = members[entry["path"]]
        require(
            len(data) == entry["size_bytes"] and sha256(data) == entry["sha256"],
            "Archive input size/checksum changed: " + entry["path"],
        )
    return manifest, members, sha256(payload)


def _validate_contents(directory: Path, manifest: dict, members: dict) -> tuple[Project, dict]:
    _materialize(directory, members)
    project, identity = _rebuild(
        directory, manifest["source_id"], manifest["corpus_kind"] == "synthetic"
    )
    require(
        set(_paths(project, manifest["source_id"])) == set(members),
        "Missing dependency or orphan build archive input",
    )
    _manifest_identity(manifest, project, identity)
    return project, identity


def create(project: Project, source_id: str, archive_id: str, output: str) -> dict:
    file_id(archive_id)
    require(Path(output).suffix.lower() == ".zip", "Build archive output must be a .zip file")
    # Validate the current live state before capturing an admitted source.
    expected_reader = digest(reader(project, source_id, "preview"))
    paths = _paths(project, source_id)
    members = {
        path: read_bytes(
            project.path(path), MAX_DOWNLOAD if path.startswith("data/raw/") else 8 * 1024 * 1024
        )
        for path in paths
    }
    require(
        sum(len(data) for data in members.values()) <= MAX_EXPANDED,
        "Build archive expanded size limit exceeded",
    )
    with tempfile.TemporaryDirectory(
        prefix="jeb-archive-", dir=native_path(Path(tempfile.gettempdir()))
    ) as temporary:
        stage = Path(temporary) / "workspace"
        _materialize(stage, members)
        rebuilt, identity = _rebuild(stage, source_id, project.synthetic)
        require(
            identity["reader_sha256"] == expected_reader,
            "Captured build inputs do not reproduce the current reader",
        )
        require(set(_paths(rebuilt, source_id)) == set(members), "Build dependency closure changed")
    manifest = {
        "schema_version": "1.0",
        "kind": "jeb-local-build-archive",
        "archive_id": archive_id,
        "source_id": source_id,
        "edition_id": project.edition["edition_id"],
        "corpus_kind": project.edition["corpus_kind"],
        "package_version": __version__,
        "engine_sha256": engine_identity(),
        "build": identity,
        "scope": "One admitted-source build snapshot; not a workspace backup or public release",
        "files": [
            {"path": path, "size_bytes": len(members[path]), "sha256": sha256(members[path])}
            for path in paths
        ],
    }
    validate_schema("build-archive-manifest", manifest)
    encoded = canonical(manifest)
    require(len(encoded) <= MAX_MANIFEST, "Build manifest exceeds 128 KiB")
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted({"manifest.json": encoded, **members}.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o600) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compresslevel=9)
    payload = stream.getvalue()
    require(len(payload) <= MAX_DOWNLOAD, "Build ZIP exceeds 32 MiB")
    atomic_write(project.path(output), payload, replace=False)
    return {
        "output": output,
        "archive_sha256": sha256(payload),
        "manifest_sha256": digest(manifest),
        "files": len(paths),
        "build": identity,
        "release": False,
    }


def validate(path: Path, *, synthetic: bool = False) -> dict:
    manifest, members, identity = _read(path, synthetic)
    with tempfile.TemporaryDirectory(
        prefix="jeb-validate-", dir=native_path(Path(tempfile.gettempdir()))
    ) as temporary:
        _validate_contents(Path(temporary) / "workspace", manifest, members)
    return {
        "valid": True,
        "archive_sha256": identity,
        "manifest_sha256": digest(manifest),
        "manifest": manifest,
        "release": False,
    }


def restore(root: Path, path: Path, destination: str, *, synthetic: bool = False) -> dict:
    root = root.resolve()
    require(native_path(root).is_dir(), "Restore root must be an existing directory")
    require(not Path(destination).is_absolute(), "Restore destination must be relative to --root")
    target = inside(root, destination)
    require(
        target != root and not os.path.lexists(native_path(target)),
        "Restore needs a new nonexistent destination; existing files are never merged",
    )
    manifest, members, identity = _read(path, synthetic)
    native_path(target.parent).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".jeb-restore-", dir=native_path(target.parent)
    ) as temporary:
        stage = Path(temporary) / "workspace"
        project, build = _validate_contents(stage, manifest, members)
        from jeb.search import build_index

        build_index(project, manifest["source_id"])
        require(
            not os.path.lexists(native_path(target)),
            "Restore destination appeared during validation; refusing to merge",
        )
        os.rename(native_path(stage), native_path(target))
    return {
        "output": destination,
        "archive_sha256": identity,
        "manifest_sha256": digest(manifest),
        "build": build,
        "exports_and_index_rebuilt": True,
        "release": False,
    }
