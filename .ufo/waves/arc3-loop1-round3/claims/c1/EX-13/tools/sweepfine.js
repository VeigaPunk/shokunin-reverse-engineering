// EX-13 fine sweep — pin the selector-count threshold for linear-EQ → pivot-GT.
// K functions only (no public var): K = 5,6,7,8; optimizer off and on(runs 200).
const fs = require('fs');
const crypto = require('crypto');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);
const OUT = '/var/tmp/ex13/out';
const SRC = '/var/tmp/ex13/src';

function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }

function genSource(k) {
  const fns = [];
  for (let i = 0; i < k; i++) {
    fns.push(`    function g${i}(uint256 x) external returns (uint256) { return x + ${i + 1}; }`);
  }
  return `// SPDX-License-Identifier: MIT\npragma solidity ^0.8.0;\n\ncontract FineK${k} {\n${fns.join('\n')}\n}\n`;
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
  return { tag, ok: true, optimize: !!opts.optimize, runtime_bytes: rtHex.length / 2, runtime_sha256: sha256(Buffer.from(rtHex, 'hex')) };
}

const summary = { variants: [] };
for (const k of [5, 6, 7, 8]) {
  const content = genSource(k);
  const fileName = `FineK${k}.sol`;
  fs.writeFileSync(`${SRC}/${fileName}`, content);
  for (const opt of [false, true]) {
    const tag = `fk${k}-${opt ? 'on200' : 'off'}`;
    const r = compile(tag, fileName, content, { optimize: opt }, `FineK${k}`);
    summary.variants.push(r);
    console.log(tag, r.ok ? `${r.runtime_bytes}B sha=${r.runtime_sha256.slice(0, 8)}` : 'FAIL');
  }
}
fs.writeFileSync(`${OUT}/fine-summary.json`, JSON.stringify(summary, null, 1));