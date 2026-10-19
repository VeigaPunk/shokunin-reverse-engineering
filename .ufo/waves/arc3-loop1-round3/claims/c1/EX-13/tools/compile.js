// EX-13 compile harness — solc 0.8.37 (receipted wave prefix), standard-JSON.
// Writes runtime/creation hex (no trailing newline, RV-2 convention), bin, abi,
// and a summary JSON with sha256 of every artifact.
const fs = require('fs');
const crypto = require('crypto');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);
const OUT = '/var/tmp/ex13/out';
const SRC = '/var/tmp/ex13/src';

function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }

function compile(tag, file, opts) {
  const content = fs.readFileSync(`${SRC}/${file}`, 'utf8');
  const input = {
    language: 'Solidity',
    sources: { [file]: { content } },
    settings: {
      optimizer: opts.optimize ? { enabled: true, runs: opts.runs || 200 } : { enabled: false },
      outputSelection: { '*': { '*': ['abi', 'metadata', 'evm.bytecode.object', 'evm.deployedBytecode.object'] } }
    }
  };
  const out = JSON.parse(solc.compile(JSON.stringify(input)));
  const errs = (out.errors || []).map(e => e.severity + ': ' + e.formattedMessage);
  if ((out.errors || []).some(e => e.severity === 'error')) {
    return { tag, errors: errs, ok: false };
  }
  const result = { tag, file, optimize: !!opts.optimize, runs: opts.optimize ? (opts.runs || 200) : null, errors: errs, contracts: {} };
  for (const cname of Object.keys(out.contracts[file])) {
    const c = out.contracts[file][cname];
    const rtHex = c.evm.deployedBytecode.object;
    const crHex = c.evm.bytecode.object;
    const prefix = `${OUT}/${tag}-${cname}`;
    fs.writeFileSync(`${prefix}.runtime.hex`, rtHex);
    fs.writeFileSync(`${prefix}.runtime.bin`, Buffer.from(rtHex, 'hex'));
    fs.writeFileSync(`${prefix}.creation.hex`, crHex);
    fs.writeFileSync(`${prefix}.abi.json`, JSON.stringify(c.abi, null, 2));
    result.contracts[cname] = {
      runtime_bytes: rtHex.length / 2,
      runtime_sha256: sha256(Buffer.from(rtHex, 'hex')),
      runtime_hex_file_sha256: sha256(Buffer.from(rtHex)),
      creation_bytes: crHex.length / 2,
      creation_sha256: sha256(Buffer.from(crHex, 'hex')),
      abi_functions: c.abi.filter(a => a.type === 'function').map(a => a.name + '(' + a.inputs.map(i => i.type).join(',') + ')').sort(),
      head40: rtHex.slice(0, 80)
    };
  }
  return { tag, file, ok: true, optimize: !!opts.optimize, runs: opts.optimize ? (opts.runs || 200) : null, errors: errs, contracts: result.contracts };
}

const runs = [
  ['rv2-off', 'Rv2Token.sol', { optimize: false }],
  ['rv2-on200', 'Rv2Token.sol', { optimize: true, runs: 200 }],
  ['tre-off', 'Treasury.sol', { optimize: false }],
  ['tre-on200', 'Treasury.sol', { optimize: true, runs: 200 }],
  ['gau-off', 'Gauge.sol', { optimize: false }],
  ['gau-on200', 'Gauge.sol', { optimize: true, runs: 200 }]
];

const summary = { solc: solc.version(), variants: [] };
for (const [tag, file, opts] of runs) {
  const r = compile(tag, file, opts);
  summary.variants.push(r);
  console.log(tag, r.ok ? 'OK' : 'FAIL');
  if (r.ok) for (const [cname, c] of Object.entries(r.contracts)) {
    console.log(' ', cname, c.runtime_bytes + 'B', 'runtime=' + c.runtime_sha256.slice(0, 8), 'head=' + c.head40.slice(0, 24));
  }
}
fs.writeFileSync(`${OUT}/summary.json`, JSON.stringify(summary, null, 1));
console.log('wrote', `${OUT}/summary.json`);