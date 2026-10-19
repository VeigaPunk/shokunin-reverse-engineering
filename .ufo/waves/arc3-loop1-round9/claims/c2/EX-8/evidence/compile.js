#!/usr/bin/env node
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const [prefix, sourceDir, outDir] = process.argv.slice(2);
if (!prefix || !sourceDir || !outDir) throw new Error('usage: compile.js <solc-prefix> <source-dir> <out-dir>');
const solc = require(path.join(prefix, 'node_modules', 'solc'));
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const variants = [
  ['no-fallback', path.join(sourceDir, 'ViaIrVault.no-fallback.sol')],
  ['payable-fallback', path.join(sourceDir, 'ViaIrVault.fallback.sol')],
];

function build(tag, sourcePath) {
  const source = fs.readFileSync(sourcePath, 'utf8');
  const input = {
    language: 'Solidity',
    sources: { 'ViaIrVault.sol': { content: source } },
    settings: {
      viaIR: true,
      optimizer: { enabled: true, runs: 200 },
      outputSelection: {
        '*': {
          '*': ['abi', 'evm.methodIdentifiers', 'evm.deployedBytecode.object', 'evm.deployedBytecode.opcodes'],
        },
      },
    },
  };
  const results = [];
  for (let pass = 1; pass <= 2; pass += 1) {
    const output = JSON.parse(solc.compile(JSON.stringify(input)));
    const errors = (output.errors ?? []).filter(item => item.severity === 'error');
    if (errors.length) throw new Error(errors.map(item => item.formattedMessage).join('\n'));
    const contract = output.contracts['ViaIrVault.sol'].ViaIrVault;
    results.push({
      runtime: Buffer.from(contract.evm.deployedBytecode.object, 'hex'),
      abi: JSON.stringify(contract.abi, null, 2) + '\n',
      methodIds: JSON.stringify(contract.evm.methodIdentifiers, null, 2) + '\n',
      opcodes: contract.evm.deployedBytecode.opcodes + '\n',
      input: JSON.stringify(input, null, 2) + '\n',
      abiFunctionCount: contract.abi.filter(item => item.type === 'function').length,
      abiFallbackCount: contract.abi.filter(item => item.type === 'fallback').length,
      abiReceiveCount: contract.abi.filter(item => item.type === 'receive').length,
      methodIdCount: Object.keys(contract.evm.methodIdentifiers).length,
      warnings: (output.errors ?? []).filter(item => item.severity !== 'error').map(item => item.formattedMessage.trim()),
    });
  }
  for (const key of ['runtime', 'abi', 'methodIds', 'opcodes', 'input']) {
    if (!results[0][key].equals?.(results[1][key]) && results[0][key] !== results[1][key]) {
      throw new Error(`${tag} compile pass mismatch in ${key}`);
    }
  }
  const result = results[0];
  const dir = path.join(outDir, tag);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'runtime.bin'), result.runtime);
  fs.writeFileSync(path.join(dir, 'runtime.hex'), result.runtime.toString('hex') + '\n');
  fs.writeFileSync(path.join(dir, 'abi.json'), result.abi);
  fs.writeFileSync(path.join(dir, 'method-identifiers.json'), result.methodIds);
  fs.writeFileSync(path.join(dir, 'runtime.opcodes.txt'), result.opcodes);
  fs.writeFileSync(path.join(dir, 'input.json'), result.input);
  return {
    tag,
    source: path.basename(sourcePath),
    source_sha256: sha256(Buffer.from(source)),
    runtime_bytes: result.runtime.length,
    runtime_sha256: sha256(result.runtime),
    abi_functions: result.abiFunctionCount,
    abi_fallback_entries: result.abiFallbackCount,
    abi_receive_entries: result.abiReceiveCount,
    method_identifiers: result.methodIdCount,
    repeat_compile_runtime_identical: true,
    repeat_compile_abi_identical: results[0].abi === results[1].abi,
    warnings: result.warnings,
  };
}

console.log(JSON.stringify({
  compiler: solc.version(),
  soljson_sha256: sha256(fs.readFileSync(path.join(prefix, 'node_modules', 'solc', 'soljson.js'))),
  settings: { viaIR: true, optimizer: { enabled: true, runs: 200 } },
  variants: variants.map(([tag, sourcePath]) => build(tag, sourcePath)),
}, null, 2));
