import json,sys
sys.path.insert(0,'/fast/scratch/hyaku/kaidoku-r49/C2CounterMut')
R=json.load(open('results-raw.json')); F=json.load(open('forgeries.json'))
def sig(r): return (r['exit'], r['mismatches'], tuple(r['red']), r['reason'], tuple(r['battery_failing'] or []))
O=R['ORIG']
print('ORIG green-battery', O['green-battery']['exit'], O['green-battery']['mismatches'], O['green-battery']['battery_failing'], O['green-battery']['do_nothing_red'])
print('ORIG green', O['green']['exit'], O['green']['mismatches'])
print('ORIG freeze', O['freeze']['exit'], O['freeze']['mismatches'], O['freeze']['red'])
print('ORIG_BB green-battery', R['ORIG_BB']['green-battery']['exit'], R['ORIG_BB']['green-battery']['battery_failing'])
print()
# forgeries
mis=[]
acc=[]
for f in F:
    o=O['F:'+f['id']]; ob=O['F:'+f['id']+':battery'] if 'F:'+f['id']+':battery' in O else None
    got='accept' if o['exit']==0 else 'reject'
    if got!=f['expect_orig']: mis.append((f['id'],f['expect_orig'],got,o['exit'],o['red'],o['reason']))
    if got=='accept': acc.append((f['id'],ob['exit'] if ob else None, ob['battery_failing'] if ob else None, ob['mut_red'] if ob else None))
print('forgery expectation mismatches:', mis)
print('accepted by ORIG:', acc)
print('rejected by ORIG:', [(f['id'], O['F:'+f['id']]['exit'], O['F:'+f['id']]['red'], O['F:'+f['id']]['reason']) for f in F if O['F:'+f['id']]['exit']!=0])
