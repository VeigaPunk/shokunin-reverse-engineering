#!/usr/bin/env node
// RV-1 r3 — keccak path C: solc 0.8.37's compiler-internal keccak, via standard-JSON
// `evm.methodIdentifiers`.  Uses the receipted arc3-loop1-round1 solc prefix (no install).
// Usage: node solc_methodids.js <source.sol> [--optimize [--optimize-runs N]]
const path = require('path');
const fs = require('fs');
const PREFIX = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix';
const solc = require(path.join(PREFIX, 'node_modules/solc'));

const file = process.argv[2];
if (!file) { console.error('usage: node solc_methodids.js <source.sol> [--optimize [--optimize-runs N]]'); process.exit(2); }
const args = process.argv.slice(3);
const optimize = args.includes('--optimize');
const ri = args.indexOf('--optimize-runs');
const runs = ri >= 0 ? parseInt(args[ri + 1], 10) : 200;

const input = {
  language: 'Solidity',
  sources: { [path.basename(file)]: { content: fs.readFileSync(file, 'utf8') } },
  settings: {
    optimizer: { enabled: optimize, runs },
    outputSelection: { '*': { '*': ['abi', 'evm.methodIdentifiers', 'evm.deployedBytecode.object', 'evm.bytecode.object'] } },
  },
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
const errs = (out.errors || []).filter(e => e.severity === 'error');
if (errs.length) { console.error(JSON.stringify(errs, null, 2)); process.exit(1); }
const result = { source: file, solcVersion: solc.version(), optimize, runs, contracts: {} };
for (const [srcName, cs] of Object.entries(out.contracts || {})) {
  for (const [cname, c] of Object.entries(cs)) {
    result.contracts[cname] = {
      methodIdentifiers: c.evm.methodIdentifiers,
      abiFunctions: c.abi.filter(i => i.type === 'function').map(f => `${f.name}(${f.inputs.map(i => i.type).join(',')})`),
      deployedBytecode: c.evm.deployedBytecode.object,
      bytecode: c.evm.bytecode.object,
    };
  }
}
console.log(JSON.stringify(result, null, 2));