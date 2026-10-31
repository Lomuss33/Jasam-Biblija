from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jeb.core import (
    JebError,
    Project,
    canonical,
    digest,
    native_path,
    read_bytes,
    read_yaml,
    write_json,
)
from jeb.export import export, reader
from jeb.knowledge import stored_records, target_identity, validate_knowledge
from jeb.knowledge_curation import (
    CHECKS,
    MAX_DECISIONS,
    apply,
    heads,
    read_decisions,
    read_receipts,
    report,
    validate_decisions,
)
from jeb.knowledge_packets import prepare, validate_response
from jeb.knowledge_review import REVISION_CHECK
from jeb.review import all_decisions
from jeb.search import build_index, search
from tests import test_knowledge_review as fixtures
from tests.support import WorkspaceTest


class KnowledgeCurationTests(WorkspaceTest):
    annotation_response = fixtures.KnowledgeReviewTests.annotation_response
    evidence = fixtures.KnowledgeReviewTests.evidence
    graph = fixtures.KnowledgeReviewTests.graph
    stage = fixtures.KnowledgeReviewTests.stage
    decisions = fixtures.KnowledgeReviewTests.decisions
    approve_values = fixtures.KnowledgeReviewTests.apply_value

    def promote(self, records=None, label="first", version_of=None):
        response = self.annotation_response(records, packet_id="packet-" + label)
        self.stage(response)
        value = self.decisions(response, review_id="review-" + label)
        for item in value["items"]:
            if version_of and item["record_id"] in version_of:
                item["version_of"] = target_identity(version_of[item["record_id"]])
                item["checks"].append(REVISION_CHECK)
        self.approve_values(value)
        return stored_records(self.project)

    def version_pair(self):
        old = self.promote([self.knowledge_record("original")])["original"]
        revised = self.knowledge_record("revision")
        revised["text"] += " Revised synthetic reflection, not the owner voice."
        return self.promote([revised], "revision", {"revision": old})

    def item(self, kind, record, supersedes=None):
        return {
            "kind": kind,
            "target": target_identity(record),
            "supersedes": supersedes,
            "rationale": "Simulated owner curation inside a temporary synthetic test; no actual participation",
            "checks": sorted(CHECKS[kind]),
        }

    def choice(self, candidates, selected, supersedes=None, group="reflection-versions"):
        return {
            "kind": "select",
            "group_id": group,
            "candidates": [target_identity(record) for record in candidates],
            "selected_record_id": selected,
            "supersedes": supersedes,
            "rationale": "Temporary simulated comparison of original synthetic alternatives",
            "checks": sorted(CHECKS["select"]),
        }

    def action(self, *items, action_id="curation", source=True):
        return {
            "schema_version": "1.0",
            "action_id": action_id,
            "source_id": self.source_id if source else None,
            "policy_sha256": self.project.policy_hash(),
            "reviewer_id": "SYNTHETIC-TEST-OWNER; temporary simulation, not an actual person",
            "reviewer_role": "owner",
            "human_attestation": True,
            "reviewed_at": "2026-10-31",
            "items": list(items),
        }

    def govern(self, value):
        path = self.project.path("temporary-curation-decisions.json")
        write_json(path, value)
        return apply(self.project, path)

    def visible(self):
        return {
            r["record_id"] for r in reader(self.project, self.source_id, "preview")["knowledge"]
        }

    def test_withdrawal_hides_support_dependents_and_preserves_every_approval_and_text(self):
        records = self.promote(self.graph())
        before = reader(self.project, self.source_id, "preview")
        original = canonical(records)
        result = self.govern(self.action(self.item("withdraw", records["evidence"])))
        after = reader(self.project, self.source_id, "preview")
        self.assertEqual(after["knowledge"], [])
        self.assertEqual(after["books"], before["books"])
        self.assertEqual(after["coverage"], before["coverage"])
        self.assertEqual(canonical(stored_records(self.project)), original)
        self.assertEqual(all_decisions(self.project), {})
        self.assertEqual(result["approvals_created"], 0)
        self.assertEqual(after["knowledge_curation"]["withdrawn_record_ids"], ["evidence"])
        packet = prepare(self.project, self.source_id, "fixture", "annotate", "after-withdrawal")
        self.assertTrue(all(not row["current"] for row in packet["knowledge_catalog"]))
        export(
            self.project, self.source_id, "preview", "markdown", "exports/withdrawn.md", "five-book"
        )
        self.assertIn(
            "withdrawn_record_ids", self.project.path("exports/withdrawn.md").read_text("utf-8")
        )

    def test_withdrawal_remains_available_when_policy_and_source_display_are_stale(self):
        record = self.promote()["reflection"]
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        registry["sources"][0]["status"] = "needs_review"
        write_json(self.project.path("sources/registry.yaml"), registry)
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        policy.write_bytes(policy.read_bytes() + b"\nChanged temporary policy\n")
        self.govern(self.action(self.item("withdraw", record), source=False))
        self.assertEqual(len(read_receipts(self.project)), 1)
        with self.assertRaisesRegex(JebError, "needs_review"):
            reader(self.project, self.source_id, "preview")
        report(self.project, "reports/blocked-source.md", self.source_id)
        text = self.project.path("reports/blocked-source.md").read_text("utf-8")
        self.assertIn("eligibility unavailable", text)
        self.assertNotIn(record["text"], text)

    def test_reactivation_requires_explicit_withdrawal_and_a_current_dependency_group(self):
        records = self.promote(self.graph())
        with self.assertRaisesRegex(JebError, "prior withdrawal"):
            self.govern(self.action(self.item("reactivate", records["evidence"])))
        self.govern(
            self.action(
                self.item("withdraw", records["evidence"]),
                self.item("withdraw", records["claim"]),
                action_id="withdraw-both",
            )
        )
        with self.assertRaisesRegex(JebError, "current source, support"):
            self.govern(
                self.action(
                    self.item("reactivate", records["claim"], "withdraw-both"),
                    action_id="incomplete",
                )
            )
        self.assertEqual(len(read_receipts(self.project)), 1)
        self.govern(
            self.action(
                self.item("reactivate", records["evidence"], "withdraw-both"),
                self.item("reactivate", records["claim"], "withdraw-both"),
                action_id="restore-both",
            )
        )
        self.assertEqual(self.visible(), set(records))
        self.assertEqual(canonical(stored_records(self.project)), canonical(records))

    def test_reactivation_does_not_clear_stale_policy_or_bypass_source_gates(self):
        record = self.promote()["reflection"]
        self.govern(self.action(self.item("withdraw", record), action_id="withdraw"))
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        policy.write_bytes(policy.read_bytes() + b"\nDifferent temporary policy\n")
        value = self.action(self.item("reactivate", record, "withdraw"), action_id="restore")
        with self.assertRaisesRegex(JebError, "current source, support"):
            self.govern(value)
        value["source_id"] = None
        with self.assertRaisesRegex(JebError, "eligible source"):
            self.govern(value)
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        registry["sources"][0]["status"] = "needs_review"
        write_json(self.project.path("sources/registry.yaml"), registry)
        value["source_id"] = self.source_id
        with self.assertRaisesRegex(JebError, "needs_review"):
            self.govern(value)
        self.assertEqual(len(read_receipts(self.project)), 1)

    def test_declared_revision_stays_hidden_until_the_owner_selects_it(self):
        records = self.version_pair()
        self.assertEqual(self.visible(), {"original"})
        self.assertEqual(
            records["revision"]["provenance"]["version_of"], target_identity(records["original"])
        )
        before = reader(self.project, self.source_id, "preview")["books"]
        self.govern(self.action(self.choice(records.values(), "revision")))
        self.assertEqual(self.visible(), {"revision"})
        artifact = reader(self.project, self.source_id, "preview")
        self.assertEqual(artifact["books"], before)
        self.assertEqual(
            artifact["knowledge_curation"]["selected_versions"], {"reflection-versions": "revision"}
        )
        self.assertEqual(
            artifact["knowledge"][0]["provenance"]["attribution"],
            records["revision"]["provenance"]["attribution"],
        )
        self.assertEqual(canonical(stored_records(self.project)), canonical(records))

    def test_switching_back_is_explicit_and_withdrawing_the_selected_version_has_no_fallback(self):
        records = self.version_pair()
        self.govern(self.action(self.choice(records.values(), "revision"), action_id="pick-new"))
        self.govern(
            self.action(self.item("withdraw", records["revision"]), action_id="withdraw-new")
        )
        self.assertEqual(self.visible(), set())
        self.govern(
            self.action(self.choice(records.values(), "original", "pick-new"), action_id="pick-old")
        )
        self.assertEqual(self.visible(), {"original"})
        self.assertEqual(stored_records(self.project)["revision"]["review_state"], "approved")

    def test_reactivation_and_selection_can_be_one_atomic_current_choice(self):
        records = self.version_pair()
        self.govern(
            self.action(
                self.choice(records.values(), "original"),
                self.item("withdraw", records["revision"]),
                action_id="old-and-withdrawn",
            )
        )
        with self.assertRaisesRegex(JebError, "current source, support"):
            self.govern(
                self.action(
                    self.choice(records.values(), "revision", "old-and-withdrawn"),
                    action_id="pick-withdrawn",
                )
            )
        with self.assertRaisesRegex(JebError, "current source, support"):
            self.govern(
                self.action(
                    self.item("reactivate", records["revision"], "old-and-withdrawn"),
                    action_id="restore-unselected",
                )
            )
        self.govern(
            self.action(
                self.item("reactivate", records["revision"], "old-and-withdrawn"),
                self.choice(records.values(), "revision", "old-and-withdrawn"),
                action_id="restore-and-pick",
            )
        )
        self.assertEqual(self.visible(), {"revision"})

    def test_revision_can_replace_withdrawn_original_without_reactivating_its_claims(self):
        old = self.promote([self.knowledge_record("original")])["original"]
        self.govern(self.action(self.item("withdraw", old), action_id="old-withdrawn"))
        records = self.promote([self.knowledge_record("revision")], "new", {"revision": old})
        self.assertEqual(self.visible(), set())
        self.govern(
            self.action(self.choice(records.values(), "revision"), action_id="new-selected")
        )
        self.assertEqual(self.visible(), {"revision"})
        self.assertEqual(
            reader(self.project, self.source_id, "preview")["knowledge_curation"][
                "withdrawn_record_ids"
            ],
            ["original"],
        )

    def test_unrelated_notes_are_not_inferred_to_be_versions(self):
        records = self.promote([self.knowledge_record("one"), self.knowledge_record("two")])
        self.assertEqual(self.visible(), {"one", "two"})
        self.govern(self.action(self.choice(records.values(), "one")))
        self.assertEqual(self.visible(), {"one"})

    def test_selecting_new_evidence_hides_old_dependents_without_retargeting_them(self):
        original = self.promote(self.graph())
        records = self.promote(
            [self.evidence("evidence-revision")],
            "evidence-revision",
            {"evidence-revision": original["evidence"]},
        )
        self.govern(
            self.action(
                self.choice(
                    [records["evidence"], records["evidence-revision"]],
                    "evidence-revision",
                    group="evidence-versions",
                )
            )
        )
        self.assertEqual(self.visible(), {"evidence-revision"})
        self.assertEqual(stored_records(self.project)["claim"], original["claim"])
        self.assertEqual(stored_records(self.project)["note"], original["note"])

    def test_search_index_must_be_rebuilt_after_curation_even_when_passage_text_is_unchanged(self):
        record = self.promote()["reflection"]
        build_index(self.project, self.source_id)
        self.govern(self.action(self.item("withdraw", record)))
        with self.assertRaisesRegex(JebError, "Stale index"):
            search(self.project, "covik", self.source_id)
        build_index(self.project, self.source_id)
        self.assertEqual(len(search(self.project, "covik", self.source_id)), 1)
        self.assertEqual(self.visible(), set())

    def test_selection_cannot_mix_categories_or_omit_bound_revision_ancestors(self):
        old = self.promote([self.knowledge_record("original"), self.evidence()])["original"]
        records = self.promote([self.knowledge_record("middle")], "middle", {"middle": old})
        middle = records["middle"]
        records = self.promote([self.knowledge_record("latest")], "latest", {"latest": middle})
        with self.assertRaisesRegex(JebError, "category or passage"):
            self.govern(
                self.action(self.choice([records["original"], records["evidence"]], "original"))
            )
        with self.assertRaisesRegex(JebError, "ancestry"):
            self.govern(
                self.action(self.choice([records["original"], records["latest"]], "latest"))
            )
        self.govern(
            self.action(
                self.choice([records[k] for k in ("original", "middle", "latest")], "latest")
            )
        )
        self.assertEqual(self.visible(), {"latest", "evidence"})

    def test_groups_cannot_drop_candidates_or_compete_for_the_same_record(self):
        records = self.version_pair()
        self.govern(
            self.action(self.choice(records.values(), "revision"), action_id="first-choice")
        )
        records = self.promote(
            [self.knowledge_record("third")], "third", {"third": records["revision"]}
        )
        with self.assertRaisesRegex(JebError, "competing version groups"):
            self.govern(
                self.action(
                    self.choice(
                        [records["original"], records["revision"]], "original", group="other-group"
                    ),
                    action_id="conflict",
                )
            )
        # Two independent alternatives make the non-shrinking group rule observable separately from ancestry.
        independent = self.promote([self.knowledge_record("independent")], "independent")
        with self.assertRaisesRegex(JebError, "drop prior candidates"):
            self.govern(
                self.action(
                    self.choice(
                        [independent["original"], independent["independent"]],
                        "original",
                        "first-choice",
                    ),
                    action_id="drop",
                )
            )
        self.govern(
            self.action(
                self.choice(
                    [records[k] for k in ("original", "revision", "third")], "third", "first-choice"
                ),
                action_id="expand",
            )
        )
        self.assertEqual(self.visible(), {"third", "independent"})

    def test_stale_selected_revision_never_falls_back_to_a_current_legacy_original(self):
        old = self.approve_test_knowledge(self.knowledge_record("original"))
        self.write_knowledge(old)
        records = self.promote([self.knowledge_record("revision")], "revision", {"revision": old})
        self.govern(self.action(self.choice(records.values(), "revision")))
        changed = copy.deepcopy(self.books())
        changed["GEN"]["segments"][1]["normalized_text"] += " Adjacent synthetic context changed."
        with patch("jeb.export.load_corpus", return_value=changed):
            artifact = reader(self.project, self.source_id, "preview")
        self.assertEqual(artifact["knowledge"], [])
        self.assertEqual(
            artifact["knowledge_curation"]["selected_versions"]["reflection-versions"], "revision"
        )

    def test_owner_identity_checks_dates_hashes_and_duplicate_subjects_are_strict(self):
        record = self.promote()["reflection"]
        original = self.action(self.item("withdraw", record))
        for key, value in (
            ("human_attestation", False),
            ("reviewer_role", "ai"),
            ("policy_sha256", "0" * 64),
            ("action_id", "../unsafe"),
            ("reviewed_at", "2026-10-29"),
            ("source_id", "invented"),
        ):
            changed = copy.deepcopy(original)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(JebError):
                self.govern(changed)
        for key, value in (("checks", []), ("supersedes", "invented"), ("rationale", " ")):
            changed = copy.deepcopy(original)
            changed["items"][0][key] = value
            with self.subTest(key=key), self.assertRaises(JebError):
                self.govern(changed)
        for key in ("record_sha256", "approval_sha256", "provenance_sha256"):
            changed = copy.deepcopy(original)
            changed["items"][0]["target"][key] = "0" * 64
            with self.subTest(key=key), self.assertRaisesRegex(JebError, "identity changed"):
                self.govern(changed)
        changed = copy.deepcopy(original)
        changed["items"].append(copy.deepcopy(changed["items"][0]))
        with self.assertRaisesRegex(JebError, "Duplicate"):
            self.govern(changed)
        self.assertEqual(read_receipts(self.project), {})

    def test_drafts_and_unknown_ids_cannot_be_curated(self):
        draft = self.knowledge_record("draft")
        self.write_knowledge(draft)
        with self.assertRaisesRegex(JebError, "human-approved"):
            target_identity(draft)
        record = self.promote()["reflection"]
        item = self.item("withdraw", record)
        item["target"]["record_id"] = "invented"
        with self.assertRaisesRegex(JebError, "Unknown canonical"):
            self.govern(self.action(item))
        self.assertEqual(read_receipts(self.project), {})

    def test_curation_history_refuses_branching_cycles_replays_and_missing_predecessors(self):
        record = self.promote()["reflection"]
        value = self.action(self.item("withdraw", record), action_id="first")
        self.govern(value)
        with self.assertRaisesRegex(JebError, "already used"):
            self.govern(value)
        with self.assertRaisesRegex(JebError, "already explicitly withdrawn"):
            self.govern(self.action(self.item("withdraw", record, "first"), action_id="repeat"))
        second = validate_decisions(
            self.project, self.action(self.item("reactivate", record, "first"), action_id="second")
        )
        first = read_receipts(self.project)["first"]
        third = copy.deepcopy(second)
        third["decisions"]["action_id"] = "third"
        with self.assertRaisesRegex(JebError, "Branching"):
            heads({"first": first, "second": second, "third": third})
        first["decisions"]["items"][0]["supersedes"] = "second"
        with self.assertRaisesRegex(JebError, "Cycle"):
            heads({"first": first, "second": second})
        with self.assertRaisesRegex(JebError, "Missing"):
            heads({"second": second})

    def test_invalid_or_failed_atomic_apply_leaves_no_partial_action(self):
        records = self.promote([self.knowledge_record("reflection"), self.evidence()])
        value = self.action(
            self.item("withdraw", records["reflection"]),
            self.choice(records.values(), "reflection"),
        )
        with self.assertRaises(JebError):
            self.govern(value)
        self.assertEqual(read_receipts(self.project), {})
        with (
            patch(
                "jeb.knowledge_curation.write_json",
                side_effect=OSError("Simulated pre-commit failure"),
            ),
            self.assertRaises(OSError),
        ):
            self.govern(self.action(self.item("withdraw", records["reflection"])))
        self.assertEqual(read_receipts(self.project), {})
        path = self.project.path("large-action.json")
        path.write_bytes(b" " * (MAX_DECISIONS + 1))
        with self.assertRaisesRegex(JebError, "exceeds"):
            read_decisions(path)

    def test_action_id_case_variants_cannot_corrupt_windows_receipt_identity(self):
        records = self.promote([self.knowledge_record("one"), self.knowledge_record("two")])
        self.govern(self.action(self.item("withdraw", records["one"]), action_id="chosen-id"))
        with self.assertRaisesRegex(JebError, "already used"):
            self.govern(self.action(self.item("withdraw", records["two"]), action_id="CHOSEN-ID"))
        self.assertEqual(len(read_receipts(self.project)), 1)
        self.assertEqual(self.visible(), {"two"})

    def test_tampered_receipts_and_changed_canonical_targets_fail_closed_until_restored(self):
        record = self.approve_test_knowledge(self.knowledge_record("legacy"))
        self.write_knowledge(record)
        result = self.govern(self.action(self.item("withdraw", record)))
        original_receipt = read_bytes(self.project.path(result["output"]))
        altered = self.approve_test_knowledge(
            {**record, "text": record["text"] + " Changed after curation."}
        )
        self.write_knowledge(altered)
        with self.assertRaisesRegex(JebError, "restore the immutable"):
            validate_knowledge(self.project, self.books())
        self.write_knowledge(record)
        self.assertEqual(self.visible(), set())
        receipt = json.loads(original_receipt)
        receipt["decisions"]["items"][0]["rationale"] += " Changed"
        write_json(self.project.path(result["output"]), receipt)
        with self.assertRaisesRegex(JebError, "filename/hash"):
            read_receipts(self.project)

    def test_unsigned_report_has_metadata_bindings_without_body_text_or_actions(self):
        record = self.promote()["reflection"]
        before = canonical(reader(self.project, self.source_id, "preview"))
        result = report(self.project, "reports/curation.md", self.source_id)
        text = self.project.path("reports/curation.md").read_text("utf-8")
        self.assertIn(digest(record), text)
        self.assertIn("unsigned", text)
        self.assertNotIn(record["text"], text)
        self.assertEqual(result["owner_actions_created"], 0)
        self.assertEqual(read_receipts(self.project), {})
        self.assertEqual(before, canonical(reader(self.project, self.source_id, "preview")))

    def test_withdrawal_invalidates_prepared_support_packets_without_changing_drafts(self):
        records = self.promote([self.evidence()])
        claim = self.graph()[1]
        response = self.annotation_response([claim], packet_id="before-withdrawal")
        self.stage(response)
        self.govern(self.action(self.item("withdraw", records["evidence"])))
        with self.assertRaisesRegex(JebError, "Stale"):
            validate_response(self.project, response)
        self.assertEqual(stored_records(self.project)["evidence"], records["evidence"])

    def test_declaring_a_revision_requires_the_original_identity_scope_and_extra_human_check(self):
        old = self.promote([self.knowledge_record("original")])["original"]
        response = self.annotation_response(
            [self.knowledge_record("revision")], packet_id="new-revision"
        )
        self.stage(response)
        value = self.decisions(response, review_id="revision-review")
        value["items"][0]["version_of"] = target_identity(old)
        with self.assertRaisesRegex(JebError, "explicit human knowledge check"):
            self.approve_values(value)
        value["items"][0]["checks"].append(REVISION_CHECK)
        value["items"][0]["version_of"]["record_sha256"] = "0" * 64
        with self.assertRaisesRegex(JebError, "identity changed"):
            self.approve_values(value)
        self.assertEqual(set(stored_records(self.project)), {"original"})

    def test_cli_requires_separate_owner_decisions_and_records_no_validation_side_effects(self):
        record = self.promote()["reflection"]
        path = self.project.path("cli-action.json")
        write_json(path, {"human_attestation": False})
        prefix = [
            sys.executable,
            "-m",
            "jeb",
            "--root",
            str(self.project.root),
            "--synthetic",
            "knowledge",
            "curate",
        ]
        invalid = subprocess.run(
            prefix + ["apply", "--decisions", str(path)],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(invalid.returncode, 2)
        self.assertNotIn("Traceback", invalid.stderr)
        write_json(path, self.action(self.item("withdraw", record)))
        checked = subprocess.run(
            prefix + ["validate", "--decisions", str(path)],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(read_receipts(self.project), {})
        applied = subprocess.run(
            prefix + ["apply", "--decisions", str(path)],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(json.loads(applied.stdout)["approvals_created"], 0)
        self.assertEqual(self.visible(), set())

    @unittest.skipUnless(os.name == "nt", "Windows extended-length curation receipt paths")
    def test_long_windows_curation_receipts_are_readable_and_replay_safe(self):
        record = self.promote()["reflection"]
        with tempfile.TemporaryDirectory(dir=native_path(Path(tempfile.gettempdir()))) as directory:
            root = Path(directory.removeprefix("\\\\?\\")) / ("deep-" + "x" * 50)
            shutil.copytree(self.project.root, native_path(root))
            project = Project(root, synthetic=True)
            value = self.action(self.item("withdraw", record), action_id="a" * 80)
            path = project.path("action.json")
            write_json(path, value)
            result = apply(project, path)
            self.assertGreater(len(str(project.path(result["output"]))), 260)
            self.assertEqual(len(read_receipts(project)), 1)
            self.assertEqual(reader(project, self.source_id, "preview")["knowledge"], [])
            with self.assertRaisesRegex(JebError, "already used"):
                apply(project, path)
