const fs=require('fs');
const {keccak256}=require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');
const norm=s=>String(s).replace(/^0x/,'').toLowerCase();
function sigsFromAbi(p){const abi=JSON.parse(fs.readFileSync(p,'utf8'));
 return abi.filter(e=>e.type==='function').map(e=>e.name+'('+(e.inputs||[]).map(i=>i.type).join(',')+')');}
const C='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/';
const legs=[
 ['VaultB.opt200','EX-10/out/VaultB.opt200.abi.json','EX-10/probe/probe-B-opt200-hex-6.4.0.json','EX-10/planted-K.json','json'],
 ['VaultB.nopt','EX-10/out/VaultB.nopt.abi.json','EX-10/probe/probe-B-nopt-hex-6.4.0.json','EX-10/planted-K.json','json'],
 ['carrierB.opt200','EX-04/evidence/carrierB.abi-opt200.json','EX-04/evidence/probe/probe-opt200-hex-6.4.0.json','EX-04/planted-B.txt','txt'],
 ['carrierB.noopt','EX-04/evidence/carrierB.abi-noopt.json','EX-04/evidence/probe/probe-noopt-hex-6.4.0.json','EX-04/planted-B.txt','txt'],
 ['CarrierB','EX-05/out/CarrierB.abi.json','EX-05/probe/probe-runtime-hex-6.4.0.json','EX-05/planted-K.json','json'],
 ['CarrierBErr','EX-05/attack/out/CarrierBErr.abi.json','EX-05/attack/probe-runtime-hex-6.4.0.json','EX-05/expected-selectors.txt','txt'],
 ['Rv2TokenOpt','EX-07/Rv2TokenOpt.abi.json','EX-07/optB-hex-6.4.0.json','EX-07/Rv2TokenOpt.planted-K.json','json'],
];
const setEq=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
for(const [name,abiP,envP,plantedP,kind] of legs){
 const mine=new Set(sigsFromAbi(C+abiP).map(s=>keccak256(s).slice(0,8)));
 const env=new Set(JSON.parse(fs.readFileSync(C+envP,'utf8')).normalized_result.functions.map(f=>norm(f.selector)));
 let planted;
 if(kind==='txt'){
   const lines=fs.readFileSync(C+plantedP,'utf8').trim().split('\n');
   planted=new Set(lines.map(l=>l.trim()).filter(l=>l&&!l.startsWith('K=')).map(l=>norm(l.split(/\s+/)[0])));
 } else {
   const p=JSON.parse(fs.readFileSync(C+plantedP,'utf8'));
   planted=new Set((p.entries||p.functions||p.selectors||[]).map(e=>norm(typeof e==='string'?e:(e.selector||e.sel||''))));
 }
 console.log(`${name}: K abi=${mine.size} env=${env.size} planted=${planted.size} | abi==env ${setEq(mine,env)} abi==planted ${setEq(mine,planted)}`);
}
