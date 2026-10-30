from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from jeb.batch import import_response, prepare
from jeb.core import digest, read_json, read_yaml, sha256, write_json
from jeb.corpus import ingest, load_corpus, segments
from jeb.demo import SOURCE_ID, create_workspace

REPO = Path(__file__).resolve().parents[1]


class WorkspaceTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        shutil.copytree(REPO / "config", self.base / "config")
        (self.base / "docs").mkdir()
        shutil.copyfile(REPO / "docs/EDITORIAL_POLICY.md", self.base / "docs/EDITORIAL_POLICY.md")
        self.project = create_workspace(self.base, self.base / "fixture")
        self.source_id = SOURCE_ID
        ingest(self.project, SOURCE_ID, normalized=False)
        ingest(self.project, SOURCE_ID, normalized=True)

    def books(self):
        return load_corpus(self.project, SOURCE_ID)

    def raw(self):
        lock = read_json(self.project.path("sources/lock.json"))["sources"][0]
        return self.project.path(f"data/raw/{SOURCE_ID}/{lock['sha256']}.txt").read_bytes()

    def rewrite_fixture(self, payload: bytes, coverage=None):
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        source = registry["sources"][0]
        source["artifact"].update(sha256=sha256(payload), size_bytes=len(payload))
        lock_document = read_json(self.project.path("sources/lock.json"))
        lock = lock_document["sources"][0]
        lock.update(
            sha256=sha256(payload), size_bytes=len(payload), source_record_sha256=digest(source)
        )
        if coverage is not None:
            lock["coverage"] = coverage
        write_json(self.project.path("sources/registry.yaml"), registry)
        write_json(self.project.path("sources/lock.json"), lock_document)
        write_json(self.project.path("rewrite-log.json"), {"synthetic_test_only": True})
        path = self.project.path(f"data/raw/{SOURCE_ID}/{lock['sha256']}.txt")
        path.write_bytes(payload)

    def response(self, batch_id="test-batch"):
        packet = prepare(self.project, SOURCE_ID, batch_id, "fixture", "modernize")
        return {
            "schema_version": "1.0",
            "batch_id": batch_id,
            "packet_sha256": packet["packet_sha256"],
            "tool": {
                "name": "Synthetic test tool; not a real model run",
                "model_identifier": None,
                "reported_at": "2026-10-30",
            },
            "items": [
                {
                    "segment_id": s["segment_id"],
                    "action": "no_change",
                    "proposed_text": s["normalized_text"],
                    "change_class": "A",
                    "rationale": "Synthetic test data only",
                    "flags": [],
                    "evidence_ids": [],
                    "name_mapping_ids": [],
                }
                for s in packet["segments"]
            ],
        }

    def import_test_response(self, response=None):
        response = response if response is not None else self.response()
        path = self.project.path("returned.json")
        write_json(path, response)
        result = import_response(self.project, path)
        proposal = read_json(self.project.path(f"data/proposals/{result['proposal_id']}.json"))
        return proposal

    def decision(self, proposal, index=0, decision_id="test-decision"):
        item = proposal["items"][index]
        return {
            "schema_version": "1.0",
            "decision_id": decision_id,
            "proposal_id": proposal["proposal_id"],
            "proposal_sha256": digest(proposal),
            "segment_id": item["segment_id"],
            "text_sha256": item["text_sha256"],
            "policy_sha256": self.project.policy_hash(),
            "state": "approved",
            "reviewer_id": "SYNTHETIC-TEST-OWNER",
            "reviewer_role": "owner",
            "human_attestation": True,
            "reviewed_at": "2026-10-30",
            "rationale": "Simulated owner decision in an isolated automated test only; no real human approval.",
            "resolutions": [
                {"flag": f, "resolution": "Simulated test resolution only"} for f in item["flags"]
            ],
            "supersedes": None,
        }

    def apply_test_decisions(self, decisions):
        from jeb.review import apply

        path = self.project.path("test-decisions.json")
        write_json(path, {"schema_version": "1.0", "decisions": decisions})
        return apply(self.project, path)

    def knowledge_record(self, record_id="test-reflection"):
        segment = next(iter(segments(self.books()).values()))
        return {
            "schema_version": "1.0",
            "record_id": record_id,
            "record_type": "annotation",
            "book_id": "GEN",
            "layer": "personal_reflection",
            "text": "Synthetic reflection draft; not an explanatory assertion.",
            "segment_ids": [segment["segment_id"]],
            "source_id": None,
            "bibliographic_details": None,
            "url": None,
            "locator": None,
            "access_date": None,
            "evidence_category": "personal_reflection",
            "evidence_ids": [],
            "claim_ids": [],
            "entity_ids": [],
            "related_ids": [],
            "selected_name_mapping_id": None,
            "uncertainty": "Synthetic fixture only",
            "review_state": "draft",
            "depends_on": {
                segment["segment_id"]: sha256(segment["normalized_text"].encode("utf-8"))
            },
            "approval": None,
        }

    def write_knowledge(self, *records):
        path = self.project.path("data/knowledge/records.jsonl")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(
            b"".join((json.dumps(r, ensure_ascii=False) + "\n").encode("utf-8") for r in records)
        )

    def approve_test_knowledge(self, record):
        record = copy.deepcopy(record)
        record["review_state"] = "approved"
        record["approval"] = {
            "reviewer_id": "SYNTHETIC-TEST-OWNER",
            "date": "2026-10-30",
            "human_attestation": True,
            "content_sha256": digest({k: v for k, v in record.items() if k != "approval"}),
        }
        return record
