// compare-b.js — planted vs probe set comparison for carrier B (c1/EX-04)
// usage: node compare-b.js <plantedJson> <probeJson> <leg> <encoding> <runtimeBin>
const fs = require('fs');
const crypto = require('crypto');

const [plantedPath, probePath, leg, enc, runtimeBin] = process.argv.slice(2);
const planted = JSON.parse(fs.readFileSync(plantedPath, 'utf8'));
const probe = JSON.parse(fs.readFileSync(probePath, 'utf8'));
const nr = probe.normalized_result || {};
const fns = nr.functions || [];
const probeSels = fns.map((f) => f.selector);
const plantedSels = planted.functions.map((f) => f.selector);
const missing = plantedSels.filter((s) => !probeSels.includes(s));
const extra = probeSels.filter((s) => !plantedSels.includes(s));

const bytes = fs.readFileSync(runtimeBin);
const sha = crypto.createHash('sha256').update(bytes).digest('hex');
const bytecodeShaMatch = (nr.bytecode || {}).sha256 === sha;
const bytecodeBytesMatch = (nr.bytecode || {}).bytes === bytes.length;

const jumpdest = (off) => off >= 0 && off < bytes.length && bytes[off] === 0x5b;
const offsetsOnJumpdest = fns.map((f) => jumpdest(f.bytecode_offset));
const dispatchAllAbi = fns.every((f) => f.dispatch === 'abi');

const mutMismatch = [];
for (const f of fns) {
  const p = planted.functions.find((x) => x.selector === f.selector);
  if (!p) continue;
  if (p.mutability !== f.inferred_state_mutability) {
    mutMismatch.push({ selector: f.selector, sig: p.sig, abi_mutability: p.mutability, probe_inferred: f.inferred_state_mutability });
  }
}

const out = {
  leg,
  encoding: enc,
  planted_K: plantedSels.length,
  probe_functions: fns.length,
  missing,
  extra,
  set_equal: missing.length === 0 && extra.length === 0,
  all_dispatch_abi: dispatchAllAbi,
  offsets_on_jumpdest: offsetsOnJumpdest.every(Boolean),
  offset_jumpdest_failures: fns.filter((f, i) => !offsetsOnJumpdest[i]).map((f) => `${f.selector}@${f.bytecode_offset}`),
  bytecode_sha_matches_runtime_file: bytecodeShaMatch,
  bytecode_bytes_match: bytecodeBytesMatch,
  probe_bytecode_sha256: (nr.bytecode || {}).sha256,
  runtime_sha256: sha,
  discovery_completeness: nr.discovery_completeness ?? null,
  mutability_mismatches: mutMismatch,
  evidence_id: probe.evidence_id,
  probe_selectors_sorted: [...probeSels].sort(),
};
console.log(JSON.stringify(out, null, 1));
fs.writeFileSync(probePath.replace(/\.json$/, '.compare.json'), JSON.stringify(out, null, 2));