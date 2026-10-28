import copy, json, os, subprocess, sys, importlib.util
S = '/fast/scratch/hyaku/kaidoku-r49/W2Honesty'
CL = S + '/atk/A1/clone'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
IDS = ['v1le', 'v1be', 'v2le', 'v2be']
os.environ['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'; os.environ['TMPDIR'] = S
def dump(e): return json.dumps(e, indent=1, sort_keys=True) + '\n'
envs = {}
for i in IDS:
    raw = subprocess.run(['git', '-C', CL, 'show', 'HEAD:corpus/evidence/round-44/c1/%s/after.json' % i], capture_output=True, check=True).stdout
    e = json.loads(raw)
    out = '%s/atk/A1/%s/rea-out' % (S, i)
    e['parameters']['output_directory'] = out
    e['normalized_result']['output_directory'] = out
    envs[i] = e
spec = importlib.util.spec_from_file_location('c1ctl', CL + '/tools/round-49/c1-controls.py')
ctl = importlib.util.module_from_spec(spec); cwd = os.getcwd(); os.chdir(CL); spec.loader.exec_module(ctl); os.chdir(cwd)
os.makedirs(S + '/atk/A1/mint', exist_ok=True)
os.chdir(CL); minted = ctl.mint_evidence_ids(S + '/atk/A1/mint', PKG, envs)
for i, e in envs.items():
    e['evidence_id'] = minted[i]
    p = os.path.join(CL, 'corpus/evidence/round-49/c1/%s/after.json' % i)
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(dump(e))
print('minted', minted)
