# Human knowledge review and canonical promotion

This workflow records an actual owner's decisions about imported annotation
drafts. It never creates a decision on the owner's behalf. Text approval, source
admission and original-name approval remain separate. The five demonstration
drafts are still unapproved; their unsigned review report contains no human
attestation.

## Export the exact review subject

Import the annotation response with the existing `knowledge import` command.
Use its full response SHA-256, not a shortened ID or an arbitrary local file:

```text
jeb knowledge review export --packet-id <packet-id> --response-sha256 <full-sha256> --output reports/generated/knowledge-review.md
```

The report includes current passage wording, exact packet/response/policy and
draft-envelope hashes, attribution, tool identity, uncertainty, dependency
locators and recorded review states. Returned text is fenced as data. Existing
different report files are preserved. Export supplies bindings, not prefilled
reviewer fields or approval decisions. Research leads cannot use this interface.

Source/context, policy, attached evidence or unrelated canonical namespace
changes require a new packet. A partial approval from this exact response is
accounted for when reconstructing its original snapshot, so the remaining group
can be reviewed without rewriting the original packet. Every normal AI-response
import still uses the strict current namespace and rejects collisions.

## Record a truthful human decision

The owner creates a UTF-8 JSON file conforming to the installed
`knowledge-review-decisions` schema. Its required fields are:

- `schema_version: "1.0"`, a new safe `review_id`, exact `packet_id`,
  `packet_sha256`, `response_sha256` and current `policy_sha256` from the report.
- A real `reviewer_id`, `reviewer_role: "owner"`, truthful
  `human_attestation: true` and `reviewed_at` date. Software cannot authenticate
  identity or establish scholarly expertise from these fields.
- A nonempty `items` array. Each item names a draft `record_id`, the exact
  `draft_sha256` of its whole record/attribution/rationale envelope, `state`,
  independently written `rationale`, `checks` and `supersedes`.

States are `approved`, `rejected` and `needs_review`. There is no implied
decision for omitted drafts. Rejection and pending review are retained in the
history and add no canonical knowledge record. Review dates cannot precede the
returned draft or superseded decision.

Each approval must explicitly include all five checks:

```json
[
  "content_and_scope_checked",
  "attribution_checked",
  "category_and_uncertainty_checked",
  "support_inspected",
  "contribution_rights_checked"
]
```

These checks are the human's attestations about the actual subject inspected.
They do not prove a claim true, waive anyone's rights, establish legal clearance
or supply expert participation. Inspect evidence and exact locators, distinguish
narrative observation from historical corroboration, and preserve uncertainty.
Reflection remains attributed reflection; fiction remains labelled fiction.
Approving either cannot change its category or make it evidence. Approval does
not grant ownership of upstream material or imply the owner's authorship.

```text
jeb knowledge review validate --decisions <reviewed-json>
jeb knowledge review apply --decisions <reviewed-json>
```

Validation writes nothing. Apply validates the complete submitted set and its
current dependencies before one atomic receipt write. AI annotation responses,
missing checks, stale inputs, unsupported roles and forged draft IDs/hashes fail.
Decision input is bounded to 32 KiB; the complete receipt is bounded to 160 KiB.
Global `--root` and `--synthetic` precede `knowledge`; input paths are relative to
the shell, and output paths must remain inside the selected project.

For an actual revision of an approved record, optionally add `version_of` with
the original's exact record/approval/provenance binding and include the additional
`revision_relationship_checked` check. The type, layer/category and segment scope
must match. Declared revisions stay out of the reader until explicitly selected;
see [knowledge curation](KNOWLEDGE_CURATION.md). Independent notes are not inferred
to be versions, and the original approval and AI response remain unchanged.

## Dependencies, alternatives and corrections

All evidence/claim/entity/related references of an approved draft must point to
already approved current canonical records or drafts approved in the same
submitted group. Approving only a dependent note fails; approving its evidence
first, then its remaining dependents, works. A related-note cycle must be
approved together. Circular evidentiary support remains invalid.

Different returned responses remain separate choices even if they reuse draft
IDs. A later decision for an unpromoted ID must explicitly name its current
pending/rejected review's `review_id` in that item's `supersedes`. History must
be acyclic, nonbranching and refer to the same record and book. Reusing a review
ID, silently picking a winner, mixing envelopes or overwriting canonical IDs
fails. No tool consensus counts as independent evidence.

Approved canonical IDs remain immutable. A revised draft needs a new ID and a
new packet; it does not silently replace or withdraw an earlier approved note.
The separate [curation workflow](KNOWLEDGE_CURATION.md) now records exact-hash
withdrawals, explicit reactivation and selection among approved versions.
Its actions change reader eligibility while preserving every original receipt.

## Storage and exports

Each successful apply writes one canonical-content-hashed document under
`data/knowledge-reviews/<review-id>/<receipt-sha256>.json`. It preserves the whole
original packet, response, attribution and human decision. This single receipt
is the commit unit; there is no partly copied set of JSONL records. Canonical
knowledge validation combines legacy `data/knowledge/*.jsonl` with deterministic
approved-record projections from these receipts. Rejected/pending drafts do not
enter that projection. Do not hand-copy projected records into JSONL or discard
their receipt. Duplicate IDs and tampered receipt names/content are refused.

Projected records retain AI-assisted credit, original tool/rationale, packet,
response, draft and decision hashes, source-corpus/policy/bibliography identity,
and exact support bindings. Their content approval includes that provenance.
Reader JSON and Markdown preserve it. Passage/context, policy, bibliography or
support changes leave the historical receipt intact while hiding stale notes
and their dependents from reader output. A note change never changes passage
text decisions or source admission. Synthetic release remains forbidden.

These receipts are canonical build inputs, despite being ignored by Git by
default. Keep a recoverable permitted archive and deliberately curate eligible
approved inputs before any future release. Reader generation can use a receipt
after the working packet/response cache is removed, because both snapshots are
inside it. The local workflow assumes one writer; hashes detect accidental
edits, not authenticated reviewer identity or a maliciously rewritten archive.
The [local build archive](BUILD_ARCHIVES.md) preserves these canonical receipts;
unapproved working caches are outside that archive's explicit scope.

The [unsigned synthetic review](../reports/knowledge-review-synthetic.md) shows
the actual five staged drafts. Simulated approvals are confined to temporary
automated tests. Production and the persistent demonstration have zero owner
text/name/note approvals and zero promoted records.
