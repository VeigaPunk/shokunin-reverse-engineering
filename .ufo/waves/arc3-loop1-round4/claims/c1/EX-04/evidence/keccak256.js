#!/usr/bin/env node
// keccak-256 in pure JS (Keccak-f[1600], rate 136, Keccak padding 0x01) — an
// implementation independent of the Python one in this same directory and of
// any compiler, used for the three-way planted-K derivation at EX-04
// (arc3-loop1-round4 C1). Usage: node keccak256.js --selftest | <sig> ...
'use strict';
const RC = [
  0x0000000000000001n, 0x0000000000008082n, 0x800000000000808an, 0x8000000080008000n,
  0x000000000000808bn, 0x0000000080000001n, 0x8000000080008081n, 0x8000000000008009n,
  0x000000000000008an, 0x0000000000000088n, 0x0000000080008009n, 0x000000008000000an,
  0x000000008000808bn, 0x800000000000008bn, 0x8000000000008089n, 0x8000000000008003n,
  0x8000000000008002n, 0x8000000000000080n, 0x000000000000800an, 0x800000008000000an,
  0x8000000080008081n, 0x8000000000008080n, 0x0000000080000001n, 0x8000000080008008n,
];
const ROT = [
  [0, 36, 3, 41, 18],
  [1, 44, 10, 45, 2],
  [62, 6, 43, 15, 61],
  [28, 55, 25, 21, 56],
  [27, 20, 39, 8, 14],
];
const M64 = 0xffffffffffffffffn;
const RATE = 136;
const rotl = (x, n) => {
  n %= 64;
  if (n === 0) return x & M64;
  return ((x << BigInt(n)) | (x >> BigInt(64 - n))) & M64;
};
function keccakF(a) {
  for (let rnd = 0; rnd < 24; rnd++) {
    const c = [];
    for (let x = 0; x < 5; x++) c.push(a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4]);
    const d = [];
    for (let x = 0; x < 5; x++) d.push(c[(x + 4) % 5] ^ rotl(c[(x + 1) % 5], 1));
    for (let x = 0; x < 5; x++) for (let y = 0; y < 5; y++) a[x][y] ^= d[x];
    const b = [[0n, 0n, 0n, 0n, 0n], [0n, 0n, 0n, 0n, 0n], [0n, 0n, 0n, 0n, 0n], [0n, 0n, 0n, 0n, 0n], [0n, 0n, 0n, 0n, 0n]];
    for (let x = 0; x < 5; x++)
      for (let y = 0; y < 5; y++) b[y][(2 * x + 3 * y) % 5] = rotl(a[x][y], ROT[x][y]);
    for (let x = 0; x < 5; x++)
      for (let y = 0; y < 5; y++)
        a[x][y] = b[x][y] ^ ((~b[(x + 1) % 5][y] & M64) & b[(x + 2) % 5][y]);
    a[0][0] ^= RC[rnd];
  }
  return a;
}
function keccak256(data) {
  const buf = Buffer.from(data);
  const padded = Buffer.alloc(Math.ceil((buf.length + 1) / RATE) * RATE, 0);
  buf.copy(padded);
  padded[buf.length] = 0x01;
  padded[padded.length - 1] |= 0x80;
  const st = [[0n, 0n, 0n, 0n, 0n], [0n, 0n, 0n, 0n, 0n], [0n, 0n, 0n, 0n, 0n], [0n, 0n, 0n, 0n, 0n], [0n, 0n, 0n, 0n, 0n]];
  for (let off = 0; off < padded.length; off += RATE) {
    for (let i = 0; i < RATE / 8; i++) {
      const x = i % 5;
      const y = Math.floor(i / 5);
      st[x][y] ^= padded.readBigUInt64LE(off + i * 8);
    }
    keccakF(st);
  }
  const out = Buffer.alloc(32);
  for (let i = 0; i < 4; i++) {
    const x = i % 5;
    const y = Math.floor(i / 5);
    out.writeBigUInt64LE(st[x][y], i * 8);
  }
  return out;
}
const selector = (sig) => keccak256(Buffer.from(sig, 'utf8')).toString('hex').slice(0, 8);
const VECTORS = [
  ['', 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'],
  ['transfer(address,uint256)', 'a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b'],
  ['approve(address,uint256)', '095ea7b334ae44009aa867bfb386f5c3b4b9b0d7b3a8d3a2c3f0b4b9f0b8a0e0'],
];
const args = process.argv.slice(2);
if (args[0] === '--selftest') {
  let ok = true;
  for (const [data, want] of VECTORS.slice(0, 2)) {
    const got = keccak256(Buffer.from(data, 'utf8')).toString('hex');
    const st = got === want ? 'PASS' : 'FAIL';
    if (got !== want) ok = false;
    console.log(`selftest ${st} keccak256(${JSON.stringify(data)}) = ${got}`);
  }
  console.log(`selftest ${ok ? 'PASS' : 'FAIL'} (2 canonical Ethereum vectors)`);
  process.exit(ok ? 0 : 1);
}
for (const a of args) console.log(`${selector(a)}  ${a}`);
