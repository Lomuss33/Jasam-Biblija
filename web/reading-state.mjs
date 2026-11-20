// Offsets exchanged with Python count Unicode code points, never UTF-16 units.
export function pointOffset(text, utf16Offset) {
  return Array.from(text.slice(0, utf16Offset)).length;
}

export function sameReadingView(left, right) {
  const keys = ['record_id', 'revision_id', 'record_sha256', 'body_sha256'];
  return Boolean(left && right && Object.keys(left).length === keys.length && Object.keys(right).length === keys.length && keys.every(key => Object.hasOwn(left, key) && Object.hasOwn(right, key) && left[key] === right[key]));
}

export function draftNeedsRecovery(draft, data) {
  return Boolean(draft && (draft.recovery || !data?.enabled || !sameReadingView(draft.view_ref, data.view_ref) || !(data.passages || []).some(p => p.id === draft.passage_id) || draft.failure === 'stale_view'));
}

export function recoveryNote(draft, viewRef, passageId, requestId) {
  return { view_ref: { ...viewRef }, request_id: requestId, kind: 'note', passage_id: passageId,
    text: draft.text, anchor: null, target_id: null, edit_record_id: null, expected_revision: null };
}

export function browserDraftExport(draft) {
  return JSON.stringify({ description: 'Private synthetic browser draft; not a bank backup or source approval.', synthetic: true, releasable: false, review_state: 'private_proposal', draft }, null, 2) + '\n';
}

export function saveUnconfirmed(result, wasUnconfirmed = false) {
  if (result?.saved) return false;
  if (!result?.error || result.error === 'reading_unavailable') return true;
  // These writer errors follow the committed request-ID search. An HTTP/auth,
  // lock or validation failure alone cannot settle an earlier unknown save.
  return wasUnconfirmed && !['stale_view', 'revision_conflict'].includes(result.error);
}

function exactAnchor(text, anchor, points = null) {
  if (typeof text !== 'string' || !anchor) return false;
  points ??= Array.from(text);
  return Number.isInteger(anchor.start) && Number.isInteger(anchor.end) && anchor.start >= 0 && anchor.end <= points.length && anchor.start < anchor.end && points.slice(anchor.start, anchor.end).join('') === anchor.exact;
}

export function canLocateItem(item, passage) {
  return item.current_view === true && item.passage_id === passage?.id && exactAnchor(passage?.text, item.anchor);
}

export function sourceSegments(passage, items = [], focus = null) {
  if (typeof passage?.text !== 'string') return [];
  const saved = items.filter(item => item.kind === 'highlight' && canLocateItem(item, passage));
  const anchors = saved.map(item => item.anchor);
  if (focus) anchors.push(focus);
  return textSegments(passage.text, anchors).map(segment => {
    const end = segment.start + Array.from(segment.text).length;
    return { ...segment, savedIds: saved.filter(item => item.anchor.start <= segment.start && item.anchor.end >= end).map(item => item.id) };
  });
}

export function searchItems(items, passages, query = '', kind = 'all') {
  const term = query.trim().toLocaleLowerCase();
  const byId = new Map(passages.map(p => [p.id, p]));
  return items.filter(item => {
    if (kind !== 'all' && item.kind !== kind) return false;
    const source = byId.get(item.passage_id), target = byId.get(item.target_id);
    const fields = [item.text, item.anchor?.exact, item.passage_id, source?.book, source?.location,
      ...Object.values(source?.title || {}), ...Object.values(target?.title || {})];
    return fields.join(' ').toLocaleLowerCase().includes(term);
  }).sort((a, b) => b.revised_at.localeCompare(a.revised_at) || a.id.localeCompare(b.id));
}

export function textSegments(text, anchors = []) {
  const points = Array.from(text);
  const ranges = anchors.filter(a => exactAnchor(text, a, points));
  const cuts = [...new Set([0, points.length, ...ranges.flatMap(a => [a.start, a.end])])].sort((a, b) => a - b);
  return cuts.slice(0, -1).map((start, i) => ({ start, text: points.slice(start, cuts[i + 1]).join(''), marked: ranges.some(a => a.start <= start && a.end >= cuts[i + 1]) }));
}

export function safeLink(value) {
  try { const url = new URL(value); return ['http:', 'https:'].includes(url.protocol) ? url.href : null; }
  catch { return null; }
}
