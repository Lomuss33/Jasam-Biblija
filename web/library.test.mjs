import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const json = async file => JSON.parse(await readFile(new URL(`../library/${file}`, import.meta.url), 'utf8'));

test('every requested title and attribution remains separate, with honest discovery state', async () => {
  const catalog = await json('catalog.json');
  const searches = await json('research/searches.json');
  const source = await readFile(new URL('../library/requested-books.md', import.meta.url), 'utf8');
  const requests = source.split(/\r?\n/).filter(line => line.startsWith('- ')).map(line => line.slice(2));
  assert.equal(requests.length, 291);
  assert.deepEqual(catalog.books.map(b => b.request), requests);
  assert.equal(new Set(catalog.books.map(b => b.id)).size, 291);
  assert.equal(new Set(catalog.books.map(b => b.group)).size, 14);
  assert.equal(catalog.books.filter(b => b.title === 'Haiku').length, 3);
  assert.equal(catalog.scope, 'personal_research_library_not_bible_edition');
  assert.equal(searches.length, 73);
  assert.equal(searches.reduce((count, s) => count + s.queries.length, 0), 291);
  const ids = new Set(catalog.books.map(b => b.id));
  const searchIds = new Set(searches.map(s => s.id));
  for (const search of searches) {
    assert.equal(search.status, 'discovery_only_unreviewed');
    assert.equal(search.book_ids.length, search.queries.length);
    for (const id of search.book_ids) assert.ok(ids.has(id));
    for (const lead of search.leads) {
      assert.equal([...lead.title].some(c => /\p{L}/u.test(c) && !/\p{Script=Latin}/u.test(c)), false);
    }
  }
  for (const book of catalog.books) {
    assert.equal(book.search_batches.length, 1);
    for (const id of book.search_batches) assert.ok(searchIds.has(id));
    if (!book.findings.length) assert.equal(book.status, 'search_needs_review');
    for (const finding of book.findings) {
      assert.equal(finding.book_id, book.id);
      assert.equal(new URL(finding.url).protocol, 'https:');
      assert.equal(finding.quality, 'not_compared');
    }
  }
  const production = JSON.parse(await readFile(new URL('../sources/lock.json', import.meta.url), 'utf8'));
  assert.deepEqual(production.sources, []);
});

test('download receipt retains private scope, translator and distribution limits', async () => {
  const downloads = await json('research/downloads.json');
  const copy = downloads.find(d => d.book_id === 'book-067');
  assert.equal(copy.translator, 'Čedomil Veljačić');
  assert.equal(copy.corpus_admitted, false);
  assert.equal(copy.publication_cleared, false);
  assert.equal(copy.use, 'private_personal_research_only');
  assert.match(copy.provider_distribution_notice, /besplatnu distribuciju/);
  assert.match(copy.sha256, /^[a-f0-9]{64}$/);
  assert.ok(copy.bytes > 0);
  const catalog = await json('catalog.json');
  const saved = catalog.books.flatMap(b => b.findings.filter(f => f.local_file));
  assert.equal(downloads.length, saved.length);
  for (const record of downloads) {
    assert.equal(saved.some(f => f.book_id === record.book_id && f.local_file === record.file), true);
    assert.equal(record.corpus_admitted, false);
    assert.equal(record.publication_cleared, false);
    assert.equal(record.use, 'private_personal_research_only');
    assert.match(record.sha256, /^[a-f0-9]{64}$/);
  }
  const samkhya = downloads.find(d => d.book_id === 'book-048');
  assert.match(samkhya.provider_distribution_notice, /bez ikakvih izmena/);
});

test('partial texts and unbound contents never acquire full-edition or saved-copy status', async () => {
  const catalog = await json('catalog.json');
  const avot = catalog.books.find(b => b.id === 'book-017');
  assert.equal(avot.status, 'online_excerpt');
  assert.equal(avot.findings.some(f => f.local_file), false);
  const asclepius = catalog.books.find(b => b.id === 'book-032');
  assert.equal(asclepius.status, 'contents_lead');
  assert.match(asclepius.findings[0].coverage, /21–29/);
  assert.equal(asclepius.findings[0].translator, null);
  const ids = catalog.books.flatMap(b => b.findings.map(f => f.id));
  assert.equal(ids.length, new Set(ids).size);
  const evidence = await json('research/batch-02-evidence.json');
  assert.equal(evidence.publication_cleared, false);
  assert.equal(evidence.corpus_admitted, false);
});

test('publisher previews and failed downloads do not become saved whole works', async () => {
  const catalog = await json('catalog.json');
  for (const id of ['book-035', 'book-036', 'book-043']) {
    const book = catalog.books.find(b => b.id === id);
    assert.equal(book.status, 'edition_lead');
    assert.match(book.findings[0].coverage, /izbor, ne cijelo djelo/);
    assert.equal(book.findings.some(f => f.local_file), false);
  }
  const mundaka = catalog.books.find(b => b.id === 'book-040');
  assert.equal(mundaka.status, 'contents_lead');
  assert.match(mundaka.findings[0].edition_identity_note, /identitet.*ostaje otvoren/);
  const yoga = catalog.books.find(b => b.id === 'book-047');
  const kotarac = yoga.findings.find(f => f.translator.startsWith('Iva'));
  assert.equal(kotarac.local_file, undefined);
  assert.equal(kotarac.access, 'catalogue_or_purchase');
  const attempts = await json('research/batch-03-acquisition.json');
  assert.equal(attempts.find(r => r.id === 'yoga-kotarac').error, 'ERR_TLS_CERT_ALTNAME_INVALID');
  assert.equal(attempts.find(r => r.id === 'upanisade-sample').purpose, 'publisher_preview_metadata_and_contents_only');
});
