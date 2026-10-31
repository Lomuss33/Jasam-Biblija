# Withdrawals, reactivation and version selection

Approved knowledge records and their original review receipts remain immutable.
An actual owner can separately withdraw a note, reactivate it, or choose among
approved versions. These actions change reader eligibility, not passage text,
source admission, original attribution or the historical approval. No assistant
may create such an action as if the owner had participated.

The persistent demonstration has five unapproved drafts, zero approved records
and zero curation actions. Its [unsigned curation report](../reports/knowledge-curation-synthetic.md)
therefore has no approved target to withdraw or select. Successful simulated
actions exist only inside temporary automated tests.

## Inspect exact subjects

```text
jeb knowledge curate export --output reports/generated/curation.md
jeb knowledge curate export --source <eligible-source-id> --output reports/generated/current-curation.md
```

The unsigned report contains metadata, exact record/approval/provenance hashes,
revision ancestry, current curation state and optionally current reader
eligibility. It omits stored text bodies and creates no human action. Without a
source, current reader eligibility is explicitly unassessed. A blocked source
is reported as unavailable; no source gate is bypassed to display its wording.
Different existing output files are preserved.

## Declare an actual revision before approval

Use a new draft ID and a new annotation packet when revising an approved record.
In that draft's human `knowledge-review-decisions` item, supply optional
`version_of` with the original record's complete target binding from the report:
`record_id`, `record_sha256`, `approval_sha256` and `provenance_sha256` (null for
legacy records without provenance). Add `revision_relationship_checked` to the
five normal approval checks. The owner must compare the actual revision and its
relationship; software does not infer that two notes on one passage are versions.

The original must already be approved, have the same record type, book,
layer/category and exact segment-ID set, and match all bound hashes. It may be
stale or withdrawn; ancestry is not a factual support link and does not reactivate
its assertions. Actual evidence/claim/related links still govern support.
Approval preserves the exact draft, credit and revision binding in provenance.

A declared revision remains outside the reader until explicitly selected with
its original ancestry. Ordinary independent notes remain independent. Mark a
real replacement as a revision rather than approving it as an unrelated note;
software cannot establish a semantic replacement relationship from wording alone.

## Submit truthful owner actions

Create UTF-8 JSON conforming to `knowledge-curation-decisions`. Required wrapper
fields are `schema_version: "1.0"`, a new safe `action_id`, `source_id` (nullable
for withdrawals), current `policy_sha256`, real `reviewer_id`,
`reviewer_role: "owner"`, truthful `human_attestation: true`, `reviewed_at` date
and a nonempty `items` array. Dates cannot precede the bound approvals or
superseded actions. Recorded fields do not authenticate a person or prove facts.

Each item contains an independently written `rationale`, `checks`, and
`supersedes` (null initially, otherwise the current action ID for that subject).
The action-specific fields are:

| Kind | Subject and required fields | Required checks |
| --- | --- | --- |
| withdraw | `target`: exact approved-record binding | record_identity_checked, impact_checked |
| reactivate | `target`: exact previously withdrawn binding | record_identity_checked, impact_checked, withdrawal_reason_resolved, current_dependencies_checked |
| select | `group_id`, at least two exact `candidates`, one `selected_record_id` | record_identity_checked, impact_checked, current_dependencies_checked, alternatives_compared |

```text
jeb knowledge curate validate --decisions <owner-actions-json>
jeb knowledge curate apply --decisions <owner-actions-json>
```

Validation writes nothing. Apply validates the entire set and its prospective
state before one atomic receipt write. Inputs are bounded to 32 KiB; receipts to
256 KiB. Put global `--root` and `--synthetic` before `knowledge`. Input paths are
relative to the shell; output paths must stay inside the selected project.

AI responses, unapproved drafts, missing checks, stale policy or target hashes,
duplicate subjects, reused IDs and conflicting histories fail. Action IDs are
also compared without letter case, so filenames remain unambiguous on Windows.
Use a new ID for a new decision; preserve previous spelling when recovering an
interrupted write. No command rewrites or deletes the approved record.

## Withdrawal and reactivation rules

A withdrawal can be recorded even if the original note's context/policy is stale
or source admission now blocks corpus display. Exact canonical approval inputs
must still be present and valid, and the action binds the current policy. This
lets the owner suppress problematic material without reacquiring or displaying
blocked wording. It does not grant permission to adapt or publish anything.

Withdrawals hide the target and all evidence/claim/entity/related dependents
transitively. Historical approvals remain approved records; withheld items count
under `pending_or_stale` rather than `approved_current`. Returning the source or
restoring an old policy does not automatically undo the withdrawal.

Reactivation must explicitly supersede the current withdrawal and attest that
its reason was resolved. It requires an eligible current source, current exact
passage/support bindings and a compatible active version choice. Related
dependency cycles may need joint reactivation. Reactivation and a selection can
be submitted atomically when neither would be valid alone. It cannot approve a
new wording, clear stale review dependencies or change source rights.

## Version groups and alternatives

The owner creates a stable group ID and binds its approved candidates. Candidates
must share record type, book, layer/category and exact segment-ID set; hashes of
their dependent text may differ for historical versions. Every declared revision
must include its exact original ancestry among the candidates. Only one candidate
is selected. New revisions remain withheld until added and explicitly selected.

Later choices explicitly supersede the current group head and retain all prior
candidates. A record cannot belong to competing groups. Two genuine independent
notes are not grouped automatically; an owner may explicitly identify approved
alternatives. Selecting a version never retargets another note's evidence link:
dependents of an inactive version remain withheld until separately revised and
reviewed.

A stale or withdrawn selected version yields no automatic fallback. The owner
must explicitly choose another approved current candidate. Withdrawing a version
and choosing a replacement may be one submitted set. Switching back to an older
version requires that it is still current and not withdrawn. Labels and AI credit
remain unchanged; reflection or fiction cannot become explanatory evidence.

## History, exports and recovery

Apply writes one immutable content-hashed receipt under
`data/knowledge-curation/<action-id>/<receipt-sha256>.json`. It contains the owner
decision and exact approved-record snapshots. Histories are acyclic,
nonbranching and tied to the same record/group. Duplicate replays, missing
predecessors and silent conflict resolution are refused.

Reader JSON/Markdown record active head IDs, receipt hashes, withdrawn and
inactive-version IDs and selected groups. Original knowledge records and their
approval/provenance hashes are unchanged. Passage approval counts and wording
stay independent. Packet evidence catalogs mark withdrawn/inactive records and
their dependents unusable. The search index must be rebuilt after curation,
because it is bound to the complete reader artifact. Synthetic release remains
forbidden.

Keep curation receipts with all original review/approval inputs in a recoverable
permitted archive; these canonical inputs are ignored by Git by default. Missing
or changed targets and malformed/tampered receipts block validation. Restore the
exact immutable inputs from that archive and validate again; do not delete a
withdrawal to reactivate content or hand-copy provenance records into JSONL.
An interruption before the atomic write records no action; a completed receipt
is replay-protected. There is no multi-file promotion to complete by hand.
The [local build archive](BUILD_ARCHIVES.md) now provides one bounded canonical
backup and isolated restore path; it does not copy the entire working workspace.

The local workflow assumes one writer. Hashes expose accidental edits, not
authenticated identity or a maliciously rewritten archive. No source text,
expert participation, human decision or permission is manufactured by the tool.
