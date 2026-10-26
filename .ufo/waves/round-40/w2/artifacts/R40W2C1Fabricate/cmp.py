import importlib.util, json, subprocess, sys
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', L+'/tools/round-40/c1-counter.py')
c1=importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
REV='42c10a58cb2cae3a4a0122af35a0cf95ac718043'
def committed(cid):
    raw=subprocess.run(['git','-C',L,'show',f'{REV}:corpus/evidence/round-40/c1/{cid}/after.json'],capture_output=True,check=True).stdout
    return json.loads(raw)
for cid,fab in [('L1','L1'),('V1','V1'),('V2','V2'),('L2','L2')]:
    a=c1.projection(committed(cid),'plus-extractor')
    b=c1.projection(json.load(open('fab/%s.json'%fab))['data'],'plus-extractor')
    eq,keys,detail=c1.projection_diff(a,b,'plus-extractor')
    print(f'== {cid}: fab projection == committed projection: {eq}  differing keys={keys}')
    for k in c1.PROJECTION_KEYS_BY_PROFILE['plus-extractor']:
        print(f'   {k}: committed_len={len(a[k]) if isinstance(a[k],list) else a[k]!r} fab_len={len(b[k]) if isinstance(b[k],list) else b[k]!r} equal={a[k]==b[k]}')
    if not eq:
        print('   DETAIL', json.dumps(detail, indent=1)[:1500])
# per-file-hash variant vs committed L1
a=c1.projection(committed('L1'),'plus-extractor')
b=c1.projection(json.load(open('fab/L1-perfilehash.json'))['data'],'plus-extractor')
eq,keys,detail=c1.projection_diff(a,b,'plus-extractor')
print('== L1 per-file-HashReport variant: equal=%s keys=%s'%(eq,keys))
print('   sample committed files row', a['files'][0])
print('   sample variant   files row', b['files'][0])
