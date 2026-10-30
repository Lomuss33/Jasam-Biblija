# Optional SWORD 1.9.0 synthetic diagnostic

This is an experiment using original technical sentences, not a historical-text
adapter. Normal installation, tests, source inspection and the four-segment demo
need no native toolchain. Nothing here admits or fetches a scripture artifact.

The reviewed software archive is the official
[SWORD 1.9.0 release](https://www.crosswire.org/ftpmirror/pub/sword/source/v1.9/sword-1.9.0.tar.gz):
2,606,652 bytes, SHA-256
`42409cf3de2faf1108523e2c5ac0745d21f9ed2a5c78ed878ee9dcc303426b8a`.
Store it locally, for example at
`dist/toolchains/sword-1.9.0/sword-1.9.0.tar.gz`. The builder performs no downloads.
Its archive identity check runs before extraction or compilation. The official
software bundle includes upstream examples; none is used as a JEB corpus input.

## Build in this checkout

Requirements already installed: Python 3.13 with this package, GCC/G++ supporting
C++11, CMake, and Ninja on PATH. The verified local platform was Windows 11,
MinGW GCC/G++ 13.2.0, CMake 4.0.2. No Visual Studio, system install, permissive
compiler mode, ICU, curl, CLucene or network installation backend is used.
The build uses a static SWORD library and its bundled zlib. Existing build/output
directories are never replaced; choose a new output path when repeating a run.

```powershell
.\.venv\Scripts\python.exe -m jeb toolchain build --archive dist/toolchains/sword-1.9.0/sword-1.9.0.tar.gz --output dist/sword-tools-rebuild --compiler C:/Strawberry/c/bin/g++.exe --c-compiler C:/Strawberry/c/bin/gcc.exe
.\.venv\Scripts\python.exe -m jeb toolchain evaluate --lock dist/sword-tools-rebuild/toolchain.lock.json --tools dist/sword-tools-rebuild/build/utilities --output dist/sword-evaluation-rebuilt
```

Paths above record the actual Windows run. For another machine, provide its
compiler paths or omit those options to use `g++` and `gcc` from PATH. The same
CLI has Linux filename/link flags, but no Linux native build was run in this
session. The builder requires this checkout's `toolchains/sword-1.9.0` resources;
those sources are not bundled into the installed Python wheel.

The builder verifies all source preimages/postimages and the exact patch diffs:

- `rawstr4-win64.patch`: two pointer null checks without 32-bit integer casts.
- `pointer-key-win64.patch`: pointer-derived keys use `std::uintptr_t` in eleven
  filter files, retaining the existing lookup behavior.
- `offline-no-ftp.patch`: omit the legacy no-curl FTP source from this offline
  profile. Its 32-bit callbacks are unsuitable for this Win64 build; remote
  installation tools are neither built nor supported by this profile.

Seven Android symlinks in the software archive are recorded and omitted, never
materialized. Only the three stock utilities needed here and the original
`synthetic_probe.cpp` are built. Upstream regex/compiler warnings remain in the
logs; this is not a warning-free build or a general security audit of SWORD.
Full commands, stdout/stderr, omitted members and failures stay under the chosen
ignored `dist/` path. No `cmake --install` step runs.

`windows-local.lock.json` records the first manually configured local build.
`windows-rebuild.lock.json` records the subsequent successful CLI rebuild.
Both pin actual executable sizes/hashes. A fresh build writes its own lock;
executable bytes need not match across compiler versions, paths or platforms.
Use that build's reviewed lock, then compare the validated synthetic capture.
An editable lock is an identity record, not a signature or trust guarantee.

## Inspect without native execution

```powershell
.\.venv\Scripts\python.exe -m jeb toolchain validate --input tests/fixtures/sword/synthetic-probe.jsonl
```

The ten captured slots came from actual native execution of the original
`src/jeb/assets/sword-synthetic.imp`. `capture-provenance.json` records the raw
stdout identity and its JSON reserialization for portable LF Git storage.
The validator checks exact stored text against that package asset. It has no
arbitrary module/source option and cannot turn this result into a production
source approval. See the [findings](../../docs/sources/SWORD_TOOLCHAIN_EVALUATION.md).

## Licenses

The patch files are GPL-2.0-only derivatives of CrossWire SWORD code. Preserve
upstream notices; the complete upstream license is
[`LICENSES/SWORD-GPL-2.0.txt`](../../LICENSES/SWORD-GPL-2.0.txt). Its copyright
introduction remains intact. The unmodified upstream software is identified by
the official URL and hash above; each patch has a JSON before/after descriptor.
Bundled zlib and other upstream components keep their own notices.

The original Python builder/validator, C++ probe source and software docs are
MIT. A probe executable statically linked to SWORD is subject to the combined
program's GPL version 2 terms. Native binaries are local ignored artifacts;
redistributing them requires the applicable notices, license and corresponding
source, including the unmodified upstream source and these changes. They are
not included in the Python wheel. Original invented fixture sentences are CC0
where the contributor holds rights. No historical text receives any license
from this experiment.
