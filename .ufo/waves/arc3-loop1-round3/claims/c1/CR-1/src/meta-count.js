const fs=require('fs');
const PUSH={0x60:1,0x61:2,0x62:3,0x63:4,0x64:5,0x65:6,0x66:7,0x67:8,0x68:9,0x69:10,0x6a:11,0x6b:12,0x6c:13,0x6d:14,0x6e:15,0x6f:16,0x70:17,0x71:18,0x72:19,0x73:20,0x74:21,0x75:22,0x76:23,0x77:24,0x78:25,0x79:26,0x7a:27,0x7b:28,0x7c:29,0x7d:30,0x7e:31,0x7f:32};
function sweep(code,end){let i=0;const out=[];while(i<end){const op=code[i];if(PUSH[op]!==undefined){const ln=PUSH[op];if(i+1+ln>code.length)break;if(op===0x63)out.push({off:i,imm:code.subarray(i+1,i+5).toString('hex')});i+=1+ln;continue;}i+=1;}return out;}
for(const f of process.argv.slice(2)){
  const code=Buffer.from(fs.readFileSync(f,'utf8').trim(),'hex');
  const cbor=code.readUInt16BE(code.length-2);
  const end=(cbor>0&&cbor<code.length-2&&code[code.length-2-cbor]===0xa2)?code.length-2-cbor:code.length;
  const full=sweep(code,code.length), codeOnly=sweep(code,end);
  const inMeta=full.filter(p=>p.off>=end);
  console.log(`${f.split('/').pop()}: bytes=${code.length} codeEnd=${end} push4(full=${full.length}, code=${codeOnly.length}) metadata-region PUSH4: ${inMeta.map(p=>p.imm+'@'+p.off).join(' ')||'(none)'}`);
}
