// EX-13 payable-preamble threshold check: receive()+K functions, optimizer off/on.
const fs = require('fs');
const crypto = require('crypto');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);
const OUT = '/var/tmp/ex13/out';
const SRC = '/var/tmp/ex13/src';
function sha256(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function genSource(k) {
  const fns = [];
  for (let i = 0; i < k; i++) fns.push(`    function p${i}(uint256 x) external returns (uint256) { return x + ${i + 1}; }`);
  return `// SPDX-License-Identifier: MIT\npragma solidity ^0.8.0;\n\ncontract PayK${k} {\n    receive() external payable {}\n\n${fns.join('\n')}\n}\n`;
}
function compile(tag, fileName, content, opts, contractName) {
  const input = { language: 'Solidity', sources: { [fileName]: { content } },
    settings: { optimizer: opts.optimize ? { enabled: true, runs: 200 } : { enabled: false },
      outputSelection: { '*': { '*': ['abi', 'evm.deployedBytecode.object'] } } } };
  const out = JSON.parse(solc.compile(JSON.stringify(input)));
  if ((out.errors || []).some(e => e.severity === 'error')) return { tag, ok: false, errors: out.errors.map(e => e.formattedMessage) };
  const c = out.contracts[fileName][contractName];
  const rt = c.evm.deployedBytecode.object;
  fs.writeFileSync(`${OUT}/${tag}.runtime.hex`, rt);
  fs.writeFileSync(`${OUT}/${tag}.runtime.bin`, Buffer.from(rt, 'hex'));
  fs.writeFileSync(`${OUT}/${tag}.abi.json`, JSON.stringify(c.abi, null, 2));
  return { tag, ok: true, bytes: rt.length / 2, sha256: sha256(Buffer.from(rt, 'hex')) };
}
for (const k of [6, 7]) {
  const content = genSource(k);
  const fileName = `PayK${k}.sol`;
  fs.writeFileSync(`${SRC}/${fileName}`, content);
  for (const opt of [false, true]) {
    const r = compile(`pk${k}-${opt ? 'on200' : 'off'}`, fileName, content, { optimize: opt }, `PayK${k}`);
    console.log(`pk${k}-${opt ? 'on200' : 'off'}`, r.ok ? `${r.bytes}B sha=${r.sha256.slice(0, 8)}` : 'FAIL');
  }
}