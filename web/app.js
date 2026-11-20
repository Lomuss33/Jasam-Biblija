import { renderCollection } from '/library.js';
import { renderReadingDesk } from '/reading.js';
const main = document.querySelector('main');
const dialog = document.querySelector('#reader');
const pages = { desk: 'Stol za čitanje', collection: 'Moja biblioteka', overview: 'Pregled', sources: 'Izvori i istraživanje', language: 'Jezik i stil', library: 'Dokumenti', knowledge: 'Baza znanja', historical: 'Entiteti i svjetovi' };
let workspace;
let request = 0;
const books = [['GEN', 'Postanak', '1:1–5'], ['MAT', 'Matej', '5:1–12'], ['MRK', 'Marko', '1:1–8'], ['LUK', 'Luka', '17:20–21'], ['JHN', 'Ivan', '1:1–5']];
const button = (id, label) => `<button class="doc-link" data-doc="${id}">${label}<span aria-hidden="true">↗</span></button>`;
const heading = (label, title, description) => `<div class="page-heading"><p class="eyebrow">${label}</p><h1>${title}</h1><p>${description}</p></div>`;
const notice = () => `<div class="notice"><span class="notice-mark">!</span><div><strong>${workspace.lockedSources === 0 ? 'Stvarni korpus još nije odobren.' : 'Status prava provjeri u uredničkom alatu.'}</strong><p>Privatno istraživanje i sintetički primjeri ne predstavljaju prihvaćeni tekst. Ovaj pregled ne dodjeljuje odobrenja.</p></div></div>`;

function render() {
  const route = location.hash.slice(1).split('?')[0];
  const page = Object.hasOwn(pages, route) ? route : 'desk';
  main.classList.toggle('reading-main', page === 'desk');
  document.body.classList.toggle('reading-mode', page === 'desk');
  document.querySelector('#breadcrumb').textContent = pages[page];
  document.querySelectorAll('[data-page]').forEach(a => {
    if (a.dataset.page === page) a.setAttribute('aria-current', 'page');
    else a.removeAttribute('aria-current');
  });
  if (page === 'desk') {
    renderReadingDesk(main);
  } else if (page === 'collection') {
    renderCollection(main);
  } else if (page === 'overview') {
    main.innerHTML = heading('OD IZVORA DO JASNOG TEKSTA', 'Riječ po riječ.<br>Sačuvaj smisao.', 'Mjesto za orijentaciju, izvore i jezične odluke projekta.') +
      `<div class="stats"><div><span>Odobreni opseg</span><strong>05 <small>knjiga</small></strong></div><div><span>Izvori u produkcijskom locku</span><strong>${workspace.lockedSources.toString().padStart(2, '0')} <small>izvora</small></strong></div><div><span>Trenutna radna etapa</span><strong class="stat-text">Istraživanje</strong></div></div>` + notice() +
      `<section class="next-panel"><div><p class="eyebrow">NASTAVI GDJE SMO STALI</p><h2>Usporedi svjedoke.<br>Pripremi povezanu cjelinu.</h2><p>Sljedeći sadržajni korak zabilježen je u radnom planu. Pregledaj tačne stranice, jezične primjere i preostala otvorena pitanja.</p></div><div class="next-links">${button('next', 'Otvori aktualni plan')}${button('entries', 'Posljednji jezični nalazi')}${button('comparison', 'Usporedba izvora')}</div></section>
      <section><div class="section-title"><h2>Pet knjiga, jedan okvir</h2><span>PLANIRANI PILOT-ODLOMCI</span></div><div class="books">${books.map(([id, name, pilot], i) => `<div class="book"><span class="book-number">0${i + 1} / ${id}</span><h3>${name}</h3><p>${pilot}</p><span class="book-state">Planirani pilot</span></div>`).join('')}</div><p class="caption">Oznake odlomaka su plan rada. Tekst i pokrivenost korpusa nisu učitani u ovaj pregled.</p></section>`;
  } else if (page === 'sources') {
    main.innerHTML = heading('PORIJEKLO PRIJE OBRADE', 'Izvori i istraživanje', 'Izdanje, prevodilački kredit i digitalni put ostaju vidljivi i odvojeni.') + notice() +
      `<div class="source-list"><section class="source-card"><span class="tag">ISTRAŽIVAČKI NALAZ · 31. 10. 2026.</span><h2>Pešta, 1868.</h2><p>Identificirano latinično izdanje. Privatni GEN 1:1–5 pilot je pripremljen za pregled. Potpunost pet knjiga i uvjeti upotrebe ostaju otvoreni.</p>${button('comparison', 'Pogledaj usporedbu i ograničenja')}</section><section class="source-card"><span class="tag">DIGITALNI KANDIDATI · ISTRAŽIVANJE</span><h2>CrossWire i eBible</h2><p>Zabilježene su praznine u digitalnom porijeklu i povijesti izmjena. Kasniji uvodi, naslovi i druge komponente traže zaseban pregled.</p>${button('comparison', 'Pročitaj konkretne nalaze')}</section><section class="source-card"><span class="tag">USPOREDNI HISTORIJSKI SVJEDOK</span><h2>Škarić, 1858.</h2><p>Pregledani su naslov i početni listovi Postanka. Zabilježene razlike služe usporedbi; ne postaju automatske zamjene.</p>${button('entries', 'Otvori usporedne primjere')}</section></div><p class="caption">Sažeci opisuju dokumentirane nalaze od 31. 10. 2026.; nisu automatizirana procjena prihvatljivosti izvora.</p>${button('rights', 'Pravila prava i korištenja')}`;
  } else if (page === 'language') {
    main.innerHTML = heading('LOKALNI GLAS, RAZUMLJIVA CJELINA', 'Jezik koji čuva smisao.', 'Hercegovački izraz s širokom bosanskohercegovačkom razumljivošću.') +
      `<section class="literal-panel"><p class="eyebrow">SAČUVANI VLASNIKOVI OBLICI</p><div class="literals"><span>svjet</span><span>vrjeme</span><span>covik</span><span>razumit</span></div><p>Čuvaju se doslovno. Iz njih se ne izvode nova pravila ni sklonidbe.</p></section><div class="two-col"><section class="source-card"><span class="tag">SMJER JE ZAPISAN</span><h2>Jedan glas, povezani paketi</h2><p>Riječi i iznimke pripremamo zajedno s dokazima i nesigurnostima. Jezični smjer ne predstavlja odobrenje konačnog teksta.</p>${button('direction', 'Pročitaj vlasnikov smjer')}</section><section class="source-card"><span class="tag">PITANJA ZA DALJNJI RAD</span><h2>Primjer prije pravila</h2><p>Hljeb/kruh, oblici riječi i značenjske razlike provjeravaju se u odlomku. Historijski svjedoci ostaju zasebni.</p>${button('entries', 'Pregledaj istražene natuknice')}</section></div>${button('language', 'Otvori cijeli jezični vodič')}`;
  } else if (page === 'knowledge') {
    renderKnowledge();
  } else if (page === 'historical') {
    renderHistorical();
  } else {
    main.innerHTML = heading('RADNA POLICA', 'Dokumenti pri ruci.', 'Pretraži odabranu projektnu dokumentaciju po naslovu ili sadržaju.') +
      `<label class="search-label" for="search">Pretraži dokumente</label><input id="search" type="search" placeholder="Npr. jezik, izvor, pregled…" autocomplete="off"><p id="search-state" class="caption" role="status"></p><div id="doc-list" class="doc-list"></div>`;
    setupSearch();
  }
}
async function renderHistorical() {
  main.innerHTML = heading('HISTORIJSKI TEKSTOVI', 'Likovi, mjesta i svjetovi.', 'Pretraži pojave u dostupnim izdanjima i otvori njihov dossier s porijeklom i lokatorima.') +
    '<div id="historical-root"><div class="stats historical-stats"><div><span>Artefakti</span><strong id="historical-artifacts">—</strong></div><div><span>Kandidati</span><strong id="historical-candidates">—</strong></div><div><span>Dossier prijedlozi</span><strong id="historical-total">—</strong></div><div><span>Čekaju obradu / pregled</span><strong id="historical-pending">—</strong></div></div><p id="historical-pipeline" class="caption" role="status"></p><div class="historical-controls"><label>Lik, mjesto ili pojam<input id="historical-search" type="search" placeholder="Npr. Luma u sintetičkom demu" autocomplete="off"></label><label>Status<select id="historical-status"><option value="">Svi</option><option value="proposed">Prijedlozi</option></select></label><label>Dostupnost<select id="historical-availability"><option value="">Sve</option><option value="private">Privatni artefakt</option><option value="discovered">Pronađen izvor</option></select></label><label>Djelo<input id="historical-work" type="search" placeholder="Npr. MAT" autocomplete="off"></label></div><div class="historical-actions"><button id="historical-build" type="button">Otvori dossier za upit</button><button id="historical-refresh" type="button">Osvježi status</button></div><p id="historical-state" class="caption" role="status"></p><div id="historical-list" class="doc-list"></div><div class="historical-actions"><button id="historical-prev" type="button" disabled>Prethodna stranica</button><button id="historical-next" type="button" disabled>Sljedeća stranica</button></div></div>';
  const root = document.querySelector('#historical-root');
  const list = root.querySelector('#historical-list');
  const state = root.querySelector('#historical-state');
  const controls = ['historical-search', 'historical-status', 'historical-availability', 'historical-work'].map(id => root.querySelector(`#${id}`));
  const previous = root.querySelector('#historical-prev');
  const next = root.querySelector('#historical-next');
  let offset = 0, sequence = 0, timer, controller;
  const params = () => new URLSearchParams({ q: controls[0].value, status: controls[1].value, availability: controls[2].value, work: controls[3].value, limit: '50', offset: String(offset) });
  const showPipeline = pipeline => {
    root.querySelector('#historical-artifacts').textContent = pipeline.counts?.registry?.artifacts ?? '—';
    root.querySelector('#historical-candidates').textContent = pipeline.counts?.index?.candidates ?? '—';
    root.querySelector('#historical-total').textContent = pipeline.counts?.dossiers?.dossiers ?? '—';
    root.querySelector('#historical-pending').textContent = pipeline.counts?.index?.pending ?? '—';
    const queue = pipeline.pipeline?.queue;
    const progress = queue ? `Dovršeno: ${queue.complete} · Na redu: ${queue.queued + queue.processing} · Čeka izvor: ${queue.pending} · Treba pregled: ${queue.needs_review}.` : '';
    const blockers = (pipeline.blockers || []).map(item => `${item.layer}: ${item.reason}`).join(' · ');
    root.querySelector('#historical-pipeline').textContent = pipeline.error ? `Status trenutno nije dostupan: ${pipeline.error}` : `${pipeline.synthetic ? 'SINTETIČKI DEMO · UNRELEASABLE. ' : ''}${progress} ${blockers || 'Slojevi su usklađeni.'}`;
  };
  const renderDossiers = result => {
    list.replaceChildren();
    previous.disabled = offset === 0;
    next.disabled = !result.truncated;
    if (result.error || !result.enabled) {
      state.textContent = result.error ? `Podaci trenutno nisu dostupni: ${result.error}` : 'Uključi lokalni workspace preko JEB_HISTORICAL_WORKSPACE; za sintetički demo postavi i JEB_HISTORICAL_SYNTHETIC=1.';
      next.disabled = true;
      return;
    }
    state.textContent = result.total ? `${offset + 1}–${offset + result.results.length} od ${result.total} prijedloga` : 'Nema pronađenih prijedloga za ovaj upit.';
    for (const dossier of result.results) {
      const button = document.createElement('button');
      button.className = 'library-item'; button.dataset.historicalDossier = dossier.id;
      const count = document.createElement('span'); count.textContent = `${dossier.candidate_count} pojava · prijedlog`;
      const title = document.createElement('strong'); title.textContent = `${dossier.surface_variants.join(', ')} · ${dossier.works.map(work => work.title || work.id).join(', ')}`;
      const arrow = document.createElement('span'); arrow.textContent = '↗'; arrow.setAttribute('aria-hidden', 'true');
      button.append(count, title, arrow); list.append(button);
    }
  };
  const load = async () => {
    const current = ++sequence;
    controller?.abort(); controller = new AbortController();
    state.textContent = 'Pretražujem…';
    try {
      const response = await fetch(`/api/historical/dossiers?${params()}`, { signal: controller.signal });
      const result = await response.json();
      if (current === sequence && root.isConnected) renderDossiers(result);
    } catch (error) { if (error.name !== 'AbortError' && root.isConnected && current === sequence) state.textContent = 'Pretraga trenutno nije dostupna.'; }
  };
  controls.forEach(control => control.addEventListener(control.tagName === 'SELECT' ? 'change' : 'input', () => {
    offset = 0; clearTimeout(timer); timer = setTimeout(() => { if (root.isConnected) load(); }, 300);
  }));
  previous.addEventListener('click', () => { offset = Math.max(0, offset - 50); load(); });
  next.addEventListener('click', () => { offset += 50; load(); });
  root.querySelector('#historical-refresh').addEventListener('click', async () => {
    try {
      const response = await fetch('/api/historical/status');
      const pipeline = await response.json();
      if (!root.isConnected) return;
      workspace.historical_pipeline = pipeline; showPipeline(pipeline); await load();
    } catch { if (root.isConnected) state.textContent = 'Status trenutno nije dostupan.'; }
  });
  const open = async (url, title, combined) => {
    const current = ++request;
    document.querySelector('#reader-title').textContent = title; showText('Učitavam dossier…'); dialog.showModal();
    try {
      const result = await (await fetch(url)).json();
      if (current !== request || !dialog.open) return;
      showText(result.error ? `Dossier trenutno nije dostupan: ${result.error}` : combined ? combinedDossierText(result) : historicalDetailText(result));
    } catch { if (current === request && dialog.open) showText('Dossier trenutno nije dostupan.'); }
  };
  list.addEventListener('click', event => {
    const item = event.target.closest('[data-historical-dossier]');
    if (item) open(`/api/historical/dossier/${encodeURIComponent(item.dataset.historicalDossier)}`, 'Dossier prijedlog', false);
  });
  root.querySelector('#historical-build').addEventListener('click', () => {
    if (!controls[0].value.trim() && !controls[3].value.trim()) { state.textContent = 'Upiši lik, mjesto, pojam ili djelo za dossier.'; controls[0].focus(); return; }
    const query = params(); query.delete('offset'); query.set('limit', '20'); query.set('locator_limit', '10');
    open(`/api/historical/build-dossier?${query}`, `Dossier · ${controls[0].value || controls[3].value}`, true);
  });
  showPipeline(workspace.historical_pipeline || {});
  await load();
}
function historicalDetailText(dossier) {
  const lines = [`# ${dossier.surface_variants.join(', ')}`, `Status: ${dossier.status} · ${dossier.candidate_count} pojava`, '', '## Izdanja i izvori'];
  if (dossier.synthetic) lines.splice(2, 0, 'SINTETIČKI DEMO · UNRELEASABLE');
  for (const source of dossier.sources || []) {
    lines.push(`- ${source.work_title || source.work_id || 'nepoznato'} · ${source.edition_title || source.edition_id || 'izdanje nedostupno'} · ${source.artifact_status}`);
    if (source.contributors?.length) lines.push(`  Krediti: ${source.contributors.join(', ')}`);
    if (source.source_sha256) lines.push(`  Izvor SHA-256: ${source.source_sha256}`);
  }
  lines.push('', '## Lokatori');
  for (const locator of dossier.locators || []) lines.push(`- ${locator.exact} · ${locator.projection} · znakovi ${locator.start}–${locator.end} · ${locator.artifact_id}`);
  if (dossier.locators_truncated) lines.push(`Prikazano ${dossier.locators.length} od ${dossier.locators_total} lokatora. API podržava locator_offset za nastavak.`);
  return lines.join('\n');
}
function combinedDossierText(value) {
  const lines = ['# Dossier prijedlog', `Upit: ${value.query || value.work}`, `Pronađeno: ${value.entities_total} grupa pojava · ${value.works_total} djela · ${value.relations_total} relacija`];
  if (value.synthetic) lines.push('SINTETIČKI DEMO · UNRELEASABLE');
  for (const dossier of value.entities || []) lines.push('', historicalDetailText(dossier));
  lines.push('', '## Relacije u kontekstu djela');
  for (const relation of value.relations || []) lines.push(`- ${relation.from_title || relation.from_id} → ${relation.relation} → ${relation.to_title || relation.to_id} · ${relation.status}`);
  if (value.truncated) lines.push('Rezultat ima dodatne stranice; API podržava offset.');
  return lines.join('\n');
}
async function renderKnowledge() {
  main.innerHTML = heading('OSOBNA BAZA', 'Znanje na jednom mjestu.', 'Pregledaj spremljene zapise i otvori njihove izvore, tvrdnje i dokaze.') + '<div id="knowledge-root"><p class="caption">Učitavam bazu…</p></div>';
  const root = document.querySelector('#knowledge-root');
  if (!workspace.bank?.enabled) { root.innerHTML = '<div class="notice"><span class="notice-mark">!</span><div><strong>Baza nije uključena.</strong><p>Pokreni lokalni server s JEB_BANK_ROOT putanjom do privatne baze.</p></div></div>'; return; }
  const records = workspace.bank.records;
  root.innerHTML = `<div class="stats"><div><span>Zapisi</span><strong>${records.length}</strong></div><div><span>Format</span><strong class="stat-text">${workspace.bank.workspace.schema_version}</strong></div><div><span>Način rada</span><strong class="stat-text">Samo čitanje</strong></div></div><label class="search-label" for="knowledge-search">Pretraži bazu</label><input id="knowledge-search" type="search" placeholder="Npr. Aleksandar, izvor, tvrdnja…" autocomplete="off"><label class="search-label" for="knowledge-kind">Prikaži tip zapisa</label><select id="knowledge-kind"><option value="">Svi tipovi</option><option value="entity">Entity</option><option value="source">Source</option><option value="article">Article</option><option value="claim">Claim</option><option value="evidence">Evidence</option></select><p id="knowledge-state" class="caption"></p><div id="knowledge-list" class="doc-list"></div>`;
  const list = document.querySelector('#knowledge-list'); const state = document.querySelector('#knowledge-state'); const search = document.querySelector('#knowledge-search'); const kind = document.querySelector('#knowledge-kind');
  const renderRecords = items => { list.replaceChildren(); state.textContent = `${items.length} zapisa · ${workspace.bank.workspace.title}`; for (const record of items) { const button = document.createElement('button'); button.className = 'library-item'; button.dataset.bankRecord = record.id; const kind = document.createElement('span'); kind.textContent = record.kind; const title = document.createElement('strong'); title.textContent = record.title; const arrow = document.createElement('span'); arrow.textContent = '↗'; button.append(kind, title, arrow); list.append(button); } };
  renderRecords(records);
  let searchSequence = 0;
  const applyKind = items => kind.value ? items.filter(record => record.kind === kind.value) : items;
  search.addEventListener('input', async () => { const sequence = ++searchSequence; const response = await fetch(`/api/bank/search?q=${encodeURIComponent(search.value)}`); if (!response.ok || sequence !== searchSequence) return; const result = await response.json(); renderRecords(applyKind(result.results)); });
  kind.addEventListener('change', async () => { const response = await fetch(`/api/bank/search?q=${encodeURIComponent(search.value)}`); if (!response.ok) return; const result = await response.json(); renderRecords(applyKind(result.results)); });
  const openBankRecord = async id => { const response = await fetch(`/api/bank/record/${id}`); if (!response.ok) return; const value = await response.json(); document.querySelector('#reader-title').textContent = value.record.title; showText(bankDetailText(value)); renderBankLinks(value); dialog.showModal(); };
  list.addEventListener('click', async event => { const button = event.target.closest('[data-bank-record]'); if (!button) return; await openBankRecord(button.dataset.bankRecord); });
  document.querySelector('#contents').onclick = async event => { const link = event.target.closest('[data-bank-related]'); if (!link) return; event.preventDefault(); await openBankRecord(link.dataset.bankRelated); };
}
function renderBankLinks(value) {
  const contents = document.querySelector('#contents');
  const related = [];
  if (value.links?.subject) related.push(['Predmet', value.links.subject]);
  if (value.links?.claim) related.push(['Tvrdnja', value.links.claim]);
  if (value.links?.source) related.push(['Izvor', value.links.source]);
  for (const evidence of value.links?.evidence || []) related.push([`Dokaz · ${evidence.relation}`, { id: evidence.id, title: evidence.title, kind: 'evidence' }]);
  if (!related.length) return;
  const heading = document.createElement('strong'); heading.textContent = 'Povezani zapisi'; contents.prepend(heading);
  for (const [label, target] of related) { const link = document.createElement('a'); link.href = '#'; link.dataset.bankRelated = target.id; link.textContent = `${label}: ${target.title} [${target.kind}]`; contents.append(link); }
}
function bankDetailText(value) {
  const { record, body, links } = value;
  const lines = [
    `Vrsta: ${record.kind}`,
    `Stanje obrade: ${record.processing_state}`,
    `Vidljivost: ${record.visibility}`,
    `Revizija: ${record.revision_id}`,
  ];
  if (value.history?.length) {
    lines.push('', `Povijest revizija (${value.history.length}):`);
    for (const revision of value.history) lines.push(`- ${revision.revision_id} · ${revision.revised_at} · ${revision.reason}`);
  }
  const ref = (label, target) => {
    if (!target) return `${label}: nedostupno`;
    const status = target.is_current_revision ? 'aktualna revizija' : `povijesna revizija; aktualna je ${target.current_revision_id}`;
    return `${label}: ${target.title} [${target.kind}] — ${status}`;
  };
  if (record.kind === 'claim') {
    lines.push('', 'Tvrdnja:', record.data.statement, `Kategorija: ${record.data.category}`, ref('Predmet', links.subject), '', 'Dokazi:');
    if (!links.evidence?.length) lines.push('Nema spremljenih dokaza za ovu tvrdnju.');
    else for (const evidence of links.evidence) lines.push(`- ${evidence.relation}: ${evidence.title} — ${evidence.applies_to_current_claim ? 'odnosi se na aktualnu tvrdnju' : 'odnosi se na povijesnu reviziju tvrdnje'}`);
  } else if (record.kind === 'evidence') {
    lines.push('', ref('Tvrdnja', links.claim), ref('Izvor', links.source), `Odnos: ${links.relation}`, `Lokator: ${JSON.stringify(links.locator)}`);
  }
  if (body !== null) lines.push('', 'Tijelo zapisa:', body);
  return lines.join('\n');
}
function renderList(docs) {
  const list = document.querySelector('#doc-list');
  if (!list) return;
  list.replaceChildren();
  for (const doc of docs) {
    const b = document.createElement('button');
    b.className = 'library-item'; b.dataset.doc = doc.id;
    const category = document.createElement('span'); category.textContent = doc.category;
    const title = document.createElement('strong'); title.textContent = doc.title;
    const arrow = document.createElement('span'); arrow.textContent = '↗'; arrow.setAttribute('aria-hidden', 'true');
    b.append(category, title, arrow); list.append(b);
  }
  document.querySelector('#search-state').textContent = `${docs.length} dokumenata`;
}
const cache = new Map();
async function getDocument(id) {
  if (!cache.has(id)) cache.set(id, fetch(`/api/document/${id}`).then(async r => {
    if (!r.ok) throw new Error('Dokument trenutno nije dostupan.');
    return (await r.json()).text;
  }).catch(error => { cache.delete(id); throw error; }));
  return cache.get(id);
}
function setupSearch() {
  const search = document.querySelector('#search');
  renderList(workspace.documents);
  let sequence = 0;
  search.addEventListener('input', async () => {
    const current = ++sequence;
    const query = search.value.trim().toLocaleLowerCase('hr');
    if (!query) return renderList(workspace.documents);
    const values = await Promise.all(workspace.documents.map(async doc => {
      try { return { doc, text: await getDocument(doc.id) }; }
      catch { return { doc, text: '', unavailable: true }; }
    }));
    if (current !== sequence || !search.isConnected) return;
    renderList(values.filter(({ doc, text }) => `${doc.title} ${doc.category} ${text}`.toLocaleLowerCase('hr').includes(query)).map(v => v.doc));
    if (values.some(v => v.unavailable)) document.querySelector('#search-state').textContent += ' · Dio sadržaja nije dostupan za pretragu.';
  });
}
// Render repository content as text nodes; raw HTML and Markdown links never execute.
function showText(text) {
  const article = document.querySelector('#document');
  const contents = document.querySelector('#contents');
  article.replaceChildren(); contents.replaceChildren();
  let block = [], pre = false, count = 0;
  const flush = () => {
    if (!block.length) return;
    const node = document.createElement(pre ? 'pre' : 'p');
    node.textContent = block.join('\n'); article.append(node); block = [];
  };
  for (const line of text.split(/\r?\n/)) {
    if (line.startsWith('```')) { flush(); pre = !pre; continue; }
    const match = !pre && /^(#{1,4})\s+(.+)$/.exec(line);
    if (match) {
      flush();
      const h = document.createElement(`h${Math.min(match[1].length + 1, 6)}`);
      h.id = `section-${count++}`; h.textContent = match[2]; article.append(h);
      if (match[1].length <= 2) {
        const link = document.createElement('a'); link.href = `#${h.id}`; link.textContent = match[2];
        link.addEventListener('click', e => { e.preventDefault(); h.scrollIntoView({ block: 'start' }); });
        contents.append(link);
      }
    } else if (!line.trim() && !pre) flush();
    else block.push(line);
  }
  flush();
}
main.addEventListener('click', async e => {
  const selected = e.target.closest('[data-doc]');
  if (!selected) return;
  const doc = workspace.documents.find(d => d.id === selected.dataset.doc);
  if (!doc) return;
  const current = ++request;
  document.querySelector('#reader-title').textContent = doc.title;
  showText('Učitavam dokument…'); dialog.showModal();
  try { const text = await getDocument(doc.id); if (current === request && dialog.open) showText(text); }
  catch (error) { if (current === request && dialog.open) showText(error.message); }
  document.querySelector('.reader-layout').scrollTop = 0;
});
document.querySelector('#close-reader').addEventListener('click', () => dialog.close());
window.addEventListener('hashchange', () => { if (workspace) render(); });
async function start() {
  try {
    const response = await fetch('/api/workspace');
    if (!response.ok) throw new Error();
    workspace = await response.json(); render();
  } catch {
    main.replaceChildren();
    const p = document.createElement('p'); p.setAttribute('role', 'alert');
    p.textContent = 'Projekt se nije mogao učitati. Provjeri lokalni server pa osvježi stranicu.'; main.append(p);
  }
}
start();
