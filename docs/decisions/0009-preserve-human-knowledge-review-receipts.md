# 0009: Preserve human knowledge decisions as atomic canonical receipts

Date: 2026-10-30. Status: reversible local implementation.

Use a separate owner-decision schema and CLI for staged annotation drafts.
Reports remain unsigned; no assistant-generated real approval is permitted.
Bind every chosen draft envelope, original packet/response, policy and current
passage/support dependencies. Explicit human checks cover scope, attribution,
category/uncertainty, actual support inspection and contribution rights.

Store the full original packet, response and human decisions in one immutable,
content-hashed receipt. Canonical approved records are deterministic projections
of those receipts alongside legacy JSONL records. This avoids a partial
multi-file promotion and preserves attribution in both canonical data and reader
exports without rewriting the original AI-response schema or cached packets.

Only closed current approval groups are projected. Rejected/pending decisions
are history, not canonical content. Allow explicit nonbranching supersession of
pending/rejected heads and resumption after partial promotion of the same exact
response. Preserve all alternative responses; model agreement supplies no
authority. Existing canonical IDs cannot be overwritten or reinterpreted.

Add optional provenance to knowledge and reader records; approval hashes include
it. Preserve exact source-corpus/policy/bibliography and support identities so
changes hide affected notes transitively without changing passage approvals.
Reflection and fiction retain their labels and AI credit after acceptance.

Approved IDs are immutable in this slice. Withdrawal/selection among approved
versions requires a separate subsequent workflow; a new version does not remove
an old one. No actual demonstration approval is generated. Hashes and recorded
attestations do not authenticate a person, prove facts or grant source rights.
