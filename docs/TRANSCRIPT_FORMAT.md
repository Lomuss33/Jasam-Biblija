# JEB-TRANSCRIPT/1: deliberately limited TXT adapter

This project-defined grammar supports the original synthetic fixture and an
eventual independently cleared exact transcript. It is **not USFM, OSIS,
SWORD, an eBible TXT grammar, or an adapter for the current historical leads**.
Do not rename another source file to make it fit. Real source-format selection
requires a separate adapter evaluation with fidelity tests.

The file is strict UTF-8 without BOM. Its first physical line is exactly
`JEB-TRANSCRIPT/1` followed by LF. Each following physical line is exactly one
JSON object; no blank lines, comments or extra keys. LF is required, including
after the final record. Physical CR/CRLF is rejected so original byte locators
cannot silently change. Newlines and CR inside content are JSON escapes on a
single physical line. Duplicate keys, invalid encoding, unknown types,
unsupported markup and truncated input cause failure and quarantine diagnostics.

`src/jeb/schemas/transcript-record.json` is normative for field/type validation.
The adapter adds state, bounds, reference and relationship checks.

| Record | Required content | Effect |
| --- | --- | --- |
| book | `book_id`, `scheme` | Opens a unique, approved, locked book in collection order |
| block | `block_id`, `kind`, `level` | Declares a unique paragraph or poetry block |
| segment | reference labels and `parts` | Preserves one explicit mapped segment |
| end | no other fields | Ends the complete transcript; no trailing records |

Each segment carries string `chapter_label`, `verse_label`, unique string array
`verse_labels`, and `alternate_labels`. Its primary reference, mappings and
order must match the **reviewed exact-edition coverage manifest**. A bridge such
as `3-4` must have an explicit reviewed mapping; it is not split by the parser.
Suffix labels such as `2a` and alternate numbering are retained. Duplicate or
overlapping mappings are unsupported and rejected by this limited adapter.
There is no assumed universal verse count or automatic numeric-gap repair.

`parts` is an ordered array. A text part has `type: text`, an exact `text`
string, and a declared `block_id`. Text parts concatenate **without inserted
spaces** into main text. A segment can span blocks and a block can span
segments. Blocks are independent of verse milestones and cannot remain empty.

A note part has `type: note`, a unique `annotation_id`, a `kind` (heading,
footnote, cross_reference, introduction) and `content`. Content nodes are text
or italic/bold emphasis with nested children, to maximum depth 8. Unknown
character markers, milestones and other node kinds fail rather than disappear.
Notes remain typed annotations with their source ID, inline part index and
source span. A heading/note is never concatenated into verse text. Cross-reference
text can mention another book without importing that book's wording.

Each segment retains the complete original JSON line plus its source cache
path, physical line and exact half-open UTF-8 byte span (including final LF).
The raw file checksum binds these spans. Normalization changes decoded main
text only to NFC and LF, retaining exact before/after details. Original note
content is unchanged; a non-Latin source requiring display transliteration is
not supported for normalization/export by this adapter. Its bytes can still be
preserved and inspected locally. Latin-script enforcement does not transliterate.

The packaged `src/jeb/assets/synthetic.txt` is the executable grammar example.
It includes multiline strings, nested notes, a heading, cross-reference, poetry,
suffix numbering, a bridge, explicit mappings and decomposed Unicode. All its
sentences are invented technical examples. Reference-like labels test software;
they do not constitute real Genesis coverage.
