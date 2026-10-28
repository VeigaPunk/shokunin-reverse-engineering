import json,os,sys,hashlib
C=sys.argv[1]
listed=set(); 
for k in sorted(os.listdir(C)):
    mp=os.path.join(C,k,'manifest.json'); m=json.load(open(mp))
    listed.add(os.path.relpath(mp,C))
    for rel,meta in m['files'].items():
        fp=os.path.join(C,meta['fixture']); 
        raw=open(fp,'rb').read()
        ok=hashlib.sha256(raw).hexdigest()==meta['sha256'] and len(raw)==meta['size']
        listed.add(meta['fixture'])
        print(k,rel,'pin-ok' if ok else 'PIN-MISMATCH', 'dest-matches-fixture-path' if meta['fixture']==k+'/'+rel else 'PATH-DIFF')
allf=set()
for d,_,fs in os.walk(C):
    for f in fs: allf.add(os.path.relpath(os.path.join(d,f),C))
print('orphans',sorted(allf-listed)); print('listed-missing',sorted(listed-allf))
