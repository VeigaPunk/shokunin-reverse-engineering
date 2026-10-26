import importlib.util, json, os, subprocess, sys, gzip, tempfile
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
INTERP=LANE+'/tools/round-40/sqfs-triage-v2.py'
HELD=LANE+'/corpus/evidence/round-40/c2/heldout'
DEV=LANE+'/.ufo/waves/round-40/w1/artifacts/R40C2HeldoutGen/dev-run'
HEADER=['label','operation','provider','handler','gap kinds','dependencies','-be in child argv','symlink removed','published files','action','cause','source']
VOCAB='none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty'

def envelope_paths(which):
    root = HELD if which=='held' else DEV
    man=json.load(open(os.path.join(root,'manifest.json')))
    out=[]
    for c in man['carriers']:
        p=os.path.join(root,c['id'],'envelope.json' if which=='held' else 'envelope.json.gz')
        out.append((c['id'],c['class'],c['label'],c['action'],p))
    return out

def materialize(which,work):
    envs=[]
    for cid,cls,lab,act,p in envelope_paths(which):
        if p.endswith('.gz'):
            fp=os.path.join(work,cid+'.json'); open(fp,'wb').write(gzip.open(p).read())
        else: fp=p
        envs.append((cid,cls,lab,act,fp))
    return envs

def skill_file(rows, path, marker='<!-- sqfs-triage-table v2 -->'):
    cell=lambda s: '`%s`'%s if s!='*' else '*'
    out=['# SKILL','','## Queue-drain craft','','prose.','',marker,
         '<!-- sqfs-triage-actions: %s -->'%VOCAB,
         '| '+' | '.join(HEADER)+' |','|'+' --- |'*len(HEADER)]
    for r in rows:
        out.append('| '+' | '.join(r)+' |')
    out+=['','## Later','','x','']
    open(path,'w').write('\n'.join(out))
    return path

def score(skill, envs):
    p=subprocess.run([sys.executable,'-I','-B',INTERP,'--skill',skill]+[e[4] for e in envs],
                     capture_output=True,text=True)
    got={}
    for line in p.stdout.splitlines():
        f=line.split('\t')
        if len(f)>=3:
            key=os.path.basename(f[0])
            for suf in ('.json','.json.gz'):
                if key.endswith(suf): key=key[:-len(suf)]
            if key in ('envelope','after'):
                key=os.path.basename(os.path.dirname(f[0]))
            got[key]=(f[1].strip(),f[2].strip())
    right=[e for e in envs if got.get(e[0])==(e[2],e[3])]
    wrong=sorted({e[1] for e in envs if got.get(e[0])!=(e[2],e[3])})
    return {'exit':p.returncode,'matched':len(right),'n':len(envs),'wrong':wrong,
            'stderr':p.stderr.strip()[:300],'got':got}

def row(label, op='*', pv='*', h='*', g='*', d='*', be='*', sr='*', files='*',
        action='none', cause='cause -> action', source='w2-min'):
    return [label,op,pv,h,g,d,be,sr,files,action,cause,source]
