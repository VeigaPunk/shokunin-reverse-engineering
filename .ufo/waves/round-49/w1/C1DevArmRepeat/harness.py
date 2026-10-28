import sys, os, json, time, shutil, subprocess, hashlib, importlib.util
S='/fast/scratch/hyaku/kaidoku-r49/C1DevArmRepeat'
clone=S+'/clone'
spec=importlib.util.spec_from_file_location('c1c', clone+'/tools/round-49/c1-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
pkg='/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
freeze=subprocess.check_output(['git','-C',clone,'rev-parse','HEAD']).decode().strip()
spec_c=json.loads(m.show(clone,'HEAD',m.CARRIERS))
res={}
tag=sys.argv[1]; workroot=sys.argv[2]
os.makedirs(workroot,exist_ok=True)
runner=m.make_real_runner(workroot,None,900)
envs={}; walls={}
for c in spec_c['carriers']:
    raw=m.show(clone,'HEAD',c['path'])
    t=time.time()
    st,pl=runner(raw,c['id'],{'max_depth':3})
    walls[c['id']]=round(time.time()-t,2)
    assert st=='ok',(st,pl)
    envs[c['id']+'/after']=pl
ev=m.evidence_ids(clone,freeze,pkg,envs,workroot)
out={}
for k,e in envs.items():
    cid=k.split('/')[0]
    h=[c['handler'] for c in (e.get('normalized_result') or {}).get('chunks',[])]
    pr=m.projection(e,'plus-extractor',[c for c in spec_c['carriers'] if c['id']==cid][0]['handler'])
    nr=e['normalized_result']
    out[cid]={'wall':walls[cid],'evidence_id':ev[k],'handlers':h,
      'output_directory':e['parameters'].get('output_directory'),
      'published':sorted((x.get('relative_path'),x.get('sha256'),x.get('size')) for x in nr.get('files',[])),
      'gap_kinds':sorted([g.get('kind') for g in nr.get('extraction_gaps',[])]),
      'unpublished':nr.get('unpublished_entries'),
      'projection':pr,'projection_sha':hashlib.sha256(json.dumps(pr,sort_keys=True).encode()).hexdigest(),
      'raw_keys':sorted(e.keys()),
      'raw_sha':hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest()}
    json.dump(e,open(f'{S}/h/{tag}-{cid}.env.json','w'),sort_keys=True,indent=1)
json.dump(out,open(f'{S}/h/{tag}.json','w'),sort_keys=True,indent=1)
print(tag,'ok',walls)
