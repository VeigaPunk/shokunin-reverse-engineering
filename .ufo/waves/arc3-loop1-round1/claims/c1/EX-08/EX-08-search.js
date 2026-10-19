// EX-08: bounded structural search for the r3-07 81-byte dispatcher bytes.
// Target sha256: prefix 3e2fd6ca, suffix fe67 (81 bytes, truncated in all records).
const crypto = require('crypto');
const SELS = ['a9059cbb','70a08231','095ea7b3'];
const DST = ['3e','44','4a']; // 62,68,74
const TARGET_PREFIX='3e2fd6ca', TARGET_SUFFIX='fe67';
const prologues = ['60043560e01c','60043560e01c']; // canonical: PUSH1 04 CALLDATALOAD PUSH1 e0 SHR
let tried=0, hits=[];
function sha(hex){ return crypto.createHash('sha256').update(Buffer.from(hex,'hex')).digest('hex'); }
const entryForms = [
  s=>`8063${s}1460`,
  s=>`63${s}1460`,
  s=>`8063${s}146050`,
];
const gaps = [n=>'00'.repeat(n), n=>'600080fd'+'00'.repeat(n-4), n=>'5b'+'00'.repeat(n-1), n=>'60005b'+'00'.repeat(n-3)];
const bodies = [n=>'5b'+'01'+'00'.repeat(n-3), n=>'5b'+'50'+'00'.repeat(n-3), n=>'5b'+'00'.repeat(n-1)];
const perms = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
for (const pro of prologues){
  for (let ef=0; ef<entryForms.length; ef++){
    const efLen = ef===1?9: ef===2?11:10;
    const gapLen = 62 - (pro.length/2 + 3*efLen);
    if (gapLen<0) continue;
    for (let g=0; g<gaps.length; g++){
      const gap = gaps[g](gapLen);
      if (gap.length/2 !== gapLen) continue;
      for (const perm of perms){
        // body sizes: 62..67 (6B), 68..73 (6B), 74..80 (7B)
        const sizes=[6,6,7];
        for (let b0=0;b0<bodies.length;b0++) for (let b1=0;b1<bodies.length;b1++) for (let b2=0;b2<bodies.length;b2++){
          const bl=[bodies[b0](sizes[0]),bodies[b1](sizes[1]),bodies[b2](sizes[2])];
          if (bl.some((x,i)=>x.length/2!==sizes[i])) continue;
          let chain='';
          for (let k=0;k<3;k++){ const sel=SELS[perm[k]]; const dst=DST[perm[k]];
            chain += entryForms[ef](sel)+dst+'57'; }
          const hex = pro+chain+gap+bl.join('');
          if (hex.length!==162) continue;
          tried++;
          const h=sha(hex);
          if (h.startsWith(TARGET_PREFIX) && h.endsWith(TARGET_SUFFIX)) hits.push({hex,h});
        }
      }
    }
  }
}
console.log(JSON.stringify({tried, hits: hits.length, hit: hits[0]||null}));
