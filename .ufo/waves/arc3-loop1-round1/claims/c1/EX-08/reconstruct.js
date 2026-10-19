#!/usr/bin/env node
// EX-08 (chain c1, arc3-loop1-round1) — reconstruction of the r3-07 81-byte
// synthetic dispatcher. The ORIGINAL bytes were elided from every record
// (corpus/knowledge/2026-10-13-r3-evm-interface.md:53-56 elides them; r4
// audit-A records them unrecoverable), so this is a same-shape rebuild:
//   * 81 bytes total
//   * 3 planted ERC-20 selectors: a9059cbb, 70a08231, 095ea7b3
//   * Solidity-style dispatch: DUP1; PUSH4 sel; EQ; PUSH1 dst; JUMPI
//   * JUMPDEST dispatch targets at bytecode offsets 62, 68, 74
//   * minimal ADD/MUL/SUB stub bodies (r3 wording), STOP padding
// Emits r3-07-recon.hex (ASCII hex carrier) and r3-07-recon.bin (raw twin).
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const SELS = ['a9059cbb', '70a08231', '095ea7b3']; // transfer, balanceOf, approve
const DST = ['3e', '44', '4a'];                     // 62, 68, 74
const STUBS = ['01', '02', '03'];                   // ADD, MUL, SUB

const prologue = '60003560e01c';                    // PUSH1 00 CALLDATALOAD PUSH1 e0 SHR (6 B)
// NOTE (EX-08 finding): CALLDATALOAD MUST be at offset 0. EVMole labels the SHR
// result as the selector only when the loaded word's low 4 bytes equal its
// synthetic calldata selector aabbccdd (cdump/evmole src/selectors/mod.rs
// `SHR { args: [_, elabel!(CallData)] }` + src/selectors/calldata.rs
// `selector()`), which only holds for an offset-0 load. `60043560e01c`
// (offset 4) recovers 0 selectors with exit 0 — see variants2/off4.json.
let chain = '';
for (let i = 0; i < 3; i++) chain += `8063${SELS[i]}1460${DST[i]}57`; // 10 B each -> ends at 36
const fallback = '600080fd';                        // PUSH1 00 DUP1 REVERT (4 B) -> ends at 40
const pad = '00'.repeat(22);                        // STOP padding -> first JUMPDEST at 62
const bodies = STUBS.map((s, i) => '5b' + s + '00'.repeat(i === 2 ? 5 : 4)); // 62:6B 68:6B 74:7B

const hex = prologue + chain + fallback + pad + bodies.join('');
if (hex.length !== 162) throw new Error('not 81 bytes: ' + hex.length / 2);

const outDir = __dirname;
fs.writeFileSync(path.join(outDir, 'r3-07-recon.hex'), hex + '\n');
fs.writeFileSync(path.join(outDir, 'r3-07-recon.bin'), Buffer.from(hex, 'hex'));

const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const bytes = Buffer.from(hex, 'hex');
console.log(JSON.stringify({
  bytes: bytes.length,
  hex_sha256: sha(Buffer.from(hex + '\n')),
  bytecode_sha256: sha(bytes),
  r3_recorded_bytecode_sha256_prefix: '3e2fd6ca',
  r3_recorded_bytecode_sha256_suffix: 'fe67',
  differs_from_r3_record: !(sha(bytes).startsWith('3e2fd6ca') && sha(bytes).endsWith('fe67')),
  hex,
}, null, 2));
