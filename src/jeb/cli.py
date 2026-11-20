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
from jeb.search import build_index
from jeb.search import search as project_search
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
    reading = commands.add_parser("reading", help="Local synthetic reading desk and private items")
    reading_commands = reading.add_subparsers(dest="reading_operation", required=True)
    for operation in ("demo", "view", "save", "backup", "restore"):
        command = reading_commands.add_parser(operation)
        if operation != "restore":
            command.add_argument("--bank-root", required=True, type=Path)
        if operation == "backup":
            command.add_argument("--output", required=True, type=Path)
        if operation == "restore":
            command.add_argument("--input", required=True, type=Path)
            command.add_argument("--destination", required=True, type=Path)
    bank = commands.add_parser("bank", help="Independent local knowledge-bank snapshots")
    bank_commands = bank.add_subparsers(dest="bank_operation", required=True)
    evidence = bank_commands.add_parser("evidence").add_subparsers(
        dest="evidence_operation", required=True
    )
    command = evidence.add_parser("links")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("record_id")
    for operation in ("prepare", "validate", "inspect"):
        command = evidence.add_parser(operation)
        command.add_argument("--bank-root", type=Path, required=True)
        command.add_argument("--input", type=Path, required=True)
        if operation == "prepare":
            command.add_argument("--output", type=Path, required=True)
            command.add_argument("--actor", required=True)
            command.add_argument("--actor-kind", choices=("human", "agent", "tool"), required=True)
    for operation in ("validate", "show"):
        command = bank_commands.add_parser(operation)
        command.add_argument("--bank-root", type=Path, required=True)
        if operation == "show":
            command.add_argument("record_id")
    command = bank_commands.add_parser("init")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("--title", required=True)
    command.add_argument("--format", dest="bank_format", choices=("2.0", "3.0"), default="2.0")
    command = bank_commands.add_parser("reference")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("record_id")
    command.add_argument("--revision")
    command = bank_commands.add_parser("search")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("--query", required=True)
    command = bank_commands.add_parser("migrate-plan")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("--output", type=Path, required=True)
    command = bank_commands.add_parser("migrate-plan-verify")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("--input", type=Path, required=True)
    command = bank_commands.add_parser("migrate-decision-validate")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("--plan", type=Path, required=True)
    command.add_argument("--input", type=Path, required=True)
    command = bank_commands.add_parser("migrate-simulate")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("--plan", type=Path, required=True)
    command.add_argument("--input", type=Path, required=True)
    command.add_argument("--synthetic", action="store_true", required=True)
    command = bank_commands.add_parser("backup")
    command.add_argument("--bank-root", type=Path, required=True)
    command.add_argument("--output", type=Path, required=True)
    command = bank_commands.add_parser("backup-verify")
    command.add_argument("--input", type=Path, required=True)
    command = bank_commands.add_parser("restore")
    command.add_argument("--input", type=Path, required=True)
    command.add_argument("--destination", type=Path, required=True)
    for operation in ("create", "edit"):
        command = bank_commands.add_parser(operation)
        command.add_argument("--bank-root", type=Path, required=True)
        command.add_argument("--input", type=Path, required=True)
        command.add_argument("--body", type=Path)
        command.add_argument("--actor", required=True)
        command.add_argument("--actor-kind", choices=("human", "agent", "tool"), required=True)
        command.add_argument("--reason", required=True)
        if operation == "edit":
            command.add_argument("record_id")
            command.add_argument("--expected-revision", required=True)
    for operation in ("history", "diff", "recover"):
        command = bank_commands.add_parser(operation)
        command.add_argument("--bank-root", type=Path, required=True)
        if operation == "recover":
            command.add_argument("--transaction")
        else:
            command.add_argument("record_id")
            if operation == "diff":
                command.add_argument("--from-revision", required=True)
                command.add_argument("--to-revision", required=True)
    work = commands.add_parser("work", help="Human terminal menu and short everyday tasks")
    work.add_argument(
        "action",
        nargs="?",
        default="menu",
        choices=("menu", "status", "sources", "queue", "review", "demo", "check"),
    )
    work.add_argument(
        "--demo", action="store_true", help="Explicitly use the isolated dist/demo workspace"
    )
    work.add_argument("--source", help="Show blockers for one source with the sources task")
    commands.add_parser(
        "demo", help="Build a synthetic workspace under dist/demo; never ingest scripture"
    )
    archives = commands.add_parser("archive").add_subparsers(
        dest="archive_operation", required=True
    )
    sub = archives.add_parser("create")
    sub.add_argument("--source", required=True)
    sub.add_argument("--archive-id", required=True)
    sub.add_argument("--output", required=True)
    for name in ("validate", "restore"):
        sub = archives.add_parser(name)
        sub.add_argument("--input", required=True, type=Path)
        if name == "restore":
            sub.add_argument("--destination", required=True)
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
    candidates = sources.add_parser(
        "candidates", help="Validate/import untrusted search results without acquiring content"
    ).add_subparsers(dest="candidates_operation", required=True)
    for name in ("validate", "import"):
        sub = candidates.add_parser(name)
        sub.add_argument("--input", required=True, type=Path)
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
    curation = knowledge.add_parser("curate").add_subparsers(
        dest="curation_operation", required=True
    )
    sub = curation.add_parser("export")
    sub.add_argument("--output", required=True)
    sub.add_argument("--source")
    for name in ("validate", "apply"):
        curation.add_parser(name).add_argument("--decisions", required=True, type=Path)
    narrative = knowledge.add_parser("narrative").add_subparsers(
        dest="narrative_operation", required=True
    )
    sub = narrative.add_parser("prepare")
    sub.add_argument("--source", required=True)
    sub.add_argument(
        "--selection", required=True, choices=("GEN", "MAT", "MRK", "LUK", "JHN", "fixture")
    )
    sub.add_argument("--packet-id", required=True)
    for name in ("validate", "import", "report"):
        sub = narrative.add_parser(name)
        sub.add_argument("--input", required=True, type=Path)
        if name == "report":
            sub.add_argument("--output", required=True)
    narrative_review = narrative.add_parser("review").add_subparsers(
        dest="narrative_review_operation", required=True
    )
    sub = narrative_review.add_parser("export")
    sub.add_argument("--packet-id", required=True)
    sub.add_argument("--response-sha256", required=True)
    sub.add_argument("--output", required=True)
    narrative_review.add_parser("validate").add_argument("--decisions", required=True, type=Path)
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
    historical = commands.add_parser(
        "historical", help="Local historical registry, incremental pipeline and queries"
    )
    historical_commands = historical.add_subparsers(dest="historical_operation", required=True)
    registry = historical_commands.add_parser("registry-build")
    registry.add_argument("--input", required=True, type=Path)
    registry.add_argument("--output", required=True, type=Path)
    entities = historical_commands.add_parser("entity-index")
    entities.add_argument("--registry", required=True, type=Path)
    entities.add_argument("--root", required=True, type=Path)
    entities.add_argument("--output", required=True, type=Path)
    groups = historical_commands.add_parser("entity-groups")
    groups.add_argument("--input", required=True, type=Path)
    groups.add_argument("--output", required=True, type=Path)
    dossiers = historical_commands.add_parser("entity-dossiers")
    dossiers.add_argument("--registry", required=True, type=Path)
    dossiers.add_argument("--index", required=True, type=Path)
    dossiers.add_argument("--groups", required=True, type=Path)
    dossiers.add_argument("--output", required=True, type=Path)
    for operation in ("status", "lookup", "relations", "dossiers", "dossier", "detail"):
        command = historical_commands.add_parser(operation)
        for name in ("registry", "index", "groups", "dossiers", "workspace"):
            command.add_argument(f"--{name}", type=Path)
        if operation != "status":
            command.add_argument("--query", default="")
            command.add_argument("--work", default="")
            command.add_argument("--status", default="")
            command.add_argument("--availability", default="")
            command.add_argument("--relation", default="")
            command.add_argument("--id", default="")
            command.add_argument("--limit", default="100")
            command.add_argument("--offset", default="0")
            command.add_argument("--locator-limit", default="20")
            command.add_argument("--locator-offset", default="0")
    pipeline = historical_commands.add_parser("pipeline").add_subparsers(
        dest="pipeline_operation", required=True
    )
    command = pipeline.add_parser("init")
    command.add_argument("--registry", required=True, type=Path)
    command.add_argument("--root", required=True, type=Path)
    command.add_argument("--workspace", required=True, type=Path)
    command = pipeline.add_parser("step")
    command.add_argument("--workspace", required=True, type=Path)
    command.add_argument("--max-artifacts", default=4, type=int)
    command.add_argument("--max-seconds", default=10, type=float)
    command.add_argument("--retry-pending", action="store_true")
    command.add_argument("--refresh", action="store_true")
    command = pipeline.add_parser("status")
    command.add_argument("--workspace", required=True, type=Path)
    command = historical_commands.add_parser("demo")
    command.add_argument("--workspace", required=True, type=Path)
    command = historical_commands.add_parser("projection-verify")
    command.add_argument("--workspace", required=True, type=Path)
    command.add_argument("--cache-sha256", required=True)
    sub = (
        commands.add_parser("release")
        .add_subparsers(dest="operation", required=True)
        .add_parser("check")
    )
    sub.add_argument("--source", required=True)
    sub.add_argument("--edition", required=True)
    return cli


def run(args: argparse.Namespace):
    if args.command == "reading":
        from jeb import reading

        if args.reading_operation == "demo":
            return reading.create_demo(args.bank_root, synthetic=args.synthetic)
        if args.reading_operation == "backup":
            return reading.create_backup(args.bank_root, args.output, synthetic=args.synthetic)
        if args.reading_operation == "restore":
            return reading.restore_backup(args.input, args.destination, synthetic=args.synthetic)
        payload = None
        if args.reading_operation == "save":
            raw = sys.stdin.buffer.read(reading.MAX_REQUEST + 1)
            try:
                require(len(raw) <= reading.MAX_REQUEST, "Reading request exceeds limit")
                payload = json_loads(raw.decode("utf-8", errors="strict"))
            except (ValueError, UnicodeError):
                return {"enabled": False, "error": "invalid_reading_input"}
        return reading.rpc(
            args.bank_root, args.reading_operation, synthetic=args.synthetic, payload=payload
        )
    if args.command == "historical":
        from jeb.historical import (
            build_entity_dossiers,
            build_entity_groups,
            build_entity_index,
            build_registry,
        )

        if args.historical_operation == "registry-build":
            return build_registry(args.input, args.output)
        if args.historical_operation == "entity-groups":
            return build_entity_groups(args.input, args.output)
        if args.historical_operation == "entity-dossiers":
            return build_entity_dossiers(args.registry, args.index, args.groups, args.output)
        if args.historical_operation == "entity-index":
            return build_entity_index(
                args.registry, args.root, args.output, synthetic=args.synthetic
            )
        if args.historical_operation == "demo":
            from jeb.historical_demo import create_demo

            return create_demo(args.workspace, synthetic=args.synthetic)
        if args.historical_operation == "projection-verify":
            from jeb.historical_pipeline import verify_projection

            return verify_projection(args.workspace, args.cache_sha256, synthetic=args.synthetic)
        if args.historical_operation == "pipeline":
            from jeb.historical_pipeline import initialize, pipeline_status, step

            if args.pipeline_operation == "init":
                return initialize(
                    args.registry, args.root, args.workspace, synthetic=args.synthetic
                )
            if args.pipeline_operation == "status":
                return pipeline_status(args.workspace, synthetic=args.synthetic)
            return step(
                args.workspace,
                synthetic=args.synthetic,
                max_artifacts=args.max_artifacts,
                max_seconds=args.max_seconds,
                retry_pending=args.retry_pending,
                refresh=args.refresh,
            )
        from jeb.historical_query import inspect, query

        paths = {key: getattr(args, key) for key in ("registry", "index", "groups", "dossiers")}
        if args.historical_operation == "status":
            return inspect(paths, workspace=args.workspace, synthetic=args.synthetic)
        params = {
            key: getattr(args, key)
            for key in (
                "work",
                "status",
                "availability",
                "relation",
                "id",
                "limit",
                "offset",
                "locator_limit",
                "locator_offset",
            )
        }
        params["q"] = args.query
        return query(
            args.historical_operation,
            paths,
            params,
            workspace=args.workspace,
            synthetic=args.synthetic,
        )
    if args.command == "bank":
        from jeb.bank import storage
        from jeb.bank.validation import show_record, validate_bank

        if args.bank_operation == "evidence":
            from jeb.bank import evidence

            if args.evidence_operation == "links":
                from jeb.bank.references import evidence_links

                return evidence_links(args.bank_root, args.record_id)

            if args.evidence_operation == "prepare":
                return evidence.prepare(
                    args.bank_root, args.input, args.output, args.actor, args.actor_kind
                )
            if args.evidence_operation == "inspect":
                return evidence.inspect(args.bank_root, args.input)
            return evidence.validate(args.bank_root, args.input)

        if args.bank_operation in ("backup", "backup-verify", "restore"):
            from jeb.bank import backup

            if args.bank_operation == "backup":
                return backup.create(args.bank_root, args.output)
            if args.bank_operation == "backup-verify":
                return backup.verify(args.input)
            return backup.restore(args.input, args.destination)

        if args.bank_operation == "init":
            return storage.initialize(args.bank_root, args.title, args.bank_format)
        if args.bank_operation == "reference":
            from jeb.bank.references import record_reference

            return record_reference(args.bank_root, args.record_id, args.revision)
        if args.bank_operation == "search":
            from jeb.bank.search import search

            return search(args.bank_root, args.query)
        if args.bank_operation == "migrate-plan":
            from jeb.bank.migration import write_plan

            return write_plan(args.bank_root, args.output)
        if args.bank_operation == "migrate-plan-verify":
            from jeb.bank.migration import verify_plan

            return verify_plan(args.bank_root, args.input)
        if args.bank_operation == "migrate-decision-validate":
            from jeb.bank.decision import validate

            return validate(args.bank_root, args.plan, args.input)
        if args.bank_operation == "migrate-simulate":
            from jeb.bank.simulation import simulate

            return simulate(args.bank_root, args.plan, args.input, synthetic=args.synthetic)
        if args.bank_operation in ("create", "edit"):
            from jeb.core import read_bytes

            content = storage.document(args.input)
            body = (
                read_bytes(args.body, storage.MAX_FILE_BYTES).decode("utf-8") if args.body else None
            )
            return storage.save_record(
                args.bank_root,
                content,
                args.actor,
                args.actor_kind,
                args.reason,
                body,
                getattr(args, "record_id", None),
                getattr(args, "expected_revision", None),
            )
        if args.bank_operation == "history":
            return storage.history(args.bank_root, args.record_id)
        if args.bank_operation == "diff":
            return storage.diff(
                args.bank_root, args.record_id, args.from_revision, args.to_revision
            )
        if args.bank_operation == "recover":
            return storage.recover(args.bank_root, args.transaction)
        if args.bank_operation == "show":
            return show_record(args.bank_root, args.record_id)
        return validate_bank(args.bank_root)
    if args.command == "archive":
        from jeb import build_archive

        if args.archive_operation == "validate":
            return build_archive.validate(args.input, synthetic=args.synthetic)
        if args.archive_operation == "restore":
            return build_archive.restore(
                args.root, args.input, args.destination, synthetic=args.synthetic
            )
        return build_archive.create(
            Project(args.root, synthetic=args.synthetic), args.source, args.archive_id, args.output
        )
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
        if args.operation == "candidates":
            from jeb import source_candidates

            if args.candidates_operation == "validate":
                value = source_candidates.validate(args.input)
                return {
                    "batch_id": value["batch_id"],
                    "candidates": len(value["candidates"]),
                    "review_state": "unreviewed",
                    "corpus_permission": False,
                }
            return source_candidates.import_batch(project, args.input)
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

        if args.operation == "narrative":
            from jeb import narrative_packets

            if args.narrative_operation == "review":
                from jeb import narrative_review

                if args.narrative_review_operation == "validate":
                    return narrative_review.validate_decisions(project, args.decisions)
                return narrative_review.report(
                    project, args.packet_id, args.response_sha256, args.output
                )
            if args.narrative_operation == "prepare":
                packet = narrative_packets.prepare(
                    project, args.source, args.selection, args.packet_id
                )
                return {
                    "output": f"data/narrative-proposals/{args.packet_id}/input.json",
                    "packet_sha256": packet["packet_sha256"],
                    "segments": len(packet["coverage_manifest"]),
                    "approval_authority": "none",
                }
            if args.narrative_operation == "import":
                return narrative_packets.import_response(project, args.input)
            if args.narrative_operation == "report":
                return narrative_packets.report(project, args.input, args.output)
            value = narrative_packets.read_response(args.input)
            narrative_packets.validate_response(project, value)
            return {
                "valid_items": len(value["items"]),
                "nodes": len(value["nodes"]),
                "support_drafts": len(value["support_drafts"]),
                "review_state": "unreviewed",
                "approval_authority": "none",
            }
        if args.operation == "curate":
            from jeb import knowledge_curation

            if args.curation_operation == "export":
                return knowledge_curation.report(project, args.output, args.source)
            if args.curation_operation == "apply":
                return knowledge_curation.apply(project, args.decisions)
            receipt = knowledge_curation.validate_decisions(
                project, knowledge_curation.read_decisions(args.decisions)
            )
            return {
                "valid_items": len(receipt["decisions"]["items"]),
                "owner_actions_created": 0,
                "approvals_created": 0,
            }
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
        return project_search(project, args.query, args.source)
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
        if args.command == "work":
            from jeb import workbench

            for stream in (sys.stdout, sys.stderr):
                if hasattr(stream, "reconfigure"):
                    stream.reconfigure(encoding="utf-8", errors="replace")
            try:
                return workbench.run(
                    Project(args.root, synthetic=args.synthetic),
                    args.action,
                    demo=args.demo,
                    source_id=args.source,
                )
            except KeyboardInterrupt:
                print("\nCancelled.")
                return 130
        result = run(args)
    except (ValueError, OSError, UnicodeError, sqlite3.Error) as exc:
        message = str(exc)
        if args.command == "work":
            from jeb.workbench import visible

            message = (
                "Invalid saved data; use its explicit validator for details"
                if " schema:" in message
                else message
            )
            message = visible(message)
        print(f"jeb: {message}", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(canonical(result))
    return 2 if args.command in ("historical", "reading") and result.get("error") else 0
