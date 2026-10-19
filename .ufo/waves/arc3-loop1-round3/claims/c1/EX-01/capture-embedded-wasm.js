#!/usr/bin/env node
// Capture the compiler core embedded in an Emscripten soljson.js.
//
// solc 0.8.37's npm `soljson.js` is a single-file Emscripten build: the wasm
// module is LZ4-compressed, base64-encoded, and assigned to
// Module["wasmBinary"] by the shipped decoder at load time. There is no
// soljson.wasm on disk. This script evaluates the file in a fresh vm context
// with a Proxy standing in for Module, keeps the first large wasmBinary
// assignment (Emscripten overwrites it with undefined later), and reports the
// decoded module's size, magic, sha256, version strings, and the version the
// module itself answers.
//
// usage: capture-embedded-wasm.js <path-to-soljson.js> [out.wasm]
//
// measured 2026-10-19 (wave prefix + ambient fnm tree, byte-identical):
//   22,012,583 bytes | sha256 df14c4e5ee58b27f06b6ce9966d6de6d6382dbe6b43e41a387c9812648afca1e
//   version region contains "commit.f401782d.Emscripten.clang"
//   solidity_version() -> 0.8.37+commit.f401782d.Emscripten.clang

const fs = require('fs');
const vm = require('vm');
const crypto = require('crypto');

const soljsonPath = process.argv[2];
if (!soljsonPath) {
  console.error('usage: capture-embedded-wasm.js <path-to-soljson.js> [out.wasm]');
  process.exit(2);
}
const dir = require('path').dirname(soljsonPath);
const src = fs.readFileSync(soljsonPath, 'utf8');

let captured = null;
const seen = [];
const target = {};
const proxy = new Proxy(target, {
  set(o, k, v) {
    if (k === 'wasmBinary') {
      const len = v && v.length;
      seen.push(len === undefined ? null : len);
      if (!captured && len && len > 1000000) captured = v;
    }
    o[k] = v;
    return true;
  },
  get(o, k) { return o[k]; },
});
const ctx = {
  __dirname: dir, __filename: soljsonPath, Module: proxy, console,
  TextDecoder, TextEncoder, WebAssembly, Buffer, process, require,
  setTimeout, clearTimeout, Math, Date, JSON, Uint8Array, ArrayBuffer,
  Uint32Array, Reflect, Object, String, Number, Array, Error, Function, Promise,
};
vm.createContext(ctx);
vm.runInContext(src, ctx, { timeout: 180000 });

console.log('soljson.js:', Buffer.byteLength(src), 'bytes  sha256:',
            crypto.createHash('sha256').update(src).digest('hex'));
console.log('wasmBinary assignments (lengths):', JSON.stringify(seen));
if (!captured) {
  console.error('no wasmBinary payload captured');
  process.exit(3);
}
const bytes = Buffer.from(new Uint8Array(captured));
const latin = bytes.toString('latin1');
console.log('captured bytes:', bytes.length);
console.log('magic:', JSON.stringify(bytes.slice(0, 8).toString('latin1')));
console.log('embedded wasm sha256:', crypto.createHash('sha256').update(bytes).digest('hex'));
for (const pat of ['0.8.37', 'f401782d', 'Emscripten.clang', 'solidity_version']) {
  console.log(`  ${JSON.stringify(pat)}:`, latin.split(pat).length - 1);
}
const i = latin.indexOf('f401782d');
if (i >= 0) {
  console.log('  version region:', JSON.stringify(bytes.slice(Math.max(0, i - 44), i + 52).toString('latin1')));
}
console.log('solidity_version() from this module:', ctx.Module.cwrap('solidity_version', 'string')());
if (process.argv[3]) {
  fs.writeFileSync(process.argv[3], bytes);
  console.log('wrote', process.argv[3]);
}