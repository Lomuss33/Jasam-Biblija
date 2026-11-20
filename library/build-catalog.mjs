// Rebuild only the library inventory. Never touches the jeb corpus or source lock.
import { readFile, writeFile } from 'node:fs/promises';
const dir = new URL('./', import.meta.url);
const read = async file => JSON.parse(await readFile(new URL(file, dir), 'utf8'));
const source = await readFile(new URL('requested-books.md', dir), 'utf8');
let group = '';
const books = [];
for (const line of source.split(/\r?\n/)) {
  if (line.startsWith('## ')) group = line.slice(3);
  if (!line.startsWith('- ')) continue;
  const request = line.slice(2);
  const parts = request.split(' — ');
  const attribution = parts.pop();
  books.push({ id: `book-${String(books.length + 1).padStart(3, '0')}`, group,
    title: parts.join(' — '), requested_attribution: attribution, request });
}
let findings = [], searches = [];
try { findings = await read('findings.json'); } catch (e) { if (e.code !== 'ENOENT') throw e; }
try { searches = await read('research/searches.json'); } catch (e) { if (e.code !== 'ENOENT') throw e; }
for (const book of books) {
  book.findings = findings.filter(f => f.book_id === book.id);
  book.search_batches = searches.filter(s => s.book_ids.includes(book.id)).map(s => s.id);
  book.status = book.findings.some(f => f.local_file) ? 'saved_private'
    : book.findings.some(f => f.access === 'online_reading') ? 'online_reading'
    : book.findings.some(f => f.access === 'online_excerpt') ? 'online_excerpt'
    : book.findings.some(f => f.access === 'catalogue_or_purchase') ? 'edition_lead'
    : book.findings.some(f => f.access === 'contents_only') ? 'contents_lead'
    : book.search_batches.length ? 'search_needs_review' : 'not_searched';
}
const ids = new Set(books.map(b => b.id));
for (const f of findings) {
  if (!ids.has(f.book_id)) throw new Error(`Unknown book ${f.book_id}`);
  if (new URL(f.url).protocol !== 'https:') throw new Error('HTTPS source required');
}
const catalog = { version: 1, requested_on: '2026-11-14',
  scope: 'personal_research_library_not_bible_edition',
  language_priority: ['hercegovački/regionalni', 'bosanski', 'hrvatski', 'crnogorski', 'srpski na latinici'],
  quality_note: 'Jezični prioritet nije dokaz kvalitete. Izbor najboljeg prijevoda i viši jezični prioriteti ostaju otvoreni dok se ne usporede konkretna izdanja.',
  books };
await writeFile(new URL('catalog.json', dir), JSON.stringify(catalog, null, 2) + '\n');
console.log(JSON.stringify({ books: books.length, groups: new Set(books.map(b => b.group)).size,
  findings: findings.length, searched: books.filter(b => b.search_batches.length).length }));
