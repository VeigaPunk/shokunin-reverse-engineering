const fs=require('fs'), path=require('path'), crypto=require('crypto');
const solc=require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc');
const src=fs.readFileSync('ViaIrVault.sol','utf8');
function sha(b){return crypto.createHash('sha256').update(b).digest('hex')}
function comp(tag, settings){
  const input={language:'Solidity',sources:{'ViaIrVault.sol':{content:src}},settings:Object.assign({optimizer:{enabled:true,runs:200},outputSelection:{'*':{'*':['abi','evm.methodIdentifiers','evm.bytecode.object','evm.deployedBytecode.object']}}},settings)};
  const o=JSON.parse(solc.compile(JSON.stringify(input)));
  if(o.errors) for(const e of o.errors) if(e.severity==='error') throw new Error(e.formattedMessage);
  const c=o.contracts['ViaIrVault.sol']['ViaIrVault'];
  const rt=Buffer.from(c.evm.deployedBytecode.object,'hex'), cr=Buffer.from(c.evm.bytecode.object,'hex');
  fs.mkdirSync('out2/'+tag,{recursive:true});
  fs.writeFileSync('out2/'+tag+'/runtime.bin',rt); fs.writeFileSync('out2/'+tag+'/creation.bin',cr);
  fs.writeFileSync('out2/'+tag+'/abi.json',JSON.stringify(c.abi,null,2)+'\n');
  fs.writeFileSync('out2/'+tag+'/method-identifiers.json',JSON.stringify(c.evm.methodIdentifiers,null,2)+'\n');
  console.log(JSON.stringify({tag,solc:solc.version(),runtime_len:rt.length,runtime_sha256:sha(rt),creation_len:cr.length,creation_sha256:sha(cr),methodIdentifiers_sha256:sha(Buffer.from(JSON.stringify(c.evm.methodIdentifiers))) }));
}
comp('viair-opt200',{viaIR:true});
comp('viair-noopt',{viaIR:true,optimizer:{enabled:false}});
comp('std-opt200',{});
