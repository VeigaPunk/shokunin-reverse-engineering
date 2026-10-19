// CR-1 compare driver: planted (ABI) vs present (PUSH4 census) per carrier/tag.
// Answers attacks 1 (optimizer transforms dispatch) and 2 (planted-from-ABI vs actual dispatch).
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { keccak256 } = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');

const PUSH = { 0x60:1,0x61:2,0x62:3,0x63:4,0x64:5,0x65:6,0x66:7,0x67:8,0x68:9,0x69:10,0x6a:11,0x6b:12,0x6c:13,0x6d:14,0x6e:15,0x6f:16,0x70:17,0x71:18,0x72:19,0x73:20,0x74:21,0x75:22,0x76:23,0x77:24,0x78:25,0x79:26,0x7a:27,0x7b:28,0x7c:29,0x7d:30,0x7e:31,0x7f:32 };

function sweep(code) {
  let i = 0; const push4 = [], jumpdests = new Set();
  while (i < code.length) {
    const op = code[i];
    if (op === 0x5b) jumpdests.add(i);
    if (PUSH[op] !== undefined) {
      const ln = PUSH[op], imm = code.subarray(i + 1, i + 1 + ln);
      if (imm.length < ln) break;
      if (op === 0x63) push4.push({ off: i, imm: imm.toString('hex') });
      i += 1 + ln; continue;
    }
    i += 1;
  }
  return { push4, jumpdests };
}

function canonicalType(inp) {
  if (inp.type === 'tuple' || inp.type.startsWith('tuple')) {
    const inner = (inp.components || []).map(canonicalType).join(',');
    return (inp.type === 'tuple' ? '' : inp.type.replace('tuple', '')) + '(' + inner + ')';
  }
  return inp.type;
}
function sigOf(e) { return e.name + '(' + (e.inputs || []).map(canonicalType).join(',') + ')'; }

// classify dispatch structure: walk a window after each PUSH4 for EQ/JUMPI / GT/LT patterns
function classify(code, push4) {
  let eqAfter = 0, cmpNear = 0, andMask = 0, jumpiNear = 0;
  for (const p of push4) {
    const win = code.subarray(p.off + 5, p.off + 14);
    // pattern A (classic): PUSH4 sel ; DUP1 ; EQ ; PUSH2 ; JUMPI
    const hex = win.toString('hex');
    if (/^(14|8014)/.test(hex)) eqAfter++;                      // EQ or DUP1 EQ right after
    if (hex.includes('11') || hex.includes('10')) cmpNear++;     // GT(11)/LT(10) in window
    if (hex.includes('16')) andMask++;                           // AND (masked compare)
    if (hex.includes('57')) jumpiNear++;                         // JUMPI within window
  }
  return { eqAfter, cmpNear, andMask, jumpiNear };
}

const outdir = process.argv[2] || '/var/tmp/cr1-round3/out';
const files = fs.readdirSync(outdir).filter(f => f.endsWith('.runtime.hex'));
const report = { generatedAt: new Date().toISOString(), carriers: [] };
for (const f of files.sort()) {
  const base = f.replace('.runtime.hex', '');
  if (base.startsWith('ICr1')) continue;
  const [cname, tag] = base.split('.');
  const hex = fs.readFileSync(path.join(outdir, f), 'utf8').trim();
  const code = Buffer.from(hex, 'hex');
  const abi = JSON.parse(fs.readFileSync(path.join(outdir, base + '.abi.json'), 'utf8'));
  const filtered = [], nonFunction = [];
  for (const e of abi) {
    if (e.type !== 'function') { nonFunction.push({ type: e.type, sig: e.name ? sigOf(e) : `(${e.type})`, selector: e.name ? keccak256(sigOf(e)).slice(0, 8) : null }); continue; }
    filtered.push({ sig: sigOf(e), selector: keccak256(sigOf(e)).slice(0, 8) });
  }
  const fset = [...new Set(filtered.map(r => r.selector))].sort();
  const nset = [...new Set([...filtered.map(r => r.selector), ...nonFunction.filter(n => n.selector).map(n => n.selector)])].sort();
  const { push4, jumpdests } = sweep(code);
  const pset = new Set(push4.map(p => p.imm));
  const missingFiltered = fset.filter(s => !pset.has(s));           // planted-but-absent (dispatch table)
  const extraPresent = push4.map(p => p.imm).filter(s => !fset.includes(s)); // unplanted-but-present
  const nonFnPlantAbsent = nonFunction.filter(n => n.selector && !pset.has(n.selector)).map(n => `${n.type}:${n.sig}=${n.selector}`);
  // offsets per selector (dedup target detection)
  const offBySel = {};
  for (const p of push4) (offBySel[p.imm] = offBySel[p.imm] || []).push(p.off);
  // find PUSH2 targets that follow EQ right after a PUSH4 (dispatch targets)
  const targets = {};
  for (const p of push4) {
    const off = p.off; let j = off + 5;
    // skip DUP1/EQ
    let guard = 0;
    while (j < code.length && guard < 6) {
      const op = code[j];
      if (op === 0x61) { const t = code.readUInt16BE(j + 1); targets[p.imm] = targets[p.imm] || []; targets[p.imm].push(t); break; }
      if (op === 0x14 || op === 0x80 || op === 0x15 || op === 0x50) { j++; guard++; continue; }
      break;
    }
  }
  const struct = classify(code, push4);
  report.carriers.push({
    carrier: `${cname}.${tag}`,
    runtimeBytes: code.length,
    runtimeSha256: crypto.createHash('sha256').update(code).digest('hex'),
    abiEntries: abi.length, abiEntryTypes: abi.reduce((a, e) => (a[e.type] = (a[e.type] || 0) + 1, a), {}),
    filteredK: fset.length, filtered: fset,
    naiveK: nset.length, nonFunctionEntries: nonFunction,
    push4Count: push4.length,
    push4Imms: push4.map(p => p.imm),
    push4ImmsUniq: [...pset].sort(),
    missingFiltered, extraPresent, nonFnPlantAbsent,
    offBySel, dispatchTargets: targets,
    jumpdestCount: jumpdests.size,
    prologue16: code.subarray(0, 16).toString('hex'),
    struct,
  });
}
fs.writeFileSync('/var/tmp/cr1-round3/recon/census.json', JSON.stringify(report, null, 2) + '\n');
for (const c of report.carriers) {
  console.log(`\n=== ${c.carrier} (${c.runtimeBytes} B, sha256 ${c.runtimeSha256.slice(0, 8)}) ===`);
  console.log(`abiEntries=${c.abiEntries} types=${JSON.stringify(c.abiEntryTypes)} filteredK=${c.filteredK} push4Count=${c.push4Count} uniqPush4=${c.push4ImmsUniq.length} jumpdests=${c.jumpdestCount}`);
  console.log(`prologue16=${c.prologue16}`);
  console.log(`struct=${JSON.stringify(c.struct)}`);
  console.log(`missingFiltered=${JSON.stringify(c.missingFiltered)}`);
  console.log(`extraPresent=${JSON.stringify(c.extraPresent)}`);
  console.log(`nonFnPlantAbsent=${JSON.stringify(c.nonFnPlantAbsent)}`);
}