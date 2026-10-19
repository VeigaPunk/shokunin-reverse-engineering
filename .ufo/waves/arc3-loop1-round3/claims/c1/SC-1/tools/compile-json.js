// SC-1 arc3-loop1-round3 reference compile harness (scratch).
// Usage: node compile-json.js <source.sol> <ContractName> <outdir> <opt0|opt200>
const solc = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc');
const fs = require('fs');
const path = require('path');

const [srcPath, contractName, outdir, mode] = process.argv.slice(2);
const source = fs.readFileSync(srcPath, 'utf8');
const settings = {
  outputSelection: { '*': { '*': ['abi', 'metadata', 'evm.methodIdentifiers', 'evm.bytecode.object', 'evm.deployedBytecode.object'] } }
};
if (mode === 'opt200') settings.optimizer = { enabled: true, runs: 200 };
else settings.optimizer = { enabled: false };

const input = { language: 'Solidity', sources: { [path.basename(srcPath)]: { content: source } }, settings };
const out = JSON.parse(solc.compile(JSON.stringify(input)));
const fatal = (out.errors || []).filter(e => e.severity === 'error');
for (const e of out.errors || []) console.error('solc:', e.severity, e.formattedMessage);
if (fatal.length) process.exit(1);

const c = out.contracts[path.basename(srcPath)][contractName];
const runtimeHex = c.evm.deployedBytecode.object;
const creationHex = c.evm.bytecode.object;
fs.mkdirSync(outdir, { recursive: true });
const base = path.join(outdir, contractName + '.' + mode);
fs.writeFileSync(base + '.runtime.hex', runtimeHex + '\n');
fs.writeFileSync(base + '.runtime.bin', Buffer.from(runtimeHex, 'hex'));
fs.writeFileSync(base + '.creation.hex', creationHex + '\n');
fs.writeFileSync(base + '.creation.bin', Buffer.from(creationHex, 'hex'));
fs.writeFileSync(base + '.abi.json', JSON.stringify(c.abi, null, 2));
fs.writeFileSync(base + '.methodIdentifiers.json', JSON.stringify(c.evm.methodIdentifiers, null, 2));
console.log(JSON.stringify({
  solc: solc.version(),
  mode,
  contract: contractName,
  runtime_bytes: runtimeHex.length / 2,
  creation_bytes: creationHex.length / 2,
  methodIdentifiers: Object.keys(c.evm.methodIdentifiers).length,
  output_base: base
}, null, 1));