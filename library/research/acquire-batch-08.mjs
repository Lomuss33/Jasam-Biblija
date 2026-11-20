// Only the two public downloads linked by Srednji put; never run by the viewer.
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
if (!process.argv.includes('--private')) throw new Error('Explicit --private required');
const receiptPath = new URL('batch-08-acquisition.json', import.meta.url);
try { await readFile(receiptPath); throw new Error('Receipt exists'); }
catch (error) { if (error.code !== 'ENOENT') throw error; }
const receipts = [];
for (const [id, driveId] of [
  ['suttanipata', '1YqfrsWQnJq7FDP1KCLkKX3zObp43Mg1d'],
  ['udana', '1MxRQ63zyU3aeyF7tw2sRWn1qd-bqRbdp'],
]) {
  const source_url = `https://drive.google.com/file/d/${driveId}/view?usp=sharing`;
  const file = `library/private/evidence/${id}-linked-pdf.pdf`;
  try {
    const response = await fetch(`https://drive.google.com/uc?export=download&id=${driveId}`,
      {signal: AbortSignal.timeout(45000)});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const chunks = []; let bytes = 0;
    for await (const chunk of response.body) {
      bytes += chunk.length;
      if (bytes > 20_000_000) throw new Error('Exceeds 20 MB');
      chunks.push(chunk);
    }
    const payload = Buffer.concat(chunks);
    if (payload.subarray(0, 5).toString() !== '%PDF-') throw new Error('Non-PDF response; no login or confirmation bypass');
    await writeFile(new URL('../../' + file, import.meta.url), payload, {flag: 'wx'});
    receipts.push({id, source_url, file, bytes, sha256: createHash('sha256').update(payload).digest('hex'),
      status: 'downloaded_for_inspection', purpose: 'private_evidence_pending_edition_and_notice_check',
      retrieved_on: '2026-11-15', corpus_admitted: false, publication_cleared: false});
  } catch (error) {
    receipts.push({id, source_url, status: 'failed', error: error.cause?.code || error.message,
      retrieved_on: '2026-11-15', corpus_admitted: false, publication_cleared: false});
  }
}
await writeFile(receiptPath, JSON.stringify(receipts, null, 2) + '\n', {flag: 'wx'});
console.log(JSON.stringify(receipts));
