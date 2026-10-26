#!/usr/bin/env python3
"""Third-party leg: hash a direct sasquatch-v4be extraction (NO -be) and compare it to
the committed oracle.tsv / nonregular.tsv. argv: LABEL=TREE=ORACLE=TSV ..."""
import hashlib, json, os, sys
res={}
for arg in sys.argv[1:]:
    label,tree,oracle,nonreg=arg.split('=',3)
    files={}; syms={}; dirs=set()
    for dp,dn,fn in os.walk(tree):
        for n in dn+fn:
            p=os.path.join(dp,n); rel=os.path.relpath(p,tree)
            if os.path.islink(p): syms[rel]=os.readlink(p)
            elif os.path.isdir(p): dirs.add(rel)
            elif os.path.isfile(p):
                try: files[rel]=(hashlib.sha256(open(p,'rb').read()).hexdigest(), os.path.getsize(p))
                except OSError: pass
    orows={}
    for line in open(oracle,encoding='utf-8'):
        if line.strip():
            p,h,s=line.rstrip('\n').split('\t'); orows[p]=(h,int(s))
    nrows={}
    for line in open(nonreg,encoding='utf-8'):
        if line.strip():
            f=line.rstrip('\n').split('\t'); nrows[f[0]]=(f[1], f[2] if len(f)>2 else None)
    nsym={p:v for p,v in nrows.items() if v[0]=='symlink'}
    ndir={p for p,v in nrows.items() if v[0]=='dir'}
    ndev={p for p,v in nrows.items() if v[0] not in ('dir','symlink')}
    res[label]={'sasquatch_files':len(files),'sasquatch_symlinks':len(syms),'sasquatch_dirs':len(dirs),
                'oracle_rows':len(orows),'oracle_only':sorted(set(orows)-set(files)),
                'tree_only':sorted(set(files)-set(orows)),
                'value_differ':[p for p in set(orows)&set(files) if orows[p]!=files[p]],
                'symlink_path_sets_equal':set(nsym)==set(syms),
                'symlink_target_mismatch':[p for p in set(nsym)&set(syms) if (nsym[p][1] or '')!=syms[p]],
                'dir_path_sets_equal':ndir==dirs,
                'device_rows':sorted(ndev),
                'device_created_by_sasquatch':sorted(ndev & {os.path.relpath(os.path.join(dp,n),tree) for dp,dn,fn in os.walk(tree) for n in dn+fn})}
print(json.dumps(res,indent=1,sort_keys=True))
