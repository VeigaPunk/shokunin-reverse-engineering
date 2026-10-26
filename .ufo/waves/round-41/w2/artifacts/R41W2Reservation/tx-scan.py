#!/usr/bin/env python3
"""Transcript scan: every toolCall of every wave-1 seat (+ planner KaidokuR41, KengakuR41): which can run REA/unblob
(directly or through a harness script), and which name reserved identifiers.
usage: tx-scan.py <session dir> <w1 swarm-registry.json> <out.json>"""
import json,os,re,sys
D,REG,OUT=sys.argv[1:4]
members=sorted(json.load(open(REG))['members'])+['KaidokuR41','KengakuR41']
PIN8='c4f74f54|ce27ebca|04cfb4cd|4c0e5459|770efb4e|a5a3a763|87cc5d6b|4cfc3016|4d5de25c'
RES=re.compile(PIN8+r'|5490|5491|filesystem_core|FRITZ|fritzbox|download\.avm|/c1/(V3|V4|L3|L4)\b|\b(V3|V4|L3|L4)/carrier|\bcarrier-?(L3|L4|V3|V4)\b',re.I)
RUN=re.compile(r'extract-firmware|rea-agents|REA_UNBLOB|\bunblob\b|c1-run\.sh|c1-counter\.py|run-all\.sh|commands\.sh|probe\.sh|run-dev\.sh|heldout-gen|comboprobe|nested\.py|flat\.py|attack-controls|\bnpx\b')
rows=[];tot=0;perseat={}
for m in members:
    fs=[f for f in sorted(os.listdir(D)) if re.fullmatch(re.escape(m)+r'(-\d+)?\.jsonl',f)]
    if not fs: perseat[m]=None; continue
    n=0
    for f in fs:
        for l in open(os.path.join(D,f)):
            try:d=json.loads(l)
            except Exception: continue
            c=(d.get('message') or {}).get('content')
            if not isinstance(c,list): continue
            for b in c:
                if b.get('type')!='toolCall': continue
                n+=1;tot+=1
                a=json.dumps(b.get('arguments'),ensure_ascii=False)
                rr=bool(RES.search(a)); ru=bool(RUN.search(a))
                if ru or rr:
                    rows.append(dict(seat=m,file=f,ts=d.get('timestamp'),tool=b.get('name'),run=ru,res=rr,
                      res_hits=sorted(set(x.group(0) for x in RES.finditer(a)))[:6],
                      run_hits=sorted(set(x.group(0) for x in RUN.finditer(a)))[:6],args=a[:2500]))
    perseat[m]=dict(toolcalls=n,files=fs)
json.dump(dict(members=members,per_seat=perseat,total=tot,rows=rows),open(OUT,'w'),indent=1)
print('seats',len(members),'no transcript:',[m for m,v in perseat.items() if v is None],'toolcalls',tot)
print('RUN-capable:',sum(r['run'] for r in rows),' naming reserved:',sum(r['res'] for r in rows),' BOTH:',sum(r['run'] and r['res'] for r in rows))
