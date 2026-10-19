const fs = require('fs');
const path = require('path');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);
const crypto = require('crypto');
const WORK = '/var/tmp/ex08-r3/work';
const OUT = '/var/tmp/ex08-r3/evidence';

const src = fs.readFileSync(path.join(WORK, 'CarrierB.sol'), 'utf8');
const srcSha = crypto.createHash('sha256').update(src).digest('hex');
fs.mkdirSync(OUT, { recursive: true });

function compile(optimizer) {
  const input = {
    language: 'Solidity',
    sources: { 'CarrierB.sol': { content: src } },
    settings: {
      optimizer,
      libraries: { 'CarrierB.sol': { HarborLib: '0x0000000000000000000000000000000000000042' } },
      outputSelection: {
        '*': { '*': ['abi', 'metadata', 'evm.bytecode.object', 'evm.deployedBytecode.object', 'evm.methodIdentifiers'] },
      },
    },
  };
  const out = JSON.parse(solc.compile(JSON.stringify(input)));
  const errs = (out.errors || []).filter(e => e.severity === 'error');
  if (errs.length) { for (const e of errs) console.error('solc error:', e.formattedMessage); process.exit(1); }
  const warn = (out.errors || []).filter(e => e.severity === 'warning').map(e => e.formattedMessage.split('\n')[0]);
  return { out, warn };
}

function sha256Hex(hex) { return crypto.createHash('sha256').update(Buffer.from(hex, 'hex')).digest('hex'); }

function emit(tag, contract, optimizer) {
  const runtimeHex = contract.evm.deployedBytecode.object;
  const creationHex = contract.evm.bytecode.object;
  if (!/^[0-9a-fA-F]*$/.test(runtimeHex)) throw new Error(tag + ': runtime not pure hex (unlinked library?)');
  fs.writeFileSync(path.join(OUT, tag + '.runtime.hex'), runtimeHex + '\n');
  fs.writeFileSync(path.join(OUT, tag + '.creation.hex'), creationHex + '\n');
  fs.writeFileSync(path.join(OUT, tag + '.runtime.bin'), Buffer.from(runtimeHex, 'hex'));
  fs.writeFileSync(path.join(OUT, tag + '.creation.bin'), Buffer.from(creationHex, 'hex'));
  fs.writeFileSync(path.join(OUT, tag + '.abi.json'), JSON.stringify(contract.abi, null, 2));
  return {
    tag,
    optimizer,
    solc: solc.version(),
    runtime_bytes: runtimeHex.length / 2,
    runtime_sha256: sha256Hex(runtimeHex),
    creation_bytes: creationHex.length / 2,
    creation_sha256: sha256Hex(creationHex),
    method_identifiers: contract.evm.methodIdentifiers,
    abi_functions: contract.abi.filter(a => a.type === 'function').map(a => a.name + '(' + a.inputs.map(i => i.type).join(',') + ')').sort(),
    abi_events: contract.abi.filter(a => a.type === 'event').map(a => a.name).sort(),
    abi_errors: contract.abi.filter(a => a.type === 'error').map(a => a.name + '(' + a.inputs.map(i => i.type).join(',') + ')').sort(),
  };
}

const { out: optOut, warn: optWarn } = compile({ enabled: true, runs: 200 });
const B = emit('CarrierB', optOut.contracts['CarrierB.sol'].HarborBound, { enabled: true, runs: 200 });
const L = emit('HarborLib', optOut.contracts['CarrierB.sol'].HarborLib, { enabled: true, runs: 200 });

const { out: noOptOut, warn: noOptWarn } = compile({ enabled: false, runs: 200 });
const Bn = emit('CarrierBNoOpt', noOptOut.contracts['CarrierB.sol'].HarborBound, { enabled: false, runs: 200 });

const report = {
  source_path: path.join(WORK, 'CarrierB.sol'),
  source_sha256: srcSha,
  solc_version: solc.version(),
  libraries: { HarborLib: '0x0000000000000000000000000000000000000042' },
  carriers: [B, L, Bn],
  warnings_opt: optWarn,
  warnings_noopt: noOptWarn,
};
fs.writeFileSync(path.join(OUT, 'compile-report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));