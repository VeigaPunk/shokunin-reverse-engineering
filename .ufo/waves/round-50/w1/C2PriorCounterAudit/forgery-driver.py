#!/usr/bin/env python3
"""Seat C2PriorCounterAudit: attack the frozen round-49 counters on clone commits (never the lane).

Each case = one commit on top of the base HEAD inside a `git clone --shared` scratch clone; the
counter (lane copy, sha256 == FREEZE blob) is run with --root <clone> --rev <case commit>.
Receipts: stdout/json sha256 per case, written to receipts/cases.jsonl.
"""
import hashlib, json, os, subprocess, sys, time

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = '7c678ae6d97aedb969fd253b52b3d2882ef1e186'
FREEZE = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
S = os.environ['S']
CLONE = os.path.join(S, 'clone')
OUT = os.path.join(LANE, '.ufo/waves/round-50/w1/C2PriorCounterAudit/receipts')
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'


def sh(args, cwd=None, check=True, inp=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, env=ENV, input=inp)
    if check and p.returncode != 0:
        raise SystemExit('FAILED %r: %s' % (args, p.stderr.decode(errors='replace')))
    return p


def git(*a, check=True):
    return sh(['git', '-C', CLONE] + list(a), check=check)


def show(path, rev=BASE):
    return sh(['git', '-C', LANE, 'show', '%s:%s' % (rev, path)]).stdout.decode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def assert_clone():
    top = git('rev-parse', '--show-toplevel').stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(CLONE), top


def reset_base():
    git('reset', '-q', '--hard', BASE)
    git('clean', '-qfd')


def commit(files, msg, removes=(), extra_cmds=()):
    """files: {path: str} written in clone (text); removes: paths deleted."""
    assert_clone()
    for p, t in files.items():
        full = os.path.join(CLONE, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(t if isinstance(t, bytes) else t.encode())
        git('add', '--', p)
    for p in removes:
        git('rm', '-q', '--', p)
    for c in extra_cmds:
        c()
    git('-c', 'user.name=c2audit', '-c', 'user.email=c2audit@shokunin.local', 'commit', '-q', '-m', msg)
    return git('rev-parse', 'HEAD').stdout.decode().strip()


def run_counter(counter, rev, label, extra=()):
    jout = os.path.join(S, 'json', label + '.json')
    os.makedirs(os.path.dirname(jout), exist_ok=True)
    t0 = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    cmd = ['python3', '-I', '-B', counter, '--root', CLONE, '--rev', rev, '--freeze', FREEZE,
           '--json-out', jout] + list(extra)
    if 'c1' in os.path.basename(counter):
        cmd += ['--pkg65', PKG65, '--work', os.path.join(S, 'w', label)]
    p = sh(cmd, check=False)
    res = {}
    try:
        res = json.load(open(jout))
    except Exception:
        pass
    red = []
    if 'atoms' in res:
        red = sorted(k for k, v in res['atoms'].items() if not v['ok'])
    return {
        'exit': p.returncode, 'stdout_sha256': sha(p.stdout), 'json_sha256': sha(open(jout, 'rb').read()) if os.path.exists(jout) else None,
        'reason': res.get('reason'), 'mismatches': res.get('mismatches'), 'red_atoms': red,
        'carriers_matched': res.get('carriers_matched'), 'failing': res.get('failing'),
        'utc': t0, 'cmd': ' '.join(os.path.basename(x) if i == 2 else x for i, x in enumerate(cmd))}


def sub1(text, old, new):
    assert text.count(old) >= 1, 'pattern not found: %r' % old[:70]
    return text.replace(old, new, 1)


def lines_edit(text, fn):
    ls = text.split('\n')
    fn(ls)
    return '\n'.join(ls)


C2 = os.path.join(LANE, 'tools/round-49/c2-mismatch.py')
C1 = os.path.join(LANE, 'tools/round-49/c1-counter.py')
LESSON = 'corpus/lessons/round-49.md'
SRC = 'corpus/SOURCES.md'
SC = 'SCORECARD.md'

cases = []
results = []


def case(cid, finding, desc, counter, mk, expect):
    reset_base()
    rev = mk() if mk else BASE
    r = run_counter(counter, rev, cid)
    r.update({'case': cid, 'finding': finding, 'desc': desc, 'rev': rev, 'expect_note': expect})
    results.append(r)
    print(cid, 'exit', r['exit'], 'mism', r['mismatches'], 'red', r['red_atoms'], 'reason', r['reason'], flush=True)


def edit_text(path, fn):
    t = show(path)
    return fn(t)


def mk_file_commit(path_edits, msg):
    def f():
        files = {}
        for p, fn in path_edits.items():
            files[p] = fn(show(p))
        return commit(files, msg)
    return f


# control
case('CTL-HEAD', '-', 'control: base HEAD, no commit', C2, None, 'exit 0 expected')

# A8 search log
def ins_after(tag_line_prefix, new_line):
    def fn(t):
        ls = t.split('\n')
        idx = [i for i, l in enumerate(ls) if l.startswith(tag_line_prefix)]
        assert len(idx) == 1, (tag_line_prefix, idx)
        ls.insert(idx[0] + 1, new_line)
        return '\n'.join(ls)
    return fn

R48_UNMARKED = ('- 2026-10-28 round 48 \u2014 Question: fixture (unmarked second round-48 entry). '
                'Identified 9, screened 9, included 9, excluded 0; rows 1 \u2192 9. Stop: fixture.')
case('A8-unmarked-r48', 'F1 (W2C2SearchLog) / M23 (W2C2Mutate)',
     'unmarked second round-48 entry after the late entry', C2,
     mk_file_commit({SRC: ins_after('- 2026-10-28 round 48 (late entry', R48_UNMARKED)}, 'fx A8 r48'), 'exit 0 (defect)')
R49_HYPHEN = ('- 2026-10-28 round-49 \u2014 Question: fixture (hyphen marker). Identified 9, screened 9, '
              'included 9, excluded 0; rows 146 \u2192 150. Stop: fixture.')
case('A8-hyphen-r49', 'M22 (W2C2Mutate)', 'second round-49 entry with `round-49` marker', C2,
     mk_file_commit({SRC: ins_after('- 2026-10-28 round 49 ', R49_HYPHEN)}, 'fx A8 hyphen'), 'exit 0 (defect)')
R49_DATE = ('- 2026-10-29 round 49 \u2014 Question: fixture (other date). Identified 9, screened 9, '
            'included 9, excluded 0; rows 146 \u2192 150. Stop: fixture.')
case('A8-date-r49', 'F4 (W2C2Rescore)', 'second round-49 entry dated 2026-10-29', C2,
     mk_file_commit({SRC: ins_after('- 2026-10-28 round 49 ', R49_DATE)}, 'fx A8 date'), 'exit 0 (defect)')

def dup_row_s149(t):
    ls = t.split('\n')
    idx = [i for i, l in enumerate(ls) if l.lstrip().startswith('| S149 ')]
    assert len(idx) == 1
    ls.insert(idx[0] + 1, ls[idx[0]])
    return '\n'.join(ls)
case('REG-dup-S149', 'F2 (W2C2SearchLog) / M17 (W2C2Mutate)', 'physically duplicated S149 row', C2,
     mk_file_commit({SRC: dup_row_s149}, 'fx dup S149'), 'exit 0 (defect); census E03 catches it')

def s149_pin(t):
    return sub1(t, 'sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf`',
                'sha256 `1fc793a398a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf`')
case('REG-S149-pin', 'F1 (W2C2Registry) / M16 (W2C2Mutate)', 'S149 anchor sha256 pin wrong (1 hex)', C2,
     mk_file_commit({SRC: s149_pin}, 'fx S149 pin'), 'exit 0 (defect: S149 read by no atom)')

def s147_quote_s3(t):
    old = '"falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific" (21 words)'
    new = '"In a word, an exception, far from \u201cproving\u201d a rule, conclusively refutes it." (13 words)'
    return sub1(t, old, new)
case('A6-locator-s3', 'Rescore F3 (W2C2Rescore)', 'S147 quote 1 replaced by a section-3 sentence, anchor parenthetical kept', C2,
     mk_file_commit({SRC: s147_quote_s3}, 'fx A6 locator'), 'exit 0 (defect: substring head test)')

def s148_teach_dup(t):
    return sub1(t, 'defines EX_USAGE is 64', 'defines EX_USAGE is 64; an older mirror has EX_USAGE  is 2')
case('A7-double-space', 'N06 (W2C2Forge) / F2', 'S148 teaches adds `EX_USAGE  is 2` (two spaces)', C2,
     mk_file_commit({SRC: s148_teach_dup}, 'fx A7 dbl'), 'exit 0 (defect)')

def s148_teach_was(t):
    return sub1(t, 'defines EX_USAGE is 64', 'defines EX_USAGE is 64; EX_USAGE was 2 in 1994')
case('A7-was', 'Rescore F1', 'S148 teaches adds `EX_USAGE was 2 in 1994`', C2,
     mk_file_commit({SRC: s148_teach_was}, 'fx A7 was'), 'exit 0 (defect)')

# A9 SCORECARD
def a9_comment(t):
    return lines_edit(t, lambda ls: (lambda i: (ls.insert(i + 1, '-->'), ls.insert(i, '<!--')))(
        [k for k, l in enumerate(ls) if l.startswith('- A9 verdict=rejected-harmed')][0]))
case('A9-html-comment', 'F5 (W2C2Scorecard)', 'A9 line wrapped in an HTML comment (visible line kept)', C2,
     mk_file_commit({SC: a9_comment}, 'fx A9 comment'), 'exit 0 (defect)')

def a9_fence(t):
    def fn(ls):
        i = [k for k, l in enumerate(ls) if l.startswith('- A9 verdict=rejected-harmed')][0]
        ls[i] = '```'
        ls.insert(i + 1, '- A9 verdict=rejected-harmed source=corpus/lessons/round-48-verifier-spotcheck.md calibration=harmed')
        ls.insert(i + 2, '```')
    return lines_edit(t, fn)
case('A9-code-fence', 'F5 (W2C2Scorecard)', 'A9 line inside a fenced code block, the visible line replaced by the fence', C2,
     mk_file_commit({SC: a9_fence}, 'fx A9 fence'), 'exit 0 (defect: rendered SCORECARD shows no A9)')

# lesson atoms
def a1_comment(t):
    def fn(ls):
        i = [k for k, l in enumerate(ls) if l.startswith('- A1 declared=')][0]
        ls.insert(i + 1, '-->')
        ls.insert(i, '<!--')
    return lines_edit(t, fn)
case('LESSON-A1-comment', 'new (not in W2 reports; plan: atoms in HTML comment do not count)', 'lesson A1 line inside a multi-line HTML comment', C2,
     mk_file_commit({LESSON: a1_comment}, 'fx A1 comment'), 'exit 0 (defect: lesson atoms are not comment/fence-aware)')

def hdr_b6f7(t):
    ls = t.split('\n')
    assert 'decc5697' in ls[3], ls[3]
    ls[3] = ls[3].replace('decc5697bfd4ec1e9de4a762ad199d9bd9c4230d', 'b6f7ca2a6391964dfdedd477cd560bd42159873a')
    return '\n'.join(ls)
case('LESSON49-header', 'M02 (W2C2Mutate) / F9 (W2C2Registry? no: W2C2Forge F9)', 'round-49 lesson `Declared freeze` header set to b6f7ca2a', C2,
     mk_file_commit({LESSON: hdr_b6f7}, 'fx r49 header'), 'exit 0 (defect: header outside every atom)')

def a3_dupkey(t):
    return sub1(t, 'log_2e785632=3440,3441,3445', 'log_2e785632=9999 log_2e785632=3440,3441,3445')
case('A3-dup-key', 'N01 (W2C2Forge) / F3', 'duplicate key on the A3 line, wrong value first, right value last', C2,
     mk_file_commit({LESSON: a3_dupkey}, 'fx A3 dup'), 'exit 0 (defect: last-wins; the wrong value is hidden)')

def a3_nonnum(t):
    return sub1(t, 'log_c093e798=3440,3441,3445', 'log_c093e798=3440,3441,3445,xyz')
case('A3-nonnumeric', 'F12 (W2C2Forge)', 'non-numeric token in the A3 set', C2,
     mk_file_commit({LESSON: a3_nonnum}, 'fx A3 xyz'), 'exit 0 (defect: isdigit drops it)')

def a4_dupkey(t):
    return sub1(t, 'seats=75 reports=72', 'seats=9 seats=75 reports=72')
case('A4-dup-key', 'N02 (W2C2Forge) / F3', 'duplicate `seats` key on the A4 line', C2,
     mk_file_commit({LESSON: a4_dupkey}, 'fx A4 dup'), 'exit 0 (defect)')

# S149 / A8 via re.search first-statement: restated line appended to round-49 entry
def a8_restated(t):
    ls = t.split('\n')
    i = [k for k, l in enumerate(ls) if l.startswith('- 2026-10-28 round 49 ')][0]
    ls[i] = ls[i] + ' Restated: identified 1, screened 1, included 1, excluded 0; rows 1 -> 2.'
    return '\n'.join(ls)
case('A8-restated', 'F4 (W2C2Forge)', 'a restated rows/identified statement appended to the round-49 entry', C2,
     mk_file_commit({SRC: a8_restated}, 'fx A8 restated'), 'exit 0 (defect: re.search first match; contradictory second statement invisible)')

# A8 identified asserted (disclosed) -- one run for the record
case('A8-identified', 'M21 (W2C2Mutate), disclosed', 'identified 3 -> 300 (plan limit)', C2,
     mk_file_commit({SRC: lambda t: sub1(t, 'Identified 3, screened 3', 'Identified 300, screened 3')}, 'fx ident'),
     'exit 0 (disclosed limit)')

# SCORECARD round-48 declared freeze at REV (A1 reads base) -- by design
def sc_r48(t):
    return sub1(t, 'Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873a`', 'Declared freeze:** `2e785632863f043a985f7953775b6aca191f1169`')
case('A1-REV-scorecard', 'Quality F4 / Mutate M26', 'round-48 SCORECARD declared freeze changed at REV (A1 reads base)', C2,
     mk_file_commit({SC: sc_r48}, 'fx A1 rev sc'), 'exit 0 (by design: immune)')

# ---------- merge shape over-refusal (C2 touched)
def merge_case():
    reset_base()
    git('checkout', '-q', '-b', 'side-fx')
    commit({'scratch-side.txt': 'side\n'}, 'fx side')
    git('checkout', '-q', '--detach', BASE)
    commit({'scratch-main.txt': 'main\n'}, 'fx main')
    git('-c', 'user.name=c2audit', '-c', 'user.email=c2audit@shokunin.local', 'merge', '--no-ff', '-q', '-m', 'fx merge', 'side-fx')
    return git('rev-parse', 'HEAD').stdout.decode().strip()
case('MERGE-plain-nonfrozen', 'W2C1Drift F4 (C2 touched, merge shape)', 'benign merge of a non-frozen side branch (no frozen path in either parent)', C2,
     merge_case, 'exit 2 frozen_path_changed = over-refusal (defect)')

# ---------- copies / quoted names (C1 and C2 walks)
def copy_commit():
    readme = show('corpus/README.md')
    return commit({'corpus/README.md': readme + '\n<!-- fx copy -->\n',
                   'tools/round-49/copied-from-readme.md': readme}, 'fx copy')
case('COPY-C2', 'W2C1Drift F2 (C2 side)', 'copy into tools/round-49 with diff.renames=copies', C2,
     lambda: (git('config', 'diff.renames', 'copies'), copy_commit())[1], 'exit 2 (fail closed)')
case('COPY-C1', 'W2C1Drift F2', 'same copy fixture, C1 walk', C1,
     lambda: (git('config', 'diff.renames', 'copies'), copy_commit())[1], 'exit 0 expected by F2 (fail-open)')
git('config', '--unset', 'diff.renames', check=False)

def quoted_commit():
    return commit({'tools/round-49/q"x.json': '{}\n'}, 'fx quoted')
case('QUOTED-C2', 'W2C1Drift F1 (C2 side)', 'added path with a quote char under tools/round-49', C2,
     quoted_commit, 'exit 2 (fail closed)')
case('QUOTED-C1', 'W2C1Drift F1', 'same fixture, C1 walk', C1,
     quoted_commit, 'exit 0 expected by F1 (fail-open)')

# C1 counter bytes unbound: comment-only edit run from a scratch copy
os.makedirs(os.path.join(S, 'cp'), exist_ok=True)
cp = os.path.join(S, 'cp', 'c1-counter-commentonly.py')
with open(C1, 'rb') as fh:
    src = fh.read()
with open(cp, 'wb') as fh:
    fh.write(src + b'\n# comment-only edit (audit probe)\n')
reset_base()
r = run_counter(cp, BASE, 'C1-OWN-BYTES')
r.update({'case': 'C1-OWN-BYTES', 'finding': 'W2C1Drift counter-bytes (C1)', 'desc': 'comment-only edit of c1-counter.py run from scratch copy, rev HEAD', 'rev': BASE, 'expect_note': 'exit 0 (defect: no own-bytes check)'})
results.append(r)
print('C1-OWN-BYTES exit', r['exit'], 'matched', r['carriers_matched'], flush=True)
r2 = run_counter(C2, BASE, 'C2-OWN-BYTES', extra=())
cp2 = os.path.join(S, 'cp', 'c2-mismatch-commentonly.py')
with open(C2, 'rb') as fh:
    s2 = fh.read()
with open(cp2, 'wb') as fh:
    fh.write(s2 + b'\n# comment-only edit (audit probe)\n')
r2 = run_counter(cp2, BASE, 'C2-OWN-BYTES')
r2.update({'case': 'C2-OWN-BYTES', 'finding': 'control', 'desc': 'comment-only edit of c2-mismatch.py', 'rev': BASE, 'expect_note': 'exit 2 counter_not_frozen'})
results.append(r2)
print('C2-OWN-BYTES exit', r2['exit'], r2['reason'], flush=True)

with open(os.path.join(OUT, 'cases.jsonl'), 'w') as fh:
    for r in results:
        fh.write(json.dumps(r, sort_keys=True) + '\n')
print('wrote', len(results), 'cases')
