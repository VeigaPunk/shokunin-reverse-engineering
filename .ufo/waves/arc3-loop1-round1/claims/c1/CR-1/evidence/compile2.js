const solc = require('/dev/shm/cr1/solc-prefix/node_modules/solc');
const { keccak256 } = require('/dev/shm/cr1/solc-prefix/node_modules/js-sha3');
const fs = require('fs');
const source = fs.readFileSync('/dev/shm/cr1/Cr1Sample.sol', 'utf8');
const input = { language: 'Solidity', sources: { 'Cr1Sample.sol': { content: source } }, settings: { optimizer: { enabled: false }, outputSelection: { '*': { '*': ['abi','evm.methodIdentifiers','evm.bytecode.object','evm.deployedBytecode.object'] } } } };
const out = JSON.parse(solc.compile(JSON.stringify(input)));
if (out.errors) for (const e of out.errors) if (e.severity === 'error') { console.error(e.formattedMessage); process.exit(1); }
const c = out.contracts['Cr1Sample.sol'].Cr1Sample;
const mi = c.evm.methodIdentifiers;
const names = Object.keys(mi).sort();
console.log('compiler methodIdentifiers (K=' + names.length + '):');
for (const n of names) {
  const mine = keccak256(n).slice(0, 8);
  console.log('  ' + mi[n] + '  ' + n + '  (independent keccak: ' + mine + ' match=' + (mine === mi[n]) + ')');
}
fs.writeFileSync('/dev/shm/cr1/solc-runtime.hex', c.evm.deployedBytecode.object);
fs.writeFileSync('/dev/shm/cr1/solc-creation.hex', c.evm.bytecode.object);
fs.writeFileSync('/dev/shm/cr1/selectors.json', JSON.stringify(names.map(n => ({ name: n, selector: mi[n] })), null, 2));
console.log('runtime bytes:', c.evm.deployedBytecode.object.length/2, 'creation bytes:', c.evm.bytecode.object.length/2);
