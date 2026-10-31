# Unreviewed structured narrative drafts

This local manual workflow stages typed entities, events and stories for one
exact eligible pilot passage, or the opt-in original synthetic fixture. It does
not supply a historical source, clear rights, approve interpretation or populate
the canonical bank. Source, transcription, reader wording, support proposals and
narrative drafts remain distinct. No model API, scraping or network call runs.

```powershell
jeb --root dist/demo --synthetic knowledge narrative prepare --source synthetic-v1 --selection fixture --packet-id fixture-narrative-v1
jeb --root dist/demo --synthetic knowledge narrative validate --input reports/narrative-synthetic-response.json
jeb --root dist/demo --synthetic knowledge narrative import --input reports/narrative-synthetic-response.json
jeb --root dist/demo --synthetic knowledge narrative report --input reports/narrative-synthetic-response.json --output reports/narrative.md
```

Omit the synthetic options only for an actually admitted historical source.
`--selection` is exactly GEN, MAT, MRK, LUK, JHN or synthetic-only fixture.
Historical selections use the existing exact pilot manifests; a missing segment
fails rather than inviting reconstructed wording. No real source is admitted.

Prepare writes `data/narrative-proposals/<packet-id>/input.json`. The manual
response follows its embedded schema. Import validates it before one immutable
canonical-JSON write under `responses/<response-sha256>.json`. Identical packet
preparation is idempotent; duplicate imports and differing existing files fail.
Use a new packet ID after inputs change. Reports accept either a returned file
or the imported file, fence untrusted data, and never execute returned content.

The packet binds admitted source/corpus, actual current reader wording, policy,
terminology, attached approved name mappings, registered bibliographic metadata,
scoped knowledge metadata/currentness and the complete canonical ID namespace.
Its hash also binds prompt, coverage and return schema. Regeneration detects
stale or substituted inputs. Unapproved modernization is never the displayed
passage. Only selected segments may be authored; adjacent context is read-only.

## Three explicit bases

| Basis | Meaning and structural requirements |
| --- | --- |
| `source_narrative` | What this source narrates. Exact source spans and selected-source `primary_witness` coverage are required. It makes no independent historical claim. |
| `historical_claim` | An unverified historical interpretation. It additionally needs separately registered `secondary_scholarship` coverage and historical-layer claims directly linked to that secondary evidence. |
| `fiction` | Invented adaptation. No evidence/claim links, attested mentions or historical name mappings. All referenced participants/events must also be fiction. |

Every node requires explicit uncertainty, AI-assisted contribution credit,
rationale, exact current display dependencies, `review_state: draft` and null
approval. The overall response is unreviewed, has no approval authority and
cannot carry a human attestation. Registered source IDs and bibliography are
metadata, not proof of inspection, independence, truth or reusable rights.
Even a structurally valid historical claim remains an unreviewed proposal.

Factual and fictional graphs cannot share participant/event references. Neither
can link to narrative nodes in another response, book or unrequested passage.
This avoids silent scene harmonization and reuse of fictional roles as evidence.
Existing canonical evidence/claims may be referenced only when attached, current,
correctly typed and relevant to the selected scope. New `support_drafts` are
limited to draft evidence/claim envelopes, separately attributed and validated
by the existing annotation graph checks. Circular support, unregistered sources,
stale dependencies and ID collisions fail. Support remains unapproved too.

## Typed nodes and spans

The self-contained schemas ship as `narrative-node`, `narrative-packet` and
`narrative-response` under `src/jeb/schemas`, all version 1.0. The generic
canonical `knowledge` envelope and existing annotation schemas are unchanged.

- Entity: type, label, exact mention and optional approved name-mapping ID.
  Without a mapping the label equals the exact source slice. With a mapping it
  equals `display_form`, and the mention must match its attested Latin form,
  recorded historical form, display form or alias. Candidate/rejected mappings
  and invented native forms are refused. No inflection or transliteration runs.
  Each source entity represents one exact mention; equal labels do not establish
  identity across mentions, passages or responses.
- Event: action/speech/state/unspecified description, one source anchor and
  typed participants. Roles are agent, patient, speaker, recipient, location,
  instrument or unspecified, each with uncertainty. References must resolve to
  same-basis entities. Scope is exactly the anchor/participant union. A fictional
  event has no source anchor and needs participant scope. No inferred date,
  motive or generated quotation field is provided.
- Story: title, member event IDs, presentation order and explicit relations.
  Scope is the exact event union. Source event lists follow source anchor order;
  this is a reading order, not historical chronology. Fiction uses explicitly
  fictional presentation. All relations retain stated uncertainty.

Spans use `{segment_id, start, end}` into the exact `display.text`, counting
Python Unicode characters from zero, with an exclusive end. They are not byte,
UTF-16 or raw-source offsets. They cannot be empty, exceed the display, or refer
outside node scope. Original raw byte spans stay in the source snapshot.

`narrative_before` relates two member events in presentation order; source
anchors must be distinct and nonoverlapping. It asserts no temporal cause or
historical sequence. `source_stated_before` requires an explicit source span and
is unavailable to fiction. Its meaning must still be inspected by a human:
an in-range span alone does not prove that the source says “before.” `uncertain`
does not establish an ordering edge. Asserted ordering edges cannot cycle;
uncertain relations can describe unresolved alternatives. Self, duplicate and
nonmember relations fail. No cross-book harmonization is provided.

Responses include one ordered coverage item per selected segment, with exact
display hash and every applicable support/node ID in response order. Empty
graphs and `no_draft` are valid. Bounds: packet 96 KiB, response 48 KiB, at most
32 narrative nodes, 20 support drafts, 32 participants/events per node and 64
relations per story. Existing 64 KiB passage-snapshot preparation also applies.
Readers enforce bounds before parsing, strict JSON and Latin-authored strings.

## Actual original synthetic example

[`reports/narrative-synthetic-response.json`](../reports/narrative-synthetic-response.json)
and the [readable report](../reports/narrative-synthetic.md) contain eight nodes
and one new witness proposal. Five source-narrative nodes describe only the
invented first fixture segment. The label `covik`, negation `ne` and numeral `2`
are preserved. The reading clause names its object; its omitted subject is not
assigned to the preceding person. Two clauses have presentation order only.
Three separate fiction nodes describe an invented reader sorting cards.

There are no actual historical-claim nodes or new scholarly sources. The prior
five annotation drafts stay unchanged. All nine new proposals remain unreviewed;
no owner/name/text/note approval or curation action was generated. The actual
workflow and verification/package reports record hashes and observed commands.

## Current limits and preservation

Narrative import cannot use `knowledge review apply`; that endpoint still accepts
only its original annotation protocol. There is no narrative promotion path,
reader export, search indexing or canonical archive inclusion in this slice.
An [unsigned exact-response inspection handoff](NARRATIVE_REVIEW.md) is now
available with `knowledge narrative review export`; it adds no decisions.
Human decision validation and typed canonical promotion remain future work.
Structural checks cannot establish source fidelity, a participant's real identity,
implied agents, genuine independent corroboration or theological correctness.

Ignored narrative working caches are outside canonical-build backups. Keep
eligible pending packet/response files separately if needed. The curated
synthetic response/report in this repository contains only original technical
fiction and is not a template for inserting historical text without permission.

Code/schema changes change the exact archive engine identity even when the dev
version is unchanged. The earlier `fixture-build-final-v1.zip` and its recorded
matching wheel remain historical artifacts; retain them together. This milestone
records a different current-engine synthetic build check without overwriting
that earlier ZIP, wheel or reports. There is no silent migration or release.
