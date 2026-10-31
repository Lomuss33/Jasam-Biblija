# Session continuity: 2026-10-30

Latest continuation: human knowledge review and provenance-preserving canonical
promotion implemented; the five persistent synthetic drafts remain unapproved.
Current checks: **186 tests passed, 26 schemas valid**; all **18 installed-wheel
checks passed**, including two temporary simulated review tests. Historical
corpus coverage and real human approvals remain zero. Earlier session records
below are preserved; the latest details follow at the end.

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
