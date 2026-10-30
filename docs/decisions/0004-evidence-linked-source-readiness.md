# 0004: Make historical source admission evidence-linked

Date: 2026-10-30. Status: reversible implementation of the existing entry gate.

Provider configuration research located concrete missing edition/transcriber
information and a non-default declared versification. A status string and hash
alone must not hide those gaps. The existing prompt requires exact-edition
assessment, component rights, source fidelity and an evaluated real adapter.

Add a versioned source-assessment dossier bound to the registry record hash.
Its five checks are exact edition, digital provenance, component rights,
versification fidelity and adapter evaluation. Verified checks require valid
local evidence IDs. Historical admission requires those checks, known edition
identity/transcriber fields, country rights and matching locked artifact/coverage
records. A changed registry needs explicit dossier re-evaluation. Audit also
validates candidate dossiers and rejects orphan records.

Add read-only `jeb sources inspect` to show the current evidence and admission
gaps. It performs no network requests, hash refresh, status transition or approval.
Provider configuration/catalogue metadata hashes cannot substitute for a corpus
hash. The transcript parser must use the assessed source scheme.

Synthetic fixtures retain their isolated opt-in exception; they remain barred
from release. Source dossier validation proves structure and binding, not a
legal conclusion or reviewer identity. No newly required human approval is
invented, and no source is promoted by this change. No production text or
editorial decision is invalidated: none exists yet.
