# Architecture and reproducibility

The installable `jeb` package uses Python 3.13.x and a single CLI. Configuration
and sources live in the explicitly selected project root; the installed package
carries its JSON Schemas and original synthetic fixture. There is no upward
root discovery, nested Git repository, model API, cloud service or web server.

`sources.py` admits only matching reviewed registry/lock records.
`source_assessment.py` validates historical edition/provenance/component/
versification/adapter dossiers and supplies an offline readiness report.
Synthetic workspaces bypass this historical assessment only; their release
prohibition is unchanged.
`source_research.py` creates metadata-only manual packets before clearance.
It reads no corpus, uses no network and never changes source assessments or
locks. Preparation snapshots the current source/dossier, scope and rights policy;
validation regenerates that exact expected packet to reject stale or substituted
inputs, prompts and output schemas. A bounded response contains unreviewed leads
and explicit question/evidence references, not approvals. Import writes a single
immutable canonical response; a separate command renders a review report with
untrusted content fenced as data. New responses use separate hashes and duplicate
imports fail. Historical results stay available even when their inputs become
stale; there is no automatic merge or promotion of findings.
`fetch.py` performs bounded HTTPS acquisition after that gate. The initial
transcript adapter creates faithful per-book records in `data/transcribed`.
`normalize.py` produces NFC/LF main text in `data/normalized` without changing
source bytes, source records or typed notes. Every load re-derives the corpus
from the locked source and rejects hand edits, extra books and missing files.

`batch.py` builds small manual modernization packets and validates returned
JSON before importing into `data/proposals`. Source, policy, corpus and packet
hashes bind the work. `review.py` records distinct, human-attested decisions in
`data/approved`. Changing approved text or its inputs invalidates the current
decision. Historical decisions are retained and explicit supersession resolves
conflicts; a policy change does not erase history or prevent re-review.

`review_assistance.py` prepares bounded manual critique packets for an existing
validated proposal. Rebuilding the expected packet checks source eligibility,
source/proposal/policy revisions, evidence metadata and its underlying content
hashes, prompt and response schema. It includes evidence locators and record
hashes without copying potentially restricted evidence text bodies. Strict
responses cover exact segments and existing flags, retain expert escalation,
and carry no human or approval authority. Import writes only a separate hashed
unreviewed response; a report presents source, proposal, diff and critique with
untrusted text fenced as data. These files do not influence reader generation,
human decisions, flags or release gates. Competing critiques remain separate.

`knowledge.py` validates JSONL relationships and separate annotation approvals.
Its graph validator also accepts in-memory candidate records, so proposed notes
can be checked without writing a temporary canonical file. `batch.select_passage`
shares the existing exact pilot manifest/context selection without changing the
modernization packet bytes.
`knowledge_packets.py` prepares separate bounded passage research and annotation
protocols. It combines eligible source context with the current reader text,
including actual approved edits. Scoped knowledge metadata and underlying record
hashes are supplied without external evidence text bodies. Currentness propagates
through dependencies; stale, rejected or unbound support is unusable. Research
returns unverified leads/questions. Annotation returns new attributed draft
evidence/claim/annotation graphs with exact current text hashes, typed references,
separate explanatory/reflection/creative layers and no human approval. Imports
write only hashed responses outside the canonical bank; reports retain the
unreviewed data and provenance. No reader, text decision or source lock changes.
`knowledge_review.py` exports an unsigned review subject and validates a separate
owner-decision document. One atomic, content-hashed receipt retains the complete
original packet, response and actual human decisions. Canonical validation
combines legacy JSONL with approved projections from these receipts, preserving
AI attribution, exact content/support identities and independent text approval.
Pending/rejected decisions are history only. Current dependency groups can be
promoted partially and resumed from the same exact response; competing pending
heads require explicit nonbranching supersession. Approved IDs are immutable.
`export.py` builds reader JSON or Markdown from faithful normalized text plus
exactly approved text, preserving typed layout/notes and explicit coverage.
Current approved knowledge records and their current dependencies can appear;
stale/unreviewed records count as pending and are omitted. `search.py` rebuilds
a disposable SQLite FTS5 index from the same preview. Its stored artifact hash
prevents searching a stale index. Only approved name aliases are indexed.

## Acquisition boundaries

HTTPS only, fixed timeout, bounded retries, exact allowlisted redirects, fixed
maximum and locked size, stream bounds and SHA-256 checks precede an atomic
cache write. Unexpected HTML, wrong header, short files and changed upstream
bytes fail. The cache is content-addressed and cannot be silently refreshed.
Configuration/source symlinks escaping the chosen project and unsafe file IDs
are refused. Text parsing failures get a diagnostic in `data/quarantine`, never
guessed scripture. Existing different transcription artifacts are not overwritten.

A tested ZIP helper reads safe members into a bounded in-memory dictionary:
no `extractall`, absolute/traversal/drive/Windows-device paths, symlinks,
special files, encryption, duplicate paths or oversized expansion. This is
**not** an implemented corpus ZIP import. The only accepted corpus format now is
JEB-TRANSCRIPT/1. SWORD, USFM, OSIS and arbitrary TXT/HTML fail explicitly.
No unsafe XML parser or external entities are enabled.

The independent `sword_build.py` and `sword_diagnostic.py` provide an optional
synthetic-only experiment, not another corpus adapter. The builder verifies the
exact software archive, omits seven known Android symlinks, safely extracts
regular software files and verifies each patch's before/after hashes. It uses
already installed C/C++/CMake/Ninja tools, with no global installation or network
installer. The evaluator checks native executable hashes before running four
fixed commands in an isolated library, with child-only home/library variables,
timeouts and bounded output checks. It accepts no historical module argument.
Native builds remain optional and local; the offline suite validates an actual
capture from the original fixture. Diagnostic XML rejects DTD/entity declarations
and imposes size/depth/node bounds. This narrow XML fragment check does not claim
general OSIS import or XML-schema validation.

## Determinism

`requirements.lock` pins all runtime/transitive/build/lint versions and records
their published release hashes from PyPI. Install with `--require-hashes` and
then the package with `--no-build-isolation --no-deps`. The supported runtime
range is deliberately one minor version: CPython >=3.13,<3.14. Windows and Linux
are CI targets; the local validation platform is recorded in PROGRESS.
sqlite3/FTS5 must be present in the Python build. Dependency license metadata
is kept separate from our corpus licenses.

Canonical JSON is UTF-8, sorted keys, two-space indentation, LF and a final LF;
non-finite numbers, duplicate keys and schema extras are rejected. Corpus and
packet artifacts contain no changing build timestamps. Reviewer/tool dates are
explicit recorded inputs, not generated claims of participation. Reports can
carry run metadata separately. Repeated generation from identical locked source,
policy and decisions produces identical corpus bytes. ZIP/wheel packaging bytes
and SQLite's internal file layout are not the deterministic corpus contract.

The filesystem workflow is intended for one local writer at a time. Individual
writes are atomic; a multi-file batch is validated before writing but is not a
database transaction. After an interrupted write, rerun structural validation
and compare immutable artifacts; do not approve a partially recovered batch.
Core bounded reads, atomic writes, containment symlink checks and response-import
duplicate checks use absolute extended-length paths on Windows. Logical and
stored project paths retain their usual spelling. This supports long staged
response filenames without changing machine settings; it does not establish
long-path compatibility for every optional native tool. See the
[Windows path rules](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation).
No code signs or proves the authenticity of a human attestation or legal opinion;
the owner is responsible for truthful identity and source assessments.

## Scope of this implementation

Real source-format adapters, knowledge withdrawal/version selection, rich
structured entity/event/story authoring,
expert D-class approval, rich scholarly title/word-alignment authoring tools,
automatic inflection rules, complete-book editorial work, EPUB/PDF/USFM/OSIS
output and frontend/publishing are future phases. The initial knowledge schema
provides versioned typed relationships; it is not a populated scholarly bank.
No completeness or professional review is inferred from a passing command.
