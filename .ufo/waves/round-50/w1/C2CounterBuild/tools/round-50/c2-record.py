#!/usr/bin/env python3
"""R50-C2 counter (calibration): count mismatches between the lane's round-48/49
self-assessment record and the repository state the non-author closures observed.

DRAFT of `tools/round-50/c2-record.py`, ported from `tools/round-49/c2-mismatch.py`
(round 49).  The plan sentence is `plans/round-50-claims.md` R50-C2; this docstring, the
code and the receipt label are the same predicate.

The unit is an *atom*: one statement the lane made (or a state the repository still
carries) paired with a re-derivation from committed bytes.  An atom is a **mismatch** when
its re-derivation disagrees with the record or when the record that must correct it is
absent.  Eleven atoms, B1..B11 (`ATOMS` below is the table; the predicate text of each is
its `text` field).  The counter reads lane bytes only through git objects and never
touches the network; it needs a scratch directory (`--work` or `TMPDIR`, never `/tmp`)
only to run the B10 self-test and for `--battery` / `--selftest`.

**Two read sets.**  Every round-48/49 *input* (the round-48 closure, results file and
receipts, the round-49 lesson, closure, SCORECARD sections, `FREEZE`, `LOG.md`, the
round-49 instrument tree, the corpus snapshots S145-S149 pin) is read at the round-50
base `BASE`, never at REV: editing a historical input after the freeze cannot move an
atom.  Round-50 *outputs* (SCORECARD correction lines and rows, the SOURCES correction
rows, the SKILL registry rows, the README coverage map, the knowledge tree, the B10
self-test and its expected values) are read at REV.

**Hardening inherited from round 49 wave 2.**  (1) A line or row inside an HTML comment
(`<!-- ... -->`, an unterminated one runs to end of file) or a fenced code block (an
unterminated fence runs to end of file) does not count; lines are split on LF only, never
on the Unicode line separators `str.splitlines` also splits on.  (2) An atom line that
occurs more than once, a key repeated inside one line, an unknown key, a token that is not
`key=value`, and a registry id or correction row that occurs more than once are
mismatches, never "first wins" or "last wins".  (3) Every quote is `<= 25` words, its
stated `(N words)` equals the real count and it is located in the sha256-pinned committed
snapshot after tag removal and whitespace collapse; the heading the snapshot puts above the
quote is the locator and must be named in the row.  (4) The frozen-path walk
(`git -c core.quotePath=false log --full-history -m --no-renames --name-status -z`, plus a
blob-and-mode compare of every frozen path at FREEZE and REV) sees renames, quoted names,
mode changes, added files and touch-and-restore.  (5) The counter exits 2
`counter_not_frozen` when its own bytes differ from `tools/round-50/c2-record.py` at FREEZE.

Predicate (the same sentence as the plan): at the measured revision REV, with FREEZE an
ancestor of REV, frozen paths untouched and this file's bytes equal to FREEZE's,
`atoms_total == 11`, `mismatches == 0`, and (with `--battery`) a battery in which every
single-mutation overlay turns exactly its own atom red (none a no-op) and the do-nothing
overlay (every path changed since FREEZE restored to its FREEZE blob) turns every atom red;
exit 0.  At FREEZE the same command without `--battery` reports `mismatches N`, exit 1.

  B1  owned-axes coverage: `SCORECARD.md` `## Owned axes` coverage row at REV states, as
      its first `N/N knowledge files mapped`, N equal to the count of `corpus/knowledge/**.md`
      at REV, and every knowledge file at REV (so the round's C1 entry) is mapped by its
      backticked stem in `corpus/README.md` `## Coverage map` (`138/138` at the base vs 139).
  B2  owned-axes calibration: the `calibration` row at REV names `rejected-harmed`, the
      round-48 closure (which states `Admission: **rejected-harmed**` at BASE) and the
      round-49 receipt `.ufo/waves/round-49/l1/scores/c2-final.json`, and states
      `mismatches 9 -> 0` with both numbers re-derived from the committed round-49
      do-nothing control and `c2-final.json`.
  B3  the round-48 seat settlement: correction line `B3` (`seats reports blocked aborted
      missing`), re-derived from `.ufo/waves/round-48/r48-w1-results.json` and the `w1/`
      tree at BASE (75 results, `C1Meaning` blocked, `ScribeReportNumbers` aborted, 72
      report artifacts); the round-48 SCORECARD section at REV equals the base section
      (a correction is a new line, never a rewrite) and still carries the corrected sentence.
  B4  the round-48 per-axis verdicts: correction line `B4`, every verdict re-derived from
      the round-48 closure at BASE (quality harmed, discernment improved at decision level
      only, calibration harmed, ...); the round-48 SCORECARD section is unchanged.
  B5  the round-48 final receipts: correction line `B5` names `33f65a91` (the receipts'
      `rev`) and the lane tip `8847042a`, both raw sha256 of the two final receipts, each
      re-derived at BASE; the round-48 SCORECARD section names neither at BASE.
  B6  S149 correction row: exactly one new registry row whose teaches opens
      `supersedes S149 \u2014`, states that FreeBSD is the origin of sysexits, status
      `rejected` kept, locator `ERRORS`, the quote located in the committed snapshot
      `corpus/evidence/round-49/c2/freebsd-sysexits.html`; S149's own line unchanged.
  B7  S147 tier correction row: exactly one new row `supersedes S147 \u2014`, tier B per
      CORPUS tier text, the quote and its heading located in
      `corpus/evidence/round-49/c2/popper.html`; S147's own line unchanged.
  B8  S138 grounding row: exactly one new row `supersedes S138 \u2014`, a located quote in a
      committed pinned snapshot that grounds the census (the member count S138 states),
      with `used-by`; S138's own line unchanged.
  B9  registry census: every `tools/round-49/**` `.py`/`.sh` path at BASE and every
      `tools/round-50/**` `.py`/`.sh` path at REV (control fixtures excluded) is the cell-0
      path of exactly one row of the marker-bound `instrument-registry v2` region of
      `SKILL.md`, with a gate|probe kind, an entry command naming the path, a verdict map
      binding 0/1/2 to meanings (the round-48 meaning rule, ported), a self-test spelling
      and a pinned-value path.
  B10 `tools/round-50/selftest-r49-c2.py` exists, and run from the REV bytes against this
      repository (`--root`) it exits 0 with `failures []`; its committed expected values
      (`tools/round-50/selftest-r49-c2.expected.json`) equal its output; correction line
      `B10` states the case count and the expected-file sha256 the counter re-derives.
  B11 the round-49 declared freeze: correction line `B11` states the one freeze that the
      round-49 lesson, the round-49 SCORECARD section, `.ufo/waves/round-49/l1/FREEZE` and
      `LOG.md` all name (line numbers re-derived at BASE); it is a commit and an ancestor of
      BASE; the lesson, the SCORECARD round-49 section and the `LOG.md` prefix at REV are
      unchanged from BASE.

Freeze integrity: exit 2 when REV does not descend from FREEZE or FREEZE does not descend
from BASE, when any frozen path (`tools/round-50`, `plans/round-50-claims.md`) differs
between FREEZE and REV in the log walk or the blob-and-mode compare (`frozen_path_changed`),
or when this file differs from its FREEZE blob (`counter_not_frozen`).  The counter cannot
bind which commit the operator passes as `--freeze`; the L1 records it in
`.ufo/waves/round-50/l1/FREEZE` and `LOG.md` before any data run.

Usage:
  c2-record.py --root LANE --rev REV --freeze FREEZE [--work DIR] [--json-out PATH]
  c2-record.py --root LANE --rev REV --freeze FREEZE --battery [--work DIR] [--json-out PATH]
  c2-record.py --selftest --root LANE [--work DIR] [--json-out PATH]
Exit: 0 mismatches == 0 (and, with --battery, a clean battery; with --selftest, every
case as asserted), 1 mismatches > 0 or a battery/selftest failure, 2 unevaluable.
"""
import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = '7c678ae6d97aedb969fd253b52b3d2882ef1e186'
R48_TIP = '8847042a140b044dbf335210c965bf7b06b09b4f'
R49_FREEZE_EXPECT = None  # derived at BASE from the round-49 lesson, never a constant
ROUND_DATES = ('2026-10-28', '2026-10-29')
FROZEN = ('tools/round-50', 'plans/round-50-claims.md')
SELF = 'tools/round-50/c2-record.py'
SELFTEST_PATH = 'tools/round-50/selftest-r49-c2.py'
SELFTEST_EXPECTED = 'tools/round-50/selftest-r49-c2.expected.json'
LESSON50 = 'corpus/lessons/round-50.md'
CLOSURE48 = 'corpus/lessons/round-48-verifier-spotcheck.md'
CLOSURE49 = 'corpus/lessons/round-49-verifier-spotcheck.md'
LESSON49 = 'corpus/lessons/round-49.md'
RESULTS48 = '.ufo/waves/round-48/r48-w1-results.json'
W1_48 = '.ufo/waves/round-48/w1'
RECEIPT48 = '.ufo/waves/round-48/l1/scores/%s-final-%s.json'
C2_FINAL49 = '.ufo/waves/round-49/l1/scores/c2-final.json'
CTL49 = '.ufo/waves/round-49/controls/ctl-c2-0-do-nothing.json'
FREEZE_FILE49 = '.ufo/waves/round-49/l1/FREEZE'
CORR_HEAD = '## Record corrections \u2014 round 50'
R49_KNOWLEDGE = 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
SNAP = {'S149': 'corpus/evidence/round-49/c2/freebsd-sysexits.html',
        'S147': 'corpus/evidence/round-49/c2/popper.html'}
REG_OPEN = '<!-- instrument-registry v2 -->'
REG_CLOSE = '<!-- /instrument-registry -->'
CENSUS_BASE_PREFIX = 'tools/round-49'
CENSUS_REV_PREFIX = 'tools/round-50'
HEX40 = re.compile(r'[0-9a-f]{40}')
HEX64 = re.compile(r'[0-9a-f]{64}')
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
CORR_RE = re.compile(r'^ {0,3}- (B\d+)(?:\s+(.*))?$')
ATOM_IDS = tuple('B%d' % i for i in range(1, 12))
CORR_ATOMS = ('B3', 'B4', 'B5', 'B10', 'B11')  # atoms whose statement is a SCORECARD line
FRONT_ATOMS = {'B1', 'B2'}
ENV_KEEP = ('PATH', 'HOME', 'LANG', 'LC_ALL')

# --- verdict-meaning rule (round 48 `tools/round-48/meanings.py`, ported) ---------------
SEG = re.compile(r'(?<![0-9])([012])\s*=\s*')
SUCCESS = re.compile(r'\b(met|clean|ok|green|pass|passed|verified|succeeded|wrote)\b')
NOTMET = re.compile(r'(not met|violation|red|fail|failed|no verdict|refusal|refused|unresolved)')
UNEVAL = re.compile(r'(could-not-evaluate|unevaluable|could not evaluate|\busage\b|'
                    r'\berror\b|absent|unreadable|refus)')
NEGATED = re.compile(r'\bnot\s+met\b|\bno\s+verdict\b')
BANANA = re.compile(r'\b(banana|nope|whatever)\b')


# ------------------------------------------------------------------------ git access


class Git:
    def __init__(self, root):
        self.root = root
        self._cache = {}

    def _run(self, *args, check_env=True):
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env['GIT_NO_REPLACE_OBJECTS'] = '1'
        env['GIT_TERMINAL_PROMPT'] = '0'
        return subprocess.run(['git', '-c', 'core.quotePath=false', '-C', self.root] + list(args),
                              capture_output=True, env=env)

    def show(self, rev, path):
        k = (rev, path)
        if k not in self._cache:
            p = self._run('cat-file', 'blob', '%s:%s' % (rev, path))
            self._cache[k] = p.stdout if p.returncode == 0 else None
        return self._cache[k]

    def is_commit(self, h):
        return bool(h) and self._run('cat-file', '-e', h + '^{commit}').returncode == 0

    def ancestor(self, a, b):
        return self._run('merge-base', '--is-ancestor', a, b).returncode == 0

    def resolve(self, rev):
        p = self._run('rev-parse', '--verify', '--end-of-options', rev + '^{commit}')
        return p.stdout.decode().strip() if p.returncode == 0 else None

    def tree(self, rev, *prefixes):
        """{path: (mode, sha)} of every blob at `rev` under the pathspecs."""
        k = ('tree', rev, prefixes)
        if k in self._cache:
            return self._cache[k]
        p = self._run('ls-tree', '-r', '-z', '--full-tree', rev, '--', *prefixes)
        out = {}
        if p.returncode == 0:
            for rec in p.stdout.split(b'\0'):
                if not rec:
                    continue
                meta, _, path = rec.partition(b'\t')
                mode, _, sha = meta.decode().split(' ')
                out[path.decode('utf-8', 'surrogateescape')] = (mode, sha)
        self._cache[k] = out
        return out

    def ls(self, rev, prefix):
        return sorted(self.tree(rev, prefix))

    def touched(self, freeze, rev):
        p = self._run('log', '--full-history', '-m', '--no-renames', '--name-status', '-z',
                      '--format=%x01%H', '%s..%s' % (freeze, rev), '--', *FROZEN)
        if p.returncode != 0:
            return None
        out, cur, toks = [], None, p.stdout.decode('utf-8', 'surrogateescape').split('\0')
        i = 0
        while i < len(toks):
            t = toks[i].strip('\n')
            i += 1
            if t.startswith('\x01'):
                cur = t[1:].strip()
            elif re.fullmatch(r'[ACDMRTUXB]\d*', t) and i < len(toks):
                out.append('%s %s %s' % ((cur or '?')[:8], t, toks[i]))
                i += 1
        return out

    def changed(self, a, b):
        p = self._run('diff', '--name-only', '-z', '--no-renames', a, b)
        return [x.decode('utf-8', 'surrogateescape') for x in p.stdout.split(b'\0') if x]


class Overlay:
    """REV with some paths replaced (bytes) or removed (None).  Other revs read through."""

    def __init__(self, base, rev, over):
        self.b, self.rev, self.over = base, rev, over
        self.root = base.root

    def show(self, rev, path):
        if rev == self.rev and path in self.over:
            return self.over[path]
        return self.b.show(rev, path)

    def tree(self, rev, *prefixes):
        out = dict(self.b.tree(rev, *prefixes))
        if rev == self.rev:
            for p, v in self.over.items():
                if v is None:
                    out.pop(p, None)
                elif any(p == x or p.startswith(x.rstrip('/') + '/') for x in prefixes):
                    out[p] = ('100644', sha(v))
        return out

    def ls(self, rev, prefix):
        return sorted(self.tree(rev, prefix))

    def __getattr__(self, name):
        return getattr(self.b, name)


# ---------------------------------------------------------------------- text helpers


def sha(b):
    return hashlib.sha256(b).hexdigest()


def text(b):
    return b.decode('utf-8', 'replace') if b is not None else ''


FENCE_OPEN = re.compile(r'^ {0,3}(`{3,}|~{3,})')
INLINE_COMMENT = re.compile(r'<!--.*?-->')


def vis(t, keep=()):
    """The text a reader sees: lines inside fenced code blocks or HTML comments become empty
    lines (line numbers stay), an inline comment becomes one NUL.  An unterminated fence or
    comment runs to the end.  Lines are split on LF only.  `keep` lines (exact, stripped)
    are marker comments the caller wants preserved."""
    out, fence, cm = [], None, False
    for ln in t.split('\n'):
        if cm:
            if '-->' in ln:
                cm = False
            out.append('')
            continue
        if fence:
            m = re.match(r'^ {0,3}(`+|~+)[ \t]*$', ln)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
                fence = None
            out.append('')
            continue
        if ln.strip() in keep:
            out.append(ln)
            continue
        m = FENCE_OPEN.match(ln)
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            out.append('')
            continue
        if re.match(r'^ {0,3}<!--', ln):
            if '-->' not in ln.split('<!--', 1)[1]:
                cm = True
            out.append('')
            continue
        if '<!--' in ln:
            ln = INLINE_COMMENT.sub('\x00', ln)
            if '<!--' in ln:
                ln = ln.split('<!--', 1)[0] + '\x00'
                cm = True
        out.append(ln)
    return '\n'.join(out)


def sections(t, head):
    """Every section whose `## ` heading line starts with `head`: list of line lists.
    `t` must already be `vis`-filtered."""
    out, cur = [], None
    for l in t.split('\n'):
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
    c = [x.strip().replace('\x01', '|') for x in line.strip().replace('\\|', '\x01').split('|')]
    return c[1:-1] if len(c) >= 2 else c


def registry_rows(t):
    """{id: line}, {duplicate ids}, over `vis`-filtered SOURCES text."""
    rows, dups = {}, set()
    for l in t.split('\n'):
        m = ROW_RE.match(l)
        if m:
            if m.group(1) in rows:
                dups.add(m.group(1))
            rows[m.group(1)] = l
    return rows, dups


def strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s)


def html_norm(b):
    """Tag-stripped, entity-decoded, whitespace-collapsed body; h2/h3 headings and
    `<a id="X"><b>X</b></a>` man-page anchors become \\x01heading\\x02 markers."""
    t = text(b)
    t = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', ' ', t)
    t = re.sub(r'(?is)<h([23])[^>]*>(.*?)</h\1>',
               lambda m: ' \x01' + strip_tags(m.group(2)) + '\x02 ', t)
    t = re.sub(r'(?is)<a id="([A-Za-z][A-Za-z ]*)"[^>]*>\s*<b>\s*\1\s*</b>\s*</a>',
               lambda m: ' \x01' + m.group(1) + '\x02 ', t)
    t = html.unescape(strip_tags(t))
    return re.sub(r'\s+', ' ', t)


def snap_norm(path, b):
    if path.endswith(('.html', '.htm')):
        return html_norm(b)
    return re.sub(r'\s+', ' ', text(b))


def section_of(norm, idx):
    best = None
    for m in re.finditer('\x01(.*?)\x02', norm):
        if m.start() < idx:
            best = re.sub(r'\s+', ' ', m.group(1)).strip()
    return best


def quotes(cell):
    """[(quote, stated_word_count or None)] for every "..." with an optional (N words...)."""
    return [(m.group(1), int(m.group(2)) if m.group(2) else None)
            for m in re.finditer(r'"([^"]+)"(?:\s*\((\d+) words\b[^)]*\))?', cell)]


def line_numbers(blob, needle):
    return [i + 1 for i, l in enumerate(text(blob).split('\n')) if needle in l]


# -------------------------------------------------------------------------- context


class Ctx:
    """What an atom may read.  `b(path)` is BASE bytes, `v(path)` is REV bytes (overlaid)."""

    def __init__(self, r, rev, work, root):
        self.r, self.rev, self.work, self.root = r, rev, work, root
        self._corr = None
        self.b10_cache = {}

    def b(self, path):
        return self.r.show(BASE, path)

    def v(self, path):
        return self.r.show(self.rev, path)

    def bt(self, path):
        return text(self.b(path))

    def vt(self, path):
        return text(self.v(path))

    def corr(self):
        """({atom: [(kv dict, problems)]}, section_problem) from the round-50 correction
        section of SCORECARD.md at REV (visible text only)."""
        if self._corr is None:
            sec, bad = unique_section(vis(self.vt('SCORECARD.md')), CORR_HEAD)
            lines = {}
            if sec is not None:
                for l in sec:
                    m = CORR_RE.match(l)
                    if not m:
                        continue
                    kv, probs = {}, []
                    for tok in (m.group(2) or '').split():
                        if '=' not in tok or tok.startswith('=') or tok.endswith('='):
                            probs.append('stray token %r' % tok[:30])
                            continue
                        k, v = tok.split('=', 1)
                        if k in kv:
                            probs.append('key %s repeated' % k)
                        kv[k] = v
                    lines.setdefault(m.group(1), []).append((kv, probs))
            self._corr = (lines, bad)
        return self._corr

    def line(self, atom, keys):
        """The one `- <atom> k=v ...` line with exactly `keys`, or (None, [problems])."""
        lines, bad = self.corr()
        if bad:
            return None, [bad]
        got = lines.get(atom, [])
        if not got:
            return None, ['correction line %s absent' % atom]
        if len(got) > 1:
            return None, ['correction line %s occurs %d times' % (atom, len(got))]
        kv, probs = got[0]
        if probs:
            return None, ['line %s: %s' % (atom, '; '.join(probs))]
        if sorted(kv) != sorted(keys):
            return None, ['line %s keys %s, want exactly %s' % (atom, sorted(kv), sorted(keys))]
        return kv, []


def sec_text(t, head):
    s, bad = unique_section(vis(t), head)
    return ('\n'.join(s), None) if s is not None else (None, bad)


def keeps_sentences(c, frags):
    """Problems unless every sentence fragment of the round-48 SCORECARD section is present at
    BASE (so there is something to correct) and still present at REV (a correction is a new
    line beside the entry, never a rewrite of it)."""
    head = '## Round 48'
    a, ba = sec_text(c.bt('SCORECARD.md'), head)
    b, bb = sec_text(c.vt('SCORECARD.md'), head)
    if a is None or b is None:
        return [ba or bb]
    out = []
    for f in frags:
        if f not in a:
            out.append('base SCORECARD round-48 section lacks `%s`' % f)
        elif f not in b:
            out.append('round-48 sentence `%s` rewritten in place' % f)
    return out


# ---------------------------------------------------------------------------- atoms


def map_token(stem):
    """How the README Coverage map names an entry: a backticked `stem`, `knowledge/stem` or
    `corpus/knowledge/stem`, with or without `.md`."""
    return re.compile(r'`(?:corpus/)?(?:knowledge/)?%s(?:\.md)?`' % re.escape(stem))


def b1(c):
    out = []
    sec, bad = unique_section(vis(c.vt('SCORECARD.md')), '## Owned axes')
    if sec is None:
        return [bad]
    rows = [l for l in sec if re.match(r'^ {0,3}\|\s*coverage\s*\|', l)]
    if len(rows) != 1:
        return ['%d coverage rows in Owned axes, want 1' % len(rows)]
    fr = re.findall(r'(\d+)/(\d+) knowledge files mapped', rows[0])
    files = [p for p in c.r.ls(c.rev, 'corpus/knowledge') if p.endswith('.md')]
    if not fr:
        out.append('coverage row states no N/N knowledge files mapped')
    elif fr[0] != (str(len(files)), str(len(files))):
        out.append('coverage row states %s/%s, derived %d knowledge files' % (fr[0] + (len(files),)))
    cov, bad = unique_section(vis(c.vt('corpus/README.md')), '## Coverage map')
    if cov is None:
        return out + [bad]
    ct = '\n'.join(cov)
    unmapped = [p for p in files if not map_token(os.path.basename(p)[:-3]).search(ct)]
    if unmapped:
        out.append('knowledge files not mapped in README Coverage map: %s' % unmapped[:4])
    return out


def b2(c):
    out = []
    sec, bad = unique_section(vis(c.vt('SCORECARD.md')), '## Owned axes')
    if sec is None:
        return [bad]
    rows = [l for l in sec if re.match(r'^ {0,3}\|\s*calibration\s*\|', l)]
    if len(rows) != 1:
        return ['%d calibration rows in Owned axes, want 1' % len(rows)]
    row = rows[0]
    if 'rejected-harmed' not in row:
        out.append('calibration row does not cite the round-48 `rejected-harmed` verdict')
    if CLOSURE48 not in row:
        out.append('calibration row does not cite %s' % CLOSURE48)
    if 'Admission: **rejected-harmed**' not in vis(c.bt(CLOSURE48)):
        out.append('closure (base) does not state `Admission: **rejected-harmed**`')
    if C2_FINAL49 not in row:
        out.append('calibration row does not cite %s' % C2_FINAL49)
    try:
        fin = json.loads(c.b(C2_FINAL49))
        ctl = json.loads(c.b(CTL49))
        before, after = ctl['mismatches'], fin['mismatches']
        if fin.get('atoms_total') != 9 or fin.get('exit_code') != 0 or fin['battery']['failing']:
            out.append('round-49 c2-final is not a green 9-atom battery receipt')
    except (TypeError, ValueError, KeyError):
        return out + ['round-49 receipts unreadable at base']
    if not re.search(r'mismatches\s+%d\s*(?:\u2192|->)\s*%d\b' % (before, after), row):
        out.append('calibration row does not state `mismatches %d -> %d`' % (before, after))
    return out


def _results48(c):
    res = json.loads(c.b(RESULTS48))['results']
    names = [x['name'] for x in res]
    blocked, aborted = [], []
    for x in res:
        try:
            o = json.loads(x['output'])
        except (TypeError, ValueError):
            o = {}
        if isinstance(o, dict):
            if o.get('status') == 'blocked':
                blocked.append(x['name'])
            if o.get('aborted') is True:
                aborted.append(x['name'])
    tree = list(c.r.ls(BASE, W1_48))
    missing = []
    for n in names:
        paths = [p for p in tree if p == '%s/%s.md' % (W1_48, n)
                 or (p.startswith('%s/%s/' % (W1_48, n)) and p.endswith('.md'))]
        if not any(c.b(p) for p in paths):
            missing.append(n)
    return names, blocked, aborted, missing


def b3(c):
    d, bad = c.line('B3', ('seats', 'reports', 'blocked', 'aborted', 'missing'))
    if bad:
        return bad
    out = []
    try:
        names, blocked, aborted, missing = _results48(c)
    except (TypeError, ValueError, KeyError):
        return out + ['round-48 results file unreadable at base']
    if len(set(names)) != len(names):
        out.append('duplicate seat names in the results file')
    out += keeps_sentences(c, ['all %d seats settled' % len(names)])
    if d['seats'] != str(len(names)):
        out.append('seats stated %s, derived %d' % (d['seats'], len(names)))
    if d['reports'] != str(len(names) - len(missing)):
        out.append('reports stated %s, derived %d' % (d['reports'], len(names) - len(missing)))
    for k, derived in (('blocked', blocked), ('aborted', aborted), ('missing', missing)):
        if sorted(x for x in d[k].split(',') if x) != sorted(derived):
            out.append('%s stated %s, derived %s' % (k, d[k], sorted(derived)))
    return out


def _closure_verdicts(t):
    v = {}
    t = vis(t)
    for m in re.finditer(r'^\|\s*(coverage|depth|calibration)\s*\|\s*([a-z]+)\s*\|', t, re.M | re.I):
        v.setdefault(m.group(1).lower(), []).append(m.group(2).lower())
    for m in re.finditer(r'^- \*\*(expansion|quality|discernment)\s*\u2014\s*([a-z]+)\s*(?:\(([^)]*)\))?\.?\*\*',
                         t, re.M):
        v.setdefault(m.group(1), []).append(m.group(2))
        if m.group(3):
            v.setdefault(m.group(1) + '_scope', []).append(
                re.sub(r'[\s]+', '-', m.group(3).strip().lower()))
    return v


def b4(c):
    keys = ('coverage', 'depth', 'calibration', 'expansion', 'quality', 'discernment',
            'discernment_scope', 'source')
    d, bad = c.line('B4', keys)
    if bad:
        return bad
    out = keeps_sentences(c, ['quality **improved on the instruments**', 'discernment **improved**'])
    v = _closure_verdicts(c.bt(CLOSURE48))
    for k in keys[:-1]:
        got = v.get(k, [])
        if len(got) != 1:
            out.append('closure (base) states %s %d times, want 1' % (k, len(got)))
        elif d[k] != got[0]:
            out.append('%s stated %s, closure says %s' % (k, d[k], got[0]))
    if d['source'] != CLOSURE48:
        out.append('source is not %s' % CLOSURE48)
    if d.get('discernment_scope') != 'decision-level-only':
        out.append('discernment scope is not decision-level-only')
    return out


def b5(c):
    d, bad = c.line('B5', ('receipt', 'tip', 'c1_sha256', 'c2_sha256'))
    if bad:
        return bad
    out = []
    sc = (sec_text(c.bt('SCORECARD.md'), '## Round 48')[0] or '') + (sec_text(c.vt('SCORECARD.md'), '## Round 48')[0] or '')
    revs = set()
    for k in ('c1', 'c2'):
        try:
            rec = json.loads(c.b(RECEIPT48 % (k, d['receipt'])))
        except (TypeError, ValueError):
            out.append('receipt %s absent or unreadable at base' % (RECEIPT48 % (k, d['receipt'])))
            continue
        revs.add(rec.get('rev'))
        if d[k + '_sha256'] != sha(c.b(RECEIPT48 % (k, d['receipt']))):
            out.append('%s_sha256 stated %s, derived %s' % (
                k, d[k + '_sha256'], sha(c.b(RECEIPT48 % (k, d['receipt'])))))
    if len(revs) != 1 or not all(revs) or list(revs)[0][:8] != d['receipt']:
        out.append('receipt %s is not the 8-hex of the receipts\' rev %s' % (d['receipt'], sorted(map(str, revs))))
    else:
        rv = list(revs)[0]
        if not (c.r.is_commit(rv) and c.r.ancestor(rv, BASE)):
            out.append('the receipts\' rev is not an ancestor of BASE')
        if not c.r.ancestor(rv, R48_TIP):
            out.append('the receipts\' rev is not an ancestor of the lane tip')
    if d['tip'] != R48_TIP[:8] or not c.r.is_commit(R48_TIP) or not c.r.ancestor(R48_TIP, BASE):
        out.append('tip %s is not the round-48 lane tip %s (an ancestor of BASE)' % (d['tip'], R48_TIP[:8]))
    if d['tip'] not in c.bt(CLOSURE48) and d['tip'] not in c.bt(CLOSURE49):
        out.append('no closure at base names the tip %s' % d['tip'])
    for h in (d['receipt'], d['tip']):
        if h in sc:
            out.append('round-48 SCORECARD section already names %s (nothing to correct)' % h)
    return out


def _quote_check(out, c, norm, cell, require_headings=True):
    qs = quotes(cell)
    if not qs:
        out.append('anchor carries no quoted passage')
    heads = []
    for q, stated in qs:
        qn = re.sub(r'\s+', ' ', q).strip()
        n = len(qn.split())
        if n > 25:
            out.append('quote over 25 words (%d)' % n)
        if stated is None or stated != n:
            out.append('stated word count %s != real %d' % (stated, n))
        i = norm.find(qn)
        if i < 0:
            out.append('quote not in the committed snapshot: %s' % qn[:60])
            continue
        if norm.find(qn, i + 1) >= 0 and False:
            pass
        h = section_of(norm, i)
        heads.append(h)
        if require_headings and h and h not in cell:
            out.append('anchor does not name the snapshot heading above the quote (%s)' % h)
    return heads


def _row(c, old, snaps, kind_tier=None, same_url=True, used_by_need=(), teaches_re=()):
    """Shared structure of the B6/B7/B8 correction rows.  Returns (problems, cells, heads)."""
    out = []
    rows, dups = registry_rows(vis(c.vt('corpus/SOURCES.md')))
    base_rows, _ = registry_rows(vis(c.bt('corpus/SOURCES.md')))
    if old in dups:
        out.append('duplicate registry id %s' % old)
    if old not in base_rows:
        return ['%s absent at base' % old], None, []
    if rows.get(old) != base_rows[old]:
        out.append('%s was rewritten (append-only)' % old)
    new = [i for i in rows if i not in base_rows]
    mine = [i for i in new if len(cells(rows[i])) > 6
            and cells(rows[i])[6].startswith('supersedes %s \u2014' % old)]
    any_sup = [i for i, l in rows.items() if len(cells(l)) > 6
               and cells(l)[6].startswith('supersedes %s' % old) and i not in base_rows]
    if len(mine) != 1 or len(any_sup) != 1:
        return out + ['%d new rows open `supersedes %s \u2014`, want exactly 1' % (len(any_sup), old)], None, []
    rid = mine[0]
    if rid in dups:
        out.append('duplicate registry id %s' % rid)
    cl = cells(rows[rid])
    oc = cells(base_rows[old])
    if len(cl) != 11:
        return out + ['%s has %d cells, want 11' % (rid, len(cl))], None, []
    tier = kind_tier or oc[3]
    if cl[2] != oc[2] or cl[3] != tier or cl[7] != oc[7]:
        out.append('%s kind/tier/status %s, want %s' % (rid, cl[2:4] + cl[7:8], [oc[2], tier, oc[7]]))
    if cl[8] not in ROUND_DATES:
        out.append('%s opened %s not in %s' % (rid, cl[8], ROUND_DATES))
    if same_url:
        urls = re.findall(r'https?://\S+', oc[1])
        if not urls or urls[0] not in cl[1]:
            out.append('%s source does not carry the corrected row\'s URL' % rid)
    for pat in teaches_re:
        if not re.search(pat, cl[6], re.I | re.S):
            out.append('%s teaches lacks /%s/' % (rid, pat))
    paths = [p for p in re.findall(r'corpus/evidence/[A-Za-z0-9._/\-]+', cl[5])]
    paths = [p.rstrip('.') for p in paths]
    for need in snaps:
        if need not in paths:
            out.append('%s anchor does not cite the snapshot %s' % (rid, need))
    pinned = []
    for p in dict.fromkeys(paths):
        b = c.v(p)
        if b is None:
            out.append('snapshot %s absent at REV' % p)
        elif sha(b) not in HEX64.findall(cl[5]):
            out.append('%s anchor does not pin the sha256 %s of %s' % (rid, sha(b), p))
        else:
            pinned.append((p, b))
    if not pinned:
        out.append('%s cites no committed pinned snapshot' % rid)
    heads = []
    if pinned:
        norm = ' '.join(snap_norm(p, b) for p, b in pinned)
        if len(pinned) > 1:  # headings are per file; compare quote by quote
            for p, b in pinned:
                heads += _quote_check([], c, snap_norm(p, b), cl[5], False)
            for q, stated in quotes(cl[5]):
                qn = re.sub(r'\s+', ' ', q).strip()
                if not any(qn in snap_norm(p, b) for p, b in pinned):
                    out.append('quote not in any pinned snapshot: %s' % qn[:60])
                if stated is None or stated != len(qn.split()) or len(qn.split()) > 25:
                    out.append('quote word count wrong or over 25: %s' % qn[:40])
        else:
            heads = _quote_check(out, c, snap_norm(*pinned[0]), cl[5])
    ub = cl[10]
    ubp = re.findall(r'(?:corpus|tools|plans|\.ufo)/[A-Za-z0-9._/\-]+', ub)
    if not ubp:
        out.append('%s used-by names no path' % rid)
    for p in ubp:
        if c.v(p.rstrip('.')) is None and not c.r.ls(c.rev, p.rstrip('.')):
            out.append('%s used-by path absent at REV: %s' % (rid, p))
    for need in used_by_need:
        if need not in ub:
            out.append('%s used-by does not list %s' % (rid, need))
    return out, cl, heads


def b6(c):
    out, cl, heads = _row(
        c, 'S149', [SNAP['S149']], used_by_need=(LESSON50,),
        teaches_re=(r'FreeBSD\b.{0,120}\borigin\b|\borigin\b.{0,120}\bFreeBSD\b', r'sysexits'))
    if cl is not None:
        if 'ERRORS' not in heads:
            out.append('no quote of the row sits under the snapshot heading ERRORS')
        if '`ERRORS`' not in cl[5]:
            out.append('anchor does not name the locator `ERRORS`')
        if cl[7] != 'rejected':
            out.append('status is not `rejected`')
    return out


def b7(c):
    out, cl, heads = _row(
        c, 'S147', [SNAP['S147']], kind_tier='B', used_by_need=(LESSON50,),
        teaches_re=(r'\btier B\b', r'CORPUS'))
    if cl is not None and cl[3] != 'B':
        out.append('tier is not B')
    return out


def b8(c):
    base_rows, _ = registry_rows(vis(c.bt('corpus/SOURCES.md')))
    m = re.search(r'(\d+) files', base_rows.get('S138', ''))
    n = m.group(1) if m else None
    pats = [r'\bcensus\b', r'\b%s[- ]member\b|\b%s members?\b|\b%s files\b' % ((n or 'N/A',) * 3)]
    out, cl, heads = _row(c, 'S138', [], same_url=False,
                          used_by_need=(R49_KNOWLEDGE,), teaches_re=pats)
    if n is None:
        out.append('S138 at base states no `N files` census to ground')
    return out


def meaning_classes(cell):
    text_ = cell.strip()
    marks = list(SEG.finditer(text_))
    if [m.group(1) for m in marks] != ['0', '1', '2']:
        return 'verdict map does not parse as 0=;1=;2='
    segs = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text_)
        segs[m.group(1)] = text_[m.end():end].strip().rstrip(';').strip().lower()
    if BANANA.search(' '.join(segs.values())):
        return 'placeholder text in the verdict map'
    if not (SUCCESS.search(segs['0']) and not NEGATED.search(segs['0'])):
        return 'exit 0 segment names no success meaning'
    if not NOTMET.search(segs['1']):
        return 'exit 1 segment names no not-met meaning'
    if not UNEVAL.search(segs['2']):
        return 'exit 2 segment names no unevaluable meaning'
    if len(set(segs.values())) != 3:
        return 'verdict segments are not three distinct meanings'
    return None


def registry_region(t):
    """Rows (path -> list of cell lists) of the one marker-bound registry region of
    SKILL.md at REV, visible text only; (rows, problem)."""
    v = vis(t, keep=(REG_OPEN, REG_CLOSE))
    lines = v.split('\n')
    o = [i for i, l in enumerate(lines) if l.strip() == REG_OPEN]
    cl = [i for i, l in enumerate(lines) if l.strip() == REG_CLOSE]
    if len(o) != 1 or len(cl) != 1 or o[0] >= cl[0]:
        return None, 'registry markers absent, doubled or reversed (%d/%d)' % (len(o), len(cl))
    rows = {}
    for l in lines[o[0] + 1:cl[0]]:
        if re.match(r'^ {0,3}\|\s*`', l):
            cs = cells(l)
            rows.setdefault(cs[0].strip('` ') if cs else '', []).append(cs)
    return rows, None


def census_paths(c):
    def pick(rev, prefix):
        return [p for p in c.r.ls(rev, prefix)
                if p.endswith(('.py', '.sh')) and '/control-fixtures/' not in p + '/']
    return pick(BASE, CENSUS_BASE_PREFIX) + pick(c.rev, CENSUS_REV_PREFIX)


def b9(c):
    rows, bad = registry_region(c.vt('SKILL.md'))
    if rows is None:
        return [bad]
    out = []
    paths = census_paths(c)
    if not any(p.startswith(CENSUS_BASE_PREFIX) for p in paths):
        return ['no %s instruments at base: census empty' % CENSUS_BASE_PREFIX]
    for p in paths:
        got = rows.get(p, [])
        if not got:
            out.append('%s: no registry row' % p)
            continue
        if len(got) > 1:
            out.append('%s: %d registry rows, want 1' % (p, len(got)))
            continue
        cs = got[0]
        if len(cs) != 7:
            out.append('%s: row has %d cells, want 7' % (p, len(cs)))
            continue
        if not re.match(r'(?i)(gate|probe)\b', cs[1]):
            out.append('%s: kind cell does not open gate|probe' % p)
        entry = r'(?:python3?|bash|sh|node)\s+(?:-\S+\s+)*(?:\./)?' + re.escape(p) + r'(?![\w./\-])'
        if not any(re.search(entry, x) for x in cs[1:5]):
            out.append('%s: no entry command naming the path' % p)
        why = meaning_classes(cs[2])
        if why:
            out.append('%s: %s' % (p, why))
        st = cs[3]
        if not (re.match(r'(?:python3?|bash|sh)\s+(?:-\S+\s+)*(?:\./)?' + re.escape(p) +
                         r'\b.*--selftest', st)
                or re.match(r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){2,}', st)):
            out.append('%s: self-test cell is neither `<interpreter> %s ... --selftest` nor `none \u2014 <reason>`' % (p, p))
        pin = cs[4]
        if not (re.match(r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){1,}', pin)
                or re.search(r'[\w.\-]+/[\w./\-]*|\b[\w\-]+\.(?:json|tsv|md|py|sh|txt|html)\b', pin)):
            out.append('%s: pinned-value cell names no path and is not `none \u2014 <reason>`' % p)
    return out


def export_tree(c, dest):
    """Write the REV (overlaid) `tools/round-50` tree under dest/tools/round-50."""
    n = 0
    for p in c.r.ls(c.rev, 'tools/round-50'):
        b = c.v(p)
        if b is None:
            continue
        fp = os.path.join(dest, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'wb') as fh:
            fh.write(b)
        n += 1
    return n


def run_selftest_r49(c):
    """(result dict or None, problems)"""
    if not c.work:
        return None, ['no scratch root for the B10 run']
    st, ex = c.v(SELFTEST_PATH), c.v(SELFTEST_EXPECTED)
    if st is None:
        return None, ['%s absent at REV' % SELFTEST_PATH]
    if ex is None:
        return None, ['%s absent at REV' % SELFTEST_EXPECTED]
    key = sha(st + b'\0' + ex)
    if key in c.b10_cache:
        return c.b10_cache[key]
    os.makedirs(c.work, exist_ok=True)
    dest = tempfile.mkdtemp(prefix='b10-', dir=c.work)
    try:
        export_tree(c, dest)
        env = {k: os.environ[k] for k in ENV_KEEP if k in os.environ}
        env['TMPDIR'] = c.work
        jo = os.path.join(dest, 'out.json')
        try:
            p = subprocess.run([sys.executable, '-I', '-B', os.path.join(dest, SELFTEST_PATH),
                                '--root', c.root, '--work', dest, '--json-out', jo],
                               capture_output=True, cwd=dest, env=env, timeout=900)
        except subprocess.TimeoutExpired:
            res = (None, ['B10 self-test timed out'])
        else:
            try:
                data = json.load(open(jo))
            except (OSError, ValueError):
                data = None
            probs = []
            if p.returncode != 0:
                probs.append('self-test exit %d' % p.returncode)
            if not isinstance(data, dict):
                probs.append('self-test wrote no JSON result')
                data = None
            else:
                if data.get('failures') != []:
                    probs.append('self-test failures %s' % str(data.get('failures'))[:120])
                if not isinstance(data.get('cases'), int) or data['cases'] < 1:
                    probs.append('self-test ran no cases')
                if data.get('expected_sha256') != sha(ex):
                    probs.append('self-test did not compare against the committed expected file')
            res = (data, probs)
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    c.b10_cache[key] = res
    return res


def b10(c):
    d, bad = c.line('B10', ('selftest', 'cases', 'expected_sha256'))
    if bad:
        return bad
    out = []
    data, probs = run_selftest_r49(c)
    out += probs
    if d['selftest'] != SELFTEST_PATH:
        out.append('selftest is not %s' % SELFTEST_PATH)
    if data is not None:
        if d['cases'] != str(data.get('cases')):
            out.append('cases stated %s, self-test ran %s' % (d['cases'], data.get('cases')))
        if d['expected_sha256'] != data.get('expected_sha256'):
            out.append('expected_sha256 stated %s, self-test compared %s' % (
                d['expected_sha256'], data.get('expected_sha256')))
    try:
        ex = json.loads(c.v(SELFTEST_EXPECTED) or b'')
        if not ex:
            out.append('expected file is empty')
    except ValueError:
        out.append('expected file is not JSON')
    return out


def b11(c):
    keys = ('freeze', 'lesson_line', 'scorecard_line', 'freeze_file', 'log_lines')
    d, bad = c.line('B11', keys)
    if bad:
        return bad
    out = []
    lesson = c.b(LESSON49)
    hits = [(i + 1, m.group(1)) for i, l in enumerate(text(lesson).split('\n'))
            for m in re.finditer(r'Declared freeze\s+`([0-9a-f]{40})`', l)]
    sc, _ = sec_text(c.bt('SCORECARD.md'), '## Round 49')
    scl = [(i + 1, m.group(1)) for i, l in enumerate(c.bt('SCORECARD.md').split('\n'))
           for m in re.finditer(r'\*\*Declared freeze:\*\*\s*`([0-9a-f]{40})`', l)
           if sc is not None and l in sc.split('\n') and 'Base `' in l]
    ff = text(c.b(FREEZE_FILE49)).strip()
    if len(hits) != 1:
        return ['round-49 lesson names %d declared freezes, want 1' % len(hits)]
    f = hits[0][1]
    if len(scl) != 1 or scl[0][1] != f:
        out.append('round-49 SCORECARD section declared freeze %s != lesson %s' % (scl, f))
    if ff != f:
        out.append('%s holds %s != lesson %s' % (FREEZE_FILE49, ff, f))
    log = c.b('LOG.md')
    ll = line_numbers(log, f[:8]) if log is not None else []
    if not ll:
        out.append('LOG.md (base) never names %s' % f[:8])
    if not (c.r.is_commit(f) and c.r.ancestor(f, BASE)):
        out.append('%s is not a commit that is an ancestor of BASE' % f[:8])
    if d['freeze'] != f:
        out.append('freeze stated %s, derived %s' % (d['freeze'], f))
    if d['lesson_line'] != str(hits[0][0]):
        out.append('lesson_line stated %s, derived %d' % (d['lesson_line'], hits[0][0]))
    if scl and d['scorecard_line'] != str(scl[0][0]):
        out.append('scorecard_line stated %s, derived %d' % (d['scorecard_line'], scl[0][0]))
    if d['freeze_file'] != FREEZE_FILE49:
        out.append('freeze_file is not %s' % FREEZE_FILE49)
    if sorted(x for x in d['log_lines'].split(',') if x) != [str(x) for x in ll]:
        out.append('log_lines stated %s, derived %s' % (d['log_lines'], ll))
    now = c.v('LOG.md')
    if log is None or now is None or not now.startswith(log):
        out.append('LOG.md at REV does not begin with the base blob (not append-only)')
    if c.v(LESSON49) != lesson:
        out.append('round-49 lesson rewritten (not byte-identical to base)')
    a = sec_text(c.bt('SCORECARD.md'), '## Round 49')[0]
    b = sec_text(c.vt('SCORECARD.md'), '## Round 49')[0]
    if a is None or a != b:
        out.append('round-49 SCORECARD section differs from the base')
    return out


# The atom table.  `text` is the predicate clause (see the docstring); `fn(ctx)` returns the
# list of mismatch reasons (empty = the atom holds).  Adjust a clause here and in the
# docstring together.
ATOMS = [
    ('B1', 'coverage fraction = knowledge-file count at REV, every file mapped', b1),
    ('B2', 'calibration row cites rejected-harmed and the c2-final measure', b2),
    ('B3', 'round-48 seat settlement correction (75/72, blocked, aborted)', b3),
    ('B4', 'round-48 per-axis verdict correction', b4),
    ('B5', 'round-48 final receipts 33f65a91 / tip 8847042a named', b5),
    ('B6', 'S149 correction row (FreeBSD origin, ERRORS, rejected kept)', b6),
    ('B7', 'S147 tier B correction row', b7),
    ('B8', 'S138 census grounding row', b8),
    ('B9', 'registry census: tools/round-49 at base + tools/round-50 at REV', b9),
    ('B10', 'selftest-r49-c2.py expected values equal its output', b10),
    ('B11', 'round-49 declared freeze: lesson, SCORECARD, FREEZE, LOG agree', b11),
]
assert tuple(a[0] for a in ATOMS) == ATOM_IDS


def score(c):
    res = {}
    for k, _, fn in ATOMS:
        try:
            res[k] = fn(c)
        except Exception as e:  # an atom that crashes is a mismatch, never a pass
            res[k] = ['atom crashed: %r' % (e,)]
    return res


# ------------------------------------------------------------------ freeze integrity


def freeze_check(r, freeze, rev):
    if not r.ancestor(BASE, freeze):
        return 'freeze does not descend from BASE', 'bad_freeze'
    if not r.ancestor(freeze, rev):
        return 'freeze is not an ancestor of rev', 'bad_freeze'
    t = r.touched(freeze, rev)
    if t is None:
        return 'cannot walk FREEZE..REV', 'cannot_walk'
    if t:
        return 'frozen path touched in FREEZE..REV: %s' % ';'.join(t[:6]), 'frozen_path_changed'
    a, b = r.tree(freeze, *FROZEN), r.tree(rev, *FROZEN)
    diff = sorted(p for p in set(a) | set(b) if a.get(p) != b.get(p))
    if diff:
        return 'frozen blob or mode differs: %s' % ';'.join(diff[:6]), 'frozen_path_changed'
    return None, None


# --------------------------------------------------------------------------- battery


def _line_of(c, atom):
    t = c.vt('SCORECARD.md')
    for l in t.split('\n'):
        m = CORR_RE.match(l)
        if m and m.group(1) == atom:
            return l
    return None


def mutations(c):
    """(label, atom it must flip, overlay dict) -- each from REV's own bytes."""
    muts = []
    sc = c.vt('SCORECARD.md')
    soc = c.vt('corpus/SOURCES.md')

    def screp(label, atom, a, b, count=1):
        if a in sc:
            muts.append((label, atom, {'SCORECARD.md': sc.replace(a, b, count).encode()}))

    # B1 / B2: Owned-axes rows
    m = re.search(r'(\d+)/(\d+) knowledge files mapped', sc[sc.find('| coverage'):])
    if m and sc.find('| coverage') >= 0:
        muts.append(('B1 coverage fraction off by one', 'B1', {'SCORECARD.md': (
            sc[:sc.find('| coverage')] + sc[sc.find('| coverage'):].replace(
                m.group(0), '%d/%d knowledge files mapped' % (int(m.group(1)) + 1, int(m.group(2)) + 1), 1)
        ).encode()}))
    rd = c.vt('corpus/README.md')
    cm = rd.find('## Coverage map')
    if cm >= 0:
        end = rd.find('\n## ', cm + 5)
        span = rd[cm:end if end > 0 else len(rd)]
        files = sorted(p for p in c.r.ls(c.rev, 'corpus/knowledge') if p.endswith('.md'))
        added = [p for p in files if p not in c.r.ls(BASE, 'corpus/knowledge')] or files[-1:]
        stem = os.path.basename(added[-1])[:-3]
        if map_token(stem).search(span):
            muts.append(('B1 one knowledge entry unmapped', 'B1', {
                'corpus/README.md': (rd[:cm] + map_token(stem).sub('`unmapped-stem`', span) + rd[cm + len(span):]).encode()}))
    ci = sc.find('| calibration')
    if ci >= 0:
        row_end = sc.find('\n', ci)
        row = sc[ci:row_end]
        for label, a, b in (('B2 rejected-harmed dropped', 'rejected-harmed', 'rejected-x'),
                            ('B2 c2-final path broken', 'c2-final.json', 'c2-finalx.json')):
            if a in row:
                muts.append((label, 'B2', {'SCORECARD.md': (sc[:ci] + row.replace(a, b) + sc[row_end:]).encode()}))
    # correction lines: value tweak + the four structural forgeries
    tweaks = {'B3': ('seats=75', 'seats=76'), 'B4': ('quality=harmed', 'quality=improved'),
              'B5': (r'c1_sha256=[0-9a-f]{64}', 'c1_sha256=' + '0' * 64),
              'B10': ('cases=', 'cases=9'), 'B11': (r'log_lines=[0-9,]+', 'log_lines=1')}
    for atom, (a, b) in tweaks.items():
        ln = _line_of(c, atom)
        if ln is None:
            continue
        new = re.sub(a, b, ln, count=1) if a.startswith('c1_') or a.startswith('log_') else ln.replace(a, b, 1)
        if new != ln:
            muts.append(('%s value tweaked' % atom, atom, {'SCORECARD.md': sc.replace(ln, new, 1).encode()}))
        muts.append(('%s duplicate line' % atom, atom, {'SCORECARD.md': (sc.rstrip('\n') + '\n' + ln + '\n').encode()}))
        muts.append(('%s line in an HTML comment' % atom, atom, {'SCORECARD.md': sc.replace(ln, '<!--\n%s\n-->' % ln, 1).encode()}))
        muts.append(('%s line in a fenced block' % atom, atom, {'SCORECARD.md': sc.replace(ln, '```\n%s\n```' % ln, 1).encode()}))
        muts.append(('%s repeated key in the line' % atom, atom, {'SCORECARD.md': sc.replace(ln, ln + ' ' + ln.split()[2], 1).encode()}))
    # round-48 section rewritten in place (B3/B4/B5 each read it): one mutation each
    if 'all 75 seats settled' in sc:
        muts.append(('B3 round-48 sentence rewritten in place', 'B3', {
            'SCORECARD.md': sc.replace('all 75 seats settled', 'all 72 seats settled', 1).encode()}))
    m48 = re.search(r'(?ms)^## Round 48.*?(?=^## |\Z)', sc)
    if m48:
        sec48 = m48.group(0)
        if 'quality **improved on the instruments**' in sec48:
            muts.append(('B4 round-48 trend sentence rewritten in place', 'B4', {
                'SCORECARD.md': sc.replace(sec48, sec48.replace('quality **improved on the instruments**',
                                                               'quality **harmed**', 1), 1).encode()}))
        muts.append(('B5 round-48 section already names the receipts', 'B5', {
            'SCORECARD.md': sc.replace(sec48, sec48.replace('Waves:', '33f65a91 Waves:', 1), 1).encode()}))
    # SOURCES rows
    rows, _ = registry_rows(vis(soc))
    base_rows, _ = registry_rows(vis(c.bt('corpus/SOURCES.md')))
    byold = {}
    for i, l in rows.items():
        cs = cells(l)
        if i not in base_rows and len(cs) > 6:
            mm = re.match(r'supersedes (S\d+) \u2014', cs[6])
            if mm:
                byold[mm.group(1)] = (i, l, cs)

    def rowrep(label, atom, old, a, b, idx=None):
        """Replace every `a` in the correction row for `old` (or only in cell `idx`)."""
        if old not in byold:
            return
        line = byold[old][1]
        if idx is None:
            new = line.replace(a, b)
        else:
            cs = cells(line)
            cs[idx] = cs[idx].replace(a, b)
            new = '| ' + ' | '.join(cs) + ' |'
        if new != line:
            muts.append((label, atom, {'corpus/SOURCES.md': soc.replace(line, new, 1).encode()}))

    rowrep('B6 locator changed to DESCRIPTION', 'B6', 'S149', '`ERRORS`', '`DESCRIPTION`')
    rowrep('B6 status flipped to mined', 'B6', 'S149', '| rejected |', '| mined |')
    rowrep('B6 the origin statement removed', 'B6', 'S149', 'origin', 'oddity')
    rowrep('B7 tier changed to A', 'B7', 'S147', '| B |', '| A |')
    if 'S147' in byold:
        rowrep('B7 stated word count wrong', 'B7', 'S147', '(21 words', '(7 words')
    rowrep('B8 census number changed in teaches', 'B8', 'S138', '22', '23', idx=6)
    for old, atom in (('S149', 'B6'), ('S147', 'B7'), ('S138', 'B8')):
        if old in byold:
            i, l, cs = byold[old]
            muts.append(('%s correction row in an HTML comment' % atom, atom, {
                'corpus/SOURCES.md': soc.replace(l, '<!--\n%s\n-->' % l, 1).encode()}))
            muts.append(('%s correction row duplicated' % atom, atom, {
                'corpus/SOURCES.md': (soc.rstrip('\n') + '\n' + l + '\n').encode()}))
    if 'S149' in byold:
        b = c.v(SNAP['S149'])
        if b:
            muts.append(('B6 snapshot bytes edited', 'B6', {SNAP['S149']: b.replace(b'EX_USAGE', b'EX_USAGF')}))
    if 'S147' in byold:
        b = c.v(SNAP['S147'])
        if b:
            muts.append(('B7 snapshot bytes edited', 'B7', {SNAP['S147']: b.replace(b'empirical', b'empirica1')}))
    # B9 registry
    sk = c.vt('SKILL.md')
    target = 'tools/round-49/c2-mismatch.py'
    for l in sk.split('\n'):
        if re.match(r'^ {0,3}\|\s*`%s`' % re.escape(target), l):
            cs = cells(l)
            if len(cs) == 7:
                muts.append(('B9 registry row for %s in an HTML comment' % target, 'B9', {
                    'SKILL.md': sk.replace(l, '<!--\n%s\n-->' % l, 1).encode()}))
                bad = list(cs)
                bad[2] = '0=banana; 1=nope; 2=whatever'
                muts.append(('B9 verdict map is placeholder text', 'B9', {
                    'SKILL.md': sk.replace(l, '| ' + ' | '.join(bad) + ' |', 1).encode()}))
                bad = list(cs)
                bad[1] = 'tool \u2014 ' + re.sub(r'^\S+\s*[\u2014-]?\s*', '', cs[1])
                muts.append(('B9 kind cell is not gate|probe', 'B9', {
                    'SKILL.md': sk.replace(l, '| ' + ' | '.join(bad) + ' |', 1).encode()}))
                bad = list(cs)
                bad[3] = 'maybe'
                muts.append(('B9 self-test cell is neither spelling nor none', 'B9', {
                    'SKILL.md': sk.replace(l, '| ' + ' | '.join(bad) + ' |', 1).encode()}))
                muts.append(('B9 row duplicated', 'B9', {
                    'SKILL.md': sk.replace(l, l + '\n' + l, 1).encode()}))
            break
    # B10 expected values
    ex = c.v(SELFTEST_EXPECTED)
    if ex:
        muts.append(('B10 expected file value changed', 'B10', {SELFTEST_EXPECTED: ex + b' ' if False else
                                                             re.sub(rb'\d', lambda m: b'7' if m.group(0) != b'7' else b'8', ex, count=1)}))
    return muts


def battery(r, rev, freeze, work, root):
    c = Ctx(r, rev, work, root)
    muts = mutations(c)
    out = {'green': score(c), 'mutations': [], 'failing': [], 'mutation_count': len(muts)}
    if any(out['green'].values()):
        out['failing'].append('genuine REV is not green')
    have = {m[1] for m in muts}
    for k in ATOM_IDS:
        if k not in have:
            out['failing'].append('no mutation realized for atom %s' % k)
    for label, atom, over in muts:
        noop = [p for p, v in over.items() if v == r.show(rev, p)]
        cc = Ctx(Overlay(r, rev, over), rev, work, root)
        cc.b10_cache = c.b10_cache
        got = score(cc)
        red = sorted(k for k, v in got.items() if v)
        ok = red == [atom] and not noop
        out['mutations'].append({'label': label, 'atom': atom, 'red': red, 'noop': noop, 'ok': ok})
        if not ok:
            out['failing'].append('%s -> red %s noop %s' % (label, red, noop))
    changed = r.changed(freeze, rev)
    dn_over = {x: r.show(freeze, x) for x in changed}
    cc = Ctx(Overlay(r, rev, dn_over), rev, work, root)
    cc.b10_cache = c.b10_cache
    dn = score(cc)
    red = sorted(k for k, v in dn.items() if v)
    out['do_nothing_red'] = red
    out['do_nothing_paths'] = len(changed)
    if red != sorted(ATOM_IDS, key=lambda x: x):
        out['failing'].append('do-nothing overlay red %s, want all %d' % (red, len(ATOM_IDS)))
    return out


# --------------------------------------------------------------------------- driver


def scratch_root(arg_work):
    w = arg_work or os.environ.get('TMPDIR')
    if not w:
        return None
    w = os.path.abspath(w)
    if w == '/tmp' or w.startswith('/tmp/'):
        return None
    os.makedirs(w, exist_ok=True)
    return w


def evaluate(root, rev_arg, freeze_arg, do_battery=False, work=None, own_path=None):
    """The counter proper; returns the result dict (exit_code inside)."""
    root = os.path.abspath(root)
    g = Git(root)
    rev, freeze = g.resolve(rev_arg), g.resolve(freeze_arg)
    own = open(own_path or __file__, 'rb').read()
    res = {'schema': 'kaidoku-r50-c2-v1', 'base': BASE, 'rev': rev, 'freeze': freeze,
           'counter_sha256': sha(own), 'exit_code': 2}
    if not rev or not freeze or not g.is_commit(BASE):
        res['reason'] = 'unresolvable rev, freeze or base'
        return res
    wk = scratch_root(work)
    if wk is None:
        res['reason'] = 'no_scratch_root'
        res['detail'] = 'pass --work DIR or set TMPDIR (never /tmp)'
        return res
    at_freeze = g.show(freeze, SELF)
    res['counter_sha256_at_freeze'] = sha(at_freeze) if at_freeze is not None else None
    why, kind = freeze_check(g, freeze, rev)
    if at_freeze is None or sha(at_freeze) != sha(own):
        res['reason'] = 'counter_not_frozen'
        res['detail'] = 'this file differs from %s at FREEZE' % SELF
        return res
    if why:
        res['reason'] = kind
        res['detail'] = why
        return res
    c = Ctx(g, rev, wk, root)
    sc = score(c)
    res['atoms_total'] = len(ATOM_IDS)
    res['atoms'] = {k: {'ok': not v, 'why': v} for k, v in sc.items()}
    res['mismatches'] = sum(1 for v in sc.values() if v)
    code = 0 if res['mismatches'] == 0 else 1
    if do_battery:
        b = battery(g, rev, freeze, wk, root)
        res['battery'] = b
        if b['failing']:
            code = 1
    res['exit_code'] = code
    return res


# -------------------------------------------------------------------- green fixture
# The fixture builder: text for every atom's record, written against the real BASE, from
# LITERAL values (not through the counter's derivations).  Used by --selftest and by the
# seat harness that builds the GREEN scratch clone.  Fixture text is synthetic: it states
# what the atoms need and is not the L1's landing text.

LIT = {
    'c1_sha': '6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e',
    'c2_sha': 'd1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914',
    'freebsd_sha': '1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf',
    'popper_sha': '2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207',
    'r49_freeze': 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d',
}
S138_SNAP = 'corpus/evidence/round-50/c2/s138-census-listing.txt'
S138_SNAP_TEXT = ('FIXTURE listing (synthetic, selftest only).\n'
                  'The unblob 26.6.4 expected trees hold 22 members across the four endian '
                  'trees.\n')


def _ln(base_text, needle):
    return [i + 1 for i, l in enumerate(base_text.split('\n')) if needle in l]


def build_green(r, stand_in_selftest=None):
    """{path: bytes} overlay that makes every atom green at a REV built from BASE (+ the
    FREEZE contents the caller commits).  `r` reads BASE objects."""
    def base(p):
        return text(r.show(BASE, p))
    ov = {}
    sc = base('SCORECARD.md')
    n_files = len([p for p in r.ls(BASE, 'corpus/knowledge') if p.endswith('.md')]) + 1
    sc = sc.replace('138/138 knowledge files mapped at the round-47 landing',
                    '%d/%d knowledge files mapped at the round-50 landing' % (n_files, n_files), 1)
    i = sc.find('| calibration |')
    j = sc.find('\n', i)
    sc = (sc[:j] + ' Round 50: the round-48 closure `corpus/lessons/round-48-verifier-spotcheck.md` '
          'graded calibration `rejected-harmed`; the round-49 record corrections measured '
          '`mismatches 9 \u2192 0` (`.ufo/waves/round-49/l1/scores/c2-final.json`).' + sc[j:]) if i >= 0 else sc
    # the one correction section, appended last
    lesson49 = base(LESSON49)
    lesson_line = _ln(lesson49, 'Declared freeze `' + LIT['r49_freeze'] + '`')[0]
    sc_lines = base('SCORECARD.md').split('\n')
    sc_line = [k + 1 for k, l in enumerate(sc_lines) if '**Declared freeze:** `' + LIT['r49_freeze'] + '`' in l][0]
    log_lines = ','.join(str(x) for x in _ln(base('LOG.md'), LIT['r49_freeze'][:8]))
    sc = sc.rstrip('\n') + '\n\n' + CORR_HEAD + '\n\n' + '\n'.join([
        '- B3 seats=75 reports=72 blocked=C1Meaning aborted=ScribeReportNumbers '
        'missing=C1Battery,C1Meaning,ScribeReportNumbers',
        '- B4 coverage=unchanged depth=improved calibration=harmed expansion=unchanged '
        'quality=harmed discernment=improved discernment_scope=decision-level-only '
        'source=' + CLOSURE48,
        '- B5 receipt=33f65a91 tip=8847042a c1_sha256=%s c2_sha256=%s' % (LIT['c1_sha'], LIT['c2_sha']),
        '- B10 selftest=%s cases=%%CASES%% expected_sha256=%%EXPSHA%%' % SELFTEST_PATH,
        '- B11 freeze=%s lesson_line=%d scorecard_line=%d freeze_file=%s log_lines=%s' % (
            LIT['r49_freeze'], lesson_line, sc_line, FREEZE_FILE49, log_lines)]) + '\n'
    ov['SCORECARD.md'] = sc  # %CASES%/%EXPSHA% filled by the caller after the selftest files exist
    # SOURCES rows
    soc = base('corpus/SOURCES.md').rstrip('\n')
    rows = [
        '| S150 | sysexits(3) FreeBSD manual, correction of S149 \u2014 '
        'https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 | docs | C | the reason and locator of S149 '
        'only | `ERRORS`: "EX_USAGE (64) The command was used incorrectly" (7 words, verbatim, under the `ERRORS` '
        'heading); snapshot `corpus/evidence/round-49/c2/freebsd-sysexits.html`, sha256 `%s` | supersedes S149 \u2014 '
        'FreeBSD is the origin of sysexits and the page carries the EX_USAGE gloss under ERRORS; S149 inverted '
        'the provenance | rejected | 2026-10-28 | on-request | `%s` |' % (LIT['freebsd_sha'], LESSON50),
        '| S151 | Stanford Encyclopedia of Philosophy, Karl Popper \u2014 https://plato.stanford.edu/entries/popper/ '
        '| docs | B | the tier of S147 only | `2. Backdrop to Popper\u2019s Thought`: "falsifiability as his criterion for '
        'demarcating science from non-science: if a theory is incompatible with possible empirical observations it '
        'is scientific" (21 words); snapshot `corpus/evidence/round-49/c2/popper.html`, sha256 `%s` | supersedes '
        'S147 \u2014 tier B per CORPUS tier text (strong secondary survey), not A | mined | 2026-10-28 | 365d | `%s` |'
        % (LIT['popper_sha'], LESSON50),
        '| S152 | unblob 26.6.4 SquashFS expected-tree listing, census grounding of S138 \u2014 '
        'https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs | dataset | A | '
        'the 22-member census only | "The unblob 26.6.4 expected trees hold 22 members across the four endian '
        'trees." (13 words); snapshot `%s`, sha256 `%%S138SHA%%` | supersedes S138 \u2014 the census of 22 files '
        'rests on the fetched member listing, not the directory name | mined | 2026-10-28 | 365d | '
        '`%s`, `%s` |' % (S138_SNAP, LESSON50, R49_KNOWLEDGE),
    ]
    snap = S138_SNAP_TEXT.encode()
    rows[2] = rows[2].replace('%S138SHA%', sha(snap))
    ov['corpus/SOURCES.md'] = soc + '\n' + '\n'.join(rows) + '\n'
    ov[S138_SNAP] = snap
    ov[LESSON50] = ('# Round 50 (fixture)\n\nSynthetic lesson for the counter fixture.\n').encode()
    # knowledge + README
    ov['corpus/knowledge/2026-10-28-r50-fixture-entry.md'] = b'# fixture entry\n'
    rd = base('corpus/README.md')
    k = rd.find('## Coverage map')
    e = rd.find('\n## ', k + 5)
    rd = rd[:e] + '\n| fixture (round 50) | `2026-10-28-r50-fixture-entry` | fixture |\n' + rd[e:]
    ov['corpus/README.md'] = rd
    # SKILL registry rows
    sk = base('SKILL.md')
    paths = [p for p in r.ls(BASE, CENSUS_BASE_PREFIX) if p.endswith(('.py', '.sh'))
             and '/control-fixtures/' not in p]
    paths += ['tools/round-50/c2-record.py', SELFTEST_PATH]
    new = []
    for p in paths:
        interp = 'bash' if p.endswith('.sh') else 'python3 -I -B'
        if p.endswith('.sh') or p.endswith('c1-oracle.py'):
            st = 'none \u2014 no self-test is shipped for this instrument'
        else:
            st = '%s %s --selftest' % (interp, p)
        new.append('| `%s` | gate \u2014 fixture row for %s, run as `%s %s` | 0=met, every clause true; 1=not met, '
                   'a clause false; 2=could-not-evaluate, unreadable input or a refusal | %s | '
                   'none \u2014 no pinned value file | stdout only | kaidoku |' % (p, p, interp, p, st))
    ov['SKILL.md'] = sk.replace(REG_CLOSE, '\n'.join(new) + '\n' + REG_CLOSE, 1)
    return ov


def stand_in_selftest_files():
    """A tiny deterministic B10 self-test (fixture only): two cases against its expected file."""
    code = ('#!/usr/bin/env python3\n'
            'import argparse, hashlib, json, os\n'
            'ap = argparse.ArgumentParser()\n'
            'ap.add_argument("--root"); ap.add_argument("--work"); ap.add_argument("--json-out")\n'
            'a = ap.parse_args()\n'
            'here = os.path.dirname(os.path.abspath(__file__))\n'
            'raw = open(os.path.join(here, "selftest-r49-c2.expected.json"), "rb").read()\n'
            'exp = json.loads(raw)\n'
            'got = {"freeze_mismatches": 9, "landed_mismatches": 0}\n'
            'fails = [k for k in exp if exp[k] != got.get(k)]\n'
            'out = {"cases": len(exp), "failures": fails, "expected_sha256": hashlib.sha256(raw).hexdigest()}\n'
            'open(a.json_out, "w").write(json.dumps(out))\n'
            'raise SystemExit(1 if fails else 0)\n')
    exp = json.dumps({'freeze_mismatches': 9, 'landed_mismatches': 0}, sort_keys=True, indent=1) + '\n'
    return code.encode(), exp.encode()


def finish_green(ov, selftest_bytes, expected_bytes, cases):
    """Fill the B10 line of a green overlay once the self-test files are fixed."""
    s = ov['SCORECARD.md'].replace('%CASES%', str(cases)).replace('%EXPSHA%', sha(expected_bytes))
    ov = dict(ov)
    ov['SCORECARD.md'] = s
    return ov


# ------------------------------------------------------------------------ selftest


class Fx:
    """An isolated scratch clone, with git calls that name the clone and assert its toplevel."""

    def __init__(self, root, work):
        self.dir = tempfile.mkdtemp(prefix='fx-', dir=work)
        subprocess.run(['git', 'clone', '-q', '--shared', root, self.dir], check=True,
                       capture_output=True)
        top = self.git('rev-parse', '--show-toplevel').stdout.decode().strip()
        if os.path.realpath(top) != os.path.realpath(self.dir):
            raise RuntimeError('fixture toplevel %s != %s' % (top, self.dir))
        self.git('config', 'user.name', 'c2-record-selftest')
        self.git('config', 'user.email', 'c2-record-selftest@invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('checkout', '-q', '--detach', BASE)

    def git(self, *args):
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env['GIT_NO_REPLACE_OBJECTS'] = '1'
        return subprocess.run(['git', '-C', self.dir] + list(args), capture_output=True, env=env)

    def commit(self, files, msg, rm=()):
        top = self.git('rev-parse', '--show-toplevel').stdout.decode().strip()
        assert os.path.realpath(top) == os.path.realpath(self.dir)
        for p, b in files.items():
            fp = os.path.join(self.dir, p)
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp, 'wb') as fh:
                fh.write(b if isinstance(b, bytes) else b.encode())
        for p in rm:
            self.git('rm', '-q', '-f', '--', p)
        self.git('add', '-A', '--', '.')
        p = self.git('commit', '-q', '--allow-empty', '-m', msg)
        if p.returncode != 0:
            raise RuntimeError('fixture commit failed: %s' % p.stderr.decode()[:200])
        return self.git('rev-parse', 'HEAD').stdout.decode().strip()

    def reset(self, rev):
        self.git('checkout', '-q', '--detach', rev)

    def drop(self):
        shutil.rmtree(self.dir, ignore_errors=True)


def selftest(root, work, own_path):
    """Isolated-fixture cases: (name, expected exit, expected reason/red ids) -> failures."""
    wk = scratch_root(work)
    if wk is None:
        return {'exit_code': 2, 'reason': 'no_scratch_root', 'cases': 0, 'failures': []}
    root = os.path.abspath(root)
    g = Git(root)
    if not g.is_commit(BASE):
        return {'exit_code': 2, 'reason': 'BASE not in --root', 'cases': 0, 'failures': []}
    own = open(own_path, 'rb').read()
    fx = Fx(root, wk)
    cases, failures = [], []
    try:
        st_code, st_exp = stand_in_selftest_files()
        freeze_files = {SELF: own, SELFTEST_PATH: st_code, SELFTEST_EXPECTED: st_exp,
                        'plans/round-50-claims.md': b'# fixture plan\n',
                        'tools/round-50/control-fixtures/x.txt': b'x\n'}
        F = fx.commit(freeze_files, 'fixture FREEZE')
        gg = Git(fx.dir)
        ov = finish_green(build_green(gg), st_code, st_exp, 2)
        G = fx.commit({p: v for p, v in ov.items()}, 'fixture green')

        def run(name, rev, freeze, want_exit, want_red=None, want_reason=None, battery_=False,
                counter=None, cwd_root=None):
            res = evaluate(fx.dir, rev, freeze, battery_, wk, counter or own_path)
            red = sorted(k for k, v in res.get('atoms', {}).items() if not v['ok'])
            ok = res['exit_code'] == want_exit
            if want_red is not None:
                ok = ok and red == sorted(want_red)
            if want_reason is not None:
                ok = ok and res.get('reason') == want_reason
            if battery_ and want_exit == 0:
                ok = ok and not res['battery']['failing']
            cases.append(name)
            if not ok:
                failures.append({'case': name, 'exit': res['exit_code'], 'red': red,
                                 'reason': res.get('reason'), 'detail': str(res.get('detail'))[:120],
                                 'battery_failing': res.get('battery', {}).get('failing', [])[:3]})
            return res

        run('do-nothing at FREEZE is red on every atom', F, F, 1, ATOM_IDS)
        run('green fixture exits 0', G, F, 0, [])
        run('green fixture with --battery exits 0, battery clean', G, F, 0, [], battery_=True)

        def variant(name, files, red, rm=(), base_rev=G):
            fx.reset(base_rev)
            rev = fx.commit(files, name, rm)
            run(name, rev, F, 1, red)
            fx.reset(G)

        scg = fx.git('show', G + ':SCORECARD.md').stdout.decode()
        b3 = [l for l in scg.split('\n') if l.startswith('- B3 ')][0]
        variant('B3 line in an HTML comment', {'SCORECARD.md': scg.replace(b3, '<!--\n' + b3 + '\n-->')}, ['B3'])
        variant('B3 line in a fenced block', {'SCORECARD.md': scg.replace(b3, '```\n' + b3 + '\n```')}, ['B3'])
        variant('B3 duplicate line', {'SCORECARD.md': scg.rstrip('\n') + '\n' + b3 + '\n'}, ['B3'])
        variant('B3 repeated key', {'SCORECARD.md': scg.replace(b3, b3 + ' seats=9')}, ['B3'])
        variant('B3 unterminated comment hides itself and every later line', {
            'SCORECARD.md': scg.replace(b3, '<!--\n' + b3)}, ['B3', 'B4', 'B5', 'B10', 'B11'])
        variant('B3 U+2028 separator does not make a line', {
            'SCORECARD.md': scg.replace(b3, 'prose\u2028' + b3)}, ['B3'])
        soc = fx.git('show', G + ':corpus/SOURCES.md').stdout.decode()
        s150 = [l for l in soc.split('\n') if l.startswith('| S150 ')][0]
        variant('B6 correction row in a fence', {'corpus/SOURCES.md': soc.replace(s150, '~~~\n' + s150 + '\n~~~')}, ['B6'])
        variant('B6 snapshot cited but not committed', {'corpus/SOURCES.md': soc.replace(s150, s150.replace(
            LIT['freebsd_sha'], '0' * 64))}, ['B6'])
        sk = fx.git('show', G + ':SKILL.md').stdout.decode()
        row = [l for l in sk.split('\n') if l.startswith('| `tools/round-49/c1-run.sh`')][0]
        variant('B9 registry row removed', {'SKILL.md': sk.replace(row + '\n', '')}, ['B9'])
        variant('B9 registry row in an HTML comment', {'SKILL.md': sk.replace(row, '<!-- ' + row + ' -->')}, ['B9'])
        variant('B11 LOG.md rewritten (not append-only)', {
            'LOG.md': fx.git('show', G + ':LOG.md').stdout.replace(b'decc5697', b'decc5698', 1)}, ['B11'])
        # freeze-integrity exits (exit 2)
        fx.reset(G)
        r1 = fx.commit({'tools/round-50/new-file.py': 'x\n'}, 'frozen path: file added')
        run('added frozen file -> frozen_path_changed', r1, F, 2, None, 'frozen_path_changed')
        fx.reset(G)
        r2 = fx.commit({'tools/round-50/control-fixtures/x.txt': 'y\n'}, 'frozen path: fixture edited')
        run('edited frozen fixture -> frozen_path_changed', r2, F, 2, None, 'frozen_path_changed')
        fx.reset(G)
        r3a = fx.commit({'plans/round-50-claims.md': 'touched\n'}, 'touch')
        r3 = fx.commit({'plans/round-50-claims.md': b'# fixture plan\n'}, 'restore')
        run('touch-and-restore -> frozen_path_changed', r3, F, 2, None, 'frozen_path_changed')
        fx.reset(G)
        r4 = fx.commit({'tools/round-50/caf\u00e9 \u201cq\u201d.py': 'z\n'}, 'frozen path: non-ASCII name added')
        run('non-ASCII frozen name -> frozen_path_changed', r4, F, 2, None, 'frozen_path_changed')
        fx.reset(G)
        fx.git('mv', 'plans/round-50-claims.md', 'plans/moved.md')
        r5 = fx.commit({}, 'frozen path: renamed away')
        run('renamed frozen file -> frozen_path_changed', r5, F, 2, None, 'frozen_path_changed')
        fx.reset(G)
        run('freeze not an ancestor -> exit 2', F, G, 2, None, 'bad_freeze')
        run('unresolvable rev -> exit 2', 'nonexistent-ref', F, 2)
        # counter bytes differ from the FREEZE blob
        alt = os.path.join(wk, 'altered-counter.py')
        with open(alt, 'wb') as fh:
            fh.write(own + b'\n# altered\n')
        try:
            run('counter bytes differ from FREEZE -> counter_not_frozen', G, F, 2, None, 'counter_not_frozen',
                counter=alt)
        finally:
            os.unlink(alt)
        # a FREEZE that does not carry the counter at all
        run('FREEZE without the counter -> counter_not_frozen', G, BASE, 2, None, 'counter_not_frozen')
        # vis() unit cases
        unit = [('vis drops a fenced line', vis('a\n```\n- B3 x=1\n```\nb') == 'a\n\n\n\nb'),
                ('vis drops a comment block', vis('a\n<!--\n- B3 x=1\n-->\nb') == 'a\n\n\n\nb'),
                ('vis drops an unterminated fence', vis('a\n~~~\n- B3 x=1\nb') == 'a\n\n\n'),
                ('vis drops an unterminated comment', vis('a\n<!-- c\n- B3 x=1') == 'a\n\n'),
                ('vis inline comment becomes NUL', vis('- B3 a=1 <!-- b=2 --> c=3') == '- B3 a=1 \x00 c=3'),
                ('vis keeps LF-only split', vis('a\u2028b') == 'a\u2028b')]
        for name, okk in unit:
            cases.append(name)
            if not okk:
                failures.append({'case': name})
    except Exception as e:
        failures.append({'case': 'selftest crashed', 'error': repr(e)[:200]})
    finally:
        fx.drop()
    return {'exit_code': 0 if not failures else 1, 'cases': len(cases), 'case_names': cases,
            'failures': failures}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--battery', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--work')
    ap.add_argument('--json-out')
    a = ap.parse_args(argv)
    if a.selftest:
        res = selftest(a.root, a.work, os.path.abspath(__file__))
        res['schema'] = 'kaidoku-r50-c2-selftest-v1'
    else:
        if not a.rev or not a.freeze:
            ap.error('--rev and --freeze are required without --selftest')
        res = evaluate(a.root, a.rev, a.freeze, a.battery, a.work)
    s = json.dumps(res, indent=1, sort_keys=True)
    if a.json_out:
        with open(a.json_out, 'w') as fh:
            fh.write(s + '\n')
    print(s)
    return res['exit_code']


if __name__ == '__main__':
    sys.exit(main())
