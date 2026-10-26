#!/usr/bin/env python3
"""R36-C2 counter (calibration: self-assessment vs observed repo state).

Predicate P36-C2 (frozen; same sentence in plans/round-36-claims.md):
  At the measured revision, the lane's current self-assessment surfaces —
  the SCORECARD `## Owned axes` rows, the SCORECARD `## Capabilities` table rows
  and the SHONEN.md boxes — carry zero mismatches with observed repo state:
  every backticked repo pointer in them resolves at that revision (path exists,
  line range inside the file), the four stated counts equal the counts the
  lane's command A / command B observe at that revision, and the three stated
  section ranges equal the observed heading-to-last-non-blank-line ranges;
  with no unit removed, no fewer pointers than at the base, and every pointer
  unresolved at the base repaired by a resolving pointer to the same document.

Target: mismatches == 0 and guards_ok (base 3 mismatches at cab59f22).

Usage:
  c2-counter.py --root LANE --rev REV --base BASE [--json-out PATH]
  c2-counter.py --selftest
Exit: 0 target met, 1 not met, 2 unevaluable. Reads only git objects.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

TOKEN = re.compile(r'`([^`\s]+)`')
PTR = re.compile(r'^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$')
BOX1 = 'SKILL.md contains real decision tables'
BOX4 = 'No cross-domain bleed'


class Unevaluable(Exception):
    pass


def show(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout.decode() if p.returncode == 0 else None


def exists(root, rev, path):
    return subprocess.run(['git', '-C', root, 'cat-file', '-e', f'{rev}:{path}'], capture_output=True).returncode == 0


def section(text, heading):
    lines = text.splitlines()
    if heading not in lines:
        return None
    out = []
    for line in lines[lines.index(heading) + 1:]:
        if line.startswith('## '):
            break
        out.append(line)
    return out


def first_cell(row):
    return row.strip().strip('|').split('|')[0].strip()


def units(root, rev):
    """{unit_key: text} for the three surfaces."""
    sc = show(root, rev, 'SCORECARD.md')
    sh = show(root, rev, 'SHONEN.md')
    if sc is None or sh is None:
        raise Unevaluable('SCORECARD.md or SHONEN.md absent')
    u = {}
    owned = section(sc, '## Owned axes') or []
    for l in owned:
        if l.startswith('|') and not l.startswith('|---') and first_cell(l) != 'Axis':
            u['owned:' + first_cell(l)] = l
    caps = section(sc, '## Capabilities') or []
    started = False
    for l in caps:
        if l.startswith('|'):
            started = True
            if not l.startswith('|---') and first_cell(l) != 'Capability':
                u['cap:' + first_cell(l)] = l
        elif started:
            break
    cur = None
    for l in sh.splitlines():
        m = re.match(r'^- \[[ x~]\] (.*)$', l)
        if m:
            cur = 'shonen:' + m.group(1).strip()
            u[cur] = l
        elif cur and l.startswith('  '):
            u[cur] += '\n' + l
        else:
            cur = None
    return u


def pointers(text):
    out = []
    for tok in TOKEN.findall(text):
        m = PTR.match(tok)
        if not m or tok.startswith(('/', '~')):
            continue
        path = m.group(1)
        if '/' not in path and not path.endswith('.md'):
            continue
        out.append((tok, path, m.group(2), m.group(3)))
    return out


def resolves(root, rev, path, a, b, cache):
    p = path.rstrip('/')
    if not p or not exists(root, rev, p):
        return False
    if a is None:
        return True
    if p not in cache:
        t = show(root, rev, p)
        cache[p] = len(t.splitlines()) if t is not None else 0
    lo, hi = int(a), int(b or a)
    return 1 <= lo <= hi <= cache[p]


def command_a(root, rev):
    p = subprocess.run(['git', '-C', root, 'ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge'], capture_output=True, text=True)
    files = {os.path.splitext(os.path.basename(x))[0] for x in p.stdout.splitlines() if x.endswith('.md')}
    readme = show(root, rev, 'corpus/README.md') or ''
    sec = readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0] if '## Coverage map\n' in readme else ''
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', sec))
    skill = show(root, rev, 'SKILL.md') or ''
    craft = skill.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0] if '## Queue-drain craft ' in skill else ''
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pat = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved = 0
    for rule in rules:
        refs = re.findall(pat, rule)
        ok = bool(refs)
        for name, f, l in refs:
            t = show(root, rev, 'corpus/knowledge/' + name)
            if t is None:
                ok = False
                continue
            s, e = int(f or 1), int(l or f or 1)
            ok = ok and 1 <= s <= e <= len(t.splitlines())
        resolved += ok
    return {'mapped': len(files & mapped), 'knowledge_files': len(files), 'resolved_rules': resolved, 'rule_blocks': len(rules)}


def command_b(root, rev):
    t = show(root, rev, 'evidence/round-1-2026-10-15/result.json')
    if t is None:
        return None
    ob = json.loads(t).get('obligations') or []
    return (len([o for o in ob if o.get('status') == 'aligned']), len(ob))


def heading_range(text, heading_prefix, stop):
    lines = (text or '').splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith(heading_prefix)), None)
    if start is None:
        return None
    last = start
    for i in range(start + 1, len(lines)):
        if stop(lines[i]):
            break
        if lines[i].strip():
            last = i
    return (start + 1, last + 1)


def measure(root, rev, base):
    for r in (rev, base):
        if subprocess.run(['git', '-C', root, 'cat-file', '-e', f'{r}^{{commit}}'], capture_output=True).returncode:
            raise Unevaluable(f'unknown revision {r}')
    U, B = units(root, rev), units(root, base)
    cache = {}
    res = {'revision': rev, 'base': base, 'predicate': 'P36-C2'}
    unresolved, total = [], 0
    for k, t in U.items():
        for tok, path, a, b in pointers(t):
            total += 1
            if not resolves(root, rev, path, a, b, cache):
                unresolved.append([k, tok])
    res['pointers'] = total
    res['unresolved'] = unresolved
    A = command_a(root, rev)
    Bc = command_b(root, rev)
    res['observed'] = {'command_a': A, 'command_b': Bc}
    skill = show(root, rev, 'SKILL.md')
    prov = show(root, rev, 'PROVINCE.md')
    craft = heading_range(skill, '## Queue-drain craft', lambda l: l.startswith('## '))
    adj = heading_range(prov, '## Adjacent', lambda l: l.startswith('#'))
    res['observed']['craft_range'] = craft
    res['observed']['adjacent_range'] = adj
    sh1 = next((v for k, v in U.items() if k.startswith('shonen:' + BOX1)), '')
    sh4 = next((v for k, v in U.items() if k.startswith('shonen:' + BOX4)), '')

    def stated(text, rx):
        m = re.search(rx, text or '')
        return (int(m.group(1)), int(m.group(2))) if m else None

    checks = {
        'O1 coverage mapped/files': (stated(U.get('owned:coverage'), r'(\d+)/(\d+) knowledge files mapped'), (A['mapped'], A['knowledge_files'])),
        'O2 depth resolved/rules': (stated(U.get('owned:depth'), r'(\d+)/(\d+) queue-drain rule blocks'), (A['resolved_rules'], A['rule_blocks'])),
        'O3 calibration aligned/total': (stated(U.get('owned:calibration'), r'(\d+)/(\d+) preselected reconciliation obligations'), Bc),
        'O4 SHONEN box1 rule blocks': (stated(sh1, r'(\d+)/(\d+) rule blocks'), (A['resolved_rules'], A['rule_blocks'])),
        'R1 depth row craft range': (stated(U.get('owned:depth'), r'`SKILL\.md:(\d+)-(\d+)`'), craft),
        'R2 SHONEN box1 craft range': (stated(sh1, r'`SKILL\.md:(\d+)-(\d+)`'), craft),
        'R3 SHONEN box4 Adjacent range': (stated(sh4, r'`PROVINCE\.md:(\d+)-(\d+)`'), adj),
    }
    failed = []
    for name, (s, o) in checks.items():
        if s is None or o is None or tuple(s) != tuple(o):
            failed.append({'check': name, 'stated': s, 'observed': o})
    res['assertions'] = len(checks)
    res['assertion_mismatches'] = failed
    # guards against deletion / substitution shortcuts
    missing_units = sorted(set(B) - set(U))
    base_total = 0
    bad_base = []
    for k, t in B.items():
        for tok, path, a, b in pointers(t):
            base_total += 1
            if not resolves(root, base, path, a, b, {}):
                bad_base.append((k, path.rstrip('/')))
    unrepaired = []
    for k, path in bad_base:
        ok = any(resolves(root, rev, p2, a2, b2, cache) and (p2.rstrip('/') == path or p2.rstrip('/').endswith('/' + path))
                 for _, p2, a2, b2 in pointers(U.get(k, '')))
        if not ok:
            unrepaired.append([k, path])
    res['guards'] = {'missing_units': missing_units, 'base_pointers': base_total, 'pointers_not_fewer': total >= base_total,
                     'base_unresolved': [list(x) for x in bad_base], 'unrepaired': unrepaired}
    res['guards_ok'] = not missing_units and total >= base_total and not unrepaired
    res['mismatches'] = len(unresolved) + len(failed)
    res['met_target'] = res['mismatches'] == 0 and res['guards_ok']
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--base')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.rev and a.base):
        print('usage: --root --rev --base required', file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.base)
    except Unevaluable as e:
        res = {'unevaluable': str(e)}
        print(json.dumps(res))
        return 2
    res['argv'] = sys.argv
    print(json.dumps({k: res[k] for k in ('revision', 'mismatches', 'unresolved', 'assertion_mismatches', 'guards_ok', 'met_target')}, sort_keys=True))
    if a.json_out:
        json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
    return 0 if res['met_target'] else 1


# ---------------------------------------------------------------- selftest
def selftest():
    def files(cov='3/3', depth='1/1', cal='2/2', box1n='1/1', craft='SKILL.md:3-5', adj='PROVINCE.md:3-5',
              cap_ptr='`docs/x.md`', drop_box=False, extra_ptr='', ptr2='`d/y.md`'):
        sc = ('# S\n\n## Owned axes\n\n| Axis | s | o | e | r |\n|---|---|---|---|---|\n'
              f'| coverage | 10 | {cov} knowledge files mapped | `corpus/README.md` | r |\n'
              f'| depth | 10 | {depth} queue-drain rule blocks | `{craft}` | r |\n'
              f'| calibration | 10 | {cal} preselected reconciliation obligations | x | r |\n\n'
              '## Capabilities\n\n| Capability | w | e | r |\n|---|---|---|---|\n'
              f'| cap one | w | {cap_ptr} {extra_ptr} | r |\n\n## Saturation\n')
        sh = (f'# P\n\n- [~] {BOX1}\n  asserted `{craft}` {box1n} rule blocks\n'
              f'- [~] At least one end-to-end domain task\n  asserted {ptr2}\n')
        if not drop_box:
            sh += f'- [~] {BOX4} (PROVINCE.md still accurate)\n  asserted `{adj}`\n'
        skill = '# K\n\n## Queue-drain craft (x)\n\n- **r1** `corpus/knowledge/2026-10-01-a.md:1-1`\n\n## Next\n'
        prov = '# P\n\n## Adjacent\n\n- refuse\n\n### Sub\n'
        readme = '# R\n\n## Coverage map\n\n| `2026-10-01-a` | `2026-10-01-b` | `2026-10-01-c` |\n\n## End\n'
        res = json.dumps({'obligations': [{'status': 'aligned'}, {'status': 'aligned'}]})
        return {'SCORECARD.md': sc, 'SHONEN.md': sh, 'SKILL.md': skill, 'PROVINCE.md': prov, 'corpus/README.md': readme,
                'evidence/round-1-2026-10-15/result.json': res, 'corpus/knowledge/2026-10-01-a.md': 'a\n',
                'corpus/knowledge/2026-10-01-b.md': 'b\n', 'corpus/knowledge/2026-10-01-c.md': 'c\n',
                'docs/x.md': 'x\n', 'd/y.md': 'y\n', 'd/z/y.md': 'y\n'}

    base = files(cov='2/2', cap_ptr='`x.md`')          # two base mismatches: stale count + unresolved pointer
    cases = [
        ('green: repaired by document', files(), 0),
        ('do-nothing', base, 1),
        ('junk count', files(cov='999/999'), 1),
        ('count deleted', files(cov='all'), 1),
        ('unresolved pointer deleted (fewer pointers)', files(cap_ptr=''), 1),
        ('substituted by other document', files(cap_ptr='`d/y.md`'), 1),
        ('box removed', files(drop_box=True), 1),
        ('craft range off by one', files(craft='SKILL.md:3-6'), 1),
        ('adjacent range wrong', files(adj='PROVINCE.md:3-7'), 1),
        ('range beyond file', files(extra_ptr='`docs/x.md:1-9`'), 1),
        ('new unresolved pointer', files(ptr2='`d/missing.md`'), 1),
        ('calibration count wrong', files(cal='1/2'), 1),
        ('SHONEN rule count wrong', files(box1n='2/1'), 1),
    ]
    sroot = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'kaidoku-r36')
    os.makedirs(sroot, exist_ok=True)
    fails = []
    green = red = 0
    env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@invalid',
               GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@invalid')
    for name, fs, want in cases:
        d = tempfile.mkdtemp(prefix='c2-selftest.', dir=sroot)
        try:
            subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
            top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
            if os.path.realpath(top) != os.path.realpath(d):
                raise SystemExit('fixture toplevel mismatch')
            revs = []
            for tree in (base, fs):
                for p in subprocess.run(['git', '-C', d, 'ls-files'], capture_output=True, text=True).stdout.split():
                    os.remove(os.path.join(d, p))
                for p, c in tree.items():
                    os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
                    open(os.path.join(d, p), 'w').write(c)
                subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
                subprocess.run(['git', '-C', d, 'commit', '-qm', 'x', '--allow-empty'], check=True, env=env)
                revs.append(subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip())
            try:
                r = measure(d, revs[1], revs[0])
                got = 0 if r['met_target'] else 1
            except Unevaluable as e:
                got = 2
                fails.append(f'{name}: {e}')
            if got == want:
                green += want == 0
                red += want == 1
            else:
                fails.append(f'{name}: want {want} got {got}')
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print(json.dumps({'selftest': 'c2-counter', 'cases': len(cases), 'green_ok': green, 'red_ok': red, 'failures': fails}))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
