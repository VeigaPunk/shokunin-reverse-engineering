#!/usr/bin/env node
// EX-6 verification rig: independent compile of a source under three legs.
// Usage: node compile3.js <solcPrefixDir> <srcPath> <contract> <outDir>
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const [prefix, srcPath, contract, outDir] = process.argv.slice(2);
const solc = require(path.join(prefix, 'node_modules', 'solc'));
const src = fs.readFileSync(srcPath, 'utf8');
const sha = b => crypto.createHash('sha256').update(b).digest('hex');

function compile(tag, extra) {
  const input = {
    language: 'Solidity',
    sources: { [path.basename(srcPath)]: { content: src } },
    settings: Object.assign({
      optimizer: { enabled: true, runs: 200 },
      outputSelection: { '*': { '*': ['abi', 'evm.methodIdentifiers', 'evm.bytecode.object',
        'evm.deployedBytecode.object', 'evm.deployedBytecode.opcodes'] } },
    }, extra),
  };
  const out = JSON.parse(solc.compile(JSON.stringify(input)));
  if (out.errors) for (const e of out.errors) console.error(e.severity.toUpperCase() + ': ' + e.formattedMessage.trim());
  const c = out.contracts[path.basename(srcPath)][contract];
  const rt = Buffer.from(c.evm.deployedBytecode.object, 'hex');
  const cr = Buffer.from(c.evm.bytecode.object, 'hex');
  const d = path.join(outDir, tag); fs.mkdirSync(d, { recursive: true });
  fs.writeFileSync(path.join(d, 'runtime.bin'), rt);
  fs.writeFileSync(path.join(d, 'runtime.hex'), rt.toString('hex') + '\n');
  fs.writeFileSync(path.join(d, 'creation.bin'), cr);
  fs.writeFileSync(path.join(d, 'creation.hex'), cr.toString('hex') + '\n');
  fs.writeFileSync(path.join(d, 'abi.json'), JSON.stringify(c.abi, null, 2) + '\n');
  fs.writeFileSync(path.join(d, 'method-identifiers.json'), JSON.stringify(c.evm.methodIdentifiers, null, 2) + '\n');
  fs.writeFileSync(path.join(d, 'runtime.opcodes.txt'), c.evm.deployedBytecode.opcodes + '\n');
  console.log(JSON.stringify({ tag, solc: solc.version(), runtime_len: rt.length,
    creation_len: cr.length, sha256_runtime: sha(rt), sha256_creation: sha(cr),
    sha256_abi: sha(fs.readFileSync(path.join(d, 'abi.json'))),
    sha256_methods: sha(fs.readFileSync(path.join(d, 'method-identifiers.json'))),
    n_functions: c.abi.filter(x => x.type === 'function').length }));
}
compile('viair-opt200', { viaIR: true });
compile('viair-noopt', { viaIR: true, optimizer: { enabled: false } });
compile('std-opt200', {});
