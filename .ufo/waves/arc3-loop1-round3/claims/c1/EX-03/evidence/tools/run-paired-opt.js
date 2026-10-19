// arc3-loop1-round3 c1/EX-03 — paired optimizer leg for carrier A.
// Usage: node run-paired-opt.js off   (or on)
// Same compiler, same source unit name, same outputSelection as the main leg;
// only settings.optimizer differs. Used to measure the optimizer-enabled
// dispatch-shape delta for the SAME carrier source.
const fs = require('fs');
const path = require('path');
const solc = require(path.join(
  '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc'
));

const mode = process.argv[2];
if (mode !== 'off' && mode !== 'on') { console.error('usage: node run-paired-opt.js off|on'); process.exit(64); }
const enabled = mode === 'on';

const S = '/var/tmp/ex03-r3';
const SRC = S + '/a/carrierA.sol';
const OUT = S + '/a-stdjson-opt-' + mode;
fs.mkdirSync(OUT, { recursive: true });

const content = fs.readFileSync(SRC, 'utf8');
const settings = {
  outputSelection: {
    '*': {
      '*': [
        'abi',
        'metadata',
        'evm.bytecode.object',
        'evm.deployedBytecode.object',
        'evm.methodIdentifiers'
      ]
    }
  }
};
if (enabled) settings.optimizer = { enabled: true, runs: 200 };

const input = { language: 'Solidity', sources: { 'carrierA.sol': { content } }, settings };
fs.writeFileSync(OUT + '/carrierA.solc-input.json', JSON.stringify(input, null, 2) + '\n');

const out = JSON.parse(solc.compile(JSON.stringify(input)));
const diags = out.errors || [];
for (const d of diags) console.log('SOLC-' + d.severity.toUpperCase() + ': ' + (d.formattedMessage || d.message));
if (diags.some((d) => d.severity === 'error')) process.exit(2);

const c = out.contracts['carrierA.sol']['CarrierA'];
fs.writeFileSync(OUT + '/carrierA.abi.json', JSON.stringify(c.abi, null, 2) + '\n');
fs.writeFileSync(OUT + '/carrierA.creation.hex', c.evm.bytecode.object + '\n');
fs.writeFileSync(OUT + '/carrierA.runtime.hex', c.evm.deployedBytecode.object + '\n');
fs.writeFileSync(OUT + '/carrierA.methodIdentifiers.json', JSON.stringify(c.evm.methodIdentifiers, null, 2) + '\n');
const runtimeBytes = c.evm.deployedBytecode.object.length / 2;
const creationBytes = c.evm.bytecode.object.length / 2;
const summary =
  'optimizer=' + (enabled ? 'ON runs=200' : 'OFF') + '\n' +
  'solc.version() = ' + solc.version() + '\n' +
  'diagnostics = ' + diags.length + '\n' +
  'runtime bytes = ' + runtimeBytes + '\n' +
  'creation bytes = ' + creationBytes + '\n' +
  'runtime head (first 32 B) = ' + c.evm.deployedBytecode.object.slice(0, 64) + '\n';
fs.writeFileSync(OUT + '/summary.txt', summary);
console.log(summary);