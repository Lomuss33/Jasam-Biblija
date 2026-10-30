# Synthetic SWORD toolchain evaluation

2026-10-30. Actual local native execution on Windows 11 / Python 3.13.3.
**Zero historical passages acquired, compared, parsed or approved.** This
evaluates one original technical fixture; the CrossWire candidate stays
`needs_review` and its adapter/fidelity checks stay unresolved.

## Software and reproducibility

The official [SWORD 1.9.0 release archive](https://www.crosswire.org/ftpmirror/pub/sword/source/v1.9/sword-1.9.0.tar.gz)
was retrieved as software, 2,606,652 bytes, SHA-256
`42409cf3de2faf1108523e2c5ac0745d21f9ed2a5c78ed878ee9dcc303426b8a`.
GCC/G++ 13.2.0 (MinGW x86_64 ucrt), CMake 4.0.2 and Ninja built a static,
offline profile with three recorded patches. The first manual build and a
fresh extraction/build through `jeb toolchain build` both succeeded. Native
`imp2vs`, the original entry probe, `mod2imp` and `mod2osis` all returned 0 in
both final experiments. The rebuild's probe stdout matched the earlier capture
exactly: SHA-256
`034dc398d555241f8b01ffc319ec0af2b21feb3a5130ad60390f8ce4d1e6da1d`.

The [toolchain README](../../toolchains/sword-1.9.0/README.md) gives the actual
build/evaluation commands, patch rationale, compiler identities and license
boundaries. Logs and software archives remain in ignored `dist/` directories.
Tracked records include both local executable locks, patch pre/post hashes,
the original probe, a portable captured fixture and the
[native evaluation report](../../reports/sword-toolchain-evaluation.json).
Native binary reproducibility across machines is not claimed. The offline
Python checks require no compiler or software download. No Linux native run or
remote CI success is claimed.

## Original input and measured structure

`src/jeb/assets/sword-synthetic.imp` contains eight original IMP entries with
invented technical sentences, never reconstructed historical wording. It
deliberately includes a book introduction, chapter introduction, nested
heading/note/italic/bold markup, two poetry lines, Latin diacritics, the literal
forms `svjet`, `vrjeme`, `covik`, `razumit`, a negation, a number, an internal
newline, a cross-reference, a two-label bridge and independent repeated wording.
It declares OSIS markup, zText/ZIP/BOOK storage and Calvin versification.
Its SHA-256 is
`b58fa820857a6ba89ec20cf4687b031c7ade30898ce6a49bdceb6c8dc1ae92f3`.

Ten keys are requested explicitly. Nine have entries, including two
introductions and the linked alias `Gen.1.4` for `Gen.1.3`. `Gen.1.6` is
explicitly empty. `Gen.1.7` has identical words to `Gen.1.3` but is an independent
stored entry. Treating equal words as proof of a link would corrupt this fixture.
Test references are labels only and never enter JEB corpus, search or reader
exports. Stock utilities enumerate unused book/verse slots as part of their
native dump; those empty records are not imported into the collection.

The original bounded C++ probe opens only the isolated `JEBSynthetic` library,
rejects additional modules, uses explicit requested keys and reports:

- Book/chapter introduction versus verse, entry presence and exact key.
- An engine-tested link target among previously requested present keys, with
  `link_scope=requested_keys_only`. It does not promise a whole-module link graph.
- Actual stored uncompressed bytes, read using zText's underlying accessors,
  separately from `getRawEntry()` output and both UTF-8 byte lengths.

The JSONL fields `raw_length_bytes` and `engine_osis` describe the engine's
`getRawEntry()` result. `stored_length_bytes` and `stored_osis` describe the
separate underlying stored text. The former is not an immutable-byte witness
despite the upstream method's name.

## Export/import changes actually observed

In this pinned build, `mod2imp` emits both bridge keys with repeated text, but
does not encode their link relationship. The third equal-text entry is also
present. This differs from the older provider documentation's warning about
skipping linked entries; do not report a missing test verse that this build
actually emitted. Preserve the measured build behavior and the documented
warning separately. Plain text/IMP wording cannot identify the link graph.

`mod2osis` omits the synthetic book and chapter introductions. Its header emits
`Bible.KJV` twice even though this module declares Calvin. It also prints an
explicit export/losslessness warning to stderr while returning success. Exit 0
does not establish completeness or correct reference identity. Notes, headings,
poetry and nested markup in the populated verses survive this fixture's stock
output, but that does not establish full OSIS fidelity.

SWORD's zText `getRawEntry()` invokes `prepText`: this fixture's internal LF
becomes a space and terminal whitespace is removed. All nine present slot
records differ between stored and engine text; the report retains both hashes.
The probe keeps the stored markup separately, so this change is inspectable.

The pinned `imp2vs` EOF loop adds one extra final LF to the last input record
(`Matt.5.1`). The validator records this exact importer delta against the
original fixture. It is neither silently erased nor adopted as a general corpus
normalization rule. Input bytes, stored module text and engine output are
three different evidence objects.

The provider's [module developer documentation](https://wiki.crosswire.org/DevTools:Modules)
warns against assuming a lossless round trip. The pinned archive's
`utilities/mod2osis.cpp`, `src/modules/texts/ztext/ztext.cpp`,
`src/modules/swmodule.cpp` and `utilities/imp2vs.cpp` explain the measured
export/header, preparation and EOF behavior. The official
[configuration documentation](https://wiki.crosswire.org/DevTools:conf_Files)
distinguishes storage, markup, display options and versification.

## Implemented checks and remaining work

`jeb toolchain evaluate` verifies executable hashes before execution, creates a
fresh isolated library from the package's fixed original fixture, runs fixed
commands without a shell, keeps stdout/stderr hashes and validates all requested
states. It writes no production source/approval records. `toolchain validate`
checks the portable captured JSONL offline. Its strict schema accepts only this
module and these ten slots; XML checks forbid DTD/entities and bound size,
nesting and node count. It is not a general OSIS parser or importer.

The thirteen new tests cover exact stored bytes and lengths, missing/reordered
slots, false/invented links, independent equal words, introduction/empty states,
nested markup/poetry, prohibited XML, changed executable hashes and an unchanged
production workspace. The successful native rebuild is separate validation of
the optional build path. Upstream compile warnings remain, and this experiment
is not a general audit of the native engine.

Historical import still requires the exact digital lineage, component rights,
per-country assessment, locked artifact and reviewed five-book coverage. Prefer
the provider's original OSIS plus its transformation history when available.
An actual historical adapter would additionally need original source spans,
whole-selected-book link/empty/bridge inventory, exact Calvin mappings, typed
annotations, unknown-marker failure behavior and source-faithful reconstruction
tests. The synthetic probe does not restore layout already absent upstream.
No source status or human approval was changed by this experiment.
