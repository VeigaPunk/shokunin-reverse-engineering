import sys, hashlib, json, re
def load(p):
    return open(p,'rb').read()
def find_all(hay, needle):
    out=[]; i=hay.find(needle)
    while i!=-1:
        out.append(i); i=hay.find(needle, i+1)
    return out
for p in sys.argv[1:]:
    b=load(p); hx=b.hex()
    d={}
    d['path']=p; d['bytes']=len(b); d['sha256']=hashlib.sha256(b).hexdigest()
    d['off_5f3560e01c']=find_all(hx,'5f3560e01c')
    d['off_60003560e01c']=find_all(hx,'60003560e01c')
    d['off_calldatasize_guard_60043610']=find_all(hx,'60043610')
    d['head']=hx[:80]
    # extract PUSH4 constants after dispatcher start (selector compare pattern 80 63 <sel> 14)
    sels=re.findall(r'8063([0-9a-f]{8})14', hx)
    d['dispatch_sels_8063..14']=sorted(set(sels))
    print(json.dumps(d))
