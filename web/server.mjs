import http from 'node:http';
import { readdir, readFile, realpath } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { randomBytes, timingSafeEqual } from 'node:crypto';
import { createHistoricalBridge, historicalHttpStatus } from './historical.mjs';
import { boundedBody, createReadingBridge, readingStatus } from './reading-api.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
export const documents = [
  ['next', 'Sljedeći koraci', 'Radni plan', 'NEXT_STEPS.md'],
  ['comparison', 'Koji izvor koristiti?', 'Izvori', 'docs/sources/SOURCE_COMPARISON_2026-10-31.md'],
  ['language', 'Hercegovački jezični vodič', 'Jezik', 'docs/HERZEGOVINIAN_LANGUAGE_GUIDE.md'],
  ['entries', 'Riječi i historijski svjedoci', 'Jezik', 'docs/sources/LANGUAGE_ENTRY_BATCH_2026-10-31.md'],
  ['direction', 'Dogovoreni jezični smjer', 'Jezik', 'docs/decisions/0014-herzegovinian-register-with-broad-comprehensibility.md'],
  ['charter', 'Svrha i opseg projekta', 'Projekt', 'docs/PROJECT_CHARTER.md'],
  ['rights', 'Prava i uvjeti korištenja', 'Izvori', 'docs/RIGHTS_POLICY.md'],
  ['review', 'Kako pregledavati prijedloge', 'Radni postupak', 'docs/REVIEW_GUIDE.md'],
  ['terminal', 'Rad u terminalu', 'Radni postupak', 'docs/TERMINAL_WORKFLOW.md'],
  ['architecture', 'Kako je alat složen', 'Projekt', 'docs/ARCHITECTURE.md'],
];
// Only named public project inputs are readable. Never serve the repository root.
async function read(relative) {
  const resolved = await realpath(path.join(root, relative));
  const base = await realpath(root);
  const within = path.relative(base, resolved);
  if (within.startsWith('..') || path.isAbsolute(within)) throw new Error('Outside workspace');
  return readFile(resolved, 'utf8');
}
async function readBankFile(bankRoot, relative) {
  const resolved = await realpath(path.join(bankRoot, relative));
  const base = await realpath(bankRoot);
  const within = path.relative(base, resolved);
  if (within.startsWith('..') || path.isAbsolute(within)) throw new Error('Outside bank');
  return readFile(resolved, 'utf8');
}
async function bankState(bankRoot) {
  if (!bankRoot) return { enabled: false };
  const workspace = JSON.parse(await readBankFile(bankRoot, 'workspace.json'));
  const head = JSON.parse(await readBankFile(bankRoot, 'HEAD.json'));
  const manifest = JSON.parse(await readBankFile(bankRoot, `snapshots/${head.transaction_id}/manifest.json`));
  const ids = await readdir(path.join(bankRoot, 'snapshots', head.transaction_id, 'records'));
  const records = [];
  for (const id of ids.sort()) {
    if (!/^[0-9a-f-]{36}$/.test(id)) continue;
    const record = JSON.parse(await readBankFile(bankRoot, `snapshots/${head.transaction_id}/records/${id}/record.json`));
    records.push({ id: record.id, revision_id: record.revision_id, kind: record.kind, title: record.title, visibility: record.visibility, processing_state: record.processing_state });
  }
  return { enabled: true, workspace: { workspace_id: workspace.workspace_id, title: workspace.title, schema_version: workspace.schema_version }, head, manifest: { transaction_id: manifest.transaction_id, created_at: manifest.created_at }, records };
}
async function bankSearch(bankRoot, query) {
  if (!bankRoot) return { enabled: false, query, results: [] };
  const state = await bankState(bankRoot);
  const lowered = query.trim().toLocaleLowerCase('hr');
  if (!lowered) return { enabled: true, query, results: state.records };
  const results = [];
  for (const item of state.records) {
    const record = JSON.parse(await readBankFile(bankRoot, `snapshots/${state.head.transaction_id}/records/${item.id}/record.json`));
    let body = '';
    if (record.body_sha256) body = await readBankFile(bankRoot, `snapshots/${state.head.transaction_id}/records/${item.id}/body.md`);
    const fields = { title: record.title, kind: record.kind, processing_state: record.processing_state, data: JSON.stringify(record.data), body };
    const matches = Object.entries(fields).filter(([, value]) => value.toLocaleLowerCase('hr').includes(lowered)).map(([field]) => field);
    if (matches.length) results.push({ ...item, matches });
  }
  return { enabled: true, query, results };
}
function referenceTarget(records, reference) {
  if (!reference) return null;
  const target = records.find(record => record.id === reference.record_id);
  if (!target) return null;
  return {
    id: target.id,
    title: target.title,
    kind: target.kind,
    revision_id: reference.revision_id,
    current_revision_id: target.revision_id,
    is_current_revision: reference.revision_id === target.revision_id,
  };
}
function bankLinks(records, record) {
  if (record.kind === 'claim') {
    return {
      subject: referenceTarget(records, record.data.subject),
      evidence: records.filter(candidate => candidate.kind === 'evidence' && candidate.data?.claim?.record_id === record.id).map(candidate => ({
        id: candidate.id,
        title: candidate.title,
        relation: candidate.data.relation,
        claim_revision_id: candidate.data.claim.revision_id,
        applies_to_current_claim: candidate.data.claim.revision_id === record.revision_id,
        source: referenceTarget(records, candidate.data.source),
      })),
    };
  }
  if (record.kind === 'evidence') {
    return {
      claim: referenceTarget(records, record.data.claim),
      source: referenceTarget(records, record.data.source),
      relation: record.data.relation,
      locator: record.data.locator,
    };
  }
  return null;
}
async function bankHistory(bankRoot, transactionId, recordId) {
  const history = [];
  const seen = new Set();
  let transaction = transactionId;
  while (transaction) {
    if (seen.has(transaction) || seen.size >= 128) throw new Error('Invalid bank history chain');
    seen.add(transaction);
    const manifest = JSON.parse(await readBankFile(bankRoot, `snapshots/${transaction}/manifest.json`));
    if (manifest.changed_record === recordId) {
      const record = JSON.parse(await readBankFile(bankRoot, `snapshots/${transaction}/records/${recordId}/record.json`));
      history.push({
        transaction_id: transaction,
        created_at: manifest.created_at,
        reason: manifest.reason,
        revision_id: record.revision_id,
        parent_revision: record.parent_revision,
        revised_at: record.revised_at,
        title: record.title,
        kind: record.kind,
      });
    }
    transaction = manifest.parent_head?.transaction_id || null;
  }
  return history.reverse();
}
export function createServer(options = {}) {
  const readingWritable = options.readingWritable ?? process.env.JEB_READING_WRITE === '1';
  const reading = createReadingBridge(root, {
    bankRoot: options.readingRoot || process.env.JEB_READING_ROOT || null,
    synthetic: options.readingSynthetic ?? process.env.JEB_READING_SYNTHETIC === '1',
    writable: readingWritable,
    python: options.readingPython,
  });
  const readingToken = randomBytes(32).toString('hex');
  const bankRoot = options.bankRoot || (process.env.JEB_BANK_ROOT ? path.resolve(process.env.JEB_BANK_ROOT) : null);
  const historicalDossiersPath = options.historicalDossiersPath || (process.env.JEB_HISTORICAL_DOSSIERS ? path.resolve(process.env.JEB_HISTORICAL_DOSSIERS) : null);
  const historicalPaths = {
    registry: options.historicalRegistryPath || (process.env.JEB_HISTORICAL_REGISTRY ? path.resolve(process.env.JEB_HISTORICAL_REGISTRY) : null),
    index: options.historicalIndexPath || (process.env.JEB_HISTORICAL_INDEX ? path.resolve(process.env.JEB_HISTORICAL_INDEX) : null),
    groups: options.historicalGroupsPath || (process.env.JEB_HISTORICAL_GROUPS ? path.resolve(process.env.JEB_HISTORICAL_GROUPS) : null),
    dossiers: historicalDossiersPath,
  };
  const historical = createHistoricalBridge(root, {
    registryPath: historicalPaths.registry, indexPath: historicalPaths.index,
    groupsPath: historicalPaths.groups, dossiersPath: historicalPaths.dossiers,
    workspace: options.historicalWorkspace || process.env.JEB_HISTORICAL_WORKSPACE || null,
    synthetic: options.historicalSynthetic ?? process.env.JEB_HISTORICAL_SYNTHETIC === '1',
    python: options.historicalPython,
  });
  return http.createServer(async (req, res) => {
    const headers = {
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff',
      'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
    };
    function send(code, body, type = 'application/json; charset=utf-8') {
      res.writeHead(code, { ...headers, 'Content-Type': type });
      res.end(body);
    }
    async function sendHistorical(operation, params = {}) {
      const result = await historical(operation, params);
      return send(historicalHttpStatus(result), JSON.stringify(result));
    }
    try {
      // Reject foreign browser origins and Host headers (including DNS rebinding).
      const host = req.headers.host || '';
      if (!/^(localhost|127\.0\.0\.1):\d+$/.test(host)) return send(403, '{"error":"Local access only"}');
      if (req.headers.origin && ![`http://${host}`].includes(req.headers.origin)) return send(403, '{"error":"Foreign origin"}');
      const url = new URL(req.url, `http://${host}`);
      if (req.method === 'POST' && url.pathname === '/api/reading/items' && readingWritable) {
        const token = Buffer.from(req.headers['x-reading-token'] || '');
        if (req.headers.origin !== `http://${host}` ||
            (req.headers['sec-fetch-site'] && req.headers['sec-fetch-site'] !== 'same-origin') ||
            token.length !== readingToken.length || !timingSafeEqual(token, Buffer.from(readingToken))) {
          return send(403, '{"error":"reading_write_forbidden"}');
        }
        if (req.headers['content-type'] !== 'application/json') return send(415, '{"error":"json_required"}');
        if (Number(req.headers['content-length']) > 16384) return send(413, '{"error":"request_too_large"}');
        const body = await boundedBody(req);
        if (body === null) return send(413, '{"error":"request_too_large"}');
        let text;
        try { text = new TextDecoder('utf-8', { fatal: true }).decode(body); }
        catch { return send(400, '{"error":"invalid_reading_input"}'); }
        const result = await reading('save', text);
        return send(readingStatus(result), JSON.stringify(result));
      }
      if (req.method !== 'GET') return send(405, '{"error":"Read only"}');
      if (url.pathname === '/api/reading/session' || url.pathname === '/api/reading/view') {
        const result = await reading('view');
        if (url.pathname.endsWith('/session') && result.enabled && !result.error) {
          result.writable = readingWritable;
          if (readingWritable) result.write_token = readingToken;
        }
        return send(readingStatus(result), JSON.stringify(result));
      }
      if (url.pathname === '/api/library') {
        return send(200, await read('library/catalog.json'));
      }
      if (url.pathname.startsWith('/api/library/research/')) {
        const id = url.pathname.slice('/api/library/research/'.length);
        const searches = JSON.parse(await read('library/research/searches.json'));
        const search = searches.find(s => s.id === id);
        if (!search) return send(404, '{"error":"Search not available"}');
        return send(200, JSON.stringify(search));
      }
      if (url.pathname === '/api/workspace') {
        const lock = JSON.parse(await read('sources/lock.json'));
        const [historicalState, pipeline] = await Promise.all([historical('dossiers', { limit: '100' }), historical('status')]);
        return send(200, JSON.stringify({
          lockedSources: lock.sources.length,
          documents: documents.map(([id, title, category, file]) => ({ id, title, category, file })),
          bank: await bankState(bankRoot),
          historical: historicalState,
          historical_pipeline: pipeline,
        }));
      }
      const historicalRoutes = { '/api/historical/status': 'status', '/api/historical/lookup': 'lookup', '/api/historical/relations': 'relations', '/api/historical/build-dossier': 'dossier', '/api/historical/dossiers': 'dossiers' };
      if (historicalRoutes[url.pathname]) return sendHistorical(historicalRoutes[url.pathname], Object.fromEntries(url.searchParams));
      if (url.pathname.startsWith('/api/historical/dossier/')) {
        let id;
        try { id = decodeURIComponent(url.pathname.slice('/api/historical/dossier/'.length)); }
        catch { return send(400, '{"enabled":false,"error":"invalid_query"}'); }
        if (!id || id.length > 240) return send(404, '{"error":"Dossier not available"}');
        return sendHistorical('detail', { ...Object.fromEntries(url.searchParams), id });
      }
      if (url.pathname === '/api/bank') return send(200, JSON.stringify(await bankState(bankRoot)));
      if (url.pathname === '/api/bank/search') return send(200, JSON.stringify(await bankSearch(bankRoot, url.searchParams.get('q') || '')));
      if (url.pathname.startsWith('/api/bank/record/')) {
        if (!bankRoot) return send(404, '{"error":"Knowledge bank is not enabled"}');
        const id = url.pathname.slice('/api/bank/record/'.length);
        if (!/^[0-9a-f-]{36}$/.test(id)) return send(404, '{"error":"Record not available"}');
        const state = await bankState(bankRoot);
        if (!state.records.some(record => record.id === id)) return send(404, '{"error":"Record not available"}');
        const record = JSON.parse(await readBankFile(bankRoot, `snapshots/${state.head.transaction_id}/records/${id}/record.json`));
        let body = null;
        if (record.body_sha256) body = await readBankFile(bankRoot, `snapshots/${state.head.transaction_id}/records/${id}/body.md`);
        const allRecords = [];
        for (const candidate of state.records) {
          allRecords.push(JSON.parse(await readBankFile(bankRoot, `snapshots/${state.head.transaction_id}/records/${candidate.id}/record.json`)));
        }
        const history = await bankHistory(bankRoot, state.head.transaction_id, id);
        return send(200, JSON.stringify({ record, body, links: bankLinks(allRecords, record), history }));
      }
      if (url.pathname.startsWith('/api/document/')) {
        const doc = documents.find(([id]) => url.pathname === `/api/document/${id}`);
        if (!doc) return send(404, '{"error":"Document not available"}');
        return send(200, JSON.stringify({ text: await read(doc[3]) }));
      }
      const assets = { '/favicon.svg': ['assets/brand/icon.svg', 'image/svg+xml'], '/': ['web/index.html', 'text/html'], '/app.js': ['web/app.js', 'text/javascript'], '/library.js': ['web/library.js', 'text/javascript'], '/style.css': ['web/style.css', 'text/css'], '/reading.js': ['web/reading.js', 'text/javascript'], '/reading-i18n.mjs': ['web/reading-i18n.mjs', 'text/javascript'], '/reading-state.mjs': ['web/reading-state.mjs', 'text/javascript'] };
      const asset = assets[url.pathname];
      if (url.pathname === '/reading.css') return send(200, await read('web/reading.css'), 'text/css; charset=utf-8');
      if (!asset) return send(404, '{"error":"Not found"}');
      send(200, await read(asset[0]), `${asset[1]}; charset=utf-8`);
    } catch {
      send(500, '{"error":"Project file could not be read"}');
    }
  });
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const server = createServer();
  server.on('error', error => { console.error(error.message); process.exitCode = 1; });
  const port = Number(process.env.PORT || 5187);
  server.listen(port, '127.0.0.1', () => console.log(`JSB lokalni pregled → http://127.0.0.1:${port}`));
}
