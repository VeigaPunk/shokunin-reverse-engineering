const fs = require('fs');
const EX05 = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/EX-05/';
const load05 = f => { const j = JSON.parse(fs.readFileSync(EX05 + f, 'utf8')); return j.data ? j.data : j; };
const loadMine = f => JSON.parse(fs.readFileSync('/dev/shm/ex06/' + f, 'utf8'));
const strip = (j) => {
  const c = JSON.parse(JSON.stringify(j));
  delete c.evidence_id; delete c.evidence_links;
  if (c.subject) { delete c.subject.name; delete c.subject.local_path; delete c.subject.digest; }
  if (c.parameters) { delete c.parameters.path; delete c.parameters.encoding; }
  if (c.normalized_result && c.normalized_result.artifact) delete c.normalized_result.artifact;
  if (c.locations) delete c.locations;
  return c;
};
const diff = (a, b, path = '') => {
  const out = [];
  if (a === b) return out;
  if (typeof a !== typeof b || a === null || b === null || typeof a !== 'object') { out.push(`${path || '$'}: ${JSON.stringify(a)} != ${JSON.stringify(b)}`); return out; }
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  for (const k of keys) {
    if (!(k in a)) { out.push(`${path}.${k}: absent in A, present in B`); continue; }
    if (!(k in b)) { out.push(`${path}.${k}: present in A, absent in B`); continue; }
    out.push(...diff(a[k], b[k], `${path}.${k}`));
  }
  return out;
};
const pairs = [
  ['EX-05 raw  vs my hex  (same bytes, cross-seat)', load05('kdx.raw.json'), loadMine('ex05/my-hex-on-ex05-bytes.json')],
  ['EX-05 raw  vs my raw  (same bytes, path control)', load05('kdx.raw.json'), loadMine('ex05/my-raw-on-ex05-bytes.json')],
  ['EX-05 hex  vs my hex  (same bytes, cross-seat)', load05('kdx.hex.json'), loadMine('ex05/my-hex-on-ex05-bytes.json')],
  ['EX-05 raw  vs EX-05 hex (their own pair)', load05('kdx.raw.json'), load05('kdx.hex.json')],
];
for (const [label, A, B] of pairs) {
  const d = diff(strip(A), strip(B));
  console.log(`\n=== ${label}: ${d.length === 0 ? 'DEEP-EQUAL (0 diffs after normalization)' : d.length + ' diffs'}`);
  for (const l of d.slice(0, 12)) console.log('   ', l);
  const payload = (j) => JSON.stringify({ funcs: j.raw_result.functions, bsha: j.normalized_result.bytecode.sha256, meta: j.raw_result.metadata });
  console.log('    A payload:', payload(A).slice(0, 260));
  console.log('    B payload:', payload(B).slice(0, 260));
  console.log('    A evidence_id:', A.evidence_id, '| B evidence_id:', B.evidence_id);
}
