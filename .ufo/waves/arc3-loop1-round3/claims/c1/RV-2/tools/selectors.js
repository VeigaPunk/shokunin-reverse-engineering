#!/usr/bin/env node
// RV-2 (arc3-loop1-round3): independent selector derivation from ABI JSON.
// usage: node selectors.js <abi.json> [<abi.json> ...]
const fs = require('fs');
const sha3 = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');
for (const f of process.argv.slice(2)) {
  const abi = JSON.parse(fs.readFileSync(f, 'utf8'));
  const out = [];
  for (const e of abi) {
    if (e.type !== 'function') continue;
    const sig = `${e.name}(${(e.inputs || []).map((i) => i.type).join(',')})`;
    const h = sha3.keccak256(sig);
    out.push({ sig, selector: h.slice(0, 8), full: h });
  }
  out.sort((a, b) => a.selector.localeCompare(b.selector));
  console.log(`== ${f}  (${out.length} functions)`);
  for (const o of out) console.log(`${o.selector}  ${o.sig}`);
  console.log(`FULLHASH ${f}`);
  for (const o of out) console.log(`${o.selector} ${o.full}`);
}