const fs=require('fs'), path=require('path'), crypto=require('crypto');
const [prefix, srcPath, outPath, optFlag, runsArg] = process.argv.slice(2);
const solc=require(path.join(prefix,'node_modules','solc'));
const src=fs.readFileSync(srcPath,'utf8');
const input={language:'Solidity',sources:{'C.sol':{content:src}},settings:{optimizer:{enabled:optFlag==='1',runs:runsArg?parseInt(runsArg,10):200},outputSelection:{'*':{'*':['evm.deployedBytecode.object']}}}};
const out=JSON.parse(solc.compile(JSON.stringify(input)));
if(out.errors) for(const e of out.errors) if(e.severity==='error'){console.error(e.formattedMessage);process.exit(1);}
const b=Buffer.from(out.contracts['C.sol']['C'].evm.deployedBytecode.object,'hex');
fs.writeFileSync(outPath,b);
console.log(crypto.createHash('sha256').update(b).digest('hex'));
