// Bounded retrieval of institutional research evidence, not a library/corpus import.
import { mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
if (!process.argv.includes('--private')) throw new Error('Explicit --private research opt-in required');
const url = 'https://www.zenskestudije.org.rs/pdf/knjige/feministicka_teologija.pdf';
const response = await fetch(url, { redirect: 'error', signal: AbortSignal.timeout(60000) });
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const chunks = []; let bytes = 0;
for await (const chunk of response.body) {
  bytes += chunk.length;
  if (bytes > 25_000_000) throw new Error('Evidence exceeds 25 MB limit');
  chunks.push(chunk);
}
const body = Buffer.concat(chunks);
if (body.subarray(0, 5).toString() !== '%PDF-') throw new Error('Not a PDF');
await mkdir(new URL('../private/evidence/', import.meta.url), { recursive: true });
await writeFile(new URL('../private/evidence/feministicka-teologija.pdf', import.meta.url), body, { flag: 'wx' });
const receipt = { url, retrieved_on: '2026-11-14', bytes,
  sha256: createHash('sha256').update(body).digest('hex'),
  file: 'library/private/evidence/feministicka-teologija.pdf',
  purpose: 'Inspect anthology metadata and Pirkei Avot section, not a selected full-work acquisition',
  access_basis: 'Public PDF served by the institutional host; private inspection only, no independent republication clearance',
  corpus_admitted: false, publication_cleared: false };
await writeFile(new URL('batch-02-evidence.json', import.meta.url), JSON.stringify(receipt, null, 2) + '\n', { flag: 'wx' });
console.log(JSON.stringify(receipt));
