import json, hashlib, subprocess, os
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE='49096c7e6f226af0c750c4b003be58883cb6049f'; TIP='7a24ff74736e84b1903db7ba01891c406a6e32a2'
S='/fast/scratch/hyaku/kaidoku-r41/R41W2C1Chain'
paths=[l.split('\t',1)[1] for l in subprocess.run(['git','-C',LANE,'diff','--name-status','--diff-filter=A','--format=',f'{BASE}..{TIP}'],capture_output=True,check=True).stdout.decode().splitlines() if l.strip()]
q=''.join(f'{TIP}:{p}\n' for p in paths).encode()
res=subprocess.run(['git','-C',LANE,'cat-file','--batch'],input=q,capture_output=True,check=True).stdout
blobs=[]; i=0
while i<len(res):
    nl=res.index(b'\n',i); parts=res[i:nl].decode().split()
    if len(parts)==2: i=nl+1; continue
    size=int(parts[2]); body=res[nl+1:nl+1+size]
    if len(parts)==3: pass
    blobs.append((paths[len(blobs)], body)); i=nl+1+size+1
print('blobs', len(blobs))
carriers={os.path.basename(f): open(f,'rb').read() for f in os.popen(f'ls {S}/cache/*.bin').read().split()}
print('carriers', {k:len(v) for k,v in carriers.items()})
hits=[]; tested=0
for p, body in blobs:
    if len(body) < 32: continue
    for name, c in carriers.items():
        tested += 1
        pos = c.find(body)
        if pos != -1:
            hits.append((p, len(body), name, pos))
print('substring tests', tested)
print('HITS (committed blob found verbatim inside a vendor carrier):')
for h in hits: print('  ', h)
