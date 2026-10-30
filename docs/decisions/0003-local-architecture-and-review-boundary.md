# 0003: Minimal local reproducible architecture

Date: 2026-10-30. Status: reversible engineering default.

Use Python 3.13.x, one package/CLI, strict JSON Schema and safe YAML, a standard
library test runner, and SQLite FTS5. Pin runtime/build/lint dependencies and
their PyPI artifact hashes. CI targets Windows/Linux with read-only permissions.
Schemas and the synthetic fixture ship inside the package so wheel installation
does not depend on an editable source tree.

The initial parser is the deliberately limited project transcript grammar, not
a pretend USFM/SWORD parser. Unknown formats and unsupported structures reject.
NFC/LF technical normalization is the only deterministic main-text rule; no B
rules, global linguistic replacements or transliteration mappings are approved.
All chats are manual subscription work. No API adapter or browser automation.

Initial packets support modernization only. Other task types and D-class expert
approval are explicitly deferred and blocked. These omissions are documented
instead of being represented as complete scholarly workflow. Per-book source
data, separate proposed/approved decisions, linked knowledge records and
deterministic reader exports form the first usable vertical slice.
