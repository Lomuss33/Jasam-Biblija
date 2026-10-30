# Initial source audit: 2026-10-30

This is the first-session inspection record. The
[follow-up investigation](sources/CROSSWIRE_PROVENANCE.md) adds separately hashed
provider/catalogue metadata, the declared Calvin scheme, primary HR/BA/RS legal
leads, ME's law link and an evidence-linked readiness report. It does not clear
the source or add scripture text. The scope table below records the initial session.

**Result: zero cleared historical artifacts, no raw historical download, no
production source locks and no real textual coverage.** Exact source SHA-256 and
file sizes remain null. No human legal sign-off occurred. Phase 1 therefore
uses an original synthetic fixture. The lack of clearance blocks real ingestion,
not independent engineering.

## CrossWire SrKDIjekav: needs_review

The [module page](https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=SrKDIjekav)
identifies the historical translators, NT 1847 and OT completion 1865. Its
version is 1.0 (2017-06-18). It labels the language Ijekavski and distribution
public domain. These are provider assertions, not a complete audit.

Following its download link to the verification page exposed the actual
[raw ZIP link](https://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/SrKDIjekav.zip).
The browser research fetch reported unsupported application/zip; the artifact
was not downloaded through another tool because entry evidence remains
unresolved. Module script, exact base edition, later alterations, digital
transcriber, notes, mappings and actual Ijekavian passages remain unverified.
No SWORD installation/export toolchain has been evaluated. It is not USFM.

## eBible srp1865: needs_review

The [catalogue](https://ebible.org/find/show.php?id=srp1865) exposes a real
[USFM artifact link](https://ebible.org/Scriptures/srp1865_usfm.zip); it was
discovered, not inferred from a code. Browser research reports unsupported
application/zip; no file was ingested. The catalogue's displayed revision is
2026-01-03. The [rights page](https://ebible.org/srp1865/copyright.htm) labels
the work public domain and credits the two translators. It reports Vienna NT
publication 1847, OT addition 1867, complete Bible 1868. The precise edition,
later revisions and transcription provenance have not been established. The
CrossWire and eBible dating statements concern different milestones and need
checking against bibliographic/edition evidence, not forced reconciliation.

The displayed [Genesis 1 sample](https://ebible.org/srp1865/GEN01.htm) uses Latin
script and Ekavian forms (for example, `beše`, `svetlost`). This limited
observation does not characterize every passage or prove what the ZIP contains.
It does refute treating the tag alone as proof of Ijekavian text. Wording was
inspected for source assessment, not copied into the repository corpus.

## Šarić / eBible hrv: excluded

The [provider page](https://ebible.org/hrv/copyright.htm) names Ivan Šarić and
labels the translation public domain. The owner's bibliography supplies death
year 1960 and historical 1941-1942 editions. Under ordinary German term rules
that creates an unresolved conflict with the provider label; see the rights
policy. The supplied [scholarly PDF](https://hrcak.srce.hr/file/38594) returned
HTTP 418 to the research fetch, as did a related `38593` lead. The death year
was therefore **not independently confirmed from that paper in this session**.
No exact hrv edition or downloadable artifact was inspected; none is guessed.
The source remains excluded, without date-based automatic admission.

## Lifespan references and limits

The [Hrvatska enciklopedija Karadžić entry](https://www.enciklopedija.hr/clanak/karadzic-vuk-stefanovic)
supports death year 1864. Only the year is used here; calendar styles and other
historical claims on that page are not adopted as project conclusions. The
[Serbian Academy Daničić entry](https://www.sanu.ac.rs/en/member/danicic-djura/)
supports death in Zagreb on 17 November 1882. These support a promising
historical-text lead, not clearance of modern digital files or apparatus.

## Scope actually assessed

| Scope | Work done | Clearance |
| --- | --- | --- |
| DE | Official term/edition provisions inspected preliminarily | Unresolved exact edition and related rights |
| US | Official duration chapter inspected preliminarily | Unresolved exact work/publication facts |
| BA, HR, RS, ME | No country-specific assessment | Not assessed |
| Other EU / worldwide | No general assessment | No clearance claimed |

The source register records the evidence, access date, roles, missing facts,
jurisdiction status and limitations. All unresolved exact file hashes/sizes are
null rather than invented. `sources/evidence/initial-audit.json` stores an
independently written inspection log, not copied notes or external legal opinions.

## Next admission work

Start with the CrossWire Ijekavian candidate: identify the precise historical
edition and digital history, compare it with an eligible facsimile, establish
included components and permissions per country, and evaluate a reproducible
SWORD export. Record any unresolved alteration instead of calling the file
faithful by assumption. A narrowly cleared alternative historical transcript is
also acceptable if its exact identity is documented. Only after that assessment
may the artifact be locked, ingested and used in the five pilot passages.
