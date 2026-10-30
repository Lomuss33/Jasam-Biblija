# Initial data model (schema 1.0)

Twenty-four self-contained Draft 2020-12 JSON Schemas ship with the package under
`src/jeb/schemas/`. No remote schema references are resolved at runtime. Schemas
reject extra properties and version mismatches; code validates collection,
foreign keys, exact identities, hashes and review gates across documents.

`source-assessment` adds the historical source's evidence-linked admission
dossier. It binds the current registry hash, dated assessor, five readiness
checks and their evidence IDs. Provider/catalogue metadata snapshots carry
separate identities and are never corpus hashes. Missing/dangling evidence,
stale registry bindings and inconsistent declared versification fail validation;
an inspection report cannot change source status or claim human legal review.

`source-research-packet` and `source-research-response` describe metadata-only
manual research. The packet binds exact registry/dossier snapshots, configured
edition/collection, rights policy, prompt and output schema. It has no scripture
segments or acquisition/contact permission. Its question manifest includes only
unresolved dossier checks. The response distinguishes existing evidence IDs from
new leads, carries URLs/locators/dates and limitations, and remains unreviewed.
IDs, order, references, bounded size and current inputs are validated; factual
claims and a lead's relationship still need inspection. Imported responses are
stored separately, with canonical-content hashes, and never enter source locks,
corpus, knowledge approval or reader output.

`review-assistance-packet` and `review-assistance-response` describe optional AI
critique of an existing proposal. The packet binds the complete validated source
packet and proposal, policy, exact segment manifest and relevant evidence
metadata/content hashes. External evidence text bodies are not copied into the
packet. The response repeats source/proposed text hashes, assesses every existing
flag in order, and separates observations, issues and uncertainty. It cannot
replace text, clear flags or attest human review. Meaning-sensitive items retain
expert escalation. Imported critiques remain unreviewed and separate from human
`decision` records; they never enter corpus, reader output or release authority.

`passage-work-packet`, `passage-research-response` and `annotation-response`
provide the two bounded passage knowledge protocols. Packets retain the exact
source/context and current reader text, policy, approved name mappings, scoped
knowledge metadata/content hashes and registered bibliographic source metadata.
Research leads remain separate from canonical evidence records. Annotation
responses propose only new evidence, claim and annotation drafts, with explicit
AI-assisted attribution, null approval and exact current text dependencies.
Typed references and coverage are validated as a joint candidate graph without
writing to the canonical JSONL bank. Explanatory drafts need evidence; reflection
and creative material cannot become explanatory evidence. New support cycles
are refused; ordinary related-note cycles are allowed. Stale/rejected/unbound
support and its transitive dependents cannot support a returned draft. Imports
remain unreviewed proposals and do not change reader or approval counts.

`toolchain-lock` records a pinned software archive, patches, probe source,
compiler/build identity and executable hashes for the optional synthetic-only
SWORD experiment. `sword-probe-entry` describes only the ten fixed synthetic
slots, stored markup versus engine text, introduction/empty states and explicit
links among requested keys. Neither schema admits historical text or changes a
source-assessment check. These diagnostic records never enter corpus or reader
storage. A matching checksum proves identity, not program trust or text fidelity.

`edition`, `collection`, `registry`, `lock` and `names` describe project scope,
source identity/rights, exact-edition coverage, absences and proposed/approved
name mappings. Editions carry their own version, corpus kind, language policy,
jurisdictions and maturity boundary. The explicit allowlist is repeated at
schema/runtime boundaries. A new book needs a new owner decision and reviewed
implementation, not just a config edit.

`book` stores one source-specific book per file for readable diffs. Its stable
segment ID is `<source-id>:<book>.<chapter-label>.<verse-label>`. IDs are logical
strings, never directly used as Windows filenames. References retain scheme,
string labels, bridges, suffixes and explicit mappings. Original source line,
byte spans and source text remain distinct from NFC/LF text. Main text and source
annotations/layout stay separate. Source SHA-256 binds all records.

Unapproved modernizations live in `proposal` documents containing the exact
returned `batch-response`, source text hashes, proposed text, rationale, change
class, flags, evidence/name references and diff. The `batch-packet` retains the
exact supplied source context, policy/name/glossary snapshot, hashes, prompt,
output schema and coverage manifest. Model/tool identity may be null where
unknown; the interface must not invent hidden model versions.

`decision` / `decisions` record a human reviewer identifier, role, attestation,
date, exact proposal/text/policy hashes, state, issue resolutions and optional
superseded decision ID. States are approved, rejected, linguistic_review and
meaning_sensitive_review; source_only and proposed live in their appropriate
earlier layers. No approval is embedded into or silently mutates source text.
The selected current decision is derived from an acyclic, nonbranching history.

The `knowledge` schema is the first common JSONL relationship envelope for
book, section, passage, phrase, entity, event, story, claim, evidence and
annotation records. It carries stable record IDs, approved-book/segment links,
typed evidence/claim/entity/related links, separate layer/category, inspectable
bibliography/URL/locator, uncertainty, maturity and text-hash dependencies.
Bibliographic source IDs must be registered; contextual sources do not thereby
gain corpus permission. Explanatory historical/linguistic/literary claims need
evidence. Personal reflection and creative adaptation have distinct labels;
neither is historical corroboration. No numerical confidence scores are used.

Approval of a knowledge record has a separate human attestation and exact
content hash. All dependent text hashes must be recorded. Only approved, current
records whose dependency records are also current enter reader output. A changed
passage leaves its dependent interpretations/alignments pending for review;
changing a note never changes scripture approval. A syntactically valid claim
or locator still needs actual evidence inspection by a human.

The initial envelope is deliberately small. Rich attested-word analysis,
one-to-many/many-to-one/unresolved lexical alignments, title term morphology,
full book scholarship fields and bounded event/story structures require later
schema extensions and real evidence. Do not fill the generic text field with
unsupported assertions to imitate complete metadata. Original-name mappings
already distinguish attested Latin forms, witness/language/locator, historical
attestation versus reconstruction, alternatives, scheme, aliases, rationale
and owner approval; none is populated or approved in production.

`reader` is a generated single-edition artifact, not canonical storage. It
states source identities and rights scope, collection completeness, actual
source-segment and approved-segment counts for each approved book, annotation
coverage, absences, typed layout/notes and approved knowledge records.
Absent states are `outside_source_canon`, `historically_absent`, `not_downloaded`,
`parsing_failure`, `untranslated`, plus operational `not_ingested`. Missing files
or parse failures never turn into fabricated text. An absence record cannot
contradict available locked coverage.

SQLite is a rebuildable index of this same validated reader preview, with a
stored artifact hash and canonical segment IDs. Familiar regional aliases and
approved original-name transliterations can be indexed without changing IDs.
Source text coverage and annotation maturity are reported independently.
