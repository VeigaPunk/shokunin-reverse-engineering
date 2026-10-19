#!/usr/bin/env node
// planted-K.js — derive the planted selector set from the compiler-emitted ABI
// (not from hand-transcribed signatures), with the receipted tree's js-sha3@0.8.0.
// Writes planted-K.json + expected-selectors.txt and checks verbatim presence of
// every selector constant in the runtime hex. Seat EX-05, arc3-loop1-round3 C1.
//
// usage: node planted-K.js --abi=<f.abi.json> --runtime=<f.runtime.hex> \
//         --out=<dir> --name=CarrierB --prefix=<solc-prefix>

const fs = require('fs');
const path = require('path');

function arg(n) {
  const hit = process.argv.slice(2).find((a) => a.startsWith('--' + n + '='));
  return hit === undefined ? undefined : hit.slice(('--' + n + '=').length);
}

const abiPath = arg('abi');
const runtimePath = arg('runtime');
const outDir = arg('out');
const name = arg('name');
const prefix = arg('prefix');

const keccak256 = require(path.resolve(process.cwd(), prefix, 'node_modules/js-sha3')).keccak256;
const abi = JSON.parse(fs.readFileSync(abiPath, 'utf8'));
const runtimeHex = fs.readFileSync(runtimePath, 'utf8').trim().replace(/^0x/, '').toLowerCase();

function canonical(fn) {
  const types = fn.inputs.map((i) => i.type).join(',');
  return `${fn.name}(${types})`;
}

const fns = abi.filter((x) => x.type === 'function').map((fn) => {
  const sig = canonical(fn);
  const selector = '0x' + keccak256(sig).slice(0, 8);
  return {
    signature: sig,
    selector,
    selectorHex: selector.slice(2),
    mutability: fn.stateMutability,
    inputs: fn.inputs.map((i) => i.type),
    outputs: fn.outputs.map((o) => o.type),
  };
});
fns.sort((a, b) => a.selectorHex.localeCompare(b.selectorHex));

const K = fns.length;
const presence = fns.map((fn) => {
  const idx = runtimeHex.indexOf(fn.selectorHex);
  const count = runtimeHex.split(fn.selectorHex).length - 1;
  return { selector: fn.selector, found: idx >= 0, firstOffsetBytes: idx >= 0 ? idx / 2 : null, occurrences: count };
});

const report = {
  seat: 'EX-05',
  carrier: name,
  abiFile: path.resolve(abiPath),
  runtimeFile: path.resolve(runtimePath),
  keccakOracle: 'js-sha3@0.8.0 (dependency of the receipted solc prefix tree)',
  plantedK: K,
  functions: fns,
  presenceInRuntime: presence,
  allPresent: presence.every((p) => p.found),
};
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'planted-K.json'), JSON.stringify(report, null, 2) + '\n');
fs.writeFileSync(
  path.join(outDir, 'expected-selectors.txt'),
  fns.map((f) => f.selectorHex).join('\n') + '\n'
);

console.log(JSON.stringify({ carrier: name, plantedK: K, allPresent: report.allPresent, fns: fns.map((f) => `${f.selectorHex} ${f.signature} [${f.mutability}]`) }, null, 2));