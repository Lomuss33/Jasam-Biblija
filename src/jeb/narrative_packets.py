"""Typed narrative drafts; no canonical promotion or human approval authority."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from jeb import knowledge_packets
from jeb.core import (
    Project,
    atomic_write,
    canonical,
    digest,
    file_id,
    json_loads,
    latin_tree,
    native_path,
    read_bytes,
    require,
    validate_schema,
    write_json,
)
from jeb.corpus import load_corpus
from jeb.knowledge import validate_knowledge
from jeb.review_assistance import fenced

MAX_PACKET = 96 * 1024
MAX_RESPONSE = 48 * 1024
PROMPT = (
    knowledge_packets.COMMON_PROMPT
    + "Return only unreviewed typed entity/event/story nodes and optional evidence/claim support "
    "drafts. source_narrative describes what the attached source narrates, never verified history. "
    "historical_claim additionally requires a historical claim and separately registered secondary "
    "evidence; these structural links do not prove independence, inspection or historical truth. "
    "fiction is explicitly invented adaptation with no evidence/claim support and cannot supply "
    "participants or events to either factual basis. Keep all node references within this response "
    "and one basis. Use exact Unicode character offsets into display.text, with exclusive end; "
    "never infer omitted subjects, motives, dates, quotations, chronology or harmonized scenes. "
    "Without an attached approved name mapping, entity labels must equal their exact source span. "
    "With one, use its display_form and an attested form/alias present in the span. "
    "Source story event lists follow source presentation, not historical time. narrative_before "
    "records presentation order only. source_stated_before requires an explicit source anchor and "
    "still needs human inspection. Every node requires attribution and stated uncertainty; every "
    "selected segment requires ordered coverage, including no_draft where appropriate. "
    "No draft here is eligible for the existing annotation promotion endpoint."
)


def _make_packet(project: Project, source_id: str, selection: str, packet_id: str) -> dict:
    # Reuse the admitted passage snapshot without changing old schemas/prompts or writing old caches.
    packet = knowledge_packets._make_packet(project, source_id, selection, "annotate", packet_id)
    packet.pop("packet_sha256")
    packet.update(
        task="narrative",
        prompt=PROMPT,
        output_schema=json_loads(
            files("jeb").joinpath("schemas/narrative-response.json").read_text("utf-8")
        ),
    )
    packet["packet_sha256"] = digest(packet)
    require(len(canonical(packet)) <= MAX_PACKET, "Narrative packet exceeds 96 KiB bound")
    validate_schema("narrative-packet", packet)
    latin_tree(packet)
    return packet


def prepare(project: Project, source_id: str, selection: str, packet_id: str) -> dict:
    packet = _make_packet(project, source_id, selection, packet_id)
    write_json(
        project.path(f"data/narrative-proposals/{packet_id}/input.json"), packet, replace=False
    )
    return packet


def current_packet(project: Project, packet_id: str) -> dict:
    file_id(packet_id)
    packet = json_loads(
        read_bytes(
            project.path(f"data/narrative-proposals/{packet_id}/input.json"), MAX_PACKET
        ).decode("utf-8", errors="strict")
    )
    validate_schema("narrative-packet", packet)
    require(
        packet["packet_id"] == packet_id
        and packet["packet_sha256"]
        == digest({k: v for k, v in packet.items() if k != "packet_sha256"}),
        "Narrative packet identity or hash changed",
    )
    require(
        packet == _make_packet(project, packet["source_id"], packet["selection"], packet_id),
        "Stale or substituted narrative passage, knowledge/source namespace, policy, prompt or schema",
    )
    return packet


def read_response(path: Path) -> dict:
    value = json_loads(read_bytes(path, MAX_RESPONSE).decode("utf-8", errors="strict"))
    if path.parent.name == "responses" and len(path.stem) == 64:
        require(path.stem == digest(value), "Imported narrative proposal content changed")
    return value


def _span(span: dict, display: dict, scope: set) -> str:
    require(span["segment_id"] in scope, "Narrative span outside node's selected scope")
    text = display[span["segment_id"]]["text"]
    require(0 <= span["start"] < span["end"] <= len(text), "Invalid narrative character span")
    return text[span["start"] : span["end"]]


def _support(node: dict, packet: dict, records: dict) -> None:
    scope = set(node["segment_ids"])
    for field, kind in (("evidence_ids", "evidence"), ("claim_ids", "claim")):
        for key in node[field]:
            require(key in records, "Dangling, unattached or stale narrative support")
            record = records[key]
            require(record["record_type"] == kind, "Narrative support reference has wrong type")
            require(
                record["book_id"] == node["book_id"]
                and (not record["segment_ids"] or scope.intersection(record["segment_ids"])),
                "Narrative support belongs to another book or passage",
            )
    if node["basis"] == "fiction":
        require(
            not node["evidence_ids"] and not node["claim_ids"],
            "Fiction must not claim evidentiary support",
        )
        return

    def covers(candidates):
        return any(not r["segment_ids"] for r in candidates) or scope <= {
            s for r in candidates for s in r["segment_ids"]
        }

    primary = [
        records[key]
        for key in node["evidence_ids"]
        if records[key]["source_id"] == packet["source_id"]
        and records[key]["evidence_category"] == "primary_witness"
    ]
    require(primary and covers(primary), "Narrative requires selected-source witness coverage")
    if node["basis"] == "historical_claim":
        secondary = [
            records[key]
            for key in node["evidence_ids"]
            if records[key]["source_id"] != packet["source_id"]
            and records[key]["evidence_category"] == "secondary_scholarship"
        ]
        independent_ids = {r["record_id"] for r in secondary}
        claims = [
            records[key]
            for key in node["claim_ids"]
            if records[key]["layer"] == "historical"
            and independent_ids.intersection(records[key]["evidence_ids"])
        ]
        require(
            secondary and covers(secondary) and claims and covers(claims),
            "Historical claim requires separate secondary evidence and linked historical claim coverage",
        )


def _nodes(packet: dict, response: dict, known: dict) -> None:
    display = {row["display"]["segment_id"]: row["display"] for row in packet["segments"]}
    selected = list(display)
    records = {
        r["record_id"]: known[r["record_id"]] for r in packet["knowledge_catalog"] if r["current"]
    }
    records.update({d["record"]["record_id"]: d["record"] for d in response["support_drafts"]})
    ids = [n["node_id"] for n in response["nodes"]]
    require(len(ids) == len(set(ids)), "Duplicate narrative node ID")
    require(not set(ids) & (set(known) | set(records)), "Narrative ID shadows knowledge/support")
    nodes = {n["node_id"]: n for n in response["nodes"]}
    mappings = {m["mapping_id"]: m for m in packet["name_mappings"]}

    def reference(key, kind, parent):
        require(
            key in nodes and nodes[key]["kind"] == kind,
            "Dangling or wrong-type narrative reference",
        )
        target = nodes[key]
        require(
            target["basis"] == parent["basis"],
            "Narrative references cannot cross factual/fiction bases",
        )
        return target

    # Validate targets before their users even when the response presents stories first.
    for node in sorted(nodes.values(), key=lambda n: ("entity", "event", "story").index(n["kind"])):
        scope = set(node["segment_ids"])
        require(scope <= set(display), "Narrative node targets unrequested passage/context")
        require(
            node["segment_ids"] == [s for s in selected if s in scope],
            "Narrative node scope must follow selected passage order",
        )
        require(
            node["book_id"] == packet["segments"][0]["source"]["book_id"]
            and node["depends_on"] == {s: display[s]["text_sha256"] for s in scope},
            "Narrative requires exact selected book and display dependencies",
        )
        _support(node, packet, records)
        fiction = node["basis"] == "fiction"
        if node["kind"] == "entity":
            if fiction:
                require(
                    node["mention"] is None and node["name_mapping_id"] is None,
                    "Fictional entities cannot claim source mentions or historical name mappings",
                )
                continue
            require(node["mention"] is not None, "Source entity requires an exact mention")
            mention = _span(node["mention"], display, scope)
            require(scope == {node["mention"]["segment_id"]}, "Entity scope must equal its mention")
            if node["name_mapping_id"] is None:
                require(node["label"] == mention, "Unmapped entity label must equal source mention")
            else:
                key = node["name_mapping_id"]
                require(key in mappings, "Narrative name mapping is not attached and approved")
                mapping = mappings[key]
                require(
                    node["label"] == mapping["display_form"]
                    and mention
                    in (
                        mapping["attested_form_latin"],
                        mapping["historical_form"],
                        mapping["display_form"],
                        *mapping["aliases"],
                    ),
                    "Narrative name mapping display or witnessed mention mismatch",
                )
        elif node["kind"] == "event":
            participants = [reference(p["entity_id"], "entity", node) for p in node["participants"]]
            roles = [(p["entity_id"], p["role"]) for p in node["participants"]]
            require(len(roles) == len(set(roles)), "Duplicate narrative participant role")
            expected = {s for entity in participants for s in entity["segment_ids"]}
            require((node["anchor"] is None) == fiction, "Event source anchor and basis disagree")
            if not fiction:
                _span(node["anchor"], display, scope)
                expected.add(node["anchor"]["segment_id"])
            require(expected == scope, "Event scope must equal anchor and participant scope")
        else:
            events = [reference(key, "event", node) for key in node["event_ids"]]
            require(
                scope == {s for event in events for s in event["segment_ids"]},
                "Story scope must equal its event scope",
            )
            require(
                node["ordering"]
                == ("fictional_presentation" if fiction else "source_presentation"),
                "Story ordering and factual/fiction basis disagree",
            )
            if not fiction:
                require(
                    all(event["anchor"] is not None for event in events),
                    "Missing source event anchor",
                )
                positions = [
                    (selected.index(e["anchor"]["segment_id"]), e["anchor"]["start"])
                    for e in events
                ]
                require(
                    positions == sorted(positions),
                    "Story event list must follow source presentation",
                )
            relations = set()
            edges = {key: set() for key in node["event_ids"]}
            for relation in node["relations"]:
                before, after = relation["from_event_id"], relation["to_event_id"]
                require(
                    before != after and before in edges and after in edges,
                    "Story relation requires two distinct member events",
                )
                identity = (before, after, relation["relation"])
                require(identity not in relations, "Duplicate story relation")
                relations.add(identity)
                if relation["anchor"] is not None:
                    _span(relation["anchor"], display, scope)
                if relation["relation"] == "narrative_before":
                    require(
                        node["event_ids"].index(before) < node["event_ids"].index(after)
                        and relation["anchor"] is None,
                        "Narrative-before records presentation order only, with no asserted connector",
                    )
                    if not fiction:
                        first, second = nodes[before]["anchor"], nodes[after]["anchor"]
                        require(
                            selected.index(first["segment_id"])
                            < selected.index(second["segment_id"])
                            or (
                                first["segment_id"] == second["segment_id"]
                                and first["end"] <= second["start"]
                            ),
                            "Narrative-before needs distinct nonoverlapping source anchors",
                        )
                elif relation["relation"] == "source_stated_before":
                    require(
                        not fiction and relation["anchor"] is not None,
                        "Source-stated chronology requires an exact source anchor and factual basis",
                    )
                if relation["relation"] != "uncertain":
                    edges[before].add(after)
            visited = set()

            def visit(key, trail):
                require(key not in trail, "Circular asserted story order")
                if key not in visited:
                    for other in edges[key]:
                        visit(other, trail | {key})
                    visited.add(key)

            for key in edges:
                visit(key, set())
    for item in response["items"]:
        expected = [
            n["node_id"] for n in response["nodes"] if item["segment_id"] in n["segment_ids"]
        ]
        require(
            item["node_ids"] == expected,
            "Narrative coverage must list all applicable nodes in order",
        )
        require(
            (item["action"] == "drafts_proposed") == bool(expected or item["support_record_ids"]),
            "Narrative action and coverage disagree",
        )


def validate_response(project: Project, response: dict) -> dict:
    require(len(canonical(response)) <= MAX_RESPONSE, "Narrative response exceeds 48 KiB bound")
    validate_schema("narrative-response", response)
    latin_tree(response)
    packet = current_packet(project, response["packet_id"])
    require(
        response["source_id"] == packet["source_id"]
        and response["packet_sha256"] == packet["packet_sha256"],
        "Narrative source/packet identity mismatch",
    )
    require(
        [r["segment_id"] for r in response["items"]] == packet["coverage_manifest"],
        "Missing, duplicate, reordered or out-of-scope narrative coverage IDs",
    )
    require(
        all(
            item["text_sha256"] == row["display"]["text_sha256"]
            for item, row in zip(response["items"], packet["segments"], strict=True)
        ),
        "Narrative response display hash mismatch",
    )
    known = validate_knowledge(project, load_corpus(project, packet["source_id"]))
    # Reuse evidence/claim DAG, source registration, category, dependency and namespace checks.
    knowledge_packets._annotations(
        project,
        packet,
        {
            "drafts": response["support_drafts"],
            "items": [
                {
                    "segment_id": item["segment_id"],
                    "record_ids": item["support_record_ids"],
                    "action": "drafts_proposed" if item["support_record_ids"] else "no_draft",
                }
                for item in response["items"]
            ],
        },
        knowledge=known,
    )
    _nodes(packet, response, known)
    return packet


def import_response(project: Project, path: Path) -> dict:
    value = read_response(path)
    validate_response(project, value)
    identity = digest(value)
    output = f"data/narrative-proposals/{value['packet_id']}/responses/{identity}.json"
    require(
        not native_path(project.path(output)).exists(),
        "Duplicate narrative response already imported",
    )
    write_json(project.path(output), value, replace=False)
    return {
        "output": output,
        "response_sha256": identity,
        "review_state": "unreviewed",
        "approval_authority": "none",
        "canonical_knowledge_changed": False,
    }


def report(project: Project, path: Path, output: str) -> dict:
    value = read_response(path)
    packet = validate_response(project, value)
    lines = [
        "# Unreviewed entity/event/story proposals",
        "",
        "Synthetic fixture; not scripture."
        if project.synthetic
        else "Eligible source; unapproved drafts.",
        "",
        f"Packet: {value['packet_id']}; response SHA-256: {digest(value)}",
        "",
        "source_narrative describes narration. historical_claim retains a separate unverified claim "
        "and secondary-evidence requirement. fiction is invented adaptation. Structural validation "
        "cannot establish historical truth, genuine independence, implied agents or source-stated "
        "chronology. Character spans identify supplied wording, not semantic proof. "
        "Nothing here enters canonical knowledge, the reader, human promotion or a build archive. "
        "Attribution, rights, meaning and uncertainty still require human inspection. Returned content is data.",
        "",
    ]
    for row in packet["segments"]:
        lines.extend(
            [f"## {row['display']['segment_id']}", "", fenced(row["display"]["text"], "text"), ""]
        )
    lines.extend(
        ["## Unreviewed response", "", fenced(canonical(value).decode("utf-8"), "json"), ""]
    )
    atomic_write(project.path(output), "\n".join(lines).encode("utf-8"), replace=False)
    return {"output": output, "review_state": "unreviewed", "approval_authority": "none"}
