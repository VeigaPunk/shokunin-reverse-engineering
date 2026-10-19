// Census with metadata exclusion + two-tier dispatch classification.
const fs=require('fs');
const PUSH={0x60:1,0x61:2,0x62:3,0x63:4,0x64:5,0x65:6,0x66:7,0x67:8,0x68:9,0x69:10,0x6a:11,0x6b:12,0x6c:13,0x6d:14,0x6e:15,0x6f:16,0x70:17,0x71:18,0x72:19,0x73:20,0x74:21,0x75:22,0x76:23,0x77:24,0x78:25,0x79:26,0x7a:27,0x7b:28,0x7c:29,0x7d:30,0x7e:31,0x7f:32};
function sweep(code,end){let i=0,push4=[],jd=new Set();while(i<end){const op=code[i];if(op===0x5b)jd.add(i);if(PUSH[op]!==undefined){const ln=PUSH[op];if(i+1+ln>code.length)break;if(op===0x63)push4.push({off:i,imm:code.subarray(i+1,i+5).toString('hex')});i+=1+ln;continue;}i+=1;}return{push4,jd};}
function cat(code,p){const w=code.subarray(p.off+5,p.off+12).toString('hex');if(/^1161/.test(w))return'GT';if(/^1461/.test(w))return'EQ';if(/^8014|^14/.test(w))return'EQ';if(/^10/.test(w))return'LT';return'?';}
for(const f of process.argv.slice(2)){
  const hex=fs.readFileSync(f,'utf8').trim().replace(/^0x/,'');
  const code=Buffer.from(hex,'hex');
  if(code.length<4){console.log(`${f}: ${code.length}B`);continue;}
  const cborLen=code.readUInt16BE(code.length-2);
  const codeEnd=(cborLen>0&&cborLen<code.length-2&&code[code.length-2-cborLen]===0xa2)?code.length-2-cborLen:code.length;
  const {push4,jd}=sweep(code,codeEnd);
  const kinds={};for(const p of push4)kinds[cat(code,p)]=(kinds[cat(code,p)]||0)+1;
  const uniq=[...new Set(push4.map(p=>p.imm))].sort();
  const nonDispatch=push4.filter(p=>cat(code,p)==='?');
  console.log(`${f}`);
  console.log(`  bytes=${code.length} codeEnd=${codeEnd} push4(code)=${push4.length} uniq=${uniq.length} kinds=${JSON.stringify(kinds)} jd=${jd.size}`);
  console.log(`  uniq: ${uniq.join(' ')}`);
  console.log(`  non-dispatch-shaped: ${nonDispatch.map(p=>p.imm+'@'+p.off).join(' ')||'(none)'} | dupes: ${uniq.filter(s=>push4.filter(p=>p.imm===s).length>1).join(' ')||'(none)'}`);
}
