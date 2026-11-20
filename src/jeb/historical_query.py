"""Shared read-only CLI/API inspection and source-scoped dossier queries."""

from __future__ import annotations

from pathlib import Path

from jeb.core import canonical, digest, require
from jeb.historical import (
    LAYER_SCHEMAS,
    binding_blockers,
    entity_dossiers,
    load_layer,
    surface_key,
)

MAX_RESPONSE_BYTES = 4 * 1024 * 1024


def load_inputs(
    paths: dict[str, Path | None], *, workspace: Path | None = None, synthetic: bool = False
) -> tuple[dict, dict, dict, dict]:
    values, provenance, snapshot = {}, {}, {}
    configured = {layer: bool(paths.get(layer)) for layer in LAYER_SCHEMAS}
    blockers = []
    if workspace is not None:
        if any(configured.values()):
            return (
                {},
                {},
                {
                    "enabled": False,
                    "read_only": True,
                    "configured": configured,
                    "counts": {},
                    "blockers": [{"layer": "pipeline", "reason": "configuration_conflict"}],
                    "status": "blocked",
                },
                {},
            )
        from jeb.historical_pipeline import load_published, summarize_checkpoint

        try:
            state, values, provenance, manifest = load_published(workspace, synthetic=synthetic)
            snapshot = {
                "snapshot_id": manifest["snapshot_id"],
                "synthetic": manifest["synthetic"],
                "releasable": False,
                "pipeline": summarize_checkpoint(state, values, manifest),
            }
            configured = dict.fromkeys(LAYER_SCHEMAS, True)
        except (OSError, ValueError, UnicodeError):
            blockers.append({"layer": "pipeline", "reason": "invalid_workspace"})
    else:
        for layer in LAYER_SCHEMAS:
            path = paths.get(layer)
            if path is None:
                blockers.append({"layer": layer, "reason": "path_not_configured"})
                continue
            try:
                values[layer] = load_layer(layer, path)
            except UnicodeError:
                blockers.append({"layer": layer, "reason": "invalid_json"})
            except OSError:
                blockers.append({"layer": layer, "reason": "unreadable_input"})
            except ValueError as exc:
                reason = "invalid_schema" if "schema:" in str(exc) else "invalid_json"
                blockers.append({"layer": layer, "reason": reason})
    blockers.extend(binding_blockers(values))
    if not any(item["reason"] != "path_not_configured" for item in blockers):
        try:
            if all(key in values for key in ("registry", "index", "groups")):
                expected = entity_dossiers(values["registry"], values["index"], values["groups"])
                if "dossiers" in values:
                    require(
                        expected == values["dossiers"],
                        "Dossier projection differs from upstream layers",
                    )
            elif "registry" in values and "index" in values:
                artifacts = {item["id"] for item in values["registry"]["artifacts"]}
                require(
                    all(
                        item["artifact_id"] in artifacts
                        for item in values["index"]["candidates"] + values["index"]["pending"]
                    ),
                    "Foreign artifact",
                )
        except (KeyError, ValueError):
            blockers.append({"layer": "pipeline", "reason": "inconsistent_layers"})
    counts = {}
    for layer, fields in {
        "registry": ("works", "editions", "artifacts", "relations"),
        "index": ("candidates", "pending"),
        "groups": ("groups",),
        "dossiers": ("dossiers",),
    }.items():
        if layer in values:
            counts[layer] = {field: len(values[layer][field]) for field in fields}
    status = {
        "enabled": bool(values),
        "read_only": True,
        "configured": configured,
        "counts": counts,
        "blockers": blockers,
        "status": "blocked" if blockers else "ready",
        **snapshot,
    }
    return values, provenance, status, snapshot


def inspect(
    paths: dict[str, Path | None], *, workspace: Path | None = None, synthetic: bool = False
) -> dict:
    return load_inputs(paths, workspace=workspace, synthetic=synthetic)[2]


def page(items: list, limit: int, offset: int) -> dict:
    return {
        "total": len(items),
        "limit": limit,
        "offset": offset,
        "truncated": offset + limit < len(items),
        "results": items[offset : offset + limit],
    }


def summary(dossier: dict) -> dict:
    works = {
        source["work_id"]: {"id": source["work_id"], "title": source["work_title"]}
        for source in dossier["sources"]
        if source["work_id"]
    }
    return {
        key: dossier[key]
        for key in (
            "id",
            "record_type",
            "status",
            "normalized_key",
            "surface_variants",
            "candidate_count",
        )
    } | {
        "source_count": len(dossier["sources"]),
        "locator_count": len(dossier["locators"]),
        "works": list(works.values())[:100],
        "works_total": len(works),
        "artifact_statuses": sorted({source["artifact_status"] for source in dossier["sources"]}),
    }


def matches(text: str, query: str) -> bool:
    return surface_key(query) in surface_key(text)


def work_ids(registry: dict | None, text: str) -> set[str]:
    if not registry or not text:
        return set()
    return {
        work["id"]
        for work in registry["works"]
        if any(matches(value, text) for value in [work["id"], work["title"], *work["aliases"]])
    }


def select_dossiers(dossiers: list[dict], registry: dict | None, params: dict) -> list[dict]:
    query, work = params.get("q", ""), params.get("work", "")
    query_works = work_ids(registry, query)
    result = []
    for dossier in dossiers:
        if params.get("status") and dossier["status"] != params["status"]:
            continue
        if params.get("availability") and not any(
            source["artifact_status"] == params["availability"] for source in dossier["sources"]
        ):
            continue
        if work and not any(
            any(matches(value or "", work) for value in (source["work_id"], source["work_title"]))
            for source in dossier["sources"]
        ):
            continue
        if (
            query
            and not any(
                matches(value, query)
                for value in [dossier["normalized_key"], *dossier["surface_variants"]]
            )
            and not any(source["work_id"] in query_works for source in dossier["sources"])
        ):
            continue
        result.append(dossier)
    return sorted(result, key=lambda item: (item["normalized_key"], item["id"]))


def scoped_dossier(dossier: dict, params: dict) -> dict:
    sources = [
        source
        for source in dossier["sources"]
        if (
            not params.get("work")
            or any(
                matches(value or "", params["work"])
                for value in (source["work_id"], source["work_title"])
            )
        )
        and (not params.get("availability") or source["artifact_status"] == params["availability"])
    ]
    artifacts = {source["artifact_id"] for source in sources}
    locators = [locator for locator in dossier["locators"] if locator["artifact_id"] in artifacts]
    return {**dossier, "sources": sources, "locators": locators, "candidate_count": len(locators)}


def detail(dossier: dict, registry: dict | None, provenance: dict, params: dict) -> dict:
    edition_map = {item["id"]: item for item in (registry or {}).get("editions", [])}
    sources = []
    for source in dossier["sources"][:50]:
        edition = edition_map.get(source["edition_id"], {})
        sources.append(
            {
                **source,
                "contributors": edition.get("contributors", []),
                "creators": edition.get("creators", []),
                "publication": edition.get("publication", {}),
                "language": edition.get("language"),
                "rights_status": edition.get("rights_status", "unknown"),
                **provenance.get(source["artifact_id"], {}),
            }
        )
    count = min(int(params.get("locator_limit", 20)), 100)
    offset = int(params.get("locator_offset", 0))
    locators = [
        {**loc, "offset_unit": "unicode_code_points", **provenance.get(loc["artifact_id"], {})}
        for loc in dossier["locators"][offset : offset + count]
    ]
    return {
        **summary(dossier),
        "sources": sources,
        "sources_truncated": len(sources) < len(dossier["sources"]),
        "locators": locators,
        "locator_offset": offset,
        "locator_limit": count,
        "locators_total": len(dossier["locators"]),
        "locators_truncated": offset + len(locators) < len(dossier["locators"]),
    }


def relation_results(
    registry: dict | None, params: dict, *, context_works: set[str] | None = None
) -> list[dict]:
    if registry is None:
        return []
    records = {
        item["id"]: item for key in ("works", "editions", "artifacts") for item in registry[key]
    }

    def endpoint_work(record_id: str) -> str | None:
        item = records.get(record_id, {})
        if item.get("record_type") == "artifact":
            item = records[item["edition_id"]]
        return item.get("work_id") or (
            item.get("id") if item.get("record_type") == "work" else None
        )

    selected = []
    requested = work_ids(registry, params.get("work", ""))
    for item in registry["relations"]:
        if params.get("relation") and item["relation"] != params["relation"]:
            continue
        if params.get("status") and item["status"] != params["status"]:
            continue
        endpoints = {endpoint_work(item["from_id"]), endpoint_work(item["to_id"])}
        text = " ".join(
            [
                item["id"],
                item["from_id"],
                item["to_id"],
                records.get(item["from_id"], {}).get("title", ""),
                records.get(item["to_id"], {}).get("title", ""),
            ]
        )
        if params.get("work") and not endpoints & requested:
            continue
        if context_works is not None:
            if not endpoints & context_works:
                continue
        elif params.get("q") and not matches(text, params["q"]):
            continue
        selected.append(
            {
                **item,
                "from_title": records.get(item["from_id"], {}).get("title"),
                "to_title": records.get(item["to_id"], {}).get("title"),
                "evidence_count": len(item["evidence"]),
                "authoritative": False,
                "selection_basis": "work_context" if context_works is not None else "query",
            }
        )
    return sorted(selected, key=lambda item: item["id"])


def query(
    operation: str,
    paths: dict[str, Path | None],
    params: dict | None = None,
    *,
    workspace: Path | None = None,
    synthetic: bool = False,
) -> dict:
    params = params or {}
    base = {"proposal_only": True, "authoritative": False, "releasable": False}
    try:
        for key in ("q", "work", "status", "availability", "relation", "id"):
            require(
                isinstance(params.get(key, ""), str) and len(params.get(key, "")) <= 500,
                "Invalid query value",
            )
        maxima = {"dossiers": 1000, "lookup": 100, "relations": 500, "dossier": 100, "detail": 100}
        maximum = maxima[operation]
        limit, offset = min(int(params.get("limit", 100)), maximum), int(params.get("offset", 0))
        require(limit >= 1 and 0 <= offset <= 100_000, "Invalid pagination")
        require(
            1 <= int(params.get("locator_limit", 20)) <= 100
            and 0 <= int(params.get("locator_offset", 0)) <= 100_000,
            "Invalid locator pagination",
        )
        if operation == "dossier":
            require(
                bool(params.get("q", "").strip() or params.get("work", "").strip()),
                "A topic or work is required",
            )
    except (KeyError, TypeError, ValueError):
        return {**base, "enabled": False, "error": "invalid_query"}
    values, provenance, status, snapshot = load_inputs(
        paths, workspace=workspace, synthetic=synthetic
    )
    invalid = [
        blocker for blocker in status["blockers"] if blocker["reason"] != "path_not_configured"
    ]
    if invalid:
        return {
            **base,
            "enabled": False,
            "error": "stale_pipeline_inputs"
            if any(item["reason"] == "stale_hash" for item in invalid)
            else "invalid_historical_input",
            "layer": invalid[0]["layer"],
            "blockers": invalid,
            "entities": [],
            "relations": [],
            "results": [],
        }
    registry = values.get("registry")
    dossiers = values.get("dossiers", {}).get("dossiers", [])
    selected = [
        scoped_dossier(item, params) for item in select_dossiers(dossiers, registry, params)
    ]
    selected = [item for item in selected if item["locators"]]
    base |= {
        "enabled": bool(values),
        "query": params.get("q", ""),
        "work": params.get("work", ""),
        "integrity": "verified" if not status["blockers"] else "partial",
        "unavailable_layers": [item["layer"] for item in status["blockers"]],
        **snapshot,
    }
    if operation == "dossiers":
        result = {**base, **page([summary(item) for item in selected], limit, offset)}
    elif operation == "detail":
        item = next((item for item in selected if item["id"] == params.get("id")), None)
        result = (
            {**base, **detail(item, registry, provenance, params)}
            if item
            else {**base, "error": "not_found"}
        )
    elif operation == "lookup":
        by_work = {}
        for item in selected:
            for work_id in sorted(
                {source["work_id"] for source in item["sources"] if source["work_id"]}
            ):
                work_sources = [
                    source for source in item["sources"] if source["work_id"] == work_id
                ]
                artifact_ids = {source["artifact_id"] for source in work_sources}
                entry = by_work.setdefault(
                    work_id,
                    {
                        "work_id": work_id,
                        "work_title": work_sources[0]["work_title"],
                        "dossier_ids": [],
                        "candidate_count": 0,
                        "locator_count": 0,
                    },
                )
                entry["dossier_ids"].append(item["id"])
                count = sum(loc["artifact_id"] in artifact_ids for loc in item["locators"])
                entry["candidate_count"] += count
                entry["locator_count"] += count
        for item in by_work.values():
            item["dossier_total"] = len(item["dossier_ids"])
            item["dossier_ids"] = item["dossier_ids"][:100]
        result = {**base, **page([by_work[key] for key in sorted(by_work)], limit, offset)}
    elif operation == "relations":
        result = {**base, **page(relation_results(registry, params), limit, offset)}
    else:
        context = {
            source["work_id"]
            for item in selected
            for source in item["sources"]
            if source["work_id"]
        }
        context |= work_ids(registry, params.get("work", "")) | work_ids(
            registry, params.get("q", "")
        )
        relations = relation_results(
            registry,
            {key: value for key, value in params.items() if key != "q"},
            context_works=context,
        )
        works = [item for item in (registry or {}).get("works", []) if item["id"] in context]
        result = {
            **base,
            "works": works[offset : offset + limit],
            "works_total": len(works),
            "entities": [
                detail(
                    item,
                    registry,
                    provenance,
                    {**params, "locator_limit": min(int(params.get("locator_limit", 20)), 20)},
                )
                for item in selected[offset : offset + limit]
            ],
            "entities_total": len(selected),
            "relations": relations[offset : offset + limit],
            "relations_total": len(relations),
            "limit": limit,
            "offset": offset,
            "truncated": offset + limit < max(len(selected), len(relations), len(works)),
            "input_hashes": {key: digest(value) for key, value in values.items()},
        }
    # Never silently drop rows: advancing by the requested limit would skip them.
    if len(canonical(result)) > MAX_RESPONSE_BYTES:
        return {
            **base,
            "enabled": False,
            "error": "response_limit_exceeded",
            "retryable": True,
            "hint": "Reduce limit or locator_limit and retry the same offset",
        }
    return result
