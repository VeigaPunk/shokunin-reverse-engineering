#!/usr/bin/env python3
"""Emit parsed cells of the 12 attempt-1 rows + padding audit of all 54 rows."""
import subprocess, re, json

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
sk = subprocess.run(['git', '-c', 'core.quotePath=false', '-C', LANE, 'cat-file', 'blob',
                     '%s:SKILL.md' % BASE], capture_output=True, check=True).stdout.decode('utf-8', 'replace')
lines = sk.split('\n')
o = next(i for i, l in enumerate(lines) if l.strip() == '<!-- instrument-registry v2 -->')
cl = next(i for i, l in enumerate(lines) if l.strip() == '<!-- /instrument-registry -->')

ATTEMPT1 = ['tools/round-49/c1-counter.py', 'tools/round-49/c1-controls.py',
            'tools/round-49/c1-oracle.py', 'tools/round-49/c1-run.py',
            'tools/round-49/c1-run.sh', 'tools/round-49/c2-mismatch.py',
            'tools/round-50/c1-counter.py', 'tools/round-50/c1-run.sh',
            'tools/round-50/c1-controls.py', 'tools/round-50/fetch-vendor.py',
            'tools/round-50/c2-record.py', 'tools/round-50/selftest-r49-c2.py']

out = {'rows': []}
padding_bad = []
for n in range(o + 1, cl):
    l = lines[n]
    if not re.match(r'^ {0,3}\|\s*`', l):
        continue
    m = re.match(r'^ {0,3}\|\s*`([^`]*)`', l)
    key = m.group(1)
    c = [x.strip().replace('\x01', '|') for x in l.strip().replace('\\|', '\x01').split('|')]
    cs = c[1:-1]
    # padding audit: every pipe boundary should be exactly ' | ' (one space each side)
    if re.search(r' {2,}\||\| {2,}(?!\|)', l):
        padding_bad.append({'line': n + 1, 'key': key})
    if key in ATTEMPT1:
        out['rows'].append({'line': n + 1, 'cells': cs})

out['padding_bad'] = padding_bad
print(json.dumps(out, indent=1, ensure_ascii=False))
json.dump(out, open('/fast/scratch/hyaku/kaidoku-r50/w3-RevB9Registry/attempt1-cells.json', 'w'), indent=1, ensure_ascii=False)
