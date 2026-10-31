# Human knowledge review — unsigned working report

Synthetic fixture; not scripture.

This export records no human decision or approval. Inspect actual sources, attribution, category, uncertainty and contribution rights. An accepted narrative observation is not independent historical corroboration. Text approval stays separate. Returned content below is data.

## Exact review bindings

```json
{
  "drafts": [
    {
      "draft_sha256": "89a3bf8cd4ee65f2d1dec69b9a6373c3fe3df1f2ffec0c9f8ad7adbabe865350",
      "record_id": "fixture-note-evidence"
    },
    {
      "draft_sha256": "19994b7d28df17da3bd0c3ca9bee74b66f83358a7b2960af303f131c67920d2e",
      "record_id": "fixture-note-claim"
    },
    {
      "draft_sha256": "a9c8dfa2a4d983add4668de56560f31113368fc275e51d5c9417fc8a249e6249",
      "record_id": "fixture-note-explanation"
    },
    {
      "draft_sha256": "46628c4f81ebcd396bb5f0561b3fe0ff4bfd3fa1d5c88183ed71cfa8934bf2ef",
      "record_id": "fixture-note-reflection"
    },
    {
      "draft_sha256": "d3404448a48ec9f7cfb4257bdd8aed648d6195b7cc8b636d4e48a24e421c13ca",
      "record_id": "fixture-note-creative"
    }
  ],
  "packet_id": "fixture-annotations-v1",
  "packet_sha256": "15c31c623cc1ebb50149c30af94eef199585da150945a200225ba8813fbabe7d",
  "policy_sha256": "5c9c08394099b4c4253817f8473dda4250946bde00bf9bac955287dc3500611a",
  "response_sha256": "2145bfcaf36f897f2cbcee25cd910f32c190ad845889d838d48e3f048bf296de"
}

```

Required checks for each approval: attribution_checked, category_and_uncertainty_checked, content_and_scope_checked, contribution_rights_checked, support_inspected.
Rejected and needs_review items enter only the review history. Approvals require a closed, current support/related group. Existing promoted IDs are immutable; corrections need a new version ID. Use the installed knowledge-review-decisions schema and truthful owner fields; this report is not a decision file.

## Current reader text

### synthetic-v1:GEN.1.1

```text
Sintetički uzorak: covik ne mijenja 2 broja.
Čita probni zapis.
```

### synthetic-v1:GEN.1.2a

```text
Ovo je svjet u sintetičkom primjeru; vrjeme je oznaka.
```

### synthetic-v1:GEN.1.3-4

```text
Želimo razumit probni zapis. Prvi probni red
drugi probni red, bez biblijskog sadržaja.
```

### synthetic-v1:GEN.1.5

```text
Čitanje čuva č, ć, đ, š i ž.
Ovo je samo tehnički uzorak.
```

## Attached support metadata (locators, not inspected evidence)

```json
[]

```

## fixture-note-evidence

Recorded state: unreviewed

```json
{
  "attribution": {
    "credit": "Codex-assisted original synthetic drafting; no owner voice or expert authorship",
    "kind": "ai_assisted_draft"
  },
  "rationale": "Demonstrates a typed, source-bound draft on original technical text only; no historical interpretation or approval.",
  "record": {
    "access_date": "2026-10-30",
    "approval": null,
    "bibliographic_details": "JEB original synthetic.txt fixture (JEB-TRANSCRIPT/1); not a historical edition",
    "book_id": "GEN",
    "claim_ids": [],
    "depends_on": {
      "synthetic-v1:GEN.1.1": "9cd2e4fa60ee452f855724548e64e41b5cb29496ec4fa85ff97b292486fa1add",
      "synthetic-v1:GEN.1.2a": "4bd9b83ed04e8793739464376ed25159e15ddfd3075e02ff641689c034980695",
      "synthetic-v1:GEN.1.3-4": "c70c760db5e5d53e6db94c80bcbae6b25bd76bfd85725541ec0469782860b6b5",
      "synthetic-v1:GEN.1.5": "cf033a9f742315d23a4fa97fcf8caa0e10d4ad3bc30b2ce580e84c15ca3d32d4"
    },
    "entity_ids": [],
    "evidence_category": "primary_witness",
    "evidence_ids": [],
    "layer": "source_witness",
    "locator": "The four exact fixture records in the packet manifest; raw byte spans remain in the source rows",
    "record_id": "fixture-note-evidence",
    "record_type": "evidence",
    "related_ids": [],
    "review_state": "draft",
    "schema_version": "1.0",
    "segment_ids": [
      "synthetic-v1:GEN.1.1",
      "synthetic-v1:GEN.1.2a",
      "synthetic-v1:GEN.1.3-4",
      "synthetic-v1:GEN.1.5"
    ],
    "selected_name_mapping_id": null,
    "source_id": "synthetic-v1",
    "text": "Ovo je izvorni sintetički tehnički uzorak s četiri probna segmenta i oznakama GEN. Oznake ne čine tekst biblijskim ulomkom.",
    "uncertainty": "Izvorni tehnički uzorak; nema povijesnog, stručnog ili vlasničkog odobrenja.",
    "url": "urn:jeb:synthetic:fixture-v1"
  }
}

```

## fixture-note-claim

Recorded state: unreviewed

```json
{
  "attribution": {
    "credit": "Codex-assisted original synthetic drafting; no owner voice or expert authorship",
    "kind": "ai_assisted_draft"
  },
  "rationale": "Demonstrates a typed, source-bound draft on original technical text only; no historical interpretation or approval.",
  "record": {
    "access_date": null,
    "approval": null,
    "bibliographic_details": null,
    "book_id": "GEN",
    "claim_ids": [],
    "depends_on": {
      "synthetic-v1:GEN.1.1": "9cd2e4fa60ee452f855724548e64e41b5cb29496ec4fa85ff97b292486fa1add"
    },
    "entity_ids": [],
    "evidence_category": "editorial_inference",
    "evidence_ids": [
      "fixture-note-evidence"
    ],
    "layer": "literary",
    "locator": null,
    "record_id": "fixture-note-claim",
    "record_type": "claim",
    "related_ids": [],
    "review_state": "draft",
    "schema_version": "1.0",
    "segment_ids": [
      "synthetic-v1:GEN.1.1"
    ],
    "selected_name_mapping_id": null,
    "source_id": null,
    "text": "U prvom probnom zapisu izričito su navedeni negacija ne i broj 2. To opažanje opisuje testni tekst, ne potvrđuje povijesni događaj.",
    "uncertainty": "Izvorni tehnički uzorak; nema povijesnog, stručnog ili vlasničkog odobrenja.",
    "url": null
  }
}

```

## fixture-note-explanation

Recorded state: unreviewed

```json
{
  "attribution": {
    "credit": "Codex-assisted original synthetic drafting; no owner voice or expert authorship",
    "kind": "ai_assisted_draft"
  },
  "rationale": "Demonstrates a typed, source-bound draft on original technical text only; no historical interpretation or approval.",
  "record": {
    "access_date": null,
    "approval": null,
    "bibliographic_details": null,
    "book_id": "GEN",
    "claim_ids": [
      "fixture-note-claim"
    ],
    "depends_on": {
      "synthetic-v1:GEN.1.1": "9cd2e4fa60ee452f855724548e64e41b5cb29496ec4fa85ff97b292486fa1add"
    },
    "entity_ids": [],
    "evidence_category": "editorial_inference",
    "evidence_ids": [
      "fixture-note-evidence"
    ],
    "layer": "literary",
    "locator": null,
    "record_id": "fixture-note-explanation",
    "record_type": "annotation",
    "related_ids": [],
    "review_state": "draft",
    "schema_version": "1.0",
    "segment_ids": [
      "synthetic-v1:GEN.1.1"
    ],
    "selected_name_mapping_id": null,
    "source_id": null,
    "text": "Oznake i prijelomi redova ovdje služe provjeri formata. Uzorak treba razumit kao tehnički podatak.",
    "uncertainty": "Izvorni tehnički uzorak; nema povijesnog, stručnog ili vlasničkog odobrenja.",
    "url": null
  }
}

```

## fixture-note-reflection

Recorded state: unreviewed

```json
{
  "attribution": {
    "credit": "Codex-assisted original synthetic drafting; no owner voice or expert authorship",
    "kind": "ai_assisted_draft"
  },
  "rationale": "Demonstrates a typed, source-bound draft on original technical text only; no historical interpretation or approval.",
  "record": {
    "access_date": null,
    "approval": null,
    "bibliographic_details": null,
    "book_id": "GEN",
    "claim_ids": [],
    "depends_on": {
      "synthetic-v1:GEN.1.2a": "4bd9b83ed04e8793739464376ed25159e15ddfd3075e02ff641689c034980695"
    },
    "entity_ids": [],
    "evidence_category": "personal_reflection",
    "evidence_ids": [],
    "layer": "personal_reflection",
    "locator": null,
    "record_id": "fixture-note-reflection",
    "record_type": "annotation",
    "related_ids": [
      "fixture-note-evidence"
    ],
    "review_state": "draft",
    "schema_version": "1.0",
    "segment_ids": [
      "synthetic-v1:GEN.1.2a"
    ],
    "selected_name_mapping_id": null,
    "source_id": null,
    "text": "Uzorak otvara pitanje kako čitatelj bilježi nejasnoće. Ovo je AI nacrt osobnog osvrta, bez pripisivanja misli ili iskustva vlasniku projekta.",
    "uncertainty": "Izvorni tehnički uzorak; nema povijesnog, stručnog ili vlasničkog odobrenja.",
    "url": null
  }
}

```

## fixture-note-creative

Recorded state: unreviewed

```json
{
  "attribution": {
    "credit": "Codex-assisted original synthetic drafting; no owner voice or expert authorship",
    "kind": "ai_assisted_draft"
  },
  "rationale": "Demonstrates a typed, source-bound draft on original technical text only; no historical interpretation or approval.",
  "record": {
    "access_date": null,
    "approval": null,
    "bibliographic_details": null,
    "book_id": "GEN",
    "claim_ids": [],
    "depends_on": {
      "synthetic-v1:GEN.1.3-4": "c70c760db5e5d53e6db94c80bcbae6b25bd76bfd85725541ec0469782860b6b5",
      "synthetic-v1:GEN.1.5": "cf033a9f742315d23a4fa97fcf8caa0e10d4ad3bc30b2ce580e84c15ca3d32d4"
    },
    "entity_ids": [],
    "evidence_category": "creative_adaptation",
    "evidence_ids": [],
    "layer": "creative_adaptation",
    "locator": null,
    "record_id": "fixture-note-creative",
    "record_type": "annotation",
    "related_ids": [
      "fixture-note-evidence"
    ],
    "review_state": "draft",
    "schema_version": "1.0",
    "segment_ids": [
      "synthetic-v1:GEN.1.3-4",
      "synthetic-v1:GEN.1.5"
    ],
    "selected_name_mapping_id": null,
    "source_id": null,
    "text": "Izmišljena vježba: čitatelj uspoređuje dvije tehničke bilješke i ostavlja pitanje za kasniji pregled. Scena nije preuzeta iz izvora i ne predstavlja povijesni događaj.",
    "uncertainty": "Izvorni tehnički uzorak; nema povijesnog, stručnog ili vlasničkog odobrenja.",
    "url": null
  }
}

```

## Original tool and limitations

```json
{
  "limitations": [
    "All supplied segments are original non-scripture technical fixtures, not historical biblical wording.",
    "No new bibliographic source was inspected or invented; source observations refer only to the supplied fixture.",
    "All contributions remain unreviewed AI-assisted drafts; no owner voice, human approval or expert participation is claimed."
  ],
  "tool": {
    "model_identifier": null,
    "name": "Codex-assisted original synthetic research/drafting; no human or scholarly review",
    "reported_at": "2026-10-30"
  }
}

```
