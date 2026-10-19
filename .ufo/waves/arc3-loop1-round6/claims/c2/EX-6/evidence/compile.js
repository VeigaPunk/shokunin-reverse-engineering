#!/usr/bin/env node
// EX-6 seat (arc3-loop1-round6): compile ViaIRVault.sol with the receipted
// wave-1 solc prefix (reuse, no new install), standard-JSON input, three
// variants: viaIR nopt, viaIR opt200, legacy opt200 control.
// Usage: node compile.js <solcPrefixDir> <srcPath> <outDir> <tag> <viaIR:0|1> <opt:0|1> [runs]
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const [prefix, srcPath, outDir, tag, viaIRFlag, optFlag, runsArg] = process.argv.slice(2);
const runs = runsArg ? parseInt(runsArg, 10) : 200;
const viaIR = viaIRFlag === '1';
const optimizerEnabled = optFlag === '1';
const solc = require(path.join(prefix, 'node_modules', 'solc'));

const src = fs.readFileSync(srcPath, 'utf8');
const input = {
  language: 'Solidity',
  sources: { 'ViaIRVault.sol': { content: src } },
  settings: {
    viaIR,
    optimizer: { enabled: optimizerEnabled, runs },
    outputSelection: { '*': { '*': ['abi', 'evm.bytecode.object', 'evm.deployedBytecode.object', 'evm.deployedBytecode.opcodes', 'evm.methodIdentifiers'] } },
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
const c = out.contracts['ViaIRVault.sol']['ViaIRVault'];
const rt = Buffer.from(c.evm.deployedBytecode.object, 'hex');
const cr = Buffer.from(c.evm.bytecode.object, 'hex');
const abi = JSON.stringify(c.abi, null, 2);
const mid = JSON.stringify(c.evm.methodIdentifiers, null, 2);
fs.mkdirSync(outDir, { recursive: true });
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
function wr(name, data) {
  const p = path.join(outDir, name);
  fs.writeFileSync(p, data);
  console.log(`${sha(Buffer.isBuffer(data) ? data : Buffer.from(data))}  ${p}  (${Buffer.byteLength(data)} B)`);
}
wr(`ViaIRVault.${tag}.runtime.bin`, rt);
wr(`ViaIRVault.${tag}.runtime.hex`, rt.toString('hex'));
wr(`ViaIRVault.${tag}.creation.bin`, cr);
wr(`ViaIRVault.${tag}.creation.hex`, cr.toString('hex'));
wr(`ViaIRVault.${tag}.abi.json`, abi);
wr(`ViaIRVault.${tag}.methodIdentifiers.json`, mid);
wr(`ViaIRVault.${tag}.runtime.opcodes.txt`, c.evm.deployedBytecode.opcodes + '\n');
console.log(JSON.stringify({ tag, viaIR, optimizerEnabled, runs, solc: solc.version(), runtime_len: rt.length, creation_len: cr.length, sha256_runtime: sha(rt), sha256_creation: sha(cr) }));
