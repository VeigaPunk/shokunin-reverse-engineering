import sys,os,json,importlib.util
O='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w1/C1OracleBuild/'
spec=importlib.util.spec_from_file_location('ob',O+'tools/round-50/oracle-build.py');ob=importlib.util.module_from_spec(spec);spec.loader.exec_module(ob)
res={}
for cid in ['a7530','a7590','c6490','c6430']:
    root=[os.path.join('ub',cid,'fs.image_extract',d) for d in os.listdir(f'ub/{cid}/fs.image_extract') if d.endswith('squashfs_v4_le_extract')][0]
    tree,errs=ob.walk_tree(root)
    # also the single-child layout? ensure root contents
    orc={l.split('\t')[0]:l.rstrip('\n').split('\t')[1:] for l in open(O+cid+'/oracle.tsv',encoding='utf-8',errors='surrogateescape')}
    nr={l.split('\t')[0]:l.rstrip('\n').split('\t')[1:] for l in open(O+cid+'/nonregular.tsv',encoding='utf-8',errors='surrogateescape')}
    f={r:(v[3],str(v[1])) for r,v in tree.items() if v[0]=='file'}
    s={r:v[2] for r,v in tree.items() if v[0]=='symlink'}
    d={r for r,v in tree.items() if v[0]=='dir'}
    onlyo=sorted(set(orc)-set(f)); onlyu=sorted(set(f)-set(orc))
    diff=[r for r in set(orc)&set(f) if orc[r]!=list(f[r])]
    osyms={r:v[1] for r,v in nr.items() if v[0]=='symlink'}; odirs={r for r,v in nr.items() if v[0]=='dir'}
    rem=sorted(set(osyms)-set(s)); symdiff=[r for r in set(osyms)&set(s) if osyms[r]!=s[r]]
    res[cid]={'oracle_files':len(orc),'ub_files':len(f),'files_missing_in_ub':len(onlyo),'files_extra_in_ub':len(onlyu),'files_differ':len(diff),
      'oracle_syms':len(osyms),'ub_syms':len(s),'syms_removed_by_ub':len(rem),'syms_target_differs':len(symdiff),'syms_extra_in_ub':len(set(s)-set(osyms)),
      'oracle_dirs':len(odirs),'ub_dirs':len(d),'dirs_missing_in_ub':len(odirs-d),
      'oracle_devices':[r for r,v in nr.items() if v[0].endswith('device')],'ub_devices':[r for r,v in tree.items() if v[0].endswith('device')],
      'removed_examples':[[r,osyms[r]] for r in rem[:6]],'removed_abs':sum(1 for r in rem if osyms[r].startswith('/')),
      'removed_rel':sum(1 for r in rem if not osyms[r].startswith('/')),'missing_files_examples':onlyo[:5],'extra_files_examples':onlyu[:5]}
    json.dump({'removed_symlinks':[[r,osyms[r]] for r in rem],'missing_files':onlyo,'extra_files':onlyu,'file_diffs':diff,'symlink_target_diffs':[[r,osyms[r],s[r]] for r in symdiff]},open(O+cid+'/unblob-vs-oracle.json','w'),indent=1)
print(json.dumps(res,indent=1))
