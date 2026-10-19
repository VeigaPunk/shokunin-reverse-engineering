#!/usr/bin/env node
// EX-11 (arc3-loop1-round6) independent compile: same standard-JSON contract,
// own script, no reuse of EX-7's compile.js.
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const solc = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc');
const [srcPath, name, outDir, mode] = process.argv.slice(2);
const src = fs.readFileSync(srcPath, 'utf8');
const extra = {
  'viair-opt200': { viaIR: true, optimizer: { enabled: true, runs: 200 } },
  'viair-noopt':  { viaIR: true, optimizer: { enabled: false } },
  'std-opt200':   { optimizer: { enabled: true, runs: 200 } },
}[mode];
const input = {
  language: 'Solidity',
  sources: { [path.basename(srcPath)]: { content: src } },
  settings: Object.assign({
    outputSelection: { '*': { '*': ['abi','evm.methodIdentifiers','evm.bytecode.object','evm.deployedBytecode.object','evm.deployedBytecode.opcodes'] } },
  }, extra),
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
let fatal = false;
for (const e of (out.errors||[])) { if (e.severity === 'error') { fatal = true; console.error(e.formattedMessage); } }
if (fatal) process.exit(1);
const c = out.contracts[path.basename(srcPath)][name];
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const rt = Buffer.from(c.evm.deployedBytecode.object, 'hex');
const cr = Buffer.from(c.evm.bytecode.object, 'hex');
fs.mkdirSync(path.join(outDir, mode), { recursive: true });
fs.writeFileSync(path.join(outDir, mode, 'runtime.bin'), rt);
fs.writeFileSync(path.join(outDir, mode, 'runtime.hex'), rt.toString('hex') + '\n');
fs.writeFileSync(path.join(outDir, mode, 'creation.bin'), cr);
fs.writeFileSync(path.join(outDir, mode, 'abi.json'), JSON.stringify(c.abi, null, 2));
fs.writeFileSync(path.join(outDir, mode, 'method-identifiers.json'), JSON.stringify(c.evm.methodIdentifiers, null, 2));
fs.writeFileSync(path.join(outDir, mode, 'runtime.opcodes.txt'), c.evm.deployedBytecode.opcodes);
console.log(JSON.stringify({contract:name, mode, solc:solc.version(), runtime_len:rt.length, creation_len:cr.length, sha256_runtime:sha(rt), sha256_creation:sha(cr), sha256_abi:sha(JSON.stringify(c.abi,null,2)), K:Object.keys(c.evm.methodIdentifiers).length}));
