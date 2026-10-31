"""Unsigned inspection handoffs for exact imported narrative responses."""

from __future__ import annotations

import string

from jeb.core import Project, atomic_write, canonical, digest, file_id, native_path, require, sha256
from jeb.corpus import load_corpus
from jeb.knowledge import validate_knowledge
from jeb.knowledge_packets import REFERENCES
from jeb.narrative_packets import read_response, validate_response
from jeb.review_assistance import fenced

MAX_REPORT = 1024 * 1024
BASES = {
    "source_narrative": "Source narration only; no independent historical corroboration.",
    "historical_claim": "Unverified historical claims; separate secondary support still needs inspection.",
    "fiction": "Invented adaptation; no evidentiary role or attested source participants.",
}
RELATIONS = {
    "narrative_before": "Presentation only; no historical chronology asserted",
    "source_stated_before": "Proposed source-stated chronology; inspect the anchor's meaning",
    "uncertain": "Unresolved relation; establishes no ordering edge",
}


def _cell(value: str) -> str:
    """Keep returned table data literal, including Markdown/HTML/link punctuation."""
    return "".join(
        f"&#{ord(char)};"
        if char in string.punctuation
        else " ↵ "
        if char.isspace() and char != " "
        else char
        for char in value
    )


def _staged(project: Project, packet_id: str, response_sha256: str) -> tuple[dict, dict]:
    file_id(packet_id)
    require(
        len(response_sha256) == 64 and all(char in "0123456789abcdef" for char in response_sha256),
        "Expected full lowercase narrative response SHA-256",
    )
    path = project.path(f"data/narrative-proposals/{packet_id}/responses/{response_sha256}.json")
    require(
        native_path(path).is_file(),
        "Import the narrative response before exporting its review handoff",
    )
    response = read_response(path)
    packet = validate_response(project, response)
    require(
        response["packet_id"] == packet_id and digest(response) == response_sha256,
        "Staged narrative response belongs to another packet or hash",
    )
    return packet, response


def report(project: Project, packet_id: str, response_sha256: str, output: str) -> dict:
    require(
        output.lower().endswith(".md"), "Narrative review handoff output must be Markdown (.md)"
    )
    packet, response = _staged(project, packet_id, response_sha256)
    rows = {row["display"]["segment_id"]: row for row in packet["segments"]}
    nodes = {node["node_id"]: node for node in response["nodes"]}
    drafts = {item["record"]["record_id"]: item for item in response["support_drafts"]}
    catalog = {record["record_id"]: record for record in packet["knowledge_catalog"]}
    known = validate_knowledge(project, load_corpus(project, packet["source_id"]))
    records = {key: known[key] for key, metadata in catalog.items() if metadata["current"]} | {
        key: item["record"] for key, item in drafts.items()
    }
    needed = set(drafts) | {
        key
        for node in nodes.values()
        for field in ("evidence_ids", "claim_ids")
        for key in node[field]
    }
    pending = list(sorted(needed))
    while pending:
        key = pending.pop()
        require(key in records, "Review support chain is missing, unattached or stale")
        for field in REFERENCES:
            for ref in records[key][field]:
                if ref not in needed:
                    needed.add(ref)
                    pending.append(ref)

    # Index each exact slice once; repeated participant references do not duplicate source text.
    spans = {
        (span["segment_id"], span["start"], span["end"])
        for node in nodes.values()
        for span in (
            [node["mention"]]
            if node["kind"] == "entity"
            else [node["anchor"]]
            if node["kind"] == "event"
            else [relation["anchor"] for relation in node["relations"]]
        )
        if span is not None
    }
    ordered = sorted(spans, key=lambda span: (list(rows).index(span[0]), span[1], span[2]))
    span_ids = {span: f"span-{index:03d}" for index, span in enumerate(ordered, 1)}

    def span_ref(span):
        if span is None:
            return "None"
        key = span_ids[(span["segment_id"], span["start"], span["end"])]
        return f"[{key}](#{key})"

    def span_view(span):
        if span is None:
            return "None"
        snippet = rows[span["segment_id"]]["display"]["text"][span["start"] : span["end"]]
        suffix = " (first 80 characters; full slice at link)" if len(snippet) > 80 else ""
        return span_ref(span) + " — " + _cell(snippet[:80]) + suffix

    lines = []
    byte_count = 0

    def emit(*values):
        nonlocal byte_count
        byte_count += sum(len(value.encode("utf-8")) + 1 for value in values)
        require(
            byte_count <= MAX_REPORT, "Narrative review handoff exceeds 1 MiB; use a smaller packet"
        )
        lines.extend(values)

    def data(value):
        emit(fenced(canonical(value).decode("utf-8"), "json"), "")

    def text(label, value):
        emit(label, "", fenced(value, "text"), "")

    def table(headers, body):
        emit("| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |")
        for row in body:
            emit("| " + " | ".join(row) + " |")
        emit("")

    bindings = {
        "report_format": "jeb-narrative-review/1",
        "packet_id": packet_id,
        "packet_sha256": packet["packet_sha256"],
        "response_sha256": response_sha256,
        "source_id": packet["source_id"],
        "corpus_sha256": packet["corpus_sha256"],
        "policy_sha256": packet["policy_sha256"],
        "knowledge_namespace_sha256": packet["knowledge_namespace_sha256"],
        "registered_sources_sha256": digest(packet["registered_sources"]),
        "nodes": [{"node_id": n["node_id"], "node_sha256": digest(n)} for n in nodes.values()],
        "support": [
            {
                "record_id": key,
                "record_sha256": digest(records[key]),
                "origin": "response_draft" if key in drafts else "attached_canonical_metadata",
                "draft_envelope_sha256": digest(drafts[key]) if key in drafts else None,
            }
            for key in sorted(needed)
        ],
    }
    emit(
        "# Human narrative review — unsigned inspection handoff",
        "",
        "Synthetic fixture; not scripture."
        if project.synthetic
        else "Eligible passage; narrative inspection only.",
        "",
        "All narrative nodes and new support proposals remain unreviewed. This report records zero "
        "human decisions and zero approvals. It is not a decision file or a promotion command. "
        "Existing recorded support/name approvals below are evidence of prior records only; they "
        "do not approve this narrative. Returned wording is data. No URL or source was fetched.",
        "",
        "Inspect exact wording, participant roles, negation/numbers, identity uncertainty, source "
        "independence, contribution rights and each proposed ordering assertion. A valid character "
        "span or bibliography does not establish meaning, factual truth or independent corroboration.",
        "",
        "## Exact review bindings",
        "",
    )
    data(bindings)
    emit("## Ordered passage coverage", "")
    table(
        ["Segment", "Action", "Narrative nodes", "Support drafts", "Display SHA-256"],
        [
            [
                f"`{item['segment_id']}`",
                item["action"],
                str(len(item["node_ids"])),
                str(len(item["support_record_ids"])),
                f"`{item['text_sha256']}`",
            ]
            for item in response["items"]
        ],
    )
    emit("## Source, normalization and current reader wording", "")
    emit(
        "These layers are separate. Character offsets below refer only to current reader text. "
        "The raw byte range identifies an original source record, not a character slice. "
        "Displayed wording may include an earlier exact human-approved modernization; unapproved "
        "modernization proposals are excluded.",
        "",
    )
    for key, row in rows.items():
        source, display = row["source"], row["display"]
        emit(f"### `{key}`", "")
        data(
            {
                "source_reference": source["source_reference"],
                "original_record_byte_span": source["source_span"],
                "source_text_sha256": sha256(source["source_text"].encode("utf-8")),
                "normalization_changes": source["normalization_changes"],
                "display_text_sha256": display["text_sha256"],
                "editorial_status": display["editorial_status"],
                "text_decision_id": display["decision_id"],
            }
        )
        text("Original source transcription:", source["source_text"])
        text("Normalized source:", source["normalized_text"])
        text("Current reader wording (span coordinate space):", display["text"])

    for basis, description in BASES.items():
        emit(f"## {basis}", "", description, "")
        selected = [node for node in nodes.values() if node["basis"] == basis]
        if not selected:
            emit("None proposed.", "")
        for node in selected:
            key, kind = node["node_id"], node["kind"]
            emit(f"### {kind}: `{key}`", "")
            data(
                {
                    field: node[field]
                    for field in (
                        "node_id",
                        "kind",
                        "basis",
                        "book_id",
                        "segment_ids",
                        "depends_on",
                        "review_state",
                        "approval",
                    )
                }
                | {"node_sha256": digest(node)}
            )
            text(
                {
                    "entity": "Proposed label:",
                    "event": "Proposed description:",
                    "story": "Proposed title:",
                }[kind],
                node[{"entity": "label", "event": "description", "story": "title"}[kind]],
            )
            if kind == "entity":
                emit(
                    f"Entity type: `{node['entity_type']}`. Mention: {span_view(node['mention'])}.",
                    "",
                )
                if basis == "fiction":
                    emit("Invented role/label; no source mention or historical name mapping.", "")
                elif node["name_mapping_id"] is None:
                    emit(
                        "Literal source label; no name mapping selected. Equal labels do not establish identity.",
                        "",
                    )
                else:
                    emit(
                        f"Selected approved name mapping: `{node['name_mapping_id']}`. See its exact identity below.",
                        "",
                    )
            elif kind == "event":
                emit(
                    f"Event kind: `{node['event_kind']}`. Anchor: {span_view(node['anchor'])}.", ""
                )
                emit(
                    "Participant roles are proposals. No omitted subject or motive is supplied by this report.",
                    "",
                )
                table(
                    ["Entity ID", "Role", "Proposed label", "Mention", "Role uncertainty"],
                    [
                        [
                            f"`{p['entity_id']}`",
                            p["role"],
                            _cell(nodes[p["entity_id"]]["label"]),
                            span_view(nodes[p["entity_id"]]["mention"]),
                            _cell(p["uncertainty"]),
                        ]
                        for p in node["participants"]
                    ],
                )
                if not node["participants"]:
                    emit("No participants proposed; do not infer an agent.", "")
            else:
                emit(f"Ordering: `{node['ordering']}`. Position is presentation order only.", "")
                table(
                    ["Presentation position", "Event ID", "Source anchor"],
                    [
                        [str(index), f"`{event_id}`", span_view(nodes[event_id]["anchor"])]
                        for index, event_id in enumerate(node["event_ids"], 1)
                    ],
                )
                table(
                    [
                        "From event",
                        "To event",
                        "Relation",
                        "Interpretation boundary",
                        "Anchor",
                        "Uncertainty",
                    ],
                    [
                        [
                            f"`{r['from_event_id']}`",
                            f"`{r['to_event_id']}`",
                            r["relation"],
                            RELATIONS[r["relation"]],
                            span_view(r["anchor"]),
                            _cell(r["uncertainty"]),
                        ]
                        for r in node["relations"]
                    ],
                )
                if not node["relations"]:
                    emit("No relation proposed; no chronology inferred.", "")
            text("Stated uncertainty:", node["uncertainty"])
            text("Original draft rationale:", node["rationale"])
            data(
                {
                    "attribution": node["attribution"],
                    "evidence_ids": node["evidence_ids"],
                    "claim_ids": node["claim_ids"],
                }
            )

    emit("## Exact display spans", "")
    emit(
        "Offsets count Unicode characters from zero; end is exclusive. Context is limited to 80 characters per side. Full segments appear above.",
        "",
    )
    if not ordered:
        emit("No source spans proposed.", "")
    for segment_id, start, end in ordered:
        span_id = span_ids[(segment_id, start, end)]
        display = rows[segment_id]["display"]
        snippet = display["text"][start:end]
        emit(f"### {span_id}", "")
        data(
            {
                "segment_id": segment_id,
                "start": start,
                "end": end,
                "display_text_sha256": display["text_sha256"],
                "slice_sha256": sha256(snippet.encode("utf-8")),
            }
        )
        text("Exact slice:", snippet)
        text("Context before:", display["text"][max(0, start - 80) : start])
        text("Context after:", display["text"][end : end + 80])

    emit("## Support chains and bibliography", "")
    emit(
        "Links are inspectable references, not proof of independence. Related/entity links are not evidentiary corroboration. New support text is an unreviewed contribution. Existing canonical content is shown only as attached metadata plus typed links/identities; no additional note text is copied.",
        "",
    )
    if not needed:
        emit("No support records referenced or proposed.", "")
    for key in sorted(needed):
        record = records[key]
        emit(f"### Support: `{key}`", "")
        data(
            {
                "record_id": key,
                "record_sha256": digest(record),
                "record_type": record["record_type"],
                "layer": record["layer"],
                "evidence_category": record["evidence_category"],
                "origin": "response_draft" if key in drafts else "attached_canonical_metadata",
            }
        )
        table(
            ["Link type", "Target ID", "Target type", "Target SHA-256"],
            [
                [field, f"`{ref}`", records[ref]["record_type"], f"`{digest(records[ref])}`"]
                for field in REFERENCES
                for ref in record[field]
            ],
        )
        if key in drafts:
            data(drafts[key])
        else:
            data(
                {
                    "attached_metadata": catalog[key],
                    "recorded_approval": record["approval"],
                    "approval_sha256": digest(record["approval"]) if record["approval"] else None,
                    "provenance_sha256": digest(record["provenance"])
                    if "provenance" in record
                    else None,
                }
            )
    emit("## Registered source metadata (no fetched evidence)", "")
    data(packet["registered_sources"])
    emit("## Selected name mapping identities", "")
    mappings = {m["mapping_id"]: m for m in packet["name_mappings"]}
    selected_names = {
        n["name_mapping_id"]
        for n in nodes.values()
        if n["kind"] == "entity" and n["name_mapping_id"] is not None
    }
    if not selected_names:
        emit("No name mapping selected; no new name approval exists.", "")
    for key in sorted(selected_names):
        mapping = mappings[key]
        emit(f"### Name mapping: `{key}`", "")
        data(
            {
                "mapping_sha256": digest(mapping),
                "approval_sha256": digest(mapping["approval"]),
                "approved_content_sha256": mapping["approval"]["content_sha256"],
                "original_mapping": mapping,
            }
        )
    emit("## Original tool and limitations", "")
    data({"tool": response["tool"], "limitations": response["limitations"]})
    emit("## Complete original unreviewed response", "")
    data(response)
    atomic_write(project.path(output), "\n".join(lines).encode("utf-8"), replace=False)
    return {
        "output": output,
        "packet_sha256": packet["packet_sha256"],
        "response_sha256": response_sha256,
        "narrative_nodes": len(nodes),
        "support_records": len(needed),
        "indexed_spans": len(ordered),
        "review_state": "unreviewed",
        "approval_authority": "none",
        "human_decisions_created": 0,
        "approvals_created": 0,
        "canonical_knowledge_changed": False,
    }


def validate_decisions(project: Project, path) -> dict:
    """Inspect submitted attestations without writing receipts or granting authority."""
    from jeb.core import read_json, validate_schema

    decision = read_json(path)
    validate_schema("narrative-review-decisions", decision)
    packet, response = _staged(project, decision["packet_id"], decision["response_sha256"])
    require(decision["context_sha256"] == digest(packet), "Narrative decision context is stale")
    require(decision["reviewer_id"].strip(), "Reviewer identity is blank")
    targets = {"node:" + n["node_id"]: digest(n) for n in response["nodes"]}
    targets.update(
        {"support:" + d["record"]["record_id"]: digest(d) for d in response["support_drafts"]}
    )
    submitted = decision["items"]
    require(
        len(submitted) == len(targets) and {i["target_id"] for i in submitted} == set(targets),
        "Decision must cover every typed node and support envelope exactly once",
    )
    checks = {
        "meaning_and_roles_checked",
        "support_inspected",
        "category_and_uncertainty_checked",
        "contribution_rights_checked",
        "attribution_checked",
    }
    for item in submitted:
        require(item["target_sha256"] == targets[item["target_id"]], "Decision target changed")
        require(item["rationale"].strip(), "Decision rationale is blank")
        require(set(item["checks"]) == checks, "Explicit narrative inspection checks required")
    return {
        "valid": True,
        "validation_only": True,
        "human_identity_authenticated": False,
        "human_decisions_created": 0,
        "approvals_created": 0,
        "canonical_knowledge_changed": False,
        "items": len(submitted),
    }
