# Ja sam jasna biblija (JSB)

**Product direction, 2026-11-19:** one private reading and research desk for books,
their context, explanations, evidence, characters and related stories. Usability
and clear navigation now lead the delivery plan. See the
[reading-desk product brief](docs/READING_DESK_PRODUCT_DIRECTION.md) for the
owner-stated direction, recorded preferences and the proposed first
book-to-evidence-to-connection journey. The owner has now selected
[John 9 as the first usability pilot](docs/JOHN_9_READING_DESK_PILOT.md): library
and search together, desktop side-by-side text/explanation, expandable evidence
and connections, switchable English/Bosnian-Herzegovinian, and private notes,
highlights and suggested connections in the first usable version. Textual
witnesses and independent historical evidence will be distinct categories.
The local interaction prototype now implements that reading flow and saved
private tools on original synthetic stories. John 9 remains a planned research
destination with no admitted text or sourced explanations; the prototype does
not manufacture those contents.

After the existing Python setup below, run:

```powershell
npm run reading:demo -- --synthetic
```

On Windows you can instead double-click [start-reading-demo.cmd](start-reading-demo.cmd)
in the project folder. Follow the [first-session guide](docs/READING_DESK_FIRST_SESSION.md)
for a 10-minute walkthrough; the bilingual guide is also available at the top of
the reading desk under **How to use this desk / Kako koristiti stol**.

Open **http://127.0.0.1:5187/#desk**. The command creates the isolated example only
if missing; otherwise it validates and reopens it with existing private items
preserved. It installs nothing and changes no production source status. Stop
with Ctrl+C; `PORT` can select another loopback port. Use either invented story
to exercise reading, evidence, connections, notes, highlights and suggestions.
John 9 supports a private topic note; highlighting requires actual available text.
The English/Bosnian-Herzegovinian switch leaves source text and your notes intact.
The writing editor stays beside the source. Unfinished drafts recover after a
refresh in the same browser tab when storage is available; **Save privately**
keeps the finished item in the bank. Home search also finds your notes and quoted
highlights under **My saved reading work**, with links back to the passage.
Click a saved highlight to open its comment beside the source. **Ctrl+Enter**
saves from the editor. Conflicting edits can be compared and explicitly saved as
separate private items, preserving the newer saved version.
When a reading view changes or removes a passage, the original draft remains
reachable with its quote and recorded credits. The recovery panel can download
that private draft or prepare a separate note on a current passage, without
moving the old highlight. Unknown save outcomes remain locked for exact retry.

An independent, noninstitutional **selected collection**: Genesis/Postanak
(`GEN`), Matthew (`MAT`), Mark (`MRK`), Luke (`LUK`), John (`JHN`). The intended
text is an independently edited modernization of a verified historical
translation, with explicit translator credits. It is not a new translation from
ancient languages, a complete Bible, or a church-endorsed canon.

Development version: **0.1.0-dev**. Phase 0 and the synthetic Phase 1 slice are
implemented. **No historical scripture artifact is cleared or ingested into the
corpus; zero admitted real verses and zero owner text approvals.** Private source
investigations do not count as admitted coverage. The software demonstration
uses four explicitly invented segments, never scripture generated from memory.
Read [PROGRESS.md](PROGRESS.md) and [NEXT_STEPS.md](NEXT_STEPS.md) when resuming.

## Personal knowledge-bank foundation

New banks may explicitly select `bank init --format 3.0` for persistent unreviewed
claim/evidence records with exact historical revision references. Existing2.0
banks remain unchanged and the default stays2.0. `bank reference` and
`bank evidence links` expose pinned versions and whether support applies to the
current claim. Both managed formats have private backup/restore support.
See [persistent evidence workflow](docs/BANK_PERSISTENT_EVIDENCE.md).

The separate personal bank supports `jeb bank init/create/edit`, revision
`history/diff`, interrupted-write `recover`, and `validate/show`, all with an
explicit `--bank-root` directory. Managed format 2.0 uses immutable full snapshots
and an atomic HEAD pointer, with a process lock and expected-revision conflicts.
Entity/source/article records have strict schemas, typed references and body
hash checks. Initial format 1.0 remains read-only with no automatic migration.
This does not admit sources into the biblical corpus. Evidence assessment,
selected-content export and general bank editing in the browser remain future
phases. The bank viewer is read-only; the separate synthetic reading desk supports
only the private reading tools described above.
Private `bank backup/backup-verify/restore` now preserve the committed chain;
see [backup instructions and limits](docs/BANK_BACKUPS.md). Full-copy history
currently has protective limits of 128 snapshots and 128 MiB of history payload.
`bank evidence prepare/validate/inspect` now supports separate unreviewed claim
and evidence packets bound to exact2.0 record revisions and HEAD. Text spans
are checked against local source bodies; page/section/time locators remain
declared only. These private drafts are outside the canonical bank and its
backups; see [evidence workflow and original example](docs/BANK_EVIDENCE.md).
See [bank workflow and original example](docs/BANK_WORKFLOW.md),
[format](docs/BANK_FORMAT.md), [v2→v3 dry-run contract](docs/BANK_MIGRATION.md)
and [implementation plan](docs/KNOWLEDGE_BANK_IMPLEMENTATION_PLAN.md). For a
first local bank session, use the [bank quickstart](docs/BANK_QUICKSTART.md).
The initial Catholic Bible knowledge-bank pilot is scoped in
[BANK_CATHOLIC_BIBLE_PILOT.md](docs/BANK_CATHOLIC_BIBLE_PILOT.md).

## Optional local visual workspace

The viewer now opens on **Stol za čitanje / Reading desk**, with library and
prominent search together. **Moja biblioteka** retains the owner's separate 291-item
research inventory, with category/status filters, title/author/translator search,
reviewed edition links and explicitly unreviewed discovery leads. See
[library notes](library/README.md) for actual acquisition counts and limitations.
This does not expand the five-book edition. Personal-library downloads stay
private and are not served by the viewer.

With Node.js 22+ installed, run from this repository:

```powershell
npm run dev
```

Open **http://127.0.0.1:5187**. No npm install is needed: the optional viewer
uses only Node's standard library and plain HTML/CSS/JavaScript. Stop with Ctrl+C.
Set `PORT` if needed (PowerShell: `$env:PORT = '5188'`).

The read-only interface also provides project orientation, the production lock entry
count, dated source-research summaries, language direction and ten selected
documents with full-content search and section navigation. Refresh to reread
changed project files. Markdown is shown as safe text with heading/code styling;
inline formatting and tables retain their original notation. By default it does
not load private evidence, historical scripture, proposals, approvals or the
synthetic workspace. The separate opt-in views below expose only their documented
data. It cannot validate source eligibility or replace the Python CLI.
By default these views write no files. The explicit synthetic reading-demo
launcher additionally enables only the bounded private reading-item endpoint;
existing bank, historical and document routes remain read-only. Nothing is
published. The server binds only to loopback.
The Python package and its hash-locked environment remain independent.

## Optional local knowledge-bank view

To view an existing private managed bank in the local read-only interface, set
`JEB_BANK_ROOT` before starting the server:

```powershell
$env:JEB_BANK_ROOT = 'C:\moja-baza-znanja'
npm run dev
```

The **Baza znanja** page lists current entity/source/article/claim/evidence
records and opens their stored metadata/body as safe text. For v3 claims and
evidence it shows typed subject/source/claim relationships, relation labels,
revision status and a bounded history summary; related records can be opened
through local safe links. Records can also be filtered by entity, source,
article, claim or evidence. The bank is not enabled unless `JEB_BANK_ROOT` is
explicitly set; the viewer has no write route, does not expose the repository
root, serves no historical body bytes through the history summary, and never
serves the bank through the public network.

Run the local server access checks with `npm run test:web`.

## Historical processing and dossier queries

The local historical pipeline now processes bounded artifact batches, resumes
interrupted jobs and publishes complete hash-bound snapshots. CLI and the
optional viewer share the Python validation/query implementation. Queries return
proposal groups, exact projection offsets, editions and contributor credits;
they do not merge identities or approve sources.

After the Python setup below, create an isolated original fixture at a **new**
path, then query its invented label:

```powershell
.\.venv\Scripts\python.exe -m jeb --synthetic historical demo --workspace dist/historical-synthetic-demo
.\.venv\Scripts\python.exe -m jeb --synthetic historical dossier --workspace dist/historical-synthetic-demo/pipeline --query Luma
```

If that directory already exists, inspect it with the second command or choose
a new demo destination. The fixture is marked synthetic and unreleasable; it
contains three readable artifacts, one missing file and one invalid UTF-8 file.
Real-source extraction remains blocked by `source_review_required` before opening
source bytes. Never use `--synthetic` on historical material. See the
[pipeline guide](docs/HISTORICAL_TEXTS_PIPELINE.md) for incremental steps,
retries, limits, locator semantics, CLI/API errors and explicit viewer opt-in.

New synthetic PDF tasks retain the exact bounded UTF-8 projection in a separate
v2 extraction cache. `historical projection-verify --workspace ... --cache-sha256
...` checks its hash and literal spans without reopening the PDF or invoking the
tool. Existing v1 caches stay unchanged and explicitly report that projection
bytes were not retained. This preserves projection evidence, not the source PDF
or source eligibility; see the retention contract in the pipeline guide.

## Everyday use in the repository terminal

Already set up? On Windows, run **`.\jeb.cmd`** for the numbered task menu.
Choose status, source blockers, saved review work, the isolated example or checks.
Review selection uses numbers instead of copying long hashes.

```powershell
.\jeb.cmd status
.\jeb.cmd demo
.\jeb.cmd --demo review
.\jeb.cmd check
```

See the [short terminal guide](docs/TERMINAL_WORKFLOW.md). The menu produces
inspection reports and never records approvals, changes source clearance or
publishes. Existing advanced JSON commands remain available. First-time setup
is below; no activation or PowerShell execution-policy change is needed.

## Start on Windows 11 / PowerShell

Run from this existing repository. Python **3.13.x** is the supported runtime.
No API keys, model API calls, cloud database, paid services or browser-chat
automation are used. Installing dependencies needs ordinary package-download
access; subsequent tests and the demo are offline.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements.lock
.\.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .
.\jeb.cmd
```

Using the venv executable directly avoids changing PowerShell execution policy.
The equivalent Linux setup is:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-build-isolation --no-deps -e .
.venv/bin/python -m jeb sources audit
.venv/bin/python -m jeb demo
```

`jeb` is also installed into the venv. The commands below use it as shorthand.
The demo creates an isolated workspace at `dist/demo/` and can be rerun with
identical inputs. It refuses to overwrite changed configuration/source artifacts.
It never changes production source clearance or creates human approvals.

Open these generated files locally:

- `dist/demo/exports/reader.json` and `reader.md`: source-only synthetic previews,
  exact coverage for all five approved books, typed layout and source notes.
- `dist/demo/reports/review.md`: source, proposal, diff, flags, hashes, and
  unreviewed decision status.
- `dist/demo/data/batches/fixture-modernize-v1/input.json`: self-contained manual
  work packet with policy, glossary, source context and strict output schema.
- `dist/demo/data/index/search.sqlite3`: disposable local FTS5 search index.

## Implemented commands

Global `--root` and `--synthetic` options go **before** the command. Outputs must
stay within the selected root. Source IDs are mandatory for corpus operations.

```powershell
jeb --version
jeb sources audit
jeb sources inspect --source crosswire-srkdijekav
jeb validate --stage schemas
jeb --root dist/demo --synthetic validate --stage normalized --source synthetic-v1
jeb --root dist/demo --synthetic validate --stage knowledge --source synthetic-v1
jeb --root dist/demo --synthetic search --source synthetic-v1 --query covik
jeb --root dist/demo --synthetic export --source synthetic-v1 --profile five-book --format json --maturity preview --output exports/another-reader.json
```

The following interfaces exist, but real corpus commands require an eligible
source, reviewed lock, supported adapter and exact coverage manifest. **There is
currently no historical source ID that can pass those gates.**

`sources inspect` is read-only and offline: successful inspection does not mean
admission. Its evidence-linked report identifies the exact missing edition,
provenance, component-rights, versification, adapter, jurisdiction and lock checks.
Provider configuration/catalogue metadata hashes are distinct from scripture
artifact hashes. See the [CrossWire follow-up](docs/sources/CROSSWIRE_PROVENANCE.md).

```text
jeb fetch --source <verified-id>
jeb parse --source <verified-id>
jeb normalize --source <verified-id>
jeb batch prepare --source <verified-id> --batch-id <new-id> --selection GEN --task modernize
jeb batch validate --input <returned-json>
jeb batch import --input <returned-json>
jeb review export --proposal <proposal-id> --output reports/generated/review.md
jeb review apply --decisions <human-reviewed-json>
jeb index --source <verified-id>
jeb release check --source <verified-id> --edition jeb-selected-dev
```

Pilot selection uses **one coherent passage per packet**: `GEN` = 1:1-5, `MAT`
= 5:1-12, `MRK` = 1:1-8, `LUK` = 17:20-21, `JHN` = 1:1-5. These are future
eligible work packets, not existing text or wording approvals. `fixture` is a
separate synthetic-only selection. Passage research, annotation drafts and
optional AI review assistance use separate workflows below. Full USFM, OSIS,
SWORD, EPUB, PDF and a reader frontend
are also deferred. `jeb --help` is the implemented CLI, not a roadmap.

An optional **synthetic-only SWORD diagnostic** is implemented separately from
corpus parsing. A pinned native rebuild exposed lost introduction records,
mislabelled versification and whitespace changes in stock exports. The bounded
probe retains stored markup, explicit link identities and empty slots. Validate
the captured original fixture without C++ tools or network access:

```powershell
jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
```

See the [evaluation](docs/sources/SWORD_TOOLCHAIN_EVALUATION.md) and
[optional build instructions](toolchains/sword-1.9.0/README.md). This diagnostic
cannot import a historical module or approve a production adapter. Its original
technical sentences are additional test data, separate from the four-segment demo.

Metadata-only source research has a separate manual workflow. It works before
source clearance and includes no scripture payload. Prepare a packet to paste or
attach in a subscription tool, then validate and stage its returned observations:

```powershell
jeb sources research prepare --source crosswire-srkdijekav --packet-id lineage-01
jeb sources research validate --input <returned-metadata-json>
jeb sources research import --input <returned-metadata-json>
jeb sources research report --input <returned-metadata-json> --output reports/generated/lineage-01.md
```

The prepared file is `data/source-research/lineage-01/input.json`. Imports remain
unreviewed and never edit the registry, dossier or source lock. Packet input
changes invalidate responses; competing responses remain separate, with no
automatic consensus or conflict resolution. See the
[manual research guide](docs/SOURCE_RESEARCH_WORKFLOW.md) and the new
[primary submission-history findings](docs/sources/CROSSWIRE_SUBMISSION_HISTORY.md).

Optional review-assistance packets compare an existing proposal with its exact
source/context, policy, diff and flags. They use the same source-admission gate
as the proposal, and returned critiques have no approval authority:

```powershell
jeb review assist prepare --proposal <proposal-id> --packet-id review-01
jeb review assist validate --input <returned-critique-json>
jeb review assist import --input <returned-critique-json>
jeb review assist report --input <returned-critique-json> --output reports/generated/critique-01.md
```

For the demo, put `--root dist/demo --synthetic` before `review`. Each existing
flag must remain explicitly assessed, and meaning-sensitive items retain expert
escalation. These commands cannot apply text edits, resolve flags or change human
decisions. See the [review-assistance guide](docs/REVIEW_ASSISTANCE.md) and
[actual synthetic critique](reports/review-assistance-synthetic.md). Owner review
still uses the separate `review apply --decisions` interface.

Passage research and annotation work uses eligible source context and the exact
current reader wording. It does not annotate an unapproved modernization:

```powershell
jeb knowledge prepare --source <verified-id> --selection GEN --task research --packet-id research-01
jeb knowledge prepare --source <verified-id> --selection GEN --task annotate --packet-id notes-01
jeb knowledge validate --input <returned-json>
jeb knowledge import --input <returned-json>
jeb knowledge report --input <returned-json> --output reports/generated/notes-01.md
```

Research returns unverified leads and questions. Annotation returns attributed,
unapproved evidence/claim/annotation drafts with exact text and evidence links.
Imports stay under `data/knowledge-proposals/`, separate from the canonical bank
and reader. Explanation, personal reflection and creative adaptation retain
distinct labels. See the [passage workflow](docs/PASSAGE_KNOWLEDGE_WORKFLOW.md)
and [synthetic drafts](reports/annotation-synthetic.md). The unchanged v1 editorial
policy's final implementation note describes the initial slice; this command
guide records the current interfaces.

Human knowledge review uses a separate owner-decision format:

```powershell
jeb knowledge review export --packet-id <packet-id> --response-sha256 <full-sha256> --output reports/generated/human-notes.md
jeb knowledge review validate --decisions <reviewed-json>
jeb knowledge review apply --decisions <reviewed-json>
```

The [human knowledge review guide](docs/KNOWLEDGE_REVIEW.md) explains exact
bindings, explicit checks, partial dependency groups and competing responses.
One immutable receipt preserves the original packet, AI attribution and human
decision; approved records derive from it without hand-copying JSONL. Rejections
and pending reviews add no canonical content. Approved IDs remain immutable;
separate curation controls their reader eligibility. The
[synthetic review report](reports/knowledge-review-synthetic.md) is unsigned;
the five persistent drafts still have no human approval.

Withdrawals, explicit reactivation and selection among approved versions use:

```powershell
jeb knowledge curate export --output reports/generated/curation.md
jeb knowledge curate validate --decisions <owner-actions-json>
jeb knowledge curate apply --decisions <owner-actions-json>
```

See the [curation guide](docs/KNOWLEDGE_CURATION.md). A revised draft can declare
its exact original in the human approval item's optional `version_of`, with an
additional relationship check. It stays withheld until explicitly selected.
Curation keeps original approvals and attribution intact, hides dependents and
never silently falls back to an older note. Withdrawal works for stale or
rights-blocked subjects; selection/reactivation require current source/support.
The [unsigned synthetic curation report](reports/knowledge-curation-synthetic.md)
has no approved targets, because the five drafts remain unapproved.

Typed unreviewed entities, events and stories use a separate manual workflow:

```powershell
jeb knowledge narrative prepare --source <eligible-source> --selection GEN --packet-id narrative-01
jeb knowledge narrative validate --input <returned-json>
jeb knowledge narrative import --input <returned-json>
jeb knowledge narrative report --input <returned-json> --output reports/generated/narrative-01.md
```

The [narrative guide](docs/NARRATIVE_DRAFTS.md) explains exact character spans,
participants, presentation order, source evidence and uncertainty. Source
narration, unverified historical claims and fiction keep separate typed graphs.
Only attached approved name mappings can change a source mention's display.
Imports stay outside canonical knowledge, human promotion, reader/search and
build archives. The [original synthetic example](reports/narrative-synthetic.md)
adds eight nodes and one witness proposal, all unreviewed; real coverage stays
zero. No historical events or owner approvals were manufactured.

For an exact imported narrative response, export the unsigned inspection handoff:

```powershell
jeb knowledge narrative review export --packet-id <packet-id> --response-sha256 <full-sha256> --output reports/generated/narrative-review.md
```

The [handoff guide](docs/NARRATIVE_REVIEW.md) and
[synthetic handoff](reports/narrative-review-synthetic.md) show literal spans beside
roles/ordering proposals, support chains and prior name-approval identities.
This writes one bounded Markdown report and creates no decision or approval.

Preview exports include faithful normalized source text and exact approved
text where present. They never export unapproved modernization. Every segment
states its maturity; unchanged approved historical text has a distinct label.
Release requires all five complete source books, all included text approved,
current provenance and a separately approved honest preface. Synthetic fixtures
and unresolved meaning-sensitive edits can never pass release checks.

## Validate locally

Local build recovery is available without publishing an edition:

```powershell
jeb --root dist/demo --synthetic archive create --source synthetic-v1 --archive-id fixture-build-01 --output dist/archives/fixture-build-01.zip
jeb --synthetic archive validate --input <archive.zip>
jeb --root <existing-parent> --synthetic archive restore --input <archive.zip> --destination recovered-build
```

The [archive guide](docs/BUILD_ARCHIVES.md) describes the explicit input allowlist,
scope, limits and compatible-engine requirement. Original review/curation history
is preserved; corpus, reader and index are rebuilt in staging. Recovery needs a
new destination and creates no approvals. This is a local canonical-build backup;
unapproved working caches and arbitrary workspace files are excluded.

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m ruff format --check src tests
.\.venv\Scripts\python.exe -m jeb validate --stage schemas
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The offline suite exercises failed acquisition, changed hashes, archive safety,
exact coverage, notes/poetry/bridges, normalization, strict model-return schemas,
collection boundaries, stale proposals and approvals, evidence links, independent
text/note review, deterministic exports and SQLite search. Passing tests prove
software behavior, not legal clearance, linguistic fidelity or scholarly review.
The SWORD capture tests also reject dropped/invented links, changed stored bytes,
introduction/empty-slot confusion and executable checksum mismatches. Native
compilation is optional and is not required by the offline suite or CI.

Runtime dependencies are PyYAML (safe, duplicate-aware YAML configuration) and
jsonschema (strict versioned data validation). SQLite, HTTPS, hashing, CLI and
tests use the standard library. `requirements.lock` pins transitive, build and
lint dependencies with PyPI release hashes for Windows/Linux Python 3.13 wheels.
Editable installation uses the already locked build backend; it does not
resolve new dependencies. See [architecture](docs/ARCHITECTURE.md).

## Editorial and source boundaries

The owner's literal choices `svjet`, `vrjeme`, `covik`, `razumit` are recorded;
derived inflections remain unapproved. Ordinary Latin diacritics remain.
`hljeb`/`kruh` context proposals await sample review. No original-name spelling,
reconstructed native form or transliteration scheme has been approved.

See [charter](docs/PROJECT_CHARTER.md), [source audit](docs/SOURCE_AUDIT.md),
[rights policy](docs/RIGHTS_POLICY.md), [editorial policy](docs/EDITORIAL_POLICY.md),
[review guide](docs/REVIEW_GUIDE.md), [data model](docs/DATA_MODEL.md) and
[format grammar](docs/TRANSCRIPT_FORMAT.md). Upstream rights, our editorial
contributions and software licenses stay distinguishable in the
[license matrix](LICENSES/README.md) and [NOTICE.md](NOTICE.md).

Changes are local and uncommitted. Review them in GitHub Desktop. Committing or
pushing, publishing a site and creating a public release are separate owner
actions; nothing in this setup performs them.
