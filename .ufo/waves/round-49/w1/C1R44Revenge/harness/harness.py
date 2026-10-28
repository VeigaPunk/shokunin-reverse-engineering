import importlib.util, json, os, subprocess, copy, sys
C='/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge/clone'
S='/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge'
F='5a71eaf0d23c6f2d43fa8262bda526ab157490c0'
PKG='/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
IDS=['v1le','v1be','v2le','v2be']
spec=importlib.util.spec_from_file_location('c1c', C+'/tools/round-49/c1-counter.py')
M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
M.WORK_OVERRIDE=S+'/w/h'; os.makedirs(M.WORK_OVERRIDE, exist_ok=True)
def sh(*a, cwd=C):
    return subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
def git(*a):
    r=sh('git','-C',C,*a); 
    if r.returncode: raise SystemExit('git fail %r %s'%(a,r.stderr))
    return r.stdout.strip()
def orig(i): return json.load(open(f'{LANE}/corpus/evidence/round-44/c1/{i}/after.json'))
ORIG={i:orig(i) for i in IDS}
def inj(envs):
    def rr(raw, k, params=None):
        return 'ok', copy.deepcopy(envs[k.split('/')[0]])
    return rr
def summ(res):
    return {'rev':res['revision'][:12],'carriers_matched':res['carriers_matched'],'met_target':res['met_target'],
            'frozen_path_changed':res['frozen_path_changed'],'bindings_false':[k for k,v in res['bindings'].items() if v is False],
            'per_carrier_false':{k:[c for c in IDS if res['carriers'][c].get(c2) is False] for k in [0] for c2 in M.CLAUSES if any(res['carriers'][c].get(c2) is False for c in IDS)}}
out={}
# --- sanity: re-mint must reproduce stored id on untouched original
ids_orig=M.evidence_ids(C, F, PKG, {f'{i}/after':ORIG[i] for i in IDS}, S+'/w')
out['orig_id_check']={i:(ids_orig[f'{i}/after'][0]==ids_orig[f'{i}/after'][1]) for i in IDS}
# --- E1: relabel + re-mint
relab={}
for i in IDS:
    e=copy.deepcopy(ORIG[i]); e['parameters']['output_directory']=f'/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge/relabel/{i}/rea-out'
    relab[i]=e
ids=M.evidence_ids(C, F, PKG, {f'{i}/after':relab[i] for i in IDS}, S+'/w')
for i in IDS:
    stored,recomp=ids[f'{i}/after']; relab[i]['evidence_id']=recomp
out['E1_reminted_ids']={i:relab[i]['evidence_id'][:20] for i in IDS}
for i in IDS: json.dump(relab[i],open(f'{C}/corpus/evidence/round-49/c1/{i}/after.json','w'),indent=2)
git('checkout','-q','relabelE1')
for i in IDS: json.dump(relab[i],open(f'{C}/corpus/evidence/round-49/c1/{i}/after.json','w'),indent=2)
git('add','corpus/evidence/round-49'); git('commit','-q','--amend','-m','E1 relabel + re-minted evidence id')
rev_e1=git('rev-parse','HEAD')
out['E1_rev']=rev_e1
r=M.measure(C, rev_e1, F, PKG, rerun=inj(ORIG), target=4)
out['E1_injected']=summ(r)
out['E1_injected_carrier_detail']={i:{k:r['carriers'][i].get(k) for k in ('run_provenance_ok','evidence_id_ok','projection_ok','gaps_ok','oracle_hits_ok','subject_pin_ok','handler_ok','layout_ok','receipt_fresh','evidence_envelope_ok','matched','output_directory')} for i in IDS}
# --- E2: plain copy (plan's own CTL-C1-4 shape) 
rev_e2=git('rev-parse','plainE2')
r=M.measure(C, rev_e2, F, PKG, rerun=inj(ORIG), target=4)
out['E2_plain_copy_injected']=summ(r)
json.dump(out,open(S+'/results.partial.json','w'),indent=1,sort_keys=True)
print(json.dumps(out,indent=1,sort_keys=True))
