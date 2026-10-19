const fs=require('fs');
const {keccak256}=require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');
for (const p of process.argv.slice(2)) {
  const abi=JSON.parse(fs.readFileSync(p,'utf8'));
  const sels={};
  for (const a of abi) {
    if (a.type!=='function') continue;
    const sig=`${a.name}(${a.inputs.map(i=>i.type).join(',')})`;
    sels[keccak256(sig).slice(0,8)]=sig;
  }
  console.log(p);
  for (const k of Object.keys(sels).sort()) console.log(' ',k,sels[k]);
}
