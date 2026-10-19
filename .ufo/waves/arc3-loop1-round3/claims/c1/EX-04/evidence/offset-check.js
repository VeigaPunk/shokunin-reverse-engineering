// offset-check.js — probe bytecode_offset vs dispatcher PUSH2 jump targets (c1/EX-04)
// usage: node offset-check.js <plantedJson> <probeJson> <runtimeHexFile> <outJson>
// Semantics under test: does the probe's bytecode_offset equal a JUMPDEST that the
// dispatcher's compare legs (PUSH4 <sel> (GT|EQ|LT) PUSH2 <target> JUMPI) jump to for
// that selector? All occurrences are collected — solc's binary-search dispatcher emits
// the same selector at several tree nodes.
const fs = require('fs');
const [plantedPath, probePath, hexPath, outPath] = process.argv.slice(2);
const planted = JSON.parse(fs.readFileSync(plantedPath, 'utf8'));
const probe = JSON.parse(fs.readFileSync(probePath, 'utf8'));
const hex = fs.readFileSync(hexPath, 'utf8').trim().toLowerCase();
const fns = (probe.normalized_result || {}).functions || [];
const OPNAME = { 10: 'LT', 11: 'GT', 14: 'EQ' };

const rows = [];
for (const f of planted.functions) {
  const sel = f.selector.slice(2);
  const re = new RegExp('63' + sel + '(10|11|14)61([0-9a-f]{4})57', 'g');
  const legs = [];
  let m;
  while ((m = re.exec(hex)) !== null) {
    const target = parseInt(m[2], 16);
    legs.push({
      compare_op: OPNAME[m[1]],
      push4_pc: Math.floor(m.index / 2),
      push2_jump_target: target,
      jumpdest_at_target: hex.slice(target * 2, target * 2 + 2) === '5b',
    });
  }
  const pf = fns.find((x) => x.selector === f.selector);
  const off = pf ? pf.bytecode_offset : null;
  rows.push({
    selector: f.selector,
    sig: f.sig,
    push4_compare_legs: legs,
    probe_bytecode_offset: off,
    probe_offset_is_leg_target: legs.some((l) => l.push2_jump_target === off),
    probe_offset_jumpdest: off !== null && hex.slice(off * 2, off * 2 + 2) === '5b',
    legs_at_probe_offset: legs.filter((l) => l.push2_jump_target === off).length,
  });
}
const out = {
  leg: planted.leg,
  carrier: 'VaultB',
  rows,
  all_probe_offsets_are_leg_targets: rows.every((r) => r.probe_offset_is_leg_target),
  all_probe_offsets_jumpdest: rows.every((r) => r.probe_offset_jumpdest),
  compare_ops_used: [...new Set(rows.flatMap((r) => r.push4_compare_legs.map((l) => l.compare_op)))],
  total_legs: rows.reduce((n, r) => n + r.push4_compare_legs.length, 0),
};
console.log(JSON.stringify(out, null, 1));
fs.writeFileSync(outPath, JSON.stringify(out, null, 2));