const fs=require('fs');
function push4sites(binPath){
 const buf=fs.readFileSync(binPath);
 const sites=[];
 for(let pc=0;pc<buf.length;pc++){
   const op=buf[pc];
   if(op===0x63){ // PUSH4
     sites.push({pc, val:buf.slice(pc+1,pc+5).toString('hex')});
     pc+=4;
   } else if(op>=0x60&&op<=0x7f){ pc+=op-0x5f; }
   else if(op===0x5f||op===0x5b||(op>=0x80&&op<=0x8f)||op===0x00||(op>=0x30&&op<=0x4f)||(op>=0x50&&op<=0x5a)||(op>=0xf0&&op<=0xfd)||op===0xfe||op===0xff){}
   else if((op>=0x90&&op<=0x9f)||(op>=0xa0&&op<=0xa4)||(op>=0x60&&op<=0x7f)){}
   else if(op>=0x60&&op<=0x7f){}
 }
 return sites;
}
const C='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/';
for(const [n,p] of [['Rv2TokenOpt',C+'EX-07/Rv2TokenOpt.runtime.bin'],['VaultB.opt200',C+'EX-10/out/VaultB.opt200.runtime.bin'],['VaultB.nopt',C+'EX-10/out/VaultB.nopt.runtime.bin']]){
 const buf=fs.readFileSync(p);
 const sites=push4sites(p);
 console.log(n,'bytes',buf.length,'PUSH4 sites',sites.length);
 console.log('  vals:',sites.map(s=>s.val).join(' '));
 console.log('  first bytes:',buf.slice(0,12).toString('hex'));
 // CBOR trailer detection: last two bytes length
 const tail=buf.slice(-2); const cborLen=tail[1]; const cborStart=buf.length-cborLen;
 console.log('  cborLen',cborLen,'cborStart',cborStart,'code region ends',cborStart);
 for(const s of sites){ if(s.pc>=cborStart) console.log('   TRAILER site',s.pc,s.val); }
}
