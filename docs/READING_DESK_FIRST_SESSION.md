# Your first session at the reading desk

Allow about 10 minutes. You will read an example, follow its evidence and a
connection, then save a highlight, a note and a suggested connection.

The current desk uses **two invented practice stories**. They let you try the
reading tools. **John 9 is a planned research topic; its actual text,
explanations and historical evidence are not available in this collection yet.**

## 1. Start the desk

On this Windows computer:

1. Open the `Jasam-Biblija` project folder in File Explorer.
2. Double-click **start-reading-demo.cmd**. Leave its terminal window open.
3. When the window shows the local address, open
   **http://127.0.0.1:5187/#desk** in your browser.
4. Choose **English** in **Language / Jezik** at the top right if you want to
   follow the English button names below. You can switch back at any time.

The launcher reopens your existing practice workspace and saved notes. It does
not reset them or install anything. This checkout already has the Python setup;
a new computer also needs the [README setup](../README.md#start-on-windows-11--powershell)
and Node.js 22 or later.

If you prefer the terminal, open PowerShell in the project folder and run:

```powershell
npm run reading:demo -- --synthetic
```

You can also open **How to use this desk · 10 minutes** at the top of the desk
to keep these instructions beside your session.

## 2. Open the practice story

On the home screen, find **The ledger and the ribbon** and click **Open reading**.
In Bosnian the story is **Zapis i vrpca** and the button is **Otvori za čitanje**.
You can also type `Luma` into the prominent search field to find it.

The **Read** pane on the left holds the exact source text and its edition/creator
details. The **Understand** pane on the right holds the explanation. Scroll
inside either pane to read more. On a narrow screen the panes appear one below
the other.

## 3. Inspect the evidence

In the right pane, open **Sources & evidence**, then **Exact wording in this
fixture** under **Exact source wording**. Read the quoted words and click
**Locate in source**: the left pane brings the exact phrase into view.

Here the evidence only shows that the phrase occurs in the saved invented
story. The other groups distinguish manuscripts, independent evidence about an
event, historical background and interpretation. They are empty in this practice
example. An empty group describes this collection, not everything that might
exist elsewhere.

## 4. Follow a connection and return

In **Connections to follow**, read why the two stories are linked, then click
**A note in the reading room**. You are now reading the second story.

Click **Back to previous reading** near the top to return. The original pane
positions and expanded sections are preserved. This is how you will explore
supporting material without losing your place.

## 5. Save a highlight

In the left source pane, drag across the words **blue ribbon** to select them.
Click **Highlight selection** in the pane header. The editor opens under the
**Understand** heading, beside the source on desktop and above the explanation.
On a narrow screen, it appears below the source.

Check the quoted selection, optionally add a comment, then click **Save privately**.
Look for **Saved privately.** and your highlight under **My reading notes**.

The saved highlight also appears beside the source immediately after saving.
Click its highlighted words in the source to reopen the comment and use **Edit**
to change it. You can reach a highlight with **Tab**, then **Enter** or **Space**.
If highlights overlap, the shared words open all saved comments covering them.
Selecting text for copying or another highlight does not open those comments.

## 6. Save a private note

Click **Add note** to write about the whole passage. The editor opens beside the
source; type `My first reading note`, then **Save privately**. A highlight's
optional comment is the way to write about selected words.

Your note appears under **My reading notes** below the panes. The link with that
name beside the passage title takes you straight there. Use **Edit** on an item
to change it. **Cancel** discards the unsaved draft and leaves the saved item alone.

**Ctrl+Enter** saves from the editor. **Enter** by itself adds a new line. After
saving, your private item appears beside the source; **Close saved items** hides
that viewer without discarding an unfinished draft.

## 7. Suggest your own connection

Click **Suggest connection**. In **Connect to**, choose **A note in the reading
room**. Enter your reason, for example `I want to compare the ribbon in these
two scenes`, then click **Save privately**.

This is your private suggestion. It is kept apart from the supplied explanation
and connections.

## 8. Check that your work stays with you

Switch **Language / Jezik** to **Bosanski / hercegovački**. The controls and
explanation change language; the original English source and your own note
wording stay unchanged.

Refresh the browser. Your saved highlight, note and suggested connection should
still be present under **Moje bilješke uz čitanje**. Only changes confirmed with
**Saved privately. / Privatno spremljeno.** count as saved; save your work before
closing the page.

While writing, **Draft kept in this browser tab** means you can refresh that same
tab and recover the unfinished text. It is not a saved bank item or a backup.
If browser storage is unavailable, the editor says the draft is unsaved instead.
Save privately before closing the tab.

## Find your saved work again

Click **Library & search**. The main search now also finds words in your own notes
and highlighted quotes. Look under **My saved reading work** and use **Show saved
work** to filter notes, highlights or suggested connections. Recent changes appear
first; **Show more saved work** reveals additional results.

**Open saved item** opens its passage and focuses the saved note. **Locate in
source** goes straight to its exact quote. Notes attached to an earlier reading
view keep their original quote and are labelled; they are not silently moved to
the current source text.

## Next, look at John 9

Click **Library & search**, search `John 9` or `Ivan 9`, and open the planned
study. Its missing-text message is expected. You can save a private topic note
with a question you want to investigate; highlighting needs available source
text and is disabled here.

The lower **From your research library** section is a catalogue. Its references
help you find editions; a catalogue entry does not mean that book's text is
available to read in the desk.

## Stop and come back

Save your changes. In the launcher's terminal window, press **Ctrl+C** to stop
the desk; confirm termination if Windows asks. Next time, double-click the same
launcher and open the address again. Your confirmed private items are kept
locally in `dist/reading-desk-demo`.

If a save says it could not be confirmed, keep that browser tab open and use
**Check / retry this save**. It checks the same request without making duplicate
notes. Reopen the same launcher if you had stopped the server. For copying saved
work to another location, use the [backup instructions](JOHN_9_READING_DESK_PILOT.md#storage-writes-and-recovery).

If the same item was edited elsewhere, the editor shows **Latest saved version**
below your kept draft. **Cancel** discards this draft and keeps the saved version.
**Save my draft as a separate item** keeps both as different private items. It
does not overwrite the newer saved version. This choice is available only after
a confirmed conflict; an unconfirmed save must be checked/retried first.

## If the reading view changes while you have a draft

The desk opens **Recover your earlier draft**. Your original writing and exact
quote remain read-only, with the edition details captured when you began the
draft. Older drafts without captured edition details say so. The old quote is
never attached automatically to the current text.

1. If the original save is unconfirmed, use **Check / retry this save** first.
   A denied or busy retry alone cannot settle an earlier unknown save.
2. **Download original draft** keeps a private JSON snapshot containing the
   writing, quote, recorded credits and bindings. Keep the file if you want the
   original selection outside this browser tab. Full bank backup is separate.
3. Click **Prepare a new passage note**. Your writing is copied into a separate
   editor. Choose a current passage under **Save the new note with**, revise the
   wording if wanted, then **Save new passage note**. This saves a new note with
   no quote anchor; the old highlight or suggested connection is not moved.
4. If that prepared destination view also changes, use **Use the current view for
   this new note** deliberately, then check the destination again before saving.
5. A save that could not be confirmed stays locked for exact retry. Refreshing the
   same tab keeps that request when browser storage is available.
6. **Cancel new note** discards only the prepared, unsaved copy. After a confirmed
   recovery save, **Open saved item** lets you inspect the new note. The original
   stays here until you choose **Discard original draft**; discarding it never
   deletes a saved bank item. Discard is blocked while a prepared copy is unsaved
   or a save outcome is unknown.

If the original passage was removed from the reading view, the same recovery
panel appears on the home screen. You can still download the original or choose
another current passage for a new note. A restored draft in the same tab is not
a promise of recovery after closing that tab or clearing browser storage.

If the desk says the workspace is not connected or the buttons are disabled,
stop an earlier ordinary `npm run dev` session and use **start-reading-demo.cmd**.
If the launcher reports an invalid existing workspace, keep it intact and share
the error; do not delete the workspace to make the screen start.

After trying this session, tell me the first point that felt unclear: what you
clicked, what happened and what you expected. No need to evaluate everything.
