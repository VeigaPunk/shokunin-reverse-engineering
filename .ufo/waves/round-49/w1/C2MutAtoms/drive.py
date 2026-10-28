#!/usr/bin/env python3
"""C2MutAtoms fixture-side mutation driver (seat C2MutAtoms, round 49 wave 1).

Every mutation is a commit made in the SCRATCH clone built by mkclone.sh + c2-after.py
(identity r49-dev, clone-only). Each mutated commit descends from DEV_AFTER (the GREEN fixture),
is scored by the DRAFT counter tools/round-49/c2-mismatch.py at that commit with --freeze
DEV_FREEZE, and the clone is then reset to DEV_AFTER. The lane tree is never written.

usage: drive.py <clone> <artifact-dir>
"""
import hashlib, json, os, re, subprocess, sys, datetime

C, ART = sys.argv[1], sys.argv[2]
AF = 'ea7e1ccca5f5af698ab0ff15b60836d7ac9d979c'   # DEV_AFTER (green fixture)
FZ = '7a202afa75d4a75d15892df2e5d1af7f16eddfb1'   # DEV_FREEZE
LES = 'corpus/lessons/round-49.md'
SC = 'SCORECARD.md'
REG = 'corpus/SOURCES.md'
POP = 'corpus/evidence/round-49/c2/popper.html'
SYS = 'corpus/evidence/round-49/c2/sysexits.html'
CLO = 'corpus/lessons/round-48-verifier-spotcheck.md'
RES = '.ufo/waves/round-48/r48-w1-results.json'
C2R = '.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json'
ATOMS = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
os.makedirs(ART, exist_ok=True)


def g(*a, text=False):
    p = subprocess.run(['git', '-C', C] + list(a), capture_output=True)
    if p.returncode != 0 and text:
        raise SystemExit('git failed: %r %s' % (a, p.stderr.decode()))
    return p.stdout.decode() if text else p.stdout


assert g('rev-parse', '--show-toplevel', text=True).strip() == C, 'toplevel mismatch'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def base(p):
    return g('show', '%s:%s' % (AF, p))


def rep(t, old, new, n=1):
    k = t.count(old)
    assert k == n, 'expected %d occurrence(s), found %d: %r' % (n, k, old[:70])
    return t.replace(old, new)


def edit_line(t, prefix, fn):
    lines = t.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, 'line prefix %r matches %d lines' % (prefix, len(idx))
    lines[idx[0]] = fn(lines[idx[0]])
    return '\n'.join(lines)


def dec(p):
    return base(p).decode('utf-8')


# ---------------------------------------------------------------- mutation definitions
# each: id, atom expected to flip (None for expected-green), description, builder(files) -> files
# files: dict path -> bytes (new content) or None (delete); builders read AF bytes via base()

def m_A1a():
    t = dec(SC)
    return {SC: rep(t, '**Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873a`',
                    '**Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873b`').encode()}


def m_A1b():
    t = dec(SC)
    les = dec(LES)
    return {SC: rep(t, '**Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873a`',
                    '**Declared freeze:** `61b87d742032e65fca9c38267d7d6ed7e555edad`').encode(),
            LES: rep(les, 'declared=b6f7ca2a6391964dfdedd477cd560bd42159873a',
                     'declared=61b87d742032e65fca9c38267d7d6ed7e555edad').encode()}


def m_A1c():
    les = dec(LES)
    lines = les.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith('- A1 ')]
    assert len(idx) == 1
    del lines[idx[0]]
    return {LES: '\n'.join(lines).encode()}


def m_A2a():
    les = dec(LES)
    return {LES: rep(les, 'dead=663f30ee7516942a0120e7de68fe88356e680822',
                     'dead=663f30ee7516942a0120e7de68fe88356e680823').encode()}


def m_A2b():
    les = dec(LES)
    return {LES: rep(les, 'actual=663f30ee751694fb0970e7de68fe88356e680822',
                     'actual=663f30ee751694fb0970e8de68fe88356e680822').encode()}


def m_A2c():
    les = dec(LES)
    return {LES: rep(rep(les, 'dead=663f30ee7516942a0120e7de68fe88356e680822',
                         'dead=663f30ee751694fb0970e7de68fe88356e680822'),
                     'actual=663f30ee751694fb0970e7de68fe88356e680822',
                     'actual=663f30ee7516942a0120e7de68fe88356e680822').encode()}


def m_A3a():
    les = dec(LES)
    return {LES: rep(les, ' log_33f65a91=3440,3441,3444', '').encode()}


def m_A3b():
    les = dec(LES)
    return {LES: rep(les, 'unnamed=577a02a5,8847042a', 'unnamed=8847042a').encode()}


def m_A3c():
    les = dec(LES)
    return {LES: rep(les, 'log_2e785632=3440,3441,3445', 'log_2e785632=3440,3441,3446').encode()}


def m_A4a():
    les = dec(LES)
    return {LES: rep(les, 'seats=75', 'seats=76').encode()}


def m_A4b():
    return {'.ufo/waves/round-48/w1/CritAssim.md': None}


def m_A4c():
    t = dec(RES)
    t = rep(t, '"name": "ScribeBlock",', '"name": "@@SWAP@@",')
    t = rep(t, '"name": "ScribeScore",', '"name": "ScribeBlock",')
    t = rep(t, '"name": "@@SWAP@@",', '"name": "ScribeScore",')
    return {RES: t.encode()}


def m_A5a():
    les = dec(LES)
    return {LES: rep(les, 'c2_raw=d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914',
                     'c2_raw=d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23915').encode()}


def m_A5b():
    les = dec(LES)
    return {LES: rep(les, ' report_c1=3cc2d72d', '').encode()}


def m_A5c():
    b = base(C2R)
    nb = rep(b.decode(), '"axes_atoms": 2,', '"axes_atoms": 3,').encode()
    les = dec(LES)
    stripped = nb[:-1] if nb.endswith(b'\n') else nb
    les = rep(les, 'c2_raw=d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914',
              'c2_raw=' + sha(nb))
    les = rep(les, 'c2_stripped=c30628ae7c439754f570476d570ed57db3361c1a3b5178ecb1c97f065c1e1ce8',
              'c2_stripped=' + sha(stripped))
    les = rep(les, 'report_c2=c30628ae', 'report_c2=' + sha(stripped)[:8])
    return {C2R: nb, LES: les.encode()}


def m_A6a():
    reg = dec(REG)
    old = ('"falsifiability as his criterion for demarcating science from non-science: if a theory '
           'is incompatible with possible empirical observations it is scientific" (21 words)')
    new = '"falsifiability as his criterion for demarcating science" (21 words)'
    return {REG: rep(reg, old, new).encode()}


def m_A6b():
    pop = base(POP) + b'<!-- r49 re-pin probe: unrelated trailing byte -->\n'
    reg = dec(REG)
    reg = edit_line(reg, '| S147 |', lambda l: rep(l, sha(base(POP)), sha(pop)))
    return {POP: pop, REG: reg.encode()}


def m_A6c():
    reg = dec(REG)
    reg = edit_line(reg, '| S147 |', lambda l: rep(l, '| mined | 2026-10-28 | 180d |',
                                                   '| mined | 2026-10-27 | 180d |'))
    return {REG: reg.encode()}


def m_A7a():
    reg = dec(REG)
    reg = edit_line(reg, '| S148 |', lambda l: rep(l, 'EX_USAGE is 64, not 2', 'EX_USAGE is 2, not 64'))
    return {REG: reg.encode()}


def m_A7b():
    reg = dec(REG)
    reg = edit_line(reg, '| S148 |', lambda l: rep(
        l, '"The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, '
           'bad syntax in a parameter, or whatever."',
        '"The command was used incorrectly, e.g., with the wrong number of arguments"'))
    return {REG: reg.encode()}


def m_A7c():
    sx = base(SYS)
    nsx, k = re.subn(rb'EX_USAGE(\s+)64', rb'EX_USAGE\g<1>65', sx)
    assert k == 1, 'EX_USAGE 64 occurrences: %d' % k
    reg = dec(REG)
    reg = edit_line(reg, '| S148 |', lambda l: rep(l, sha(sx), sha(nsx)))
    return {SYS: nsx, REG: reg.encode()}


def m_A8a():
    reg = dec(REG)
    reg = edit_line(reg, '- 2026-10-28 round 49 ', lambda l: rep(l, 'identified 2,', 'identified 3,'))
    return {REG: reg.encode()}


def m_A8b():
    reg = dec(REG)
    reg = edit_line(reg, '- 2026-10-28 round 48 ', lambda l: rep(
        l, 'included 1, excluded 1', 'included 0, excluded 2'))
    return {REG: reg.encode()}


def m_A8c():
    reg = dec(REG).split('\n')
    i48 = [i for i, l in enumerate(reg) if l.startswith('- 2026-10-28 round 48 ')]
    i49 = [i for i, l in enumerate(reg) if l.startswith('- 2026-10-28 round 49 ')]
    assert len(i48) == 1 and len(i49) == 1 and i49[0] == i48[0] + 1
    reg[i48[0]], reg[i49[0]] = reg[i49[0]], reg[i48[0]]
    return {REG: '\n'.join(reg).encode()}


def m_A9a():
    sc = dec(SC).split('\n')
    i = [k for k, l in enumerate(sc) if l.startswith('- A9 verdict=rejected-harmed')]
    assert len(i) == 1
    sc.insert(i[0] + 1, '- A9 verdict=accepted source=corpus/lessons/round-48-verifier-spotcheck.md '
                        'calibration=improved')
    return {SC: '\n'.join(sc).encode()}


def m_A9b():
    clo = dec(CLO)
    clo = rep(clo, 'Admission: **rejected-harmed**', 'Admission: **accepted**')
    clo = clo.rstrip('\n') + '\n\nEarlier draft verdict: rejected-harmed (superseded).\n'
    return {CLO: clo.encode()}


def m_A9c():
    sc = dec(SC).split('\n')
    i = [k for k, l in enumerate(sc) if l.startswith('- A9 verdict=rejected-harmed')]
    assert len(i) == 1
    line = sc.pop(i[0])
    j = sc.index('## Record corrections \u2014 round 49')
    sc.insert(j, line)
    return {SC: '\n'.join(sc).encode()}


# extras beyond the 27 (reorder/shadow variants of the same atoms)
def x_shadow_row():
    reg = dec(REG).split('\n')
    i = [k for k, l in enumerate(reg) if l.startswith('| S148 |')]
    assert len(i) == 1
    bogus = reg[i[0]].replace('EX_USAGE is 64, not 2', 'EX_USAGE is 2, not 64')
    reg.insert(i[0], bogus)
    return {REG: '\n'.join(reg).encode()}


def x_dup_section():
    les = dec(LES).rstrip('\n') + '\n\n## Corrections to round 48\n\n' \
        '- A1 declared=61b87d742032e65fca9c38267d7d6ed7e555edad stale=0f06251bf6a3a6964c715f67243d4df12e854258\n'
    return {LES: les.encode()}


MUTS = [
    ('M01', 'A1', 'SCORECARD declared freeze last hex digit a->b (lesson A1 unchanged)', m_A1a),
    ('M02', None, 'coordinated re-pin: SCORECARD declared + lesson A1 declared -> R48 base commit 61b87d74', m_A1b),
    ('M03', 'A1', 'delete lesson A1 correction line', m_A1c),
    ('M04', None, 'A2 dead hash last hex digit 2->3 (not a commit, lesson only)', m_A2a),
    ('M05', 'A2', 'A2 actual hash digit 9e->8e (8-hex prefix kept, not a commit)', m_A2b),
    ('M06', 'A2', 'swap dead/actual values (dead becomes the real commit)', m_A2c),
    ('M07', None, 'delete pointer log_33f65a91 from A3 line', m_A3a),
    ('M08', None, 'drop 577a02a5 from A3 unnamed list', m_A3b),
    ('M09', 'A3', 'A3 pointer log_2e785632 line 3445 -> 3446', m_A3c),
    ('M10', 'A4', 'A4 seats 75 -> 76', m_A4a),
    ('M11', 'A4', 'delete committed round-48 report artifact w1/CritAssim.md', m_A4b),
    ('M12', None, 'swap seat names of results entries 49 (ScribeBlock) and 52 (ScribeScore)', m_A4c),
    ('M13', 'A5', 'A5 c2_raw last hex digit 4->5 (lesson only)', m_A5a),
    ('M14', 'A5', 'delete report_c1 pointer from A5 line', m_A5b),
    ('M15', None, 'coordinated re-pin: round-48 c2 receipt edited (axes_atoms 2->3) + A5 c2 digests', m_A5c),
    ('M16', None, 'truncate S147 quote in anchor cell; "(21 words)" left unchanged', m_A6a),
    ('M17', None, 'snapshot popper.html gets an unrelated trailing byte; S147 anchor re-pinned', m_A6b),
    ('M18', 'A6', 'S147 opened date 2026-10-28 -> 2026-10-27', m_A6c),
    ('M19', None, 'S148 teaches: "EX_USAGE is 64, not 2" -> "EX_USAGE is 2, not 64" (swap)', m_A7a),
    ('M20', None, 'truncate S148 quote in anchor cell; "(22 words)" left unchanged', m_A7b),
    ('M21', 'A7', 'snapshot sysexits.html EX_USAGE 64 -> 65; S148 anchor re-pinned', m_A7c),
    ('M22', None, 'round-49 search-log entry identified 2 -> 3', m_A8a),
    ('M23', 'A8', 'round-48 search-log entry included 1/excluded 1 -> 0/2', m_A8b),
    ('M24', None, 'swap the round-48 and round-49 search-log entry lines (order only)', m_A8c),
    ('M25', None, 'append a second, contradictory A9 line (calibration=improved) after the real one', m_A9a),
    ('M26', None, 'closure verdict Admission flipped to accepted; token kept in a prose aside', m_A9b),
    ('M27', 'A9', 'move the A9 line under the round-48 corrections heading', m_A9c),
    ('X01', None, 'EXTRA shadow: duplicate S148 row (bogus teaches) inserted before the real row', x_shadow_row),
    ('X02', None, 'EXTRA section: second "## Corrections to round 48" appended with a false A1 line', x_dup_section),
]


def apply(files):
    for p, b in files.items():
        full = os.path.join(C, p)
        if b is None:
            if os.path.exists(full):
                os.remove(full)
        else:
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'wb').write(b)


def reset():
    g('checkout', '-q', '-f', '--detach', AF)
    g('clean', '-fdq')


def score(rev):
    jout = os.path.join(ART, 'json', '%s.json' % rev[:12])
    os.makedirs(os.path.dirname(jout), exist_ok=True)
    p = subprocess.run(['python3', '-I', '-B', os.path.join(C, 'tools/round-49/c2-mismatch.py'),
                        '--root', C, '--rev', rev, '--freeze', FZ, '--json-out', jout],
                       capture_output=True, cwd=os.environ.get('TMPDIR', C))
    out = p.stdout
    d = json.loads(out) if out.strip() else {}
    red = sorted(k for k, v in d.get('atoms', {}).items() if not v['ok'])
    return p.returncode, sha(out), d, red, out


reset()
assert g('rev-parse', 'HEAD', text=True).strip() == AF
rows, summary = [], []
for mid, want, desc, fn in MUTS:
    reset()
    files = fn()
    apply(files)
    g('add', '-A')
    changed = g('diff', '--cached', '--name-only', text=True).split()
    assert changed, 'no-op mutation %s' % mid
    assert set(changed) == set(k for k in files), 'unexpected path set %s vs %s' % (changed, list(files))
    g('-c', 'user.name=r49-dev', '-c', 'user.email=r49@dev.invalid', 'commit', '-q', '-m', 'mut ' + mid)
    rev = g('rev-parse', 'HEAD', text=True).strip()
    diff = g('diff', AF, rev)
    os.makedirs(os.path.join(ART, 'diffs'), exist_ok=True)
    open(os.path.join(ART, 'diffs', mid + '.diff'), 'wb').write(diff)
    t0 = utc()
    code, osha, d, red, _ = score(rev)
    if not red and code == 0:
        verdict = 'GREEN (undetected)'
    elif red == ([want] if want else []):
        verdict = 'red (own atom only)'
    elif red:
        verdict = 'red (cross-atom %s)' % red
    else:
        verdict = 'exit %d (not counted)' % code
    row = dict(id=mid, expect_atom=want, desc=desc, mut_commit=rev, exit=code,
               stdout_sha256=osha, mismatches=d.get('mismatches'), red=red, verdict=verdict,
               changed_paths=changed, diff_sha256=sha(diff), diff_bytes=len(diff),
               utc=t0, counter_sha256=d.get('counter_sha256'))
    rows.append(row)
    print('%s exit=%s mismatches=%s red=%s verdict=%s' % (mid, code, d.get('mismatches'), red, verdict),
          flush=True)

# restore and re-score the green fixture as a control
reset()
code, osha, d, red, _ = score(AF)
ctl = dict(id='CTL-green', exit=code, stdout_sha256=osha, mismatches=d.get('mismatches'), red=red)
print('CTL-green exit=%s mismatches=%s' % (code, d.get('mismatches')))
json.dump({'rows': rows, 'control': ctl, 'fixture_green': AF, 'freeze': FZ},
          open(os.path.join(ART, 'results.json'), 'w'), indent=1, sort_keys=True)
with open(os.path.join(ART, 'results.tsv'), 'w') as fh:
    fh.write('id\texpect\texit\tmismatches\tred\tverdict\tmut_commit\tdiff_sha256\tchanged_paths\tdesc\n')
    for r in rows:
        fh.write('\t'.join(map(str, [r['id'], r['expect_atom'] or '-', r['exit'], r['mismatches'],
                                     ','.join(r['red']) or '-', r['verdict'], r['mut_commit'],
                                     r['diff_sha256'], ','.join(r['changed_paths']), r['desc']])) + '\n')
