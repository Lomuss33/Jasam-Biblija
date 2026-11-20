# John 9 reading desk — first usability pilot

Direction date: 2026-11-19. Implementation update: 2026-11-20. The local synthetic
interaction prototype now implements reading and saved private tools. The real
John 9 source, exegesis and historical-evidence dossier are not populated or cleared.

## Working local prototype — 2026-11-20

For first use, follow [Your first session at the reading desk](READING_DESK_FIRST_SESSION.md).
Windows also has a double-click `start-reading-demo.cmd` launcher. The desk's
**How to use this desk / Kako koristiti stol** control provides the bilingual
walkthrough and opens the practice story without writing any private items.

Run `npm run reading:demo -- --synthetic` after the existing locked Python setup.
Open `http://127.0.0.1:5187/#desk`. The launcher creates `dist/reading-desk-demo`
only when absent, otherwise validates/reopens it. Existing or invalid directories
are preserved; there is no reset/overwrite switch. No npm install is required.

Available behavior:

- Library and prominent search together, including the existing research catalogue.
- English/Bosnian-Herzegovinian reading UI with desktop side-by-side text and
  explanation; attributed views and distinct evidence categories expand on demand.
- Two original invented scenes with exact source wording, a shared-motif connection,
  source locator navigation and a return path preserving reading position.
- Saving, editing and reopening private notes, exact-selection highlights and
  suggested connections, without CLI/JSON/hash copying in the reading task.
- A writing editor beside the source, clear passage-note/selection scope,
  optional highlight comments and recoverable drafts after a same-tab refresh.
- Click/keyboard access to saved highlight comments beside the text, including
  overlapping highlights, and Ctrl+Enter saving with an inline saved-item viewer.
- Conflicting edits show the latest saved version and kept draft, with an explicit
  save-as-separate-item choice that preserves both instead of overwriting.
- Changed-view or removed-passage drafts remain reachable with their original
  quote/recorded credits, a private draft download and an explicit new unanchored
  passage-note recovery flow. Original drafts stay until deliberately discarded.
- Home search includes personal wording and highlighted quotes, with kind filters,
  recent saved work and a route back to the saved item or its exact current quote.
- John 9 as an honest planned topic with no imported text or invented scholarship;
  a private topic note is possible, while highlighting is disabled without text.
- Source text, authored notes, current reading location and an open draft are
  preserved across language switching. Narrow screens stack the reading panes.

The prototype implements interaction mechanics, not the actual John 9 reading
material or historical research. The following owner scenario remains the
acceptance target for a populated study desk. A real-browser synthetic test is
engineering evidence, not a claim that the owner has completed a usability review.

## Storage, writes and recovery

The prototype uses a dedicated managed v3 bank. A `reading-view-v1` document is
stored as the JSON body of one private `article`; it binds the bank workspace,
reading contract hashes, book entities and exact source revisions. Each private
item is another private `article` with a `reading-item-v1` JSON body. These are
explicit document contracts, not new v3 record kinds or evidence approvals.
Generic bank tools can inspect their original bodies; the reading UI provides
the usable projection. Existing v3 schemas and backup formats are unchanged.

Python owns all validation and writing. The bank writer has an optional expected
HEAD guard, used to revalidate an operation after concurrent unrelated writes.
Per-item edits also require the exact expected revision. A stored request UUID
makes retries idempotent even after a later edit or uncertain post-commit failure.
No user identity or owner attestation is fabricated: writer metadata identifies
the local reading interface as a tool, and private items remain proposals.

New local endpoints are GET `/api/reading/session`, GET `/api/reading/view` and
the narrowly scoped POST `/api/reading/items`. Writing requires configured reading
root, synthetic opt-in, write opt-in, exact same-origin Host/Origin, a per-server
session token and bounded JSON. The body is capped at 16 KiB; duplicate keys,
unknown fields, foreign bindings and invalid Unicode spans fail. The HTTP caller
cannot choose a filesystem path, bank root or source file. All other write routes
remain unavailable. The server remains loopback-only with the existing CSP.

For manual configuration instead of the launcher:

```powershell
$env:JEB_READING_ROOT = (Resolve-Path dist/reading-desk-demo).Path
$env:JEB_READING_SYNTHETIC = '1'
$env:JEB_READING_WRITE = '1'
npm run dev
```

Omit `JEB_READING_WRITE` for read-only access. The normal default viewer does not
create a reading workspace or enable private writes automatically.

Saved view/source/item documents and their complete committed history are included
in the existing bank backup. The reading wrappers additionally validate reading
contracts before restore:

```powershell
.\.venv\Scripts\python.exe -m jeb --synthetic reading backup --bank-root dist/reading-desk-demo --output dist/my-reading-backup.zip
.\.venv\Scripts\python.exe -m jeb --synthetic reading restore --input dist/my-reading-backup.zip --destination dist/my-reading-restored
```

Both output and restore destination must be new. To reopen a restored desk, set
`JEB_READING_ROOT` to that destination with the explicit flags above. The wrapper
uses bank backup/restore; it does not copy arbitrary library files, historical
pipeline caches or external PDFs. Keep the matching wheel for versioned contracts.

Browser-local language/position preferences and unfinished drafts are not part of
the bank backup. Drafts are kept in session storage, when available, by reading
view record identity and recover across a refresh in the same tab. Separate
unconfirmed save requests take precedence for exact retry; neither is treated as
a saved bank item. Existing legacy pending requests migrate only for the matching
view. Confirmed items survive reopening the browser or server. Cancel before
saving discards its browser draft and writes nothing. An uncertain save must be checked/
retried rather than falsely claiming cancellation undid a possible commit.

Stale drafts capture their original edition/creator/translator and exact binding
when begun; older drafts explicitly label missing edition metadata. Recovery
prepares a new note on an explicitly chosen current passage, copying only private
wording and dropping quote, connection target and edit binding. The original
draft remains read-only until the user discards it. Its downloadable private JSON
snapshot includes the quote/recorded credits and recovery state; it is browser
state for keeping a copy, with no bank restore/import workflow. A changed prepared
destination needs another explicit choice; it is never silently refreshed.
Recovery saves use the same bounded Python endpoint, request UUIDs and locks.
An unknown save stays immutable across auth/busy/validation failures until a
matching committed result or a conclusive writer-history check settles it.

Existing protective limits remain: 128 full bank history snapshots / 128 MiB
history payload, 20,000 characters per reader source, 32 passage entries and a
bounded view response. Every saved change consumes a snapshot; the UI shows the
remaining count. Hitting a limit preserves existing data. No compaction or silent
history deletion is supplied. This is a small prototype, not a large-corpus store.

Existing editorial pages retain their original language; the bilingual scope is
the new reading desk and its navigation. Search is literal retrieval, not AI
question answering. General explanation editing, identity review, corpus
admission and real scholarly content acquisition remain outside this increment.

## Verification commands

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_reading -v
npm run test:web
npm run test:reading:browser
```

The browser test uses an already-installed local Chromium/Edge through CDP with
Node built-ins, installs nothing and skips only if no supported local browser is
found. It creates and cleans its own temporary synthetic bank and browser profile.
It verifies real text selection, all three saves, safe rendering of HTML-like
notes, evidence navigation, edit/cancel, language/draft/source preservation,
connection return/location, reopening and narrow-screen overflow. Tests also
cover bank backup/restore, concurrency, idempotent retries and source/view changes.

## Owner scenario and original acceptance plan

The owner selected John 9, described as the story of the blind man, and asked for
its meaning, religious blindness, related blindness stories, Jesus as a character,
evidence for the particular story including fragments, historical context for the
Pharisees, and symbolism in and around the story. These are research questions
and requested navigation destinations. No biblical wording, interpretation,
manuscript identification or corroborating historical claim is supplied here.

The five initial preferences and three follow-up preferences are recorded in
[the product direction](READING_DESK_PRODUCT_DIRECTION.md). John 9 is a chapter
within the existing JHN scope; choosing this usability scenario does not admit
its text, expand the corpus or approve any interpretation.

## Confirmed experience

| Choice | Owner's answer |
| --- | --- |
| Home | Library and one prominent search, equally important. |
| Main device | Mostly desktop or laptop; retain an accessible narrow-screen layout. |
| Reading | Text and explanation side by side; evidence and connections expandable. |
| Explanation | A short clear account first, then attributed views and their evidence. |
| Language | Switchable English and Bosnian/Herzegovinian; exact source editions retain their own language. |
| Evidence | Both manuscript/textual witnesses and independent historical evidence, where available. |
| Personal actions in the first usable version | Private notes, highlights and suggested connections. |

The first usable version includes those personal actions. A read-only screen can
be an internal increment, but is not completion of this owner-selected milestone.
Full editing of shared explanations or curation of authoritative relationships
was not selected and is outside this small pilot.

## Opening the desk

The home screen presents the library and a prominent search together. Book cards
show actual reading availability, edition information and a route into context.
Searching for John 9 and browsing to John should reach the same reading state.
Search initially retrieves available records and curated metadata; it does not
promise an AI answer or semantic reasoning that has not been implemented.

On desktop/laptop the main screen has:

- A stable reading header identifying work, chapter/story location, edition and
  translator, with availability and an English/Bosnian-Herzegovinian control.
- The selected source text in one pane, with readable typography and selectable
  passage ranges. Missing or blocked text has an honest availability state.
- An explanation pane beside it, starting with a concise, attributed account.
  Further views, evidence and connections expand without replacing the source.
- Accessible actions to add a private note, highlight a selected span or suggest
  a connection. Personal material is visibly separate from sourced explanations.
- A reliable return path after following another passage, character or source,
  restoring the original reading location and the relevant open explanation.

These are functional requirements, not a fixed pixel layout or a chosen visual
theme. On narrow screens panes may stack or switch accessibly; the current
location and source/explanation distinction must remain understandable.

## Following the owner's questions

| Requested destination | Required reading behavior | Evidence boundary |
| --- | --- | --- |
| Meaning and religious blindness | Open the short explanation, then attributed theological/literary readings and their passage anchors. | Religious blindness is the owner's requested interpretive angle, not an interpretation approved by this plan. |
| Other blind people/stories | Open a list of specifically sourced passages and a reason each is related; compare and return. | A shared motif is not a claim that characters are the same person or stories describe the same event. |
| Jesus as a character | Follow reviewed mentions or clearly labelled identity proposals, with the role in this narrative distinguished from separate historical claims. | Do not infer identity, chronology or historical corroboration from a matching name. |
| Pharisees and historical context | Read attributed background, its date/context, and how a source relates to the selected passage. | Distinguish portrayal in the story from broader historical claims about a group or its members. |
| Symbolism in and around the story | Inspect the proposed symbol, exact passage anchor and commentator's explanation, including alternatives. | Distinguish what a source explicitly states from what an interpreter proposes. |
| Textual witnesses/fragments | See which exact words or passage range an identified witness preserves and open its catalogue/image/edition evidence when permitted. | A witness elsewhere in the book does not establish preservation of this story. |
| Independent historical evidence | See the exact event-level assertion being assessed, the candidate evidence and its relevance, limits or disagreement. | Evidence that a text circulated is not independent evidence that the narrated event occurred. |

The biblical scope remains GEN/MAT/MRK/LUK/JHN. References elsewhere
can remain bibliographic/context links within the existing research boundary;
they do not add another book or authorize its text. This planning task supplies
no named parallel passages, fragments or historical facts from model memory.

## Evidence categories that must remain separate

Both kinds requested by the owner are first-version destinations, even when a
category has no verified local records. The interface must explain absence,
partial coverage and uncertainty rather than fill them with plausible content.

**Textual transmission.** A record needs an exact witness identity and a source
for that identification; edition/catalogue or repository reference; stated dating
and its uncertainty/source; exact preserved passage coverage; and, where permitted,
the relevant image, transcription or scholarly edition locator. Distinguish
fragmentary wording from a full chapter and an inspected witness from a catalogue
lead. Transcriptions, translations and commentary remain separate contributions.

**Event-level historical evidence.** A record identifies the exact historical
assertion, the evidence offered, its date/provenance, relevance and limits, and
any dependency on other sources. Repetition of the same account is not counted
automatically as independent corroboration. A source's description and a later
researcher's assessment remain attributed and distinguishable.

**Historical background.** Contextual evidence about a place, period, institution
or group can illuminate a story without verifying its particular event. Keep it
accessible beside event-level evidence, with an explicit contextualizes label.

**Interpretation and reception.** Explanations, symbolism and religious readings
identify the interpreter, work/edition, anchor and stated view. Their inclusion
does not turn them into archaeological evidence or reviewed historical fact.

An evidence card should answer: What is this? Who identified or argued it? Which
exact part of John 9 does it address? What does it support, and what does it not
establish? Deeper identity/hash details can remain expandable.

No witness or historical corroboration is researched or asserted by this planning
slice. Planned empty states describe the collection, for example "No verified
textual witness attached to this passage yet" or "No independent event-level
evidence verified in this collection." Neither statement means none exists
anywhere. Do not combine all categories into a misleading count of proofs.

## Private notes, highlights and suggested connections

The owner must be able to perform all three actions from the reading experience,
without JSON editing, CLI commands or manual hash copying. The implementation
must define a small explicit reading-tools data contract before adding writes.
Existing v3 schemas do not already provide a complete highlight/reading-session
model; do not silently widen enums, overload an evidence claim or migrate banks.

Required behavior:

1. A note can attach to a book/story or a particular available passage. Preserve
   its author-entered language and distinguish it from the explanation being read.
2. A highlight binds the exact selected quote and Unicode span to the actual
   source/edition/revision or retained projection identity, not merely the label
   "John 9" or a mutable paragraph position.
3. A suggested connection names both destinations, the proposed relationship and
   the owner's reason. It is private and proposed; saving it does not merge people
   or create a scholarly approval or canonical relation.
4. Saved personal work survives closing/reopening and has recovery, integrity and
   backup coverage explicitly documented. Existing bank backup does not silently
   cover a new sidecar store or an external PDF.
5. Editing uses expected revisions or equivalent conflict protection. Cancel does
   not save. Failures and uncertain save outcomes are understandable and do not
   cause duplicate notes on retry.
6. A changed source keeps the earlier anchor; do not move a highlight to similar
   new wording automatically. Missing/blocked/stale sources retain honest status
   without exposing text that is no longer eligible for display.

Private actions use the existing Python storage/validation boundary. The current
Node viewer remains GET-only until a bounded reading-tools write surface is
implemented and tested; do not add arbitrary filesystem writes. Normal private
note actions should not require an editorial approval workflow. No fabricated
owner attestations or silent promotion of user notes are acceptable.

## Bilingual behavior

English and Bosnian/Herzegovinian are switchable interface/explanation languages.
Switching language preserves the current book, reading location, open evidence
and private notes. It does not translate or replace the selected source edition.
Missing explanation translations should be labelled, with an explicit available
language fallback; do not invent a translation during switching.

Keep language variants tied to their actual contribution/version and attribution.
Two translations of one explanation are not independent witnesses. Personal notes
keep their authored wording. Preserve the established literal forms svjet,
vrjeme, covik and razumit; the language choice does not authorize inferred
inflections, original-name mappings, transliteration or theological substitution.

## Delivery and acceptance

Implement as one small extension of the existing local application, in reviewable
increments, rather than a new platform:

1. Define the reading-view projection, explicit record/source bindings and private
   reading-tools contract/versioning. Identify exactly what existing bank,
   catalogue and historical APIs can supply and what is absent.
2. Deliver equal library/search entry and the desktop side-by-side reading state,
   with concise explanation, attributed expandable alternatives and a return path.
3. Add the requested connection/context destinations and separate evidence groups,
   including honest empty, unavailable, partial, stale and unreviewed states.
4. Add bounded private note/highlight/suggested-connection actions and persistence;
   specify recovery, conflicts and backup coverage using the same Python boundary.
5. Check bilingual switching, keyboard/narrow-screen behavior and source-location
   preservation across the complete journey, then observe the owner's use.

An internal read-only increment is useful, but cannot be labelled the completed
first usable version while the three selected personal actions are absent.
Preserve existing versioned schema contracts and source gates; define any new
reading-tools version explicitly rather than weakening existing contracts to
make a demonstration look complete.

Technical acceptance includes exact source/anchor validation, private-data
boundaries, write conflicts/cancel/recovery, preserved editions/credits and
unchanged existing bank/corpus behavior. Usability acceptance is the owner
completing the John 9-shaped journey, explaining why a connection is relevant,
distinguishing evidence categories, adding all three personal items, reopening
them and returning to the original reading location without a terminal.

No real source is currently cleared. Maintain two visible readiness states:
the interaction can be demonstrated on original synthetic fixtures, while an
actual John 9 study desk also needs an eligible exact edition, source-backed
explanations/connections and reviewed evidence records. Do not paraphrase John 9
into a synthetic fixture, invent fragments, or call a fictional demonstration
a populated John 9 research tool. Plan the necessary exact-edition and source
research separately; this documentation step acquires no content or rights.

Related: [product direction](READING_DESK_PRODUCT_DIRECTION.md),
[bank implementation plan](KNOWLEDGE_BANK_IMPLEMENTATION_PLAN.md),
[historical processing contract](HISTORICAL_TEXTS_PIPELINE.md),
[rights policy](RIGHTS_POLICY.md) and [next tasks](../NEXT_STEPS.md).
