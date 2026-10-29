#!/usr/bin/env python3
"""scan-stats.py (PlanClaimSizing draft): classify rows of l1/scan-output.txt (format of l1/scan.py).
Row kinds: err (exception text), noimage, bogus (magic not a superblock: b'./va'), hsqs-avm (LE v4.0 comp4 mkfs==bytes_used),
sqsh-avm (BE, any version with mkfs==bytes_used), std (mkfs!=bytes_used), other."""
import ast, collections, sys
rows = []
for line in open(sys.argv[1], encoding='utf-8'):
    line = line.rstrip('\n')
    if line:
        m, rest = line.split(' ', 1); rows.append((m, rest))
kinds = collections.defaultdict(list)
for m, r in rows:
    if r.startswith('err'): kinds['err'].append(m); continue
    if r.startswith('noimage'): kinds['noimage'].append(m); continue
    t = ast.literal_eval(r)
    name, mg, maj, mi, _, comp, tag, size = t
    if mg == b'./va': kinds['bogus'].append(m)
    elif mg == b'hsqs' and tag == 'avm' and comp == 4 and (maj, mi) == (4, 0): kinds['hsqs-avm'].append(m)
    elif mg == b'sqsh' and tag == 'avm': kinds['sqsh-avm'].append(m)
    elif tag == 'std': kinds['std'].append(m)
    else: kinds['other'].append(m)
print('rows', len(rows), 'unique models', len({m for m, _ in rows}))
for k in ('hsqs-avm', 'sqsh-avm', 'std', 'other', 'bogus', 'err', 'noimage'):
    print(k, len(kinds[k]), ' '.join(kinds[k]))
print('sum', sum(len(v) for v in kinds.values()))
