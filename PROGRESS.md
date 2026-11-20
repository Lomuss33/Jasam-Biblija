# Session continuity: 2026-10-31

## Git handoff authorized by the owner — 2026-11-20

The owner explicitly requested "push all to git". Read PROGRESS, NEXT_STEPS,
AGENTS and git status before preparing the commit. The current branch is main,
tracking origin/main at https://github.com/Lomuss33/Jasam-Biblija. `git fetch
origin` succeeded and `git rev-list --left-right --count HEAD...origin/main`
reported 0 / 0 before this commit. Remotes and existing history were not changed.

Reviewed all tracked/non-ignored inputs and the pending code, metadata and
documentation. An inline read-only Python audit checked 373 files (4,811,045
bytes): no protected private/workspace paths, binary payloads, non-UTF-8 files
or recognizable credential/private-key patterns were found in the Git set.
`git ls-files -ci --exclude-standard` was empty. Existing ignores continue to
exclude private historical evidence, all five personal-library source files,
raw downloads, local banks, .venv, dist and generated reports. No ignored source
bytes or generated artifacts are force-added. Library receipts, catalogue and
research links are metadata, not the private edition files.

Pre-commit commands `.venv/Scripts/python.exe -m ruff check src tests`,
`.venv/Scripts/python.exe -m ruff format --check src tests`,
`.venv/Scripts/python.exe -m jeb validate --stage schemas` and `git diff --check`
passed: 75 formatted Python files and 62 valid schemas. All 108 packaged Python
files exactly match the previously verified wheel. The existing full offline
baseline remains 439 tests, OK with one Windows symlink skip (370.862 s), plus
the latest 17/17 web checks and passing complete browser journey (54.489 s).
Those test results are recorded above; no unchanged full suite is claimed as
rerun solely for a Git operation. This handoff includes the existing pending
bank/historical/library work together with the completed reader and draft
recovery, retaining all source/editorial decisions and synthetic restrictions.

Staged inspection exposed two extra trailing blank lines in previously
untracked text files and Git normalization of 11 CRLF bank-schema resources.
Removed only those blank lines and marked packaged schemas byte-preserving in
`.gitattributes`: backup/reading identities hash exact schema bytes, so a fresh
checkout must retain the already-verified resource bytes. No schema body or
validation/rights rule was changed. Staged/checkout-filter byte parity is checked
before committing; private workspaces and backup files remain untouched.
The schema-only whitespace attribute recognizes CRLF while retaining ordinary
blank-at-EOL/EOF and space-before-tab checks; it does not mask content whitespace.
Final staged audit passed: 138 changed files, all 108 packaged files equal the
verified wheel, and all 62 schemas preserve their exact bytes through Git's
checkout filters. `git diff --cached --check` passed after the two EOF fixes.

The authorized next Git operations are one ordinary commit of non-ignored
project changes and a non-force push to the existing origin/main. No release,
deployment, source clearance, real owner text approval or PR creation is part
of this handoff. The next product task remains the John 9 source-readiness plan.

## Changed-view and orphaned draft recovery — 2026-11-20

Continued the documented next writing task after the owner's Continue. Read
PROGRESS, NEXT_STEPS, git status and AGENTS first, preserving pre-existing dirty
work, source/editorial decisions and the five-book scope. No further preference
question or owner approval was inferred.

Drafts bound to an earlier reading view now open a recovery panel with read-only
original writing and quote, instead of an ordinary editor pointing at changed
text. New drafts capture their original title/location, source binding and
edition/creator/translator credits; older drafts label missing metadata honestly.
Cleared temporary source focus when the view changes so coincidentally identical
words cannot acquire an old draft's visual anchor. The panel also renders on the
home screen when its passage was removed. Fixed source/context capture and
restoration to tolerate absent reading panes, avoiding the former Return-to-draft
dead end and null-pane access after a view refresh.

Explicit recovery prepares a separate whole-passage note on the chosen current
destination, copying private wording only. Its new payload has no quote anchor,
connection target, old item ID or expected edit revision; existing Python
validation/writing still owns all persistence. Original draft/binding/quote are
never rewritten, and remain visible after the new note saves. If the prepared
destination view changes too, another explicit current-view choice is required.
Cancel new note discards only an unsaved prepared copy; original discard is
blocked until that copy is either cancelled or confirmed saved. Discarding a
browser original never deletes any committed bank item.

Added a user-triggered private JSON download preserving original draft metadata,
quote, credits and recovery request state. It serializes only the draft (no
session token or application state), labels it synthetic/unreleasable/private and
does not claim a bank backup or new import/restore contract. Nothing downloads
automatically. Browser-draft retention is still limited to available session
storage and the same tab; the existing committed bank backup is unchanged.

Recovery copies retain their own immutable payload/UUID across unknown outcomes,
while keeping the original draft. Strengthened ordinary and recovery retry
handling: a denied, busy or validation failure during retry cannot prove an
earlier unknown request never committed. Only a matching saved result or the
existing writer errors emitted after committed request-ID lookup settle that
uncertainty. Unknown operations cannot be edited, cancelled or copied afresh.
The UI shows Saving while a request is running, then exposes Retry only after
an unknown result. No arbitrary Node writer, new HTTP route, schema or source
gate change was introduced.

Updated the guide, README, pilot, product direction and NEXT_STEPS. No Python
source, schema hashes, source bytes, real John 9 material, translator/name
decisions, rights records or approvals changed. No dependency install, external
contact, publication, commit or push occurred.

Actual verification:

- `npm run test:web`: 17/17 passed (21.883 s). New checks cover strict view
  bindings, missing passages, unavailable views, pending recovery visibility,
  independent unanchored payload creation, exact draft/quote/credit export and
  preserving unknown outcomes across auth/read-only/busy/validation failures.
  Log: `reports/generated/reading-recovery-web-2026-11-20.txt`.
- `npm run test:reading:browser`: final run 1/1 passed, no skips or browser
  runtime errors (54.489 s). In an isolated bank, an unsent unknown original save
  was resolved before copying; two actual view revisions kept the old quote and
  credits while requiring deliberate recovery destination selection. A real
  recovery save committed despite a simulated lost reply; an intervening denied
  retry kept it locked, and refresh/exact retry preserved the same revision and
  quota. The recovered item is a fifth private item, a JHN topic note with null
  anchor/target and a new binding. The original browser draft stayed intact.
  Removing its old passage and refreshing still exposed recovery on home, with
  no stale locator or null-pane crash and no horizontal overflow at 460 px.
  Original discard left all five bank items intact. Prior writing, conflict,
  source wording, private types, language/help, search and location checks passed.
  Log: `reports/generated/reading-recovery-browser-2026-11-20.txt`; report:
  `reports/generated/reading-browser-verification.json`.
- The first browser attempt sampled history before an in-flight recovery request
  completed because the disabled button already said Retry. Fixed the progress
  label and tightened the completion wait, then reran successfully. No storage
  gate or expected result was relaxed.

Tests revised only original synthetic view metadata in temporary banks, not
historical text or the owner's workspace. Their server/profile/processes were
cleaned up. The prior 439-test Python and installed-wheel result remains the
unchanged Python baseline, not a new full-suite run here. Final commands
`node --check web/reading.js`, `node --check web/reading-state.mjs` and
`node --check web/reading-i18n.mjs` passed. Unchanged-source checks
`.venv/Scripts/python.exe -m ruff check src tests`,
`.venv/Scripts/python.exe -m ruff format --check src tests` and
`.venv/Scripts/python.exe -m jeb validate --stage schemas` passed: 75 formatted
Python files and 62 valid schemas. `git diff --check` and a read-only check of
Latin-authored text, whitespace and 63 local links across six guide/handoff
documents passed. Final status preserves the existing dirty/untracked work.

Next small task: the bounded John 9 exact-edition/source-readiness plan using
existing evidence and current gates; the implemented writing recovery is not a
populated real study desk or a claim of completed owner usability acceptance.

## Direct highlight comments, keyboard writing and conflict recovery — 2026-11-20

Continued after the owner's explicit CONTINUE, retaining the chosen writing
notes/highlights priority. Read PROGRESS, NEXT_STEPS, git status and AGENTS first;
preserved existing dirty/untracked work and editorial decisions. No new product
preference question or inferred owner approval was needed.

Saved highlight text now opens a private-item viewer beside the source, with
mouse click or Tab then Enter/Space. Overlapping ranges expose all saved
highlights covering the selected segment; exact source text and Unicode code
points remain unchanged. The new `sourceSegments` projection validates current
view/anchor ownership once per item, then attaches only matching saved IDs to
text spans. Old-view/foreign/invalid anchors cannot become interactive, and a
temporary evidence/focus mark is not treated as a saved comment. Selecting source
text, including a range crossing credits and text, does not open the viewer.

Confirmed saves show their private item beside the source rather than leaving
the writer with only a message and a distant list. The viewer supports editing
the existing item and closing without discarding an open draft. It uses safe
text nodes, explicit private-item kinds and keyboard focus. Ctrl+Enter (also
Meta+Enter) submits the editor through its existing validation; ordinary Enter
remains multiline input. Saving/unknown-result guards still prevent duplicate
submissions and prohibit editing/cancelling an uncertain committed request.

On a confirmed revision conflict the UI refreshes the saved item, keeps the
writer's draft, and displays the latest saved wording (and connection target
where relevant). The ordinary save is disabled for that conflicting edit.
An explicit **Save my draft as a separate item** action creates a fresh private
item/request ID with the original source/anchor/view binding, preserving the
newer saved record. It cannot run for an unknown save outcome, blank required
text, read-only session or changed view. Cancel discards only the browser draft.
Conflict state survives same-tab refresh. No automatic merge, overwrite,
re-anchoring or new writer route was added; existing Python validation/writing
and strict request fields handle the operation.

Updated English/Bosnian help, first-session guide, README, pilot, product direction
and NEXT_STEPS. No Python source, schema hashes, bank formats, protected literals,
translator/edition/name decisions, rights gates or source files changed. No real
John 9 text, interpretation or evidence was invented/acquired. The prototype is
still opt-in, isolated and unreleasable. No dependency install, publication,
owner attestation, commit or push was made.

Actual checks:

- `npm run test:web`: 14/14 passed (23.350 s). The additional projection test
  covers exact original text, overlapping comment IDs, Unicode offsets,
  earlier/foreign/invalid-anchor exclusion and evidence-only markers. Existing
  saved-work search, HTTP/token/origin/size/conflict/retry checks still passed.
  Log: `reports/generated/reading-comment-web-2026-11-20.txt`.
- `npm run test:reading:browser`: final run 1/1 passed with zero skips/runtime
  errors (34.673 s). Extended the complete reading journey to click and keyboard
  open highlight comments, edit via the inline viewer, save with Ctrl+Enter,
  retain multiline Enter, avoid opening while selecting/copying and preserve
  a draft while opening/closing comments. An actual external edit caused a
  conflict; its latest wording and the original draft both survived refresh.
  Saving the draft separately produced a fourth item while the original kept
  its latest saved content and the new item kept its view/anchor scope. Source
  wording, all three private kinds, cancel, language/help, saved-work retrieval,
  exact locators, lost-response recovery, source scroll and narrow layout passed.
  Log: `reports/generated/reading-comment-browser-2026-11-20.txt`; report:
  `reports/generated/reading-browser-verification.json`.
- The first browser attempt stopped on a test-harness global `const mark`
  redeclaration. Scoped the test snippets to their own functions and reran; no
  application workaround was needed. A later final run also verified a selection
  spanning source credits and text after tightening that click guard.
- `node --check web/reading.js`, `node --check web/reading-state.mjs` and
  `node --check web/reading-i18n.mjs`: passed.
- `.venv/Scripts/python.exe -m ruff check src tests`: passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`: 75 formatted files.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`: 62 schemas passed.
- `git diff --check`: passed after the handoff edits. A read-only documentation
  check passed for Latin-authored text, whitespace and 63 local links across six
  current guide/product/handoff documents. Final status preserves the existing
  dirty and untracked work.

Tests ran against separate temporary synthetic banks/profiles and cleaned their
owned servers/processes; the owner's saved workspace was not used. The prior
439-test Python/wheel verification remains the unchanged Python baseline, not a
new full-suite run in this client-only increment. Full study content and owner
acceptance remain open. Next small coding task: make stale-view draft recovery
clearer while preserving the old exact anchor, without automatic reattachment;
the separate real John 9 source/content plan remains pending.

## Better note/highlight writing and saved-work retrieval — 2026-11-20

Read PROGRESS, NEXT_STEPS, git status and AGENTS before continuing; retained all
pre-existing uncommitted implementation/editorial work. The owner reported
"works good i guess. but needs more work." Asked which part felt unfinished
while examining concrete gaps in saved-work retrieval. The owner selected
**Writing notes and highlights**. Recorded that as the current priority; it is
tentative trial feedback, not full usability acceptance or a source approval.

The private editor now opens above the explanation in the right reading pane,
beside the exact source on desktop, rather than sending the writer below both
panes. On narrow screens it follows the source. Add note starts a whole-passage
note even when words happen to be selected. Highlight selection shows the exact
quote and an explicitly optional comment. Editing existing anchored notes keeps
their original scope. Labels/placeholders explain what to write; blank notes or
connection reasons cannot be submitted. Save/Cancel and uncertain-save guards
remain explicit. A link/count beside the passage title reaches saved notes.

Ordinary unfinished drafts are now kept in browser session storage when
available, scoped by reading-view record identity. They survive same-tab refresh
and language/navigation changes without writing bank revisions. The editor
honestly distinguishes a browser-kept draft from a committed private item and
falls back to an unsaved warning if storage fails. Cancel and confirmed save
clear that draft. Separate unconfirmed requests take precedence on recovery;
their immutable UUID/payload is retried without changing text or duplicating a
committed edit. Legacy unscoped requests migrate only for the matching view;
another workspace's pending request is preserved. Closing a tab and browser
draft backup are not promised; committed bank backup coverage is unchanged.

Home search now finds personal wording, exact highlighted quotes and associated
passage/destination titles under **My saved reading work / Moji spremljeni
zapisi**. It supports note/highlight/suggestion filters, recent-first ordering,
explicit result counts and Show more. Open saved item focuses its private card;
Locate in source brings the exact current quote into view. Stale/earlier-view
items keep their wording and label, without applying a locator merely because
the same words occur in a newer view. Catalogue, source passages and personal
items remain separate groups; literal retrieval is not AI answering.

Updated the English/Bosnian in-app guide, first-session document, README,
John 9 pilot, product direction and NEXT_STEPS with actual writing/recovery
behavior. No Python source, packaged schema, bank format, real text, source
policy, edition/translator/name decision or approval was changed. The synthetic
workspace remains explicit, isolated and unreleasable. No source acquisition,
publication, dependency download, commit or push was made.

Actual verification:

- `npm run test:web`: 13/13 passed (19.540 s); existing HTTP/storage-boundary
  checks and a new retrieval/anchor test cover private wording and quotes,
  English/Bosnian titles, kind filtering, preserved input order, Unicode spans
  and refusing older/foreign/changed source bindings even when wording matches.
  Log: `reports/generated/reading-saved-work-web-2026-11-20.txt`.
- `npm run test:reading:browser`: final run 1/1 passed, no skips or runtime
  errors (22.514 s). The complete local Edge journey now covers the editor
  beside the source, optional highlight comment, a new whole-passage note despite
  an active selection, empty-note prevention, same-tab draft refresh/recovery,
  no history consumption while typing, cancel removing recovery state, keeping
  a foreign pending request, saved-word/quote search, kind filtering, focus on
  the saved card, exact-source return, bilingual/help behavior and narrow layout.
  Simulated a lost response after a real committed note edit, moved its request
  into the legacy key, refreshed and retried: the committed revision and remaining
  history count stayed identical. Existing source wording, three saved item types,
  source scroll/expanded-section return and reopened items still passed.
  Log: `reports/generated/reading-writing-browser-2026-11-20.txt`; machine
  report: `reports/generated/reading-browser-verification.json`.
- `node --check web/reading.js`, `node --check web/reading-state.mjs` and
  `node --check web/reading-i18n.mjs`: passed.
- `.venv/Scripts/python.exe -m ruff check src tests`: passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`: 75 files formatted.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`: all 62 passed.
- `git diff --check`: passed. A read-only Python documentation check verified
  Latin-authored text, whitespace and 63 local links across six current
  guide/product/handoff documents. Final git status retains the existing dirty
  and untracked work.

The earlier 439-test Python suite and installed-wheel check remain the prior
unchanged Python implementation result, not a new full-suite run in this UI
increment. Tests used isolated temporary banks/browser profiles, not the owner's
saved workspace. The browser-owned server/profile were cleaned up.

Next small task: the owner tries one passage note and one commented highlight
with the revised editor, then fix the first concrete remaining writing issue.
Real John 9 source/text/explanations/evidence remain a separate unpopulated track.

## First-use guide and Windows reading launcher — 2026-11-20

Read PROGRESS/NEXT_STEPS/git status and AGENTS before continuing; preserved the
existing uncommitted work. Asked for concrete observed friction while examining
the remaining John 9 preparation. The owner clarified they had not tried the
prototype and requested a clear guide. Prioritized first-use instructions; no
owner usability pass or new source-research finding is claimed.

Added `docs/READING_DESK_FIRST_SESSION.md`, a 10-minute walkthrough using the
actual control labels: launch, choose language, open the ledger practice story,
read source/explanation, locate exact evidence, follow a connection and return,
save a highlight/note/suggestion, switch language, reopen and stop/restart. It
explains where editors and saved items appear, the catalogue/text distinction,
John 9's expected planned state and recovery of an unconfirmed save. It links
the existing backup instructions instead of inventing another export workflow.

Added `start-reading-demo.cmd` for intentional double-click startup on Windows.
It selects its own project directory, checks Node/local Python availability,
calls the existing launcher with explicit synthetic opt-in and leaves actionable
errors visible. No dependency installation, automatic browser opening, reset or
source clearance occurs. Existing private items are preserved.

Added **How to use this desk / Kako koristiti stol** in the reading header,
with the complete walkthrough in English and Bosnian-Herzegovinian and a button
opening the actual practice story. It is available from home or a reading page;
opening/closing help preserves the current draft and source positions. Help
uses safe text nodes, clear headings and an accessible expanded-state control.
The guide and language switch do not write private bank items. Updated README,
the John 9 pilot and NEXT_STEPS with the new entry point.

Actual verification:

- `npm run test:reading:browser`: 1/1 passed, no skips or browser runtime errors
  (13.018 s). Extended the existing full reading journey to open help in both
  languages, follow its practice link without creating any items, retain an
  unsaved draft through help open/close and check the open guide at 460 px with
  no horizontal overflow. Existing saves, edits, cancel, source-language/wording,
  evidence lookup, scroll restoration and reopen checks still passed.
  Log: `reports/generated/reading-guide-browser-2026-11-20.txt`; report:
  `reports/generated/reading-browser-verification.json`.
- `node reports/generated/reading-windows-launcher-check.mjs`: passed. Ran the
  actual `.cmd` from a different temporary directory containing a space, reached
  HTTP 200 with synthetic reading/private writing enabled, found the practice
  source and planned John 9, and checked existing HEAD bytes were unchanged.
  Stopped only the test-owned process tree and removed its verified temporary
  directory. Report: `reports/generated/reading-guide-launcher-verification.json`.
- `node --check web/reading.js`, `node --check web/reading-i18n.mjs` and
  `git diff --check`: passed.
- `.venv/Scripts/python.exe -m ruff check src tests`,
  `.venv/Scripts/python.exe -m ruff format --check src tests` and
  `.venv/Scripts/python.exe -m jeb validate --stage schemas`: passed unchanged;
  75 formatted Python files and 62 valid schemas. A read-only documentation
  check passed across five current guide/handoff documents and 55 local links,
  including Latin-authored text and whitespace.

Python code, schemas, bank formats, source policy and historical content were not
changed in this guide increment. The earlier 439-test offline Python result is
the previous implementation check, not a new full-suite run. No source bytes were
acquired or generated, and no approval, publication, commit or push was made.
Next small task is the owner's first guided session and its first concrete
friction report; a populated real John 9 desk remains separate unfinished work.

## Working synthetic reading desk and private reading tools — 2026-11-20

Continued from the eight recorded owner preferences and John 9 pilot rather
than restarting discovery. Read PROGRESS, NEXT_STEPS, git status and repository
instructions first; preserved all existing uncommitted implementation/editorial
work. Applied the Sites skill's local implementation guidance to the existing
plain viewer. No new framework, dependency download, cloud service, publication,
source acquisition, owner approval, commit or push was introduced.

Implemented a coherent local interaction prototype: library plus prominent
search, desktop side-by-side source/explanation, expandable attributed views,
separate evidence categories with exact source navigation, explained fixture
connections and a return path retaining source scroll/open sections. The new
desk and navigation switch between English and Bosnian-Herzegovinian; source
edition wording and authored notes stay unchanged. Header actions place Add note,
Highlight selection and Suggest connection beside the reading panes. Narrow
screens stack the panes. Existing catalogue metadata remains separate from
available source text and private library downloads are not served.

All three private tools save, edit and reopen through Python. New versioned
`reading-view-v1` and `reading-item-v1` schemas ship under `src/jeb/schemas`.
`src/jeb/reading.py` stores the view and private items as explicitly typed JSON
bodies of existing private v3 articles in a dedicated synthetic bank. Exact book,
source and view revisions, Unicode code-point spans, contract hashes and expected
item revisions are checked. V3 record enums and backup schemas were not widened;
private notes/highlights/suggestions are not evidence approvals. Writer actor
metadata names a local tool, not a fictitious owner or human reviewer.

The existing bank writer gains an optional expected-HEAD check under its lock.
Retries use recorded request UUIDs across committed history, including after a
later edit or uncertain post-commit failure. Foreign bindings, stale views,
revision conflicts, invalid anchors, duplicate keys and unknown fields fail
without silently relocating notes. Old source/view bindings remain inspectable.
Reading backup/restore wraps existing complete committed bank backups and checks
reading contracts; installed-package backup/restore was also exercised.

Added bounded GET session/view and POST private-item endpoints to the existing
loopback server. A configured fixed root, synthetic flag, write flag, exact
same-origin checks and a per-server token are required for writes. Python owns
all persistence; HTTP inputs cannot select paths. Requests are limited to 16 KiB
and bounded concurrent subprocesses, with safe path-free errors. Other routes
remain read-only. Browser drafts survive language/navigation changes; unconfirmed
save requests persist in session storage for exact retry. Cancel before save
writes nothing; an uncertain commit is never presented as undone by Cancel.

`npm run reading:demo -- --synthetic` creates the isolated example only if absent
and otherwise validates/reopens it at `http://127.0.0.1:5187/#desk`, preserving
existing items and invalid directories. The launcher installs nothing and does
not auto-open a browser. Missing explicit opt-in fails. Original software scenes
are clearly synthetic/unreleasable, not scripture or a John 9 paraphrase. John 9
is an honest planned topic with no source text, exegesis, manuscript records or
independent historical corroboration supplied; a private topic note works and
highlighting is unavailable without source text. Production admitted text and
real owner approvals remain zero; five-book scope and rights gates are unchanged.

Updated README, the reading-desk direction/pilot, the bank implementation plan
and NEXT_STEPS with implemented behavior, commands, backup coverage, remaining
limits and the next small task. The full history still has the existing 128
snapshot / 128 MiB cap, with remaining saves shown; sources are limited to 20,000
characters, views to 32 passages and responses to 1 MiB. There is no history
compaction or large-corpus claim. Literal search is not an AI answer service.
Legacy editorial pages keep their original language. Observed owner usability
and a populated real John 9 study desk remain open acceptance work.

Actual offline validation in the existing locked Python 3.13 environment:

- `.venv/Scripts/python.exe -m ruff check src tests`: passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`: 75 files formatted.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`: 62 schemas passed.
- `.venv/Scripts/python.exe -m unittest tests.test_reading -v`: 10 passed; the
  corrected final test version is also included in the complete suite below.
- `.venv/Scripts/python.exe -m unittest discover -s tests -v`: 439 tests in
  370.862 s, OK with one existing Windows symlink-capability skip. Full log:
  `reports/generated/reading-desk-unittest-2026-11-20.txt`.
- `npm run test:web`: 12/12 passed (27.403 s), including real Python-backed HTTP
  saves, retries, conflicts, concurrency, body/type/origin/token checks and
  unchanged legacy viewer/library checks.
- `npm run test:reading:browser`: final local Edge run passed, 1/1, zero skips,
  zero runtime errors (11.242 s). It exercised actual DOM source selection, all
  three private tools, safe literal rendering, note editing without capturing an
  unrelated selection, evidence location, language/draft/source preservation,
  cancel without saving, related-story return with scroll 55 restored, reopening
  all three saved items and a 460 px viewport without horizontal overflow.
  Log: `reports/generated/reading-browser-final-2026-11-20.txt`; machine report:
  `reports/generated/reading-browser-verification.json`; local QA screenshot:
  `reports/generated/reading-desk-desktop.png`. No shared browser preview or
  hosting was used; temporary browser/test banks were cleaned up.
- `.venv/Scripts/python.exe -m pip check`: passed; JavaScript syntax checks passed.
- `.venv/Scripts/python.exe -m jeb sources audit`: admitted_count 0; two
  needs_review candidates and one excluded candidate; no source status changed.

Built and checked the installable package without downloading dependencies:

```text
.venv/Scripts/python.exe -m pip wheel --no-index --no-build-isolation --no-deps --wheel-dir dist/reading-desk-package .
.venv/Scripts/python.exe -m pip install --no-index --no-deps --target dist/reading-desk-installed dist/reading-desk-package/jugoslavenska_ekumenska_biblija-0.1.0.dev0-py3-none-any.whl
.venv/Scripts/python.exe -I -B reports/generated/reading-wheel-check.py
node reports/generated/reading-launcher-check.mjs
```

Installed-wheel imports came from the target package, including all 62 schema
resources. All three item kinds, retry idempotence, identical restored reading
state and isolated CLI/function parity passed from outside the repository.
Wheel SHA-256: `0d93be0b66333c6dcaa8515b34fca1731f6c7b9bd144a3887302db71063a29e2`.
Report: `reports/generated/reading-wheel-verification-2026-11-20.json`.
The launcher check confirmed explicit opt-in, HTTP 200, writable synthetic state,
three entries and byte-identical existing HEAD when reopened; it stopped its
owned server. Report: `reports/generated/reading-launcher-verification.json`.
The editable development environment and earlier distribution artifacts remain
intact. No development server is intentionally left running.

Final checks after the last UI/documentation edits: `git diff --check` passed;
Ruff check/format and all 62 schemas passed again. A read-only Python check
verified Latin-authored text, whitespace and 64 local links across six current
handoff/product documents, and exact source-byte parity for all 108 packaged
wheel files. Final git status retains the pre-existing dirty/untracked work.

Next small task: observe the owner using the synthetic reading journey and fix
the first concrete navigation/label/save problem. Separately prepare bounded
exact-edition/source research for real John 9 content under existing gates; do
not manufacture study content or call automated checks an owner usability pass.

## John 9 usability pilot and recorded owner preferences — 2026-11-19

Read current PROGRESS/NEXT_STEPS/git status, product brief and bank/source
boundaries. Preserved all existing uncommitted implementation and editorial
work. The owner answered the five discovery questions and three follow-ups:
library plus prominent search equally; side-by-side text/explanation with
expandable evidence/connections; short clear account then attributed views;
John 9 as the concrete scenario; private notes/highlights/suggested connections
in the first usable version; desktop/laptop first; switchable English and
Bosnian/Herzegovinian; and both textual witnesses and independent historical
evidence where available. These are actual product preferences, not source
clearance, theological decisions, text approval or generated attestations.

Added `docs/JOHN_9_READING_DESK_PILOT.md` with the requested journey: meaning and
religious blindness, related blindness stories, Jesus as a character, Pharisees
in historical context, symbolism and evidence for the selected story. It records
the requested research destinations without supplying exegesis, verse wording,
parallel-passage claims, manuscript identities or historical corroboration from
model memory. No content research/acquisition was performed in this planning
slice. John 9 stays within JHN and adds no book or admitted source.

The plan separates textual transmission, event-level historical evidence,
background context and interpretation. Exact preserved passage coverage and
attribution are required for future witness records; a fragment preserving text
must not be displayed as independent event corroboration. Empty states describe
unverified content in this collection rather than claim evidence cannot exist.

Updated READING_DESK_PRODUCT_DIRECTION to record all eight answers and complete
core U0 discovery. U1 now explicitly includes save/reopen of all three private
reading tools: a read-only increment is not the completed selected first version.
The small versioned reading-view/private-tools contract must reuse Python
validation/writing, preserve exact source anchors, handle conflicts/cancel/
recovery and declare backup coverage without silently widening v3 schemas.
Language switching must preserve location, personal wording and the exact source
edition. Full explanation editing/authoritative curation remains later backlog.

Aligned README, NEXT_STEPS, KNOWLEDGE_BANK_IMPLEMENTATION_PLAN,
HISTORICAL_TEXTS_PIPELINE and BANK_CATHOLIC_BIBLE_PILOT. The next implementation
task is the minimum reading-view/private-tools contract and a small connected
viewer slice, using original synthetic fixtures while separately addressing
real John 9 source/content readiness. Do not restart the same eight preference
questions, resume infrastructure-first work or mislabel a synthetic interaction
demo as a populated real John 9 study desk.

This continuation changes documentation/plans only. No application/schema/source
policy changes, real review records, publication, commit or push were made.
Actual checks: `git diff --check` passed; a read-only Python documentation check
passed across seven product/continuation documents and 66 local links, including
Latin-authored text, whitespace, protected literals and recorded-answer state.
No full application test rerun is claimed for this documentation-only change.

## Reading-desk usability direction and discovery questions — 2026-11-19

The owner explicitly prioritized usability: one clear place to explore books,
context, evidence, explanations, characters, related stories and supporting
literature, using the analogy of a medieval scribe's main text and reference
library. The owner asked for questions and documentation/plan changes. Read
current PROGRESS/NEXT_STEPS/git status and the existing bank, pilot, historical,
viewer and usefulness documents before editing. Preserved uncommitted work.

Added `docs/READING_DESK_PRODUCT_DIRECTION.md`, preserving the owner's actual
wording and distinguishing confirmed direction from proposed interaction rules,
open questions and unimplemented milestones. Asked five questions through the
conversation: entry point, reading layout, disagreement presentation, a concrete
reading session and personal notes/highlights/editing in the first version.
Answers are pending; no suggested option is recorded as an owner decision.

The current plan now prioritizes one book/passage → explanation → exact evidence
→ meaningful story/character connection → return journey. Its dependent layout
and editing behavior remain open until the owner answers. Proposed acceptance
checks emphasize clear attribution, understandable connection reasons, retained
reading location and completing the scenario without terminal/JSON/hash copying.
Underlying source/record validation remains in Python. The previous CLI candidate
context task moves to supporting backlog rather than remaining the default next
product milestone.

Aligned README, NEXT_STEPS, KNOWLEDGE_BANK_IMPLEMENTATION_PLAN,
HISTORICAL_TEXTS_PIPELINE and BANK_CATHOLIC_BIBLE_PILOT with that priority. Replaced
the obsolete immediate F0/F1 task in the architecture plan with the current
discovery/reading-slice sequence, preserving the older technical backlog.
Kept actual capabilities separate from desired ones. No new interface, record,
schema, source access, source clearance or formal owner approval was created.
The five-book corpus, personal-library boundary, protected literal forms and
existing editorial/rights decisions remain unchanged. No publication or push.

This is documentation and discovery only; no application tests were rerun.
Documentation link/Latin/whitespace checks and `git diff --check` are recorded
below after validation.

Validation passed: `git diff --check` exited 0. A read-only local Python check
verified six touched product/continuation documents, 52 existing local links,
Latin-authored documentation, whitespace, the four protected literals and the
explicit pending-answer state. No code/schema tests were needed for these
documentation-only changes.

## Current usefulness assessment — 2026-11-19

Read current PROGRESS/NEXT_STEPS/git status and inspected README, bank/history/
backup/search contracts, historical processing documentation, library metadata
and retained verification evidence. Added
`docs/PROJECT_USEFULNESS_REPORT_2026-11-19.md`, separating immediately usable
catalogue/personal-bank features, synthetic engineering demonstrations and the
unimplemented real-text knowledge-base experience. It documents practical use
cases, manual handoffs, preservation/scale limits and a recommendation for one
small owner-written/permitted-content pilot. This report is an engineering
assessment, not a user study, source clearance or a completion score.

Fresh read-only commands:

```text
.\.venv\Scripts\python.exe -m jeb sources audit
.\.venv\Scripts\python.exe -m jeb bank validate --bank-root dist/bank-v3-synthetic-demo
.\.venv\Scripts\python.exe -m jeb --synthetic historical status --workspace dist/historical-projection-synthetic-2026-11-19/pipeline
```

Actual results: 0 admitted sources; four valid synthetic bank records and one
bound body; coherent synthetic historical snapshot with five candidate spans,
no pending artifacts and releasable=false. Read-only Python metadata inspection
confirmed 291 catalogue items, 153 findings covering 138 item IDs, five private
download receipts and all five referenced paths present. Private source contents
and their hashes were not re-audited for this report. Latest test evidence remains
the preceding actual run: 429 Python tests (one skip), nine Node tests and 60
schemas; no full test rerun is claimed for this documentation-only task.

No application/schema/source-policy changes, record creation, publication,
commit or push. The existing next small coding task in NEXT_STEPS is preserved;
the report adds a product-level evaluation recommendation rather than starting
another implementation. Documentation whitespace/Latin and git diff checks are
recorded after completion below.

Report checks passed: `git diff --check` exited 0; a local Python check verified
Latin-authored text, no trailing whitespace and all 15 report links resolving
to existing local files. No code tests were needed for this documentation-only
assessment.

## Retained synthetic PDF projections and exact-span verification — 2026-11-19

Read PROGRESS, NEXT_STEPS, AGENTS and git status before continuing. Preserved
the preceding uncommitted implementation, research and policy work. Implemented
the selected next slice: durable bounded PDF text projections in the isolated
synthetic historical workspace. No real source, book, rights or owner decision
was added or changed.

New managed PDF extractions use the packaged `historical-extraction-v2` schema.
It explicitly fixes synthetic=true/releasable=false and binds projection hash
and byte length. Exact UTF-8 bytes are retained atomically at
`projections/<sha256>.txt` before cache/checkpoint/HEAD publication. Existing
different bytes at the same path fail closed. Each read validates the cache
schema/hash, projection reference/hash/size/strict UTF-8, and every candidate's
literal Unicode code-point slice. Shared blobs are deduplicated. Bounds are
16 MiB per projection and 128 MiB unique referenced projection bytes per
snapshot, additional to the existing layer bounds.

Workspace write failures propagate instead of being misreported as source-read
failures: the processing checkpoint can resume and the previous HEAD remains
readable. No reader repairs missing/corrupt evidence or reruns extraction.
The selected PDF executable is pinned for the call and its hash checked before
and after extraction. PDF candidate IDs also bind the projection hash; plain
text IDs retain their previous form. Source text and protected literals are
not normalized or rewritten.

Existing v1 extraction/checkpoint/snapshot schemas are byte-identical to the
previous installed engine. V1 caches remain readable and unmodified, with
explicit projection_retained=false/locator_verification=not_retained. Only an
explicit new extraction/refresh creates a new v2 cache; it never backfills the
lost bytes of a historical v1 projection. Query provenance now carries the exact
extraction cache hash and retained/span-verification state.

The new read-only command is:

```text
python -m jeb --synthetic historical projection-verify --workspace <workspace> --cache-sha256 <exact-cache-hash>
```

It validates current or old retained extraction evidence using only the cache
and retained projection, without opening the current source or invoking a PDF
tool. It reports hashes, byte length and verified candidate count, not full
projection text. V1 returns projection_not_retained and exit 2. No HTTP route,
frontend, source admission or human decision workflow was added. README and the
pipeline guide document retention, compatibility, limits and usage; NEXT_STEPS
now points to small read-only candidate/context inspection by exact identities.

Actual commands and results in the existing locked CPython 3.13.3 environment:

```text
.\.venv\Scripts\python.exe -m unittest tests.test_historical_projection -v
.\.venv\Scripts\python.exe -m unittest tests.test_historical tests.test_historical_projection -v
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m ruff format --check src tests
.\.venv\Scripts\python.exe -m jeb validate --stage schemas
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
npm run test:web
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

Results: **10 new projection tests passed in 6.727 seconds; all 34 historical
tests passed in 42.403 seconds; 73 Python files formatted; 60 schemas valid;
429 full-suite tests completed in 304.137 seconds, OK (skipped=1); all 9 Node
tests passed in 24.592 seconds**. The only skip remains the existing Windows
symlink-creation test. The new optional real PDF test actually ran and passed
with the already installed local MiKTeX pdftotext; no PDF library/tool/dependency
was installed or downloaded. Ruff, dependency consistency, diff and manual
new-file whitespace/Latin-guide checks passed. Full actual output is retained
at `reports/generated/historical-projection-unittest-2026-11-19.txt`.

Tests cover exact CRLF/decomposed-Unicode bytes, literal spans, deleted inputs,
changed input/tool output, unchanged prior cache/snapshot bytes, v1 no-backfill,
wrong hash/size/UTF-8/span, missing/corrupt blobs, junction guards, write-failure
recovery, deduplication, snapshot byte budget and unchanged real-source gate.
The real PDF fixture is built entirely from original software-test sentences
with a standard-library byte writer; its independently captured local-tool
output is byte-identical to the retained projection. No historical text is used.

Additional actual verification commands:

```text
.\.venv\Scripts\python.exe -B reports/generated/historical-projection-smoke.py
.\.venv\Scripts\python.exe -m pip wheel --no-index --no-build-isolation --no-deps --wheel-dir dist/historical-projection-package .
.\.venv\Scripts\python.exe -m pip install --no-index --no-deps --target dist/historical-projection-installed dist/historical-projection-package/jugoslavenska_ekumenska_biblija-0.1.0.dev0-py3-none-any.whl
.\.venv\Scripts\python.exe -I -B reports/generated/historical-projection-wheel-check.py
```

The smoke recorder executed 8 real CLI calls against a new labelled original
fixture at `dist/historical-projection-synthetic-2026-11-19/pipeline`. It retained
a 76-byte exact projection with five proposed candidates, changed the input,
refreshed into a new extraction, then moved the input out of the configured
path. With subprocess PATH empty, both old and new caches verified and the
dossier still resolved the current exact Luma locator. All 23 workspace files
were byte-identical before/after these reads; prior immutable cache/projection/
snapshot bytes were also preserved. The two generated original PDF inputs were
retained separately as private synthetic smoke artifacts, not historical data.
Full commands/outcomes:
`reports/generated/historical-projection-smoke-2026-11-19.json`.

Original cache hash:
`147e4b9aab68bc62d9d403a2bf965a4697a125eab4985a3db93f239a5d9969e2`.
Original projection hash:
`7ff507125eac3709f133a26f2c1b423f1d232b73e280e5769ab6c65662af8e00`.

The new wheel was built offline and installed only into the new isolated target;
the existing venv and preceding wheel/installed verification were preserved.
Python -I loaded the actual target package, checked matching current modules
and all 60 packaged schemas, verified both retained caches through CLI/function
parity with no tools on PATH, and read the preceding v1 text-demo workspace
without migration. This uses existing locked-venv dependencies, not a fresh
dependency installation or a Linux test. Results:
`reports/generated/historical-projection-wheel-2026-11-19.json`.
Wheel SHA-256:
`f951b46718bd5ef6bc55128b654811bd7f292665f24c4a9d9bd35641dce92ff1`.

Remaining limits: retention applies only to new managed synthetic PDF tasks;
original source PDF bytes, legacy projections, fonts/page alignment and OCR
evidence are not archived by the pipeline. Standalone entity-index stays
hash-only. Per-snapshot byte bounds do not impose a full-history disk quota;
there is no pruning or full pipeline backup/restore. Retained-span validation
does not prove historical fidelity, entity identity or human/legal approval.
Real-source extraction still stops at source_review_required before opening
source bytes. No real acquisition, model API, external contact, paid service,
commit, push, release, publication or owner approval occurred.

## Incremental historical pipeline completed and verified — 2026-11-19

Resumed the interrupted local implementation after reading PROGRESS,
NEXT_STEPS, AGENTS and git status. Preserved the existing uncommitted bank,
library, source-research, config and policy changes. This continuation did not
change source registry/lock, rights policy, editorial decisions or book scope.

The completed slice provides `historical pipeline init/step/status`, an explicit
original synthetic demo and shared read-only `status/dossiers/detail/lookup/
relations/dossier` queries. A writer lock, per-artifact atomic checkpoints,
hash-addressed extraction caches and immutable four-layer snapshots allow
bounded batches, interruption recovery, pending retries, refresh rotation and
recovery after a failed HEAD publication. The last complete snapshot remains
readable while later work is pending. Input registry changes require a new
workspace; existing destinations are not adopted or overwritten.

Extraction retains exact Unicode code-point offsets, CRLF bytes, surface forms,
source/projection hashes, adapter identity, editions and translator credits.
Capitalized Latin tokens remain unknown proposed candidates; normalized groups
are same-surface proposals, not identities. Real extraction now explicitly
returns `needs_review/source_review_required` before source bytes are opened.
The earlier 18,230-candidate private research run is historical evidence, not
admitted content, current cleared coverage or input to this synthetic demo.

Node uses a bounded Python CLI bridge instead of maintaining separate hashing
and semantic checks. HTTP tests exercise nonempty input, exact CLI/API parity,
work-specific locator counts, malformed/stale configured layers, query errors,
synthetic opt-in and runtime failure without hiding unrelated viewer data.
GET queries leave checkpoint/HEAD bytes unchanged. The existing small viewer
now has search/filter pagination, an explicit combined dossier and status
refresh; it stays loopback, opt-in and read-only. No approval/merge/write action
or large frontend was added.

Further fixes in the resumed work:

- Pin query data and accompanying status/counts to one HEAD, including a test
  where a writer publishes between the read and response construction.
- Apply combined dossier offsets to works as well as entities/relations; apply
  work/availability filters to the same artifact, including detail responses.
- Reject malformed HEAD JSON types and foreign/conflicting pending artifacts.
- Return `response_limit_exceeded` for oversized serialized responses instead
  of dropping rows that pagination would then silently skip.
- Give PDF output reading and process completion one shared timeout deadline.
- Load the viewer's initial list with its actual 50-row page size and retain
  the synthetic label when opening an individual dossier.

Actual offline checks used the existing hash-locked environment, CPython 3.13.3
and Node v24.11.1. No dependency download or environment upgrade was performed:

```text
.\.venv\Scripts\python.exe -m unittest tests.test_historical -v
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m ruff format --check src tests
.\.venv\Scripts\python.exe -m jeb validate --stage schemas
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
npm run test:web
node --check web/app.js
node --check web/server.mjs
node --check web/historical.mjs
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

Results: **24 targeted historical tests passed; 72 Python files formatted;
59 schemas valid; 419 full-suite tests completed in 256.042 seconds,
OK (skipped=1); all 9 Node tests passed in 18.936 seconds**. The one expected
skip is `test_links_rejected_when_available`: this Windows environment does
not permit symlink creation. Ruff, syntax, dependency consistency and diff
checks passed. Full actual unittest output is retained at
`reports/generated/historical-pipeline-unittest-2026-11-19.txt`.

The following additional verification/build commands actually ran:

```text
.\.venv\Scripts\python.exe -B reports/generated/historical-pipeline-smoke.py
.\.venv\Scripts\python.exe -m pip wheel --no-index --no-build-isolation --no-deps --wheel-dir dist/historical-pipeline-package .
.\.venv\Scripts\python.exe -m pip install --no-index --no-deps --target dist/historical-pipeline-installed dist/historical-pipeline-package/jugoslavenska_ekumenska_biblija-0.1.0.dev0-py3-none-any.whl
.\.venv\Scripts\python.exe -I -B reports/generated/historical-pipeline-wheel-check.py
```

The smoke recorder verified 16 real CLI calls, retaining commands and outcomes
in `reports/generated/historical-pipeline-smoke-2026-11-19.json`. Its new
`dist/historical-synthetic-verified-2026-11-19/pipeline` workspace has three
complete artifacts, one deliberately missing file and one invalid UTF-8 file.
The invented label Luma has four exact locators: three across two MAT editions
and one in MRK. The query retains all three original synthetic contributor
credits. It verified all 37 pipeline files byte-for-byte unchanged by read-only
queries and failed non-opt-in/no-clobber attempts. A separate workspace completed
five one-artifact steps, retried two blocked tasks and reused all three unchanged
UTF-8 caches on refresh. No historical source content was used.

The wheel built offline and installed only into the new isolated target above;
the existing venv installation was not replaced. Python `-I` imported the actual
target package, found all four new modules and all 59 packaged schemas, and
confirmed installed CLI/function parity on a temporary nonempty synthetic demo,
plus invalid-query exit 2. Dependencies came from the existing locked venv;
this was not a clean dependency-install or Linux test. Results:
`reports/generated/historical-pipeline-wheel-2026-11-19.json`.
Wheel SHA-256:
`4549b7ad6d5288c9a5810c15c38d994257e467bd4fcb89cbdc38ce73264e3d55`.

README and `docs/HISTORICAL_TEXTS_PIPELINE.md` now document runnable commands,
no-clobber behavior, retry/refresh, limits, status semantics, exact offset units,
CLI/API error codes, viewer opt-in and honest source gates. `ready` means readable
coherent layers, not a completed queue or human/legal approval.

Limits remain: heuristic unknown candidates; no HTML/OCR adapter, human identity
review, real-source admission, bank promotion, snapshot pruning or full pipeline
backup/restore. PDF projections have hashes but are not retained, so hashes
alone do not archive old projection text. The time budget checks work admission
and PDF subprocess timeout; in-process processing/validation/publication may run
longer. Tests stub the PDF adapter and do not claim a real PDF/tool round-trip.
Next small task: preserve and validate an exact bounded synthetic PDF projection
with an original fixture, before using such locators for durable evidence.

No source acquisition, model/paid API, contact, owner approval, commit, push,
publication or release occurred. GEN/MAT/MRK/LUK/JHN, protected literal forms,
Latin-authored displays and zero admitted real scripture coverage remain intact.

## Synthetic CLI/API parity fixture — 2026-11-19

Added an end-to-end temporary four-layer historical fixture with matching
registry/index/groups/dossiers hashes. The same fixture is inspected through
`jeb historical status` and `/api/historical/status`; both must return the
same `ready` status, counts and blocker list. The fixture is removed after the
test and never touches real sources.

Actual checks: 8 Node viewer tests passed, including parity, Node syntax checks
passed and `git diff --check` passed.

## CLI/API status parity — 2026-11-19

Aligned the read-only CLI and viewer API status envelopes around the same
`configured`, `counts`, `blockers` and `status` fields. Unconfigured layers
use the shared `path_not_configured` blocker category, while malformed JSON is
reported as `invalid_json`; neither interface starts processing or writes data.

Actual checks: 9 CLI tests passed, 7 Node viewer tests passed, Ruff, format,
Node syntax checks and `git diff --check` passed.

## Read-only historical CLI inspection — 2026-11-19

Added `jeb historical status` with optional registry/index/groups/dossiers
paths. It prints the same pipeline counts and blockers without starting a
server or writing output; unconfigured layers are reported as blockers and
malformed files remain machine-readable errors at the API boundary.

Actual checks: 9 CLI tests passed, 7 Node viewer tests passed, Ruff, format,
Node syntax checks and `git diff --check` passed.

## Historical API error and limit contracts — 2026-11-19

Added machine-readable `invalid_historical_input` responses with HTTP 422 for
malformed configured historical JSON, including only the affected logical
layer and no filesystem path. Contract tests also verify bounded lookup and
relation result limits; the API remains read-only.

Actual checks: 7 Node viewer tests passed, Node syntax checks passed and
`git diff --check` passed.

## Downstream contract and stale-input guard — 2026-11-19

Added canonical hash binding checks to `build-dossier` when registry, index,
groups and dossiers are all configured. A mixed or stale set returns
`stale_pipeline_inputs` with mismatch details and no combined data. A contract
test covers the fail-closed path with intentionally wrong hashes.

Actual checks: 7 Node viewer tests passed, Node syntax checks passed and
`git diff --check` passed.

## Combined build-dossier response — 2026-11-19

Added read-only `/api/historical/build-dossier`, combining matching entity
dossier summaries with work-scoped relation proposals. It preserves layer
boundaries, reports unavailable layers, and marks the complete response
`proposal_only: true` and `authoritative: false`.

Actual checks: 7 Node viewer tests passed, Node syntax checks passed and
`git diff --check` passed.

## Relation-proposal lookup — 2026-11-19

Added read-only `/api/historical/relations` over the explicitly configured
registry. It filters by relation type, work, status or query and returns
bounded relation summaries with endpoint labels and evidence counts. Every
response carries `authoritative: false`; no similarity, parallel or same-as
proposal becomes a fact.

Actual checks: 7 Node viewer tests passed, Node syntax checks passed and
`git diff --check` passed.

## Bounded work/topic lookup — 2026-11-19

Added read-only `/api/historical/lookup`, which groups matching dossier
proposals by work for bounded downstream use. It accepts a topic query and/or
work filter and returns dossier IDs plus candidate/locator counts; it never
creates aliases, identity merges or claims.

Actual checks: 7 Node viewer tests passed, Node syntax checks passed and
`git diff --check` passed.

## Historical pipeline status summary — 2026-11-19

Added read-only `/api/historical/status` and workspace status data. When the
four explicit historical paths are configured, the viewer reports counts for
registry works/editions/artifacts/relations, index candidates/pending, groups
and dossiers. Missing or unreadable phases are reported by name; no pipeline
step is started and no file is written. The UI shows the available counts while
keeping all items proposed and unreleasable.

Actual checks: 7 Node viewer tests passed, Node syntax checks passed and
`git diff --check` passed.

## Read-only historical dossier viewer — 2026-11-18

Connected the opt-in entity dossier file to the local viewer through
`JEB_HISTORICAL_DOSSIERS`. The new read-only API exposes bounded summaries,
search, status/availability/work filters and a detail view with exact
projection-labelled locators. The UI explicitly labels results as proposed;
there are no approval, merge or release actions. With no environment variable,
the historical view stays disabled.

Actual checks: 7 Node viewer tests passed, Node syntax checks passed and
`git diff --check` passed. The test dossier was temporary and removed.
The repository offline suite also passed: 56 schemas, Ruff, format and 394
unittest tests passed with 1 expected symlink skip.

## Entity dossier layer — 2026-11-18

Added `jeb historical entity-dossiers`, which joins conservative surface groups
to registry work/edition/artifact metadata and exact candidate locators. It
returns dossier proposals only; it does not assert that a group is one person,
place or literary character. The current pipeline produced 3,594 dossier
proposals from 18,230 candidate spans, retaining source artifact, work, edition,
projection, start/end and exact surface fields without copying full text.

Actual checks:56 schemas, Ruff, format, CLI tests and `git diff --check` passed.
Temporary registry/index/group/dossier artifacts were removed after the run.

## Conservative entity grouping — 2026-11-18

Added `jeb historical entity-groups`. It groups only exact surface forms after
NFC, whitespace collapse and casefold; it does not strip diacritics, transliterate,
infer inflections or merge identities. Groups remain
`proposed_same_surface` with candidate and artifact IDs.

The first 18,230-candidate run produced 3,594 conservative groups. The initial
8 MiB generic JSON reader correctly rejected the large index; entity grouping now
uses its own explicit 64 MiB bound rather than weakening general file limits.
The retry succeeded; temporary registry/index/group files were removed.

Checks:55 schemas, Ruff, format, 8 CLI tests and `git diff --check` passed.

## Bounded PDF projection for entity candidates — 2026-11-18

Extended `historical entity-index` with a local `pdftotext` projection for
private PDF artifacts. The projection is temporary and its offsets are labelled
`pdftotext_utf8`; full extracted text is not written to the registry or tracked
workspace. Plain text/Markdown still use `source_utf8`. Unsupported/missing
artifacts remain pending.

Current catalog run: 18,230 unknown entity candidates from 4 local PDFs and
149 pending artifacts. All candidates remain `proposed`/`entity_type: unknown`;
there is no person/place merge, semantic claim or rights clearance.

Checks:53 schema validation, Ruff, format, 8 CLI tests and `git diff --check`
passed.

## Read-only entity candidate index — 2026-11-18

Added `jeb historical entity-index`, which walks registry artifacts without
downloading or modifying them. It extracts only bounded, exact-offset candidate
spans from local UTF-8 `.txt`/`.md` artifacts; unsupported, missing and
metadata-only artifacts remain explicitly `pending`. Candidates are unknown,
proposed entities, never silently classified as people or places.

Current catalog run: `0 candidates`, `153 pending_artifacts`,
`proposals_only:true`. This is expected because the current private artifacts
are mostly PDF/HTML or metadata-only and no text parser was assumed. Schemas,
CLI tests, Ruff and diff checks pass.

## Read-only historical registry builder — 2026-11-18

Added `jeb historical registry-build --input library/catalog.json --output ...`.
It deterministically converts the existing personal-library metadata into a
separate registry of works, edition records, discovered artifacts and
metadata-backed `version_of` relation proposals. It does not download text,
promote rights, merge characters, or admit a source into the biblical corpus.

Actual result on the current catalog:
- 291 works,153 editions,153 artifacts,153 relation proposals;
  `metadata_only:true`.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`:53 schemas passed.
- `.venv/Scripts/python.exe -m ruff check src tests`:passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`:68 files passed.
- `tests.test_cli`:8 tests passed.
- `git diff --check`:passed.

Next small task: add a read-only entity extraction/index contract for available
text artifacts, keeping character/place matches as proposals with evidence.

## Historical-texts pipeline foundation — 2026-11-18

Started the actual product direction: a local registry and pipeline for works,
editions, digital artifacts and proposed cross-world relations. Added four
versioned schemas for `work`, `edition`, `artifact` and `relation`, plus
`docs/HISTORICAL_TEXTS_PIPELINE.md`. This is registry metadata and proposal
structure only; it does not ingest historical text, clear rights, merge people
or admit new biblical books. V3 remains the provenance/evidence layer.

Actual checks are pending in this entry; the next command is schema validation
and the offline CLI regression after updating the packaged-schema count.

## JHN 1:1–5 exact-volume lead — 2026-11-18

The follow-up search found a stronger Katančić lead: a scholarly Hrcak record
identifies *Sveto pismo Novog' zakona*, volume I, Budim 1831, as the Gospel
volume and includes JHN 1:1–5 as a textual example. Wikimedia also exposes a
title-page image for the 1831 New Testament. This is still metadata/secondary
evidence, not an inspected source leaf: no biblical text was copied, no scan
checksum or page identity was established, and no rights clearance or corpus
admission was created.

Next small source task: locate and inspect the actual JHN 1:1–5 scan leaf in
Katančić New Testament volume I, retaining the original page image and exact
edition metadata before any transcription.

## JHN 1:1–5 source-candidate research — 2026-11-18

For the user-selected topic Isus Krist and pilot passage JHN 1:1–5, recorded a
metadata-only candidate review in
`docs/sources/JHN_1_1_5_CANDIDATE_RESEARCH_2026-11-18.md`. Candidates are
Škarić 1858–1861, Katančić/Čevapović 1831 and Šarić 1941–1942. No biblical text
was fetched or transcribed, no source was admitted or cleared, and the user
provided `jēšūaʿ minnåzrat` remains an unreviewed separate note. The next small
source task is to locate one exact JHN 1:1–5 scan leaf and record its edition,
page, digital revision and rights evidence before any text entry.

## Meditations topic dossier — 2026-11-18

Added `docs/TOPIC_MEDITATIONS_MARKO_AURELIJE.md` as an unreviewed, source-first
topic draft. It separates Marcus Aurelius, the work, editions/translations,
secondary interpretation and future educational outputs. It contains links and
rights caveats only; no historical source bytes, copied translation or legal
clearance was added.

The dossier deliberately remains outside the five-book Biblical corpus scope.

Created and imported the first five-entry metadata-only candidate batch for
Meditations. The CLI returned `candidates: 5`, `review_state: unreviewed`,
`corpus_permission: false` and `source_clearance_changed: false`; no content was
downloaded.

Completed the first source review pass in
`docs/RESEARCH_REVIEW_MEDITATIONS_2026-11-18.md`. It confirms provider claims
and separates them from jurisdictional clearance, exact-artifact identity and
website/UI rights. No candidate was promoted and `content_acquired` remains
false.

Added `docs/RIGHTS_MATRIX_MEDITATIONS.md`, which records the current
artifact-by-jurisdiction blockers. All five rows remain link-only for now;
this is a deliberate evidence gap, not a preference to avoid storing files.

Detailed review located Gutenberg's exact 15877 text URLs and indexed size, but
the artifact remains link-only because the configured DE/HR rights gate and
human source review are not complete. No bytes were fetched and no hash was
invented.

Owner decision applied: configured jurisdiction is now `DE` only and the GitHub
working repository is private. Public distribution remains a separate future
release scope and is not implied by this change.

Revalidated and re-imported the Meditations candidate batch with `jurisdictions:
[DE]`. The new immutable batch is
`data/source-candidates/meditations-initial/7730cbf0bf6c97fddf5fbed98a33f762eaa588e982bc016703fca827611ce7e5.json`;
the earlier multi-jurisdiction batch remains preserved as historical metadata.

## Synthetic v3 workflow end-to-end — 2026-11-18

Created the isolated `dist/bank-v3-synthetic-demo` managed3.0 bank using the
existing v3 API. It contains one synthetic entity, source, claim and evidence
record with real generated revision/raw-record/body references and an exact
text-span locator. All records are private, unreviewed, synthetic and marked
unreleasable by the workflow; no historical or project source was used.

The local viewer was started on loopback port5188 with `JEB_BANK_ROOT` bound to
that bank. API verification found schema3.0,4 records, the claim search result,
one evidence link and one history entry. A backup written to a temporary
directory verified successfully; restore returned4 records and an identical
evidence-link result. The temporary directory and archive were removed by the
temporary-directory cleanup. The viewer process was stopped afterward.

Actual result:
- `valid_records:4`, `backup_valid:true`, `restored_records:4`,
  `restored_links_equal:true`, `approvals_created:0`, `releasable:false`.

## Untrusted source-candidate intake — 2026-11-18

Added `source-candidate-batch` and `jeb sources candidates validate/import` as
the missing boundary between internet/search work and the historical source
registry. It records query, jurisdictions, URL/provider metadata, access date,
rights state and limitations, but rejects acquired content, credentialed or
non-HTTPS URLs. Imported batches are hash-addressed, unreviewed, and cannot
change source clearance, registry, locks or corpus permission. Actual download
still requires the existing exact-edition allowlist and `fetch` gate.

Actual checks:
- `.venv/Scripts/python.exe -m unittest tests.test_source_candidates tests.test_cli -v`:10 tests passed.
- `.venv/Scripts/python.exe -m ruff check src tests`:passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`:67 files passed.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`:48 schemas valid.
- `git diff --check`:passed.

Limitation remains intentional: this repository does not contain a web search
or model/cloud adapter. A browser/search export can feed this candidate inbox;
only a separately reviewed source assessment can promote a candidate.

## Catholic Bible pilot scope — 2026-11-18

Added `docs/BANK_CATHOLIC_BIBLE_PILOT.md` to turn the user's first topic into a
safe working frame. It defines the five currently allowed pilot books GEN/MAT/
MRK/LUK/JHN, a book→source→character→claim→evidence workflow, and explicit
`pending_owner_scope_decision` handling for books outside that scope. No
biblical text, real source clearance, character fact or approval was invented.

Next small task: create the first private entity/source record only after the
owner supplies the exact edition/source to use.

## v3 record-type filter — 2026-11-18

Added a small read-only filter to the Baza znanja page so current records can
be narrowed by entity, source, article, claim or evidence while retaining the
existing bounded bank search endpoint. No new route, write operation, approval
state or source content was introduced.

Actual checks:
- `npm run test:web`:6 tests passed.
- `node --check web/app.js`:passed.
- `git diff --check`:passed.

## Quickstart end-to-end smoke — 2026-11-18

Ran the documented temporary workflow exactly: managed3.0 init, entity create,
bank search, validate, backup and backup-verify. The synthetic private fixture
returned one exact `Aleksandar` result, one valid current record, two snapshots,
and a valid private backup. The temporary directory was removed afterward.

No repository, production bank, source, approval or publication was changed.

## Bank quickstart — 2026-11-18

Added `docs/BANK_QUICKSTART.md`, a short operational path from private bank
initialization through create, search, validate, read-only viewer and backup.
It keeps Python CLI as the write boundary, labels the viewer read-only, preserves
source/rights cautions, and explains entity/source/claim/evidence roles without
adding new code or data.

Actual checks:
- `git diff --check`:passed.
- No configuration, source corpus, approval, publication or external service
  changes.

Next small task: use the quickstart with the owner's first private topic and
only repair a concrete usability problem.

## v3 viewer documentation — 2026-11-18

Updated README to document typed relationship navigation and bounded revision
history, and corrected the earlier wording that described the bank UI as wholly
future work. Editing, assessment and selected-content export remain future
work; the current viewer remains opt-in and read-only.

Actual check: `git diff --check`:passed.

## Real local viewer smoke — 2026-11-18

Created a temporary private bank through the Python storage API, started the
loopback Node viewer with `JEB_BANK_ROOT`, and queried `/api/bank/search` for a
record. The viewer reported `enabled:true`, one exact result titled
`Aleksandar probni zapis`, matching `title`. The temporary fixture was removed
after the check; no repository or production bank was touched.

Next small task: stop adding interface until a concrete usability issue appears.

## Full offline regression after v3 viewer work — 2026-11-18

Ran the repository's complete offline unittest suite after the read-only v3
history and relationship-navigation changes. The bank, schema, backup/restore,
migration simulation, source gates, editorial workflows, narrative workflows
and terminal workbench all remained green.

Actual result:
- `.venv/Scripts/python.exe -m unittest discover -s tests -v`:392 tests passed,
  1 skipped because Windows did not permit the existing real-symlink privilege
  test; the mocked link guards passed.

## Viewer search opens exact bank records — 2026-11-18

Connected the read-only viewer search to `/api/bank/search`. Queries now scan
current bank title, kind, processing state, structured data and body, return
matching fields, and preserve exact record IDs for opening the bounded detail
view. Requests are sequenced so an older slow response cannot replace a newer
query. No write, approval, export or public route was added.

Actual checks:
- `npm run test:web`:6 tests passed, including bank search and exact record
  response.
- `node --check web/app.js; node --check web/server.mjs`:passed.
- `git diff --check`:passed.

Next small task: keep the viewer read-only and use it with a real local bank
fixture before adding more interface.

## Read-only bank search — 2026-11-18

Added `jeb bank search --bank-root ... --query ...` for the daily workflow. It
reads only the current validated committed HEAD, searches title, kind, processing
state, structured metadata and current body, and returns exact record/revision
IDs plus matching fields. Blank queries fail; no files or approvals are created.
Project-level search remains separate from bank search.

Actual checks:
- `test_bank_search`, `test_cli`, `test_bank_storage`:29 tests passed.
- `.venv/Scripts/python.exe -m ruff check src tests`:passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`:65 files already
  formatted.
- `git diff --check`:passed; no config or source corpus changes.

Next small task: connect search results to exact record opening in the existing
read-only viewer, without adding writes or exports.

## Clickable v3 relationship navigation — 2026-11-18

The read-only bank detail now exposes typed subject, claim, source and evidence
relationships as safe local navigation links. Opening a related record fetches
the same bounded detail/history view; no arbitrary path or write operation is
introduced.

Actual checks:
- `npm run test:web`:6 tests passed.
- `node --check web/app.js; node --check web/server.mjs`:passed.
- `git diff --check`:passed.

Next small task: preserve this viewer boundary and avoid adding a broader
frontend or export workflow without a separately defined requirement.

## Bounded v3 revision history in viewer — 2026-11-18

Added a read-only `/api/bank/record/<id>` history summary for the current
managed3.0 chain. It follows only validated snapshot parent links, caps the
walk at 128 snapshots, returns revision IDs/timestamps/reasons and never
returns historical body bytes. The bank detail view now shows the compact
revision list alongside typed claim/evidence links. No writer, migration,
approval or public route was added.

Actual checks:
- `npm run test:web`:6 tests passed, including current revision history.
- `node --check web/app.js; node --check web/server.mjs`:passed.
- `git diff --check`:passed.

Next small task: stop expanding the viewer unless a concrete read-only need is
identified; use the existing Python history/reference commands for full exact
historical inspection.

## Typed v3 claim/evidence viewer links — 2026-11-18

Continued the existing managed3.0 work without starting migration or changing
the bank writer. Extended the opt-in loopback viewer's read-only record detail
response with typed claim/evidence relationships: claim subjects, evidence
relations, exact referenced revisions, current-versus-historical status, and
evidence claim/source links with locators. The UI now renders those fields as a
bounded human-readable report instead of exposing only raw JSON. No write,
approval, export, source, or public-serving path was added.

Actual checks:
- `npm run test:web`:6 tests passed, including subject-link and current-revision
  assertions.
- `node --check web/app.js; node --check web/server.mjs`:passed.
- `git diff --check`:passed; no config or source corpus changes.

Limitation: the viewer remains read-only and only exposes current committed
heads; older claim/evidence revisions still require the Python history/reference
commands. Next small task: add a compact read-only revision/history view if it
can remain bounded and preserve exact stored bytes.

## Read-only knowledge-bank viewer — 2026-11-18

Shifted from migration infrastructure to daily usability. Added an opt-in local
**Baza znanja** page to the existing loopback viewer. The server reads a bank
only when `JEB_BANK_ROOT` is explicitly configured, exposes current record
metadata and one-record details through bounded allowlisted paths, and keeps all
routes GET-only. The UI supports search and safe-text inspection for
entity/source/article/claim/evidence records; it has no edit, approval, export or
public serving path. Default viewer startup remains bank-disabled.

Actual checks:
- `npm run test:web`:6 tests passed, including opt-in bank endpoint, traversal
  rejection and read-only method checks.
- `node --check web/app.js; node --check web/server.mjs`:passed.
- `git diff --check`:passed; no config or source corpus changes.

Typed claim/evidence link display is now covered by the entry above.

## Synthetic migration writer simulation — 2026-11-18

Added `jeb bank migrate-simulate` with mandatory `--synthetic` opt-in. It binds
the external decision and current plan, requires a target name containing
`synthetic`, copies the full v2 committed history into a new v3 chain in private
sibling staging, preserves record/revision IDs and body bytes, rewrites only
versioned envelopes/manifests, validates the target through the normal v3 reader,
and returns `releasable:false` with zero approvals. The source v2 bank and its
archives are never modified. This is an isolated development simulation, not a
real migration or owner approval.

Safety hardening: the simulator now holds the source writer lock through
revalidation, copying and publication, then uses no-clobber directory rename.
Failure injection confirms that only its own staging directory is removed.

Actual checks:
- `test_bank_simulation`, `test_bank_decision`, `test_bank_migration`,
  `test_cli`:19 tests passed, including validation-failure staging cleanup.
- `.venv/Scripts/python.exe -m ruff check src tests`:passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`:63 files already
  formatted.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`:47 schemas passed.
- `git diff --check`:passed; no config or source corpus changes.

Limitation: no real writer, owner decision, public export or release path exists.
Next small task: review the synthetic simulation output before considering any
future real writer proposal.

## Bank migration decision binding — 2026-11-18

Added versioned `bank-migration-decision-v1`, read-only
`jeb bank migrate-decision-validate`, and synthetic offline tests. The validator
requires a human-owner decision shape, exact plan-file hash, current v2
workspace/HEAD/record digest, excluded F3A packets, zero blockers and a new
target path outside the source bank. It returns `can_write` as a capability
description only; it creates no approval, target directory, writer state or
historical content. Synthetic fixtures explicitly state that they are not real
owner decisions.

Actual checks:
- `test_bank_decision`, `test_bank_migration`, `test_cli`:16 tests passed after
  adding the decision schema/validator.
- `.venv/Scripts/python.exe -m ruff check src tests`:passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`:61 files already
  formatted.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`:47 schemas passed.
- `git diff --check`:passed; no config or source corpus changes.

Limitation: no actual owner decision, target creation or migration writer was
implemented. Next small task: review decision fields, then test a writer
simulation on synthetic data only.

## Bank migration writer design — 2026-11-16

Documented the reviewed-writer boundary in `docs/BANK_MIGRATION.md` without
creating a writer, decision record, target directory or approval. The design
requires an external owner decision bound to the exact plan hash, source
workspace, HEAD and record digest; rejects blocked records and F3A packets;
revalidates the source under lock; builds a sibling staging target; validates
the complete3.0 chain privately; and publishes only to a previously absent
destination with no-clobber rename. The v2 source and its archives remain
untouched. A future interrupted run must not alter source HEAD.

Actual checks:
- `git diff --check`:passed.
- `git diff --exit-code -- config sources`:passed; no configuration or corpus
  source changes.

Limitation: the decision-record schema and reviewed writer are intentionally not
implemented. Next small task: define that schema for separate owner review.

## Bank migration plan: read-only v2→v3 contract — 2026-11-16

Continued the next authorized small task without changing existing banks or
archives. Added `docs/BANK_MIGRATION.md`, read-only `jeb bank migrate-plan` and
`jeb bank migrate-plan-verify`
command. It validates a managed2.0 committed chain, binds the report to the
current HEAD and current-record digest, lists every record and all historical
revision IDs in stable order, preserves source raw hashes as provenance, keeps
body hashes unchanged, reports blockers, and explicitly excludes F3A packets.
The command writes only one no-clobber JSON report outside `bank-root`; it never
creates a v3 target, writes a source bank, creates claims/evidence, or creates
approvals. Managed3.0 input is rejected so no accidental re-planning occurs.

Actual commands/results:
- `.venv/Scripts/python.exe -m unittest tests.test_bank_migration -v`:5 tests
  passed. They cover HEAD immutability, external/no-clobber output, v3 input
  rejection, stale-plan rejection after a new source commit and a synthetic
  blocked-record policy with no target identity.
- `.venv/Scripts/python.exe -m ruff check src tests`:passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`:59 files already
  formatted.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`:46 schemas passed.
- Targeted bank/CLI regression (`test_cli`, all bank storage/backup/evidence
  suites and `test_bank_migration`):99 tests in36.308s,OK,1 skipped for the
  existing Windows symlink privilege condition.
- CLI smoke: v2 `bank init` followed by installed local `bank migrate-plan`
  produced a dry-run JSON report with0 records,0 approvals and `writable:false`.
- `git diff --check`:passed; no config or source corpus changes.

Limitations: this is only a plan, not migration. It does not re-encode records,
write a target, import F3A packets, resolve conflicts, or make an owner decision.
Next small task: separately design the reviewed writer step.

## Bank F3B: persistent historical claim/evidence — 2026-11-16

Continued the explicitly authorized implementation after reading repository
instructions, progress/next-step notes and git status. Added opt-in managed3.0
schemas and writer/reader support for persistent `claim` and `evidence` records.
Each claim pins its subject to a committed record/revision/raw-record hash/body
hash. Each evidence record pins a claim and source the same way, records a typed
relation, rationale, limitations and locator, and remains `unreviewed`. New
records may refer only to exact earlier committed revisions; missing, forward,
self, wrong-kind, changed-hash and foreign-bank references fail closed.

History retains older source revisions, so an evidence text span can still be
checked against the exact source body it cited after that source is edited. A
new claim revision does not inherit the old evidence; links report whether the
stored evidence still points to the current claim and source revision. Page,
section and time locators are declared metadata, not verified against absent
media. No truth selection, assessment, import, migration, approval or release
operation was added. The existing F3A packet is still a separate v2-only draft
format; it is not silently imported. Default init remains2.0, and v2 schemas and
backup fingerprints remain byte-identical. See
`docs/BANK_PERSISTENT_EVIDENCE.md`.

Actual commands/results in the existing hash-locked Python3.13 environment:
- `.venv/Scripts/python.exe -m ruff check src tests`:passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`:57 files already
  formatted.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`:46 schemas passed.
- `.venv/Scripts/python.exe -m unittest tests.test_bank_persistent_evidence -v`:
  14 new offline tests passed. They cover exact references, source/claim
  revisions, locators, immutable v2 defaults, v2 draft boundary, CLI, recovery,
  and v3 backup/restore with a historical reference graph.
- `.venv/Scripts/python.exe -m unittest discover -s tests -v`:379 tests in
  268.958s,OK,1 skipped because Windows did not permit the existing symlink
  privilege test. All mocked link guards passed.
- `.venv/Scripts/python.exe -m pip wheel --no-build-isolation --no-deps
  --no-index --wheel-dir dist/bank-v3-package .`:success. Wheel SHA-256
  `7b8960f42dc72642b4b0247c824f3ca37cb13ee31a12ca835890e504f402b3e6`.
- Installed the wheel under `dist/bank-v3-installed`, verified its import path,
  and executed the complete original example from
  `docs/BANK_PERSISTENT_EVIDENCE.md`:4 valid records,1 body, local text span
  match, backup/restore graph equality,0 approvals. Temporary private example:
  `C:/Users/LovroPC/AppData/Local/Temp/jeb-bank-v3-example-fj263nsj`.
- From the installed wheel, the CLI parsed `bank --help`, initialized a fresh
  managed3.0 bank and validated it successfully with0 records.
- Compared all six v2 backup schema fingerprints against the prior installed
  wheel:identical. A backup freshly created by that prior v2 installation
  verified and restored successfully with current code.
- `git diff --check`:passed. `git diff --exit-code -- config sources`:passed;
  no configuration/source changes.

Remaining limits: 128 full snapshots/128MiB history; no scalable index or
frontend. There is no v2→v3 migration or F3A packet import, source-content
verification for declared media locators, evidence-quality assessment, claim
selection, or publish/release flow. Next small task: specify a dry-run-only v2
copy/migration contract with explicit identity mapping and blockers while
preserving the original bank and archives; keep F3A packet importing separate
until provenance and conflict behavior are explicit.

## Bank F3A: revision-bound claim/evidence drafts — 2026-11-15

Continued authorized next step after reading continuity/status, existing bank
storage/validation/backup schemas and repository instructions. Preserved earlier
uncommitted work. Added bank evidence prepare/validate/inspect with two separate
version1.0 packet/draft schemas. Managed2.0 record/workspace/transaction and backup
schemas remain byte-identical. No new canonical record kind or silent migration.

Drafts distinguish source statements, historical claims, interpretation, personal
reflection and fiction. Evidence has supports/contradicts/contextualizes/mentions,
rationale, limitations and typed text-span/page/section/time locators. Packets bind
exact workspace HEAD plus referenced entity/source revision, raw record hash and
body hash; changed HEAD/schema/bindings fail closed. Text spans check exact local
Unicode-codepoint ranges without normalization; page/section/time locators remain
declared_only, not verified source content. Claims without links are explicitly
listed. Inspect retains exact source credits/editions and packet categories.

Artifacts are outside the managed bank, no-clobber and private/unreviewed, with
approval_authority none. No real historical text/claim, human decision, corpus
admission, source/config change, model API, fetch, dependency, publish or push.
Added BANK_EVIDENCE.md with executable original example and explicit future-format
contract; updated README/workflow/backup notes, implementation plan and next task.

Actual commands/results in existing hash-locked environment:
- `python -m ruff check src tests`:passed; targeted ruff format applied to new
  evidence module/tests. Final `python -m ruff format --check src tests`:55 files
  passed. `python -m jeb validate --stage schemas`:42 schemas passed.
- `python -m unittest tests.test_bank_evidence -v`:18 original offline tests in
  5.716s,OK. Includes typed references, literal CRLF/UTF-8 ranges, invalid/declared
  locators, duplicate/colliding IDs, unsupported claims, contradictions, staleness,
  tampering/resealed bindings, unknown approval fields, output bounds and restore.
- `.venv/Scripts/python.exe -m unittest discover -s tests -v`:365 tests in236.560s,
  OK,1 skipped (existing real-symlink OS-privilege test; mocked guards pass).
- `python -m pip wheel --no-build-isolation --no-deps --no-index --wheel-dir
  dist/bank-evidence-package .`:success. Wheel SHA-256
  b0955fb6f8461f1a7f929e17f9bfa19139237614406020691df841d556d18bde.
- Installed with `pip install --no-index --no-deps --target
  dist/bank-evidence-installed <wheel>`; verified imports originate there and
  both new schema resources exist. Executed exact BANK_EVIDENCE.md example with
  installed code:1 claim/1 local_text_match,0 approvals. Installed parser/run
  validate/inspect and packet validation after bank backup/restore passed.
  Original example retained at C:/Users/LovroPC/AppData/Local/Temp/
  jeb-evidence-example-exotwpoh for inspection, not publication.
- Compared six backup schema hashes to the earlier bank-backup wheel:identical.
  A subprocess using that prior installed wheel created a fresh original archive;
  current code verified/restored it successfully. No old backup regeneration.
- `git diff --check`, `git diff --exit-code -- config sources`:passed exit0.
No web/library code changes, web/browser checks or historical acquisition.

Limitations: external draft packets are not canonical records or part of bank
backups; retain them separately. Whole-HEAD staleness is deliberately conservative.
Page/section/time content is unverified without media artifacts. Exact text match
does not establish historical truth, independence or rights. No assessment,
selection/promotion or canonical claim persistence yet. Next small task: explicit
new-format schema/reader contract for persisted exact-revision claim/evidence,
preserving existing2.0 schemas/archives; then writer/import support, no implicit
upgrade or fabricated human review.

## Bank committed-chain backup and restore — 2026-11-15

Continued the authorized next step after reading current continuity and git
status; preserved all earlier uncommitted library/viewer/bank work. Added
`jeb bank backup`, `backup-verify` and `restore` independently of Project/corpus.
The private ZIP copies only exact committed2.0 HEAD/workspace/history bytes;
staging, locks, inactive snapshots and library/private are excluded. Packaged
bank-backup schema binds file sizes/hashes, workspace/HEAD and six relevant
schema identities. No model/cloud dependency, source admission, real content,
approval, publication, Git commit or push was introduced.

Backup holds the existing writer lock, verifies a temporary archive end-to-end
and publishes with a same-filesystem hard link that cannot replace an existing
file. ZIP directory counts/metadata are bounded before zipfile allocation;
only allowlisted ordinary files/stored-deflate content are accepted. Validation
reconstructs the complete committed chain privately and checks inner manifests
and revision semantics as well as the outer inventory. Restore validates first,
exclusively reserves a new directory, copies under a new lock and publishes the
exact original HEAD bytes last. Handled failures remove only tracked new files
and empty directories; no recursive deletion of arbitrary user trees.

Added20 original offline backup tests, including exact-byte CRLF/noncanonical
HEAD round-trip, disconnected original source, writable restored history, empty
bank, omitted pending/private work, no-clobber races, hash/inventory/schema/HEAD
damage, inactive snapshot injection, path traversal/special/duplicate entries,
false ZIP member count, corrupt deflate, size limits and partial-write cleanup.
Added BANK_BACKUPS.md and updated workflow/format/README/plan/next small task.

Actual commands/results:
- Initial temporary smoke found Windows fsync EBADF on a read-only ZIP handle;
  changed it to r+b before fsync. Repeat create/restore smoke passed.
- Targeted lint/format corrected new import order and an unused test binding.
  A test insertion briefly misplaced the corrupt-deflate block (NameError);
  corrected placement and reran the entire20-test backup group successfully.
- `.venv/Scripts/python.exe -m unittest tests.test_bank_backup -v`:final targeted
  run20 tests in8.194s,OK. That run includes the exact-original-HEAD regression.
- `.venv/Scripts/python.exe -m ruff check src tests`:passed.
- `.venv/Scripts/python.exe -m ruff format --check src tests`:passed53 files.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`:40 schemas passed.
- Intermediate full `python -m unittest discover -s tests -v`:346 tests in
  239.207s,OK,1 skipped. It loaded the earlier19-test backup group before the
  final exact-HEAD preservation correction; a fresh full run was started after
  that correction and final private-permission defaults.
- Final `.venv/Scripts/python.exe -m unittest discover -s tests -v` on final code:
  347 tests in319.094s,OK,1 skipped (the existing real-symlink privilege test).
  Final lint/format checks and40-schema validation also passed before that run.
- `python -m pip wheel --no-build-isolation --no-deps --no-index --wheel-dir
  dist/bank-backup-package .`:success. Final wheel SHA-256
  2c3bb0e319e84a742114a7f837ffa75a3eebf6ab80b86938db6f2565c900cf33.
- Installed with `pip install --no-index --no-deps --target
  dist/bank-backup-installed <wheel>`; verified imports from that target and
  packaged schema. Installed parser/run backup/verify/restore lifecycle passed
  on temporary original data:3 snapshots,2 retained record revisions,0 approvals;
  restored history/validate/recover passed, no pending material imported.
- `git diff --check` and `git diff --exit-code -- config sources`:passed exit0.
  `python -m jeb bank --help` lists all11 operations. No web/library code changed,
  so no web suite or browser verification was needed/performed.

Limits: this is an unencrypted private committed-text-history backup, not public
export, a whole-project backup, or a copy of linked remote/media content. Current
schema hashes must match; no migration, automatic scheduling or encryption is
provided. Abrupt restore termination can leave incomplete new/temp directories;
no power-loss or hostile/network-filesystem guarantee. Retain the matching wheel
and store independent copies on appropriate media. Next small task is the F3
claim/evidence/typed-locator format contract, with explicit version transition.

## Knowledge bank F2: managed revisions and recovery — 2026-11-15

Continued after owner approval and continuation request. Read current status,
PROGRESS/NEXT_STEPS and preserved all earlier uncommitted work. Added separate
managed bank format2.0 without relaxing initial1.0 schemas or silently migrating
them. Four additional packaged schemas bind workspace, record revision, HEAD and
transaction. Existing validate/show dispatch to either supported format before
Project construction. Added init/create/edit/history/diff/recover commands.

Writer builds complete snapshots under staging, validates exact bytes and typed
references, then renames the snapshot and atomically replaces HEAD.json. Old
snapshots are unchanged. Nonblocking OS byte-lock/flock coordinates local writers;
process exit releases locks without deleting the persistent lock file. Edit
requires exact expected-revision. Reader follows one captured hash-bound HEAD
through validated history. Recovery explicitly activates only a complete candidate
whose parent still matches; incomplete/conflicting material remains untouched.
History and diff retain old body bytes, metadata, revision actor and reasons.
No human approval, real historical content, corpus/source change, network fetch,
model API, cloud dependency, publication, commit or push was introduced.

Added19 original offline storage tests: cross-process contention/release, abrupt
os._exit before publication, failures at each file-write step, prepared-directory
rename/HEAD replacement failures, old-state visibility during staging, recovery
and idempotence/conflicts, parent/revision/immutable-field tampering, historical
body tampering, limits, legacy non-migration and CLI lifecycle. Existing17 bank
tests remain. Updated README, BANK_FORMAT/WORKFLOW, plan and next task.

Actual commands/results using the existing hash-locked .venv:
- Initial `python -m ruff check src tests` found one new import-order issue;
  targeted `ruff check --fix src/jeb/bank tests/test_bank_storage.py` fixed two
  import-order issues after tests were added. No unrelated files reformatted.
- `python -m ruff format src/jeb/bank src/jeb/cli.py` and targeted test formatting
  applied; final `python -m ruff check src tests`:passed.
- `python -m ruff format --check src tests`:passed51 files.
- `python -m jeb validate --stage schemas`:39 schemas passed.
- `python -m unittest tests.test_bank_storage tests.test_bank -v`:36 tests in
  7.248s,OK,1 skipped (OS disallowed real symlink creation; mocked guards pass).
- `python -m unittest discover -s tests -v`:327 tests in203.257s,OK,1 skipped.
- `python -m pip wheel --no-build-isolation --no-deps --no-index --wheel-dir
  dist/bank-f2-package .`:success. Wheel SHA-256
  500d0cae40078b8e6b66b840508bc4a494a2b38332f2665c7d9b275a99b0c7e4.
- `python -m pip install --no-index --no-deps --target dist/bank-f2-installed
  <wheel>`:success. Verified imports originate from that target, all four new
  schemas are packaged, and installed parser/run lifecycle init/create/edit/
  validate/show/history/diff/recover passes on temporary original data.
- `git diff --check`, `git diff --exit-code -- config sources`:passed exit0.
  `python -m jeb bank --help` lists all eight implemented operations.
No web/library code changed; their tests/browser preview were not rerun.

Limitations: full-copy history is capped at128 active snapshots/128MiB payload,
not yet a scalable database. No backup/restore, migration, evidence assessments,
index or bank UI. Locks assume cooperative local processes; no hostile-filesystem
or network-filesystem guarantee. Windows power-loss durability is not promised.
Failed early initialization may leave an incomplete new directory; it never
overwrites an existing one. After a post-HEAD error inspect state before retrying
create. Next small task: bounded committed-chain backup/restore to a new directory,
excluding staging and locks, before valuable personal data; then F3 evidence.

## Knowledge bank F0 / minimal read-only F1 — 2026-11-15

Owner said to proceed with coding. Read current continuity/status first and
preserved existing library/viewer edits, including batch16. Implemented a separate
`jeb bank validate/show --bank-root ...` entry before Project construction: no
biblical configuration required or corpus admission implied. Added packaged
bank-workspace/bank-record schemas, bounded read-only snapshot reader and original
temporary tests. Entity/source/article records bind workspace/record/revision IDs,
typed article references and exact UTF-8 Markdown hashes. Duplicate JSON keys,
unknown versions/fields, body tampering, unsafe directory names, links/junctions
and size/count overruns fail closed. No URLs fetched; source references remain
unverified metadata. Initial parent_revision must be null; no writer/history,
bank UI, claim assessment or export functionality is claimed implemented.

Added BANK_FORMAT.md, BANK_WORKFLOW.md with runnable original example, README
entry and implementation-plan status. NEXT_STEPS names versioned revision and
single-writer commit/recovery design as the next small slice. No historical text,
owner approval, config/source change, push, release or publication was created.

Environment and actual results:
- `py -3.13 -m venv .venv`: success; existing Python observed as3.13.3.
- `.venv/Scripts/python.exe -m pip install --require-hashes -r requirements.lock`:
  success, exact locked dependencies installed without editing the lock.
- `.venv/Scripts/python.exe -m pip install --no-build-isolation --no-deps -e .`:
  success, one editable package/CLI.
- `.venv/Scripts/python.exe -m ruff check src tests`: passed.
- `.venv/Scripts/python.exe -m ruff format src/jeb/bank tests/test_bank.py`:
  two files formatted; later `-m ruff format --check src tests` passed49 files.
- `.venv/Scripts/python.exe -m jeb validate --stage schemas`:35 schemas passed.
- `.venv/Scripts/python.exe -m unittest discover -s tests -v`:307 tests in194.610s,
  OK,1 skipped (OS disallowed real symlink creation). This run loaded the original
  16 bank tests before an extra mocked link/junction guard test was added.
- Final `.venv/Scripts/python.exe -m unittest tests.test_bank -v`:17 tests in1.241s,
  OK,1 skipped. Mocked symlink/junction guards both passed without OS privileges.
- `.venv/Scripts/python.exe -m pip wheel --no-build-isolation --no-deps --no-index
  --wheel-dir dist/bank-f1-package .`: success; wheel SHA-256
  e03efd3f84cda079f278155c19f940e12322f1345f54729b014838a261382ab6.
- Installed that wheel with `pip install --no-index --no-deps --target
  dist/bank-f1-installed <wheel>`; verified import resolves under that target,
  both new schema resources exist, and executed the exact documented Python
  example with installed code:2 records,1 bound body,0 approvals. Example retained
  outside repo at C:/Users/LovroPC/AppData/Local/Temp/jeb-bank-example-9plx8q9i.
- `git diff --check`, `git diff --exit-code -- config sources`: passed exit0.
  `jeb bank --help`: lists validate/show. Web tests not rerun: no web/library code
  changed in this slice. No browser inspection claimed.

Limitations: structural/integrity validation cannot prove content or actor identity;
no protection against a hostile process racing filesystem reads; privacy labels
are metadata, not authorization. Valuable data should wait for tested history,
commit recovery and backup. Current full-suite total plus separately verified new
guard case is308 tests; a second full run was unnecessary for that isolated test.

## Personal library, sixteenth batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status before work; preserved all existing edits
and separate knowledge-bank proposal. Reviewed20 targets146–165, added16
findings for15 newly represented works:153 findings for138 works. Enriched
existing038 Hafiz2009 and039 Mesnevi2016/three physical volumes, without
duplicate edition counts. See library/research/batch-16-review.md for all20
outcomes, exact source URLs, access failures and edition limitations.
Recorded Croatian Diogenes/Boethius/Cicero leads, Plotinus volume6 only,
Haveric's Ibn Tufayl, Bucan's al-Maarri selection, Bosnian Khayyam/Attar/Rumi/
Saadi candidates and institutional Ibn Arabi credit. Fihi1996 French-mediated
and Drkic2011 editions separate. Invalid Attar retailer identifier not accepted
as ISBN. Bosnian place of publication not treated as language evidence.
Unresolved146,153,154. Five private files unchanged; no full acquisitions,
source reconstruction, transliteration, corpus admission, approval or release.

Actual commands/results: `npm run library:catalog` passed291 books/14 groups/
153 findings. `npm run test:web` passed5/5,0 failures,140.6327ms. Node inventory
and assertions confirmed153 findings/138 works,16 new observations/15 works,
no new local_file,5 private files,3 unresolved IDs and2 enriched old findings.
`git diff --check` and `git diff --exit-code -- config sources src tests`
passed exit0. Python suites not rerun: no Python/schema/corpus changes.
README counts and next library group166–185 updated, bank F0/F1 task preserved.
No commit,push,release,server start or browser preview.

## Personal library, fifteenth batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status before continuing; preserved existing work
and the separate knowledge-bank proposal. Reviewed20 targets126–145, added17
findings for16 works (15 newly represented):137 findings for123 works.
library/research/batch-15-review.md records all20 outcomes and source URLs.
Aristotle Talanga/Ladan, Epicurus three verified component titles, Lucretius
Tepes, Epictetus distinct editions, Aurelius Vujacic, Seneca distinct volumes/
essays/translators, Musonius magazine selection and Sextus Grgic recorded.
No third Epicurus letter inferred from Latin source title. Musonius article
author not automatically promoted to translator; magazine date discrepancy
retained. Seneca letters limited to1–81. Four unresolved targets130,132,144,145.
Five private files unchanged; no new full acquisitions, approvals, corpus
changes, reconstruction from memory, transliteration or publication.

Actual commands/results: `npm run library:catalog` passed291 books/14 groups/
137 findings. `npm run test:web` passed5/5,0 failures,144.0816ms. Node inventory
and assertions confirmed137 findings/123 works,17 new observations/16 works,
no new local_file,5 private files and the four unresolved IDs above.
`git diff --check` and `git diff --exit-code -- config sources src tests`
passed exit0. Python suites not rerun: no Python/schema/corpus code changes.
README counts and separate library next group146–165 updated; bank F0/F1
next task preserved. No commit,push,release,server start or browser preview.

## Personal library, fourteenth batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status,AGENTS and rights policy; preserved existing
uncommitted work and separate knowledge-bank proposal. Reviewed20 targets106–125,
added15 findings for15 works:120 findings for108 works. See
library/research/batch-14-review.md for the20-row outcome matrix and exact URLs.
Three haiku authors share one Croatian anthology; Takuan's sample establishes
the requested essay and imprint credit Zvonimir Baretic despite retailer Zoran.
Musashi NDL/publisher ISBN and page discrepancies retained. Heraclitus root text
inside Mikecin commentary distinguished; Parmenides PDF418 and Menon publisher403
recorded honestly. Plato translations retain individual translator versus
editor/intro roles, and Plato/Xenophon same-title works are not conflated.
Five targets unresolved; five private edition files unchanged, no new full text
acquisition, automatic transliteration, corpus change, approval or publication.

Actual commands/results: `npm run library:catalog` passed291 books/14 groups/
120 findings. `npm run test:web` passed all5 tests,0 failures,137.5972ms.
Node inventory/assertions confirmed120 findings/108 works,15 distinct new works,
no new local_file and5 private files; unresolved109,110,111,112,115.
`git diff --check` and `git diff --exit-code -- config sources src tests`
passed exit0. Python suites not rerun: no Python/schema/corpus code changes.
README and separate research next step updated to126–145; knowledge-bank F0/F1
task preserved. No commit,push,release,server start or browser preview.

## Personal library, larger thirteenth batch — 2026-11-15

Owner asked for more work per turn. Read PROGRESS,NEXT_STEPS,git status;
preserved all existing work, including the separate knowledge-bank coding plan.
Reviewed20 targets086–105 and recorded their individual outcomes in
library/research/batch-13-review.md. Added9 findings for8 new works: total105
findings for93 works. Dao2020/2023 separated by ISBN; Merton/Baretic is a free
interpretive selection and a12-page online sample, not full Zhuangzi. Daxue/
Zhongyong share one Ethos2019 volume; Hojoki/Tsurezuregusa share one LOM2024
volume via English Keene. Shonagon2022 explicitly a selection. Croatian Basho
2000 has both translator credits and explicit Latin-script metadata. Twelve
targets remain without qualifying findings; no claim their translations do
not exist. Five private full-edition files unchanged, no new full acquisition.
No historical text, model API, real approval, corpus admission or publication.

Actual checks: `npm run library:catalog` passed, reported291 books/14 groups/
105 findings. `npm run test:web` passed all5 tests,0 failures,154.646ms.
Node inventory check returned105 findings/93 works, batch9 findings/8 works,
5 private files. `git diff --check` and
`git diff --exit-code -- config sources src tests` both passed (exit0).
Python suites not rerun: no Python/schema/corpus code changed. Updated current
library README counts and separate research next step106–125; preserved F0/F1
knowledge-bank next task. No commit,push,release,server start or browser preview.

## General knowledge-bank coding plan — 2026-11-15

Owner requested a large coding plan for an open personal knowledge bank with
evidence, retained assessment history, mixed media and reusable agent/project
exports. Read PROGRESS/NEXT_STEPS/git status, repository instructions, package
manifests, existing CLI/knowledge/server boundaries and rights policy. Preserved
uncommitted work, including batch12 added while this plan was being written.
Added docs/KNOWLEDGE_BANK_IMPLEMENTATION_PLAN.md: separate proposed bank namespace,
15 phases F0–F14, data model, revision/recovery, private projections, offline agent
proposals, media, export/import and backup/restore. Documentation only: described
commands/schemas/features are not implemented. No corpus, approval or dependency
change. Next small task is format specification/minimal read-only validation.

Actual checks: `git diff --check` passed (exit 0); `git diff --exit-code -- config
sources src tests` passed (exit 0). PowerShell phase count returned15; plan length
516 lines. Python/web suites not rerun: no executable/schema/catalogue/UI changes
in this task. No commit, push, publication or real historical claim was created.

## Personal library, twelfth batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status. Added3 catalogue observations for2 works,
now96 findings for85 works; five private files unchanged. Huangbo2004 and1986
editions separate; Xinxin Ming Osho commentary not root text. Platform/Linji
unresolved. Existing uncommitted work preserved. See batch-12-review.md for
exact URLs and access depths; no language/script inferred from location or
catalogue script, no bypass of access challenges, no new full acquisition.
Commands: npm run library:catalog passed291/14/96; npm run test:web all5 passed.
git diff --check and git diff --exit-code -- config sources src tests passed.
No Python changes/checks, corpus admission, approval or publication.

## Personal library, eleventh batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status; preserved work. Added3 candidates for3
works, total93 findings for83 works; no new files. Explicitly distinguished
catalogue credits from AI-translated preface description, indexed Heart Sutra
from challenged live page, and Diamond Sutra English translator from unnamed
regional translator. Vimalakirti unresolved. No bypass of403/access challenge.
See batch-11-review.md for URLs, source depths, and quality limits.
Commands/results: npm run library:catalog passed291/14/93; npm run test:web
all5 passed. git diff --check and git diff --exit-code -- config sources src
tests passed. No Python changes/checks, publication, approvals or corpus change.

## Personal library, tenth batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status; preserved work. Two new findings (MMK
first-chapter bibliographic record, incomplete Ratnavali PDF), Milindapanha
record corrected to explicitly abridged. Totals90 findings for80 works,five
private files. Suhrllekha unresolved. See batch-10-review.md for sources and
limits. No new downloads, full-language-search claim or inferred translator.
Validation: npm run library:catalog passed291/14/90; npm run test:web all5
passed. git diff --check and git diff --exit-code -- config sources src tests
passed. No Python changes/checks, corpus admission, human approval or publication.

## Personal library, ninth batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status; preserved work. Added one shared PDF finding,
now88 findings for78 works and five private files. Corrected Thera/Theri online
records to explicitly selected excerpts and Itivuttaka HTML to introduction.
Applied previously read PDF skill read-only: pdftotext and pdftoppm succeeded
on actual Drive PDF; visually checked PDF3/4 notice and credits.224 PDF pages,
221 inCIP, terminal section112 onPDF219. No full textual collation.
Initial SER05 URL fetch404, subsequent extraction failed because file absent;
normal public Drive download succeeded4389623bytes. Exact receipt/hash/limits
in library/research/batch-09-review.md. Combined file counted once, no admission.

Validation: npm run library:catalog passed291/14/88; npm run test:web all5 passed,
139.6734ms. After final metadata-only introduction precision, catalog rebuilt.
Node readFile/createHash verified new file size/hash; git check-ignore confirmed
private file. git diff --check and git diff --exit-code -- config sources src
tests passed. No Python changes/checks, publication, human approval or Git push.

## Personal library, eighth batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status. Preserved uncommitted work. Added4 findings,
now87 findings for78 works. Pancatantra Matisic1980 and1999 are separate editions,
not separate translations; Hitopadesa unconfirmed. Two public PDFs linked by
Srednji put acquired unchanged; now four private library copies. Detailed URLs,
counts and SHA-256 in library/research/batch-08-review.md and downloads.json.
Applied PDF skill read-only, no authoring marker. pdftotext -layout, pdfinfo and
pdftoppm succeeded. Suttanipata PDF3/4 and Udana PDF3/4 visually inspected for
notice/credits; an initial Udana PDF2 render showed title, then PDF4 was rendered
to verify translator. Udana extraction80 headings, Suttanipata last verse1149;
no full textual collation. Provider free-distribution labels not universal rights.

Commands/results: node library/research/acquire-batch-08.mjs --private succeeded,
2310579 and3131093 bytes; receipts recorded. npm run library:catalog passed
(291 books,14 groups,87 findings); npm run test:web all5 passed,141.2178ms.
node --check library/research/acquire-batch-08.mjs passed; download sizes/hashes
verified with Node readFile/createHash. git check-ignore confirmed both PDFs;
git diff --check and git diff --exit-code -- config sources src tests passed.
No Python code changes/checks, corpus admission, approval, publication or push.
Next small task in NEXT_STEPS: remaining early Buddhist collections.

## Personal library, seventh research batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status; preserved uncommitted work. Executed16
queries in4 web calls for Basava/ Akka Mahadevi Vacane and two Jain sutras.
No qualifying regional edition confirmed. Stored exact queries and rejected
candidate URLs in library/research/batch-07-review.md. No additions to findings
or copies; totals remain83 findings for77 works and two private full files.
Kept English/Czech texts, isolated mentions and different authors separate.
Did not claim full language search, nonexistence, source reading or clearance.

Validation: git diff --check passed; git diff --exit-code -- config sources
src tests passed. Documentation-only batch; no application/Python tests rerun.
No corpus, schema, source lock, approvals, publication or Git history changes.
Next small batch recorded in NEXT_STEPS: Pancatantra/Hitopadesa/Suttanipata/Udana.

## Personal library, sixth evidence batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status; preserved uncommitted work. Added4
observations for4 works, total83 findings for77 works. Three are the same
national CIP collection candidate, not independent translations or verified
complete collections. Script/language/individual coverage unconfirmed. Bijak
is a hosted introductory excerpt; regional translator unknown, no claim of
human translation. Separate Mandic poetry collection not equated with Bijak.
Exact URLs/access limitations in library/research/batch-06-review.md. No new
download, publication, owner approval, scope or source-lock change.

Commands/results: npm run library:catalog passed (291 books,14 groups,83 findings).
npm run test:web all5 passed,139.5645ms. git diff --check passed;
git diff --exit-code -- config sources src tests passed. No Python code/schema
changes or Python checks. Next four works recorded in NEXT_STEPS.

## Personal library, fifth evidence batch — 2026-11-15

Read PROGRESS,NEXT_STEPS,git status; preserved uncommitted work. Added4 findings
for4 new works, total79 observations for73 works; no new private full copies.
See library/research/batch-05-review.md for exact URLs and access depths.
Kept Mandukya research bibliography distinct from whole-work translation;
Yoga Vasistha indexed136-page scan has named translators but uncertain coverage;
Vijnana2025 retailers disagree205/191pp; Tirukkural is a short PDF61 excerpt
with unknown translator. No nationality/language inferred from shop location.
No access challenge bypass, automatic correction, model text or rights clearance.

Commands/results: npm run library:catalog passed (291 books,14 groups,79 findings).
npm run test:web all5 passed,138.8562ms. git diff --check passed;
git diff --exit-code -- config sources src tests passed. No Python/schema/code
changes or Python checks. No browser preview requested or performed. No commit,
publication, corpus admission or human approval. Next: Bhartrhari and Kabir.

## Personal library, fourth evidence batch — 2026-11-15

Read PROGRESS, NEXT_STEPS, git status. Preserved all uncommitted work.
Added5 observations for4 new works, total75 findings for69 works. Exact links,
credits and limits in library/research/batch-04-review.md. No new downloads.
Atmabodha credit Veljacic differs from Vivekacudamani Vuckovic/Antic; preserved
individual credits and126-page PDF versus167-page CIP discrepancy. Avadhuta
blog chapter headings I–VII confirmed, completeness unassessed. Croatian
Astavakra1997 retailer record lacks translator and real publisher name.
No inferred language from Lotos library location. PDF screenshot attempts
returned no usable image payload; no visual verification claimed this batch.

Commands/results: npm run library:catalog passed (291 books,14 groups,75 findings);
npm run test:web all5 passed,165.4902ms. git diff --check passed;
git diff --exit-code -- config sources src tests passed. No Python changes or
new Python checks. No publication or change to source lock/scope/approvals.
Next small task recorded in NEXT_STEPS: following four Indian works.

## Personal library, third evidence batch — completed 2026-11-15

Read PROGRESS, NEXT_STEPS and git status; preserved earlier uncommitted work.
Research begun 2026-11-14: added 14 findings for 13 additional requested works,
now 70 observations for 65 of 291 works. See library/research/batch-03-review.md.
Babun publisher preview retained as metadata/contents evidence only, not ten
whole works. Three Upanishads explicitly selections; printed Mandaka remains
an unresolved identity candidate for Mundaka. Matica primary catalogue confirms
Jezic's Croatian Aitareya edition. Yoga Turina remains link-only with restrictive
rights; Kotarac indexed CC edition download failed TLS, alternative returned404.
No TLS override, fabricated bytes, language priority or rights clearance.

Actual acquisition commands/results (2026-11-14):
- node library/research/acquire-batch-03.mjs --private: initial TLS error;
  per-target error reporting then recorded two failures and publisher preview
  success, 286906 bytes. Receipt batch-03-acquisition.json.
- node library/research/acquire-samkhya.mjs --private: success, 810182 bytes,
  hash dc8e8c0fa35c85828f44dbb6476e4531cc9482b7e54d67be36306ed93c3ca006.
- pdftotext -layout and pdftoppm: success. Visually checked Babun PDF4–6,
  Antic PDF2 notice and PDF31 end of Karika. Karika numbered1–71, PDF19–31;
  separate Sutra startsPDF32. Modernized translation through English sources.
  Receipt records private unchanged use only. Two private copies total.

Validation (2026-11-15):
- npm run library:catalog: success,291 books,14 groups,70 findings,291 searched.
- npm run test:web: all5 tests passed,373.2025ms; added safeguards for selections,
  unresolved title and failed download; checked each saved finding has receipt.
- node --check library/research/acquire-batch-03.mjs: passed.
- node --check library/research/acquire-samkhya.mjs: passed.
- node --check web/library.js: passed. Copy label now supports PDF as well as HTML.
- Node readFile/createHash verification of both downloads: sizes/hashes matched.
- git diff --check: passed.
- git diff --exit-code -- config sources src tests: passed, unchanged.
- git check-ignore on Samkhya and publisher preview: both private paths ignored.
Python checks not rerun: no Python/schema/corpus changes, prior hash-locked
environment remains unavailable. No browser preview requested or performed.
No publication, commit, scope extension or human approval. Next small task in
NEXT_STEPS: four subsequent Indian works, with exact translators and coverage.

## Personal library, second evidence batch — 2026-11-14

Read PROGRESS, NEXT_STEPS and git status; preserved existing uncommitted work.
Applied PDF skill read-only. Added 16 observations: seven TELEdisk 2002 contents
and catalogue cross-checks, eight contents-only entries with unresolved imprint,
and one visually verified Pirkei Avot opening excerpt. Current totals: 56
observations / 52 requested works. No claims of full-text acquisition, best
translation, exhaustive language search or rights clearance were inferred.

Inspected institutional PDF Feministicka teologija, Futura publikacije 1999,
edited by Svenka Savic (credits retain actual diacritics in library metadata).
The web tool refused its 21368856-byte length. Bounded Node retrieval from the
institutional host succeeded, 21368856 bytes, SHA-256
d60cc36850de677338fe738ff196f560d88deb4f81a5b832495c3dc220b0dce7.
Receipt: library/research/batch-02-evidence.json. Original PDF plus extraction
and page PNGs stay under ignored library/private/evidence/. This is evidence
for one truncated excerpt, not another selected complete-work download.
pdftotext -layout and pdftoppm succeeded. Visual inspection: title PDF p3;
Avot opening PDF p169 / printed p167; unrelated next article PDF p170.
No excerpt transcription or translator was invented. First Python console print
failed on cp1252; rerun with `python -X utf8` succeeded. Poppler emitted missing
Symbol/ArialUnicode font warnings; the three relevant pages were image-inspected.

The 897-page ivantic compilation contains several segments. Extracted contents
of the TELEdisk segment and the later Gnostika segment were inspected online;
imprint/translator for the latter remains unresolved, never silently equated
with Demetra 2007. Screenshot calls did not produce inspectable images (one
timeout); no visual verification of that remote file is claimed. No local full
mirror PDF acquisition. Asclepius 21-29 remains partial. Cyrillic Sekstove
izreke 2019 was rejected as a Latin-selection candidate; no transliteration.
Jevrejska digitalna biblioteka human-verification gate was not bypassed.
Detailed findings and limitations: library/research/batch-02-review.md.

Added bounded status distinctions online_excerpt / contents_lead in catalogue
builder and viewer, plus evidence links and edition identity notes. This keeps
partial/unbound evidence distinct from online full-work routes and identified
editions. No Python code/schema, config, source lock, corpus, synthetic fixtures,
human decisions or publication behavior changed. No contact, purchase or push.
Validation: `npm run library:catalog` returned 291 books / 14 groups / 56 findings;
`npm run test:web` passed all 4 tests in 382.428 ms. `node --check web/library.js`,
`git diff --check` and `git diff --exit-code -- config sources src tests` passed
(exit 0). `git check-ignore` confirmed the anthology PDF is private/ignored.
No Python suite was rerun because Python source and schemas were unchanged.

## Personal research library — 2026-11-14

Read PROGRESS/NEXT_STEPS/git status; preserved the uncommitted local viewer.
Owner supplied 291 titles with attributions in 14 groups after asking for online
discovery and organised project storage, prioritising Herzegovinian/regional,
Bosnian, Croatian, Montenegrin, then Serbian Latin. Recorded the complete request
separately under library/. No new biblical book IDs, source admission, editorial
approval or publication authority was inferred. Existing five-book config and
empty production lock remain unchanged. No corpus/synthetic fixture was modified.

Ran a broad discovery pass: 73 calls with up to four queries, all 291 titles
represented. Saved query-to-book identities and 1,595 result-title/URL leads in
library/research/searches.json, omitting signed/token query URLs. Results are
shared at the batch level, contain noise and are explicitly unreviewed. The
combined language queries do not exhaust every language priority. No declaration
that missing translations do not exist or that a best translation was selected.

Added 40 inspected metadata/page observations for 39 requested works, including
16 KS chapter links, Buddhist texts/indices, identified Croatian translations,
and Bosnian institutional/catalogue leads. Null translator/edition/language
fields remain unresolved. Coverage notes retain selections, collections,
revised texts and commentary distinctions. Modern copyrighted texts remain links.
Search hits, library catalogues and publisher pages are not source rights clearance.

Actually downloaded only the free-distribution-labelled Dhammapada/Put
ispravnosti HTML by Čedomil Veljačić from Srednji put, fixed URL, redirect refusal,
timeout/size bound and unchanged bytes. 236222 bytes; SHA-256
45a11d52548e9b7a189f9e431616dcb68a601a1c4e45b6beb3dae18e15a3b72c.
Provider notice: "Samo za besplatnu distribuciju, kao dar Dhamme". Original credit
and HTML retained in ignored library/private/, outside corpus/reader/archives
and web access. Receipt in library/research/downloads.json records private-only
use, no publication clearance and no independent textual/rights assessment.
No other full work was downloaded; no purchase, contact, login or bypass.

The bounded read-only viewer now opens on Moja biblioteka: search, category/status
filters, 291 separate entries, checked metadata, external links and separately
expandable unreviewed batch leads. Safe DOM text rendering, HTTPS-only outgoing
links, no new third-party dependency. Private files remain unserved. The existing
project overview/docs and Python CLI remain available. No browser verification
was performed on this turn; earlier preview availability was false.

Actual commands/results: `node library/build-catalog.mjs` returned 291 books,
14 groups, 40 findings, 291 searched; `node library/download-dhammapada.mjs
--private` succeeded with the receipt above. `npm run test:web` passed all 3
offline integration/data checks (199.0087 ms), including retained request lines,
duplicate-title separation, query coverage, empty production lock and private
access denial. `node --check web/app.js` and `node --check web/library.js` passed;
`git diff --check` passed including the final notes. Final regression passed all
3 tests again (136.8565 ms); unchanged config/sources diff returned exit 0, and
git check-ignore confirmed the private HTML is ignored. Non-Latin discovery
headlines were replaced by neutral Latin labels with original URLs, without
transliteration; an additional assertion protects the Latin display boundary.
No Python code/schemas changed; no Python suite rerun in the missing .venv.
No commit, push, release, model API, cloud dependency or sharing was performed.

Latest local UI addition: 2026-11-14. Owner explicitly asked for a useful visual
interface with `npm run dev` / HTML/CSS. Added a bounded, optional read-only
Node standard-library server and plain browser UI under `web/`, plus private
root package.json scripts. No dependency install, Python package/schema change,
new source, editorial decision or publication. Production locks/gates unchanged.
The four pages show orientation, dated source findings, language direction and
ten allowlisted documents. Search reads document content; the dialog provides
heading navigation and literal safe-text rendering. The source count is read
from sources/lock.json, not inferred clearance. Private evidence, corpus,
synthetic data and reviewer writes are not exposed. Server binds loopback and
rejects foreign Host/Origin headers and non-GET methods. Symlink containment
is checked before reading allowlisted files. Node v24.11.1 / npm 11.6.2 observed.

Actual commands/results:
- `npm run test:web`: initial run failed the foreign-Host assertion because
  Node fetch did not transmit the overridden Host header. Replaced that request
  with raw Node http.get; rerun passed (1 integration test, including ten
  documents, home page, private/traversal denial, write/Origin/Host refusal).
- `node --check web/app.js`: passed, exit 0.
- `git diff --check`: passed, exit 0, including final documentation edits.
- `npm run dev`: original 5173 port was occupied; changed default to 5187.
  Watch restart successfully printed http://127.0.0.1:5187; owned server stopped.
- Host preview status returned available:false. No browser rendering, mobile
  layout or interaction verification claimed. Manual browser QA remains next.

Earlier attempt to run `.venv/Scripts/python.exe` during project orientation
failed because that interpreter is absent in this checkout. No Python tests
were rerun; the recorded 291-test baseline is historical, not today's result.
No install or environment repair was attempted. Git was clean before this work.
No commit, push, contact, release, model API, or cloud dependency was introduced.
This optional viewer does not change the single installable Python package/CLI.

Latest continuation: human terminal use is simplified with `.\jeb.cmd` / `jeb
work`, a numbered menu, status/source blockers, saved-work selection without
copying hashes, immutable reports/pager, explicit demo switching and one-command
offline checks. Current checks: **291 tests passed, 33 schemas valid, 21 installed
package checks passed**. Existing source/review gates, JSON commands, draft and
reader identities remain intact. Real admitted coverage and approvals remain
zero. Local commit `8a736d4` and its validation-only narrative/schema/private
source-audit work were preserved. The menu never submits decisions or approves.
Older archives/matching wheels remain available; no migration was performed.
Earlier session records are preserved; latest details follow at the end.

Version: 0.1.0-dev. **Phase 0 completed; Phase 1 working synthetic slice
implemented and tested. Real-source ingestion and the editorial pilot remain
blocked.** The project itself and five-book editorial work are not complete.

## Repository audit

The existing folder contained only `.git`, with no tracked files, commits or
AGENTS instructions in the project/ancestors. Git status was clean on unborn
`main`, tracking an absent `origin/main`. The existing remote is unchanged:
`https://github.com/Lomuss33/Jugoslavenska-Ekumenska-Biblija.git`.
No nested repository, commit, push, history rewrite, site publication or release
was made. All new project files remain local/uncommitted for GitHub Desktop review.

## Implemented and recorded

- Charter, rights/source audit, editorial policy, terminology, exact collection
  decision, contributor rules, license matrix and three decision records.
- Source register with discovered URLs and missing fields explicitly unresolved;
  empty production lock and independently written evidence inspection log.
- Installable Python CLI, 14 packaged schemas, hash-locked minimal dependencies,
  safe source admission/acquisition, limited transcript adapter, exact source
  spans, immutable records, NFC/LF differences and quarantine diagnostics.
- Manual bounded modernization packets, strict returns, unapproved import,
  readable review reports, exact-hash human-owner decisions, explicit
  supersession, separate knowledge approval/dependencies and release refusal.
- Versioned JSONL relationship validation, deterministic reader JSON/Markdown,
  independent text/annotation coverage, approved aliases and rebuildable SQLite.
- An isolated original synthetic demonstration and offline security/editorial
  tests. Windows/Linux CI is configured with read-only permissions and pinned
  Actions; it has not run remotely because nothing was pushed.

Actual implementation paths: `src/jeb/`, `src/jeb/schemas/`, `config/`,
`sources/`, `tests/`, `.github/workflows/ci.yml`, `requirements.lock`, `docs/`.
No frontend, cloud service, model API key, paid credit or automated chat session.

## Source and exact coverage status

| Source | Status | Historical artifact hash |
| --- | --- | --- |
| crosswire-srkdijekav | needs_review | null; not downloaded |
| ebible-srp1865 | needs_review | null; not downloaded |
| ebible-hrv-saric | excluded | null; not downloaded |

Only preliminary DE and US legal references were inspected; neither exact-edition
assessment is complete. BA/HR/RS/ME country assessments have not been performed.
The eBible displayed Genesis sample is Latin/Ekavian; that is not a full artifact
audit. Supplied scholarly PDF leads returned HTTP 418. ZIP research fetches
reported unsupported binary content. No alternate download bypassed the gate.
Full findings and limitations: `docs/SOURCE_AUDIT.md` and
`sources/evidence/initial-audit.json`. No legal sign-off is claimed.

**Real source text, complete source books, modernized passages, evidence-bank
claims and owner text/name/note approvals: zero.** Real coverage for each of GEN,
MAT, MRK, LUK and JHN is zero. The exact five pilot passages have not been
ingested, modernized or reviewed.

The demo has **four synthetic GEN-labelled segments** (1, 2a, 3-4, 5), including
alternate labels, multiline text, nested notes, heading, cross-reference and
poetry. These are non-scripture sentences and do not count as Genesis coverage.
No complete book or real human approval is implied. Fictional scope ZZ is test-only.

Synthetic fixture SHA-256:
`620cbcdeeb78e462ce5a584084aed0358f5132ee108de22729322d2de5637b50`

Generated local artifacts (all under ignored `dist/demo/`):

- `exports/reader.json` SHA-256
  `c671d2838aff3c6fb507323c19081bbc3b77cbae7c5e86434bed609299b23b43`.
- `exports/reader.md` SHA-256
  `07278218ea0d46266172454e20f1ef111462c0eed4eae0d0cb4743657fd9ade9`.
- `reports/review.md`: source, unapproved local fixture proposal, diff, rationale,
  flags and exact hashes. It does not record a model run or human sign-off.
- `data/batches/fixture-modernize-v1/input.json` and synthetic returned JSON;
  proposal `fixture-modernize-v1-40b78ddaba32f24c` remains proposed.
- `data/index/search.sqlite3`; literal search for `covik` returns one synthetic match.

## Actual verification

Local platform: **Windows 11, CPython 3.13.3**. Final successful commands use
`.venv/Scripts/python.exe` (shown below as `python`):

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb demo
```

Results: lint clean; 23 Python files formatted; **14 schemas valid;
85 tests passed in 16.661 seconds**; production audit admitted_count 0; demo
produced four synthetic segments, zero real segments and zero owner approvals.
Actual machine-readable command/results are in `reports/verification.json`,
with complete offline test output in `reports/test-results.txt`.

The initial 73-test run found two Windows cleanup errors from unclosed SQLite
connections. Explicit connection closing fixed them; expanded final tests pass.
The tests exercise mocked acquisition, bad/changed files, excluded/contextual
sources, archive path/link/size defenses, structure/coverage, Unicode, proposal
scope/hash/evidence/name rejection, exact review hashes, independent note review,
stale dependencies, repeated export bytes and actual CLI exit codes.

Also actually performed:

```text
python -m pip wheel --no-build-isolation --no-deps --wheel-dir dist/wheels .
python -m venv dist/verify-venv
<clean-python> -m pip install --require-hashes -r requirements.lock
<clean-python> -m pip install --no-deps <built-wheel>
<clean-python> -I -m jeb --version
<clean-python> -I -m jeb validate --stage schemas
<clean-python> -I -m jeb demo
<clean-python> -I -m jeb --root dist/demo --synthetic search --source synthetic-v1 --query covik
<clean-python> -m pip check
```

The final rebuilt wheel was reinstalled with `--force-reinstall --no-deps` after
the last gate correction. Import location was its clean `site-packages`, not an
editable checkout; all 14 schemas, original fixture and license notices shipped.
Installed demo hashes matched the editable run. `pip check` reported no broken
requirements. `reports/package-verification.json` records the final wheel's
hash and isolated CLI results. Wheel bytes are not the deterministic corpus
contract; the reader artifact hashes above are.

No Linux runtime execution, remote CI result, successful live historical fetch,
USFM/SWORD conversion, expert review or legal approval is claimed. Passing tests
establish software behavior only. No source-rights date automatically unlocks text.

## Unfinished work and decisions

1. Establish an exact historical edition/digital artifact and rights across the
   configured scope, then evaluate its real parser/export toolchain and lock it.
2. Prepare only the five specified eligible pilot passages; seek owner review of
   actual wording, inflections, covik/čovik options, hljeb/kruh contexts and names.
   The literal forms and five-book inclusion decision are already recorded.
3. Implement separate evidence-research, annotation and review packet types;
   add expert meaning-sensitive approval and richer scholarly authoring schemas
   only with real evidence and documented participation.
4. Preserve eligible approved source/packet/proposal snapshots in a permitted
   reproducible archive before any later release. Nothing currently qualifies.
5. Scale only these five books after measuring actual pilot review effort. Later
   EPUB/PDF/web releases need separate work and publication authorization.

No new owner decision is required to preserve this completed local slice.
Unresolved orthographic/name decisions should be presented with concrete
eligible sample options when the source gate permits them. Next task is in
`NEXT_STEPS.md`; continue there instead of regenerating the foundation.

## Continuation 1: exact-source investigation and readiness reporting

Resumed after reading this log, NEXT_STEPS, AGENTS and Git. All foundation files
were still local/uncommitted. No owner work or editorial decisions were removed.

Actually retrieved only two non-scripture evidence artifacts into the ignored
private evidence cache:

- CrossWire's separately discovered `srkdijekav.conf`: 910 bytes, SHA-256
  `67d1b3237912e57bb8c8300237dfdd39720f91b5e61faaa7ab568c315335fa1e`.
- Internet Archive catalogue metadata for `svetopismostaro00daniuoft`:
  174222 bytes, SHA-256
  `8c531f4f1b57667fd9bd8416aab4bcb4fac38f8fce0cf50a7f0a494b3a3aeb4c`.

Neither checksum is a scripture artifact hash. No module ZIP, scan, OCR,
scripture PDF/EPUB, or historical verse was acquired. Production lock stays empty
and all three source artifact hashes/sizes stay null. GEN/MAT/MRK/LUK/JHN real
source and approved coverage are each zero. All prior synthetic demo reader
hashes and its unapproved proposal ID reproduce unchanged.

Primary findings: configuration declares zText/OSIS, **Calvin** versification,
headings and NoParagraphs; TextSource and print-edition linkage are absent.
The public contact field does not establish the transcriber. Provider news
supports release date only. A specific 1868 catalogue item is now identified,
but no evidence connects it to the module. Its metadata has degraded contributor
strings, language code chu and null rights/license fields. Mirrors repeating
the same module About/history are not independent corroboration.

Provider toolchain documentation warns that mod2imp skips link entries and
cannot guarantee a lossless round trip. No SWORD binaries were executed, no
adapter approved and no historical fidelity test performed. The next toolchain
evaluation must preserve linked/empty entries, raw markup, headings and exact
source mappings instead of trusting a plain-text verse count.

Rights research progressed to official HR current-law/BA/RS general-term
references. Those artifact-level rights remain unresolved. ME's official law
link was located, but its Word text was not inspected; current-law/term review
remains not_assessed. The earlier DE/US work is still preliminary. No jurisdiction
is claimed fully cleared and no human legal sign-off occurred. Šarić remains
excluded; CrossWire and eBible srp1865 remain needs_review.

New/changed concrete paths:

- `sources/assessments/crosswire-srkdijekav.json`: ten linked evidence records,
  separate metadata identities, five unresolved admission checks, six questions.
  `sources/registry.yaml` now records these findings and official country leads.
- `src/jeb/source_assessment.py`, `src/jeb/schemas/source-assessment.json`,
  `src/jeb/sources.py`, `src/jeb/cli.py`: offline `jeb sources inspect --source
  crosswire-srkdijekav`, evidence validation, stale/orphan rejection and explicit
  historical edition/provenance/components/versification/adapter admission gates.
- `src/jeb/parse/transcript.py`: rejects a scheme different from the assessed source.
- `tests/test_source_assessment.py`, updated CLI schema test and CI inspection step.
- `docs/sources/CROSSWIRE_PROVENANCE.md`, `docs/sources/CROSSWIRE_QUESTIONS.md`,
  decision 0004, and targeted README/data-model/rights/architecture/continuity edits.

Actual final local verification (Windows 11 / Python 3.13.3):

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb demo
```

Results: lint/format clean (25 Python files), **15 schemas valid, 98 tests passed
in 17.761 seconds**, production admitted_count 0, 16 reported admission blockers,
and unchanged synthetic JSON/Markdown hashes. An initial focused test missed the
fixture's historical-mode allowlisted URL; the test fixture was corrected
without weakening the URL gate. Full regression and final formatting pass.

Machine-readable results: `reports/source-followup-verification.json`;
complete test output: `reports/source-followup-tests.txt`;
current inspection: `reports/crosswire-source-readiness.json`.

Rebuilt the wheel, reinstalled it into the existing clean hash-locked verification
venv, and used Python `-I` to verify installed imports, all 15 schemas, real
candidate inspection (admitted false, corpus hash null), deterministic demo and
`pip check`. Results: all passed; `reports/source-followup-package.json` records
the exact wheel hash and actual smoke commands. No Linux execution or remote
CI success is claimed.

Research limitations: mailing-list index inaccessible through the research tool;
Archive page/metadata web fetches failed but bounded metadata-only retrieval
succeeded; ME document page timed out and linked Word content was unsupported
in web research. An initial console print of UTF-8 config metadata hit Windows
cp1252 output encoding; exact saved bytes were then inspected via UTF-8 output.
No failed request or print is represented as a successful corpus operation.

The question draft is concrete but **unsent**. No email/contact, commit, push,
site publication, release, paid service or model API call was made. Next useful
external evidence is the original digital-source/edition/correction record;
do not repeat the completed metadata searches or promote a source to bypass it.

## Continuation: synthetic native SWORD evaluation — 2026-10-30

Completed the independent toolchain task using original technical sentences.
No candidate scripture artifact was acquired, compared, parsed or admitted.
The configured collection is unchanged: GEN/MAT/MRK/LUK/JHN each have **zero
real source segments, complete source books, modernized passages and human
approvals**. CrossWire and eBible srp1865 remain needs_review; Šarić remains
excluded. The production source lock is empty. Phase 1 remains demonstrated
with synthetic data, and the real five-book editorial pilot is still blocked.

Retrieved the official SWORD 1.9.0 **software** archive, 2,606,652 bytes, SHA-256
`42409cf3de2faf1108523e2c5ac0745d21f9ed2a5c78ed878ee9dcc303426b8a`.
Native GCC/G++ 13.2.0 / CMake 4.0.2 / Ninja builds succeeded locally, first
manually and then through a fresh extraction with the new optional CLI builder.
The archive and native outputs remain ignored under `dist/`. Upstream example
material was not used as corpus input. The complete upstream GPL license and
three derivative portability/offline patches retain separate licensing.

New implementation and evidence:

- `toolchains/sword-1.9.0/`: exact patch diffs and before/after descriptors,
  original MIT probe source, two actual Windows executable locks and instructions.
- `src/jeb/sword_build.py`, `src/jeb/sword_diagnostic.py`, CLI `toolchain
  build/evaluate/validate`, and two additional packaged diagnostic schemas.
- `src/jeb/assets/sword-synthetic.imp`: eight invented input entries, SHA-256
  `b58fa820857a6ba89ec20cf4687b031c7ade30898ce6a49bdceb6c8dc1ae92f3`.
  Ten requested slots include two introductions, one empty slot, one linked
  alias and independent identical wording. They are not ten biblical verses.
- `tests/fixtures/sword/`: actual native capture, reserialized JSONL and its
  provenance. `tests/test_sword_diagnostic.py`: thirteen new offline tests.
- `docs/sources/SWORD_TOOLCHAIN_EVALUATION.md`, decision 0005, updated candidate
  dossier, license matrix/NOTICE, README, architecture, CI and continuity notes.
- `reports/sword-toolchain-build.json`, `reports/sword-toolchain-evaluation.json`:
  actual build commands/return codes and measured native results.

Measured limitations matter for the next adapter. This mod2imp build emits both
bridge keys as repeated wording without link identity; it does not drop the
synthetic alias as older documentation warns. mod2osis omits book/chapter
introductions and emits Bible.KJV metadata for the declared Calvin module.
getRawEntry prepares whitespace rather than preserving stored bytes, and imp2vs
adds a final LF at EOF. The probe independently preserves actual stored markup,
presence and requested-key links; it cannot reconstruct lost historical layout.
Both native builds produced identical probe stdout SHA-256
`034dc398d555241f8b01ffc319ec0af2b21feb3a5130ad60390f8ce4d1e6da1d`.
This is fixed-fixture evidence only; no historical adapter was approved.

Actual optional native commands (existing compiler/CMake/Ninja installation):

```text
python -m jeb toolchain build --archive dist/toolchains/sword-1.9.0/sword-1.9.0.tar.gz --output dist/sword-tools-rebuild --compiler C:/Strawberry/c/bin/g++.exe --c-compiler C:/Strawberry/c/bin/gcc.exe
python -m jeb toolchain evaluate --lock dist/sword-tools-rebuild/toolchain.lock.json --tools dist/sword-tools-rebuild/build/utilities --output dist/sword-evaluation-final
```

Actual final offline checks, Windows 11 / CPython 3.13.3:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
```

All passed: lint clean, 28 Python files formatted, **17 schemas valid, 111 tests
passed in 24.834 seconds**, admitted_count 0 and the same sixteen candidate
admission blockers. Machine results: `reports/sword-diagnostic-verification.json`;
full test output: `reports/sword-diagnostic-tests.txt`; current candidate
inspection: `reports/crosswire-readiness-after-sword.json`.

Built a wheel locally with `--no-index --no-build-isolation --no-deps`, reinstalled
it into the existing clean hash-locked verification venv, then used Python `-I`
to check installed imports, all seventeen schemas, the synthetic diagnostic,
uncleared candidate inspection and unchanged deterministic demo. `pip check`
passed. The wheel includes the IMP asset and notices, with no native binaries.
The wheel SHA-256 is
`db59eff906bce639db9acc68f6de815d3b1729a7c79505db68bbbd4ba1e6a137`;
actual smoke results are in `reports/sword-diagnostic-package.json`.
The demo's four original segments and both reader hashes are unchanged.

Initial native attempts exposed Win64 pointer casts and legacy FTP callbacks;
the tracked patches resolve the tested profile without -fpermissive. Initial
PowerShell argument splitting was replaced with subprocess argument lists.
Upstream integer/pointer and bundled-regex compiler warnings remain in logs;
this is not a general engine security audit. A focused test draft initially had
lint formatting issues, corrected before the successful full run. No Linux or
remote CI execution is claimed. Capture/source/toolchain bindings, every patch
hash and all license hashes were also checked directly after the full suite.

All files remain local and uncommitted on unborn main; the Git remote is
unchanged. No provider message, push, publication, release, paid service or model
API call occurred. Next external evidence is still the original digital source,
exact edition and correction/component history. See NEXT_STEPS; do not repeat
the completed metadata searches/native experiment as a substitute for lineage.

## Continuation: submission records and source research packets — 2026-10-30

Continued the missing digital-lineage task without repeating the native build or
acquiring a scripture artifact. Following the official list-info/archive links
made the previously inaccessible public mailing-list index readable. Inspected
three primary posts individually: the 2017 SrKDIjekav upload notice, the adjacent
SrKDEkavski notice and a 2014 development post about two unnamed Serbian texts.

The Ijekavian notice credits the unexpanded string Br; the separate Ekavian
notice credits Tomas. Neither identifies an exact print edition or transcriber
role. Generic automatic update wording does not prove an earlier revision, and
the unnamed 2014 texts are not established ancestors. No people identities or
roles were inferred from unrelated search matches. Three private HTML metadata
snapshots and independent summaries are recorded in
`sources/evidence/crosswire-submission-research.json`; the dossier now links
fourteen evidence records. Metadata hashes were checked against saved bytes.

No source registry record, transcriber field or production source lock changed.
CrossWire and eBible srp1865 remain needs_review; Šarić remains excluded. All five
CrossWire dossier checks remain unresolved, with sixteen admission blockers.
No new country/legal assessment or human review occurred. **GEN/MAT/MRK/LUK/JHN
each still have zero real source passages, complete source books, modernizations,
knowledge claims and owner text/name/note approvals.** Phase 1 remains a working
synthetic slice; the real pilot and project are not complete.

Implemented a directly useful independent step for this research:

- `src/jeb/source_research.py` and CLI `sources research prepare/validate/import/
  report`: manual metadata packets, bounded returns, unreviewed staging and
  readable reports. No network, model API, scripture acquisition or contact.
- Two packaged schemas, bringing the total to nineteen. Source/dossier, scope,
  rights policy, prompt, response schema and exact question coverage are bound.
  Imported findings cannot change source admission or create human approval.
- `tests/test_source_research.py`: fifteen offline tests covering changed/stale
  inputs, substituted prompts/schemas, invented IDs, broken lead references,
  duplicate imports/URLs, context limits, script, approval claims and source
  immutability. Changed imported canonical content is detected.
- `.gitignore` now excludes working source-research artifacts. CI includes offline
  packet preparation. README, data-model/architecture/rights docs, decision 0006,
  the manual research guide and the unsent provider questions were updated.
- `docs/sources/CROSSWIRE_SUBMISSION_HISTORY.md` records primary URLs, identities,
  uncertainty and the concrete handoff without treating upload credits as authors.

Actual workflow demonstration used the real archive observations. Prepared
`cw-submission-history-01` (31,855 bytes), validated its five question responses
and three archive leads, imported them as unreviewed and rendered
`reports/crosswire-submission-review.md`. Its canonical response SHA-256 is
`6dbc911f3d156493be491b357b5c2aa8d425201aa14260d73e9ac5c59aa41ceb`.
Separately indexed the already inspected metadata in the unresolved dossier by a
local Codex edit, without changing any verified status or claiming human review.
The CLI then correctly rejected the earlier response as stale (exit 2, no
traceback). The historical report remains available; it is not the current input.

Prepared a fresh follow-up at
`data/source-research/cw-lineage-followup-01/input.json`, **35,033 bytes** and five
unresolved questions. Its canonical packet identity is
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
`reports/source-research-workflow.json` records actual preparation/staging and the
expected stale-result rejection. This packet is ready for manual subscription
use or further authorized public metadata research; it grants no contact or
corpus permission.

Actual final local commands, Windows 11 / CPython 3.13.3:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb sources research prepare --source crosswire-srkdijekav --packet-id cw-lineage-followup-01
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
```

All passed: lint clean; thirty Python files formatted; **19 schemas valid;
126 tests passed in 28.577 seconds**. The initial fourteen focused tests also
passed; the size-limit test was then added and included in the successful full
run. The four-segment synthetic demo, proposal and both reader hashes are
unchanged. No native rebuild or historical fidelity claim was repeated.
Results: `reports/source-research-verification.json`; full output:
`reports/source-research-tests.txt`; current source inspection:
`reports/crosswire-readiness-after-submission-research.json`.

Built/reinstalled the wheel locally with no index, no build isolation and no
dependency resolution into the existing clean hash-locked verification venv.
Using Python `-I`, checked installed imports, all nineteen schemas, current
packet preparation, all four new commands in an isolated metadata smoke root,
the stale historical response rejection, unresolved source inspection and the
unchanged demo. `pip check` passed. All smoke source files were unchanged; no raw
corpus or approval directory was created. The wheel includes the new module and
schemas and no native binaries. Wheel SHA-256:
`d09effceda4b4cea788aa1a9fa98aab7927f6a0ad7d73646a7894b677b27bac6`.
Actual commands/results: `reports/source-research-package.json`.

Limitations: structurally valid new URLs may still be fabricated or unhelpful;
the offline validator does not inspect their claims. All leads remain unreviewed
and require actual evidence inspection. No Linux or remote CI execution is
claimed. Source bytes/edition/transcriber/components and intended-use clearance
are still missing; none can be inferred from upload-template wording.

All changes remain local/uncommitted on unborn main with the existing remote.
No provider message, commit, push, publication, release, paid service, model API
call or chat automation occurred. Continue with the ready current packet and
the specific original-source/role questions in NEXT_STEPS. Do not repeat the
completed upload-notice/index searches as new independent lineage evidence.

## Continuation: optional AI review assistance — 2026-10-30

Read continuity/Git and checked a bounded set of remaining public source-history
leads. No new inspectable primary edition/transcription record was established.
Source-tree and Gentoo package metadata endpoints were inaccessible through web
research; repeated provider/downstream metadata did not resolve the lineage.
Exact queries, failed metadata endpoints and limits are recorded in
`sources/evidence/lineage-search-followup.json`. No checksum or mirror was
substituted for a source identity. This is not an exhaustive-search claim.

Kept the source register, fourteen-record CrossWire dossier, empty production
lock and current metadata research packet unchanged. CrossWire and eBible
srp1865 remain needs_review; Šarić remains excluded. All five dossier checks and
sixteen admission blockers remain unresolved. **Real coverage for GEN, MAT,
MRK, LUK and JHN is still zero**, with no complete source book, modernization,
approved knowledge claim or owner text/name/note approval. No historical artifact
was acquired or parsed. Phase 1 remains demonstrated with original synthetic data.

Continued the explicitly requested but missing review packet type independently:

- `src/jeb/review_assistance.py` and `jeb review assist prepare/validate/import/
  report`: bounded optional AI critiques of an existing validated proposal.
- `review-assistance-packet` and `review-assistance-response`: two additional
  packaged schemas, bringing the total to twenty-one. Exact source/proposal/
  policy/evidence snapshots, prompt/schema and ordered segment/flag coverage bind
  the work. Evidence locators and underlying record hashes are included without
  copying potentially restricted external evidence text bodies.
- Critiques cannot rewrite text, clear existing flags, attest human review,
  change human decisions or grant approval. Meaning-sensitive items retain
  expert escalation; D-class owner approval remains blocked. Each imported
  response is separate, immutable, unreviewed and content-hashed.
- `tests/test_review_assistance.py`: eighteen offline tests covering source
  eligibility, stale/substituted inputs, exact hashes/IDs, evidence changes,
  flag preservation, expert escalation, null unresolved text, impersonation,
  bounds, safe reports, duplicate/competing critiques and unchanged reader/owner
  decisions. Simulated human decisions stay inside temporary synthetic tests.
- `docs/REVIEW_ASSISTANCE.md`, decision 0007, targeted README/review-guide/
  architecture/data-model/continuity updates, ignored working critiques and
  offline CI preparation/validation of the cached original example.

An actual Codex critique compared the four original non-scripture proposal
segments. It retained one open linguistic question about mijenja/prepravlja in
the first invented sentence. Negation, quantity and the selected literal covik
remain unchanged; this is an observation for owner inspection, not approval or
a certified equivalence judgment. The other three proposals equal their
normalized fixture source. No historical passage or external evidence was
invented, and no human or expert participation was claimed.

Concrete current artifacts:

- `dist/demo/data/review-assistance/fixture-review-v1/input.json`: 32,414 bytes;
  packet identity
  `bcad69b64a11b7ddd9bc9178a014d89c3db98f6ed54fa711c6632f310bfecf7b`.
- `reports/review-assistance-synthetic-response.json`: actual unreviewed critique;
  canonical response hash
  `4a86b521b1abe6d24e47971032e6ebbfd0f8752eba88f77f6a158e19ce2abbc2`.
- `reports/review-assistance-synthetic.md`: readable source/proposal/diff and
  critique report, copied unchanged from the actual CLI output.
- `reports/review-assistance-workflow.json`: actual preparation, validation,
  import/report commands and unchanged proposal, linguistic flag and reader hash.

Actual final local commands, Windows 11 / CPython 3.13.3:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb sources research prepare --source crosswire-srkdijekav --packet-id cw-lineage-followup-01
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
python -m jeb --root dist/demo --synthetic review assist prepare --proposal fixture-modernize-v1-40b78ddaba32f24c --packet-id fixture-review-v1
python -m jeb --root dist/demo --synthetic review assist validate --input reports/review-assistance-synthetic-response.json
```

All passed: lint clean; thirty-two Python files formatted; **21 schemas valid;
144 tests passed in 37.460 seconds**. The eighteen focused tests passed in
16.504 seconds. Results: `reports/review-assistance-verification.json`; full test
output: `reports/review-assistance-tests.txt`; current source inspection:
`reports/crosswire-readiness-after-review-assistance.json`.

Built/reinstalled a local wheel with no index, build isolation or dependency
resolution into the existing clean hash-locked verification venv. Python `-I`
checks verified installed imports, twenty-one schemas and all four new commands
in a fresh isolated synthetic workspace. The cached critique/report reproduced;
`review apply` correctly rejected the AI response (exit 2 without traceback),
and synthetic release stayed blocked. No approval directory was created. The
proposal and source-only reader bytes stayed unchanged. The current lineage
packet still has identity
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
Production admitted_count remains 0 and `pip check` passed. The wheel includes
the new module/schemas and no native binaries. Wheel SHA-256:
`ce86fc90d94b1b4ded95748151364053189fba0e96cb62ca40c222d1238a2341`.
All fifteen installed-wheel commands/results, including expected gate rejections,
are in `reports/review-assistance-package.json`.

The original synthetic demo still has four source segments, zero real segments
and zero owner approvals. Its JSON/Markdown reader hashes and original proposal
ID are unchanged. No source-rights policy, editorial-policy input or existing
owner decision was modified. A critique is advisory, cannot authenticate a
reviewer and cannot certify factual or semantic fidelity. No Linux or remote CI
execution is claimed; CI is configured for both platforms but has not been pushed.

All files remain local/uncommitted on unborn main; the existing Git remote is
unchanged. No contact, commit, push, publication, release, paid service, model API
call or chat automation occurred. Next independent implementation is bounded
passage evidence-research/annotation packets with unapproved knowledge staging.
Real-source work still needs the original digital file and exact edition/roles/
correction/component evidence. Preserve the ready metadata packet and resume
that investigation on a new primary lead rather than recycling completed searches.

## Continuation: passage research and annotation staging, 2026-10-30

Completed the next independent task in NEXT_STEPS. All four requested manual
packet types now exist: modernization, optional AI critique, passage research
and annotation. Source-metadata research remains a separate permission-free
investigation workflow. No real biblical source is cleared or ingested.

Implemented and documented:

- `src/jeb/knowledge_packets.py`, `jeb knowledge prepare/validate/import/report`
  and three new packaged schemas: passage-work-packet,
  passage-research-response and annotation-response. One exact pilot passage
  or the opt-in original fixture per packet; 64 KiB input and 32 KiB return.
- Shared exact passage/context selection in `batch.py` and side-effect-free
  canonical-plus-draft graph checks in `knowledge.py`. Existing modernization
  and critique packet identities remain unchanged.
- Current reader wording, eligible source/context, exact hashes, policies,
  approved names, registered bibliography and scoped knowledge metadata bind
  each packet. External evidence text bodies are not copied. Stale, rejected
  or unbound transitive support cannot be used as current evidence.
- Typed research leads and attributed evidence/claim/annotation drafts. Exact
  scope, ordered complete coverage, current display dependencies, typed links,
  ID collisions, fabricated registered references, self/circular support,
  unsupported script and impersonated approvals are rejected. Explanations,
  reflection and fiction remain separate; zero leads/drafts is valid.
- Immutable unreviewed responses under ignored `data/knowledge-proposals/`,
  with safe readable reports. No canonical bank, human decision, name mapping,
  rights assessment, source lock or reader is changed by import.
- `docs/PASSAGE_KNOWLEDGE_WORKFLOW.md`, decision 0008, current README,
  data-model, architecture, review-guide and CI instructions. Rich structured
  entity/event/story authoring and human knowledge promotion remain future work.

Actual Codex-assisted fixture work, without invented human participation:

| Protocol | Packet ID | Packet bytes | Result |
| --- | --- | ---: | --- |
| research | fixture-passage-research-v1 | 23,978 | four items, zero new bibliographic leads |
| annotate | fixture-annotations-v1 | 29,993 | four items, five unapproved drafts |

Packet identities:

- Research: `bbef75dfe9cf9b5b8b7e4eba999e0dc54fb3f11fb71fbaf940daad0398af7671`.
- Annotation: `15c31c623cc1ebb50149c30af94eef199585da150945a200225ba8813fbabe7d`.

The five drafts are original fixture evidence, a textual claim, an explanatory
note, an attributed AI-assisted reflection and an explicitly fictional note.
They concern only four invented non-scripture sentences. The fixture-witness
record supplies no independent historical corroboration. The owner voice is not
claimed. All five remain outside the canonical bank and reader, with null
approval. Actual returns and reports are preserved at:

- `reports/passage-research-synthetic-response.json` and
  `reports/passage-research-synthetic.md`.
- `reports/annotation-synthetic-response.json` and
  `reports/annotation-synthetic.md`.
- `reports/knowledge-packets-workflow.json`: actual eight preparation,
  validation, staging and reporting commands, response hashes and output hashes.

The first installed-wheel check exposed a genuine Windows failure: an atomic
rename to a 270-character response filename raised WinError 3. The earlier
wheel and failed workspace are retained. Read-only inspection found
LongPathsEnabled=0. Core bounded reads, atomic writes, containment symlink
checks and all four response-import duplicate checks now use absolute Windows
extended-length paths internally. Stored project paths retain their spelling;
no registry or other machine setting was changed. Two Windows regressions cover
long-path immutable writes and actual annotation import/read/report/duplicate
rejection. This does not assert compatibility for every optional native tool.
Failure record: `reports/knowledge-packets-package-attempt.json`.

Final local verification: Windows 11 / CPython 3.13.3, using the existing
hash-locked `.venv`. Actual commands include:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb sources research prepare --source crosswire-srkdijekav --packet-id cw-lineage-followup-01
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
python -m jeb --root dist/demo --synthetic review assist prepare --proposal fixture-modernize-v1-40b78ddaba32f24c --packet-id fixture-review-v1
python -m jeb --root dist/demo --synthetic review assist validate --input reports/review-assistance-synthetic-response.json
python -m jeb --root dist/demo --synthetic knowledge prepare --source synthetic-v1 --selection fixture --task research --packet-id fixture-passage-research-v1
python -m jeb --root dist/demo --synthetic knowledge prepare --source synthetic-v1 --selection fixture --task annotate --packet-id fixture-annotations-v1
python -m jeb --root dist/demo --synthetic knowledge validate --input reports/passage-research-synthetic-response.json
python -m jeb --root dist/demo --synthetic knowledge validate --input reports/annotation-synthetic-response.json
```

All passed: lint clean, **34 Python files formatted, 24 valid schemas, 164 tests
passed in 46.180 seconds** (18 new packet tests and two Windows regressions).
The two focused Windows regressions also passed in 0.829 seconds. Complete final
outputs and source/test fingerprints are in
`reports/knowledge-packets-final-verification.json` and
`reports/knowledge-packets-final-tests.txt`. The earlier 162-test check is kept
in `reports/knowledge-packets-verification.json` as an intermediate snapshot.
No Linux execution or remote CI run is claimed.

Built the fixed wheel offline with `pip wheel --no-index --no-build-isolation
--no-deps`; reinstalled it into the existing clean verification venv with no
dependency resolution. All **24 installed-wheel checks passed** in a new deeper
`dist/verify-knowledge-base-v2/dist/demo` workspace. Python `-I` verified actual
site-packages imports and all 24 packaged schemas. Both prepare/validate/import/
report workflows reproduced the recorded packet and report hashes; staged paths
were 273 and 268 characters, duplicate imports failed cleanly, and imported long
files were readable and valid. AI-as-human review and synthetic release were
correctly rejected with exit 2 and no traceback. No approval/release file was
created; canonical records stayed zero and `pip check` passed. The wheel contains
no native binaries and retains the separate license files. Full actual command
output: `reports/knowledge-packets-package.json`. Fixed wheel SHA-256:
`20dafca3899ce0d23061b2f748bc3bc3d5094f276c1500ed4d1cbeaa361c33a1`.

Historical status remains unchanged: CrossWire SrKDIjekav and eBible srp1865
need review, Šarić is excluded, production lock is empty, and all five exact
pilot passages and complete books have **zero real coverage**. CrossWire still
has fourteen evidence records, five unresolved checks and sixteen admission
blockers. The current lineage packet remains
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
Owner text/name/note approvals and approved knowledge records remain zero.
Synthetic reader JSON stays
`c671d2838aff3c6fb507323c19081bbc3b77cbae7c5e86434bed609299b23b43`;
Markdown and the original modernization proposal are unchanged. No editorial
policy or rights-policy input bytes were changed.

Current Git inspection shows existing commit `0dac5e8` (1st update) on main;
earlier unborn/uncommitted statements above are historical snapshots. This
continuation did not create a commit or push. The existing SWORD pointer-patch
worktree edit was preserved, and the remote is unchanged. Source/schema/example
files from this milestone are present in the current baseline; the Windows fix,
new verification records and continuity edits remain local changes for review.
No contact, publication, release, paid service, model API or chat automation.

Next independent task: a provenance-preserving human knowledge review and
promotion workflow for these staged packages. It must keep source facts,
AI-assisted attribution, exact dependencies and independent text/note approval
intact, reject stale/conflicting packages, and never invent owner participation.
No new owner decision is required for that reversible engineering work.
Real-source pilot work still requires new exact-edition/lineage/component/rights
evidence; preserve the prepared metadata handoff instead of repeating old leads.

## Continuation: human knowledge review and canonical receipts, 2026-10-30

Completed the next independent task from NEXT_STEPS without generating an owner
decision. The persistent five-draft synthetic package is still unreviewed; no
record was promoted in the production or persistent demo workspace.

Implemented:

- `src/jeb/knowledge_review.py` and `jeb knowledge review export/validate/apply`.
  Export is an unsigned readable review subject with exact packet, response,
  policy and draft-envelope hashes, current text, AI credit, tool, uncertainty,
  locators and recorded review states. It creates no reviewer fields or approval.
- Two additional self-contained schemas: `knowledge-review-decisions` and
  `knowledge-review-receipt`, bringing the total to twenty-six. A separate actual
  owner decision must attest human participation and explicitly check content/
  scope, attribution, category/uncertainty, actual support inspection and
  contribution rights. The system cannot authenticate the person, certify facts,
  supply expertise or waive third-party rights from these fields.
- One atomic, immutable canonical-content-hashed receipt per complete submitted
  review, under ignored `data/knowledge-reviews/<review-id>/<receipt-hash>.json`.
  It embeds the entire original packet, response and human decision. Canonical
  validation combines legacy JSONL with deterministic approved projections from
  these receipts. There is no partial multi-file copying of approved records.
- Optional provenance in `knowledge` and `reader` schemas: exact AI attribution,
  tool/rationale, packet/response/draft/decision identities, source-corpus/policy/
  bibliography hashes and support bindings. Approval hashes cover this provenance.
  Original annotation-response schema and earlier packet bytes remain unchanged.
- Full current evidence/claim/entity/related closure for approval. Closed partial
  groups can be promoted and resumed from the same exact staged response; the
  original packet is reconstructed while excluding only its own already verified
  projections. Normal AI imports keep the strict namespace/collision gate.
- Rejected and needs_review decisions are history only. Competing responses need
  explicit, acyclic, nonbranching supersession of pending/rejected heads for the
  same ID/book. Approved IDs and existing canonical records cannot be overwritten.
  Reflection and fiction retain their exact categories and credit after approval.
- Changed passage/context, policy, bibliography or exact supporting record hides
  affected notes and their transitive dependents. Historical receipts remain
  available; text approvals and source admission are independent. A receipt is
  sufficient to rebuild its approved projection after working caches are removed.

The first promotion workflow deliberately leaves approved IDs immutable.
Withdrawal and editorial selection among approved versions remain unimplemented;
a new approved version does not remove an earlier one. This limitation is explicit
in the guide and decision 0009, and is the next small engineering task.

Documentation: `docs/KNOWLEDGE_REVIEW.md`,
`docs/decisions/0009-preserve-human-knowledge-review-receipts.md`, README,
DATA_MODEL, ARCHITECTURE, REVIEW_GUIDE and PASSAGE_KNOWLEDGE_WORKFLOW. CI now
imports the original annotation package and exports its unsigned human-review
subject. No human decision is generated by the CI workflow.

Actual persistent demonstration:

```text
python -m jeb --root dist/demo --synthetic knowledge review export --packet-id fixture-annotations-v1 --response-sha256 2145bfcaf36f897f2cbcee25cd910f32c190ad845889d838d48e3f048bf296de --output reports/human-knowledge-review.md
python -m jeb --root dist/demo --synthetic knowledge review validate --decisions reports/annotation-synthetic-response.json
python -m jeb --root dist/demo --synthetic knowledge review apply --decisions reports/annotation-synthetic-response.json
python -m jeb --root dist/demo --synthetic validate --stage knowledge --source synthetic-v1
python -m jeb --root dist/demo --synthetic export --source synthetic-v1 --format json --maturity preview --output exports/after-knowledge-review.json
python -m jeb --root dist/demo --synthetic export --source synthetic-v1 --format json --maturity release --output exports/forbidden-knowledge-release.json
```

Export succeeded and created no human decisions. Both attempts to use the AI
annotation response as a human decision correctly failed with exit 2 and no
traceback. Knowledge validation returned zero canonical records; preview bytes
were unchanged; synthetic release correctly failed with exit 2 and no output.
These are observed gate checks, not an attempted human approval. No persistent
review receipt or owner approval was written.

The unsigned report was copied byte-for-byte to
`reports/knowledge-review-synthetic.md`, SHA-256
`67780651d88dc53156b449a5ce7438b6a22fe3ab5ea899b300e71952dd89f265`.
It covers all five original technical drafts, with exact individual envelope
hashes. `reports/knowledge-review-workflow.json` records the actual six commands,
expected refusals and zero approval/record counts. Existing annotation packet
identity remains `15c31c623cc1ebb50149c30af94eef199585da150945a200225ba8813fbabe7d`.

Actual local verification, Windows 11 / CPython 3.13.3:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb sources research prepare --source crosswire-srkdijekav --packet-id cw-lineage-followup-01
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
```

All passed: lint clean, **36 Python files formatted, 26 valid schemas, 186 tests
passed in 69.666 seconds**. Twenty-two added regressions cover closed and partial
promotion, rejected/pending history, competing responses, owner/check/hash/date
boundaries, stale policy/corpus/bibliography/support, original receipt integrity,
cache independence, approval attribution, reader/text separation, CLI decisions
and Windows long paths. All simulated attestations stay in temporary synthetic
test roots; no actual person or expert participated. Final actual commands,
outputs and code/schema/test fingerprints: `reports/knowledge-review-verification.json`;
full test output: `reports/knowledge-review-tests.txt`.

Prior research/annotation packets, optional critique and native diagnostic capture
were also revalidated successfully. The current lineage packet identity is still
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
No native build or repeated public-source investigation was needed.

Built the local wheel with `--no-index --no-build-isolation --no-deps` and
reinstalled it without dependency resolution into the existing clean verification
venv. **All 18 installed-wheel checks passed.** Python `-I` verified site-packages
imports, 26 schemas and the fresh deep synthetic workflow. Two targeted tests
using the installed package simulated successful CLI validate/apply and long-path
receipt reading/duplicate rejection only in automatically removed temporary roots.
The persistent fresh workspace imported its draft at a 272-character path,
reproduced the unsigned report, rejected AI-as-human validation/apply, retained
zero receipts and canonical records, reproduced the unchanged reader, and blocked
synthetic release. Production audit still admitted zero sources; `pip check`
passed. Full actual output: `reports/knowledge-review-package.json`. Wheel SHA-256:
`6f98601ac3adddc27901526b84f2105348fd360dddf1a85281a436d282b4bcdc`.
No native binaries are included, and separate license files are retained.
No Linux or remote CI execution is claimed.

Source status and coverage remain unchanged: CrossWire SrKDIjekav and eBible
srp1865 need review; Šarić stays excluded; the production lock is empty. CrossWire
has fourteen evidence records, five unresolved checks and sixteen admission
blockers. Real source text, pilot passages, complete books, modernized passages,
approved knowledge records and owner text/name/note approvals are all **zero**
for GEN, MAT, MRK, LUK and JHN. Four invented non-scripture source segments and
five staged drafts are the only persistent demonstration. Reader JSON remains
`c671d2838aff3c6fb507323c19081bbc3b77cbae7c5e86434bed609299b23b43`;
Markdown, original proposal, rights-policy and editorial-policy input bytes are
unchanged. No actual source artifact was acquired or parsed.

Preserved the existing worktree, prior Windows long-path fix, SWORD pointer-patch
edit and commit `0dac5e8`; the remote is unchanged. This continuation made no
commit, push, contact, publication, release, paid-service/model API call, machine
setting change or chat automation. Changes remain local for GitHub Desktop review.

Next independent task: exact-hash human withdrawal and version selection for
approved knowledge, preserving receipts and hiding dependent notes transitively.
Use temporary synthetic decisions only; the five actual demonstration drafts
must remain unapproved until real owner review. No new owner decision is needed
for that reversible implementation. The real editorial pilot still needs new
primary exact-edition/digital-lineage/component/rights evidence. Preserve the
prepared metadata handoff and do not recycle completed searches as new evidence.

## Continuation: knowledge withdrawal and version selection, 2026-10-31

Resumed the next independent task from NEXT_STEPS, preserving the prior worktree
and all editorial/source gates. User instructions reconfirmed the same five-book
scope and no fabricated human participation. No actual owner action was supplied
or generated. The five persistent demonstration drafts remain unapproved.

Implemented:

- `src/jeb/knowledge_curation.py` and `jeb knowledge curate export/validate/apply`.
  Reports are unsigned metadata subjects with exact record/approval/provenance
  bindings and no stored text bodies. Optional source eligibility is assessed
  honestly; blocked corpus display does not prevent a metadata report or an
  exact withdrawal of a previously approved subject.
- Two new self-contained schemas, `knowledge-curation-decisions` and
  `knowledge-curation-receipt`, bringing the total to twenty-eight. Separate
  actual-owner actions have explicit checks for identity/impact, resolved
  withdrawal reasons/current support, or comparison of alternatives. They do
  not grant source rights, expert participation, identity authentication or new
  wording approval.
- One atomic immutable content-hashed receipt under ignored
  `data/knowledge-curation/<action-id>/<receipt-hash>.json`, containing the owner
  decision and exact approved snapshots. Original records, approval receipts,
  attribution and passage decisions are never rewritten or deleted. Current
  heads require explicit acyclic/nonbranching supersession. Replays, conflicts,
  missing predecessors and filename-case action-ID collisions are refused.
- Withdrawals work with stale context/policy or a now-blocked source, provided
  intact canonical approval identities remain and the action binds the current
  policy. They hide their target and evidence/claim/entity/related dependents
  transitively. Reactivation requires the current withdrawal, a resolved-reason
  check, current eligible source/support and a compatible active version choice.
- Optional human approval-item `version_of`, bound to an exact already approved
  original, plus `revision_relationship_checked`. Type, book, layer/category and
  exact segment scope must match. The binding survives in canonical/reader
  provenance. Declared revisions remain withheld until explicitly selected;
  independent notes are not automatically inferred to be versions.
- Version groups bind at least two approved candidates, retain prior candidates
  and complete declared ancestry, have exclusive membership, and select one
  current version. A withdrawn/stale selection has no automatic fallback.
  Reactivation and selection may be one atomic submitted group. Selecting new
  evidence does not retarget another note's old supporting links.
- Reader JSON/Markdown disclose active receipt/head identities and withheld/
  selected IDs. Approval history remains intact; withheld records count under
  pending_or_stale. Packet evidence marks withdrawn/inactive support unusable,
  and search indexes become stale when their complete reader artifact changes.
  With no curation or declared revisions, the old reader bytes are unchanged.

Documentation: `docs/KNOWLEDGE_CURATION.md`, decision 0010, targeted updates to
README, KNOWLEDGE_REVIEW, REVIEW_GUIDE, DATA_MODEL, ARCHITECTURE and CHANGELOG.
CI adds only an unsigned synthetic curation export, never owner decisions.
Neither source-rights policy nor the editorial-policy input was regenerated.

Actual persistent commands and outcomes:

```text
python -m jeb --root dist/demo --synthetic knowledge curate export --source synthetic-v1 --output reports/knowledge-curation.md
python -m jeb knowledge curate export --output reports/generated/knowledge-curation.md
python -m jeb --root dist/demo --synthetic knowledge curate validate --decisions reports/annotation-synthetic-response.json
python -m jeb --root dist/demo --synthetic knowledge curate apply --decisions reports/annotation-synthetic-response.json
python -m jeb --root dist/demo --synthetic validate --stage knowledge --source synthetic-v1
python -m jeb --root dist/demo --synthetic export --source synthetic-v1 --format json --maturity preview --output exports/after-knowledge-curation.json
python -m jeb --root dist/demo --synthetic export --source synthetic-v1 --format json --maturity release --output exports/forbidden-curation-release.json
```

Both reports succeeded with zero approved subjects and zero actions created.
Using the AI annotation response as a curator decision correctly failed twice
with exit 2 and no traceback. Canonical validation returned zero records, preview
bytes matched the original reader, and synthetic release correctly failed with
exit 2 and no release file. No actual approval, withdrawal, reactivation or
selection was manufactured. The seven observed commands and zero-count results
are in `reports/knowledge-curation-workflow.json`.

Reports copied byte-for-byte from actual CLI output:

- `reports/knowledge-curation-synthetic.md`, SHA-256
  `6745d771b5a52761721f5387733a811c45c17a5baec5447c2b715b41b228bf1b`.
- `reports/knowledge-curation-production.md`, SHA-256
  `8bddc1d0f975af5611ae8c75961a87714add322b1bbbfef2582dfb0a28ad4491`.

Actual final local verification: Windows 11 / CPython 3.13.3, the existing
hash-locked environment, no new runtime dependency or external service.

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb sources research prepare --source crosswire-srkdijekav --packet-id cw-lineage-followup-01
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
```

All passed: lint clean, **38 Python files formatted, 28 valid schemas, 211 tests
passed in 134.036 seconds**. Twenty-five new regression cases cover withdrawal
cascades, stale policy/rights gates, explicit reactivation, closed prospective
groups, revision declarations and selection, ancestry/membership/history
conflicts, no fallback or support retargeting, immutable restoration checks,
atomic failures, CLI schema boundaries, search identity and Windows receipt paths.
The initial 22 focused cases passed in 43.722 seconds; added targeted cases and
the final complete suite also passed. All simulated attestations/actions stay
inside automatically removed temporary synthetic roots.

Results and exact code/schema/test fingerprints:
`reports/knowledge-curation-verification.json`; complete test output:
`reports/knowledge-curation-tests.txt`. Existing manual packets, AI critique,
unsigned knowledge review and fixed native diagnostic capture also revalidated.
No native rebuild or repeated public-source investigation was performed.

Built the wheel offline with `--no-index --no-build-isolation --no-deps`, then
reinstalled it without dependency resolution into the existing clean verification
venv. **All 19 installed-wheel checks passed.** Python `-I` verified actual
site-packages imports and all 28 packaged schemas. Three targeted installed tests
simulated successful CLI owner actions, revision withholding/selection and long
Windows receipt reading/replay rejection only inside temporary test roots.
The fresh persistent deep workspace reproduced the 274-character staged response
path and unsigned report, rejected AI-as-owner validation/apply, retained zero
records and curation receipts, reproduced the source-only reader, and blocked
synthetic release. Production metadata reporting, source audit, unchanged
lineage packet and `pip check` passed. All actual outputs:
`reports/knowledge-curation-package.json`. Wheel SHA-256:
`6f43c600c4cf8825f4eef0e3abfbfba68bff94aa1f752fa9ce82e65a7b2c70ec`.
The wheel contains no native binaries and retains separate license files.
No Linux execution or remote CI result is claimed by this local run.

Historical status is unchanged: CrossWire SrKDIjekav and eBible srp1865 need
review; Šarić remains excluded; production lock is empty. CrossWire still has
fourteen evidence records, five unresolved checks and sixteen admission blockers.
The ready metadata packet remains
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
No historical artifact was acquired or parsed. Real GEN 1:1-5, MAT 5:1-12,
MRK 1:1-8, LUK 17:20-21 and JHN 1:1-5 coverage is **zero**, as are complete real
books, real modernization, approved knowledge and owner text/name/note approvals.
Persistent review/curation receipts remain zero. Four invented source segments
and five unapproved drafts do not count as biblical coverage. Reader JSON stays
`c671d2838aff3c6fb507323c19081bbc3b77cbae7c5e86434bed609299b23b43`;
Markdown, original proposal and cached manual packet identities are unchanged.

Final Git inspection found the existing main commit `17f2613` (update 2), which
this continuation did not create. Earlier commit/unborn statements above are
historical snapshots. Preserved the current baseline, prior local work and
remote configuration. No commit, push, branch/history rewrite, contact,
publication, release, paid-service/model API call, machine setting change or chat
automation was performed by this continuation.

Next independent task: bounded local archive/restore of eligible canonical build
inputs, with an inspectable manifest and exact review/curation history, so ignored
approval files are recoverable. Exercise it with synthetic temporary decisions;
never bundle arbitrary workspace files/secrets, relax source eligibility or
publish an archive as a release. The actual five drafts must remain unapproved.
Real pilot work still requires new primary exact-edition/digital-lineage/
component/rights evidence. No new owner decision blocks the reversible archive
implementation; preserve the prepared metadata handoff rather than repeat old
searches without a new lead.

## Continuation: local build archive and isolated recovery, 2026-10-31

Completed the next independent task from NEXT_STEPS. Kept the source gate,
five-book allowlist, existing editorial decisions and all prior work. No real
source has become eligible, and no actual owner decision was supplied or created.

Implemented:

- `src/jeb/build_archive.py` and `jeb archive create/validate/restore`. Creation
  snapshots one admitted source with fixed configuration/editorial policy,
  registry/lock/assessment metadata, exact locked transcript bytes, imported
  modernization proposals and their input packets, all text decisions, legacy
  canonical knowledge and complete review/curation receipts. Available fixed
  rights/license notices are preserved; historical builds require a rights policy.
- One new self-contained `build-archive-manifest` schema, bringing the packaged
  total to twenty-nine. The inspectable manifest binds sorted file paths, sizes,
  SHA-256 values, edition/corpus kind, exact package/schema engine and rebuilt
  corpus/policy/reader JSON/Markdown identities plus review counts.
- Strict ZIP-only bounds: 32 MiB container, 64 MiB expanded inputs, 255 inputs
  plus manifest, and 128 KiB manifest. No `extractall`, directory/link/device or
  encrypted members, traversal/drive/device paths, filename-case duplicates,
  unlisted/orphan inputs, arbitrary workspace files or executable software.
- Validation in a private temporary workspace before a restored destination is
  published. It rebuilds corpus and reader artifacts, validates active review
  heads and complete hash-bound historical snapshots, checks expected identities
  and dependencies, and rejects unsupported engine/schema migration.
- Restore works without the original project/configuration, rebuilds exports and
  the SQLite index, and renames staging only into a new nonexistent destination.
  Existing files/empty destinations are refused. Synthetic opt-in remains
  mandatory. Original approval, attribution, revision and curation identities
  remain unchanged; no new approval or release authority is generated.

This is deliberately a canonical-build archive, not a general workspace backup.
Unapproved knowledge/research working caches, AI critiques, private research
snapshot files, older full source artifacts, secrets, environments and binaries
are excluded. Original annotation input/response snapshots already inside a
canonical review receipt are retained. Restoring only this archive does not
recreate unfinished working caches; the original five pending drafts remain in
the untouched original workspace. Current raw artifacts and historical bounded
packet/receipt contexts are distinguished explicitly in the guide.

Documentation: `docs/BUILD_ARCHIVES.md`, decision 0011, README, DATA_MODEL,
ARCHITECTURE and CHANGELOG. CI now creates, validates and restores only the
original synthetic build. It never creates human decisions. No policy input,
source register, source lock or source-assessment bytes were regenerated.

Actual persistent recovery workflow:

```text
python -m jeb --root dist/demo --synthetic archive create --source synthetic-v1 --archive-id fixture-build-final-v1 --output dist/archives/fixture-build-final-v1.zip
python -m jeb --synthetic archive validate --input dist/demo/dist/archives/fixture-build-final-v1.zip
python -m jeb --synthetic archive restore --input dist/demo/dist/archives/fixture-build-final-v1.zip --destination dist/archive-restored-fixture-v1
```

All succeeded. The ZIP has eleven explicit inputs, four invented non-scripture
source segments, one unapproved modernization proposal and zero text decisions,
canonical knowledge records, review receipts or curation actions. The new
`dist/archive-restored-fixture-v1` workspace rebuilds identical source-only reader
JSON/Markdown and a usable search index; `covik` returns one synthetic match.
It is still a partial synthetic fixture, not biblical or complete-book coverage.

Concrete recorded artifacts:

- Local ZIP: `dist/demo/dist/archives/fixture-build-final-v1.zip`, SHA-256
  `c7290f39f3575ce3cd30f8b1c1ec548ea8fbba671dfe773f8936205425ccb40c`.
- Inspectable `reports/build-archive-manifest.json`, canonical manifest SHA-256
  `052ffada40ab6a6ab9c2f502e230aa2924f45e0def8066a0d5c58538fc1b9724`.
- Exact engine identity:
  `1f37db2ff57c1d22dff3c7ea0a513d54cf82e8897f85220272dc7775fde70842`.
- `reports/build-archive-workflow.json`: all nine observed workflow/gate commands,
  archive/manifest/reader identities, rebuilt counts and explicit scope limits.

Repeated restore into the existing destination, validation without synthetic
opt-in, historical archive creation from the unresolved CrossWire source and
synthetic edition release all correctly failed with exit 2 and no traceback.
No blocked-source ZIP, overwritten destination or release file was created.
An earlier exploratory `synthetic-build-v1.zip` is retained under ignored local
storage; its pre-final engine is not the final backup recorded above. Exact
engine compatibility is required, and there is no silent refresh/migration.

Actual final local verification: Windows 11 / CPython 3.13.3, existing
hash-locked environment, no new runtime dependency or external service:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb sources research prepare --source crosswire-srkdijekav --packet-id cw-lineage-followup-01
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
```

All passed: lint clean, **40 Python files formatted, 29 valid schemas, 230 tests
passed in 163.381 seconds**. Nineteen new cases cover deterministic snapshots,
admission/opt-in, secret exclusion, loss of the original configuration, exact
selected/withdrawn knowledge and superseded text-history recovery, immutable
destinations, checksum/engine/reader mismatches, malformed archives, missing
dependencies, unsafe paths/links/case variants, resource limits, corrupt cached
normalization, failed atomic publication, CLI recovery and long Windows receipts.
The initial focused suite passed in 29.758 seconds; the added targeted limits/
corruption checks also passed. All simulated attestations and their archives
remain confined to automatically removed temporary synthetic test roots.

Actual outputs and exact code/schema/test fingerprints:
`reports/build-archive-verification.json`; complete test output:
`reports/build-archive-tests.txt`. Existing manual passage packets, optional AI
critique, unsigned review/curation reports and native diagnostic capture also
revalidated. Their packet identities did not change. No native build was rerun.

Built the wheel offline with `--no-index --no-build-isolation --no-deps`, then
reinstalled into the existing clean verification venv without dependency
resolution. **All 17 installed-wheel checks passed.** Python `-I` verified
site-packages imports and all 29 schemas, validated the development snapshot with
the installed engine, and produced a byte-identical ZIP from a fresh synthetic
workspace. It recovered into a blank parent with no project configuration,
rebuilt matching reader/search artifacts, refused duplicate restore/missing
synthetic opt-in/uncleared real-source archive/release, and passed `pip check`.
Two targeted installed tests recovered temporary simulated review/curation/text
history and long Windows receipt paths. Persistent roots still have zero owner
approvals/actions. Actual output: `reports/build-archive-package.json`.
Matching wheel SHA-256:
`d3341ca0a9d3fa5a851f1dd0d739bca5e57dbd783fdf94567038f475bbbaf45e`.
Retain that wheel and dependency lock separately for this exact engine; the
archive does not bundle or install software. No native binaries are in the wheel;
separate license files remain intact. No Linux or remote CI result is claimed.

Source status is unchanged: CrossWire SrKDIjekav and eBible srp1865 need review;
Šarić remains excluded; production lock is empty. CrossWire retains fourteen
evidence records, five unresolved checks and sixteen admission blockers. Current
metadata handoff identity remains
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
No historical artifact was acquired or parsed. Real pilot/complete-book coverage,
real modernization, approved knowledge and owner text/name/note approvals are
**zero for GEN, MAT, MRK, LUK and JHN**. The four invented fixture segments and
five pending drafts do not count as scripture coverage. Original and recovered
JSON reader SHA stays
`c671d2838aff3c6fb507323c19081bbc3b77cbae7c5e86434bed609299b23b43`;
Markdown stays
`07278218ea0d46266172454e20f1ef111462c0eed4eae0d0cb4743657fd9ade9`.

Preserved existing main commit `17f2613` and all prior local work. This
continuation made no commit, push, remote/history change, contact, publication,
release, paid/model API call, machine setting change or chat automation.
Only local ignored archives/recovery workspaces and reviewable project files were
written. No new user decision blocked this authorized implementation.

Next independent task: a bounded typed event/story draft model and manual
unreviewed authoring for an exact eligible passage or the original fixture.
Keep narrated events, historical corroboration and fictional adaptation distinct;
preserve evidence, uncertainty, attribution, exact scope and name-mapping gates.
Do not invent real biblical events/participants or expand the collection. Real
editorial work still needs new primary edition/lineage/component/rights evidence.
Preserve the prepared metadata handoff rather than repeat completed searches.

## Continuation: typed unreviewed narrative drafts, 2026-10-31

Read the continuity files and Git state before continuing the stated next task.
Preserved main commit `17f2613`, the existing remote, all earlier local work and
all editorial/source decisions. Implemented the bounded draft slice without
changing canonical knowledge or the existing annotation return schema/prompt.

New implementation:

- `src/jeb/narrative_packets.py`: admitted exact-passage snapshots, manual
  prepare/validate/import/report, immutable hashed staging and fenced reports.
- `src/jeb/schemas/narrative-{node,packet,response}.json`: three self-contained
  versioned schemas, bundled in the same package/CLI. Responses are unreviewed,
  have no approval authority, cannot attest human review and retain null node
  approvals. Source IDs, current display/policy/knowledge namespace, prompts and
  return schemas are bound to the packet hash.
- `knowledge narrative` CLI branch and ignored `data/narrative-proposals/`
  namespace. Nothing imports into canonical JSONL, human annotation promotion,
  reader/search or build archives. No model API, network operation or new runtime
  dependency was added.
- `tests/test_narrative_packets.py`: twenty-three focused regression cases;
  updated the CLI schema-count assertion for the three actual new schemas.
- `docs/NARRATIVE_DRAFTS.md`, decision 0012, current README/model/architecture/
  review guides, CI smoke commands and the next-task handoff.

Entity labels require their exact source mention unless an attached approved
name mapping supplies the exact display form and a matching witnessed form.
No native names, transliteration, saint prefixes or inflection rules were
generated. Spans use bounded Unicode character offsets into current reader text,
separate from original source byte spans. Event participants are typed same-basis
entity references; story members are typed same-basis events. Source entities
represent individual mentions, not inferred identity across passages. Scopes
are exact selected-book/segment/dependency unions; IDs cannot shadow knowledge.

`source_narrative` requires selected-source primary-witness coverage.
`historical_claim` additionally requires separately registered secondary evidence
and historical claims directly linked to that evidence, all still unreviewed.
These structural rules do not prove independence, source inspection or history.
`fiction` cannot claim evidentiary support, source mentions or historical name
mappings, and cannot supply nodes to either factual graph. Support proposals
reuse existing evidence/claim category, scope, registration and acyclic support
checks. No real historical event or participant was authored.

Story event lists follow presentation order. `narrative_before` requires ordered
distinct nonoverlapping source anchors; it is not chronological corroboration.
`source_stated_before` needs an exact source span and human semantic inspection.
Asserted edges cannot cycle; uncertain alternatives remain labelled. There are
no inferred motives, omitted subjects, dates, quotations or harmonized scenes.
Bounds are packet 96 KiB, response 48 KiB, 32 nodes, 20 support drafts, 32
participants/events per node and 64 relations per story; the reused passage
snapshot also retains its 64 KiB preparation limit.

Actual manually authored Codex-assisted synthetic demonstration:

- Packet `dist/demo/data/narrative-proposals/fixture-narrative-v1/input.json`,
  46,360 bytes, canonical SHA-256
  `a1624156c28bb4ced94a32254ac5f2c30f725520526cfd34624f2f3ff594978c`.
- `reports/narrative-synthetic-response.json`, 13,375 bytes, canonical SHA-256
  `14daac25578624d336fa2b0f004318bd662ee874f212d69b56e9cbdceaee6733`.
- `reports/narrative-synthetic.md`, SHA-256
  `b18fd9b87ffd2d714288361d960f6d461db3c3c06ef83ed4f94e95ee7b1560fb`.
- `reports/narrative-workflow.json` records the actual commands, exact bindings,
  counts, labels, archive compatibility smoke and remaining limitations.

Five source-narrative nodes describe only the first invented fixture segment:
two exact mentions (`covik` and `probni zapis`), two events and their presentation
story. The negation and numeral 2 are preserved. The reading clause's omitted
agent is deliberately not assigned to the preceding person. Three separately
labelled fiction nodes invent a reader sorting cards. One new attributed primary
witness proposal describes the original technical fixture. There are **zero
actual historical-claim nodes, new scholarly sources or human decisions**.
All nine new proposals are unreviewed. The prior five annotation drafts, their
response hash and all previous packet hashes remain unchanged. An empty response
is valid; there is no requirement to manufacture content for a missing segment.

Actual final local checks used the existing hash-locked Windows 11 / CPython
3.13.3 environment:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb sources research prepare --source crosswire-srkdijekav --packet-id cw-lineage-followup-01
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
```

All passed: **42 Python files formatted, 32 valid schemas, 253 tests passed in
188.223 seconds**. The focused twenty-three-case suite passed in 28.639 seconds.
The first full run had 252 passes and one outdated expected-schema-count
assertion (29 instead of 32), in 198.097 seconds. Corrected the assertion; no
rights, review or admission gate was changed. The failed attempt and its exact
test output are preserved as `reports/narrative-verification-attempt.json` and
`reports/narrative-tests-attempt.txt`. Earlier focused fixture mistakes were
corrected before the successful focused/full runs. Final source/schema/test
fingerprints and all observed commands/results are in
`reports/narrative-verification.json`; full test output is
`reports/narrative-tests.txt`.

New tests cover deterministic snapshots, admission/opt-in, changed input/policy/
source/namespace/display hashes, false approval fields, Latin and five-book
scope, Unicode offset bounds, literal labels and approved witnessed mappings,
typed/dangling/shadowed references, fiction leakage, secondary evidence/claim
requirements, source presentation versus anchored/uncertain order and cycles,
out-of-order node input, complete ordered coverage, empty drafts, size/JSON
bounds, immutable imports/report fencing and unchanged reader/archive behavior.
All simulated name attestations and test historical claims exist only in
automatically removed temporary synthetic test roots, not in the real workspace.

All **26 installed-wheel checks passed**, including three targeted temporary
tests for approved-name bindings, historical support and reordered malformed
nodes. Built offline with `--no-index --no-build-isolation --no-deps`; reinstalled
only into the existing clean verification venv without dependency resolution.
Python `-I` confirmed site-packages imports and all 32 bundled schemas. Old and
new packet hashes matched; the actual report and archive were byte-identical to
the development run. Deep Windows response paths worked. A blank-parent restore
rebuilt matching reader/search artifacts, excluded narrative working caches and
retained zero canonical knowledge/decisions. Duplicate import, missing synthetic
opt-in, unresolved real-source drafting, synthetic release and incompatible old
engine use correctly failed with exit 2 and no traceback. `pip check` passed.
Actual commands/output: `reports/narrative-package.json`.

Current matching wheel:
`dist/narrative-wheels/jugoslavenska_ekumenska_biblija-0.1.0.dev0-py3-none-any.whl`,
SHA-256 `6bd44db26e667d0379aad27093d1eac883d98f33c645a11fd1523815fdef98a0`.
No native binaries entered the wheel. No Linux or remote CI result is claimed.
The optional native diagnostic capture revalidated; no native build was rerun.

Current-engine archive smoke uses a separate snapshot, preserving the original:

- `dist/demo/dist/archives/narrative-engine-v1.zip`, SHA-256
  `c40be4f01337cf6b21822d441b2c0795fde73ccf31015698f1126e8a9123b22f`.
- `reports/narrative-build-manifest.json`, canonical SHA-256
  `004ec38d488d9678e8f0253e537c4d4993412d8c44e4710b7b6539dce97997cf`.
- Exact new engine:
  `7048d97bdb13d7369376d9ea2a3e8d64c3e3aaec102684b8b4c63587097093c7`.
- Restored `dist/narrative-build-restored-v1`; eleven canonical-build input files,
  zero review/curation/text decisions and no pending narrative cache included.

The prior `fixture-build-final-v1.zip`, its manifest/reports, recovered root and
matching wheel SHA `d3341ca0...` were not overwritten. Before replacing the smoke
venv's old engine, it successfully revalidated that unchanged old ZIP; the
read-only result is `reports/narrative-prior-engine-check.json`. The new engine
correctly refuses it rather than migrating it. Retain each matching wheel and
dependency lock with its archive. Neither snapshot is a full working-cache
backup, authenticated signature, rights clearance or public release.

The actual JSON reader SHA remains
`c671d2838aff3c6fb507323c19081bbc3b77cbae7c5e86434bed609299b23b43`;
Markdown remains
`07278218ea0d46266172454e20f1ef111462c0eed4eae0d0cb4743657fd9ade9`.
The source registry, rights/editorial policy and five configuration inputs have
no tracked changes (`git diff --exit-code -- config sources
docs/EDITORIAL_POLICY.md docs/RIGHTS_POLICY.md` returned 0). Source clearance is
unchanged: CrossWire/eBible srp1865 need review; Šarić is excluded; the production
lock is empty. CrossWire retains fourteen evidence records, five unresolved
checks and sixteen admission blockers. The metadata handoff hash remains
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
No historical text was acquired or parsed. Exact real pilot coverage, complete
books, real modernization, approved knowledge and owner text/name/note approvals
are **zero for GEN, MAT, MRK, LUK, JHN**. The synthetic fixture is unreleasable.

This continuation made no commit, push, remote/history change, contact,
publication, release, paid/model API call, machine setting change or chat
automation. Existing local work remains reviewable in GitHub Desktop.

Next small independent task: an unsigned read-only human narrative review
handoff that places exact spans, roles, supporting claims/evidence, uncertainty,
name-approval identities and presentation/chronology assertions side by side.
Do not manufacture owner attestations or promote these drafts; a typed
promotion workflow is a separately reviewed future slice. Real editorial work
still needs new primary edition/lineage/component/rights evidence. No new owner
input is required for the next reversible engineering task. See NEXT_STEPS.

## Continuation: unsigned narrative inspection handoff, 2026-10-31

Read AGENTS, continuity files and Git status before continuing the specified
next task. Preserved commit `17f2613`, all earlier local work, exact five-book
scope and the existing editorial/source decisions. Added a read-only inspection
aid for an exact already-imported narrative response; no new draft was authored.

Implementation and documentation:

- `src/jeb/narrative_review.py` and `knowledge narrative review export`: require
  a safe packet ID/full lowercase response hash, validate the immutable imported
  response and current admitted packet, then write only the requested Markdown
  handoff. Missing imports, cross-packet substitution, changed data, stale policy/
  source/namespace/display, unsupported apply and missing synthetic opt-in fail.
- The derived `jeb-narrative-review/1` report binds packet, corpus, policy,
  source metadata, namespace, individual nodes and support/envelope identities.
  It shows original/normalized/reader wording separately, proposed roles beside
  source excerpts, exact deduplicated spans with Unicode offsets/slice hashes,
  story presentation/anchored/uncertain relations and original attribution.
- Transitive typed support links remain inspectable, including related cycles
  without claiming corroboration. Draft support is shown intact; canonical
  support is attached metadata plus typed links and approval/provenance hashes,
  without copying additional note prose. Selected narrative name mappings retain
  the complete original mapping and exact prior approval/content identities.
- Free text is fenced; returned table punctuation is encoded literally and line
  breaks are visible. Full exact spans remain available; table previews exceeding
  80 characters are explicitly labelled and linked. Context is at most 80
  characters per side. Output is capped at 1 MiB before one atomic immutable write.
- `tests/test_narrative_review.py` adds fifteen focused regression cases.
  `docs/NARRATIVE_REVIEW.md`, decision 0013, README/model/architecture/review guides,
  CI smoke commands and NEXT_STEPS describe the actual boundaries.

There is no new stored-data schema, decision format, narrative approval or
promotion operation. All 32 existing schemas, packet prompts and response
identities are preserved. Export generates no human identity, date, answers or
attestation. Existing recorded name/support approvals do not approve a narrative.
No report content is executed, no citation is fetched, and no new runtime
dependency, service or frontend was added.

Actual synthetic handoff:

```text
python -m jeb --root dist/demo --synthetic knowledge narrative review export --packet-id fixture-narrative-v1 --response-sha256 14daac25578624d336fa2b0f004318bd662ee874f212d69b56e9cbdceaee6733 --output reports/narrative-review.md
```

This succeeded and an identical repeat was idempotent. The curated copy is
`reports/narrative-review-synthetic.md`, 37,841 bytes, SHA-256
`584d7c2769d4487de65475f1aa6e27457598016d4a065e097cb2aaa0426ebcc2`.
It indexes four distinct spans from five source-narrative nodes and three
separate fiction nodes, with one existing witness proposal. There are zero
historical-claim nodes and zero selected name mappings in this actual example.
The reading clause retains an unspecified agent; negation and number 2 remain.
No event, participant, scripture wording or new scholarly bibliography was added.
The original packet hash remains
`a1624156c28bb4ced94a32254ac5f2c30f725520526cfd34624f2f3ff594978c`;
response hash remains
`14daac25578624d336fa2b0f004318bd662ee874f212d69b56e9cbdceaee6733`.
The previous generic narrative report and all earlier annotation/research/AI
critique packets also revalidated with unchanged identities. The earlier five
annotation drafts and all nine narrative/support proposals remain unreviewed.

Actual final checks used the existing hash-locked Windows 11 / CPython 3.13.3
environment. No dependency resolution, historical text or network was needed:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
python -m jeb sources audit
python -m jeb sources inspect --source crosswire-srkdijekav
python -m jeb sources research prepare --source crosswire-srkdijekav --packet-id cw-lineage-followup-01
python -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
python -m jeb demo
```

All passed: lint clean, **44 Python files formatted, 32 schemas valid, 268 tests
passed in 186.580 seconds**. The focused fifteen-case suite passed in 20.269
seconds. A preliminary unused test import was removed; no functional test failed
in the focused/full runs. Actual complete output is
`reports/narrative-review-tests.txt`. Exact source/schema/test fingerprints and
all thirty observed workflow/check commands are in
`reports/narrative-review-verification.json`; actual handoff identities and
limits are in `reports/narrative-review-workflow.json`.

The new tests cover imported identity and cross-packet substitution, stale rights/
policy/namespace and cached-content integrity, Unicode offsets, raw/normalized/
approved-display separation, role/fiction/chronology boundaries, complete typed
support chains including related cycles, literal returned table content and
safe fences, exact prior mapping approvals, bounded atomic immutable output,
empty/support-only/reordered graphs, CLI refusal and no extra data writes.
Tests compare every original workspace file plus reader/decision state before
and after handoff generation. All simulated text/name attestations remain only
inside automatically removed temporary synthetic test roots. No actual owner
approval was created or inferred from running the tests or exporting the report.

All **29 installed-wheel checks passed**, including four targeted temporary
tests for approved-display offsets, canonical metadata isolation/support chains,
exact prior name approval and literal table/fence rendering. Built with
`--no-index --no-build-isolation --no-deps`, then installed only into the existing
clean verification venv with `--no-index --no-deps --force-reinstall`. Python
`-I` confirmed site-packages imports and all 32 schemas. Old/new packet hashes
matched, and the handoff and current-engine archive were byte-identical to the
development run. Deep Windows imported-response/report paths worked. Missing
import, short hash, nonexistent apply, missing synthetic opt-in, uncleared real
source, synthetic release and old-engine mismatch all failed with exit 2 and no
traceback. A blank-parent recovery rebuilt matching reader/search data with zero
knowledge/text decisions and no pending narrative cache. `pip check` passed.
Commands/output: `reports/narrative-review-package.json`. No Linux or remote CI
execution is claimed. Native capture validation passed; no native build was run.

Current matching wheel:
`dist/narrative-review-wheels/jugoslavenska_ekumenska_biblija-0.1.0.dev0-py3-none-any.whl`,
SHA-256 `15c5e092b07ee941bf5b99b04182fb30392e178bcbae234e6d49dea1dd4cab4b`.
No native binaries entered the package. New code changes the exact engine even
though the dev version is unchanged; the compatibility smoke uses a new archive:

- `dist/demo/dist/archives/narrative-review-engine-v1.zip`, SHA-256
  `27c557f9677c88480f554ba427c3deed97667486914fbdcfdd90d53faf3e3d48`.
- `reports/narrative-review-build-manifest.json`, canonical SHA-256
  `5e24b5e242fa72f3b56eecf29e8d16a8eda0c21906bf6783d96b903931092b9f`.
- Exact engine:
  `4172835d8b9653f1b8dd3523afdad6a5c7d5cf1bb5a8775951c872498f38726c`.
- Recovery root `dist/narrative-review-build-restored-v1`; eleven canonical-build
  inputs, zero decisions/curation/review receipts and no narrative working cache.

The previous `narrative-engine-v1.zip`, its reports/recovery root and matching
wheel SHA `6bd44db2...` remain unchanged. Before updating the verification venv,
its retained prior engine successfully revalidated that ZIP; see
`reports/narrative-review-prior-engine-check.json`. The current engine correctly
refuses the older snapshot. The even earlier archive and matching wheel also
remain intact. Retain each exact wheel and dependency lock with its snapshot;
there is no automatic migration, public release or full working-cache backup.

Reader JSON SHA stays
`c671d2838aff3c6fb507323c19081bbc3b77cbae7c5e86434bed609299b23b43`;
Markdown SHA stays
`07278218ea0d46266172454e20f1ef111462c0eed4eae0d0cb4743657fd9ade9`.
`git diff --exit-code -- config sources docs/EDITORIAL_POLICY.md
docs/RIGHTS_POLICY.md` returned 0: no source/rights/editorial configuration input
was changed. CrossWire SrKDIjekav and eBible srp1865 still need review, Šarić is
excluded, and the production lock is empty. The fourteen CrossWire evidence
records, five unresolved checks and sixteen admission blockers are unchanged.
The source-research handoff remains
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
No historical text was acquired or parsed. Exact real pilot/complete-book
coverage, real modernization, canonical knowledge and owner text/name/note
approvals remain **zero for GEN, MAT, MRK, LUK and JHN**.

This continuation made no commit, push, remote/history change, release,
publication, contact, paid/model API call, machine setting change or chat
automation. Existing local work remains available for GitHub Desktop review.
No new owner input was required for this authorized reversible engineering slice.

Next small task: a dedicated versioned human narrative decision format and
validation-only command for one exact imported response, with truthful owner
participation and explicit meaning/support/category/rights checks. It must bind
the complete typed graph and original contribution identities, create no
receipt/approval/canonical data, and exercise attestations only in temporary
synthetic tests. Eventual receipt/promotion is a separate later slice. Real
editorial work still needs new primary source-lineage/edition/rights evidence.
See NEXT_STEPS; do not repeat the completed handoff or source searches.


## 2026-10-31 — validation-only decisions and independent source audit

Read PROGRESS, NEXT_STEPS and git status before editing; preserved the substantial
existing uncommitted work. Added shipped narrative-review-decisions 1.0 schema
and `python -m jeb knowledge narrative review validate --decisions PATH`.
The command binds the complete current validated packet and exact imported
response, every typed node and original support envelope; requires owner
attestation, date/identity, explicit five inspection checks and rationale.
It writes nothing and creates no receipt/approval/canonical content. Human
identity and attestation truth are not authenticated. Original credits remain
bound through exact response/envelope hashes; no actual owner document was made.
Tests use only temporary synthetic attestations. Existing annotation promotion
was not changed. No new wheel/archive compatibility verification was performed;
retain previous exact engines with their archives.

Source investigation: public web opens of all five supplied leads plus direct
Python urllib acquisition recovered actual CrossWire ZIP and eBible USFM/USFX
ZIPs (initial eBible 403 overcome using www hostname/browser User-Agent), IA
metadata/OCR and selected page JPEGs. Metadata web fetch failed, but direct
HTTPS succeeded. Direct page n980 returned 404; full scan completeness is not
claimed. All downloads remain ignored private evidence under
`data/private-source-audit`, outside package/demo/corpus. No network tests added.
The audit has exact evidence URLs and component/gap distinctions:
`docs/sources/SOURCE_COMPARISON_2026-10-31.md`; acquired file sizes/SHA-256 in
`reports/source-audit-2026-10-31.json`.

Inspected actual module config (not only catalogue): first release 2017-06-18,
no exact print source/transcriber/correction history, OSIS headings enabled,
Calvin/zText. Did not decode compressed scripture or claim a component inventory
from that config. eBible front matter declares modernization/Ekavianization and
a Cyrillic 1868 base although the downloaded text is Latin; metadata says
Revision with empty archive history. Introduction credits Branko Bjelajac,
1996, requiring separate rights evidence. Unknown transcription is not proof
of infringement; blanket PD notices do not settle later component rights.

Visually inspected IA general title n4, OT contents n6, GEN page 1/n8 and NT
title n740. Both title pages identify Latin 1868 Pest BFBS edition and translator
credits. This supplies a better documented research route, not production
clearance. Private GEN 1:1–5 pilot compares every verse to n8 and records OCR
corrections separately; no transliteration or modernization, human review still
pending. Whole-scan/five-book collation and exact jurisdiction assessment remain.
Source registry, rights assessments and empty lock are unchanged. No source was
admitted. No messages sent: short CrossWire/eBible drafts and official contact
routes are in the audit. Scope stays GEN/MAT/MRK/LUK/JHN; no real approval,
publication, push, release, model API or historical text reconstruction.

Verification commands used the existing hash-locked `.venv` Python 3.13:

- `python -m ruff check src tests`: passed.
- `python -m ruff format --check src tests`: 44 files formatted, passed.
- `python -m jeb validate --stage schemas`: 33 schemas valid.
- `python -m jeb knowledge narrative review validate --help`: exit 0.
- `git diff --check`: exit 0 (only existing Windows line-ending warnings).
- `python -m unittest tests.test_narrative_review.NarrativeDecisionTests tests.test_cli.CliTests.test_all_packaged_schemas_validate -v`: 2 passed in 3.132s.

Initial full run: 284 tests, one schema-count assertion failure and one inherited
helper collision error. Fixed expected schema count to 33 and isolated the new
test class/helper; no production behavior failed in that run. Output retained in
`reports/narrative-decision-tests.txt` (and partial attempt snapshot). An attempted
rerun to the same still-open log failed at shell redirection; fresh run uses
`reports/narrative-decision-tests-final.txt`. Final result follows below.


Final full offline verification: `python -m unittest discover -s tests -v`
**passed all 269 tests in 208.500 seconds**, exit 0. Complete output:
`reports/narrative-decision-tests-final.txt`. Lint, formatting and all 33 schemas
also passed. New decision tests verify exact target/context coverage, explicit
checks, owner declaration fields, tampered hashes and no filesystem mutation.
The earlier two test-harness failures are retained honestly above and are fixed.
Next small tasks and remaining source limitations are in NEXT_STEPS.md.

## Continuation: simplify the human repository terminal, 2026-10-31

The owner explicitly prioritized terminal usability and selected the defaults:
simple task menu, clear status/blockers, choosing review work without copying
hashes, synthetic demo shortcut and one-command checks. This took precedence
over adding another narrative decision workflow. Read the continuity/Git state
and preserved existing work. Local commit `8a736d4` appeared during this work;
its added validation-only schema/test and private source-research progress were
retained. The terminal work does not modify those source/decision components.

The human entry point is now:

```powershell
.\jeb.cmd
.\jeb.cmd status
.\jeb.cmd sources
.\jeb.cmd demo
.\jeb.cmd --demo review
.\jeb.cmd check
```

`jeb.cmd` uses the repository's `.venv` from any working directory. It requires
no activation, PowerShell policy change, global install or new dependency. A
missing environment points to the existing three hash-locked README setup
commands and installs nothing automatically. `python -m jeb work` / `jeb work`
provide the same tasks on an installed environment; Linux can use the venv
executable directly. Existing advanced commands retain their JSON interfaces.

`src/jeb/workbench.py` provides:

- Plain status with workspace label, exact collection, source eligibility/gaps
  and saved-work count that is explicitly not approval/coverage. Real source
  status still blocks editing. Source details are read offline without contact,
  acquisition or clearance.
- Numbered text/annotation/narrative inspection work. Each competing response is
  listed; no implicit latest candidate. The queue reads saved metadata, then a
  chosen item repeats full existing validation with its complete held identity.
  Changed, corrupt, out-of-root, stale-policy or rights-blocked work fails without
  selecting another candidate. Text source metadata comes from its exact batch
  packet, not from a guessed ID. Passage research retains its separate workflow.
- Existing report APIs render to a private temporary derived path, then the
  complete result is published immutably under `reports/generated/work/` with
  a bounded content-addressed name. Identical reports reuse the file; changed
  reports get another name; human edits are never overwritten. Temporary reports
  are cleaned up. No source/draft/approval/canonical/reader records are changed.
- An optional read-only 35-line pager, Enter for next page and q to stop. Terminal
  escape/control characters are displayed literally as escapes; stored report
  bytes and protected literal words remain unchanged.
- Explicit isolated demo switching and return to the initial workspace. A
  shortcut's `--demo` requires an existing example; it never silently creates
  one. The demo action runs the original synthetic workflow only. Fresh demos
  have the original text proposal; existing annotation/narrative responses are
  listed when present without inventing/importing new model results.
- A live four-step offline check runner with the current Python and explicit
  repository cwd, no shell, first-failure stop and timeouts. Missing development
  dependencies are reported, not installed. Cancellation/EOF selects nothing.

Updated `src/jeb/cli.py`, the README quick start, `docs/TERMINAL_WORKFLOW.md`, CI
smoke commands and NEXT_STEPS. Added twenty-two focused cases in
`tests/test_workbench.py`. No stored-data schema was added by this terminal layer.
The 33rd schema and its additional test belong to the preserved local validation
work already in `8a736d4`; the complete current suite includes them.

Actual focused suite: **22 tests passed in 11.088 seconds**. Early checks found
and corrected a text-queue metadata assumption (source is in the batch packet),
a missing real-context registry in a temporary test fixture, and test-harness
quoting for cmd.exe. Both Windows launcher cases then passed: another cwd, and
a missing environment under a path with spaces/ampersand. No source/review gate
was relaxed. Tests also cover all three report APIs/data preservation, competing
responses, exact snapshot changes, stale rights/policy, unsafe paths, edited
reports, invalid metadata, bounded scans, cancel/EOF, terminal controls, demo
separation, check failures/timeouts and unchanged legacy JSON output.

Actual full verification ran through the new human shortcut:

```text
.\jeb.cmd check
```

It executed these required commands in order:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
```

All passed in the existing hash-locked Windows 11 / CPython 3.13.3 environment:
**46 Python files formatted, 33 schemas valid, 291 tests passed in 225.500
seconds**, exit 0. Complete actual output: `reports/terminal-workflow-checks.txt`.
The verification recorder initially expected the older 290-test count; the
preserved local validation test made the correct total 291. The checks themselves
passed. The recorder was corrected to read actual test/schema results and resumed
after verifying every source/test/schema/launcher fingerprint unchanged; no
successful full check was skipped or claimed from an unexecuted run.

`reports/terminal-workflow-verification.json` records all 24 observed commands,
results and exact fingerprints. `reports/terminal-workflow.json` records the
three numbered synthetic selections, full input identities and resulting report
paths/hashes. The annotation, narrative and text reports all generated without
manual full-hash input or human decisions. The narrative output is byte-identical
to the prior unsigned handoff (`584d7c27...`). Real-project review work remains
empty. All prior manual packet identities, metadata handoff `f4b980da...`, the
native diagnostic capture and source audit revalidated. No native build ran.

All **21 installed-package checks passed**, including four targeted temporary
tests covering three report types/data preservation, stale source/policy gates,
local report notes and terminal control escaping. Built with `--no-index
--no-build-isolation --no-deps` and force-reinstalled only into the existing clean
verification venv without dependency resolution. Python `-I` confirmed actual
site-packages imports and all 33 schemas. The installed menu/status/source tasks,
fresh demo, numbered review/pager and unchanged JSON audit passed. Source and
installed text reports and archives were byte-identical. Unknown approve,
missing synthetic opt-in, incompatible old engine and synthetic release failed
with exit 2 and no traceback. Blank-parent recovery rebuilt identical reader and
search artifacts. `pip check` passed. Results: `reports/terminal-workflow-package.json`.
No Linux or remote CI run is claimed; no native binaries entered the wheel.

Current matching wheel:
`dist/terminal-workflow-wheels/jugoslavenska_ekumenska_biblija-0.1.0.dev0-py3-none-any.whl`,
SHA-256 `d8c373ed4f3027b9ad2bbee7939aa32da94d562f9e3511be22afabb9c509b195`.
Current-engine snapshot:

- `dist/demo/dist/archives/terminal-workflow-engine-v1.zip`, SHA-256
  `2c987885ee9e0944a52aab89c6b258db16af0522d0a6c5c5eda5841473a47bb1`.
- `reports/terminal-workflow-build-manifest.json`, canonical SHA-256
  `7e56de92dc94b18621a2e5668768f7826b0188091138df2fb0a0eca8a0bf4c6d`.
- Exact engine:
  `493c9d840d9f5ec3ac4dd502dd7849680c0acec76e6f63dbf88c5c5f8805313b`.

The preceding `narrative-review-engine-v1.zip` successfully validated with its
retained installed engine before the verification venv update; its ZIP, wheel
and all earlier snapshots/reports remain unchanged. Current code correctly
refuses an old engine instead of migrating it. Eleven canonical-build inputs
remain; generated terminal reports, pending working caches and the launcher
software are outside that build scope. Retain the matching wheel and repository
launcher separately; there is no full workspace backup or public release.

Reader JSON SHA remains
`c671d2838aff3c6fb507323c19081bbc3b77cbae7c5e86434bed609299b23b43`;
Markdown remains
`07278218ea0d46266172454e20f1ef111462c0eed4eae0d0cb4743657fd9ade9`.
`git diff --exit-code -- config sources docs/EDITORIAL_POLICY.md
docs/RIGHTS_POLICY.md` returned 0 against the current local commit. The production
lock is empty, both Serbian candidates still need review and Šarić is excluded.
Existing private scan/OCR research recorded in the preceding continuation stays
private evidence, not cleared corpus coverage; this terminal work acquired or
parsed no additional historical text. README now distinguishes private source
investigation from admitted corpus data. **Admitted real pilot/complete-book
coverage, canonical knowledge and owner text/name/note approvals remain zero**
for GEN, MAT, MRK, LUK, JHN. All existing synthetic drafts remain unapproved.

No commit, push, remote/history rewrite, contact, publication, release,
paid/model API, global install or machine setting change was made by this
continuation. Local `8a736d4` and existing uncommitted research/progress were
preserved. No new owner input was needed after the owner selected the defaults.

Next small usability task: section jumps in the read-only report pager, so a
human can reach source/proposal/flags or roles/relations without paging through
every provenance block. Preserve stored bytes and exact validation; no decision
writing or approval shortcuts. Advanced narrative decision validation already
exists separately; any receipt/promotion workflow remains a later reviewed slice.
Real editorial work still requires the unresolved source evidence and actual
human review. See NEXT_STEPS for the current priority and limitations.


## 2026-10-31 — owner register direction recorded

Read PROGRESS, NEXT_STEPS and git status; preserved existing terminal-workflow
changes. Recorded the exact owner direction in decision 0014: local Herzegovinian
speech with broadly understandable Bosnian/Herzegovinian wording. Updated
EDITORIAL_POLICY and next content priority: multiple independent language and
translation evidence sources, then a reusable style/vocabulary proposal.
Prepare review batches rather than paragraph-by-paragraph questions. No new
lexical/inflection rule, final-text approval, source clearance or scope expansion
was inferred. No code changed. Policy hash changes intentionally stale earlier
bound packets; no packet/receipt was resealed or migrated. No publication/contact.
Validation: `git diff --check` run after edits; result recorded below.
Result: git diff --check passed (exit 0; Windows line-ending warnings only). No code tests needed for these documentation-only changes.


## 2026-10-31 — evidence-backed language guide, first research batch

Read PROGRESS/NEXT_STEPS/git status; preserved existing local code and editorial
work. Added docs/HERZEGOVINIAN_LANGUAGE_GUIDE.md, with eleven targeted regional,
standard-language and translation references and explicit inspection depth.
Primary publisher/institution/library records distinguish catalogue-only books
from inspected paper sections. Šimić 2021 pp.331–332 supplies five located lexical
examples (jopet, studeno, težak, tovar, dažd), all unapproved candidates with
context/comprehensibility warnings. Four owner literals stay unchanged; no
inflections or conversion rules inferred. Guide is a research proposal, outside
canonical knowledge/terminology/policy inputs. No actual Bible wording generated.

Verified Kraljević dictionary identity through Matica/NSK, retaining title and
pagination differences. Verified Halilović BHDZb VII and Hadžimejlić BHDZb XI via
publisher records; Peco book remains a cited lead, not read content. Čedić et al.
2007 and Halilović 2017 provide wider-language reference leads, not inspected
entries. Added distinct Škarić 1858–1861, Katančić 1831 and Zagreb 1968 comparison
routes; exact scans/verse comparison still outstanding. These are not independent
witnesses for every claim. No rights clearance or theological substitution.

Actual research used public web search/open/find; no paid/model API, contact,
source lock/registry change or publication. One Institut full-paper URL returned
404 despite a search snippet; its contents were not used as inspected evidence.
Anonymous full-dictionary PDF was not acquired. hljeb/kruh remains unresolved;
no general claim about all Herzegovinian vocabulary follows from one local study.
Next small task is exact entry/edition inspection, not more approval machinery.
Docs-only change: no code/schema changes or new tests required.

Checks: git diff --check passed (exit 0; line-ending warnings only); new guide Latin-script/protected-literal checks passed. No application code changed.


## 2026-10-31 — concrete lexical entries and second historical witness

Read PROGRESS/NEXT_STEPS/git status. Preserved all existing local work. Added
LANGUAGE_ENTRY_BATCH_2026-10-31.md and guide follow-up. Public HJP form POST
returned hljeb/kruh comparison context, svjetlost/tama entries (kruh via direct
retrieved URL); found permanent IDs from returned HTML. Saved bounded private
HTML, no bulk dictionary copy or paradigm activation. duh query did not provide
a single inspected entry. HJP's Croatian labels do not define Bosnian usage.

Acquired actual Škarić slog 1 1858 PDF (16,458,985 bytes), IA metadata, OCR and
scandata as ignored private evidence. Applied PDF skill read-only. Used pdftotext
-layout (mostly empty text; Invalid Font Weight warning) and pdftoppm PNG rendering;
no dependencies installed. OCR XML objects located the relevant leaves; directly
viewed PDF 12 title and PDF 48–50 / printed 1–3. Recorded GEN 1:1–5 lexical and
construction differences, not a reconstructed complete transcription. Historical
commentary beneath the rule stays separate from scripture. No spelling or
meaning from memory. Exact file sizes/hashes:
reports/language-entry-evidence-2026-10-31.json. No admitted corpus/approval.

Provider BOSSPS title Saric conflicts with Škarić description/archive link;
recorded mismatch rather than merging translators. IA user-upload description
claims Google origin, PDF visibly has Google layers; original Google edition
link/physical-copy chain and component usage still unverified. Public-domain
mark does not clear the entire artifact. Katančić institutional bibliography
advanced, but no 1831 facsimile page located. Documented 2016 revision distinction
from KBF; did not substitute it. New book IDs were not added.

Commands: Python urllib acquisition/form requests; pdftotext -layout;
pdftoppm -f 12/-f 48 -l 50 (plus exploratory 3/5/13) and image inspection.
No source/rights policy, registry, lock, terminology or application code changed.
No contact, publication, release or approval. Docs-only checks follow.

Results: git diff --check passed (exit 0, line-ending warnings only); Latin-script document and evidence manifest checks passed. No code tests rerun for documentation/private-evidence-only changes.
