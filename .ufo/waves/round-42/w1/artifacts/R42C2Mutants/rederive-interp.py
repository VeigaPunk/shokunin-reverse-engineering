#!/usr/bin/env python3
"""R42C2Mutants: re-derive the round-41 interpreter/evaluator survivors on the
round-42 base bytes (c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c).

Kill check (identical to the round-41 detector):
  1. the tool's own --selftest must still pass on the mutant, and
  2. the (label, action) pairs over the 52 held-out envelopes must equal the
     pristine baseline.
Survived = both hold. Then each survivor is shown against its round-41 killing
envelope (kill/K*.json): pristine pair vs mutant pair on that single envelope.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # seat scratch
BASE = os.path.join(ROOT, 'base')
ENV = os.path.join(ROOT, 'env')
FLAT = os.path.join(ROOT, 'flat')
KILL = os.path.join(ROOT, 'kill')
OUT = os.path.join(ROOT, 'out')
SKILL = os.path.join(BASE, 'SKILL.md')
INTERP = 'sqfs-triage-v3.py'
EVAL = 'indep-eval-v3.py'
MUT = os.path.join(ROOT, 'muts')

# --- survivor specs, edits verbatim from the round-41 wave-2 artifacts -------
MUTANTS = [
    dict(id='I08', tool=INTERP, kill='K12',
         edits=[("        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:",
                 "        if isinstance(report, dict) and report.get('type') == SYMLINK_TYPENAME:")]),
    dict(id='I10', tool=INTERP, kill='K11',
         edits=[("        'P': len(_as_list(nr.get('files'))),",
                 "        'P': 1 if _as_list(nr.get('files')) else 0,")]),
    dict(id='I11', tool=INTERP, kill='K2',
         edits=[("        'P': len(_as_list(nr.get('files'))),",
                 "        'P': len(nr['files']) if isinstance(nr.get('files'), list) else 1,")]),
    dict(id='I14', tool=INTERP, kill='K3',
         edits=[("        if isinstance(handler, str) and handler.startswith('squashfs'):",
                 "        if isinstance(handler, str) and handler:")]),
    dict(id='E01', tool=EVAL, kill='K1',
         edits=[('    has = "-be" in tokens',
                 '    has = any("-be" in t for t in tokens)')]),
    dict(id='E04', tool=EVAL, kill='K8',
         edits=[('    if REMOVED_SYMLINK_TYPENAME in stdout:',
                 '    if False and REMOVED_SYMLINK_TYPENAME in stdout:')]),
    dict(id='E05', tool=EVAL, kill='K9',
         edits=[('    for diag in nr.get("diagnostics") or []:\n        for holder in (diag, diag.get("report") if isinstance(diag.get("report"), dict) else None):\n            if not isinstance(holder, dict):\n                continue\n            for key in TYPENAME_KEYS:',
                 '    for diag in nr.get("diagnostics") or []:\n        for holder in (diag.get("report") if isinstance(diag.get("report"), dict) else None,):\n            if not isinstance(holder, dict):\n                continue\n            for key in TYPENAME_KEYS:')]),
    dict(id='E07', tool=EVAL, kill='K11',
         edits=[('    p = len(files) if isinstance(files, list) else 0',
                 '    p = 1 if isinstance(files, list) and files else 0')]),
    dict(id='E08', tool=EVAL, kill='K5',
         edits=[('    if "missing-extractor-dependency" in g:\n        if BE_DEPENDENCY in d:\n            return _done("dep-missing-be", 3)\n        if LE_DEPENDENCY in d:\n            return _done("dep-missing-le", 3)\n        # neither name present: step 3 states no outcome; fall through.\n    # 4\n    if "extractor-failure" in g and p > 0:\n        return _done("partial-body-failure", 4)',
                 '    # 4\n    if "extractor-failure" in g and p > 0:\n        return _done("partial-body-failure", 4)\n    if "missing-extractor-dependency" in g:\n        if BE_DEPENDENCY in d:\n            return _done("dep-missing-be", 3)\n        if LE_DEPENDENCY in d:\n            return _done("dep-missing-le", 3)\n        # neither name present: step 3 states no outcome; fall through.')]),
]


def run(a):
    return subprocess.run(a, capture_output=True, text=True)


def interp_pairs(exe, paths):
    r = run([sys.executable, '-I', '-B', exe, '--skill', SKILL, *paths])
    if r.returncode != 0:
        return None, r
    pairs = {}
    for line in r.stdout.splitlines():
        if line.strip():
            p, l, a = line.split('\t')
            pairs[os.path.splitext(os.path.basename(p))[0]] = [l, a]
    return pairs, r


def eval_pairs(exe, dirp):
    r = run([sys.executable, '-I', '-B', exe, '--envelopes', dirp])
    if r.returncode != 0:
        return None, r
    doc = json.loads(r.stdout)
    return {k: [v['label'], v['action']] for k, v in doc['labels'].items()}, r


def selftest(exe):
    r = run([sys.executable, '-I', '-B', exe, '--selftest'])
    tail = (r.stdout or '')[-160:] + (r.stderr or '')[-160:]
    return r.returncode, tail


def one_interp(exe, path):
    pr, r = interp_pairs(exe, [path])
    if pr is None:
        return 'EXIT%d' % r.returncode
    return pr[os.path.splitext(os.path.basename(path))[0]]


def one_eval(exe, path):
    iso = tempfile.mkdtemp(prefix='kc.', dir=OUT)
    with open(path, 'rb') as fh:
        data = fh.read()
    with open(os.path.join(iso, 'env.json'), 'wb') as fh:
        fh.write(data)
    pr, r = eval_pairs(exe, iso)
    shutil.rmtree(iso, ignore_errors=True)
    if pr is None:
        return 'EXIT%d' % r.returncode
    return next(iter(pr.values()))


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    os.makedirs(MUT, exist_ok=True)
    pristine = {INTERP: os.path.join(BASE, INTERP), EVAL: os.path.join(BASE, EVAL)}
    ib, _ = interp_pairs(pristine[INTERP], sorted(
        os.path.join(ENV, f) for f in os.listdir(ENV)))
    eb, _ = eval_pairs(pristine[EVAL], FLAT)
    assert ib and len(ib) == 52 and eb and len(eb) == 52, 'baseline broken'
    results = {'base_sha': {t: sha(p) for t, p in pristine.items()},
               'skill_sha': sha(SKILL), 'mutants': []}
    for spec in MUTANTS:
        src = open(pristine[spec['tool']], encoding='utf-8').read()
        for old, new in spec['edits']:
            n = src.count(old)
            assert n == 1, '%s anchor x%d' % (spec['id'], n)
            src = src.replace(old, new)
        mp = os.path.join(MUT, '%s-%s' % (spec['tool'], spec['id']))
        with open(mp, 'w', encoding='utf-8') as fh:
            fh.write(src)
        st_exit, st_tail = selftest(mp)
        pairs, r = (interp_pairs(mp, sorted(os.path.join(ENV, f) for f in os.listdir(ENV)))
                    if spec['tool'] == INTERP else eval_pairs(mp, FLAT))
        base = ib if spec['tool'] == INTERP else eb
        changed = None if pairs is None else sorted(
            k for k in set(base) | set(pairs) if base.get(k) != pairs.get(k))
        survived = st_exit == 0 and pairs is not None and not changed
        row = {'id': spec['id'], 'tool': spec['tool'], 'kill_case': spec['kill'],
               'mutant_sha256': sha(mp), 'selftest_exit': st_exit,
               'pairs_exit': r.returncode, 'pairs_changed': changed,
               'verdict': 'SURVIVED' if survived else 'KILLED',
               'selftest_tail': st_tail}
        kill = os.path.join(KILL, '%s.json' % spec['kill']) \
            if os.path.exists(os.path.join(KILL, '%s.json' % spec['kill'])) else None
        if kill is None:
            cand = [f for f in os.listdir(KILL) if f.startswith(spec['kill'] + '-')]
            kill = os.path.join(KILL, cand[0]) if cand else None
        if kill:
            pp = one_interp(pristine[INTERP], kill)
            pm = one_interp(mp, kill) if spec['tool'] == INTERP else None
            if spec['tool'] == EVAL:
                pp = one_eval(pristine[EVAL], kill)
                pm = one_eval(mp, kill)
            row['kill_case_path'] = os.path.basename(kill)
            row['kill_pristine_pair'] = pp
            row['kill_mutant_pair'] = pm
            row['kill_flips'] = pp != pm
        results['mutants'].append(row)
        print('%-4s %-18s %-8s selftest=%d pairs_changed=%s kill=%s %s -> %s flip=%s'
              % (spec['id'], spec['tool'], row['verdict'], st_exit,
                 (len(changed) if changed is not None else 'EXIT%d' % r.returncode),
                 row.get('kill_case_path'), row.get('kill_pristine_pair'),
                 row.get('kill_mutant_pair'), row.get('kill_flips')))
        sys.stdout.flush()
    with open(os.path.join(OUT, 'rederive-interp.json'), 'w') as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    n_surv = sum(1 for m in results['mutants'] if m['verdict'] == 'SURVIVED')
    print('DONE %d mutants, %d survived (expected 9)' % (len(results['mutants']), n_surv))


if __name__ == '__main__':
    main()
