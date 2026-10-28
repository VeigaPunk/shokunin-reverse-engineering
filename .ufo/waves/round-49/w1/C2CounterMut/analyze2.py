import json
R=json.load(open('results-raw.json')); F=json.load(open('forgeries.json'))
def sig(r): return (r['exit'], r['mismatches'], tuple(r['red']), r['reason'], tuple(r['battery_failing'] or []))
O=R['ORIG']
ids=[f['id'] for f in F]
rows=[]
for mid in sorted(R):
    if mid=='ORIG': continue
    r=R[mid]
    gb=r['green-battery']; g=r['green']; fz=r['freeze']
    gen_kill = []
    if gb['exit']!=0 or gb['battery_failing']: gen_kill.append('battery:%s'%(gb['battery_failing'] or gb['exit']))
    if g['exit']!=0 or g['mismatches']!=0: gen_kill.append('green-run:exit%s'%g['exit'])
    if fz['exit']!=1 or fz['mismatches']!=9: gen_kill.append('freeze:exit%s/m%s'%(fz['exit'],fz['mismatches']))
    fk=[]
    for fid in ids:
        a=R[mid]['F:'+fid]; b=O['F:'+fid]
        if sig(a)!=sig(b): fk.append(fid)
    rows.append((mid, gen_kill, fk))
for mid,gk,fk in rows:
    st = 'KILLED' if (gk or fk) else 'SURVIVED'
    print(mid, st, '| genuine/battery:', gk or '-', '| forgeries:', ','.join(fk) or '-')
print()
# sanity: forgery battery for ORIG on accepted
