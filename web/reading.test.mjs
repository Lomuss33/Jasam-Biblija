import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { mkdtemp, realpath, rm, readFile } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { createServer } from './server.mjs';
import { textSegments, pointOffset, safeLink, canLocateItem, searchItems, sourceSegments, sameReadingView, draftNeedsRecovery, recoveryNote, browserDraftExport, saveUnconfirmed } from './reading-state.mjs';

const exec = promisify(execFile);
const repo = fileURLToPath(new URL('../', import.meta.url));
const python = process.env.JEB_TEST_PYTHON || path.join(repo, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
async function cleanup(directory) {
  const resolved = await realpath(directory), base = await realpath(os.tmpdir());
  const relative = path.relative(base, resolved);
  assert.ok(relative && !relative.startsWith('..') && !path.isAbsolute(relative) && path.basename(resolved).startsWith('jsb-reading-'));
  await rm(resolved, { recursive: true, force: true });
}

test('Unicode selections preserve original text and merge overlapping visual highlights only', () => {
  const text = '😀 Z\u030cana vidi Luma.';
  const utf16Start = text.indexOf('Luma');
  const start = pointOffset(text, utf16Start);
  assert.equal(Array.from(text).slice(start, start + 4).join(''), 'Luma');
  assert.equal(start, utf16Start - 1);
  const segments = textSegments(text, [{ start, end: start + 4, exact: 'Luma' }, { start: 0, end: 1, exact: 'WRONG' }]);
  assert.equal(segments.map(s => s.text).join(''), text);
  assert.deepEqual(segments.filter(s => s.marked).map(s => s.text), ['Luma']);
  const overlaps = textSegments('Luma Nera', [{ start: 0, end: 4, exact: 'Luma' }, { start: 0, end: 9, exact: 'Luma Nera' }]);
  assert.equal(overlaps.map(s => s.text).join(''), 'Luma Nera');
  assert.equal(safeLink('javascript:alert(1)'), null);
});

test('saved-work search finds personal wording and exact quotes without rebinding old anchors', () => {
  const passages = [
    { id: 'ledger', book: 'MAT', title: { en: 'The ledger', bs: 'Zapis' }, location: 'Original example', text: '😀 blue ribbon' },
    { id: 'room', book: 'MRK', title: { en: 'Reading room', bs: 'Čitaonica' }, text: null },
  ];
  const anchor = { start: 2, end: 13, exact: 'blue ribbon' };
  const earlier = { id: 'old', passage_id: 'ledger', current_view: false, kind: 'highlight', anchor, text: '', revised_at: '2026-11-19T10:00:00Z' };
  const highlight = { ...earlier, id: 'new', current_view: true, revised_at: '2026-11-20T10:00:00Z' };
  const note = { ...highlight, id: 'note', kind: 'note', anchor: null, text: '<script>svjet vrjeme covik razumit</script>', revised_at: '2026-11-20T11:00:00Z' };
  const connection = { ...note, id: 'link', kind: 'connection', target_id: 'room', text: 'Compare these scenes', revised_at: '2026-11-20T12:00:00Z' };
  const items = [earlier, highlight, note, connection];
  assert.deepEqual(searchItems(items, passages, 'blue ribbon').map(i => i.id), ['new', 'old']);
  assert.deepEqual(searchItems(items, passages, ' RAZUMIT ', 'note').map(i => i.id), ['note']);
  assert.deepEqual(searchItems(items, passages, 'ČITAONICA').map(i => i.id), ['link']);
  assert.deepEqual(searchItems(items, passages, 'Zapis', 'highlight').map(i => i.id), ['new', 'old']);
  assert.deepEqual(searchItems(items, passages, '', 'note').map(i => i.id), ['note']);
  assert.deepEqual(searchItems(items, passages, 'missing'), []);
  assert.equal(items[0], earlier, 'Search must not reorder the stored input');
  assert.equal(canLocateItem(highlight, passages[0]), true);
  assert.equal(canLocateItem(earlier, passages[0]), false, 'Identical wording cannot rebind an earlier view');
  assert.equal(canLocateItem(highlight, { ...passages[0], id: 'foreign' }), false);
  assert.equal(canLocateItem(highlight, { ...passages[0], text: '😀 new wording' }), false);
  assert.equal(canLocateItem(highlight, undefined), false);
  assert.equal(canLocateItem(note, passages[0]), false);
  assert.equal(canLocateItem({ ...highlight, anchor: { ...anchor, start: 3 } }, passages[0]), false, 'Offsets count Unicode points');
});

test('overlapping highlights preserve exact text and expose only current saved comments', () => {
  const passage = { id: 'ledger', text: '😀 blue ribbon' };
  const whole = { id: 'whole', kind: 'highlight', current_view: true, passage_id: 'ledger', anchor: { start: 2, end: 13, exact: 'blue ribbon' } };
  const word = { ...whole, id: 'word', anchor: { start: 2, end: 6, exact: 'blue' } };
  const old = { ...whole, id: 'old', current_view: false };
  const foreign = { ...whole, id: 'foreign', passage_id: 'elsewhere' };
  const invalid = { ...whole, id: 'invalid', anchor: { ...whole.anchor, exact: 'Different words' } };
  const segments = sourceSegments(passage, [whole, word, old, foreign, invalid]);
  assert.equal(segments.map(s => s.text).join(''), passage.text);
  assert.deepEqual(segments.find(s => s.text === 'blue').savedIds, ['whole', 'word']);
  assert.deepEqual(segments.find(s => s.text === ' ribbon').savedIds, ['whole']);
  assert.deepEqual(segments[0].savedIds, []);
  const evidenceOnly = sourceSegments(passage, [old], whole.anchor);
  assert.ok(evidenceOnly.some(s => s.marked));
  assert.ok(evidenceOnly.every(s => !s.savedIds.length), 'A proof marker cannot impersonate a saved private highlight');
  assert.deepEqual(sourceSegments({ id: 'unavailable', text: null }, [whole]), []);
});

test('stale and orphaned drafts remain distinct from the current view', () => {
  const reference = { record_id: 'view', revision_id: 'first', record_sha256: 'record', body_sha256: 'body' };
  const draft = { view_ref: reference, passage_id: 'ledger' };
  const data = { enabled: true, view_ref: { ...reference }, passages: [{ id: 'ledger' }] };
  assert.equal(sameReadingView(reference, data.view_ref), true);
  assert.equal(sameReadingView(undefined, undefined), false);
  assert.equal(sameReadingView(reference, { ...reference, body_sha256: 'changed' }), false);
  assert.equal(draftNeedsRecovery(draft, data), false);
  assert.equal(draftNeedsRecovery(draft, { ...data, view_ref: { ...reference, revision_id: 'later' } }), true);
  assert.equal(draftNeedsRecovery(draft, { ...data, passages: [] }), true);
  assert.equal(draftNeedsRecovery(draft, { enabled: false }), true);
  assert.equal(draftNeedsRecovery({ ...draft, recovery: { status: 'uncertain' } }, data), true, 'An uncertain recovery cannot be hidden by returning to the old view');
});

test('recovery creates an unanchored new note and exports the unchanged original quote and credits', () => {
  const original = { kind: 'connection', text: 'svjet vrjeme covik razumit\nMy private reason', passage_id: 'ledger', target_id: 'room', request_id: 'original-request', edit_record_id: 'old-item', expected_revision: 'old-revision',
    anchor: { start: 2, end: 13, exact: 'blue ribbon' }, view_ref: { record_id: 'view', revision_id: 'old', record_sha256: 'old-record', body_sha256: 'old-body' },
    source_context: { source: { title: 'Original invented edition', edition: 'Fixture v1', creator: 'Fixture author', translator: 'Original fixture credit' } } };
  const preserved = structuredClone(original);
  const current = { ...original.view_ref, revision_id: 'new' };
  const payload = recoveryNote(original, current, 'john-9', 'fresh-request');
  assert.equal(payload.kind, 'note'); assert.equal(payload.text, original.text);
  assert.equal(payload.passage_id, 'john-9'); assert.equal(payload.anchor, null); assert.equal(payload.target_id, null);
  assert.equal(payload.edit_record_id, null); assert.equal(payload.expected_revision, null);
  assert.notEqual(payload.request_id, original.request_id);
  assert.deepEqual(original, preserved);
  payload.view_ref.revision_id = 'local-change';
  assert.equal(current.revision_id, 'new', 'Preparing a note must not mutate the current binding');
  const packet = JSON.parse(browserDraftExport(original));
  assert.deepEqual(packet.draft, preserved); assert.equal(packet.releasable, false);
  assert.equal(packet.draft.source_context.source.translator, 'Original fixture credit');
  assert.equal(packet.draft.anchor.exact, 'blue ribbon');
});

test('an auth or lock failure cannot settle an earlier unconfirmed write', () => {
  for (const error of ['reading_forbidden', 'reading_read_only', 'reading_busy', 'history_limit', 'invalid_reading_input']) {
    assert.equal(saveUnconfirmed({ error }, true), true, error);
    assert.equal(saveUnconfirmed({ error }, false), false, error);
  }
  assert.equal(saveUnconfirmed({ error: 'stale_view' }, true), false);
  assert.equal(saveUnconfirmed({ error: 'revision_conflict' }, true), false);
  assert.equal(saveUnconfirmed({ saved: true }, true), false);
  assert.equal(saveUnconfirmed({ error: 'reading_unavailable' }, false), true);
  assert.equal(saveUnconfirmed({}, true), true);
});

test('reading API persists all private types, rejects stale writes and preserves exact requests', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'jsb-reading-http-'));
  const bank = path.join(directory, 'bank');
  let server;
  try {
    await exec(python, ['-B', '-m', 'jeb', '--synthetic', 'reading', 'demo', '--bank-root', bank], { cwd: repo, windowsHide: true });
    const before = await readFile(path.join(bank, 'HEAD.json'), 'utf8');
    server = createServer({ readingRoot: bank, readingSynthetic: true, readingWritable: true, readingPython: python });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    const session = await (await fetch(`${base}/api/reading/session`)).json();
    assert.equal(session.enabled, true);
    assert.equal(session.passages.find(p => p.id === 'john-9').text, null);
    assert.match(session.write_token, /^[0-9a-f]{64}$/);
    assert.equal(await readFile(path.join(bank, 'HEAD.json'), 'utf8'), before);
    const post = (body, headers = {}) => fetch(`${base}/api/reading/items`, { method: 'POST', headers: { Origin: base, 'Content-Type': 'application/json', 'X-Reading-Token': session.write_token, ...headers }, body: typeof body === 'string' ? body : JSON.stringify(body) });
    const payload = (kind = 'note', changes = {}) => ({ view_ref: session.view_ref, request_id: randomUUID(), kind, passage_id: 'ledger-entry', text: '<script>window.privateNoteExecuted=true</script>', anchor: null, target_id: null, edit_record_id: null, expected_revision: null, ...changes });
    const note = payload();
    const first = await (await post(note)).json(); assert.equal(first.saved, true);
    const again = await (await post(note)).json(); assert.equal(again.id, first.id); assert.equal(again.replayed, true);
    const body = session.passages[0].text;
    const start = Array.from(body.slice(0, body.indexOf('blue ribbon'))).length;
    const highlight = payload('highlight', { text: '', anchor: { start, end: start + 11, exact: 'blue ribbon' } });
    assert.equal((await (await post(highlight)).json()).saved, true);
    assert.equal((await (await post(payload('connection', { target_id: 'reading-room', text: 'A private motif suggestion' }))).json()).saved, true);
    let state = await (await fetch(`${base}/api/reading/view`)).json(); assert.equal(state.items.length, 3);
    const edit = payload('note', { edit_record_id: first.id, expected_revision: first.revision_id, text: 'A newer note' });
    assert.equal((await (await post(edit)).json()).saved, true);
    const conflict = await post({ ...edit, request_id: randomUUID(), text: 'Stale edit' });
    assert.equal(conflict.status, 409); assert.equal((await conflict.json()).error, 'revision_conflict');
    for (const headers of [{ Origin: 'https://foreign.example' }, { 'X-Reading-Token': 'wrong' }, { 'Sec-Fetch-Site': 'cross-site' }]) assert.equal((await post(payload(), headers)).status, 403);
    assert.equal((await post(payload(), { 'Content-Type': 'text/plain' })).status, 415);
    assert.equal((await post('x'.repeat(17000))).status, 413);
    assert.equal((await post('{broken')).status, 422);
    assert.equal((await post('{"kind":"note","kind":"highlight"}')).status, 422);
    assert.equal((await post({ ...payload(), bank_root: '/outside' })).status, 422);
    assert.equal((await fetch(`${base}/api/bank`, { method: 'POST' })).status, 405);
    const concurrent = payload();
    const responses = await Promise.all([post(concurrent), post(concurrent)]);
    assert.ok(responses.some(r => r.status === 200));
    await Promise.all(responses.map(r => r.json()));
    assert.equal((await (await post(concurrent)).json()).replayed, true);
    state = await (await fetch(`${base}/api/reading/view`)).json();
    assert.equal(state.items.length, 4);
    assert.equal(state.items.find(item => item.id === first.id).text, 'A newer note');
    assert.ok(!JSON.stringify(state).includes(directory));
  } finally {
    if (server?.listening) { server.closeAllConnections(); await new Promise(resolve => server.close(resolve)); }
    await cleanup(directory);
  }
});

test('non-opt-in reading workspaces never gain write access', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'jsb-reading-disabled-'));
  let server;
  try {
    const bank = path.join(directory, 'bank');
    await exec(python, ['-B', '-m', 'jeb', '--synthetic', 'reading', 'demo', '--bank-root', bank], { cwd: repo, windowsHide: true });
    const before = await readFile(path.join(bank, 'HEAD.json'), 'utf8');
    server = createServer({ readingRoot: bank, readingSynthetic: false, readingWritable: true, readingPython: python });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    const response = await fetch(`${base}/api/reading/session`);
    assert.equal(response.status, 422);
    const result = await response.json(); assert.equal(result.enabled, false); assert.equal(result.write_token, undefined);
    assert.equal(await readFile(path.join(bank, 'HEAD.json'), 'utf8'), before);
  } finally {
    if (server?.listening) { server.closeAllConnections(); await new Promise(resolve => server.close(resolve)); }
    await cleanup(directory);
  }
});
