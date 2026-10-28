# Provenance attacks on the DRAFT C1 counter. Each case = one scratch clone at the
# dev freeze + committed receipts under corpus/evidence/round-49/c1/<id>/after.json,
# scored by the draft counter in full (default, rerun on). Usage: attacks.py <S> <lane>
import copy, hashlib, importlib.util, json, os, subprocess, sys
S, LANE = sys.argv[1], sys.argv[2]
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
MK = os.path.join(LANE, '.ufo/waves/round-49/draft/mkclone.sh')
CARS = os.path.join(LANE, '.ufo/waves/round-49/draft/tools/round-49/carriers.json')
IDS = ['v1le', 'v1be', 'v2le', 'v2be']
os.environ['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'; os.environ['TMPDIR'] = S
cars = {c['id']: c for c in json.load(open(CARS))['carriers']}
real = {i: json.load(open(f'{S}/real49/{i}/after.json')) for i in IDS}
r44 = {i: json.load(open(f'{LANE}/corpus/evidence/round-44/c1/{i}/after.json')) for i in IDS}
def dump(e): return json.dumps(e, indent=1, sort_keys=True) + '\n'
def rebase(env, old, new):
    # replace the old output directory and its parent (unblob-tee.sh lives there) everywhere
    txt = json.dumps(env, sort_keys=True)
    txt = txt.replace(old, new).replace(os.path.dirname(old), os.path.dirname(new))
    return json.loads(txt)
def set_outdir(env, out):
    e = copy.deepcopy(env); e['parameters']['output_directory'] = out
    e['normalized_result']['output_directory'] = out; return e
def oracle_env(i):
    """A65 fabrication: no REA run. Shape from the committed round-44 receipt (template),
    files/sizes/digests/chunk handler from the frozen oracle members, dir under /kaidoku-r49/."""
    c = cars[i]; out = f'{S}/atk/A5/{i}/rea-out'
    t = copy.deepcopy(r44[i]); nr = t['normalized_result']
    members = [m for m in c['oracle']['members'] if m.get('type') in (None, 'regular')]
    nr['files'] = [{'analysis_depth': 1, 'mime_type': 'text/plain', 'original_file_range': None,
                    'path': f'{out}/firmware.bin_extract/{m["path"]}',
                    'relative_path': f'firmware.bin_extract/{m["path"]}', 'reported_sha256': m['sha256'],
                    'runtime_address': None, 'sha256': m['sha256'], 'size': m['size']} for m in members]
    nr['published_bytes'] = sum(m['size'] for m in members)
    nr['chunks'][0]['handler'] = c['handler']
    nr['derivations'] = [d for d in nr['derivations'] if d['child_path'].startswith('$output/firmware.bin_extract/')
                         and d['child_path'] != '$output/firmware.bin_extract'] + \
        [{'child_path': '$output/firmware.bin_extract', 'handler': c['handler'],
          'parent_file_range': {'length': 4096, 'offset': 0}, 'parent_path': '$input',
          'provider_blob_id': nr['derivations'][0]['provider_blob_id']}]
    nr['derivations'] = [d for d in nr['derivations']]  # template children, frozen names
    nr['engine']['executable_path'] = f'{S}/atk/A5/{i}/unblob-tee.sh'
    nr['engine']['executable_sha256'] = '0' * 64
    nr['output_directory'] = out
    t['parameters']['output_directory'] = out; t['parameters']['path'] = f'{S}/atk/A5/{i}/carrier.bin'
    t['raw_result'] = {}; t['subject']['digest']['sha256'] = c['sha256']
    return t
CASES = {}
CASES['P0_positive_real_rea_r49_path'] = {i: real[i] for i in IDS}
def a1(i):
    old = r44[i]['parameters']['output_directory']
    return set_outdir(r44[i], f'{S}/atk/A1/{i}/rea-out')
CASES['A1_r44_receipt_outdir_only_repointed'] = {i: a1(i) for i in IDS}
def a2(i):
    old = r44[i]['parameters']['output_directory']
    return rebase(r44[i], old, f'{S}/atk/A2/{i}/rea-out')
CASES['A2_r44_receipt_all_paths_rebased'] = {i: a2(i) for i in IDS}
def a3(i):
    old = real[i]['parameters']['output_directory']
    return rebase(real[i], old, f'/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-49/c1/{i}/kaidoku-r49/rea-out')
CASES['A3_real_r49_run_outdir_is_committed_path_plus_segment'] = {i: a3(i) for i in IDS}
CASES['A4_control_r44_receipt_reminted_unchanged_outdir'] = {i: r44[i] for i in IDS}
CASES['A5_oracle_fabrication_outdir_r49_no_run'] = {i: oracle_env(i) for i in IDS}

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
json.dump(out, open(f'{S}/attacks.json', 'w'), indent=1, sort_keys=True)
print('WROTE', f'{S}/attacks.json', flush=True)
