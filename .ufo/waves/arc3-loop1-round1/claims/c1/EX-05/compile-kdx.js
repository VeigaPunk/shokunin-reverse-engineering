const fs = require('fs');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);
const src = fs.readFileSync('/dev/shm/ex05/KdxToken.sol', 'utf8');
const input = {
  language: 'Solidity',
  sources: { 'KdxToken.sol': { content: src } },
  settings: { outputSelection: { '*': { '*': ['abi', 'metadata', 'evm.bytecode.object', 'evm.deployedBytecode.object'] } } }
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
if (out.errors) for (const e of out.errors) console.error('solc:', e.severity, e.formattedMessage);
const c = out.contracts['KdxToken.sol']['KdxToken'];
fs.writeFileSync('/dev/shm/ex05/kdx-runtime.hex', c.evm.deployedBytecode.object + '\n');
fs.writeFileSync('/dev/shm/ex05/kdx-creation.hex', c.evm.bytecode.object + '\n');
fs.writeFileSync('/dev/shm/ex05/kdx-runtime.bin', Buffer.from(c.evm.deployedBytecode.object, 'hex'));
fs.writeFileSync('/dev/shm/ex05/kdx-creation.bin', Buffer.from(c.evm.bytecode.object, 'hex'));
fs.writeFileSync('/dev/shm/ex05/kdx-abi.json', JSON.stringify(c.abi, null, 2));
console.log(JSON.stringify({ solc: solc.version(), runtime_bytes: c.evm.deployedBytecode.object.length/2, creation_bytes: c.evm.bytecode.object.length/2 }, null, 1));
