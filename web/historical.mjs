import { execFile } from 'node:child_process';
import path from 'node:path';

// All semantic validation and hashing live in the installable Python package.
// The loopback viewer only adapts GET requests to read-only CLI operations.
export function createHistoricalBridge(root, options = {}) {
  const names = ['registry', 'index', 'groups', 'dossiers'];
  const paths = Object.fromEntries(names.map(name => [name, options[`${name}Path`] || null]));
  const workspace = options.workspace || null;
  const enabled = Boolean(workspace || Object.values(paths).some(Boolean));
  const python = options.python || path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
  const running = new Map();
  const allowed = new Set(['q', 'work', 'status', 'availability', 'relation', 'id', 'limit', 'offset', 'locator_limit', 'locator_offset']);
  return async (operation, params = {}) => {
    if (!enabled) {
      if (operation === 'status') return { enabled: false, read_only: true, configured: Object.fromEntries(names.map(name => [name, false])), counts: {}, blockers: names.map(layer => ({ layer, reason: 'path_not_configured' })), status: 'blocked' };
      return { enabled: false, proposal_only: true, authoritative: false, releasable: false, results: [], total: 0, entities: [], relations: [], unavailable_layers: names };
    }
    if (Object.entries(params).some(([key, value]) => !allowed.has(key) || typeof value !== 'string' || value.length > 500)) return { enabled: false, error: 'invalid_query' };
    const args = ['-B', '-m', 'jeb', '--root', root];
    if (options.synthetic) args.push('--synthetic');
    args.push('historical', operation);
    if (workspace) args.push('--workspace', workspace);
    for (const name of names) if (paths[name]) args.push(`--${name}`, paths[name]);
    if (operation !== 'status') for (const [key, value] of Object.entries(params)) args.push(`--${key === 'q' ? 'query' : key.replaceAll('_', '-')}=${value}`);
    const key = JSON.stringify(args);
    if (running.has(key)) return running.get(key);
    if (running.size >= 2) return { enabled: false, error: 'historical_busy', retryable: true };
    const result = new Promise(resolve => {
      execFile(python, args, { cwd: root, windowsHide: true, timeout: 30000, maxBuffer: 8 * 1024 * 1024, encoding: 'utf8' }, (error, stdout) => {
        if (stdout && (!error || error.code === 2)) {
          try { return resolve(JSON.parse(stdout)); } catch { /* Use a path-free error below. */ }
        }
        resolve({ enabled: false, error: 'historical_runtime_unavailable', retryable: true });
      });
    });
    running.set(key, result);
    try { return await result; } finally { running.delete(key); }
  };
}

export function historicalHttpStatus(result) {
  if (!result.error) return 200;
  if (result.error === 'not_found') return 404;
  if (result.error === 'invalid_query') return 400;
  if (result.error === 'stale_pipeline_inputs') return 409;
  if (['historical_busy', 'historical_runtime_unavailable'].includes(result.error)) return 503;
  return 422;
}
