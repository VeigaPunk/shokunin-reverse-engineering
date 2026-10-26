#!/usr/bin/env python3
"""Tree-aware pointer audit: (a) C2-scope units, (b) the SCORECARD '## Round 38' section.
Usage: audit.py <lane> <rev>"""
import re, subprocess, sys
LANE = re.compile(r'^(corpus/|tools/|\.ufo/|plans/|evidence/|scripts/|considerthese/|SCORECARD\.md|SHONEN\.md|SKILL\.md|PROVINCE\.md|LOG\.md)')
ROOT, REV = sys.argv[1], sys.argv[2]


def g(path):
    p = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (REV, path)], capture_output=True)
    return p.stdout.decode() if p.returncode == 0 else None


def typ(path):
    p = subprocess.run(['git', '-C', ROOT, 'cat-file', '-t', '%s:%s' % (REV, path)], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def table_after(text, heading):
    lines = text.splitlines()
    if heading not in lines:
        return []
    rows = []
    for l in lines[lines.index(heading) + 1:]:
        if l.startswith('## '):
            break
        if l.lstrip().startswith('|'):
            rows.append(l.lstrip())
    return rows


sc, sh, pv = g('SCORECARD.md'), g('SHONEN.md'), g('PROVINCE.md')
units = {}
for r in table_after(sc, '## Owned axes'):
    cells = [c.strip() for c in r.strip('|').split('|')]
    if cells and cells[0] != 'Axis' and not set(cells[0]) <= set('-: '):
        units['owned:' + cells[0]] = r
for r in table_after(sc, '## Capabilities'):
    cells = [c.strip() for c in r.strip('|').split('|')]
    if cells and cells[0] != 'Capability' and not set(cells[0]) <= set('-: '):
        units['cap:' + cells[0]] = r
for head, pre in (('## Core', 'prov_core:'), ('## Frontier', 'prov_frontier:')):
    for r in table_after(pv, head):
        cells = [c.strip() for c in r.strip('|').split('|')]
        if cells and not set(cells[0]) <= set('-: '):
            units[pre + cells[0]] = r
cur = None
for l in sh.splitlines():
    m = re.match(r'^- \[[ x~]\] (.*)$', l)
    if m:
        cur = 'shonen:' + m.group(1).strip()
        units[cur] = l
    elif cur and l.startswith('  '):
        units[cur] += '\n' + l
    else:
        cur = None

# '## Round 38' section of SCORECARD
sec_start = sc.index('\n## Round 38')
sec = sc[sec_start:]

PAT = re.compile(r'^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$')


def audit(name, text):
    ok = tree = bad = 0
    rows = []
    for tok in re.findall(r'`([^`\n]+)`', text):
        m = PAT.match(tok)
        if not m or tok.startswith(('/', '~')) or not LANE.match(m.group(1)):
            continue
        path = m.group(1)
        base = path.rstrip('/')
        t = typ(base)
        if t is None:
            bad += 1
            rows.append(('UNRESOLVED', tok))
            continue
        if m.group(2):
            if t != 'blob':
                bad += 1
                rows.append(('RANGE-ON-NON-BLOB', tok))
                continue
            nl = len(g(base).splitlines())
            lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
            if not (1 <= lo <= hi <= nl):
                bad += 1
                rows.append(('RANGE-BAD', tok, lo, hi, nl))
                continue
        if t == 'tree':
            tree += 1
        ok += 1
    return {'surface': name, 'pointers': ok + bad, 'resolved': ok, 'resolved_as_tree': tree, 'unresolved': bad, 'details': rows}


print(audit_scoped := [audit('C2-scope units (52-pointer set)', '\n'.join(units.values())),
                       audit("SCORECARD '## Round 38' section (not in C2 scope)", sec)])
