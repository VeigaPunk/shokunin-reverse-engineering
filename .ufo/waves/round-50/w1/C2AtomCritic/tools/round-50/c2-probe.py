#!/usr/bin/env python3
"""DRAFT probe, seat C2AtomCritic (round 50 wave 1). NOT the frozen counter.

For each round-50 C2 atom B1-B11 it implements two predicates over an in-memory view of the
repository:
  naive  = the plan's wording taken literally (a token or phrase is present in the raw text);
  tight  = a draft tightened predicate (comment and code-fence text excluded, exact cell or line
           parse, pinned values re-derived from the base or from the pinned bytes, exactly one).
A landing overlay G (the correction text the plan asks for) must score green on both; each
forgery overlay F is a single targeted edit of G. A forgery that scores green on naive while
the atom is supposed to be red is a plan-wording defect; one that scores green on tight is a
predicate defect. Reads lane bytes only with `git show` / `git ls-tree` (read-only).
Usage: SCR=<scratch dir> python3 -I -B c2-probe.py > out.txt
"""
import hashlib, importlib.util, json, os, re, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = '7c678ae6d97aedb969fd253b52b3d2882ef1e186'
SCR = os.environ['SCR']
R48 = '.ufo/waves/round-48/w1'
RES48 = '.ufo/waves/round-48/r48-w1-results.json'
C1R = '.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json'
C2R = '.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json'
FB = 'corpus/evidence/round-49/c2/freebsd-sysexits.html'
POP = 'corpus/evidence/round-49/c2/popper.html'
DASH = '\u2014'


def git(*a):
    return subprocess.run(['git', '-C', LANE] + list(a), capture_output=True)


def show(path, rev=BASE):
    p = git('show', '%s:%s' % (rev, path))
    return p.stdout if p.returncode == 0 else None


def sha(b):
    return hashlib.sha256(b).hexdigest()


# frozen round-49 helpers (html_norm, quotes, section_of, cells, registry_rows): read-only import
# of the base blob copied into scratch; the probe never edits them.
c2src = show('tools/round-49/c2-mismatch.py')
with open(os.path.join(SCR, 'c2_r49_helpers.py'), 'wb') as fh:
    fh.write(c2src)
sys.path.insert(0, SCR)
import c2_r49_helpers as H  # noqa: E402


class View:
    def __init__(self, over=None):
        self.over = over or {}

    def get(self, path):
        return self.over[path] if path in self.over else show(path)

    def text(self, path):
        b = self.get(path)
        return b.decode() if b is not None else ''


def visible(t):
    """Lines a reader sees: HTML comments and fenced code removed."""
    t = re.sub(r'(?s)<!--.*?-->', '', t)
    out, fence = [], False
    for l in t.split('\n'):
        if re.match(r'^\s*(```|~~~)', l):
            fence = not fence
            continue
        if not fence:
            out.append(l)
    return out


def raw_section(t, heading):
    lines, out, on = t.split('\n'), [], False
    for l in lines:
        if l.startswith('## '):
            on = l.strip() == heading
            continue
        if on:
            out.append(l)
    return out


def vis_section(t, heading):
    return raw_section('\n'.join(visible(t)), heading)


_count = {}


def knowledge_count(rev):
    if rev not in _count:
        p = git('ls-tree', '-r', '--name-only', rev, 'corpus/knowledge')
        _count[rev] = None if p.returncode else sum(1 for x in p.stdout.decode().split('\n') if x.endswith('.md'))
    return _count[rev]


def is_commit(h):
    return git('cat-file', '-e', h + '^{commit}').returncode == 0


BASE_SRC_ROWS, _ = H.registry_rows('\n'.join(visible(show('corpus/SOURCES.md').decode())))
BASE_SRC_RAW = show('corpus/SOURCES.md').decode()
FREEZE = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
TARGET_PATHS = [x for x in git('ls-tree', '-r', '--name-only', BASE, 'tools/round-49').stdout.decode().split('\n')
                if x.endswith(('.py', '.sh'))]


def derived_b3():
    """seats, reports, missing set from the round-48 results at base (same rule as round-49 A4)."""
    res = json.loads(show(RES48))
    names = [r['name'] for r in res['results']]
    tree = git('ls-tree', '-r', '--name-only', BASE, R48).stdout.decode().split('\n')
    missing = []
    for n in names:
        ok = False
        for p in tree:
            if (p == '%s/%s.md' % (R48, n) or (p.startswith('%s/%s/' % (R48, n)) and p.endswith('.md'))) and show(p):
                ok = True
                break
        if not ok:
            missing.append(n)
    return len(names), len(names) - len(missing), sorted(missing)


# ----------------------------------------------------------------- atoms: naive and tight
def owned_row(v, label):
    rows = [l for l in vis_section(v.text('SCORECARD.md'), '## Owned axes') if l.startswith('| %s |' % label)]
    return rows


def B1_naive(v):
    n = knowledge_count(BASE)
    return '%d/%d knowledge files' % (n, n) in v.text('SCORECARD.md')


def B1_tight(v):
    rows = owned_row(v, 'coverage')
    if len(rows) != 1:
        return False
    m = re.search(r'(\d+)/(\d+) knowledge files mapped at ([0-9a-f]{40})', rows[0])
    if not m or m.group(1) != m.group(2):
        return False
    return knowledge_count(m.group(3)) == int(m.group(1))


def B2_naive(v):
    t = v.text('SCORECARD.md')
    return 'rejected-harmed' in t and 'c2-final' in t


def B2_tight(v):
    rows = owned_row(v, 'calibration')
    if len(rows) != 1:
        return False
    h = sha(show('.ufo/waves/round-49/l1/scores/c2-final.json'))
    return 'rejected-harmed' in rows[0] and h in rows[0]


def B3_naive(v):
    s = '\n'.join(raw_section(v.text('SCORECARD.md'), '## Record corrections \u2014 round 50'))
    return 'C1Meaning' in s and 'ScribeReportNumbers' in s and '72' in s


def B3_tight(v):
    lines = [l for l in vis_section(v.text('SCORECARD.md'), '## Record corrections \u2014 round 50') if l.startswith('- B3 ')]
    if len(lines) != 1:
        return False
    m = re.fullmatch(r'- B3 seats=(\d+) reports=(\d+) missing=([A-Za-z0-9,]+)\s*', lines[0])
    if not m:
        return False
    seats, reps, _ = derived_b3()
    miss = sorted(m.group(3).split(','))
    return int(m.group(1)) == seats and int(m.group(2)) == reps and miss == derived_b3()[2]


def B4_naive(v):
    s = '\n'.join(raw_section(v.text('SCORECARD.md'), '## Record corrections \u2014 round 50'))
    return 'discernment' in s and 'quality' in s and 'harmed' in s


def B4_tight(v):
    lines = [l for l in vis_section(v.text('SCORECARD.md'), '## Record corrections \u2014 round 50') if l.startswith('- B4 ')]
    if len(lines) != 1:
        return False
    if lines[0].strip() != '- B4 quality=harmed discernment=improved-decision-level-only source=corpus/lessons/round-48-verifier-spotcheck.md':
        return False
    c = show('corpus/lessons/round-48-verifier-spotcheck.md').decode()
    return bool(re.search(r'quality \u2014 harmed', c)) and bool(re.search(r'discernment \u2014 improved \(decision-level only\)', c))


def B5_naive(v):
    t = v.text('SCORECARD.md')
    return '33f65a91' in t and '8847042a' in t


def B5_tight(v):
    lines = [l for l in vis_section(v.text('SCORECARD.md'), '## Record corrections \u2014 round 50') if l.startswith('- B5 ')]
    if len(lines) != 1:
        return False
    want = '- B5 receipts=%s,%s sha256=%s,%s' % (C1R, C2R, sha(show(C1R)), sha(show(C2R)))
    return lines[0].strip() == want


def _supersedes(v, old, tier, status, snap, heading):
    reg = v.text('corpus/SOURCES.md')
    rows, dups = H.registry_rows('\n'.join(visible(reg)))
    cand = [k for k, l in rows.items() if H.cells(l)[6].startswith('supersedes %s %s' % (old, DASH))]
    if len(cand) != 1 or dups:
        return False
    new = cand[0]
    if new in BASE_SRC_ROWS or rows.get(old) != BASE_SRC_ROWS.get(old):
        return False
    c = H.cells(rows[new])
    if len(c) != 11 or c[3] != tier or c[7] != status:
        return False
    snapb = show(snap)
    if snapb is None or sha(snapb) not in c[5]:
        return False
    norm = H.html_norm(snapb)
    qs = H.quotes(c[5])
    if not qs:
        return False
    for q, _ in qs:
        qn = re.sub(r'\s+', ' ', q).strip()
        if heading not in c[5]:
            return False
        if qn not in norm or heading not in (H.section_of(norm, norm.find(qn)) or ''):
            return False
    return True


def B6_naive(v):
    return 'supersedes S149 %s' % DASH in v.text('corpus/SOURCES.md')


def B6_tight(v):
    return _supersedes(v, 'S149', 'C', 'rejected', FB, 'ERRORS')


def B7_naive(v):
    return 'supersedes S147 %s' % DASH in v.text('corpus/SOURCES.md')


def B7_tight(v):
    return _supersedes(v, 'S147', 'B', 'mined', POP, 'Backdrop to Popper')


def B8_naive(v):
    return 'supersedes S138 %s' % DASH in v.text('corpus/SOURCES.md')


def B8_tight(v):
    # no committed listing snapshot of the 22-member census exists at base: cannot be bound
    return None


def _skill_registry(v):
    t = v.text('SKILL.md')
    return t, [l for l in vis_section(t, '## Local round-evidence gate registry') if l.startswith('| `')]


VERDICT_OK = re.compile(r'^0=(met|clean|pass|success)\b')
VERDICT_BAD = re.compile(r'^1=(not met|violation|fail)')
VERDICT_2 = re.compile(r'2=(could-not-evaluate|usage|error)')


def B9_naive(v):
    t = v.text('SKILL.md')
    return all(p in t for p in TARGET_PATHS)


def B9_tight(v):
    _, rows = _skill_registry(v)
    byp = {}
    for l in rows:
        c = H.cells(l)
        byp.setdefault(c[0].strip('`'), []).append(c)
    for p in TARGET_PATHS:
        if p not in byp or len(byp[p]) != 1:
            return False
        vm = [x.strip() for x in byp[p][0][2].split(';')]
        if len(vm) != 3 or not (VERDICT_OK.match(vm[0]) and VERDICT_BAD.match(vm[1]) and VERDICT_2.search(vm[2])):
            return False
    return True


def B10_naive(v):
    return v.get('tools/round-50/selftest-r49-c2.py') is not None


def B10_tight(v):
    # not run: the file would sit inside tools/round-50/ (frozen at FREEZE); see report
    return None


def B11(v):
    les = v.text('corpus/lessons/round-49.md').split('\n')[3]
    m = re.search(r'Declared freeze `([0-9a-f]{40})`', les)
    sc = re.search(r'\*\*Declared freeze:\*\* `([0-9a-f]{40})`', '\n'.join(raw_section(v.text('SCORECARD.md'), '## Round 49 \u2014 one freeze, SquashFS v1/v2 to Core, nine record atoms re-derived (met under the frozen counters; counter misses reported)')))
    fr = v.text('.ufo/waves/round-49/l1/FREEZE').strip()
    return bool(m) and bool(sc) and m.group(1) == sc.group(1) == fr


ATOMS = {
    'B1': (B1_naive, B1_tight), 'B2': (B2_naive, B2_tight), 'B3': (B3_naive, B3_tight),
    'B4': (B4_naive, B4_tight), 'B5': (B5_naive, B5_tight), 'B6': (B6_naive, B6_tight),
    'B7': (B7_naive, B7_tight), 'B8': (B8_naive, B8_tight), 'B9': (B9_naive, B9_tight),
    'B10': (B10_naive, B10_tight), 'B11': (lambda v: B11(v), lambda v: B11(v)),
}
