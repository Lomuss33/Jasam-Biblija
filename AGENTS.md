# Repository working instructions

Read `PROGRESS.md`, `NEXT_STEPS.md` and `git status` before continuing. Preserve
uncommitted work and existing editorial decisions. Do not reinitialize Git,
change remotes, rewrite history, publish, push or create releases without explicit
authorization. Reversible local work is authorized by the project prompt.

Scope is exactly GEN, MAT, MRK, LUK, JHN. Adding a book needs a new explicit
owner decision with date and text, then a separately reviewed schema/code change.
Do not interpret a cross-reference or archive member as approval to add a book.

No real source is currently cleared. Never relax rights or review gates to make
a demo pass. The synthetic workspace must stay opt-in, isolated, labelled and
unreleasable. Historical source bytes may not be filled from model memory.
Preserve translator credits and exact editions. A provider label is evidence,
not universal legal clearance. See `docs/RIGHTS_POLICY.md`.

Preserve svjet, vrjeme, covik, razumit literally. No inferred inflection rules,
automatic transliteration, saint prefixes, invented native names, unreviewed
original-name mappings or theological substitution. Latin-authored displays
only; unchanged upstream script can remain private evidence.

Keep source, transcription, modernization proposals, human approvals and
knowledge layers distinct. An AI is never a human reviewer. Never generate a
real owner approval. Synthetic test attestations are isolated test data only.

Python 3.13.x, one installable package/CLI, no model APIs, chat scraping, paid
services or cloud dependencies. Versioned schemas ship under `src/jeb/schemas`.
Use the hash-locked environment documented in README. Offline checks:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
```

Tests run offline without historical text. Keep commands and actual results in
`PROGRESS.md`. State remaining limitations honestly and identify the next small
task in `NEXT_STEPS.md`. Do not restart policy work or build a large frontend.
