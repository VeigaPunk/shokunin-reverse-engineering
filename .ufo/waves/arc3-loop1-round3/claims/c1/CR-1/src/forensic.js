// CR-1 forensic pass: for each runtime, locate interesting 4-byte values as (a) raw bytes anywhere,
// (b) PUSH4 immediates, (c) context window; plus metadata-region split (CBOR tail) and dedup-target check.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { keccak256 } = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');
const PUSH = { 0x60:1,0x61:2,0x62:3,0x63:4,0x64:5,0x65:6,0x66:7,0x67:8,0x68:9,0x69:10,0x6a:11,0x6b:12,0x6c:13,0x6d:14,0x6e:15,0x6f:16,0x70:17,0x71:18,0x72:19,0x73:20,0x74:21,0x75:22,0x76:23,0x77:24,0x78:25,0x79:26,0x7a:27,0x7b:28,0x7c:29,0x7d:30,0x7e:31,0x7f:32 };

function sweep(code) {
  let i = 0; const push4 = []; const jumpdests = new Set();
  while (i < code.length) {
    const op = code[i];
    if (op === 0x5b) jumpdests.add(i);
    if (PUSH[op] !== undefined) { const ln = PUSH[op];
      if (i + 1 + ln > code.length) break;
      if (op === 0x63) push4.push({ off: i, imm: code.subarray(i+1, i+5).toString('hex') });
      i += 1 + ln; continue; }
    i += 1;
  }
  return { push4, jumpdests };
}
function occurrences(buf, val) { // val = 8-hex
  const needle = Buffer.from(val, 'hex'); const outs = [];
  let idx = 0;
  while (true) { const p = buf.indexOf(needle, idx); if (p < 0) break; outs.push(p); idx = p + 1; }
  return outs;
}
const outdir = process.argv[2];
const files = fs.readdirSync(outdir).filter(f => f.endsWith('.runtime.hex')).sort();
for (const f of files) {
  const base = f.replace('.runtime.hex', '');
  const hex = fs.readFileSync(path.join(outdir, f), 'utf8').trim();
  const code = Buffer.from(hex, 'hex');
  const abi = JSON.parse(fs.readFileSync(path.join(outdir, base + '.abi.json'), 'utf8'));
  const canon = i => i.type === 'tuple' ? '(' + (i.components||[]).map(canon).join(',') + ')' : i.type;
  const fsel = {};
  const others = {};
  for (const e of abi) {
    if (!e.name) continue;
    const sig = e.name + '(' + (e.inputs||[]).map(canon).join(',') + ')';
    const sel = keccak256(sig).slice(0, 8);
    (e.type === 'function' ? fsel : others)[sig] = sel;
  }
  // metadata tail: last 2 bytes = cbor length
  const cborLen = code.readUInt16BE(code.length - 2);
  const codeEnd = code.length - 2 - cborLen;
  const { push4 } = sweep(code);
  const push4set = new Set(push4.map(p => p.imm));
  const p4code = push4.filter(p => p.off < codeEnd);
  const p4meta = push4.filter(p => p.off >= codeEnd);
  console.log(`\n### ${base} bytes=${code.length} codeEnd=${codeEnd} (cbor=${cborLen}) push4(code)=${p4code.length} push4(meta/data)=${p4meta.length}`);
  console.log(`  push4 in code region: ${p4code.map(p=>p.imm+'@'+p.off).join(' ')}`);
  if (p4meta.length) console.log(`  push4 in metadata/data region: ${p4meta.map(p=>p.imm+'@'+p.off).join(' ')}`);
  // unplanted in code region
  const planted = new Set(Object.values(fsel));
  const unplanted = p4code.filter(p => !planted.has(p.imm));
  for (const u of unplanted) {
    const ctxA = code.subarray(Math.max(0,u.off-10), u.off).toString('hex');
    const ctxB = code.subarray(u.off+5, u.off+15).toString('hex');
    console.log(`  UNPLANTED ${u.imm}@${u.off}  ctx: ${ctxA} [PUSH4 ${u.imm}] ${ctxB}`);
  }
  // planted-but-absent in code region
  const absent = [...planted].filter(s => !push4set.has(s));
  if (absent.length) console.log(`  PLANTED-BUT-ABSENT(anywhere): ${absent.join(' ')}`);
  // where do non-function ABI entries' selectors appear?
  for (const [sig, sel] of Object.entries(others)) {
    const occ = occurrences(code, sel);
    console.log(`  non-fn ABI entry ${sig} sel=${sel}: raw occurrences @ [${occ.join(',')}] ${occ.some(o=>o<codeEnd)?'(code region)':'(outside code)'} inPush4=${push4set.has(sel)}`);
  }
  // asking: does the Error(string) selector appear?
  const es = occurrences(code, '08c379a0');
  const pan = occurrences(code, '4e487b71');
  console.log(`  Error(string)=08c379a0 occurrences=[${es.join(',')}] Panic=4e487b71 occurrences=[${pan.join(',')}]`);
}