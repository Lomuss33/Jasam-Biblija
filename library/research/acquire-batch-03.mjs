// Explicit, bounded personal-library/research downloads from named primary hosts.
import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
if (!process.argv.includes('--private')) throw new Error('Explicit --private required');
const targets = [
  { id: 'yoga-kotarac', url: 'https://hr.mihailokotarac.com/wp-content/uploads/2025/01/Mihailo-Kotarac-Patanjali-Joga-sutre-Suvremeno-citanje.pdf',
    file: 'library/private/yoga-kotarac-2024.pdf', purpose: 'personal_library_modern_interpretation', book_id: 'book-047' },
  { id: 'upanisade-sample', url: 'https://babun.net/slike/knjige/Upanishade.pdf',
    file: 'library/private/evidence/upanisade-babun-2020-sample.pdf', purpose: 'publisher_preview_metadata_and_contents_only' },
  { id: 'yoga-kotarac-sr', url: 'https://mihailokotarac.com/wp-content/uploads/Patandjali-Joga-sutre-Mihailo-Kotarac.pdf',
    file: 'library/private/yoga-kotarac-sr-2025.pdf', purpose: 'personal_library_modern_interpretation_alternative_not_replacement', book_id: 'book-047' },
];
const receipts = [];
for (const target of targets) {
  try {
  const response = await fetch(target.url, { redirect: 'error', signal: AbortSignal.timeout(45000) });
  if (!response.ok) throw new Error(`${target.id}: HTTP ${response.status}`);
  const chunks = []; let bytes = 0;
  for await (const chunk of response.body) {
    bytes += chunk.length;
    if (bytes > 10_000_000) throw new Error('Download exceeds 10 MB limit');
    chunks.push(chunk);
  }
  const payload = Buffer.concat(chunks);
  if (payload.subarray(0, 5).toString() !== '%PDF-') throw new Error('Unexpected non-PDF response');
  const destination = new URL('../../' + target.file, import.meta.url);
  await mkdir(new URL('./', destination), { recursive: true });
  // Idempotent only for the same bytes; changed evidence is never silently replaced.
  try { await writeFile(destination, payload, { flag: 'wx' }); }
  catch (error) {
    if (error.code !== 'EEXIST' || !(await readFile(destination)).equals(payload)) throw error;
  }
  receipts.push({ ...target, retrieved_on: '2026-11-14', bytes,
    sha256: createHash('sha256').update(payload).digest('hex'),
    corpus_admitted: false, publication_cleared: false,
    status: 'downloaded', notice_check: 'Pending direct inspection of retained PDF; retrieval is not a license assessment' });
  } catch (error) {
    receipts.push({ id: target.id, url: target.url, purpose: target.purpose,
      status: 'failed', error: error.cause?.code || error.code || error.message,
      retrieved_on: '2026-11-14', corpus_admitted: false, publication_cleared: false });
  }
}
await writeFile(new URL('batch-03-acquisition.json', import.meta.url), JSON.stringify(receipts, null, 2) + '\n', { flag: 'wx' });
console.log(JSON.stringify(receipts));
