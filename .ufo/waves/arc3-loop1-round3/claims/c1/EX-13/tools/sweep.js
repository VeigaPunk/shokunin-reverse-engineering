// EX-13 selector-count sweep — does the optimizer change the dispatch STRUCTURE?
// Generates N-function contracts, compiles each at optimizer off/on(runs 200),
// writes runtime hex/bin + abi + summary with sha256.
const fs = require('fs');
const crypto = require('crypto');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);
const OUT = '/var/tmp/ex13/out';
const SRC = '/var/tmp/ex13/src';

function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }

function genSource(n) {
  const fns = [];
  for (let i = 0; i < n; i++) {
    fns.push(`    function f${i}(uint256 x) external returns (uint256) { return x + ${i + 1}; }`);
  }
  return `// SPDX-License-Identifier: MIT\npragma solidity ^0.8.0;\n\ncontract Sweep${n} {\n    uint256 public total;\n\n${fns.join('\n')}\n}\n`;
}

function compile(tag, fileName, content, opts, contractName) {
  const input = {
    language: 'Solidity',
    sources: { [fileName]: { content } },
    settings: {
      optimizer: opts.optimize ? { enabled: true, runs: 200 } : { enabled: false },
      outputSelection: { '*': { '*': ['abi', 'evm.deployedBytecode.object'] } }
    }
  };
  const out = JSON.parse(solc.compile(JSON.stringify(input)));
  const errs = (out.errors || []).map(e => e.severity + ': ' + e.formattedMessage);
  if ((out.errors || []).some(e => e.severity === 'error')) return { tag, ok: false, errors: errs };
  const c = out.contracts[fileName][contractName];
  const rtHex = c.evm.deployedBytecode.object;
  fs.writeFileSync(`${OUT}/${tag}.runtime.hex`, rtHex);
  fs.writeFileSync(`${OUT}/${tag}.runtime.bin`, Buffer.from(rtHex, 'hex'));
  fs.writeFileSync(`${OUT}/${tag}.abi.json`, JSON.stringify(c.abi, null, 2));
  return {
    tag, ok: true, optimize: !!opts.optimize, runs: opts.optimize ? 200 : null,
    runtime_bytes: rtHex.length / 2, runtime_sha256: sha256(Buffer.from(rtHex, 'hex')),
    head40: rtHex.slice(0, 80), errors: errs
  };
}

const summary = { solc: solc.version(), variants: [] };
for (const n of [8, 16, 32]) {
  const content = genSource(n);
  const fileName = `Sweep${n}.sol`;
  fs.writeFileSync(`${SRC}/${fileName}`, content);
  for (const opt of [false, true]) {
    const tag = `sw${n}-${opt ? 'on200' : 'off'}`;
    const r = compile(tag, fileName, content, { optimize: opt }, `Sweep${n}`);
    summary.variants.push(r);
    console.log(tag, r.ok ? `${r.runtime_bytes}B runtime=${r.runtime_sha256.slice(0, 8)} head=${r.head40.slice(0, 28)}` : 'FAIL ' + JSON.stringify(r.errors));
  }
}
fs.writeFileSync(`${OUT}/sweep-summary.json`, JSON.stringify(summary, null, 1));
console.log('wrote', `${OUT}/sweep-summary.json`);