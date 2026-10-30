# 0007: Keep AI critique separate from human decisions

Date: 2026-10-30. Status: reversible local implementation.

The requested manual workflow includes optional review packets. Existing
modernization proposals and human exact-hash decisions already work; an AI
critique needs a separate record type and storage path so its observations cannot
be confused with owner approval or silently change a proposal.

Add `jeb review assist prepare/validate/import/report`, with a bounded packet
containing the exact validated proposal and source packet, policy, diff, flags,
segment IDs and relevant evidence metadata/content hashes. Exclude external
evidence text bodies. Bind the current prompt and output schema as well as the
source/proposal/evidence revision. Use no API or chat automation.

Require exact segment/hash/flag coverage. Existing flags stay open, D-class items
retain expert escalation and unresolved text cannot acquire replacement wording.
Responses are explicitly AI assistance, unreviewed, without approval authority
or human attestation. Store each critique separately by canonical-content hash;
preserve competing outputs and detect stale or edited records.

Do not modify human decision handling, source clearance, proposal text, flags,
reader output or release gates. An owner may inspect the critique and act through
the existing decision interface. Schema success is neither human participation
nor semantic verification. Demonstrate this only on original synthetic data
while historical source admission remains unresolved.
