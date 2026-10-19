#!/usr/bin/env node
// compile-noopt.js — re-compile EX-04's carrierB.sol with the optimizer OFF,
// reproducing the noopt leg of the cross-seat re-derivation (seat EX-05).
// usage: node compile-noopt.js <solcPrefixDir> <sourceFile> <outDir> <ContractName> <SourceUnitName>
const fs = require('fs');
const crypto = require('crypto');

const [solcPrefix, src, out, name, unit] = process.argv.slice(2);
const solc = require(require('path').resolve(process.cwd(), solcPrefix) + '/node_modules/solc');

const raw = JSON.stringify({
  language: 'Solidity',
  sources: { [unit]: { content: fs.readFileSync(src, 'utf8') } },
  settings: {
    optimizer: { enabled: false },
    outputSelection: { '*': { '*': ['evm.bytecode.object', 'evm.deployedBytecode.object'] } },
  },
});

const o = JSON.parse(solc.compile(raw));
const c = o.contracts[unit][name];
const rt = Buffer.from(c.evm.deployedBytecode.object, 'hex');
const cr = Buffer.from(c.evm.bytecode.object, 'hex');
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(out + '/' + name + '.runtime.hex', c.evm.deployedBytecode.object + '\n');
fs.writeFileSync(out + '/' + name + '.creation.hex', c.evm.bytecode.object + '\n');
console.log(JSON.stringify({
  compiler: solc.version(),
  unit,
  runtimeBytes: rt.length,
  runtimeSha256: crypto.createHash('sha256').update(rt).digest('hex'),
  creationBytes: cr.length,
  creationSha256: crypto.createHash('sha256').update(cr).digest('hex'),
}, null, 2));