from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jeb.core import JebError, atomic_write, canonical, digest, read_json, sha256
from jeb.historical import (
    build_entity_dossiers,
    build_entity_groups,
    build_entity_index,
    build_registry,
    entity_dossiers,
    entity_groups,
    extract_artifact,
    load_layer,
)
from jeb.historical_demo import create_demo
from jeb.historical_pipeline import (
    initialize,
    load_published,
    pipeline_status,
    published_snapshot,
    step,
    writer_lock,
)
from jeb.historical_query import inspect, query


class HistoricalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="jeb-historical-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.inputs = self.base / "inputs"
        self.inputs.mkdir()
        self.registry_path = self.base / "registry.json"
        self.workspace = self.base / "pipeline"

    def registry(self, names=("missing.txt", "one.txt", "invalid.txt")):
        catalog = {
            "books": [
                {
                    "id": "MAT",
                    "title": "Synthetic MAT",
                    "status": "candidate",
                    "findings": [
                        {
                            "id": str(number),
                            "edition_title": f"Synthetic edition {number}",
                            "translator": "Synthetic contributor",
                            "local_file": name,
                            "language": "hr",
                        }
                        for number, name in enumerate(names)
                    ],
                }
            ]
        }
        catalog_path = self.base / "catalog.json"
        atomic_write(catalog_path, canonical(catalog))
        build_registry(catalog_path, self.registry_path)
        return load_layer("registry", self.registry_path)

    def start(self):
        self.registry()
        (self.inputs / "one.txt").write_bytes(
            "Luma vidi Žana.\r\nLuma cuva svjet, vrjeme, covik, razumit.".encode()
        )
        (self.inputs / "invalid.txt").write_bytes(b"SYNTHETIC\xff")
        return initialize(self.registry_path, self.inputs, self.workspace, synthetic=True)

    def test_batches_skip_bad_inputs_and_resume_with_exact_provenance(self):
        self.assertEqual(self.start()["queue"]["queued"], 3)
        first_head = (self.workspace / "HEAD.json").read_bytes()
        one = step(self.workspace, synthetic=True, max_artifacts=1)
        self.assertEqual(
            (one["processed"], one["queue"]["pending"], one["queue"]["queued"]), (1, 1, 2)
        )
        two = step(self.workspace, synthetic=True, max_artifacts=1)
        self.assertEqual(two["queue"]["complete"], 1)
        final = step(self.workspace, synthetic=True, max_artifacts=1)
        self.assertEqual(
            final["queue"],
            {"queued": 0, "processing": 0, "complete": 1, "pending": 1, "needs_review": 1},
        )
        self.assertFalse(final["releasable"])
        built = query("dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True)
        self.assertEqual(built["entities_total"], 1)
        self.assertEqual(built["entities"][0]["candidate_count"], 2)
        locator = built["entities"][0]["locators"][1]
        raw = (self.inputs / "one.txt").read_bytes()
        self.assertEqual(raw.decode()[locator["start"] : locator["end"]], "Luma")
        self.assertEqual(locator["source_sha256"], sha256(raw))
        self.assertEqual(locator["projection_sha256"], sha256(raw))
        self.assertEqual(locator["offset_unit"], "unicode_code_points")
        self.assertEqual(
            built["entities"][0]["sources"][0]["contributors"], ["Synthetic contributor"]
        )
        old_snapshot = json.loads(first_head)["snapshot_id"]
        self.assertTrue((self.workspace / "snapshots" / old_snapshot / "manifest.json").is_file())
        self.assertEqual(step(self.workspace, synthetic=True)["processed"], 0)

    def test_interruption_recovers_processing_task_and_keeps_last_snapshot(self):
        self.start()
        old_head = (self.workspace / "HEAD.json").read_bytes()
        with patch("jeb.historical_pipeline.extract_artifact", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                step(self.workspace, synthetic=True, max_artifacts=1)
        self.assertEqual((self.workspace / "HEAD.json").read_bytes(), old_head)
        interrupted = pipeline_status(self.workspace, synthetic=True)
        self.assertTrue(interrupted["publication_pending"])
        self.assertEqual(interrupted["queue"]["processing"], 1)
        self.assertEqual(
            step(self.workspace, synthetic=True, max_artifacts=1)["queue"]["processing"], 0
        )

    def test_failed_publication_can_resume_without_reextracting(self):
        self.start()
        old_head = (self.workspace / "HEAD.json").read_bytes()

        def fail_head(path, *args, **kwargs):
            if path.name == "HEAD.json":
                raise OSError("synthetic publication failure")
            return atomic_write(path, *args, **kwargs)

        with patch("jeb.historical_pipeline.atomic_write", side_effect=fail_head):
            with self.assertRaises(OSError):
                step(self.workspace, synthetic=True, max_artifacts=3)
        self.assertEqual((self.workspace / "HEAD.json").read_bytes(), old_head)
        self.assertTrue(pipeline_status(self.workspace, synthetic=True)["publication_pending"])
        with patch(
            "jeb.historical_pipeline.extract_artifact",
            side_effect=AssertionError("Must use checkpoint"),
        ):
            result = step(self.workspace, synthetic=True)
        self.assertFalse(result["publication_pending"])
        self.assertEqual(result["processed"], 0)

    def test_retry_refresh_and_cache_keep_prior_versions(self):
        self.start()
        step(self.workspace, synthetic=True, max_artifacts=3)
        before = (self.workspace / "HEAD.json").read_bytes()
        old = query("dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True)
        (self.inputs / "missing.txt").write_bytes(b"Sela vidi Luma.")
        retried = step(self.workspace, synthetic=True, retry_pending=True)
        self.assertEqual(retried["queue"]["complete"], 2)
        self.assertEqual(step(self.workspace, synthetic=True, refresh=True)["reused"], 2)
        (self.inputs / "one.txt").write_bytes(b"Nera vidi Sela.")
        step(self.workspace, synthetic=True, refresh=True)
        current = query("dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True)
        self.assertEqual(current["entities"][0]["candidate_count"], 1)
        old_id = json.loads(before)["snapshot_id"]
        old_dossiers = read_json(self.workspace / "snapshots" / old_id / "dossiers.json")
        self.assertEqual(
            next(item for item in old_dossiers["dossiers"] if item["normalized_key"] == "luma")[
                "candidate_count"
            ],
            old["entities"][0]["candidate_count"],
        )

    def test_opt_in_locks_and_no_clobber(self):
        self.start()
        with self.assertRaises(JebError):
            pipeline_status(self.workspace)
        before = (self.workspace / "pipeline.json").read_bytes()
        with writer_lock(self.workspace):
            with self.assertRaises(JebError):
                step(self.workspace, synthetic=True)
        with self.assertRaises(FileExistsError):
            initialize(self.registry_path, self.inputs, self.workspace, synthetic=True)
        self.assertEqual(before, (self.workspace / "pipeline.json").read_bytes())

    def test_foreign_directory_and_link_guards_write_nothing(self):
        foreign = self.base / "foreign"
        foreign.mkdir()
        (foreign / "keep.txt").write_bytes(b"USER DATA")
        with self.assertRaises(OSError):
            step(foreign, synthetic=True)
        self.assertEqual([path.name for path in foreign.iterdir()], ["keep.txt"])
        self.registry()
        with patch.object(Path, "is_junction", return_value=True):
            with self.assertRaises(JebError):
                initialize(self.registry_path, self.inputs, self.workspace, synthetic=True)
        self.assertFalse(self.workspace.exists())

    def test_resealed_but_inconsistent_layers_are_rejected(self):
        self.start()
        step(self.workspace, synthetic=True)
        values, _, _ = published_snapshot(self.workspace, synthetic=True)
        paths = {}
        values["dossiers"]["dossiers"][0]["sources"][0]["edition_title"] = "Invented substitution"
        for name, value in values.items():
            paths[name] = self.base / f"{name}-resealed.json"
            atomic_write(paths[name], canonical(value))
        status = inspect(paths)
        self.assertIn({"layer": "pipeline", "reason": "inconsistent_layers"}, status["blockers"])
        self.assertEqual(query("dossier", paths, {"q": "Luma"})["entities"], [])

    def test_decomposed_latin_names_keep_source_offsets_and_normalize_only_for_groups(self):
        artifact = self.registry(("one.txt",))["artifacts"][0]
        text = "SYNTHETIC.\r\nŽana vidi Z\u030cana. svjet vrjeme covik razumit."
        (self.inputs / "one.txt").write_bytes(text.encode("utf-8"))
        result = extract_artifact(artifact, self.inputs, synthetic=True)
        names = [item for item in result["candidates"] if item["surface"] != "SYNTHETIC"]
        self.assertEqual([item["surface"] for item in names], ["Žana", "Z\u030cana"])
        for name in names:
            self.assertEqual(text[name["start"] : name["end"]], name["surface"])
        self.assertIn("svjet vrjeme covik razumit", (self.inputs / "one.txt").read_bytes().decode())

    def test_non_synthetic_extraction_stays_behind_review_gate(self):
        registry = self.registry(("one.txt",))
        with patch(
            "jeb.historical.read_bytes", side_effect=AssertionError("Source must not be opened")
        ):
            result = extract_artifact(registry["artifacts"][0], self.inputs, synthetic=False)
        self.assertEqual(result["reason"], "source_review_required")
        self.assertEqual(result["candidates"], [])

    def test_refresh_rotates_and_skips_unchanged_text_extraction(self):
        self.registry(("a.txt", "b.txt", "c.txt"))
        for name in ("a.txt", "b.txt", "c.txt"):
            (self.inputs / name).write_bytes(b"Luma.")
        initialize(self.registry_path, self.inputs, self.workspace, synthetic=True)
        step(self.workspace, synthetic=True)
        with patch(
            "jeb.historical_pipeline.extract_artifact",
            side_effect=AssertionError("Unchanged source should reuse cache"),
        ):
            for _ in range(3):
                self.assertEqual(
                    step(self.workspace, synthetic=True, refresh=True, max_artifacts=1)["reused"], 1
                )
        attempts = [
            task["attempts"] for task in read_json(self.workspace / "pipeline.json")["tasks"]
        ]
        self.assertEqual(attempts, [2, 2, 2])

    def test_file_and_candidate_limits_have_stable_reasons(self):
        artifact = self.registry(("one.txt",))["artifacts"][0]
        (self.inputs / "one.txt").write_bytes(b"Luma Luma Luma")
        with patch("jeb.historical.MAX_SOURCE_BYTES", 8):
            self.assertEqual(
                extract_artifact(artifact, self.inputs, synthetic=True)["reason"],
                "source_too_large",
            )
        with patch("jeb.historical.MAX_ARTIFACT_CANDIDATES", 1):
            self.assertEqual(
                extract_artifact(artifact, self.inputs, synthetic=True)["reason"],
                "candidate_limit_exceeded",
            )

    def test_pdf_projection_is_hash_bound_and_failures_do_not_invent_text(self):
        artifact = self.registry(("one.pdf",))["artifacts"][0]
        (self.inputs / "one.pdf").write_bytes(b"SYNTHETIC PDF INPUT")
        with (
            patch("jeb.historical.shutil.which", return_value=sys.executable),
            patch("jeb.historical.pdf_projection", return_value=b"Luma sees Nera."),
        ):
            projected = extract_artifact(artifact, self.inputs, synthetic=True)
        self.assertEqual(projected["provenance"]["projection"], "pdftotext_utf8")
        self.assertEqual(projected["provenance"]["projection_sha256"], sha256(b"Luma sees Nera."))
        with (
            patch("jeb.historical.shutil.which", return_value=sys.executable),
            patch("jeb.historical.pdf_projection", side_effect=TimeoutError),
        ):
            failed = extract_artifact(artifact, self.inputs, synthetic=True)
        self.assertEqual((failed["reason"], failed["candidates"]), ("extraction_timeout", []))

    def test_traversal_bad_utf8_and_hash_mismatch_are_per_artifact(self):
        artifact = self.registry(("../outside.txt",))["artifacts"][0]
        self.assertEqual(
            extract_artifact(artifact, self.inputs, synthetic=True)["status"], "needs_review"
        )
        artifact["relative_path"] = "one.txt"
        artifact["sha256"] = "0" * 64
        (self.inputs / "one.txt").write_bytes(b"Luma.")
        self.assertEqual(
            extract_artifact(artifact, self.inputs, synthetic=True)["reason"],
            "source_hash_mismatch",
        )

    def test_nonempty_demo_lookup_counts_each_work_once_and_preserves_credits(self):
        result = create_demo(self.base / "demo", synthetic=True)
        workspace = Path(result["workspace"])
        lookup = query("lookup", {}, {"q": "Luma"}, workspace=workspace, synthetic=True)
        self.assertEqual(
            {item["work_id"]: item["locator_count"] for item in lookup["results"]},
            {"MAT": 3, "MRK": 1},
        )
        built = query(
            "dossier",
            {},
            {"q": "Luma", "work": "MAT", "locator_limit": "1"},
            workspace=workspace,
            synthetic=True,
        )
        self.assertEqual(built["entities"][0]["candidate_count"], 3)
        self.assertTrue(built["entities"][0]["locators_truncated"])
        self.assertEqual(len(built["entities"][0]["locators"]), 1)
        self.assertTrue(
            all(item["selection_basis"] == "work_context" for item in built["relations"])
        )
        self.assertTrue(all(item["to_id"] == "MAT" for item in built["relations"]))
        empty = query("dossier", {}, {"q": "Nonexistent"}, workspace=workspace, synthetic=True)
        self.assertEqual(empty["relations"], [])
        self.assertEqual(empty["entities"], [])

    def test_stale_partial_inputs_malformed_json_and_no_path_leak(self):
        self.start()
        step(self.workspace, synthetic=True)
        values, _, _ = published_snapshot(self.workspace, synthetic=True)
        paths = {}
        for name, value in values.items():
            paths[name] = self.base / f"{name}-copy.json"
            atomic_write(paths[name], canonical(value))
        self.assertEqual(inspect(paths)["status"], "ready")
        changed = copy.deepcopy(values["registry"])
        changed["works"][0]["title"] = "Changed synthetic metadata"
        atomic_write(paths["registry"], canonical(changed))
        partial = {key: paths[key] for key in ("registry", "index")}
        status = inspect(partial)
        self.assertTrue(any(item["reason"] == "stale_hash" for item in status["blockers"]))
        self.assertEqual(query("dossier", partial, {"q": "Luma"})["error"], "stale_pipeline_inputs")
        paths["registry"].write_bytes(b'{"schema_version": "1.0", "schema_version": "1.0"}')
        malformed = inspect(paths)
        self.assertIn({"layer": "registry", "reason": "invalid_json"}, malformed["blockers"])
        self.assertNotIn(str(self.base), json.dumps(malformed))

    def test_stale_builder_refuses_before_writing_output(self):
        self.start()
        index = self.base / "index.json"
        groups = self.base / "groups.json"
        output = self.base / "dossiers.json"
        build_entity_index(self.registry_path, self.inputs, index, synthetic=True)
        build_entity_groups(index, groups)
        registry = load_layer("registry", self.registry_path)
        registry["works"][0]["title"] = "Changed"
        atomic_write(self.registry_path, canonical(registry))
        with self.assertRaises(JebError):
            build_entity_dossiers(self.registry_path, index, groups, output)
        self.assertFalse(output.exists())

    def test_real_pagination_and_query_errors(self):
        self.start()
        step(self.workspace, synthetic=True)
        values, _, _ = published_snapshot(self.workspace, synthetic=True)
        prototype = values["registry"]["relations"][0]
        values["registry"]["relations"] = [
            {**prototype, "id": f"relation-{number:04}"} for number in range(620)
        ]
        file = self.base / "large-registry.json"
        atomic_write(file, canonical(values["registry"]))
        result = query("relations", {"registry": file}, {"limit": "999999"})
        self.assertEqual(
            (result["total"], len(result["results"]), result["truncated"]), (620, 500, True)
        )
        next_page = query("relations", {"registry": file}, {"limit": "500", "offset": "500"})
        self.assertEqual(len(next_page["results"]), 120)
        for invalid in ("NaN", "Infinity", "0", "-1", "1.5"):
            self.assertEqual(
                query("relations", {"registry": file}, {"limit": invalid})["error"], "invalid_query"
            )
        self.assertEqual(query("dossier", {}, {})["error"], "invalid_query")

    def test_snapshot_tampering_is_rejected(self):
        self.start()
        step(self.workspace, synthetic=True)
        head = read_json(self.workspace / "HEAD.json")
        path = self.workspace / "snapshots" / head["snapshot_id"] / "dossiers.json"
        original = path.read_bytes()
        path.write_bytes(original + b" ")
        result = query("dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True)
        self.assertEqual(result["error"], "invalid_historical_input")
        self.assertEqual(result["entities"], [])

    def test_cli_dossier_runs_without_project_and_returns_exact_snapshot(self):
        demo = create_demo(self.base / "demo", synthetic=True)
        command = [
            sys.executable,
            "-B",
            "-m",
            "jeb",
            "--root",
            str(self.base / "not-a-project"),
            "--synthetic",
            "historical",
            "dossier",
            "--workspace",
            demo["workspace"],
            "--query",
            "Luma",
        ]
        result = subprocess.run(command, capture_output=True, encoding="utf-8", check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["snapshot_id"], demo["pipeline"]["snapshot_id"])
        self.assertEqual(payload["entities"][0]["candidate_count"], 4)
        self.assertFalse(payload["authoritative"])

    def test_query_stays_on_one_snapshot_when_a_writer_publishes_during_the_read(self):
        self.start()
        old_head = read_json(self.workspace / "HEAD.json")
        advanced = False

        def publish_after_read(*args, **kwargs):
            nonlocal advanced
            result = load_published(*args, **kwargs)
            if not advanced:
                advanced = True
                step(self.workspace, synthetic=True, max_artifacts=3)
            return result

        with patch("jeb.historical_pipeline.load_published", side_effect=publish_after_read):
            result = query("dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True)
        self.assertEqual(result["snapshot_id"], old_head["snapshot_id"])
        self.assertEqual(result["pipeline"]["snapshot_id"], result["snapshot_id"])
        self.assertEqual(result["pipeline"]["candidate_count"], 0)
        self.assertEqual(result["entities"], [])
        current = query("dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True)
        self.assertNotEqual(current["snapshot_id"], result["snapshot_id"])
        self.assertEqual(current["entities"][0]["candidate_count"], 2)

    def test_malformed_heads_return_path_free_errors(self):
        self.start()
        head = read_json(self.workspace / "HEAD.json")
        for invalid in (None, [], {}, {**head, "snapshot_id": 4}, {**head, "snapshot_id": []}):
            with self.subTest(head=invalid):
                atomic_write(self.workspace / "HEAD.json", canonical(invalid))
                result = query(
                    "dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True
                )
                self.assertEqual(result["error"], "invalid_historical_input")
                self.assertEqual(result["entities"], [])
                self.assertNotIn(str(self.base), json.dumps(result))

    def test_combined_dossier_paginates_works_and_rejects_oversized_responses(self):
        demo = create_demo(self.base / "demo", synthetic=True)
        workspace = Path(demo["workspace"])
        for offset, work in ((0, "MAT"), (1, "MRK")):
            result = query(
                "dossier",
                {},
                {"q": "Luma", "limit": "1", "offset": str(offset)},
                workspace=workspace,
                synthetic=True,
            )
            self.assertEqual(result["works_total"], 2)
            self.assertEqual([item["id"] for item in result["works"]], [work])
        full = query("dossier", {}, {"q": "Luma"}, workspace=workspace, synthetic=True)
        budget = len(canonical(full)) - 1
        with patch("jeb.historical_query.MAX_RESPONSE_BYTES", budget):
            oversized = query("dossier", {}, {"q": "Luma"}, workspace=workspace, synthetic=True)
            self.assertEqual(oversized["error"], "response_limit_exceeded")
            self.assertNotIn("entities", oversized)
            self.assertLessEqual(len(canonical(oversized)), budget)
            smaller = query(
                "dossier",
                {},
                {"q": "Luma", "locator_limit": "1"},
                workspace=workspace,
                synthetic=True,
            )
            self.assertNotIn("error", smaller)
            self.assertEqual(smaller["entities"][0]["locators_total"], 4)

    def test_work_and_availability_filters_apply_to_the_same_artifact(self):
        demo = create_demo(self.base / "demo", synthetic=True)
        values, _, _ = published_snapshot(Path(demo["workspace"]), synthetic=True)
        edition_work = {item["id"]: item["work_id"] for item in values["registry"]["editions"]}
        for artifact in values["registry"]["artifacts"]:
            if edition_work[artifact["edition_id"]] == "MRK":
                artifact["status"] = "discovered"
        values["index"]["registry_sha256"] = digest(values["registry"])
        values["groups"] = entity_groups(values["index"])
        values["dossiers"] = entity_dossiers(values["registry"], values["index"], values["groups"])
        paths = {}
        for name, value in values.items():
            paths[name] = self.base / f"{name}-filtered.json"
            atomic_write(paths[name], canonical(value))
        missing = query(
            "dossier", paths, {"q": "Luma", "work": "MAT", "availability": "discovered"}
        )
        self.assertEqual(missing["entities_total"], 0)
        all_luma = query("dossier", paths, {"q": "Luma"})
        detail = query(
            "detail",
            paths,
            {
                "id": all_luma["entities"][0]["id"],
                "work": "MRK",
                "availability": "discovered",
            },
        )
        self.assertEqual(detail["candidate_count"], 1)
        self.assertEqual([source["work_id"] for source in detail["sources"]], ["MRK"])

    def test_resealed_pending_entries_cannot_reference_foreign_or_completed_artifacts(self):
        self.start()
        step(self.workspace, synthetic=True, max_artifacts=3)
        original, _, _ = published_snapshot(self.workspace, synthetic=True)
        complete_id = original["index"]["candidates"][0]["artifact_id"]
        for artifact_id in ("foreign-artifact", complete_id):
            values = copy.deepcopy(original)
            values["index"]["pending"].append(
                {
                    "artifact_id": artifact_id,
                    "status": "pending",
                    "reason": "synthetic-test",
                }
            )
            values["groups"]["index_sha256"] = digest(values["index"])
            values["dossiers"]["index_sha256"] = digest(values["index"])
            values["dossiers"]["groups_sha256"] = digest(values["groups"])
            paths = {}
            for name, value in values.items():
                paths[name] = self.base / f"{name}-invalid.json"
                atomic_write(paths[name], canonical(value))
            result = query("dossier", paths, {"q": "Luma"})
            self.assertEqual(result["error"], "invalid_historical_input")
            self.assertEqual(result["entities"], [])
