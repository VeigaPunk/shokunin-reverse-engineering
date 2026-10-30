import hashlib, importlib.util, io, os, shutil, tarfile, datetime, json, subprocess, sys, traceback
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SRC=os.path.join(LANE,'tools/round-50/fetch-vendor.py')
WORK='/fast/scratch/hyaku/kaidoku-r52/w1-CritFetchChain/ev/work'
def sha(b): return hashlib.sha256(b.encode() if isinstance(b,str) else b).hexdigest()
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def tar_of(name,payload):
    bio=io.BytesIO()
    with tarfile.open(fileobj=bio,mode='w') as tf:
        ti=tarfile.TarInfo(name); ti.size=len(payload); tf.addfile(ti, io.BytesIO(payload))
    return bio.getvalue()
res=[]
def rec(name,cmd,rc,out,note=''):
    res.append({'probe':name,'command':cmd,'exit_code':rc,'stdout_sha256':sha(out),
                'stdout_bytes':len(out),'utc':datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00','Z'),'note':note})
    print('=== %s rc=%s'%(name,rc)); print(out); print()

CAR=b'CARRIERBYTES-1234'; IMG=tar_of('./var/tmp/filesystem.image',CAR)
# P3 FIXED: wrong image_sha256 -> tar_member must NOT be called
fv=load(SRC,'fv')
calls=[]; orig=fv.tar_member
fv.tar_member=lambda im,m:(calls.append(m),orig(im,m))[1]
SPEC_BAD={'carriers':[{'id':'A','sha256':sha(CAR),'external':{
  'url':'https://download.avm.de/a.image','image_sha256':'0'*64,
  'member':'./var/tmp/filesystem.image','member_sha256':sha(CAR),'length':len(CAR)}}]}
C=os.path.join(WORK,'p3'); shutil.rmtree(C,ignore_errors=True)
recs,rc=fv.run(SPEC_BAD,C,None,lambda u,ic,w:(IMG,'fake'))
rec('P3 image-sha mismatch fails closed BEFORE member extraction',
  'in-process: fv.run(spec with image_sha256=0*64, fake fetcher returning a valid tar)', rc,
  'rc=%d link=%s tar_member_calls=%d\n=> 0 calls: the image hash is verified before the member is read'
  %(rc,recs[0].get('link'),len(calls)),
  'AVM re-publishing a changed image lands here: link=image_sha256, exit 1, nothing written')
# P7 FIXED: a body that IS the pinned image but is not a readable tar -> uncaught abort
fv2=load(SRC,'fv')
SPEC_NOTAR={'carriers':[{'id':'A','sha256':sha(CAR),'external':{
  'url':'https://download.avm.de/a.image','image_sha256':sha(b'NOTATAR'),
  'member':'./var/tmp/filesystem.image','member_sha256':sha(CAR),'length':len(CAR)}}]}
C7=os.path.join(WORK,'p7'); shutil.rmtree(C7,ignore_errors=True)
try:
    recs,rc=fv2.run(SPEC_NOTAR,C7,None,lambda u,ic,w:(b'NOTATAR','fake'))
    rec('P7 an unreadable container aborts the whole run (no per-carrier link, no receipt)',
      'in-process: fv.run(spec whose pinned image is not a tar)', rc,
      'rc=%d link=%s'%(rc,recs[0].get('link')))
except Exception as e:
    rec('P7 an unreadable container aborts the whole run (no per-carrier link, no receipt)',
      'in-process: fv.run(spec whose pinned image is not a tar)', 1,
      'UNCAUGHT %s: %s\n%s'%(type(e).__name__,e,traceback.format_exc(limit=2).strip().split('\n')[-1]),
      'tarfile.ReadError escapes run(): remaining carriers never attempted, no link= recorded, no --json-out')
# P11: multi-carrier run where the FIRST carrier is fine and the SECOND is a non-tar -> first carrier's cache file survives, no receipt
CAR2=b'SECOND-CARRIER-BYTES'
IMG2=tar_of('./var/tmp/filesystem.image',CAR2)
SPEC4={'carriers':[
  {'id':'A','sha256':sha(CAR),'external':{'url':'https://download.avm.de/a.image','image_sha256':sha(IMG),
     'member':'./var/tmp/filesystem.image','member_sha256':sha(CAR),'length':len(CAR)}},
  {'id':'B','sha256':sha(CAR2),'external':{'url':'https://download.avm.de/b.image','image_sha256':sha(b'NOTATAR'),
     'member':'./var/tmp/filesystem.image','member_sha256':sha(CAR2),'length':len(CAR2)}}]}
fv3=load(SRC,'fv')
C8=os.path.join(WORK,'p11'); shutil.rmtree(C8,ignore_errors=True)
try:
    recs,rc=fv3.run(SPEC4,C8,None,lambda u,ic,w:(IMG if 'a.image' in u else b'NOTATAR','fake'))
    out='rc=%d recs=%d'%(rc,len(recs))
except Exception as e:
    files=sorted(os.listdir(C8)) if os.path.isdir(C8) else []
    out=('UNCAUGHT %s: %s\ncache_dir_after=%s\nA_written=%s (a partial cache the counter would read)'
         %(type(e).__name__,e,files,sha(CAR)+'.bin' in files))
rec('P11 one unreadable carrier aborts the run and leaves a PARTIAL cache dir',
  'in-process: fv.run(spec with 2 carriers, the 2nd pinned to a non-tar image)', 1, out,
  'the counter would find carrier A present and score it; no receipt explains the abort')
json.dump(res, open(os.path.join(WORK,'results2.json'),'w'), indent=1)
print('PROBES=%d'%len(res))
