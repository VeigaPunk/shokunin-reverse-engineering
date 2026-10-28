#!/usr/bin/env python3
"""C2CounterMut scratch driver: builds source mutants of c2-mismatch.py and fixture forgeries
(git commits in the scratch clone only), runs every counter on every state, and writes
results.json. Writes nothing in the lane, the fleet repo or the drafts."""
import concurrent.futures as cf
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time

S = '/fast/scratch/hyaku/kaidoku-r49/C2CounterMut'
CL = S + '/clone'
FREEZE = 'dc6b13fed334a7f771d10f687ccd5798a80f9c6e'   # mkclone DEV_FREEZE
GREEN = 'ed537b258e4439c88e9f596ad8504a4cacd89456'    # c2-after DEV_AFTER
BASE = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
DRAFT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft'
ORIG = S + '/c2-mismatch.orig.py'
for d in ('mut', 'runs', 'forge'):
    os.makedirs(f'{S}/{d}', exist_ok=True)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*a):
    p = subprocess.run(['git', '-C', CL] + list(a), capture_output=True)
    if p.returncode != 0:
        raise SystemExit('git %s failed: %s' % (a, p.stderr.decode()))
    return p.stdout.decode()


assert git('rev-parse', '--show-toplevel').strip() == CL

# ------------------------------------------------------------------ mutants
# (id, atom-or-area, description, old, new, occurrence index, base)
MUT = [
    ('M01', 'A1', 'declared!=SCORECARD check removed', "if d.get('declared') != declared_sc:", "if False:", 0, 'orig'),
    ('M02', 'A1', 'stale!=lesson-header check removed', "if d.get('stale') != stale:", "if False:", 0, 'orig'),
    ('M03', 'A1', 'round-48 lesson byte-identity compare removed', "if les is None or base is None or sha(les) != sha(base):", "if les is None or base is None:", 0, 'orig'),
    ('M04', 'A1', 'declared==stale no-disagreement check removed', "if declared_sc and stale and declared_sc == stale:", "if False:", 0, 'orig'),
    ('M05', 'A2', 'dead-hash-resolves-to-commit check removed', "if r.is_commit(dead):", "if False:", 0, 'orig'),
    ('M06', 'A2', '8-hex prefix check removed (dead==real kept)', "if dead[:8] != real[:8] or dead == real:", "if dead == real:", 0, 'orig'),
    ('M07', 'A2', 'real-is-ancestor-of-REV check removed', "elif not r.ancestor(real, rev):", "elif False:", 0, 'orig'),
    ('M08', 'A3', 'LOG.md append-only startswith compare removed', "if base is None or now is None or not now.startswith(base):", "if base is None or now is None:", 0, 'orig'),
    ('M09', 'A3', 'stated-vs-derived line-number compare removed', "        if sorted(want) != got:", "        if False:", 0, 'orig'),
    ('M10', 'A3', 'only the first log_ pointer checked', "    for k in keys:", "    for k in keys[:1]:", 0, 'orig'),
    ('M11', 'A3', 'unnamed-hash check removed', "    for h in un:", "    for h in []:", 0, 'orig'),
    ('M12', 'A4', 'seats count check removed', "if d.get('seats') != str(len(names)):", "if False:", 0, 'orig'),
    ('M13', 'A4', 'missing-seat list check removed', "if sorted(x for x in d.get('missing', '').split(',') if x) != sorted(missing):", "if False:", 0, 'orig'),
    ('M14', 'A4', 'every seat counted as having a report', "has = ('%s/%s.md' % (W1, n)) in tree or any(", "has = True or any(", 0, 'orig'),
    ('M15', 'A4', 'non-.md file under seat dir counts as report', " and p.endswith('.md')", "", 0, 'orig'),
    ('M16', 'A5', 'stripped-digest compare removed', "if d.get(k + '_stripped') != stripped:", "if False:", 0, 'orig'),
    ('M17', 'A5', 'report-prefix compare weakened to length only', "if len(q) != 8 or stripped[:8] != q or raw[:8] == q:", "if len(q) != 8:", 0, 'orig'),
    ('M18', 'A5', 'raw-digest compare removed', "if d.get(k + '_raw') != raw:", "if False:", 0, 'orig'),
    ('M19', 'A5', 'stripped digest computed without stripping', "stripped = sha(b[:-1] if b.endswith(b'\\n') else b)", "stripped = sha(b)", 0, 'orig'),
    ('M20', 'A6/A7', 'row teaches must open "supersedes <old> —" removed', "if not c[6].startswith('supersedes %s \\u2014' % old):", "if False:", 0, 'orig'),
    ('M21', 'A6/A7', 'anchor sha256 pin to snapshot removed', "if sha(b) not in pin:", "if False:", 0, 'orig'),
    ('M22', 'A6', 'word limit 25 -> 250 (A6)', "if len(qn.split()) > 25:", "if len(qn.split()) > 250:", 0, 'orig'),
    ('M22b', 'A7', 'word limit 25 -> 250 (A7)', "if len(qn.split()) > 25:", "if len(qn.split()) > 250:", 1, 'orig'),
    ('M23', 'A6', 'anchor must name the snapshot heading removed', "if not head or head not in c[5]:", "if False:", 0, 'orig'),
    ('M24', 'A6', 'S147 quoted-passage presence removed', "if not qs:", "if False:", 0, 'orig'),
    ('M24b', 'A7', 'S148 quoted-passage presence removed', "if not qs:", "if False:", 1, 'orig'),
    ('M25', 'A7', 'S148 quote-in-snapshot check removed', "if qn not in norm:", "if False:", 0, 'orig'),
    ('M26', 'A7', 'snapshot must carry "EX_USAGE 64" removed', "if 'EX_USAGE 64' not in norm:", "if False:", 0, 'orig'),
    ('M27', 'A7', 'teaches must name 64 removed (keeps EX_USAGE)', "if 'EX_USAGE' not in c[6] or not re.search(r'\\b64\\b', c[6]):", "if 'EX_USAGE' not in c[6]:", 0, 'orig'),
    ('M28', 'A7', 'S148 source URL (3head) check removed', "if 'man7.org/linux/man-pages/man3/sysexits.h.3head.html' not in c[1]:", "if False:", 0, 'orig'),
    ('M29', 'A6', 'S147 source-domain check removed', "if 'plato.stanford.edu/entries/popper/' not in c[1]:", "if False:", 0, 'orig'),
    ('M30', 'A8', 'exactly-one search-log entry per round weakened to >=1', "if len(ent) != 1:", "if len(ent) < 1:", 0, 'orig'),
    ('M31', 'A8', 'screened == included+excluded check removed', "or scr != inc + exc or idn < scr:", "or idn < scr:", 0, 'orig'),
    ('M32', 'A8', 'identified >= screened check removed', " or idn < scr:", ":", 0, 'orig'),
    ('M33', 'A8', 'rows B -> A check removed', "if (int(n.group(1)), int(n.group(2))) != want[:2]:", "if False:", 0, 'orig'),
    ('M34', 'A8', 'round-48 late-entry filter removed', "ent = [l for l in ent if 'late entry' in l]", "ent = ent", 0, 'orig'),
    ('M35', 'A9', 'SCORECARD A9 line presence removed', "if not any(want in l for l in sc):", "if False:", 0, 'orig'),
    ('M36', 'A9', 'source calibration|harmed row check removed', "if not re.search(r'\\|\\s*calibration\\s*\\|\\s*harmed\\s*\\|', src):", "if False:", 0, 'orig'),
    ('M37', 'A9', 'source rejected-harmed token check removed', "if 'rejected-harmed' not in src:", "if False:", 0, 'orig'),
    ('M38', 'freeze', 'FREEZE ancestor-of-REV check removed', "if not r.ancestor(freeze, rev):", "if False:", 0, 'orig'),
    ('M39', 'freeze', 'FREEZE..REV path walk (touched) removed', "    if t:\n        return 'frozen path touched in FREEZE..REV: %s' % ';'.join(t[:6])", "    if False:\n        return 'frozen path touched in FREEZE..REV: %s' % ';'.join(t[:6])", 0, 'orig'),
    ('M40', 'freeze', 'blob-equality backstop removed', "if p and r.show(freeze, p) != r.show(rev, p):", "if False:", 0, 'orig'),
    ('M41', 'freeze', 'plans/round-49-claims.md dropped from the walk', "'--', *FROZEN)", "'--', 'tools/round-49')", 0, 'orig'),
    ('M42', 'exit', 'exit code forced to 0', "code = 0 if res['mismatches'] == 0 else 1", "code = 0", 0, 'orig'),
    ('M43', 'exit', 'battery failing list ignored in exit code', "if b['failing']:", "if False:", 0, 'orig'),
    ('M44', 'battery', 'do-nothing all-nine-red check removed', "if red != sorted(ATOM_IDS):", "if False:", 0, 'orig'),
    ('M45', 'A2', 'absent A2 line accepted', "return ['lesson line A2 absent']", "return []", 0, 'orig'),
    ('M46', 'A3', 'absent A3 line accepted', "return ['lesson line A3 absent']", "return []", 0, 'orig'),
    ('M47', 'A3', 'no-log_-pointer check removed', "    if not keys:", "    if False:", 0, 'orig'),
    ('M49', 'lesson', 'lesson lines: first occurrence wins (not last)', "out[m.group(1)] = kv", "out.setdefault(m.group(1), kv)", 0, 'orig'),
    ('M50', 'A4', 'reports count check removed', "if d.get('reports') != str(len(names) - len(missing)):", "if False:", 0, 'orig'),
    ('M51', 'A6/A7', 'row append-only compare of S145/S146 removed', "if rows.get(old) != base_rows.get(old) or old not in rows:", "if old not in rows:", 0, 'orig'),
    ('M52', 'A8', 'and/or swapped in the A8 (inc,exc) clause', "if (inc, exc) != want[2:] or scr != inc + exc or idn < scr:", "if (inc, exc) != want[2:] and scr != inc + exc or idn < scr:", 0, 'orig'),
    ('M53', 'A6/A7', 'row used-by lesson check removed', "if LESSON not in c[10] or r.show(rev, LESSON) is None:", "if False:", 0, 'orig'),
    ('M54', 'A6/A7', 'row status/tier/opened check weakened (date dropped)', "if c[2] != 'docs' or c[3] != 'A' or c[7] != 'mined' or c[8] != ROUND_DATE:", "if c[2] != 'docs' or c[3] != 'A' or c[7] != 'mined':", 0, 'orig'),
    ('M55', 'exit', 'battery-broken: orig with a no-op battery mutation (see BB pair)', "if b['failing']:", "if False:", 0, 'bb'),
]


def apply(src, old, new, occ):
    pos = -1
    for _ in range(occ + 1):
        pos = src.find(old, pos + 1)
        if pos < 0:
            raise SystemExit('mutation anchor not found: %r (occ %d)' % (old[:70], occ))
    return src[:pos] + new + src[pos + len(old):]


ORIG_SRC = open(ORIG).read()
BB_SRC = ORIG_SRC.replace("rep('SCORECARD.md', 'calibration=harmed', 'calibration=improved')",
                          "rep('SCORECARD.md', 'calibration=harmed', 'calibration=harmed')", 1)
assert BB_SRC != ORIG_SRC
SRC = {'orig': ORIG_SRC, 'bb': BB_SRC}
MUT_FILES = {}
for mid, atom, desc, old, new, occ, base in MUT:
    m = apply(SRC[base], old, new, occ)
    if m == SRC[base]:
        raise SystemExit('noop mutant ' + mid)
    compile(m, mid, 'exec')
    p = f'{S}/mut/{mid}.py'
    open(p, 'w').write(m)
    MUT_FILES[mid] = p
MUT_FILES['ORIG'] = ORIG
# a full-battery-broken original for M55 (its partner is 'ORIG_BB')
open(f'{S}/mut/ORIG_BB.py', 'w').write(BB_SRC)
MUT_FILES['ORIG_BB'] = f'{S}/mut/ORIG_BB.py'

# ------------------------------------------------------------------ forgeries
ORIG_HEAD = git('rev-parse', 'HEAD').strip()
L49 = 'corpus/lessons/round-49.md'
Q1 = ('falsifiability as his criterion for demarcating science from non-science: if a theory is '
      'incompatible with possible empirical observations it is scientific')


def reset():
    git('checkout', '-q', '-f', GREEN)
    git('clean', '-fdq')


def rd(p):
    return open(os.path.join(CL, p), 'rb').read()


def rt(p):
    return rd(p).decode('utf-8')


def wr(p, b):
    fp = os.path.join(CL, p)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'wb').write(b.encode() if isinstance(b, str) else b)


def sub1(p, old, new, n=1):
    t = rt(p)
    c = t.count(old)
    assert c == n, (p, old[:70], c)
    wr(p, t.replace(old, new))


def line_sub(p, startswith, fn):
    lines = rt(p).split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(startswith)]
    assert len(idx) == 1, (p, startswith, len(idx))
    lines[idx[0]] = fn(lines[idx[0]]) if callable(fn) else fn
    wr(p, '\n'.join(lines))


def line_del(p, startswith):
    lines = rt(p).split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(startswith)]
    assert len(idx) == 1, (p, startswith, len(idx))
    del lines[idx[0]]
    wr(p, '\n'.join(lines))


def line_ins_before(p, startswith, new):
    lines = rt(p).split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(startswith)]
    assert len(idx) == 1
    lines.insert(idx[0], new)
    wr(p, '\n'.join(lines))


def line_ins_after(p, startswith, new):
    lines = rt(p).split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(startswith)]
    assert len(idx) == 1
    lines.insert(idx[0] + 1, new)
    wr(p, '\n'.join(lines))


def row_sub(rid, old, new):
    lines = rt('corpus/SOURCES.md').split('\n')
    idx = [i for i, l in enumerate(lines) if re.match(r'^ {0,3}\|\s*' + rid + r'\s*\|', l)]
    assert len(idx) == 1, rid
    assert lines[idx[0]].count(old) == 1, (rid, old[:60], lines[idx[0]].count(old))
    lines[idx[0]] = lines[idx[0]].replace(old, new)
    wr('corpus/SOURCES.md', '\n'.join(lines))


def lesson(key, newline):
    line_sub(L49, '- ' + key + ' ', newline)


def commit(msg):
    git('add', '-A')
    git('commit', '-q', '-m', msg)
    return git('rev-parse', 'HEAD').strip()


def f_popper_pin():
    return sha(rd('corpus/evidence/round-49/c2/popper.html'))


def f_sysexits_pin():
    return sha(rd('corpus/evidence/round-49/c2/sysexits.html'))


C1_RECEIPT = '.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json'
ROUND48_LESSON = 'corpus/lessons/round-48.md'
CLOSURE = 'corpus/lessons/round-48-verifier-spotcheck.md'
A1_BASE = 'declared=b6f7ca2a6391964dfdedd477cd560bd42159873a stale=0f06251bf6a3a6964c715f67243d4df12e854258'
A2_BASE = 'dead=663f30ee7516942a0120e7de68fe88356e680822 actual=663f30ee751694fb0970e7de68fe88356e680822'
A4_BASE = 'seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers'
A3_BASE = 'log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a'
SC_R48_FREEZE = r'(\*\*Declared freeze:\*\*\s*`)b6f7ca2a6391964dfdedd477cd560bd42159873a`'
ROUND49_LINE = '- 2026-10-28 round 49'
C1_RAW_OLD = '6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e'


def side_commit():
    git('checkout', '-q', '-f', BASE)
    wr('side-note.txt', 'side branch, not a descendant of FREEZE\n')
    x = commit('side commit (not an ancestor of REV)')
    git('checkout', '-q', '-f', GREEN)
    git('clean', '-fdq')
    return x


def touch_then(path, restore):
    """Two commits: modify a frozen path, then (optionally) restore its FREEZE bytes."""
    orig = subprocess.run(['git', '-C', CL, 'show', FREEZE + ':' + path], capture_output=True).stdout
    wr(path, orig + b'\n# touched\n')
    commit('touch frozen path ' + path)
    if restore:
        wr(path, orig)
        return commit('restore frozen path ' + path)
    return git('rev-parse', 'HEAD').strip()


def build_forgeries():
    F = []

    def add(fid, desc, expect, fn):
        reset()
        fn()
        git('add', '-A')
        dirty = git('status', '--porcelain').strip() != ''
        rev = commit(fid) if dirty else git('rev-parse', 'HEAD').strip()
        F.append({'id': fid, 'desc': desc, 'expect_orig': expect, 'rev': rev})

    def f01():
        lesson('A3', '- A3 log_2e785632=3440,3441,3445 unnamed=577a02a5,8847042a')
    add('F01', 'A3 pointer for 33f65a91 dropped (incomplete pointer set)', 'accept', f01)

    def f02():
        lesson('A2', '- A2 dead=663f30ee' + 'b' * 32 + ' actual=663f30ee751694fb0970e7de68fe88356e680822')
    add('F02', 'A2 dead hash replaced by an invented non-commit (no report check)', 'accept', f02)

    def f03():
        assert not os.path.exists(CL + '/.ufo/waves/round-48/w1/C1Meaning.md')
        wr('.ufo/waves/round-48/w1/C1Meaning.md', '')
        lesson('A4', '- A4 seats=75 reports=73 missing=C1Battery,ScribeReportNumbers')
    add('F03', 'A4 empty placeholder report.md written for C1Meaning; lesson re-stated', 'accept', f03)

    def f04():
        pop = rd('corpus/evidence/round-49/c2/popper.html')
        old = sha(pop)
        new = pop + b'\n<p>Unverified addition, fabricated snapshot.</p>\n'
        wr('corpus/evidence/round-49/c2/popper.html', new)
        row_sub('S147', old, sha(new))
    add('F04', 'A6 snapshot fabricated (extra paragraph) and sha256 pin re-written to match', 'accept', f04)

    add('F05', 'A7 teaches inverted fact: "EX_USAGE is 2, not 64" (keeps both tokens)', 'accept',
        lambda: row_sub('S148', 'EX_USAGE is 64, not 2', 'EX_USAGE is 2, not 64'))

    def f06():
        line_sub('corpus/SOURCES.md', ROUND49_LINE, lambda l: l.replace('identified 2, screened 2', 'identified 200, screened 2'))
    add('F06', 'A8 round-49 identified count inflated 2 -> 200 (identified unverified)', 'accept', f06)

    def f07():
        line_sub('SCORECARD.md', '- A9 verdict=', lambda l: l + ' (superseded: calibration=improved)')
    add('F07', 'A9 SCORECARD line carries a contradicting suffix (substring match)', 'accept', f07)

    def f08():
        t = rt('SCORECARD.md')
        new, n = re.subn(SC_R48_FREEZE, r'\g<1>61b87d742032e65fca9c38267d7d6ed7e555edad`', t)
        assert n == 1, n
        wr('SCORECARD.md', new)
        lesson('A1', '- A1 declared=61b87d742032e65fca9c38267d7d6ed7e555edad stale=0f06251bf6a3a6964c715f67243d4df12e854258')
    add('F08', 'historical SCORECARD Round-48 declared freeze rewritten; A1 re-stated to match', 'accept', f08)

    def f09():
        old = rd(C1_RECEIPT)
        assert old.endswith(b'\n')
        new = old[:-1] + b' \n'
        wr(C1_RECEIPT, new)
        raw, strip = sha(new), sha(new[:-1])
        line_sub(L49, '- A5 ', lambda l: re.sub(r'report_c1=\S+', 'report_c1=' + strip[:8],
                 re.sub(r'c1_stripped=\S+', 'c1_stripped=' + strip,
                        re.sub(r'c1_raw=\S+', 'c1_raw=' + raw, l))))
    add('F09', 'round-48 C1 receipt bytes rewritten; A5 digests re-derived and re-stated', 'accept', f09)

    add('F10', 'A3 unnamed list drops 8847042a (incomplete unnamed set)', 'accept',
        lambda: lesson('A3', '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5'))

    def f11():
        row_sub('S147', f_popper_pin(), '0' * 64)
    add('F11', 'A6 S147 sha256 pin zeroed', 'reject', f11)

    def f12():
        row_sub('S147', '"' + Q1 + '"', Q1)
    add('F12', 'A6 S147 quotation marks removed (no quoted passage)', 'reject', f12)

    add('F13', 'A7 S148 quote altered (improperly)', 'reject',
        lambda: row_sub('S148', 'The command was used incorrectly', 'The command was used improperly'))

    def f14():
        sx = rd('corpus/evidence/round-49/c2/sysexits.html')
        old_pin = sha(sx)
        new, n = re.subn(rb'(EX_USAGE\D{1,60}?)64', rb'\g<1>2', sx, count=1)
        assert n == 1, n
        wr('corpus/evidence/round-49/c2/sysexits.html', new)
        row_sub('S148', old_pin, sha(new))
    add('F14', 'A7 snapshot EX_USAGE value edited to 2 with pin re-written (teaches keeps 64)', 'reject', f14)

    add('F15', 'A7 S148 source URL is the non-3head page', 'reject',
        lambda: row_sub('S148', 'man3/sysexits.h.3head.html', 'man3/sysexits.h.3.html'))

    def f16():
        line_ins_after('corpus/SOURCES.md', ROUND49_LINE,
                       '- 2026-10-28 round 49 — duplicate line: identified 2, screened 2, included 1, excluded 1; rows 146 → 148.')
    add('F16', 'A8 second round-49 entry with wrong numbers appended after the correct one', 'reject', f16)

    add('F17', 'A8 round-49 identified 1 < screened 2', 'reject',
        lambda: line_sub('corpus/SOURCES.md', ROUND49_LINE, lambda l: l.replace('identified 2, screened 2', 'identified 1, screened 2')))
    add('F18', 'A8 round-49 screened 3 != included+excluded 2 (identified 3)', 'reject',
        lambda: line_sub('corpus/SOURCES.md', ROUND49_LINE, lambda l: l.replace('identified 2, screened 2, included 2', 'identified 3, screened 3, included 2')))
    add('F19', 'A8 round-49 rows stated 146 -> 147 (derived 148)', 'reject',
        lambda: line_sub('corpus/SOURCES.md', ROUND49_LINE, lambda l: l.replace('rows 146 → 148', 'rows 146 → 147')))
    add('F20', 'A9 closure calibration row edited to improved', 'reject',
        lambda: sub1(CLOSURE, '| calibration | harmed |', '| calibration | improved |'))
    add('F21', 'A9 closure admission token rewritten to accepted (all occurrences)', 'reject',
        lambda: sub1(CLOSURE, 'rejected-harmed', 'accepted', 1))

    def f22():
        x = side_commit()
        git('checkout', '-q', '-f', GREEN)
        git('clean', '-fdq')
        lesson('A2', '- A2 dead=' + x[:8] + '1' * 32 + ' actual=' + x)
    add('F22', 'A2 real hash is a side-branch commit that is not an ancestor of REV', 'reject', f22)

    def f23():
        touch_then('tools/round-49/c2-mismatch.py', restore=True)
    add('F23', 'frozen tools/round-49/c2-mismatch.py touched then restored byte-identically (later restore)', 'reject', f23)

    def f24():
        touch_then('plans/round-49-claims.md', restore=True)
    add('F24', 'frozen plans/round-49-claims.md touched then restored byte-identically', 'reject', f24)

    def f25():
        touch_then('tools/round-49/c2-mismatch.py', restore=False)
    add('F25', 'frozen tools file modified and not restored (control)', 'reject', f25)

    def f26():
        line_ins_before(L49, '- A2 ', '- A2 dead=663f30ee7516942a0120e7de68fe88356e680822 actual=663f30ee' + 'c' * 32)
    add('F26', 'A2 duplicate line placed before the real one (last line wins in the parser)', 'accept', f26)

    add('F27', 'A3 line carries no log_ pointer at all', 'reject',
        lambda: lesson('A3', '- A3 unnamed=577a02a5,8847042a'))

    add('F28', 'A6 S147 used-by names a lesson that is not the round-49 lesson', 'reject',
        lambda: row_sub('S147', 'corpus/lessons/round-49.md', 'corpus/lessons/round-48.md'))
    add('F29', 'A6 S147 opened date 2026-10-27', 'reject',
        lambda: row_sub('S147', '| mined | 2026-10-28 |', '| mined | 2026-10-27 |'))
    add('F30', 'S145 registry line edited in place (append-only broken)', 'reject',
        lambda: row_sub('S145', 'The falsifiability criterion as the demarcation of an empirical check',
                        'The falsifiability criterion as the demarcation of an empirical check (edited)'))
    add('F31', 'A6 S147 source URL changed to another path on the same host', 'reject',
        lambda: row_sub('S147', 'https://plato.stanford.edu/entries/popper/', 'https://plato.stanford.edu/entries/popper-2/'))

    def f32():
        norm = SPEC_MOD.html_norm(rd('corpus/evidence/round-49/c2/popper.html'))
        i = norm.index(Q1)
        passage = ' '.join(norm[i:].split(' ')[:30])
        assert all(c not in passage for c in '"|`\x01\x02'), passage
        row_sub('S147', '"' + Q1 + '"', '"' + passage + '"')
    add('F32', 'A6 S147 quotation lengthened to 30 words, present in the snapshot', 'reject', f32)

    add('F33', 'A5 lesson report_c1 names the RAW digest prefix', 'reject',
        lambda: line_sub(L49, '- A5 ', lambda l: re.sub(r'report_c1=\S+', 'report_c1=' + sha(rd(C1_RECEIPT))[:8], l)))
    add('F34', 'A5 lesson c1_raw zeroed', 'reject',
        lambda: line_sub(L49, '- A5 ', lambda l: re.sub(r'c1_raw=\S+', 'c1_raw=' + '0' * 64, l)))
    add('F35', 'A1 lesson stale names a commit that is not the lesson header freeze', 'reject',
        lambda: lesson('A1', '- A1 declared=b6f7ca2a6391964dfdedd477cd560bd42159873a stale=61b87d742032e65fca9c38267d7d6ed7e555edad'))

    def f36():
        wr(ROUND48_LESSON, rd(ROUND48_LESSON) + b'\n<!-- edited -->\n')
    add('F36', 'round-48 lesson edited in place (not byte-identical to base)', 'reject', f36)

    def f37():
        t = rt('SCORECARD.md')
        new, n = re.subn(SC_R48_FREEZE, r'\g<1>0f06251bf6a3a6964c715f67243d4df12e854258`', t)
        assert n == 1
        wr('SCORECARD.md', new)
        lesson('A1', '- A1 declared=0f06251bf6a3a6964c715f67243d4df12e854258 stale=0f06251bf6a3a6964c715f67243d4df12e854258')
    add('F37', 'SCORECARD declared == lesson header (no disagreement)', 'reject', f37)

    add('F38', 'A1 lesson declared names a freeze that is not SCORECARD declared', 'reject',
        lambda: lesson('A1', '- A1 declared=0f06251bf6a3a6964c715f67243d4df12e854258 stale=0f06251bf6a3a6964c715f67243d4df12e854258'))
    add('F39', 'A2 dead hash prefix differs from the real hash prefix', 'reject',
        lambda: lesson('A2', '- A2 dead=0f06251b' + 'd' * 32 + ' actual=663f30ee751694fb0970e7de68fe88356e680822'))
    add('F40', 'A4 seats stated 76', 'reject',
        lambda: lesson('A4', '- A4 seats=76 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers'))
    add('F41', 'A4 missing list drops C1Battery (reports count still consistent)', 'reject',
        lambda: lesson('A4', '- A4 seats=75 reports=72 missing=C1Meaning,ScribeReportNumbers'))
    add('F42', 'A3 first pointer numbers wrong (3443 for 3445)', 'reject',
        lambda: lesson('A3', '- A3 log_2e785632=3440,3441,3443 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a'))
    add('F43', 'A3 second pointer numbers wrong (3443 for 3444)', 'reject',
        lambda: lesson('A3', '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3443 unnamed=577a02a5,8847042a'))
    add('F44', 'A3 unnamed list names a hash that LOG.md does name', 'reject',
        lambda: lesson('A3', '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a,2e785632'))
    add('F45', 'LOG.md edited on line 1 (not append-only)', 'reject',
        lambda: sub1('LOG.md', '# kaidoku-shokunin — Iteration Log', '# kaidoku-shokunin — Iteration Log (edited)'))
    add('F46', 'A3 line removed entirely', 'reject', lambda: line_del(L49, '- A3 '))
    add('F47', 'A2 line removed entirely', 'reject', lambda: line_del(L49, '- A2 '))
    add('F48', 'S147 teaches opens "fixes S145" instead of "supersedes S145"', 'reject',
        lambda: row_sub('S147', 'supersedes S145 \u2014', 'fixes S145 \u2014'))
    add('F49', 'A8 round-49 included/excluded 1/1 (derived 2/0; screened still 2)', 'reject',
        lambda: line_sub('corpus/SOURCES.md', ROUND49_LINE, lambda l: l.replace('included 2, excluded 0', 'included 1, excluded 1')))
    add('F50', 'A4 reports stated 71 (derived 72)', 'reject',
        lambda: lesson('A4', '- A4 seats=75 reports=71 missing=C1Battery,C1Meaning,ScribeReportNumbers'))
    add('F51', 'non-.md file placed under the C1Meaning seat directory', 'accept',
        lambda: wr('.ufo/waves/round-48/w1/C1Meaning/notes.txt', 'notes\n'))
    add('F52', 'SCORECARD A9 line deleted (heading kept)', 'reject',
        lambda: line_del('SCORECARD.md', '- A9 verdict='))
    add('F53', 'S147 anchor heading names a different section', 'reject',
        lambda: row_sub('S147', '`2. Backdrop to Popper’s Thought`', '`3. The Problem of Demarcation`'))
    add('F54', 'A8 round-48 entry carries the late marker but its numbers are wrong (rows 144 -> 999)', 'reject',
        lambda: line_sub('corpus/SOURCES.md', '- 2026-10-28 round 48', lambda l: l.replace('rows 144 → 146', 'rows 144 → 999')))
    def f55():
        sx = rd('corpus/evidence/round-49/c2/sysexits.html')
        norm = SPEC_MOD.html_norm(sx)
        q2 = 'The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, bad syntax in a parameter, or whatever.'
        i = norm.index(q2)
        passage = ' '.join(norm[i:].split(' ')[:30])
        assert all(c not in passage for c in '"|`\x01\x02'), passage
        row_sub('S148', '"' + q2 + '"', '"' + passage + '"')
    add('F55', 'A7 S148 quotation lengthened to 30 words, present in the snapshot', 'reject', f55)
    add('F56', 'A7 S148 quotation marks removed (no quoted passage)', 'reject',
        lambda: row_sub('S148', '"The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, bad syntax in a parameter, or whatever."',
                        'The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, bad syntax in a parameter, or whatever.'))
    reset()
    return F


SPEC = importlib.util.spec_from_file_location('c2m', ORIG)
SPEC_MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SPEC_MOD)


def _html_norm(b):
    return SPEC_MOD.html_norm(b)


class _M:  # shim so f32 can call html_norm through the module spec
    html_norm = staticmethod(_html_norm)


def run(counter, rev, battery, tag):
    out = f'{S}/runs/{tag}.json'
    if os.path.exists(out):
        os.remove(out)
    cmd = ['python3', '-I', '-B', counter, '--root', CL, '--rev', rev, '--freeze', FREEZE, '--json-out', out]
    if battery:
        cmd.append('--battery')
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    try:
        d = json.load(open(out))
    except Exception:
        d = {'unparsed': True}
    b = d.get('battery') or {}
    return {
        'tag': tag, 'counter': os.path.basename(counter), 'rev': rev[:12], 'battery': battery,
        'exit': p.returncode, 'stdout_sha256': sha(p.stdout.encode()), 'json_sha256': sha(open(out, 'rb').read()) if os.path.exists(out) else None,
        'mismatches': d.get('mismatches'), 'reason': d.get('reason'),
        'red': sorted(k for k, v in (d.get('atoms') or {}).items() if not v['ok']),
        'battery_failing': b.get('failing'), 'do_nothing_red': b.get('do_nothing_red'),
        'mut_red': sorted(m['label'] + ' -> ' + ','.join(m['red']) for m in b.get('mutations', []) if not m['ok']),
        'stderr_tail': p.stderr[-200:], 'secs': round(time.time() - t0, 2),
    }


def sig(r):
    return (r['exit'], r['mismatches'], tuple(r['red']), r['reason'], tuple(r['battery_failing'] or []))


if __name__ == '__main__':
    F = build_forgeries()
    json.dump(F, open(f'{S}/forgeries.json', 'w'), indent=1, ensure_ascii=False)
    print('forgeries', len(F), file=sys.stderr)
    jobs = []
    for mid in MUT_FILES:
        jobs.append((mid, MUT_FILES[mid], GREEN, True, 'green-battery'))
        jobs.append((mid, MUT_FILES[mid], GREEN, False, 'green'))
        jobs.append((mid, MUT_FILES[mid], FREEZE, False, 'freeze'))
    fjobs = []
    for f in F:
        for mid in MUT_FILES:
            fjobs.append((mid, MUT_FILES[mid], f['rev'], False, 'F:' + f['id']))
        fjobs.append(('ORIG', ORIG, f['rev'], True, 'F:' + f['id'] + ':battery'))
    res = {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(run, c, rev, bat, '%s.%s' % (mid, tag)): (mid, tag) for mid, c, rev, bat, tag in jobs + fjobs}
        for fu in cf.as_completed(futs):
            mid, tag = futs[fu]
            res.setdefault(mid, {})[tag] = fu.result()
    json.dump(res, open(f'{S}/results-raw.json', 'w'), indent=1, sort_keys=True)
    print('done', len(res), file=sys.stderr)
