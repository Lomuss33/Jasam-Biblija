# License matrix

| Component | License / status | Scope and obligations |
| --- | --- | --- |
| Original Python, tests, build/CI configuration, software docs | MIT | Retain copyright and license notice |
| Original `toolchains/sword-1.9.0/synthetic_probe.cpp` source | MIT | Retain copyright and license notice; the linked binary has GPL obligations |
| SWORD source changes in `toolchains/sword-1.9.0/*.patch` | GPL-2.0-only, upstream derivatives | Preserve CrossWire notices and provide applicable license/source when redistributing |
| Optional compiled SWORD tools and statically linked probe | GPL-2.0, with upstream component notices | Local ignored build artifacts; redistribution requires corresponding source and applicable notices |
| Original eligible editorial policies, project metadata, synthetic fixture | CC0-1.0, to extent contributor holds rights | Dedication covers only our own eligible rights; preserve provenance |
| Historical text | None admitted | Future exact artifacts retain their own assessed rights, credits, notices and restrictions |
| External research / provider pages | Linked evidence, not relicensed | Independently written summaries; no corpus or bulk notes copied |
| Dependencies | Their upstream licenses | Do not relabel CC0; package metadata/notices remain authoritative |
| External fonts/images/media | None used | Any future assets need precise license checks |

Original software-associated documentation includes README, AGENTS,
CONTRIBUTING, architecture/format/data-model/review guides and continuity logs.
Editorial policies, the project charter, original decision records, original
configuration/provenance descriptions and original fixture sentences are
dedicated under CC0 where eligible. Where a file mixes components, each upstream
component retains its own rights; CC0 never removes those obligations. There is
no claim that the whole repository/corpus is globally public domain.

`CC0-1.0.txt` was retrieved from the
[official Creative Commons legal code](https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt).
`MIT.txt` uses the standard
[SPDX MIT text](https://spdx.org/licenses/MIT.txt), also published by the
[Open Source Initiative](https://opensource.org/license/mit), with copyright
fields filled for original JEB software contributors. Text line endings are LF.
Retrieved 2026-10-30. The first unauthenticated license fetch returned HTTP 403;
a normal browser User-Agent retrieval succeeded. No invented substitute is used.

`SWORD-GPL-2.0.txt` is the complete, unchanged `LICENSE` from the official
[SWORD 1.9.0 software archive](https://www.crosswire.org/ftpmirror/pub/sword/source/v1.9/sword-1.9.0.tar.gz).
It retains the CrossWire copyright introduction and the GNU GPL version 2 text.
The three derivative patches keep their upstream licensing; they are excluded
from the original-software MIT grant. The original Python wrapper uses native
tools as subprocesses. No SWORD library or executable is included in the Python
wheel. A statically linked probe executable is covered by the linked program's
GPL terms; its MIT source grant does not remove those terms. Internal zlib and
other upstream bundled components retain their original notices. See the
toolchain README and `LICENSES/provenance.json` for identities and boundaries.

Direct runtime dependencies: PyYAML (MIT) and jsonschema (MIT). Locked transitive
dependencies include attrs (MIT), jsonschema-specifications (MIT), referencing
(MIT), rpds-py (MIT). Development/build tools include ruff (MIT), setuptools
(MIT) and wheel (MIT). Their packages can contain bundled third-party components
with additional notices; inspect the installed `.dist-info/licenses` and wheel
contents when redistributing them. This project does not vendor those packages.
Python/SQLite and GitHub Actions retain their own licenses/terms.

AI-assisted output can lack protectable rights or carry unresolved third-party
issues; CC0 does not cure that. Contributors may dedicate only rights they
actually hold. Keep source and assistance disclosures and required upstream
attribution/share-alike obligations distinguishable. No contributor may waive
another contributor's rights.
