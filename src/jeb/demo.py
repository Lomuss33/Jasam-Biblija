"""A labelled, isolated vertical slice with invented non-scripture wording."""

from __future__ import annotations

import copy
from importlib.resources import files
from pathlib import Path

from jeb.batch import import_response, prepare
from jeb.core import Project, atomic_write, digest, sha256, write_json
from jeb.corpus import ingest
from jeb.export import export
from jeb.review import report
from jeb.search import build_index, search

SOURCE_ID = "synthetic-v1"


def create_workspace(base: Path, destination: Path) -> Project:
    """Never overwrite existing, different configuration, policy, source or decision bytes."""
    original = Project(base)
    destination = original.path(destination)
    for name in ("collection", "terminology", "name_registry", "modernization_rules"):
        atomic_write(
            destination / f"config/{name}.yaml",
            original.path(f"config/{name}.yaml").read_bytes(),
            replace=False,
        )
    edition = copy.deepcopy(original.edition)
    edition.update(
        edition_id="jeb-synthetic-demo",
        corpus_kind="synthetic",
        jurisdictions=["ZZ"],
        release_preface_approved=False,
        title="JEB synthetic software demonstration",
    )
    # JSON is a YAML 1.2 subset; the rest of the project can use ordinary YAML.
    write_json(destination / "config/edition.yaml", edition, replace=False)
    atomic_write(
        destination / "docs/EDITORIAL_POLICY.md",
        original.path("docs/EDITORIAL_POLICY.md").read_bytes(),
        replace=False,
    )
    payload = files("jeb").joinpath("assets/synthetic.txt").read_bytes()
    fixture_hash = sha256(payload)
    source = {
        "source_id": SOURCE_ID,
        "title": "Synthetic parser fixture; NOT scripture",
        "kind": "synthetic",
        "status": "verified_for_scope",
        "contributors": [],
        "edition": {
            "year": "2026",
            "publication_place": None,
            "revisions": [],
            "transcriber": "JEB test fixture generator",
            "provider": "Local package",
        },
        "landing_url": "urn:jeb:synthetic:fixture-v1",
        "download_urls": [],
        "rights_statement_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "access_date": "2026-10-30",
        "rights_by_jurisdiction": {
            "ZZ": {
                "status": "verified",
                "basis": "ZZ is a fictional test scope. Only original synthetic test data; no historical edition or legal assessment.",
                "evidence_urls": ["urn:jeb:synthetic:fixture-v1"],
            }
        },
        "included_material": [
            "Invented text",
            "Invented heading and nested note",
            "Layout fixtures",
        ],
        "language": "Synthetic regional Latin-script examples",
        "script": "Latin",
        "regional_characteristics": "Selected literal forms in test sentences; not scripture",
        "canon_coverage": "Four invented segments under GEN test references; no real textual coverage",
        "versification": "synthetic-test-v1",
        "artifact": {
            "format": "jeb-transcript-v1",
            "provider_revision": "fixture-v1",
            "sha256": fixture_hash,
            "size_bytes": len(payload),
            "expected_identity": "Packaged synthetic.txt, header JEB-TRANSCRIPT/1",
        },
        "evidence_summary": "Locally authored parser example; cannot clear or substitute for a historical source.",
        "assessment": {
            "author": "Automated synthetic fixture declaration; no human sign-off",
            "review_date": "2026-10-30",
            "limitations": [
                "No biblical wording",
                "No real jurisdictional clearance",
                "Never releasable as an edition",
            ],
        },
        "credits": "Original JEB software fixture; no historical translator involved.",
        "license_notice": "CC0-1.0 for eligible original synthetic fixture contributions only.",
    }
    coverage = []
    for line in payload.decode("utf-8").splitlines()[1:]:
        from jeb.core import json_loads

        record = json_loads(line)
        if record["type"] == "segment":
            coverage.append(
                {
                    key: record[key]
                    for key in ("chapter_label", "verse_label", "verse_labels", "alternate_labels")
                }
            )
    write_json(
        destination / "sources/registry.yaml",
        {"schema_version": "1.0", "sources": [source]},
        replace=False,
    )
    write_json(
        destination / "sources/lock.json",
        {
            "schema_version": "1.0",
            "sources": [
                {
                    "source_id": SOURCE_ID,
                    "source_record_sha256": digest(source),
                    "sha256": fixture_hash,
                    "size_bytes": len(payload),
                    "format": "jeb-transcript-v1",
                    "download_url": None,
                    "coverage": {"GEN": coverage},
                    "complete_books": [],
                    "absences": [],
                }
            ],
        },
        replace=False,
    )
    atomic_write(destination / f"data/raw/{SOURCE_ID}/{fixture_hash}.txt", payload, replace=False)
    return Project(destination, synthetic=True)


def demo(root: Path) -> dict:
    project = create_workspace(root, Path("dist/demo"))
    ingest(project, SOURCE_ID, normalized=False)
    result = ingest(project, SOURCE_ID, normalized=True)
    packet = prepare(project, SOURCE_ID, "fixture-modernize-v1", "fixture", "modernize")
    response = {
        "schema_version": "1.0",
        "batch_id": packet["batch_id"],
        "packet_sha256": packet["packet_sha256"],
        "tool": {
            "name": "Local synthetic demonstration generator (not a model run)",
            "model_identifier": None,
            "reported_at": "2026-10-30",
        },
        "items": [
            {
                "segment_id": s["segment_id"],
                "action": "propose" if i == 0 else "no_change",
                "proposed_text": s["normalized_text"].replace("mijenja", "prepravlja")
                if i == 0
                else s["normalized_text"],
                "change_class": "C" if i == 0 else "A",
                "rationale": "Invented demonstration proposal only; no owner approval or model call.",
                "flags": [],
                "evidence_ids": [],
                "name_mapping_ids": [],
            }
            for i, s in enumerate(packet["segments"])
        ],
    }
    response_path = project.path("data/batches/fixture-modernize-v1/synthetic-response.json")
    write_json(response_path, response, replace=False)
    proposal_id = f"{packet['batch_id']}-{digest(response)[:16]}"
    if not project.path(f"data/proposals/{proposal_id}.json").exists():
        import_response(project, response_path)
    report(project, proposal_id, "reports/review.md")
    exports = [
        export(project, SOURCE_ID, "preview", fmt, f"exports/reader.{suffix}", "five-book")
        for fmt, suffix in (("json", "json"), ("markdown", "md"))
    ]
    build_index(project, SOURCE_ID)
    matches = search(project, "covik", SOURCE_ID)
    return {
        "workspace": "dist/demo",
        "synthetic_only": True,
        "real_biblical_segments": 0,
        "synthetic_segments": result["segments"],
        "proposal_id": proposal_id,
        "owner_approvals": 0,
        "exports": exports,
        "search_matches": len(matches),
    }
