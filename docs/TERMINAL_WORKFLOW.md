# Everyday terminal workflow

After the one-time README setup, open the repository terminal and run:

```powershell
.\jeb.cmd
```

This opens a numbered menu. Enter a task number; `0` goes back or exits. Blank
input/EOF cancels rather than selecting a task. The Windows launcher uses this
repository's `.venv` without activation, execution-policy changes or global
installs. It also works when called by its full path from another folder.
If the environment is missing, it points to the three README setup commands and
installs nothing automatically.

For Linux or an installed Python environment, use `.venv/bin/python -m jeb work`
or `jeb work`. The terminal tasks are part of the same installable CLI.

## Shortcuts for the common tasks

| What you need | Windows repository terminal |
| --- | --- |
| Show status and what is blocking real work | `.\jeb.cmd status` |
| Explain source evidence gaps | `.\jeb.cmd sources` |
| Inspect one source's gaps | `.\jeb.cmd sources --source crosswire-srkdijekav` |
| Build the isolated, unreleasable example | `.\jeb.cmd demo` |
| List the example's saved review work | `.\jeb.cmd --demo queue` |
| Choose an example report without copying a hash | `.\jeb.cmd --demo review` |
| Choose saved real-project work, when available | `.\jeb.cmd review` |
| Run the four offline repository checks | `.\jeb.cmd check` |

The equivalent commands start with `jeb work`, for example
`jeb work --demo review`. The launcher is for these human tasks; existing
advanced `jeb sources`, `jeb review`, `jeb knowledge` and archive commands still
use their original arguments and JSON output.

## Reviewing something

1. Choose **List saved review work** or **Choose work and read an inspection
   report**. The list shows text proposals, annotation responses and narrative
   responses separately. It is an inspection list, not a count of pending or
   approved records. Passage research remains in its existing workflow.
2. Enter the item's number. Every competing response is listed; nothing is
   selected as “latest.” The short fingerprint distinguishes candidates but
   you never need to copy it. The exact full identity is held for the selection.
3. The existing report API checks the source, policy, packet and exact content
   again. Changed/stale/blocked work fails; the tool does not choose another
   candidate or relax a gate. Listing an item alone does not establish readiness.
4. The tool prints a report path under `reports/generated/work/`. Type `v` to
   read it in the terminal. Enter advances a page; `q` stops viewing. You can also
   open the printed Markdown path in your editor. Viewing is read-only; terminal
   control characters are shown as escapes.

Generated filenames are content-addressed and bounded in length. Identical
reports reuse the same file. Reports changed by later decisions get a different
name; an existing file with local edits is never overwritten. A temporary
derived report is removed after the final immutable write. Existing source,
drafts, approvals, canonical records and reader data are not edited by this task.

**This menu does not submit a review decision.** Text/annotation decisions still
need the existing explicit human-authored exact-hash workflow. Narrative review
is an unsigned inspection aid; no narrative apply/promotion endpoint exists.
No reviewer identity, answer, attestation or approval is generated here.

## Real project versus the example

The menu always labels its current workspace. **Build/use the isolated synthetic
demo** is an explicit opt-in and stays under `dist/demo`; it never adds fixture
records to production. **Return to the initial workspace** switches back.
`--demo` explicitly selects an already-built example for short commands; it does
not silently create one. A fresh demo includes the original synthetic text
proposal. Previously staged synthetic annotation/narrative examples also appear
when present; the launcher does not invent or import new AI responses.

At present no historical source is cleared. Real-project status therefore
reports a block and its review list is empty. **Sources** explains the missing
edition, digital lineage, component/rights and adapter evidence. No source is
fetched, approved or contacted by a terminal task. The five-book scope and
protected literal forms remain unchanged.

## One-command checks

`check` runs these exact commands, in order, using the current Python executable
and the repository root:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
```

Output is streamed so the terminal shows progress. Tests can take several
minutes. The first failed step stops the run with a nonzero exit; no success is
claimed after failure or timeout. Ruff comes from the hash-locked setup. The
task does not install missing dependencies or download text. Checks use the
repository even while the menu is viewing its demo. A recovered/demo-only
workspace without `src`/`tests` cannot run repository checks.

The menu/short commands print human-readable text. Existing JSON commands remain
available unchanged for automation. Saved-work scans are limited to 100 items;
larger stores use the explicit commands. Review files and pending caches remain
outside canonical-build archives. Code changes also require a new exact archive
engine; earlier matching wheels/snapshots are preserved as recorded in PROGRESS.
