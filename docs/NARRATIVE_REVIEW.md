# Unsigned narrative inspection handoff

Export a readable inspection aid for one exact **imported** narrative response:

```powershell
jeb --root dist/demo --synthetic knowledge narrative review export --packet-id fixture-narrative-v1 --response-sha256 14daac25578624d336fa2b0f004318bd662ee874f212d69b56e9cbdceaee6733 --output reports/narrative-review.md
```

The command reads the immutable response in
`data/narrative-proposals/<packet-id>/responses/<full-sha256>.json` and its
current packet. It rejects missing imports, shortened/uppercase hashes, unsafe
IDs, substituted responses and stale source/policy/display/knowledge inputs.
It repeats normal narrative validation and source admission; an old packet does
not give permission to display a now-blocked source. Use the full lowercase
response hash returned by import, not a file checksum from a different encoding.

This export writes only the requested Markdown file within the project. It
creates zero decisions, approvals, canonical records or curation actions. There
is no narrative `review apply` operation. The report is unsigned, has no owner
answers or generated attestation, and cannot be submitted as annotation decisions.
Existing recorded support/name approvals are displayed as prior records only;
they do not approve the proposed narrative. No URL is fetched or opened.

## What the handoff shows

- Exact packet/response/corpus/policy/source-metadata/knowledge-namespace hashes,
  each node hash and each referenced support record/envelope hash.
- Ordered selected-segment coverage, including `no_draft`, followed by separate
  original source, normalized source and current reader wording. Raw record byte
  spans and any prior text decision ID remain separate from character offsets.
- Separate `source_narrative`, `historical_claim` and `fiction` sections. Empty
  sections say no nodes were proposed. Contribution credit, rationale and
  uncertainty remain attached to every node.
- Entity mentions and proposed event roles beside literal source excerpts.
  Unmapped labels remain exact source wording. Omitted agents are not supplied
  by the report, and equal labels do not establish identity across mentions.
- Story presentation positions and relation tables. Presentation order is not
  historical chronology. A proposed source-stated chronology relation retains
  its exact anchor and needs human semantic inspection. Uncertain relations do
  not establish ordering edges. Fiction is labelled and never evidentiary support.
- An index of deduplicated exact display spans with exclusive-end Unicode
  offsets, exact slice hashes and up to 80 characters of context on each side.
  Table previews show at most 80 characters and explicitly link to the full
  slice; long previews are labelled. Original text is never silently truncated.
- Transitive typed evidence/claim/entity/related links, categories and exact
  record identities. Related/entity links are not independent corroboration.
  Draft support envelopes are shown intact. Existing canonical records are
  limited to attached catalogue metadata plus typed links and approval/provenance
  identities; additional canonical note text is not copied into the report.
- Selected name mappings, if any, with complete original mapping, chosen display,
  witness fields, approved content hash, full mapping hash and approval hash.
  These are exact prior approval identities, not new attestations.
- Original tool identity, stated limitations and the complete unreviewed response
  for checking the readable view against the original data.

The report format is `jeb-narrative-review/1`; no new stored-data schema or
canonical narrative type is introduced. It reuses the existing versioned packet,
node and response schemas. Literal `svjet`, `vrjeme`, `covik`, `razumit`, Latin
authorship and exact GEN/MAT/MRK/LUK/JHN scope retain their existing gates.

## Determinism and bounds

Identical current inputs produce identical bytes; no review date, reviewer or
decision is invented. Export to the same path with identical bytes is idempotent.
Different existing content is never overwritten. All validation and rendering
finish before the one atomic output write. Markdown output is bounded to 1 MiB;
an oversized handoff fails with no partial file and requires a smaller packet.
Existing 96 KiB packet and 48 KiB response limits also apply.

Free text remains in adaptive code fences. Returned table text encodes ASCII
punctuation as literal character entities and makes line breaks visible, so
returned Markdown/HTML/link syntax cannot change the report structure. Exact
unencoded wording remains in the full fenced slices and original response.
No returned content is executed and no installation/service is needed.

## Actual original synthetic handoff and limits

The [curated synthetic handoff](../reports/narrative-review-synthetic.md) reads
the existing eight nodes and one witness proposal. It indexes four distinct
source spans. Five nodes describe the invented fixture and three belong to a
separate fictional card-sorting scene; there are no historical-claim nodes or
selected name mappings. It adds no drafts and changes neither the earlier five
annotation drafts nor reader output. Every proposed narrative/support item
remains unreviewed. This is original technical fiction, not scripture coverage.

Observed commands, identities and verification/package results are recorded in
`reports/narrative-review-workflow.json`, `reports/narrative-review-verification.json`
and `reports/narrative-review-package.json`. No real historical source is cleared.
Structural checks cannot prove interpretation, independent scholarship, rights,
participant identity or historical truth. A separate human decision format and
typed promotion workflow are future work. Pending narrative caches remain
outside canonical-build archives; retain their permitted working files separately.


## Validation-only decision documents

`jeb knowledge narrative review validate --decisions PATH` reads the shipped
`narrative-review-decisions` 1.0 schema. It requires an exact imported response,
`context_sha256 = digest(current validated packet)` and one item per typed node
(`node:ID`) and original support envelope (`support:ID`), each with its exact
canonical hash. The whole packet binds policy, spans, selected name approval
identities, source and support context; the response binds contribution credits.
Every item requires meaning/roles, support, category/uncertainty, contribution
rights and attribution checks and a nonblank rationale. Owner identity, date and
human attestation are declarations; validation cannot authenticate a human or
establish the truth of those declarations. AI must not fill real reviewer fields.

Even submitted `approved` states only validate document structure and currentness.
The command writes nothing, creates no approval or receipt and promotes nothing.
Graph validation/currentness reuse the exact imported-response validator. There
is no narrative apply endpoint; annotation promotion remains separate. Synthetic
attestations occur only in automatically removed test workspaces.
