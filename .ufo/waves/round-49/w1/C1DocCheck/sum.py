import json,sys,glob,os
S='/fast/scratch/hyaku/kaidoku-r49/C1DocCheck'
for w in ['w0']+sorted(os.path.basename(p) for p in glob.glob(S+'/w-*')):
    d=S+'/'+w
    try:
        c=json.load(open(d+'/ctl-out/pos/counter.json')); r=json.load(open(d+'/ctl-out/pos/receipt.json')); k=json.load(open(d+'/ctl.json'))['controls']['CTL-C1-POS']
    except Exception as e: print(w,'ERR',e); continue
    b=c['bindings']
    red=sorted(x for x,v in b.items() if isinstance(v,bool) and not v)
    print(w,'counter_exit',c['exit_code'],'matched',c['carriers_matched'],'met',c['met_target'],'red',red,'verdict',k['verdict'],'ctl_exit',k['exit_code'],'ctl_stdout',k['stdout_sha256'][:12],'counter_sha',c['counter_sha256'][:12])
