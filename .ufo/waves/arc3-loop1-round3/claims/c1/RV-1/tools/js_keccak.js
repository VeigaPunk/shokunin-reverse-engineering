#!/usr/bin/env node
// RV-1 r3 — keccak path B: js-sha3@0.8.0 bundled inside the receipted
// arc3-loop1-round1 solc prefix (no install; package-lock pins 0.8.0).
// Usage: node js_keccak.js <sigs-file>   (one signature per line)
const path = require('path');
const PREFIX = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix';
const sha3 = require(path.join(PREFIX, 'node_modules/js-sha3'));
const fs = require('fs');
const pkgVersion = require(path.join(PREFIX, 'node_modules/js-sha3/package.json')).version;

const file = process.argv[2];
if (!file) { console.error('usage: node js_keccak.js <sigs-file>'); process.exit(2); }
console.log(`# path B — js-sha3@${pkgVersion} (from receipted solc prefix)`);
console.log(`# self-test keccak256('') = ${sha3.keccak256('')}`);
const lines = fs.readFileSync(file, 'utf8').split('\n');
for (const raw of lines) {
  const line = raw.trim();
  if (!line || line.startsWith('#')) continue;
  const h = sha3.keccak256(line);
  console.log(`${h.slice(0, 8)} ${line}`);
}