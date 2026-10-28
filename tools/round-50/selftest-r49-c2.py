#!/usr/bin/env python3
"""Hermetic self-test for the frozen round-49 C2 counter `tools/round-49/c2-mismatch.py`.

The counter has no `--selftest` of its own (argparse rejects it, exit 2) and stays byte-frozen;
this script is the self-test the round-48/49 closures asked for, kept beside the round-50 tools.

What it does
  1. Makes one fixture repo `WORK/clone` = `git clone --shared LANE`, detached at BASE (the lane
     commit that carries the genuine round-49 record, `7c678ae6...`). Git identity is set in
     that clone only; every git call names `-C WORK/clone`; the clone's toplevel is asserted
     equal to its path before the first commit. The lane is read (object store only), never
     written. Environment for every child: GIT_CONFIG_GLOBAL/SYSTEM=/dev/null, HOME=WORK/home,
     TMPDIR=WORK, PYTHONDONTWRITEBYTECODE=1 (and the counter runs `python3 -I -B`).
  2. For each case in this file, checks out BASE, applies ONE defect to committed record bytes
     (each edit asserts its pattern matched, so a case can never be a silent no-op), commits it
     (the green case commits nothing: REV is BASE), and runs the counter at that REV with
     FREEZE = decc5697 (the round-49 freeze).
  3. Compares exit code, red-atom set, `reason`, and a few structural facts against the EXPECTED
     FILE `selftest-r49-c2.expected.json` (hand-written, committed beside this script, never
     computed from a counter run). A counter run that disagrees is a failed case.
  3b. A case may also pin a fragment of the red atom's `why` text (`why_contains`), so a defect
     is caught by the clause that should catch it, not by a sibling clause of the same atom.
  4. Checks the expected file and the case list name the same ids (an unchecked case or an
     orphan expectation is itself a failure), and that the counter's sha256 equals the pin.

Cases (see the expected file for the per-case contract)
  green and green+battery; single-defect reds A1..A9 (several variants on A3/A5/A6/A7/A8);
  the contradiction-at-the-freeze control (REV == FREEZE: all nine red); counter-bytes mismatch
  (a one-line-appended copy of the counter, exit 2 `counter_not_frozen`); frozen path touched
  (edited file, added file, edited plan: exit 2 `frozen_path_changed`); freeze not an ancestor;
  unresolvable rev; CLI refusals (no args; `--selftest` is not an option; unwritable
  `--json-out`); and two KNOWN-BLIND cases (the A9 line hidden in an HTML comment / a code
  fence is still counted: exit 0). Known-blind cases pin the counter's CURRENT behaviour; they
  are not claims that the behaviour is right.

Exit: 0 every case matches its expectation; 1 at least one case differs (or the expected-file /
case-list sets disagree); 2 could not evaluate (clone/base/freeze unavailable, counter bytes
differ from the pin, bad arguments, work dir inside the lane). Writes only under --work (default:
a fresh directory under $TMPDIR), removed at the end unless --keep; --json-out writes one receipt
file, which must not be inside the lane.

Usage:
  selftest-r49-c2.py [--lane LANE] [--work DIR] [--expected PATH] [--counter PATH]
                     [--mutant-counter PATH] [--only ID[,ID...]] [--keep] [--json-out PATH] [--list]

--mutant-counter is the self-test's own discrimination check: the counter file at PATH replaces
the frozen one (its blob is grafted into synthetic FREEZE/BASE commits in the fixture clone only,
so it passes its own counter_not_frozen guard) and the same expected file is applied. Exit 1 =
the self-test caught the mutant; exit 0 = it did NOT (the mutant is invisible to these cases).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

LANE_DEFAULT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTED_DEFAULT = os.path.join(HERE, 'selftest-r49-c2.expected.json')
COUNTER_REL = 'tools/round-49/c2-mismatch.py'
LESSON = 'corpus/lessons/round-49.md'
SOURCES = 'corpus/SOURCES.md'
SCORECARD = 'SCORECARD.md'
POP = 'corpus/evidence/round-49/c2/popper.html'
SYS = 'corpus/evidence/round-49/c2/sysexits.html'
L48 = 'corpus/lessons/round-48.md'
ATOMS = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']


class Unevaluable(Exception):
    pass


# ----------------------------------------------------------------------------- fixtures


class Fx:
    """One fixture clone. All mutations go through here."""

    def __init__(self, work, lane, base, freeze):
        self.work, self.lane, self.base, self.freeze = work, lane, base, freeze
        self.dir = os.path.join(work, 'clone')
        self.env = dict(os.environ)
        for k in list(self.env):
            if k.startswith('GIT_'):
                del self.env[k]
        home = os.path.join(work, 'home')
        os.makedirs(home, exist_ok=True)
        self.env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null',
                        GIT_CONFIG_NOSYSTEM='1', HOME=home, TMPDIR=work,
                        PYTHONDONTWRITEBYTECODE='1', LC_ALL='C.UTF-8')

    def git(self, *a, check=True, inp=None):
        p = subprocess.run(['git', '-C', self.dir] + list(a), capture_output=True, env=self.env,
                           input=inp)
        if check and p.returncode != 0:
            raise Unevaluable('git %s failed: %s' % (' '.join(a), p.stderr.decode()[:300]))
        return p

    def make(self):
        p = subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', self.lane, self.dir],
                           capture_output=True, env=self.env)
        if p.returncode != 0:
            raise Unevaluable('clone failed: ' + p.stderr.decode()[:300])
        top = self.git('rev-parse', '--show-toplevel').stdout.decode().strip()
        if os.path.realpath(top) != os.path.realpath(self.dir):
            raise Unevaluable('fixture toplevel %s != %s' % (top, self.dir))
        self.git('config', 'user.name', 'r50-selftest')
        self.git('config', 'user.email', 'r50-selftest@fixture.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', '/dev/null')
        for rev in (self.base, self.freeze):
            if self.git('cat-file', '-e', rev + '^{commit}', check=False).returncode != 0:
                raise Unevaluable('commit %s not in the lane' % rev)
        if self.git('merge-base', '--is-ancestor', self.freeze, self.base, check=False).returncode:
            raise Unevaluable('FREEZE is not an ancestor of BASE')
        self.reset()

    def graft_counter(self, mutant_bytes):
        """Mutation mode: rebuild FREEZE and BASE (plumbing only, in the clone) with the counter blob
        replaced by `mutant_bytes`, so the mutant passes its own counter_not_frozen guard and the
        selftest can be asked whether it notices a behaviourally different counter."""
        blob = self.git('hash-object', '-w', '--stdin', inp=mutant_bytes).stdout.decode().strip()
        idx = os.path.join(self.work, 'graft.idx')
        genv = dict(self.env, GIT_INDEX_FILE=idx)
        out = {}
        parent = None
        for label, rev in (('freeze', self.freeze), ('base', self.base)):
            if os.path.exists(idx):
                os.remove(idx)
            for args in (['read-tree', rev],
                         ['update-index', '--add', '--cacheinfo', '100644,%s,%s' % (blob, COUNTER_REL)]):
                p = subprocess.run(['git', '-C', self.dir] + args, capture_output=True, env=genv)
                if p.returncode:
                    raise Unevaluable('graft %s failed: %s' % (args[0], p.stderr.decode()[:200]))
            tree = subprocess.run(['git', '-C', self.dir, 'write-tree'], capture_output=True,
                                  env=genv).stdout.decode().strip()
            ctenv = dict(self.env, GIT_AUTHOR_NAME='r50', GIT_AUTHOR_EMAIL='r50@fixture.invalid',
                         GIT_COMMITTER_NAME='r50', GIT_COMMITTER_EMAIL='r50@fixture.invalid',
                         GIT_AUTHOR_DATE='2026-10-28T00:00:00Z', GIT_COMMITTER_DATE='2026-10-28T00:00:00Z')
            p = subprocess.run(['git', '-C', self.dir, 'commit-tree', tree, '-p', parent or rev, '-m',
                                'mutant ' + label], capture_output=True, env=ctenv)
            if p.returncode:
                raise Unevaluable('commit-tree failed: ' + p.stderr.decode()[:200])
            parent = out[label] = p.stdout.decode().strip()
        os.remove(idx)
        self.freeze, self.base = out['freeze'], out['base']
        self.reset()

    def reset(self):
        self.git('checkout', '-q', '--detach', '-f', self.base)
        self.git('clean', '-fdxq')

    def path(self, rel):
        return os.path.join(self.dir, rel)

    def read(self, rel):
        with open(self.path(rel), 'rb') as f:
            return f.read()

    def write(self, rel, data):
        os.makedirs(os.path.dirname(self.path(rel)), exist_ok=True)
        with open(self.path(rel), 'wb') as f:
            f.write(data)

    def sub(self, rel, pat, repl, count=1, flags=0):
        """Regex-substitute in committed text; the pattern must match (never a silent no-op)."""
        t = self.read(rel).decode('utf-8')
        n = len(re.findall(pat, t, flags))
        if n < 1:
            raise Unevaluable('fixture edit matched nothing: %s in %s' % (pat[:60], rel))
        new = re.sub(pat, repl, t, count=count, flags=flags)
        if new == t:
            raise Unevaluable('fixture edit changed nothing: %s in %s' % (pat[:60], rel))
        self.write(rel, new.encode('utf-8'))

    def bsub(self, rel, old, new):
        b = self.read(rel)
        if old not in b:
            raise Unevaluable('fixture byte edit matched nothing: %r in %s' % (old, rel))
        self.write(rel, b.replace(old, new))

    def commit(self, msg):
        top = self.git('rev-parse', '--show-toplevel').stdout.decode().strip()
        if os.path.realpath(top) != os.path.realpath(self.dir):
            raise Unevaluable('refusing to commit: toplevel %s' % top)
        self.git('add', '-A')
        if not self.git('diff', '--cached', '--name-only').stdout.strip():
            raise Unevaluable('fixture produced an empty commit (no-op defect)')
        self.git('commit', '-q', '-m', msg)
        return self.git('rev-parse', 'HEAD').stdout.decode().strip()

    def head(self):
        return self.git('rev-parse', 'HEAD').stdout.decode().strip()


def swap_a1(m):
    return '- A1 declared=%s stale=%s' % (m.group(2), m.group(1))


# every builder edits the checked-out BASE worktree; returning is enough
def b_green(fx):
    pass


def b_a1(fx):
    fx.sub(LESSON, r'- A1 declared=([0-9a-f]{40}) stale=([0-9a-f]{40})', swap_a1)


def b_a1_rewrite(fx):  # a correction is a new entry, never a rewrite of the round-48 lesson
    fx.write(L48, fx.read(L48) + b'\n')


def b_a1_stale(fx):  # only `stale` wrong, and wrong by naming a real commit
    fx.sub(LESSON, r'(- A1 declared=[0-9a-f]{40} stale=)[0-9a-f]{40}', r'\g<1>decc5697bfd4ec1e9de4a762ad199d9bd9c4230d')


def b_a2(fx):  # the "real" commit replaced by a same-prefix non-commit
    fx.sub(LESSON, r'(- A2 dead=[0-9a-f]{40} actual=[0-9a-f]{8})[0-9a-f]{32}', r'\g<1>' + '0' * 32)


def b_a2_dead(fx):  # the "dead" hash replaced by the real commit: it now resolves to a commit
    fx.sub(LESSON, r'- A2 dead=[0-9a-f]{40} actual=([0-9a-f]{40})', r'- A2 dead=\1 actual=\1')


def b_a3_num(fx):
    fx.sub(LESSON, r'log_33f65a91=3440', 'log_33f65a91=3439')


def b_a3_key(fx):
    fx.sub(LESSON, r' unnamed=577a02a5,8847042a,7fe11332', ' unnamed=577a02a5,8847042a')


def b_a3_dup(fx):
    t = fx.read(LESSON).decode()
    m = re.search(r'^- A3 .*$', t, re.M)
    fx.write(LESSON, (t.rstrip('\n') + '\n' + m.group(0) + '\n').encode())


def b_a3_extra(fx):  # a fourth log_ key
    fx.sub(LESSON, r'(- A3 .*)$', r'\1 log_577a02a5=1', flags=re.M)


def b_a3_log(fx):  # LOG.md at REV no longer begins with the base blob
    fx.write('LOG.md', b'x' + fx.read('LOG.md'))


def b_a4(fx):
    fx.sub(LESSON, r'seats=75', 'seats=74')


def b_a5_zero(fx):
    fx.sub(LESSON, r'c2_stripped=[0-9a-f]{64}', 'c2_stripped=' + '0' * 64)


def b_a5_rawprefix(fx):  # report_c1 quotes the raw digest prefix instead of the stripped one
    t = fx.read(LESSON).decode()
    raw = re.search(r'c1_raw=([0-9a-f]{64})', t).group(1)
    fx.sub(LESSON, r'report_c1=[0-9a-f]{8}', 'report_c1=' + raw[:8])


def b_a6_count(fx):
    fx.sub(SOURCES, r'\(21 words\)', '(7 words)')


def b_a6_snap(fx):
    fx.bsub(POP, b'empirical', b'empirica1')


def b_a6_anchor(fx):
    fx.sub(SOURCES, r'`2\. Backdrop to Popper', '`3. The Problem of Demarcation; Popper')


def b_a7_teaches(fx):
    fx.sub(SOURCES, r'EX_USAGE is 64', 'EX_USAGE is 2')


def b_a7_snap(fx):
    fx.bsub(SYS, b'EX_USAGE', b'EX_USAGF')


def b_a7_repin(fx):  # snapshot loses `EX_USAGE 64`, and the row's sha256 pin is updated to match
    old = sha(fx.read(SYS))
    fx.bsub(SYS, b'#define EX_USAGE        64', b'#define EX_USAGE        65')
    fx.sub(SOURCES, old, sha(fx.read(SYS)))


def b_battery_incomplete(fx):  # green record, but one battery mutation has nothing to bite on
    fx.sub(SOURCES, r'`2\. Backdrop to Popper\u2019s Thought`', '2. Backdrop to Popper\u2019s Thought')


def b_a8_late(fx):
    fx.sub(SOURCES, r'late entry', 'last entry')


def b_a8_rows(fx):
    fx.sub(SOURCES, r'(- 2026-10-28 round 49 .*?rows 146 \u2192 )149', r'\g<1>150', flags=re.S)


def b_a8_dup(fx):
    t = fx.read(SOURCES).decode()
    ln = next(l for l in t.split('\n') if l.startswith('- 2026-10-28 round 49 '))
    fx.write(SOURCES, t.replace(ln, ln + '\n' + ln, 1).encode())


def b_a9_value(fx):
    fx.sub(SCORECARD, r'^(- A9 .*)calibration=harmed$', r'\1calibration=improved', flags=re.M)


def b_a9_second(fx):
    t = fx.read(SCORECARD).decode()
    fx.write(SCORECARD, (t.rstrip('\n') + '\n- A9 verdict=admitted source=x calibration=improved\n').encode())


def _wrap_a9(fx, open_, close):
    t = fx.read(SCORECARD).decode()
    m = re.search(r'^- A9 .*$', t, re.M)
    fx.write(SCORECARD, t.replace(m.group(0), open_ + '\n' + m.group(0) + '\n' + close, 1).encode())


def b_a9_comment(fx):  # the only A9 line lives inside an HTML comment
    _wrap_a9(fx, '<!--', '-->')


def b_a9_fence(fx):  # the only A9 line lives inside a fenced code block
    _wrap_a9(fx, '```', '```')


def b_frozen_edit(fx):
    fx.write('tools/round-49/c1-run.sh', fx.read('tools/round-49/c1-run.sh') + b'\n# edited after freeze\n')


def b_frozen_add(fx):
    fx.write('tools/round-49/late-addition.json', b'{}\n')


def b_frozen_plan(fx):
    fx.write('plans/round-49-claims.md', fx.read('plans/round-49-claims.md') + b'\nAmended after freeze.\n')


# case table: id -> (description, builder, how to run)
#   run kinds: rev=<'HEAD'|'base'|'freeze'>, freeze=<'freeze'|'base'|..>, battery bool,
#   counter=<'real'|'tampered'>, plus special `cli` cases
CASES = [
    ('green', 'genuine round-49 record at BASE', b_green, {}),
    ('green-battery', 'genuine record, --battery (16 mutations + do-nothing)', b_green, {'battery': True, 'jsonout': True}),
    ('a1-swap', 'A1 declared/stale hashes swapped', b_a1, {}),
    ('a1-rewrite-r48', 'A1 round-48 lesson rewritten (byte appended)', b_a1_rewrite, {}),
    ('a1-stale-only', 'A1 stale names a different real commit, declared untouched', b_a1_stale, {}),
    ('a2-noncommit', 'A2 real hash replaced by a same-prefix non-commit', b_a2, {}),
    ('a2-dead-resolves', 'A2 dead hash replaced by the real commit (resolves to a commit)', b_a2_dead, {}),
    ('a3-linenum', 'A3 one pointer line number moved', b_a3_num, {}),
    ('a3-unnamed', 'A3 one unnamed hash dropped', b_a3_key, {}),
    ('a3-extra-key', 'A3 fourth log_ key added', b_a3_extra, {}),
    ('a3-log-rewritten', 'A3 LOG.md at REV not append-only', b_a3_log, {}),
    ('a3-dup', 'A3 line duplicated', b_a3_dup, {}),
    ('a4-seats', 'A4 seats count off by one', b_a4, {}),
    ('a5-zero', 'A5 c2_stripped digest zeroed', b_a5_zero, {}),
    ('a5-rawprefix', 'A5 report_c1 quotes the raw digest prefix', b_a5_rawprefix, {}),
    ('a6-count', 'A6 S147 stated word count wrong', b_a6_count, {}),
    ('a6-snapshot', 'A6 popper snapshot bytes edited (pin and quote)', b_a6_snap, {}),
    ('a6-anchor', 'A6 S147 anchor names the wrong section', b_a6_anchor, {}),
    ('a7-teaches', 'A7 S148 teaches states EX_USAGE is 2', b_a7_teaches, {}),
    ('a7-snapshot', 'A7 sysexits snapshot bytes edited', b_a7_snap, {}),
    ('a7-repinned', 'A7 snapshot loses EX_USAGE 64 with its pin updated', b_a7_repin, {}),
    ('a8-late', 'A8 round-48 entry loses `late entry`', b_a8_late, {}),
    ('a8-rows', 'A8 round-49 entry rows A wrong', b_a8_rows, {}),
    ('a8-dup', 'A8 round-49 entry duplicated', b_a8_dup, {}),
    ('a9-value', 'A9 calibration= value flipped', b_a9_value, {}),
    ('a9-second', 'A9 contradictory second line appended', b_a9_second, {}),
    ('a9-battery', 'A9 defect run with --battery: genuine REV not green', b_a9_value, {'battery': True}),
    ('battery-incomplete', 'green record but a battery mutation is inapplicable: --battery exit 1', b_battery_incomplete, {'battery': True}),
    ('freeze-is-rev', 'do-nothing control: REV == FREEZE', b_green, {'rev': 'freeze'}),
    ('x-counter-bytes', 'counter copy with one appended line: counter_not_frozen', b_green, {'counter': 'tampered'}),
    ('x-frozen-edit', 'tools/round-49/c1-run.sh edited after the freeze', b_frozen_edit, {}),
    ('x-frozen-add', 'file added under tools/round-49 after the freeze', b_frozen_add, {}),
    ('x-frozen-plan', 'plans/round-49-claims.md edited after the freeze', b_frozen_plan, {}),
    ('x-freeze-not-ancestor', 'FREEZE passed as REV and BASE as FREEZE', b_green, {'rev': 'freeze', 'freeze': 'base'}),
    ('x-bad-rev', 'unresolvable --rev', b_green, {'rev': 'deadbeef' * 5}),
    ('cli-noargs', 'no arguments: argparse refusal', b_green, {'cli': []}),
    ('cli-selftest-flag', '--selftest is not an option of the frozen counter', b_green, {'cli': ['--root', '.', '--rev', 'HEAD', '--freeze', 'HEAD', '--selftest']}),
    ('cli-jsonout-missing-dir', '--json-out into a missing directory: uncaught OSError', b_green, {'jsonout': 'missing'}),
    ('blind-a9-comment', 'KNOWN BLIND: only A9 line inside an HTML comment still counts', b_a9_comment, {}),
    ('blind-a9-fence', 'KNOWN BLIND: only A9 line inside a code fence still counts', b_a9_fence, {}),
]


# ----------------------------------------------------------------------------- running


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_case(fx, cid, desc, builder, opt, counter, tampered, freeze_h, base_h):
    fx.reset()
    builder(fx)
    rev_h = fx.commit('fixture: ' + cid) if fx.git('status', '--porcelain').stdout.strip() else fx.head()
    rev = {'freeze': freeze_h}.get(opt.get('rev'), opt.get('rev')) or rev_h
    fr = {'base': base_h}.get(opt.get('freeze'), opt.get('freeze')) or freeze_h
    cmd = [sys.executable, '-I', '-B', tampered if opt.get('counter') == 'tampered' else counter]
    jpath = None
    if 'cli' in opt:
        cmd += opt['cli']
    else:
        cmd += ['--root', fx.dir, '--rev', rev, '--freeze', fr]
        if opt.get('battery'):
            cmd.append('--battery')
        if opt.get('jsonout') == 'missing':
            cmd += ['--json-out', os.path.join(fx.work, 'no-such-dir', 'x.json')]
        elif opt.get('jsonout'):
            jpath = os.path.join(fx.work, 'out-%s.json' % cid)
            cmd += ['--json-out', jpath]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, env=fx.env, cwd=fx.work)
    dt = time.time() - t0
    res = {'id': cid, 'desc': desc, 'rc': p.returncode, 'sec': round(dt, 3),
           'stdout_sha256': sha(p.stdout), 'rev': rev_h, 'json': None, 'red': None,
           'reason': None, 'json_out_equals_stdout': None}
    try:
        j = json.loads(p.stdout.decode())
        res['json'] = j
        res['red'] = sorted(k for k, v in (j.get('atoms') or {}).items() if not v['ok'])
        res['reason'] = j.get('reason')
        if jpath:
            with open(jpath, 'rb') as f:
                res['json_out_equals_stdout'] = f.read() == p.stdout
    except ValueError:
        res['stderr_tail'] = p.stderr.decode('utf-8', 'replace').strip().splitlines()[-1:]
    return res


def judge(res, exp):
    """Return a list of disagreements between a run and its expectation."""
    bad = []
    if res['rc'] != exp['exit']:
        bad.append('exit %s, expected %s' % (res['rc'], exp['exit']))
    j = res['json']
    if 'red' in exp:
        if res['red'] != sorted(exp['red']):
            bad.append('red %s, expected %s' % (res['red'], sorted(exp['red'])))
    if 'reason' in exp:
        if exp['reason'] is None:
            if res['reason'] is not None:
                bad.append('reason %r, expected none' % res['reason'])
        elif not (res['reason'] or '').startswith(exp['reason']):
            bad.append('reason %r, expected prefix %r' % (res['reason'], exp['reason']))
    if 'mismatches' in exp and (j or {}).get('mismatches') != exp['mismatches']:
        bad.append('mismatches %s, expected %s' % ((j or {}).get('mismatches'), exp['mismatches']))
    if 'atoms_total' in exp and (j or {}).get('atoms_total') != exp['atoms_total']:
        bad.append('atoms_total %s, expected %s' % ((j or {}).get('atoms_total'), exp['atoms_total']))
    if 'stdout_json' in exp and (j is not None) != exp['stdout_json']:
        bad.append('stdout is %sJSON, expected %s' % ('' if j is not None else 'not ', exp['stdout_json']))
    if 'stderr_contains' in exp:
        tail = ' '.join(res.get('stderr_tail', []))
        if exp['stderr_contains'] not in tail:
            bad.append('stderr tail %r lacks %r' % (tail, exp['stderr_contains']))
    if 'json_out_equals_stdout' in exp and res['json_out_equals_stdout'] != exp['json_out_equals_stdout']:
        bad.append('json_out_equals_stdout %s' % res['json_out_equals_stdout'])
    for atom, frag in sorted((exp.get('why_contains') or {}).items()):
        whys = ((j or {}).get('atoms') or {}).get(atom, {}).get('why') or []
        if not any(frag in w for w in whys):
            bad.append('atom %s why %s lacks %r' % (atom, whys[:3], frag))
    b = (j or {}).get('battery')
    if 'battery' in exp:
        eb = exp['battery']
        if b is None:
            bad.append('no battery block')
        else:
            if 'failing_empty' in eb and (b['failing'] == []) != eb['failing_empty']:
                bad.append('battery.failing %s' % b['failing'])
            if 'failing_contains' in eb and not any(eb['failing_contains'] in x for x in b['failing']):
                bad.append('battery.failing lacks %r: %s' % (eb['failing_contains'], b['failing']))
            if 'mutations' in eb and len(b['mutations']) != eb['mutations']:
                bad.append('mutations %d, expected %d' % (len(b['mutations']), eb['mutations']))
            if eb.get('all_ok') and not all(m['ok'] for m in b['mutations']):
                bad.append('a mutation is not ok')
            if 'do_nothing_red' in eb and b['do_nothing_red'] != sorted(eb['do_nothing_red']):
                bad.append('do_nothing_red %s' % b['do_nothing_red'])
    if 'counter_sha256_differs_from_freeze' in exp:
        d = (j or {}).get('counter_sha256') != (j or {}).get('counter_sha256_at_freeze')
        if d != exp['counter_sha256_differs_from_freeze']:
            bad.append('counter digests differ=%s' % d)
    return bad


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--lane', default=LANE_DEFAULT)
    ap.add_argument('--work')
    ap.add_argument('--expected', default=EXPECTED_DEFAULT)
    ap.add_argument('--counter', help='default: LANE/' + COUNTER_REL)
    ap.add_argument('--mutant-counter', help='mutation mode: judge this (behaviourally different) counter, grafted in as if frozen; a red run then means the selftest caught the mutant')
    ap.add_argument('--only')
    ap.add_argument('--keep', action='store_true')
    ap.add_argument('--json-out')
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args(argv)
    if a.list:
        for cid, desc, _, _ in CASES:
            print('%s\t%s' % (cid, desc))
        return 0
    t_all = time.time()
    lane = os.path.realpath(a.lane)
    try:
        with open(a.expected) as f:
            E = json.load(f)
        if a.work:
            work = os.path.realpath(a.work)
            os.makedirs(work, exist_ok=True)
            created = False
        else:
            tmp = os.environ.get('TMPDIR')
            if not tmp or not os.path.isdir(tmp):
                raise Unevaluable('no --work and $TMPDIR is not a directory')
            work = tempfile.mkdtemp(prefix='selftest-r49-c2-', dir=tmp)
            created = True
        if work == lane or work.startswith(lane + os.sep):
            raise Unevaluable('work directory is inside the lane')
        if a.json_out and os.path.realpath(a.json_out).startswith(lane + os.sep):
            raise Unevaluable('--json-out is inside the lane')
        counter = os.path.realpath(a.mutant_counter or a.counter or os.path.join(lane, COUNTER_REL))
        with open(counter, 'rb') as f:
            cbytes = f.read()
        if not a.mutant_counter and sha(cbytes) != E['counter_sha256']:
            raise Unevaluable('counter sha256 %s != pinned %s' % (sha(cbytes), E['counter_sha256']))
        ids = [c[0] for c in CASES]
        if len(set(ids)) != len(ids):
            raise Unevaluable('duplicate case ids')
        fx = Fx(work, lane, E['base'], E['freeze'])
        fx.make()
        if a.mutant_counter:
            fx.graft_counter(cbytes)
        tampered = os.path.join(work, 'tampered', 'c2-mismatch.py')
        os.makedirs(os.path.dirname(tampered))
        with open(tampered, 'wb') as f:
            f.write(cbytes + b'\n# tampered copy: not the frozen bytes\n')
    except (Unevaluable, OSError, ValueError, KeyError) as e:
        print(json.dumps({'cases': 0, 'passed': 0, 'failed': [], 'exit_code': 2,
                          'unevaluable': str(e)}, indent=1))
        return 2
    only = set(a.only.split(',')) if a.only else None
    results, failed, order = [], [], []
    try:
        exp = E['cases']
        problems = sorted(set(ids) - set(exp)) + sorted(set(exp) - set(ids))
        for cid, desc, builder, opt in CASES:
            if only and cid not in only:
                continue
            order.append(cid)
            if cid not in exp:
                failed.append({'id': cid, 'why': ['no expectation in the expected file']})
                continue
            r = run_case(fx, cid, desc, builder, opt, counter, tampered, fx.freeze, fx.base)
            why = judge(r, exp[cid])
            r['ok'] = not why
            r['why'] = why
            r['kind'] = exp[cid].get('kind', 'case')
            results.append(r)
            if why:
                failed.append({'id': cid, 'why': why})
        for cid in problems:
            if not only:
                failed.append({'id': cid, 'why': ['case list and expected file disagree']})
        if not only and len(order) != E.get('cases_total', len(order)):
            failed.append({'id': '*', 'why': ['cases_total %s, ran %d' % (E.get('cases_total'), len(order))]})
        cov = sorted({x for c in order for x in (exp.get(c, {}).get('red') or []) if x in ATOMS
                      and len(exp[c].get('red')) == 1 and exp[c]['exit'] == 1})
        if not only and cov != ATOMS:
            failed.append({'id': '*', 'why': ['atoms with a single-defect red case: %s, want all nine' % cov]})
    except Unevaluable as e:
        print(json.dumps({'cases': len(results), 'exit_code': 2, 'unevaluable': str(e)}, indent=1))
        return 2
    finally:
        if not a.keep:
            shutil.rmtree(work if created else os.path.join(work, 'clone'), ignore_errors=True)
            if not created:
                for d in ('tampered', 'home'):
                    shutil.rmtree(os.path.join(work, d), ignore_errors=True)
                for fn in os.listdir(work):
                    if fn.startswith('out-') and fn.endswith('.json'):
                        os.remove(os.path.join(work, fn))
    summary = {'schema': 'kaidoku-r50-selftest-r49-c2-v1', 'counter_sha256': sha(cbytes),
               'base': E['base'], 'freeze': E['freeze'],
               'mutant_counter': bool(a.mutant_counter), 'cases': len(results), 'passed': sum(1 for r in results if r['ok']),
               'failed': failed, 'wall_sec': round(time.time() - t_all, 2),
               'per_case': [{k: r[k] for k in ('id', 'kind', 'rc', 'red', 'reason', 'sec',
                                               'stdout_sha256', 'ok')} for r in results],
               'exit_code': 1 if failed else 0}
    s = json.dumps(summary, indent=1, sort_keys=True)
    if a.json_out:
        with open(a.json_out, 'w') as f:
            f.write(s + '\n')
    print(s)
    return summary['exit_code']


if __name__ == '__main__':
    sys.exit(main())
