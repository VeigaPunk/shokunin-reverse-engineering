// CR-1 attack-2 checker: ABI-derived planted set vs actual dispatch sites in the runtime.
// usage: node abi-vs-dispatch.js <abi.json> <runtime.hex|runtime.bin> [label]
const fs = require('fs');
const { keccak256 } = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');
const PUSH = { 0x60:1,0x61:2,0x62:3,0x63:4,0x64:5,0x65:6,0x66:7,0x67:8,0x68:9,0x69:10,0x6a:11,0x6b:12,0x6c:13,0x6d:14,0x6e:15,0x6f:16,0x70:17,0x71:18,0x72:19,0x73:20,0x74:21,0x75:22,0x76:23,0x77:24,0x78:25,0x79:26,0x7a:27,0x7b:28,0x7c:29,0x7d:30,0x7e:31,0x7f:32 };
function canon(i){ if(i.type==='tuple'||i.type.startsWith('tuple')){const inner=(i.components||[]).map(canon).join(','); return (i.type==='tuple'?'':i.type.replace('tuple',''))+'('+inner+')';} return i.type; }
function census(code){ const cbor=code.readUInt16BE(code.length-2); const end=(cbor>0&&cbor<code.length-2&&code[code.length-2-cbor]===0xa2)?code.length-2-cbor:code.length;
  let i=0; const eq=[];
  while(i<end){ const op=code[i]; if(PUSH[op]!==undefined){const ln=PUSH[op]; if(i+1+ln>code.length)break;
    if(op===0x63){const imm=code.subarray(i+1,i+5).toString('hex'); let j=i+5,comp=null,g=0;
      while(j<end&&g<4){const o2=code[j]; if(o2===0x14){comp='EQ';j++;g++;continue;} if(o2===0x10||o2===0x11){comp=o2===0x10?'LT':'GT';j++;g++;continue;} if(o2>=0x80&&o2<=0x82){j++;g++;continue;} break;}
      if(comp==='EQ'&&code[j]===0x61&&code[j+3]===0x57)eq.push({imm,off:i,dest:code.readUInt16BE(j+1)});}
    i+=1+ln;continue;} i+=1;}
  return {end, eqSet:[...new Set(eq.map(e=>e.imm))].sort(), eq};}
const abi=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const raw=fs.readFileSync(process.argv[3],'utf8').trim();
const code=/^[0-9a-fA-F\s]+$/.test(raw.slice(0,80))&&!process.argv[3].endsWith('.bin')?Buffer.from(raw.replace(/\s/g,''),'hex'):Buffer.from(raw,'hex');
const label=process.argv[4]||process.argv[3];
const fns=[],others=[];
for(const e of abi){ if(!e.name){others.push(e.type+'(nameless)');continue;} const sig=e.name+'('+(e.inputs||[]).map(canon).join(',')+')'; const sel=keccak256(sig).slice(0,8);
  if(e.type==='function')fns.push({sig,sel}); else others.push(`${e.type}:${sig}=${sel}`);}
const {end,eqSet,eq}=census(code);
const pset=new Set(fns.map(f=>f.sel));
const missing=fns.filter(f=>!eqSet.includes(f.sel));
const extras=eqSet.filter(s=>!pset.has(s));
console.log(`\n[${label}] abiEntries=${abi.length} fns=${fns.length} nonFn=${others.length} codeEnd=${end} eqDispatchSites=${eqSet.length}`);
console.log(`  ABI functions missing from dispatch (unreachable/dropped): ${missing.length? missing.map(m=>m.sig+'='+m.sel).join(' '):'(none)'}`);
console.log(`  dispatch selectors NOT in ABI functions: ${extras.length? extras.join(' '):'(none)'}`);
if(others.length) console.log(`  non-function ABI entries (no dispatch expected): ${others.join(' ')}`);
const shared={}; for(const s of eq)(shared[s.dest]=shared[s.dest]||[]).push(s.imm);
const sh=Object.entries(shared).filter(([,v])=>v.length>1);
if(sh.length)console.log(`  shared bodies (optimizer dedup): ${sh.map(([d,v])=>'dest'+d+'<-'+v.join('/')).join('; ')}`);