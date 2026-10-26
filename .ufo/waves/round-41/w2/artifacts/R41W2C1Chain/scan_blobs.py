import json, hashlib, subprocess, sys, os, re
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE='49096c7e6f226af0c750c4b003be58883cb6049f'
TIP='7a24ff74736e84b1903db7ba01891c406a6e32a2'
def git(*a, input=None):
    return subprocess.run(['git','-C',LANE]+list(a), capture_output=True, input=input, check=True).stdout
# added paths
out = git('diff','--name-status','--diff-filter=A','--format=',f'{BASE}..{TIP}').decode()
paths=[l.split('\t',1)[1] for l in out.splitlines() if l.strip()]
print('added paths', len(paths))
# blob ids at tip
q=''.join(f'{TIP}:{p}\n' for p in paths).encode()
res=subprocess.run(['git','-C',LANE,'cat-file','--batch'], input=q, capture_output=True, check=True).stdout
i=0; recs=[]
while i < len(res):
    nl=res.index(b'\n', i)
    hdr=res[i:nl].decode()
    parts=hdr.split()
    if len(parts)==2:  # missing
        i=nl+1; continue
    sha, typ, size = parts[0], parts[1], int(parts[2])
    body=res[nl+1:nl+1+size]
    recs.append((sha, typ, size, body))
    i=nl+1+size+1
print('blobs read', len(recs), 'bytes', sum(r[2] for r in recs))
# pins
pins=set()
spec=json.load(open(os.path.join(LANE,'.ufo/waves/round-41/c1/carriers.json')))
for c in spec['carriers']:
    pins.add(c['sha256'].lower())
    e=c.get('external') or {}
    for k in ('image_sha256','member_sha256'):
        if k in e: pins.add(e[k].lower())
    if 'nested' in e: pins.add(e['nested']['sha256'].lower())
print('round-41 pins', len(pins))
# round-40 carrier pins from git if present
for revpath in ['.ufo/waves/round-40/c1/carriers.json']:
    p=subprocess.run(['git','-C',LANE,'show',f'{TIP}:{revpath}'],capture_output=True)
    if p.returncode==0:
        s=json.loads(p.stdout)
        def walk(o):
            if isinstance(o,dict):
                for k,v in o.items(): yield from walk(v)
            elif isinstance(o,list):
                for v in o: yield from walk(v)
            elif isinstance(o,str) and re.fullmatch(r'[0-9a-f]{64}',o): yield o
        n40=set(walk(s)); print('round-40 pins', len(n40)); pins|=n40
# oracle sha256 values (regular-file bodies that must not be committed)
oracle_sha=set()
for p in paths:
    if '/oracle.tsv' in p:
        txt=subprocess.run(['git','-C',LANE,'show',f'{TIP}:{p}'],capture_output=True,check=True).stdout.decode()
        for line in txt.splitlines()[:1]: pass
        for line in txt.splitlines():
            for tok in re.findall(r'[0-9a-f]{64}', line): oracle_sha.add(tok)
print('oracle sha256 tokens', len(oracle_sha), 'sample paths', [p for p in paths if 'oracle.tsv' in p][:6])
hits=[]; magic=[]
for sha,typ,size,body in recs:
    h=hashlib.sha256(body).hexdigest()
    if h in pins or h in oracle_sha: hits.append((size,h))
    head=body[:4]
    if head in (b'sqsh',b'hsqh',b'qshs',b'shsq') or head[:2]==b'\x1f\x8b' or head[:6]==b'\xfd7zXZ\x00':
        magic.append((size,h,head))
print('PIN/ORACLE HITS:', hits)
print('compressed/squashfs-magic blobs:', magic[:20], 'n=',len(magic))
big=sorted(recs,key=lambda r:-r[2])[:6]
for sha,typ,size,body in big:
    print(size, hashlib.sha256(body).hexdigest(), [p for p in paths if True][0] if False else '')
