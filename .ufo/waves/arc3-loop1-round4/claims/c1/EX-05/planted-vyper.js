#!/usr/bin/env node
// planted-vyper.js — seat EX-05 (chain c1, arc3-loop1-round4).
//
// Input:  a Vyper-emitted ABI JSON file (path argv[2]).
// Output: canonical signature -> keccak256 -> 4-byte selector table,
//         computed with TWO independent implementations and asserted equal:
//           impl A: js-sha3@0.8.0 keccak256, loaded from the round-1
//                   receipted prefix tree (required by the seat line);
//           impl B: node:crypto 'keccak-256' (OpenSSL-backed, no shared
//                   code with js-sha3).
//         Optional impl C: pure-Python keccak (keccak_ref.py) is run by the
//         companion shell wrapper; this script only does A and B.
//
// usage: node planted-vyper.js <abi.json> <out-dir>
//
// Writes <out-dir>/planted.txt (r3 planted-file format) and
// <out-dir>/planted-full.json (per-entry 32-byte hashes + agreement).
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PREFIX = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix';
const jsSha3 = require(path.join(PREFIX, 'node_modules/js-sha3/src/sha3.js'));
const jsSha3Version = require(path.join(PREFIX, 'node_modules/js-sha3/package.json')).version;

const abiPath = process.argv[2];
const outDir = process.argv[3];
if (!abiPath || !outDir) {
  console.error('usage: node planted-vyper.js <abi.json> <out-dir>');
  process.exit(2);
}

const implA = (s) => jsSha3.keccak256(s);                       // js-sha3
const implB = (s) => crypto.createHash('keccak-256').update(s, 'utf8').digest('hex');

// self-check vectors before any ABI work
const VEC_EMPTY = 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470';
const VEC_TRANSFER = 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef';
for (const [name, fn] of [['js-sha3', implA], ['node-crypto', implB]]) {
  if (fn('') !== VEC_EMPTY || fn('Transfer(address,address,uint256)') !== VEC_TRANSFER) {
    console.error(`SELF-CHECK FAILED for ${name}`);
    process.exit(1);
  }
}

// canonical type name for ABI inputs (handles tuples/components and arrays)
function canonicalType(input) {
  const t = input.type || '';
  if (t.startsWith('tuple')) {
    const inner = (input.components || []).map(canonicalType).join(',');
    return `(${inner})${t.slice('tuple'.length)}`;
  }
  return t;
}

const abiRaw = fs.readFileSync(abiPath, 'utf8');
const abi = JSON.parse(abiRaw);
const abiSha = crypto.createHash('sha256').update(abiRaw).digest('hex');

const entries = [];
for (const item of abi) {
  if (item.type !== 'function') continue;
  const sig = `${item.name}(${(item.inputs || []).map(canonicalType).join(',')})`;
  const hA = implA(sig);
  const hB = implB(sig);
  entries.push({
    sig,
    mutability: item.stateMutability || '',
    keccak256_js_sha3: hA,
    keccak256_node_crypto: hB,
    selector: '0x' + hA.slice(0, 8),
    selector_node_crypto: '0x' + hB.slice(0, 8),
    agree: hA === hB,
  });
}

const allAgree = entries.every((e) => e.agree);
const dupSelectors = entries.map((e) => e.selector).filter((s, i, a) => a.indexOf(s) !== i);

entries.sort((x, y) => (x.selector < y.selector ? -1 : x.selector > y.selector ? 1 : 0));

fs.mkdirSync(outDir, { recursive: true });

const header = [
  `# planted selectors — seat EX-05 (chain c1, arc3-loop1-round4)`,
  `# source ABI: ${abiPath}`,
  `# abi sha256: ${abiSha}`,
  `# impl A: js-sha3@${jsSha3Version} (round-1 receipted prefix) keccak256`,
  `# impl B: node:crypto keccak-256 (OpenSSL-backed)`,
  `# two-implementation agreement: ${allAgree ? 'ALL AGREE' : 'DISAGREEMENT — SEE planted-full.json'}`,
  `# typed result: ${entries.length === 0 ? 'EMPTY — the ABI carries zero function entries; no selectors exist to plant' : 'SELECTORS — one line per ABI function'}`,
  '',
];
const body = entries.map((e) => `${e.selector} ${e.sig} [${e.mutability}]`);
const tail = ['', `K=${entries.length}`, ''];

fs.writeFileSync(path.join(outDir, 'planted.txt'), header.concat(body, tail).join('\n'));
fs.writeFileSync(
  path.join(outDir, 'planted-full.json'),
  JSON.stringify(
    {
      seat: 'EX-05',
      wave: 'arc3-loop1-round4',
      chain: 'c1',
      abi_path: abiPath,
      abi_sha256: abiSha,
      impl_a: `js-sha3@${jsSha3Version} keccak256 (round-1 receipted prefix)`,
      impl_b: 'node:crypto keccak-256 (OpenSSL-backed)',
      all_agree: allAgree,
      duplicate_selectors: dupSelectors,
      typed_result: entries.length === 0 ? 'EMPTY' : 'SELECTORS',
      K: entries.length,
      entries,
    },
    null,
    2
  ) + '\n'
);

console.log(`abi entries(function): ${entries.length}`);
console.log(`typed result: ${entries.length === 0 ? 'EMPTY (zero function entries)' : 'SELECTORS'}`);
console.log(`two-implementation agreement: ${allAgree}`);
if (dupSelectors.length) console.log(`DUPLICATE selectors: ${dupSelectors.join(',')}`);
console.log('planted.txt written:', path.join(outDir, 'planted.txt'));
if (!allAgree) process.exit(1);
if (entries.length === 0) process.exit(3);
