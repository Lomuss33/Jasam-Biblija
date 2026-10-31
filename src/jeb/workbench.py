"""Small human terminal workflow over the existing exact-hash APIs."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from jeb.core import (
    JebError,
    Project,
    atomic_write,
    digest,
    file_id,
    native_path,
    read_bytes,
    read_json,
    require,
    sha256,
)
from jeb.source_assessment import inspect_source
from jeb.sources import audit

MAX_ITEMS = 100
CHECKS = (
    ("ruff", "check", "src", "tests"),
    ("ruff", "format", "--check", "src", "tests"),
    ("jeb", "validate", "--stage", "schemas"),
    ("unittest", "discover", "-s", "tests", "-v"),
)


def visible(text: str) -> str:
    """Display data without passing terminal escape/control sequences through."""
    return "".join(c if c.isprintable() or c == "\n" else f"\\u{ord(c):04x}" for c in text)


class Terminal:
    def __init__(self, input_stream: TextIO | None = None, output: TextIO | None = None):
        self.input = input_stream if input_stream is not None else sys.stdin
        self.output = output if output is not None else sys.stdout

    def say(self, text=""):
        self.output.write(visible(str(text)) + "\n")
        self.output.flush()

    def ask(self, prompt):
        self.say(prompt)
        line = self.input.readline()
        return line.strip() if line else None


@dataclass(frozen=True)
class SavedWork:
    kind: str
    key: str
    source_id: str
    path: str
    sha256: str
    problem: str = ""


def saved_work(project: Project) -> list[SavedWork]:
    """Read metadata only. Selection repeats full validation; nothing is 'latest'."""
    found = []
    root = native_path(project.root)
    for kind, pattern in (
        ("text", "data/proposals/*.json"),
        ("annotations", "data/knowledge-proposals/*/responses/*.json"),
        ("narrative", "data/narrative-proposals/*/responses/*.json"),
    ):
        for path in sorted(root.glob(pattern)):
            require(
                len(found) < MAX_ITEMS,
                "More than 100 saved items; use the explicit review commands",
            )
            relative = path.relative_to(root).as_posix()
            key, source_id, identity = path.stem, "unknown", ""
            try:
                value = read_json(project.path(relative))
                require(isinstance(value, dict), "Expected a saved-work object")
                if kind == "text":
                    key = value.get("proposal_id")
                    require(key == path.stem, "Proposal filename/ID mismatch")
                else:
                    # Passage research uses another workflow; this menu lists editorial drafts.
                    if kind == "annotations" and value.get("task") == "research":
                        continue
                    key = value.get("packet_id")
                    require(key == path.parent.parent.name, "Packet directory/ID mismatch")
                    require(path.stem == digest(value), "Response filename/hash mismatch")
                    require(
                        value.get("task")
                        == {"annotations": "annotate", "narrative": "narrative"}[kind],
                        "Wrong saved-response task",
                    )
                require(isinstance(key, str), "Missing saved-work ID")
                file_id(key)
                source_id = value.get("source_id")
                require(isinstance(source_id, str), "Missing source ID")
                file_id(source_id)
                identity = digest(value)
                problem = ""
            except (ValueError, OSError, UnicodeError):
                # Schema/error messages can contain source prose. Keep the queue metadata-only.
                problem = "Unreadable or mismatched saved metadata; use the explicit validator for details"
                key, source_id = path.stem, "unknown"
            found.append(SavedWork(kind, key, source_id, relative, identity, problem))
    return sorted(found, key=lambda item: (item.kind, item.key, item.sha256, item.path))


def show_queue(project: Project, terminal: Terminal) -> list[SavedWork]:
    items = saved_work(project)
    terminal.say("Saved review work (no automatic selection or approval)")
    if not items:
        terminal.say("No saved editorial drafts in this workspace.")
        if not project.synthetic:
            terminal.say("Try the isolated example: .\\jeb.cmd demo, then .\\jeb.cmd --demo review")
        return items
    terminal.say("Source, policy and exact content are checked again when you choose an item.")
    for index, item in enumerate(items, 1):
        label = "BLOCKED: " + item.problem if item.problem else "saved; check on selection"
        terminal.say(f"{index}. {item.kind} | {item.key} | source: {item.source_id} | {label}")
        # A short discriminator distinguishes competing responses; users never need to copy it.
        terminal.say(f"   Saved response: {item.sha256[:12] or 'invalid'}")
    return items


def status(project: Project, terminal: Terminal) -> None:
    result = audit(project)
    terminal.say("JEB terminal workspace")
    terminal.say(
        "SYNTHETIC EXAMPLE — NOT SCRIPTURE; cannot be released"
        if project.synthetic
        else "Real project workspace"
    )
    terminal.say(f"Folder: {project.root}")
    terminal.say("Collection: " + ", ".join(project.collection["books"]))
    terminal.say(f"Python: {sys.version.split()[0]}")
    terminal.say(f"Sources eligible for ingestion here: {result['admitted_count']}")
    if not project.synthetic and result["admitted_count"] == 0:
        terminal.say(
            "Real text editing is blocked: exact edition, digital lineage and rights evidence are still needed."
        )
    for source in result["sources"]:
        terminal.say(f"  {source['source_id']}: {source['status']}")
    items = saved_work(project)
    terminal.say(f"Saved review items: {len(items)} (inspection work, not a count of approvals)")
    terminal.say(
        "This task menu never approves text, changes source clearance, pushes or publishes."
    )


def source_gaps(project: Project, terminal: Terminal, source_id: str | None = None) -> None:
    sources = audit(project)["sources"]
    require(
        source_id is None or source_id in {s["source_id"] for s in sources}, "Unknown source ID"
    )
    for source in sources:
        if source_id is not None and source["source_id"] != source_id:
            continue
        result = inspect_source(project, source["source_id"])
        terminal.say(f"\n{source['source_id']}: {source['status']}")
        if result["admitted"]:
            terminal.say(
                "  Eligible for this workspace's configured scope; not publication approval."
            )
        else:
            for blocker in result["admission_blockers"]:
                terminal.say("  - " + blocker["detail"])
    terminal.say(
        "\nNo source was downloaded or cleared. Existing evidence questions: docs/sources/CROSSWIRE_QUESTIONS.md"
    )


def export_report(project: Project, item: SavedWork) -> str:
    require(not item.problem, item.problem or "Invalid saved work")
    require(
        digest(read_json(project.path(item.path))) == item.sha256,
        "Saved work changed after selection; list it again and choose explicitly",
    )
    parent = project.path("reports/generated/work")
    native_path(parent).mkdir(parents=True, exist_ok=True)
    # Some older report APIs overwrite derived files. Render privately, then publish immutably.
    with tempfile.TemporaryDirectory(prefix=".inspect-", dir=native_path(parent)) as temporary:
        scratch = f"reports/generated/work/{Path(temporary).name}/review.md"
        if item.kind == "text":
            from jeb import review

            review.report(project, item.key, scratch)
        elif item.kind == "annotations":
            from jeb import knowledge_review

            knowledge_review.report(project, item.key, item.sha256, scratch)
        else:
            from jeb import narrative_review

            require(item.kind == "narrative", "Unknown review item kind")
            narrative_review.report(project, item.key, item.sha256, scratch)
        payload = read_bytes(project.path(scratch), 2 * 1024 * 1024)
        output = f"reports/generated/work/{item.kind}-{item.key[:32]}-{sha256(payload)[:16]}.md"
        atomic_write(project.path(output), payload, replace=False)
    return output


def view_report(project: Project, output: str, terminal: Terminal) -> None:
    text = read_bytes(project.path(output), 2 * 1024 * 1024).decode("utf-8", errors="strict")
    lines = text.splitlines()
    terminal.say("Read-only report view; terminal control characters are displayed as escapes.")
    for index in range(0, len(lines), 35):
        terminal.say("\n".join(lines[index : index + 35]))
        if index + 35 < len(lines):
            choice = terminal.ask("Enter = next page; q = stop viewing")
            if choice is None or choice.lower() in ("q", "0"):
                break


def choose_review(project: Project, terminal: Terminal) -> None:
    items = show_queue(project, terminal)
    if not items:
        return
    while True:
        choice = terminal.ask("Choose a number to create an inspection report; 0 = back")
        if choice is None or choice in ("", "0", "q"):
            return
        if not choice.isascii() or not choice.isdecimal() or not 1 <= int(choice) <= len(items):
            terminal.say("Enter one of the listed numbers, or 0 to go back.")
            continue
        item = items[
            int(choice) - 1
        ]  # keep this exact snapshot; never rescan and choose another item
        output = export_report(project, item)
        terminal.say(f"Inspection report saved: {project.path(output)}")
        terminal.say("No decision or approval was recorded.")
        if terminal.ask("Type v to read it here, or Enter to return") == "v":
            view_report(project, output, terminal)
        return


def existing_demo(project: Project) -> Project:
    require(not project.synthetic, "Already in a synthetic workspace; omit --demo")
    path = project.path("dist/demo")
    require(
        native_path(path / "config/edition.yaml").is_file(),
        "No demo workspace yet. Run .\\jeb.cmd demo (or python -m jeb work demo)",
    )
    return Project(path, synthetic=True)


def build_demo(project: Project, terminal: Terminal) -> Project:
    require(
        not project.synthetic,
        "The demo is already selected; return to the repository to rebuild it",
    )
    from jeb.demo import demo

    terminal.say("Building the isolated synthetic example — NOT scripture; no approvals.")
    result = demo(project.root)
    terminal.say(f"Demo ready: {project.path(result['workspace'])}")
    terminal.say(
        "Review the example with .\\jeb.cmd --demo review (or python -m jeb work --demo review)."
    )
    return existing_demo(project)


def check(project: Project, terminal: Terminal) -> int:
    require(
        native_path(project.path("src/jeb")).is_dir()
        and native_path(project.path("tests")).is_dir(),
        "Run checks from the repository root, not a demo/recovered workspace",
    )
    require(
        importlib.util.find_spec("ruff") is not None,
        "Ruff is missing from this Python environment; install requirements.lock as documented in README",
    )
    terminal.say("Running the four offline repository checks. Tests may take several minutes.")
    for index, arguments in enumerate(CHECKS, 1):
        terminal.say(f"\n[{index}/4] python -m " + " ".join(arguments))
        try:
            result = subprocess.run(
                [sys.executable, "-m", *arguments], cwd=project.root, timeout=600, check=False
            )
        except subprocess.TimeoutExpired as exc:
            raise JebError("Offline check timed out; no success is claimed") from exc
        if result.returncode != 0:
            terminal.say(f"Check {index} failed (exit {result.returncode}). See the output above.")
            return 2
    terminal.say(
        "\nAll four offline checks passed. This is software verification, not editorial approval."
    )
    return 0


def run(project: Project, action="menu", *, demo=False, source_id=None, terminal=None) -> int:
    terminal = terminal if terminal is not None else Terminal()
    home = project
    project = existing_demo(home) if demo else home
    if action != "menu":
        if action == "status":
            status(project, terminal)
        elif action == "sources":
            source_gaps(project, terminal, source_id)
        elif action == "queue":
            show_queue(project, terminal)
        elif action == "review":
            choose_review(project, terminal)
        elif action == "demo":
            build_demo(home, terminal)
        elif action == "check":
            return check(home, terminal)
        else:
            raise JebError("Unknown terminal task")
        return 0
    while True:
        terminal.say("\nJEB — human terminal tasks")
        terminal.say("SYNTHETIC EXAMPLE — NOT SCRIPTURE" if project.synthetic else "Real project")
        terminal.say(
            "1. Status and next useful step\n2. Why a source is blocked\n3. List saved review work\n4. Choose work and read an inspection report\n5. Run offline checks\n6. Build/use the isolated synthetic demo\n7. Return to the initial workspace\n0. Exit"
        )
        choice = terminal.ask("Choose a task number (0 = exit)")
        if choice is None or choice in ("", "0", "q"):
            terminal.say("Done. Short commands: status, sources, queue, review, demo, check.")
            return 0
        try:
            if choice == "1":
                status(project, terminal)
            elif choice == "2":
                source_gaps(project, terminal)
            elif choice == "3":
                show_queue(project, terminal)
            elif choice == "4":
                choose_review(project, terminal)
            elif choice == "5":
                check(home, terminal)
            elif choice == "6":
                project = (
                    existing_demo(home)
                    if native_path(home.path("dist/demo/config/edition.yaml")).is_file()
                    else build_demo(home, terminal)
                )
            elif choice == "7":
                project = home
            else:
                terminal.say("Choose a listed number, or 0 to exit.")
        except (ValueError, OSError, UnicodeError) as exc:
            message = (
                "Invalid saved data; use its explicit validator for details"
                if " schema:" in str(exc)
                else str(exc)
            )
            terminal.say("Task could not finish: " + message)
