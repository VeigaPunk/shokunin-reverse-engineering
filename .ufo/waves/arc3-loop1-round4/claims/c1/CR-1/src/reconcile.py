import json, sys, os, glob
def load(p):
    try: return json.load(open(p))
    except Exception as e: return None
rows=[]
for f in sorted(glob.glob('probe/*.6.4.0.json')):
    b=os.path.basename(f).replace('.6.4.0.json','')
    j=load(f)
    if not j: rows.append((b,'PARSE-FAIL',None,None)); continue
    d=j.get('data',j)
    nr=d.get('normalized_result',{})
    funcs=nr.get('functions',[])
    probe=set(x['selector'].replace('0x','') for x in funcs)
    mids=load(f'vyout/{b}.methodids.json') or {}
    planted=set(v.replace('0x','') for v in mids.values())
    missing=sorted(planted-probe); extra=sorted(probe-planted)
    dec=nr.get('bytecode',{}).get('sha256','')[:12]
    rows.append((b,len(planted),len(probe),missing,extra,dec,d.get('evidence_id','')[:14]))
print(f"{'carrier':8} {'Kplant':6} {'Kprobe':6} {'missing':34} {'extra':34} decoded      evid")
allok=True
for r in rows:
    if r[1]=='PARSE-FAIL': print(r); continue
    b,kp,kn,miss,ext,dec,ev=r
    ok = (not miss) and (not ext) and kp==kn
    allok = allok and ok
    print(f"{b:8} {kp:<6} {kn:<6} {str(miss):34} {str(ext):34} {dec:12} {ev} {'' if ok else '<<< MISMATCH'}")
print()
print("ALL K/K:", allok)
