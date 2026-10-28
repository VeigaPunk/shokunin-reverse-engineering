"""Read-only probe driver for seat R46W1RegA (kaidoku round 46, wave 1).

Every mode re-reads the three instruments at the freeze commit through
`git -C <lane> show <freeze>:<path>` and scores rows.md with the FROZEN
`tools/round-46/registry.py` (copied to scratch out of the same commit).
Nothing under the lane tree is written.
"""
import importlib.util
import json
import os
import subprocess
import sys

L = os.environ['LANE']
F = os.environ['FREEZE']
S = os.environ['SCRATCH']
ROWS = os.path.join(L, '.ufo', 'waves', 'round-46', 'w1', 'R46W1RegA', 'rows.md')
MINE = ['tools/round-41/c1-counter.py',
        'tools/round-42/c1-counter.py',
        'tools/round-43/heldout-gen-v4r43.py']
HEADER = ('| tool | gate or probe - purpose | verdict map (exit codes) | '
          'self-test command | pinned-value path | write scope | owner |')


def registry():
    spec = importlib.util.spec_from_file_location('reg', os.path.join(S, 'r46', 'registry.py'))
    mod = importlib.util.module_from_spec(spec)
    sys.modules['reg'] = mod
    spec.loader.exec_module(mod)
    return mod


def git_show(path):
    r = subprocess.run(['git', '-C', L, 'show', F + ':' + path],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def build(reg, body, header=HEADER, sep='|---|---|---|---|---|---|---|'):
    return ('## Probe\n\n' + reg.HEAD + '\n' + header + '\n' + sep + '\n'
            + body + reg.TAIL + '\n')


def files_mine(path):
    if path == 'tools/round-46/census.json':
        return json.dumps({'paths': MINE})
    return git_show(path)


def main(mode):
    rows = open(ROWS).read()
    bt = chr(96)

    if mode == 'rows':
        lines = [l.rstrip('\n') for l in rows.splitlines() if l.strip()]
        print('rows:', len(lines))
        bad = 0
        for i, line in enumerate(lines):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            want = bt + MINE[i] + bt if i < len(MINE) else None
            c3 = cells[2] if len(cells) > 2 else ''
            ok = (len(cells) == 7 and cells[0] == want and '' not in
                  [t for t in ('0=', '1=', '2=') if t not in c3])
            print('row%d cells=%d cell1=%s binds0/1/2=%s %s'
                  % (i + 1, len(cells), cells[0], c3.count('=') >= 3,
                     'PASS' if ok else 'FAIL'))
            bad += 0 if ok else 1
        print('ALL PASS' if bad == 0 and len(lines) == 3 else 'FAILURES')
        return 0 if bad == 0 and len(lines) == 3 else 1

    reg = registry()
    if mode == 'A':
        code, r = reg.score(build(reg, rows), git_show, 'r46', 'v2', F)
        print(json.dumps({'mode': 'A real frozen census, my 3 rows only',
                          'exit': code, 'scope_size': r['scope_size'],
                          'header_ok': r['header'] == reg.HOUSE,
                          'registered': r['registered'], 'thin': r['thin'],
                          'absent_at_rev': r['absent_at_rev'],
                          'unregistered_count': len(r['unregistered']),
                          'failing': r['failing']}, indent=1))
        return code
    if mode == 'B':
        code, r = reg.score(build(reg, rows), files_mine, 'r46', 'v2', F)
        print(json.dumps({'mode': 'B scope = exactly my 3 paths', 'exit': code,
                          'registered': r['registered'],
                          'unregistered': r['unregistered'], 'thin': r['thin'],
                          'absent_at_rev': r['absent_at_rev'],
                          'failing': r['failing'], 'met_target': r['met_target']},
                         indent=1))
        return code
    if mode == 'M0':
        code, r = reg.score(build(reg, rows), files_mine, 'r46', 'v2', F)
        print('M0 unmutated control: exit=%s met_target=%s' % (code, r['met_target']))
        return code
    if mode == 'M1':
        m = rows.replace('0=met,', '0 rows,').replace('1=not met,', '1 column,') \
                .replace('2=could-not-evaluate,', '2 bytes,')
        code, r = reg.score(build(reg, m), files_mine, 'r46', 'v2', F)
        print('M1 prose-digit verdict map: exit=%s thin=%s failing=%s'
              % (code, r['thin'], r['failing']))
        return code
    if mode == 'M2':
        m = bt * 3 + '\n' + rows + bt * 3 + '\n'
        code, r = reg.score(build(reg, m), files_mine, 'r46', 'v2', F)
        print('M2 fenced rows: exit=%s registry_rows=%d unregistered=%s'
              % (code, r['registry_rows'], r['unregistered']))
        return code
    if mode == 'M3':
        m = rows.replace('| ' + bt + 'tools/round-41/c1-counter.py' + bt + ' |',
                         '| ' + bt + 'round-41/c1-counter.py' + bt + ' |')
        code, r = reg.score(build(reg, m), files_mine, 'r46', 'v2', F)
        print('M3 suffix cell 0: exit=%s unregistered=%s' % (code, r['unregistered']))
        return code
    if mode == 'M4':
        m = ('## Probe\n\n' + reg.HEAD + '\n| tool | purpose | exits |\n|---|---|---|\n'
             + rows + reg.TAIL + '\n')
        code, r = reg.score(m, files_mine, 'r46', 'v2', F)
        print('M4 three-cell header: exit=%s failing=%s' % (code, r['failing']))
        return code
    if mode == 'pins':
        spec = importlib.util.spec_from_file_location(
            'r43', os.path.join(L, 'tools', 'round-43', 'heldout-gen-v4r43.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        p = mod.default_fixture_pins()
        print(json.dumps({'default_fixture_pins': p, 'exists': os.path.exists(p),
                          'EXIT_DECLARED_TUPLE_UNOBSERVED':
                          mod.EXIT_DECLARED_TUPLE_UNOBSERVED}, indent=1))
        return 0 if p and os.path.exists(p) else 1
    if mode == 'census':
        doc = json.loads(git_show('tools/round-46/census.json'))
        paths = doc['paths']
        print(json.dumps({'scope_size': len(paths),
                          'named_but_absent': len(doc.get('named_but_absent') or []),
                          'mine': {p: (p in paths) for p in MINE}}, indent=1))
        return 0 if all(p in paths for p in MINE) else 1
    raise SystemExit('unknown mode ' + mode)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
