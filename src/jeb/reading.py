"""Opt-in synthetic reading desk; versioned documents inside existing v3 articles.

The ordinary bank writer owns revisions, locks, recovery and backups. Reading
documents add exact anchor semantics without changing any bank schema.
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from jeb.bank import backup, storage
from jeb.bank.references import binding, locator_check, resolve
from jeb.core import (
    JebError,
    canonical,
    json_loads,
    latin,
    latin_tree,
    require,
    sha256,
    validate_schema,
)

MAX_REQUEST = 16 * 1024
MAX_RESPONSE = 1024 * 1024
KINDS = {"reading_view": "reading-view-v1", "reading_item": "reading-item-v1"}
FIELDS = {
    "view_ref",
    "request_id",
    "kind",
    "passage_id",
    "text",
    "anchor",
    "target_id",
    "edit_record_id",
    "expected_revision",
}


class ReadingError(JebError):
    pass


def contracts() -> dict:
    return {
        name: sha256(files("jeb").joinpath(f"schemas/{name}.json").read_bytes())
        for name in KINDS.values()
    }


def document(body: str | None) -> dict:
    require(body is not None, "Missing reading document")
    value = json_loads(body)
    require(
        isinstance(value, dict) and value.get("document_type") in KINDS, "Not a reading document"
    )
    validate_schema(KINDS[value["document_type"]], value)
    return value


def source(state: dict, passage: dict) -> dict | None:
    if passage["source_ref"] is None:
        return None
    found = resolve(passage["source_ref"], "source", state["revisions"])
    require(found["body"] is not None and len(found["body"]) <= 20_000, "Invalid reading source")
    return found


def validate_view(value: dict, state: dict) -> None:
    validate_schema("reading-view-v1", value)
    require(
        value["workspace_id"] == state["workspace"]["workspace_id"], "Foreign reading workspace"
    )
    require(value["contracts"] == contracts(), "Reading contract changed; retain matching engine")
    latin_tree(value, "reading view")
    ids = [item["id"] for item in value["passages"]]
    require(bool(ids) and len(ids) == len(set(ids)), "Invalid reading passage IDs")
    passages = {item["id"]: item for item in value["passages"]}
    for reference in value["books"].values():
        book = resolve(reference, "entity", state["revisions"])
        require(book["record"]["data"]["entity_type"] == "work", "Reading book must be a work")
    for passage in passages.values():
        require(passage["book"] in value["books"], "Missing reading book")
        source(state, passage)
        for connection in passage["connections"]:
            require(
                connection["target_id"] in passages and connection["target_id"] != passage["id"],
                "Invalid reading destination",
            )
        for evidence in passage["evidence"]:
            require(evidence["passage_id"] in passages, "Missing evidence passage")
            target = source(state, passages[evidence["passage_id"]])
            locator_check(
                {"type": "text_span", **evidence["anchor"]}, target["body"] if target else None
            )


def check_item(value: dict, state: dict, view_id: str) -> tuple[dict, dict]:
    validate_schema("reading-item-v1", value)
    latin(value["text"], "private reading item")
    require(value["view_ref"]["record_id"] == view_id, "Foreign reading view")
    prior = resolve(value["view_ref"], "article", state["revisions"])
    old_view = document(prior["body"])
    require(old_view["document_type"] == "reading_view", "Reference is not a reading view")
    validate_view(old_view, state)
    passage = next((p for p in old_view["passages"] if p["id"] == value["passage_id"]), None)
    require(passage is not None, "Unknown reading passage")
    target = source(state, passage)
    if value["anchor"] is not None:
        locator_check({"type": "text_span", **value["anchor"]}, target["body"] if target else None)
    if value["kind"] == "highlight":
        require(value["anchor"] is not None, "Highlight needs an exact selection")
    else:
        require(bool(value["text"].strip()), "A note or connection reason is required")
    if value["kind"] == "connection":
        require(
            value["target_id"] in {p["id"] for p in old_view["passages"]}
            and value["target_id"] != passage["id"],
            "Connection needs another destination",
        )
    else:
        require(value["target_id"] is None, "Unexpected connection destination")
    require(
        (value["edit_record_id"] is None) == (value["expected_revision"] is None),
        "Invalid edit binding",
    )
    return old_view, passage


def loaded(state: dict) -> dict:
    require(state["workspace"]["schema_version"] == "3.0", "Reading desk requires managed v3")
    articles = []
    for record in state["records"].values():
        if record["kind"] == "article":
            require(record["visibility"] == "private", "Reading articles must stay private")
            articles.append((record, document(state["bodies"].get(record["id"]))))
    views = [(record, doc) for record, doc in articles if doc["document_type"] == "reading_view"]
    require(len(views) == 1, "Configure a dedicated reading bank with exactly one view")
    record, value = views[0]
    validate_view(value, state)
    reference = binding(state["revisions"][(record["id"], record["revision_id"])])
    items = []
    for item_record, doc in articles:
        if doc["document_type"] != "reading_item":
            continue
        old_view, passage = check_item(doc, state, record["id"])
        required_sources = [passage["source_ref"]["record_id"]] if passage["source_ref"] else []
        require(
            item_record["data"]
            == {
                "subjects": [old_view["books"][passage["book"]]["record_id"]],
                "sources": required_sources,
            },
            "Reading article links differ",
        )
        items.append(
            {
                "id": item_record["id"],
                "revision_id": item_record["revision_id"],
                "revised_at": item_record["revised_at"],
                **doc,
                "current_view": doc["view_ref"] == reference,
                "source_ref": passage["source_ref"],
                "review_state": "private_proposal",
            }
        )
    return {
        "state": state,
        "view": value,
        "view_ref": reference,
        "items": sorted(items, key=lambda item: (item["revised_at"], item["id"])),
    }


def load(root: Path, *, synthetic: bool) -> dict:
    require(synthetic, "Reading desk requires explicit --synthetic opt-in")
    return loaded(storage.read_managed(root))


def view(root: Path, *, synthetic: bool) -> dict:
    data = load(root, synthetic=synthetic)
    passages = []
    for item in data["view"]["passages"]:
        found = source(data["state"], item)
        record = found["record"] if found else None
        passages.append(
            {
                **item,
                "text": found["body"] if found else None,
                "source": {
                    "title": record["title"],
                    **record["data"],
                    "is_current": record["revision_id"]
                    == data["state"]["records"][record["id"]]["revision_id"],
                }
                if record
                else None,
            }
        )
    result = {
        "enabled": True,
        "synthetic": True,
        "releasable": False,
        "view_ref": data["view_ref"],
        "passages": passages,
        "items": data["items"],
        "remaining_saves": storage.MAX_HISTORY - len(data["state"]["chain"]),
    }
    require(len(canonical(result)) <= MAX_RESPONSE, "Reading response exceeds limit")
    return result


def save(root: Path, payload: dict, *, synthetic: bool) -> dict:
    require(isinstance(payload, dict) and set(payload) == FIELDS, "Invalid reading save fields")
    value = {
        "document_type": "reading_item",
        "schema_version": "1.0",
        "synthetic": True,
        "releasable": False,
        **payload,
    }
    validate_schema("reading-item-v1", value)
    for _ in range(3):
        data = load(root, synthetic=synthetic)
        state = data["state"]
        # Search committed history too: retries remain idempotent after later edits.
        for revision in state["revisions"].values():
            if revision["record"]["kind"] != "article":
                continue
            prior = document(revision["body"])
            if prior.get("request_id") == value["request_id"]:
                if prior != value:
                    raise ReadingError("request_id_conflict")
                return {
                    "saved": True,
                    "replayed": True,
                    "id": revision["record"]["id"],
                    "revision_id": revision["record"]["revision_id"],
                    "approvals_created": 0,
                }
        if value["view_ref"] != data["view_ref"]:
            raise ReadingError("stale_view")
        _, passage = check_item(value, state, data["view_ref"]["record_id"])
        identity = value["edit_record_id"]
        if identity:
            old = next((item for item in data["items"] if item["id"] == identity), None)
            if old is None or old["revision_id"] != value["expected_revision"]:
                raise ReadingError("revision_conflict")
            require(
                all(value[key] == old[key] for key in ("kind", "passage_id", "anchor", "view_ref")),
                "Editing cannot move a reading anchor",
            )
        content = {
            "kind": "article",
            "title": f"Private reading {value['kind']}: {passage['id']}",
            "visibility": "private",
            "processing_state": "inbox",
            "data": {
                "subjects": [data["view"]["books"][passage["book"]]["record_id"]],
                "sources": [passage["source_ref"]["record_id"]] if passage["source_ref"] else [],
            },
        }
        try:
            result = storage.save_record(
                root,
                content,
                "local-reading-interface",
                "tool",
                "Save private reading item; no approval",
                canonical(value).decode(),
                identity,
                value["expected_revision"],
                expected_head=state["head"],
            )
            return {"saved": True, "replayed": False, **result}
        except JebError as exc:
            if str(exc) != "Bank HEAD changed; retry operation":
                raise
    raise ReadingError("reading_busy")


def rpc(root: Path, operation: str, *, synthetic: bool, payload: dict | None = None) -> dict:
    try:
        return (
            view(root, synthetic=synthetic)
            if operation == "view"
            else save(root, payload, synthetic=synthetic)
        )
    except ReadingError as exc:
        return {"enabled": False, "error": str(exc)}
    except (OSError, UnicodeError):
        return {"enabled": False, "error": "reading_unavailable"}
    except ValueError as exc:
        message = str(exc)
        code = (
            "reading_busy"
            if "writer is busy" in message.lower()
            else "history_limit"
            if "History limit" in message or "History exceeds" in message
            else "invalid_reading_input"
        )
        return {"enabled": False, "error": code}


def create_demo(root: Path, *, synthetic: bool) -> dict:
    require(synthetic, "Reading demo requires --synthetic")
    storage.initialize(root, "SYNTHETIC reading desk; original software fixture", "3.0")
    common = {"visibility": "private", "processing_state": "inbox"}

    def put(kind, title, data, body=None):
        saved = storage.save_record(
            root,
            {**common, "kind": kind, "title": title, "data": data},
            "reading-fixture-generator",
            "tool",
            "Original synthetic fixture",
            body,
        )
        state = storage.read_managed(root)
        return binding(state["revisions"][(saved["id"], saved["revision_id"])])

    books = {
        book: put("entity", f"{book} reading topic", {"entity_type": "work"})
        for book in ("MAT", "MRK", "JHN")
    }
    texts = [
        "SYNTHETIC SOFTWARE FIXTURE — NOT SCRIPTURE.\n\nLuma opens a ledger in the workshop. Nera places a blue ribbon beside the entry.\n\nLuma records the shelf mark, then leaves the ledger open for Nera.\n\nProtected software-test literals: svjet vrjeme covik razumit.\n",
        "SYNTHETIC SOFTWARE FIXTURE — NOT SCRIPTURE.\n\nNera carries a blue ribbon into a reading room. Sela asks which shelf holds the ledger.\n\nNera writes the shelf mark on a card and sets it beside the ribbon.\n",
    ]
    refs = [
        put(
            "source",
            f"Original invented reading example {i + 1}",
            {
                "source_type": "document",
                "creator": "Original software fixture generated by a tool",
                "translator": None,
                "edition": "Synthetic English fixture v1; not a historical edition",
                "url": None,
                "accessed_at": None,
                "limitations": "Invented software data, not scripture, scholarship or historical evidence.",
            },
            text,
        )
        for i, text in enumerate(texts)
    ]

    def localized(en, bs):
        return {"en": en, "bs": bs}

    ids = ("ledger-entry", "reading-room")
    titles = (
        localized("The ledger and the ribbon", "Zapis i vrpca"),
        localized("A note in the reading room", "Bilješka u čitaonici"),
    )
    passages = []
    for i in range(2):
        quote = "blue ribbon"
        start = texts[i].index(quote)
        passages.append(
            {
                "id": ids[i],
                "book": ("MAT", "MRK")[i],
                "title": titles[i],
                "location": f"Original fiction example {i + 1}",
                "source_language": "en",
                "source_ref": refs[i],
                "explanation": localized(
                    "This invented scene lets you read an explanation beside its exact source. Follow the blue-ribbon connection to compare another scene, then return here.",
                    "Ova izmišljena scena služi za čitanje objašnjenja uz tačan izvor. Prati vezu plave vrpce do druge scene, pa se vrati na ovo mjesto.",
                ),
                "interpretations": [
                    {
                        "by": "Software fixture author; unreviewed example",
                        "text": localized(
                            "The ribbon can be discussed as a shared motif. This is an interpretation of invented writing, not a historical finding.",
                            "Vrpca se može razmatrati kao zajednički motiv. Ovo je tumačenje izmišljenog teksta, ne historijski nalaz.",
                        ),
                    }
                ],
                "evidence": [
                    {
                        "category": "wording",
                        "title": localized(
                            "Exact wording in this fixture", "Tačan zapis u ovom primjeru"
                        ),
                        "text": localized(
                            "This span verifies only that these words occur in the saved original fixture.",
                            "Ovaj raspon potvrđuje samo da se riječi nalaze u sačuvanom izmišljenom primjeru.",
                        ),
                        "passage_id": ids[i],
                        "anchor": {"start": start, "end": start + len(quote), "exact": quote},
                    }
                ],
                "connections": [
                    {
                        "target_id": ids[1 - i],
                        "relation": "shared_motif",
                        "reason": localized(
                            "Both invented scenes mention a blue ribbon. A shared motif does not establish the identity of the characters.",
                            "Obje izmišljene scene spominju plavu vrpcu. Zajednički motiv ne potvrđuje identitet likova.",
                        ),
                    }
                ],
            }
        )
    passages.append(
        {
            "id": "john-9",
            "book": "JHN",
            "title": localized("John 9 · planned study", "Ivan 9 · planirano istraživanje"),
            "location": "JHN 9",
            "source_language": "en",
            "source_ref": None,
            "explanation": localized(
                "Your selected study: meaning and religious blindness, related stories, Jesus as a character, Pharisees in context, symbolism and evidence. No eligible source text or sourced explanation is attached yet.",
                "Odabrano istraživanje: smisao i vjerska sljepoća, povezane priče, Isus kao lik, farizeji u kontekstu, simbolika i dokazi. Dopušten izvorni tekst i objašnjenje potkrijepljeno izvorima još nisu priloženi.",
            ),
            "interpretations": [],
            "evidence": [],
            "connections": [],
        }
    )
    state = storage.read_managed(root)
    value = {
        "document_type": "reading_view",
        "schema_version": "1.0",
        "synthetic": True,
        "releasable": False,
        "workspace_id": state["workspace"]["workspace_id"],
        "contracts": contracts(),
        "books": books,
        "passages": passages,
    }
    validate_view(value, state)
    put(
        "article",
        "Synthetic reading view v1",
        {
            "subjects": [ref["record_id"] for ref in books.values()],
            "sources": [ref["record_id"] for ref in refs],
        },
        canonical(value).decode(),
    )
    return {
        "bank_root": str(root.absolute()),
        "synthetic": True,
        "releasable": False,
        "passages": len(passages),
        "approvals_created": 0,
    }


def create_backup(root: Path, output: Path, *, synthetic: bool) -> dict:
    load(root, synthetic=synthetic)
    return backup.create(root, output)


def restore_backup(input_path: Path, destination: Path, *, synthetic: bool) -> dict:
    require(synthetic, "Reading restore requires --synthetic")
    with backup.checked_backup(input_path) as (_, _, state):
        loaded(state)
    result = backup.restore(input_path, destination)
    load(destination, synthetic=synthetic)
    return result
