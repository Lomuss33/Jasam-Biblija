"""Bounded artifact jobs, recoverable checkpoints and immutable local snapshots."""

from __future__ import annotations

import os
import re
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from time import monotonic
from uuid import UUID, uuid4

from jeb.core import (
    JebError,
    atomic_write,
    canonical,
    digest,
    json_loads,
    read_bytes,
    require,
    sha256,
    validate_schema,
)
from jeb.historical import (
    MAX_CANDIDATES,
    MAX_ENTITY_INDEX_BYTES,
    MAX_SOURCE_BYTES,
    artifact_path,
    binding_blockers,
    entity_dossiers,
    entity_groups,
    extract_artifact,
    load_layer,
    validate_layer,
)

LAYERS = ("registry", "index", "groups", "dossiers")
MAX_SNAPSHOT_BYTES = 128 * 1024 * 1024
MAX_RETAINED_PROJECTION_BYTES = 128 * 1024 * 1024


def workspace_path(workspace: Path, relative: str = "") -> Path:
    """Refuse links, junctions and path traversal for all managed writes/reads."""
    base = workspace.absolute()
    for current in (base, *base.parents):
        require(not current.is_symlink() and not current.is_junction(), "Linked pipeline workspace")
    target = base / relative
    require(target.resolve().is_relative_to(base.resolve()), "Pipeline path escapes workspace")
    current = target
    while current != base:
        require(not current.is_symlink() and not current.is_junction(), "Linked pipeline file")
        current = current.parent
    return target


def document(path: Path) -> dict:
    return json_loads(read_bytes(path, MAX_ENTITY_INDEX_BYTES).decode("utf-8", errors="strict"))


@contextmanager
def writer_lock(workspace: Path):
    with workspace_path(workspace, ".writer.lock").open("a+b") as stream:
        if stream.seek(0, 2) == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise JebError("Historical pipeline writer is busy") from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def load_checkpoint(workspace: Path, *, synthetic: bool) -> tuple[dict, dict]:
    state = document(workspace_path(workspace, "pipeline.json"))
    validate_schema("historical-pipeline-v1", state)
    require(not state["synthetic"] or synthetic, "Synthetic pipeline requires --synthetic")
    registry = load_layer("registry", workspace_path(workspace, "registry.json"))
    require(
        state["registry_sha256"] == digest(registry),
        "Pipeline registry changed; initialize a new workspace",
    )
    tasks = [task["artifact_id"] for task in state["tasks"]]
    require(
        len(tasks) == len(set(tasks))
        and set(tasks) == {item["id"] for item in registry["artifacts"]},
        "Pipeline task coverage differs from registry",
    )
    require(
        all(
            (task["cache_sha256"] is not None) == (task["status"] == "complete")
            for task in state["tasks"]
        ),
        "Pipeline task cache state differs",
    )
    return state, registry


def store_projection(workspace: Path, raw: bytes) -> dict:
    """Retain exact bytes without adopting or replacing a corrupt existing blob."""
    require(len(raw) <= MAX_SOURCE_BYTES, "Retained projection exceeds size limit")
    raw.decode("utf-8", errors="strict")
    descriptor = {"sha256": sha256(raw), "byte_length": len(raw)}
    path = workspace_path(workspace, f"projections/{descriptor['sha256']}.txt")
    if path.exists():
        require(read_bytes(path, MAX_SOURCE_BYTES) == raw, "Existing projection differs")
    else:
        atomic_write(path, raw, replace=False)
    return descriptor


def projection_text(workspace: Path, descriptor: dict) -> str:
    require(
        bool(re.fullmatch("[0-9a-f]{64}", descriptor["sha256"])),
        "Invalid projection hash",
    )
    raw = read_bytes(
        workspace_path(workspace, f"projections/{descriptor['sha256']}.txt"), MAX_SOURCE_BYTES
    )
    require(len(raw) == descriptor["byte_length"], "Projection byte length mismatch")
    require(sha256(raw) == descriptor["sha256"], "Projection checksum mismatch")
    return raw.decode("utf-8", errors="strict")


def extraction_cache(workspace: Path, cache_hash: str, artifact_id: str | None = None) -> dict:
    require(bool(re.fullmatch("[0-9a-f]{64}", cache_hash)), "Invalid extraction hash")
    raw = read_bytes(workspace_path(workspace, f"cache/{cache_hash}.json"), MAX_ENTITY_INDEX_BYTES)
    require(sha256(raw) == cache_hash, "Extraction checksum mismatch")
    result = json_loads(raw.decode("utf-8"))
    retained = isinstance(result, dict) and result.get("schema_version") == "2.0"
    validate_schema("historical-extraction-v2" if retained else "historical-extraction-v1", result)
    require(
        (artifact_id is None or result["artifact_id"] == artifact_id)
        and result["status"] == "complete"
        and result["provenance"] is not None,
        "Invalid extraction cache",
    )
    artifact_id = result["artifact_id"]
    require(result["provenance"]["artifact_id"] == artifact_id, "Extraction provenance mismatch")
    validate_layer(
        "index",
        {
            "schema_version": "1.0",
            "registry_sha256": "0" * 64,
            "candidates": result["candidates"],
            "pending": [],
        },
    )
    require(
        all(
            item["artifact_id"] == artifact_id
            and item["offset_space"] == result["provenance"]["projection"]
            for item in result["candidates"]
        ),
        "Extraction candidate mismatch",
    )
    if retained:
        descriptor = result["projection_file"]
        require(
            descriptor["sha256"] == result["provenance"]["projection_sha256"],
            "Projection reference differs from provenance",
        )
        text = projection_text(workspace, descriptor)
        require(
            all(
                text[item["start"] : item["end"]] == item["surface"]
                for item in result["candidates"]
            ),
            "Candidate differs from retained projection",
        )
    return result


def check_projection_budget(projections: dict, cached: dict, *, synthetic: bool) -> None:
    if cached.get("schema_version") == "2.0":
        require(synthetic, "Synthetic extraction in real pipeline")
        descriptor = cached["projection_file"]
        projections[descriptor["sha256"]] = descriptor["byte_length"]
        require(
            sum(projections.values()) <= MAX_RETAINED_PROJECTION_BYTES,
            "Snapshot retained projections exceed aggregate limit",
        )


def verify_projection(workspace: Path, cache_hash: str, *, synthetic: bool = False) -> dict:
    """Verify a retained historical cache without reading source files or using PDF tools."""
    state, registry = load_checkpoint(workspace, synthetic=synthetic)
    cached = extraction_cache(workspace, cache_hash)
    require(
        cached["artifact_id"] in {item["id"] for item in registry["artifacts"]},
        "Foreign extraction artifact",
    )
    retained = cached.get("schema_version") == "2.0"
    require(not retained or state["synthetic"], "Synthetic extraction in real pipeline")
    result = {
        "read_only": True,
        "synthetic": state["synthetic"],
        "releasable": False,
        "artifact_id": cached["artifact_id"],
        "cache_sha256": cache_hash,
        "projection_retained": retained,
        "provenance": cached["provenance"],
    }
    if not retained:
        return {**result, "error": "projection_not_retained"}
    return {
        **result,
        "projection_file": cached["projection_file"],
        "verified_candidates": len(cached["candidates"]),
        "locator_verification": "retained_projection",
    }


def load_published(workspace: Path, *, synthetic: bool) -> tuple[dict, dict, dict, dict]:
    """Pin one HEAD for both query results and their accompanying status."""
    state, _ = load_checkpoint(workspace, synthetic=synthetic)
    head = document(workspace_path(workspace, "HEAD.json"))
    require(
        isinstance(head, dict) and set(head) == {"snapshot_id", "manifest_sha256"},
        "Invalid pipeline HEAD",
    )
    snapshot_id = head["snapshot_id"]
    require(
        isinstance(snapshot_id, str) and str(UUID(snapshot_id)) == snapshot_id,
        "Invalid snapshot ID",
    )
    relative = f"snapshots/{snapshot_id}"
    raw = read_bytes(workspace_path(workspace, f"{relative}/manifest.json"))
    require(sha256(raw) == head["manifest_sha256"], "Snapshot manifest checksum mismatch")
    manifest = json_loads(raw.decode("utf-8"))
    validate_schema("historical-snapshot-v1", manifest)
    require(
        manifest["workspace_id"] == state["workspace_id"]
        and manifest["snapshot_id"] == snapshot_id
        and manifest["synthetic"] == state["synthetic"],
        "Foreign pipeline snapshot",
    )
    values, provenance = {}, {}
    total = 0
    for layer in LAYERS:
        raw = read_bytes(
            workspace_path(workspace, f"{relative}/{layer}.json"), MAX_ENTITY_INDEX_BYTES
        )
        total += len(raw)
        require(total <= MAX_SNAPSHOT_BYTES, "Snapshot exceeds aggregate limit")
        require(
            sha256(raw) == manifest["files"][f"{layer}.json"], "Snapshot file checksum mismatch"
        )
        values[layer] = json_loads(raw.decode("utf-8"))
        validate_layer(layer, values[layer])
    require(not binding_blockers(values), "Stale published pipeline")
    require(digest(values["registry"]) == state["registry_sha256"], "Foreign snapshot registry")
    cached_candidates, projections = [], {}
    for item in manifest["extractions"]:
        require(item["artifact_id"] not in provenance, "Duplicate snapshot extraction")
        cached = extraction_cache(workspace, item["cache_sha256"], item["artifact_id"])
        check_projection_budget(projections, cached, synthetic=state["synthetic"])
        retained = cached.get("schema_version") == "2.0"
        provenance[item["artifact_id"]] = {
            **cached["provenance"],
            "extraction_cache_sha256": item["cache_sha256"],
            "projection_retained": retained,
            "locator_verification": "retained_projection" if retained else "not_retained",
        }
        cached_candidates.extend(cached["candidates"])
    require(
        cached_candidates == values["index"]["candidates"],
        "Snapshot candidates differ from extraction cache",
    )
    pending_ids = {item["artifact_id"] for item in values["index"]["pending"]}
    require(
        not pending_ids.intersection(provenance)
        and pending_ids.union(provenance)
        == {item["id"] for item in values["registry"]["artifacts"]},
        "Snapshot artifact coverage differs",
    )
    require(
        all(item["artifact_id"] in provenance for item in values["index"]["candidates"]),
        "Snapshot lacks candidate provenance",
    )
    return state, values, provenance, manifest


def published_snapshot(workspace: Path, *, synthetic: bool) -> tuple[dict, dict, dict]:
    _, values, provenance, manifest = load_published(workspace, synthetic=synthetic)
    return values, provenance, manifest


def checkpoint(workspace: Path, state: dict) -> None:
    state["revision"] += 1
    validate_schema("historical-pipeline-v1", state)
    atomic_write(workspace_path(workspace, "pipeline.json"), canonical(state))


def publish(workspace: Path, state: dict, registry: dict) -> str:
    # Readers only see a fully written snapshot through one atomic HEAD update.
    current_head = workspace_path(workspace, "HEAD.json")
    if current_head.exists():
        _, _, current = published_snapshot(workspace, synthetic=state["synthetic"])
        if current["checkpoint_sha256"] == digest(state):
            return current["snapshot_id"]
    candidates, pending, extractions, projections = [], [], [], {}
    for task in state["tasks"]:
        if task["status"] == "complete":
            cached = extraction_cache(workspace, task["cache_sha256"], task["artifact_id"])
            check_projection_budget(projections, cached, synthetic=state["synthetic"])
            candidates.extend(cached["candidates"])
            extractions.append(
                {"artifact_id": task["artifact_id"], "cache_sha256": task["cache_sha256"]}
            )
        else:
            pending.append(
                {
                    "artifact_id": task["artifact_id"],
                    "status": "pending",
                    "reason": task["reason"] or task["status"],
                }
            )
        require(len(candidates) <= MAX_CANDIDATES, "Aggregate candidate limit exceeded")
    index = {
        "schema_version": "1.0",
        "registry_sha256": digest(registry),
        "candidates": candidates,
        "pending": pending,
    }
    validate_layer("index", index)
    groups = entity_groups(index)
    dossiers = entity_dossiers(registry, index, groups)
    values = {"registry": registry, "index": index, "groups": groups, "dossiers": dossiers}
    encoded = {name: canonical(value) for name, value in values.items()}
    require(
        all(len(raw) <= MAX_ENTITY_INDEX_BYTES for raw in encoded.values())
        and sum(map(len, encoded.values())) <= MAX_SNAPSHOT_BYTES,
        "Published layers exceed size limit",
    )
    snapshot_id = str(uuid4())
    location = workspace_path(workspace, f"snapshots/{snapshot_id}")
    location.mkdir()
    manifest = {
        "schema_version": "1.0",
        "snapshot_id": snapshot_id,
        "workspace_id": state["workspace_id"],
        "synthetic": state["synthetic"],
        "releasable": False,
        "checkpoint_sha256": digest(state),
        "files": {f"{name}.json": sha256(raw) for name, raw in encoded.items()},
        "extractions": extractions,
    }
    validate_schema("historical-snapshot-v1", manifest)
    for name, raw in encoded.items():
        atomic_write(
            workspace_path(workspace, f"snapshots/{snapshot_id}/{name}.json"), raw, replace=False
        )
    atomic_write(
        workspace_path(workspace, f"snapshots/{snapshot_id}/manifest.json"),
        canonical(manifest),
        replace=False,
    )
    atomic_write(
        current_head, canonical({"snapshot_id": snapshot_id, "manifest_sha256": digest(manifest)})
    )
    return snapshot_id


def initialize(
    registry_path: Path, input_root: Path, workspace: Path, *, synthetic: bool = False
) -> dict:
    registry = load_layer("registry", registry_path)
    require(input_root.is_dir(), "Input root is not a directory")
    require(len(registry["artifacts"]) <= 5000, "Pipeline artifact limit exceeded")
    workspace_path(workspace).mkdir()  # Exclusive; existing directories are never adopted.
    workspace_path(workspace, "cache").mkdir()
    workspace_path(workspace, "snapshots").mkdir()
    state = {
        "schema_version": "1.0",
        "record_type": "historical_pipeline",
        "workspace_id": str(uuid4()),
        "synthetic": synthetic,
        "releasable": False,
        "label": "SYNTHETIC - UNRELEASABLE" if synthetic else "PRIVATE RESEARCH - UNRELEASABLE",
        "input_root": str(input_root.resolve()),
        "registry_sha256": digest(registry),
        "revision": 0,
        "tasks": [
            {
                "artifact_id": item["id"],
                "status": "queued",
                "reason": None,
                "attempts": 0,
                "cache_sha256": None,
            }
            for item in registry["artifacts"]
        ],
    }
    with writer_lock(workspace):
        atomic_write(workspace_path(workspace, "registry.json"), canonical(registry), replace=False)
        checkpoint(workspace, state)
        publish(workspace, state, registry)
    return pipeline_status(workspace, synthetic=synthetic)


def pipeline_status(workspace: Path, *, synthetic: bool = False) -> dict:
    state, values, _, manifest = load_published(workspace, synthetic=synthetic)
    return summarize_checkpoint(state, values, manifest)


def summarize_checkpoint(state: dict, values: dict, manifest: dict) -> dict:
    counts = Counter(task["status"] for task in state["tasks"])
    return {
        "workspace_id": state["workspace_id"],
        "synthetic": state["synthetic"],
        "releasable": False,
        "label": state["label"],
        "revision": state["revision"],
        "snapshot_id": manifest["snapshot_id"],
        "publication_pending": manifest["checkpoint_sha256"] != digest(state),
        "queue": {
            key: counts[key]
            for key in ("queued", "processing", "complete", "pending", "needs_review")
        },
        "reasons": dict(Counter(task["reason"] for task in state["tasks"] if task["reason"])),
        "candidate_count": len(values["index"]["candidates"]),
        "dossier_count": len(values["dossiers"]["dossiers"]),
    }


def step(
    workspace: Path,
    *,
    synthetic: bool = False,
    max_artifacts: int = 4,
    max_seconds: float = 10,
    retry_pending: bool = False,
    refresh: bool = False,
) -> dict:
    require(1 <= max_artifacts <= 100 and 0 < max_seconds <= 60, "Invalid pipeline work budget")
    load_checkpoint(
        workspace, synthetic=synthetic
    )  # Reject foreign directories before creating a lock.
    with writer_lock(workspace):
        state, registry = load_checkpoint(workspace, synthetic=synthetic)
        artifacts = {item["id"]: item for item in registry["artifacts"]}
        deadline = monotonic() + max_seconds
        processed, reused = 0, 0
        # Queued work always precedes retries/refreshes; one blocked file cannot starve others.
        tasks = sorted(
            state["tasks"],
            key=lambda task: (
                0 if task["status"] == "processing" else 1 if task["status"] == "queued" else 2,
                task["attempts"],
            ),
        )
        for task in tasks:
            eligible = (
                task["status"] in {"queued", "processing"}
                or (retry_pending and task["status"] in {"pending", "needs_review"})
                or (refresh and task["status"] == "complete")
            )
            if not eligible:
                continue
            if processed >= max_artifacts or monotonic() >= deadline:
                break
            old_hash = task["cache_sha256"]
            reusable = None
            if old_hash and state["synthetic"]:
                old_cache = extraction_cache(workspace, old_hash, task["artifact_id"])
                artifact = artifacts[task["artifact_id"]]
                try:
                    path = artifact_path(Path(state["input_root"]), artifact.get("relative_path"))
                    if (
                        path
                        and path.suffix.lower() in {".txt", ".md"}
                        and old_cache["provenance"]["adapter"] == "utf8-verbatim-v1"
                        and sha256(read_bytes(path, MAX_SOURCE_BYTES))
                        == old_cache["provenance"]["source_sha256"]
                    ):
                        reusable = old_cache
                except (OSError, ValueError):
                    pass  # Let the extraction path record a stable per-artifact reason.
            task.update(status="processing", reason=None, cache_sha256=None)
            task["attempts"] += 1
            checkpoint(workspace, state)
            result = reusable or extract_artifact(
                artifacts[task["artifact_id"]],
                Path(state["input_root"]),
                synthetic=state["synthetic"],
                timeout=max(0.01, deadline - monotonic()),
                projection_sink=lambda raw: store_projection(workspace, raw),
            )
            cache_hash = None
            if result["status"] == "complete":
                validate_schema(
                    "historical-extraction-v2"
                    if result.get("schema_version") == "2.0"
                    else "historical-extraction-v1",
                    result,
                )
                cache_hash = digest(result)
                cache_path = workspace_path(workspace, f"cache/{cache_hash}.json")
                if cache_path.exists():
                    extraction_cache(workspace, cache_hash, task["artifact_id"])
                else:
                    atomic_write(cache_path, canonical(result), replace=False)
                reused += cache_hash == old_hash
            task.update(status=result["status"], reason=result["reason"], cache_sha256=cache_hash)
            checkpoint(workspace, state)
            processed += 1
        publish(workspace, state, registry)
    return {
        **pipeline_status(workspace, synthetic=synthetic),
        "processed": processed,
        "reused": reused,
    }
