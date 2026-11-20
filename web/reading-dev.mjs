import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { createServer } from './server.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const bankRoot = path.join(root, 'dist/reading-desk-demo');
const python = path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
try {
  if (process.argv.length !== 3 || process.argv[2] !== '--synthetic') throw new Error('Explicit opt-in required: npm run reading:demo -- --synthetic');
  const command = ['-B', '-m', 'jeb', '--synthetic', 'reading', existsSync(bankRoot) ? 'view' : 'demo', '--bank-root', bankRoot];
  const result = await promisify(execFile)(python, command, { cwd: root, windowsHide: true, maxBuffer: 2 * 1024 * 1024 });
  const state = JSON.parse(result.stdout);
  if (state.error) throw new Error('Existing reading workspace failed validation; it has been preserved.');
  const port = Number(process.env.PORT || 5187);
  if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('PORT must be an integer from 1024 to 65535');
  const server = createServer({ readingRoot: bankRoot, readingSynthetic: true, readingWritable: true });
  server.on('error', error => { console.error(error.message); process.exitCode = 1; });
  server.listen(port, '127.0.0.1', () => {
    console.log(`SYNTHETIC reading desk · private notes enabled · http://127.0.0.1:${port}/#desk`);
    console.log('John 9 is a planned topic; invented examples are not scripture. Existing notes are preserved.');
  });
} catch (error) { console.error(error.message); process.exitCode = 2; }
