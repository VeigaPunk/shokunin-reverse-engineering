#!/usr/bin/env python3
"""Independent re-derivation of the seven P38-C2 observables at a rev.
Deliberately does not import or shell out to the frozen counter."""
import json, re, subprocess, sys

LANE = re.compile(r'^(corpus/|tools/|\.ufo/|plans/|evidence/|scripts/|considerthese/|SCORECARD\.md|SHONEN\.md|SKILL\.md|PROVINCE\.md|LOG\.md)')
ROOT = sys.argv[1]
REV = sys.argv[2]
BASE = sys.argv[3]


def g(rev, path):
    p = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return p.stdout.decode() if p.returncode == 0 else None


def isfile(rev, path):
    p = subprocess.run(['git', '-C', ROOT, 'cat-file', '-t', '%s:%s' % (rev, path)], capture_output=True, text=True)
    return p.returncode == 0 and p.stdout.strip() in ('blob',)


def table_after(text, heading):
    """rows of the first markdown table following an exact '## heading' line"""
    lines = text.splitlines()
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    rows = []
    for l in lines[i + 1:]:
        if l.startswith('## '):
            break
        if l.lstrip().startswith('|'):
            rows.append(l.lstrip())
    return rows


def row_named(rows, name):
    for r in rows or []:
        cells = [c.strip() for c in r.strip('|').split('|')]
        if cells and cells[0] == name:
            return cells
    return None


# ---- O1: coverage ---------------------------------------------------------
ktree = subprocess.run(['git', '-C', ROOT, 'ls-tree', '-r', '--name-only', REV, 'corpus/knowledge'],
                       capture_output=True, text=True).stdout.split()
kstems = sorted(x[len('corpus/knowledge/'):-3] for x in ktree if x.endswith('.md'))
readme = g(REV, 'corpus/README.md')
sec = readme.split('## Coverage map', 1)[1]
sec = sec.split('\n## ', 1)[0]
stems_in_map = set(re.findall(r'`(2026-\d{2}-\d{2}-[a-z0-9-]+)`', sec))
missing = [s for s in kstems if s not in stems_in_map]

# ---- O2: depth -----------------------------------------------------------
skill = g(REV, 'SKILL.md')
lines = skill.splitlines()
ci = nonblank_head = None
for i, l in enumerate(lines):
    if l.startswith('## Queue-drain craft'):
        ci = i
        break
end = next(i for i in range(ci + 1, len(lines)) if lines[i].startswith('## '))
craft_lines = lines[ci + 1:end]
craft_last = ci + 1 + max(i for i, l in enumerate(craft_lines) if l.strip()) + 1  # 1-based
block_starts = [i for i, l in enumerate(craft_lines) if l.startswith('- **')]
blocks = []
for n, s in enumerate(block_starts):
    e = block_starts[n + 1] if n + 1 < len(block_starts) else len(craft_lines)
    blocks.append('\n'.join(craft_lines[s:e]))
resolved = 0
unresolved_cites = []
for b in blocks:
    ok = True
    refs = re.findall(r'corpus/knowledge/([a-z0-9.-]+\.md)(?::(\d+)(?:-(\d+))?)?', b)
    if not refs:
        ok = False
    for name, a, bb in refs:
        t = g(REV, 'corpus/knowledge/' + name)
        if t is None:
            ok = False
            unresolved_cites.append((name, 'MISSING FILE'))
            continue
        lo = int(a) if a else 1
        hi = int(bb) if bb else lo
        nl = len(t.splitlines())
        if not (1 <= lo <= hi <= nl):
            ok = False
            unresolved_cites.append((name, '%d-%d of %d' % (lo, hi, nl)))
    resolved += 1 if ok else 0

# ---- O3: calibration (command B) ----------------------------------------
res_txt = g(REV, 'evidence/round-1-2026-10-15/result.json')
ob = json.loads(res_txt)['obligations']
aligned = [o for o in ob if o.get('status') == 'aligned']
measured_rev = json.loads(res_txt).get('measured_revision')

# ---- pointers -----------------------------------------------------------
prov = g(REV, 'PROVINCE.md')
shonen = g(REV, 'SHONEN.md')
sc = g(REV, 'SCORECARD.md')

units = {}
for name in ('coverage', 'depth', 'calibration'):
    r = row_named(table_after(sc, '## Owned axes'), name)
    if r:
        units['owned:' + name] = ' | '.join(r)
for r in table_after(sc, '## Capabilities') or []:
    cells = [c.strip() for c in r.strip('|').split('|')]
    if cells and cells[0] != 'Capability' and not set(cells[0]) <= set('-: '):
        units['cap:' + cells[0]] = ' | '.join(cells)
for head, pre in (('## Core', 'prov_core:'), ('## Frontier', 'prov_frontier:')):
    for r in table_after(prov, head) or []:
        cells = [c.strip() for c in r.strip('|').split('|')]
        if cells and not set(cells[0]) <= set('-: '):
            units[pre + cells[0]] = ' | '.join(cells)
for m in re.finditer(r'(?m)^- \[[ x~]\] (.*)$', shonen):
    units['shonen:' + m.group(1).strip()] = m.group(0)


def resolve_tok(tok):
    m = re.match(r'^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$', tok)
    if not m:
        return None
    path = m.group(1)
    if not LANE.match(path):
        return None
    if not isfile(REV, path.rstrip('/')):
        return ('UNRESOLVED', path)
    if m.group(2):
        nl = len(g(REV, path).splitlines())
        lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
        if not (1 <= lo <= hi <= nl):
            return ('RANGE-BAD', path, lo, hi, nl)
    return ('OK', path)


bad = []
total = 0
for k, t in units.items():
    for tok in re.findall(r'`([^`\n]+)`', t):
        r = resolve_tok(tok)
        if r is None:
            continue
        total += 1
        if r[0] != 'OK':
            bad.append([k, tok, r])

# ---- stated values in SHONEN -------------------------------------------
box1 = next((v for k, v in units.items() if k.startswith('shonen:SKILL.md contains real decision tables')), '')
box4 = next((v for k, v in units.items() if k.startswith('shonen:No cross-domain bleed')), '')
cov_row = units.get('owned:coverage', '')
dep_row = units.get('owned:depth', '')
cal_row = units.get('owned:calibration', '')


def grab(t, rx):
    m = re.search(rx, t or '')
    return (int(m.group(1)), int(m.group(2))) if m else None


# ---- PROVINCE Adjacent range -------------------------------------------
pl = prov.splitlines()
ai = next(i for i, l in enumerate(pl) if l.startswith('## Adjacent'))
alast = ai + 1 + max(i for i, l in enumerate(pl[ai + 1:]) if l.strip() and not l.startswith('#'))
adjacent = (ai + 1, alast + 1)

out = {
    'revision': REV,
    'O1': {'knowledge_files': len(kstems), 'map_stems': len(stems_in_map), 'unmapped': missing,
           'stated': grab(cov_row, r'(\d+)/(\d+) knowledge files mapped')},
    'O2': {'rule_blocks': len(blocks), 'resolved': resolved, 'bad_cites': unresolved_cites,
           'stated': grab(dep_row, r'(\d+)/(\d+) queue-drain rule blocks')},
    'O3': {'aligned': len(aligned), 'total': len(ob), 'measured_revision': measured_rev,
           'stated': grab(cal_row, r'(\d+)/(\d+) preselected reconciliation obligations')},
    'craft_range': (ci + 1, craft_last),
    'R1_stated_craft': grab(dep_row, r'`SKILL\.md:(\d+)-(\d+)`'),
    'R2_stated_craft': grab(box1, r'`SKILL\.md:(\d+)-(\d+)`'),
    'R2_stated_blocks': grab(box1, r'(\d+)/(\d+) rule blocks'),
    'adjacent_range': adjacent,
    'R3_stated_adjacent': grab(box4, r'`PROVINCE\.md:(\d+)-(\d+)`'),
    'pointers': total,
    'pointer_failures': bad,
    'ok': (not missing and resolved == len(blocks) and len(aligned) == len(ob) and not bad
           and (ci + 1, craft_last) == grab(dep_row, r'`SKILL\.md:(\d+)-(\d+)`') == grab(box1, r'`SKILL\.md:(\d+)-(\d+)`')
           and adjacent == grab(box4, r'`PROVINCE\.md:(\d+)-(\d+)`')
           and grab(cov_row, r'(\d+)/(\d+) knowledge files mapped') == (len(kstems), len(kstems))
           and grab(dep_row, r'(\d+)/(\d+) queue-drain rule blocks') == (resolved, len(blocks))
           and grab(box1, r'(\d+)/(\d+) rule blocks') == (resolved, len(blocks))
           and grab(cal_row, r'(\d+)/(\d+) preselected reconciliation obligations') == (len(aligned), len(ob))),
}
print(json.dumps(out, indent=1, sort_keys=True))
sys.exit(0 if out['ok'] else 1)
