import os, subprocess, json, hashlib, time, sys
S = '/fast/scratch/hyaku/kaidoku-r49/W2C1Drift'
FRZ = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku')
FX = json.load(open(os.path.join(S, 'fx', 'index.json')))
only = sys.argv[1:]  # optional subset
out = {}
for name, meta in FX.items():
    if only and name not in only:
        continue
    d = os.path.join(S, 'fx', name)
    rev = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True, env=ENV).stdout.strip()
    assert rev == meta['head'], (name, rev)
    res = {'desc': meta['desc'], 'head': rev}
    # C2 freeze check (no battery) with the frozen copy
    cp = os.path.join(S, 'src', 'c2-mismatch.py')
    t0 = time.strftime('%FT%TZ', time.gmtime())
    p = subprocess.run(['python3', '-I', '-B', cp, '--root', d, '--rev', rev, '--freeze', FRZ,
                        '--json-out', os.path.join(S, 'fx', name + '.c2.json')], capture_output=True, env=ENV)
    j = json.load(open(os.path.join(S, 'fx', name + '.c2.json')))
    res['c2'] = {'utc': t0, 'exit': p.returncode, 'reason': j.get('reason'), 'detail': j.get('detail'), 'mismatches': j.get('mismatches')}
    # C1 with the frozen copy (fx12 uses its own edited copy)
    c1 = os.path.join(d, 'tools/round-49/c1-counter.py') if name == 'fx12-counter' else os.path.join(S, 'src', 'c1-counter.py')
    wd = os.path.join(S, 'fx', name + '.c1work'); os.makedirs(wd, exist_ok=True)
    t0 = time.strftime('%FT%TZ', time.gmtime())
    p = subprocess.run(['python3', '-I', '-B', c1, '--root', d, '--rev', rev, '--freeze', FRZ, '--pkg65', PKG,
                        '--work', wd, '--json-out', os.path.join(S, 'fx', name + '.c1.json')], capture_output=True, env=ENV)
    try:
        j = json.load(open(os.path.join(S, 'fx', name + '.c1.json')))
        res['c1'] = {'utc': t0, 'exit': p.returncode, 'carriers_matched': j.get('carriers_matched'),
                     'frozen_path_changed': j.get('frozen_path_changed'), 'failing': j.get('failing')[:8] if isinstance(j.get('failing'), list) else j.get('failing'),
                     'reason': j.get('reason'), 'detail': j.get('detail')}
    except Exception as e:
        res['c1'] = {'utc': t0, 'exit': p.returncode, 'stderr_tail': p.stderr.decode(errors='replace')[-400:], 'err': str(e)}
    out[name] = res
    print(name, json.dumps(res)[:700], flush=True)
json.dump(out, open(os.path.join(S, 'fx', 'results%s.json' % ('-' + '-'.join(only) if only else '')), 'w'), indent=1)
