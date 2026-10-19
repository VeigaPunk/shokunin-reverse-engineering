const fs = require('fs');
const load = f => JSON.parse(fs.readFileSync('/dev/shm/ex06/' + f, 'utf8'));
const strip = (j) => {
  const c = JSON.parse(JSON.stringify(j));
  delete c.evidence_id;
  delete c.evidence_links;
  if (c.subject) { delete c.subject.name; delete c.subject.local_path; delete c.subject.digest; }
  if (c.parameters) { delete c.parameters.path; delete c.parameters.encoding; }
  if (c.normalized_result && c.normalized_result.artifact) delete c.normalized_result.artifact;
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
const files = process.argv.slice(2);
const base = strip(load(files[0]));
console.log('REFERENCE:', files[0]);
console.log('functional payload (functions):');
for (const fn of base.raw_result.functions) console.log('  ', JSON.stringify(fn));
console.log('  bytecode sha256:', base.normalized_result.bytecode.sha256, 'bytes:', base.normalized_result.bytecode.bytes);
console.log('  dispatch values:', JSON.stringify([...new Set(base.raw_result.functions.map(f => f.dispatch))]));
console.log('  metadata:', JSON.stringify(base.raw_result.metadata));
for (const f of files.slice(1)) {
  const other = strip(load(f));
  const d = diff(base, other);
  console.log(`\n=== ${f}: ${d.length === 0 ? 'DEEP-EQUAL after normalization (0 diffs)' : d.length + ' diffs'}`);
  for (const line of d.slice(0, 25)) console.log('   ', line);
  // artifact-side raw values for the record
  const raw = load(f);
  console.log('    raw artifact digest:', raw.normalized_result.artifact.sha256, `(encoding=${raw.normalized_result.artifact.encoding}, bytes=${raw.normalized_result.artifact.bytes})`);
  console.log('    decoded bytecode sha256:', raw.normalized_result.bytecode.sha256);
}
