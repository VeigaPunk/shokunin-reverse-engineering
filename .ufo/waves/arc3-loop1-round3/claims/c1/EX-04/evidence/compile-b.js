// compile-b.js — carrier B compile driver (arc3-loop1-round3, chain c1, EX-04)
// usage: node compile-b.js <srcPath> <outDir> <opt200|noopt>
const fs = require('fs');
const crypto = require('crypto');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);

const [srcPath, outDir, mode] = process.argv.slice(2);
if (!srcPath || !outDir || !['opt200', 'noopt'].includes(mode)) {
  console.error('usage: node compile-b.js <srcPath> <outDir> <opt200|noopt>');
  process.exit(2);
}
fs.mkdirSync(outDir, { recursive: true });

const src = fs.readFileSync(srcPath, 'utf8');
const settings = {
  outputSelection: {
    '*': {
      '*': ['abi', 'metadata', 'evm.bytecode.object', 'evm.deployedBytecode.object', 'evm.methodIdentifiers'],
    },
  },
};
if (mode === 'opt200') settings.optimizer = { enabled: true, runs: 200 };
const input = { language: 'Solidity', sources: { 'carrierB.sol': { content: src } }, settings };

const inputText = JSON.stringify(input, null, 1);
fs.writeFileSync(`${outDir}/solc-input-${mode}.json`, inputText);

const raw = solc.compile(JSON.stringify(input));
// solcjs may prefix stdout with a ">>> ..." SMT-retry line (PL-1 F3, r1); strip to the JSON object.
const jsonText = raw.slice(raw.indexOf('{'));
let out;
try {
  out = JSON.parse(jsonText);
} catch (e) {
  fs.writeFileSync(`${outDir}/compile-${mode}.raw.txt`, raw);
  console.error('JSON.parse failed; raw stdout saved');
  process.exit(1);
}
const errors = (out.errors || []).map((e) => `${e.severity}: ${e.formattedMessage}`);
const fatal = (out.errors || []).some((e) => e.severity === 'error');
if (fatal) {
  console.error(errors.join('\n'));
  process.exit(1);
}

const c = out.contracts['carrierB.sol']['VaultB'];
const runtimeHex = c.evm.deployedBytecode.object;
const creationHex = c.evm.bytecode.object;
const abi = c.abi;
const methodIdentifiers = c.evm.methodIdentifiers;
const metadata = JSON.parse(c.metadata);

fs.writeFileSync(`${outDir}/carrierB.runtime-${mode}.hex`, runtimeHex + '\n');
fs.writeFileSync(`${outDir}/carrierB.creation-${mode}.hex`, creationHex + '\n');
fs.writeFileSync(`${outDir}/carrierB.runtime-${mode}.bin`, Buffer.from(runtimeHex, 'hex'));
fs.writeFileSync(`${outDir}/carrierB.creation-${mode}.bin`, Buffer.from(creationHex, 'hex'));
fs.writeFileSync(`${outDir}/carrierB.abi-${mode}.json`, JSON.stringify(abi, null, 2));
fs.writeFileSync(`${outDir}/methodIdentifiers-${mode}.json`, JSON.stringify(methodIdentifiers, null, 2));
fs.writeFileSync(`${outDir}/metadata-${mode}.json`, JSON.stringify(metadata, null, 2));

const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const summary = {
  seat: 'EX-04 (chain c1, executor)',
  wave: 'arc3-loop1-round3',
  mode,
  solc_version: solc.version(),
  optimizer: settings.optimizer || { enabled: false },
  evmVersion_metadata: metadata.settings.evmVersion,
  source_sha256: sha(srcPath),
  compiler_warnings: errors.filter((e) => e.startsWith('warning')).length,
  compiler_warning_texts: errors.filter((e) => e.startsWith('warning')),
  runtime_bytes: runtimeHex.length / 2,
  creation_bytes: creationHex.length / 2,
  runtime_sha256: sha(`${outDir}/carrierB.runtime-${mode}.bin`),
  creation_sha256: sha(`${outDir}/carrierB.creation-${mode}.bin`),
  abi_sha256: sha(`${outDir}/carrierB.abi-${mode}.json`),
  abi_functions: abi
    .filter((a) => a.type === 'function')
    .map((a) => ({ sig: `${a.name}(${a.inputs.map((i) => i.type).join(',')})`, mutability: a.stateMutability }))
    .sort((a, b) => a.sig.localeCompare(b.sig)),
  method_identifiers: methodIdentifiers,
  method_identifiers_count: Object.keys(methodIdentifiers).length,
};
fs.writeFileSync(`${outDir}/compile-summary-${mode}.json`, JSON.stringify(summary, null, 2));
console.log(JSON.stringify(summary, null, 1));