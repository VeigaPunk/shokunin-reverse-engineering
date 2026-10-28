# Adds the draft landing bytes (controls' _doc_landing: the wave-1 doc artifacts, unchanged)
# on top of each attack clone's receipt commit, then scores with the draft counter in full.
import importlib.util, json, os, subprocess, sys
S, LANE = sys.argv[1], sys.argv[2]; PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
DOC = os.path.join(LANE, '.ufo/waves/round-49/w1/artifacts')
os.environ['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'; os.environ['TMPDIR'] = S
out = []
for case in sys.argv[3:]:
    cl = f'{S}/atk/{case}/clone'
    freeze = subprocess.run(['git', '-C', cl, 'rev-parse', 'HEAD~1'], capture_output=True, text=True).stdout.strip()
    spec = importlib.util.spec_from_file_location('c1ctl', f'{cl}/tools/round-49/c1-controls.py')
    ctl = importlib.util.module_from_spec(spec); cwd = os.getcwd(); os.chdir(cl); spec.loader.exec_module(ctl)
    files, _ = ctl._doc_landing({'root': cl, 'freeze': freeze, 'doc_dir': DOC})
    for rel, raw in files.items():
        p = os.path.join(cl, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(raw)
    subprocess.run(['git', '-C', cl, 'add', '-A', '--', 'PROVINCE.md', 'corpus/README.md', 'corpus/SOURCES.md', 'corpus/knowledge'], check=True)
    subprocess.run(['git', '-C', cl, 'commit', '-q', '-m', f'attack {case}: draft landing bytes (wave-1 artifacts)'], check=True)
    rev = subprocess.run(['git', '-C', cl, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    d = f'{S}/atk/{case}'; jo = f'{d}/score-landed.json'
    r = subprocess.run([sys.executable, '-I', '-B', 'tools/round-49/c1-counter.py', '--root', cl, '--rev', rev,
                        '--freeze', freeze, '--pkg65', PKG, '--work', f'{d}/work-landed', '--json-out', jo],
                       cwd=cl, capture_output=True, text=True)
    os.chdir(cwd)
    doc = json.load(open(jo))
    res = {'case': case, 'rev': rev, 'freeze': freeze, 'landing_files': sorted(files), 'exit': r.returncode,
           'carriers_matched': doc.get('carriers_matched'), 'failing': doc.get('failing'),
           'bindings_false': doc.get('bindings_false'),
           'score_json_sha256': __import__('hashlib').sha256(open(jo, 'rb').read()).hexdigest()}
    out.append(res); print(json.dumps(res), flush=True)
json.dump(out, open(f'{S}/landing.json', 'w'), indent=1, sort_keys=True)
print('WROTE', flush=True)
