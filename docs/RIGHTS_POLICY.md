# Rights gate and licensing policy

Assess each exact edition and digital artifact before ingestion. Online access,
a familiar translator name, a provider tag, a rewrite, design changes or a
similarity score do not establish adaptation/distribution rights. Do not use
synonym replacement, back-translation or stitching protected notes as a rights
strategy. No tool promises legal immunity or worldwide public-domain status.

The intended assessment scope is DE (maintainer), US (distribution infrastructure),
BA, HR, RS, ME (intended readers). The first session inspected preliminary DE/US
legal references. The follow-up adds HR's official act and BA/RS official
general-term guidance; ME's official law link was located but its Word text was
not inspected. No exact-artifact assessment is complete for any of these
countries. The rest of the EU is not assessed. A release's documented scope must fit the configured jurisdiction
list; do not silently narrow it to bypass unresolved rights. Software metadata
does not prevent readers accessing a file outside that scope.

German sections 64 and 69 supply the ordinary death-plus-70/calendar-year
calculation; sections 23, 70 and 71 require attention to adaptations, qualifying
scientific editions and first publication of previously unpublished works.
Database and digitization questions also require separate assessment. For the
owner-supplied Šarić death year 1960, the ordinary calculation yields the end of
2030 and possible entry from 2031-01-01, subject to applicable details. **Do not
automatically unlock anything on that date.** Later revisers and apparatus may
have separate rights. US rules must be assessed on the actual work/publication
facts, not inferred from a German or provider conclusion.

Legal references inspected 2026-10-30:

- [German Copyright Act](https://www.gesetze-im-internet.de/urhg/BJNR012730965.html),
  sections 23, 64, 69, 70, 71 and related database provisions.
- [US Copyright Office, Title 17 chapter 3](https://www.copyright.gov/title17/92chap3.html),
  duration provisions; not a completed foreign-edition assessment.

Only `verified_for_scope` records with evidence for **every configured country**,
exact format, SHA-256, size, identity, assessment author/date and a matching
reviewed lock can enter the pipeline. Candidate, needs_review, excluded and
unknown statuses fail closed. The lock binds the full source assessment as well
as the artifact. Edited upstream bytes, changed rights records and unavailable
snapshots must fail clearly; never silently substitute an edition or hash.

Historical admission also requires an evidence-linked source assessment under
`sources/assessments/`, bound to the current registry record. Its exact-edition,
digital-provenance, component-rights, versification-fidelity and adapter checks
must be verified with inspectable evidence. Missing edition identity/transcriber
data remain blocking. `jeb sources inspect` reports those gaps without changing
status or treating metadata snapshot hashes as corpus hashes. Synthetic fixtures
retain their explicit isolated exception and remain unreleasable.

Initial registration/assessment and lock creation are deliberately manual and
reviewable. There is no CLI for auto-clearing rights or refreshing hashes.
Schemas validate records, not the truth of a legal opinion. The initial source
audit is Codex-assisted research and **not human legal sign-off**. Seek focused
expert legal review for unresolved publication questions while independent
engineering continues.

`jeb sources research` prepares bounded metadata-only manual work packets for
unresolved dossier questions. It can stage returned observations and a review
report without acquiring scripture. Source/dossier, scope, policy, prompt and
schema changes invalidate the current packet. Imported leads remain unreviewed;
structural validation does not verify a URL's claims, identify a transcriber or
clear any rights. Registry, dossier checks and locks are never changed by this
workflow. Contacting a provider is a separate action requiring explicit owner
instructions; a research packet does not authorize sending its contents.

Keep raw bytes immutable locally with recorded checksums. Being Git-ignored or
private does not authorize prohibited use. Track only eligible metadata,
fixtures, approved editorial inputs and source snapshots where their permissions
allow. Make approved build inputs recoverable in a permitted archive before
release; reproducibility fails if only a vanished website had the file.

Protected contemporary translations, Dretar, TOB, Kršćanska sadašnjost,
Jerusalem Bible, modern Šarić revisions and commercial editions are contextual
bibliographic leads only unless precise independent permission is documented.
Do not ingest their passages, use them as rewrite inputs, bulk-copy study notes,
paraphrase notes to manufacture independence, or reproduce them merely because
they have a citation. Link when reproduction is not permitted. A restricted
comparison does not license reuse of its wording.

Our eligible original editorial contributions are dedicated under CC0-1.0 only
to the extent their contributors hold those rights. CC0 cannot cancel upstream,
database, personality or other contributors' rights. Preserve required
attribution/share-alike terms and check compatibility before combining sources;
the first pipeline deliberately handles one source per build. Original software
is MIT. Dependencies keep their own licenses. See the license matrix and official
texts. AI output is not automatically copyrightable, public domain or legally
clean. All contributors must disclose upstream material and AI assistance.

Synthetic demo `ZZ` is a fictional test jurisdiction and its fixture declaration
is not a historical source clearance. Synthetic outputs are explicitly opted
into, separately labelled and categorically barred from edition release.
