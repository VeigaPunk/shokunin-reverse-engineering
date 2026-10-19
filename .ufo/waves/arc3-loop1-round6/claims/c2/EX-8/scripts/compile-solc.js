#!/usr/bin/env node
// EX-8 independent driver: rebuild the standard-JSON input from the carrier
// source, compile three legs with the pinned solc, dump artifacts.
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const prefix = process.argv[2], srcPath = process.argv[3], outDir = process.argv[4];
const solc = require(path.join(prefix, 'node_modules', 'solc'));
const src = fs.readFileSync(srcPath, 'utf8');
const SEL = { '*': { '*': ['abi', 'evm.methodIdentifiers', 'evm.bytecode.object',
  'evm.deployedBytecode.object', 'evm.deployedBytecode.opcodes'] } };
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
for (const [tag, extra] of [
  ['viair-opt200', { viaIR: true, optimizer: { enabled: true, runs: 200 } }],
  ['viair-noopt', { viaIR: true, optimizer: { enabled: false } }],
  ['std-opt200', { optimizer: { enabled: true, runs: 200 } }],
]) {
  const input = { language: 'Solidity', sources: { 'ViaIrVault.sol': { content: src } },
                  settings: Object.assign({ optimizer: { enabled: true, runs: 200 }, outputSelection: SEL }, extra) };
  const res = JSON.parse(solc.compile(JSON.stringify(input)));
  if (res.errors) for (const e of res.errors) if (e.severity === 'error') { console.error(e.formattedMessage); process.exit(1); }
  const c = res.contracts['ViaIrVault.sol']['ViaIrVault'];
  const rt = Buffer.from(c.evm.deployedBytecode.object, 'hex'), cr = Buffer.from(c.evm.bytecode.object, 'hex');
  const d = path.join(outDir, tag); fs.mkdirSync(d, { recursive: true });
  fs.writeFileSync(path.join(d, 'runtime.bin'), rt);
  fs.writeFileSync(path.join(d, 'runtime.hex'), rt.toString('hex') + '\n');
  fs.writeFileSync(path.join(d, 'creation.bin'), cr);
  fs.writeFileSync(path.join(d, 'abi.json'), JSON.stringify(c.abi, null, 2) + '\n');
  fs.writeFileSync(path.join(d, 'method-identifiers.json'), JSON.stringify(c.evm.methodIdentifiers, null, 2) + '\n');
  fs.writeFileSync(path.join(d, 'opcodes.txt'), c.evm.deployedBytecode.opcodes + '\n');
  console.log(JSON.stringify({ tag, solc: solc.version(), runtime_len: rt.length, creation_len: cr.length,
    sha256_runtime: sha(rt), sha256_creation: sha(cr), abi_entries: c.abi.filter(x => x.type === 'function').length }));
}
