// Optional real-browser integration test, using only Node built-ins and local CDP.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawn, execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { existsSync } from 'node:fs';
import { mkdtemp, readFile, realpath, rm, mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import os from 'node:os';
import { randomUUID } from 'node:crypto';
import { createServer } from './server.mjs';
import { browserDraftExport } from './reading-state.mjs';

const repo = fileURLToPath(new URL('../', import.meta.url));
const python = process.env.JEB_TEST_PYTHON || path.join(repo, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
const browser = [process.env.JEB_BROWSER_PATH, 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', 'C:/Program Files/Google/Chrome/Application/chrome.exe', '/usr/bin/chromium', '/usr/bin/google-chrome'].find(file => file && existsSync(file));
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));

test('real reading journey saves all item types, preserves language/source/location, cancels and reopens', { skip: !browser && 'No local Chromium browser installed', timeout: 120000 }, async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'jsb-reading-browser-'));
  const bank = path.join(directory, 'bank');
  const profile = path.join(directory, 'profile');
  let server, child, socket;
  try {
    await promisify(execFile)(python, ['-B', '-m', 'jeb', '--synthetic', 'reading', 'demo', '--bank-root', bank], { cwd: repo, windowsHide: true });
    server = createServer({ readingRoot: bank, readingSynthetic: true, readingWritable: true, readingPython: python });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    child = spawn(browser, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-background-networking', '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=0', `--user-data-dir=${profile}`, 'about:blank'], { windowsHide: true, stdio: 'ignore' });
    let port;
    const started = Date.now();
    while (!port && Date.now() - started < 15000) {
      try { port = Number((await readFile(path.join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]); } catch { await pause(100); }
    }
    assert.ok(port, 'Browser did not expose local CDP');
    const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    const target = targets.find(item => item.type === 'page'); assert.ok(target);
    socket = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => { socket.addEventListener('open', resolve, { once: true }); socket.addEventListener('error', reject, { once: true }); });
    let id = 0;
    const pending = new Map();
    const browserErrors = [];
    socket.addEventListener('message', event => {
      const message = JSON.parse(String(event.data));
      if (message.method === 'Runtime.exceptionThrown') browserErrors.push(message.params.exceptionDetails.text);
      const request = pending.get(message.id);
      if (request) { pending.delete(message.id); clearTimeout(request.timer); message.error ? request.reject(new Error(message.error.message)) : request.resolve(message.result); }
    });
    const cdp = (method, params = {}) => new Promise((resolve, reject) => {
      const number = ++id;
      pending.set(number, { resolve, reject, timer: setTimeout(() => { pending.delete(number); reject(new Error(`CDP timeout: ${method}`)); }, 15000) });
      socket.send(JSON.stringify({ id: number, method, params }));
    });
    const evaluate = async expression => {
      const result = await cdp('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
      if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
      return result.result.value;
    };
    const until = async expression => {
      const start = Date.now();
      while (Date.now() - start < 18000) { if (await evaluate(expression)) return; await pause(100); }
      throw new Error(`Page did not reach: ${expression}\n${await evaluate('document.body.innerText')}`);
    };
    await cdp('Runtime.enable');
    await cdp('Emulation.setDeviceMetricsOverride', { width: 1360, height: 650, deviceScaleFactor: 1, mobile: false });
    await cdp('Page.navigate', { url: `${base}/#desk` });
    await until('Boolean(document.querySelector("#desk-search"))');
    await evaluate('document.querySelector("#desk-language").value="en"; document.querySelector("#desk-language").dispatchEvent(new Event("change"))');
    assert.equal(await evaluate('document.documentElement.lang'), 'en');
    assert.equal(await evaluate('document.querySelector("#reading-guide").hidden'), true);
    await evaluate('document.querySelector("#reading-guide-toggle").click()');
    assert.equal(await evaluate('document.querySelector("#reading-guide-toggle").getAttribute("aria-expanded")'), 'true');
    assert.equal(await evaluate('document.querySelector("#reading-guide-title").textContent'), 'Your first reading session');
    assert.equal(await evaluate('document.activeElement.id'), 'reading-guide-toggle');
    await evaluate('document.querySelector("#desk-language").value="bs"; document.querySelector("#desk-language").dispatchEvent(new Event("change"))');
    assert.equal(await evaluate('document.querySelector("#reading-guide-title").textContent'), 'Tvoje prvo čitanje');
    assert.equal(await evaluate('document.querySelector("#reading-guide").hidden'), false);
    await evaluate('document.querySelector("#desk-language").value="en"; document.querySelector("#desk-language").dispatchEvent(new Event("change")); document.querySelector("#reading-guide-practice").click()');
    await until('document.querySelector(".desk-reading-heading h1")?.textContent === "The ledger and the ribbon"');
    assert.equal(await evaluate('document.querySelector("#reading-guide").hidden'), true);
    assert.equal((await (await fetch(`${base}/api/reading/view`)).json()).items.length, 0, 'The guide and practice link must not create private items');
    await evaluate('document.querySelector(".desk-bar button").click()');
    await until('Boolean(document.querySelector("#desk-search"))');
    await evaluate('document.querySelector("#desk-search").value="ledger"; document.querySelector("#desk-search").dispatchEvent(new Event("input")); document.querySelector("[data-open-passage=ledger-entry]").click()');
    await until('Boolean(document.querySelector("#reading-source-text"))');
    const source = await evaluate('document.querySelector("#reading-source-text").textContent');
    await evaluate(`(() => { const element=document.querySelector('#reading-source-text');const text=element.firstChild.firstChild;const start=text.textContent.indexOf('blue ribbon');const range=document.createRange();range.setStart(text,start);range.setEnd(text,start+11);const selection=getSelection();selection.removeAllRanges();selection.addRange(range);document.querySelector('[data-reading-action=highlight]').click(); })()`);
    await until('Boolean(document.querySelector("#reading-save"))');
    assert.equal(await evaluate('Boolean(document.querySelector(".desk-context-scroll #reading-editor"))'), true, 'Write beside the source instead of below the reading panes');
    assert.equal(await evaluate('document.querySelector("label[for=reading-note]").textContent'), 'Comment (optional)');
    await evaluate('document.querySelector("#reading-save").click()');
    await until('document.querySelectorAll(".desk-personal-item").length===1 && !document.querySelector("#reading-editor")');
    assert.equal(await evaluate('document.querySelector("#reading-items blockquote").textContent'), 'blue ribbon');
    assert.ok((await evaluate('document.querySelector("#reading-inspector").textContent')).includes('No comment added.'));
    await evaluate('document.querySelector("#reading-inspector-close").click(); getSelection().removeAllRanges(); document.querySelector("[data-saved-highlight]").click()');
    await until('Boolean(document.querySelector("#reading-inspector"))');
    await evaluate('document.querySelector("[data-edit-inspected]").click(); document.querySelector("#reading-note").value="My private ribbon comment"; document.querySelector("#reading-note").dispatchEvent(new Event("input")); document.querySelector("#reading-note").dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}))');
    assert.equal(await evaluate('Boolean(document.querySelector("#reading-editor"))'), true, 'Enter alone must not save a multiline comment');
    await evaluate('document.querySelector("#reading-note").dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",ctrlKey:true,bubbles:true}))');
    await until('!document.querySelector("#reading-editor") && document.querySelector("#reading-inspector").textContent.includes("My private ribbon comment")');
    await evaluate('(() => {document.querySelector("#reading-inspector-close").click(); const mark=document.querySelector("[data-saved-highlight]"); const range=document.createRange();range.selectNodeContents(mark);getSelection().removeAllRanges();getSelection().addRange(range);mark.click();})()');
    assert.equal(await evaluate('Boolean(document.querySelector("#reading-inspector"))'), false, 'Selecting highlighted words must not open their saved comment');
    await evaluate('(() => {const range=document.createRange();range.selectNodeContents(document.querySelector(".desk-source-scroll"));getSelection().removeAllRanges();getSelection().addRange(range);document.querySelector("[data-saved-highlight]").click();})()');
    assert.equal(await evaluate('Boolean(document.querySelector("#reading-inspector"))'), false, 'A selection spanning source credits and text must not open a saved comment');
    await evaluate('(() => {getSelection().removeAllRanges(); const mark=document.querySelector("[data-saved-highlight]"); mark.focus();mark.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}));})()');
    await until('Boolean(document.querySelector("#reading-inspector"))');
    assert.equal(await evaluate('document.querySelector("#reading-source-text").textContent'), source);
    const note = '<script>window.privateNoteExecuted=true</script> svjet vrjeme covik razumit';
    await evaluate(`document.querySelector('[data-reading-action=note]').click();document.querySelector('#reading-note').value=${JSON.stringify(note)};document.querySelector('#reading-note').dispatchEvent(new Event('input'));document.querySelector('#reading-save').click()`);
    await until('document.querySelectorAll(".desk-personal-item").length===2 && !document.querySelector("#reading-editor")');
    assert.equal(await evaluate('Boolean(window.privateNoteExecuted)'), false);
    await evaluate('document.querySelector("details[data-panel=evidence]").open=true;document.querySelector(".desk-evidence-card").open=true;document.querySelector(".desk-evidence-card button").click()');
    await until('document.querySelector("[data-proof=true]")?.textContent === "blue ribbon"');
    await evaluate(`document.querySelector('[data-reading-action=connection]').click();document.querySelector('#reading-note').value='My private ribbon connection';document.querySelector('#reading-note').dispatchEvent(new Event('input'));document.querySelector('#reading-save').click()`);
    await until('document.querySelectorAll(".desk-personal-item").length===3 && !document.querySelector("#reading-editor")');
    const savedItems = (await (await fetch(`${base}/api/reading/view`)).json()).items;
    const noteId = savedItems.find(item => item.kind === 'note').id;
    const highlightId = savedItems.find(item => item.kind === 'highlight').id;
    assert.ok((await evaluate('document.querySelector("#reading-notes-jump").textContent')).includes('(3)'));
    await evaluate('document.querySelector("#reading-notes-jump").click()');
    assert.equal(await evaluate('document.activeElement.id'), 'reading-personal');
    await evaluate(`document.querySelector('[data-locate-item="${highlightId}"]').click()`);
    await until('document.querySelector("[data-proof=true]")?.textContent === "blue ribbon"');
    await evaluate('document.querySelector(".desk-bar button").click(); document.querySelector("#desk-search").value="privateNoteExecuted"; document.querySelector("#desk-search").dispatchEvent(new Event("input"))');
    assert.equal(await evaluate('document.querySelectorAll(".desk-saved-card").length'), 1);
    assert.ok((await evaluate('document.querySelector(".desk-saved-card").textContent')).includes(note));
    assert.equal(await evaluate('Boolean(window.privateNoteExecuted)'), false);
    await evaluate(`document.querySelector('[data-jump-item="${noteId}"]').click()`);
    await until(`document.activeElement.dataset.itemId === '${noteId}'`);
    await evaluate('document.querySelector(".desk-bar button").click(); document.querySelector("#desk-search").value="ribbon"; document.querySelector("#desk-search").dispatchEvent(new Event("input")); document.querySelector("#saved-kind").value="highlight"; document.querySelector("#saved-kind").dispatchEvent(new Event("change"))');
    assert.equal(await evaluate('document.querySelectorAll(".desk-saved-card").length'), 1);
    assert.equal(await evaluate('document.querySelector(".desk-saved-card blockquote").textContent'), 'blue ribbon');
    await evaluate(`document.querySelector('[data-locate-item="${highlightId}"]').click()`);
    await until('document.querySelector("[data-proof=true]")?.textContent === "blue ribbon"');
    assert.equal((await (await fetch(`${base}/api/reading/view`)).json()).items.length, 3, 'Search and source navigation must not save anything');
    await evaluate('document.querySelector("#desk-language").value="bs";document.querySelector("#desk-language").dispatchEvent(new Event("change"))');
    assert.equal(await evaluate('document.querySelector("#reading-source-text").textContent'), source);
    assert.equal(await evaluate('document.querySelector(".desk-pane-title").textContent'), 'Čitaj');
    assert.ok((await evaluate('document.querySelector("#reading-items").textContent')).includes(note));
    const savesBeforeDraft = (await (await fetch(`${base}/api/reading/view`)).json()).remaining_saves;
    await evaluate(`(() => { const text=document.querySelector('#reading-source-text').firstChild.firstChild;const range=document.createRange();range.setStart(text,0);range.setEnd(text,9);getSelection().removeAllRanges();getSelection().addRange(range);document.querySelector('[data-reading-action=note]').click(); })()`);
    assert.equal(await evaluate('Boolean(document.querySelector("#reading-editor blockquote"))'), false, 'Add note is passage-level even when source words happen to be selected');
    assert.equal(await evaluate('document.querySelector("#reading-save").disabled'), true, 'An empty passage note cannot be submitted');
    await evaluate(`document.querySelector('#reading-note').value='Unsubmitted draft';document.querySelector('#reading-note').dispatchEvent(new Event('input'));document.querySelector('#desk-language').value='en';document.querySelector('#desk-language').dispatchEvent(new Event('change'))`);
    assert.equal(await evaluate('document.querySelector("#reading-note").value'), 'Unsubmitted draft');
    await evaluate('getSelection().removeAllRanges(); document.querySelector("[data-saved-highlight]").click()');
    assert.equal(await evaluate('document.querySelector("#reading-note").value'), 'Unsubmitted draft', 'Reading a saved comment must preserve the open draft');
    await evaluate('document.querySelector("#reading-inspector-close").click()');
    assert.equal(await evaluate('document.querySelector("#reading-note").value'), 'Unsubmitted draft');
    await evaluate('document.querySelector("#reading-guide-toggle").click()');
    assert.equal(await evaluate('document.querySelector("#reading-note").value'), 'Unsubmitted draft', 'Opening help must retain the unsaved draft');
    await evaluate('document.querySelector("#reading-guide-toggle").click()');
    assert.equal(await evaluate('document.querySelector("#reading-note").value'), 'Unsubmitted draft', 'Closing help must retain the unsaved draft');
    await evaluate(`sessionStorage.setItem('jeb.reading.pending', JSON.stringify({view_ref:{record_id:crypto.randomUUID()}, kind:'note', text:'Foreign workspace request', uncertain:true}))`);
    await cdp('Page.reload');
    await until('document.querySelector("#reading-note")?.value === "Unsubmitted draft"');
    assert.ok((await evaluate('document.querySelector("#reading-status").textContent')).includes('restored'));
    assert.ok((await evaluate('document.querySelector("#reading-draft-status").textContent')).includes('this browser tab'));
    assert.equal((await (await fetch(`${base}/api/reading/view`)).json()).remaining_saves, savesBeforeDraft, 'Typing and refreshing a browser draft must not consume bank history');
    assert.ok((await evaluate('sessionStorage.getItem("jeb.reading.pending")')).includes('Foreign workspace request'), 'Restoring this draft must preserve another workspace request');
    await evaluate('document.querySelector("#reading-cancel").click()');
    assert.equal((await (await fetch(`${base}/api/reading/view`)).json()).items.length, 3);
    await cdp('Page.reload');
    await until('Boolean(document.querySelector("#reading-source-text"))');
    assert.equal(await evaluate('Boolean(document.querySelector("#reading-editor"))'), false, 'Cancel must remove the recoverable draft');
    await evaluate(`(() => {const text=document.querySelector('#reading-source-text').firstChild.firstChild;const range=document.createRange();range.setStart(text,0);range.setEnd(text,9);getSelection().removeAllRanges();getSelection().addRange(range);const card=[...document.querySelectorAll('.desk-personal-item')].find(c=>c.querySelector('.desk-kicker').textContent==='Private note');card.querySelector('button').click();})()`);
    assert.equal(await evaluate('Boolean(document.querySelector("#reading-editor blockquote"))'), false, 'Editing a book-level note must not pick up a fresh selection');
    await evaluate(`document.querySelector('#reading-note').value+=' revised';document.querySelector('#reading-note').dispatchEvent(new Event('input'));document.querySelector('#reading-save').click()`);
    await until('!document.querySelector("#reading-editor") && document.querySelector("#reading-items").textContent.includes(" revised")');
    const beforeLostReply = (await (await fetch(`${base}/api/reading/view`)).json()).remaining_saves;
    await evaluate(`(() => {const card=[...document.querySelectorAll('.desk-personal-item')].find(c=>c.querySelector('.desk-kicker').textContent==='Private note');card.querySelector('button').click();document.querySelector('#reading-note').value+=' after retry';document.querySelector('#reading-note').dispatchEvent(new Event('input'));const nativeFetch=window.fetch;window.fetch=async (...args)=>{const response=await nativeFetch(...args);if(String(args[0]).endsWith('/api/reading/items'))throw new TypeError('Simulated lost committed response');return response;};document.querySelector('#reading-save').click();})()`);
    await until('document.querySelector("#reading-cancel")?.disabled && document.querySelector("#reading-save")?.textContent === "Check / retry this save"');
    const committedAfterLoss = await (await fetch(`${base}/api/reading/view`)).json();
    assert.equal(committedAfterLoss.remaining_saves, beforeLostReply - 1);
    await evaluate(`(() => {const key=Object.keys(sessionStorage).find(k=>k.startsWith('jeb.reading.pending.'));sessionStorage.setItem('jeb.reading.pending',sessionStorage.getItem(key));sessionStorage.removeItem(key);})()`);
    await cdp('Page.reload');
    await until('document.querySelector("#reading-save")?.textContent === "Check / retry this save"');
    assert.equal(await evaluate('document.querySelector("#reading-note").disabled'), true, 'An uncertain restored save cannot be edited before checking it');
    assert.equal(await evaluate('sessionStorage.getItem("jeb.reading.pending")'), null, 'A matching legacy request is migrated for exact retry');
    await evaluate('document.querySelector("#reading-save").click()');
    await until('!document.querySelector("#reading-editor") && document.querySelector("#reading-items").textContent.includes(" after retry")');
    const afterRetry = await (await fetch(`${base}/api/reading/view`)).json();
    assert.equal(afterRetry.remaining_saves, committedAfterLoss.remaining_saves, 'Checking an uncertain save must not add a revision');
    assert.equal(afterRetry.items.find(item => item.id === noteId).revision_id, committedAfterLoss.items.find(item => item.id === noteId).revision_id);
    await evaluate('document.querySelector("details[data-panel=evidence]").open=true;document.querySelector(".desk-source-scroll").scrollTop=55');
    const scroll = await evaluate('document.querySelector(".desk-source-scroll").scrollTop');
    await evaluate('document.querySelector(".desk-connection button").click()');
    await until('document.querySelector(".desk-reading-heading h1")?.textContent === "A note in the reading room"');
    await evaluate('[...document.querySelectorAll(".desk-bar button")].find(b=>b.textContent==="Back to previous reading").click()');
    await until('document.querySelector(".desk-reading-heading h1")?.textContent === "The ledger and the ribbon"');
    await pause(50);
    assert.equal(await evaluate('document.querySelector(".desk-source-scroll").scrollTop'), scroll);
    assert.equal(await evaluate('document.querySelector("details[data-panel=evidence]").open'), true);
    await evaluate(`document.querySelector('[data-item-id="${noteId}"] button').click(); document.querySelector('#reading-note').value='My conflict draft'; document.querySelector('#reading-note').dispatchEvent(new Event('input'))`);
    const concurrentSession = await (await fetch(`${base}/api/reading/session`)).json();
    const currentNote = concurrentSession.items.find(item => item.id === noteId);
    const externalEdit = await fetch(`${base}/api/reading/items`, { method: 'POST', headers: { Origin: base, 'Content-Type': 'application/json', 'X-Reading-Token': concurrentSession.write_token }, body: JSON.stringify({ view_ref: concurrentSession.view_ref, request_id: randomUUID(), kind: 'note', passage_id: currentNote.passage_id, text: 'Latest saved wording from another edit', anchor: currentNote.anchor, target_id: null, edit_record_id: noteId, expected_revision: currentNote.revision_id }) });
    assert.equal(externalEdit.status, 200); await externalEdit.json();
    await evaluate('document.querySelector("#reading-save").click()');
    await until('document.querySelector("#reading-conflict")?.textContent.includes("Latest saved wording from another edit")');
    assert.equal(await evaluate('document.querySelector("#reading-note").value'), 'My conflict draft');
    assert.equal(await evaluate('document.querySelector("#reading-save").disabled'), true);
    await evaluate('document.querySelector("#reading-note").value=""; document.querySelector("#reading-note").dispatchEvent(new Event("input"))');
    assert.equal(await evaluate('document.querySelector("#reading-save-separate").disabled'), true);
    await evaluate('document.querySelector("#reading-note").value="My conflict draft"; document.querySelector("#reading-note").dispatchEvent(new Event("input"))');
    await cdp('Page.reload');
    await until('document.querySelector("#reading-conflict")?.textContent.includes("Latest saved wording from another edit")');
    assert.equal(await evaluate('document.querySelector("#reading-note").value'), 'My conflict draft', 'Conflict recovery must survive refreshing the tab');
    await evaluate('document.querySelector("#reading-save-separate").click()');
    await until('!document.querySelector("#reading-editor") && document.querySelectorAll(".desk-personal-item").length === 4');
    const afterConflict = await (await fetch(`${base}/api/reading/view`)).json();
    assert.equal(afterConflict.items.find(item => item.id === noteId).text, 'Latest saved wording from another edit');
    const rescued = afterConflict.items.find(item => item.text === 'My conflict draft');
    assert.ok(rescued && rescued.id !== noteId);
    assert.equal(rescued.anchor, null);
    assert.equal(rescued.view_ref.revision_id, concurrentSession.view_ref.revision_id);
    await cdp('Page.reload');
    await until('document.querySelectorAll(".desk-personal-item").length===4');
    assert.equal(await evaluate('document.querySelector("#reading-source-text").textContent'), source);
    await mkdir(path.join(repo, 'reports/generated'), { recursive: true });
    const desktop = await cdp('Page.captureScreenshot', { format: 'png' });
    await writeFile(path.join(repo, 'reports/generated/reading-desk-desktop.png'), Buffer.from(desktop.data, 'base64'));
    await cdp('Emulation.setDeviceMetricsOverride', { width: 460, height: 850, deviceScaleFactor: 1, mobile: false });
    assert.ok(await evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Reading view overflows narrow viewport');
    await evaluate('document.querySelector("#reading-guide-toggle").click()');
    assert.ok(await evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Open guide overflows narrow viewport');
    await evaluate('document.querySelector("#reading-guide-toggle").click(); document.querySelector(".desk-bar button").click()');
    assert.ok(await evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Saved-work search overflows narrow viewport');
    await cdp('Emulation.setDeviceMetricsOverride', { width: 1360, height: 650, deviceScaleFactor: 1, mobile: false });
    await cdp('Page.navigate', { url: `${base}/#desk?passage=ledger-entry` });
    await until('Boolean(document.querySelector("#reading-source-text"))');
    const reviseView = async mode => promisify(execFile)(python, ['-B', '-c', `
import sys
from pathlib import Path
from jeb import reading
from jeb.bank import storage
from jeb.core import canonical
root = Path(sys.argv[1])
data = reading.load(root, synthetic=True)
value = data['view']
if sys.argv[2] == 'remove':
    value['passages'] = [p for p in value['passages'] if p['id'] != 'ledger-entry']
    for p in value['passages']:
        p['connections'] = [c for c in p['connections'] if c['target_id'] != 'ledger-entry']
        p['evidence'] = [e for e in p['evidence'] if e['passage_id'] != 'ledger-entry']
else:
    value['passages'][0]['explanation']['en'] += ' Synthetic view revision for recovery verification.'
identity = data['view_ref']['record_id']
prior = data['state']['records'][identity]
content = {key: prior[key] for key in ('kind', 'title', 'visibility', 'processing_state', 'data')}
storage.save_record(root, content, 'test-tool', 'tool', 'Synthetic reading-view revision', canonical(value).decode(), identity, prior['revision_id'])
`, bank, mode], { cwd: repo, windowsHide: true });
    const originalThought = 'Keep this earlier highlight thought: svjet vrjeme covik razumit';
    await evaluate(`(() => {const mark=document.querySelector('[data-saved-highlight]');const range=document.createRange();range.selectNodeContents(mark);getSelection().removeAllRanges();getSelection().addRange(range);document.querySelector('[data-reading-action=highlight]').click();document.querySelector('#reading-note').value=${JSON.stringify(originalThought)};document.querySelector('#reading-note').dispatchEvent(new Event('input'));const nativeFetch=window.fetch;window.fetch=async(...args)=>{if(String(args[0]).endsWith('/api/reading/items'))throw new TypeError('Synthetic unsent request');return nativeFetch(...args);};document.querySelector('#reading-save').click();})()`);
    await until('document.querySelector("#reading-save")?.textContent === "Check / retry this save"');
    await reviseView('change');
    await cdp('Page.reload');
    await until('Boolean(document.querySelector("#reading-recovery"))');
    assert.equal(await evaluate('document.querySelector("#reading-original-quote").textContent'), 'blue ribbon');
    assert.equal(await evaluate('document.querySelector("#reading-original-text").value'), originalThought);
    assert.equal(await evaluate('document.querySelector("#reading-recovery-prepare").disabled'), true, 'An original unconfirmed save must be checked before copying');
    await evaluate('document.querySelector("#reading-original-retry").click()');
    await until('document.querySelector("#reading-recovery-prepare")?.disabled === false');
    assert.equal(await evaluate('document.querySelectorAll("[data-saved-highlight]").length'), 0, 'Identical current wording cannot reactivate old-view highlights');
    assert.equal(await evaluate('document.querySelector("#reading-source-text").textContent'), source);
    await evaluate('document.querySelector("#reading-recovery-prepare").click()');
    assert.equal(await evaluate('document.querySelector("#reading-discard-original").disabled'), true);
    await evaluate('document.querySelector("#reading-recovery-cancel").click()');
    assert.equal(await evaluate('document.querySelector("#reading-original-text").value'), originalThought);
    await evaluate('document.querySelector("#reading-recovery-prepare").click(); document.querySelector("#reading-recovery-text").value="Recovered as a new passage note"; document.querySelector("#reading-recovery-text").dispatchEvent(new Event("input")); document.querySelector("#reading-recovery-target").value="john-9"; document.querySelector("#reading-recovery-target").dispatchEvent(new Event("change"))');
    await reviseView('change');
    await cdp('Page.reload');
    await until('Boolean(document.querySelector("#reading-recovery-refresh"))');
    assert.equal(await evaluate('document.querySelector("#reading-recovery-save").disabled'), true, 'A prepared note cannot be moved to another view silently');
    assert.equal(await evaluate('document.querySelector("#reading-recovery-text").value'), 'Recovered as a new passage note');
    await evaluate('document.querySelector("#reading-recovery-refresh").click()');
    assert.equal(await evaluate('document.querySelector("#reading-recovery-save").disabled'), false);
    const beforeRecoverySave = (await (await fetch(`${base}/api/reading/view`)).json()).remaining_saves;
    await evaluate(`(() => {const nativeFetch=window.fetch;window.__recoveryNativeFetch=nativeFetch;window.fetch=async(...args)=>{const response=await nativeFetch(...args);if(String(args[0]).endsWith('/api/reading/items'))throw new TypeError('Synthetic lost recovery response');return response;};document.querySelector('#reading-recovery-save').click();})()`);
    await until('document.querySelector("#reading-recovery-save")?.textContent === "Check / retry this save" && !document.querySelector("#reading-recovery-save").disabled');
    assert.equal(await evaluate('document.querySelector("#reading-discard-original").disabled'), true);
    const committedRecovery = await (await fetch(`${base}/api/reading/view`)).json();
    assert.equal(committedRecovery.remaining_saves, beforeRecoverySave - 1);
    await evaluate(`window.fetch=async(...args)=>String(args[0]).endsWith('/api/reading/items') ? new Response(JSON.stringify({error:'reading_forbidden'}),{status:403,headers:{'Content-Type':'application/json'}}) : window.__recoveryNativeFetch(...args);document.querySelector('#reading-recovery-save').click()`);
    await until('document.querySelector("#reading-recovery-save")?.disabled === false');
    assert.equal(await evaluate('document.querySelector("#reading-recovery-text").disabled'), true, 'Auth failure cannot unlock an uncertain saved copy');
    assert.equal(await evaluate('document.querySelector("#reading-discard-original").disabled'), true);
    await cdp('Page.reload');
    await until('document.querySelector("#reading-recovery-save")?.textContent === "Check / retry this save"');
    await evaluate('document.querySelector("#reading-recovery-save").click()');
    await until('!document.querySelector("#reading-recovery-save") && document.querySelector("#reading-recovery").textContent.includes("New passage note saved privately")');
    const recoveredState = await (await fetch(`${base}/api/reading/view`)).json();
    assert.equal(recoveredState.remaining_saves, committedRecovery.remaining_saves, 'Recovery retry must not consume a second bank revision');
    const newNote = recoveredState.items.find(item => item.text === 'Recovered as a new passage note');
    assert.equal(newNote.kind, 'note'); assert.equal(newNote.anchor, null); assert.equal(newNote.target_id, null); assert.equal(newNote.passage_id, 'john-9');
    assert.equal(recoveredState.items.length, 5);
    const originalKept = await evaluate(`JSON.parse(Object.entries(sessionStorage).find(([key])=>key.startsWith('jeb.reading.draft.'))[1])`);
    assert.equal(originalKept.text, originalThought); assert.equal(originalKept.anchor.exact, 'blue ribbon');
    assert.notEqual(originalKept.view_ref.revision_id, newNote.view_ref.revision_id);
    assert.ok(originalKept.source_context.source.edition.includes('Synthetic English fixture'));
    assert.equal(JSON.parse(browserDraftExport(originalKept)).draft.anchor.exact, 'blue ribbon');
    await reviseView('remove');
    await evaluate(`[...document.querySelectorAll('.desk-personal-actions button')].find(button=>button.textContent==='Refresh saved notes').click()`);
    await until('Boolean(document.querySelector("#desk-search")) && Boolean(document.querySelector("#reading-recovery"))');
    assert.equal(await evaluate('document.querySelector("#reading-original-text").value'), originalThought, 'A removed passage must not strand or erase the draft');
    await cdp('Page.reload');
    await until('Boolean(document.querySelector("#reading-recovery"))');
    await cdp('Emulation.setDeviceMetricsOverride', { width: 460, height: 850, deviceScaleFactor: 1, mobile: false });
    assert.ok(await evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Orphaned-draft recovery overflows a narrow viewport');
    assert.equal(await evaluate('document.querySelector("#reading-original-quote").textContent'), 'blue ribbon');
    await evaluate('document.querySelector("#reading-discard-original").click()');
    assert.equal(await evaluate('Boolean(document.querySelector("#reading-recovery"))'), false);
    assert.equal((await (await fetch(`${base}/api/reading/view`)).json()).items.length, 5, 'Discarding the browser original must not delete saved items');
    assert.deepEqual(browserErrors, []);
    await writeFile(path.join(repo, 'reports/generated/reading-browser-verification.json'), JSON.stringify({ browser, saved_types: ['highlight', 'note', 'connection'], restored_items: 5, literal_source_unchanged: true, language_and_draft_preserved: true, cancelled_draft_not_saved: true, source_scroll_restored: scroll, narrow_viewport: 460, bilingual_guide_and_practice_link: true, guide_preserves_draft: true, saved_work_search_and_source_return: true, editor_beside_source: true, draft_survives_refresh_without_bank_writes: true, uncertain_save_retry_and_legacy_recovery: true, clickable_and_keyboard_highlight_comments: true, ctrl_enter_saves: true, conflict_recovery_preserves_both_versions: true, stale_and_orphaned_draft_recovery: true, recovery_retry_preserves_original_and_auth_safety: true, browser_errors: browserErrors }, null, 2));
    await cdp('Browser.close').catch(() => {});
  } finally {
    socket?.close();
    child?.kill();
    if (server?.listening) { server.closeAllConnections(); await new Promise(resolve => server.close(resolve)); }
    const resolved = await realpath(directory), base = await realpath(os.tmpdir());
    const relative = path.relative(base, resolved);
    assert.ok(relative && !relative.startsWith('..') && !path.isAbsolute(relative) && path.basename(resolved).startsWith('jsb-reading-'));
    await rm(resolved, { recursive: true, force: true, maxRetries: 15, retryDelay: 200 });
  }
});
