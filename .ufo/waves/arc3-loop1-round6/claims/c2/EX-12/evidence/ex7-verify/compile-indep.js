// EX-12 independent compile: same source, my own input builder. No EX-7 code read/executed.
const fs=require('fs'), path=require('path'), crypto=require('crypto');
const prefix=process.argv[2], srcPath=process.argv[3], outDir=process.argv[4];
const solc=require(path.join(prefix,'node_modules','solc'));
const src=fs.readFileSync(srcPath,'utf8');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function leg(tag, settings){
  const input={language:'Solidity',sources:{'ViaIrVault.sol':{content:src}},
    settings:Object.assign({optimizer:{enabled:true,runs:200},
      outputSelection:{'*':{'*':['abi','evm.methodIdentifiers','evm.bytecode.object','evm.deployedBytecode.object']}}},settings)};
  const out=JSON.parse(solc.compile(JSON.stringify(input)));
  for(const e of out.errors||[]) if(e.severity==='error') throw new Error(e.formattedMessage);
  const c=out.contracts['ViaIrVault.sol']['ViaIrVault'];
  const rt=Buffer.from(c.evm.deployedBytecode.object,'hex');
  const cr=Buffer.from(c.evm.bytecode.object,'hex');
  fs.mkdirSync(path.join(outDir,tag),{recursive:true});
  fs.writeFileSync(path.join(outDir,tag,'runtime.bin'),rt);
  fs.writeFileSync(path.join(outDir,tag,'creation.bin'),cr);
  fs.writeFileSync(path.join(outDir,tag,'abi.json'),JSON.stringify(c.abi,null,2)+'\n');
  fs.writeFileSync(path.join(outDir,tag,'method-identifiers.json'),JSON.stringify(c.evm.methodIdentifiers,null,2)+'\n');
  console.log(JSON.stringify({tag, runtime_len:rt.length, runtime_sha256:sha(rt),
    creation_len:cr.length, creation_sha256:sha(cr), abi_sha256:sha(JSON.stringify(c.abi,null,2)+'\n'),
    method_ids_sha256:sha(JSON.stringify(c.evm.methodIdentifiers,null,2)+'\n'), solc:solc.version()}));
}
leg('viair-opt200',{viaIR:true});
leg('viair-noopt',{viaIR:true,optimizer:{enabled:false}});
leg('std-opt200',{});
