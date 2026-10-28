import json,os,subprocess,hashlib,sys,shutil
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S=os.environ['S']
d=json.load(open(L+'/.ufo/waves/round-49/draft/tools/round-49/carriers.json'))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def walk(root):
    out=[]
    for dp,dn,fn in os.walk(root):
        for n in dn+fn:
            p=os.path.join(dp,n); rel=os.path.relpath(p,root)
            if os.path.islink(p): out.append((rel,'symlink',None,None))
            elif os.path.isdir(p): out.append((rel,'dir',None,None))
            else: out.append((rel,'regular',os.path.getsize(p),sha(p)))
    return sorted(out)
def run(argv):
    r=subprocess.run(argv,capture_output=True)
    return r.returncode,hashlib.sha256(r.stdout).hexdigest(),r.stdout.decode(errors='replace')[-300:],r.stderr.decode(errors='replace')[-400:]
def dig(ms): return hashlib.sha256(''.join(f'{p}\t{h}\n' for p,_,_,h in sorted(ms) if _ is not None).encode()).hexdigest()
res={}
for c in d['carriers']:
    cid=c['id']; img=L+'/'+c['path']
    r={'img_sha_ok':sha(img)==c['sha256'],'size_ok':os.path.getsize(img)==c['size']}
    ud=f'{S}/un/{cid}'; os.makedirs(S+'/un',exist_ok=True); shutil.rmtree(ud,ignore_errors=True)
    r['unsq']=run(['/usr/bin/unsquashfs','-d',ud,img])[:2]
    r['unsq_lls']=run(['/usr/bin/unsquashfs','-lls',img])[:3]
    un=[x for x in walk(ud) if x[1]=='regular']
    r['unsq_members']=un
    sd=f'{S}/7z/{cid}'; shutil.rmtree(sd,ignore_errors=True); os.makedirs(sd)
    rc7=run(['/usr/bin/7z','x','-y','-o'+sd,img]); r['7z']=rc7
    r['7z_t']=run(['/usr/bin/7z','x','-y','-tSquashFS','-o'+sd+'t',img])[:2]
    sz=[x for x in walk(sd) if x[1]=='regular']
    r['7z_members']=sz
    r['7z_all']=walk(sd)
    # oracle
    ocm=[(m['path'],'regular',m['size'],m['sha256']) for m in c['oracle']['members']]
    r['oracle_members_eq_unsq']= sorted(ocm)==sorted(un)
    r['oracle_digest_stored']=c['oracle']['output_tree_digest']
    r['digest_recomputed_unsq']=dig(un)
    r['digest_recomputed_7z']=dig(sz)
    cen=[x for x in c['oracle']['census'] if x['type']=='regular']
    r['census_regular_eq']=sorted((x['rel'],x['size']) for x in cen)==sorted((p,s) for p,_,s,_ in un)
    r['census_nonreg']=[(x['rel'],x['type']) for x in c['oracle']['census'] if x['type']!='regular']
    # unblob tree
    ot=L+'/'+c['output_tree']
    ub=walk(ot); r['unblob_all']=ub
    ubr=[x for x in ub if x[1]=='regular']
    r['unblob_eq_unsq']=ubr==un
    r['unblob_eq_7z']=ubr==sz
    r['7z_eq_unsq']=sz==un
    res[cid]=r
json.dump(res,open(S+'/ind.json','w'),indent=1,default=list)
for k,r in res.items():
    print(k,{a:b for a,b in r.items() if a not in('unsq_members','7z_members','7z_all','unblob_all')})
    print(' unsq',r['unsq_members']); print(' 7z_all',r['7z_all']); print(' unblob_all',r['unblob_all'])
