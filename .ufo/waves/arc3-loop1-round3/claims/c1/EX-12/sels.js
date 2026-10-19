const { keccak256 } = require(process.argv[2] + '/node_modules/js-sha3');
const fs = require('fs');
const abi = JSON.parse(fs.readFileSync('/var/tmp/ex12-controls/VaultA.abi.json','utf8'));
const rows = [];
for (const e of abi) {
  if (e.type !== 'function') continue;
  const sig = e.name + '(' + e.inputs.map(i => i.type).join(',') + ')';
  const sel = keccak256(sig).slice(0,8);
  rows.push([sel, sig, e.stateMutability]);
}
rows.sort();
for (const r of rows) console.log('0x'+r[0]+' '+r[1]+' ['+r[2]+']');
console.log('K='+rows.length);
console.log('receive() payable: ' + abi.some(e=>e.type==='receive') + ' | fallback() payable: ' + abi.some(e=>e.type==='fallback'));
