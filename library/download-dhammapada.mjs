// Explicit, bounded personal-library acquisition. Never run by the viewer.
import { mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
if (!process.argv.includes('--private')) throw new Error('Use --private for personal research only');
const url = 'https://srednjiput.rs/pali-kanon/sutta-pitaka/khuddaka-nikaya/dhammapada-2/dhammapada/';
const response = await fetch(url, { redirect: 'error', signal: AbortSignal.timeout(30000) });
if (!response.ok || !response.headers.get('content-type')?.includes('text/html')) throw new Error('Unexpected response');
const chunks = []; let size = 0;
for await (const chunk of response.body) {
  size += chunk.length;
  if (size > 2_000_000) throw new Error('Download exceeds limit');
  chunks.push(chunk);
}
const bytes = Buffer.concat(chunks);
const html = bytes.toString('utf8');
if (!html.includes('Samo za besplatnu distribuciju') || !html.includes('Veljačić')) throw new Error('Expected credit/distribution notice missing');
const folder = new URL('private/', import.meta.url);
await mkdir(folder, { recursive: true });
await writeFile(new URL('dhammapada-veljacic.html', folder), bytes, { flag: 'wx' });
const receipt = { book_id: 'book-067', source_url: url, retrieved_on: '2026-11-14',
  file: 'library/private/dhammapada-veljacic.html', bytes: size,
  sha256: createHash('sha256').update(bytes).digest('hex'),
  media_type: 'text/html', translator: 'Čedomil Veljačić',
  provider_distribution_notice: 'Samo za besplatnu distribuciju, kao dar Dhamme',
  use: 'private_personal_research_only', corpus_admitted: false, publication_cleared: false,
  limitations: 'Unchanged full HTML includes site navigation. No textual collation, best-translation assessment or independent rights clearance. Keep the source credit and distribution conditions.' };
await writeFile(new URL('research/downloads.json', import.meta.url), JSON.stringify([receipt], null, 2) + '\n', { flag: 'wx' });
console.log(JSON.stringify(receipt));
