import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import http from 'node:http';
import { mkdtemp, mkdir, readdir, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import os from 'node:os';
import path from 'node:path';
import { createServer, documents } from './server.mjs';

const execFileAsync = promisify(execFile);
const repo = fileURLToPath(new URL('../', import.meta.url));
const python = process.env.JEB_TEST_PYTHON || path.join(repo, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
async function historicalCli(...args) {
  const command = ['-B', '-m', 'jeb', '--root', repo, '--synthetic', 'historical', ...args];
  try { return JSON.parse((await execFileAsync(python, command, { cwd: repo, windowsHide: true, maxBuffer: 8 * 1024 * 1024 })).stdout); }
  catch (error) { if (error.code === 2 && error.stdout) return JSON.parse(error.stdout); throw error; }
}
async function cleanup(directory) {
  const resolved = await realpath(directory);
  const temporary = await realpath(os.tmpdir());
  const relative = path.relative(temporary, resolved);
  assert.ok(relative && !relative.startsWith('..') && !path.isAbsolute(relative) && path.basename(resolved).startsWith('jsb-'));
  await rm(resolved, { recursive: true, force: true });
}

test('local viewer exposes only explicit documents and never accepts writes', async () => {
  const server = createServer();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    const home = await fetch(base);
    assert.equal(home.status, 200);
    assert.match(await home.text(), /lang="hr"/);
    assert.match(home.headers.get('content-security-policy'), /frame-ancestors 'none'/);
    const state = await (await fetch(`${base}/api/workspace`)).json();
    assert.equal(state.documents.length, documents.length);
    assert.equal(typeof state.lockedSources, 'number');
    assert.equal(state.bank.enabled, false);
    assert.equal(state.historical_pipeline.status, 'blocked');
    assert.equal(state.historical_pipeline.blockers.length, 4);
    assert.equal((await fetch(`${base}/api/bank`)).status, 200);
    assert.equal((await (await fetch(`${base}/api/bank`)).json()).enabled, false);
    const catalog = await (await fetch(`${base}/api/library`)).json();
    assert.equal(catalog.books.length, 291);
    const discovery = await (await fetch(`${base}/api/library/research/search-001`)).json();
    assert.equal(discovery.book_ids.length, 4);
    assert.equal((await fetch(`${base}/api/library/research/unknown`)).status, 404);
    assert.equal((await fetch(`${base}/library/private/dhammapada-veljacic.html`)).status, 404);
    for (const asset of ['/app.js', '/style.css', '/library.js']) {
      assert.equal((await fetch(`${base}${asset}`)).status, 200);
    }
    for (const [id] of documents) {
      const response = await fetch(`${base}/api/document/${id}`);
      assert.equal(response.status, 200);
      assert.ok((await response.json()).text.length > 0);
    }
    for (const route of ['/sources/lock.json', '/.git/config', '/data/private-source-audit/GEN-1-1-5-review.md', '/api/document/../../PROGRESS.md', '/api/document/%2e%2e%2fPROGRESS.md', '/api/document/unknown']) {
      assert.equal((await fetch(`${base}${route}`)).status, 404, route);
    }
    assert.equal((await fetch(base, { method: 'POST', body: '{}' })).status, 405);
    assert.equal((await fetch(base, { headers: { Origin: 'https://example.org' } })).status, 403);
    const foreignHost = await new Promise((resolve, reject) => {
      http.get(base, { headers: { Host: 'example.org:5187' } }, response => {
        response.resume(); resolve(response.statusCode);
      }).on('error', reject);
    });
    assert.equal(foreignHost, 403);
  } finally {
    await new Promise(resolve => server.close(resolve));
  }
});

test('knowledge-bank endpoint is opt-in and read-only', async () => {
  const bank = await mkdtemp(path.join(os.tmpdir(), 'jsb-bank-view-'));
  const transaction = '11111111-1111-4111-8111-111111111111';
  const record = '22222222-2222-4222-8222-222222222222';
  await mkdir(path.join(bank, 'snapshots', transaction, 'records', record), { recursive: true });
  await mkdir(path.join(bank, 'staging'));
  const workspace = { schema_version: '3.0', workspace_id: '33333333-3333-4333-8333-333333333333', title: 'Sintetička baza', created_at: '2026-11-18T00:00:00Z' };
  const head = { transaction_id: transaction, manifest_sha256: '4'.repeat(64) };
  const manifest = { schema_version: '3.0', transaction_id: transaction, parent_head: null, snapshot_sha256: '5'.repeat(64), changed_record: record, created_at: '2026-11-18T00:00:00Z', reason: 'Sintetički test' };
  const item = { schema_version: '3.0', workspace_id: workspace.workspace_id, id: record, kind: 'claim', title: 'Probna tvrdnja', created_at: '2026-11-18T00:00:00Z', recorded_by: { id: 'test', kind: 'tool' }, revision_id: '44444444-4444-4444-8444-444444444444', parent_revision: null, body_sha256: null, visibility: 'private', processing_state: 'inbox', data: { subject: { record_id: record, revision_id: '44444444-4444-4444-8444-444444444444', record_sha256: '6'.repeat(64), body_sha256: null }, statement: 'Probna tvrdnja', category: 'source_statement', limitations: 'Test', review_state: 'unreviewed' }, revised_at: '2026-11-18T00:00:00Z', reason: 'Sintetički test' };
  await writeFile(path.join(bank, 'workspace.json'), JSON.stringify(workspace));
  await writeFile(path.join(bank, 'HEAD.json'), JSON.stringify(head));
  await writeFile(path.join(bank, 'snapshots', transaction, 'workspace.json'), JSON.stringify({ ...workspace, schema_version: '1.0' }));
  await writeFile(path.join(bank, 'snapshots', transaction, 'manifest.json'), JSON.stringify(manifest));
  await writeFile(path.join(bank, 'snapshots', transaction, 'records', record, 'record.json'), JSON.stringify(item));
  const server = createServer({ bankRoot: bank });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    const state = await (await fetch(`${base}/api/bank`)).json();
    assert.equal(state.enabled, true);
    assert.equal(state.records[0].kind, 'claim');
    const search = await (await fetch(`${base}/api/bank/search?q=Probna`)).json();
    assert.equal(search.results.length, 1);
    assert.ok(search.results[0].matches.includes('title'));
    const detail = await (await fetch(`${base}/api/bank/record/${record}`)).json();
    assert.equal(detail.record.title, 'Probna tvrdnja');
    assert.equal(detail.links.subject.id, record);
    assert.equal(detail.links.subject.is_current_revision, true);
    assert.deepEqual(detail.links.evidence, []);
    assert.equal(detail.history.length, 1);
    assert.equal(detail.history[0].revision_id, item.revision_id);
    assert.equal((await fetch(`${base}/api/bank/record/../../workspace.json`)).status, 404);
    assert.equal((await fetch(base, { method: 'POST', body: '{}' })).status, 405);
  } finally {
    await new Promise(resolve => server.close(resolve));
    await rm(bank, { recursive: true, force: true });
  }
});

test('nonempty synthetic pipeline has exact CLI/API parity and source-scoped lookups', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'jsb-historical-view-'));
  let server;
  try {
    const demo = await historicalCli('demo', '--workspace', path.join(directory, 'demo'));
    const workspace = demo.workspace;
    const before = await readFile(path.join(workspace, 'pipeline.json'), 'utf8');
    const headBefore = await readFile(path.join(workspace, 'HEAD.json'), 'utf8');
    server = createServer({ historicalWorkspace: workspace, historicalSynthetic: true, historicalPython: python });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    const apiStatus = await (await fetch(`${base}/api/historical/status`)).json();
    const cliStatus = await historicalCli('status', '--workspace', workspace);
    assert.deepEqual(apiStatus, cliStatus);
    assert.equal(apiStatus.status, 'ready');
    assert.ok(apiStatus.counts.index.candidates > 0);
    assert.equal(apiStatus.pipeline.queue.complete, 3);
    assert.equal(apiStatus.pipeline.queue.pending, 1);
    assert.equal(apiStatus.pipeline.queue.needs_review, 1);
    const built = await (await fetch(`${base}/api/historical/build-dossier?q=Luma&work=MAT&locator_limit=1`)).json();
    const cliBuilt = await historicalCli('dossier', '--workspace', workspace, '--query=Luma', '--work=MAT', '--locator-limit=1');
    assert.deepEqual(built, cliBuilt);
    assert.equal(built.entities_total, 1);
    assert.equal(built.entities[0].candidate_count, 3);
    assert.equal(built.entities[0].locators.length, 1);
    assert.equal(built.entities[0].locators_truncated, true);
    assert.match(built.entities[0].locators[0].source_sha256, /^[a-f0-9]{64}$/);
    assert.equal(built.entities[0].sources[0].contributors.length, 1);
    const lookup = await (await fetch(`${base}/api/historical/lookup?q=Luma`)).json();
    assert.deepEqual(lookup.results.map(item => [item.work_id, item.locator_count]), [['MAT', 3], ['MRK', 1]]);
    const work = await (await fetch(`${base}/api/historical/dossiers?q=MAT&limit=1`)).json();
    assert.equal(work.results.length, 1);
    assert.equal(work.truncated, true);
    const details = await (await fetch(`${base}/api/historical/dossier/${built.entities[0].id}?locator_limit=1&locator_offset=1`)).json();
    assert.equal(details.locator_offset, 1);
    const relation = await (await fetch(`${base}/api/historical/relations?work=MAT&relation=version_of`)).json();
    assert.equal(relation.total, 3);
    assert.ok(relation.results.every(item => item.authoritative === false));
    const empty = await (await fetch(`${base}/api/historical/build-dossier?q=UnknownTopic`)).json();
    assert.deepEqual(empty.relations, []);
    for (const endpoint of ['/api/historical/dossiers?limit=NaN', '/api/historical/build-dossier', '/api/historical/lookup?offset=-1', '/api/historical/relations?workspace=unexpected']) assert.equal((await fetch(`${base}${endpoint}`)).status, 400);
    assert.equal((await fetch(`${base}/api/historical/dossier/unknown`)).status, 404);
    assert.equal((await fetch(`${base}/api/historical/status`, { method: 'POST' })).status, 405);
    const state = await (await fetch(`${base}/api/workspace`)).json();
    assert.equal(state.historical.enabled, true);
    assert.equal(state.lockedSources, 0);
    assert.equal(await readFile(path.join(workspace, 'pipeline.json'), 'utf8'), before);
    assert.equal(await readFile(path.join(workspace, 'HEAD.json'), 'utf8'), headBefore);
  } finally {
    if (server?.listening) await new Promise(resolve => server.close(resolve));
    await cleanup(directory);
  }
});

test('configured stale and malformed layers produce equivalent path-free errors', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'jsb-historical-errors-'));
  let server;
  try {
    const demo = await historicalCli('demo', '--workspace', path.join(directory, 'demo'));
    const head = JSON.parse(await readFile(path.join(demo.workspace, 'HEAD.json'), 'utf8'));
    const files = {};
    for (const layer of ['registry', 'index', 'groups', 'dossiers']) {
      files[layer] = path.join(directory, `${layer}.json`);
      await writeFile(files[layer], await readFile(path.join(demo.workspace, 'snapshots', head.snapshot_id, `${layer}.json`)));
    }
    server = createServer({ historicalRegistryPath: files.registry, historicalIndexPath: files.index, historicalGroupsPath: files.groups, historicalDossiersPath: files.dossiers, historicalPython: python });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    const registry = JSON.parse(await readFile(files.registry, 'utf8'));
    registry.works[0].title = 'Changed synthetic edition metadata';
    await writeFile(files.registry, JSON.stringify(registry));
    const args = Object.entries(files).flatMap(([layer, file]) => [`--${layer}`, file]);
    const status = await (await fetch(`${base}/api/historical/status`)).json();
    assert.deepEqual(status, await historicalCli('status', ...args));
    assert.equal(status.status, 'blocked');
    assert.ok(status.blockers.some(item => item.reason === 'stale_hash'));
    const stale = await fetch(`${base}/api/historical/build-dossier?q=Luma`);
    assert.equal(stale.status, 409);
    assert.deepEqual(await stale.json(), await historicalCli('dossier', '--query=Luma', ...args));
    await writeFile(files.registry, '{bad-json');
    const malformed = await fetch(`${base}/api/historical/relations`);
    assert.equal(malformed.status, 422);
    const payload = await malformed.json();
    assert.equal(payload.error, 'invalid_historical_input');
    assert.equal(payload.layer, 'registry');
    assert.ok(!JSON.stringify(payload).includes(directory));
    const workspace = await (await fetch(`${base}/api/workspace`)).json();
    assert.equal(workspace.documents.length, documents.length);
    assert.equal(workspace.historical.error, 'invalid_historical_input');
    assert.equal((await fetch(base)).status, 200);
  } finally {
    if (server?.listening) await new Promise(resolve => server.close(resolve));
    await cleanup(directory);
  }
});

test('historical workspace opt-in and runtime failures do not hide unrelated viewer data', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'jsb-historical-opt-in-'));
  let server;
  try {
    const demo = await historicalCli('demo', '--workspace', path.join(directory, 'demo'));
    server = createServer({ historicalWorkspace: demo.workspace, historicalSynthetic: false, historicalPython: python });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    const blocked = await (await fetch(`${base}/api/historical/status`)).json();
    assert.equal(blocked.status, 'blocked');
    assert.equal(blocked.blockers[0].reason, 'invalid_workspace');
    assert.equal((await fetch(`${base}/api/library`)).status, 200);
    await new Promise(resolve => server.close(resolve));
    server = createServer({ historicalWorkspace: demo.workspace, historicalSynthetic: true, historicalPython: path.join(directory, 'missing-python') });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const unavailable = await fetch(`http://127.0.0.1:${server.address().port}/api/historical/status`);
    assert.equal(unavailable.status, 503);
    assert.equal((await unavailable.json()).error, 'historical_runtime_unavailable');
    assert.ok((await readdir(demo.workspace)).includes('pipeline.json'));
  } finally {
    if (server?.listening) await new Promise(resolve => server.close(resolve));
    await cleanup(directory);
  }
});
