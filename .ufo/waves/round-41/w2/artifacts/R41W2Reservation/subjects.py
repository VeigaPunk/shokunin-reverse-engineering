#!/usr/bin/env python3
"""Enumerate every REA-shaped envelope (any wrapper depth: dict with subject.digest.sha256) under a tree and
compare subject digests with the four pins and the five image/member/nested digests."""
import os,sys,json,gzip,collections
root,out=sys.argv[1:3]
PINS={'V3':'c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a','V4':'ce27ebca903a1574465ddfa0626943339ce6bc8155f31f88d04049afb570087f','L3':'04cfb4cd6189742eaba94d0022d242d4194726a6f0684fd8381b39bc4e6c45a3','L4':'4c0e545975d2993f5b3417d55990a5df5ad67fa2f21164b831119f6e85cbcfbc'}
OTH={'img5490':'770efb4e368a58104bf362c990114db8b70a5060932ce8bcec7ef1bc75045ab7','mem5490':'87cc5d6b3ad105221114a86f6a4d4d868f731b868ff875979e7f0cb47bcea0f8','img5491':'a5a3a763a615c2dab226d15463bc05fbc74e844736687fa5cc87a91d2f35f661','mem5491':'4cfc3016d84cccf4982d6a4c50935f1771ad350994f569496e91e42be3d92f6c','nest5491':'4d5de25c7bee7ae9206ae1882a66abe6c694ce19bcb4d568fa235fb30c7ad947'}
RES={**PINS,**OTH}.values()
subs=[]
def walk(x,p,path):
    if isinstance(x,dict):
        s=x.get('subject')
        if isinstance(s,dict) and isinstance(s.get('digest'),dict) and s['digest'].get('sha256'):
            subs.append((p,s['digest']['sha256'],os.path.basename(str(s.get('local_path') or s.get('name')))))
        for v in x.values(): walk(v,p,path)
    elif isinstance(x,list):
        for v in x: walk(v,p,path)
nfiles=0;unparsed=0
for dp,_,fn in os.walk(root):
    for f in fn:
        if not (f.endswith('.json') or f.endswith('.json.gz') or f.endswith('.jsonl')): continue
        p=os.path.join(dp,f); nfiles+=1
        try:
            b=open(p,'rb').read()
            if f.endswith('.gz'): b=gzip.decompress(b)
            t=b.decode('utf-8','replace')
            if f.endswith('.jsonl'):
                for ln in t.splitlines():
                    try: walk(json.loads(ln),os.path.relpath(p,root),'')
                    except Exception: pass
            else: walk(json.loads(t),os.path.relpath(p,root),'')
        except Exception: unparsed+=1
d=collections.Counter(s[1] for s in subs)
hits=[s for s in subs if s[1] in RES]
json.dump(dict(json_files=nfiles,unparsed=unparsed,subject_records=len(subs),distinct_subject_digests=len(d),hits_on_reserved=hits,
  files_with_subjects=len(set(s[0] for s in subs))),open(out,'w'),indent=1)
print('json files',nfiles,'unparsed',unparsed,'subject records',len(subs),'distinct digests',len(d),'files w/ subject',len(set(s[0] for s in subs)),'HITS on reserved:',hits)
