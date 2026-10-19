// arc3-loop1-round3 c1/EX-02 — post-landing re-derivation (rule #14).
// Verifies the LANDED artifact copies: source↔solc-input identity, planted set
// re-derived from the landed ABI via js-sha3, runtime digest re-derived.
// Run: NODE_PATH=<prefix>/node_modules node reverifyA.js
const fs = require('fs');
const crypto = require('crypto');
const { keccak256 } = require('js-sha3');

const REPO = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-02';
const EV = REPO + '/evidence';
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex');

let ok = true;
const say = (s) => {
  console.log(s);
};

// 1. landed source == source embedded in the landed solc input
const src = fs.readFileSync(REPO + '/carrierA.sol', 'utf8');
const inp = JSON.parse(fs.readFileSync(EV + '/carrierA.solc-input.json', 'utf8'));
const emb = inp.sources['carrierA.sol'].content;
say('1. source identity');
say('   sha256(carrierA.sol)            = ' + sha(Buffer.from(src)));
say('   sha256(solc-input source)       = ' + sha(Buffer.from(emb)));
say('   identical: ' + (src === emb));
ok = ok && src === emb;

// 2. planted set re-derived from landed ABI via js-sha3 == landed planted-A.txt
const abi = JSON.parse(fs.readFileSync(EV + '/carrierA.abi.json', 'utf8'));
const rows = [];
for (const e of abi.filter((x) => x.type === 'function')) {
  const sig = e.name + '(' + e.inputs.map((i) => i.type).join(',') + ')';
  rows.push({ sig, selector: '0x' + keccak256(sig).slice(0, 8), mutability: e.stateMutability });
}
const rederived = rows
  .map((r) => `${r.selector} ${r.sig} [${r.mutability}]`)
  .sort();
const landed = fs
  .readFileSync(REPO + '/planted-A.txt', 'utf8')
  .split('\n')
  .filter((l) => l.startsWith('0x'))
  .map((l) => l.trim())
  .sort();
say('2. planted set re-derivation (js-sha3, from landed ABI)');
say('   re-derived K=' + rederived.length + '  landed K=' + landed.length);
say('   set-equal: ' + (JSON.stringify(rederived) === JSON.stringify(landed)));
ok = ok && JSON.stringify(rederived) === JSON.stringify(landed);
for (const r of rederived) say('   ' + r);

// 3. runtime digest re-derived from the landed hex carrier
const hexText = fs.readFileSync(EV + '/carrierA.runtime.hex', 'utf8');
const bytes = Buffer.from(hexText.trim(), 'hex');
const dg = sha(bytes);
say('3. runtime identity');
say('   file sha256 (hex text)          = ' + sha(Buffer.from(hexText)));
say('   decoded bytecode sha256         = ' + dg + ' (' + bytes.length + ' B)');
say('   matches probed digest 9f7392ac… : ' + (dg === '9f7392acccea72cd42bdd8095a8578cab0727766f218b5399da22bc21d23741a'));
ok = ok && dg === '9f7392acccea72cd42bdd8095a8578cab0727766f218b5399da22bc21d23741a';

say('REVERIFY: ' + (ok ? 'ALL CHECKS PASS' : 'FAILED'));
process.exit(ok ? 0 : 2);