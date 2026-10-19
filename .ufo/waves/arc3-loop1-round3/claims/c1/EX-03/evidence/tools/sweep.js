// arc3-loop1-round3 c1/EX-03 — dispatch/PUSH4 inventory for the compiled carriers.
// Linear opcode sweep (method named; may desync on data bytes past the code region).
// Inputs are the pinned runtime hex files produced by this seat's legs.
const fs = require('fs');
const crypto = require('crypto');
const { keccak256 } = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');

const S = '/var/tmp/ex03-r3';
const carriers = [
  {
    name: 'OptVault (PL-1 plan §1.A carrier A, optimizer ON runs=200)',
    rt: S + '/ov-stdjson-out/OptVault.runtime.hex',
    abi: S + '/ov-stdjson-out/OptVault.abi.json',
    mids: S + '/ov-stdjson-out/OptVault.methodIdentifiers.json'
  },
  {
    name: 'CarrierA (EX-02 alternate, optimizer ON runs=200)',
    rt: S + '/a-stdjson-out/carrierA.runtime.hex',
    abi: S + '/a-stdjson-out/carrierA.abi.json',
    mids: S + '/a-stdjson-out/carrierA.methodIdentifiers.json'
  }
];

const KNOWN = {
  '4e487b71': 'Panic(uint256)',
  '08c379a0': 'Error(string)',
  'f4a4cf0e': 'not a known error selector'
};

const L = [];
const say = (s) => { L.push(s); console.log(s); };

for (const c of carriers) {
  const hex = fs.readFileSync(c.rt, 'utf8').trim().replace(/^0x/, '');
  const buf = Buffer.from(hex, 'hex');
  const rtSha = crypto.createHash('sha256').update(buf).digest('hex');

  say('## ' + c.name);
  say('runtime bytes ' + buf.length + '  raw sha256 ' + rtSha);

  const abi = JSON.parse(fs.readFileSync(c.abi, 'utf8'));
  const fns = abi.filter((e) => e.type === 'function');
  const rows = fns.map((e) => {
    const sig = e.name + '(' + e.inputs.map((i) => i.type).join(',') + ')';
    return { sig, sel: keccak256(sig).slice(0, 8), mut: e.stateMutability };
  }).sort((a, b) => (a.sel < b.sel ? -1 : 1));
  const mids = JSON.parse(fs.readFileSync(c.mids, 'utf8'));
  const mine = new Set(rows.map((r) => r.sel));
  const solcSel = new Set(Object.values(mids).map((s) => s.toLowerCase()));
  const miss = [...solcSel].filter((x) => !mine.has(x));
  const extra = [...mine].filter((x) => !solcSel.has(x));
  say('K=' + rows.length + ' js-sha3 vs solc methodIdentifiers: ' +
      (miss.length === 0 && extra.length === 0 ? 'SET-EQUAL' : 'DISAGREE missing=' + JSON.stringify(miss) + ' extra=' + JSON.stringify(extra)));
  for (const r of rows) {
    const offs = [];
    let i = hex.indexOf(r.sel);
    while (i !== -1) { offs.push(i / 2); i = hex.indexOf(r.sel, i + 1); }
    say('  planted 0x' + r.sel + ' ' + r.sig + ' [' + r.mut + '] first-occurrence byte offsets: ' + (offs.length ? offs.join(',') : 'ABSENT'));
  }

  for (const h of ['5f3560e01c', '60003560e01c', '8063']) {
    const offs = [];
    let i = hex.indexOf(h);
    while (i !== -1 && offs.length < 12) { offs.push(i / 2); i = hex.indexOf(h, i + 1); }
    say('  marker ' + h + ' at byte offsets: ' + (offs.length ? offs.join(',') : 'ABSENT'));
  }
  say('  EQ-jump 1461 count ' + (hex.match(/1461/g) || []).length + ' | GT-jump 1161 count ' + (hex.match(/1161/g) || []).length);

  // linear sweep for PUSH4 (0x63) immediates
  const isPush = (op) => op >= 0x60 && op <= 0x7f;
  const inv = [];
  for (let pc = 0; pc < buf.length;) {
    const op = buf[pc];
    if (op === 0x63 && pc + 4 < buf.length) inv.push({ pc, c: buf.slice(pc + 1, pc + 5).toString('hex') });
    pc += isPush(op) ? 1 + (op - 0x5f) : 1;
  }
  const counts = {};
  for (const x of inv) counts[x.c] = (counts[x.c] || 0) + 1;
  const plantedSet = new Set(rows.map((r) => r.sel));
  say('  linear-sweep PUSH4 sites: ' + inv.length + '; distinct constants: ' + Object.keys(counts).length);
  for (const [k, v] of Object.entries(counts).sort()) {
    const kind = plantedSet.has(k) ? 'PLANTED selector' : (KNOWN[k] ? 'non-dispatch: ' + KNOWN[k] : 'other');
    say('    0x' + k + ' x' + v + ' @pcs ' + inv.filter((x) => x.c === k).map((x) => x.pc).join(',') + '  [' + kind + ']');
  }
  const erc = ['a9059cbb', '70a08231', '095ea7b3', '23b872dd', '18160ddd', 'dd62ed3e', '313ce567', '06fdde03', '95d89b41'];
  const ercPresent = erc.filter((s) => hex.includes(s));
  say('  ERC-20 ambient selector constants present: ' + (ercPresent.length ? ercPresent.join(',') : 'NONE'));
  say('');
}

fs.writeFileSync(S + '/sweep-both-carriers.txt', L.join('\n') + '\n');
console.log('wrote ' + S + '/sweep-both-carriers.txt');