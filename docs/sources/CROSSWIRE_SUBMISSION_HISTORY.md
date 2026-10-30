# CrossWire submission-history investigation

2026-10-30. Primary public archive inspection, independently written metadata
summaries only. No historical scripture artifact acquired or compared; the source
remains `needs_review`, and all five dossier checks remain unresolved.

## New inspected records

The public archive became accessible by following the official mailing-list
information page. Earlier tool failures are retained in the prior session log;
they are not a claim that the records were permanently unavailable. The
[June 2017 thread index](https://crosswire.org/pipermail/sword-devel/2017-June/thread.html)
links the two module notices individually.

The [SrKDIjekav upload notice](https://crosswire.org/pipermail/sword-devel/2017-June/044747.html),
dated 18 June 2017, gives the credit **Br** without expanding its identity or
role. It is an automatic upload message, not a transcription statement. It
does not identify a print edition, original OSIS file or correction record.
Its generic update wording is insufficient to establish an earlier artifact or
revision, even though the configuration describes the first release.

The adjacent [SrKDEkavski notice](https://crosswire.org/pipermail/sword-devel/2017-June/044746.html)
credits **Tomas**. That is the separate Ekavian module; do not transfer the
credit to SrKDIjekav, merge the people or call either credit a rights holder or
transcriber. No identity is inferred from unrelated search matches or contact
fields. The registered historical translator credits are unchanged.

The [27 December 2014 development post](https://crosswire.org/pipermail/sword-devel/2014-December/041834.html)
by Peter von Kaehne mentions two Serbian texts planned for beta. It supplies no
module identifiers or edition/transcription chain. This is an earlier development
lead, not proof that those texts underlie the 2017 artifact. Nearby messages in
that discussion concern other modules and add no demonstrated Serbian lineage.

Three individual HTML snapshots, not a bulk mail archive, are kept privately:

- `cw-upload-ijek-2017.html`: 2,641 bytes, SHA-256
  `f2af1e420b1933906afb0925bb36eba92b53b90e253cd1de900396d6ff9c1d05`.
- `cw-upload-ekav-2017.html`: 2,669 bytes, SHA-256
  `59bc2737e413d766317219c440c66c1239d75184f7c37482bda4474540029b30`.
- `cw-two-serbian-2014.html`: 3,126 bytes, SHA-256
  `8937a64e19c2c26b953d6521022084f8f4cd9c866e1d940b40c92de8912018d2`.

Paths and independent summaries are recorded in
`sources/evidence/crosswire-submission-research.json` and linked into the dossier.
These metadata identities never substitute for the unknown scripture ZIP hash.
Search results dominated by downstream displays did not establish an independent
print witness. No mirror file or scripture API endpoint was fetched, and no verse
wording from those results was saved to the project.

## Reviewable research artifacts

The new [manual metadata workflow](../SOURCE_RESEARCH_WORKFLOW.md) was used on
these actual observations. Packet `cw-submission-history-01` contained five
unresolved question IDs. Its returned observations referenced three new archive
leads and remained unreviewed; validation/import/report all succeeded. The
[historical review report](../../reports/crosswire-submission-review.md) records
that exact earlier snapshot, without human or legal approval.

Separately, the inspected archive metadata was indexed by a local Codex edit in
the dossier. No source status, transcriber field, verified check or production
lock was changed. This is independent metadata indexing, not automatic promotion
of a model response. The original packet/response is now **stale**, and the CLI
correctly refuses to revalidate it against the changed dossier. Keep the old
artifact as history, not as the current research input.

A fresh five-question packet is ready locally at
`data/source-research/cw-lineage-followup-01/input.json`, SHA-256 (canonical
packet identity excluding its own hash field)
`f4b980da7684f7d0605e1ca72a59c00de4806204c3b4d39d50b8754b76c3cb28`.
Actual preparation, staging and stale-result checks are recorded in
`reports/source-research-workflow.json`.

## Evidence still needed

The next useful records identify Br's actual role and the original digital
source, its exact print ancestry, corrections and component permissions. The
2017 upload template and 2014 unnamed development post cannot supply those facts.
The existing provider question draft has been made more specific and remains
unsent. Contact still requires explicit instructions; public metadata research
can continue without sending anything. Historical ingestion, five-book fidelity
testing and the real editorial pilot remain blocked by the existing entry gate.
