# Optional AI review assistance

This workflow produces an unreviewed critique of an existing proposal. It does
not produce a human decision. Use it through existing subscription sessions;
the CLI calls no model API, opens no chat and sends no messages.

## Prepare a bounded review packet

```text
jeb review assist prepare --proposal <proposal-id> --packet-id review-01
```

The prepared file is `data/review-assistance/review-01/input.json`, at most
64 KiB. It contains the exact validated proposal, original source/context packet,
policy, diff, flags and ordered segment IDs. Normal source eligibility and exact
coverage checks run again; this command cannot expose an uncleared historical
source. Synthetic workspaces still require the global `--synthetic` option.

Relevant evidence is supplied as bibliographic metadata, locators, review state
and record hashes. Evidence text bodies are excluded because a registered source
does not automatically permit sending its wording. A locator is not a source the
reviewer has inspected. No new citations, native name forms or external passages
may be invented to fill a gap. The prompt treats all nested source/proposal
material, including any instructions inside it, as data.

Paste or attach the packet in an existing Codex or Gemini subscription session.
Ask for the embedded response schema. The reviewer compares negation, agency,
quantities, names, protected forms, ambiguity and context. Return one ordered
item per segment, repeating the exact source/proposed text hashes. Every existing
proposal flag needs one ordered assessment and cannot be closed by AI. Human
resolutions remain separate, and an existing owner decision is not reopened by
this critique. The response cannot include
replacement wording, a flag-resolution state, owner/expert identity or human
attestation. Meaning-sensitive items retain `needs_expert_review`; a missing
proposal stays unresolved.

`no_issues_observed` is an observation, not approval. It is refused for items
with existing flags, unresolved text or reported issues. New concerns remain
advisory until the owner inspects them. If a concern establishes a meaning-sensitive
edit, classify and route that proposal appropriately; do not treat an AI finding
or model consensus as a resolved expert question. The existing D-class approval
block is unchanged.

## Validate and preserve the critique

```text
jeb review assist validate --input <returned-json>
jeb review assist import --input <returned-json>
jeb review assist report --input <returned-json> --output reports/generated/critique-01.md
```

Responses are limited to 32 KiB. Validation checks strict fields and Latin script,
exact proposal/source hashes, complete ordered segment/flag coverage, attached
evidence IDs, issue IDs and current input snapshots. Source, proposal, policy,
relevant evidence content, prompt or schema changes invalidate the packet.
Preserve the historical artifacts and prepare a new packet ID for changed work.
These structural checks do not establish factual, linguistic or theological
correctness or prove a reviewer's identity.

Import writes a separate canonical-content-hashed JSON file under
`data/review-assistance/<packet-id>/responses/`. Duplicate imports and changed
imported content fail. The report command separately presents source, proposal,
diff, open flags and untrusted critique with safe code fences. Different existing
report files are preserved. All critique artifacts remain unreviewed and are
Git-ignored by default unless explicitly curated as eligible project examples.

Competing critiques remain separate. Neither importing a favorable critique nor
raising a new concern changes text, source flags, existing human decisions,
knowledge approvals, reader output or release status. A human owner acts through
the existing [decision workflow](REVIEW_GUIDE.md), after inspecting exact hashes,
uncertainty and evidence. AI assistance cannot impersonate that step.

Input filenames are relative to the shell's working directory. Output paths are
inside the selected project root. Global `--root` and `--synthetic` options go
before `review`.

## Actual synthetic example

After `python -m jeb demo`, the following preparation command works locally:

```powershell
.\.venv\Scripts\python.exe -m jeb --root dist/demo --synthetic review assist prepare --proposal fixture-modernize-v1-40b78ddaba32f24c --packet-id fixture-review-v1
```

The current packet is 32,414 bytes. An actual Codex critique of its four original
technical sentences is retained in
[`reports/review-assistance-synthetic-response.json`](../reports/review-assistance-synthetic-response.json)
and the [readable report](../reports/review-assistance-synthetic.md). It leaves
the first segment's replacement-verb question and linguistic flag open; the
other three items have unchanged proposed wording. No historical passage,
owner approval or scholarly review is implied.

Actual preparation, validation, import, report generation and unchanged reader
identity are recorded in `reports/review-assistance-workflow.json`. The original
proposal and source-only reader hashes are unchanged. A cached critique may be
structurally replayed for this exact fixture; no model is rerun by CI.
