#!/usr/bin/env node
// EX-10 seat (arc3-loop1-round3): compile VaultB.sol (carrier B) with the
// receipted wave solc prefix, standard-JSON input, two optimizer variants.
// Usage: node compile.js <solcPrefixDir> <sourcePath> <outDir> <opt:0|1> [runs]
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const [prefix, srcPath, outDir, optFlag, runsArg] = process.argv.slice(2);
const runs = runsArg ? parseInt(runsArg, 10) : 200;
const optimizerEnabled = optFlag === '1';
const solc = require(path.join(prefix, 'node_modules', 'solc'));

const src = fs.readFileSync(srcPath, 'utf8');
const input = {
  language: 'Solidity',
  sources: { 'VaultB.sol': { content: src } },
  settings: {
    optimizer: { enabled: optimizerEnabled, runs },
    outputSelection: { '*': { '*': ['abi', 'evm.bytecode.object', 'evm.deployedBytecode.object', 'evm.deployedBytecode.opcodes'] } },
  },
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
if (out.errors) {
  for (const e of out.errors) {
    if (e.severity === 'error') {
      console.error('COMPILE ERROR:', e.formattedMessage);
      process.exit(1);
    }
    console.error('warning:', e.formattedMessage);
  }
}
const c = out.contracts['VaultB.sol']['VaultB'];
const rt = Buffer.from(c.evm.deployedBytecode.object, 'hex');
const cr = Buffer.from(c.evm.bytecode.object, 'hex');
const abi = JSON.stringify(c.abi, null, 2);
fs.mkdirSync(outDir, { recursive: true });
const tag = optimizerEnabled ? `opt${runs}` : 'nopt';
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
function wr(name, data) {
  const p = path.join(outDir, name);
  fs.writeFileSync(p, data);
  console.log(`${sha(Buffer.isBuffer(data) ? data : Buffer.from(data))}  ${p}  (${Buffer.byteLength(data)} B)`);
}
wr(`VaultB.${tag}.runtime.bin`, rt);
wr(`VaultB.${tag}.runtime.hex`, rt.toString('hex'));
wr(`VaultB.${tag}.creation.bin`, cr);
wr(`VaultB.${tag}.creation.hex`, cr.toString('hex'));
wr(`VaultB.${tag}.abi.json`, abi);
wr(`VaultB.${tag}.runtime.opcodes.txt`, c.evm.deployedBytecode.opcodes + '\n');
console.log(JSON.stringify({ tag, solc: solc.version(), runtime_len: rt.length, creation_len: cr.length, sha256_runtime: sha(rt), sha256_creation: sha(cr) }));