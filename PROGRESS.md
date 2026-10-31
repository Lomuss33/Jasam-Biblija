# Session continuity: 2026-10-31

Latest continuation: exact imported narrative responses now have an unsigned
inspection handoff with source spans beside roles/relations, support chains and
prior name-approval identities. Current checks: **268 tests passed, 32 schemas
valid, 29 installed-wheel checks passed**. The report indexes four spans from
the existing eight original synthetic nodes and one witness proposal; it creates
no draft, decision or approval. Prior annotation/narrative drafts and reader
bytes are unchanged. Real coverage and human approvals/actions remain zero.
There is no narrative decision validator, apply or promotion endpoint yet.
Older archives and matching wheels remain preserved; use each exact engine.
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
