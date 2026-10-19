const fs=require('fs'), crypto=require('crypto');
const solc=require('/var/tmp/cr03-r6/s2828/node_modules/solc');
const src=fs.readFileSync('ViaIrVault.sol','utf8');
function sha(b){return crypto.createHash('sha256').update(b).digest('hex')}
const input={language:'Solidity',sources:{'ViaIrVault.sol':{content:src}},settings:{viaIR:true,optimizer:{enabled:true,runs:200},outputSelection:{'*':{'*':['abi','evm.methodIdentifiers','evm.bytecode.object','evm.deployedBytecode.object']}}}};
const o=JSON.parse(solc.compile(JSON.stringify(input)));
if(o.errors) for(const e of o.errors){ if(e.severity==='error'){console.error(e.formattedMessage);process.exit(1)} else console.error('warn',e.formattedMessage.trim().slice(0,160)); }
const c=o.contracts['ViaIrVault.sol']['ViaIrVault'];
const rt=Buffer.from(c.evm.deployedBytecode.object,'hex'), cr=Buffer.from(c.evm.bytecode.object,'hex');
fs.mkdirSync('out2828/viair-opt200',{recursive:true});
fs.writeFileSync('out2828/viair-opt200/runtime.bin',rt); fs.writeFileSync('out2828/viair-opt200/creation.bin',cr);
fs.writeFileSync('out2828/viair-opt200/abi.json',JSON.stringify(c.abi,null,2)+'\n');
fs.writeFileSync('out2828/viair-opt200/method-identifiers.json',JSON.stringify(c.evm.methodIdentifiers,null,2)+'\n');
console.log(JSON.stringify({solc:solc.version(),runtime_len:rt.length,runtime_sha256:sha(rt),creation_len:cr.length,creation_sha256:sha(cr),mid_keys:Object.keys(c.evm.methodIdentifiers).length}));
