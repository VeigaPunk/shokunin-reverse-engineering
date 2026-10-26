import json,os,hashlib,sys
H='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-39/c2/heldout/'
S='/fast/scratch/hyaku/kaidoku-r39/R39W2HeldReproA/'
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda: f.read(1<<20), b''): h.update(b)
    return h.hexdigest()
for i in sys.argv[1:]:
    tree=json.load(open(H+i+'/tree.json'))
    root=os.path.join(S,'fresh',i+'-out','firmware.bin_extract')
    act_files={}; act_dirs=set(); act_links={}
    for dp,dns,fns in os.walk(root):
        for dn in dns: act_dirs.add(os.path.relpath(os.path.join(dp,dn),root))
        for fn in fns:
            p=os.path.join(dp,fn); rel=os.path.relpath(p,root)
            if os.path.islink(p): act_links[rel]=os.readlink(p)
            else: act_files[rel]=(sha(p),os.path.getsize(p))
    orc=tree['oracle']
    of={f['path']:(f['sha256'],f['size']) for f in orc['files']}
    od=set(orc['directories']); ol={s['path']:s.get('target') for s in orc.get('symlinks',[])}
    # normalize: unblob may emit firmware.bin_extract top; oracle paths are relative to extraction root
    print('==',i,'class',tree['class'],'endian',tree.get('endian'),'compression',tree.get('compression'))
    print('   oracle files',len(of),'dirs',len(od),'symlinks',len(ol))
    print('   actual files',len(act_files),'dirs',len(act_dirs),'symlinks',len(act_links))
    print('   files match:',of==act_files)
    if of!=act_files:
        print('     only-oracle',{k:v for k,v in of.items() if k not in act_files})
        print('     only-actual',{k:v for k,v in act_files.items() if k not in of})
        print('     diff-values',{k:(of[k],act_files[k]) for k in of if k in act_files and of[k]!=act_files[k]})
    print('   dirs match:',od==act_dirs, 'od-act',od-act_dirs,'act-od',act_dirs-od)
    print('   symlinks match:',ol==act_links, 'oracle',ol,'actual',act_links)
