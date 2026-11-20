const states = {
  saved_private: 'Privatna kopija spremljena',
  online_reading: 'Online čitanje',
  edition_lead: 'Izdanje identificirano',
  online_excerpt: 'Online ulomak',
  contents_lead: 'Sadržaj pronađen · izdanje otvoreno',
  search_needs_review: 'Nalazi čekaju pregled',
  not_searched: 'Čeka pretragu',
};
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function external(url, text) {
  const a = element('a', text, 'source-url');
  try {
    if (new URL(url).protocol !== 'https:') return element('span', 'Nevažeća poveznica');
    a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
  } catch { return element('span', 'Nevažeća poveznica'); }
  return a;
}
const normal = text => text.normalize('NFD').replace(/\p{M}/gu, '').toLocaleLowerCase('hr');
let dataPromise;
export async function renderCollection(main) {
  const page = element('div'); main.replaceChildren(page);
  const heading = element('div', undefined, 'page-heading');
  heading.append(element('p', 'KNJIGE KOJE SKUPLJAŠ', 'eyebrow'), element('h1', 'Tvoja polica znanja.'),
    element('p', 'Pronađi knjigu, provjeri izdanje i nastavi čitati. Izvori i prevodilački krediti ostaju uz svaki nalaz.'));
  page.append(heading);
  const loading = element('p', 'Učitavam biblioteku…'); loading.setAttribute('role', 'status'); page.append(loading);
  let catalog;
  try {
    if (!dataPromise) dataPromise = fetch('/api/library').then(async response => {
      if (!response.ok) throw new Error();
      return response.json();
    }).catch(error => { dataPromise = undefined; throw error; });
    catalog = await dataPromise;
  } catch { loading.textContent = 'Biblioteka nije dostupna. Provjeri lokalni server i osvježi stranicu.'; return; }
  if (!page.isConnected) return;
  loading.remove();
  const books = catalog.books;
  const counts = element('div', undefined, 'library-counts');
  for (const [count, label] of [
    [books.length, 'na tvojoj listi'],
    [books.filter(b => b.findings.length).length, 's pregledanim nalazom'],
    [books.filter(b => b.status === 'saved_private').length, 'privatna kopija'],
  ]) {
    const card = element('div'); card.append(element('strong', String(count)), element('span', label)); counts.append(card);
  }
  page.append(counts);
  const info = element('div', undefined, 'notice');
  const p = element('p', 'Jezični redoslijed: hercegovački/regionalni → bosanski → hrvatski → crnogorski → srpski na latinici. Početna pretraga obuhvaća cijeli popis; najbolji prijevodi i viši prioriteti još nisu uspoređeni za svaku knjigu.');
  info.append(p); page.append(info);
  const controls = element('div', undefined, 'library-controls');
  const searchLabel = element('label', 'Naslov ili autor');
  const search = element('input'); search.type = 'search'; search.placeholder = 'Traži knjigu, autora ili prevodioca…'; searchLabel.append(search);
  const groupLabel = element('label', 'Zbirka');
  const groups = element('select'); groups.append(new Option('Sve zbirke', ''));
  for (const group of new Set(books.map(b => b.group))) groups.append(new Option(group, group));
  groupLabel.append(groups);
  const stateLabel = element('label', 'Dostupnost');
  const status = element('select'); status.append(new Option('Svi statusi', ''));
  for (const [key, label] of Object.entries(states)) status.append(new Option(label, key));
  stateLabel.append(status); controls.append(searchLabel, groupLabel, stateLabel); page.append(controls);
  const count = element('p', '', 'caption'); count.setAttribute('role', 'status'); page.append(count);
  const list = element('div', undefined, 'collection-list'); page.append(list);
  function renderBooks() {
    const query = normal(search.value.trim());
    const shown = books.filter(book => (!groups.value || book.group === groups.value) && (!status.value || book.status === status.value)
      && normal(`${book.request} ${book.group} ${book.findings.map(f => `${f.translator || ''} ${f.edition_title}`).join(' ')}`).includes(query));
    count.textContent = `${shown.length} od ${books.length} stavki · naslovi i atribucije iz tvog popisa; nalazi provjereni 14. 11. 2026.`;
    list.replaceChildren();
    if (!shown.length) { list.append(element('p', 'Nema rezultata za odabrane uvjete. Pokušaj promijeniti pretragu ili filtre.')); return; }
    for (const book of shown) {
      const detail = element('details', undefined, 'collection-book');
      const summary = element('summary');
      const index = element('span', book.id.slice(-3), 'collection-number');
      const title = element('span', undefined, 'collection-title');
      title.append(element('strong', book.title), element('span', book.requested_attribution));
      const state = element('span', states[book.status], `collection-state ${book.findings.length ? 'has-finding' : ''}`);
      summary.append(index, title, state); detail.append(summary);
      const body = element('div', undefined, 'collection-body');
      body.append(element('p', book.group, 'eyebrow'));
      for (const finding of book.findings) body.append(renderFinding(finding));
      if (!book.findings.length) body.append(element('p', 'Početna pretraga je zabilježena. Relevantnost, jezik, izdanje i dopuštenje preuzimanja još nisu potvrđeni. Ovo ne znači da prijevod ne postoji.'));
      const leads = element('details', undefined, 'discovery');
      leads.append(element('summary', 'Tragovi početne pretrage · nisu potvrđena izdanja'));
      const leadBody = element('div'); leads.append(leadBody);
      let loaded = false;
      leads.addEventListener('toggle', async () => {
        if (!leads.open || loaded) return;
        loaded = true; leadBody.textContent = 'Učitavam tragove…';
        try {
          const batches = await Promise.all(book.search_batches.map(async id => {
            const r = await fetch(`/api/library/research/${id}`); if (!r.ok) throw new Error(); return r.json();
          }));
          leadBody.replaceChildren(element('p', 'Rezultati su skupni za četiri upita. Mogu biti nepovezani, na drugom jeziku ili s nepotvrđenim pravima. Nisu preporuke za preuzimanje.'));
          const seen = new Set();
          for (const batch of batches) {
            const query = batch.queries[batch.book_ids.indexOf(book.id)];
            leadBody.append(element('p', `Upit: ${query}`, 'caption'));
            for (const lead of batch.leads) {
              if (seen.has(lead.url)) continue; seen.add(lead.url);
              leadBody.append(external(lead.url, lead.title));
            }
          }
          if (!seen.size) leadBody.append(element('p', 'Nema pohranjenih poveznica u ovom krugu. Potrebna je ciljana bibliografska pretraga.'));
        } catch { loaded = false; leadBody.textContent = 'Tragovi nisu dostupni. Zatvori i ponovo otvori ovaj odjeljak za novi pokušaj.'; }
      });
      body.append(leads); detail.append(body); list.append(detail);
    }
  }
  for (const node of [search, groups, status]) node.addEventListener('input', renderBooks);
  renderBooks();
}
function renderFinding(finding) {
  const section = element('section', undefined, 'finding');
  section.append(element('h3', finding.edition_title));
  const metadata = [finding.language, finding.translator ? `Prijevod: ${finding.translator}` : 'Prevodilac: nije potvrđen', finding.publisher, finding.year].filter(Boolean);
  section.append(element('p', metadata.join(' · ')));
  if (finding.isbn) section.append(element('p', `ISBN: ${finding.isbn}`, 'caption'));
  section.append(element('p', finding.coverage), element('p', finding.rights, 'caption'));
  if (finding.edition_identity_note) section.append(element('p', finding.edition_identity_note, 'caption'));
  if (finding.local_file) section.append(element('p', `Privatna kopija u projektu: ${finding.local_file}. Izvorna datoteka; nije uključena u biblijski korpus ni javni izvoz.`, 'saved-copy'));
  const labels = { online_reading: 'Otvori tekst ili indeks na izvornom webu ↗', online_excerpt: 'Otvori ulomak u izvornom dokumentu ↗', contents_only: 'Otvori pregledani sadržaj · izdanje nepotvrđeno ↗' };
  section.append(external(finding.url, labels[finding.access] || 'Otvori kataloški zapis / izdanje ↗'));
  if (finding.evidence_urls?.length) {
    const evidence = element('details'); evidence.append(element('summary', 'Dokazi za identitet i sadržaj'));
    for (const [index, url] of finding.evidence_urls.entries()) evidence.append(external(url, `Dokaz ${index + 1} ↗`));
    section.append(evidence);
  }
  return section;
}
