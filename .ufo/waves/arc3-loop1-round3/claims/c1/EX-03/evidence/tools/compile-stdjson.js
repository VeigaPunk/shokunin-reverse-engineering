// arc3-loop1-round3 c1/EX-03 — generic standard-JSON leg driver.
// Usage: node compile-stdjson.js <srcdir> <srckey> <outdir> <on|off>
// <srckey> must equal the path given to solcjs on the CLI leg (metadata input).
const fs = require('fs');
const path = require('path');
const solc = require(path.join(
  '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc'
));

const [srcdir, srckey, outdir, mode] = process.argv.slice(2);
if (!srcdir || !srckey || !outdir || (mode !== 'on' && mode !== 'off')) {
  console.error('usage: node compile-stdjson.js <srcdir> <srckey> <outdir> <on|off>');
  process.exit(64);
}
fs.mkdirSync(outdir, { recursive: true });

const content = fs.readFileSync(path.join(srcdir, srckey), 'utf8');
const settings = {
  outputSelection: {
    '*': {
      '*': [
        'abi',
        'metadata',
        'evm.bytecode.object',
        'evm.bytecode.sourceMap',
        'evm.deployedBytecode.object',
        'evm.deployedBytecode.sourceMap',
        'evm.methodIdentifiers'
      ]
    }
  }
};
if (mode === 'on') settings.optimizer = { enabled: true, runs: 200 };

const input = { language: 'Solidity', sources: { [srckey]: { content } }, settings };
fs.writeFileSync(path.join(outdir, 'solc-input.json'), JSON.stringify(input, null, 2) + '\n');

const out = JSON.parse(solc.compile(JSON.stringify(input)));
const diags = out.errors || [];
for (const d of diags) {
  const line = 'SOLC-' + d.severity.toUpperCase() + ': ' + (d.formattedMessage || d.message);
  console.log(line);
  fs.appendFileSync(path.join(outdir, 'diagnostics.txt'), line + '\n');
}
if (diags.some((d) => d.severity === 'error')) process.exit(2);

// contract name taken from the single contract produced
const contracts = out.contracts[srckey];
const names = Object.keys(contracts);
if (names.length !== 1) { console.error('expected 1 contract, got ' + names.join(',')); process.exit(3); }
const name = names[0];
const c = contracts[name];
fs.writeFileSync(path.join(outdir, name + '.abi.json'), JSON.stringify(c.abi, null, 2) + '\n');
fs.writeFileSync(path.join(outdir, name + '.metadata.json'), c.metadata + '\n');
fs.writeFileSync(path.join(outdir, name + '.creation.hex'), c.evm.bytecode.object + '\n');
fs.writeFileSync(path.join(outdir, name + '.runtime.hex'), c.evm.deployedBytecode.object + '\n');
fs.writeFileSync(path.join(outdir, name + '.methodIdentifiers.json'), JSON.stringify(c.evm.methodIdentifiers, null, 2) + '\n');
const summary =
  'contract ' + name + '\n' +
  'source key ' + srckey + '\n' +
  'optimizer ' + (mode === 'on' ? 'ON runs=200' : 'OFF') + '\n' +
  'solc ' + solc.version() + '\n' +
  'diagnostics ' + diags.length + '\n' +
  'runtime bytes ' + c.evm.deployedBytecode.object.length / 2 + '\n' +
  'creation bytes ' + c.evm.bytecode.object.length / 2 + '\n' +
  'runtime head 32B ' + c.evm.deployedBytecode.object.slice(0, 64) + '\n';
fs.writeFileSync(path.join(outdir, 'summary.txt'), summary);
console.log(summary);