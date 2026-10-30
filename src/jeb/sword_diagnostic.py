"""Bounded synthetic-only SWORD experiments. Never a historical-source adapter."""

from __future__ import annotations

import os
import subprocess
import xml.etree.ElementTree as ET
from importlib.resources import files
from pathlib import Path

from jeb.core import (
    Project,
    digest,
    json_loads,
    latin_tree,
    read_bytes,
    read_json,
    require,
    sha256,
    validate_schema,
    write_json,
)

KEYS = (
    "Gen.0.0",
    "Gen.1.0",
    "Gen.1.1",
    "Gen.1.2",
    "Gen.1.3",
    "Gen.1.4",
    "Gen.1.5",
    "Gen.1.6",
    "Gen.1.7",
    "Matt.5.1",
)
SOURCE_HASH = "42409cf3de2faf1108523e2c5ac0745d21f9ed2a5c78ed878ee9dcc303426b8a"
TOOL_NAMES = ("imp2vs", "mod2imp", "mod2osis", "jeb-synthetic-probe")
MAX_OUTPUT = 2 * 1024 * 1024


class NoDTD(ET.TreeBuilder):
    def doctype(self, name, pubid, system):
        raise ValueError("DTD/entity declarations are unsupported")


def xml_tree(text: str, *, fragment: bool) -> ET.Element:
    require(len(text.encode("utf-8")) <= 65536, "Diagnostic XML exceeds bound")
    # Check before wrapping, and disable DTD processing in the XML parser itself.
    require("<!DOCTYPE" not in text and "<!ENTITY" not in text, "DTD/entities forbidden")
    try:
        parser = ET.XMLParser(target=NoDTD())
        root = ET.fromstring(
            f"<jeb-fragment>{text}</jeb-fragment>" if fragment else text, parser=parser
        )
    except ET.ParseError as exc:
        raise ValueError(f"Malformed diagnostic XML: {exc}") from exc

    def visit(node, depth=0):
        require(depth <= 12, "Diagnostic XML nesting exceeds 12")
        for child in node:
            visit(child, depth + 1)

    visit(root)
    require(sum(1 for _ in root.iter()) <= 512, "Too many diagnostic XML nodes")
    return root


def fixture_entries() -> dict[str, str]:
    """This grammar is only for the fixed, original test asset, not arbitrary IMP ingestion."""
    text = files("jeb").joinpath("assets/sword-synthetic.imp").read_text("utf-8")
    entries = {}
    current = None
    for line in text.splitlines(keepends=True):
        if line.startswith("$$$"):
            current = line[3:].rstrip("\n")
            require(current not in entries, "Duplicate original diagnostic fixture key")
            entries[current] = ""
        else:
            require(current is not None, "Diagnostic fixture lacks key")
            entries[current] += line
    return entries


def expected_slots() -> dict[str, str]:
    entries = fixture_entries()
    slots = {}
    for key in KEYS:
        if key == "Gen.1.6":
            slots[key] = ""
        elif key in ("Gen.1.3", "Gen.1.4"):
            slots[key] = entries["Gen.1.3-4"]
        else:
            # imp2vs 1.9.0's do/while EOF handling adds one final LF to the last entry.
            # Keep that observed importer change explicit; it is not a corpus normalization rule.
            slots[key] = entries[key] + ("\n" if key == "Matt.5.1" else "")
    return slots


def validate_probe(payload: bytes) -> dict:
    require(len(payload) <= MAX_OUTPUT, "Probe output exceeds bound")
    rows = [
        json_loads(line)
        for line in payload.decode("utf-8", errors="strict").splitlines()
        if line.strip()
    ]
    require(len(rows) == len(KEYS), "Missing or extra diagnostic slots")
    for row in rows:
        validate_schema("sword-probe-entry", row)
        latin_tree(row)
    require(
        [r["osis_id"] for r in rows] == list(KEYS),
        "Duplicate, reordered or out-of-scope probe slots",
    )
    expected = expected_slots()
    by_id = {r["osis_id"]: r for r in rows}
    changed = []
    for row in rows:
        key = row["osis_id"]
        require(
            row["stored_length_bytes"] == len(row["stored_osis"].encode("utf-8"))
            and row["raw_length_bytes"] == len(row["engine_osis"].encode("utf-8")),
            "Probe UTF-8 byte length mismatch",
        )
        require(
            row["stored_osis"] == expected[key],
            f"Stored entry differs from the original fixture/importer contract: {key}",
        )
        require(row["has_entry"] == bool(expected[key]), "Empty-slot state was changed or filled")
        expected_kind = (
            "book_introduction"
            if key == "Gen.0.0"
            else "chapter_introduction"
            if key == "Gen.1.0"
            else "verse"
        )
        require(row["entry_kind"] == expected_kind, "Introduction misclassified as verse")
        require(
            row["linked_to"] == ("Gen.1.3" if key == "Gen.1.4" else None),
            "Link was dropped, invented, or inferred from identical text",
        )
        if row["linked_to"]:
            require(
                row["stored_osis"] == by_id[row["linked_to"]]["stored_osis"],
                "Linked entry text differs",
            )
        if row["has_entry"]:
            xml_tree(row["stored_osis"], fragment=True)
            xml_tree(row["engine_osis"], fragment=True)
            # This is the fixed fixture's measured engine prepText behavior, not a general OSIS rule.
            require(
                row["engine_osis"] == row["stored_osis"].replace("\n", " ").rstrip(" "),
                "Unexpected engine text transformation",
            )
        else:
            require(not row["engine_osis"], "Empty slot has rendered content")
        if row["stored_osis"] != row["engine_osis"]:
            changed.append(
                {
                    "osis_id": key,
                    "stored_sha256": sha256(row["stored_osis"].encode("utf-8")),
                    "engine_sha256": sha256(row["engine_osis"].encode("utf-8")),
                    "reason": "SWORD prepText changes LF/terminal whitespace; stored bytes retained separately.",
                }
            )
    return {
        "schema_version": "1.0",
        "synthetic_only": True,
        "real_biblical_segments": 0,
        "requested_slots": len(rows),
        "present_slots": sum(r["has_entry"] for r in rows),
        "stored_entries": len(fixture_entries()),
        "linked_aliases": 1,
        "identical_text_independent_slot": "Gen.1.7",
        "empty_slots": ["Gen.1.6"],
        "introduced_eof_lf": ["Matt.5.1"],
        "engine_transformations": changed,
        "snapshot_sha256": sha256(payload),
        "production_adapter_approved": False,
    }


def validate_capture(path: Path) -> dict:
    return validate_probe(read_bytes(path, MAX_OUTPUT))


def check_tool_lock(lock: dict, tools: Path) -> dict[str, Path]:
    validate_schema("toolchain-lock", lock)
    require(lock["source"]["sha256"] == SOURCE_HASH, "Unreviewed SWORD source archive")
    result = {}
    for name in TOOL_NAMES:
        record = lock["executables"][name]
        expected_name = name + (".exe" if lock["platform"] == "windows" else "")
        require(record["filename"] == expected_name, "Unexpected executable filename")
        path = tools / record["filename"]
        require(not path.is_symlink(), "Tool executable symlink unsupported")
        payload = read_bytes(path, 32 * 1024 * 1024)
        require(
            len(payload) == record["size_bytes"] and sha256(payload) == record["sha256"],
            f"Changed executable; re-evaluate toolchain: {name}",
        )
        result[name] = path.resolve()
    return result


def evaluate(project: Project, lock_path: Path, tools: Path, output: str) -> dict:
    lock = read_json(lock_path)
    programs = check_tool_lock(lock, tools.resolve())
    destination = project.path(output)
    require(
        not destination.exists(),
        "Diagnostic output already exists; validate it or choose a new output path",
    )
    destination.mkdir(parents=True)
    library = destination / "library"
    module = library / "modules/texts/ztext/jebsynthetic"
    module.mkdir(parents=True)
    (library / "mods.d").mkdir()
    fixture = files("jeb").joinpath("assets/sword-synthetic.imp").read_bytes()
    fixture_path = destination / "synthetic.imp"
    fixture_path.write_bytes(fixture)
    conf = (
        "[JEBSynthetic]\nDataPath=./modules/texts/ztext/jebsynthetic/\nModDrv=zText\n"
        "SourceType=OSIS\nEncoding=UTF-8\nCompressType=ZIP\nBlockType=BOOK\nVersification=Calvin\n"
        "Lang=sr-Latn\nDescription=Original synthetic diagnostic fixture; NOT scripture\n"
        "GlobalOptionFilter=OSISHeadings\nGlobalOptionFilter=OSISFootnotes\nFeature=NoParagraphs\n"
        "Version=1.0\nDistributionLicense=Public Domain\n"
    )
    (library / "mods.d/jebsynthetic.conf").write_bytes(conf.encode("utf-8"))
    env = os.environ.copy()
    env.update(
        SWORD_PATH=str(library),
        HOME=str(destination / "isolated-home"),
        APPDATA=str(destination / "isolated-appdata"),
        USERPROFILE=str(destination / "isolated-home"),
    )
    commands = [
        ("imp2vs", [str(fixture_path), "-o", str(module), "-z", "z", "-b", "4", "-v", "Calvin"]),
        ("jeb-synthetic-probe", [str(library), *KEYS]),
        ("mod2imp", ["JEBSynthetic"]),
        ("mod2osis", ["JEBSynthetic"]),
    ]
    runs = []
    try:
        for name, arguments in commands:
            args = [str(programs[name]), *arguments]
            stdout_path, stderr_path = (
                destination / f"{name}.stdout",
                destination / f"{name}.stderr",
            )
            with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
                # No shell interpolation, no install manager, no live corpus path or arbitrary module argument.
                process = subprocess.run(
                    args,
                    cwd=library,
                    env=env,
                    stdout=stdout,
                    stderr=stderr,
                    timeout=30,
                    check=False,
                )
            require(
                stdout_path.stat().st_size <= MAX_OUTPUT
                and stderr_path.stat().st_size <= MAX_OUTPUT,
                "Native diagnostic output exceeds bound",
            )
            runs.append(
                {
                    "tool": name,
                    "returncode": process.returncode,
                    "stdout_sha256": sha256(read_bytes(stdout_path, MAX_OUTPUT)),
                    "stderr_sha256": sha256(read_bytes(stderr_path, MAX_OUTPUT)),
                }
            )
            require(process.returncode == 0, f"{name} failed; see diagnostic stdout/stderr")
        report = validate_capture(destination / "jeb-synthetic-probe.stdout")
        osis = xml_tree(
            read_bytes(destination / "mod2osis.stdout", MAX_OUTPUT).decode("utf-8"), fragment=False
        )
        references = [node.text for node in osis.iter() if node.tag.endswith("}refSystem")]
        raw_osis = read_bytes(destination / "mod2osis.stdout", MAX_OUTPUT).decode("utf-8")
        # Inspect only these three fixed fixture records; this is not an IMP corpus parser.
        samples = {}
        current = None
        for line in (
            read_bytes(destination / "mod2imp.stdout", MAX_OUTPUT).decode("utf-8").splitlines()
        ):
            if line.startswith("$$$"):
                current = line[3:]
                if current in ("Genesis 1:3", "Genesis 1:4", "Genesis 1:7"):
                    samples[current] = []
            elif current in samples:
                samples[current].append(line)
        report["stock_export_observations"] = {
            "declared_module_scheme": "Calvin",
            "mod2osis_ref_systems": references,
            "book_introduction_preserved": "Synthetic book introduction" in raw_osis,
            "chapter_introduction_preserved": "Synthetic chapter introduction" in raw_osis,
            "mod2imp_sample_headers": sorted(samples),
            "mod2imp_three_samples_have_equal_text": len(samples) == 3
            and len({"\n".join(lines) for lines in samples.values()}) == 1,
            "note": "Observations apply to this pinned synthetic experiment only; no general losslessness claim.",
        }
        report.update(toolchain_lock_sha256=digest(lock), fixture_sha256=sha256(fixture), runs=runs)
        write_json(destination / "report.json", report, replace=False)
        return {"output": output, **report}
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        write_json(
            destination / "failure.json", {"error": str(exc), "runs": runs, "synthetic_only": True}
        )
        raise ValueError(f"SWORD synthetic diagnostic failed: {exc}") from exc
