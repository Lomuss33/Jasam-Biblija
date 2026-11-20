"""Historical registry contracts and deterministic proposal builders."""

from __future__ import annotations

import re
import shutil
import subprocess
import unicodedata
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pathlib import Path
from time import monotonic

from jeb.core import (
    atomic_write,
    canonical,
    digest,
    json_loads,
    latin,
    latin_tree,
    read_bytes,
    read_json,
    require,
    sha256,
    validate_schema,
)

MAX_ENTITY_INDEX_BYTES = 64 * 1024 * 1024
MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_CANDIDATES = 100_000
MAX_ARTIFACT_CANDIDATES = 10_000
NORMALIZATION = "NFC + whitespace collapse + casefold; no transliteration"
LAYER_SCHEMAS = {
    "registry": "historical-registry-v1",
    "index": "historical-entity-index-v1",
    "groups": "historical-entity-groups-v1",
    "dossiers": "historical-entity-dossiers-v1",
}


def surface_key(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split()).casefold()


def unique_records(records: list[dict]) -> dict[str, dict]:
    result = {}
    for item in records:
        require(item["id"] not in result, "Duplicate historical record ID")
        result[item["id"]] = item
    return result


def validate_layer(name: str, value: dict) -> None:
    validate_schema(LAYER_SCHEMAS[name], value)
    if name == "registry":
        unique_records(
            [item for key in ("works", "editions", "artifacts", "relations") for item in value[key]]
        )
        for key, kind in (
            ("works", "work"),
            ("editions", "edition"),
            ("artifacts", "artifact"),
            ("relations", "relation"),
        ):
            for record in value[key]:
                validate_schema(f"historical-{kind}-v1", record)
                for field in ("title", "notes"):
                    if record.get(field):
                        latin(record[field], f"historical {field}")
                for field in (
                    "aliases",
                    "contributors",
                    "creators",
                    "publication",
                    "version_label",
                ):
                    if record.get(field):
                        latin_tree(record[field], f"historical {field}")
        works = unique_records(value["works"])
        editions = unique_records(value["editions"])
        require(all(item["work_id"] in works for item in value["editions"]), "Missing work")
        require(
            all(item["edition_id"] in editions for item in value["artifacts"]), "Missing edition"
        )
    elif name == "index":
        unique_records(value["candidates"])
        pending = [item["artifact_id"] for item in value["pending"]]
        require(len(set(pending)) == len(pending), "Duplicate pending artifact")
        require(
            not set(pending).intersection(item["artifact_id"] for item in value["candidates"]),
            "Pending artifact also has candidates",
        )
        for item in value["candidates"]:
            require(item["end"] - item["start"] == len(item["surface"]), "Invalid candidate range")
            require(
                item["evidence"]
                == {
                    "artifact_id": item["artifact_id"],
                    "projection": item["offset_space"],
                    "start": item["start"],
                    "end": item["end"],
                    "exact": item["surface"],
                },
                "Candidate evidence differs from locator",
            )
            latin(item["surface"], "candidate surface")
    elif name in ("groups", "dossiers"):
        for item in unique_records(value[name]).values():
            require(
                all(
                    surface_key(text) == item["normalized_key"] for text in item["surface_variants"]
                ),
                "Invalid surface normalization",
            )
            for text in item["surface_variants"]:
                latin(text, "surface variant")
            if name == "dossiers":
                require(
                    item["candidate_count"] == len(item["locators"]),
                    "Dossier count differs from locators",
                )
                require(
                    len({loc["candidate_id"] for loc in item["locators"]}) == len(item["locators"]),
                    "Duplicate dossier locator",
                )
                require(
                    all(loc["end"] - loc["start"] == len(loc["exact"]) for loc in item["locators"]),
                    "Invalid dossier range",
                )


def load_layer(name: str, path: Path) -> dict:
    value = json_loads(read_bytes(path, MAX_ENTITY_INDEX_BYTES).decode("utf-8", errors="strict"))
    validate_layer(name, value)
    return value


def binding_blockers(values: dict[str, dict]) -> list[dict]:
    checks = (
        ("index", "registry_sha256", "registry"),
        ("groups", "index_sha256", "index"),
        ("dossiers", "index_sha256", "index"),
        ("dossiers", "groups_sha256", "groups"),
    )
    return [
        {"layer": child, "reason": "stale_hash", "field": field}
        for child, field, parent in checks
        if child in values and parent in values and values[child][field] != digest(values[parent])
    ]


def _status(value: str | None) -> str:
    return (
        value if value in {"candidate", "identified", "needs_review", "confirmed"} else "candidate"
    )


def build_registry(catalog_path: Path, output: Path) -> dict:
    catalog = read_json(catalog_path)
    books = catalog.get("books")
    if not isinstance(books, list):
        raise ValueError("Library catalog must contain a books array")
    works, editions, artifacts, relations = [], [], [], []
    for book in books:
        work_id = book["id"]
        work = {
            "schema_version": "1.0",
            "id": work_id,
            "record_type": "work",
            "title": book["title"],
            "aliases": [],
            "status": _status(book.get("status")),
            "notes": f"Group: {book.get('group', '')}. Request: {book.get('request', '')}",
        }
        validate_schema("historical-work-v1", work)
        works.append(work)
        for finding in book.get("findings", []):
            finding_id = finding["id"]
            edition_id = f"edition-{finding_id}"
            artifact_id = f"artifact-{finding_id}"
            translator = finding.get("translator")
            publication = {"publisher": finding.get("publisher"), "year": finding.get("year")}
            publication = {key: value for key, value in publication.items() if value is not None}
            edition = {
                "schema_version": "1.0",
                "id": edition_id,
                "record_type": "edition",
                "work_id": work_id,
                "title": finding["edition_title"],
                "creators": [],
                "contributors": [translator] if translator else [],
                "publication": publication,
                "language": finding.get("language") or "unknown",
                "status": "identified",
                "rights_status": "needs_review",
                "notes": finding.get("rights", ""),
            }
            artifact_type = (
                "web_capture"
                if finding.get("access") in {"online_reading", "publisher_preview"}
                else "metadata_only"
            )
            artifact = {
                "schema_version": "1.0",
                "id": artifact_id,
                "record_type": "artifact",
                "edition_id": edition_id,
                "artifact_type": artifact_type,
                "uri": finding.get("url"),
                "relative_path": finding.get("local_file"),
                "sha256": None,
                "status": "private" if finding.get("local_file") else "discovered",
                "notes": finding.get("coverage", ""),
            }
            relation = {
                "schema_version": "1.0",
                "id": f"relation-{finding_id}",
                "record_type": "relation",
                "from_id": edition_id,
                "to_id": work_id,
                "relation": "version_of",
                "status": "supported",
                "confidence": "medium",
                "evidence": [{"kind": "external_reference", "value": finding_id}],
            }
            validate_schema("historical-edition-v1", edition)
            validate_schema("historical-artifact-v1", artifact)
            validate_schema("historical-relation-v1", relation)
            editions.append(edition)
            artifacts.append(artifact)
            relations.append(relation)
    result = {
        "schema_version": "1.0",
        "source_catalog": {"path": str(catalog_path), "sha256": sha256(canonical(catalog))},
        "works": works,
        "editions": editions,
        "artifacts": artifacts,
        "relations": relations,
    }
    validate_layer("registry", result)
    atomic_write(output, canonical(result), replace=False)
    return {
        "output": str(output),
        "works": len(works),
        "editions": len(editions),
        "artifacts": len(artifacts),
        "relations": len(relations),
        "metadata_only": True,
    }


def artifact_path(root: Path, relative: str | None) -> Path | None:
    if not relative:
        return None
    root = root.resolve()
    require(
        not Path(relative).drive
        and not Path(relative).root
        and all(part not in {".", ".."} and ":" not in part for part in Path(relative).parts),
        "Unsafe artifact path",
    )
    path = root / relative
    require(
        not Path(relative).is_absolute() and path.resolve().is_relative_to(root),
        "Artifact path escapes input root",
    )
    current = path
    while current != root:
        require(not current.is_symlink() and not current.is_junction(), "Linked artifact path")
        current = current.parent
    return path


def pdf_projection(path: Path, timeout: float, *, executable: str | None = None) -> bytes:
    executable = executable or shutil.which("pdftotext")
    require(executable is not None, "pdf_adapter_unavailable")
    deadline = monotonic() + timeout
    with subprocess.Popen(
        [executable, "-enc", "UTF-8", str(path), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ) as process:
        with ThreadPoolExecutor(max_workers=1) as pool:
            reader = pool.submit(process.stdout.read, MAX_SOURCE_BYTES + 1)
            try:
                raw = reader.result(timeout=max(0.001, deadline - monotonic()))
                require(len(raw) <= MAX_SOURCE_BYTES, "projection_too_large")
                require(
                    process.wait(timeout=max(0.001, deadline - monotonic())) == 0,
                    "pdf_projection_failed",
                )
                return raw
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()


def candidate_spans(
    artifact_id: str, text: str, projection: str, source_hash: str, projection_hash: str
) -> list[dict]:
    # Capitalized Latin tokens are deliberately unknown candidates, not NER labels.
    token = r"[^\W\d_][\w\u0300-\u036f'-]*"
    pattern = re.compile(rf"\b{token}(?:[ \t]+{token}){{0,2}}")
    candidates = []
    for match in pattern.finditer(text):
        # Split a greedy run so lowercase words do not consume following names.
        for word in re.finditer(token, match.group(0)):
            surface = word.group(0)
            if not surface[0].isupper() or len(surface) < 3:
                continue
            if any(
                unicodedata.category(char).startswith("L")
                and "LATIN" not in unicodedata.name(char, "")
                for char in surface
            ):
                continue
            require(len(surface) <= 500, "candidate_surface_too_long")
            start = match.start() + word.start()
            end = start + len(surface)
            identity_parts = [artifact_id, source_hash, projection, start, end]
            if projection == "pdftotext_utf8":
                identity_parts.append(projection_hash)
            identity = digest(identity_parts)[:32]
            candidates.append(
                {
                    "schema_version": "1.0",
                    "id": f"entity-candidate-{identity}",
                    "record_type": "entity_candidate",
                    "artifact_id": artifact_id,
                    "entity_type": "unknown",
                    "surface": surface,
                    "start": start,
                    "end": end,
                    "offset_space": projection,
                    "status": "proposed",
                    "evidence": {
                        "artifact_id": artifact_id,
                        "projection": projection,
                        "start": start,
                        "end": end,
                        "exact": surface,
                    },
                }
            )
            require(len(candidates) <= MAX_ARTIFACT_CANDIDATES, "candidate_limit_exceeded")
    return candidates


def extract_artifact(
    artifact: dict,
    root: Path,
    *,
    synthetic: bool,
    timeout: float = 10,
    projection_sink: Callable[[bytes], dict] | None = None,
) -> dict:
    result = {
        "artifact_id": artifact["id"],
        "status": "pending",
        "reason": None,
        "candidates": [],
        "provenance": None,
    }
    if not synthetic:
        result.update(status="needs_review", reason="source_review_required")
        return result
    try:
        path = artifact_path(root, artifact.get("relative_path"))
        if path is None:
            result["reason"] = "no_local_text"
            return result
        if not path.is_file():
            result["reason"] = "local_artifact_unavailable"
            return result
        if artifact["status"] in {"rejected", "stale"}:
            result.update(status="needs_review", reason="artifact_not_eligible")
            return result
        raw = read_bytes(path, MAX_SOURCE_BYTES)
        source_hash = sha256(raw)
        if artifact.get("sha256") and artifact["sha256"] != source_hash:
            result.update(status="needs_review", reason="source_hash_mismatch")
            return result
        if path.suffix.lower() in {".txt", ".md"}:
            projection = "source_utf8"
            projected = raw
            adapter = "utf8-verbatim-v1"
        elif path.suffix.lower() == ".pdf":
            executable = shutil.which("pdftotext")
            if not executable:
                result["reason"] = "pdf_adapter_unavailable"
                return result
            adapter_hash = sha256(read_bytes(Path(executable), 64 * 1024 * 1024))
            projected = pdf_projection(path, timeout, executable=executable)
            require(len(projected) <= MAX_SOURCE_BYTES, "projection_too_large")
            require(
                sha256(read_bytes(path, MAX_SOURCE_BYTES)) == source_hash,
                "source_changed_during_projection",
            )
            require(
                sha256(read_bytes(Path(executable), 64 * 1024 * 1024)) == adapter_hash,
                "adapter_changed_during_projection",
            )
            projection = "pdftotext_utf8"
            adapter = "pdftotext:" + adapter_hash
        else:
            result["reason"] = "unsupported_text_format"
            return result
        text = projected.decode("utf-8", errors="strict")
        candidates = candidate_spans(
            artifact["id"], text, projection, source_hash, sha256(projected)
        )
        result.update(
            status="complete",
            candidates=candidates,
            provenance={
                "artifact_id": artifact["id"],
                "source_sha256": source_hash,
                "projection_sha256": sha256(projected),
                "projection": projection,
                "offset_unit": "unicode_code_points",
                "adapter": adapter,
            },
        )
    except UnicodeError:
        result.update(status="needs_review", reason="invalid_utf8")
    except (TimeoutError, subprocess.TimeoutExpired):
        result.update(status="needs_review", reason="extraction_timeout")
    except OSError:
        result.update(status="needs_review", reason="source_unreadable")
    except (ValueError, subprocess.SubprocessError) as exc:
        reason = str(exc)
        known = {
            "projection_too_large",
            "pdf_projection_failed",
            "source_changed_during_projection",
            "adapter_changed_during_projection",
            "candidate_limit_exceeded",
            "candidate_surface_too_long",
        }
        result.update(
            status="needs_review",
            reason=reason
            if reason in known
            else "source_too_large"
            if reason.startswith("File exceeds ")
            else "extraction_failed",
        )
    # Retention is a workspace write, not a source-read failure. Propagate failures
    # so the processing checkpoint can resume and the prior HEAD stays readable.
    if (
        result["status"] == "complete"
        and result["provenance"]["projection"] == "pdftotext_utf8"
        and projection_sink is not None
    ):
        result = {
            **result,
            "schema_version": "2.0",
            "record_type": "historical_extraction",
            "synthetic": True,
            "releasable": False,
            "projection_file": projection_sink(projected),
        }
    return result


def build_entity_index(
    registry_path: Path, root: Path, output: Path, *, synthetic: bool = False
) -> dict:
    registry = load_layer("registry", registry_path)
    candidates, pending = [], []
    for artifact in registry["artifacts"]:
        extraction = extract_artifact(artifact, root, synthetic=synthetic)
        candidates.extend(extraction["candidates"])
        require(len(candidates) <= MAX_CANDIDATES, "Total candidate limit exceeded")
        if extraction["status"] != "complete":
            pending.append(
                {"artifact_id": artifact["id"], "status": "pending", "reason": extraction["reason"]}
            )
    result = {
        "schema_version": "1.0",
        "registry_sha256": sha256(canonical(registry)),
        "candidates": candidates,
        "pending": pending,
    }
    validate_layer("index", result)
    atomic_write(output, canonical(result), replace=False)
    return {
        "output": str(output),
        "candidates": len(candidates),
        "pending_artifacts": len(pending),
        "proposals_only": True,
    }


def build_entity_groups(index_path: Path, output: Path) -> dict:
    index = load_layer("index", index_path)
    result = entity_groups(index)
    atomic_write(output, canonical(result), replace=False)
    return {"output": str(output), "groups": len(result["groups"]), "merge_authority": False}


def entity_groups(index: dict) -> dict:
    groups = {}
    for candidate in index["candidates"]:
        key = surface_key(candidate["surface"])
        groups.setdefault(key, {"surface_variants": [], "candidate_ids": [], "artifact_ids": []})
        group = groups[key]
        if candidate["surface"] not in group["surface_variants"]:
            group["surface_variants"].append(candidate["surface"])
        group["candidate_ids"].append(candidate["id"])
        if candidate["artifact_id"] not in group["artifact_ids"]:
            group["artifact_ids"].append(candidate["artifact_id"])
    result = {
        "schema_version": "1.0",
        "index_sha256": sha256(canonical(index)),
        "normalization": NORMALIZATION,
        "groups": [
            {
                "id": f"entity-group-{sha256(key.encode('utf-8'))[:32]}",
                "normalized_key": key,
                "status": "proposed_same_surface",
                **value,
            }
            for key, value in sorted(groups.items())
        ],
    }
    validate_layer("groups", result)
    return result


def build_entity_dossiers(
    registry_path: Path, index_path: Path, groups_path: Path, output: Path
) -> dict:
    registry = load_layer("registry", registry_path)
    index = load_layer("index", index_path)
    groups = load_layer("groups", groups_path)
    require(
        not binding_blockers({"registry": registry, "index": index, "groups": groups}),
        "Stale historical inputs",
    )
    result = entity_dossiers(registry, index, groups)
    atomic_write(output, canonical(result), replace=False)
    return {"output": str(output), "dossiers": len(result["dossiers"]), "proposed_only": True}


def entity_dossiers(registry: dict, index: dict, groups: dict) -> dict:
    artifacts = {item["id"]: item for item in registry["artifacts"]}
    editions = {item["id"]: item for item in registry["editions"]}
    works = {item["id"]: item for item in registry["works"]}
    candidates = {item["id"]: item for item in index["candidates"]}
    require(
        all(item["artifact_id"] in artifacts for item in index["pending"]),
        "Unknown pending artifact",
    )
    require(
        all(item["artifact_id"] in artifacts for item in candidates.values()),
        "Unknown candidate artifact",
    )
    grouped = [candidate for group in groups["groups"] for candidate in group["candidate_ids"]]
    require(
        len(grouped) == len(candidates) and set(grouped) == set(candidates),
        "Groups must cover every candidate exactly once",
    )
    dossiers = []
    for group in groups["groups"]:
        members = [candidates[candidate_id] for candidate_id in group["candidate_ids"]]
        require(
            set(group["artifact_ids"]) == {item["artifact_id"] for item in members},
            "Group artifact membership differs",
        )
        require(
            set(group["surface_variants"]) == {item["surface"] for item in members},
            "Group surface membership differs",
        )
        locators = []
        sources = {}
        for candidate_id in group["candidate_ids"]:
            candidate = candidates[candidate_id]
            require(
                surface_key(candidate["surface"]) == group["normalized_key"],
                "Group mixes different surfaces",
            )
            artifact = artifacts[candidate["artifact_id"]]
            edition = editions.get(artifact["edition_id"])
            work = works.get(edition["work_id"]) if edition else None
            source = {
                "artifact_id": artifact["id"],
                "artifact_status": artifact["status"],
                "edition_id": edition["id"] if edition else None,
                "edition_title": edition["title"] if edition else None,
                "work_id": work["id"] if work else None,
                "work_title": work["title"] if work else None,
            }
            sources[artifact["id"]] = source
            locators.append(
                {
                    "candidate_id": candidate["id"],
                    "artifact_id": candidate["artifact_id"],
                    "projection": candidate["offset_space"],
                    "start": candidate["start"],
                    "end": candidate["end"],
                    "exact": candidate["surface"],
                }
            )
        dossiers.append(
            {
                "id": group["id"],
                "record_type": "entity_dossier",
                "status": "proposed",
                "normalized_key": group["normalized_key"],
                "surface_variants": group["surface_variants"],
                "candidate_count": len(group["candidate_ids"]),
                "sources": list(sources.values()),
                "locators": locators,
            }
        )
    result = {
        "schema_version": "1.0",
        "groups_sha256": sha256(canonical(groups)),
        "index_sha256": sha256(canonical(index)),
        "dossiers": dossiers,
    }
    validate_layer("dossiers", result)
    return result


def inspect_pipeline(
    registry_path: Path | None,
    index_path: Path | None,
    groups_path: Path | None,
    dossiers_path: Path | None,
) -> dict:
    """Backward-compatible Python entry point for the shared query contract."""
    from jeb.historical_query import inspect

    return inspect(
        {
            "registry": registry_path,
            "index": index_path,
            "groups": groups_path,
            "dossiers": dossiers_path,
        }
    )
