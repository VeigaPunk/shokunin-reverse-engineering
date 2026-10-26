import hashlib, os, stat, sys, json

def read_tsv(p):
    out=[]
    for line in open(p, encoding='utf-8', errors='surrogateescape'):
        line=line.rstrip('\n')
        if not line.strip(): continue
        out.append(line.split('\t'))
    return out

res={}
for cid in ('V1','V2','L1','L2'):
    root=os.path.join('x',cid,'root')
    oracle={r[0]: (r[1], int(r[2])) for r in read_tsv(os.path.join('out',cid,'oracle.tsv'))}
    nonreg={r[0]: (r[1], r[2] if len(r)>2 else '') for r in read_tsv(os.path.join('out',cid,'nonregular.tsv'))}
    seen_files={}; seen_links={}; seen_dirs=set(); others={}
    for dp, dns, fns in os.walk(root):
        rel=os.path.relpath(dp, root)
        if rel!='.': seen_dirs.add(rel)
        for n in list(dns):
            p=os.path.join(dp,n); r=os.path.relpath(p, root)
            if os.path.islink(p):
                seen_links[r]=os.readlink(p); dns.remove(n)
        for n in fns:
            p=os.path.join(dp,n); r=os.path.relpath(p, root)
            st=os.lstat(p)
            if stat.S_ISLNK(st.st_mode): seen_links[r]=os.readlink(p)
            elif stat.S_ISREG(st.st_mode):
                h=hashlib.sha256(open(p,'rb').read()).hexdigest()
                seen_files[r]=(h, st.st_size)
            else: others[r]=stat.S_IFMT(st.st_mode)
    # compare
    missing=sorted(set(oracle)-set(seen_files))
    extra=sorted(set(seen_files)-set(oracle))
    bad_hash=[k for k in set(oracle)&set(seen_files) if oracle[k][0]!=seen_files[k][0]]
    bad_size=[k for k in set(oracle)&set(seen_files) if oracle[k][1]!=seen_files[k][1]]
    lmiss=sorted({k for k,v in nonreg.items() if v[0]=='symlink'} - set(seen_links))
    lextra=sorted(set(seen_links)-{k for k,v in nonreg.items() if v[0]=='symlink'})
    bad_target=[k for k,v in nonreg.items() if v[0]=='symlink' and k in seen_links and seen_links[k]!=v[1]]
    dmiss=sorted({k for k,v in nonreg.items() if v[0]=='dir'} - seen_dirs)
    dextra=sorted(seen_dirs-{k for k,v in nonreg.items() if v[0]=='dir'})
    devs={k:v for k,v in nonreg.items() if v[0] not in ('symlink','dir')}
    res[cid]=dict(oracle_files=len(oracle), extracted_files=len(seen_files),
                  hashes_mismatch=len(bad_hash), sizes_mismatch=len(bad_size),
                  missing_files=missing[:5], extra_files=extra[:5],
                  oracle_symlinks=sum(1 for v in nonreg.values() if v[0]=='symlink'),
                  extracted_symlinks=len(seen_links), bad_targets=bad_target[:5],
                  symlink_missing=lmiss[:5], symlink_extra=lextra[:5],
                  dirs_oracle=sum(1 for v in nonreg.values() if v[0]=='dir'),
                  dirs_extracted=len(seen_dirs), dirs_missing=dmiss[:5], dirs_extra=dextra[:5],
                  device_entries=devs, other_nodes=sorted(others)[:5])
print(json.dumps(res, indent=1))
