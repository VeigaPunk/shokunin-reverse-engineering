// emit-receipts.js — assemble carrier B receipts (arc3-loop1-round3, c1/EX-04)
// reads the measured JSON artifacts and emits compile / planted / probe receipts.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { keccak256, selector } = require('/dev/shm/ex04-r3/keccak.js');

const R = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-04';
const E = path.join(R, 'evidence');
const rd = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const stat = (p) => {
  const s = fs.statSync(p);
  return `${s.mtime.toISOString()} (${s.size} B)`;
};
const line = (c = '-') => c.repeat(78);

const opt = rd(path.join(E, 'compile-summary-opt200.json'));
const noopt = rd(path.join(E, 'compile-summary-noopt.json'));
const pOpt = rd(path.join(E, 'planted-B-opt200.json'));
const pNo = rd(path.join(E, 'planted-B-noopt.json'));
const ocOpt = rd(path.join(E, 'probe', 'offset-check-opt200.json'));
const ocNo = rd(path.join(E, 'probe', 'offset-check-noopt.json'));
const toolchain = fs.readFileSync(path.join(E, 'toolchain.txt'), 'utf8');

const anchor = [
  ['keccak256("")', keccak256(Buffer.alloc(0)).toString('hex'), 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'],
  ['transfer(address,uint256)', selector('transfer(address,uint256)'), 'a9059cbb'],
  ['balanceOf(address)', selector('balanceOf(address)'), '70a08231'],
  ['approve(address,uint256)', selector('approve(address,uint256)'), '095ea7b3'],
];
const anchorText = anchor
  .map(([n, got, want]) => `${got === want ? 'PASS' : 'FAIL'}  ${n} -> ${got}${got === want ? '' : ' (want ' + want + ')'}`)
  .join('\n');

let s = '';
s += line('=') + '\nCOMPILE RECEIPT — carrier B (arc3-loop1-round3, chain c1)\n';
s += 'Seat: EX-04 (chain c1, executor)   Date: 2026-10-19 (UTC-3 host clock)\n' + line('=') + '\n\n';
s += '1. COMPILER IDENTITY — round-1 solc prefix REUSED (no install this wave)\n' + line() + '\n';
s += toolchain.trim() + '\n';
s += `soljson.js sha256 matches round-1 EX-04 compile-receipt (221d7a66…) — prefix receipt re-verified.\n\n`;
s += '2. SOURCE IDENTITY\n' + line() + '\n';
s += `  carrierB.sol  sha256 ${sha(path.join(R, 'carrierB.sol'))}  size ${fs.statSync(path.join(R, 'carrierB.sol')).size} B\n`;
s += `  planted-B.txt sha256 ${sha(path.join(R, 'planted-B.txt'))}  (pre-probe table; see probe receipt §4)\n\n`;
for (const [name, m] of [['opt200', opt], ['noopt', noopt]]) {
  s += `3. LEG "${name}"\n` + line() + '\n';
  s += `  settings.optimizer = ${JSON.stringify(m.optimizer)}   metadata.settings.evmVersion = ${m.evmVersion_metadata}\n`;
  s += `  solc ${m.solc_version}\n`;
  s += `  runtime ${m.runtime_bytes} B  sha256 ${m.runtime_sha256}\n`;
  s += `  creation ${m.creation_bytes} B  sha256 ${m.creation_sha256}\n`;
  s += `  abi sha256 ${m.abi_sha256}   methodIdentifiers: ${m.method_identifiers_count} entries\n`;
  s += `  compiler warnings: ${m.compiler_warnings}\n`;
  for (const w of m.compiler_warning_texts) s += '    ' + w.trim().replace(/\n/g, '\n    ') + '\n';
  const p = name === 'opt200' ? pOpt : pNo;
  s += `  dispatcher prologue (first 12 runtime bytes): ${fs.readFileSync(path.join(E, `carrierB.runtime-${name}.hex`), 'utf8').slice(0, 24)}\n`;
  s += `  PUSH4 sites total ${p.push4_sites_total}; dispatch constants match planted ${p.dispatch_constants_match_planted}; extra non-dispatch PUSH4 immediates: ${JSON.stringify(p.extra_push4_immediates)}\n\n`;
}
s += '4. OPTIMIZER DELTA (the C1 named-Unknown leg)\n' + line() + '\n';
s += `  runtime bytes: opt200 ${opt.runtime_bytes} vs noopt ${noopt.runtime_bytes} (delta ${opt.runtime_bytes - noopt.runtime_bytes})\n`;
s += `  opt200-only non-dispatch PUSH4 constant: ${JSON.stringify(pOpt.extra_push4_immediates)} (Panic(uint256) selector 0x4e487b71 @pc ${pOpt.push4_immediates.filter((x) => x.startsWith('0x4e487b71')).join(',')})\n`;
s += `  same 11/11 planted selectors and same binary-search dispatcher shape (EQ+GT legs, ${ocOpt.total_legs} legs) on BOTH legs.\n\n`;
s += '5. REPRODUCE\n' + line() + '\n';
s += `  node evidence/compile-b.js carrierB.sol <outdir> opt200     # then noopt\n`;
s += `  node evidence/plant-b.js <outdir> opt200                    # then noopt\n`;
s += `  node evidence/offset-check.js evidence/planted-B-opt200.json probe/probe-opt200-hex-6.4.0.json evidence/carrierB.runtime-opt200.hex /dev/stdout\n`;
fs.writeFileSync(path.join(E, 'compile-receipt.txt'), s);

s = '';
s += line('=') + '\nKECCAK / PLANTED RECEIPT — carrier B (arc3-loop1-round3, chain c1)\n';
s += 'Seat: EX-04 (chain c1, executor)   Date: 2026-10-19\n' + line('=') + '\n\n';
s += 'METHOD — three independent derivations of keccak256(sig)[0:4]\n' + line() + '\n';
s += '  (a) pure-JS keccak.js (own Keccak-f[1600] implementation, reused verbatim from\n';
s += '      round-1 EX-06 evidence; source sha256 ' + sha(path.join(E, 'keccak.js')) + ')\n';
s += '  (b) js-sha3@0.8.0 from the solc prefix dep tree\n';
s += '  (c) solc 0.8.37 evm.methodIdentifiers (the compiler\'s own table)\n\n';
s += 'ANCHORS (keccak.js self-test, re-run this seat)\n' + line() + '\n' + anchorText + '\n\n';
s += 'TABLE — planted set, leg opt200 (K=' + pOpt.K + '), 3-way agreement ' + pOpt.functions.filter((f) => f.agree).length + '/' + pOpt.K + '\n' + line() + '\n';
s += '  selector    signature                                      mutability   js-sha3     solc        agree\n';
for (const f of pOpt.functions) {
  s += `  ${f.selector}  ${f.sig.padEnd(45)} ${f.mutability.padEnd(11)} ${f.js_sha3}  ${f.solc}  ${f.agree}\n`;
}
s += `\n  ERC-20 selectors present: ${JSON.stringify(pOpt.erc20_selectors_present)}  (non-ERC-20 shape holds by construction)\n`;
s += `  planted-B-opt200.json sha256 ${sha(path.join(E, 'planted-B-opt200.json'))}\n`;
s += `  planted-B-noopt.json  sha256 ${sha(path.join(E, 'planted-B-noopt.json'))}\n`;
s += `  planted-B.txt (identical table both legs) sha256 ${sha(path.join(R, 'planted-B.txt'))}\n\n`;
s += 'PRE-PROBE RECORDING (rule: planted set recorded before probing)\n' + line() + '\n';
s += `  scratch planted-B-opt200.txt mtime 2026-10-19 10:07:18.366781950 -0300\n`;
s += `  first probe envelope mtime          2026-10-19 10:07:27.704819928 -0300  (9.3 s later)\n`;
s += `  artifact copy in this tree: planted-B.txt ${stat(path.join(R, 'planted-B.txt'))}; probe envelopes ${stat(path.join(E, 'probe', 'probe-opt200-hex-6.4.0.json'))}\n`;
s += `  (scratch /dev/shm/ex04-r3 mtimes are the primary ordering evidence; the copies\n   preserve bytes — sha256 above — not scratch mtimes.)\n\n`;
s += 'DISPATCH-TABLE CROSS-CHECK (PUSH4 immediates vs planted)\n' + line() + '\n';
s += `  opt200: ${pOpt.push4_sites_total} PUSH4 sites; all 11 planted selectors present; extras ${JSON.stringify(pOpt.extra_push4_immediates)}\n`;
s += `  noopt : ${pNo.push4_sites_total} PUSH4 sites; all 11 planted selectors present; extras ${JSON.stringify(pNo.extra_push4_immediates)}\n`;
fs.writeFileSync(path.join(E, 'keccak-planted-receipt.txt'), s);

const legs = [
  ['opt200', 'hex', 'probe-opt200-hex-6.4.0'],
  ['opt200', 'raw-bin', 'probe-opt200-rawbin-6.4.0'],
  ['opt200', 'raw(hex file — TRAP)', 'probe-opt200-raw-6.4.0'],
  ['noopt', 'hex', 'probe-noopt-hex-6.4.0'],
  ['noopt', 'raw-bin', 'probe-noopt-rawbin-6.4.0'],
  ['noopt', 'raw(hex file — TRAP)', 'probe-noopt-raw-6.4.0'],
];
s = '';
s += line('=') + '\nPROBE RECEIPT — carrier B vs inspect-evm-interface (chain c1)\n';
s += 'Seat: EX-04 (chain c1, executor)   Date: 2026-10-19\n' + line('=') + '\n\n';
s += 'COMMAND FORM (r1 recheck line; disk-backed TMPDIR required on this host)\n' + line() + '\n';
s += '  TMPDIR=/var/tmp/ex04-r3-tmp npx -y rea-agents@6.4.0 inspect-evm-interface \\\n';
s += '      evidence/carrierB.runtime-<leg>.<hex|bin> <hex|raw> --format json\n';
s += '  rea-agents 6.4.0 from npx cache (package.json sha256 1c6244e5689db5354fffc0e92f4ee0e0237c3a6d645de564ade2d8375fa570f9)\n';
s += '  all runs exit 0; stderr empty (0 B, captured in probe/*.err)\n\n';
s += 'RESULTS — planted K=11 vs probe set\n' + line() + '\n';
s += '  file                         enc                  probes  missing extra  set-eq  sha-match  ev_id\n';
for (const [leg, enc, base] of legs) {
  const c = rd(path.join(E, 'probe', base + '.compare.json'));
  const ev = c.evidence_id.length > 18 ? c.evidence_id.slice(0, 18) + '…' : c.evidence_id;
  s += `  carrierB.runtime-${leg}${leg === 'opt200' ? '' : ' '}  ${enc.padEnd(21)} ${String(c.probe_functions).padEnd(7)} ${String(c.missing.length).padEnd(7)} ${String(c.extra.length).padEnd(6)} ${String(c.set_equal).padEnd(7)} ${String(c.bytecode_sha_matches_runtime_file).padEnd(10)} ${ev}\n`;
}
s += '\n';
s += 'OFFSET SEMANTICS (probe bytecode_offset vs dispatcher compare legs)\n' + line() + '\n';
for (const [leg, oc] of [['opt200', ocOpt], ['noopt', ocNo]]) {
  s += `  ${leg}: probe offsets are dispatch-leg PUSH2 targets for all ${oc.rows.length} selectors: ${oc.all_probe_offsets_are_leg_targets}; all land on JUMPDEST (5b): ${oc.all_probe_offsets_jumpdest}\n`;
  s += `         dispatcher shape: binary search, ops ${oc.compare_ops_used.join('+')}, ${oc.total_legs} compare legs for 11 selectors\n`;
  const dup = oc.rows.find((r) => r.push4_compare_legs.length > 1);
  if (dup) s += `         duplicated node: ${dup.selector} ${dup.sig} — legs ${JSON.stringify(dup.push4_compare_legs)}; probe offset ${dup.probe_bytecode_offset} = the EQ leg (function entry); the GT leg target (${dup.push4_compare_legs[0].push2_jump_target}) is the binary-search split, not the entry.\n`;
}
s += '\nMUTABILITY INFERENCE vs COMPILED ABI\n' + line() + '\n';
for (const [leg, base] of [['opt200', 'probe-opt200-hex-6.4.0'], ['noopt', 'probe-noopt-hex-6.4.0']]) {
  const c = rd(path.join(E, 'probe', base + '.compare.json'));
  s += `  ${leg}: mismatches ${JSON.stringify(c.mutability_mismatches)}\n`;
}
s += '  -> upstream inference reports pure fn computeTxHash(…) as "view" — it separates\n';
s += '     state-mutating from non-mutating, not pure from view. (First pure function in\n';
s += '     this carrier family; r1 carriers had no pure leg.)\n\n';
s += 'TRAP LEG (re-run of the r1 raw-of-hex trap on a new carrier)\n' + line() + '\n';
s += '  Feeding the *hex text file* to the raw encoding decodes the ASCII file bytes as\n';
s += '  code: exit 0, 0 functions, probe bytecode sha256 == the hex FILE sha256\n';
s += `  (7dc26d4d…/54b8c906…), discovery_completeness "unknown" — parsed-and-empty, not an error.\n\n`;
s += 'NOT EXAMINED (scope)\n' + line() + '\n';
s += '  creation-blob legs for carrier B (r1 covered parsed-and-empty on two other carriers);\n';
s += '  rea-agents@6.7.0 on carrier B (chain may add); evmVersion/target chain identity (never claimed).\n';
fs.writeFileSync(path.join(E, 'probe-receipt.txt'), s);
console.log('wrote compile-receipt.txt, keccak-planted-receipt.txt, probe-receipt.txt');
console.log('sha256 planted-B.txt', sha(path.join(R, 'planted-B.txt')));
console.log('sha256 carrierB.sol  ', sha(path.join(R, 'carrierB.sol')));