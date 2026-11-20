import { execFile } from 'node:child_process';
import path from 'node:path';

export function createReadingBridge(root, options = {}) {
  const python = options.python || path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
  let running = 0;
  let writing = false;
  return async (operation, payload = null) => {
    if (!options.bankRoot) return { enabled: false, passages: [], items: [] };
    if (!['view', 'save'].includes(operation)) return { error: 'invalid_reading_input' };
    if (operation === 'save' && !options.writable) return { error: 'reading_read_only' };
    if (running >= 3 || (operation === 'save' && writing)) return { error: 'reading_busy' };
    const args = ['-B', '-m', 'jeb'];
    if (options.synthetic) args.push('--synthetic');
    args.push('reading', operation, '--bank-root', options.bankRoot);
    running++;
    if (operation === 'save') writing = true;
    try {
      return await new Promise(resolve => {
        const child = execFile(python, args, { cwd: root, windowsHide: true, timeout: 30000, maxBuffer: 2 * 1024 * 1024, encoding: 'utf8' }, (error, stdout) => {
          if (stdout && (!error || error.code === 2)) {
            try { return resolve(JSON.parse(stdout)); } catch { /* Return a path-free error. */ }
          }
          resolve({ enabled: false, error: 'reading_unavailable' });
        });
        child.stdin.on('error', () => {});
        child.stdin.end(payload || '');
      });
    } finally {
      running--;
      if (operation === 'save') writing = false;
    }
  };
}

export function readingStatus(result) {
  if (!result.error) return 200;
  if (result.error === 'reading_read_only') return 403;
  if (['revision_conflict', 'stale_view', 'request_id_conflict', 'history_limit'].includes(result.error)) return 409;
  if (['reading_unavailable', 'reading_busy'].includes(result.error)) return 503;
  return 422;
}

export async function boundedBody(req, maximum = 16384) {
  return new Promise((resolve, reject) => {
    let size = 0;
    let chunks = [];
    req.setTimeout(5000, () => req.destroy());
    req.on('data', chunk => {
      size += chunk.length;
      if (size <= maximum) chunks.push(chunk);
      else chunks = [];
    });
    req.on('end', () => { req.setTimeout(0); resolve(size > maximum ? null : Buffer.concat(chunks)); });
    req.on('aborted', () => reject(new Error('Request interrupted')));
    req.on('error', reject);
  });
}
