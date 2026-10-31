"""Small installable CLI. Commands listed here are real; later phases stay in docs."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator

from jeb import __version__
from jeb.batch import import_response, prepare, validate_response
from jeb.core import JebError, Project, canonical, json_loads, read_json, require
from jeb.corpus import ingest, load_corpus
from jeb.export import export, reader
from jeb.fetch import fetch
from jeb.knowledge import validate_knowledge
from jeb.review import apply, report
from jeb.search import build_index, search
from jeb.source_assessment import inspect_source
from jeb.sources import audit
from jeb.sword_diagnostic import evaluate, validate_capture


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(prog="jeb", description="JEB local source and editorial pipeline")
    cli.add_argument("--version", action="version", version=__version__)
    cli.add_argument(
        "--root", type=Path, default=Path.cwd(), help="Project root; no upward implicit discovery"
    )
    cli.add_argument(
        "--synthetic", action="store_true", help="Explicitly allow an isolated synthetic workspace"
    )
    commands = cli.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "demo", help="Build a synthetic workspace under dist/demo; never ingest scripture"
    )
    sources = commands.add_parser("sources").add_subparsers(dest="operation", required=True)
    sources.add_parser("audit")
    sources.add_parser("inspect").add_argument("--source", required=True)
    research = sources.add_parser("research").add_subparsers(
        dest="research_operation", required=True
    )
    sub = research.add_parser("prepare")
    sub.add_argument("--source", required=True)
    sub.add_argument("--packet-id", required=True)
    for name in ("validate", "import", "report"):
        sub = research.add_parser(name)
        sub.add_argument("--input", required=True, type=Path)
        if name == "report":
            sub.add_argument("--output", required=True)
    toolchain = commands.add_parser("toolchain").add_subparsers(dest="operation", required=True)
    toolchain.add_parser("validate").add_argument("--input", required=True, type=Path)
    sub = toolchain.add_parser("build")
    sub.add_argument("--archive", required=True, type=Path)
    sub.add_argument("--output", required=True)
    sub.add_argument("--compiler", default="g++")
    sub.add_argument("--c-compiler", default="gcc")
    sub.add_argument("--cmake", default="cmake")
    sub = toolchain.add_parser("evaluate")
    sub.add_argument("--lock", required=True, type=Path)
    sub.add_argument("--tools", required=True, type=Path)
    sub.add_argument("--output", required=True)
    for name in ("fetch", "parse", "normalize", "index"):
        sub = commands.add_parser(name)
        sub.add_argument("--source", required=True)
    sub = commands.add_parser("validate")
    sub.add_argument("--stage", required=True, choices=("schemas", "normalized", "knowledge"))
    sub.add_argument("--source")
    batch = commands.add_parser("batch").add_subparsers(dest="operation", required=True)
    sub = batch.add_parser("prepare")
    sub.add_argument("--source", required=True)
    sub.add_argument("--batch-id", required=True)
    sub.add_argument(
        "--selection", required=True, choices=("GEN", "MAT", "MRK", "LUK", "JHN", "fixture")
    )
    sub.add_argument("--task", choices=("modernize",), default="modernize")
    for name in ("validate", "import"):
        batch.add_parser(name).add_argument("--input", required=True, type=Path)
    knowledge = commands.add_parser("knowledge").add_subparsers(dest="operation", required=True)
    sub = knowledge.add_parser("prepare")
    sub.add_argument("--source", required=True)
    sub.add_argument(
        "--selection", required=True, choices=("GEN", "MAT", "MRK", "LUK", "JHN", "fixture")
    )
    sub.add_argument("--task", required=True, choices=("research", "annotate"))
    sub.add_argument("--packet-id", required=True)
    for name in ("validate", "import", "report"):
        sub = knowledge.add_parser(name)
        sub.add_argument("--input", required=True, type=Path)
        if name == "report":
            sub.add_argument("--output", required=True)
    knowledge_review = knowledge.add_parser("review").add_subparsers(
        dest="knowledge_review_operation", required=True
    )
    sub = knowledge_review.add_parser("export")
    sub.add_argument("--packet-id", required=True)
    sub.add_argument("--response-sha256", required=True)
    sub.add_argument("--output", required=True)
    for name in ("validate", "apply"):
        knowledge_review.add_parser(name).add_argument("--decisions", required=True, type=Path)
    review = commands.add_parser("review").add_subparsers(dest="operation", required=True)
    sub = review.add_parser("export")
    sub.add_argument("--proposal", required=True)
    sub.add_argument("--output", required=True)
    review.add_parser("apply").add_argument("--decisions", required=True, type=Path)
    assistance = review.add_parser("assist").add_subparsers(dest="assist_operation", required=True)
    sub = assistance.add_parser("prepare")
    sub.add_argument("--proposal", required=True)
    sub.add_argument("--packet-id", required=True)
    for name in ("validate", "import", "report"):
        sub = assistance.add_parser(name)
        sub.add_argument("--input", required=True, type=Path)
        if name == "report":
            sub.add_argument("--output", required=True)
    sub = commands.add_parser("export")
    sub.add_argument("--source", required=True)
    sub.add_argument("--profile", default="five-book", choices=("five-book",))
    sub.add_argument("--format", required=True, choices=("json", "markdown"))
    sub.add_argument("--maturity", required=True, choices=("preview", "release"))
    sub.add_argument("--output", required=True)
    sub = commands.add_parser("search")
    sub.add_argument("--source", required=True)
    sub.add_argument("--query", required=True)
    sub = (
        commands.add_parser("release")
        .add_subparsers(dest="operation", required=True)
        .add_parser("check")
    )
    sub.add_argument("--source", required=True)
    sub.add_argument("--edition", required=True)
    return cli


def run(args: argparse.Namespace):
    if args.command == "demo":
        from jeb.demo import demo

        return demo(args.root)
    project = Project(args.root, synthetic=args.synthetic)
    if args.command == "toolchain":
        if args.operation == "build":
            from jeb.sword_build import build

            return build(
                project, args.archive, args.output, args.compiler, args.c_compiler, args.cmake
            )
        if args.operation == "validate":
            return validate_capture(args.input)
        return evaluate(project, args.lock, args.tools, args.output)
    if args.command == "sources":
        if args.operation == "research":
            from jeb import source_research

            if args.research_operation == "prepare":
                packet = source_research.prepare(project, args.source, args.packet_id)
                return {
                    "output": f"data/source-research/{args.packet_id}/input.json",
                    "packet_sha256": packet["packet_sha256"],
                    "questions": len(packet["questions"]),
                    "corpus_permission": False,
                }
            if args.research_operation == "import":
                return source_research.import_response(project, args.input)
            if args.research_operation == "report":
                return source_research.report(project, args.input, args.output)
            value = source_research.read_response(args.input)
            source_research.validate_response(project, value)
            return {
                "valid_questions": len(value["items"]),
                "leads": len(value["leads"]),
                "review_state": "unreviewed",
                "corpus_permission": False,
            }
        return audit(project) if args.operation == "audit" else inspect_source(project, args.source)
    if args.command == "fetch":
        return fetch(project, args.source)
    if args.command in ("parse", "normalize"):
        return ingest(project, args.source, normalized=args.command == "normalize")
    if args.command == "validate":
        if args.stage == "schemas":
            resources = [
                p for p in files("jeb").joinpath("schemas").iterdir() if p.name.endswith(".json")
            ]
            for path in resources:
                Draft202012Validator.check_schema(json_loads(path.read_text("utf-8")))
            return {"valid_schemas": len(resources)}
        require(bool(args.source), "--source is required for corpus/knowledge validation")
        books = load_corpus(project, args.source)
        if args.stage == "knowledge":
            return {"valid_knowledge_records": len(validate_knowledge(project, books))}
        return {
            "valid_books": list(books),
            "valid_segments": sum(len(b["segments"]) for b in books.values()),
        }
    if args.command == "batch":
        if args.operation == "prepare":
            packet = prepare(project, args.source, args.batch_id, args.selection, args.task)
            return {
                "packet": f"data/batches/{args.batch_id}/input.json",
                "packet_sha256": packet["packet_sha256"],
                "segments": len(packet["segments"]),
            }
        if args.operation == "validate":
            packet, items = validate_response(project, read_json(args.input))
            return {"batch_id": packet["batch_id"], "valid_items": len(items), "approved": False}
        return import_response(project, args.input)
    if args.command == "knowledge":
        from jeb import knowledge_packets

        if args.operation == "review":
            from jeb import knowledge_review

            if args.knowledge_review_operation == "export":
                return knowledge_review.report(
                    project, args.packet_id, args.response_sha256, args.output
                )
            if args.knowledge_review_operation == "apply":
                return knowledge_review.apply(project, args.decisions)
            receipt = knowledge_review.validate_decisions(
                project, knowledge_review.read_decisions(args.decisions)
            )
            return {
                "valid_items": len(receipt["decisions"]["items"]),
                "human_decisions_created": 0,
                "approvals_created": 0,
            }
        if args.operation == "prepare":
            packet = knowledge_packets.prepare(
                project, args.source, args.selection, args.task, args.packet_id
            )
            return {
                "output": f"data/knowledge-proposals/{args.packet_id}/input.json",
                "packet_sha256": packet["packet_sha256"],
                "task": packet["task"],
                "segments": len(packet["coverage_manifest"]),
                "approval_authority": "none",
            }
        if args.operation == "import":
            return knowledge_packets.import_response(project, args.input)
        if args.operation == "report":
            return knowledge_packets.report(project, args.input, args.output)
        value = knowledge_packets.read_response(args.input)
        knowledge_packets.validate_response(project, value)
        return {
            "valid_items": len(value["items"]),
            "task": value["task"],
            "drafts": len(value.get("drafts", [])),
            "leads": len(value.get("leads", [])),
            "review_state": "unreviewed",
            "approval_authority": "none",
        }
    if args.command == "review":
        if args.operation == "assist":
            from jeb import review_assistance

            if args.assist_operation == "prepare":
                packet = review_assistance.prepare(project, args.proposal, args.packet_id)
                return {
                    "output": f"data/review-assistance/{args.packet_id}/input.json",
                    "packet_sha256": packet["packet_sha256"],
                    "segments": len(packet["coverage_manifest"]),
                    "approval_authority": "none",
                }
            if args.assist_operation == "import":
                return review_assistance.import_response(project, args.input)
            if args.assist_operation == "report":
                return review_assistance.report(project, args.input, args.output)
            value = review_assistance.read_response(args.input)
            review_assistance.validate_response(project, value)
            return {
                "valid_items": len(value["items"]),
                "review_state": "unreviewed",
                "approval_authority": "none",
            }
        return (
            apply(project, args.decisions)
            if args.operation == "apply"
            else report(project, args.proposal, args.output)
        )
    if args.command == "export":
        return export(project, args.source, args.maturity, args.format, args.output, args.profile)
    if args.command == "index":
        return build_index(project, args.source)
    if args.command == "search":
        return search(project, args.query, args.source)
    if args.command == "release":
        require(
            args.edition == project.edition["edition_id"], "Edition ID does not match workspace"
        )
        reader(project, args.source, "release")
        return {"release_ready": True, "edition": args.edition}
    raise JebError("Unknown command")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = run(args)
    except (ValueError, OSError, UnicodeError, sqlite3.Error) as exc:
        print(f"jeb: {exc}", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(canonical(result))
    return 0
