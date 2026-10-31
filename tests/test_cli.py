from __future__ import annotations

import json
import subprocess
import sys

from tests.support import REPO, WorkspaceTest


class CliTests(WorkspaceTest):
    def cli(self, *args, root=None, synthetic=True):
        command = [sys.executable, "-m", "jeb", "--root", str(root or self.project.root)]
        if synthetic:
            command.append("--synthetic")
        return subprocess.run(
            command + list(args), capture_output=True, encoding="utf-8", check=False
        )

    def test_help_matches_implemented_interfaces(self):
        result = self.cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("normalize", result.stdout)
        self.assertIn("batch", result.stdout)
        self.assertNotIn("epub", result.stdout)

    def test_all_packaged_schemas_validate(self):
        result = self.cli("validate", "--stage", "schemas")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["valid_schemas"], 26)

    def test_production_audit_is_successful_inspection_without_clearance(self):
        result = self.cli("sources", "audit", root=REPO, synthetic=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["admitted_count"], 0)

    def test_excluded_fetch_is_exit_two_without_traceback(self):
        result = self.cli("fetch", "--source", "ebible-hrv-saric", root=REPO, synthetic=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("excluded", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_synthetic_root_requires_global_flag(self):
        result = self.cli("sources", "audit", synthetic=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--synthetic", result.stderr)

    def test_missing_source_argument_fails_clearly(self):
        result = self.cli("validate", "--stage", "normalized")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--source is required", result.stderr)

    def test_synthetic_release_cli_refuses(self):
        result = self.cli(
            "release", "check", "--source", self.source_id, "--edition", "jeb-synthetic-demo"
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Synthetic fixtures", result.stderr)

    def test_demo_reruns_reproducibly(self):
        first = self.cli("demo", root=self.base, synthetic=False)
        second = self.cli("demo", root=self.base, synthetic=False)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout)["real_biblical_segments"], 0)
