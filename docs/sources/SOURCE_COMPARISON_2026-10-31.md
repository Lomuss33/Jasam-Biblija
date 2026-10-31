# Source comparison — 2026-10-31

Codex-assisted public evidence investigation, not human clearance. Existing source assessments and empty production lock remain unchanged. No contact, publication or expansion beyond GEN/MAT/MRK/LUK/JHN.

| Route | Verified observation | Provider claim / remaining gap |
|---|---|---|
| eBible srp1865 | Recovered actual [USFM ZIP via www](https://www.ebible.org/Scriptures/srp1865_usfm.zip), 1,370,190 bytes, and [USFX ZIP](https://ebible.org/Scriptures/srp1865_usfx.zip), 1,493,396 bytes after initial 403. Inspected FRT, INT, copr.htm and metadata. | Public Domain is a provider claim. FRT declares modernization/Ekavianization; INT credits a 1996 work. See component findings below. Exact transcriber, edition fingerprint and correction history remain gaps. |
| CrossWire SrKDIjekav | Downloaded actual [raw ZIP](https://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/SrKDIjekav.zip), 1,609,798 bytes. Contains six compressed OT/NT files and mods.d/srkdijekav.conf. Actual config says OSIS/zText, ZIP, BOOK, UTF-8, Calvin versification, OSISHeadings, NoParagraphs, version 1.0, first release 2017-06-18. CopyrightContact=ecce@ecce.cz. [Catalogue](https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=SrKDIjekav) independently retrieved but belongs to the same provider. | Public Domain, Ijekavski and historical dates are provider declarations, not fidelity or worldwide rights findings. No TextSource, print edition, transcriber or detailed correction log in the package config. Headings are enabled; this does not establish their author or rights. No original OSIS file bundled. Compressed verse content was not decoded in this pass; notes/introductions inventory and five-book fidelity remain unverified. Earlier Br upload credit remains a role/identity gap. |
| Historical scan | Directly inspected [general title n4](https://archive.org/download/svetopismostaro00daniuoft/page/n4.jpg), [OT contents n6](https://archive.org/download/svetopismostaro00daniuoft/page/n6.jpg), [Genesis n8](https://archive.org/download/svetopismostaro00daniuoft/page/n8.jpg), [NT title n740](https://archive.org/download/svetopismostaro00daniuoft/page/n740.jpg). Both title pages print Pest, British and Foreign Bible Society, 1868; translator credits agree with [Open Library](https://openlibrary.org/books/OL23344280M/Sveto_pismo_Staroga_i_Novoga_zavjeta.). Inspected pages are Latin, with Ijekavian wording. | [IA metadata](https://archive.org/metadata/svetopismostaro00daniuoft) says Robarts/University of Toronto, 984 images, ABBYY FineReader 8.0, possible-copyright-status NOT_IN_COPYRIGHT. These are repository statements, not legal findings. Its language code chu and damaged catalogue names demonstrate metadata imperfections. Open Library derives from IA: not an independent physical collation. |

## Completeness and usage

OT contents, Genesis opening and separate NT title are present. Image n975 is blank; n980 returned 404, despite imagecount=984. Leaf numbers must not be inferred from imagecount. Full page sequence, NT ending, missing/duplicate leaves and completeness of the five approved books have **not** been collated. The scan is a better identified edition, not yet a complete verified corpus. No content outside the approved scope was transcribed.

IA supplies download access and a NOT_IN_COPYRIGHT metadata label, with no specific licence URL in the retrieved item metadata. No new conclusion about all-jurisdiction digitization/database rights or platform conditions is asserted. Bibliographic identity and practical access are established separately from publication clearance; the existing rights assessment for DE/US/BA/HR/RS/ME still needs exact-edition completion. Modern library handwriting is excluded from the transcription; generated OCR and repository descriptions are not treated as historical authored text.

Missing transcriber/revision records are provenance gaps, **not evidence of infringement**. Equally, a provider's Public Domain label does not establish clearance of all headings, notes, introductions, revision contributions or generated apparatus. These two questions remain separate.

## Recommendation and concrete pilot

Prefer direct image transcription from this identifiable 1868 Latin edition for the next small research slice. It avoids assuming a digital source's lineage or making an Ekavian-to-Ijekavian conversion. Preserve translator and edition credits. Use digital candidates as comparison evidence only until lineage is supplied. No source has been admitted.

Prepared private, unapproved GEN 1:1–5 in `data/private-source-audit/GEN-1-1-5-review.md`, with n8/printed page 1 identification and one OCR correction record per verse. Each verse was compared against the page image. Only whitespace/line joining is normalized; no modernization or transliteration was performed. This is a research pilot for review, outside corpus/demo/reader/build inputs. Human checking remains outstanding. Raw downloads are ignored by Git. Sizes/hashes for acquired evidence are in `reports/source-audit-2026-10-31.json`. The metadata and entire compressed module are private evidence, not approval to add their other books.

## Short unsent provider message

Verified public contact route: CrossWire's [official support page](https://www.crosswire.org/sword/support/index.jsp) lists sword-feedback@crosswire.org for feedback. The downloaded module additionally gives ecce@ecce.cz as CopyrightContact; delivery or current availability of either address has not been tested.

Subject: SrKDIjekav 1.0 source-edition and component history

Hello, I am assessing SrKDIjekav 1.0 (2017-06-18) for a five-book research project. Could you point to records identifying (1) its exact print edition or earlier digital source and transcriber, including the role of the credited “Br”; (2) any corrections, regional/orthographic conversions and revision history; (3) the original OSIS and its redistribution terms; and (4) who supplied the headings, introductions or notes, which components the Public Domain statement covers, and known Calvin versification/link/empty-entry issues for Genesis, Matthew, Mark, Luke and John? I have not assumed that the translation dates identify the source edition. Existing records or stable links would be very helpful. Thank you.

Not sent. A reply could resolve the digital route but is not required to continue the independent scan research. No user documentation collection is requested.

## Recovered eBible components

Initial 403 was overcome with the www hostname and a browser User-Agent; USFX also downloaded. USFM contains FRT, INT, book files, copr.htm, keys.asc, signature.txt.asc and dejavuserif.css. USFX contains BookNames.xml, srp1865metadata.xml, USFX, VernacularAdditional/Parms XML and rights/signature/style files. Signatures were not cryptographically verified.

FRT describes a Cyrillic, Ekavianized, modernized and paragraphed text of an 1868 edition. The actual package is Latin: script conversion history remains unexplained. It gives no physical witness or publisher for that claimed base. Metadata explicitly labels the translation Revision, dateCompleted=1865; neither is an edition fingerprint. archivistName/dateArchived/dateUpdated/comments are empty. Packaged copr.htm gives source date 2026-01-03 and HTML generation 2026-10-30. Generation dates are not revision logs.

INT ends with a credit to Branko Bjelajac, Sveto pismo u Srba, chapter VIII, 1996. It includes historical claims and interpretive correction proposals. This verifies a separately attributed later component, not the truth of its claims or permission to reuse it. The blanket Public Domain notice does not explain that component's permission basis. No infringement conclusion follows. No introduction/correction material enters project knowledge or editorial text. This strengthens the recommendation for direct scan transcription.

Verified contact route: [eBible official contact form](https://ebible.org/contact.php), inspected 2026-10-31. Short unsent draft:

Hello, could you identify srp1865's exact 1868 print witness and transcriber, Cyrillic-to-Latin/Ekavianization/modernization history and dated correction log? FRT describes Cyrillic text while the package is Latin. INT credits Branko Bjelajac, Sveto pismo u Srba, chapter VIII, 1996: what permission covers this introduction and later headings/notes/revisions separately from the historical translation? Metadata labels Revision but archive history fields are empty. Stable records would help. Thank you.

No message sent. Entire downloaded archives remain private evidence, not approval to add their other books.
