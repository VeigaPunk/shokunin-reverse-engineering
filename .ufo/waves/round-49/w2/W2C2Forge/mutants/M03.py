#!/usr/bin/env python3
"""R49-C2 counter (calibration): count mismatches between the lane's round-48 self-assessment
and the repository state the round-48 non-author closure observed.

The claim text is `plans/round-49-claims.md` R49-C2. The unit is an *atom*: one statement the
lane made (or a statement the repository still carries) paired with a re-derivation from
committed bytes. An atom is a **mismatch** when its re-derivation disagrees with the record or
when the record that must correct it is absent. Nine atoms, A1..A9, one per defect the
round-48 closure (`corpus/lessons/round-48-verifier-spotcheck.md`, "Routed defects") named that
this round repairs. The counter reads lane bytes only through git objects (`git show REV:path`)
and writes nothing; it needs no scratch directory and never touches the network.

**Two read sets.** Every round-48 input (SCORECARD round-48 section, LOG.md, the round-48
lesson, the closure, the round-48 results file, the committed `w1/` tree and both receipts)
is read at the round-49 base `LANE_BASE`, never at REV: editing a historical input after
the freeze cannot move an atom. Round-49 outputs (the lesson corrections, SOURCES rows S147/S148
and the search log, the SCORECARD correction section, the committed source snapshots) are read at
REV. A heading or an atom line that occurs more than once is a mismatch, never "first wins".

Predicate (the same sentence as the plan): at the measured revision REV, `mismatches == 0`
over the nine atoms (`atoms_total == 9`) and the in-counter battery is clean; at the freeze the
count is 9.

  A1  the declared freeze: `SCORECARD.md` `## Round 48` (at base) declares one 40-hex freeze,
      LOG.md (at base) names it as the final declared freeze and the closure names its 8-hex;
      the filed round-48 lesson header names a different one; the round-49 correction line `A1`
      names both, both are commits, and `corpus/lessons/round-48.md` at REV is byte-identical to
      the base blob (a correction is a new entry, never a rewrite).
  A2  the dead hash: the closure quotes `663f30ee7516942a0120e7de68fe88356e680822` as the round-48
      fleet report's cited hash; line `A2` names it and the real commit; the dead one is not a
      commit, the real one is, is an ancestor of REV, and shares the first 8 hex.
  A3  the LOG pointers: line `A3` states the full LOG.md line-number set (at base) naming each of
      `2e785632`, `33f65a91`, `c093e798`, and lists as `unnamed` exactly `577a02a5`, `8847042a`,
      `7fe11332` (commits LOG.md never names); every set is re-derived from the base blob, and
      REV's LOG.md must begin with the base blob.
  A4  the wave accounting: line `A4` states seats, seats with a non-empty report artifact (a `.md`
      at `w1/<seat>.md` or under `w1/<seat>/`) and the seats without one, re-derived at base from
      `.ufo/waves/round-48/r48-w1-results.json` and the committed `w1/` tree.
  A5  the receipt digests: line `A5` states raw and newline-stripped sha256 of both round-48
      final receipts (read at base) and which of them the closure shows the round-48 report
      quoted (its first 8 hex; the closure must quote that prefix and not the raw one).
  A6  S145's wrong locator: registry row S147 `supersedes S145 —`, locator = the heading the
      quote sits under in the committed snapshot `corpus/evidence/round-49/c2/popper.html`
      (sha256-pinned in the row), quote <= 25 words, its stated word count equal to the real
      count, present in the snapshot; used-by lists `corpus/lessons/round-49.md`; S145's own
      line is byte-identical to the base; the id is not duplicated.
  A7  S146's wrong rationale: registry row S148 `supersedes S146 —` on the reachable
      `sysexits.h.3head.html`, quote (word count stated and real) present in the sha256-pinned
      snapshot `corpus/evidence/round-49/c2/sysexits.html`, the snapshot carries `EX_USAGE 64`,
      the teaches cell states `EX_USAGE is 64` and no other status for `EX_USAGE`; S146's own
      line is byte-identical to the base.
  A8  the search log: `corpus/SOURCES.md` `## Search log` carries exactly one round-48 entry
      (marked `late entry`) and exactly one round-49 entry; each states
      identified/screened/included/excluded and `rows B -> A`, a `where searched:` clause, a
      `stop:` rationale and, when excluded > 0, an `exclusion:` reason. `rows`, `included` and
      `excluded` are re-derived from the registry at the revisions concerned (round 48: base
      `61b87d74` -> tip `8847042a`; round 49: lane base -> REV); `screened == included +
      excluded` and `identified >= screened` are checked, `identified` itself is asserted by the
      lane, not derivable.
  A9  the calibration record: `SCORECARD.md` `## Record corrections — round 49` (exactly one such
      heading) carries exactly one line `- A9 verdict=rejected-harmed
      source=corpus/lessons/round-48-verifier-spotcheck.md calibration=harmed`; the closure at
      base states `Admission: **rejected-harmed**` and a `| calibration | harmed |` axis row.

Freeze integrity: REV must descend from FREEZE and no commit in FREEZE..REV may touch
`tools/round-49` or `plans/round-49-claims.md` (an added file counts), and every blob under them
equals its FREEZE blob; otherwise exit 2 `frozen_path_changed` (never "met"). The counter also
exits 2 `counter_not_frozen` when its own bytes differ from `tools/round-49/c2-mismatch.py` at
FREEZE, and records both digests. It cannot bind which commit the operator passes as FREEZE;
the L1 records that hash in `.ufo/waves/round-49/l1/FREEZE` and LOG.md before any data run.

Usage:
  c2-mismatch.py --root LANE --rev REV --freeze FREEZE [--json-out PATH]
  c2-mismatch.py --root LANE --rev REV --freeze FREEZE --battery [--json-out PATH]
Exit: 0 mismatches == 0 (and, with --battery, a clean battery), 1 mismatches > 0 or a battery
failure, 2 unevaluable. `--battery` applies the single-mutation overlays (`N_MUT` of them, each
turning exactly its own atom red and none a no-op) and a do-nothing overlay (every path changed
since FREEZE restored to its FREEZE blob, which must turn all nine red) to an in-memory overlay of REV.
"""
import argparse
import hashlib
import html
import json
import re
import subprocess
import sys

R48_BASE = '61b87d742032e65fca9c38267d7d6ed7e555edad'
R48_TIP = '8847042a140b044dbf335210c965bf7b06b09b4f'
LANE_BASE = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
ROUND_DATE = '2026-10-28'
LESSON = 'corpus/lessons/round-49.md'
SECTION = '## Corrections to round 48'
CLOSURE = 'corpus/lessons/round-48-verifier-spotcheck.md'
FROZEN = ('tools/round-49', 'plans/round-49-claims.md')
SELF = 'tools/round-49/c2-mismatch.py'
HEX40 = re.compile(r'[0-9a-f]{40}')
HEX64 = re.compile(r'[0-9a-f]{64}')
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
W1 = '.ufo/waves/round-48/w1'
RESULTS48 = '.ufo/waves/round-48/r48-w1-results.json'
RECEIPTS = {'c1': '.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json',
            'c2': '.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json'}
LOG_KEYS = ('2e785632', '33f65a91', 'c093e798')
UNNAMED = ('577a02a5', '8847042a', '7fe11332')
ATOM_IDS = ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9')
N_MUT = 16


class Git:
    def __init__(self, root):
        self.root = root

    def _run(self, *args):
        return subprocess.run(['git', '-C', self.root] + list(args), capture_output=True)

    def show(self, rev, path):
        p = self._run('show', '%s:%s' % (rev, path))
        return p.stdout if p.returncode == 0 else None

    def is_commit(self, h):
        return self._run('cat-file', '-e', h + '^{commit}').returncode == 0

    def ancestor(self, a, b):
        return self._run('merge-base', '--is-ancestor', a, b).returncode == 0

    def ls(self, rev, prefix):
        p = self._run('-c', 'core.quotePath=false', 'ls-tree', '-r', '--name-only', rev,
                      '--', prefix)
        return p.stdout.decode().split('\n') if p.returncode == 0 else []

    def resolve(self, rev):
        p = self._run('rev-parse', '--verify', rev + '^{commit}')
        return p.stdout.decode().strip() if p.returncode == 0 else None

    def touched(self, freeze, rev):
        p = self._run('-c', 'core.quotePath=false', 'log', '-m', '--diff-merges=first-parent',
                      '--name-status', '--format=%H', '%s..%s' % (freeze, rev), '--', *FROZEN)
        return [l for l in p.stdout.decode().splitlines() if l.strip()] \
            if p.returncode == 0 else None

    def changed(self, a, b):
        p = self._run('-c', 'core.quotePath=false', 'diff', '--name-only', a, b)
        return [x for x in p.stdout.decode().split('\n') if x]


class Overlay:
    """REV with some paths replaced (bytes) or removed (None). Other revs read through."""

    def __init__(self, base, rev, over):
        self.b, self.rev, self.over = base, rev, over

    def show(self, rev, path):
        if rev == self.rev and path in self.over:
            return self.over[path]
        return self.b.show(rev, path)

    def ls(self, rev, prefix):
        out = list(self.b.ls(rev, prefix))
        if rev == self.rev:
            out = [p for p in out if self.over.get(p, b'') is not None]
            out += [p for p, v in self.over.items() if v is not None and p not in out
                    and p.startswith(prefix)]
        return out

    def __getattr__(self, name):
        return getattr(self.b, name)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def text(b):
    return b.decode('utf-8', 'replace') if b is not None else ''


def sections(t, head):
    """Every section whose `## ` heading line starts with `head`: list of line lists."""
    out, cur = [], None
    for l in t.splitlines():
        if l.startswith('## '):
            cur = [] if l.startswith(head) else None
            if cur is not None:
                out.append(cur)
            continue
        if cur is not None:
            cur.append(l)
    return out


def unique_section(t, head):
    s = sections(t, head)
    return (s[0], None) if len(s) == 1 else (None, '%d `%s` sections, want 1' % (len(s), head))


def cells(line):
    c = [x.strip() for x in line.strip().split('|')]
    return c[1:-1] if len(c) >= 2 else c


def registry_rows(t):
    rows, dups = {}, set()
    for l in t.splitlines():
        m = ROW_RE.match(l)
        if m:
            if m.group(1) in rows:
                dups.add(m.group(1))
            rows[m.group(1)] = l
    return rows, dups


def lesson_lines(r, rev):
    """({atom: {k: v}}, {atoms seen more than once}) or (None, set()) if absent."""
    lt = r.show(rev, LESSON)
    if lt is None:
        return None, set()
    secs = sections(text(lt), SECTION)
    if len(secs) != 1:
        return None, set()
    out, dups = {}, set()
    for l in secs[0]:
        m = re.match(r'^- (A\d)\s+(.*)$', l.strip())
        if m:
            if m.group(1) in out:
                dups.add(m.group(1))
            kv = {}
            for tok in m.group(2).split():
                if '=' in tok:
                    k, v = tok.split('=', 1)
                    kv[k] = v
            out[m.group(1)] = kv
    return out, dups


def strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s)


def html_norm(b):
    t = text(b)
    t = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', ' ', t)
    t = re.sub(r'(?is)<h([23])[^>]*>(.*?)</h\1>',
               lambda m: ' \x01' + strip_tags(m.group(2)) + '\x02 ', t)
    t = html.unescape(strip_tags(t))
    return re.sub(r'\s+', ' ', t)


def quotes(cell):
    """[(quote, stated_word_count or None)] for every "..." followed by (N words)."""
    return [(m.group(1), int(m.group(2)) if m.group(2) else None)
            for m in re.finditer(r'"([^"]+)"(?:\s*\((\d+) words\))?', cell)]


def section_of(norm, idx):
    best = None
    for m in re.finditer('\x01(.*?)\x02', norm):
        if m.start() < idx:
            best = re.sub(r'\s+', ' ', m.group(1)).strip()
    return best


def line_numbers(blob, needle):
    return [i + 1 for i, l in enumerate(text(blob).split('\n')) if needle in l]


def ctx_for(r, key, L, dups):
    d = L.get(key) if L is not None else None
    if not d:
        return None, ['lesson line %s absent' % key]
    if key in dups:
        return None, ['lesson line %s occurs more than once' % key]
    return d, []


# ------------------------------------------------------------------ atoms (round-48 inputs
# are read at LANE_BASE; round-49 outputs at `rev`)


def a1(r, rev, L, dups):
    d, bad = ctx_for(r, 'A1', L, dups)
    if bad:
        return bad
    out = []
    sc = sections(text(r.show(LANE_BASE, 'SCORECARD.md')), '## Round 48')
    sc_decl = re.findall(r'\*\*Declared freeze:\*\*\s*`([0-9a-f]{40})`', '\n'.join(sc[0]) if len(sc) == 1 else '')
    if len(sc) != 1 or len(sc_decl) != 1:
        out.append('SCORECARD Round 48: %d sections, %d declared-freeze statements, want 1/1' % (
            len(sc), len(sc_decl)))
    declared_sc = sc_decl[0] if len(sc_decl) == 1 else None
    les = r.show(rev, 'corpus/lessons/round-48.md')
    st = re.findall(r'Declared freeze\s+`([0-9a-f]{40})`', text(les))
    stale = st[0] if len(st) == 1 else None
    if stale is None:
        out.append('round-48 lesson names %d freezes, want 1' % len(st))
    if d.get('declared') != declared_sc:
        out.append('A1 declared != SCORECARD base freeze')
    if d.get('stale') != stale:
        out.append('A1 stale != lesson header freeze')
    if declared_sc and stale and declared_sc == stale:
        out.append('no disagreement to correct')
    if declared_sc and ('final declared freeze `%s`' % declared_sc) not in text(r.show(LANE_BASE, 'LOG.md')):
        out.append('LOG.md (base) does not name the declared freeze as final')
    if declared_sc and declared_sc[:8] not in text(r.show(LANE_BASE, CLOSURE)):
        out.append('closure (base) does not name the declared freeze')
    for h in (d.get('declared'), d.get('stale')):
        if not (h and HEX40.fullmatch(h) and r.is_commit(h)):
            out.append('not a commit: %s' % h)
    base = r.show(LANE_BASE, 'corpus/lessons/round-48.md')
    if les is None or base is None or sha(les) != sha(base):
        out.append('round-48 lesson rewritten (not byte-identical to base)')
    return out


def a2(r, rev, L, dups):
    d, bad = ctx_for(r, 'A2', L, dups)
    if bad:
        return bad
    dead, real = d.get('dead', ''), d.get('actual', '')
    out = []
    if not (HEX40.fullmatch(dead) and HEX40.fullmatch(real)):
        return ['A2 hashes are not 40-hex']
    if dead not in text(r.show(LANE_BASE, CLOSURE)):
        out.append('the closure (base) does not quote the dead hash')
    if r.is_commit(dead):
        out.append('the "dead" hash resolves to a commit')
    if not r.is_commit(real):
        out.append('the real hash is not a commit')
    elif not r.ancestor(real, rev):
        out.append('the real commit is not an ancestor of REV')
    if False:
        out.append('hashes do not share exactly the 8-hex prefix')
    return out


def a3(r, rev, L, dups):
    d, bad = ctx_for(r, 'A3', L, dups)
    if bad:
        return bad
    out = []
    base = r.show(LANE_BASE, 'LOG.md')
    now = r.show(rev, 'LOG.md')
    if base is None or now is None or not now.startswith(base):
        out.append('LOG.md at REV does not begin with the base blob (not append-only)')
    keys = sorted(k[4:] for k in d if k.startswith('log_'))
    if keys != sorted(LOG_KEYS):
        out.append('A3 log_ keys %s, want exactly %s' % (keys, sorted(LOG_KEYS)))
    for h in LOG_KEYS:
        want = [int(x) for x in d.get('log_' + h, '').split(',') if x.isdigit()]
        got = line_numbers(base, h) if base is not None else []
        if not got or sorted(want) != got:
            out.append('log_%s: stated %s, derived %s' % (h, want, got))
    un = sorted(x for x in d.get('unnamed', '').split(',') if x)
    if un != sorted(UNNAMED):
        out.append('A3 unnamed %s, want exactly %s' % (un, sorted(UNNAMED)))
    for h in UNNAMED:
        if base is not None and line_numbers(base, h):
            out.append('%s is named in LOG.md at the base' % h)
        if not r.is_commit(h):
            out.append('%s is not a commit' % h)
    return out


def a4(r, rev, L, dups):
    d, bad = ctx_for(r, 'A4', L, dups)
    if bad:
        return bad
    res = r.show(LANE_BASE, RESULTS48)
    try:
        names = [x['name'] for x in json.loads(res)['results']]
    except (TypeError, ValueError, KeyError):
        return ['round-48 results.json unreadable at base']
    tree = [p for p in r.ls(LANE_BASE, W1) if p]
    missing = []
    for n in names:
        paths = [p for p in tree if p == '%s/%s.md' % (W1, n)
                 or (p.startswith('%s/%s/' % (W1, n)) and p.endswith('.md'))]
        if not any(r.show(LANE_BASE, p) for p in paths):
            missing.append(n)
    out = []
    if d.get('seats') != str(len(names)):
        out.append('seats stated %s, derived %d' % (d.get('seats'), len(names)))
    if d.get('reports') != str(len(names) - len(missing)):
        out.append('reports stated %s, derived %d' % (d.get('reports'), len(names) - len(missing)))
    if sorted(x for x in d.get('missing', '').split(',') if x) != sorted(missing):
        out.append('missing stated %s, derived %s' % (d.get('missing'), sorted(missing)))
    return out


def a5(r, rev, L, dups):
    d, bad = ctx_for(r, 'A5', L, dups)
    if bad:
        return bad
    out = []
    closure = text(r.show(LANE_BASE, CLOSURE))
    for k, path in RECEIPTS.items():
        b = r.show(LANE_BASE, path)
        if b is None:
            out.append('receipt %s absent at base' % path)
            continue
        raw = sha(b)
        stripped = sha(b[:-1] if b.endswith(b'\n') else b)
        if d.get(k + '_raw') != raw:
            out.append('%s_raw stated %s, derived %s' % (k, d.get(k + '_raw'), raw))
        if d.get(k + '_stripped') != stripped:
            out.append('%s_stripped stated %s, derived %s' % (k, d.get(k + '_stripped'), stripped))
        q = d.get('report_' + k, '')
        if len(q) != 8 or stripped[:8] != q or raw[:8] == q:
            out.append('report_%s %s is not the stripped digest prefix' % (k, q))
        if q and q not in closure:
            out.append('the closure (base) never quotes %s' % q)
    return out


def _snapshot_row(r, rev, L, dups, key, rid, old, snap):
    d, bad = ctx_for(r, key, L, dups)
    if bad:
        return bad, None, None
    if d.get('row') != rid:
        return ['lesson line %s names no row %s' % (key, rid)], None, None
    out = []
    rows, rdup = registry_rows(text(r.show(rev, 'corpus/SOURCES.md')))
    base_rows, _ = registry_rows(text(r.show(LANE_BASE, 'corpus/SOURCES.md')))
    if rid in rdup or old in rdup:
        out.append('duplicate registry id %s/%s' % (rid, old))
    if rid not in rows:
        return ['registry row %s absent' % rid], None, None
    if old not in rows or rows.get(old) != base_rows.get(old):
        out.append('%s was rewritten (append-only)' % old)
    c = cells(rows[rid])
    if len(c) != 11:
        return ['%s has %d cells, want 11' % (rid, len(c))], None, None
    if not c[6].startswith('supersedes %s \u2014' % old):
        out.append('%s teaches does not open "supersedes %s \u2014"' % (rid, old))
    if c[2] != 'docs' or c[3] != 'A' or c[7] != 'mined' or c[8] != ROUND_DATE:
        out.append('%s kind/tier/status/opened wrong: %s' % (rid, c[2:4] + c[7:9]))
    if LESSON not in c[10] or r.show(rev, LESSON) is None:
        out.append('%s used-by does not list a lesson that exists' % rid)
    b = r.show(rev, snap)
    if b is None:
        out.append('snapshot %s absent' % snap)
        return out, c, None
    if sha(b) not in HEX64.findall(c[5]):
        out.append('%s anchor does not pin the snapshot sha256 %s' % (rid, sha(b)))
    return out, c, b


def _check_quotes(out, c, norm):
    qs = quotes(c[5])
    if not qs:
        out.append('anchor carries no quoted passage')
    for q, stated in qs:
        qn = re.sub(r'\s+', ' ', q).strip()
        n = len(qn.split())
        if n > 25:
            out.append('quote over 25 words (%d)' % n)
        if stated is None or stated != n:
            out.append('stated word count %s != real %d' % (stated, n))
        if qn not in norm:
            out.append('quote not in the committed snapshot: %s' % qn[:60])
    return qs


def a6(r, rev, L, dups):
    out, c, b = _snapshot_row(r, rev, L, dups, 'A6', 'S147', 'S145',
                              'corpus/evidence/round-49/c2/popper.html')
    if c is None or b is None:
        return out
    if 'plato.stanford.edu/entries/popper/' not in c[1]:
        out.append('S147 source is not the SEP Popper entry')
    norm = html_norm(b)
    for q, _ in _check_quotes(out, c, norm):
        qn = re.sub(r'\s+', ' ', q).strip()
        i = norm.find(qn)
        if i >= 0:
            head = section_of(norm, i)
            if not head or head not in c[5]:
                out.append('anchor does not name the snapshot heading above the quote (%s)' % head)
    return out


def a7(r, rev, L, dups):
    out, c, b = _snapshot_row(r, rev, L, dups, 'A7', 'S148', 'S146',
                              'corpus/evidence/round-49/c2/sysexits.html')
    if c is None or b is None:
        return out
    if 'man7.org/linux/man-pages/man3/sysexits.h.3head.html' not in c[1]:
        out.append('S148 source is not the sysexits.h.3head page')
    norm = html_norm(b)
    _check_quotes(out, c, norm)
    if 'EX_USAGE 64' not in norm:
        out.append('snapshot does not carry `EX_USAGE 64`')
    if not re.search(r'EX_USAGE is 64\b', c[6]) or re.search(r'EX_USAGE is (?!64\b)\S', c[6]):
        out.append('S148 teaches does not state exactly `EX_USAGE is 64`')
    return out


def _derived(r, a, b):
    ra, _ = registry_rows(text(r.show(a, 'corpus/SOURCES.md')))
    rb, _ = registry_rows(text(r.show(b, 'corpus/SOURCES.md')))
    new = [i for i in rb if i not in ra]
    inc = sum(1 for i in new if cells(rb[i])[7] != 'rejected')
    return len(ra), len(rb), inc, len(new) - inc


def a8(r, rev, L, dups):
    reg = text(r.show(rev, 'corpus/SOURCES.md'))
    secs = sections(reg, '## Search log')
    if len(secs) != 1:
        return ['%d `## Search log` sections, want 1' % len(secs)]
    sec = secs[0]
    out = []
    for tag, a, b in (('round 48', R48_BASE, R48_TIP), ('round 49', LANE_BASE, rev)):
        ent = [l for l in sec if l.startswith('- %s %s' % (ROUND_DATE, tag))]
        if tag == 'round 48':
            ent = [l for l in ent if 'late entry' in l]
        if len(ent) != 1:
            out.append('%s: %d matching search-log entries, want 1' % (tag, len(ent)))
            continue
        e = ent[0]
        want = _derived(r, a, b)
        m = re.search(r'identified (\d+), screened (\d+), included (\d+), excluded (\d+)', e, re.I)
        n = re.search(r'rows (\d+) (?:\u2192|->) (\d+)', e)
        if not m or not n:
            out.append('%s: identified/screened/included/excluded or rows B -> A missing' % tag)
            continue
        idn, scr, inc, exc = map(int, m.groups())
        if (int(n.group(1)), int(n.group(2))) != want[:2]:
            out.append('%s: rows %s -> %s, derived %d -> %d' % (tag, n.group(1), n.group(2), want[0], want[1]))
        if (inc, exc) != want[2:] or scr != inc + exc or idn < scr:
            out.append('%s: included/excluded %d/%d (screened %d, identified %d), derived %d/%d' % (
                tag, inc, exc, scr, idn, want[2], want[3]))
        low = e.lower()
        for token in ('where searched:', 'stop:'):
            if token not in low:
                out.append('%s: entry lacks `%s`' % (tag, token))
        if want[3] > 0 and 'exclusion:' not in low:
            out.append('%s: excluded %d but no `exclusion:` reason' % (tag, want[3]))
    return out


def a9(r, rev, L, dups):
    secs = sections(text(r.show(rev, 'SCORECARD.md')), '## Record corrections \u2014 round 49')
    if len(secs) != 1:
        return ['SCORECARD `## Record corrections \u2014 round 49`: %d sections, want 1' % len(secs)]
    want = ('- A9 verdict=rejected-harmed source=corpus/lessons/round-48-verifier-spotcheck.md '
            'calibration=harmed')
    hits = [l for l in secs[0] if l.strip().startswith('- A9 ')]
    out = []
    if len(hits) != 1 or hits[0].strip() != want:
        out.append('SCORECARD correction section carries %d A9 lines, want exactly one equal to the contract line' % len(hits))
    src = text(r.show(LANE_BASE, CLOSURE))
    if 'Admission: **rejected-harmed**' not in src:
        out.append('closure (base) does not state `Admission: **rejected-harmed**`')
    if not re.search(r'\|\s*calibration\s*\|\s*harmed\s*\|', src):
        out.append('closure (base) has no calibration | harmed axis row')
    return out


ATOMS = {'A1': a1, 'A2': a2, 'A3': a3, 'A4': a4, 'A5': a5, 'A6': a6, 'A7': a7, 'A8': a8,
         'A9': a9}


def score(r, rev):
    L, dups = lesson_lines(r, rev)
    res = {}
    for k in ATOM_IDS:
        try:
            res[k] = ATOMS[k](r, rev, L, dups)
        except Exception as e:  # an atom that crashes is a mismatch, never a pass
            res[k] = ['atom crashed: %r' % (e,)]
    return res


def freeze_check(r, freeze, rev):
    if not r.ancestor(freeze, rev):
        return 'freeze is not an ancestor of rev'
    t = r.touched(freeze, rev)
    if t is None:
        return 'cannot walk FREEZE..REV'
    if t:
        return 'frozen path touched in FREEZE..REV: %s' % ';'.join(t[:6])
    for p in r.ls(freeze, 'tools/round-49') + r.ls(freeze, 'plans/round-49-claims.md'):
        if p and r.show(freeze, p) != r.show(rev, p):
            return 'blob changed: %s' % p
    return None


def mutations(r, rev):
    """(label, atom it must flip, overlay dict) -- each from REV's own bytes."""
    def tx(p):
        return text(r.show(rev, p))

    def rep(p, a, b, count=1):
        t = tx(p)
        return {p: t.replace(a, b, count).encode()} if a in t else None

    muts = []
    les = tx(LESSON)

    def les_rep(label, atom, pat, fn):
        m = re.search(pat, les)
        if m:
            muts.append((label, atom, {LESSON: les.replace(m.group(0), fn(m), 1).encode()}))

    les_rep('A1 swap declared/stale', 'A1', r'- A1 declared=([0-9a-f]{40}) stale=([0-9a-f]{40})',
            lambda m: '- A1 declared=%s stale=%s' % (m.group(2), m.group(1)))
    les_rep('A2 real hash replaced by a non-commit', 'A2',
            r'- A2 dead=([0-9a-f]{40}) actual=([0-9a-f]{40})',
            lambda m: '- A2 dead=%s actual=%s' % (m.group(1), m.group(2)[:8] + '0' * 32))
    les_rep('A3 one pointer line number moved', 'A3', r'log_2e785632=(\d+)',
            lambda m: 'log_2e785632=%d' % (int(m.group(1)) + 1))
    les_rep('A3 one pointer key dropped', 'A3', r' log_c093e798=[0-9,]+', lambda m: '')
    les_rep('A3 one unnamed hash dropped', 'A3', r',7fe11332', lambda m: '')
    les_rep('A4 reports count off by one', 'A4', r'reports=(\d+)',
            lambda m: 'reports=%d' % (int(m.group(1)) + 1))
    les_rep('A5 stripped digest zeroed', 'A5', r'c1_stripped=([0-9a-f]{64})',
            lambda m: 'c1_stripped=' + '0' * 64)
    m = re.search(r'^- A3 .*$', les, re.M)
    if m:
        muts.append(('A3 duplicate atom line', 'A3', {LESSON: (les.rstrip('\n') + '\n' + m.group(0) + '\n').encode()}))
    pop = r.show(rev, 'corpus/evidence/round-49/c2/popper.html')
    if pop:
        muts.append(('A6 snapshot bytes edited', 'A6', {
            'corpus/evidence/round-49/c2/popper.html': pop.replace(b'empirical', b'empirica1')}))
    sx = r.show(rev, 'corpus/evidence/round-49/c2/sysexits.html')
    if sx:
        muts.append(('A7 snapshot bytes edited', 'A7', {
            'corpus/evidence/round-49/c2/sysexits.html': sx.replace(b'EX_USAGE', b'EX_USAGF')}))
    o = rep('corpus/SOURCES.md', '`2. Backdrop to Popper', '`3. The Problem of Demarcation; Popper')
    if o:
        muts.append(('A6 anchor names the wrong section', 'A6', o))
    o = rep('corpus/SOURCES.md', '(21 words)', '(7 words)')
    if o:
        muts.append(('A6 stated word count wrong', 'A6', o))
    o = rep('corpus/SOURCES.md', 'EX_USAGE is 64', 'EX_USAGE is 2, not 64')
    if o:
        muts.append(('A7 teaches states a second status', 'A7', o))
    o = rep('corpus/SOURCES.md', 'late entry', 'last entry')
    if o:
        muts.append(('A8 round-48 entry loses its late marker', 'A8', o))
    reg = tx('corpus/SOURCES.md')
    line49 = next((l for l in reg.split('\n') if l.startswith('- %s round 49' % ROUND_DATE)), None)
    if line49:
        muts.append(('A8 round-49 entry loses its stop rationale', 'A8', {
            'corpus/SOURCES.md': reg.replace(line49, re.sub(r'(?i)stop:', 'halt:', line49), 1).encode()}))
    sc = tx('SCORECARD.md')
    if 'calibration=harmed' in sc:
        muts.append(('A9 contradictory second line appended', 'A9', {
            'SCORECARD.md': (sc.rstrip('\n') + '\n- A9 verdict=admitted source=x calibration=improved\n').encode()}))
    return muts


def battery(r, rev, freeze):
    muts = mutations(r, rev)
    out = {'green': score(r, rev), 'mutations': [], 'failing': []}
    if any(out['green'].values()):
        out['failing'].append('genuine REV is not green')
    if len(muts) != N_MUT:
        out['failing'].append('mutation set incomplete: %d of %d' % (len(muts), N_MUT))
    for label, atom, over in muts:
        noop = [p for p, v in over.items() if v == r.show(rev, p)]
        got = score(Overlay(r, rev, over), rev)
        red = sorted(k for k, v in got.items() if v)
        ok = red == [atom] and not noop
        out['mutations'].append({'label': label, 'atom': atom, 'red': red, 'noop': noop, 'ok': ok})
        if not ok:
            out['failing'].append('%s -> red %s noop %s' % (label, red, noop))
    # do-nothing: REV minus the round's work = every path changed since FREEZE restored to FREEZE
    changed = r.changed(freeze, rev)
    dn = score(Overlay(r, rev, {x: r.show(freeze, x) for x in changed}), rev)
    red = sorted(k for k, v in dn.items() if v)
    out['do_nothing_red'] = red
    out['do_nothing_paths'] = len(changed)
    if red != sorted(ATOM_IDS):
        out['failing'].append('do-nothing overlay red %s, want all nine' % red)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--battery', action='store_true')
    ap.add_argument('--json-out')
    a = ap.parse_args(argv)
    g = Git(a.root)
    rev, freeze = g.resolve(a.rev), g.resolve(a.freeze)
    own = open(__file__, 'rb').read()
    res = {'schema': 'kaidoku-r49-c2-v2', 'rev': rev, 'freeze': freeze,
           'counter_sha256': sha(own), 'exit_code': 2}
    if not rev or not freeze:
        res['reason'] = 'unresolvable rev or freeze'
    else:
        at_freeze = g.show(freeze, SELF)
        res['counter_sha256_at_freeze'] = sha(at_freeze) if at_freeze is not None else None
        why = freeze_check(g, freeze, rev)
        if at_freeze is None or sha(at_freeze) != sha(own):
            res['reason'] = 'counter_not_frozen'
            res['detail'] = 'this file differs from %s at FREEZE' % SELF
        elif why:
            res['reason'] = 'frozen_path_changed' if 'frozen' in why or 'blob' in why else why
            res['detail'] = why
        else:
            res['atoms_total'] = len(ATOM_IDS)
            sc = score(g, rev)
            res['atoms'] = {k: {'ok': not v, 'why': v} for k, v in sc.items()}
            res['mismatches'] = sum(1 for v in sc.values() if v)
            code = 0 if res['mismatches'] == 0 else 1
            if a.battery:
                b = battery(g, rev, freeze)
                res['battery'] = b
                if b['failing']:
                    code = 1
            res['exit_code'] = code
    s = json.dumps(res, indent=1, sort_keys=True)
    if a.json_out:
        with open(a.json_out, 'w') as fh:
            fh.write(s + '\n')
    print(s)
    return res['exit_code']


if __name__ == '__main__':
    sys.exit(main())
