// CR-1 audit harness: for every probe envelope in a tree, extract decoded bytecode,
// re-census dispatch sites (EQ;PUSH2;JUMPI), and reconcile probe set vs byte-level dispatch set.
// Also groups envelopes by decoded digest to detect costume retries / partial->full transitions.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PUSH = { 0x60:1,0x61:2,0x62:3,0x63:4,0x64:5,0x65:6,0x66:7,0x67:8,0x68:9,0x69:10,0x6a:11,0x6b:12,0x6c:13,0x6d:14,0x6e:15,0x6f:16,0x70:17,0x71:18,0x72:19,0x73:20,0x74:21,0x75:22,0x76:23,0x77:24,0x78:25,0x79:26,0x7a:27,0x7b:28,0x7c:29,0x7d:30,0x7e:31,0x7f:32 };

function metaEnd(code) {
  if (code.length < 4) return code.length;
  const cborLen = code.readUInt16BE(code.length - 2);
  if (cborLen > 0 && cborLen < code.length - 2 && code[code.length - 2 - cborLen] === 0xa2) return code.length - 2 - cborLen;
  return code.length;
}
function census(code) {
  const end = metaEnd(code);
  let i = 0; const push4 = [], eqSites = [], gtSites = [];
  while (i < end) {
    const op = code[i];
    if (PUSH[op] !== undefined) {
      const ln = PUSH[op];
      if (i + 1 + ln > code.length) break;
      if (op === 0x63) {
        const imm = code.subarray(i + 1, i + 5).toString('hex');
        push4.push({ off: i, imm });
        // walk forward: optional DUP1/DUP2, expect EQ/LT/GT then PUSH2 then JUMPI
        let j = i + 5, comp = null, guard = 0;
        while (j < end && guard < 4) {
          const o2 = code[j];
          if (o2 === 0x14) { comp = 'EQ'; j++; guard++; continue; }
          if (o2 === 0x10) { comp = 'LT'; j++; guard++; continue; }
          if (o2 === 0x11) { comp = 'GT'; j++; guard++; continue; }
          if (o2 === 0x80 || o2 === 0x81 || o2 === 0x82) { j++; guard++; continue; }
          break;
        }
        if (comp && code[j] >= 0x60 && code[j] <= 0x62) {
          const w = code[j] - 0x5f;
          const dest = code.readUIntBE(j + 1, w);
          const after = code[j + 1 + w];
          if (after === 0x57) {
            if (comp === 'EQ') eqSites.push({ off: i, imm, dest });
            else gtSites.push({ off: i, imm, dest, cmp: comp });
          }
        }
      }
      i += 1 + ln; continue;
    }
    i += 1;
  }
  const eqSet = [...new Set(eqSites.map(s => s.imm))].sort();
  const allSet = [...new Set(push4.map(s => s.imm))].sort();
  const nonEq = allSet.filter(s => !eqSet.includes(s));
  return { end, push4Count: push4.length, eqSet, eqSites, gtSites, allSet, nonEqConstants: nonEq, byteLen: code.length };
}

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.json')) out.push(p);
  }
  return out;
}

const roots = process.argv.slice(2);
const envelopes = [];
for (const root of roots) {
  for (const f of walk(root)) {
    let j; try { j = JSON.parse(fs.readFileSync(f, 'utf8')); } catch { continue; }
    const list = Array.isArray(j) ? j : [j];
    for (const o of list) {
      if (!o || !o.normalized_result || !o.normalized_result.functions || !o.subject || !o.subject.digest) continue;
      const st = fs.statSync(f);
      envelopes.push({
        file: f, mtime: st.mtime.toISOString(), ev: o.evidence_id,
        subject: o.subject.digest.sha256, decoded: o.normalized_result.bytecode.sha256,
        bytes: o.normalized_result.bytecode.bytes, hex: o.normalized_result.bytecode.hex,
        n: o.normalized_result.functions.length,
        sels: o.normalized_result.functions.map(x => x.selector.replace(/^0x/, '')).sort(),
        dispatchKinds: [...new Set(o.normalized_result.functions.map(x => x.dispatch))],
        params: o.parameters,
      });
    }
  }
}
console.log(`envelopes=${envelopes.length}`);
const byDigest = {};
for (const e of envelopes) (byDigest[e.decoded] = byDigest[e.decoded] || []).push(e);

for (const [d, es] of Object.entries(byDigest)) {
  es.sort((a, b) => a.mtime.localeCompare(b.mtime));
  const code = Buffer.from(es[0].hex, 'hex');
  const c = census(code);
  const probeSet = [...new Set(es.flatMap(e => e.sels))].sort();
  const missing = c.eqSet.filter(s => !probeSet.includes(s));
  const extras = probeSet.filter(s => !c.eqSet.includes(s));
  console.log(`\n=== decoded ${d.slice(0, 16)} (${c.byteLen} B; codeEnd=${c.end}; cbor=${c.byteLen - c.end - 2}) ===`);
  console.log(`  envelopes: ${es.map(e => path.basename(e.file) + '@' + e.mtime.slice(11, 19) + 'Z n=' + e.n).join(' | ')}`);
  console.log(`  distinct subjects: ${[...new Set(es.map(e => e.subject.slice(0, 12)))].join(',')} | subject==decoded: ${es.map(e => e.subject === e.decoded).join(',')}`);
  console.log(`  probe set (n=${probeSet.length}): ${probeSet.join(' ')}`);
  console.log(`  EQ-dispatch set (n=${c.eqSet.length}): ${c.eqSet.join(' ')}`);
  console.log(`  GT-tier PUSH4 sites: ${c.gtSites.map(s => s.imm + '@' + s.off).join(' ') || '(none)'}`);
  console.log(`  non-EQ constants in code region: ${c.nonEqConstants.join(' ') || '(none)'}`);
  console.log(`  RECONCILE: probe-missing-from-dispatch=[${missing.join(' ')}] probe-extras-not-in-dispatch=[${extras.join(' ')}]`);
  const partials = es.map(e => e.n);
  if (new Set(partials).size > 1) console.log(`  !! PARTIAL->FULL TRANSITION within same decoded digest: n=${partials.join(',')}`);
  // dest-collision check (dedup / shared bodies)
  const dests = {};
  for (const s of c.eqSites) (dests[s.dest] = dests[s.dest] || []).push(s.imm);
  const shared = Object.entries(dests).filter(([, v]) => v.length > 1);
  if (shared.length) console.log(`  shared dispatch targets (dedup): ${shared.map(([d2, v]) => 'dest ' + d2 + ' <- ' + v.join('/')).join('; ')}`);
}