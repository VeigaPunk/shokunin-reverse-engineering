import importlib.util, json, os, subprocess, sys
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
GEN=os.path.join(LANE,'tools/round-40/heldout-gen-v2.py'); WRITER=os.path.join(LANE,'tools/round-39/gen-squashfs.py')
OUT=os.path.abspath('probe3'); os.makedirs(OUT,exist_ok=True)
spec=importlib.util.spec_from_file_location('h',GEN); h=importlib.util.module_from_spec(spec); sys.modules['h']=h; spec.loader.exec_module(h)
h.WRITER_PATH=WRITER; w=h.load_writer(WRITER); h.install_block_encoder(w)
root=os.path.join(OUT,'tree'); os.makedirs(root,exist_ok=False)
open(os.path.join(root,'only.bin'),'wb').write(b'X'*4096)
img=os.path.join(OUT,'flat.sqsh'); w.build_image(root,img,'le','gzip')
res={'carrier_sha256':h.sha256_file(img),'runs':[]}
def feats(d):
    nr=d.get('normalized_result') or {}
    return {'handlers':sorted({c.get('handler') for c in (nr.get('chunks') or []) if c.get('handler')}),
            'gaps':sorted({g.get('kind') for g in (nr.get('extraction_gaps') or [])}),
            'P':len(nr.get('files') or []),'dl':nr.get('depth_limited_paths') or [],
            'max_depth':(d.get('parameters') or {}).get('max_depth'),
            'unpub':len(nr.get('unpublished_entries') or [])}
for depth in (1,2,3):
    work=os.path.join(OUT,'w%d'%depth); os.makedirs(work,exist_ok=True)
    out=os.path.join(work,'out')
    env=h.rea_env('after')
    cmd=['npx','-y',h.REA_PACKAGE,'extract-firmware','--format','json','--full-output','--max-depth',str(depth),img,out]
    p=subprocess.run(cmd,cwd=work,env=env,capture_output=True,text=True)
    full=h._parse_stdout(p.stdout); d=(full or {}).get('data')
    res['runs'].append({'depth':depth,'exit':p.returncode,'ok':(full or {}).get('ok'),'features':feats(d) if d else None})
json.dump(res,open(os.path.join(OUT,'report3.json'),'w'),indent=1)
print(json.dumps(res,indent=1))
