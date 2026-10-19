#!/usr/bin/env node
// compile.js — standard-JSON compile driver, arc3-loop1-round3 C1 seat EX-05.
// Route A (primary). Emits creation + runtime bytecode, ABI, metadata, the
// exact solc standard-JSON input used, and a report with derived sha256s.
//
// usage: node compile.js --solc=<prefix>/node_modules/solc --src=<file.sol> \
//         --out=<dir> --contract=<Name> --optimize-runs=200

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function arg(name) {
  const hit = process.argv.slice(2).find((a) => a.startsWith('--' + name + '='));
  return hit === undefined ? undefined : hit.slice(('--' + name + '=').length);
}

const solcPath = arg('solc');
const srcFile = arg('src');
const outDir = arg('out');
const contractName = arg('contract');
const optimizeRuns = parseInt(arg('optimize-runs') || '200', 10);
// sourceName: the source *unit name* recorded in metadata/outputs. Defaults to
// the file's basename (like solc's standard-JSON examples); overridable so a
// route-parity experiment can mirror solcjs CLI's path-as-passed naming.
const sourceNameArg = arg('source-name');

if (!solcPath || !srcFile || !outDir || !contractName) {
  console.error('usage: node compile.js --solc=<mod> --src=<f.sol> --out=<dir> --contract=<Name> [--optimize-runs=200]');
  process.exit(2);
}

const solc = require(path.resolve(process.cwd(), solcPath));
const source = fs.readFileSync(srcFile, 'utf8');
const sourceName = sourceNameArg || path.basename(srcFile);

const input = {
  language: 'Solidity',
  sources: { [sourceName]: { content: source } },
  settings: {
    optimizer: { enabled: true, runs: optimizeRuns },
    outputSelection: {
      '*': {
        '*': [
          'abi',
          'metadata',
          'evm.bytecode.object',
          'evm.deployedBytecode.object',
          'evm.deployedBytecode.immutableReferences',
        ],
      },
    },
  },
};

const raw = JSON.stringify(input, null, 2) + '\n';
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'solc-input.json'), raw);

const output = JSON.parse(solc.compile(raw));

const errors = (output.errors || []).filter((e) => e.severity === 'error');
const warnings = (output.errors || []).filter((e) => e.severity === 'warning');
if (errors.length) {
  console.error('COMPILE ERRORS:\n' + errors.map((e) => e.formattedMessage).join('\n'));
  process.exit(1);
}

const c = output.contracts[sourceName][contractName];
const creationHex = c.evm.bytecode.object;
const runtimeHex = c.evm.deployedBytecode.object;

function sha256hex(s) {
  return crypto.createHash('sha256').update(s).digest('hex');
}
function sha256file(p) {
  return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
}

const files = {
  [`${contractName}.creation.hex`]: creationHex + '\n',
  [`${contractName}.runtime.hex`]: runtimeHex + '\n',
  [`${contractName}.abi.json`]: JSON.stringify(c.abi, null, 2) + '\n',
  [`${contractName}.metadata.json`]: c.metadata + '\n',
};
for (const [name, content] of Object.entries(files)) {
  fs.writeFileSync(path.join(outDir, name), content);
}

const creationBytes = Buffer.from(creationHex, 'hex');
const runtimeBytes = Buffer.from(runtimeHex, 'hex');
const report = {
  seat: 'EX-05',
  route: 'A — solc JS API, solc.compile(standard-JSON)',
  compilerVersion: solc.version(),
  solcModulePath: solcPath,
  sourceFile: path.resolve(srcFile),
  sourceName,
  contract: contractName,
  sourceSha256: sha256hex(source),
  solcInputSha256: sha256hex(raw),
  optimizer: { enabled: true, runs: optimizeRuns },
  evmVersionDefault: true,
  creation: {
    hexChars: creationHex.length,
    bytes: creationBytes.length,
    sha256: sha256hex(creationBytes),
  },
  runtime: {
    hexChars: runtimeHex.length,
    bytes: runtimeBytes.length,
    sha256: sha256hex(runtimeBytes),
  },
  abiFunctions: c.abi.filter((x) => x.type === 'function').length,
  immutableReferences: c.evm.deployedBytecode.immutableReferences || {},
  warnings: warnings.map((w) => w.formattedMessage),
  outputFiles: Object.keys(files).map((f) => ({
    file: f,
    sha256: sha256file(path.join(outDir, f)),
  })),
};
fs.writeFileSync(path.join(outDir, `${contractName}.report.json`), JSON.stringify(report, null, 2) + '\n');

console.log(JSON.stringify({
  version: report.compilerVersion,
  contract: contractName,
  creationBytes: creationBytes.length,
  creationSha256: report.creation.sha256,
  runtimeBytes: runtimeBytes.length,
  runtimeSha256: report.runtime.sha256,
  abiFunctions: report.abiFunctions,
  warnings: report.warnings.length,
}, null, 2));