# One place to read, understand and follow the evidence

Date: 2026-11-19. Status: owner-stated product direction and eight recorded
experience preferences. This is a product brief and delivery plan, not a
claim that the proposed interface or content already exists.

Implementation status, 2026-11-20: the local synthetic reader now provides the
library/search entry, bilingual side-by-side reading, expandable evidence and
connections, and saved private notes/highlights/suggestions through the Python
bank writer. Start it with `npm run reading:demo -- --synthetic`. The real John 9
content and completion of the owner's full study journey remain outstanding; see
[the pilot's implementation/run notes](JOHN_9_READING_DESK_PILOT.md).

First trial feedback, 2026-11-20: the owner tentatively said it works but needs
more work, then selected **Writing notes and highlights** as the unfinished
part. The editor now stays beside the source, with explicit passage/selection
scope and same-tab draft recovery. Saved work is also searchable and linked back
to its source. These are implemented responses to that feedback, not a claim of
completed owner acceptance.

Continued implementation, 2026-11-20: saved highlight comments now open beside
the source by click/keyboard, confirmed items remain visible there, Ctrl+Enter
saves and a conflicting edit can be compared and explicitly kept as a separate
private item. Existing text, draft, source-binding and uncertain-save boundaries
remain intact. The reading guide describes the working controls.

Changed-view draft recovery is also implemented: original wording, quote and
recorded edition credits remain visible, including when its passage disappears
from the current view. The user can explicitly prepare a new unanchored passage
note or download the original browser draft. The original is retained until
deliberate discard; unknown requests are checked before any recovery copy.

The owner described the intended use:

> "i want it to be the place where i go to check out books and their context and evidences and connections to other storys charachters whatever"
>
> "just like a mideaval scribe had his bible and all the supporting literature for evidence for explanations related etc etc... all in one place and really nicely strucuted and clearity in mind."

The medieval-scribe comparison describes access to a main text and its supporting
literature at one desk. It does not decide a medieval visual style, a religious
interpretation, a product name or the authority of any source.

## Confirmed direction

The main product is a private reading and research desk. A person should be able
to open a book, understand its context, inspect explanations and evidence, and
follow useful connections to other stories, characters and supporting works.
The experience should feel like one coherent place, even where the underlying
catalogue, bank, historical extraction and editorial records remain separate.

Usability and clarity now drive the order of delivery. Storage, hashes, schemas
and processing machinery support this experience. More infrastructure by itself
is not the next user-facing milestone. Existing mechanics and review gates are
retained; an extract/candidate table is not the intended final reading experience.

The owner requested questions and answered the five initial questions and three
follow-ups. Their confirmed preferences are recorded below; further interaction
details remain design proposals, not invented owner answers. The selected pilot
is [John 9 and its supporting literature](JOHN_9_READING_DESK_PILOT.md).

## The experience to design

An initial reading journey should allow this sequence without manual ID copying
or searching several disconnected project screens:

```text
Find a book or subject
  → understand which work and edition is available
  → open a passage or a clear availability explanation
  → read its explanation/context
  → inspect the source behind an explanation or claim
  → follow a related story, character or theme and see why it is linked
  → return to the original passage with its location preserved
```

The owner selected equal library/search entry, side-by-side reading/explanation,
and a short clear explanation followed by expandable attributed views, evidence
and connections. Private notes, highlights and suggested connections belong in
the first usable version. The pilot specifies how that journey addresses John 9.

| Reading question | Information the desk should make understandable |
| --- | --- |
| What book am I looking at? | Work, edition, translator, available coverage and a readable introduction with attributed sources. |
| What does this passage say? | The exact selected text and reading location, with original source and later proposals kept distinct. |
| How can I understand it? | Clearly attributed explanations, historical/literary context and interpretations, with their evidentiary limits. |
| Where does that explanation come from? | The particular claim, supporting or contradicting source, edition, precise location and relevant context. |
| Who or what is mentioned? | Character/person/place/topic information with linked occurrences and an honest identity status. |
| What else should I read alongside it? | Supporting works or other passages with a short explanation of relevance and their availability. |
| Why are these stories connected? | A named relationship and its basis, such as a shared motif, explicit reference or an attributed comparison. |

These are content roles, not seven mandatory tabs. Use progressive disclosure
within the confirmed desktop side-by-side layout and preserve a clear return
path while following the John 9 reading example.

## Clarity at the point of reading

Proposed interaction principles:

- Use human labels such as Book, Passage, Explanation, Sources and Connections.
  Exact IDs, hashes and processing diagnostics belong in expandable details.
- Show which book/edition/passage is open and preserve a route back to it.
  Following a supporting source must not strand the reader in an unrelated list.
- Give each connection a readable reason and destination. A graph alone does
  not explain a relationship; lists or cards can be the first useful form.
- Keep a source's statement, a historical assertion, an interpretation and a
  personal note distinguishable. An interpretation is not promoted by placement.
- Show source authorship, translator, edition and exact locator when evidence
  opens. An unexplained URL or verification badge is insufficient context.
- Present availability honestly: locally readable, external reference, partial,
  unavailable or blocked. A catalogue entry is not a complete readable book.
- Use concise uncertainty/review labels close to the relevant statement. Preserve
  disagreement and contradictory evidence rather than hiding it for neatness.
- Empty states should explain what is missing and offer a valid next destination.
  Missing context is not permission to generate historical claims from memory.
- Retain keyboard navigation, visible focus, readable typography and narrow-screen
  behavior. Design primarily for desktop/laptop, as selected by the owner.

Begin with a short clear explanation, then attributed views and their evidence,
as selected by the owner. Evidence and connections expand on demand. Detailed
explanatory depth can be refined in use. No religious tradition or interpretation
is selected as authoritative by this product brief.

## Connections need meaning

The product should support exploring connections without treating every link as
the same kind of evidence. Proposed reader distinctions include:

| Connection | What the reader needs to know |
| --- | --- |
| Another occurrence | Where a label occurs; whether an identity relationship has actually been reviewed. |
| Related story or motif | What is similar, who proposed the comparison and which passages support it. |
| Commentary/explanation | Who offers the interpretation and what exact text it addresses. |
| Historical context | Which claim is being contextualized and the basis and uncertainty of its dating or historical assertion. |
| Supporting/contradicting evidence | Which statement the evidence addresses and whether it supports, challenges, contextualizes or merely mentions it. |

Similarity does not itself establish borrowing, influence, shared identity or
historical chronology. Equal surface names must not automatically merge people
or characters. These are presentation requirements for existing or future
reviewable records; this document creates no new typed relations or schemas.

## Owner answers recorded — 2026-11-19

These are actual product preferences supplied in the conversation. They are
not scripture wording, content-review attestations or rights approvals.

| Question | Confirmed choice |
| --- | --- |
| Starting point | Both equally: a library and one prominent search. |
| Reading layout | Text and explanation side by side, with evidence and connections expandable. |
| Disagreement | A short clear account, followed by attributed views and their evidence. |
| First reading scenario | John 9, the blind-man story described by the owner; meaning, religious blindness, related blindness stories, Jesus, Pharisees, symbolism and evidence including fragments. |
| First-version personal tools | Add private notes, highlights and suggested connections. |
| Main device | Mostly desktop or laptop, adapting to narrower screens. |
| Interface/explanation languages | Switchable English and Bosnian/Herzegovinian; exact source editions keep their own language. |
| Evidence focus | Both manuscript/textual witnesses and independent historical evidence, where available, presented separately. |

The owner's concrete scenario, preserved as supplied:

> "John 9 story of blind man. I would want the meaning of story explained (religous blidness etc.) connections to other blind people storys in bible, connections to Jesus as charachter of the story, connections to collected evidance of exact story even if fragments found. connections to chracthers of pharasees in the historical context. symbolims in and  around the story...."

Core discovery is complete. Do not ask these eight choices again or describe
them as pending. Visual tone, exact proportions and explanatory depth can be
refined through the first usable slice; no medieval visual style is inferred.
The bilingual preference does not change exact source text, existing literal
forms or original-name/editorial rules. A missing translation must be labelled,
not silently generated or substituted.

## Delivery plan

**U0 — recorded reading journey.** The eight answers above and the
[John 9 pilot](JOHN_9_READING_DESK_PILOT.md) now specify the first experience.
Documentation/discovery is complete for these choices; no interface, source or
stored-data changes have been implemented by this planning step.

**U1 — one coherent reading journey with private reading tools.** Extend the
existing small local application for the John 9-shaped journey: equal library/
search entry; desktop text/explanation side by side; concise explanation with
expandable attributed views, sources and connections; and return to the same
reading location. Provide switchable English/Bosnian-Herzegovinian UI and
explanations while preserving exact source languages. Support notes, highlights
and suggested connections in this first usable version, not a later optional phase.

Stage reading and private writing as reviewable internal increments. A read-only
increment does not complete U1. Define a small versioned reading-tools contract
using the existing Python writer boundary; do not silently widen v3 record enums,
overload evidence records with highlights or add an arbitrary Node filesystem
writer. Preserve exact anchors, cancel/conflict/recovery behavior and explicit
backup coverage. Personal notes are not scholarly approvals.

Use a tiny original explicitly synthetic fixture while source eligibility is
unresolved, reusing original Luma data if useful. Never paraphrase John 9 from
memory or invent historical commentary, parallels, fragments or witnesses to
populate a demo. A populated real John 9 desk has separate source/content
readiness requirements, described in the pilot.

Map existing record identities and source bindings to this journey explicitly.
Reuse Python validation and existing query code; do not silently join records
by title, label or guessed aliases. If a bounded synthetic excerpt contract is
needed, define and test it within this slice before exposing text. Keep generic
raw-file serving and real-source admission outside this UI task.

U1 acceptance checks:

- The owner completes the selected reading journey without a terminal, JSON
  editing, full-hash copying or switching between unrelated subsystem lists.
- Every displayed explanation has an inspectable source or an explicit
  unreviewed/unsupported state; each connection explains its relevance.
- Opening evidence preserves attribution, edition and exact location. Returning
  restores the original reading location and context.
- The reader can distinguish an occurrence, an interpretation, an identity
  proposal and historical evidence in the chosen example.
- Missing/private/stale material produces a clear bounded state rather than
  substituted text. The synthetic mode remains obvious and unreleasable.
- Both manuscript/textual witnesses and event-level historical evidence have
  distinct destinations, with background context and interpretation distinguishable.
  A fragment preserving text is not displayed as independent event corroboration.
- The owner adds, reopens and locates a private note, highlight and suggested
  connection without technical data entry; changes do not silently re-anchor them.
- Switching English/Bosnian-Herzegovinian preserves reading position, open
  context and personal work, and does not rewrite the selected source edition.
- Record the owner's observed navigation difficulties and ambiguous labels.
  Test counts alone do not complete the usability milestone.

**U2 — improve discovery across the available collection.** Once U1 works, connect
book/subject entry points, back-links and useful filters through the same reading
experience. Expand only what the initial journey demonstrates a need for; a full
graph, a new frontend framework or a large dashboard is not a prerequisite.

**U3 — later advanced editing/curation, only when needed.** Full explanation
editing, authoritative relationship curation or advanced graph tooling are not
part of the selected small pilot. U1 already includes private notes, highlights
and suggestions. Keep personal actions separate from any future human-review
and promotion workflow.

**Real content is a separate enabling track.** Resolve exact-edition rights,
source evidence and the admission contract before opening real material through
a new reading surface. Retain links and source metadata where content cannot
be shown. Usability prototypes can progress on original fixtures without relaxing
that track or pretending the books are already populated.

The former next CLI candidate/context inspection task is now supporting backlog.
Use it only if it directly helps U1; it is not the main product milestone.
The larger F0–F14 bank architecture plan remains a technical backlog, not an
instruction to finish every storage/indexing phase before improving reading.

## Preserved boundaries

This product direction changes experience priorities, not book admission, source
rights, editorial wording or review authority. Biblical scope stays exactly
GEN/MAT/MRK/LUK/JHN. The existing personal-library catalogue is a separate
supporting-research inventory. A reference or proposed connection does not add
a book to the biblical edition or clear its text for ingestion/display.

Keep svjet, vrjeme, covik and razumit literally; preserve translator credits and
edition identities; do not infer name mappings, transliterations, theology or
human approvals. Source, transcription, modernization proposals, explanations,
personal notes and evidence remain distinct. Reuse the local package/CLI and
existing viewer with no model APIs, paid/cloud dependencies or publication.

Related documentation: [current assessment](PROJECT_USEFULNESS_REPORT_2026-11-19.md),
[John 9 pilot](JOHN_9_READING_DESK_PILOT.md),
[bank implementation backlog](KNOWLEDGE_BANK_IMPLEMENTATION_PLAN.md),
[historical contract](HISTORICAL_TEXTS_PIPELINE.md) and
[continuation priorities](../NEXT_STEPS.md).
