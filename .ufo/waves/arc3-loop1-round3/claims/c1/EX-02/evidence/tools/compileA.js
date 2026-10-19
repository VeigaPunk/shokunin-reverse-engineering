// arc3-loop1-round3 c1/EX-02 — standard-JSON compile of carrierA.sol with the
// receipted solc prefix (solc@0.8.37), optimizer enabled, runs=200.
// Resolves solc via NODE_PATH=<prefix>/node_modules.
const fs = require('fs');
const solc = require('solc');

const SRC = '/var/tmp/ex02-r3/src/carrierA.sol';
const OUT = '/var/tmp/ex02-r3/out';

const content = fs.readFileSync(SRC, 'utf8');
const input = {
  language: 'Solidity',
  sources: { 'carrierA.sol': { content } },
  settings: {
    optimizer: { enabled: true, runs: 200 },
    outputSelection: {
      '*': {
        '*': [
          'abi',
          'metadata',
          'evm.bytecode.object',
          'evm.deployedBytecode.object',
          'evm.deployedBytecode.sourceMap',
          'evm.methodIdentifiers'
        ]
      }
    }
  }
};

fs.writeFileSync(OUT + '/carrierA.solc-input.json', JSON.stringify(input, null, 2) + '\n');

const out = JSON.parse(solc.compile(JSON.stringify(input)));
const diags = out.errors || [];
for (const d of diags) {
  console.log('SOLC-' + d.severity.toUpperCase() + ': ' + (d.formattedMessage || d.message));
}
if (diags.some((d) => d.severity === 'error')) process.exit(2);

const c = out.contracts['carrierA.sol']['CarrierA'];
fs.writeFileSync(OUT + '/carrierA.abi.json', JSON.stringify(c.abi, null, 2) + '\n');
fs.writeFileSync(OUT + '/carrierA.metadata.json', c.metadata + '\n');
fs.writeFileSync(OUT + '/carrierA.runtime.hex', c.evm.deployedBytecode.object + '\n');
fs.writeFileSync(OUT + '/carrierA.creation.hex', c.evm.bytecode.object + '\n');
fs.writeFileSync(OUT + '/carrierA.deployed.sourceMap', c.evm.deployedBytecode.sourceMap + '\n');
fs.writeFileSync(OUT + '/carrierA.methodIdentifiers.json', JSON.stringify(c.evm.methodIdentifiers, null, 2) + '\n');
fs.writeFileSync(OUT + '/solc-version.txt', solc.version() + '\n');
fs.writeFileSync(
  OUT + '/compile-stdout.txt',
  'solc.version() = ' + solc.version() + '\n' +
    'diagnostics = ' + diags.length + '\n' +
    'runtime bytes = ' + c.evm.deployedBytecode.object.length / 2 + '\n' +
    'creation bytes = ' + c.evm.bytecode.object.length / 2 + '\n' +
    'abi entries = ' + c.abi.length + '\n'
);
console.log('compile ok; runtime', c.evm.deployedBytecode.object.length / 2, 'B; creation', c.evm.bytecode.object.length / 2, 'B; diagnostics', diags.length);