import json
from collections import Counter
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
items=json.load(open(L+'/.ufo/waves/round-44/w1-spec.json'))['items']
c=Counter(i['role'] for i in items)
n=len(items)
print('seats',n); print('roles',dict(c))
narrow={'reviewer','critic','mutation-tester','labrat'}
wide=narrow|{'revenger','sentinel','connector'}
print('policy attack set (reviewer/critic/mutation-tester/labrat):',sum(c[r] for r in narrow),f'{100*sum(c[r] for r in narrow)/n:.1f}%')
print('wide set (policy + revenger/sentinel/connector):',sum(c[r] for r in wide),f'{100*sum(c[r] for r in wide)/n:.1f}%')
print('policy + revenger/sentinel/connector (excl simplifier): 13/37 = 35.1%')
