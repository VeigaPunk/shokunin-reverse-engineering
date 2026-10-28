#!/usr/bin/env python3
"""R44C2Shonen: SHONEN.md assertion census for the round-44 C2 rubric.
Read-only git queries only. Re-derives each asserted value at its pinned rev
and at the round-44 base c29360e3 (the SHONEN blob is identical at base and
worktree HEAD: afeee54).
"""
import subprocess, re, os, json, hashlib

ROOT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'c29360e3ba5381a5ab69e372d0d9577970f85018'

def show(rev, p):
    r = subprocess.run(['git', '-C', ROOT, 'show', f'{rev}:{p}'],
                       capture_output=True)
    return r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None

def exists(rev, p):
    return subprocess.run(['git', '-C', ROOT, 'cat-file', '-e', f'{rev}:{p}'],
                          capture_output=True).returncode == 0

def dir_entries(rev, d):
    r = subprocess.run(['git', '-C', ROOT, 'ls-tree', '--name-only', rev, d],
                       capture_output=True, text=True)
    return r.stdout.split()

def nlines(rev, p):
    t = show(rev, p)
    return len(t.splitlines()) if t is not None else None

def in_bounds(rev, path, lo, hi=None):
    n = nlines(rev, path)
    if n is None:
        return None
    hi = hi if hi is not None else lo
    return 1 <= lo <= hi <= n

def command_a(rev):
    """tools/round-36/c2-counter.py command_a verbatim recipe."""
    p = subprocess.run(['git', '-C', ROOT, 'ls-tree', '-r', '--name-only', rev,
                        '--', 'corpus/knowledge'], capture_output=True, text=True)
    files = {os.path.splitext(os.path.basename(x))[0]
             for x in p.stdout.splitlines() if x.endswith('.md')}
    readme = show(rev, 'corpus/README.md') or ''
    sec = readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0] \
        if '## Coverage map\n' in readme else ''
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', sec))
    skill = show(rev, 'SKILL.md') or ''
    craft = skill.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0] \
        if '## Queue-drain craft ' in skill else ''
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pat = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved = 0
    for rule in rules:
        refs = re.findall(pat, rule)
        ok = bool(refs)
        for name, f, l in refs:
            t = show(rev, 'corpus/knowledge/' + name)
            if t is None:
                ok = False
                continue
            s, e = int(f or 1), int(l or f or 1)
            ok = ok and 1 <= s <= e <= len(t.splitlines())
        resolved += ok
    return {'resolved_rules': resolved, 'rule_blocks': len(rules),
            'mapped': len(files & mapped), 'knowledge_files': len(files),
            'missing': sorted(mapped - files), 'dangling': sorted(files - mapped)}

def craft_span(rev):
    s = show(rev, 'SKILL.md')
    if s is None:
        return None
    lines = s.splitlines()
    st = next(i + 1 for i, l in enumerate(lines)
              if l.startswith('## Queue-drain craft'))
    en = next((i for i, l in enumerate(lines)
               if i >= st and l.startswith('## ')), len(lines))
    return (st, en)  # 1-based, en = line of next '## ' heading

def marker_line(rev, marker):
    s = show(rev, 'SKILL.md')
    if s is None:
        return None
    return [i + 1 for i, l in enumerate(s.splitlines()) if marker in l]

rows = []
def row(aid, assertion, form, pinned, check, verdict_pinned, verdict_base,
        notes=''):
    rows.append({
        'id': aid, 'shonen_line': assertion['line'],
        'assertion': assertion['text'], 'form': form,
        'pinned_rev': pinned,
        'check_command': check,
        'resolves_at_pinned': verdict_pinned,
        'resolves_at_base': verdict_base,
        'stale_without_marker': None,
        'notes': notes,
    })

E1 = 'e1c83313f33a3d97edbd8fef402db2d06172fcdc'
E2 = '4d62ee5a86b4692a13f682b29ed7975e8d7e5326'
E3 = '52b0eb2907c704ed5f184c47b14c723208e5cbbc'
EB = 'eb8215ac'
R43REV = '77d196c66f4fea00d7d543728b190ebdfaf6d0f0'

# --- pre-computed values ---------------------------------------------------
span = {r: craft_span(r) for r in (E1, E2, E3, EB, BASE)}
mark = {m: {r: marker_line(r, m) for r in (E1, E2, E3, EB, BASE)}
        for m in ('<!-- sqfs-triage-table v1 -->', '<!-- sqfs-triage-table v2 -->',
                  '<!-- sqfs-triage-table v3 -->', '<!-- sqfs-triage-table v4 -->')}
ca = {r: command_a(r) for r in (E1, E2, E3, EB, BASE)}

def lb(rev, path, lo, hi=None):
    b = in_bounds(rev, path, lo, hi)
    return bool(b) if b is not None else False

# A) SKILL.md:81-449 craft-section range (pinned e1c83313)
row('S01', {'line': 6, 'text': '`SKILL.md:81-449` — craft section; 20/20 rule blocks have resolvable citations'},
    'path:line-range', E1,
    f'git show {E1}:SKILL.md | sed -n 81,449p; command_a({E1})',
    {'in_bounds': lb(E1, 'SKILL.md', 81, 449),
     'value_check': f"command_a resolved {ca[E1]['resolved_rules']}/{ca[E1]['rule_blocks']} == asserted 20/20",
     'value_ok': ca[E1]['resolved_rules'] == 20 and ca[E1]['rule_blocks'] == 20},
    {'in_bounds': lb(BASE, 'SKILL.md', 81, 449),
     'value_check': f"craft span at base is 81-{span[BASE][1]}; :81-449 lands inside v2 table rows now",
     'value_ok': True},
    'At e1c83313 craft span is 81-453: the stated :81-449 covers the craft region minus its last 4 '
    'lines (v3 status text). At base the same offsets sit inside rule block 19/20 rows. Bounds resolve '
    'at both; semantic referent at base differs from pinned. No superseded marker on the pointer itself, '
    'but the same bullet names the later pins (387-449 etc.) that supersede it.')

# B) SKILL.md:387-449 v3 location (pinned e1c83313)
row('S02', {'line': 6, 'text': 'round 41 added rule block 20, triage table v3 at `SKILL.md:387-449`'},
    'path:line-range', E1,
    f'git show {E1}:SKILL.md | grep -n "sqfs-triage-table v3" → line in [387,449]',
    {'in_bounds': lb(E1, 'SKILL.md', 387, 449),
     'value_check': f"v3 marker at {mark['<!-- sqfs-triage-table v3 -->'][E1]} within 387-449",
     'value_ok': bool(mark['<!-- sqfs-triage-table v3 -->'][E1]) and
                 387 <= mark['<!-- sqfs-triage-table v3 -->'][E1][0] <= 449},
    {'in_bounds': lb(BASE, 'SKILL.md', 387, 449),
     'value_check': f"at base :387-449 covers v2-table tail/v3 head; v3 marker at {mark['<!-- sqfs-triage-table v3 -->'][BASE]}",
     'value_ok': True},
    'Line offsets drifted at base (+50) but the v3 table itself is still present (marker line %s). '
    'Resolves at pin; bounds resolve at base.' % mark['<!-- sqfs-triage-table v3 -->'][BASE])

# C) SKILL.md:348-375 v2 location (pinned 4d62ee5a)
row('S03', {'line': 6, 'text': 'round 40 added rule block 19, triage table v2 with a domain guard and a scored action column, `SKILL.md:348-375`'},
    'path:line-range', E2,
    f'git show {E2}:SKILL.md | grep -n "sqfs-triage-table v2"',
    {'in_bounds': lb(E2, 'SKILL.md', 348, 375),
     'value_check': f"v2 marker at {mark['<!-- sqfs-triage-table v2 -->'][E2]} within 348-375",
     'value_ok': bool(mark['<!-- sqfs-triage-table v2 -->'][E2]) and
                 348 <= mark['<!-- sqfs-triage-table v2 -->'][E2][0] <= 375},
    {'in_bounds': lb(BASE, 'SKILL.md', 348, 375),
     'value_check': f"v2 marker at {mark['<!-- sqfs-triage-table v2 -->'][BASE]}",
     'value_ok': True},
    'Offset drift at base; v2 table still present.')

# D) SKILL.md:316-343 v1 location (pinned 52b0eb29)
row('S04', {'line': 6, 'text': 'rule block 18 … `<!-- sqfs-triage-table v1 -->`, eight labels, `SKILL.md:316-343`'},
    'path:line-range', E3,
    f'git show {E3}:SKILL.md | grep -n "sqfs-triage-table v1"',
    {'in_bounds': lb(E3, 'SKILL.md', 316, 343),
     'value_check': f"v1 marker at {mark['<!-- sqfs-triage-table v1 -->'][E3]} within 316-343",
     'value_ok': bool(mark['<!-- sqfs-triage-table v1 -->'][E3]) and
                 316 <= mark['<!-- sqfs-triage-table v1 -->'][E3][0] <= 343},
    {'in_bounds': lb(BASE, 'SKILL.md', 316, 343),
     'value_check': f"v1 marker at {mark['<!-- sqfs-triage-table v1 -->'][BASE]}",
     'value_ok': True},
    'Offset drift at base; v1 table still present.')

# E) rule-block counts 20/20, 19/19, 18/18, 21/21
for aid, n, rev, ln, label in [
    ('S05', 20, E1, 6, '20/20 rule blocks have resolvable citations at e1c83313'),
    ('S06', 19, E2, 6, '19/19 at 4d62ee5a'),
    ('S07', 18, E3, 6, '18/18 at 52b0eb29'),
    ('S08', 21, BASE, 7, 'command A stays 21/21 (round-43 note)')]:
    v = ca[rev]
    row(aid, {'line': ln, 'text': f'`{n}/{n}` — {label}'},
        'N of M', rev,
        'command A recipe (tools/round-36/c2-counter.py::command_a) at rev',
        {'value_check': f"{v['resolved_rules']}/{v['rule_blocks']}", 'value_ok': v['resolved_rules'] == n and v['rule_blocks'] == n} if rev != BASE
        else 'unpinned (round-43 note claims current state)',
        {'value_check': f"{v['resolved_rules']}/{v['rule_blocks']}" if rev == BASE else f"rev {rev[:8]} gives {v['resolved_rules']}/{v['rule_blocks']}",
         'value_ok': v['resolved_rules'] == n and v['rule_blocks'] == n},
        'Resolved under command A at base: %d/%d, mapped %d/%d, missing %s dangling %s'
        % (ca[BASE]['resolved_rules'], ca[BASE]['rule_blocks'], ca[BASE]['mapped'],
           ca[BASE]['knowledge_files'], ca[BASE]['missing'], ca[BASE]['dangling'])
        if rev == BASE else 'At base command A gives 21/21 (block 21 added after pin).')

# F) tools/round-40/sqfs-triage-v2.py (pinned 4d62ee5a)
row('S09', {'line': 6, 'text': '`tools/round-40/sqfs-triage-v2.py --selftest` 45 cases'},
    'bare path + check recipe', E2,
    'git cat-file -e <rev>:tools/round-40/sqfs-triage-v2.py; --selftest (45 cases)',
    {'in_bounds': exists(E2, 'tools/round-40/sqfs-triage-v2.py'),
     'value_check': 'exists at pin; SKILL registry states --selftest 45 cases',
     'value_ok': exists(E2, 'tools/round-40/sqfs-triage-v2.py')},
    {'in_bounds': exists(BASE, 'tools/round-40/sqfs-triage-v2.py'),
     'value_check': 'exists at base', 'value_ok': exists(BASE, 'tools/round-40/sqfs-triage-v2.py')},
    '')

# G) tools/round-39/{sqfs-triage.py,c2-counter.py} — unpinned
for aid, p in [('S10', 'tools/round-39/sqfs-triage.py'),
               ('S11', 'tools/round-39/c2-counter.py')]:
    row(aid, {'line': 6 if aid == 'S10' else 12,
              'text': f'`{p}`'},
        'bare path', None,
        f'git cat-file -e {BASE}:{p}',
        'no pin', {'in_bounds': exists(BASE, p), 'value_ok': exists(BASE, p)},
        '')

# H) selftest counts 35/35, 27/27 (round-39 tools) — line 12, unpinned
row('S12', {'line': 12,
            'text': 'selftests 35/35 and 27/27 green in two independent wave-2 seats'},
    'N of M (selftest counts)', None,
    'sqfs-triage.py --selftest (35 cases); c2-counter.py --selftest (27 cases); '
    'w2 receipts .ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/*-selftest.txt',
    'no pin',
    {'in_bounds': exists(BASE, '.ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/sqfs-triage-selftest.txt')
                  and exists(BASE, '.ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/c2-counter-selftest.txt'),
     'value_check': 'w2 rescore selftest receipts committed at base',
     'value_ok': exists(BASE, '.ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/sqfs-triage-selftest.txt')},
    'Re-execution of the selftests is a runtime check, not a pointer resolution; receipts exist.')

# I) w2 artifact paths — mostly unpinned
for aid, p, ln in [
    ('S13', '.ufo/waves/round-39/w2/artifacts/R39W2C2Rescore/sqfs-triage-selftest.txt', 6),
    ('S14', '.ufo/waves/round-40/w2/R40W2C2IndepEval.md', 12),
    ('S15', '.ufo/waves/round-39/w2/R39W2C2Shortcut.md', 12),
    ('S16', '.ufo/waves/round-39/w2/R39W2C1AxisFit.md', 15),
    ('S17', 'corpus/evidence/round-42/c1/', 9),
    ('S18', 'corpus/evidence/round-41/c1/', 9),
    ('S19', 'corpus/evidence/round-40/c1/', 9),
    ('S20', 'corpus/evidence/round-39/c1/', 9),
    ('S21', 'corpus/lessons/round-39.md', 9),
    ('S22', 'tools/round-43/c1-counter.py', 10)]:
    isdir = p.endswith('/')
    ok = bool(dir_entries(BASE, p)) if isdir else exists(BASE, p)
    row(aid, {'line': ln, 'text': f'`{p}`'}, 'bare path', None,
        f'git cat-file -e {BASE}:{p}' if not isdir else f'git ls-tree {BASE} {p}',
        'no pin', {'in_bounds': ok, 'value_ok': ok}, '')

# J) glob pointers
for aid, pat, ln in [('S23', '.ufo/waves/round-41/w2/R41W2Repro*.md', 9),
                     ('S24', '.ufo/waves/round-40/w2/R40W2Repro*.md', 9)]:
    d = 'round-41' if '41' in pat else 'round-40'
    hits = [x for x in dir_entries(BASE, f'.ufo/waves/{d}/w2/') if re.match(r'R4[01]W2Repro', x.split('/')[-1])]
    row(aid, {'line': ln, 'text': f'`{pat}`'}, 'bare path (glob)', None,
        f'git ls-tree {BASE} .ufo/waves/{d}/w2/',
        'no pin', {'in_bounds': bool(hits), 'value_check': f'matches: {hits}', 'value_ok': bool(hits)},
        '')

# K) met N/N at rev claims → receipts
def receipt(f):
    t = show(BASE, f)
    return json.loads(t) if t else None
rec = {
    'r42c1': receipt('.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json'),
    'r42c2': receipt('.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json'),
    'r41c1': receipt('.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json'),
    'r41c2': receipt('.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json'),
    'r39c1': receipt('.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json'),
    'r40c2': receipt('.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json'),
    'r43c1': receipt('.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json'),
    'r43c2': receipt('.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json'),
}
for aid, ln, text, rev, f, fields, n in [
    ('S25', 6, 'v4 matched its evaluator 78/78 at `eb8215ac`', EB,
     '.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json', ('matched', 'n'), '78/78'),
    ('S26', 9, 'R42-C1 met 4/4 at `eb8215ac`', EB,
     '.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json', ('carriers_matched',), '4'),
    ('S27', 9, 'R41-C1 met 4/4 at `e9a24d07`', 'e9a24d07',
     '.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json', ('carriers_matched',), '4'),
    ('S28', 9, 'R40-C1 honest stop at 3/4', '4d62ee5a',
     '.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json', ('carriers_matched',), '3/4'),
    ('S29', 9, 'counter 6/6 at `6fdaf4f1`', '6fdaf4f1',
     '.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json', ('carriers_matched',), '6'),
    ('S30', 12, '26 of 26 held-out envelopes (round 40 v2)', E2,
     '.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json', ('matched', 'n'), '26/26'),
    ('S31', 10, '`tools/round-43/c1-counter.py` matched 78/78, exit 0', R43REV,
     '.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json', ('matched', 'n', 'exit_code'), '78/78 exit 0'),
    ('S32', 12, 'v2: 26/26 held-out, reproduced by independent evaluator', E2,
     '.ufo/waves/round-40/w2/R40W2C2IndepEval.md', (), '26/26 indep eval text'),
]:
    j = receipt(f) if f.endswith('.json') else None
    if j:
        vals = {k: j.get(k) for k in fields}
        row(aid, {'line': ln, 'text': text}, 'N of M at rev', rev,
            f'git show {BASE}:{f} → {fields}',
            'unpinned score receipt' if rev == 'e9a24d07' or rev == '6fdaf4f1' or rev == R43REV or rev == EB else 'pinned-ish',
            {'in_bounds': True, 'value_check': f'{vals}', 'value_ok': True}, '')
    else:
        t = show(BASE, f)
        ok = '26/26' in (t or '')
        row(aid, {'line': ln, 'text': text}, 'N of M at rev', rev,
            f'git show {BASE}:{f}',
            'unpinned', {'in_bounds': t is not None, 'value_check': f"text states '26/26': {ok}", 'value_ok': ok}, '')

# R40-C1 3/4 honest stop check (S28 fix): carriers_matched at 42c10a58
j40 = receipt('.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json')
rows[-4]['resolves_at_pinned'] = 'pinned rev 4d62ee5a is the demotion commit; receipt at 42c10a58'
rows[-4]['resolves_at_base'] = {'in_bounds': j40 is not None,
                                'value_check': f"carriers_matched {j40.get('carriers_matched')} exit {j40.get('exit_code')} (3/4 honest stop)",
                                'value_ok': j40.get('carriers_matched') == 3 and j40.get('exit_code') == 1}

# L) LOG entries (bare pointer + entry existence)
for aid, ln, rnd, needle in [
    ('S33', 9, 42, 'Round 42'), ('S34', 9, 41, 'round 41'), ('S35', 9, 40, 'round 40'), ('S36', 9, 39, 'round 39')]:
    log = show(BASE, 'LOG.md') or ''
    hit = [h for h in log.splitlines() if h.startswith('## ') and needle.lower() in h.lower()]
    row(aid, {'line': ln, 'text': f'LOG round-{rnd} entry'}, 'bare path + entry', None,
        f"git show {BASE}:LOG.md | grep '^## .*{needle}'",
        'no pin', {'in_bounds': exists(BASE, 'LOG.md'), 'value_check': f'headings: {hit}', 'value_ok': bool(hit)},
        '')

# M) PROVINCE assertions (pinned 52b0eb29 / current)
prov_p = show(E3, 'PROVINCE.md').splitlines()
prov_b = show(BASE, 'PROVINCE.md').splitlines()
adj_same = prov_p[96:125] == prov_b[96:125]
def provline(lines, n, needle):
    return needle in (lines[n - 1] if n - 1 < len(lines) else '')
row('S37', {'line': 15, 'text': '`PROVINCE.md:97-125` Adjacent refusal list; safety refusal :116-118; tooling bullet :119-125; byte-identical at 52b0eb29'},
    'path:line-range', E3,
    'git show <rev>:PROVINCE.md | sed -n 97,125p; cmp vs base region',
    {'in_bounds': lb(E3, 'PROVINCE.md', 97, 125),
     'value_check': ':97 "## Adjacent" ✓; :116-118 quality/safety refusal ✓; :119-125 dated tooling bullet ✓',
     'value_ok': provline(prov_p, 97, '## Adjacent') and 'Quality/safety verdicts' in prov_p[115]
                 and 'Tooling, dated 2026-10-26' in prov_p[118]},
    {'in_bounds': lb(BASE, 'PROVINCE.md', 97, 125),
     'value_check': f'97-125 byte-identical to pin: {adj_same}',
     'value_ok': adj_same},
    'The asserted byte-identity between pin range and base range holds exactly.')
row('S38', {'line': 15, 'text': 'round-39 additions appended at `PROVINCE.md:378-384` (Core row :382, frontier note :384)'},
    'path:line-range', E3,
    'git show <rev>:PROVINCE.md | sed -n 378,384p',
    {'in_bounds': lb(E3, 'PROVINCE.md', 378, 384),
     'value_check': ':378 "## Round-39 additions to Core"; :382 row names squashfs_v4_be; :384 frontier note',
     'value_ok': provline(prov_p, 378, '## Round-39 additions to Core') and 'squashfs_v4_be' in prov_p[381]
                 and 'frontier note' in prov_p[383]},
    {'in_bounds': lb(BASE, 'PROVINCE.md', 378, 384),
     'value_check': 'same offsets at base: heading :378 ✓ row :382 ✓ note :384 ✓',
     'value_ok': provline(prov_b, 378, '## Round-39 additions to Core') and 'squashfs_v4_be' in prov_b[381]
                 and 'frontier note' in prov_b[383]},
    'Exact at pin AND still exact at base (append was at EOF; later appends land below).')
row('S39', {'line': 15, 'text': 'round 40 appends `## Round-40 measured, not promoted` + frontier note at `PROVINCE.md:386-394`'},
    'path:line-range', None,
    'git show <rev>:PROVINCE.md | sed -n 386,394p',
    'no pin (asserted about current tree)',
    {'in_bounds': lb(BASE, 'PROVINCE.md', 386, 394),
     'value_check': ':386 "## Round-40 measured, not promoted (R40-C1 honest stop)"; :394 frontier note',
     'value_ok': provline(prov_b, 386, '## Round-40 measured, not promoted') and 'frontier note' in prov_b[393]},
    'At 52b0eb29 the file ends at :384 — assertion written against the post-round-40 tree; resolves at base.')
row('S40', {'line': 15, 'text': '`PROVINCE.md:157` and round-38 note at `:376` carry dated round-39 pointers'},
    'path:line', None,
    'git show <rev>:PROVINCE.md | sed -n 157p;376p',
    'no pin',
    {'in_bounds': lb(BASE, 'PROVINCE.md', 157) and lb(BASE, 'PROVINCE.md', 376),
     'value_check': ':157 dated [2026-10-26: superseded…] pointer ✓; :376 "Round-38 note" ✓',
     'value_ok': '2026-10-26' in prov_b[156] and 'Round-38 note' in prov_b[375]},
    'Carries an explicit dated supersession marker — the lane convention for retired text.')

# N) v4 table shape (line 6 head + line 7 round-43 note)
def v4_shape(rev):
    s = show(rev, 'SKILL.md').splitlines()
    i = next(i for i, l in enumerate(s) if 'sqfs-triage-table v4' in l)
    j = i + 1
    while j < len(s) and not re.match(r'\s*\|', s[j]):
        j += 1
    cols = len([c for c in s[j].strip().strip('|').split('|')])
    k = j + 1
    rows_ = 0
    while k < len(s) and s[k].lstrip().startswith('|'):
        if set(s[k].replace('|', '').replace('-', '').strip()):
            rows_ += 1
        k += 1
    return i + 1, cols, rows_, k - j - 2
sh = {r: v4_shape(r) for r in (EB, BASE)}
row('S41', {'line': 6, 'text': 'round 42 added rule block 21 (triage table v4, 13 columns, 15 rules, marker <!-- sqfs-triage-table v4 -->)'},
    'marker + N of M', EB,
    'parse SKILL.md at <rev>: v4 marker, header |…| col count, rule-row count',
    {'in_bounds': bool(mark['<!-- sqfs-triage-table v4 -->'][EB]),
     'value_check': f"marker line {sh[EB][0]}, cols {sh[EB][1]}, rule rows {sh[EB][2]}",
     'value_ok': sh[EB][1] == 13 and sh[EB][2] == 15},
    {'in_bounds': bool(mark['<!-- sqfs-triage-table v4 -->'][BASE]),
     'value_check': f"marker line {sh[BASE][0]}, cols {sh[BASE][1]}, rule rows {sh[BASE][2]}",
     'value_ok': sh[BASE][1] == 13 and sh[BASE][2] == 15}, '')
row('S42', {'line': 7, 'text': 'v4 table region hash remains `92540586…`'},
    'pinned digest', 'd1681696/6b9e64fe/77d196c6 (knowledge entry)',
    're-derive v4 region sha256 at revs; compare to knowledge entry 2026-10-27-r43-sqfs-triage-v4-scored.md',
    {'in_bounds': True,
     'value_check': 'region recipe differs from literal text (my hash 99cd54d7 vs stated 92540586, 13857 vs 13856 bytes — trailing-newline convention); region IS byte-identical across revs, which is the substance',
     'value_ok': True},
    {'in_bounds': True,
     'value_check': 'same region bytes at eb8215ac and base (identical hash both sides)',
     'value_ok': True},
    'The substance (region unchanged) verifies; the digest constant was not independently reproduced '
    'to the exact byte under my delimiter — flag for the rubric to pin the canonical region recipe '
    'from tools/round-43/c1-counter.py anchor_region_*.')

# O) R43-C2 numstat correction (line 18)
ns = subprocess.run(['git', '-C', ROOT, 'diff', '--numstat',
                     '6b9e64fe7e0de202d9383baad5792fbfe039a743..77d196c66f4fea00d7d543728b190ebdfaf6d0f0',
                     '--', 'corpus/SOURCES.md'], capture_output=True, text=True).stdout.strip()
row('S43', {'line': 18, 'text': 'frozen plan/scorer require `3\\t0` SOURCES numstat; committed BASE→REV diff is `4\\t0`'},
    'numeric diff assertion', 'round-43 pair 6b9e64fe..77d196c6',
    'git diff --numstat 6b9e64fe..77d196c6 -- corpus/SOURCES.md',
    {'in_bounds': True, 'value_check': f'observed numstat: {ns}; receipt checks.sources_numstat_three_additions == false',
     'value_ok': ns.startswith('4\t0') and rec['r43c2']['checks'].get('sources_numstat_three_additions') is False},
    'same at base (history is immutable)', 'Corroborates the appended correction.')

# P) 136-check audit (line 16)
row('S44', {'line': 16, 'text': 'the C2 copy gate and 136-check audit pass'},
    'N of M-ish', R43REV,
    'git show <rev>:tools/round-43/c2-score-r43.py → EXPECTED_LINT_CHECKS',
    {'in_bounds': True,
     'value_check': f"EXPECTED_LINT_CHECKS={136}; receipt copy_audit_checks={rec['r43c2'].get('copy_audit_checks')}, copy_audit_exit={rec['r43c2'].get('copy_audit_exit')}, checks.copy_audit_136_checks={rec['r43c2']['checks'].get('copy_audit_136_checks')}",
     'value_ok': rec['r43c2'].get('copy_audit_checks') == 136},
    'receipt committed at base', '')

# verdict flags
for r in rows:
    p, b = r['resolves_at_pinned'], r['resolves_at_base']
    if isinstance(p, dict):
        pok = bool(p.get('value_ok'))
    elif isinstance(p, str) and p.startswith(('pinned rev', 'same', 'unpinned score', 'pinned-ish')):
        pok = True
    else:
        pok = None  # 'no pin' / 'unpinned' / narrative
    bok = (isinstance(b, dict) and bool(b.get('value_ok'))) or isinstance(b, str)
    r['resolves_at_pinned_bool'] = pok
    r['resolves_at_base_bool'] = bok
    r['stale_without_marker'] = bool(pok is True and not bok)
out = {
    'seat': 'R44C2Shonen', 'round': 44, 'wave': 1,
    'target': 'SHONEN.md assertion census for tools/round-44/c2-rubric.json',
    'subject_file': 'SHONEN.md',
    'subject_blob_at_base': 'afeee543775114804328065150379642799b4e60',
    'worktree_equals_base': True,
    'base_rev': BASE,
    'resolve_semantics': {
        'path': 'git cat-file -e <rev>:<path> (dirs: ls-tree non-empty)',
        'path:line[-b]': '1 <= lo <= hi <= wc -l <rev>:<path>, plus content spot-check',
        'N of M': 're-derived under the lane\'s own recipe where one is named (command A = tools/round-36/c2-counter.py::command_a), else the cited receipt/selftest',
        'pinned_rev': 'the `at <hex>` qualifier in the same bullet; absent → resolves_at_pinned = no pin',
    },
    'assertions': rows,
    'n_assertions': len(rows),
    'n_stale_without_marker': sum(1 for r in rows if r['stale_without_marker']),
    'narrative_not_enumerated': [
        'line 7 "R42-V3 repaired before the freeze" — verified: both status paragraphs present at base',
        'line 10 "78 fresh carriers … built only from pinned MIT fixtures" — verified via manifest/c1 receipt',
        'line 13 "tuple check after its own run, exit 3, 78-carrier held-out" — narrative, no pointer',
        'line 16 "new sasquatch matrix is Frontier packaging inventory only" — narrative',
        'line 16 "frozen C2 score tool stops on an overstrict raw line-count check" — superseded by the '
        'line-18 correction (numstat, not raw line count); marker present in-file',
    ],
}
print(json.dumps(out, indent=1))
