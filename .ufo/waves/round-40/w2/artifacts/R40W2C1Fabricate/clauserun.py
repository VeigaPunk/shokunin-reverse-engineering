import copy,json,subprocess,sys,os
S='/fast/scratch/hyaku/kaidoku-r40/R40W2C1Fabricate'
D=open(S+'/dpath.txt').read().strip().split('=',1)[1]
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PKG='/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
base=json.load(open(S+'/fab/L1.env.json'))
CLAUSES=('carrier_present','carrier_pin_ok','layout_ok','oracle_ok','nonregular_ok','receipt_present','receipt_fresh','subject_pin_ok','operation_ok','handler_ok','chunks_ok','oracle_hits_ok','gaps_ok','nonregular_unpublished_ok','run_provenance_ok','evidence_id_ok','projection_ok')
def mint(e):
    import json as J, tempfile, os
    w=tempfile.mktemp(dir='/fast/scratch/hyaku/kaidoku-r40/R40W2C1Fabricate',suffix='.mint.json')
    J.dump({'data':e},open(w,'w'))
    r=subprocess.run(['node',L+'/tools/round-27/xpin-attribute.mjs','--pkg65',PKG,'--pkg67',PKG,w],capture_output=True,text=True)
    if r.returncode!=0: raise SystemExit('mint failed: '+r.stderr)
    line=r.stdout.strip().split('\t'); os.unlink(w); return line[2]
def run(name,fn,remint=True):
    e=copy.deepcopy(base); fn(e)
    if remint: e['evidence_id']=mint(e)
    p=D+'/lane/corpus/evidence/round-40/c1/L1/after.json'
    json.dump(e,open(p,'w'))
    subprocess.run(['git','-C',D+'/lane','-c','user.name=fx','-c','user.email=fx@fx','commit','-q','-am','mutant: '+name],check=True)
    rev=subprocess.run(['git','-C',D+'/lane','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
    out=S+'/score-%s.json'%name.replace(' ','_').replace('/','_')[:60]
    r=subprocess.run(['python3','-I','-B',L+'/tools/round-40/c1-counter.py','--root',D+'/lane','--rev',rev,'--freeze','7fce308631a8b457d6b7c5a4b39a923c4e9a49de','--pkg65',PKG,'--carrier-cache',S+'/cache','--json-out',out],capture_output=True,text=True)
    d=json.load(open(out))
    if 'carriers' not in d:
        print(name,'-> UNEVALUABLE',d.get('unevaluable') or d.get('reason')); return
    c=d['carriers']['L1']
    print('%-52s exit=%s L1.matched=%s failing=%s proj_diff=%s'%(name[:52],d['exit_code'],c['matched'], [k for k in CLAUSES if c.get(k) is not True], c.get('projection_diff')))
run('coverage_complete', lambda e: e['normalized_result'].__setitem__('coverage','complete'))
run('truthful_mime_types', lambda e: [f.__setitem__('mime_type','text/x-shellscript') for f in e['normalized_result']['files']])
run('tables_only_no_gaps', lambda e: (e['normalized_result'].__setitem__('extraction_gaps',[]), e['normalized_result'].__setitem__('unpublished_entries',[])))
run('stale_evidence_id', lambda e: e.__setitem__('evidence_id','ev_525ea7198f21dff26cceb2275263ed8899b2fb697888619bb6c5549480231c40'))
run('unminted_evidence_id', lambda e: e.__setitem__('evidence_id','ev_' + '0'*64), remint=False)
run('raw_result_fiction', lambda e: (e['raw_result'].__setitem__('execution',{'command':'/usr/bin/true','args':['--never-ran-unblob'],'exit_code':0}), e.__setitem__('limitations',['no extractor was executed']) , e.__setitem__('authority','derived-from-oracle')))
