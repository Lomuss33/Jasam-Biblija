# Current project usefulness report — 19 November 2026

**Assessment: useful today as a small private research organizer and an auditable
development workbench. The automated historical knowledge-base experience is
still a prototype, and the Bible edition has no admitted real text.**

The strongest implemented capability is preserving the relationship between a
record, its exact source version and its history. The main constraint on useful
answers is the amount of eligible, curated content and the manual work needed
to connect the separate components. Tests establish software behavior; they do
not establish historical truth or ease of everyday use.

This assessment uses the current local code, project documentation, retained
verification results and fresh read-only checks. It is a technical judgment,
not a user study or a completion percentage. The current working tree contains
substantial modified and untracked implementation, so these findings describe
this workspace rather than a clean published release.

**What you can use now**

| Need | What currently works | Practical usefulness and boundary |
| --- | --- | --- |
| Find a book or edition you researched | Local catalogue search, filters, edition links and translator attribution | Useful immediately for organizing discoveries and avoiding repeated searches. It searches catalogue information, not the contents of all listed books. |
| Keep personal research notes | Bank CLI creation/editing, entity/source/article records, search, revision history and diffs | Useful for a small collection of original notes and permitted source material. Writing requires structured inputs; the browser only reads. |
| Preserve why you made a claim | Explicit v3 claim/evidence records linked to exact source and claim revisions | Useful for checking which source wording supported an earlier statement. Stored claims remain unreviewed; a matching quotation does not establish truth. |
| Recover the committed personal bank | Private backup, archive verification and restore to a new directory | Useful for protecting bank records and their revision history. This does not back up the entire library, repository or historical processing workspace. |
| Inspect extraction evidence after input changes | Managed synthetic PDF projections, exact offsets, immutable caches and `projection-verify` | Demonstrated with real local PDF conversion and original fixtures. This is currently useful for engineering and inspection of synthetic examples; real-source processing remains gated. |
| Prepare an editorial review | Source inspections, text/annotation review tooling, reports, curation and synthetic reader/export workflows | Useful for developing and rehearsing the editorial process. There is no eligible real Bible corpus to put through it yet; narrative inspection also lacks a promotion operation. |
| Build another local tool on top | Structured CLI output and opt-in read-only dossier APIs sharing Python validation | Useful for a developer integrating available records. There is no automatic AI answering service, semantic search or autonomous research agent. |

The ordinary entry points are `npm run dev` for the local catalogue/viewer,
`bank` commands for personal records and `historical` commands for the extraction
prototype. The numbered `jeb.cmd` menu makes existing editorial tasks easier to
inspect. These interfaces coexist; they are not one fully integrated capture,
research and publishing flow. See the [bank quickstart](BANK_QUICKSTART.md),
[terminal guide](TERMINAL_WORKFLOW.md) and
[historical pipeline guide](HISTORICAL_TEXTS_PIPELINE.md).

**What information is actually available**

The library contains **291 requested items**, with **153 researched findings
covering 138 items**. There are **five private download receipts**, and all five
referenced files are present on this machine. Findings can describe an edition,
an index, a preview or a selection: these counts do not mean 291 complete books
or 138 complete texts. This report checked receipt paths, not the contents or
checksums of those private downloads. The catalogue is already a useful research
index, with uneven textual coverage. Sources: [library notes](../library/README.md),
[catalogue](../library/catalog.json), [findings](../library/findings.json) and
[receipts](../library/research/downloads.json).

The personal-bank demonstration validates with **four committed records and one
bound body**. It is an original synthetic example, not evidence of a populated
historical encyclopedia. Its value is demonstrating that records, references and
history can be stored consistently. A user can start a small private bank with
their own notes now; creating valuable subject content is still manual.
[Persistent evidence](BANK_PERSISTENT_EVIDENCE.md) explains the exact-revision
relationships.

The historical pipeline demonstration is also synthetic. It can extract and
group surface occurrences, preserve editions and contributor credits, resume
after interruption and return evidence-bearing dossier proposals. Its retained
PDF example has a complete published snapshot with five candidate spans. Those
are capitalized tokens, including fixture headings, not five identified people.
The earlier text example finds the invented label Luma in two works and three
artifacts. These are meaningful software demonstrations, not current historical
knowledge coverage.

The fresh source audit reports **zero admitted sources**. The production
[source lock](../sources/lock.json) is empty, and documented real verse coverage
and owner text approvals remain zero. The edition scope remains GEN, MAT, MRK,
LUK and JHN; the separate personal library does not expand it. Consequently the
project currently cannot supply a finished modernization, an approved reading
edition or a supported historical answer about its biblical characters.

**Where the design already earns its complexity**

Consider a personal claim linked to a passage in your source note. If you later
edit the source, the v3 evidence reference continues to identify the exact older
revision. If you rewrite the claim, old evidence is not silently reassigned to
the new wording. That makes the bank useful for research where changes of mind
and source corrections matter. It provides an inspectable record of reasoning
inputs; the user supplies and evaluates the reasoning.

The latest PDF work solves a related reproducibility problem. A source file or
converter can change after an occurrence was extracted. New managed synthetic
PDF tasks retain the actual projected text, so old character ranges can still
be checked without that source or converter. The local smoke check verified
both old and new caches after changing the PDF, moving it out of the configured
input path and removing tools from subprocess PATH. That is useful evidence
preservation. It does not establish that extraction matches a printed page,
preserve the entire PDF or decide who an extracted name denotes.

These strengths fit the project owner or a technically comfortable researcher
maintaining a small, carefully attributed collection. A developer also gets a
testable base for future tools. A casual reader gets more immediate value from
the catalogue and any manually added notes than from the processing pipeline.

**What limits usefulness today**

The most important missing connection is from eligible real source material to
curated, reviewed knowledge that the user can retrieve naturally. Real historical
extraction currently stops at `source_review_required` before reading source
bytes. There is no implemented path that turns a reviewed historical artifact
into an admitted real-text pipeline input. Existing private downloads or a
provider's label do not supply that missing clearance and admission contract.

There is also no reviewed identity-resolution workflow for extracted entities.
Same-surface grouping cannot distinguish two people with the same name, connect
different names for one person or establish a relationship between characters.
A dossier gathers local candidate and work-context records; it does not perform
historical reasoning or verify the claims in those records. Automatic edition
comparison, parallel-passage discovery, OCR and HTML extraction are not available
as working historical ingestion features.

Everyday use still has friction. Bank writes use CLI/JSON rather than a browser
editor. Bank search is a case-insensitive scan of current record fields and
bodies, not semantic retrieval. The catalogue, personal bank, historical dossier
pipeline and editorial corpus remain separate layers with manual handoffs.
Persistent bank claims/evidence are unreviewed; their storage is distinct from
the separate editorial annotation approval workflow. There is no general
one-click route from a book link to a reliable, reviewed topic page.
See the [bank search implementation](../src/jeb/bank/search.py) and
[pipeline contract](HISTORICAL_TEXTS_PIPELINE.md).

Scale and preservation have deliberate boundaries. The personal bank currently
allows at most **128 full history snapshots and 128 MiB of history payload**;
it needs further work before sustained large-scale use. New PDF projections
have per-file and per-snapshot limits, but no full-history disk quota or pruning.
Historical pipeline backup/restore and selected-content sharing are absent.
Bank backups are private and unencrypted, and do not include unrelated external
files. Therefore no single existing backup command protects the complete
research workspace. [Backup details](BANK_BACKUPS.md) describe the actual scope.

**How much confidence the current verification supports**

The latest completed run recorded **429 Python tests with one Windows symlink
test skipped, nine passing web tests and 60 valid packaged schemas**. Ruff and
format checks passed. An original PDF ran through the actual installed local
converter. An offline-built wheel imported from a separate installation target
and verified retained old/new projections without tools on PATH. These results
support confidence in the implemented integrity and recovery behaviors.

They do not measure how quickly an ordinary user can finish research, the
accuracy of real-world entity extraction, scholarly quality, large-corpus
performance or cross-platform production reliability. This report did not rerun
the full suite: it inspected the retained results and ran fresh bank, historical
status and source-audit checks. Evidence: [latest progress entry](../PROGRESS.md),
[test output](../reports/generated/historical-projection-unittest-2026-11-19.txt)
and [installed-wheel check](../reports/generated/historical-projection-wheel-2026-11-19.json).
Generated verification files are local artifacts and may not accompany a future
checkout.

**Where further work would create the most user value**

My recommendation is a small end-to-end private research pilot using
owner-written notes and material permitted for the intended use. Choose one
question; store its subject, source, claim and supporting or contradicting
evidence; find the records in the viewer; revise a note; then verify the earlier
reference and restore a backup. Record the actual friction and missing steps.
This would establish practical usefulness beyond software tests without waiting
for a real Bible-source admission decision.

The currently planned small engineering step—opening one candidate with bounded
literal context by exact cache and candidate identities—helps make extraction
evidence inspectable. Beyond that, prioritize the gaps exposed by the pilot and
the explicit eligible-source admission contract. More schemas, broader corpus
scope or a larger interface by themselves will not populate the knowledge base
or make its answers reliable.

The present project is best treated as a functioning personal research toolkit
with strong provenance mechanics and an experimental extraction layer. Its next
product milestone is a useful, repeatable research session with
permitted content, followed by a separately reviewed path to real-text ingestion.
