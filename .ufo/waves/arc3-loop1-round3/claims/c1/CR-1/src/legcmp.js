const fs=require('fs');
const rows=[];
for(const f of fs.readdirSync('probe').filter(x=>x.endsWith('.json')).sort()){
  const j=JSON.parse(fs.readFileSync('probe/'+f,'utf8'));
  const nr=j.normalized_result;
  rows.push({file:f, ev:j.evidence_id.slice(0,14), subject:j.subject.digest.sha256.slice(0,12),
    decoded:(nr.bytecode&&nr.bytecode.sha256||'?').slice(0,12), bytes:nr.bytecode&&nr.bytecode.bytes,
    n:nr.functions.length, sels:nr.functions.map(x=>x.selector.slice(2)).sort().join(','),
    disp:[...new Set(nr.functions.map(x=>x.dispatch))].join('|')});
}
const byDecoded={};
for(const r of rows){(byDecoded[r.decoded]=byDecoded[r.decoded]||[]).push(r);}
for(const r of rows)console.log(`${r.file.padEnd(30)} subj=${r.subject} decoded=${r.decoded} bytes=${r.bytes} n=${r.n} dispatch=${r.disp}`);
console.log('\n--- per decoded-digest groups (costume agreement) ---');
for(const [d,rs] of Object.entries(byDecoded)){
  const sels=new Set(rs.map(r=>r.sels));
  console.log(`${d}: ${rs.length} envelopes [${rs.map(r=>r.file.replace('.json','')).join(', ')}] selsEqual=${sels.size===1} nSame=${new Set(rs.map(r=>r.n)).size===1}`);
}
// vs compiled binaries
const crypto=require('crypto');
for(const c of ['Cr1OptToken','Cr1Vault','Cr1Dedup','Cr1Lib']){
  for(const tag of ['opt200','noopt']){
    const b=fs.readFileSync(`out/${c}.${tag}.runtime.hex`,'utf8').trim();
    const h=crypto.createHash('sha256').update(Buffer.from(b,'hex')).digest('hex').slice(0,12);
    const txt=crypto.createHash('sha256').update(b).digest('hex').slice(0,12);
    const txtNl=crypto.createHash('sha256').update(b+'\n').digest('hex').slice(0,12);
    console.log(`${c}.${tag}: bytes.sha256=${h} hextext(no-nl)=${txt} hextext(nl)=${txtNl}`);
  }
}
