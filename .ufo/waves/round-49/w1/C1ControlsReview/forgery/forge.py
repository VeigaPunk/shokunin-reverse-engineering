import json, os, subprocess, sys, importlib.util, hashlib, shutil, time
CL = '/fast/scratch/hyaku/kaidoku-r49/C1ControlsReview/clone'
W = '/fast/scratch/hyaku/kaidoku-r49/C1ControlsReview/work2'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
POSTREE = '/fast/scratch/hyaku/kaidoku-r49/C1ControlsReview/work/ctl-out/pos/tree'
os.chdir(CL)
FREEZE = subprocess.run(['git', '-C', CL, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
spec = importlib.util.spec_from_file_location('c1c', CL + '/tools/round-49/c1-controls.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
DOCS = ['PROVINCE.md', 'corpus/README.md', 'corpus/SOURCES.md', 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md']
CARR = {'v1le': 'v1le', 'v1be': 'v1be', 'v2le': 'v2le', 'v2be': 'v2be'}

def load_r44(cid):
    return json.load(open(L + '/corpus/evidence/round-44/c1/%s/after.json' % cid))

def load_heldout(cid):
    m = {'v1le': 'H41', 'v1be': 'H43', 'v2be': 'H44', 'v2le': 'H45'}[cid]
    d = json.load(open(L + '/corpus/evidence/round-42/c2/heldout/%s/envelope.json' % m))
    return d.get('data') if isinstance(d.get('data'), dict) else d

def sandbox(name):
    d = os.path.join(W, 'sb-' + name); shutil.rmtree(d, ignore_errors=True)
    subprocess.run(['git', 'clone', '--shared', '--no-checkout', '-q', CL, d], check=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    for k, v in [('user.name', 'r49-forge-probe'), ('user.email', 'forge@r49.invalid'), ('commit.gpgsign', 'false')]:
        subprocess.run(['git', '-C', d, 'config', k, v], check=True)
    subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', FREEZE], check=True)
    return d

def run(name, envs, rewrite, remint):
    wk = os.path.join(W, name); shutil.rmtree(wk, ignore_errors=True); os.makedirs(wk)
    out = {}
    for cid, env in envs.items():
        env = json.loads(json.dumps(env))
        if rewrite:
            od = '/fast/scratch/hyaku/kaidoku-r49/forge-%s/%s/extract' % (name, cid)
            env.setdefault('parameters', {})['output_directory'] = od
            if isinstance(env.get('normalized_result'), dict):
                env['normalized_result']['output_directory'] = od
        out[cid] = env
    if remint:
        minted = mod.mint_evidence_ids(wk, PKG, out)
        for cid in out: out[cid]['evidence_id'] = minted[cid]
    d = sandbox(name)
    files = {}
    for rel in DOCS:
        files[rel] = open(os.path.join(POSTREE, rel), 'rb').read()
    for cid, env in out.items():
        files['corpus/evidence/round-49/c1/%s/after.json' % cid] = (json.dumps(env, indent=1, sort_keys=True) + '\n').encode()
    for rel, raw in files.items():
        p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(raw)
    subprocess.run(['git', '-C', d, 'add', '--'] + sorted(files), check=True)
    subprocess.run(['git', '-C', d, 'commit', '-q', '-m', 'forge probe ' + name], check=True)
    rev = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    jo = os.path.join(wk, 'counter.json')
    argv = [sys.executable, '-I', '-B', d + '/tools/round-49/c1-counter.py', '--root', d, '--rev', rev, '--freeze', FREEZE,
            '--pkg65', PKG, '--work', wk, '--json-out', jo]
    t0 = time.time(); r = subprocess.run(argv, capture_output=True, cwd=wk); wall = time.time() - t0
    doc = json.load(open(jo)) if os.path.isfile(jo) else {}
    cars = doc.get('carriers') or {}
    res = {'name': name, 'rev': rev, 'exit': r.returncode, 'wall_s': round(wall, 1),
           'stdout_sha256': hashlib.sha256(r.stdout).hexdigest(),
           'carriers_matched': doc.get('carriers_matched'), 'met_target': doc.get('met_target'),
           'bindings_false': doc.get('bindings_false'),
           'per_carrier_failing': {k: sorted(n for n, v in c.items() if isinstance(v, bool) and v is False) for k, c in cars.items()},
           'receipts_planted': {cid: hashlib.sha256((json.dumps(e, indent=1, sort_keys=True) + '\n').encode()).hexdigest() for cid, e in out.items()},
           'evidence_ids': {cid: e.get('evidence_id') for cid, e in out.items()},
           'output_directory': {cid: (e.get('parameters') or {}).get('output_directory') for cid, e in out.items()}}
    print(json.dumps(res, sort_keys=True, indent=1)); sys.stdout.flush()
    return res

results = []
which = sys.argv[1:] or ['A', 'B', 'C', 'D']
cids = ['v1le', 'v1be', 'v2le', 'v2be']
if 'A' in which:  # round-44 committed receipts, output_directory string-rewritten, evidence id re-minted
    results.append(run('A-r44-rewrite-remint', {c: load_r44(c) for c in cids}, True, True))
if 'B' in which:  # round-42 heldout envelopes (the driver's CTL-C1-4 source), rewritten + re-minted
    results.append(run('B-heldout-rewrite-remint', {c: load_heldout(c) for c in cids}, True, True))
if 'C' in which:  # round-44 receipts UNMODIFIED (the plan's shortcut as written), docs planted
    results.append(run('C-r44-verbatim', {c: load_r44(c) for c in cids}, False, False))
if 'D' in which:  # round-44 rewritten but id NOT re-minted (stale id)
    results.append(run('D-r44-rewrite-stale-id', {c: load_r44(c) for c in cids}, True, False))
json.dump(results, open(os.path.join(W, 'results-%s.json' % ''.join(which)), 'w'), indent=1, sort_keys=True)
