const fs=require('fs'), path=require('path');
const prefix='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix';
const solc=require(path.join(prefix,'node_modules','solc'));
for (const [srcPath, contract] of process.argv.slice(2).map(s=>s.split(':'))) {
  const src=fs.readFileSync(srcPath,'utf8');
  const name=path.basename(srcPath);
  const input={language:'Solidity',sources:{[name]:{content:src}},settings:{optimizer:{enabled:true,runs:200},viaIR:true,outputSelection:{'*':{'*':['evm.deployedBytecode.object','evm.methodIdentifiers']}}}};
  const out=JSON.parse(solc.compile(JSON.stringify(input)));
  if(out.errors) for(const e of out.errors) if(e.severity==='error'){console.error(e.formattedMessage);process.exit(1);}
  const c=out.contracts[name][contract];
  const rt=Buffer.from(c.evm.deployedBytecode.object,'hex');
  fs.writeFileSync(contract+'.runtime.bin',rt);
  console.log(contract, solc.version(), rt.length, require('crypto').createHash('sha256').update(rt).digest('hex'));
}
