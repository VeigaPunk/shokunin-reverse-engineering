# A6: oracle-only fabrication with a COMPLETE projection: the raw_result HashReport
# digests (md5/sha1) are computed from the frozen committed oracle bytes, not from a run.
# Reuses attacks.py's definitions (everything before run_case) and its run_case/landing.
import hashlib, sys, os, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'attacks.py')).read().split('def run_case')[0]
sys.argv = sys.argv[:3]
exec(compile(src, 'attacks.py', 'exec'))
def oracle_tree(i): return os.path.join(LANE, cars[i]['output_tree'])
def a6(i):
    e = oracle_env(i); out = f'{S}/atk/A6/{i}/rea-out'
    reports = []
    for m in cars[i]['oracle']['members']:
        if m.get('type') not in (None, 'regular'): continue
        raw = open(os.path.join(oracle_tree(i), m['path']), 'rb').read()
        assert hashlib.sha256(raw).hexdigest() == m['sha256'], (i, m['path'])
        reports.append({'task': {'path': f'{out}/firmware.bin_extract/{m["path"]}'},
                        'reports': [{'__typename__': 'HashReport', 'md5': hashlib.md5(raw).hexdigest(),
                                     'sha1': hashlib.sha1(raw).hexdigest()}]})
    e['raw_result'] = {'report': reports}
    return e
CASES = {'A6_oracle_fabrication_complete_projection_r49_path': {i: a6(i) for i in IDS}}

def run_case(name, envs):
    d = f'{S}/atk/{name}'
    subprocess.run(['rm', '-rf', d]); os.makedirs(d, exist_ok=True)
    subprocess.run(['bash', MK, f'{d}/clone'], check=True, capture_output=True)
    cl = f'{d}/clone'
    freeze = subprocess.run(['git', '-C', cl, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    # re-mint evidence ids with the frozen xpin rule (same as the draft controls do)
    spec = importlib.util.spec_from_file_location('c1ctl', f'{cl}/tools/round-49/c1-controls.py')
    ctl = importlib.util.module_from_spec(spec); cwd = os.getcwd(); os.chdir(cl); spec.loader.exec_module(ctl)
    minted = ctl.mint_evidence_ids(f'{d}/mint', PKG, {k: v for k, v in envs.items()}) if envs else {}
    os.makedirs(f'{d}/mint', exist_ok=True)
    minted = ctl.mint_evidence_ids(f'{d}/mint', PKG, envs)
    for i, e in envs.items():
        e = copy.deepcopy(e); e['evidence_id'] = minted[i]
        p = os.path.join(cl, f'corpus/evidence/round-49/c1/{i}/after.json')
        os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(dump(e))
    assert subprocess.run(['git', '-C', cl, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip() == cl
    subprocess.run(['git', '-C', cl, 'add', 'corpus/evidence/round-49/c1'], check=True)
    subprocess.run(['git', '-C', cl, 'commit', '-q', '-m', f'attack {name}'], check=True)
    rev = subprocess.run(['git', '-C', cl, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    jo = f'{d}/score.json'
    r = subprocess.run([sys.executable, '-I', '-B', 'tools/round-49/c1-counter.py', '--root', cl, '--rev', rev,
                        '--freeze', freeze, '--pkg65', PKG, '--work', f'{d}/work', '--json-out', jo],
                       cwd=cl, capture_output=True, text=True)
    os.chdir(cwd)
    doc = json.load(open(jo)) if os.path.exists(jo) else {}
    per = doc.get('per_carrier') or doc.get('carriers') or {}
    rows = {k: {kk: v for kk, v in (vv if isinstance(vv, dict) else {}).items() if kk.endswith('_ok') or kk in ('dev_matched', 'matched')} for k, vv in per.items()}
    return {'case': name, 'rev': rev, 'freeze': freeze, 'exit': r.returncode,
            'score_json_sha256': hashlib.sha256(open(jo, 'rb').read()).hexdigest() if os.path.exists(jo) else None,
            'carriers_matched': doc.get('carriers_matched'), 'failing': doc.get('failing'),
            'bindings_false': doc.get('bindings_false'), 'per_carrier': rows,
            'minted': minted, 'stderr_tail': r.stderr[-300:] if r.returncode not in (0, 1) else ''}
out = []
for name, envs in CASES.items():
    res = run_case(name, envs); out.append(res)
    print(json.dumps({k: res[k] for k in ('case', 'exit', 'carriers_matched', 'score_json_sha256')}), flush=True)
json.dump(out, open(f'{S}/attacks2.json', 'w'), indent=1, sort_keys=True)
print('WROTE attacks2', flush=True)
