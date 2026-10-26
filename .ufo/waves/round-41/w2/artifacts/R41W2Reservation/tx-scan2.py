#!/usr/bin/env python3
"""Pass 2: every bash/eval toolCall (all wave-1 seats) that references another seat's reserved-carrier source
(LCarriers artifacts, VendorV3/V4 scratch or artifacts, the shared vendor cache, or a wildcard over carriers) --
the only ways reserved bytes could reach a REA/unblob-capable command in a non-owner seat."""
import json,os,re,sys
D,REG,OUT=sys.argv[1:4]
members=sorted(json.load(open(REG))['members'])+['KaidokuR41','KengakuR41']
PATH=re.compile(r'R41C1LCarriers|R41C1VendorV3|R41C1VendorV4|R41C1Fetch|kaidoku-r41/cache|\bcarriers\.json|fetch-vendor|c1/(V3|V4|L3|L4)|carrier\.sqsh|\*/carrier|\.bin\b.*sha|filesystem\.image')
EXE=re.compile(r'extract-firmware|REA_UNBLOB|\bunblob\b|rea-agents|c1-run\.sh|c1-counter\.py|\bnpx\b')
rows=[]
for m in members:
    for f in sorted(os.listdir(D)):
        if not re.fullmatch(re.escape(m)+r'(-\d+)?\.jsonl',f): continue
        for l in open(os.path.join(D,f)):
            try:d=json.loads(l)
            except Exception: continue
            c=(d.get('message') or {}).get('content')
            if not isinstance(c,list): continue
            for b in c:
                if b.get('type')!='toolCall' or b.get('name') not in ('bash','eval'): continue
                a=b.get('arguments') or {}
                t=(a.get('command') or a.get('code') or json.dumps(a))
                if EXE.search(t):
                    rows.append(dict(seat=m,ts=d.get('timestamp'),tool=b['name'],path_refs=sorted(set(x.group(0) for x in PATH.finditer(t))),cmd=t[:1200]))
json.dump(rows,open(OUT,'w'),indent=1)
import collections
print('exec-capable bash/eval calls:',len(rows))
c=collections.Counter(r['seat'] for r in rows if r['path_refs'])
print('with path refs:',sum(c.values()),dict(c))
