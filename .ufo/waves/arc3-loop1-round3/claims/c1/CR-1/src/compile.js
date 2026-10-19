// CR-1 compile driver: pinned solc from the wave prefix, standard-JSON, optimizer on/off.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const solc = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc');

const src = process.argv[2];
const outdir = process.argv[3];
const tag = process.argv[4];      // e.g. "opt200" | "noopt"
const optimize = tag !== 'noopt';
const runs = 200;

const name = path.basename(src);
const source = fs.readFileSync(src, 'utf8');
const input = {
  language: 'Solidity',
  sources: { [name]: { content: source } },
  settings: {
    optimizer: { enabled: optimize, runs: optimize ? runs : 200 },
    outputSelection: { '*': { '*': ['abi', 'evm.deployedBytecode.object', 'evm.deployedBytecode.sourceMap', 'metadata'] } },
  },
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
const errs = (out.errors || []).filter(e => e.severity === 'error');
if (errs.length) { console.error(JSON.stringify(errs, null, 2)); process.exit(1); }
const warns = (out.errors || []).filter(e => e.severity === 'warning').map(e => e.formattedMessage);
fs.mkdirSync(outdir, { recursive: true });
const meta = { solc: solc.version(), tag, optimize, runs: optimize ? runs : null, source: name, sourceSha256: crypto.createHash('sha256').update(source).digest('hex'), contracts: {} };
for (const cname of Object.keys(out.contracts[name])) {
  const c = out.contracts[name][cname];
  const rb = c.evm.deployedBytecode.object;
  const rhex = rb.startsWith('0x') ? rb.slice(2) : rb;
  const abi = c.abi;
  const abiStr = JSON.stringify(abi, null, 2);
  const base = `${cname}.${tag}`;
  fs.writeFileSync(path.join(outdir, base + '.runtime.hex'), rhex + '\n');
  fs.writeFileSync(path.join(outdir, base + '.abi.json'), abiStr + '\n');
  meta.contracts[cname] = {
    runtimeBytes: rhex.length / 2,
    runtimeSha256: crypto.createHash('sha256').update(Buffer.from(rhex, 'hex')).digest('hex'),
    abiSha256: crypto.createHash('sha256').update(abiStr + '\n').digest('hex'),
    abiEntries: abi.length,
    abiEntryTypes: abi.reduce((a, e) => (a[e.type] = (a[e.type] || 0) + 1, a), {}),
  };
}
fs.writeFileSync(path.join(outdir, 'meta.' + tag + '.json'), JSON.stringify(meta, null, 2) + '\n');
if (warns.length) fs.writeFileSync(path.join(outdir, 'warnings.' + tag + '.txt'), warns.join('\n\n') + '\n');
console.log(`OK ${name} ${tag}: ` + Object.entries(meta.contracts).map(([k, v]) => `${k} ${v.runtimeBytes}B sha256 ${v.runtimeSha256.slice(0, 8)}`).join(' | '));