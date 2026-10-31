# Local build archives and isolated recovery

An archive preserves one admitted-source build snapshot. It is a bounded local
backup of canonical inputs, not a general workspace backup, source clearance,
human approval or public edition release. No historical source is currently
admitted, so only the explicitly opted-in original synthetic fixture is
demonstrated. The actual five annotation drafts remain unapproved.

## Create and inspect

```text
jeb --root <project> --synthetic archive create --source synthetic-v1 --archive-id fixture-build-01 --output dist/archives/fixture-build-01.zip
jeb --synthetic archive validate --input <archive.zip>
```

Omit `--synthetic` for a genuinely admitted historical source. Creation runs the
same admission, exact-source, normalization, review and reader gates as the build.
It does not acquire a source or change a registry status. An unclear, changed or
unsupported source fails. Current normalized artifacts must already match their
locked source; copied exports or indexes are not trusted.

The ZIP contains `manifest.json` and explicitly selected input files. Validation
returns that inspectable manifest plus ZIP/manifest hashes. Preserve the hashes
separately when recording a backup, and compare them on recovery. Internal
checksums detect accidental damage; they are not authenticated signatures or
proof of the human/source assertions inside an archive.

The manifest binds the exact installed Python package/schema engine, edition,
source, policy, raw/corpus identity, reader JSON/Markdown hashes and review counts.
It also lists every input's relative path, size and SHA-256. It contains no
changing build timestamp. Identical inputs produce the same manifest; ZIP member
timestamps/order are fixed. Cross-version compression bytes are not the corpus
determinism contract.

## Included scope

- The five fixed configuration files, editorial policy, source registry and lock.
- Exactly the selected source's locked transcript bytes and registered assessment
  documents, without acquiring linked external evidence.
- Imported modernization proposals and their exact input packets, including those
  referenced by superseded text decisions; all text-decision history.
- Legacy canonical knowledge JSONL, complete original knowledge-review receipts,
  parent revision approvals and all curation receipts.
- The rights policy, NOTICE and fixed MIT/CC0/license-matrix files when present.
  A historical archive requires its project rights policy. The original isolated
  fixture has no copied rights-policy document; its fictional rights declaration,
  credits and contribution notice remain explicit in the registry and manifest.

Only the current selected raw artifact is included. Historical packets/receipts
retain their supplied passage/policy/hash snapshots; older full artifacts and
private research evidence caches require their own eligible preservation.
Existing source credits, notices, jurisdictions and limitations remain unchanged.

Unreferenced working packets, source-research caches, AI critiques, unapproved
knowledge-proposal caches, arbitrary project files, `.git`, credentials,
environments, software/native binaries, exports and indexes are excluded. In
particular this is not a backup of the five pending annotation drafts' working
cache. Canonical review receipts retain their entire original annotation packet
and response, including attribution; canonical reader recovery does not need that
working cache. Resuming unfinished work may require separately preserving or
reconstructing the appropriate working files. No omitted file becomes approved.

One source's imported proposal set is supported per archive. Mixed-source
proposal histories or ambiguous/missing dependencies fail rather than silently
drop material. Active decisions are validated against the current build.
Superseded snapshots retain their own exact hash/coverage relationships without
being falsely re-approved against a later policy.

## Restore into a new workspace

```text
jeb --root <existing-parent> --synthetic archive restore --input <archive.zip> --destination recovered-build
```

Validation and restore do not require an existing project configuration or the
original workspace. Install the compatible package in the documented hash-locked
Python 3.13 environment first. `--root` is the existing recovery parent;
`--destination` is a new relative path below it. Input ZIP paths are relative to
the shell. Existing destinations, including empty directories, are refused.
No merge, replacement of existing files, code execution from the archive or
automatic migration is supported.

The tool reads bounded ZIP contents into memory, validates paths, allowlist,
sizes, manifest and checksums, then rebuilds in a private temporary workspace.
It reparses the locked raw bytes, normalizes, verifies proposal/approval/review/
curation relationships and reproduces the recorded reader identities. Restore
also rebuilds the search index. After complete success, it renames the staged
workspace into the new destination. A failure does not publish a partial target.
Parent directories may be created for staging. The local protocol assumes one
writer; do not run concurrent restores to the same destination.

The recovered canonical records, human decisions, provenance and curation
choices retain their original bytes and identities. No actual approval or owner
action is generated during restore. Withdrawn and inactive versions stay hidden;
there is no automatic fallback. Exact source coverage and partial-collection
statements are preserved, and a synthetic recovery remains unreleasable.

## Bounds and compatibility

Only the audited JEB-TRANSCRIPT/1 source adapter and this ZIP protocol are
supported. Limits are 32 MiB ZIP, 64 MiB expanded inputs, 255 input files plus
the manifest, and 128 KiB manifest. Existing document/receipt bounds also apply.
Directory members, links/devices, encrypted or unsupported ZIP formats,
traversal/drive/Windows-device paths, noncanonical spellings, duplicates and
filename-case collisions are refused. There is no `extractall`.

The archived engine identity covers package Python and schema bytes. A different
engine, even with the same development-version label, fails compatibility
validation. Retain the corresponding package/wheel and dependency lock separately;
the archive neither bundles nor installs software. A deliberate migration needs
its own reviewed workflow. Restored scopes are checked again by the installed
source and review gates, not unlocked by a date or checksum match.

ZIPs and recovered workspaces belong in ignored local storage. Do not push or
publish them without separate authorization and an actual scope/rights review.
For the actual fixture backup, inspect
[the recorded manifest](../reports/build-archive-manifest.json) and
[the local recovery results](../reports/build-archive-workflow.json).
