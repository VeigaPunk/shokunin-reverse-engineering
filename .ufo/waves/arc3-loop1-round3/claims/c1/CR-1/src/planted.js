// CR-1 planted-set derivation from ABI, two modes: filtered (type=="function") and naive (all entries with a name+inputs).
const fs = require('fs');
const { keccak256 } = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');

function canonicalType(inp) {
  if (inp.type === 'tuple' || inp.type.startsWith('tuple')) {
    const inner = (inp.components || []).map(canonicalType).join(',');
    return (inp.type === 'tuple' ? '' : inp.type.replace('tuple', '')) + '(' + inner + ')';
  }
  return inp.type;
}
function sigOf(e) { return e.name + '(' + (e.inputs || []).map(canonicalType).join(',') + ')'; }

const abiPath = process.argv[2];
const abi = JSON.parse(fs.readFileSync(abiPath, 'utf8'));
const filtered = [], naive = [], nonCallable = [];
for (const e of abi) {
  if (!e.name) { nonCallable.push(e.type + (e.type === 'receive' || e.type === 'fallback' ? '' : ':' + JSON.stringify(Object.keys(e)))); continue; }
  const sig = sigOf(e);
  const sel = keccak256(sig).slice(0, 8);
  const rec = { type: e.type, sig, selector: sel };
  if (e.type === 'function') filtered.push(rec); else { naive.push(rec); nonCallable.push(`${e.type}:${sig} -> ${sel}`); }
}
const uniq = a => [...new Set(a.map(r => r.selector))];
const res = {
  abiEntries: abi.length,
  filteredK: uniq(filtered).length,
  filtered: uniq(filtered).sort(),
  naiveK_plusNonFunction: uniq([...filtered, ...naive]).length,
  nonFunctionEntries: nonCallable,
  allSelectorsNaiveSorted: uniq([...filtered, ...naive]).sort(),
};
console.log(JSON.stringify(res, null, 2));