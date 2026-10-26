import collections, json, sys
def load(f, n):
    reg=[]; link=[]
    for line in open(f, encoding='utf-8', errors='surrogateescape'):
        a=line.rstrip('\n').split('\t')
        if len(a)>=2 and a[1]=='symlink': link.append(a[0])
        else: reg.append(a[0])
    return reg, link
import glob
res={}
for files, non, name in json.loads(sys.argv[1]):
    reg, _ = load(files, 'f'); _, link = load(non, 'n')
    d={'reg':len(reg),'link':len(link)}
    for k in (1,2,3):
        idx=collections.defaultdict(list)
        for lp in link: idx['/'.join(lp.split('/')[-k:])].append(lp)
        d['k%d'%k]=sum(1 for rp in reg for lp in idx.get('/'.join(rp.split('/')[-k:]),()) if lp!=rp)
    # R40-CL1 shape: regular candidate ends with '/'+link (whole link path)
    d['r40cl1_full_suffix']=sum(1 for rp in reg for lp in link if rp.endswith('/'+lp))
    d['r40cl1_rev']=sum(1 for lp in link for rp in reg if lp.endswith('/'+rp))
    res[name]=d
print(json.dumps(res, indent=1, sort_keys=True))
