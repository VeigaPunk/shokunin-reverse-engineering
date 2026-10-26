#!/usr/bin/env python3
"""R41W2C2Table: interpreter-vs-evaluator divergence probes at e9a24d07.

Runs the frozen v3 interpreter (reads only the SKILL v3 table) against the
frozen independent evaluator (applies the claims' precedence text) on
hand-built envelopes whose feature tuples sit on table-vs-precedence seams.
No carrier, no REA run, no lane write: envelopes and outputs live in scratch.
"""
import importlib.util
import json
import subprocess
import sys

BASE = '/fast/scratch/hyaku/kaidoku-r41/R41W2C2Table'
INTERP = BASE + '/sqfs-triage-v3.e9a2.py'
SKILL = BASE + '/SKILL.e9a2.md'
EVAL = BASE + '/pinned-indep-eval-v3.py'
OUT = BASE + '/divergence-results.json'

spec = importlib.util.spec_from_file_location('evalv3', EVAL)
evalv3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evalv3)


def run_interp(env, name, as_json=False):
    path = BASE + '/env-%s.json' % name
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(env, fh, indent=1, sort_keys=True)
    argv = [sys.executable, '-I', '-B', INTERP, '--skill', SKILL]
    if as_json:
        argv.append('--json')
    argv.append(path)
    res = subprocess.run(argv, capture_output=True, text=True)
    return {'exit': res.returncode, 'stdout': res.stdout.strip(),
            'stderr': res.stderr.strip()[:300]}


cases = {
    # sanity: harness agreement on plain classes
    'sanity-clean': dict(p=3),
    'sanity-avm': dict(gaps=("extractor-failure",),
                       argv="sasquatch-v4be -no-exit-code -f -d out in", p=0),
    # seam 1: clause 3 "D holds" (membership) vs exact-set dep cells
    'dep-both-names': dict(handlers=("squashfs_v4_be",),
                           gaps=("missing-extractor-dependency",),
                           deps=("sasquatch-v4be", "sasquatch"), p=0),
    'dep-superset-other': dict(handlers=("squashfs_v4_be",),
                               gaps=("missing-extractor-dependency",),
                               deps=("sasquatch-v4be", "other-tool"), p=0),
    # seam 2: clause 5 "failing chunk's handler (else H)" vs any-H fnmatch cell
    'step5-failing-chunk-le': dict(handlers=("squashfs_v4_be", "squashfs_v4_le"),
                                   gaps=("extractor-failure",),
                                   gap_handlers={"extractor-failure": "squashfs_v4_le"},
                                   argv="sasquatch-v4be -no-exit-code -f -d out in", p=0),
    # seam 3 (disclosed): clause 2 v4-only vs handler-cell `none` = no squashfs*
    'v1v3-only-chunk': dict(handlers=("squashfs_v3_be",), p=0),
    # seam 4: BE = n/a must never satisfy the avm row's `no` cell
    'timeout-no-argv': dict(handlers=("squashfs_v4_be",),
                            gaps=("extractor-failure",), p=0),
}

results = {}
for name, kw in cases.items():
    env = evalv3._env(**kw)
    feats = evalv3.features(env)
    label, action, step = evalv3.classify(feats)
    interp = run_interp(env, name)
    interp_line = None
    if interp['exit'] == 0 and interp['stdout']:
        parts = interp['stdout'].split('\t')
        interp_line = parts[1:] if len(parts) >= 3 else interp['stdout']
    results[name] = {
        'features': {k: feats[k] for k in ('OP', 'PR', 'H', 'HF', 'G', 'D', 'BE', 'SR', 'P')},
        'evaluator': {'label': label, 'action': action, 'step': step},
        'interpreter': interp_line,
        'interp_exit': interp['exit'],
        'interp_stderr': interp['stderr'],
    }

# timeout report shape: does a recorded `cmd` (ExtractorTimedOut) move BE?
env_cmd = evalv3._env(handlers=("squashfs_v4_be",), gaps=("extractor-failure",), p=0)
env_cmd['normalized_result']['diagnostics'] = [
    {'report': {'__typename__': 'ExtractorTimedOut', 'severity': 'ERROR',
                'cmd': 'sasquatch-v4be -no-exit-code -f -d out in', 'timeout': 120.0}}]
feats_cmd = evalv3.features(env_cmd)
res_cmd = run_interp(env_cmd, 'timeout-cmd-recorded', as_json=True)
results['timeout-cmd-recorded'] = {
    'features': {k: feats_cmd[k] for k in ('H', 'HF', 'G', 'D', 'BE', 'SR', 'P')},
    'evaluator': dict(zip(('label', 'action', 'step'), evalv3.classify(feats_cmd))),
    'interpreter_json': res_cmd,
}

# table-only and selftest on the pinned bytes
for tag, extra in (('table-only', ['--table-only']), ('selftest', ['--selftest'])):
    res = subprocess.run([sys.executable, '-I', '-B', INTERP, '--skill', SKILL] + extra,
                         capture_output=True, text=True)
    results['interp-' + tag] = {'exit': res.returncode,
                                'stdout': res.stdout.strip()[:400],
                                'stderr': res.stderr.strip()[:200]}
res = subprocess.run([sys.executable, '-I', '-B', EVAL, '--selftest'],
                     capture_output=True, text=True)
results['evaluator-selftest'] = {'exit': res.returncode,
                                 'stdout': res.stdout.strip()[:400],
                                 'stderr': res.stderr.strip()[:200]}

with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(results, fh, indent=1, sort_keys=True)

for name in list(cases) + ['timeout-cmd-recorded']:
    r = results[name]
    ev = r['evaluator']
    ip = r.get('interpreter')
    print('%-26s eval=(%s, %s, step %s)  interp=%s' %
          (name, ev['label'], ev['action'], ev.get('step'), ip))
for tag in ('interp-table-only', 'interp-selftest', 'evaluator-selftest'):
    print('%-26s exit=%s  %s' % (tag, results[tag]['exit'],
                                 results[tag]['stdout'].replace('\n', ' | ')[:160]))
print('BE on cmd-shaped timeout:', results['timeout-cmd-recorded']['features']['BE'],
      '| interpreter json exit', results['timeout-cmd-recorded']['interpreter_json']['exit'])
