#!/usr/bin/env python3
# Scratch fixture driver for W2C2Mutate: writes single mutations of the landed record as commits
# in a scratch clone (never the lane), then scores each commit with the FROZEN c2-mismatch.py.
import hashlib, json, os, re, subprocess, sys, importlib.util
from datetime import datetime, timezone

W = '/fast/scratch/hyaku/kaidoku-r49/W2C2Mutate'
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
R = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
F = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
D = W + '/clone'
COUNTER = W + '/c2-mismatch.py'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', TMPDIR=W, HYAKU_SCRATCH='/fast/scratch/hyaku')
LESSON = 'corpus/lessons/round-49.md'; SRC = 'corpus/SOURCES.md'; SC = 'SCORECARD.md'
LOG = 'LOG.md'; QA = 'corpus/QUALITY.md'; R48 = 'corpus/lessons/round-48.md'
POP = 'corpus/evidence/round-49/c2/popper.html'; FBS = 'corpus/evidence/round-49/c2/freebsd-sysexits.html'
ARROW = '\u2192'


def sh(args, cwd=None, check=True):
    p = subprocess.run(args, capture_output=True, env=ENV, cwd=cwd)
    if check and p.returncode != 0:
        raise SystemExit('FAILED %r: %s' % (args, p.stderr.decode(errors='replace')))
    return p


def utc():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rep(t, old, new, n=1):
    c = t.count(old)
    assert c == n, ('count %d != %d' % (c, n), old[:80])
    return t.replace(old, new)


def line_idx(lines, prefix):
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, ('line prefix', prefix, len(idx))
    return idx[0]


def line_edit(t, prefix, fn):
    lines = t.split('\n')
    i = line_idx(lines, prefix)
    lines[i] = fn(lines[i])
    return '\n'.join(lines)


def cell_set(line, k, fn):
    parts = line.split('|')
    parts[k + 1] = fn(parts[k + 1])
    return '|'.join(parts)


def row_cell(prefix, k, fn):
    return lambda t: line_edit(t, prefix, lambda l: cell_set(l, k, fn))


def load_counter():
    spec = importlib.util.spec_from_file_location('c2m', COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- REV bytes (read via git objects)
T = {}
for p in [LESSON, SRC, SC, LOG, QA, R48, POP, FBS]:
    T[p] = sh(['git', '-C', L, 'show', '%s:%s' % (R, p)]).stdout
TX = {p: T[p].decode('utf-8') for p in [LESSON, SRC, SC, LOG, QA, R48]}
C2 = load_counter()


def popper_candidate():
    """A different true 9-word passage under the same heading (unique in the snapshot)."""
    norm = C2.html_norm(T[POP])
    i = norm.find('Popper\u2019s Thought\x02')
    assert i > 0
    j = i + len('Popper\u2019s Thought\x02')
    seg = re.sub(r'[\x00-\x1f]', ' ', norm[j:j + 1500])
    words = [w for w in seg.split() if '"' not in w]
    for s in range(0, len(words) - 9):
        win = ' '.join(words[s:s + 9])
        pos = norm.find(win)
        sec = C2.section_of(norm, pos) or ''
        if pos >= 0 and norm.count(win) == 1 and 'Backdrop' in sec and win != 'it is consistent with all possible observations, is unscientific':
            return win
    raise SystemExit('no candidate passage')


CAND = popper_candidate()
NEW_POP = T[POP] + b'\n<!-- forged comment -->\n'
NEW_POP_SHA = sha(NEW_POP)
OLD_POP_SHA = sha(T[POP])
FBS_NEW = T[FBS] + b'\n<!-- forged comment -->\n'


def lesson_dup_row(prefix):
    def f(t):
        lines = t.split('\n')
        i = line_idx(lines, prefix)
        lines.insert(i + 1, lines[i])
        return '\n'.join(lines)
    return f


def insert_after(prefix, new_line):
    def f(t):
        lines = t.split('\n')
        i = line_idx(lines, prefix)
        lines.insert(i + 1, new_line)
        return '\n'.join(lines)
    return f


def pathed(d):
    return {k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in d.items()}


def apply_all(spec):
    """spec: list of (path, fn) applied in order to the REV text (bytes for binary paths)."""
    out = {}
    for path, fn in spec:
        base = out[path] if path in out else T[path]
        if isinstance(base, bytes) and path in TX:
            out[path] = fn(TX[path]).encode('utf-8') if False else fn(TX[path]).encode('utf-8')
            TX_MOD = None
        elif isinstance(base, bytes):
            out[path] = fn(base)
        else:
            out[path] = fn(base)
    return out


def E(path, fn):
    """one edit on one path: returns (path, text->text) applied to the REV text."""
    return (path, fn)


def run_edit(edits):
    out = {}
    for path, fn in edits:
        if path in out:
            cur = out[path]
        else:
            cur = TX.get(path, T.get(path))
        if path in TX:
            out[path] = fn(cur).encode('utf-8')
        else:
            out[path] = fn(cur)
    return out


def row_fn(prefix, k, fn):
    return lambda t: line_edit(t, prefix, lambda l: cell_set(l, k, fn))


MUT = []


def mut(mid, label, expected, edits):
    MUT.append((mid, label, expected, edits))


# A1..A9 targets, expected red set in comment
mut('M01', 'lesson A1 declared swapped to the FREEZE hash', ['A1'],
    [E(LESSON, lambda t: rep(t, 'declared=b6f7ca2a6391964dfdedd477cd560bd42159873a',
                             'declared=decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'))])
mut('M02', 'round-49 lesson header freeze replaced by the stale A8 commit b6f7ca2a', [],
    [E(LESSON, lambda t: rep(t, 'Declared freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`',
                             'Declared freeze `b6f7ca2a6391964dfdedd477cd560bd42159873a`'))])
mut('M03', 'lesson A2 dead hash replaced by the FREEZE hash', ['A2'],
    [E(LESSON, lambda t: rep(t, 'dead=663f30ee7516942a0120e7de68fe88356e680822',
                             'dead=decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'))])
mut('M04', 'lesson A2 actual replaced by the dead hash', ['A2'],
    [E(LESSON, lambda t: rep(t, 'actual=663f30ee751694fb0970e7de68fe88356e680822',
                             'actual=663f30ee7516942a0120e7de68fe88356e680822'))])
mut('M05', 'lesson A3 unnamed 7fe11332 replaced by 2e785632 (named in LOG)', ['A3'],
    [E(LESSON, lambda t: rep(t, 'unnamed=577a02a5,8847042a,7fe11332',
                             'unnamed=577a02a5,8847042a,2e785632'))])
mut('M06', 'lesson A3 one LOG line number for 33f65a91 moved 3444 -> 3443', ['A3'],
    [E(LESSON, lambda t: rep(t, 'log_33f65a91=3440,3441,3444', 'log_33f65a91=3440,3441,3443'))])
mut('M07', 'lesson A4 missing list drops ScribeReportNumbers', ['A4'],
    [E(LESSON, lambda t: rep(t, 'missing=C1Battery,C1Meaning,ScribeReportNumbers',
                             'missing=C1Battery,C1Meaning'))])
mut('M08', 'lesson A5 report_c2 set to the raw digest prefix d1bb87d8', ['A5'],
    [E(LESSON, lambda t: rep(t, 'report_c2=c30628ae', 'report_c2=d1bb87d8'))])
mut('M09', 'lesson gains a second, empty "## Corrections to round 48" section', ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'],
    [E(LESSON, lambda t: t + ('' if t.endswith('\n') else '\n') + '\n## Corrections to round 48\n\nNo lines here.\n')])
mut('M10', 'lesson S147 Gate row: "it is scientific" -> "it is unscientific" (lesson only)', [],
    [E(LESSON, lambda t: line_edit(t, '| S147 |', lambda l: rep(l, 'it is scientific', 'it is unscientific')))])
mut('M11', 'lesson S147 Gate row: pinned sha256 last hex digit changed (lesson only)', [],
    [E(LESSON, lambda t: line_edit(t, '| S147 |', lambda l: rep(l, '6ec207`', '6ec208`')))])
mut('M12', 'registry S147 second quote re-pointed to another true passage under the same heading', [],
    [E(SRC, row_fn('| S147 |', 5, lambda s: rep(s, '"it is consistent with all possible observations, is unscientific" (9 words)',
                                                  '"%s" (9 words)' % CAND)))])
mut('M13', 'registry S147 opened date 2026-10-28 -> 2026-10-27', ['A6'],
    [E(SRC, row_fn('| S147 |', 8, lambda s: rep(s, '2026-10-28', '2026-10-27')))])
mut('M14', 'registry S147 scope cell (column 5, unchecked by any atom) rewritten', [],
    [E(SRC, row_fn('| S147 |', 4, lambda s: ' Unrelated scope statement. '))])
mut('M15', 'registry S148 used-by lesson link removed', ['A7'],
    [E(SRC, row_fn('| S148 |', 10, lambda s: rep(s, 'corpus/lessons/round-49.md', '\u2014')))])
mut('M16', 'S149 snapshot freebsd-sysexits.html edited (comment appended); S149 anchor untouched', [],
    [('%s' % FBS, lambda b: FBS_NEW)])
mut('M17', 'registry S149 row duplicated (same id, second copy)', [],
    [E(SRC, lambda t: (lambda lines: (lines.insert(line_idx(lines, '| S149 |') + 1, lines[line_idx(lines, '| S149 |')]), '\n'.join(lines))[1])(t.split('\n')))])
mut('M18', 'registry S147 row duplicated (same id, second copy)', ['A6'],
    [E(SRC, lambda t: (lambda lines: (lines.insert(line_idx(lines, '| S147 |') + 1, lines[line_idx(lines, '| S147 |')]), '\n'.join(lines))[1])(t.split('\n')))])
mut('M19', 'registry S145 scope edited (S145 must stay byte-identical)', ['A6'],
    [E(SRC, row_fn('| S145 |', 4, lambda s: rep(s, 'demarcation of', 'demarcations of')))])
mut('M20', 'registry S149 status rejected -> mined', ['A8'],
    [E(SRC, row_fn('| S149 |', 7, lambda s: rep(s, 'rejected', 'mined')))])
mut('M21', 'search log round-49 identified 3 -> 300 (identified is asserted, not derivable)', [],
    [E(SRC, lambda t: line_edit(t, '- 2026-10-28 round 49', lambda l: rep(l, 'Identified 3, screened 3', 'Identified 300, screened 3')))])
mut('M22', 'search log: second round-49 entry marked "round-49" (hyphen) appended', [],
    [E(SRC, lambda t: insert_after('- 2026-10-28 round 49', '- 2026-10-28 round-49 \u2014 Question: duplicate entry with a hyphen marker. Where searched: none. Identified 3, screened 3, included 2, excluded 1; rows 146 ' + ARROW + ' 149. Exclusion: duplicate. Stop: duplicate.')(t))])
mut('M23', 'search log: second round-48 entry without the late marker appended', [],
    [E(SRC, lambda t: insert_after('- 2026-10-28 round 48', '- 2026-10-28 round 48 \u2014 Question: duplicate entry without the late marker. Where searched: none. Identified 1, screened 1, included 1, excluded 0; rows 61b87d74 -> 8847042a. Stop: duplicate.')(t))])
mut('M24', 'search log round-49 rows 146 -> 149 changed to 146 -> 150', ['A8'],
    [E(SRC, lambda t: line_edit(t, '- 2026-10-28 round 49', lambda l: rep(l, 'rows 146 ' + ARROW + ' 149', 'rows 146 ' + ARROW + ' 150')))])
mut('M25', 'SCORECARD A9 verdict rejected-harmed -> admitted', ['A9'],
    [E(SC, lambda t: rep(t, 'verdict=rejected-harmed', 'verdict=admitted'))])
mut('M26', 'SCORECARD round-48 declared freeze (base input) edited at REV', [],
    [E(SC, lambda t: rep(t, '**Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873a`',
                         '**Declared freeze:** `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`'))])
OLD48 = re.findall(r'Declared freeze\s+`[0-9a-f]{40}`', TX[R48])
assert len(OLD48) == 1, OLD48
mut('M27', 'round-48 lesson header (base input, must be byte-identical at REV) edited', ['A1'],
    [E(R48, lambda t: rep(t, OLD48[0], OLD48[0].replace(OLD48[0][-41:-1], 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d')))])
mut('M28', 'LOG.md line 3440 edited in place at REV (not an append)', ['A3'],
    [E(LOG, lambda t: (lambda lines: (lines.__setitem__(3439, lines[3439] + ' [edited]'), '\n'.join(lines))[1])(t.split('\n')))])
mut('M29', 'QUALITY row 88 failure clause weakened (row not read by any atom)', [],
    [E(QA, lambda t: rep(t, 'Fails when a lesson header and the SCORECARD disagree', 'Fails when a lesson header and the SCORECARD agree'))])
mut('M30', 'popper snapshot forged (comment appended) + S147 anchor sha re-pinned consistently', [],
    [('%s' % POP, lambda b: NEW_POP),
     (SRC, row_fn('| S147 |', 5, lambda s: rep(s, sha(T[POP]), NEW_POP_SHA)))])
assert len(MUT) == 30, len(MUT)


def commit_tree(files, msg):
    for path, data in files.items():
        full = os.path.join(D, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data)
    sh(['git', '-C', D, 'add', '-A'])
    sh(['git', '-C', D, '-c', 'commit.gpgsign=false', 'commit', '-q', '--allow-empty', '-m', msg])
    return sh(['git', '-C', D, 'rev-parse', 'HEAD']).stdout.decode().strip()


def score(rev, out_json):
    p = subprocess.run(['python3', '-I', '-B', COUNTER, '--root', D, '--rev', rev, '--freeze', F,
                        '--json-out', out_json], capture_output=True, env=ENV)
    d = json.load(open(out_json)) if os.path.exists(out_json) else {}
    red = sorted(k for k, v in d.get('atoms', {}).items() if not v['ok'])
    return {'exit': p.returncode, 'stdout_sha256': sha(p.stdout), 'stdout_bytes': len(p.stdout),
            'mismatches': d.get('mismatches'), 'reason': d.get('reason'), 'red': red,
            'atoms_total': d.get('atoms_total'), 'counter_sha256_run': d.get('counter_sha256')}


def reset_to_rev():
    sh(['git', '-C', D, 'reset', '-q', '--hard', R])
    sh(['git', '-C', D, 'clean', '-qfd'])


if __name__ == '__main__':
    os.makedirs(W + '/mut', exist_ok=True)
    results = []
    # clone (shared objects; read-only w.r.t. the lane)
    if not os.path.isdir(D):
        sh(['git', 'clone', '-q', '--shared', L, D])
    real = sh(['git', '-C', D, 'rev-parse', '--show-toplevel']).stdout.decode().strip()
    assert os.path.realpath(real) == os.path.realpath(D), real
    sh(['git', '-C', D, 'config', 'user.name', 'W2C2Mutate scratch'])
    sh(['git', '-C', D, 'config', 'user.email', 'w2c2mutate-scratch@invalid'])
    # controls
    reset_to_rev()
    sh(['git', '-C', D, 'checkout', '-q', '--detach', R])
    ctl = score(R, W + '/mut/C0-rev.json')
    ctl['label'] = 'C0 REV itself in the clone (expect green)'
    ctl['utc'] = utc()
    ctl['commit'] = R
    results.append(dict(id='C0', **ctl))
    reset_to_rev()
    h = commit_tree({}, 'W2C2Mutate control: empty commit')
    c1 = score(h, W + '/mut/C1-empty.json')
    results.append(dict(id='C1', label='empty commit on REV (expect green)', commit=h, utc=utc(), **c1))
    reset_to_rev()
    cf = score(F, W + '/mut/CF-freeze.json')
    results.append(dict(id='CF', label='FREEZE itself (expect 9 red, exit 1)', commit=F, utc=utc(), **cf))
    for mid, label, expected, edits in MUT:
        reset_to_rev()
        files = {}
        for path, fn in edits:
            if path in TX:
                cur = files[path].decode('utf-8') if path in files else TX[path]
                files[path] = fn(cur).encode('utf-8')
            else:
                cur = files[path] if path in files else T[path]
                files[path] = fn(cur)
        h = commit_tree(files, 'W2C2Mutate %s (scratch): %s' % (mid, label))
        changed = sh(['git', '-C', D, 'diff', '--name-only', R, h]).stdout.decode().split()
        sc = score(h, W + '/mut/%s.json' % mid)
        ok_expected = sc['red'] == sorted(expected) if expected or sc['red'] else True
        results.append(dict(id=mid, label=label, expected_red=sorted(expected), commit=h,
                            changed_paths=changed, utc=utc(), match_expected=(sc['red'] == sorted(expected)), **sc))
        print(mid, sc['exit'], sc['mismatches'], sc['red'], 'EXPECTED' if sc['red'] == sorted(expected) else 'DIFFERS', file=sys.stderr)
    reset_to_rev()
    json.dump(results, open(W + '/mut/results.json', 'w'), indent=1, sort_keys=True)
    print('wrote', W + '/mut/results.json', file=sys.stderr)
