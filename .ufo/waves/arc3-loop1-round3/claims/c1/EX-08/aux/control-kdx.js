// Control: rebuild r1's KdxToken runtime from the retained source (EX-06 evidence)
// and verify byte-identity vs the r1-recorded digest 9c40940e... (1,789 B).
const fs = require('fs');
const crypto = require('crypto');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);
const SRC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/KdxToken.sol';
const OUT = '/var/tmp/ex08-r3/evidence';
const src = fs.readFileSync(SRC, 'utf8');
const input = {
  language: 'Solidity',
  sources: { 'KdxToken.sol': { content: src } },
  settings: { outputSelection: { '*': { '*': ['abi', 'evm.bytecode.object', 'evm.deployedBytecode.object'] } } },
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
const c = out.contracts['KdxToken.sol'].KdxToken;
const runtimeHex = c.evm.deployedBytecode.object;
const bin = Buffer.from(runtimeHex, 'hex');
fs.writeFileSync(`${OUT}/KdxToken.runtime.hex`, runtimeHex + '\n');
fs.writeFileSync(`${OUT}/KdxToken.runtime.bin`, bin);
console.log(JSON.stringify({
  solc: solc.version(),
  source_sha256: crypto.createHash('sha256').update(src).digest('hex'),
  runtime_bytes: bin.length,
  runtime_sha256: crypto.createHash('sha256').update(bin).digest('hex'),
  expect_sha256: '9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e',
  byte_identical_to_r1: crypto.createHash('sha256').update(bin).digest('hex') === '9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e',
}, null, 1));