#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const repo = path.resolve(__dirname, '../../../../../../..');
const solc = require(path.join(repo, '.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc'));
const sourcePath = process.argv[2] || path.join(__dirname, 'ViaIRFallback.sol');
const outDir = process.argv[3];
if (!outDir) throw new Error('usage: node compile.js <source.sol> <output-dir>');
const sourceName = path.basename(sourcePath);
const source = fs.readFileSync(sourcePath, 'utf8');
const input = {
  language: 'Solidity',
  sources: { [sourceName]: { content: source } },
  settings: {
    optimizer: { enabled: true, runs: 200 },
    viaIR: true,
    outputSelection: { '*': { '*': ['abi', 'evm.methodIdentifiers', 'evm.bytecode.object', 'evm.deployedBytecode.object', 'evm.deployedBytecode.opcodes'] } },
  },
};
const output = JSON.parse(solc.compile(JSON.stringify(input)));
const errors = (output.errors || []).filter(error => error.severity === 'error');
if (errors.length) throw new Error(errors.map(error => error.formattedMessage).join('\n'));
const contractName = 'ViaIRFallback';
const contract = output.contracts[sourceName][contractName];
const runtime = Buffer.from(contract.evm.deployedBytecode.object, 'hex');
const creation = Buffer.from(contract.evm.bytecode.object, 'hex');
const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'input.json'), JSON.stringify(input, null, 2) + '\n');
fs.writeFileSync(path.join(outDir, 'abi.json'), JSON.stringify(contract.abi, null, 2) + '\n');
fs.writeFileSync(path.join(outDir, 'method-identifiers.json'), JSON.stringify(contract.evm.methodIdentifiers, null, 2) + '\n');
fs.writeFileSync(path.join(outDir, 'runtime.bin'), runtime);
fs.writeFileSync(path.join(outDir, 'runtime.hex'), runtime.toString('hex') + '\n');
fs.writeFileSync(path.join(outDir, 'runtime.opcodes.txt'), contract.evm.deployedBytecode.opcodes + '\n');
fs.writeFileSync(path.join(outDir, 'creation.bin'), creation);
console.log(JSON.stringify({
  solc: solc.version(),
  source: sourceName,
  runtime_bytes: runtime.length,
  runtime_sha256: sha256(runtime),
  creation_bytes: creation.length,
  creation_sha256: sha256(creation),
  method_identifiers: contract.evm.methodIdentifiers,
  abi_entry_kinds: contract.abi.map(entry => entry.type),
}, null, 2));
