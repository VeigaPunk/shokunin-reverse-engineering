import json,os,sys
LANE=sys.argv[1]
C=LANE+'/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes'
cen={}
for line in open(LANE+'/.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt'):
    if line.startswith('squashfs_v3'):
        p=line.split()
        if len(p)>=6: cen[p[2]]=(p[0],p[1],p[3],p[4],p[5])
rec=json.load(open(LANE+'/.ufo/waves/round-50/c3/c3-after.json'))
lab={e['envelope']:(e['evaluator_label'],e['evaluator_action']) for e in rec['envelopes']}
rows=[]
for n in sorted(os.listdir(C)):
    fp=os.path.join(C,n,'envelope.json')
    if not os.path.exists(fp): continue
    d=json.load(open(fp)); data=d.get('data',d)
    sha=((data.get('subject') or {}).get('digest') or {}).get('sha256','')
    s12=sha[:12]
    hit=cen.get(s12)
    fam=hit[0] if hit else '-'
    verdict=hit[4] if hit else '(no census row)'
    rows.append((n,fam,s12,verdict))
print('=== corpus envelopes bound to a reader-census row (sha256[:12]) ===')
for n,f,s,v in rows:
    if v!='(no census row)': print('%-46s %-22s %s %s'%(n,f,s,v))
print()
print('=== NO-READER bodies whose v5 label is clean/none (oracle match prescribed) ===')
for n,f,s,v in rows:
    if v.startswith('NO-READER') and lab.get(n,('',''))[0]=='clean':
        print('%-46s %-22s %s %s'%(n,f,s,lab[n]))
print()
print('=== FAILED bodies (extractor-failure) and their census verdict ===')
for e in rec['envelopes']:
    g=e['features'].get('G') or []
    if 'extractor-failure' in g:
        n=e['envelope']
        hit=[r for r in rows if r[0]==n]
        v=hit[0][3] if hit else '?'
        print('%-46s %-22s %-18s %s'%(n,e['evaluator_label'],e['evaluator_action'],v))
