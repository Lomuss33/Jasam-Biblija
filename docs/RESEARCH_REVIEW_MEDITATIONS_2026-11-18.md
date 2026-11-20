# Meditations source review — 2026-11-18

Status: **research observation, not legal clearance**.

## Observed

- Project Gutenberg entry 15877 identifies George Long (1800–1879) as
  translator and states public-domain availability in the USA. That statement
  is provider/jurisdiction-specific and does not by itself clear use under DE
  rules.
- The Gutenberg file index exposes `https://www.gutenberg.org/files/15877/15877-8.txt`
  and `15877.txt` as 441K text artifacts (last modified 2020-12-14 in the
  indexed listing). The exact bytes and SHA-256 have not been downloaded or
  recorded because the configured DE/HR rights gate is still unresolved.
- Project Gutenberg entry 2680 is a separate eBook and must be treated as a
  separate edition/artifact; its text must not be merged with 15877.
- Perseus' repository documentation states that, unless otherwise indicated,
  its canonical materials are CC BY-SA 4.0. The exact Marcus Aurelius text,
  editorial layer and version still need to be identified before reuse.
- The Library of Congress page is a bibliographic/digital-object record. Its
  catalogue presence is not a licence for extracting or redistributing the
  scanned artifact.
- IEP is a useful secondary orientation source, but its article is not a
  public-domain source text for this project.

## Blockers before canonical source creation

1. Capture the exact downloadable artifact URL, edition identity and SHA-256.
2. Record the applicable licence/rights statement for each jurisdiction
  (DE), including whether only the provider's US statement is known.
3. Separate source text, transcription/encoding, annotations and website UI
   rights.
4. Decide whether the project will store bytes, only links/locators, or a
   permitted transcription. The project default is link plus an immutable local
   artifact whenever legally permitted; link-only is allowed only with a
   documented legal/evidentiary blocker. Until that decision is recorded, keep
   `content_acquired: false`.
5. Have a human review the rights dossier; AI research is not approval.

## Sources consulted

- [Project Gutenberg 15877](https://www.gutenberg.org/ebooks/15877)
- [Project Gutenberg permission policy](https://www.gutenberg.org/policy/permission)
- [Project Gutenberg 2680](https://www.gutenberg.org/ebooks/2680)
- [Perseus canonical Greek Lit README](https://github.com/PerseusDL/canonical-greekLit/blob/master/README.md)
- [Library of Congress record 27007869](https://www.loc.gov/item/27007869/)
- [Internet Encyclopedia of Philosophy](https://iep.utm.edu/marcus-aurelius/)
