# 0010: Keep knowledge curation separate from immutable approvals

Date: 2026-10-31. Status: reversible local implementation.

Represent withdrawal, reactivation and version selection as separate exact-hash
owner actions. Preserve every original record, approval receipt and attribution.
Each complete submitted set has one atomic content-hashed curation receipt, with
exact target snapshots and a nonbranching explicit supersession history.

Permit withdrawal without current corpus-display eligibility, so a stale or
rights-blocked source cannot prevent suppression of erroneous notes. Require a
current policy and intact approved identities. Reactivation and selection require
current eligible source/support and explicit human checks. Never treat an action
as new wording approval, source clearance, expert review or proof of identity.

Declare revisions through an optional exact `version_of` binding in the separate
human approval item, with an additional relationship check. Preserve it in
provenance and withhold the revision until selected. Do not infer semantic
replacement from matching passage/category or rewrite the AI response schema.

Version groups retain prior candidates and full revision ancestry, have exclusive
membership and select exactly one current approved candidate. There is no silent
fallback, support retargeting or automatic reactivation. Withdrawal/inactive
versions hide their dependents transitively. Keep curation state in reader
metadata and respect it in packet evidence and search-artifact identities.

Demonstrate only unsigned empty curation subjects in the persistent workspace,
because no actual approved notes exist. Simulate approvals/actions exclusively
inside temporary tests. Keep the original policies, five-book allowlist, source
gates, literal language decisions and source-only reader bytes unchanged.
