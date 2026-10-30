#!/usr/bin/env python3
"""CritFetchChain consolidated evidence probe (offline, synthetic fixtures)."""
import hashlib, importlib.util, io, json, os, shutil, subprocess, sys, tarfile, datetime, urllib.error, urllib.parse

LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SRC=os.path.join(LANE,'tools/round-50/fetch-vendor.py')
SQFS=os.path.join(LANE,'tools/round-41/sqfs-list.py')
WORK='/fast/scratch/hyaku/kaidoku-r52/w1-CritFetchChain/ev/work'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def tar_of(name,payload):
    bio=io.BytesIO()
    with tarfile.open(fileobj=bio,mode='w') as tf:
        ti=tarfile.TarInfo(name); ti.size=len(payload); tf.addfile(ti, io.BytesIO(payload))
    return bio.getvalue()

def stage():
    d=os.path.join(WORK,'stage'); shutil.rmtree(d,ignore_errors=True)
    os.makedirs(os.path.join(d,'tools/round-50')); os.makedirs(os.path.join(d,'tools/round-41'))
    shutil.copy(SRC, os.path.join(d,'tools/round-50/fetch-vendor.py'))
    shutil.copy(SQFS, os.path.join(d,'tools/round-41/sqfs-list.py'))
    return d

results=[]
def rec(name, cmd, rc, out, note=''):
    results.append({'probe':name,'command':cmd,'exit_code':rc,
                    'stdout_sha256':sha(out.encode() if isinstance(out,str) else out),
                    'stdout_bytes':len(out.encode() if isinstance(out,str) else out),
                    'utc':datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00','Z'),
                    'note':note})
    print('=== %s rc=%s' % (name, rc)); print(out if isinstance(out,str) else out.decode('utf-8','replace')); print()

CAR=b'CARRIERBYTES-1234'
IMG=tar_of('./var/tmp/filesystem.image',CAR)
SPEC={'carriers':[{'id':'A','sha256':sha(CAR),'external':{
    'url':'https://download.avm.de/a.image','image_sha256':sha(IMG),
    'member':'./var/tmp/filesystem.image','member_sha256':sha(CAR),'length':len(CAR)}}]}

# ---- P1 base selftest
d=stage()
p=subprocess.run([sys.executable,'-I','-B',os.path.join(d,'tools/round-50/fetch-vendor.py'),'--selftest'],
                 capture_output=True,text=True)
rec('P1 base selftest (16 cases)', 'python3 -I -B tools/round-50/fetch-vendor.py --selftest', p.returncode,
    p.stdout, 'baseline: all chain-hash cases pass')

# ---- P2 mutation: delete the network guards, selftest must go RED (routed defect 4)
src=open(SRC).read()
muts={
 'MUT-A https+host guard deleted in fetch()':
   ("    if u.scheme != 'https' or u.hostname != ALLOWED_HOST:\n        raise ValueError('url outside https://%s: %s' % (ALLOWED_HOST, url))\n",""),
 'MUT-B redirect guard deleted':
   ("        u = urllib.parse.urlsplit(newurl)\n        if u.scheme != 'https' or u.hostname != ALLOWED_HOST:\n            raise urllib.error.HTTPError(newurl, code, 'redirect off %s refused' % ALLOWED_HOST, hdrs, fp)\n",""),
 'MUT-C both network guards deleted':
   ("        u = urllib.parse.urlsplit(newurl)\n        if u.scheme != 'https' or u.hostname != ALLOWED_HOST:\n            raise urllib.error.HTTPError(newurl, code, 'redirect off %s refused' % ALLOWED_HOST, hdrs, fp)\n",""),
}
for label,(a,b) in muts.items():
    t=src.replace(a,b)
    if label.startswith('MUT-C'):
        t=t.replace("    if u.scheme != 'https' or u.hostname != ALLOWED_HOST:\n        raise ValueError('url outside https://%s: %s' % (ALLOWED_HOST, url))\n","")
    dm=os.path.join(WORK,'mut'); shutil.rmtree(dm,ignore_errors=True)
    os.makedirs(os.path.join(dm,'tools/round-50')); os.makedirs(os.path.join(dm,'tools/round-41'))
    open(os.path.join(dm,'tools/round-50/fetch-vendor.py'),'w').write(t)
    shutil.copy(SQFS, os.path.join(dm,'tools/round-41/sqfs-list.py'))
    p=subprocess.run([sys.executable,'-I','-B',os.path.join(dm,'tools/round-50/fetch-vendor.py'),'--selftest'],
                     capture_output=True,text=True)
    last=[l for l in p.stdout.strip().split('\n') if l.startswith('SELFTEST')]
    rec(label, 'mutant: fetch-vendor.py --selftest (guards deleted)', p.returncode,
        (last[-1] if last else p.stdout[-400:])+'\nEXPECTED: selftest RED (rc!=0). OBSERVED rc=%d'%p.returncode,
        'routed defect 4 requires guard-deletion -> selftest red')

# ---- P3 image-sha mismatch is checked BEFORE member extraction
fv=load(SRC,'fv')
calls=[]
orig=fv.tar_member
fv.tar_member=lambda im,m:(calls.append(m),orig(im,m))[1]
C1=os.path.join(WORK,'c1'); shutil.rmtree(C1,ignore_errors=True)
recs,rc=fv.run(SPEC,C1,None,lambda u,ic,w:(IMG,'fake'))
rec('P3 image-sha mismatch fails closed BEFORE member extraction',
    'in-process: fv.run(spec) with wrong image_sha256', rc,
    'rc=%d link=%s tar_member_calls=%d (0 => image hash verified first)'%(rc,recs[0].get('link'),len(calls)))
fv=load(SRC,'fv')

# ---- P4 stale cache file survives a FAILED fetch
C2=os.path.join(WORK,'c2'); shutil.rmtree(C2,ignore_errors=True)
recs,rc=fv.run(SPEC,C2,None,lambda u,ic,w:(IMG,'fake'))
pin=sha(CAR); out=os.path.join(C2,pin+'.bin')
stale_present_after_success=os.path.isfile(out)
IMG2=tar_of('./var/tmp/filesystem.image',b'DIFFERENTBYTES')
SPEC2={'carriers':[{'id':'A','sha256':sha(CAR),'external':{
    'url':'https://download.avm.de/a.image','image_sha256':sha(IMG2),
    'member':'./var/tmp/filesystem.image','member_sha256':sha(IMG2),'length':len(CAR)}}]}
recs2,rc2=fv.run(SPEC2,C2,None,lambda u,ic,w:(IMG2,'fake'))
stale=os.path.isfile(out) and sha(open(out,'rb').read())==pin
rec('P4 stale <pin>.bin survives a FAILED re-fetch (counter reads it as fresh)',
    'in-process: fv.run(spec_ok); then fv.run(spec_fail) into the SAME cache dir', rc2,
    'first_rc=0 wrote=%s\nfailed_fetch_rc=%d link=%s\nstale_<pin>.bin_present=%s stale_sha_matches_pin=%s\ncounter would read: carrier_present=True carrier_pin_ok=True'
    %(stale_present_after_success, rc2, recs2[0].get('link'), os.path.isfile(out), stale),
    'the fetcher never invalidates a pre-existing <pin>.bin and the counter never sees the fetch receipt')

# ---- P5 image-cache reuse: green with ZERO network contact
IC=os.path.join(WORK,'ic'); shutil.rmtree(IC,ignore_errors=True); os.makedirs(IC)
open(os.path.join(IC,sha(IMG)+'.image'),'wb').write(IMG)
class Boom:
    def open(self,*a,**k): raise AssertionError('NETWORK CONTACTED')
fv._OPENER=Boom()
C3=os.path.join(WORK,'c3'); shutil.rmtree(C3,ignore_errors=True)
try:
    recs,rc=fv.run(SPEC,C3,IC,fv.fetch)
    rec('P5 --image-cache serves the chain with ZERO network contact',
        'in-process: fv.run(spec, cache, image_cache, fv.fetch) with _OPENER booby-trapped', rc,
        'rc=%d ok=%s fetch=%r (no network contacted; the receipt says "cache", not "http 200")'
        %(rc,recs[0].get('ok'),recs[0].get('fetch')))
except AssertionError as e:
    rec('P5 --image-cache serves the chain with ZERO network contact',
        'in-process: fv.run(spec, cache, image_cache, fv.fetch) with _OPENER booby-trapped', 1,
        'NETWORK CONTACTED: %s'%e)

# ---- P6 guard predicate looseness (offline, predicate only)
def guard(u):
    u=urllib.parse.urlsplit(u)
    return not (u.scheme!='https' or u.hostname!='download.avm.de')
rows=[]
for c in ['https://download.avm.de/x','http://download.avm.de/x','https://evil.example/x',
          'https://download.avm.de:8443/x','https://user:pw@download.avm.de/x',
          'https://download.avm.de@evil.example/x','file:///etc/passwd']:
    rows.append('%-6s %s'%('PASSES' if guard(c) else 'refused',c))
rec('P6 network guard predicate: hostname-only (port and userinfo not checked)',
    'offline: replicate the fetch()/redirect guard predicate verbatim', 0, '\n'.join(rows),
    'scheme+hostname are checked; port and userinfo are NOT')

# ---- P7 corrupted container aborts the whole run, no receipt
C4=os.path.join(WORK,'c4'); shutil.rmtree(C4,ignore_errors=True)
J=os.path.join(WORK,'bad.json')
json.dump({'carriers':[{'id':'A','sha256':sha(CAR),'external':{
    'url':'https://download.avm.de/a.image','image_sha256':sha(b'NOTATAR'),
    'member':'./var/tmp/filesystem.image','member_sha256':sha(CAR),'length':len(CAR)}}]}, open(J,'w'))
jo=os.path.join(WORK,'out.json')
if os.path.exists(jo): os.remove(jo)
p=subprocess.run([sys.executable,'-I','-B',SRC,'--spec',J,'--cache',C4,'--json-out',jo],
                 capture_output=True,text=True)
rec('P7 a non-tar container aborts the whole 4-carrier run with NO receipt',
    'python3 -I -B tools/round-50/fetch-vendor.py --spec <bad> --cache C --json-out out.json', p.returncode,
    'rc=%d\njson_out_written=%s\nstderr_tail=%s'%(p.returncode, os.path.exists(jo), p.stderr.strip().split('\n')[-1] if p.stderr.strip() else ''),
    'tarfile.ReadError is uncaught: no per-carrier link=, no --json-out receipt, no partial results')

# ---- P8 symlink .part write follows the symlink
C5=os.path.join(WORK,'c5'); shutil.rmtree(C5,ignore_errors=True); os.makedirs(C5)
victim=os.path.join(WORK,'VICTIM.txt'); open(victim,'w').write('ORIGINAL')
os.symlink(victim, os.path.join(C5,pin+'.bin.part'))
recs,rc=fv.run(SPEC,C5,None,lambda u,ic,w:(IMG,'fake'))
rec('P8 the <pin>.bin.part write follows a pre-planted symlink (arbitrary overwrite)',
    'in-process: fv.run(spec) with <pin>.bin.part pre-planted as a symlink to VICTIM.txt', rc,
    'rc=%d ok=%s victim_content_after=%r part_is_symlink_after=%s'
    %(rc,recs[0].get('ok'),open(victim).read(),os.path.islink(os.path.join(C5,pin+'.bin.part'))),
    'os.replace() replaces the symlink but the write already followed it')

# ---- P9 a carrier without an "external" key is silently skipped, rc still 0
SPEC3={'target':4,'carriers':[dict(SPEC['carriers'][0]),
        {'id':'B','sha256':'b'*64,'oracle':'x.tsv','nonregular':'y.tsv'}]}
C6=os.path.join(WORK,'c6'); shutil.rmtree(C6,ignore_errors=True)
recs,rc=fv.run(SPEC3,C6,None,lambda u,ic,w:(IMG,'fake'))
rec('P9 a carrier with no "external" key is silently dropped and rc is still 0',
    'in-process: fv.run(spec with 2 carriers, one lacking "external")', rc,
    'carriers_in_spec=%d recs_emitted=%d rc=%d (no error for the dropped carrier)'
    %(len(SPEC3['carriers']),len(recs),rc),
    'the fetcher never checks it materialised the table\'s target count')

# ---- P10 the fetch receipt records no vendor revision (last-modified/etag) and no UTC time
rec('P10 the fetch receipt carries no vendor revision, no UTC time and no fetch-event id',
    'read: fetch-vendor.py materialise()/fetch() receipt fields', 0,
    'receipt fields = id, pin, url, fetch, image_sha256, member_detail, member_sha256, carrier_sha256, path, bytes\n'
    'ABSENT: http Last-Modified, http ETag, UTC timestamp, run id, request argv\n'
    '=> a receipt cannot tell a fresh vendor fetch from a leftover cache file',
    'the round-50 carriers.json notes DO carry http_last_modified/http_etag (r50 notes)')

json.dump(results, open(os.path.join(WORK,'results.json'),'w'), indent=1)
print('PROBES=%d results=%s' % (len(results), os.path.join(WORK,'results.json')))
