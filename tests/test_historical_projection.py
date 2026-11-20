from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from jeb.core import JebError, atomic_write, canonical, digest, read_json, sha256
from jeb.historical import build_registry, extract_artifact, load_layer
from jeb.historical_pipeline import (
    initialize,
    pipeline_status,
    step,
    store_projection,
    verify_projection,
)
from jeb.historical_query import query


def synthetic_pdf(sentence: str = "Luma sees Nera.") -> bytes:
    """A complete, original one-page PDF; no libraries or historical material."""
    lines = ["SYNTHETIC SOFTWARE FIXTURE", sentence, "svjet vrjeme covik razumit"]
    stream = b"BT /F1 12 Tf 72 720 Td\n"
    for index, line in enumerate(lines):
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream += (b"0 -20 Td " if index else b"") + f"({escaped}) Tj\n".encode("ascii")
    stream += b"ET\n"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"endstream",
    ]
    raw = b"%PDF-1.4\n% SYNTHETIC ORIGINAL TEST FIXTURE\n"
    offsets = [0]
    for number, body in enumerate(objects, 1):
        offsets.append(len(raw))
        raw += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(raw)
    raw += f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode()
    raw += b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:])
    raw += f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return raw


class HistoricalProjectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="jeb-projection-test-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.inputs = self.base / "inputs"
        self.inputs.mkdir()
        self.workspace = self.base / "pipeline"

    def begin(self, names=("one.pdf",)):
        catalog = self.base / "catalog.json"
        atomic_write(
            catalog,
            canonical(
                {
                    "books": [
                        {
                            "id": "MAT",
                            "title": "Synthetic MAT fixture",
                            "findings": [
                                {
                                    "id": f"synthetic-{index}",
                                    "edition_title": "Synthetic edition",
                                    "translator": "Synthetic test contributor",
                                    "local_file": name,
                                }
                                for index, name in enumerate(names)
                            ],
                        }
                    ]
                }
            ),
        )
        registry = self.base / "registry.json"
        build_registry(catalog, registry)
        for name in names:
            (self.inputs / name).write_bytes(synthetic_pdf())
        initialize(registry, self.inputs, self.workspace, synthetic=True)
        return load_layer("registry", registry)

    @contextmanager
    def projected(self, raw, *, executable=sys.executable):
        with (
            patch("jeb.historical.shutil.which", return_value=executable),
            patch("jeb.historical.pdf_projection", return_value=raw),
        ):
            yield

    def cached(self):
        head = read_json(self.workspace / "HEAD.json")
        manifest = read_json(self.workspace / "snapshots" / head["snapshot_id"] / "manifest.json")
        cache_hash = manifest["extractions"][0]["cache_sha256"]
        return cache_hash, read_json(self.workspace / "cache" / f"{cache_hash}.json")

    def write_cache(self, value):
        cache_hash = digest(value)
        atomic_write(self.workspace / "cache" / f"{cache_hash}.json", canonical(value))
        return cache_hash

    def fingerprint(self):
        return {
            str(path.relative_to(self.workspace)): sha256(path.read_bytes())
            for path in self.workspace.rglob("*")
            if path.is_file()
        }

    def test_exact_unicode_projection_and_locators_survive_missing_source_and_tool(self):
        self.begin()
        raw = "SYNTHETIC\r\nLuma vidi Z\u030cana. svjet vrjeme covik razumit.\r\n".encode()
        with self.projected(raw):
            step(self.workspace, synthetic=True)
        cache_hash, cached = self.cached()
        self.assertEqual(cached["schema_version"], "2.0")
        self.assertTrue(cached["synthetic"])
        self.assertFalse(cached["releasable"])
        self.assertEqual(
            cached["projection_file"], {"sha256": sha256(raw), "byte_length": len(raw)}
        )
        retained = self.workspace / "projections" / f"{sha256(raw)}.txt"
        self.assertEqual(retained.read_bytes(), raw)
        (self.inputs / "one.pdf").unlink()
        before = self.fingerprint()
        with patch("jeb.historical.pdf_projection", side_effect=AssertionError("No tool allowed")):
            verified = verify_projection(self.workspace, cache_hash, synthetic=True)
            dossier = query("dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True)
        self.assertEqual(verified["verified_candidates"], len(cached["candidates"]))
        locator = dossier["entities"][0]["locators"][0]
        self.assertEqual(raw.decode()[locator["start"] : locator["end"]], "Luma")
        self.assertTrue(locator["projection_retained"])
        self.assertEqual(locator["locator_verification"], "retained_projection")
        self.assertEqual(before, self.fingerprint())
        with self.assertRaises(JebError):
            verify_projection(self.workspace, cache_hash)

    def test_tool_output_and_input_changes_preserve_prior_cache_and_projection(self):
        self.begin()
        original = b"SYNTHETIC\nLuma sees Nera.\n"
        changed = b"SYNTHETIC\nSela sees Nera.\n"
        with self.projected(original):
            step(self.workspace, synthetic=True)
        old_hash, old = self.cached()
        old_files = self.fingerprint()
        adapter = self.base / "synthetic-adapter-v2"
        adapter.write_bytes(b"SYNTHETIC EXECUTABLE IDENTITY ONLY; NOT EXECUTED")
        with self.projected(changed, executable=str(adapter)):
            step(self.workspace, synthetic=True, refresh=True)
        new_hash, new = self.cached()
        self.assertNotEqual(old_hash, new_hash)
        self.assertNotEqual(old["provenance"]["adapter"], new["provenance"]["adapter"])
        self.assertEqual(old["provenance"]["source_sha256"], new["provenance"]["source_sha256"])
        old_name = next(item for item in old["candidates"] if item["surface"] == "Luma")
        new_name = next(item for item in new["candidates"] if item["surface"] == "Sela")
        self.assertEqual(old_name["start"], new_name["start"])
        self.assertNotEqual(old_name["id"], new_name["id"])
        (self.inputs / "one.pdf").write_bytes(synthetic_pdf("Nera sees Sela."))
        with self.projected(b"SYNTHETIC\nNera sees Sela.\n"):
            step(self.workspace, synthetic=True, refresh=True)
        newest_hash, newest = self.cached()
        self.assertNotEqual(
            old["provenance"]["source_sha256"], newest["provenance"]["source_sha256"]
        )
        for cache_hash in (old_hash, new_hash, newest_hash):
            self.assertNotIn("error", verify_projection(self.workspace, cache_hash, synthetic=True))
        for name, fingerprint in old_files.items():
            if name not in {"HEAD.json", "pipeline.json"}:
                self.assertEqual(sha256((self.workspace / name).read_bytes()), fingerprint)

    def test_legacy_cache_is_not_backfilled_or_resealed_on_read(self):
        registry = self.begin()
        with self.projected(b"SYNTHETIC\nLuma."):
            legacy = extract_artifact(registry["artifacts"][0], self.inputs, synthetic=True)
        with patch("jeb.historical_pipeline.extract_artifact", return_value=legacy):
            step(self.workspace, synthetic=True)
        old_hash, old = self.cached()
        before = self.fingerprint()
        self.assertNotIn("schema_version", old)
        self.assertEqual(
            verify_projection(self.workspace, old_hash, synthetic=True)["error"],
            "projection_not_retained",
        )
        self.assertFalse((self.workspace / "projections").exists())
        self.assertEqual(before, self.fingerprint())
        with self.projected(b"SYNTHETIC\nLuma."):
            step(self.workspace, synthetic=True, refresh=True)
        new_hash, _ = self.cached()
        self.assertNotEqual(old_hash, new_hash)
        self.assertEqual(read_json(self.workspace / "cache" / f"{old_hash}.json"), old)
        self.assertEqual(
            verify_projection(self.workspace, old_hash, synthetic=True)["error"],
            "projection_not_retained",
        )
        self.assertNotIn("error", verify_projection(self.workspace, new_hash, synthetic=True))

    def test_missing_or_tampered_blob_blocks_queries_without_reextracting(self):
        self.begin()
        raw = b"SYNTHETIC Luma."
        with self.projected(raw):
            step(self.workspace, synthetic=True)
        cache_hash, _ = self.cached()
        blob = self.workspace / "projections" / f"{sha256(raw)}.txt"
        for tampered in (raw + b" ", b"X" + raw[1:], None):
            with self.subTest(tampered=tampered):
                if tampered is None:
                    blob.unlink()
                else:
                    blob.write_bytes(tampered)
                with patch(
                    "jeb.historical.pdf_projection", side_effect=AssertionError("No repair")
                ):
                    with self.assertRaises((JebError, OSError)):
                        verify_projection(self.workspace, cache_hash, synthetic=True)
                    result = query(
                        "dossier", {}, {"q": "Luma"}, workspace=self.workspace, synthetic=True
                    )
                self.assertEqual(result["error"], "invalid_historical_input")
                self.assertEqual(result["entities"], [])
                self.assertNotIn(str(self.base), json.dumps(result))
        blob.write_bytes(raw)
        self.assertNotIn("error", verify_projection(self.workspace, cache_hash, synthetic=True))

    def test_resealed_candidates_must_match_retained_unicode_spans(self):
        self.begin()
        with self.projected(b"SYNTHETIC\nLuma."):
            step(self.workspace, synthetic=True)
        _, cached = self.cached()
        for start in (10, 10000):
            bad = copy.deepcopy(cached)
            candidate = next(item for item in bad["candidates"] if item["surface"] == "Luma")
            candidate.update(start=start, end=start + 4, surface="Sela")
            candidate["evidence"].update(start=start, end=start + 4, exact="Sela")
            with self.assertRaisesRegex(JebError, "Candidate differs"):
                verify_projection(self.workspace, self.write_cache(bad), synthetic=True)

    def test_size_utf8_hash_length_and_link_guards(self):
        self.begin()
        raw = b"SYNTHETIC Luma."
        with self.projected(raw):
            step(self.workspace, synthetic=True)
        cache_hash, cached = self.cached()
        with patch("jeb.historical_pipeline.MAX_SOURCE_BYTES", 4):
            with self.assertRaises(JebError):
                store_projection(self.workspace, raw)
            with self.assertRaises(JebError):
                verify_projection(self.workspace, cache_hash, synthetic=True)
        with patch.object(Path, "is_junction", return_value=True):
            with self.assertRaises(JebError):
                store_projection(self.workspace, raw)
        for change in ("hash", "length", "utf8"):
            bad = copy.deepcopy(cached)
            if change == "hash":
                bad["projection_file"]["sha256"] = "0" * 64
            elif change == "length":
                bad["projection_file"]["byte_length"] += 1
            else:
                invalid = b"\xff\xfe"
                projection_hash = sha256(invalid)
                (self.workspace / "projections" / f"{projection_hash}.txt").write_bytes(invalid)
                bad["projection_file"] = {"sha256": projection_hash, "byte_length": len(invalid)}
                bad["provenance"]["projection_sha256"] = projection_hash
            with self.subTest(change=change), self.assertRaises((JebError, UnicodeError)):
                verify_projection(self.workspace, self.write_cache(bad), synthetic=True)

    def test_projection_write_failure_recovers_from_processing_checkpoint(self):
        self.begin()
        old_head = (self.workspace / "HEAD.json").read_bytes()

        def fail_blob(path, *args, **kwargs):
            if path.parent.name == "projections":
                raise OSError("SYNTHETIC storage failure")
            return atomic_write(path, *args, **kwargs)

        with (
            self.projected(b"SYNTHETIC Luma."),
            patch("jeb.historical_pipeline.atomic_write", side_effect=fail_blob),
        ):
            with self.assertRaises(OSError):
                step(self.workspace, synthetic=True)
        self.assertEqual((self.workspace / "HEAD.json").read_bytes(), old_head)
        self.assertEqual(pipeline_status(self.workspace, synthetic=True)["queue"]["processing"], 1)
        with self.projected(b"SYNTHETIC Luma."):
            self.assertEqual(step(self.workspace, synthetic=True)["queue"]["complete"], 1)
        cache_hash, _ = self.cached()
        self.assertNotIn("error", verify_projection(self.workspace, cache_hash, synthetic=True))

    def test_identical_blobs_are_deduplicated_and_snapshot_budget_is_enforced(self):
        self.begin(("one.pdf", "two.pdf"))
        raw = b"SYNTHETIC Luma."
        head = (self.workspace / "HEAD.json").read_bytes()
        with (
            self.projected(raw),
            patch("jeb.historical_pipeline.MAX_RETAINED_PROJECTION_BYTES", len(raw) - 1),
        ):
            with self.assertRaisesRegex(JebError, "aggregate limit"):
                step(self.workspace, synthetic=True)
        self.assertEqual((self.workspace / "HEAD.json").read_bytes(), head)
        self.assertTrue(pipeline_status(self.workspace, synthetic=True)["publication_pending"])
        with (
            patch("jeb.historical.pdf_projection", side_effect=AssertionError("Use cache")),
            patch("jeb.historical_pipeline.MAX_RETAINED_PROJECTION_BYTES", len(raw)),
        ):
            self.assertEqual(step(self.workspace, synthetic=True)["processed"], 0)
        self.assertEqual(len(list((self.workspace / "projections").iterdir())), 1)

    def test_retention_is_never_called_for_unreviewed_real_sources(self):
        registry = self.begin()
        with patch(
            "jeb.historical_pipeline.store_projection", side_effect=AssertionError("No retention")
        ):
            result = extract_artifact(
                registry["artifacts"][0],
                self.inputs,
                synthetic=False,
                projection_sink=lambda raw: store_projection(self.workspace, raw),
            )
        self.assertEqual(result["reason"], "source_review_required")
        self.assertFalse((self.workspace / "projections").exists())

    @unittest.skipUnless(shutil.which("pdftotext"), "Optional local pdftotext is not installed")
    def test_original_pdf_round_trip_with_real_local_tool_and_cli(self):
        self.begin()
        self.assertEqual(step(self.workspace, synthetic=True)["queue"]["complete"], 1)
        cache_hash, cached = self.cached()
        raw = (
            self.workspace / "projections" / f"{cached['projection_file']['sha256']}.txt"
        ).read_bytes()
        actual = subprocess.run(
            [shutil.which("pdftotext"), "-enc", "UTF-8", str(self.inputs / "one.pdf"), "-"],
            capture_output=True,
            check=True,
            timeout=20,
        ).stdout
        self.assertEqual(raw, actual)
        self.assertIn(b"SYNTHETIC SOFTWARE FIXTURE", raw)
        self.assertIn(b"svjet vrjeme covik razumit", raw)
        (self.inputs / "one.pdf").unlink()
        before = self.fingerprint()
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "jeb",
                "--synthetic",
                "historical",
                "projection-verify",
                "--workspace",
                str(self.workspace),
                "--cache-sha256",
                cache_hash,
            ],
            cwd=self.base,
            capture_output=True,
            encoding="utf-8",
            check=False,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["projection_retained"])
        self.assertEqual(before, self.fingerprint())
