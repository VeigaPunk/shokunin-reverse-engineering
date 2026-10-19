#!/usr/bin/env node
// EX-7 seat (arc3-loop1-round6): compile ViaIrVault.sol with the receipted
// wave-1 solc prefix, standard-JSON input, three legs:
//   viair-opt200 : viaIR:true  + optimizer {enabled:true, runs:200}   (primary)
//   viair-noopt  : viaIR:true  + optimizer {enabled:false}            (secondary)
//   std-opt200   : viaIR unset + optimizer {enabled:true, runs:200}   (control)
// Usage: node compile.js <solcPrefixDir> <srcPath> <outDir>
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const [prefix, srcPath, outDir] = process.argv.slice(2);
const solc = require(path.join(prefix, 'node_modules', 'solc'));
const src = fs.readFileSync(srcPath, 'utf8');

function compile(tag, extra) {
  const input = {
    language: 'Solidity',
    sources: { 'ViaIrVault.sol': { content: src } },
    settings: Object.assign({
      optimizer: { enabled: true, runs: 200 },
      outputSelection: { '*': { '*': ['abi', 'evm.methodIdentifiers', 'evm.bytecode.object',
        'evm.deployedBytecode.object', 'evm.deployedBytecode.opcodes'] } },
    }, extra),
  };
  const raw = solc.compile(JSON.stringify(input));
  const out = JSON.parse(raw);
  if (out.errors) {
    let fatal = false;
    for (const e of out.errors) {
      if (e.severity === 'error') { console.error('COMPILE ERROR:', e.formattedMessage); fatal = true; }
      else console.error('warning:', e.formattedMessage.trim());
    }
    if (fatal) process.exit(1);
  }
  const c = out.contracts['ViaIrVault.sol']['ViaIrVault'];
  const rt = Buffer.from(c.evm.deployedBytecode.object, 'hex');
  const cr = Buffer.from(c.evm.bytecode.object, 'hex');
  fs.mkdirSync(path.join(outDir, tag), { recursive: true });
  const sha = b => crypto.createHash('sha256').update(b).digest('hex');
  const wr = (name, data) => {
    const p = path.join(outDir, tag, name);
    fs.writeFileSync(p, data);
    console.log(`${sha(Buffer.isBuffer(data) ? data : Buffer.from(data))}  ${tag}/${name}  (${Buffer.byteLength(data)} B)`);
  };
  wr('runtime.bin', rt);
  wr('runtime.hex', rt.toString('hex') + '\n');
  wr('creation.bin', cr);
  wr('creation.hex', cr.toString('hex') + '\n');
  wr('abi.json', JSON.stringify(c.abi, null, 2) + '\n');
  wr('method-identifiers.json', JSON.stringify(c.evm.methodIdentifiers, null, 2) + '\n');
  wr('runtime.opcodes.txt', c.evm.deployedBytecode.opcodes + '\n');
  wr('input.json', JSON.stringify(input, null, 2) + '\n');
  console.log(JSON.stringify({ tag, solc: solc.version(), runtime_len: rt.length,
    creation_len: cr.length, sha256_runtime: sha(rt), sha256_creation: sha(cr) }));
}

compile('viair-opt200', { viaIR: true });
compile('viair-noopt', { viaIR: true, optimizer: { enabled: false } });
compile('std-opt200', {});
