const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const [solcRoot, evidenceRoot] = process.argv.slice(2);
if (!solcRoot || !evidenceRoot) throw new Error('usage: node rederive.cjs <solc-root> <evidence-root>');
const solc = require(solcRoot);
const sourcePath = path.join(evidenceRoot, 'source', 'ViaIrVault.sol');
const outputDir = path.join(evidenceRoot, 'compiled');
const source = fs.readFileSync(sourcePath, 'utf8');
const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
const sourceName = 'ViaIrVault.sol';
const contractName = 'ViaIrVault';
const input = {
  language: 'Solidity',
  sources: { [sourceName]: { content: source } },
  settings: {
    optimizer: { enabled: true, runs: 200 },
    viaIR: true,
    outputSelection: {
      '*': { '*': ['abi', 'evm.methodIdentifiers', 'evm.bytecode.object', 'evm.deployedBytecode.object'] }
    }
  }
};
const inputText = JSON.stringify(input, null, 2) + '\n';
const first = JSON.parse(solc.compile(JSON.stringify(input)));
const repeated = JSON.parse(solc.compile(JSON.stringify(input)));
const errors = (first.errors || []).filter(item => item.severity === 'error');
if (errors.length) throw new Error(JSON.stringify(errors, null, 2));
const contract = first.contracts[sourceName][contractName];
const repeatedContract = repeated.contracts[sourceName][contractName];
const runtimeHex = contract.evm.deployedBytecode.object.toLowerCase();
const repeatedRuntimeHex = repeatedContract.evm.deployedBytecode.object.toLowerCase();
const runtime = Buffer.from(runtimeHex, 'hex');
const abiFunctions = contract.abi.filter(item => item.type === 'function');
const methodIdentifiers = contract.evm.methodIdentifiers;
const selectors = new Set(Object.values(methodIdentifiers).map(value => value.toLowerCase()));
const cborLength = runtime.readUInt16BE(runtime.length - 2);
const cborStart = runtime.length - 2 - cborLength;
if (cborStart <= 0 || cborStart >= runtime.length) throw new Error('invalid CBOR metadata trailer');
const instructions = [];
for (let pc = 0; pc < cborStart;) {
  const at = pc;
  const opcode = runtime[pc++];
  let immediate = null;
  if (opcode >= 0x60 && opcode <= 0x7f) {
    const width = opcode - 0x5f;
    immediate = runtime.subarray(pc, pc + width);
    if (immediate.length !== width) throw new Error(`truncated PUSH at ${at}`);
    pc += width;
  }
  instructions.push({ pc: at, opcode, immediate: immediate?.toString('hex') ?? null });
}
const selectorSites = [];
for (let index = 0; index < instructions.length; index++) {
  const item = instructions[index];
  if (item.opcode !== 0x63 || !selectors.has(item.immediate)) continue;
  const tail = instructions.slice(index + 1, index + 4);
  const compare = tail[0]?.opcode === 0x14 ? 'EQ' : tail[0]?.opcode === 0x03 ? 'SUB' : null;
  const recognized = compare !== null && tail[1]?.opcode === 0x61 && tail[2]?.opcode === 0x57;
  selectorSites.push({
    pc: item.pc,
    selector: item.immediate,
    compare: recognized ? compare : null,
    destination: recognized ? Number.parseInt(tail[1].immediate, 16) : null
  });
}
const selectorOrder = selectorSites.map(row => row.selector);
const selectorCounts = {
  EQ: selectorSites.filter(row => row.compare === 'EQ').length,
  SUB: selectorSites.filter(row => row.compare === 'SUB').length
};
const allSelectorsLocated = selectorSites.length === selectors.size && new Set(selectorOrder).size === selectors.size;
const ascending = selectorOrder.join(',') === [...selectorOrder].sort().join(',');
const recognized = selectorSites.every(row => row.compare !== null);
const dispatcherClass = allSelectorsLocated && ascending && recognized && selectorCounts.SUB === 1
  ? `ascending selector chain (${selectorCounts.EQ} EQ legs, final selector uses SUB)`
  : allSelectorsLocated && ascending && recognized && selectorCounts.SUB === 0
    ? `ascending selector chain (${selectorCounts.EQ} EQ legs)`
    : 'other measured selector-comparison arrangement';
const metadata = runtime.subarray(cborStart, runtime.length - 2);
const receipt = {
  packageVersion: require(path.join(path.dirname(require.resolve(solcRoot)), 'package.json')).version,
  compilerVersion: solc.version(),
  soljsonSha256: sha256(fs.readFileSync(path.join(path.dirname(require.resolve(solcRoot)), 'soljson.js'))),
  packageJsonSha256: sha256(fs.readFileSync(path.join(path.dirname(require.resolve(solcRoot)), 'package.json'))),
  sourceBytes: Buffer.byteLength(source),
  sourceSha256: sha256(Buffer.from(source)),
  settings: input.settings,
  runtimeBytes: runtime.length,
  runtimeSha256: sha256(runtime),
  creationBytes: Buffer.from(contract.evm.bytecode.object, 'hex').length,
  creationSha256: sha256(Buffer.from(contract.evm.bytecode.object, 'hex')),
  abiFunctionCount: abiFunctions.length,
  receiveEntryCount: contract.abi.filter(item => item.type === 'receive').length,
  fallbackEntryCount: contract.abi.filter(item => item.type === 'fallback').length,
  methodIdentifierCount: Object.keys(methodIdentifiers).length,
  preMetadataCodeBytes: cborStart,
  metadataBytes: cborLength,
  metadataLengthPrefixBytes: 2,
  metadataSolcTag: metadata.subarray(-3).toString('hex'),
  selectorPush4SiteCount: selectorSites.length,
  allSelectorsLocated,
  selectorOrderAscending: ascending,
  selectorCompareCounts: selectorCounts,
  selectorSites,
  dispatcherClass,
  repeatRuntimeEqual: runtimeHex === repeatedRuntimeHex,
  repeatAbiEqual: JSON.stringify(contract.abi) === JSON.stringify(repeatedContract.abi),
  repeatMethodIdentifiersEqual: JSON.stringify(methodIdentifiers) === JSON.stringify(repeatedContract.evm.methodIdentifiers),
  warnings: (first.errors || []).filter(item => item.severity !== 'error').map(item => item.formattedMessage)
};
if (!receipt.repeatRuntimeEqual || !receipt.repeatAbiEqual || !receipt.repeatMethodIdentifiersEqual) {
  throw new Error('same-process repeat compile did not match');
}
fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(path.join(outputDir, 'input.json'), inputText);
fs.writeFileSync(path.join(outputDir, 'output.json'), JSON.stringify(first, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'runtime.bin'), runtime);
fs.writeFileSync(path.join(outputDir, 'runtime.hex'), runtimeHex + '\n');
fs.writeFileSync(path.join(outputDir, 'creation.hex'), contract.evm.bytecode.object.toLowerCase() + '\n');
fs.writeFileSync(path.join(outputDir, 'abi.json'), JSON.stringify(contract.abi, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'method-identifiers.json'), JSON.stringify(methodIdentifiers, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'compile-receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify(receipt, null, 2));
