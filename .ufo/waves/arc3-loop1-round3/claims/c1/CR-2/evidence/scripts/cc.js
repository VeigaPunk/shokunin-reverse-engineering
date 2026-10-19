const fs = require('fs');
const solc = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc');
// argv: srcPath outPrefix optSpec(off|on|on200)
const [srcPath, outPrefix, optSpec] = process.argv.slice(2);
const name = srcPath.split('/').pop();
const src = fs.readFileSync(srcPath, 'utf8');
let optimizer;
if (optSpec === 'off') optimizer = { enabled: false };
else if (optSpec === 'on') optimizer = { enabled: true };
else if (optSpec === 'on200') optimizer = { enabled: true, runs: 200 };
const input = {
  language: 'Solidity',
  sources: { [name]: { content: src } },
  settings: { optimizer, outputSelection: { '*': { '*': ['abi','evm.bytecode.object','evm.deployedBytecode.object'] } } }
};
const out = JSON.parse(solc.compile(JSON.stringify(input)));
if (out.errors) for (const e of out.errors) if (e.severity === 'error') { console.error('SOLC-ERROR', e.formattedMessage); process.exit(2); }
const contractNames = Object.keys(out.contracts[name]);
for (const cn of contractNames) {
  const c = out.contracts[name][cn];
  const r = c.evm.deployedBytecode.object, cr = c.evm.bytecode.object;
  fs.writeFileSync(`${outPrefix}.${cn}.runtime.hex`, r + '\n');
  fs.writeFileSync(`${outPrefix}.${cn}.creation.hex`, cr + '\n');
  fs.writeFileSync(`${outPrefix}.${cn}.runtime.bin`, Buffer.from(r, 'hex'));
  fs.writeFileSync(`${outPrefix}.${cn}.abi.json`, JSON.stringify(c.abi, null, 1));
  console.log(JSON.stringify({ contract: cn, solc: solc.version(), optSpec, runtime_bytes: r.length/2, creation_bytes: cr.length/2,
    abi_functions: c.abi.filter(a=>a.type==='function').map(a=>a.name+'('+a.inputs.map(i=>i.type).join(',')+')').sort(),
    abi_receive: c.abi.some(a=>a.type==='receive'), abi_fallback: c.abi.some(a=>a.type==='fallback') }));
}
