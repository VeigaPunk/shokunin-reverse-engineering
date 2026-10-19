const fs = require('fs');
const { selector } = require('/dev/shm/ex06/keccak.js');
const abi = JSON.parse(fs.readFileSync('/dev/shm/ex06/abi.json', 'utf8'));
const runtimeHex = fs.readFileSync('/dev/shm/ex06/KdxToken.runtime.hex', 'utf8').trim();
const fns = abi.filter(a => a.type === 'function')
  .map(a => ({ sig: a.name + '(' + a.inputs.map(i => i.type).join(',') + ')', name: a.name, mutability: a.stateMutability }))
  .map(f => ({ ...f, selector: selector(f.sig) })).sort((a, b) => a.selector.localeCompare(b.selector));
// linear scan for PUSH4 (0x63) immediate sites
const OPS = { 0x60: 1, 0x61: 2, 0x62: 3, 0x63: 4, 0x64: 5, 0x65: 6, 0x66: 7, 0x67: 8, 0x68: 9, 0x69: 10, 0x6a: 11, 0x6b: 12, 0x6c: 13, 0x6d: 14, 0x6e: 15, 0x6f: 16, 0x70: 17, 0x71: 18, 0x72: 19, 0x73: 20, 0x74: 21, 0x75: 22, 0x76: 23, 0x77: 24, 0x78: 25, 0x79: 26, 0x7a: 27, 0x7b: 28, 0x7c: 29, 0x7d: 30, 0x7e: 31, 0x7f: 32 };
const push4 = [];
let pc = 0;
while (pc < runtimeHex.length / 2) {
  const op = parseInt(runtimeHex.substr(pc*2, 2), 16);
  if (op === 0x63) push4.push({ pc, imm: runtimeHex.substr((pc+1)*2, 8) });
  pc += 1 + (OPS[op] || 0);
}
const report = {
  K: fns.length,
  functions: fns.map(f => ({ sig: f.sig, selector: '0x' + f.selector, mutability: f.mutability, push4_site_pc: (push4.find(p => p.imm === f.selector) || {}).pc ?? null })),
  push4_sites_total: push4.length,
  push4_immediates: push4.map(p => '0x' + p.imm + '@' + p.pc)
};
fs.writeFileSync('/dev/shm/ex06/planted-K.json', JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 1));
