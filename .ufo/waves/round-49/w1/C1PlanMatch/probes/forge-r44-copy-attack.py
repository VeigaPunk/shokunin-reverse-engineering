# C1PlanMatch attack: copy the committed ROUND-44 REA receipts of the four carriers, rewrite
# parameters.output_directory into a /kaidoku-r49/ scratch string, re-mint the evidence id with
# the frozen xpin rule, plant the C1 landing blocks (the POS fixture's own docs), and score with
# the frozen counter in a scratch sandbox. Scratch only; the lane is never written.
import importlib.util, json, os, subprocess, sys
os.chdir("/fast/scratch/hyaku/kaidoku-r49/C1PlanMatch/clone")
CL = '/fast/scratch/hyaku/kaidoku-r49/C1PlanMatch/clone'
TOOLS = CL + '/tools/round-49/'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
W = '/fast/scratch/hyaku/kaidoku-r49/C1PlanMatch/forge'
DOCS = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/artifacts'
os.environ['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'
def load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod); return mod
cc = load('c1controls', TOOLS + 'c1-controls.py')
cn = load('c1counter', TOOLS + 'c1-counter.py')
freeze = subprocess.run(['git', '-C', CL, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
sb = os.path.join(W, 'sb')
if os.path.isdir(sb):
    subprocess.run(['rm', '-rf', sb], check=True)
subprocess.run(['git', 'clone', '-q', '--shared', CL, sb], check=True)
assert subprocess.run(['git', '-C', sb, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip() == sb
for k, v in (('user.name', 'r49-c1planmatch'), ('user.email', 'c1planmatch@r49.invalid')):
    subprocess.run(['git', '-C', sb, 'config', k, v], check=True)
carriers = json.loads(subprocess.run(['git', '-C', CL, 'show', freeze + ':tools/round-49/carriers.json'], capture_output=True).stdout)
ids = [c['id'] for c in carriers['carriers']]
envs, sources = {}, {}
for cid in ids:
    raw = subprocess.run(['git', '-C', CL, 'show', 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9:corpus/evidence/round-44/c1/%s/after.json' % cid], capture_output=True).stdout
    env = json.loads(raw)
    env['parameters']['output_directory'] = '/fast/scratch/hyaku/kaidoku-r49/forge-r44/%s/extract' % cid
    envs[cid] = env
    sources[cid] = 'round-44 after.json (sha256 %s)' % cid
work = os.path.join(W, 'mint'); os.makedirs(work, exist_ok=True)
minted = cc.mint_evidence_ids(work, PKG, envs)
files = {}
for cid, env in envs.items():
    env['evidence_id'] = minted[cid]
    files['corpus/evidence/round-49/c1/%s/after.json' % cid] = (json.dumps(env, indent=1, sort_keys=True) + '\n').encode()
ctx = {'root': sb, 'freeze': freeze, 'work': work, 'pkg65': PKG, 'carriers': {'scored': carriers and [dict(c) for c in carriers['carriers']], 'target': 4}, 'doc_dir': DOCS}
doc_tree, _sizes = cc._doc_landing(ctx)
files.update(doc_tree)
ctr = cc.plant_and_commit(sb, files, 'ATTACK: round-44 receipts, output_directory rewritten to /kaidoku-r49/, re-minted, C1 landing planted')
print('freeze', freeze, 'rev', ctr)
print('minted', minted)
out = os.path.join(W, 'counter.json')
res = cc.run_counter(TOOLS + 'c1-counter.py', sb, ctr, freeze, PKG, os.path.join(W, 'cwork'), out)
os.makedirs(os.path.join(W, 'cwork'), exist_ok=True)
print('exit', res['exit_code'], 'stdout_sha256', res['stdout_sha256'])
d = res['receipt'] or {}
print('carriers_matched', d.get('carriers_matched'), 'met_target', d.get('met_target'))
print('bindings_false', d.get('bindings_false'))
print('failing', d.get('failing'))
for cid, v in (d.get('carriers') or {}).items():
    print(cid, {k: v.get(k) for k in ('run_provenance_ok', 'projection_ok', 'evidence_id_ok', 'handler_ok', 'subject_pin_ok', 'gaps_ok', 'oracle_hits_ok', 'receipt_fresh', 'matched')})
