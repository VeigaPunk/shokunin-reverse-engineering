import json
rule=json.load(open('tools/round-50/gap-rule.json'))
for c in ['g7581','g7582','c6490','c6430']:
    d=json.load(open(f'corpus/evidence/round-50/c1/{c}/after.json')); nr=d['normalized_result']
    nonreg=[]
    for line in open(f'tools/round-50/oracle/{c}.nonregular.tsv'):
        p=line.rstrip('\n').split('\t')
        if len(p)>=2: nonreg.append((p[0],p[1],p[2] if len(p)>2 else ''))
    gapped=set()
    for g in nr['extraction_gaps']:
        rp=g.get('relative_path')
        if rp and g['kind']!='depth-limited': gapped.add(rp.split('firmware.bin_extract/')[-1])
    rem=set()
    for x in nr['diagnostics']:
        r=x['report']
        if r.get('__typename__')==rule['removed']['diagnostic']: rem.add(r['link'].split('firmware.bin_extract/')[-1])
    missing=[]; silent=0
    for rel,kind,detail in nonreg:
        need=rule['required'].get(kind, bool(rule['allowed'].get(kind)))
        if not need: continue
        if rel in gapped or rel in rem: continue
        if detail in (rule['removed'].get('silent') or {}).get(kind,[]): silent+=1; continue
        missing.append((rel,kind,detail))
    print(f'{c}: nonregular={len(nonreg)} gapped={len(gapped)} removed={len(rem)} silent={silent} MISSING={len(missing)}')
    for m in missing: print('   ', m)
