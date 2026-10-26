#!/usr/bin/env python3
"""Score the R40-C2 pre-freeze controls on the 26 development envelopes (seed sha256("dev40")).

Each control is a SKILL-shaped file holding a v2 table; the frozen interpreter
tools/round-40/sqfs-triage-v2.py labels every dev envelope; a control meets the target only
if all 26 (label, action) pairs equal the generator's. Writes one JSON receipt with the
interpreter exit code per control. Usage: score-c2-controls.py LANE OUT.json
"""
import gzip, json, os, subprocess, sys, tempfile
lane, out = sys.argv[1], sys.argv[2]
dev = os.path.join(lane, '.ufo/waves/round-40/w1/artifacts/R40C2HeldoutGen/dev-run')
ctl = os.path.join(lane, '.ufo/waves/round-40/controls/c2')
interp = os.path.join(lane, 'tools/round-40/sqfs-triage-v2.py')
man = json.load(open(os.path.join(dev, 'manifest.json')))
td = tempfile.mkdtemp(dir=os.environ.get('TMPDIR'))
envs = []
for c in man['carriers']:
    p = os.path.join(td, c['id'] + '.json')
    open(p, 'wb').write(gzip.open(os.path.join(dev, c['id'], 'envelope.json.gz')).read())
    envs.append((c, p))
tables = sorted(f for f in os.listdir(ctl) if f.endswith('.md')) + ['ADOPTED:SKILL.md']
res = {'n': len(envs), 'dev_seed': man.get('seed'), 'controls': {}}
for t in tables:
    path = os.path.join(lane, 'SKILL.md') if t.startswith('ADOPTED') else os.path.join(ctl, t)
    p = subprocess.run([sys.executable, '-I', '-B', interp, '--skill', path] + [e for _, e in envs],
                       capture_output=True, text=True)
    got = {}
    for line in p.stdout.splitlines():
        f = line.split('\t')
        if len(f) >= 3:
            got[os.path.basename(f[0])[:-5]] = (f[1].strip(), f[2].strip())
    matched = sum(1 for c, _ in envs if got.get(c['id']) == (c['label'], c['action']))
    wrong = sorted({c['class'] for c, _ in envs if got.get(c['id']) != (c['label'], c['action'])})
    res['controls'][t] = {'interpreter_exit': p.returncode, 'matched': matched,
                          'meets_target': p.returncode == 0 and matched == len(envs),
                          'wrong_classes': wrong}
json.dump(res, open(out, 'w'), indent=1, sort_keys=True)
for t, r in res['controls'].items():
    print('%-22s exit=%s matched=%2d/%d meets=%s wrong=%s' % (t, r['interpreter_exit'], r['matched'], len(envs), r['meets_target'], ','.join(r['wrong_classes'])))
