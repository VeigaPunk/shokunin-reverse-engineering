# Replica of c1-counter.py registry loop (lines 2172-2184), read-only.
import re, sys
ENTRY = 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
STEM = '2026-10-28-r49-squashfs-v1v2-core'
OPENED = '2026-10-28'
def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]
ok = []
for line in open(sys.argv[1], encoding='utf-8'):
    if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
        continue
    c = cells(line)
    if len(c) != 11:
        print('BAD len', c[0], len(c)); continue
    if c[0] in ('S138', 'S139'):
        print(c[0], 'opened=', repr(c[8]), 'opened_ok=', c[8] == OPENED,
              'entry_in_used_by=', (ENTRY in c[10] or STEM in c[10]), 'used-by=', c[10])
        if c[8] == OPENED and (ENTRY in c[10] or STEM in c[10]):
            ok.append(c[0])
print('opened_source_rows', ok, 'sourced(S138&S139)=', {'S138', 'S139'} <= set(ok))
