from __future__ import annotations

import copy
import json
import subprocess
import sys
from unittest.mock import patch

from jeb import knowledge_packets, narrative_packets
from jeb.build_archive import create, validate
from jeb.core import (
    JebError,
    Project,
    canonical,
    digest,
    read_yaml,
    validate_schema,
    write_json,
)
from jeb.export import reader
from jeb.knowledge import validate_knowledge
from tests import test_knowledge_packets as helpers
from tests.support import WorkspaceTest


class NarrativePacketTests(WorkspaceTest):
    draft = helpers.KnowledgePacketTests.draft
    evidence = helpers.KnowledgePacketTests.evidence
    claim = helpers.KnowledgePacketTests.claim

    def packet(self, packet_id="test-narrative"):
        return narrative_packets.prepare(self.project, self.source_id, "fixture", packet_id)

    def response(self):
        packet = self.packet()
        display = packet["segments"][0]["display"]
        segment_id, text = display["segment_id"], display["text"]

        def span(phrase):
            start = text.index(phrase)
            return {"segment_id": segment_id, "start": start, "end": start + len(phrase)}

        def node(key, kind, **fields):
            return {
                "schema_version": "1.0",
                "node_id": key,
                "kind": kind,
                "book_id": "GEN",
                "basis": "source_narrative",
                "segment_ids": [segment_id],
                "depends_on": {segment_id: display["text_sha256"]},
                "evidence_ids": ["draft-evidence"],
                "claim_ids": [],
                "attribution": {"kind": "ai_assisted_draft", "credit": "Automated synthetic test"},
                "rationale": "Original invented fixture; no historical assertion.",
                "uncertainty": "Source narration only; not independently verified.",
                "review_state": "draft",
                "approval": None,
                **fields,
            }

        result = {
            "schema_version": "1.0",
            "packet_id": packet["packet_id"],
            "packet_sha256": packet["packet_sha256"],
            "source_id": self.source_id,
            "task": "narrative",
            "tool": {
                "name": "Automated synthetic test, no human review",
                "model_identifier": None,
                "reported_at": "2026-10-31",
            },
            "limitations": ["Original invented test data; not scripture or historical research."],
            "review_state": "unreviewed",
            "approval_authority": "none",
            "human_attestation": False,
            "support_drafts": [self.draft(self.evidence())],
            "nodes": [
                node(
                    "person",
                    "entity",
                    entity_type="person",
                    label="covik",
                    mention=span("covik"),
                    name_mapping_id=None,
                ),
                node(
                    "object",
                    "entity",
                    entity_type="object",
                    label="probni zapis",
                    mention=span("probni zapis"),
                    name_mapping_id=None,
                ),
                node(
                    "state",
                    "event",
                    event_kind="state",
                    description="covik ne mijenja 2 broja.",
                    anchor=span("ne mijenja 2 broja"),
                    participants=[
                        {"entity_id": "person", "role": "agent", "uncertainty": "Explicit noun."}
                    ],
                ),
                node(
                    "reading",
                    "event",
                    event_kind="action",
                    description="Čita probni zapis.",
                    anchor=span("Čita probni zapis."),
                    participants=[
                        {
                            "entity_id": "object",
                            "role": "patient",
                            "uncertainty": "No explicit agent assigned.",
                        }
                    ],
                ),
                node(
                    "sequence",
                    "story",
                    title="Two clauses in the invented fixture",
                    event_ids=["state", "reading"],
                    ordering="source_presentation",
                    relations=[
                        {
                            "from_event_id": "state",
                            "to_event_id": "reading",
                            "relation": "narrative_before",
                            "anchor": None,
                            "uncertainty": "Presentation order only; no chronology claim.",
                        }
                    ],
                ),
            ],
            "items": [
                {
                    "segment_id": row["display"]["segment_id"],
                    "text_sha256": row["display"]["text_sha256"],
                    "node_ids": [],
                    "support_record_ids": [],
                    "action": "no_draft",
                    "rationale": "Synthetic test coverage.",
                }
                for row in packet["segments"]
            ],
        }
        person = node(
            "fiction-person",
            "entity",
            basis="fiction",
            evidence_ids=[],
            entity_type="person",
            label="izmišljeni čitalac",
            mention=None,
            name_mapping_id=None,
        )
        event = node(
            "fiction-event",
            "event",
            basis="fiction",
            evidence_ids=[],
            event_kind="action",
            description="Izmišljeni čitalac slaže kartice.",
            anchor=None,
            participants=[
                {
                    "entity_id": "fiction-person",
                    "role": "agent",
                    "uncertainty": "Invented role, no source attestation.",
                }
            ],
        )
        story = node(
            "fiction-story",
            "story",
            basis="fiction",
            evidence_ids=[],
            title="Invented card sorting",
            event_ids=["fiction-event"],
            ordering="fictional_presentation",
            relations=[],
        )
        result["nodes"].extend([person, event, story])
        self.cover(result)
        return result

    def cover(self, response):
        for item in response["items"]:
            item["node_ids"] = [
                n["node_id"] for n in response["nodes"] if item["segment_id"] in n["segment_ids"]
            ]
            item["support_record_ids"] = [
                d["record"]["record_id"]
                for d in response["support_drafts"]
                if item["segment_id"] in d["record"]["segment_ids"]
            ]
            item["action"] = (
                "drafts_proposed" if item["node_ids"] or item["support_record_ids"] else "no_draft"
            )

    def returned(self, value):
        path = self.project.path("returned-narrative.json")
        write_json(path, value)
        return path

    def test_deterministic_bounded_packet_and_valid_typed_graph(self):
        with patch("urllib.request.urlopen", side_effect=AssertionError("No network")):
            first = self.packet()
            self.assertEqual(first, self.packet())
            self.assertLess(len(canonical(first)), narrative_packets.MAX_PACKET)
            self.assertEqual(
                first["coverage_manifest"], [s["display"]["segment_id"] for s in first["segments"]]
            )
            self.assertFalse(first["human_attestation"])
            self.assertEqual(first["approval_authority"], "none")
            self.assertFalse(self.project.path("data/knowledge-proposals/test-narrative").exists())
            response = self.response()
            narrative_packets.validate_response(self.project, response)
            for node in response["nodes"]:
                validate_schema("narrative-node", node)

    def test_admission_opt_in_and_exact_pilot_scope(self):
        for selection in ("GEN", "MAT", "MRK", "LUK", "JHN"):
            with (
                self.subTest(selection=selection),
                self.assertRaisesRegex(JebError, "missing/ambiguous"),
            ):
                narrative_packets.prepare(
                    self.project, self.source_id, selection, f"test-{selection}"
                )
        with self.assertRaises(JebError):
            Project(self.project.root)
        for packet_id in ("CON", "../escape"):
            with self.assertRaises(JebError):
                self.packet(packet_id)
        response = self.response()
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        registry["sources"][0]["status"] = "needs_review"
        write_json(self.project.path("sources/registry.yaml"), registry)
        with self.assertRaisesRegex(JebError, "needs_review"):
            narrative_packets.validate_response(self.project, response)

    def test_substituted_and_resealed_packet_inputs_are_rejected(self):
        packet = self.packet()
        path = self.project.path("data/narrative-proposals/test-narrative/input.json")
        changed = copy.deepcopy(packet)
        changed["prompt"] = "Changed prompt"
        write_json(path, changed)
        with self.assertRaisesRegex(JebError, "hash changed"):
            narrative_packets.current_packet(self.project, packet["packet_id"])
        for field in ("prompt", "policy", "output_schema", "knowledge_namespace_sha256"):
            changed = copy.deepcopy(packet)
            changed[field] = {"type": "object"} if field == "output_schema" else "0" * 64
            changed["packet_sha256"] = digest(
                {k: v for k, v in changed.items() if k != "packet_sha256"}
            )
            write_json(path, changed)
            with (
                self.subTest(field=field),
                self.assertRaisesRegex(JebError, "Stale or substituted"),
            ):
                narrative_packets.current_packet(self.project, packet["packet_id"])

    def test_metadata_and_knowledge_namespace_changes_make_packet_stale(self):
        response = self.response()
        path = self.project.path("sources/registry.yaml")
        registry = read_yaml(path)
        original = copy.deepcopy(registry)
        extra = copy.deepcopy(registry["sources"][0])
        extra.update(
            source_id="synthetic-context", kind="contextual", title="Original contextual test only"
        )
        registry["sources"].append(extra)
        write_json(path, registry)
        with self.assertRaisesRegex(JebError, "Stale or substituted"):
            narrative_packets.validate_response(self.project, response)
        write_json(path, original)
        self.write_knowledge(self.knowledge_record("new-record"))
        with self.assertRaisesRegex(JebError, "Stale or substituted"):
            narrative_packets.validate_response(self.project, response)

    def test_current_display_change_invalidates_packet(self):
        response = self.response()
        proposal_response = WorkspaceTest.response(self)
        proposal_response["items"][0].update(
            proposed_text="Sintetički uzorak: covik čita.",
            action="propose",
            change_class="C",
            flags=["linguistic"],
        )
        proposal = self.import_test_response(proposal_response)
        decision = self.decision(proposal)
        self.apply_test_decisions([decision])
        with self.assertRaisesRegex(JebError, "Stale or substituted"):
            narrative_packets.validate_response(self.project, response)

    def test_wrong_response_identity_hash_coverage_or_approval(self):
        original = self.response()
        mutations = [
            lambda r: r.update(packet_sha256="0" * 64),
            lambda r: r.update(source_id="invented"),
            lambda r: r["items"].reverse(),
            lambda r: r["items"].pop(),
            lambda r: r["items"][0].update(text_sha256="0" * 64),
            lambda r: r.update(human_attestation=True),
            lambda r: r["nodes"][0].update(review_state="approved"),
            lambda r: r["nodes"][0].update(approval={"reviewer_id": "invented"}),
            lambda r: r["nodes"][0].update(book_id="EXO"),
            lambda r: r["nodes"][0].update(book_id="MAT"),
            lambda r: r["nodes"][0].update(label="човек"),
        ]
        for change in mutations:
            value = copy.deepcopy(original)
            change(value)
            with self.subTest(value=value["items"][0]["segment_id"]), self.assertRaises(JebError):
                narrative_packets.validate_response(self.project, value)

    def test_character_spans_are_unicode_offsets_and_exact_unmapped_labels(self):
        value = self.response()
        entity = value["nodes"][1]
        self.assertEqual(
            entity["mention"]["start"],
            self.packet()["segments"][0]["display"]["text"].index("probni zapis"),
        )
        narrative_packets.validate_response(self.project, value)
        for start, end in ((-1, 2), (10, 10), (11, 10), (0, 100000)):
            changed = copy.deepcopy(value)
            changed["nodes"][0]["mention"].update(start=start, end=end)
            with self.subTest(start=start, end=end), self.assertRaises(JebError):
                narrative_packets.validate_response(self.project, changed)
        changed = copy.deepcopy(value)
        changed["nodes"][0]["label"] = "čovik"
        with self.assertRaisesRegex(JebError, "must equal source mention"):
            narrative_packets.validate_response(self.project, changed)

    def test_name_mapping_must_be_approved_bound_and_witnessed(self):
        # Synthetic approvals exist only in this automatically removed test root.
        mapping = {
            "mapping_id": "test-name",
            "entity_id": "test-entity",
            "attested_form_latin": "covik",
            "display_form": "Probni",
            "aliases": [],
            "source_language": "Synthetic test language",
            "witness_source_id": self.source_id,
            "witness_locator": "First invented test segment",
            "historical_form": None,
            "historical_form_status": "unknown",
            "competing_forms": [],
            "transliteration_scheme": "Original synthetic Latin test; no transliteration",
            "rationale": "Temporary automated fixture; not an actual owner mapping",
            "status": "approved",
        }
        mapping["approval"] = {
            "reviewer_id": "SYNTHETIC-TEST-OWNER",
            "date": "2026-10-31",
            "human_attestation": True,
            "content_sha256": digest({k: v for k, v in mapping.items() if k != "approval"}),
        }
        write_json(
            self.project.path("config/name_registry.yaml"),
            {"schema_version": "1.0", "scheme_status": "unapproved", "mappings": [mapping]},
        )
        value = self.response()
        value["nodes"][0].update(label="Probni", name_mapping_id=mapping["mapping_id"])
        narrative_packets.validate_response(self.project, value)
        for label, mapping_id in (("Saint Probni", mapping["mapping_id"]), ("Probni", "unknown")):
            changed = copy.deepcopy(value)
            changed["nodes"][0].update(label=label, name_mapping_id=mapping_id)
            with self.assertRaises(JebError):
                narrative_packets.validate_response(self.project, changed)
        changed = copy.deepcopy(value)
        changed["nodes"][1].update(label="Probni", name_mapping_id=mapping["mapping_id"])
        with self.assertRaisesRegex(JebError, "witnessed mention mismatch"):
            narrative_packets.validate_response(self.project, changed)

    def test_scope_dependencies_and_exact_coverage_are_required(self):
        original = self.response()
        mutations = [
            lambda r: r["nodes"][0].update(segment_ids=["unrequested"]),
            lambda r: r["nodes"][0].update(depends_on={}),
            lambda r: r["nodes"][0]["mention"].update(segment_id=r["items"][1]["segment_id"]),
            lambda r: r["items"][0]["node_ids"].pop(),
            lambda r: r["items"][0]["node_ids"].reverse(),
            lambda r: r["items"][0].update(action="no_draft"),
            lambda r: r["items"][0].update(support_record_ids=[]),
        ]
        for change in mutations:
            value = copy.deepcopy(original)
            change(value)
            with self.assertRaises(JebError):
                narrative_packets.validate_response(self.project, value)

    def test_typed_local_node_references_and_fiction_boundary(self):
        original = self.response()
        mutations = [
            lambda r: r["nodes"][2]["participants"][0].update(entity_id="missing"),
            lambda r: r["nodes"][2]["participants"][0].update(entity_id="reading"),
            lambda r: r["nodes"][2]["participants"][0].update(entity_id="fiction-person"),
            lambda r: r["nodes"][4].update(event_ids=["person"]),
            lambda r: r["nodes"][4].update(event_ids=["fiction-event"]),
            lambda r: r["nodes"][5].update(evidence_ids=["draft-evidence"]),
            lambda r: r["nodes"][5].update(name_mapping_id="invented"),
            lambda r: r["nodes"][2]["participants"].append(
                copy.deepcopy(r["nodes"][2]["participants"][0])
            ),
        ]
        for change in mutations:
            value = copy.deepcopy(original)
            change(value)
            with self.assertRaises(JebError):
                narrative_packets.validate_response(self.project, value)

    def test_draft_ids_cannot_shadow_support_or_canonical_records(self):
        original = self.response()
        for node_id in ("person", "draft-evidence"):
            value = copy.deepcopy(original)
            value["nodes"][1]["node_id"] = node_id
            self.cover(value)
            with self.assertRaises(JebError):
                narrative_packets.validate_response(self.project, value)
        self.write_knowledge(self.knowledge_record("canonical-id"))
        self.project.path("data/narrative-proposals/test-narrative/input.json").unlink()
        value = self.response()
        value["nodes"][0]["node_id"] = "canonical-id"
        self.cover(value)
        with self.assertRaisesRegex(JebError, "shadows knowledge"):
            narrative_packets.validate_response(self.project, value)

    def test_current_attached_evidence_can_support_nodes_but_stale_evidence_cannot(self):
        evidence = self.evidence("known-evidence")
        self.write_knowledge(evidence)
        value = self.response()
        value["support_drafts"] = []
        for node in value["nodes"][:5]:
            node["evidence_ids"] = ["known-evidence"]
        self.cover(value)
        narrative_packets.validate_response(self.project, value)
        evidence["depends_on"] = {key: "0" * 64 for key in evidence["segment_ids"]}
        self.write_knowledge(evidence)
        self.project.path("data/narrative-proposals/test-narrative/input.json").unlink()
        value["packet_sha256"] = self.packet()["packet_sha256"]
        with self.assertRaisesRegex(JebError, "stale narrative support"):
            narrative_packets.validate_response(self.project, value)

    def test_support_type_source_scope_and_dag_gates(self):
        original = self.response()
        mutations = [
            lambda r: r["nodes"][0].update(evidence_ids=[]),
            lambda r: r["nodes"][0].update(evidence_ids=["missing"]),
            lambda r: r["nodes"][0].update(claim_ids=["draft-evidence"]),
            lambda r: r["support_drafts"][0]["record"].update(
                evidence_category="secondary_scholarship"
            ),
            lambda r: r["support_drafts"][0]["record"].update(record_type="annotation"),
            lambda r: r["support_drafts"][0]["record"].update(source_id="invented"),
        ]
        for change in mutations:
            value = copy.deepcopy(original)
            change(value)
            with self.assertRaises(JebError):
                narrative_packets.validate_response(self.project, value)
        value = copy.deepcopy(original)
        claim = self.claim()
        claim["claim_ids"] = ["draft-claim"]
        value["support_drafts"].append(self.draft(claim))
        self.cover(value)
        with self.assertRaisesRegex(JebError, "itself"):
            narrative_packets.validate_response(self.project, value)

    def test_historical_basis_requires_secondary_and_linked_historical_claim(self):
        value = self.response()
        for node in value["nodes"][:5]:
            node["basis"] = "historical_claim"
        with self.assertRaisesRegex(JebError, "separate secondary evidence"):
            narrative_packets.validate_response(self.project, value)
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        extra = copy.deepcopy(registry["sources"][0])
        extra.update(
            source_id="synthetic-context",
            kind="contextual",
            title="Invented secondary test bibliography; no actual scholarship",
        )
        registry["sources"].append(extra)
        write_json(self.project.path("sources/registry.yaml"), registry)
        self.project.path("data/narrative-proposals/test-narrative/input.json").unlink()
        value["packet_sha256"] = self.packet()["packet_sha256"]
        secondary = self.evidence("secondary")
        secondary.update(source_id="synthetic-context", evidence_category="secondary_scholarship")
        claim = self.claim("historical-claim", "secondary")
        claim["layer"] = "historical"
        value["support_drafts"].extend([self.draft(secondary), self.draft(claim)])
        for node in value["nodes"][:5]:
            node["evidence_ids"].append("secondary")
            node["claim_ids"].append("historical-claim")
        self.cover(value)
        narrative_packets.validate_response(self.project, value)
        changed = copy.deepcopy(value)
        changed["support_drafts"][-1]["record"]["evidence_ids"] = ["draft-evidence"]
        with self.assertRaisesRegex(JebError, "linked historical claim"):
            narrative_packets.validate_response(self.project, changed)

    def test_source_order_is_distinct_from_anchored_assertions_and_uncertainty(self):
        original = self.response()
        changed = copy.deepcopy(original)
        changed["nodes"][4]["event_ids"].reverse()
        with self.assertRaisesRegex(JebError, "source presentation"):
            narrative_packets.validate_response(self.project, changed)
        changed = copy.deepcopy(original)
        relation = changed["nodes"][4]["relations"][0]
        relation["relation"] = "source_stated_before"
        with self.assertRaisesRegex(JebError, "exact source anchor"):
            narrative_packets.validate_response(self.project, changed)
        relation["anchor"] = copy.deepcopy(changed["nodes"][2]["anchor"])
        narrative_packets.validate_response(self.project, changed)  # structural, not semantic proof
        backwards = copy.deepcopy(relation)
        backwards.update(from_event_id="reading", to_event_id="state")
        changed["nodes"][4]["relations"].append(backwards)
        with self.assertRaisesRegex(JebError, "Circular asserted story order"):
            narrative_packets.validate_response(self.project, changed)
        for rel in changed["nodes"][4]["relations"]:
            rel["relation"] = "uncertain"
        narrative_packets.validate_response(self.project, changed)

    def test_out_of_order_nodes_validate_without_runtime_errors(self):
        value = self.response()
        value["nodes"].reverse()
        self.cover(value)
        narrative_packets.validate_response(self.project, value)
        next(n for n in value["nodes"] if n["node_id"] == "reading")["anchor"]["segment_id"] = (
            "unknown"
        )
        with self.assertRaises(JebError):
            narrative_packets.validate_response(self.project, value)

    def test_story_relations_need_member_events_distinct_anchors_and_honest_basis(self):
        original = self.response()
        mutations = [
            lambda r: r["nodes"][4]["relations"][0].update(to_event_id="missing"),
            lambda r: r["nodes"][4]["relations"][0].update(to_event_id="state"),
            lambda r: r["nodes"][4]["relations"].append(
                copy.deepcopy(r["nodes"][4]["relations"][0])
            ),
            lambda r: r["nodes"][3].update(anchor=copy.deepcopy(r["nodes"][2]["anchor"])),
            lambda r: r["nodes"][4].update(ordering="fictional_presentation"),
        ]
        for change in mutations:
            value = copy.deepcopy(original)
            change(value)
            with self.assertRaises(JebError):
                narrative_packets.validate_response(self.project, value)
        value = copy.deepcopy(original)
        extra = copy.deepcopy(value["nodes"][6])
        extra["node_id"] = "fiction-second"
        value["nodes"].append(extra)
        story = value["nodes"][7]
        story["event_ids"].append("fiction-second")
        story["relations"] = [
            {
                "from_event_id": "fiction-event",
                "to_event_id": "fiction-second",
                "relation": "source_stated_before",
                "anchor": copy.deepcopy(value["nodes"][2]["anchor"]),
                "uncertainty": "Test only; invalid source claim in fiction.",
            }
        ]
        self.cover(value)
        with self.assertRaisesRegex(JebError, "factual basis"):
            narrative_packets.validate_response(self.project, value)

    def test_empty_and_support_only_responses_are_valid(self):
        value = self.response()
        value["nodes"] = []
        self.cover(value)
        narrative_packets.validate_response(self.project, value)
        value["support_drafts"] = []
        self.cover(value)
        narrative_packets.validate_response(self.project, value)

    def test_size_limits_and_malformed_json_are_bounded(self):
        value = self.response()
        value["limitations"] = ["a" * narrative_packets.MAX_RESPONSE]
        with self.assertRaisesRegex(JebError, "48 KiB"):
            narrative_packets.validate_response(self.project, value)
        path = self.project.path("oversized.json")
        path.write_bytes(b" " * (narrative_packets.MAX_RESPONSE + 1))
        with self.assertRaises(JebError):
            narrative_packets.read_response(path)
        path.write_text('{"task":"narrative","task":"narrative"}', "utf-8")
        with self.assertRaises(JebError):
            narrative_packets.read_response(path)

    def test_import_is_immutable_unreviewed_and_does_not_change_reader(self):
        value = self.response()
        before = reader(self.project, self.source_id, "preview")
        result = narrative_packets.import_response(self.project, self.returned(value))
        self.assertFalse(result["canonical_knowledge_changed"])
        self.assertEqual(validate_knowledge(self.project, self.books()), {})
        self.assertEqual(reader(self.project, self.source_id, "preview"), before)
        with self.assertRaisesRegex(JebError, "Duplicate narrative"):
            narrative_packets.import_response(self.project, self.returned(value))
        imported = self.project.path(result["output"])
        value["limitations"].append("Changed data")
        write_json(imported, value)
        with self.assertRaisesRegex(JebError, "content changed"):
            narrative_packets.read_response(imported)

    def test_report_fences_untrusted_content_and_cannot_overwrite(self):
        value = self.response()
        value["nodes"][0]["rationale"] = (
            "```\n# Untrusted returned heading\n<script>alert(1)</script>"
        )
        path = self.returned(value)
        narrative_packets.report(self.project, path, "reports/narrative.md")
        text = self.project.path("reports/narrative.md").read_text("utf-8")
        self.assertIn("````json", text)
        self.assertIn("Synthetic fixture; not scripture", text)
        self.assertIn("no chronology claim", text)
        value["limitations"].append("Another draft")
        self.returned(value)
        with self.assertRaises(JebError):
            narrative_packets.report(self.project, path, "reports/narrative.md")

    def test_old_packet_protocol_and_canonical_archive_exclude_narrative_cache(self):
        before = knowledge_packets.prepare(
            self.project, self.source_id, "fixture", "annotate", "old"
        )
        value = self.response()
        narrative_packets.import_response(self.project, self.returned(value))
        after = knowledge_packets.prepare(
            self.project, self.source_id, "fixture", "annotate", "old"
        )
        self.assertEqual(before, after)
        result = create(self.project, self.source_id, "narrative-exclusion", "dist/build.zip")
        verified = validate(self.project.path(result["output"]), synthetic=True)
        self.assertFalse(
            any("narrative-proposals" in row["path"] for row in verified["manifest"]["files"])
        )
        with self.assertRaises(JebError):
            knowledge_packets.validate_response(self.project, value)

    def test_cli_stages_reports_and_rejects_false_approval_without_traceback(self):
        def run(*args):
            return subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jeb",
                    "--root",
                    str(self.project.root),
                    "--synthetic",
                    "knowledge",
                    "narrative",
                    *args,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

        prepared = run(
            "prepare",
            "--source",
            self.source_id,
            "--selection",
            "fixture",
            "--packet-id",
            "test-narrative",
        )
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        value = self.response()
        path = self.returned(value)
        for args in (
            ("validate", "--input", str(path)),
            ("import", "--input", str(path)),
            ("report", "--input", str(path), "--output", "reports/cli-narrative.md"),
        ):
            result = run(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["approval_authority"], "none")
        value["human_attestation"] = True
        result = run("validate", "--input", str(self.returned(value)))
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.project.path("data/knowledge-reviews").exists())
