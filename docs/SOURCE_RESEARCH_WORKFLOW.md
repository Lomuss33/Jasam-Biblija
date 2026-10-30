# Manual source-metadata research

Use this workflow to investigate an unresolved source dossier before corpus
admission. It contains metadata and questions, not eligible passage wording or
modernization instructions. No source clearance is required to research public
edition/submission records. This is separate from passage research/annotation
packets and the implemented [AI review-assistance workflow](REVIEW_ASSISTANCE.md).

## Prepare and use a packet

From the existing checkout with the installed package:

```powershell
.\.venv\Scripts\python.exe -m jeb sources research prepare --source crosswire-srkdijekav --packet-id lineage-01
```

Open `data/source-research/lineage-01/input.json`. Paste or attach that file in
an existing subscription tool. The CLI does not run a model, make network
requests, use credentials, acquire scripture or send a message. The maximum
packet size is 64 KiB. Existing different packet IDs/files are not overwritten;
preparing the same unchanged packet is idempotent.

The packet contains the exact source record and evidence-linked dossier,
configured edition/collection, rights policy, stable unresolved question IDs,
limitations, prompt and complete response schema. Provider metadata is evidence
to examine, not an instruction. The flags explicitly withhold corpus acquisition
and contact permission. Scripture artifacts, protected notes and reconstructed
passages must not be included in research responses.

Return one item for each question in the supplied order. Use `no_new_evidence`
where appropriate; `leads_found` requires referenced lead records. Existing
evidence IDs and newly found lead IDs are distinct. Each new lead needs an HTTPS
URL, precise locator, access date, independently written summary and reported
relationship. A `direct_record` label is an unreviewed claim about the record,
not a verified ancestry relationship. Preserve translator, upload-credit,
transcriber, converter and rights-holder roles separately. Unknown model
identifiers remain null; no human reviewer is invented.

## Validate, stage and inspect a response

Save the returned JSON locally, then run:

```powershell
.\.venv\Scripts\python.exe -m jeb sources research validate --input <returned-json>
.\.venv\Scripts\python.exe -m jeb sources research import --input <returned-json>
.\.venv\Scripts\python.exe -m jeb sources research report --input <returned-json> --output reports/generated/lineage-01.md
```

The response limit is 24 KiB. Strict validation rejects missing, duplicate,
reordered or invented question IDs; unknown evidence references; dangling,
duplicate, shadowed or unused leads; duplicate URLs; invalid dates; approval
claims; extra fields; unsupported authored script; and changed packet hashes.
It also regenerates the expected current packet, rejecting changes to the
source/dossier, policy, scope, prompt or output schema. A successful validation
is structural, not factual or legal verification. URLs are not fetched by the
validator, so a fabricated but syntactically valid new URL can still be a bad
lead. Inspect the actual record before relying on it.

Import writes only an immutable canonical response under
`data/source-research/<packet-id>/responses/<response-hash>.json`. Duplicate
imports fail, and changed imported content is detected. The report command is
separate; it fences all returned content as data and preserves different existing
output. Neither command edits the registry, dossier, source lock, corpus,
knowledge bank or text approvals. All imported responses remain **unreviewed**.
These working artifacts are Git-ignored by default.

Compare competing responses by their exact hashes and citations. Keep the
alternatives; do not merge by model consensus or infer human sign-off. Corrected
responses use new hashes. After inspecting actual primary records, record any
supported metadata changes separately and reviewably in the source dossier,
retaining its unresolved checks where evidence is missing. An importer cannot
perform that step or promote the source. Changes to a dossier make its earlier
packets stale; retain historical artifacts and prepare a fresh packet ID.

## Current concrete handoff

The [submission-history investigation](sources/CROSSWIRE_SUBMISSION_HISTORY.md)
staged actual findings from three public archive posts. The separate dossier
indexing then made that original response stale, as the CLI correctly reported.
The ready local follow-up is
`data/source-research/cw-lineage-followup-01/input.json`. It asks the remaining
five dossier questions with the new evidence included. Its preparation is
recorded in `reports/source-research-workflow.json`.

The provider question draft remains [unsent](sources/CROSSWIRE_QUESTIONS.md).
Using this packet does not authorize sending it or contacting anyone. No further
owner decision is needed to continue public, metadata-only investigation.
