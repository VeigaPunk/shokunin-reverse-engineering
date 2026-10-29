#!/usr/bin/env python3
"""Raw cell-shape drift scan of the instrument-registry region at base f890bbe."""
import subprocess, re, sys, json

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
REG_OPEN = '<!-- instrument-registry v2 -->'
REG_CLOSE = '<!-- /instrument-registry -->'

sk = subprocess.run(['git', '-c', 'core.quotePath=false', '-C', LANE, 'cat-file', 'blob',
                     '%s:SKILL.md' % BASE], capture_output=True, check=True).stdout.decode('utf-8', 'replace')
lines = sk.split('\n')
o = next(i for i, l in enumerate(lines) if l.strip() == REG_OPEN)
cl = next(i for i, l in enumerate(lines) if l.strip() == REG_CLOSE)
print('region lines: %d..%d (1-based %d..%d)' % (o, cl, o + 1, cl + 1))

ATTEMPT1 = {'tools/round-49/c1-controls.py', 'tools/round-49/c1-counter.py',
            'tools/round-49/c1-oracle.py', 'tools/round-49/c1-run.py',
            'tools/round-49/c1-run.sh', 'tools/round-49/c2-mismatch.py',
            'tools/round-50/c1-controls.py', 'tools/round-50/c1-counter.py',
            'tools/round-50/c1-run.sh', 'tools/round-50/c2-record.py',
            'tools/round-50/fetch-vendor.py', 'tools/round-50/selftest-r49-c2.py'}

def split_raw(line):
    """split on pipes NOT preceded by backslash; report escaped pipes too"""
    esc = [m.start() for m in re.finditer(r'\\\|', line)]
    # positions of unescaped pipes
    pos = []
    i = 0
    while i < len(line):
        if line[i] == '|' and (i == 0 or line[i-1] != '\\'):
            pos.append(i)
        i += 1
    return pos, esc

report = []
row_idx = 0
for n in range(o + 1, cl):
    l = lines[n]
    if not l.strip():
        continue
    if not re.match(r'^ {0,3}\|', l):
        report.append({'line': n + 1, 'class': 'non-table-line', 'text': l[:100]})
        continue
    if re.match(r'^ {0,3}\|\s*`', l):
        row_idx += 1
        m = re.match(r'^ {0,3}\|\s*`([^`]*)`', l)
        key = m.group(1)
        pos, esc = split_raw(l)
        ncells_raw = len(pos) - 1  # cells between leading and trailing pipe
        trailing_ws = l != l.rstrip(' \t')
        inner_trail = bool(re.search(r' +\|', l))
        comment = '<!--' in l
        nul = '\x00' in l
        ends_pipe = l.rstrip(' \t').endswith('|')
        rec = {'line': n + 1, 'key': key, 'row': row_idx,
               'pipes': len(pos), 'cells_raw': ncells_raw,
               'escaped_pipes': len(esc), 'trailing_ws': trailing_ws,
               'inner_trailing_space_before_pipe': inner_trail,
               'has_comment': comment, 'has_nul': nul, 'ends_with_pipe': ends_pipe}
        if key in ATTEMPT1:
            rec['attempt1'] = True
        # counter parse for comparison
        c = [x.strip().replace('\x01', '|') for x in l.strip().replace('\\|', '\x01').split('|')]
        cs = c[1:-1] if len(c) >= 2 else c
        rec['cells_counter'] = len(cs)
        report.append(rec)
    else:
        report.append({'line': n + 1, 'class': 'table-nonrow', 'text': l[:100]})

odd = [r for r in report if r.get('cells_raw') != 7 or r.get('trailing_ws') or
       r.get('escaped_pipes') or r.get('has_comment') or r.get('has_nul') or
       not r.get('ends_with_pipe', True) or r.get('class')]
print('registry row lines:', row_idx)
print('total region non-empty lines scanned:', len(report))
print('\nANOMALIES (cells_raw!=7 | trailing_ws | escaped pipes | comment | NUL | non-table | missing trailing pipe):')
found = False
for r in odd:
    found = True
    print(json.dumps(r, ensure_ascii=False))
if not found:
    print('  none')

print('\nAttempt-1 12 rows detail:')
for r in report:
    if r.get('attempt1'):
        print(json.dumps(r, ensure_ascii=False))

json.dump(report, open('/fast/scratch/hyaku/kaidoku-r50/w3-RevB9Registry/drift-scan.json', 'w'), indent=1)
