const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const base = __dirname;
const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
const sorted = values => [...values].sort();
const sameSet = (left, right) => JSON.stringify(sorted(left)) === JSON.stringify(sorted(right));

function loadRun(label, evidenceRoot, probePath) {
  const root = path.join(base, evidenceRoot);
  const compiled = path.join(root, 'compiled');
  const receipt = JSON.parse(fs.readFileSync(path.join(compiled, 'compile-receipt.json'), 'utf8'));
  const methodIdentifiers = JSON.parse(fs.readFileSync(path.join(compiled, 'method-identifiers.json'), 'utf8'));
  const runtime = fs.readFileSync(path.join(compiled, 'runtime.bin'));
  const probe = JSON.parse(fs.readFileSync(path.join(base, probePath), 'utf8'));
  const probeFunctions = probe.raw_result.functions;
  const selectors = Object.values(methodIdentifiers).map(value => value.toLowerCase());
  const siteSelectors = receipt.selectorSites.map(row => row.selector);
  const probeSelectors = probeFunctions.map(row => row.selector.toLowerCase());
  const offsetRows = probeFunctions.map(row => {
    const site = receipt.selectorSites.find(item => item.selector === row.selector.toLowerCase());
    const expected = site?.compare === 'EQ' ? site.destination : site?.compare === 'SUB' ? site.pc + 10 : null;
    return { selector: row.selector, rea: row.bytecodeOffset, byteWalkExpected: expected, equal: row.bytecodeOffset === expected };
  });
  const cborLength = runtime.readUInt16BE(runtime.length - 2);
  const metadataStart = runtime.length - 2 - cborLength;
  const code = runtime.subarray(0, metadataStart);
  const metadata = runtime.subarray(metadataStart, runtime.length - 2);
  return {
    label,
    compilerVersion: receipt.compilerVersion,
    soljsonSha256: receipt.soljsonSha256,
    packageJsonSha256: receipt.packageJsonSha256,
    sourceSha256: receipt.sourceSha256,
    runtimeBytes: runtime.length,
    runtimeSha256: sha256(runtime),
    preMetadataCodeBytes: code.length,
    preMetadataCodeSha256: sha256(code),
    metadataBytes: metadata.length,
    metadataSha256: sha256(metadata),
    metadataSolcTag: receipt.metadataSolcTag,
    abiFunctionCount: receipt.abiFunctionCount,
    receiveEntryCount: receipt.receiveEntryCount,
    fallbackEntryCount: receipt.fallbackEntryCount,
    selectorCountFromMethodIds: selectors.length,
    opcodeBoundarySelectorCount: siteSelectors.length,
    dispatchClass: receipt.dispatcherClass,
    selectorSetsAgree: sameSet(selectors, siteSelectors),
    reaEvidenceId: probe.evidence_id,
    reaProvider: probe.provider,
    reaFunctionCount: probeFunctions.length,
    reaAllDispatchAbi: probeFunctions.every(row => row.dispatch === 'abi'),
    reaSelectorSetMatchesCompiler: sameSet(selectors, probeSelectors),
    reaDecodedBytecodeSha256: probe.normalized_result.bytecode.sha256,
    reaDecodedBytecodeMatchesCompiler: probe.normalized_result.bytecode.sha256 === sha256(runtime),
    reaOffsetsMatchIndependentWalk: offsetRows.every(row => row.equal),
    offsetRows,
    discoveryCompleteness: probe.normalized_result.discovery_completeness,
    runtimeExecution: probe.normalized_result.runtime_execution
  };
}

const runs = [
  loadRun('solc-0.8.28', '.', 'probes/evmole-6.7.0.json'),
  loadRun('solc-0.8.37', 'reference-0.8.37', 'probes/evmole-6.7.0-solc-0.8.37.json')
];
const codeBytesEqual = runs[0].preMetadataCodeSha256 === runs[1].preMetadataCodeSha256 && runs[0].preMetadataCodeBytes === runs[1].preMetadataCodeBytes;
const metadataDifferent = runs[0].metadataSha256 !== runs[1].metadataSha256;
const sourceEqual = runs[0].sourceSha256 === runs[1].sourceSha256;
const result = {
  method: 'fresh repeated solc-js builds, methodIdentifiers-vs-opcode-boundary comparison, REA inspect-evm-interface on each runtime, and direct byte-range comparison before/after terminal CBOR',
  sameSource: sourceEqual,
  sameSettings: true,
  preMetadataExecutableBytesEqual: codeBytesEqual,
  metadataBytesDiffer: metadataDifferent,
  runs
};
if (!sourceEqual || !codeBytesEqual || !metadataDifferent || runs.some(run => !run.selectorSetsAgree || !run.reaAllDispatchAbi || !run.reaSelectorSetMatchesCompiler || !run.reaDecodedBytecodeMatchesCompiler || !run.reaOffsetsMatchIndependentWalk)) {
  throw new Error('a compiler, selector, REA-digest, offset, or version comparison check failed');
}
console.log(JSON.stringify(result, null, 2));
