const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const solcDir = process.argv[2];
const sourcePath = process.argv[3];
const outDir = process.argv[4];
if (!solcDir || !sourcePath || !outDir) throw new Error('usage: node compile.js <solc-package-dir> <source-path> <out-dir>');
const solc = require(solcDir);
const { keccak_256 } = require('js-sha3');
const source = fs.readFileSync(sourcePath, 'utf8');
const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
const summarize = (tag, extra) => {
  const input = {
    language: 'Solidity',
    sources: { 'ViaIrVault.sol': { content: source } },
    settings: {
      optimizer: { enabled: true, runs: 200 },
      ...extra,
      outputSelection: { '*': { '*': ['abi', 'evm.methodIdentifiers', 'evm.bytecode.object', 'evm.deployedBytecode.object', 'evm.deployedBytecode.opcodes'] } },
    },
  };
  const output = JSON.parse(solc.compile(JSON.stringify(input)));
  const fatal = (output.errors || []).filter(error => error.severity === 'error');
  if (fatal.length) throw new Error(fatal.map(error => error.formattedMessage).join('\n'));
  const contract = output.contracts['ViaIrVault.sol'].ViaIrVault;
  const runtime = Buffer.from(contract.evm.deployedBytecode.object, 'hex');
  const creation = Buffer.from(contract.evm.bytecode.object, 'hex');
  const abiFunctions = contract.abi.filter(item => item.type === 'function');
  const abiSelectors = abiFunctions.map(item => {
    const signature = `${item.name}(${item.inputs.map(input => input.type).join(',')})`;
    return [signature, keccak_256(signature).slice(0, 8)];
  });
  const methodIdentifiers = contract.evm.methodIdentifiers;
  const selectorSet = values => [...new Set(values)].sort();
  const fromAbi = selectorSet(abiSelectors.map(([, selector]) => selector));
  const fromCompiler = selectorSet(Object.values(methodIdentifiers));
  if (JSON.stringify(fromAbi) !== JSON.stringify(fromCompiler)) throw new Error(`${tag}: ABI Keccak set differs from solc methodIdentifiers`);
  const dir = path.join(outDir, tag);
  fs.mkdirSync(dir, { recursive: true });
  const write = (name, data) => fs.writeFileSync(path.join(dir, name), data);
  write('runtime.bin', runtime);
  write('runtime.hex', `${runtime.toString('hex')}\n`);
  write('creation.bin', creation);
  write('creation.hex', `${creation.toString('hex')}\n`);
  write('abi.json', `${JSON.stringify(contract.abi, null, 2)}\n`);
  write('method-identifiers.json', `${JSON.stringify(methodIdentifiers, null, 2)}\n`);
  write('selectors-derived.json', `${JSON.stringify(abiSelectors, null, 2)}\n`);
  write('runtime.opcodes.txt', `${contract.evm.deployedBytecode.opcodes}\n`);
  write('input.json', `${JSON.stringify(input, null, 2)}\n`);
  write('compiler-output.json', `${JSON.stringify(output)}\n`);
  console.log(JSON.stringify({
    tag,
    compiler: solc.version(),
    warnings: (output.errors || []).filter(error => error.severity !== 'error').length,
    runtime_bytes: runtime.length,
    runtime_sha256: sha256(runtime),
    creation_bytes: creation.length,
    creation_sha256: sha256(creation),
    abi_function_count: abiFunctions.length,
    method_identifier_count: Object.keys(methodIdentifiers).length,
    distinct_selectors: fromAbi.length,
    runtime_head_hex: runtime.subarray(0, 128).toString('hex'),
    selectors: abiSelectors,
  }));
};
summarize('viair-opt200', { viaIR: true });
summarize('std-opt200', {});
console.log(JSON.stringify({ source_sha256: sha256(source), solc: solc.version() }));
