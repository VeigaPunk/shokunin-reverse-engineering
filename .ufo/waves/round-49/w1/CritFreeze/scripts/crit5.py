import json, os, sys, subprocess, shutil, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crit as C
from crit import g, mkrepo, commit, write, FREEZE
res = {}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def head(d): return g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
def both(name, d, rev, freeze=FREEZE):
    C.FREEZE = freeze
    rec = {'rev': rev, 'c1_walk': C.c1_walk(d, rev), 'c2_walk': C.c2_walk(d, rev)}
    res[name] = rec; print(json.dumps({name: rec}, sort_keys=True), flush=True)

# S19 corrected: receipt stamped by an ALTERED counter copy at a scratch path
os.makedirs(os.path.join(C.S, 'alt'), exist_ok=True)
src = open(os.path.join(C.S, 'frozen', 'c1-counter.py')).read()
alt1 = os.path.join(C.S, 'alt', 'c1-counter-altered.py')
open(alt1, 'w').write(src + '\n# altered after freeze\n')
rec = os.path.join(C.S, 'alt', 'receipt-altered.json')
json.dump({'counter': alt1, 'counter_sha256': sha(alt1), 'exit_code': 0}, open(rec, 'w'))
p = subprocess.run([sys.executable, '-I', '-B', os.path.join(C.S, 'frozen', 'c1-counter.py'), '--verify-receipt', rec],
                   capture_output=True, cwd=C.S, env=C.ENV)
res['S19_verify_receipt_altered_counter'] = {'exit': p.returncode, 'stdout': p.stdout.decode().strip(),
    'freeze_c1_sha256': sha(os.path.join(C.S, 'frozen', 'c1-counter.py')), 'altered_sha256': sha(alt1)}
print(json.dumps({'S19': res['S19_verify_receipt_altered_counter']}, sort_keys=True))

# S20 altered C1 (frozen_drift returns []) run from OUTSIDE the lane on a REV the frozen gate refuses
alt2 = os.path.join(C.S, 'alt', 'c1-counter-gate-off.py')
open(alt2, 'w').write(src.replace('def frozen_drift(root, freeze, rev, spec):\n', 'def frozen_drift(root, freeze, rev, spec):\n    return []\n', 1))
d = os.path.join(C.S, 'sc', 'S1a_touch_restore_c1counter'); rev = head(d)
w = os.path.join(C.S, 'cli-work', 'S20'); shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
for label, path in [('frozen_bytes', os.path.join(C.S, 'frozen', 'c1-counter.py')), ('gate_off_bytes', alt2)]:
    jo = os.path.join(w, label + '.json')
    p = subprocess.run([sys.executable, '-I', '-B', path, '--root', d, '--rev', rev, '--freeze', FREEZE, '--pkg65', C.PKG,
                        '--work', w, '--json-out', jo], capture_output=True, cwd=C.S, env=C.ENV, timeout=240)
    j = json.load(open(jo))
    res['S20_' + label] = {'path': path, 'sha256': sha(path), 'exit': p.returncode, 'reason': j.get('reason'),
                           'frozen_path_changed': j.get('frozen_path_changed'), 'carriers_matched': j.get('carriers_matched')}
    print(json.dumps({'S20_' + label: res['S20_' + label]}, sort_keys=True), flush=True)

# S24 plan edit after freeze; S25 round-42 frozen tool edit; S26 round-44 oracle edit
def edit(rel, text='\n# probe\n'):
    def f(d):
        with open(os.path.join(d, rel), 'a') as fh: fh.write(text)
        g(d, 'add', '-A'); return commit(d, 'edit ' + rel)
    return f
for name, rel in [('S24_plan_edit', 'plans/round-49-claims.md'), ('S25_round42_frozen_tool_edit', 'tools/round-42/fixtures.json'),
                  ('S26_round44_oracle_edit', None)]:
    d = mkrepo(name)
    if rel is None:
        rel = g(d, 'ls-tree', '-r', '--name-only', 'HEAD', 'corpus/evidence/round-44/oracle').stdout.decode().split('\n')[0]
    rev = edit(rel)(d); both(name, d, rev); res[name]['path'] = rel

json.dump(res, open(os.path.join(C.S, 'results-walk5.json'), 'w'), indent=1, sort_keys=True)
