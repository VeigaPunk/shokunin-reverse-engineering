// RV-2 independent oracle: keccak256 over the Vyper-compiled ABI signatures.
// Uses js-sha3 from the receipted solc prefix tree (third-party, not the seats' code).
const path = require('path');
const sha3 = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');
const fs = require('fs');
const abi = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = {};
for (const e of abi) {
  if (e.type !== 'function') continue;
  const sig = e.name + '(' + (e.inputs || []).map(i => i.type).join(',') + ')';
  out[sig] = sha3.keccak256(sig).slice(0, 8);
}
console.log(JSON.stringify(out, null, 1));
