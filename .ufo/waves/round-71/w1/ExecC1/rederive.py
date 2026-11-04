import collections
import copy
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-71/w1/ExecC1'
SCRATCH = Path('/fast/scratch/hyaku/kaidoku-r71/ExecC1')
REV = 'b827a8b5d54f2885ec9be7786389f356c59226ce'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2) + '\n')

def invoke(name, argv, env=None):
    result = subprocess.run(argv, cwd=SCRATCH, env=env, capture_output=True, text=True)
    (OUT / (name + '.stdout')).write_text(result.stdout)
    (OUT / (name + '.stderr')).write_text(result.stderr)
    record = {'argv': argv, 'returncode': result.returncode}
    save(name + '.command.json', record)
    return result

try:
    nonce = secrets.token_bytes(32).hex()
    commitment = hashlib.sha256(nonce.encode('ascii')).hexdigest()
    # Commit the hash to retained evidence before launching the route.
    (OUT / 'nonce-commitment.txt').write_text(commitment + '\n')
    tool = str(SCRATCH / 'packed-elf.py')
    prefix = [sys.executable, '-I', '-B', tool, '--root', str(ROOT), '--rev', REV]
    env = dict(os.environ, KAIDOKU_ENV_CANARY='probe')
    route = invoke('route', prefix + ['--pkg', PKG, '--work', str(SCRATCH),
        '--challenge', nonce, '--nonce-commitment', commitment,
        '--child-env-log', str(SCRATCH / 'env.jsonl'), '--json-out', str(OUT / 'c1-route.json')], env)
    summary = {'axes': ['coverage/runtime environment', 'run-bound provenance', 'read-only isolation'],
               'route_rc': route.returncode, 'canary_exported': env['KAIDOKU_ENV_CANARY']}
    if not (OUT / 'c1-route.json').exists():
        save('independent-results.json', summary)
        raise RuntimeError('Route produced no receipt; inspect route.stderr')
    receipt = json.loads((OUT / 'c1-route.json').read_text())
    shutil.copyfile(SCRATCH / 'env.jsonl', OUT / 'env.jsonl')
    records = [json.loads(line) for line in (OUT / 'env.jsonl').read_text().splitlines() if line.strip()]
    run_root = Path(receipt['run_root'])
    children = collections.Counter(Path(r['argv'][0]).name for r in records)
    keys_ok = bool(records) and all(set(r['env']) == {'HOME', 'LANG', 'PATH', 'TMPDIR'} for r in records)
    paths_ok = bool(records) and all(Path(r['env'][k]).is_relative_to(run_root) and Path(r['env'][k]) != run_root
        for r in records for k in ['HOME', 'TMPDIR'])
    canary_absent = all('KAIDOKU_ENV_CANARY' not in r['env'] for r in records)
    packer = Path(receipt['packer']['path']).name if 'packer' in receipt and 'path' in receipt['packer'] else 'upx'
    required_present = all(any(name == wanted or (wanted == 'upx' and name.startswith('upx')) for name in children)
                           for wanted in ['upx', 'node', 'readelf'])
    binding_payload = nonce + ':' + receipt['instrument']['sha256'] + ':' + ','.join(sorted(c['packed_sha256'] for c in receipt['carriers']))
    binding_ok = receipt['run_binding'] == hashlib.sha256(binding_payload.encode()).hexdigest()
    summary.update({'met_target': receipt.get('met_target'), 'carriers_matched': receipt.get('carriers_matched'),
        'target': receipt.get('target'), 'records': len(records), 'children': dict(children),
        'exact_keys': keys_ok, 'home_tmp_descendants': paths_ok, 'canary_absent': canary_absent,
        'required_children_present': required_present, 'independent_binding_matches': binding_ok,
        'run_root_is_scratch_descendant': run_root.is_relative_to(SCRATCH),
        'nonce_hash_matches': hashlib.sha256(receipt['run_nonce'].encode()).hexdigest() == commitment})
    altered = {}
    altered['transplanted'] = json.loads((ROOT / '.ufo/waves/round-70/l1/scores/c3-at-landing.json').read_text())
    altered['wrong-nonce'] = copy.deepcopy(receipt)
    altered['wrong-nonce']['run_nonce'] = ('0' if nonce[0] != '0' else '1') + nonce[1:]
    altered['broken-binding'] = copy.deepcopy(receipt)
    altered['broken-binding']['run_binding'] = '0' * 64
    checks = {}
    for name in ['genuine', 'transplanted', 'wrong-nonce', 'broken-binding']:
        path = OUT / 'c1-route.json' if name == 'genuine' else OUT / (name + '.json')
        if name != 'genuine':
            save(path.name, altered[name])
        result = invoke('check-' + name, prefix + ['--check-receipt', str(path), '--nonce-commitment', commitment])
        clause = {'genuine': None, 'transplanted': 'run_nonce absent', 'wrong-nonce': 'run_nonce hash', 'broken-binding': 'run_binding'}[name]
        checks[name] = {'rc': result.returncode, 'expected_rc': 0 if name == 'genuine' else 1,
                        'clause': clause, 'clause_found': clause is None or clause in result.stdout + result.stderr}
    summary['checks'] = checks
    summary['met'] = (route.returncode == 0 and receipt.get('met_target') is True
        and receipt.get('carriers_matched') == receipt.get('target') == 4
        and all([keys_ok, paths_ok, canary_absent, required_present, binding_ok, summary['nonce_hash_matches']])
        and all(c['rc'] == c['expected_rc'] and c['clause_found'] for c in checks.values()))
    save('independent-results.json', summary)
    print(json.dumps(summary, indent=2))
finally:
    shutil.rmtree(SCRATCH)
