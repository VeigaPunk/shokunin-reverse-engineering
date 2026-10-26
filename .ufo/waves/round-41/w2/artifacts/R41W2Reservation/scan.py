#!/usr/bin/env python3
"""Reservation scan: wave-1 tree (frozen commit export and live working tree)."""
import os,re,sys,json,gzip,hashlib,collections
PINS={'V3':'c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a',
'V4':'ce27ebca903a1574465ddfa0626943339ce6bc8155f31f88d04049afb570087f',
'L3':'04cfb4cd6189742eaba94d0022d242d4194726a6f0684fd8381b39bc4e6c45a3',
'L4':'4c0e545975d2993f5b3417d55990a5df5ad67fa2f21164b831119f6e85cbcfbc'}
OTHER={'img5490':'770efb4e368a58104bf362c990114db8b70a5060932ce8bcec7ef1bc75045ab7',
'mem5490':'87cc5d6b3ad105221114a86f6a4d4d868f731b868ff875979e7f0cb47bcea0f8',
'img5491':'a5a3a763a615c2dab226d15463bc05fbc74e844736687fa5cc87a91d2f35f661',
'mem5491':'4cfc3016d84cccf4982d6a4c50935f1771ad350994f569496e91e42be3d92f6c',
'nest5491':'4d5de25c7bee7ae9206ae1882a66abe6c694ce19bcb4d568fa235fb30c7ad947'}
ALL={**PINS,**OTHER}
HEX8=re.compile('|'.join(v[:8] for v in ALL.values()))
NAMES=re.compile(r'5490|5491|FRITZ\.?Box_549|filesystem_core|carrier\.sqsh|\bL[34]\b|\bV[34]\b')
REA=re.compile(r'extract-firmware|rea-agents|REA_UNBLOB|\bunblob\b|\bREA\b|rea_extract|\brea\b',re.I)
root=sys.argv[1]; out=collections.defaultdict(list)
files=[];sha_hits=[]
def lines_of(p):
    b=open(p,'rb').read()
    if p.endswith('.gz'):
        try:b=gzip.decompress(b)
        except Exception:pass
    return b
for dp,dn,fn in os.walk(root):
    for f in sorted(fn):
        p=os.path.join(dp,f); rel=os.path.relpath(p,root); b=lines_of(p)
        h=hashlib.sha256(b).hexdigest()
        for k,v in ALL.items():
            if h==v: sha_hits.append((rel,k,'file-bytes-equal'))
        t=b.decode('utf-8','replace')
        L=t.split('\n'); A8=[i for i,l in enumerate(L) if HEX8.search(l)]
        NM=[i for i,l in enumerate(L) if NAMES.search(l)]
        RE=[i for i,l in enumerate(L) if REA.search(l)]
        files.append(dict(path=rel,size=len(b),hex=len(A8),names=len(NM),rea=len(RE),
            hex_and_rea_lines=[i+1 for i in A8 if REA.search(L[i])],
            name_and_rea_lines=[i+1 for i in NM if REA.search(L[i])]))
        # envelope detection
        if f.endswith('.json') or f.endswith('.json.gz'):
            try:
                d=json.loads(t)
                if isinstance(d,dict) and 'subject' in d and 'provider' in d:
                    sd=((d.get('subject') or {}).get('digest') or {}).get('sha256')
                    out['envelopes'].append((rel,sd,sd in ALL.values()))
            except Exception: pass
json.dump(dict(root=root,nfiles=len(files),files=files,sha_equal=sha_hits,envelopes=out['envelopes']),open(sys.argv[2],'w'),indent=1)
print(len(files),'files; envelope jsons:',len(out['envelopes']),'with reserved subject:',sum(1 for e in out['envelopes'] if e[2]))
print('byte-equal hits:',sha_hits)
print('files with hex8 hits:',sum(1 for f in files if f['hex']))
print('files hex8 AND rea-marker on same line:',[(f['path'],f['hex_and_rea_lines'][:5]) for f in files if f['hex_and_rea_lines']])
print('files name AND rea same line:',sum(1 for f in files if f['name_and_rea_lines']))
