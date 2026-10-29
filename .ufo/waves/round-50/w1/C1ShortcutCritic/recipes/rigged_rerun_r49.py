#!/usr/bin/env python3
# Round-49 counter at its landing revision 29883d4 (clone --shared, detached), with a PATH-first
# `npx` shim and a pin->receipt map. NOTE (measured): round-49 make_real_runner overwrites
# env PATH with FIXED_PATH (c1-counter.py:1896), so the shim is NOT invoked (rerun_argv_count 0);
# both runs are honest REA reruns (7.5 s, 4 KB fixtures). The swap run is therefore a null
# control, not a binding test. The npm-cache route that DOES bind is in W2C1Forge.md und5.
import os, subprocess, json, hashlib, stat, time
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r50/C1ShortcutCritic/rigged'
os.makedirs(S, exist_ok=True)
env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku', GIT_NO_REPLACE_OBJECTS='1')
C = os.path.join(S, 'clone')
if not os.path.isdir(C):
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, C], check=True)
subprocess.run(['git', '-C', C, 'checkout', '-q', '--detach', '29883d4ec35a31a8393c4ffb220888c44c0bb022'], check=True)
REV = subprocess.check_output(['git', '-C', C, 'rev-parse', 'HEAD']).decode().strip()
carr = json.loads(subprocess.check_output(['git', '-C', C, 'show', f'{REV}:tools/round-49/carriers.json']))
pinmap, recs = {}, {}
for c in carr['carriers']:
    rp = c.get('receipt') or f"corpus/evidence/round-49/c1/{c['id']}/after.json"
    p = os.path.join(S, f"rec-{c['id']}.json")
    open(p, 'wb').write(subprocess.check_output(['git', '-C', C, 'show', f'{REV}:{rp}']))
    pinmap[c['sha256']] = p; recs[c['id']] = p
shim = os.path.join(S, 'shimbin'); os.makedirs(shim, exist_ok=True)
npx = os.path.join(shim, 'npx')
open(npx, 'w').write('''#!/usr/bin/env python3
import sys, json, hashlib, os
argv = sys.argv[1:]
with open(os.environ['SHIM_LOG'], 'a') as f: f.write(json.dumps(argv) + '\\n')
if 'extract-firmware' not in argv: sys.exit(1)
inp = argv[-2]
sha = hashlib.sha256(open(inp, 'rb').read()).hexdigest()
p = json.load(open(os.environ['SHIM_MAP'])).get(sha)
if p is None:
    print(json.dumps({"ok": False, "error": "unknown carrier"})); sys.exit(0)
print(json.dumps({"ok": True, "data": json.load(open(p))}))
''')
os.chmod(npx, os.stat(npx).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
mp_true = os.path.join(S, 'map-true.json'); json.dump(pinmap, open(mp_true, 'w'))
sw = dict(pinmap); sw[carr['carriers'][0]['sha256']] = recs[carr['carriers'][1]['id']]
mp_swap = os.path.join(S, 'map-swap.json'); json.dump(sw, open(mp_swap, 'w'))
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
res = {}
for tag, mp in [('shim-true', mp_true), ('shim-swap', mp_swap)]:
    log = os.path.join(S, f'{tag}.argv.log')
    if os.path.exists(log): os.remove(log)
    e = dict(env, PATH=shim + ':' + os.environ['PATH'], SHIM_MAP=mp, SHIM_LOG=log)
    out = os.path.join(S, f'{tag}.json'); work = os.path.join(S, f'work-{tag}'); os.makedirs(work, exist_ok=True)
    t = time.time()
    r = subprocess.run(['python3', '-I', '-B', os.path.join(C, 'tools/round-49/c1-counter.py'), '--root', C,
                        '--rev', REV, '--freeze', 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d', '--pkg65', PKG,
                        '--work', work, '--json-out', out], capture_output=True, env=e, cwd=work, timeout=1500)
    doc = json.load(open(out)) if os.path.exists(out) else {}
    res[tag] = {'exit': r.returncode, 'wall_s': round(time.time() - t, 1),
                'stdout_sha256': hashlib.sha256(r.stdout).hexdigest(),
                'carriers_matched': doc.get('carriers_matched'), 'met_target': doc.get('met_target'),
                'rerun_argv_count': len(open(log).read().splitlines()) if os.path.exists(log) else 0}
json.dump({'rev': REV, 'runs': res}, open(os.path.join(S, 'rigged.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
