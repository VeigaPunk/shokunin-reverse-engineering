#!/usr/bin/env python3
"""Mutation harness for the frozen tools/round-39/sqfs-triage.py (seat R39W2TriageMutants).

The lane file is NEVER modified: every mutant is a fresh copy written under the
scratch mutants/ dir.  Detector per mutant:
  (a) label the 20 committed held-out envelopes with the lane SKILL.md and count
      agreements with manifest.json labels;
  (b) run the mutant's own --selftest (exit 0 expected).
Verdicts: KILLED-LABELS / KILLED-RUNFAIL / KILLED-SELFTEST-ONLY / SURVIVED.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SRC = LANE + '/tools/round-39/sqfs-triage.py'
SKILL = LANE + '/SKILL.md'
HELD = LANE + '/corpus/evidence/round-39/c2/heldout'
S = '/fast/scratch/hyaku/kaidoku-r39/R39W2TriageMutants'
MUTDIR = S + '/mutants'
RES = S + '/results'

MANIFEST = json.load(open(HELD + '/manifest.json'))
IDS = [c['id'] for c in MANIFEST['carriers']]
WANT = {c['id']: c['label'] for c in MANIFEST['carriers']}
ENVS = [HELD + '/' + c['id'] + '/envelope.json' for c in MANIFEST['carriers']]
SRC_TEXT = open(SRC, 'r', encoding='utf-8').read()

MUTANTS = {}

def mut(name, *pairs):
    MUTANTS[name] = list(pairs)

# ---- H handler filter -------------------------------------------------------
mut('H-exact-v4be',
    ("and handler.startswith('squashfs'):", "and handler == 'squashfs_v4_be':"))
mut('H-prefix-squash',
    ("and handler.startswith('squashfs'):", "and handler.startswith('squash'):"))
mut('H-no-filter',
    ("if isinstance(handler, str) and handler.startswith('squashfs'):",
     "if isinstance(handler, str):"))
mut('H-lower',
    ("and handler.startswith('squashfs'):",
     "and handler.lower().startswith('squashfs'):"))

# ---- G set ------------------------------------------------------------------
mut('G-first-kind-only',
    ("            gap_kinds.add(kind)\n        for dep",
     "            if not gap_kinds:\n                gap_kinds.add(kind)\n        for dep"))
mut('GD-first-gap-only',
    ("            gap_kinds.add(kind)\n        for dep",
     "            gap_kinds.add(kind)\n            break\n        for dep"))
mut('G-nonstr-included',
    ("        kind = gap.get('kind')\n        if isinstance(kind, str):\n            gap_kinds.add(kind)",
     "        kind = gap.get('kind')\n        gap_kinds.add(kind)"))

# ---- D union ----------------------------------------------------------------
mut('D-last-wins',
    ("            if isinstance(dep, str):\n                dependencies.add(dep)",
     "            if isinstance(dep, str):\n                dependencies = {dep}"))
mut('D-nonstr-included',
    ("        for dep in _as_list(gap.get('dependencies')):\n"
     "            if isinstance(dep, str):\n"
     "                dependencies.add(dep)",
     "        for dep in _as_list(gap.get('dependencies')):\n"
     "            dependencies.add(dep)"))

# ---- BE token detection -----------------------------------------------------
mut('BE-substring',
    ("            if '-be' in (command_tokens(cmd) or []):",
     "            if '-be' in str(cmd):"))
mut('BE-first-cmd-only',
    ("        for cmd in commands:\n            if '-be'",
     "        for cmd in commands[:1]:\n            if '-be'"))
mut('BE-token-prefix',
    ("            if '-be' in (command_tokens(cmd) or []):",
     "            if any(t.startswith('-be') for t in (command_tokens(cmd) or [])):"))
mut('BE-any-to-all',
    ("        be = 'no'\n        for cmd in commands:\n"
     "            if '-be' in (command_tokens(cmd) or []):\n"
     "                be = 'yes'\n"
     "                break",
     "        be = 'yes'\n        for cmd in commands:\n"
     "            if '-be' not in (command_tokens(cmd) or []):\n"
     "                be = 'no'\n"
     "                break"))

# ---- sasquatch basename detection -------------------------------------------
_SQ_OLD = "        if token.rsplit('/', 1)[-1].startswith('sasquatch'):"
mut('SQ-exact-name', (_SQ_OLD, "        if token.rsplit('/', 1)[-1] == 'sasquatch':"))
mut('SQ-v4be-only', (_SQ_OLD, "        if token.rsplit('/', 1)[-1].startswith('sasquatch-v4be'):"))
mut('SQ-substring', (_SQ_OLD, "        if 'sasquatch' in token:"))
mut('SQ-no-basename', (_SQ_OLD, "        if token.startswith('sasquatch'):"))

# ---- SR detection -----------------------------------------------------------
mut('SR-diagnostics-only',
    ("    if symlink == 'no':\n"
     "        for found in _iter_dicts(data.get('raw_result')):\n"
     "            if found.get('__typename__') == SYMLINK_TYPENAME:\n"
     "                symlink = 'yes'\n"
     "                break\n",
     "    # mutant: raw_result SR fallback removed\n"))
mut('SR-raw-only',
    ("    for diag in _as_list(nr.get('diagnostics')):\n"
     "        report = diag.get('report') if isinstance(diag, dict) else None\n"
     "        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:\n"
     "            symlink = 'yes'\n"
     "            break\n",
     "    # mutant: diagnostics SR scan removed\n"))
mut('SR-substring',
    ("if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:",
     "if isinstance(report, dict) and SYMLINK_TYPENAME in str(report.get('__typename__')):"),
    ("            if found.get('__typename__') == SYMLINK_TYPENAME:",
     "            if SYMLINK_TYPENAME in str(found.get('__typename__')):"))

# ---- P count ----------------------------------------------------------------
_P_OLD = "        'P': len(_as_list(nr.get('files'))),"
mut('P-unpublished-swap', (_P_OLD, "        'P': len(_as_list(nr.get('unpublished_entries'))),"))
mut('P-bool', (_P_OLD, "        'P': bool(_as_list(nr.get('files'))),"))
mut('P-plus-unpublished',
    (_P_OLD,
     "        'P': len(_as_list(nr.get('files'))) + len(_as_list(nr.get('unpublished_entries'))),"))

# ---- command dedup ----------------------------------------------------------
mut('CMD-dedup-drop',
    ("        if tokens and names_sasquatch(tokens) and cmd not in commands:",
     "        if tokens and names_sasquatch(tokens):"))

# ---- rule matching ----------------------------------------------------------
mut('RM-last-match',
    ("def classify(rules, feat):\n"
     "    for rule in rules:\n"
     "        if rule_matches(rule, feat):\n"
     "            return rule\n"
     "    return None",
     "def classify(rules, feat):\n"
     "    last = None\n"
     "    for rule in rules:\n"
     "        if rule_matches(rule, feat):\n"
     "            last = rule\n"
     "    return last"))
mut('RM-star-false',
    ("    if kind == 'any':\n        return True",
     "    if kind == 'any':\n        return False"))
mut('RM-none-inverted',
    ("    if kind == 'none':\n        return not values",
     "    if kind == 'none':\n        return bool(values)"))
mut('RM-hnone-inverted',
    ("    if kind == 'none':\n        if feat['H']:\n            return False",
     "    if kind == 'none':\n        if not feat['H']:\n            return False"))
mut('RM-exact-superset',
    ("    return frozenset(values) == payload",
     "    return payload <= frozenset(values)"))
mut('RM-exact-subset',
    ("    return frozenset(values) == payload",
     "    return payload >= frozenset(values)"))
mut('RM-fnmatch-equals',
    ("        if not any(fnmatch.fnmatchcase(value, payload) for value in feat['H']):",
     "        if not any(value == payload for value in feat['H']):"))
mut('RM-fnmatch-nocase',
    ("fnmatch.fnmatchcase(value, payload)",
     "fnmatch.fnmatch(value, payload)"))
mut('RM-gt0-loose',
    ("    if files == '>0' and feat['P'] <= 0:",
     "    if files == '>0' and feat['P'] < 0:"))
mut('RM-files-gt0-dead',
    ("    if files == '>0' and feat['P'] <= 0:\n        return False",
     "    if files == '>0':\n        return False"))
mut('RM-files-zero-dead',
    ("    if files == '0' and feat['P'] != 0:\n        return False",
     "    if files == '0':\n        return False"))
mut('RM-zero-loose',
    ("    if files == '0' and feat['P'] != 0:",
     "    if files == '0' and feat['P'] < 0:"))

# ---- value inversions (complete the BE/SR dependency map) --------------------
mut('BE-invert-yes-no',
    ("        be = 'no'\n        for cmd in commands:",
     "        be = 'yes'\n        for cmd in commands:"))
mut('BE-na-to-no',
    ("    if not commands:\n        be = 'n/a'",
     "    if not commands:\n        be = 'no'"))
mut('SR-invert',
    ("    symlink = 'no'\n    for diag in _as_list(nr.get('diagnostics')):",
     "    symlink = 'yes'\n    for diag in _as_list(nr.get('diagnostics')):"))


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def validate_pairs():
    bad = []
    for name, pairs in MUTANTS.items():
        for old, _new in pairs:
            n = SRC_TEXT.count(old)
            if n != 1:
                bad.append((name, n, old[:70]))
    return bad


def write_mutant(name):
    text = SRC_TEXT
    for old, new in MUTANTS[name]:
        text = text.replace(old, new, 1)
    path = '%s/%s.py' % (MUTDIR, name)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    return path


def run(cmd, timeout):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=S)


def labels_of(proc):
    got = {}
    if proc.returncode == 0:
        for line in proc.stdout.splitlines():
            path, sep, lab = line.partition('\t')
            if sep:
                hid = os.path.basename(os.path.dirname(path.strip()))
                got[hid] = lab.strip()
    return got


def run_labels(py):
    proc = run([sys.executable, '-I', '-B', py, '--skill', SKILL] + ENVS, 180)
    return proc, labels_of(proc)


def run_selftest(py):
    env = dict(os.environ, TMPDIR=S + '/tmp', PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run([sys.executable, '-I', '-B', py, '--selftest'],
                          capture_output=True, text=True, timeout=600, env=env, cwd=S)


def selftest_summary(proc):
    for line in proc.stdout.splitlines():
        if line.startswith('SELFTEST cases='):
            return line.strip()
    return 'no-summary(stderr=%r)' % proc.stderr.strip()[:120]


def probe(name):
    path = write_mutant(name)
    lproc, labels = run_labels(path)
    sproc = run_selftest(path)
    matches = sum(1 for h in IDS if labels.get(h) == WANT[h])
    mism = {h: {'want': WANT[h], 'got': labels.get(h)}
            for h in IDS if labels.get(h) != WANT[h]}
    if lproc.returncode != 0:
        verdict = 'KILLED-RUNFAIL(exit=%d)' % lproc.returncode
    elif matches < 20:
        verdict = 'KILLED-LABELS(%d/20)' % matches
    elif sproc.returncode != 0:
        verdict = 'KILLED-SELFTEST-ONLY(20/20-labels)'
    else:
        verdict = 'SURVIVED'
    return {
        'mutant': name,
        'mutant_sha256': sha256(path),
        'label_exit': lproc.returncode,
        'label_stderr': lproc.stderr.strip()[:300],
        'labels': labels,
        'matches': matches,
        'mismatches': mism,
        'selftest_exit': sproc.returncode,
        'selftest_summary': selftest_summary(sproc),
        'selftest_fails': [l.split()[1] for l in sproc.stdout.splitlines()
                           if l.startswith('FAIL ')],
        'verdict': verdict,
    }


def base():
    pris = S + '/pristine.py'
    with open(pris, 'w', encoding='utf-8') as fh:
        fh.write(SRC_TEXT)
    lproc, labels = run_labels(pris)
    jproc = run([sys.executable, '-I', '-B', pris, '--skill', SKILL, '--json'] + ENVS, 180)
    feats = {}
    if jproc.returncode == 0:
        payload = json.loads(jproc.stdout)
        feats = {os.path.basename(os.path.dirname(r['path'])):
                 {'label': r['label'], 'rule': r['rule'],
                  'H': r['features']['H'], 'G': r['features']['G'],
                  'D': r['features']['D'], 'BE': r['features']['BE'],
                  'SR': r['features']['SR'], 'P': r['features']['P']}
                 for r in payload['results']}
    sproc = run_selftest(pris)
    matches = sum(1 for h in IDS if labels.get(h) == WANT[h])
    out = {
        'src_sha256': sha256(SRC),
        'pristine_copy_sha256': sha256(pris),
        'skill_sha256': sha256(SKILL),
        'matches': matches,
        'labels': labels,
        'mismatches': {h: {'want': WANT[h], 'got': labels.get(h)}
                       for h in IDS if labels.get(h) != WANT[h]},
        'label_exit': lproc.returncode,
        'features': feats,
        'selftest_exit': sproc.returncode,
        'selftest_summary': selftest_summary(sproc),
        'selftest_fails': [l.split()[1] for l in sproc.stdout.splitlines()
                           if l.startswith('FAIL ')],
    }
    json.dump(out, open(RES + '/base.json', 'w'), indent=1, sort_keys=True)
    print(json.dumps({k: out[k] for k in ('src_sha256', 'matches', 'label_exit',
                                          'selftest_exit', 'selftest_summary',
                                          'mismatches')}, indent=1, sort_keys=True))
    print('features:')
    print(json.dumps(feats, indent=1, sort_keys=True))


def chunk(lo, hi):
    names = sorted(MUTANTS)[lo:hi]
    outs = []
    for name in names:
        t0 = time.time()
        res = probe(name)
        res['seconds'] = round(time.time() - t0, 1)
        outs.append(res)
        print('%-22s %-36s %ss' % (name, res['verdict'], res['seconds']), flush=True)
    json.dump(outs, open('%s/chunk-%d-%d.json' % (RES, lo, hi), 'w'), indent=1, sort_keys=True)


def merge():
    base = json.load(open(RES + '/base.json'))
    chunks = []
    for fn in sorted(os.listdir(RES)):
        if fn.startswith('chunk-'):
            chunks.extend(json.load(open(RES + '/' + fn)))
    json.dump({'base': base, 'mutants': chunks},
              open(S + '/results.json', 'w'), indent=1, sort_keys=True)
    print('%-22s %-8s %-6s %-14s %s' % ('mutant', 'labels', 'st-exit', 'verdict', 'selftest fails'))
    for m in sorted(chunks, key=lambda r: r['mutant']):
        print('%-22s %-8s %-6s %-14s %s' % (
            m['mutant'], '%d/20' % m['matches'], m['selftest_exit'],
            m['verdict'], ','.join(m['selftest_fails']) or '-'))
    surv = [m['mutant'] for m in chunks if m['verdict'] == 'SURVIVED']
    print('SURVIVED: %s' % (', '.join(surv) or 'none'))


def verify():
    """For every SURVIVED mutant: diff its --json features against the pristine ones."""
    base = json.load(open(RES + '/base.json'))
    chunks = []
    for fn in sorted(os.listdir(RES)):
        if fn.startswith('chunk-'):
            chunks.extend(json.load(open(RES + '/' + fn)))
    pris = S + '/pristine.py'
    out = []
    for m in sorted(chunks, key=lambda r: r['mutant']):
        if m['verdict'] != 'SURVIVED':
            continue
        jproc = run([sys.executable, '-I', '-B', '%s/%s.py' % (MUTDIR, m['mutant']),
                     '--skill', SKILL, '--json'] + ENVS, 180)
        if jproc.returncode != 0:
            out.append({'mutant': m['mutant'], 'json_exit': jproc.returncode,
                        'stderr': jproc.stderr.strip()[:200]})
            continue
        payload = json.loads(jproc.stdout)
        diffs = {}
        for r in payload['results']:
            hid = os.path.basename(os.path.dirname(r['path']))
            keys = ('H', 'G', 'D', 'BE', 'SR', 'P')
            a = {k: r['features'][k] for k in keys}
            b = {k: base['features'][hid][k] for k in keys}
            if a != b:
                diffs[hid] = {k: {'pristine': b.get(k), 'mutant': a.get(k)}
                              for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)}
        out.append({'mutant': m['mutant'], 'json_exit': 0,
                    'feature_diffs': diffs,
                    'feature_equivalent': not diffs})
    json.dump(out, open(RES + '/verify.json', 'w'), indent=1, sort_keys=True)
    for v in out:
        print('%-22s feature-equivalent=%s %s' % (
            v['mutant'], v.get('feature_equivalent'),
            json.dumps(v.get('feature_diffs', {}), sort_keys=True)[:200]))


if __name__ == '__main__':
    cmd = sys.argv[1]
    os.makedirs(RES, exist_ok=True)
    bad = validate_pairs()
    if bad:
        print('PAIR-VALIDATION-FAILED:', json.dumps(bad, indent=1))
        sys.exit(3)
    if cmd == 'base':
        base()
    elif cmd == 'chunk':
        chunk(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == 'merge':
        merge()
    elif cmd == 'verify':
        verify()
    else:
        print('unknown command'); sys.exit(2)
