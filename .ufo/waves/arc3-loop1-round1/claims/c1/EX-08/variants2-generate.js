#!/usr/bin/env node
// EX-08 variants2: mechanism-control matrix isolating the prologue requirement.
// Each carrier is a minimal 3-selector dispatcher: prologue + 3 x
// `DUP1 PUSH4 sel EQ PUSH1 dst JUMPI` + `PUSH1 00 DUP1 REVERT` fallback +
// JUMPDEST stub bodies (ADD/MUL/SUB) right after the fallback.
//   off0      60003560e01c  PUSH1 00 CALLDATALOAD  -> 3/3 recovered
//   off4      60043560e01c  PUSH1 04 CALLDATALOAD  -> 0 recovered (exit 0)
//   push0     5f3560e01c    PUSH0 CALLDATALOAD     -> 3/3 recovered (solc 0.8.x form)
//   off0-body7 60003560e01c, 7-byte bodies          -> 3/3, r4-audit-style layout
const fs = require('fs');
const path = require('path');
const SELS = ['a9059cbb', '70a08231', '095ea7b3'];
const STUBS = ['01', '02', '03'];
const OUT = path.join(__dirname, 'variants2');
fs.mkdirSync(OUT, { recursive: true });

function build(prologue, bodySize) {
  const head = prologue + SELS.map(s => `8063${s}14600057`).join('') + '600080fd';
  const t0 = head.length / 2;
  const targets = [t0, t0 + bodySize, t0 + 2 * bodySize];
  const dst = targets.map(t => t.toString(16).padStart(2, '0'));
  const chain = SELS.map((s, i) => `8063${s}1460${dst[i]}57`).join('');
  const bodies = SELS.map((s, i) => '5b' + STUBS[i] + '00'.repeat(bodySize - 2)).join('');
  const hex = prologue + chain + '600080fd' + bodies;
  return { hex, targets };
}

const specs = [
  ['off0', '60003560e01c', 6],
  ['off4', '60043560e01c', 6],
  ['push0', '5f3560e01c', 6],
  ['off0-body7', '60003560e01c', 7],
];
for (const [name, pro, size] of specs) {
  const { hex, targets } = build(pro, size);
  fs.writeFileSync(path.join(OUT, name + '.hex'), hex + '\n');
  console.log(name, hex.length / 2, 'bytes', 'targets', targets.join('/'));
}
