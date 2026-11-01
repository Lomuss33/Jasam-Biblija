from __future__ import annotations

import dataclasses
import io
import json
import os
import shutil
import subprocess
import sys
from types import SimpleNamespace
from unittest import skipUnless
from unittest.mock import patch

from jeb import workbench
from jeb.core import (
    JebError,
    Project,
    native_path,
    read_json,
    read_yaml,
    sha256,
    write_json,
)
from jeb.export import reader
from jeb.knowledge import validate_knowledge
from jeb.review import all_decisions
from tests import test_knowledge_packets as annotations
from tests import test_narrative_packets as narratives
from tests.support import REPO, WorkspaceTest


class WorkbenchTests(WorkspaceTest):
    def terminal(self, answers=""):
        output = io.StringIO()
        return workbench.Terminal(io.StringIO(answers), output), output

    def text_item(self):
        proposal = self.import_test_response()
        return next(
            item
            for item in workbench.saved_work(self.project)
            if item.key == proposal["proposal_id"]
        )

    def narrative_item(self):
        helper = narratives.NarrativePacketTests()
        helper.project, helper.source_id = self.project, self.source_id
        value = helper.response()
        from jeb.narrative_packets import import_response

        import_response(self.project, helper.returned(value))
        return next(item for item in workbench.saved_work(self.project) if item.kind == "narrative")

    def annotation_item(self):
        helper = annotations.KnowledgePacketTests()
        helper.project, helper.source_id = self.project, self.source_id
        value = helper.response()
        from jeb.knowledge_packets import import_response

        import_response(self.project, helper.returned(value))
        return next(
            item for item in workbench.saved_work(self.project) if item.kind == "annotations"
        )

    def cli(self, *arguments, root=None, input_text="", synthetic=True):
        args = [sys.executable, "-m", "jeb", "--root", str(root or self.project.root)]
        if synthetic:
            args.append("--synthetic")
        return subprocess.run(
            args + ["work", *arguments],
            input=input_text,
            capture_output=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )

    def test_status_distinguishes_real_blockers_and_synthetic_workspace_without_writes(self):
        terminal, output = self.terminal()
        workbench.status(Project(REPO), terminal)
        self.assertIn("Sources eligible for ingestion here: 0", output.getvalue())
        self.assertIn("Real text editing is blocked", output.getvalue())
        self.assertIn("GEN, MAT, MRK, LUK, JHN", output.getvalue())
        terminal, output = self.terminal()
        workbench.status(self.project, terminal)
        self.assertIn("SYNTHETIC EXAMPLE", output.getvalue())
        self.assertIn("cannot be released", output.getvalue())
        self.assertEqual(all_decisions(self.project), {})
        self.assertFalse(self.project.path("reports/generated").exists())

    def test_source_blockers_are_readable_offline_and_unknown_source_fails(self):
        terminal, output = self.terminal()
        with patch("urllib.request.urlopen", side_effect=AssertionError("No network")):
            workbench.source_gaps(Project(REPO), terminal, "crosswire-srkdijekav")
        self.assertIn("edition year", output.getvalue())
        self.assertIn("publication place", output.getvalue())
        self.assertIn("digital source", output.getvalue())
        self.assertIn("No source was downloaded or cleared", output.getvalue())
        with self.assertRaisesRegex(JebError, "Unknown source"):
            workbench.source_gaps(self.project, terminal, "invented")

    def test_queue_reads_text_source_from_exact_batch_and_never_chooses_latest(self):
        first = self.text_item()
        changed = self.response()
        changed["tool"]["name"] = "Another original synthetic test candidate"
        self.import_test_response(changed)
        items = workbench.saved_work(self.project)
        self.assertEqual(len(items), 2)
        self.assertTrue(
            all(item.source_id == self.source_id and not item.problem for item in items)
        )
        self.assertIn(first, items)
        terminal, output = self.terminal()
        self.assertEqual(workbench.show_queue(self.project, terminal), items)
        self.assertIn("no automatic selection", output.getvalue())
        self.assertIn("checked again", output.getvalue())

    def test_all_three_report_types_delegate_exact_identities_and_preserve_data(self):
        items = [self.text_item(), self.annotation_item(), self.narrative_item()]
        before_reader = reader(self.project, self.source_id, "preview")
        before = {
            p.relative_to(self.project.root).as_posix(): sha256(native_path(p).read_bytes())
            for p in self.project.root.rglob("*")
            if p.is_file()
        }
        outputs = []
        for item in items:
            output = workbench.export_report(self.project, item)
            outputs.append(output)
            self.assertTrue(output.startswith("reports/generated/work/"))
            data = native_path(self.project.path(output)).read_text("utf-8")
            self.assertIn("Synthetic fixture; not scripture", data)
            self.assertEqual(workbench.export_report(self.project, item), output)
        after = {
            p.relative_to(self.project.root).as_posix(): sha256(native_path(p).read_bytes())
            for p in self.project.root.rglob("*")
            if p.is_file()
            and not p.relative_to(self.project.root).as_posix().startswith("reports/generated/")
        }
        self.assertEqual(after, before)
        self.assertEqual(len(outputs), 3)
        self.assertEqual(validate_knowledge(self.project, self.books()), {})
        self.assertEqual(all_decisions(self.project), {})
        self.assertEqual(reader(self.project, self.source_id, "preview"), before_reader)
        self.assertFalse(
            any(
                p.name.startswith(".inspect-")
                for p in self.project.path("reports/generated/work").iterdir()
            )
        )

    def test_changed_file_after_selection_is_rejected_without_switching_candidates(self):
        item = self.narrative_item()
        path = self.project.path(item.path)
        value = read_json(path)
        value["limitations"].append("Modified after the menu was displayed")
        write_json(path, value)
        with self.assertRaisesRegex(JebError, "changed after selection"):
            workbench.export_report(self.project, item)
        self.assertFalse(self.project.path("reports/generated/work").exists())

    def test_selected_work_cannot_read_or_publish_outside_its_project(self):
        item = self.text_item()
        altered = dataclasses.replace(item, path="../outside.json")
        with self.assertRaisesRegex(JebError, "escapes project"):
            workbench.export_report(self.project, altered)
        self.assertFalse(self.project.path("reports/generated/work").exists())

    def test_stale_policy_and_source_gates_still_block_selected_reports(self):
        for item in (self.text_item(), self.annotation_item(), self.narrative_item()):
            registry_path = self.project.path("sources/registry.yaml")
            original = registry_path.read_bytes()
            registry = read_yaml(registry_path)
            registry["sources"][0]["status"] = "needs_review"
            write_json(registry_path, registry)
            with self.assertRaisesRegex(JebError, "needs_review"):
                workbench.export_report(self.project, item)
            registry_path.write_bytes(original)
        item = next(item for item in workbench.saved_work(self.project) if item.kind == "narrative")
        with self.project.path("docs/EDITORIAL_POLICY.md").open("a", encoding="utf-8") as stream:
            stream.write("\nTemporary changed test policy.\n")
        with self.assertRaisesRegex(JebError, "Stale or substituted"):
            workbench.export_report(self.project, item)
        self.assertEqual(list(self.project.path("reports/generated/work").glob("*.md")), [])

    def test_existing_report_with_human_notes_is_not_overwritten(self):
        item = self.text_item()
        output = workbench.export_report(self.project, item)
        path = self.project.path(output)
        path.write_text("Local human notes to preserve", "utf-8")
        with self.assertRaisesRegex(JebError, "Existing artifact differs"):
            workbench.export_report(self.project, item)
        self.assertEqual(path.read_text("utf-8"), "Local human notes to preserve")

    def test_malformed_and_mismatched_items_remain_visible_but_not_exportable(self):
        item = self.narrative_item()
        path = self.project.path(item.path)
        value = read_json(path)
        value["packet_id"] = "wrong-directory"
        write_json(path, value)
        broken = workbench.saved_work(self.project)
        self.assertEqual(len(broken), 1)
        self.assertTrue(broken[0].problem)
        with self.assertRaises(JebError):
            workbench.export_report(self.project, broken[0])
        terminal, output = self.terminal()
        workbench.show_queue(self.project, terminal)
        self.assertIn("BLOCKED", output.getvalue())
        self.assertNotIn(value["nodes"][0]["rationale"], output.getvalue())

    def test_unsafe_batch_ids_and_bounded_queue_do_not_escape_workspace(self):
        item = self.text_item()
        value = read_json(self.project.path(item.path))
        value["response"]["batch_id"] = "../outside"
        write_json(self.project.path(item.path), value)
        self.assertTrue(workbench.saved_work(self.project)[0].problem)
        with patch("jeb.workbench.MAX_ITEMS", 0), self.assertRaisesRegex(JebError, "100 saved"):
            workbench.saved_work(self.project)

    def test_review_number_selection_and_terminal_view_need_no_copied_hash(self):
        self.narrative_item()
        terminal, output = self.terminal("bad\n999\n1\nv\nq\n")
        workbench.choose_review(self.project, terminal)
        text = output.getvalue()
        self.assertIn("Enter one of the listed numbers", text)
        self.assertIn("Inspection report saved", text)
        self.assertIn("unsigned inspection handoff", text)
        self.assertIn("No decision or approval was recorded", text)
        self.assertEqual(all_decisions(self.project), {})

    def test_cancel_blank_and_eof_make_no_report_or_approval(self):
        self.text_item()
        for answers in ("", "\n", "0\n", "Q\n"):
            terminal, _ = self.terminal(answers)
            workbench.choose_review(self.project, terminal)
        self.assertFalse(self.project.path("reports/generated").exists())
        self.assertEqual(all_decisions(self.project), {})

    def test_terminal_view_neutralizes_control_sequences_and_stays_read_only(self):
        path = self.project.path("reports/control.md")
        path.parent.mkdir(exist_ok=True)
        payload = "covik\n\x1b[2Jpretend terminal command\x07\nsvjet"
        path.write_text(payload, "utf-8")
        terminal, output = self.terminal()
        workbench.view_report(self.project, "reports/control.md", terminal)
        self.assertIn("\\u001b[2J", output.getvalue())
        self.assertNotIn("\x1b", output.getvalue())
        self.assertNotIn("\x07", output.getvalue())
        self.assertEqual(path.read_text("utf-8"), payload)

    def test_demo_requires_explicit_selection_and_does_not_mix_real_workspace(self):
        home = Project(self.base)
        terminal, output = self.terminal()
        with self.assertRaisesRegex(JebError, "No demo workspace"):
            workbench.run(home, "queue", demo=True, terminal=terminal)
        synthetic = workbench.build_demo(home, terminal)
        self.assertTrue(synthetic.synthetic)
        self.assertFalse(home.synthetic)
        self.assertIn("NOT scripture", output.getvalue())
        self.assertEqual(workbench.existing_demo(home).root, synthetic.root)
        with self.assertRaisesRegex(JebError, "Already in a synthetic"):
            workbench.existing_demo(synthetic)
        self.assertEqual(all_decisions(synthetic), {})

    def test_menu_handles_wrong_choice_switches_demo_and_returns_to_real_context(self):
        # A real-context fixture with no eligible sources, separate from the synthetic workspace.
        (self.base / "sources").mkdir()
        write_json(self.base / "sources/registry.yaml", {"schema_version": "1.0", "sources": []})
        write_json(self.base / "sources/lock.json", {"schema_version": "1.0", "sources": []})
        home = Project(self.base)
        terminal, output = self.terminal("wrong\n6\n1\n7\n1\n0\n")
        self.assertEqual(workbench.run(home, terminal=terminal), 0)
        text = output.getvalue()
        self.assertIn("Choose a listed number", text)
        self.assertIn("SYNTHETIC EXAMPLE", text)
        self.assertIn("Real project workspace", text)
        self.assertIn("Demo ready", text)
        self.assertNotIn("Traceback", text)

    def test_menu_returns_to_tasks_after_a_blocked_review_without_fallback(self):
        item = self.text_item()
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        registry["sources"][0]["status"] = "needs_review"
        write_json(self.project.path("sources/registry.yaml"), registry)
        terminal, output = self.terminal("4\n1\n0\n")
        self.assertEqual(workbench.run(self.project, terminal=terminal), 0)
        self.assertIn("Task could not finish", output.getvalue())
        self.assertNotIn("Inspection report saved", output.getvalue())
        self.assertEqual(read_json(self.project.path(item.path))["review_state"], "proposed")

    def test_offline_check_runner_uses_exact_four_steps_and_stops_on_failure(self):
        terminal, output = self.terminal()
        with patch(
            "jeb.workbench.subprocess.run", return_value=SimpleNamespace(returncode=0)
        ) as execute:
            self.assertEqual(workbench.check(Project(REPO), terminal), 0)
            self.assertEqual(execute.call_count, 4)
            self.assertEqual(
                execute.call_args_list[-1].args[0],
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            )
            self.assertTrue(all(call.kwargs["cwd"] == REPO for call in execute.call_args_list))
            self.assertTrue(all("shell" not in call.kwargs for call in execute.call_args_list))
        terminal, output = self.terminal()
        with patch(
            "jeb.workbench.subprocess.run",
            side_effect=[SimpleNamespace(returncode=0), SimpleNamespace(returncode=1)],
        ) as execute:
            self.assertEqual(workbench.check(Project(REPO), terminal), 2)
            self.assertEqual(execute.call_count, 2)
        self.assertIn("Check 2 failed", output.getvalue())
        self.assertNotIn("All four offline checks passed", output.getvalue())

    def test_checks_refuse_missing_repo_or_dependency_and_report_timeouts(self):
        terminal, output = self.terminal()
        with self.assertRaisesRegex(JebError, "repository root"):
            workbench.check(self.project, terminal)
        with (
            patch("jeb.workbench.importlib.util.find_spec", return_value=None),
            self.assertRaisesRegex(JebError, "Ruff is missing"),
        ):
            workbench.check(Project(REPO), terminal)
        with (
            patch(
                "jeb.workbench.subprocess.run", side_effect=subprocess.TimeoutExpired("test", 600)
            ),
            self.assertRaisesRegex(JebError, "timed out"),
        ):
            workbench.check(Project(REPO), terminal)
        self.assertNotIn("All four offline checks passed", output.getvalue())

    def test_cli_human_output_is_separate_from_existing_json_api(self):
        result = self.cli("status")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SYNTHETIC EXAMPLE", result.stdout)
        self.assertFalse(result.stdout.startswith("{"))
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "jeb",
                "--root",
                str(self.project.root),
                "--synthetic",
                "sources",
                "audit",
            ],
            capture_output=True,
            encoding="utf-8",
        )
        self.assertEqual(json.loads(result.stdout)["admitted_count"], 1)
        result = self.cli(input_text="0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("human terminal tasks", result.stdout)

    def test_cli_unknown_tasks_and_non_opt_in_synthetic_roots_fail_without_tracebacks(self):
        for arguments, synthetic in ((["approve"], True), (["publish"], True), (["status"], False)):
            result = self.cli(*arguments, synthetic=synthetic)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)
        self.text_item()
        result = self.cli("review", input_text="1\n\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Inspection report saved", result.stdout)
        self.assertEqual(all_decisions(self.project), {})

    @skipUnless(os.name == "nt", "Windows repository launcher")
    def test_windows_launcher_uses_repo_venv_from_another_working_directory(self):
        command = f'"{os.environ.get("COMSPEC", "cmd.exe")}" /d /s /c ""{REPO / "jeb.cmd"}" status"'
        result = subprocess.run(
            command,
            cwd=self.base,
            input="",
            capture_output=True,
            encoding="utf-8",
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Real project workspace", result.stdout)
        self.assertIn(str(REPO), result.stdout)

    @skipUnless(os.name == "nt", "Windows repository launcher")
    def test_windows_launcher_missing_environment_explains_setup_without_installing(self):
        folder = self.base / "repo with spaces & punctuation"
        folder.mkdir()
        launcher = folder / "jeb.cmd"
        shutil.copyfile(REPO / "jeb.cmd", launcher)
        command = f'"{os.environ.get("COMSPEC", "cmd.exe")}" /d /s /c ""{launcher}" status"'
        result = subprocess.run(
            command,
            cwd=self.base,
            capture_output=True,
            encoding="utf-8",
            timeout=30,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("three setup commands in README", result.stdout)
        self.assertFalse((folder / ".venv").exists())
