import { copy } from '/reading-i18n.mjs';
import { safeLink, canLocateItem, searchItems, sourceSegments, sameReadingView, draftNeedsRecovery, recoveryNote, browserDraftExport, saveUnconfirmed } from '/reading-state.mjs';

function stored(area, key, fallback) {
  try { return JSON.parse(window[area].getItem(key)) ?? fallback; } catch { return fallback; }
}
function remember(area, key, value) {
  try { value === null ? window[area].removeItem(key) : window[area].setItem(key, JSON.stringify(value)); return true; } catch { return false; }
}
const state = {
  language: stored('localStorage', 'jeb.reading.language', 'bs'), data: null, catalog: [],
  current: null, last: stored('localStorage', 'jeb.reading.last', null), trail: [],
  positions: stored('sessionStorage', 'jeb.reading.positions', {}), query: '', savedKind: 'all', savedLimit: 6,
  draft: null, draftRecovered: false, draftKept: false,
  message: '', saving: false, focus: null, guideOpen: false, inspected: [],
};
if (!copy[state.language]) state.language = 'bs';
let root;
let loadPromise;
const words = () => copy[state.language];
const local = value => value?.[state.language] || value?.en || '';

function node(tag, className = '', text = null) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== null) element.textContent = String(text);
  return element;
}
function action(label, handler, className = 'desk-button') {
  const button = node('button', className, label); button.type = 'button';
  button.addEventListener('click', handler); return button;
}
function para(text, className = '') { return node('p', className, text); }
function group(title, key, open = false) {
  const details = node('details', 'desk-disclosure'); details.dataset.panel = key;
  details.open = state.positions[state.current]?.panels?.includes(key) ?? open;
  details.append(node('summary', '', title)); return details;
}
const fallback = () => ({ id: 'john-9', book: 'JHN', title: { en: 'John 9 · planned study', bs: 'Ivan 9 · planirano istraživanje' }, location: 'JHN 9', source_language: 'en', text: null, source: null, evidence: [], connections: [], interpretations: [], explanation: {
  en: 'Your chosen study: meaning and religious blindness, related stories, Jesus as a character, Pharisees in context, symbolism and evidence. An eligible source and sourced explanations have not been attached yet.',
  bs: 'Odabrano istraživanje: smisao i vjerska sljepoća, povezane priče, Jesus kao lik, Pharisees u kontekstu, simbolika i dokazi. Dopušten izvor i potkrijepljena objašnjenja još nisu priloženi.',
} });
const passages = () => state.data?.enabled ? state.data.passages : [fallback()];
const passage = id => passages().find(p => p.id === id);
const writable = () => Boolean(state.data?.enabled && state.data.writable && !state.data.error);
const needsRecovery = () => draftNeedsRecovery(state.draft, state.data);

function draftKey(kind, recordId = state.draft?.view_ref?.record_id) {
  return recordId ? `jeb.reading.${kind}.${recordId}` : null;
}

function restoreDraft() {
  const recordId = state.data?.view_ref?.record_id;
  if (state.draft || !recordId) return;
  for (const kind of ['pending', 'draft']) {
    const key = draftKey(kind, recordId);
    let value = stored('sessionStorage', key, null);
    const legacyKey = `jeb.reading.${kind}`;
    const legacy = stored('sessionStorage', legacyKey, null);
    if (!value && legacy?.view_ref?.record_id === recordId) {
      value = legacy;
      if (remember('sessionStorage', key, value)) remember('sessionStorage', legacyKey, null);
    }
    if (value?.view_ref?.record_id !== recordId) continue;
    state.draft = value; state.draftKept = !value.uncertain; state.draftRecovered = true;
    break;
  }
}

function capture() {
  if (!root?.isConnected || !state.current) return;
  if (!root.querySelector('.desk-source-scroll') || !root.querySelector('.desk-context-scroll')) return;
  state.positions[state.current] = {
    source: root.querySelector('.desk-source-scroll')?.scrollTop || 0,
    context: root.querySelector('.desk-context-scroll')?.scrollTop || 0,
    panels: [...root.querySelectorAll('details[data-panel][open]')].map(el => el.dataset.panel),
  };
  remember('sessionStorage', 'jeb.reading.positions', state.positions);
}
function go(id, rememberTrail = true) {
  capture();
  if (id && !passage(id)) return;
  if (rememberTrail && state.current && id !== state.current) state.trail.push(state.current);
  state.current = id; state.message = ''; state.focus = null; state.inspected = [];
  if (id) { state.last = id; remember('localStorage', 'jeb.reading.last', id); }
  history.replaceState(null, '', id ? `#desk?passage=${encodeURIComponent(id)}` : '#desk');
  draw();
}
async function readData() {
  const previous = state.data?.view_ref;
  try {
    const response = await fetch('/api/reading/session');
    state.data = await response.json();
  } catch { state.data = { enabled: false, error: 'reading_unavailable' }; }
  if (!sameReadingView(previous, state.data?.view_ref)) { state.focus = null; state.inspected = []; }
  if (state.data.error) state.message = words().unavailable;
}

export async function renderReadingDesk(main) {
  capture();
  root = node('div', 'reading-desk'); main.replaceChildren(root);
  root.append(para(words().loading, 'desk-status'));
  const owned = root;
  if (!loadPromise) {
    loadPromise = Promise.allSettled([
      readData(),
      fetch('/api/library').then(r => r.json()).then(data => { state.catalog = data.books || []; }),
    ]).finally(() => { loadPromise = null; });
  }
  await loadPromise;
  if (!owned.isConnected || root !== owned) return;
  const query = location.hash.split('?')[1] || '';
  const requested = new URLSearchParams(query).get('passage');
  state.current = passage(requested) ? requested : null;
  if (state.draft && state.data?.enabled && state.draft.view_ref?.record_id !== state.data?.view_ref?.record_id) state.draft = null;
  restoreDraft();
  if (state.draft && state.draftRecovered && !state.draft.uncertain) state.message = words().draftRestored;
  state.draftRecovered = false;
  draw();
}

function shell() {
  document.documentElement.lang = state.language;
  document.title = `${words().desk} · JSB`;
  const keys = ['desk', 'collection', 'overview', 'sources', 'language', 'library', 'knowledge', 'historical'];
  keys.forEach((key, i) => {
    const link = document.querySelector(`[data-page="${key}"]`);
    if (link) link.textContent = words().legacy[i];
  });
  document.querySelector('#breadcrumb').textContent = words().desk;
  document.querySelector('.local-label').textContent = words().privateLocal;
  const foot = document.querySelector('.sidebar-foot');
  if (foot) foot.textContent = words().privateLocal;
}
function header() {
  const bar = node('div', 'desk-bar');
  bar.append(action(words().home, () => go(null, false), 'desk-link'));
  if (state.current && state.trail.length) bar.append(action(words().back, () => go(state.trail.pop(), false), 'desk-link'));
  const guide = action(words().guide, () => {
    capture(); state.guideOpen = !state.guideOpen; draw();
    root.querySelector('#reading-guide-toggle')?.focus({ preventScroll: true });
  }, 'desk-link');
  guide.id = 'reading-guide-toggle'; guide.setAttribute('aria-expanded', String(state.guideOpen)); guide.setAttribute('aria-controls', 'reading-guide');
  bar.append(guide);
  const label = node('label', 'desk-language', 'Language / Jezik');
  const select = node('select'); select.id = 'desk-language';
  for (const [code, title] of [['en', 'English'], ['bs', 'Bosanski / hercegovački']]) {
    const option = node('option', '', title); option.value = code; select.append(option);
  }
  select.value = state.language;
  select.addEventListener('change', () => {
    capture(); state.language = select.value; state.message = ''; remember('localStorage', 'jeb.reading.language', state.language); draw();
  });
  label.append(select); bar.append(label); root.append(bar);
  drawGuide();
  if (state.data?.enabled) {
    const banner = node('details', 'desk-prototype');
    banner.append(node('summary', '', words().prototype), para(words().prototypeDetail)); root.append(banner);
  } else root.append(para(state.data?.error ? words().unavailable : words().configure, 'desk-availability'));
}

function drawGuide() {
  const guide = node('section', 'desk-guide'); guide.id = 'reading-guide'; guide.hidden = !state.guideOpen;
  guide.setAttribute('aria-labelledby', 'reading-guide-title');
  const title = node('h2', '', words().guideTitle); title.id = 'reading-guide-title';
  guide.append(title, para(words().guideIntro));
  const steps = node('ol', 'desk-guide-steps');
  for (const [heading, instruction] of words().guideSteps) {
    const item = node('li'); item.append(node('h3', '', heading), para(instruction)); steps.append(item);
  }
  guide.append(steps, para(words().guideSaved, 'desk-muted'));
  if (passage('ledger-entry')?.text) {
    const practice = action(words().guidePractice, () => { state.guideOpen = false; go('ledger-entry'); }, 'desk-button desk-primary');
    practice.id = 'reading-guide-practice'; guide.append(practice);
  } else guide.append(para(words().guideSetup, 'desk-availability'));
  root.append(guide);
}

function draw() {
  if (!root?.isConnected) return;
  const owned = root;
  shell(); root.replaceChildren(); header();
  const status = para(state.message, 'desk-status'); status.id = 'reading-status'; status.setAttribute('role', 'status'); root.append(status);
  if (state.draft && !needsRecovery() && state.draft.passage_id !== state.current) {
    const reminder = node('div', 'desk-draft-reminder'); reminder.append(para(words().draftElsewhere), action(words().returnDraft, () => go(state.draft.passage_id))); root.append(reminder);
  }
  if (state.current && passage(state.current)) drawReading(passage(state.current));
  else { if (needsRecovery()) drawRecovery(root); drawHome(); }
  requestAnimationFrame(() => {
    if (owned !== root || !owned.isConnected || !state.current) return;
    const position = state.positions[state.current];
    if (position) {
      const source = root.querySelector('.desk-source-scroll'), context = root.querySelector('.desk-context-scroll');
      if (source) source.scrollTop = position.source;
      if (context) context.scrollTop = position.context;
    }
    if (state.focus) root.querySelector('[data-proof="true"]')?.scrollIntoView({ block: 'center' });
  });
}

function drawHome() {
  const hero = node('header', 'desk-hero');
  hero.append(para(words().eyebrow, 'desk-eyebrow'), node('h1', '', words().title), para(words().intro));
  const label = node('label', 'desk-search-label', words().search); label.htmlFor = 'desk-search';
  const search = node('input', 'desk-search'); search.id = 'desk-search'; search.type = 'search'; search.placeholder = words().placeholder; search.value = state.query;
  hero.append(label, search);
  if (state.last && passage(state.last)) hero.append(action(`${words().resume}: ${local(passage(state.last).title)}`, () => go(state.last), 'desk-link desk-resume'));
  root.append(hero);
  const results = node('div'); results.id = 'desk-results'; root.append(results);
  function filter() {
    state.query = search.value;
    const term = search.value.trim().toLocaleLowerCase(); results.replaceChildren();
    const available = passages().filter(p => `${p.id} ${p.location} ${p.book} ${JSON.stringify(p.title)} ${JSON.stringify(p.explanation)} ${p.text || ''}`.toLocaleLowerCase().includes(term));
    results.append(node('h2', 'desk-section-title', words().library));
    const grid = node('div', 'desk-book-grid');
    for (const p of available) {
      const card = node('section', 'desk-book-card');
      card.append(para(p.text ? words().invented : words().planned, 'desk-kicker'), node('h3', '', local(p.title)), para(p.location));
      const button = action(words().open, () => go(p.id)); button.dataset.openPassage = p.id; card.append(button); grid.append(card);
    }
    results.append(grid);
    if (!available.length) results.append(para(words().noPassages));
    if (state.data?.enabled) drawSavedWork(results, term, filter);
    const catalogue = state.catalog.filter(book => `${book.title} ${book.requested_attribution} ${JSON.stringify(book.findings || [])}`.toLocaleLowerCase().includes(term)).slice(0, term ? 12 : 6);
    const row = node('div', 'desk-section-heading'); row.append(node('h2', '', words().catalogue));
    const all = node('a', 'desk-link', words().allBooks); all.href = '#collection'; row.append(all); results.append(row);
    const list = node('div', 'desk-catalogue');
    for (const book of catalogue) {
      const card = node('details', 'desk-catalogue-entry'); card.append(node('summary', '', book.title), para(book.requested_attribution || ''), para(words().catalogueOnly, 'desk-muted'));
      if (!book.findings?.length) card.append(para(words().noFinding));
      for (const finding of book.findings || []) {
        card.append(node('h3', '', finding.edition_title), para(finding.translator || ''));
        const href = safeLink(finding.url);
        if (href) { const link = node('a', 'desk-link', words().sourceLink); link.href = href; link.target = '_blank'; link.rel = 'noopener noreferrer'; card.append(link); }
      }
      list.append(card);
    }
    results.append(list);
    if (!catalogue.length) results.append(para(words().noCatalogueResults, 'desk-muted'));
  }
  search.addEventListener('input', () => { state.savedLimit = 6; filter(); }); filter();
}

function drawSavedWork(parent, term, filter) {
  const section = node('section', 'desk-saved-work'); section.id = 'desk-saved-work';
  section.append(node('h2', '', words().savedWork), para(words().savedIntro, 'desk-muted'));
  const controls = node('div', 'desk-saved-controls');
  const label = node('label', '', words().savedFilter); label.htmlFor = 'saved-kind';
  const kind = node('select'); kind.id = 'saved-kind';
  for (const value of ['all', 'note', 'highlight', 'connection']) {
    const option = node('option', '', value === 'all' ? words().allKinds : words()[value]); option.value = value; kind.append(option);
  }
  kind.value = state.savedKind;
  kind.addEventListener('change', () => { state.savedKind = kind.value; state.savedLimit = 6; filter(); root.querySelector('#saved-kind')?.focus({ preventScroll: true }); });
  const items = searchItems(state.data.items || [], passages(), term, state.savedKind);
  const count = para(`${words().savedShown}: ${Math.min(state.savedLimit, items.length)} / ${items.length}`, 'desk-muted');
  controls.append(label, kind, count); section.append(controls);
  const list = node('div', 'desk-saved-list');
  for (const item of items.slice(0, state.savedLimit)) {
    const p = passage(item.passage_id);
    const card = node('article', 'desk-saved-card'); card.dataset.savedItem = item.id;
    card.append(para(words()[item.kind], 'desk-kicker'), node('h3', '', p ? local(p.title) : words().missingPassage));
    if (p) card.append(para(p.location, 'desk-muted'));
    if (item.text) card.append(para(item.text, 'desk-saved-preview'));
    if (item.anchor) card.append(node('blockquote', 'desk-saved-preview', item.anchor.exact));
    if (!item.current_view) card.append(para(words().priorView, 'desk-availability'));
    const actions = node('div', 'desk-saved-actions');
    const open = action(words().openSaved, () => openItem(item), 'desk-link'); open.dataset.jumpItem = item.id; open.disabled = !p; actions.append(open);
    if (canLocateItem(item, p)) {
      const locate = action(words().locate, () => locateItem(item), 'desk-link'); locate.dataset.locateItem = item.id; actions.append(locate);
    }
    card.append(actions); list.append(card);
  }
  section.append(list);
  if (!items.length) section.append(para(state.data.items?.length ? words().noSavedResults : words().noSaved, 'desk-muted'));
  if (items.length > state.savedLimit) {
    const more = action(words().moreSaved, () => { state.savedLimit += 6; filter(); root.querySelector('#saved-more')?.focus({ preventScroll: true }); });
    more.id = 'saved-more'; section.append(more);
  }
  parent.append(section);
}

function reveal(element) {
  if (!element) return;
  element.scrollIntoView({ block: 'center' }); element.focus({ preventScroll: true });
}

function openItem(item) {
  if (!passage(item.passage_id)) return;
  go(item.passage_id);
  requestAnimationFrame(() => reveal(root.querySelector(`[data-item-id="${item.id}"]`)));
}

function locateItem(item) {
  if (!canLocateItem(item, passage(item.passage_id))) return;
  capture();
  if (state.current !== item.passage_id) go(item.passage_id);
  state.focus = item; draw();
}

function selectedAnchor() {
  const selected = window.getSelection();
  const text = root.querySelector('#reading-source-text');
  if (!selected || selected.rangeCount !== 1 || selected.isCollapsed || !text) return null;
  const range = selected.getRangeAt(0);
  if (!text.contains(range.startContainer) || !text.contains(range.endContainer)) return null;
  const before = document.createRange(); before.selectNodeContents(text); before.setEnd(range.startContainer, range.startOffset);
  const exact = range.toString();
  if (!exact || Array.from(exact).length > 2000) return null;
  const start = Array.from(before.toString()).length;
  return { start, end: start + Array.from(exact).length, exact };
}
function setMessage(value) {
  state.message = value;
  const output = root.querySelector('#reading-status'); if (output) output.textContent = value;
}
function begin(kind, item = null) {
  if (state.draft) return setMessage(words().selectScope);
  const anchor = item ? item.anchor : kind === 'note' ? null : selectedAnchor();
  if (kind === 'highlight' && !anchor) return setMessage(words().selectFirst);
  capture();
  const origin = passage(item?.passage_id || state.current);
  state.draft = {
    view_ref: item?.view_ref || state.data.view_ref, request_id: crypto.randomUUID(), kind,
    passage_id: item?.passage_id || state.current, text: item?.text || '', anchor,
    target_id: item?.target_id || (kind === 'connection' ? passages().find(p => p.id !== state.current)?.id : null),
    edit_record_id: item?.id || null, expected_revision: item?.revision_id || null,
    uncertain: false, failure: null,
    source_context: origin ? { title: origin.title, location: origin.location, source_language: origin.source_language,
      source_ref: origin.source_ref, source: origin.source ? { title: origin.source.title, edition: origin.source.edition, creator: origin.source.creator, translator: origin.source.translator || null } : null } : null,
  };
  state.focus = anchor ? { passage_id: state.draft.passage_id, anchor } : null;
  if (state.positions[state.current]) state.positions[state.current].context = 0;
  keepDraft();
  draw(); root.querySelector('#reading-note')?.focus();
}

function keepDraft() {
  const key = draftKey('draft');
  state.draftKept = Boolean(key && state.draft && !state.draft.uncertain && remember('sessionStorage', key, state.draft));
  const status = root?.querySelector('#reading-draft-status');
  if (status) status.textContent = state.draftKept ? words().draftKept : words().draftUnsaved;
}

function clearDraft() {
  for (const kind of ['draft', 'pending']) { const key = draftKey(kind); if (key) remember('sessionStorage', key, null); }
  state.draft = null; state.draftKept = false; state.focus = null;
}

function canRecoverHere() {
  return writable() && state.draft?.view_ref?.record_id === state.data?.view_ref?.record_id;
}

function canSaveRecovery() {
  const draft = state.draft, recovery = draft?.recovery;
  if (!recovery || state.saving || draft.uncertain || !canRecoverHere() || recovery.status === 'saved') return false;
  return recovery.status === 'uncertain' || (sameReadingView(recovery.payload.view_ref, state.data.view_ref) && Boolean(passage(recovery.payload.passage_id)) && Boolean(recovery.payload.text.trim()));
}

function prepareRecovery() {
  if (!needsRecovery() || state.saving || state.draft.uncertain || !canRecoverHere() || state.draft.recovery) return;
  capture();
  state.draft.recovery = { status: 'draft', error: null, saved_id: null,
    payload: recoveryNote(state.draft, state.data.view_ref, passage(state.draft.passage_id) ? state.draft.passage_id : '', crypto.randomUUID()) };
  keepDraft(); draw(); requestAnimationFrame(() => root.querySelector('#reading-recovery-text')?.focus());
}

function refreshRecoveryDestination() {
  const recovery = state.draft?.recovery;
  if (!recovery || state.saving || state.draft.uncertain || !canRecoverHere() || ['uncertain', 'saved'].includes(recovery.status)) return;
  capture();
  recovery.payload.view_ref = { ...state.data.view_ref }; recovery.payload.request_id = crypto.randomUUID();
  if (!passage(recovery.payload.passage_id)) recovery.payload.passage_id = '';
  recovery.status = 'draft'; recovery.error = null; keepDraft(); draw();
}

function cancelRecovery() {
  const recovery = state.draft?.recovery;
  if (!recovery || state.saving || state.draft.uncertain || ['uncertain', 'saved'].includes(recovery.status)) return;
  state.draft.recovery = null; keepDraft(); capture(); draw();
}

function downloadDraft() {
  if (!state.draft) return;
  const url = URL.createObjectURL(new Blob([browserDraftExport(state.draft)], { type: 'application/json;charset=utf-8' }));
  const link = node('a'); link.href = url; link.download = 'jsb-private-reading-draft.json';
  document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function drawRecovery(parent) {
  const draft = state.draft;
  if (!draft) return;
  const panel = node('section', 'desk-recovery'); panel.id = 'reading-recovery'; panel.setAttribute('aria-labelledby', 'reading-recovery-title');
  const title = node('h2', '', words().recoverTitle); title.id = 'reading-recovery-title';
  panel.append(title, para(state.data?.enabled ? words().recoverWhy : words().unavailable), para(words().recoverRule, 'desk-muted'));
  const original = node('section', 'desk-recovery-original');
  original.append(node('h3', '', words().originalDraft), para(words()[draft.kind], 'desk-kicker'));
  const context = draft.source_context;
  if (context) {
    original.append(para(local(context.title)), para(context.location, 'desk-muted'));
    if (context.source) {
      original.append(para(`${words().edition}: ${context.source.edition}`, 'desk-muted'), para(`${words().creator}: ${context.source.creator}`, 'desk-muted'));
      if (context.source.translator) original.append(para(`${words().translator}: ${context.source.translator}`, 'desk-muted'));
    } else original.append(para(words().originalNoSource, 'desk-muted'));
  } else original.append(para(words().originalDetailsMissing, 'desk-muted'));
  if (draft.anchor) { const quote = node('blockquote', '', draft.anchor.exact); quote.id = 'reading-original-quote'; original.append(quote); }
  const label = node('label', '', words().originalWriting); label.htmlFor = 'reading-original-text';
  const text = node('textarea'); text.id = 'reading-original-text'; text.rows = 3; text.readOnly = true; text.value = draft.text;
  original.append(label, text);
  const details = node('details', 'desk-item-meta'); details.append(node('summary', '', words().originalBinding), node('pre', '', JSON.stringify({ view_ref: draft.view_ref, source_context: context || null, anchor: draft.anchor }, null, 2))); original.append(details);
  const buttons = node('div', 'desk-recovery-actions');
  const download = action(words().downloadDraft, downloadDraft); download.id = 'reading-draft-download'; buttons.append(download);
  const discard = action(words().discardOriginal, () => { clearDraft(); state.message = ''; capture(); draw(); }, 'desk-link');
  discard.id = 'reading-discard-original'; discard.disabled = state.saving || draft.uncertain || Boolean(draft.recovery && draft.recovery.status !== 'saved'); buttons.append(discard); original.append(buttons);
  if (draft.uncertain) {
    original.append(para(words().recoverUnknown, 'desk-availability'));
    const retry = action(state.saving ? words().saving : words().retry, submit, 'desk-button desk-primary'); retry.id = 'reading-original-retry'; retry.disabled = state.saving || !canRecoverHere(); original.append(retry);
  }
  const grid = node('div', 'desk-recovery-grid'); grid.append(original);
  const copy = node('section', 'desk-recovery-copy'); copy.append(node('h3', '', words().newPassageNote), para(words().recoverCopyDetail));
  const recovery = draft.recovery;
  if (!recovery) {
    const prepare = action(words().prepareRecovery, prepareRecovery, 'desk-button'); prepare.id = 'reading-recovery-prepare'; prepare.disabled = state.saving || draft.uncertain || !canRecoverHere(); copy.append(prepare);
  } else {
    const locked = state.saving || draft.uncertain || !canRecoverHere() || ['uncertain', 'saved'].includes(recovery.status) || !sameReadingView(recovery.payload.view_ref, state.data?.view_ref);
    const destinationLabel = node('label', '', words().recoveryDestination); destinationLabel.htmlFor = 'reading-recovery-target';
    const destination = node('select'); destination.id = 'reading-recovery-target'; destination.disabled = locked;
    const choose = node('option', '', words().choosePassage); choose.value = ''; destination.append(choose);
    for (const p of passages()) { const option = node('option', '', `${local(p.title)} · ${p.location}`); option.value = p.id; destination.append(option); }
    if (recovery.payload.passage_id && !passage(recovery.payload.passage_id)) { const previous = node('option', '', words().missingPassage); previous.value = recovery.payload.passage_id; previous.disabled = true; destination.append(previous); }
    destination.value = recovery.payload.passage_id;
    const writingLabel = node('label', '', words().noteLabel); writingLabel.htmlFor = 'reading-recovery-text';
    const writing = node('textarea'); writing.id = 'reading-recovery-text'; writing.rows = 4; writing.maxLength = 4000; writing.value = recovery.payload.text; writing.disabled = locked;
    const update = () => { recovery.payload.text = writing.value; recovery.payload.passage_id = destination.value; recovery.payload.request_id = crypto.randomUUID(); recovery.status = 'draft'; recovery.error = null; keepDraft(); save.disabled = !canSaveRecovery(); };
    destination.addEventListener('change', update); writing.addEventListener('input', update);
    copy.append(destinationLabel, destination, writingLabel, writing);
    const save = action(state.saving ? words().saving : recovery.status === 'uncertain' ? words().retry : words().saveNewNote, saveRecovery, 'desk-button desk-primary');
    save.id = 'reading-recovery-save'; save.disabled = !canSaveRecovery();
    if (recovery.status === 'saved') {
      const saved = (state.data?.items || []).find(item => item.id === recovery.saved_id);
      copy.append(para(saved ? words().recoverySaved : words().recoveryNotListed, 'desk-availability'));
      const open = action(words().openSaved, () => openItem(saved), 'desk-link'); open.disabled = !saved || !passage(saved.passage_id); copy.append(open);
    } else {
      if (recovery.status === 'uncertain') copy.append(para(words().failed, 'desk-availability'));
      if (!sameReadingView(recovery.payload.view_ref, state.data?.view_ref) && recovery.status !== 'uncertain') {
        copy.append(para(words().recoveryDestinationChanged, 'desk-availability'));
        const refresh = action(words().refreshRecoveryDestination, refreshRecoveryDestination); refresh.id = 'reading-recovery-refresh'; refresh.disabled = state.saving || draft.uncertain || !canRecoverHere(); copy.append(refresh);
      }
      copy.append(save);
      if (recovery.status !== 'uncertain') {
        const cancel = action(words().cancelRecovery, cancelRecovery, 'desk-link'); cancel.id = 'reading-recovery-cancel'; cancel.disabled = state.saving || draft.uncertain; copy.append(cancel);
      }
    }
  }
  grid.append(copy); panel.append(grid);
  const status = para(state.draftKept ? words().draftKept : words().draftUnsaved, 'desk-muted'); status.id = 'reading-draft-status'; panel.append(status); parent.append(panel);
}

async function saveRecovery() {
  if (!needsRecovery() || !canSaveRecovery()) return;
  const draft = state.draft, recovery = draft.recovery;
  const wasUnconfirmed = recovery.status === 'uncertain';
  capture(); state.saving = true; recovery.status = 'uncertain'; keepDraft(); draw();
  try {
    const response = await fetch('/api/reading/items', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Reading-Token': state.data.write_token }, body: JSON.stringify(recovery.payload) });
    const result = await response.json();
    if (result.saved) {
      recovery.status = 'saved'; recovery.saved_id = result.id; recovery.error = null;
      await readData(); state.message = words().recoverySaved; state.inspected = [result.id];
    } else {
      recovery.status = saveUnconfirmed(result, wasUnconfirmed) ? 'uncertain' : 'failed'; recovery.error = result.error || null;
      if (['stale_view', 'reading_forbidden', 'reading_read_only'].includes(result.error)) await readData();
      const messages = { stale_view: 'recoveryDestinationChanged', history_limit: 'limit', reading_busy: 'busy' };
      state.message = words()[messages[result.error] || (recovery.status === 'uncertain' ? 'failed' : 'invalid')];
    }
  } catch { recovery.status = 'uncertain'; recovery.error = 'reading_unavailable'; state.message = words().failed; }
  finally { state.saving = false; keepDraft(); draw(); }
}

function inspectItems(ids) {
  capture(); state.inspected = ids;
  if (state.positions[state.current]) state.positions[state.current].context = 0;
  draw();
  requestAnimationFrame(() => {
    const panel = root.querySelector('#reading-inspector');
    panel?.scrollIntoView({ block: 'nearest' }); panel?.focus({ preventScroll: true });
  });
}

function drawInspector(parent, p) {
  const items = (state.data?.items || []).filter(item => state.inspected.includes(item.id) && item.passage_id === p.id);
  if (!items.length) return;
  const panel = node('section', 'desk-inspector'); panel.id = 'reading-inspector'; panel.tabIndex = -1;
  panel.setAttribute('aria-labelledby', 'reading-inspector-title');
  const heading = node('div', 'desk-inspector-heading');
  const title = node('h3', '', `${words().savedBesideText} (${items.length})`); title.id = 'reading-inspector-title';
  const close = action(words().closeSaved, () => { capture(); state.inspected = []; draw(); root.querySelector('#reading-notes-jump')?.focus({ preventScroll: true }); }, 'desk-link');
  close.id = 'reading-inspector-close'; heading.append(title, close); panel.append(heading);
  for (const item of items) {
    const card = node('article', 'desk-inspected-item'); card.dataset.inspectedItem = item.id;
    card.append(para(words()[item.kind], 'desk-kicker'));
    if (item.anchor) card.append(node('blockquote', '', item.anchor.exact));
    card.append(para(item.text || words().noComment, 'desk-inspected-text'));
    if (!item.current_view) card.append(para(words().priorView, 'desk-availability'));
    const edit = action(words().edit, () => begin(item.kind, item), 'desk-link'); edit.dataset.editInspected = item.id;
    edit.disabled = !writable() || !item.current_view || Boolean(state.draft) || state.saving; card.append(edit);
    panel.append(card);
  }
  parent.append(panel);
}

function drawReading(p) {
  const title = node('header', 'desk-reading-heading');
  title.append(para(`${p.book} · ${p.location}`, 'desk-eyebrow'), node('h1', '', local(p.title)));
  const count = (state.data?.items || []).filter(item => item.passage_id === p.id).length;
  const notes = action(`${words().personal} (${count})`, () => reveal(root.querySelector('#reading-personal')), 'desk-link desk-notes-jump');
  notes.id = 'reading-notes-jump'; title.append(notes);
  root.append(title);
  const columns = node('div', 'desk-reading-columns');
  const sourcePane = node('section', 'desk-pane'); sourcePane.setAttribute('aria-label', words().read);
  const sourceToolbar = node('div', 'desk-pane-toolbar');
  sourceToolbar.append(node('h2', 'desk-pane-title', words().read));
  for (const [kind, label] of [['note', 'addNote'], ['highlight', 'addHighlight']]) {
    const button = action(words()[label], () => begin(kind), 'desk-pane-action');
    button.dataset.readingAction = kind;
    button.disabled = !writable() || state.saving || (kind === 'highlight' && !p.text);
    sourceToolbar.append(button);
  }
  sourcePane.append(sourceToolbar);
  const sourceScroll = node('div', 'desk-source-scroll');
  sourceScroll.addEventListener('scroll', capture, { passive: true });
  if (p.text !== null) {
    const credit = node('div', 'desk-source-credit');
    credit.append(para(p.source.title), para(`${words().edition}: ${p.source.edition}`), para(`${words().creator}: ${p.source.creator}`), para(`${words().sourceLanguage}: ${p.source_language}`));
    if (p.source.translator) credit.append(para(`${words().translator}: ${p.source.translator}`));
    if (!p.source.is_current) credit.append(para(words().previousSource, 'desk-availability'));
    sourceScroll.append(credit);
    const body = node('div', 'desk-source-text'); body.id = 'reading-source-text'; body.lang = p.source_language;
    const focus = state.focus?.passage_id === p.id ? state.focus.anchor : null;
    for (const segment of sourceSegments(p, state.data.items || [], focus)) {
      const part = node(segment.marked ? 'mark' : 'span', '', segment.text);
      if (state.focus?.passage_id === p.id && segment.start >= state.focus.anchor.start && segment.start < state.focus.anchor.end) part.dataset.proof = 'true';
      if (segment.savedIds.length) {
        part.tabIndex = 0; part.setAttribute('role', 'button'); part.dataset.savedHighlight = 'true';
        part.setAttribute('aria-label', `${words().openHighlight}: ${segment.text}`);
        part.addEventListener('click', () => { const selection = window.getSelection(); if (!selection || selection.isCollapsed) inspectItems(segment.savedIds); });
        part.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); inspectItems(segment.savedIds); } });
      }
      body.append(part);
    }
    sourceScroll.append(body);
  } else sourceScroll.append(node('h3', '', words().noText), para(words().noTextDetail));
  sourcePane.append(sourceScroll); columns.append(sourcePane);
  const contextPane = node('section', 'desk-pane'); contextPane.setAttribute('aria-label', words().understand);
  const contextToolbar = node('div', 'desk-pane-toolbar');
  const suggest = action(words().addConnection, () => begin('connection'), 'desk-pane-action');
  suggest.dataset.readingAction = 'connection'; suggest.disabled = !writable() || state.saving;
  contextToolbar.append(node('h2', 'desk-pane-title', words().understand), suggest);
  contextPane.append(contextToolbar);
  const contextScroll = node('div', 'desk-context-scroll');
  contextScroll.addEventListener('scroll', capture, { passive: true });
  if (needsRecovery()) drawRecovery(contextScroll);
  else if (state.draft?.passage_id === p.id) drawForm(contextScroll);
  drawInspector(contextScroll, p);
  contextScroll.append(para(local(p.explanation), 'desk-explanation'));
  const views = group(words().views, 'views');
  for (const opinion of p.interpretations) views.append(para(local(opinion.text)), para(`${words().viewAuthor}: ${opinion.by}`, 'desk-muted'));
  if (!p.interpretations.length) views.append(para(words().noEvidence));
  contextScroll.append(views);
  const evidence = group(words().evidence, 'evidence');
  evidence.append(para(words().evidenceRule, 'desk-muted'));
  for (const category of ['wording', 'textual_witness', 'event', 'context', 'interpretation']) {
    const section = node('div', 'desk-evidence-category'); section.append(node('h3', '', words()[category]));
    const records = p.evidence.filter(item => item.category === category);
    if (!records.length) section.append(para(p.text && category !== 'wording' ? words().fixtureEvidence : words().noEvidence, 'desk-muted'));
    for (const item of records) {
      const detail = node('details', 'desk-evidence-card'); detail.append(node('summary', '', local(item.title)), para(local(item.text)), node('blockquote', '', item.anchor.exact));
      const linked = passage(item.passage_id);
      detail.append(para(`${linked.source?.title || linked.location} · ${linked.source?.edition || ''}`, 'desk-muted'));
      detail.append(action(words().locate, () => { capture(); if (p.id !== item.passage_id) go(item.passage_id); state.focus = item; draw(); }));
      const meta = node('details'); meta.append(node('summary', '', words().evidenceDetails), para(`[${item.anchor.start}, ${item.anchor.end}) · Unicode code points`)); detail.append(meta);
      section.append(detail);
    }
    evidence.append(section);
  }
  contextScroll.append(evidence);
  const connections = group(words().connections, 'connections', true);
  for (const connection of p.connections) {
    const card = node('div', 'desk-connection'); card.append(para(words()[connection.relation] || connection.relation, 'desk-kicker'), para(local(connection.reason)));
    card.append(action(local(passage(connection.target_id).title), () => go(connection.target_id), 'desk-link')); connections.append(card);
  }
  if (!p.connections.length) connections.append(para(words().noConnections));
  contextScroll.append(connections);
  contextPane.append(contextScroll); columns.append(contextPane); root.append(columns);
  drawPersonal(p);
}

function drawPersonal(p) {
  const section = node('section', 'desk-personal'); section.id = 'reading-personal'; section.tabIndex = -1;
  section.append(node('h2', '', words().personal), para(words().privateOnly, 'desk-muted'));
  const controls = node('div', 'desk-personal-actions');
  for (const [kind, label] of [['note', 'addNote'], ['highlight', 'addHighlight'], ['connection', 'addConnection']]) {
    const button = action(words()[label], () => begin(kind)); button.dataset.readingAction = kind;
    button.disabled = !writable() || state.saving || (kind === 'highlight' && !p.text); controls.append(button);
  }
  controls.append(action(words().refresh, async () => { capture(); await readData(); draw(); }, 'desk-link'));
  section.append(controls);
  if (!writable()) section.append(para(words().readOnly, 'desk-muted'));
  const list = node('div', 'desk-item-list'); list.id = 'reading-items';
  const items = (state.data?.items || []).filter(item => item.passage_id === p.id);
  if (!items.length) list.append(para(words().noNotes, 'desk-muted'));
  for (const item of items) {
    const card = node('div', 'desk-personal-item'); card.dataset.itemId = item.id; card.tabIndex = -1;
    card.append(para(words()[item.kind], 'desk-kicker'), para(item.text));
    if (item.anchor) card.append(node('blockquote', '', item.anchor.exact));
    if (!item.current_view) card.append(para(words().priorView, 'desk-availability'));
    if (canLocateItem(item, p)) {
      const locate = action(words().locate, () => locateItem(item), 'desk-link'); locate.dataset.locateItem = item.id; card.append(locate);
    }
    if (item.target_id) card.append(action(local(passage(item.target_id)?.title) || item.target_id, () => go(item.target_id), 'desk-link'));
    const edit = action(words().edit, () => begin(item.kind, item), 'desk-link'); edit.disabled = !writable() || !item.current_view || Boolean(state.draft); card.append(edit);
    const meta = node('details', 'desk-item-meta'); meta.append(node('summary', '', words().system), para(item.revised_at), para(item.revision_id)); card.append(meta); list.append(card);
  }
  section.append(list);
  if (state.data?.enabled) section.append(para(`${words().quota}: ${state.data.remaining_saves}`, 'desk-muted desk-quota'));
  root.append(section);
}

function drawForm(parent) {
  const draft = state.draft;
  const form = node('form', 'desk-editor'); form.id = 'reading-editor';
  form.addEventListener('submit', event => { event.preventDefault(); submit(); });
  form.addEventListener('keydown', event => { if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) { event.preventDefault(); if (!save.disabled) form.requestSubmit(); } });
  form.append(node('h3', '', words()[draft.kind]));
  form.append(para(draft.anchor ? words().selectedNote : words().passageNote, 'desk-kicker'));
  if (draft.anchor) form.append(para(words().selection, 'desk-kicker'), node('blockquote', '', draft.anchor.exact));
  const label = node('label', '', draft.kind === 'highlight' ? words().commentLabel : draft.kind === 'connection' ? words().connectionLabel : words().noteLabel); label.htmlFor = 'reading-note';
  const text = node('textarea'); text.id = 'reading-note'; text.maxLength = 4000; text.rows = 4; text.value = draft.text;
  text.placeholder = draft.kind === 'highlight' ? words().commentPlaceholder : draft.kind === 'connection' ? words().connectionPlaceholder : words().notePlaceholder;
  text.disabled = state.saving || draft.uncertain;
  text.addEventListener('input', () => {
    draft.text = text.value; draft.request_id = crypto.randomUUID(); keepDraft();
    const blank = draft.kind !== 'highlight' && !draft.text.trim();
    save.disabled = state.saving || !writable() || draft.failure === 'revision_conflict' || blank;
    const separate = form.querySelector('#reading-save-separate');
    if (separate) separate.disabled = state.saving || draft.uncertain || !writable() || !sameDraftView() || blank;
  });
  form.append(label, text);
  if (draft.kind === 'connection') {
    const label = node('label', '', words().target); label.htmlFor = 'reading-target';
    const select = node('select'); select.id = 'reading-target';
    for (const p of passages().filter(p => p.id !== draft.passage_id)) { const option = node('option', '', local(p.title)); option.value = p.id; select.append(option); }
    select.value = draft.target_id; select.disabled = state.saving || draft.uncertain;
    select.addEventListener('change', () => { draft.target_id = select.value; draft.request_id = crypto.randomUUID(); keepDraft(); }); form.append(label, select);
  }
  const buttons = node('div', 'desk-personal-actions');
  const save = node('button', 'desk-button desk-primary', state.saving ? words().saving : draft.uncertain ? words().retry : words().save); save.type = 'submit'; save.id = 'reading-save'; save.disabled = state.saving || !writable() || draft.failure === 'revision_conflict' || (draft.kind !== 'highlight' && !draft.text.trim());
  const cancel = action(words().cancel, () => { clearDraft(); capture(); draw(); }); cancel.id = 'reading-cancel'; cancel.disabled = state.saving || draft.uncertain;
  buttons.append(save, cancel); form.append(buttons);
  if (draft.uncertain) form.append(para(words().failed, 'desk-availability'));
  else { const status = para(state.draftKept ? words().draftKept : words().draftUnsaved, 'desk-muted'); status.id = 'reading-draft-status'; form.append(status); }
  form.append(para(words().saveShortcut, 'desk-muted'));
  if (draft.failure === 'revision_conflict') {
    const conflict = node('section', 'desk-conflict'); conflict.id = 'reading-conflict';
    conflict.append(node('h4', '', words().latestSaved), para(words().conflictChoices));
    const latest = (state.data?.items || []).find(item => item.id === draft.edit_record_id);
    if (latest) {
      conflict.append(para(latest.text || words().noComment, 'desk-inspected-text'));
      if (latest.target_id) conflict.append(para(`${words().target}: ${local(passage(latest.target_id)?.title) || words().missingPassage}`, 'desk-muted'));
    }
    const separate = action(words().saveSeparate, saveSeparate, 'desk-button'); separate.id = 'reading-save-separate';
    separate.disabled = state.saving || draft.uncertain || !writable() || !sameDraftView() || (draft.kind !== 'highlight' && !draft.text.trim());
    conflict.append(separate); form.append(conflict);
  }
  parent.append(form);
}

function sameDraftView() {
  return sameReadingView(state.draft?.view_ref, state.data?.view_ref);
}

async function saveSeparate() {
  const draft = state.draft;
  if (!draft || state.saving || !writable() || draft.uncertain || draft.failure !== 'revision_conflict' || !draft.edit_record_id || !sameDraftView() || (draft.kind !== 'highlight' && !draft.text.trim())) return;
  draft.edit_record_id = null; draft.expected_revision = null; draft.request_id = crypto.randomUUID(); draft.failure = null;
  keepDraft(); await submit();
}

async function submit() {
  if (state.saving || !state.draft || state.draft.failure === 'revision_conflict' || (needsRecovery() && !state.draft.uncertain)) return;
  capture();
  const draft = state.draft;
  const wasUnconfirmed = Boolean(draft.uncertain);
  if (draft.kind !== 'highlight' && !draft.text.trim()) return setMessage(words().invalid);
  const payload = Object.fromEntries(['view_ref', 'request_id', 'kind', 'passage_id', 'text', 'anchor', 'target_id', 'edit_record_id', 'expected_revision'].map(key => [key, draft[key]]));
  state.saving = true; const pendingKey = draftKey('pending'); if (pendingKey) remember('sessionStorage', pendingKey, { ...draft, uncertain: true }); draw();
  let result;
  try {
    const response = await fetch('/api/reading/items', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Reading-Token': state.data.write_token }, body: JSON.stringify(payload) });
    result = await response.json();
    if (result.saved) {
      clearDraft();
      await readData(); state.message = words().saved; state.inspected = [result.id];
      if (state.positions[state.current]) state.positions[state.current].context = 0;
    } else {
      const messages = { revision_conflict: 'conflict', stale_view: 'stale', history_limit: 'limit', reading_busy: 'busy', reading_unavailable: 'failed' };
      draft.uncertain = saveUnconfirmed(result, wasUnconfirmed);
      draft.failure = result.error || null;
      if (['revision_conflict', 'stale_view', 'reading_forbidden', 'reading_read_only'].includes(result.error)) await readData();
      state.message = words()[messages[result.error] || (draft.uncertain ? 'failed' : 'invalid')];
      if (!draft.uncertain) { if (pendingKey) remember('sessionStorage', pendingKey, null); keepDraft(); }
    }
  } catch {
    if (state.draft) state.draft.uncertain = true;
    state.message = words().failed;
  } finally {
    state.saving = false; draw();
    if (!state.draft && state.inspected.length) root.querySelector('#reading-inspector')?.focus({ preventScroll: true });
  }
}
