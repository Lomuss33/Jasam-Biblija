// One unchanged, private copy from the translator's own public download link.
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
if (!process.argv.includes('--private')) throw new Error('Explicit --private required');
const source_url = 'https://www.ivantic.info/Moje_knjige/Sankhya_karika_i_Sutra.pdf';
const file = 'library/private/samkhya-antic-2017.pdf';
const receiptFile = new URL('batch-03-samkhya.json', import.meta.url);
try { await readFile(receiptFile); throw new Error('Receipt exists; refusing another acquisition'); }
catch (error) { if (error.code !== 'ENOENT') throw error; }
const response = await fetch(source_url, { redirect: 'error', signal: AbortSignal.timeout(45000) });
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const chunks = [];
let bytes = 0;
for await (const chunk of response.body) {
  bytes += chunk.length;
  if (bytes > 10_000_000) throw new Error('Download exceeds 10 MB limit');
  chunks.push(chunk);
}
const payload = Buffer.concat(chunks);
if (payload.subarray(0, 5).toString() !== '%PDF-') throw new Error('Unexpected response; no access challenge bypass');
await writeFile(new URL('../../' + file, import.meta.url), payload, { flag: 'wx' });
const receipt = {
  book_id: 'book-048', source_url, file, retrieved_on: '2026-11-14', bytes,
  sha256: createHash('sha256').update(payload).digest('hex'), media_type: 'application/pdf',
  translator: 'Ivan Antić', edition_year: 2017,
  use: 'private_personal_research_only', corpus_admitted: false, publication_cleared: false,
  notice_check: 'Pending visual inspection of retained PDF',
};
await writeFile(receiptFile, JSON.stringify(receipt, null, 2) + '\n', { flag: 'wx' });
console.log(JSON.stringify(receipt));
