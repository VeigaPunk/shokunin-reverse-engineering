#!/usr/bin/env python3
"""Round-38 landing checks for the mistakes the lesson does not record.

Each check is a candidate fix that must be able to fail. Run from the lane root:
  python3 .ufo/waves/round-38/w2/artifacts/R38W2MistakeHunt/checks.py --root .
Exit 0 only when every check passes. Read-only (git show/ls-files only).
"""
import argparse, fnmatch, hashlib, json, os, re, subprocess, sys


def git(root, *a, text=True):
    return subprocess.run(['git', '-C', root, *a], capture_output=True, text=text)


def exists(root, rev, path):
    return git(root, 'cat-file', '-e', f'{rev}:{path}').returncode == 0


def blob(root, rev, path):
    r = git(root, 'show', f'{rev}:{path}')
    return r.stdout if r.returncode == 0 else None


def tracked(root, path):
    return git(root, 'ls-files', '--error-unmatch', path).returncode == 0


def check_cited_score_receipts(root):
    """A. Every scores/*.json path cited in SCORECARD.md or the round-38 lesson
    exists in the worktree and is tracked at HEAD."""
    findings = []
    heads = ['SCORECARD.md', 'corpus/lessons/round-38.md']
    cited = set()
    for h in heads:
        t = open(os.path.join(root, h), encoding='utf-8').read()
        for m in re.finditer(r'\.ufo/waves/round-38/l1/scores/([A-Za-z0-9._-]+\.json)', t):
            cited.add((h, m.group(1)))
    for h, name in sorted(cited):
        p = f'.ufo/waves/round-38/l1/scores/{name}'
        ok_file = os.path.exists(os.path.join(root, p))
        ok_track = tracked(root, p)
        if not (ok_file and ok_track):
            findings.append(f'A cited-receipt {h} -> {p} exists={ok_file} tracked={ok_track}')
    return findings


def check_instrument_map(root, freeze):
    """B. The freeze instrument map names its own freeze, distinguishes
    instruments that exist at the freeze from claim data that cannot, and
    lists only lane-relative paths."""
    findings = []
    p = '.ufo/waves/round-38/instruments.json'
    t = blob(root, freeze, p)
    if t is None:
        return ['B instruments.json absent at freeze']
    d = json.loads(t)
    fc = d.get('frozen_at_commit', '')
    if not re.fullmatch(r'[0-9a-f]{40}', fc or ''):
        findings.append(f'B frozen_at_commit is a literal {fc!r}, not a commit id')
    elif not exists(root, fc, p):
        findings.append(f'B frozen_at_commit {fc} does not resolve to the map')
    tree = git(root, 'ls-tree', '-r', '--name-only', freeze).stdout.splitlines()
    for k, v in d.get('instruments', {}).items():
        if v.startswith('/') or v.startswith('~'):
            findings.append(f'B instrument {k} is an absolute path outside the lane: {v}')
            continue
        pattern = v.split(' --')[0].split()[0]
        lst = [t for t in tree if fnmatch.fnmatch(t, pattern)]
        phase = (d.get('phases') or {}).get(k)
        if not lst and phase not in ('claim_data', 'post_freeze'):
            findings.append(f'B instrument {k} {pattern} matches nothing at the freeze '
                            f'and no phase declares it claim data')
    return findings


def check_counter_identity(root, freeze, counter):
    """C. The counter that runs must be the counter the freeze names: its bytes
    must equal git show <freeze>:<same path>."""
    findings = []
    p = counter
    if not os.path.exists(os.path.join(root, p)):
        return []
    wt = open(os.path.join(root, p), 'rb').read()
    fz = blob(root, freeze, p)
    if fz is None:
        return [f'C {p} absent at freeze']
    a = hashlib.sha256(wt).hexdigest()[:12]
    b = hashlib.sha256(fz.encode() if isinstance(fz, str) else fz).hexdigest()[:12]
    if a != b:
        findings.append(f'C {p} worktree sha {a} != freeze sha {b}')
    return findings


def check_registry_supersedes(root, opened):
    """D. A second row for a URL already registered must name the row it
    supersedes in teaches (the lane's own practice: S033, S054, S062, S069)."""
    findings = []
    rows = []
    for i, l in enumerate(open(os.path.join(root, 'corpus/SOURCES.md'), encoding='utf-8'), 1):
        if not l.startswith('| S'):
            continue
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) < 11:
            continue
        m = re.search(r'https?://[^\s|]+', c[1])
        rows.append({'id': c[0], 'url': m.group(0).rstrip('.,)') if m else None,
                     'opened': c[8], 'status': c[7], 'teaches': c[6], 'line': i})
    seen = {}
    for r in rows:
        if not r['url'] or r['opened'] != opened:
            continue
        if r['url'] in seen and not re.search(r'supersedes S\d{3}', r['teaches']):
            findings.append(f"D {r['id']} (line {r['line']}) re-registers {seen[r['url']]}'s URL "
                            f"with no 'supersedes S' in teaches")
        seen.setdefault(r['url'], r['id'])
    return findings


def check_seat_accounting(root, rev):
    """E. The wave-1 result ledger is in the landing commit and agrees with the
    committed reports."""
    findings = []
    p = '.ufo/waves/round-38/r38-w1-results.json'
    if not exists(root, rev, p):
        findings.append(f'E {p} is not in {rev[:8]}')
    reports = git(root, 'ls-tree', '-r', '--name-only', rev, '--',
                  '.ufo/waves/round-38/w1').stdout.splitlines()
    n = len([x for x in reports if x.endswith('.md') and '/artifacts/' not in x])
    if os.path.exists(os.path.join(root, p)):
        d = json.load(open(os.path.join(root, p), encoding='utf-8'))
        res = d.get('results') or {}
        got = len(res) if hasattr(res, '__len__') else -1
        if d.get('seats') != n or got != n:
            findings.append(f'E ledger seats={d.get("seats")} results={got} vs {n} reports')
    return findings


def check_draft_markers(root):
    """F. An artifact committed as wave-1 evidence whose own title asserts the
    round-38 outcome carries a machine-readable non-landed marker.

    Deliberately title-only: a body-phrase grep is NOT a discriminator — it
    returns 36 hits on this wave, almost all of them embedded claims text
    inside counter snapshots (measured, see checks-run.txt)."""
    d = os.path.join(root, '.ufo/waves/round-38/w1/artifacts')
    if not os.path.isdir(d):
        return []
    phrases = ('is now Core', 'additions to Core', 'v4 to Core', '→ Core')
    findings = []
    for sub in sorted(os.listdir(d)):
        base = os.path.join(d, sub)
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            p = os.path.join(base, f)
            if not f.endswith('.md') or not os.path.isfile(p):
                continue
            lines = open(p, encoding='utf-8', errors='replace').read().splitlines()
            head = next((l for l in lines if l.startswith('#')), '')
            if any(ph in head for ph in phrases) and not any(
                    'draft' in l.lower() or 'not landed' in l.lower() for l in lines[:15]):
                findings.append(f'F {os.path.relpath(p, root)} title asserts the outcome, no marker')
    return findings



def check_id_space(root, pkg):
    """G. Lane ids appended this round must not reuse a staged id that names a
    different document. The round's guard compared the PRE-append lane range
    (S001-S111) against the staged ids and was never re-run after appending."""
    findings = []
    staged = set()
    ap = os.path.join(pkg, 'SOURCES.append.md')
    if os.path.exists(ap):
        for l in open(ap, encoding='utf-8', errors='replace'):
            m = re.match(r'^\|\s*(S\d{3})\s*\|', l)
            if m:
                staged.add(m.group(1))
    slice_f = os.path.join(root, '.ufo/waves/round-38/assimilation/quarantine-slice')
    if os.path.exists(slice_f):
        staged |= set(re.findall(r'\bS\d{3}\b', open(slice_f, encoding='utf-8').read()))
    lane = [re.match(r'^\|\s*(S\d{3})\s*\|', l).group(1)
            for l in open(os.path.join(root, 'corpus/SOURCES.md'), encoding='utf-8')
            if re.match(r'^\|\s*(S\d{3})\s*\|', l)]
    known = {f'S{i:03d}' for i in range(106, 112)}   # reported by the round's guard
    for i in lane:
        if i in staged and i not in known:
            findings.append(f'G lane {i} reuses a staged id for a different document')
    return findings



def check_criterion_refs(root):
    """H. A QUALITY row added this round may cite only a lesson row that exists
    and only objects that are tracked."""
    findings = []
    q = open(os.path.join(root, 'corpus/QUALITY.md'), encoding='utf-8').read().splitlines()
    lesson = open(os.path.join(root, 'corpus/lessons/round-38.md'), encoding='utf-8').read()
    rows = set(re.findall(r'(?m)^\|\s*(M38-\d+)\s*\|', lesson))
    for l in q:
        if not l.startswith('|'):
            continue
        cells = [c.strip() for c in l.strip('|').split('|')]
        if not cells or not cells[0].isdigit() or int(cells[0]) < 79:
            continue
        for mid in re.findall(r'M38-\d+', l):
            if mid not in rows:
                findings.append(f'H QUALITY {cells[0]} cites {mid}, which has no row in the round-38 lesson')
        for path in re.findall(r'`(tools/round-38/[A-Za-z0-9._-]+)`', l):
            if not tracked(root, path) and ' ' not in path:
                findings.append(f'H QUALITY {cells[0]} cites untracked {path}')
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--freeze', default='e059ca9391642d5b71b6662cabcbdce0d9308719')
    ap.add_argument('--landing', default='3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8')
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    only = {x.strip().upper() for x in a.only.split(',') if x.strip()}
    groups = [
        ('A', 'A cited score receipts', lambda: check_cited_score_receipts(root)),
        ('B', 'B instrument map', lambda: check_instrument_map(root, a.freeze)),
        ('C', 'C counter identity', lambda: check_counter_identity(root, a.freeze, 'tools/round-38/c1-counter.py')),
        ('D', 'D registry supersedes', lambda: check_registry_supersedes(root, '2026-10-26')),
        ('E', 'E seat accounting', lambda: check_seat_accounting(root, a.landing)),
        ('F', 'F draft markers', lambda: check_draft_markers(root)),
        ('G', 'G id space', lambda: check_id_space(root, '/home/vgpnk/Projects/shokuknow/merge/kaidoku')),
        ('H', 'H criterion refs', lambda: check_criterion_refs(root)),
    ]
    total = 0
    for letter, name, fn in groups:
        if only and letter not in only:
            continue
        fs = fn()
        print(f'{name}: {len(fs)} finding(s)')
        for f in fs:
            print('  ', f)
        total += len(fs)
    print(json.dumps({'findings': total, 'verdict': 'FAIL' if total else 'PASS'}))
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
