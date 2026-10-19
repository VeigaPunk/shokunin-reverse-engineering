// scratch variant: compile a given source file, dump runtime hex + PUSH4 constants.
// usage: node compileVariant.js <src-file> <out-name>
const fs = require('fs');
const solc = require('solc');
const srcPath = process.argv[2];
const name = process.argv[3];
const content = fs.readFileSync(srcPath, 'utf8');
const input = {
  language: 'Solidity',
  sources: { 'carrierA.sol': { content } },
  settings: {
    optimizer: { enabled: true, runs: 200 },
    outputSelection: { '*': { '*': ['evm.deployedBytecode.object'] } }
  }
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
for (const d of out.errors || []) console.log('DIAG', d.severity, d.message);
const hex = out.contracts['carrierA.sol']['CarrierA'].evm.deployedBytecode.object;
fs.writeFileSync('/var/tmp/ex02-r3/out/' + name + '.runtime.hex', hex + '\n');

const buf = Buffer.from(hex, 'hex');
const len1 = (op) => {
  if (op >= 0x60 && op <= 0x7f) return 1 + (op - 0x5f);
  return 1;
};
const seen = new Map();
for (let pc = 0; pc + 4 < buf.length; ) {
  const op = buf[pc];
  if (op === 0x63) {
    const c = buf.slice(pc + 1, pc + 5).toString('hex');
    if (!seen.has(c)) seen.set(c, pc);
  }
  pc += len1(op);
}
console.log(name, 'runtime bytes', buf.length);
for (const [c, pc] of [...seen.entries()].sort((a, b) => a[1] - b[1])) console.log('  pc=' + pc, c);