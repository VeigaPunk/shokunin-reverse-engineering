const fs=require('fs'),crypto=require('crypto');
const files=process.argv.slice(2);
for(const f of files){
  const hex=fs.readFileSync(f,'utf8').trim().replace(/^0x/,'');
  const code=Buffer.from(hex,'hex');
  if(code.length<4){console.log(`${f}: ${code.length} bytes (skip)`);continue;}
  const cborLen=code.readUInt16BE(code.length-2);
  const codeEnd=code.length-2-cborLen;
  console.log(`${f}: bytes=${code.length} cborLen=${cborLen} codeEnd=${codeEnd} cborPrefix=${code.subarray(codeEnd,codeEnd+8).toString('hex')}`);
  for(const probe of ['16ee4b79','4e487b71','fe741b56']){
    const n=Buffer.from(probe,'hex');let i=0,offs=[];while(true){const p=code.indexOf(n,i);if(p<0)break;offs.push(p);i=p+1;}
    if(offs.length)console.log(`   ${probe} @ [${offs.join(',')}] -> ${offs.map(o=>o<codeEnd?'CODE':'METADATA').join(',')}`);
  }
}
