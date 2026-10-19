// arc3-loop1-round3 c1/EX-02 — planted selector set for carrierA.
// selector = keccak256(canonical_sig)[:4] via js-sha3 (prefix node_modules).
// Cross-checked set-equal against solc's own evm.methodIdentifiers.
const fs = require('fs');
const { keccak256 } = require('js-sha3');

const OUT = '/var/tmp/ex02-r3/out';
const abi = JSON.parse(fs.readFileSync(OUT + '/carrierA.abi.json', 'utf8'));

const canon = (p) => {
  if (p.type.startsWith('tuple')) throw new Error('tuple types not handled: ' + p.type);
  return p.type; // ABI input types are already canonical (uint256, address, ...)
};

const rows = [];
for (const e of abi.filter((x) => x.type === 'function')) {
  const sig = e.name + '(' + e.inputs.map(canon).join(',') + ')';
  rows.push({ sig, selector: '0x' + keccak256(sig).slice(0, 8), mutability: e.stateMutability });
}
rows.sort((a, b) => (a.selector < b.selector ? -1 : 1));

const nonFns = abi.filter((x) => x.type !== 'function').map((x) => x.type + ':' + (x.stateMutability || ''));
const text =
  rows.map((r) => `${r.selector} ${r.sig} [${r.mutability}]`).join('\n') +
  `\nK=${rows.length}\n` +
  `non-fn abi entries (no selector): ${nonFns.length ? nonFns.join(', ') : 'none'}\n`;
fs.writeFileSync(OUT + '/planted-A.txt', text);

// cross-check against solc-computed method identifiers (independent oracle)
const mids = JSON.parse(fs.readFileSync(OUT + '/carrierA.methodIdentifiers.json', 'utf8'));
const mine = new Set(rows.map((r) => r.selector.slice(2).toLowerCase()));
const solcSel = new Set(Object.values(mids).map((s) => s.toLowerCase()));
const missing = [...solcSel].filter((s) => !mine.has(s));
const extra = [...mine].filter((s) => !solcSel.has(s));
const ok = missing.length === 0 && extra.length === 0;

const report =
  'js-sha3 selectors: ' + rows.length + ' | solc methodIdentifiers: ' + solcSel.size + '\n' +
  'missing (in solc, not js-sha3): ' + JSON.stringify(missing) + '\n' +
  'extra (in js-sha3, not solc): ' + JSON.stringify(extra) + '\n' +
  'CROSS-CHECK: ' + (ok ? 'SET-EQUAL' : 'DISAGREE') + '\n' +
  rows.map((r) => `${r.selector.slice(2)} ${r.sig} | solc says ${mids[r.sig] || 'ABSENT'}`).join('\n') + '\n';
fs.writeFileSync(OUT + '/keccak-crosscheck-A.txt', report);
console.log(report);
if (!ok) process.exit(2);