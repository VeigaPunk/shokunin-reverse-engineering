// plant-b.js — carrier B planted-selector table (arc3-loop1-round3, chain c1, EX-04)
// usage: node plant-b.js <outDir> <opt200|noopt>
// Three-way: pure-JS keccak.js (own implementation) | js-sha3@0.8.0 (solc tree) | solc evm.methodIdentifiers
const fs = require('fs');
const crypto = require('crypto');
const { selector } = require('/dev/shm/ex04-r3/keccak.js');
const jsSha3 = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');

const [outDir, mode] = process.argv.slice(2);
if (!outDir || !['opt200', 'noopt'].includes(mode)) {
  console.error('usage: node plant-b.js <outDir> <opt200|noopt>');
  process.exit(2);
}

const abi = JSON.parse(fs.readFileSync(`${outDir}/carrierB.abi-${mode}.json`, 'utf8'));
const methodIdentifiers = JSON.parse(fs.readFileSync(`${outDir}/methodIdentifiers-${mode}.json`, 'utf8'));
const runtimeHex = fs.readFileSync(`${outDir}/carrierB.runtime-${mode}.hex`, 'utf8').trim();

// PUSH4 (0x63) immediate-site linear scan — the house disassembler idiom (EX-06 plant.js).
const OPS = { 0x60: 1, 0x61: 2, 0x62: 3, 0x63: 4, 0x64: 5, 0x65: 6, 0x66: 7, 0x67: 8, 0x68: 9, 0x69: 10, 0x6a: 11, 0x6b: 12, 0x6c: 13, 0x6d: 14, 0x6e: 15, 0x6f: 16, 0x70: 17, 0x71: 18, 0x72: 19, 0x73: 20, 0x74: 21, 0x75: 22, 0x76: 23, 0x77: 24, 0x78: 25, 0x79: 26, 0x7a: 27, 0x7b: 28, 0x7c: 29, 0x7d: 30, 0x7e: 31, 0x7f: 32 };
const push4 = [];
let pc = 0;
while (pc < runtimeHex.length / 2) {
  const op = parseInt(runtimeHex.substr(pc * 2, 2), 16);
  if (op === 0x63) push4.push({ pc, imm: runtimeHex.substr((pc + 1) * 2, 8) });
  pc += 1 + (OPS[op] || 0);
}
const push4Set = new Set(push4.map((p) => p.imm));

const fns = abi
  .filter((a) => a.type === 'function')
  .map((a) => ({
    sig: a.name + '(' + a.inputs.map((i) => i.type).join(',') + ')',
    mutability: a.stateMutability,
  }))
  .map((f) => {
    const selOwn = selector(f.sig);
    const selJs = jsSha3.keccak256(f.sig).slice(0, 8);
    const selSolc = (methodIdentifiers[f.sig] || '').toLowerCase();
    return {
      sig: f.sig,
      mutability: f.mutability,
      selector: '0x' + selOwn,
      js_sha3: '0x' + selJs,
      solc: selSolc ? '0x' + selSolc : null,
      agree: selOwn === selJs && selJs === selSolc,
      push4_site_pc: push4.find((p) => p.imm === selOwn) ? push4.find((p) => p.imm === selOwn).pc : null,
    };
  })
  .sort((a, b) => a.selector.localeCompare(b.selector));

const erc20 = ['06fdde03', '095ea7b3', '18160ddd', '23b872dd', '313ce567', '70a08231', 'a9059cbb', 'dd62ed3e'];
const erc20Present = erc20.filter((s) => fns.some((f) => f.selector === '0x' + s));

const report = {
  seat: 'EX-04 (chain c1, executor)',
  wave: 'arc3-loop1-round3',
  carrier: 'VaultB (carrierB.sol)',
  leg: mode,
  K: fns.length,
  all_agree: fns.every((f) => f.agree),
  erc20_selectors_present: erc20Present,
  functions: fns,
  push4_sites_total: push4.length,
  push4_immediates: push4.map((p) => '0x' + p.imm + '@' + p.pc),
  dispatch_constants_match_planted: fns.every((f) => push4Set.has(f.selector.slice(2))),
  extra_push4_immediates: [...push4Set].filter((i) => !fns.some((f) => f.selector.slice(2) === i)),
};
fs.writeFileSync(`${outDir}/planted-B-${mode}.json`, JSON.stringify(report, null, 2));

const lines = fns.map((f) => `${f.selector} ${f.sig} [${f.mutability}]`);
lines.push(`K=${fns.length}`);
fs.writeFileSync(`${outDir}/planted-B-${mode}.txt`, lines.join('\n') + '\n');
console.log(JSON.stringify(report, null, 1));
console.log('sha256 planted-B.json  ' + crypto.createHash('sha256').update(fs.readFileSync(`${outDir}/planted-B-${mode}.json`)).digest('hex'));
console.log('sha256 planted-B.txt   ' + crypto.createHash('sha256').update(fs.readFileSync(`${outDir}/planted-B-${mode}.txt`)).digest('hex'));