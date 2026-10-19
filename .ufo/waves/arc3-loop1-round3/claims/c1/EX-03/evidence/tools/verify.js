// arc3-loop1-round3 c1/EX-03 — verification battery for the carrier A compile legs.
// Checks:
//  V1  CLI leg-1 creation hex == standard-JSON leg creation hex (byte-identical)
//  V2  ABI: CLI --abi output vs standard-JSON abi (entry-level semantic diff)
//  V3  K-table: js-sha3 keccak selectors from the ABI vs solc methodIdentifiers
//  V4  runtime scan: prologue markers + occurrence offsets of every planted selector
//  V5  runtime .bin/.hex materialization + hashes (raw bytes written by caller)
const fs = require('fs');
const path = require('path');
const { keccak256 } = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');

const S = '/var/tmp/ex03-r3';
const LEG1 = S + '/a-out';
const LEG2 = S + '/a-stdjson-out';
const out = [];
const say = (s) => { out.push(s); console.log(s); };

// ---- V1 creation byte-equality -------------------------------------------
const cliBin = fs.readFileSync(LEG1 + '/carrierA_sol_CarrierA.bin', 'utf8');
const stdCreation = fs.readFileSync(LEG2 + '/carrierA.creation.hex', 'utf8');
const stdCreationTrim = stdCreation.replace(/\n$/, '');
say('V1 cli --bin len=' + cliBin.length + ' chars; stdjson creation len=' + stdCreationTrim.length + ' chars');
say('V1 EQUAL: ' + (cliBin === stdCreationTrim ? 'YES (byte-identical hex text)' : 'NO'));
if (cliBin !== stdCreationTrim) process.exit(2);

// ---- V2 ABI semantic diff -------------------------------------------------
const cliAbi = JSON.parse(fs.readFileSync(LEG1 + '/carrierA_sol_CarrierA.abi', 'utf8'));
const stdAbi = JSON.parse(fs.readFileSync(LEG2 + '/carrierA.abi.json', 'utf8'));
const norm = (e) =>
  JSON.stringify({
    type: e.type,
    name: e.name,
    inputs: (e.inputs || []).map((i) => [i.type, i.name, i.indexed, i.components ? 1 : 0]),
    outputs: (e.outputs || []).map((o) => [o.type, o.name, o.components ? 1 : 0]),
    stateMutability: e.stateMutability,
    anonymous: e.anonymous
  });
const cliSet = new Set(cliAbi.map(norm));
const stdSet = new Set(stdAbi.map(norm));
const onlyCli = [...cliSet].filter((x) => !stdSet.has(x));
const onlyStd = [...stdSet].filter((x) => !cliSet.has(x));
say('V2 abi entries: cli=' + cliAbi.length + ' stdjson=' + stdAbi.length +
    ' | set-equal=' + (onlyCli.length === 0 && onlyStd.length === 0) +
    ' | only-cli=' + onlyCli.length + ' only-std=' + onlyStd.length);
for (const x of onlyCli) say('  only-cli: ' + x);
for (const x of onlyStd) say('  only-std: ' + x);

// ---- V3 K-table ----------------------------------------------------------
const fns = stdAbi.filter((e) => e.type === 'function');
const rows = fns.map((e) => {
  const sig = e.name + '(' + e.inputs.map((i) => i.type).join(',') + ')';
  return { sig, sel: keccak256(sig).slice(0, 8), mut: e.stateMutability };
}).sort((a, b) => (a.sel < b.sel ? -1 : 1));
const mids = JSON.parse(fs.readFileSync(LEG2 + '/carrierA.methodIdentifiers.json', 'utf8'));
const mine = new Set(rows.map((r) => r.sel));
const solcSel = new Set(Object.values(mids).map((s) => s.toLowerCase()));
const miss = [...solcSel].filter((s) => !mine.has(s));
const extra = [...mine].filter((s) => !solcSel.has(s));
say('V3 K=' + rows.length + ' js-sha3 vs solc methodIdentifiers: missing=' + JSON.stringify(miss) +
    ' extra=' + JSON.stringify(extra) + ' -> ' + (miss.length === 0 && extra.length === 0 ? 'SET-EQUAL' : 'DISAGREE'));
for (const r of rows) say('  0x' + r.sel + ' ' + r.sig + ' [' + r.mut + ']');

// ---- V4 runtime scan -----------------------------------------------------
const rtHex = fs.readFileSync(LEG2 + '/carrierA.runtime.hex', 'utf8').trim().replace(/^0x/, '');
const rtBuf = Buffer.from(rtHex, 'hex');
say('V4 runtime bytes: ' + rtBuf.length);
const markers = ['5f3560e01c', '60003560e01c', '6080604052'];
for (const m of markers) {
  const offs = [];
  let i = rtHex.indexOf(m);
  while (i !== -1 && offs.length < 6) { offs.push(i / 2); i = rtHex.indexOf(m, i + 1); }
  say('V4 marker ' + m + ' byte offsets: ' + (offs.length ? offs.join(',') : 'ABSENT'));
}
for (const r of rows) {
  const offs = [];
  let i = rtHex.indexOf(r.sel);
  while (i !== -1) { offs.push(i / 2); i = rtHex.indexOf(r.sel, i + 1); }
  say('V4 selector 0x' + r.sel + ' ' + r.sig + ' occurrences at byte offsets: ' + (offs.length ? offs.join(',') : 'ABSENT'));
}
const erc = ['a9059cbb', '70a08231', '095ea7b3', '23b872dd', '18160ddd', 'dd62ed3e', '313ce567', '06fdde03', '95d89b41'];
say('V4 ERC-20 ambient selectors present in runtime: ' + erc.filter((s) => rtHex.includes(s)).join(',') || 'V4 ERC-20 ambient selectors present: none');

// ---- V5 materialize raw bins --------------------------------------------
fs.writeFileSync(S + '/work/carrierA.creation.bin', Buffer.from(cliBin, 'hex'));
fs.writeFileSync(S + '/work/carrierA.creation.hex', cliBin + '\n');
fs.writeFileSync(S + '/work/carrierA.runtime.bin', rtBuf);
fs.writeFileSync(S + '/work/carrierA.runtime.hex', rtHex + '\n');
say('V5 wrote raw bins into ' + S + '/work/');

// K table as artifact
const ktext = rows.map((r) => '0x' + r.sel + ' ' + r.sig + ' [' + r.mut + ']').join('\n') + '\nK=' + rows.length + '\n';
fs.writeFileSync(S + '/work/planted-selectors.txt', ktext);
say('V5 wrote K table (' + rows.length + ' selectors)');
fs.writeFileSync(S + '/transcript-verify.txt', out.join('\n') + '\n');