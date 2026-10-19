const fs = require('fs');
const SOLC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc';
const solc = require(SOLC);
const src = fs.readFileSync('/dev/shm/ex06/KdxToken.sol', 'utf8');
const input = {
  language: 'Solidity',
  sources: { 'KdxToken.sol': { content: src } },
  settings: { outputSelection: { '*': { '*': ['abi', 'metadata', 'evm.bytecode.object', 'evm.deployedBytecode.object'] } } }
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
if (out.errors) { for (const e of out.errors) console.error('solc:', e.severity, e.formattedMessage); }
const c = out.contracts['KdxToken.sol']['KdxToken'];
const runtimeHex = c.evm.deployedBytecode.object;
const creationHex = c.evm.bytecode.object;
fs.writeFileSync('/dev/shm/ex06/KdxToken.runtime.hex', runtimeHex + '\n');
fs.writeFileSync('/dev/shm/ex06/KdxToken.creation.hex', creationHex + '\n');
fs.writeFileSync('/dev/shm/ex06/KdxToken.runtime.bin', Buffer.from(runtimeHex, 'hex'));
fs.writeFileSync('/dev/shm/ex06/KdxToken.creation.bin', Buffer.from(creationHex, 'hex'));
fs.writeFileSync('/dev/shm/ex06/abi.json', JSON.stringify(c.abi, null, 2));
console.log(JSON.stringify({
  solc: solc.version(),
  runtime_bytes: runtimeHex.length / 2,
  creation_bytes: creationHex.length / 2,
  abi_functions: c.abi.filter(a => a.type === 'function').map(a => a.name + '(' + a.inputs.map(i => i.type).join(',') + ')').sort()
}, null, 1));
