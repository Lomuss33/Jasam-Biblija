## Icon integration — 2026-11-24

The project icon is available for T3 and the local viewer. The next small icon
task is owner visual review at sidebar size; existing research/editorial
priorities below remain unchanged.

# Current product priority — reading and research usability, 2026-11-19

## Changed-view and removed-passage draft recovery — 2026-11-20

The documented next writing slice is implemented. A changed view or removed
passage now opens a reachable recovery panel, preserving original writing,
quote, binding and credits captured at draft creation. Legacy drafts label
missing edition details rather than infer them from the current view. Recovery
is available on the home screen when the old passage no longer opens.

The user may download a private browser-draft snapshot or explicitly prepare a
new unanchored passage note. Preparation copies private wording only, retains
the original and asks for a current destination. Changed prepared views need an
explicit refresh of that new note's destination. Cancel/discard distinguish the
prepared copy from the original; unknown saves block either destructive step.
An auth/busy failure cannot unlock a previously unknown save. No API/schema or
source admission boundary was broadened.

17 web checks and the full local-browser journey passed, including two real view
revisions, original-save resolution, lost recovery response, a denied retry,
exact nonduplicating recovery, removed-passage reachability and narrow layout.
The first-use guide contains the complete recovery procedure. Browser drafts and
their JSON snapshots remain separate from committed bank backups.

**Next small task:** complete the bounded John 9 exact-edition/source-readiness
research plan from existing source evidence. Identify the precise metadata,
passage-locator and attribution gaps before proposing any content work. Preserve
current acquisition/rights/review gates, do not fill historical text or scholarly
claims from memory, and do not restart the completed writing/recovery work.
The owner can continue trying the updated writing flow alongside that work;
real John 9 text and its evidence dossier remain unpopulated.

## Highlight comments and conflicting-edit recovery — 2026-11-20

Continued the owner's selected notes/highlights priority. Saved highlight marks
now open their comments beside the source with click or Tab/Enter/Space. Shared
marked words expose all overlapping current highlights; earlier-view items and
temporary evidence markers do not masquerade as saved private highlights.
Selecting text for copying or another highlight does not open the viewer.

Ctrl+Enter saves from the editor, while Enter adds a line. Confirmed saves show
the private item beside the source. Reading/closing saved comments preserves an
open draft. Conflicting edits show the latest saved wording and kept draft;
**Save my draft as a separate item** explicitly preserves both as different
private items. It is unavailable for an uncertain save or a changed reading view,
and never overwrites/rebinds the newer item. Unknown save outcomes still require
exact retry before editing or cancelling.

All 14 web checks and the expanded local-browser journey passed, including an
actual concurrent edit, conflict refresh and separate-item save. The first-use
guide and English/Bosnian help describe these controls. No Python/schema/source
policy changes or real John 9 content were made.

**Next small coding task:** improve the visible recovery path for a draft whose
reading view changed, preserving the original quote and private wording without
automatically moving its anchor. Current saves fail closed and keep the draft;
an explicit recovery choice is still absent. Keep this bounded to the private
writing flow. Real John 9 exact-source/content research remains a separate
pending track; the fictional interaction example is not its completed dossier.

## Writing notes/highlights and finding saved work — 2026-11-20

The owner gave tentative positive feedback on the trial, then explicitly chose
**Writing notes and highlights** as the part needing more work. The current
increment moves the editor beside the source on desktop, clarifies whole-passage
notes versus exact-selection highlight comments, keeps unfinished drafts through
same-tab refresh when browser storage is available and preserves exact retry for
unconfirmed saves. Cancel discards the draft without changing an existing item.

Home search now includes personal wording and highlighted quotes under **My saved
reading work / Moji spremljeni zapisi**, with kind filters, recent-first results,
open-item/source-locator actions and access to older items. A count/link beside
the passage title jumps to its saved notes. Earlier-view anchors remain labelled
and cannot be applied to the current source by a coincidental text match.

All 13 web/API/state checks and the expanded real-browser journey passed. The
first-session guide now reflects the editor position and draft recovery. Browser
drafts stay separate from committed bank items/backups; closing a tab is not a
promised recovery path. Real John 9 text and scholarship remain unpopulated.

**Next small task:** try writing one passage note and one commented highlight in
the new editor, then fix the first specific remaining writing friction. The
owner's tentative impression is not full study-journey acceptance. The bounded
John 9 exact-source/content-readiness research plan remains separate pending
work; do not restart source policy or claim a fictional example is real content.

## First-use guide ready — 2026-11-20

The owner explicitly said they have not tried the prototype and requested a
clear guide. Added `docs/READING_DESK_FIRST_SESSION.md`, a Windows double-click
`start-reading-demo.cmd` launcher and **How to use this desk / Kako koristiti
stol** in the reading header. The bilingual walkthrough opens the practice story
and covers evidence, connection return, all three private tools, language/reopen,
the planned John 9 state and stopping/restarting without resetting saved items.

Windows startup from another working directory and the full local-browser
journey, including help during an unsaved draft, passed. No owner usability
session has occurred yet. The next small task is to follow this guide and record
the first observed unclear step, then make that concrete fix. Do not restart the
same discovery questions or treat a guide/test as owner acceptance. The separate
John 9 exact-source/content research plan remains pending; no acquisition or
content assertions were made in this guide increment.

## Implemented interaction prototype — 2026-11-20

The next slice described below has now been implemented on original synthetic
data. Run `npm run reading:demo -- --synthetic` and open the local reading desk.
It has library/search, side-by-side bilingual reading/explanation, distinct
evidence categories, meaningful fixture connections, exact-source locator
navigation and saved/edited private notes, highlights and proposed connections.
John 9 remains a planned topic with a book-level note and unavailable text; no
real verses, manuscript records, historical corroboration or exegesis were invented.

Reading-view and reading-item v1 documents live inside private v3 bank articles,
using existing locks/history/backup without changing v3 record enums. One bounded
opt-in write endpoint calls Python; other routes remain read-only. Notes have
exact anchors, expected revisions and retry IDs; language changes preserve source
wording and private drafts. Start/run/backup instructions and limits are in
`docs/JOHN_9_READING_DESK_PILOT.md`.

**Next small task:** have the owner use the synthetic journey and record the first
concrete navigation/label/save friction, then fix that observed issue. The real
John 9 content-readiness track also needs a bounded exact-edition/source research
plan using existing source evidence, without changing clearance or filling text
from memory. Do not claim a populated real study desk or an owner usability pass
from automated tests. Do not restart the implemented reading contract or the
same eight preference questions. The bank's small-history limits remain visible.

The 2026-11-19 implementation instructions below are retained as the milestone
definition; their initial coding task is completed by this prototype, not an
instruction to recreate it. Real-content and owner-use acceptance remain open.

The owner wants one clear place to read books and explore context, explanations,
evidence, characters and connections to other stories/supporting literature.
Read `docs/READING_DESK_PRODUCT_DIRECTION.md` first. It records the actual user
direction, distinguishes proposals from confirmed preferences and replaces
infrastructure-first delivery ordering. This changes experience priorities, not
the five-book edition, rights gates or review authority.

**Discovery answers are recorded, not pending.** The owner selected equal library
and prominent search entry; desktop/laptop first; text and explanation side by
side with expandable evidence/connections; a short clear account followed by
attributed views; switchable English/Bosnian-Herzegovinian; and private notes,
highlights and suggested connections in the first usable version. The evidence
focus is both textual witnesses/fragments and independent historical evidence,
where available. Do not ask these eight preferences again.

**Selected scenario:** John 9, the owner's blind-man story example, with meaning/
religious blindness, related blindness stories, Jesus as a character, Pharisees
in historical context, symbolism and exact-story evidence. Read
`docs/JOHN_9_READING_DESK_PILOT.md` for the concrete journey and acceptance checks.
This is a product scenario within JHN, not a source/text/interpretation approval.

**Next small implementation task:** define and implement the minimum versioned
reading-view/private-tools contract on original synthetic fixtures, explicitly
mapping current catalogue/bank/historical identities and source anchors. Then
connect it to the first side-by-side reading slice in the existing application.
Support book/passage → explanation → exact source → meaningful connection → back
to the same reading location, plus save/reopen of a private note, highlight and
suggested connection. Use the existing Python writer boundary, conflict/recovery
checks and explicit backup coverage. Do not silently widen v3 schemas or add a
generic Node filesystem writer. Stage reading and writing in small reviewable
increments, but do not call a read-only increment the completed first version.

Keep manuscript transmission, event-level corroboration, background context and
interpretation distinguishable. Missing evidence means not verified in this
collection, not that no evidence exists anywhere. Bilingual switching must not
rewrite source editions or personal note wording. Use an honest synthetic
interaction prototype until real-source eligibility is established; separately
plan the exact John 9 edition/source research needed for a populated study desk.
Do not fabricate a John 9 paraphrase, parallels, manuscripts or historical claims.

Success is completing the owner's selected reading scenario clearly, with source
attribution and understandable connection reasons, without terminal/JSON/hash
copying during the reading task. Tests remain necessary but are not a substitute
for that observed usability check. Include persistence of all three private tools
and language-switch/location preservation. Full acceptance checks are in the
brief and John 9 pilot. This remains a bounded usability slice, not a new platform.

The candidate-context CLI task below is supporting backlog, no longer the
automatic next milestone. No real content acquisition, scope expansion or source
clearance is authorized by this product discussion.

# Earlier technical continuation — 2026-11-19

Current usefulness assessment: `docs/PROJECT_USEFULNESS_REPORT_2026-11-19.md`.
It distinguishes usable catalogue/personal-bank workflows from synthetic
processing demonstrations and recommends a small practical private research
pilot. Its former next coding slice below is now deferred behind the reading
journey priority above; the assessment itself remains a dated record.

The incremental historical pipeline and nonempty synthetic CLI/API check are
implemented. See `docs/HISTORICAL_TEXTS_PIPELINE.md` for a reproducible local
demo, `pipeline init/step/status`, retries/refreshes and read-only dossier queries.
Checkpoints, extraction caches and immutable snapshots preserve prior results;
source/projection hashes, exact Unicode locators, editions and credits stay
separate from identity/review decisions. Real-source extraction now explicitly
stops at `source_review_required` before reading bytes; prior research counts
below are historical results, not cleared or current corpus coverage.

The resumed slice also pins query/status to one snapshot, fixes combined-work
pagination and same-artifact filters, rejects malformed HEAD/pending coverage,
and returns an explicit error instead of silently dropping oversized response
rows. Viewer remains opt-in, loopback and GET-only.

Completed this slice: new synthetic PDF tasks retain exact projection bytes
through `historical-extraction-v2`, hash/size/UTF-8/span validation and a 128 MiB
unique-projection budget per snapshot. `historical projection-verify` checks an
old or current cache without the PDF/tool. V1 caches and snapshots are unchanged
and remain explicitly not-retained. An original PDF fixture exercises the real
local adapter when available; failures, changed tools/inputs and old cache
preservation have offline coverage. No real source was acquired or admitted.

**Deferred supporting task:** add bounded read-only CLI inspection of one candidate from
a retained synthetic projection, selected by exact cache hash and candidate ID.
Show a small literal context with the existing Unicode offsets and explicit
synthetic/proposal labels. Do not add a raw-text HTTP route, auto-classification,
source admission or decisions. This CLI-only proposal is not the definition of
the new user-facing reading milestone.

Current limits: capitalized-token candidates are unknown proposals; HTML/OCR
and human identity review are absent; real-source admission is unimplemented;
only new managed PDF extractions retain projections; original PDFs and legacy
projections are not archived; no snapshot pruning, full pipeline backup/restore
or bank promotion is provided. No owner approval is fabricated.
Earlier next-task statements below are history, not instructions to repeat them.

# Knowledge-bank implementation plan — 2026-11-16

New product direction: the project is a historical-texts knowledge graph, not
only a Bible viewer or claim store. The first registry contract now separates
work, edition, artifact and proposed relation; see
`docs/HISTORICAL_TEXTS_PIPELINE.md` and the four `historical-*-v1` schemas.
Next small coding task: add a read-only registry builder over the existing
personal-library catalog, keeping metadata-only findings separate from acquired
text and keeping relation matches as proposals.

Completed this slice: `jeb historical registry-build` now creates that
metadata-only registry from the current library catalog: 291 works,153 editions,
153 artifacts and153 version-of proposals. No text is downloaded and no rights
or corpus status is changed.

Next small coding task: define a read-only entity extraction/index contract for
available text artifacts, with character/place matches remaining proposals until
their exact source locators are available.

Completed this slice: `jeb historical entity-index` now emits exact-offset
unknown entity candidates for supported local UTF-8 text and explicit pending
statuses for unavailable/unsupported artifacts. It produced zero candidates and
153 pending artifacts on the current catalog, without inventing content.

Next small coding task: add bounded adapters for one permitted text format at a
time (starting with an inspectable plain text or HTML artifact), preserving
source offsets and keeping extracted person/place labels as proposals.

Completed this slice: the entity index now supports a bounded temporary PDF
projection through local `pdftotext`, preserving projection-labelled offsets and
keeping all matches unknown/proposed. The current catalog yielded 18,230
candidate spans from 4 local PDFs and 149 pending artifacts.

Next small coding task: add deterministic candidate normalization and review
grouping without silently merging same-named people, places or literary
characters.

Completed this slice: deterministic conservative entity grouping now creates
3,594 `proposed_same_surface` groups from the current 18,230 candidates. It
preserves diacritics and does not grant merge authority. A separate bounded
64 MiB reader handles the large index safely.

Next small coding task: add a reviewable dossier layer that can show candidate
groups beside exact artifact locators, before any person/place/character merge.

Completed this slice: entity dossiers now show each proposed group beside its
works, editions, artifacts and exact projection-labelled locators. They remain
proposals and contain no automatic identity merge.

Next small coding task: expose dossier summaries to the local read-only viewer
and add explicit filters for candidate status, artifact availability and source
work, without adding approval or merge actions.

Completed this slice: the viewer now reads an explicitly configured dossier
file through `JEB_HISTORICAL_DOSSIERS`, with bounded search/filter results and
read-only detail locators. It remains disabled by default and does not expose
approval or merge actions.

Next small coding task: add a read-only pipeline status summary showing counts
for registry artifacts, pending artifacts, candidates, groups and dossiers;
keep it opt-in and do not add scheduling or automatic identity decisions.

Completed this slice: `/api/historical/status` and the viewer now derive those
counts from explicitly configured local JSON files. Missing or unreadable
phases are reported without stopping unrelated data or writing anything.

Next small coding task: add a bounded work-level dossier lookup so an input
like `MAT` or a reviewed topic can list related candidates across editions;
keep identity matching proposal-only and do not add automatic aliases.

Completed this slice: `/api/historical/lookup` groups matching dossier
proposals by work and returns bounded dossier IDs with candidate/locator counts.
It remains read-only and makes no identity decision.

Next small coding task: add a machine-readable relation-proposal lookup with
the same source/status boundaries; keep `similar_to`, `parallel_to` and
`same_as_candidate` explicitly non-authoritative.

Completed this slice: `/api/historical/relations` filters registry relations
and returns bounded, explicitly non-authoritative summaries with endpoint
labels and evidence counts.

Next small coding task: add a single machine-readable `build_dossier` response
that combines work lookup, matching entity dossiers and relation proposals,
while preserving every proposal status and source boundary.

Completed this slice: `/api/historical/build-dossier` combines entity and
work-scoped relation layers, retains their proposal statuses, and reports
unavailable layers without inventing data.

Next small coding task: add contract tests for downstream consumers around
missing layers, bounded limits and stale registry/index/dossier hashes; keep
the response read-only and reject silent cross-layer substitution.

Completed this slice: added canonical hash-binding checks and a fail-closed
stale-input contract test for the fully configured pipeline. Missing optional
layers remain explicitly reported rather than silently substituted.

Next small coding task: add bounded-limit contract tests and a machine-readable
error envelope for malformed configured JSON, preserving read-only behavior.

Completed this slice: bounded-limit tests now cover lookup and relation APIs;
malformed configured JSON returns a stable 422 `invalid_historical_input`
envelope naming only the affected logical layer.

Next small coding task: add a read-only CLI inspection command that prints the
same pipeline counts and blockers without starting a server or writing output.

Completed this slice: `jeb historical status` prints read-only counts and
blockers, with four explicit unconfigured-layer blockers when no paths are
provided. The command writes no output files.

Next small coding task: add a CLI/API parity fixture so the same synthetic
pipeline produces equivalent counts and blocker categories in both interfaces.

Completed this slice: CLI and viewer API now share the same status fields and
blocker categories for unconfigured and malformed layers. Their read-only
tests cover the equivalent contract.

Next small coding task: add one end-to-end synthetic fixture with all four
layers and matching hashes, then compare ready-state counts through both
interfaces without touching real source files.

Completed this slice: a temporary four-layer fixture with valid hash bindings
now runs through both CLI and API and asserts identical ready-state counts and
blockers. It is deleted after the test.

Next small coding task: expose the parity fixture as a documented local check
command, without making it a release gate or allowing real-source writes.

Current topic draft: `docs/TOPIC_MEDITATIONS_MARKO_AURELIJE.md`. Next small
task: verify the five candidate URLs and exact edition/licence details by
jurisdiction. Only then may a human-reviewed source record be created; do not
create claims or copy translation text yet.

The initial review is documented in
`docs/RESEARCH_REVIEW_MEDITATIONS_2026-11-18.md`. The next small task is to
resolve the legal blocker for each exact artifact: retain the link in all cases,
then download/hash/store the artifact whenever permitted; use link-only only
when the documented legal/evidentiary blocker requires it.

The working rights scope is now `DE` only for the private GitHub repository.
The Meditations candidate batch has been re-imported with that exact scope; the
next task remains the DE artifact rights decision for Gutenberg 15877.

The current matrix is `docs/RIGHTS_MATRIX_MEDITATIONS.md`; next small task is
human review of one exact artifact row, starting with Gutenberg 15877.

Completed this slice: added the untrusted source-candidate inbox. Use
`jeb sources candidates validate/import` for metadata exported from a search or
browser. It is deliberately not a crawler, does not download pages, and does
not assert legality; rights state stays explicit until human/source assessment.

Next small task: define one owner-supplied candidate batch for the first exact
edition, then manually review its URLs and jurisdiction-specific rights before
creating any source registry record. Do not add Bible books outside GEN/MAT/
MRK/LUK/JHN.

Completed this slice: added read-only `bank search`, returning exact current
record/revision IDs and matching fields across title, metadata and body.

Next small task: connect search results to exact record opening in the local
viewer, without adding writes or exports.

Latest completed bank slice: opt-in managed3.0 now stores `claim` and `evidence`
records against exact committed historical revisions, validates text-span
locators, exposes historical references and evidence links, and supports private
backup/restore. Existing managed2.0 schemas and backup fingerprints remain
unchanged; initialization still defaults to2.0. See
`docs/BANK_PERSISTENT_EVIDENCE.md`. The persisted examples are original,
synthetic technical fixtures, unreviewed and unreleasable.

Completed this slice: documented the dry-run-only v2→v3 copy/migration contract
in `docs/BANK_MIGRATION.md`. It requires a full v2 chain validation, explicit
record/revision identity rows, source HEAD/hash binding, deterministic blockers,
no writes and no F3A packet guessing. No migration command exists yet.

Completed this slice: read-only `bank migrate-plan` now emits that report
outside the bank, with no-clobber behavior and explicit v2-only input. Tests
cover unchanged HEAD bytes, external output and v3 rejection.

Completed this slice: `bank migrate-plan-verify` now rejects a saved plan when
the source workspace, HEAD manifest or current-record digest changed. Tests
cover stale HEAD rejection and a synthetic blocked-record policy. Do not create
the v3 target until a separate owner decision.

Completed this slice: documented the reviewed-writer design in
`docs/BANK_MIGRATION.md`: external human decision binding, revalidation under
lock, sibling staging, private target validation and no-clobber publication.
No decision artifact or writer was fabricated.

Completed this slice: added `bank migrate-decision-validate` and strict
`bank-migration-decision-v1` schema. It only checks an external decision against
the current plan and v2 HEAD; it never creates approval state or a target.

Completed this slice: added an explicit `--synthetic` migration simulation that
copies a temporary v2 fixture into a marked, unreleasable v3 target and validates
the complete copied history. It is not available as a real migration path.

Next small task: review the decision-record fields and synthetic simulation
output. Do not implement real target creation until an explicit owner decision
authorizes it.

Latest hardening: simulation revalidates and copies under the source writer lock,
publishes with no-clobber rename and cleans only owned staging after failure.

Completed this slice: the local read-only viewer now has an opt-in **Baza znanja**
page and `/api/bank` record endpoints when `JEB_BANK_ROOT` is explicitly set.
The default viewer remains bank-disabled.

Completed this slice: the read-only bank detail view now displays typed claim
subjects and evidence links, relation labels, exact referenced revisions and
current-versus-historical status. Evidence details show their claim, source and
locator. No write, approval, export or public serving path was added.

Next small task: consider a bounded read-only revision/history view; keep older
revisions accessible through the existing Python history/reference commands if
the viewer cannot preserve the same exact-byte and privacy guarantees.

Completed this slice: the viewer now shows a bounded revision summary for the
current v3 record, following snapshot parent links with a 128-snapshot cap and
without serving historical body bytes. Full exact historical inspection remains
in the Python history/reference commands. No write or approval operation was
added.

Next small task: stop expanding the viewer unless a concrete read-only need is
identified; preserve the current private, opt-in and GET-only boundary.

Completed this slice: viewer search now queries current bank metadata/body and
opens exact matching records through the bounded detail endpoint.

Next small task: use the viewer with a real local bank fixture and stop adding UI
until a concrete usability issue appears.

Completed this slice: a temporary Python-created bank was served through the
Node viewer and search returned the exact record. The fixture was removed after
the smoke test.

Next small task: stop adding interface until a concrete usability issue appears.

Completed this slice: added `docs/BANK_QUICKSTART.md` with the shortest safe
workflow for init, create, search, validate, viewer and private backup.

Verified this slice: the quickstart ran end-to-end in a temporary managed3.0
fixture, including valid backup verification.

Next small task: use the quickstart with the owner's first real private topic;
do not add more architecture until that workflow exposes a concrete problem.

New topic direction: Catholic Bible books and main characters. Start with the
five currently allowed pilot books in `docs/BANK_CATHOLIC_BIBLE_PILOT.md`;
other canon books remain pending a separate owner scope decision.

Completed this slice: typed claim/evidence relationships in the detail view are
now safe local navigation links to the related bounded record view. No arbitrary
paths, writes, approvals or export were added.

Next small task: preserve the viewer boundary; do not add a broader frontend or
export workflow without a separately defined requirement.

Completed this slice: the read-only bank page can filter current records by
entity, source, article, claim or evidence. It uses the existing bounded search
route and adds no write or approval behavior.

Next small task: preserve the current scope; stop viewer expansion until a
specific workflow requirement is defined.

# Historical knowledge-bank plan — 2026-11-15

Latest completed bank slice: F3A evidence prepare/validate/inspect now supports
external unreviewed claim/evidence packets bound to exact managed2.0 HEAD and
record/body hashes. Literal text spans are locally checked; page/section/time
locators remain declared_only. See BANK_EVIDENCE.md. These drafts are outside
canonical storage and bank backups; existing2.0/backup schemas remain unchanged.
Next small coding task: F3B explicit new-format schemas and reader semantics for
persisted claim/evidence with exact historical revision references, on original
temporary fixtures. Then add writer/import support in that version. Do not widen
v2 enums, migrate existing banks while reading, forge review state or silently
rebind old packets to new claims/sources. Preserve2.0 backup compatibility and
current library work. Earlier next-task statements below remain historical.

Latest bank step: private committed-chain backup/backup-verify/restore is
implemented for managed2.0; see docs/BANK_BACKUPS.md. Exact bytes/history survive
restore to a new directory. Staging, locks, inactive snapshots and library/private
are excluded. No public export or encryption is implied. Existing outputs and
destinations are never replaced; schema identities and full history are checked.
Next small coding task: F3 claim/evidence modelling contract and minimal schemas
for exact-revision claim support and typed locators, using original temporary
data. Explicitly design the bank-format version transition before admitting new
record kinds; preserve2.0 schemas/backups and do not silently migrate. Defer UI,
mass imports and AI integrations. Earlier next-task statements below are history.

Latest completed bank slice: F2 managed format2.0 now supports
`jeb bank init/create/edit/history/diff/recover`, plus existing validate/show.
Full immutable snapshots, hash-bound history, OS single-writer lock and required
expected-revision protect cooperative local writes. Format1.0 stays read-only;
no silent migration. See BANK_FORMAT.md/BANK_WORKFLOW.md for recovery details.
Next small bank task: bounded backup/restore of the committed2.0 chain into a
new directory, with integrity verification and offline round-trip tests. Exclude
staging/lock files; no overwrite or implicit publication. Do this before storing
valuable personal data, then continue F3 claim/evidence/assessment modelling.
Current limits:128 full snapshots/128MiB history; no scalable index, bank UI,
evidence assessments, migration, backup or export yet. Preserve library research.

Earlier F0/F1 next-task statements below are historical; F2 is now complete.

Bank F0/minimal F1 is implemented: docs/BANK_FORMAT.md and BANK_WORKFLOW.md,
two packaged schemas and `jeb bank validate/show --bank-root ...`. Initial
entity/source/article snapshots validate identities, typed links, bounded UTF-8
and exact Markdown hashes, independently of Project/corpus configuration.
This is read-only, initial parent_revision=null only; no history/writer/UI exists.
Next small coding task: design and implement F2's versioned revision envelope,
single-writer lock, expected-base conflict checks and staged commit/recovery
protocol on original temporary data. Test interrupted multi-file writes before
introducing create/edit commands. Do not relax the initial schema silently or
claim review/rights clearance. Preserve ongoing library research below.

Latest request: detailed coding plan for a broad personal knowledge bank. See
docs/KNOWLEDGE_BANK_IMPLEMENTATION_PLAN.md (F0–F14). This is a staged proposal,
not completed functionality or extension of biblical scope. Next small coding
task: F0/minimal F1, specify record envelope, identities, visibility and revision/
recovery semantics; then entity/source/article schemas and read-only validation
on original temporary fixtures. Keep one Python package/CLI, separate bank
namespace and existing corpus/review/private boundaries. No large frontend,
model API, historical example or publication in that slice. Library/source
research below remains preserved as a separate workstream.

# Personal-library research — 2026-11-15

Batch16 reviewed20 targets146–165, added16 findings for15 new works, enriched
existing038/039 without duplicates. Totals153 findings/138 works,5 private files.
See library/research/batch-16-review.md. Unresolved146,153,154. Preserve al-Maarri
selection, Plotinus volume6-only evidence, distinct Fihi editions and Anandina
mediation/coverage questions. Next larger batch166–185: remaining Sufi works,
Christian mysticism and early ancient texts. Bank F0/F1 task remains separate.

Batch15 reviewed20 targets126–145; added17 findings for16 works (15 newly
represented). Totals137 findings/123 works, five private files unchanged.
See library/research/batch-15-review.md. Unresolved130,132,144,145; preserve
Epikur's German-mediator evidence, Seneca volume1 limitation, Musonius selection
and exact edition discrepancies. Next larger batch146–165: remaining Greek/
Roman works and early Persian/Sufi/Arabic works. Separate bank F0/F1 task stays.

Batch14 reviewed20 targets106–125, added15 findings for15 works: now120
findings for108 works, five private files unchanged. See
library/research/batch-14-review.md. Five targets unresolved: Ora ga haru,
Ryokan collection, Bankei talks, Yasen kanna, Dokkodo. Preserve Takuan credit
and Musashi ISBN/page discrepancies. Next larger batch:126–145 (Aristotle,
Epicurus, Lucretius, Stoics, early Plutarch); compare exact editions and coverage.
The separate knowledge-bank F0/minimal F1 task above remains preserved.

Batch13 reviewed20 targets (086–105), added9 findings for8 works:
105 findings for93 works, five private files unchanged. See
library/research/batch-13-review.md for all20 outcomes, exact editions and
unresolved coverage/language/script. Next larger batch:106–125, remaining
Japanese works and early Greek philosophy; verify credits and complete work
versus anthology. Existing knowledge-bank F0/minimal F1 task above is preserved.

Batch12:96 findings for85 works,five private files. Huangbo2004/1986 exact
bibliographic records; Xinxin Ming Osho commentary only. Platform/Linji
unresolved. See batch-12-review.md. Next small batch: Wumenguan,Dao de jing,
Zhuangzi,Liezi. Verify translators, mediation and whole work versus selection.

Batch11:93 findings for83 works,five private files. Bodhicaryavatara2020
catalogue/PDF403; Heart Sutra indexed translator/live challenge; Diamond Sutra
unnamed non-specialist translation, source chain retained. Vimalakirti unresolved.
See batch-11-review.md. Next small batch: Platform Sutra,Xinxin Ming,Huangbo,
Linji records. Earlier unresolved language/coverage tasks remain open.

Batch10:90 findings for80 works, still five private files. Milindapanha corrected
to abridgement; Ratnavali PDF ends400, first MMK chapter bibliographic record
only, Suhrllekha unresolved. See library/research/batch-10-review.md.
Next: Bodhicaryavatara, Heart Sutra, Diamond Sutra, Vimalakirti-sutra;
distinguish root texts from commentary and complete books from excerpts.

Batch09:88 findings for78 works, five private files. Shared Udana/Itivuttaka2022
retained once under Itivuttaka, distinct from Udana2019. Theragatha/Therigatha
web sources explicitly selections; existing records corrected to excerpts.
See library/research/batch-09-review.md. Next: Milindapanha,
Mulamadhyamakakarika, Suhrllekha and Ratnavali; verify translators and coverage.

Batch08:87 findings for78 works, four unchanged private files. Suttanipata2022
and Udana2019 PDFs retained, visual translator/distribution checks and hashes
recorded. Pancatantra1980/1999 Matisic editions distinct; Hitopadesa unresolved.
See library/research/batch-08-review.md. Next: Itivuttaka,Theragatha,Therigatha;
check shared-file identity, individual translator credits and complete coverage.

Batch07 reviewed16 targeted queries for Basava, Akka Mahadevi and the two
Jain sutras. No regional edition confirmed; no new findings/downloads. Totals
remain83 findings for77 works, two private copies. See batch-07-review.md.
Keep these four unresolved; English/Czech texts and unrelated authors do not
satisfy language preferences. Next small batch: Pancatantra, Hitopadesa,
Suttanipata, Udana; distinguish abridgements and children's adaptations.

Batch06:83 findings for77 works; two unchanged private copies. Three findings
share one Satakatrajam2004 national CIP, individual coverage/script unverified;
Bijak finding is an introduction excerpt with unknown Croatian translator.
See library/research/batch-06-review.md. Do not treat Kabirove pjesme as Bijak.
Next small batch: Basava Vacane, Akka Mahadevi Vacane, Uttaradhyayana-sutra,
Acaranga-sutra. All earlier unresolved full texts/language checks remain open.

Batch05:79 findings for73 works; still two private copies. See
library/research/batch-05-review.md. Mandukya bibliography only, Yoga Vasistha
indexed imprint with completeness unconfirmed, Vijnana retailer pagination
conflict205/191, Tirukkural short unattributed-translation excerpt only.
Next small batch: Bhartrhari's Nitisataka, Vairagyasataka, Sringarasataka and
Kabir's Bijak. Distinguish requested collections from poetry selections.
All earlier unresolved leads remain open; earlier next-step entries are history.

Batch 04: 75 findings for69 requested works, still two private copies. See
library/research/batch-04-review.md. Separate translator credits on Atmabodha
and Vivekacudamani; Avadhuta blog confirms seven chapters only; Croatian
Astavakra1997 listing lacks translator/imprint. No best-edition selection.
Next small batch: Mandukya-karika, Vijnana-bhairava-tantra, Yoga Vasistha,
Tirukkural. Previous next-step statements below are historical.

Batch 03 completed: 70 findings for 65 of 291 requested works; two unchanged
private copies (Dhammapada HTML and Antic's modernized Samkhya collection PDF).
See library/research/batch-03-review.md. Babun's Upanishad preview is metadata
and contents only; three requested works are selections. Printed Mandaka is
not confirmed as Mundaka. Kotarac download failed TLS/404; no local copy.
Next small batch: Astavakra-gita, Avadhuta-gita, Atmabodha, Vivekacudamani;
verify translators, language and exact coverage before acquisition. Full Avot
and Himna biseru remain unresolved. Earlier entries below are historical.

Latest continuation: batch 02 added 16 observations, total 56 findings for 52
requested works. See library/research/batch-02-review.md. Pirkei Avot is only a
visually checked opening excerpt in an institutional anthology; eight gnostic
items are contents-only with unresolved edition identity. These have distinct
UI statuses. No new full requested work was acquired. One privately cached
institutional anthology is evidence only, not corpus or a complete Avot copy.
Next small content batch: verify Upanishad collection contents and Yoga-sutra /
Samkhya-karika editions. Preserve unresolved Himna biseru and complete Pirkei
Avot tasks; do not repeat the same blocked/index-only routes without new leads.

Owner supplied 291 requested works in 14 groups for a separate personal research
library. All are inventoried in library/requested-books.md and catalog.json;
291 initial discovery queries are logged, not all editions verified. Current
findings: 40 page/catalogue observations for 39 works; one private Dhammapada HTML
copy with translator, distribution notice, size and checksum. See library/README.md.
The web viewer opens on the library with filters and provenance. No collection,
source lock, schema or human approval changed; synthetic data remains separate.

Next small library task: inspect Pirkei Avot and remaining gnostic leads, verify
collection contents and systematically check higher language priorities before
choosing editions. Keep whole works, selections and commentaries distinct. No
absence/best-translation claim follows from the broad first pass. Continue the
remaining catalogue review rather than re-searching all 291 from scratch.

# Local visual workspace — 2026-11-14

The explicitly requested small read-only HTML/CSS/JS viewer now runs via
`npm run dev` at http://127.0.0.1:5187. No npm dependencies or publication.
See README for limits. Next small UI task: manually check desktop/mobile layout,
document search, keyboard dialog closure and section navigation in a browser;
the host preview tool was unavailable during implementation. Keep this viewer
bounded and read-only. Source/language research below remains the content priority.

# Current content step — 2026-10-31

Read docs/sources/LANGUAGE_ENTRY_BATCH_2026-10-31.md. Actual Škarić 1858 PDF title
and GEN pp.1–3 are now image-inspected; four HJP entries are inspected with their
limits. Next: inspect slog 9 title/MAT 5:1–12 and slog 10 title/JHN 1:1–5; keep
witness differences separate. Locate independent Bosnian/regional entries when
publicly available. Katančić 1831 scan remains unlocated, and 2016 revision is not
a substitute. Prepare coherent content batches, no paragraph-level questions,
no inferred replacements or source clearance. Existing code work is preserved.

# Language research completed — 2026-10-31

Read docs/HERZEGOVINIAN_LANGUAGE_GUIDE.md first. It records eleven targeted
language/translation references, access depth and five page-located lexical
examples; it does not claim eleven books were read. Next small content step:
inspect exact dictionary pages for frequent pilot vocabulary and hljeb/kruh,
and locate inspectable exact Škarić/Katančić volumes. Continue independent public
research without asking the owner to collect documentation. Prepare one coherent
batch with evidence and a short exception list, not paragraph-by-paragraph
questions. No replacement rule, new approval or source admission was created.

# Owner language direction — 2026-10-31

See decision 0014: local Herzegovinian voice with broad Bosnian/Herzegovinian
comprehensibility. Preserve the four literal forms. Next small content task:
research a compact regional-language/translation bibliography from multiple
independent sources, then prepare a reusable vocabulary/style proposal with
attested examples and uncertainties. Prepare coherent batches; do not ask for
paragraph-by-paragraph choices or infer approvals. Keep supporting evidence
books separate from the fixed GEN/MAT/MRK/LUK/JHN output scope. Do not prioritize
more review infrastructure over source/language work. This policy text change
intentionally makes earlier policy-bound packets stale; never reseal them as
human approval. Historical source clearance remains unresolved.

# Current continuation — 2026-10-31

Narrative decision schema and validation-only command are implemented. No receipt, promotion or real reviewer answers exist. Next small coding task: independently exercise the CLI against stale decision context before separately designing immutable typed-graph receipts. Do not implement promotion implicitly.

Read docs/sources/SOURCE_COMPARISON_2026-10-31.md before earlier source notes below. Actual eBible and CrossWire packages were acquired as private evidence. eBible includes a separately credited 1996 introduction and declares modernization/Ekavianization. Direct transcription of the image-identified Latin 1868 Pest scan is preferred. Private GEN 1:1–5 review pilot: data/private-source-audit/GEN-1-1-5-review.md. Next source task: exact five-book scan-leaf collation and edition usage assessment. Provider drafts/routes are documented and unsent. Source assessments/production lock remain unchanged; no source is cleared. Retain previous wheels/archives; this engine has no new wheel verification.

Earlier history follows.

# Next small task

Read PROGRESS, AGENTS and Git status first. The foundation and synthetic demo
already work. Do not restart them, expand the collection, invent real passages
or mark the project complete.

Optional AI review assistance is also implemented and tested. See
`docs/REVIEW_ASSISTANCE.md`, `reports/review-assistance-workflow.json` and the
synthetic critique report. It preserves proposal text, flags, human decisions and
reader output; it is not source clearance or owner approval. Do not rebuild it
as the next milestone.

Passage evidence-research and annotation packets are now implemented, including
separate explanation/reflection/fiction drafts and strict unreviewed staging.
See `docs/PASSAGE_KNOWLEDGE_WORKFLOW.md`, decision 0008 and
`reports/knowledge-packets-workflow.json`. Five original synthetic drafts remain
outside the canonical bank; no new real bibliography or human approval exists.
That packet milestone passed 164 tests, 24 schemas and 24 installed-wheel checks.
The Windows long-path failure and fix are recorded in
`reports/knowledge-packets-package-attempt.json` and
`reports/knowledge-packets-package.json`. Do not rebuild these packet types as
the next milestone.

Human knowledge review/promotion is now implemented. See
`docs/KNOWLEDGE_REVIEW.md`, decision 0009,
`reports/knowledge-review-workflow.json` and the unsigned
`reports/knowledge-review-synthetic.md`. Owner decisions, complete original
envelopes and attribution are retained in atomic immutable receipts; only
approved closed current groups project into canonical knowledge. Pending and
rejected heads can be explicitly superseded, and partial groups can resume from
the same response. That milestone passed **186 tests, 26 schemas and 18
installed-wheel checks**. The persistent five drafts still have zero human decisions or
approvals. Do not rebuild this workflow as the next milestone.

Knowledge withdrawal, explicit reactivation and approved-version selection are
now implemented. See `docs/KNOWLEDGE_CURATION.md`, decision 0010 and
`reports/knowledge-curation-workflow.json`. Exact original approvals and
attribution are retained; declared revisions are withheld until selected, and
withdrawn/stale selections have no automatic fallback. That milestone passed
**211 tests, 28 schemas and 19 installed-wheel checks**. Persistent
production/demo reports are unsigned, with zero approved targets and zero owner
actions. Do not rebuild this completed curation slice as the next milestone.

Bounded local canonical-build archive/validation/isolated restore is now
implemented. See `docs/BUILD_ARCHIVES.md`, decision 0011,
`reports/build-archive-manifest.json` and `reports/build-archive-workflow.json`.
The eleven-input fixture archive recovered identical reader/search data into
`dist/archive-restored-fixture-v1`. That milestone passed **230 tests, 29 schemas and
17 installed-wheel checks**. No approvals/actions were created. Original
review/curation history is preserved; unapproved working caches, arbitrary
workspace files and private research snapshots are outside this build scope.
The five actual drafts remain untouched in the original workspace. Retain the
matching engine wheel recorded in PROGRESS; there is no automatic migration or
public-release authority. Do not rebuild this completed archive slice next.

Bounded structured narrative drafts are now implemented. See
`docs/NARRATIVE_DRAFTS.md`, decision 0012 and `reports/narrative-workflow.json`.
That milestone passed **253 tests, 32 schemas and 26 installed-wheel checks**.
Three separate draft schemas and the manual `knowledge narrative` commands bind
exact display spans, typed participants, story relations, scope, support,
approved-name mappings, attribution and uncertainty. Source narration,
unverified historical claims and fiction retain separate graph rules. The
actual original fixture adds eight nodes and one support proposal; no historical
claim or human approval was created. The prior five annotation drafts remain
unchanged. Narratives stay outside canonical knowledge, human promotion,
reader/search and build archives. Do not rebuild this completed draft slice.

Retain the old archive and matching engine wheel recorded in PROGRESS. This
milestone changes the engine identity; the new synthetic compatibility check
uses a different archive. Never overwrite/migrate the earlier snapshot silently.
Pending narrative packets are not included in either canonical-build archive.

The unsigned narrative inspection handoff is now implemented. See
`docs/NARRATIVE_REVIEW.md`, decision 0013 and
`reports/narrative-review-synthetic.md`. This milestone passed **268 tests,
32 schemas and 29 installed-wheel checks**. `knowledge narrative review export`
requires an exact imported response and a current eligible packet, then shows
literal spans beside roles/relations, distinct source/normalized/reader wording,
transitive typed support metadata and exact prior name approval identities.
The existing eight nodes and one witness proposal remain unreviewed; no new
draft, decision or approval was created. There is no narrative review apply or
promotion operation. Do not rebuild this completed report slice.

The owner then prioritized human use from the repository terminal. The
`jeb.cmd` launcher and `jeb work` menu now provide status, source blockers,
numbered saved-work selection, immutable inspection reports, a read-only pager,
explicit isolated demo selection and one-command offline checks. See
`docs/TERMINAL_WORKFLOW.md` and `reports/terminal-workflow.json`. This milestone
passed **291 tests, 33 schemas and 21 installed-package checks**. Existing JSON
commands, exact identity checks and all editorial/source gates remain intact.
The menu does not generate or submit human decisions. Do not restart this
completed terminal entry-point work or silently add an approval shortcut.

**Next small usability task: section navigation in the read-only report viewer.**
Let the human jump to source/proposal/flags or narrative roles/relations instead
of paging through every provenance block. Use the already validated generated
report; preserve exact stored bytes, clear workspace labels, cancellation and
terminal-control escaping. No frontend, source download or decision writing.

The separate advanced narrative validation-only schema/command is already
present in local commit `8a736d4`; see `docs/NARRATIVE_REVIEW.md` and the later
source-audit/validation entry in PROGRESS. It creates no receipt, approval or
canonical narrative. Preserve that work; do not rebuild the validator as though
it were absent. The terminal menu does not submit decision files or populate
human answers. Any future receipt/promotion slice needs its own reviewed typed
schema/code workflow with complete original contribution provenance. Existing
annotation promotion must continue to reject narrative responses. Synthetic
attestations remain confined to temporary tests.

Keep exact GEN/MAT/MRK/LUK/JHN scope, Latin output and protected literal forms.
Demonstrate only original non-scripture data. Continue reversible engineering
without contact, paid/model APIs or publication. No new owner decision is needed
until concrete eligible editorial choices are presented.

Continue this reversible engineering work if there is no new primary lineage
record or authorized provider reply, instead of repeating completed searches.

The optional native SWORD evaluation is now implemented and tested with original
synthetic data. Read `docs/sources/SWORD_TOOLCHAIN_EVALUATION.md` and
`reports/sword-diagnostic-verification.json`. Two native builds produced the same
entry-probe capture. Do not repeat that build as the next milestone or mistake
its success for historical source clearance. The diagnostic is not a corpus
adapter and the stock exporters have measured losses.

**Next: obtain the missing digital-source lineage for CrossWire SrKDIjekav.**

This remains the prerequisite for a real pilot. The latest bounded discovery
pass found no new inspectable primary lineage record; several source/package
metadata endpoints were inaccessible through web research. See
`sources/evidence/lineage-search-followup.json`. No checksum, mirror or generic
upload notice was substituted for the missing source history. The current
follow-up packet below remains unchanged.

The concrete handoff is now prepared at
`data/source-research/cw-lineage-followup-01/input.json` (five unresolved dossier
questions, no scripture or contact permission). See
`docs/SOURCE_RESEARCH_WORKFLOW.md` and `reports/source-research-workflow.json`.
Use that current packet for further public metadata investigation or manual
subscription-tool work. The earlier `cw-submission-history-01` result is retained
as history and correctly fails validation after the separate dossier update.

The archive investigation now recovered the 2017 Ijekavian upload credit **Br**,
the separate Ekavian credit **Tomas**, and a 2014 mention of two unnamed Serbian
texts. See `docs/sources/CROSSWIRE_SUBMISSION_HISTORY.md`. None identifies the
exact print source or digital transcriber. Do not merge the credits, expand Br
from unrelated people-search results, or infer ancestry from the unnamed texts.
Determine the actual role/source file and correction history. Automated update
wording does not by itself establish an earlier textual revision.

The follow-up already inspected the separate configuration and provider release
notice. See `docs/sources/CROSSWIRE_PROVENANCE.md` and the evidence-linked
`sources/assessments/crosswire-srkdijekav.json`. Run
`jeb sources inspect --source crosswire-srkdijekav` for the current gaps.
Do not repeat the same catalogue and About-page searches as if they establish
a new independent witness.

The configuration declares Calvin versification, OSIS/zText, headings and
NoParagraphs, but has no TextSource or print-edition identifier. A catalogue
record for an 1868 Pest item is only a comparison lead; no inspected evidence
connects it to the module. The 910-byte configuration checksum is metadata only,
not the missing scripture ZIP checksum. No biblical text was downloaded.

The next useful evidence is the provider's original source-file/edition history,
transcriber and correction/component information. A concrete, **unsent** question
draft is in `docs/sources/CROSSWIRE_QUESTIONS.md`; contacting anyone needs explicit
authorization. No message was sent by this session. Public release/archive
notices alone did not resolve the lineage. The mailing-list archive, previously
inaccessible in research, was successfully inspected in the latest continuation.
Do not repeat those archive indexes/notices as new independent evidence.

Use the already discovered landing/download links in the register. Investigate
the module's actual historical base edition, later changes, digital transcriber,
component rights and relationship to the 1868 historical publication. Record
verifiable bibliography and precise component scope before any corpus download.
The Ijekavski provider label is not a fidelity check. If this candidate remains
unresolved, record the exact gap and assess a separately eligible alternative;
never silently substitute the Ekavian eBible file or a protected modern edition.

Keep the source needs_review until DE/US/BA/HR/RS/ME assessment evidence and
limitations support the intended use. Seek focused expert review for unresolved
publication rights without claiming the assistant supplied legal sign-off.
Use the completed synthetic evaluation when designing the eventual real adapter;
do not approve stock export from a verse count. Prefer the original OSIS and its
transformation history. A historical adapter still needs exact five-book
link/empty/bridge inventories, original source spans, typed annotations,
unsupported-marker failures and source-faithful reconstruction tests. Do not
treat the compressed module as USFM or strip its markers.

Admission acceptance: exact discovered artifact URL, edition and included
components, revision identity, assessment author/date/evidence for the configured
scope, actual SHA-256/size after permitted acquisition, safe reproducible adapter,
and a reviewed exact-edition coverage manifest containing only approved books.
Any upstream byte change needs explicit re-evaluation, not a lock refresh.

Then implement the first **eligible** small passage slice and prepare separate
manual packets for GEN 1:1-5, MAT 5:1-12, MRK 1:1-8, LUK 17:20-21, JHN 1:1-5.
Do not reconstruct missing wording from memory. Real source context, evidence,
notes, alternatives, attributed reflection and bounded story records must precede
scaling. Measure actual human review effort. Original-name candidates require
witnessed Latin transliteration and honest uncertainty, not fabricated native forms.

The owner already approved the five book IDs and literal svjet, vrjeme, covik,
razumit. Only when showing concrete eligible samples, present unresolved covik
versus čovik, inflections, hljeb/kruh usage and name/scheme options. No repeat
approval of existing decisions is needed. All final text remains unapproved until
a real owner reviews exact hashes.

To inspect the current software without clearing a source, run the README setup
and `python -m jeb demo`; open `dist/demo/exports/reader.md` and
`dist/demo/reports/review.md`. These are labelled synthetic fixtures. Do not
publish, push or create a release without an explicit new authorization.
