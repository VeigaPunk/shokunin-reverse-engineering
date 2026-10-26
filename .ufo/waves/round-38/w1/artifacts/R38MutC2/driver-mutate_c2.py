#!/usr/bin/env python3
"""R38MutC2 mutation battery for the frozen R38-C2 counter (selftest-level).

Reads the frozen counter bytes read-only, generates one mutant per named
mechanism in scratch, runs the counter's own selftest against each mutant,
and records killed/survived verdicts. Never writes anywhere in the lane
except the artifacts dir. Frozen counter is never modified.
"""
import hashlib, json, os, shutil, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FROZEN = os.path.join(LANE, 'tools', 'round-38', 'c2-counter.py')
BASE = '77091b492cc53f8743bd0701b1e7d5e66123dd84'
FREEZE = 'e059ca9391642d5b71b6662cabcbdce0d9308719'
S = os.environ['SEAT_SCRATCH']
ART = os.path.join(LANE, '.ufo', 'waves', 'round-38', 'w1', 'artifacts', 'R38MutC2')
os.makedirs(ART, exist_ok=True)
MUTDIR = os.path.join(S, 'mut')
os.makedirs(MUTDIR, exist_ok=True)

sha = lambda b: hashlib.sha256(b).hexdigest()
src_bytes = open(FROZEN, 'rb').read()
frozen_before = sha(src_bytes)
txt = src_bytes.decode()

PRISTINE = os.path.join(S, 'pristine.py')
open(PRISTINE, 'wb').write(src_bytes)
assert sha(open(PRISTINE, 'rb').read()) == frozen_before, 'pristine copy mismatch'

blob = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob', f'{FREEZE}:tools/round-38/c2-counter.py'],
                      capture_output=True)
provenance = {
    'freeze_commit': FREEZE,
    'blob_at_freeze_sha256': sha(blob.stdout) if blob.returncode == 0 else None,
    'disk_sha256': frozen_before,
    'disk_equals_freeze_blob': blob.returncode == 0 and sha(blob.stdout) == frozen_before,
}

PY = [sys.executable, '-I', '-B']
env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)


def run(args, timeout=600):
    return subprocess.run(PY + args, capture_output=True, text=True, env=env, timeout=timeout)


# --- baseline: pristine copy must pass its own selftest, else inconclusive ---
b = run([PRISTINE, '--selftest'])
try:
    bj = json.loads(b.stdout.strip().splitlines()[-1])
except Exception:
    bj = None
baseline = {'rc': b.returncode, 'stdout': b.stdout.strip(), 'stderr': b.stderr[-500:], 'json': bj}
if b.returncode != 0 or not bj or bj.get('failures'):
    out = {'verdict': 'INCONCLUSIVE: pristine selftest failed', 'baseline': baseline,
           'provenance': provenance}
    json.dump(out, open(os.path.join(ART, 'results.json'), 'w'), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(3)

# --- observation only: pristine counter, do-nothing at the real base ---
lane = run([PRISTINE, '--root', LANE, '--rev', BASE, '--base', BASE,
            '--json-out', os.path.join(ART, 'lane-base-donothing.json')])
lane_summary = {'rc': lane.returncode, 'stdout': lane.stdout.strip(), 'stderr': lane.stderr[-300:]}

# --- mutants: (name, family, prediction, exact-old, exact-new) ---
MUTANTS = [
    ('A1-resolver-range-dropped', 'pointer-resolver', 'killed',
     '    return 1 <= lo <= hi <= cache[p]', '    return True'),
    ('A2-resolver-trailing-slash-kept', 'pointer-resolver', 'survived',
     "    p = path.rstrip('/')", '    p = path'),
    ('A3-lane-filter-dropped', 'pointer-resolver', 'survived',
     '        if not LANE.match(path):\n            continue',
     '        if False:\n            continue'),
    ('B1-shonen-first-box-only', 'unit-enumeration', 'killed',
     "        if m:\n            cur = 'shonen:' + m.group(1).strip()",
     "        if m and not any(k.startswith('shonen:') for k in u):\n            cur = 'shonen:' + m.group(1).strip()"),
    ('B2-frontier-section-dropped', 'unit-enumeration', 'survived',
     "    for head, prefix in (('## Core', 'prov_core:'), ('## Frontier', 'prov_frontier:')):",
     "    for head, prefix in (('## Core', 'prov_core:'),):"),
    ('C1-heading-stop-ignored', 'range-bounds', 'killed',
     '        if stop(lines[i]):\n            break',
     '        if stop(lines[i]):\n            continue'),
    ('C2-heading-upper-plus1', 'range-bounds', 'killed',
     '    return (start + 1, last + 1)', '    return (start + 1, last + 2)'),
    ('C3-heading-last-start-minus1', 'range-bounds', 'survived',
     '    last = start\n    for i in range(start + 1, len(lines)):',
     '    last = start - 1\n    for i in range(start + 1, len(lines)):'),
    ('D1-assertion-inverted', 'count-comparison', 'killed',
     '        if s is None or o is None or tuple(s) != tuple(o):',
     '        if s is None or o is None or tuple(s) == tuple(o):'),
    ('D2-mismatches-drops-assertions', 'count-comparison', 'survived',
     "    res['mismatches'] = len(unresolved) + len(failed)",
     "    res['mismatches'] = len(unresolved)"),
    ('E1-missing-units-ignored', 'guard-missing_units', 'survived',
     "    res['guards_ok'] = not missing_units and total >= base_total and not unrepaired",
     "    res['guards_ok'] = total >= base_total and not unrepaired"),
    ('E2-pointers-not-fewer-strict', 'guard-pointers_not_fewer', 'killed',
     "    res['guards_ok'] = not missing_units and total >= base_total and not unrepaired",
     "    res['guards_ok'] = not missing_units and total > base_total and not unrepaired"),
    ('E3-unrepaired-ignored', 'guard-unrepaired', 'survived',
     "    res['guards_ok'] = not missing_units and total >= base_total and not unrepaired",
     "    res['guards_ok'] = not missing_units and total >= base_total"),
    ('E4-base-resolution-at-rev', 'guard-bad_base', 'survived',
     '            if not resolves(root, base, path, a, b, {}):',
     '            if not resolves(root, rev, path, a, b, cache):'),
    ('F1-met-target-or', 'count-comparison/target', 'killed',
     "    res['met_target'] = res['mismatches'] == 0 and res['guards_ok']",
     "    res['met_target'] = res['mismatches'] == 0 or res['guards_ok']"),
]

results = []
for name, family, prediction, old, new in MUTANTS:
    entry = {'mutant': name, 'family': family, 'prediction': prediction,
             'old': old, 'new': new}
    n = txt.count(old)
    if n != 1:
        entry.update({'error': f'anchor occurs {n} times, skipped', 'killed': None,
                      'verdict': 'not-applied'})
        results.append(entry)
        continue
    msrc = txt.replace(old, new, 1).encode()
    assert sha(msrc) != frozen_before
    mp = os.path.join(MUTDIR, name + '.py')
    open(mp, 'wb').write(msrc)
    entry['mutant_sha256'] = sha(msrc)
    r = run([mp, '--selftest'])
    try:
        j = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        j = None
    fails = (j or {}).get('failures') or []
    entry.update({
        'rc': r.returncode,
        'selftest': j,
        'crash': r.returncode not in (0, 1),
        'stderr_tail': r.stderr[-400:] if r.returncode not in (0, 1) else '',
        'green_case_ok': j is not None and not any(f.startswith('green:') for f in fails),
        'killed': r.returncode != 0,
        'verdict': 'killed' if r.returncode != 0 else 'SURVIVED',
    })
    results.append(entry)
    os.remove(mp)

frozen_after = sha(open(FROZEN, 'rb').read())
out = {
    'seat': 'R38MutC2',
    'frozen_counter_disk_sha256_before': frozen_before,
    'frozen_counter_disk_sha256_after': frozen_after,
    'frozen_counter_untouched': frozen_before == frozen_after,
    'provenance': provenance,
    'baseline': baseline,
    'lane_base_donothing': lane_summary,
    'mutants': results,
    'summary': {
        'applied': sum(1 for e in results if 'error' not in e),
        'killed': sorted(e['mutant'] for e in results if e.get('killed')),
        'survived': sorted(e['mutant'] for e in results if e.get('killed') is False),
    },
}
json.dump(out, open(os.path.join(ART, 'results.json'), 'w'), indent=1, sort_keys=True)
shutil.rmtree(MUTDIR, ignore_errors=True)
print(json.dumps(out['summary'], indent=1, sort_keys=True))
print(json.dumps(out['provenance'], indent=1, sort_keys=True))
for e in results:
    st = e.get('selftest') or {}
    print(f"{e['mutant']:<34} pred={e['prediction']:<8} rc={e['rc']} "
          f"green={e.get('green_case_ok')} verdict={e['verdict']} "
          f"fails={st.get('failures')}")
