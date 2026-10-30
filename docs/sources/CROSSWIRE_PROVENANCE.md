# CrossWire SrKDIjekav: follow-up investigation

The later [submission-history investigation](CROSSWIRE_SUBMISSION_HISTORY.md)
recovered three primary archive records and added a manual metadata research
handoff. It clarifies upload credits without establishing the missing edition
or transcriber. This page retains the earlier metadata follow-up record.

Inspected 2026-10-30. Source remains **needs_review**. There are still no
historical corpus bytes, real passages, production locks, owner approvals or
publication clearance. This investigation retrieved only provider configuration
and catalogue metadata. The original source audit remains an earlier session
record; this file records the new evidence and unresolved gaps.

## What the primary provider configuration establishes

The configuration was discovered through CrossWire's public directory listings:
[SWORD mirror](https://www.crosswire.org/ftpmirror/pub/sword/) → raw → mods.d →
[srkdijekav.conf](https://www.crosswire.org/ftpmirror/pub/sword/raw/mods.d/srkdijekav.conf).
No Bible ZIP URL was inferred or downloaded.

The retrieved configuration is **910 bytes**, SHA-256
`67d1b3237912e57bb8c8300237dfdd39720f91b5e61faaa7ab568c315335fa1e`.
The response gave Last-Modified `Mon, 19 Jun 2017 10:38:01 GMT` and ETag
`"38e-5524dbaa6b440"`. Those are HTTP observations, not proof that a module ZIP
or corpus is unchanged. The exact metadata bytes are retained unchanged in the
ignored private evidence cache. The tracked assessment stores selected factual
fields and independent summaries, not a relicensed copy of the provider's prose.

The declarations identify zText compression with OSIS markup, Calvin
versification, heading support and NoParagraphs. They record a first-release
history dated 2017-06-18, minimum SWORD 1.8.0, a public-domain designation and a
contact field. **TextSource is absent.** They do not identify a print edition,
digital transcriber, source file, correction history or component inventory.
The contact field does not prove who transcribed or owns any particular material.
`Lang=sr` alone does not establish the actual script; no source text was examined.

The [provider news archive](https://crosswire.org/sword/newsarchive.jsp), entry
posted 2017-06-18 by refdoc, separately announces the two regional module forms.
This supports the module-release event, not a link to the 1868 print edition.
Search results from mirrors repeating the same About/history text are not
independent corroboration and were not used to clear the source.

## Bibliographic comparison lead

[Open Library OL23344280M](https://openlibrary.org/books/OL23344280M/Sveto_pismo_Staroga_i_Novoga_zavjeta.)
describes an 1868 Pest edition and links Internet Archive item
`svetopismostaro00daniuoft`. The
[Archive item metadata](https://archive.org/metadata/svetopismostaro00daniuoft)
was retrieved as metadata only after web research could not fetch it. It names
University of Toronto sponsorship, but includes degraded contributor strings,
language code `chu`, and null rights/license fields. No scan, OCR text, PDF,
EPUB or scripture file was downloaded. Catalogue data needs verification against
the physical/title-page witness and its item-specific use terms.

The two catalogue services describe the **same item**, not two independently
verified textual ancestors. Nothing inspected links that item to SrKDIjekav.
It remains a comparison lead, not a replacement base or an admitted source.
Its metadata SHA-256 is separately recorded in the assessment; it is not a
scripture checksum.

## Toolchain finding from the metadata follow-up

The [provider's module documentation](https://wiki.crosswire.org/DevTools:Modules),
Debugging modules section, warns that `mod2imp` skips linked entries and that a
round trip is not guaranteed lossless. A verse-count test on such output could
therefore conceal lost references. The
[configuration documentation](https://wiki.crosswire.org/DevTools:conf_Files)
distinguishes data driver, embedded markup, versification and display filters.
Declaring OSIS does not make the compressed package an OSIS XML download.
NoParagraphs does not reconstruct historical paragraphing or prove that headings
and other apparatus are absent.

At that research stage no SWORD binary had been executed and no real adapter
had been approved. The subsequent
[synthetic toolchain evaluation](SWORD_TOOLCHAIN_EVALUATION.md) now records two
local native builds and the exact measured behavior of SWORD 1.9.0. That build
emits linked text through mod2imp without retaining link identity, rather than
dropping that test slot as the older documentation warning suggests. No historical
module was acquired or tested, and no real adapter has been approved.
A valid future evaluation must pin the SWORD build/tools and checksums, isolate
the module library, inventory raw/link/empty entries and markup, preserve
headings/notes and original source spans, compare exact five-book mappings,
document missing original layout, and test link-aware reconstruction. Plain
text conversion or marker deletion cannot pass by convenience. The current
JEB transcript adapter also rejects a scheme different from the assessed source.

## Preliminary jurisdiction work

The earlier DE/US legal leads remain incomplete exact-edition assessments.
This follow-up adds official HR/BA/RS general-term references and a ME legislation
link. No source status becomes verified from these observations.

- Croatia: DZIV's [current-law index](https://www.dziv.hr/hr/zakonodavstvo/nacionalno-zakonodavstvo/autorsko-pravo-i-srodna-prava/)
  points to [NN 111/2021](https://narodne-novine.nn.hr/clanci/sluzbeni/2021_10_111_1941.html).
  Articles 119 and 126 describe the ordinary life-plus-70/calendar-year framework;
  article 127 retains attribution and respect obligations after expiry. Older
  DZIV HTML also appears in search and must not be mistaken for the current act.
- Bosnia and Herzegovina: the official institute's
  [FAQ](https://www.ipr.gov.ba/en/intellectual-property/copyright-and-related-rights/faq-on-copyright-and-related-rights)
  describes the general lifetime-plus-70 term and cites the 63/10 legislation.
  This is guidance, not a completed current consolidated-law or artifact audit.
- Serbia: the official office's
  [guidance](https://www.zis.gov.rs/en/rights/copyright-and-related-rights/)
  describes the general term and distinguishes moral rights. Source-edition,
  revision, related-rights and intended-use analysis remains open.
- Montenegro: the official
  [legislation page](https://www.gov.me/en/article/copyright-and-related-rights-3)
  supplies a Word law document posted 2024-11-15. The document-page fetch timed
  out and the download was unsupported application/msword in web research.
  Older WIPO results were not assumed to be current. Full law/term assessment
  remains not_assessed. No clearance inference is drawn from another country.

General term evidence supports investigating the historical translations; it
does not settle unknown revisers, components, databases, digitization, moral
obligations or the exact file. No professional legal review is claimed.

## Inspect the remaining admission gaps

```powershell
.\.venv\Scripts\python.exe -m jeb sources inspect --source crosswire-srkdijekav
```

This is a read-only, offline report. Exit 0 means inspection succeeded; consult
`admitted` and `admission_blockers` for readiness. It does not fetch a file,
refresh a hash, change status, or authorize ingestion. The new evidence-linked
`source-assessment` schema binds the dossier to the exact registry record and
validates evidence links. Historical admission now requires the known edition,
transcriber and verified edition/provenance/components/versification/adapter
checks in addition to the existing jurisdiction and artifact locks. This makes
the original exact-edition entry requirements explicit; it adds no automatic
legal decision or fictional human approval.

The source artifact's size/hash remain null. Metadata snapshot hashes are never
copied into corpus identity. See `sources/assessments/crosswire-srkdijekav.json`.
Its six concrete unanswered questions are the next external-evidence target.
No messages or requests to providers have been sent.
