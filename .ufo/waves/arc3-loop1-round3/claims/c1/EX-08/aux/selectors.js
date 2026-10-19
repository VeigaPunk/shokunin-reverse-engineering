// Derive planted selector sets via js-sha3 keccak (independent of solc's C++ keccak),
// cross-check against solc's own evm.methodIdentifiers, and freeze planted-K.json
// BEFORE any probe runs.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const PREFIX = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix';
const { keccak256 } = require(path.join(PREFIX, 'node_modules/js-sha3'));
const OUT = '/var/tmp/ex08-r3/evidence';

const report = JSON.parse(fs.readFileSync(path.join(OUT, 'compile-report.json'), 'utf8'));
const byTag = Object.fromEntries(report.carriers.map(c => [c.tag, c]));

function sel(sig) { return '0x' + keccak256(sig).slice(0, 8); }

function plantedFor(tag, abiFile) {
  const abi = JSON.parse(fs.readFileSync(path.join(OUT, abiFile), 'utf8'));
  const fns = abi.filter(a => a.type === 'function');
  const rows = fns.map(a => {
    const sig = a.name + '(' + a.inputs.map(i => i.type).join(',') + ')';
    return { sig, selector: sel(sig), mutability: a.stateMutability };
  }).sort((a, b) => a.selector < b.selector ? -1 : 1);
  const ids = byTag[tag].method_identifiers || {};
  const mismatches = [];
  for (const r of rows) {
    const ms = '0x' + (ids[r.sig] || '').toLowerCase();
    if (ms !== r.selector) mismatches.push({ sig: r.sig, js_sha3: r.selector, solc: ms });
  }
  for (const k of Object.keys(ids)) if (!rows.some(r => r.sig === k)) mismatches.push({ extra_in_solc: k });
  return { K: rows.length, functions: rows, method_identifiers_mismatches: mismatches };
}

const libErrors = ['Unauthorized()', 'TooDeep(uint256,uint256)'];
const nonDispatch = libErrors.map(sig => ({ sig, selector: sel(sig), kind: 'custom_error' }));

const planted = {
  schema: 'ex08-r3-planted-K',
  generated_at_utc: new Date().toISOString(),
  source_sha256: report.source_sha256,
  solc: report.solc_version,
  selector_oracle: 'js-sha3@0.8.0 keccak256(sig)[0:4]; cross-checked vs solc evm.methodIdentifiers',
  HarborBound: { ...byTag.CarrierB, runtime_sha256: byTag.CarrierB.runtime_sha256, ...plantedFor('CarrierB', 'CarrierB.abi.json') },
  HarborBoundNoOpt: { runtime_sha256: byTag.CarrierBNoOpt.runtime_sha256, ...plantedFor('CarrierBNoOpt', 'CarrierBNoOpt.abi.json') },
  HarborLib: { runtime_sha256: byTag.HarborLib.runtime_sha256, ...plantedFor('HarborLib', 'HarborLib.abi.json') },
  non_dispatch_push4_controls: [
    ...nonDispatch,
    { sig: 'scale(uint256,uint256)', selector: sel('scale(uint256,uint256)'), kind: 'library_external_selector (delegatecall encoding, expected NOT in dispatch)' },
    { sig: 'tag()', selector: sel('tag()'), kind: 'library_external_selector (delegatecall encoding, expected NOT in dispatch)' },
  ],
};
fs.writeFileSync(path.join(OUT, 'planted-K.json'), JSON.stringify(planted, null, 2));
console.log(JSON.stringify(planted, null, 2));
console.log('FROZEN-AT', new Date().toISOString());