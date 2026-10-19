// arc3-loop1-round3 c1/EX-02 — runtime hex scan for carrierA (v2).
// (a) prologue/dispatch-region bytes (correct byte offsets)
// (b) binary-search dispatcher tree decode (PUSH4 sel GT/EQ PUSH2 target JUMPI)
// (c) PUSH4 constant inventory over the code region, classified
// (d) shift-encoded constant inventory: value >> k pushed with compensating SHL
// (e) planted-selector occurrence offsets; (f) ERC-20 ambient check.
// Method: linear opcode sweep from byte 0 (PUSH-aware); no jumpdest filtering.
// Code region = [0, metadata_start); metadata located by CBOR prefix a264697066735822.
const fs = require('fs');

const OUT = '/var/tmp/ex02-r3/out';
const hex = fs.readFileSync(OUT + '/carrierA.runtime.hex', 'utf8').trim().replace(/^0x/, '');
const buf = Buffer.from(hex, 'hex');

const planted = fs
  .readFileSync(OUT + '/planted-A.txt', 'utf8')
  .split('\n')
  .filter((l) => l.startsWith('0x'))
  .map((l) => {
    const [sel, ...rest] = l.split(' ');
    return { sel: sel.slice(2).toLowerCase(), sig: rest.join(' ') };
  });
const plantedSet = new Set(planted.map((p) => p.sel));

const metaHexPos = hex.indexOf('a264697066735822');
const metaStart = metaHexPos >= 0 ? metaHexPos / 2 : buf.length;

const opLen = (op) => 1 + (op >= 0x60 && op <= 0x7f ? op - 0x5f : 0);
const OPNAMES = { 0x01: 'ADD', 0x11: 'GT', 0x14: 'EQ', 0x15: 'ISZERO', 0x1b: 'SHL', 0x1c: 'SHR', 0x29: 'SAR', 0x34: 'CALLVALUE', 0x35: 'CALLDATALOAD', 0x36: 'CALLDATASIZE', 0x3d: 'RETURNDATASIZE', 0x3e: 'RETURNDATACOPY', 0x50: 'POP', 0x51: 'MLOAD', 0x52: 'MSTORE', 0x53: 'MSTORE8', 0x54: 'SLOAD', 0x55: 'SSTORE', 0x56: 'JUMP', 0x57: 'JUMPI', 0x5b: 'JUMPDEST', 0x5f: 'PUSH0', 0x90: 'SWAP1', 0x91: 'SWAP2', 0xa2: 'LOG2', 0xa3: 'LOG3', 0xf3: 'RETURN', 0xfd: 'REVERT' };
const opName = (op) => OPNAMES[op] || `op0x${op.toString(16)}`;

// sequential sweep
const ops = [];
for (let pc = 0; pc < buf.length; ) {
  const op = buf[pc];
  const len = opLen(op);
  const imm = len > 1 ? buf.slice(pc + 1, pc + len) : Buffer.alloc(0);
  ops.push({ pc, op, len, imm });
  pc += len;
}
const codeOps = ops.filter((o) => o.pc < metaStart);

let report = '';
report += `runtime bytes: ${buf.length}; code region: [0, ${metaStart}); metadata CBOR prefix (a264697066735822) at byte ${metaStart}\n`;
report += `first 48 bytes: ${hex.slice(0, 96)}\n`;
report += `prologue: ${hex.slice(0, 26)} = PUSH1 80 PUSH1 40 MSTORE PUSH1 04 CALLDATASIZE LT PUSH2 0089 JUMPI\n`;
report += `selector-recovery idiom 5f3560e01c at byte ${hex.indexOf('5f3560e01c') / 2} (PUSH0 CALLDATALOAD PUSH1 e0 SHR); marker 60003560e01c: ${hex.indexOf('60003560e01c')}\n`;
report += `fallback guard at 0x89: ${hex.slice(0x89 * 2, 0x89 * 2 + 24)} = CALLDATASIZE PUSH2 009a JUMPI (size!=0 -> fallback; size==0 -> receive)\n\n`;

// (b) dispatcher tree
report += `dispatcher tree (pc<0x100: PUSH4/<sel>/ GT|EQ / PUSH2 <target> / JUMPI):\n`;
for (let i = 0; i < ops.length - 3; i++) {
  const a = ops[i];
  if (a.pc >= 0x100 || a.op !== 0x63) continue;
  const b = ops[i + 1];
  const c = ops[i + 2];
  const d = ops[i + 3];
  if (b && (b.op === 0x11 || b.op === 0x14) && c && c.op === 0x61 && d && d.op === 0x57) {
    const sel = a.imm.toString('hex');
    const target = c.imm.readUInt16BE(0);
    const cmp = b.op === 0x11 ? 'GT' : 'EQ';
    report += `  pc=${a.pc} sel=${sel} ${cmp} -> JUMPI target=${target} (0x${target.toString(16)}) ${plantedSet.has(sel) ? planted.find((p) => p.sel === sel).sig : '(not planted)'}\n`;
  }
}

// (c) PUSH4 inventory over code region
const push4 = codeOps.filter((o) => o.op === 0x63);
const classify = (cst) => {
  if (plantedSet.has(cst)) return 'planted selector';
  if (cst === '30cd7471') return 'non-dispatch: NotOwner() error selector (plain, low bit 1)';
  if (cst === '4e487b71') return 'non-dispatch: Panic(uint256) selector (plain, low bit 1)';
  if (cst === '6508d58f') return 'non-dispatch: shl(e1,0xca11ab1e) encoding of stamp() bytes4 literal 0xca11ab1e (0xca11ab1e>>1, even value)';
  return 'unclassified';
};
report += `\nPUSH4 constants in code region (${push4.length}):\n`;
for (const o of push4) {
  const cst = o.imm.toString('hex');
  report += `  pc=${o.pc} ${cst} ${classify(cst)}\n`;
}

// (d) shift-encoded inventory for known plaintext values
const known = [];
for (const p of planted) known.push({ label: p.sig + ' (dispatch selector)', hex: p.sel });
known.push({ label: 'NotOwner() error selector', hex: '30cd7471' });
known.push({ label: 'Panic(uint256) selector', hex: '4e487b71' });
known.push({ label: 'Insufficient(uint256,uint256) error selector', hex: 'e8620800' });
known.push({ label: 'Error(string) revert selector', hex: '08c379a0' });
known.push({ label: 'stamp() bytes4 literal', hex: 'ca11ab1e' });
known.push({ label: '"CarrierA: send failed" bytes', hex: Buffer.from('CarrierA: send failed', 'utf8').toString('hex') });
known.push({ label: 'Credited(address,uint256) topic0', hex: '9c9e0cdb1670e88302408e5b941dc636f63a3293204694bb68910fcf3d9305f3' });
known.push({ label: 'Swept(address,uint256) topic0', hex: 'c36b5179cb9c303b200074996eab2b3473eac370fdd7eba3bec636fe35109696' });

report += `\nshift-encoded constant inventory (value>>k pushed as PUSHn, k = trailing zero bits used):\n`;
for (const k of known) {
  const v = BigInt('0x' + k.hex);
  const trailing = (() => {
    if (v === 0n) return 0;
    let t = 0;
    let x = v;
    while ((x & 1n) === 0n && t < 32) {
      x >>= 1n;
      t++;
    }
    return t;
  })();
  for (let shift = 0; shift <= trailing; shift++) {
    const enc = (v >> BigInt(shift)).toString(16);
    const padded = enc.length % 2 ? '0' + enc : enc;
    let idx = 0;
    const sites = [];
    while ((idx = hex.indexOf(padded, idx)) !== -1) {
      sites.push(idx / 2);
      idx += 2;
    }
    const codeSites = sites.filter((s) => s < metaStart);
    if (codeSites.length) {
      const render = (o) =>
        o.op >= 0x60 && o.op <= 0x7f ? `PUSH${o.op - 0x5f} 0x${o.imm.toString('hex')}` : opName(o.op);
      const detail = codeSites
        .slice(0, 3)
        .map((s) => {
          const i = ops.findIndex((o) => o.pc + 1 === s && o.op >= 0x60 && o.op <= 0x7f);
          if (i < 0) return `bytes@${s}: (not a PUSH payload start)`;
          const follow = ops.slice(i + 1, i + 4).map(render).join(' ; ');
          return `PUSHn@${ops[i].pc} bytes@${s} followed by: ${follow}`;
        })
        .join(' | ');
      report += `  ${k.label}: value=0x${k.hex} k=${shift} enc=0x${padded} codeSites=[${codeSites.join(',')}] ${shift ? '' : '(plain) '}${detail}\n`;
    }
    if (shift === 0 && codeSites.length) break; // plain found, no need to probe further shifts
  }
}

// (e) planted occurrence offsets
report += `\nplanted selector occurrence offsets (raw scan):\n`;
for (const p of planted) {
  const offs = [];
  let idx = 0;
  while ((idx = hex.indexOf(p.sel, idx)) !== -1) {
    offs.push(idx / 2);
    idx += 2;
  }
  report += `  ${p.sel} ${p.sig} occurrences=${offs.length} offsets=[${offs.join(',')}]\n`;
}

// (f) ERC-20 ambient check
const erc20 = ['70a08231', 'a9059cbb', '095ea7b3', '23b872dd', '18160ddd', 'dd62ed3e', '313ce567'];
const hits = erc20.filter((s) => hex.includes(s));
report += `\nERC-20 ambient selector constants present in runtime: ${hits.length ? hits.join(',') : 'none'}\n`;

fs.writeFileSync(OUT + '/dispatch-scan-A.txt', report);
console.log(report);