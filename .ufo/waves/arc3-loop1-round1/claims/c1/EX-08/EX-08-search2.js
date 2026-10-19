// EX-08: extended structural search for r3-07 81-byte dispatcher (target sha256 3e2fd6ca..fe67)
const crypto = require('crypto');
const SELS=['a9059cbb','70a08231','095ea7b3'];
const D2=['3e','44','4a'], D4=['003e','0044','004a'];
let tried=0, hits=[];
const sha=h=>crypto.createHash('sha256').update(Buffer.from(h,'hex')).digest('hex');
const prologues=['60043560e01c','60003560e01c'];
const entryForms=[
  (s,d2,d4)=>`8063${s}1460${d2}57`,   // 10
  (s,d2,d4)=>`63${s}1460${d2}57`,     // 9
  (s,d2,d4)=>`8063${s}1460${d2}5750`, // 11
  (s,d2,d4)=>`8063${s}1461${d4}57`,   // 11
  (s,d2,d4)=>`63${s}1461${d4}57`,     // 10
  (s,d2,d4)=>`8063${s}1460${d2}5b57`, // 11 (JUMPDEST before JUMPI - odd but cheap)
];
const entryLen=[10,9,11,11,10,11];
const gapFns=[n=>'00'.repeat(n), n=>'600080fd'+'00'.repeat(n-4), n=>'fd'+'00'.repeat(n-1),
              n=>'5b'+'00'.repeat(n-1), n=>'60005b'+'00'.repeat(n-3), n=>'50'.repeat(n),
              n=>'6000'.repeat(Math.floor(n/2))+'00'.repeat(n%2), n=>'56'+'00'.repeat(n-1)];
function bodyVariants(n){
  const out=[];
  for (const stub of ['01','02','03']){
    out.push('5b'+stub+'00'.repeat(n-3));
    out.push('5b'+stub+'50'.repeat(n-3));
    out.push('5b'+stub+'5b'+'00'.repeat(n-3));
    out.push('5b'+stub+'01'+'00'.repeat(n-3));
  }
  out.push('5b'+'00'.repeat(n-1));
  out.push('5b'+'50'+'00'.repeat(n-2));
  out.push('5b'+'50'.repeat(n-1));
  out.push('00'.repeat(n));
  out.push('5b'+'56'+'00'.repeat(n-2));
  out.push('5b'+'01'+'50'+'56'+'00'.repeat(n-4));
  out.push('5b'+'01'+'02'+'03'+'00'.repeat(n-4));
  out.push('5b'+'01'+'02'+'03'+'50'+'00'.repeat(n-5));
  return out.filter(h=>h.length===n*2);
}
const B=[bodyVariants(6),bodyVariants(6),bodyVariants(7)];
const perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
outer:
for (const pro of prologues){
  for (let ef=0; ef<entryForms.length; ef++){
    const gapLen=62-(pro.length/2+3*entryLen[ef]);
    if (gapLen<0) continue;
    for (const gf of gapFns){
      const gap=gf(gapLen);
      if (gap.length!==gapLen*2) continue;
      for (const perm of perms){
        for (const b0 of B[0]) for (const b1 of B[1]) for (const b2 of B[2]){
          let chain='';
          for (let k=0;k<3;k++){ const i=perm[k]; chain+=entryForms[ef](SELS[i],D2[i],D4[i]); }
          const hex=pro+chain+gap+b0+b1+b2;
          if (hex.length!==162) continue;
          tried++;
          const h=sha(hex);
          if (h.startsWith('3e2fd6ca')&&h.endsWith('fe67')){ hits.push({hex,h,pro,ef,gapLen,perm}); break outer; }
        }
      }
    }
  }
}
console.log(JSON.stringify({tried,hits:hits.length,hit:hits[0]||null}));
