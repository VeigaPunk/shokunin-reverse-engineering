// EX-13: ABI -> keccak256(sig)[0:4] ground-truth selector list, using js-sha3
// from the receipted solc prefix tree (same library the r1 legs used).
const fs = require('fs');
const JS_SHA3 = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3';
const sha3 = require(JS_SHA3);
const files = process.argv.slice(2);
for (const f of files) {
  const abi = JSON.parse(fs.readFileSync(f, 'utf8'));
  const rows = [];
  for (const a of abi) {
    if (a.type !== 'function') continue;
    const sig = a.name + '(' + a.inputs.map(i => i.type).join(',') + ')';
    const sel = sha3.keccak256(sig).slice(0, 8);
    rows.push({ sel, sig, mutability: a.stateMutability });
  }
  rows.sort((a, b) => a.sel < b.sel ? -1 : 1);
  console.log(f);
  for (const r of rows) console.log('  ' + r.sel, r.sig, '(' + r.mutability + ')');
  console.log('  K=' + rows.length, 'sorted=' + rows.map(r => r.sel).join(','));
}