import importlib.util, json, sys
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
cc=load('cc',LANE+'/tools/round-40/c1-counter.py')
R=load('rule','/fast/scratch/hyaku/kaidoku-r40/R40W2C1SuffixAudit/rule.py')
def T(p,n=2):
    o=[]
    for l in open(LANE+'/'+p):
        c=l.rstrip('\n').split('\t')
        if len(c)>=n and c[0]: o.append(tuple(c[:n]))
    return o
N=T('corpus/evidence/round-40/c1/L2/nonregular.tsv'); O=T('corpus/evidence/round-40/c1/L2/oracle.tsv')
model=json.load(open(LANE+'/.ufo/waves/round-40/c1/gap-rule.json'))
env2=json.load(open(LANE+'/corpus/evidence/round-40/c1/L2/after.json'))
root,why=R.chunk_root(env2)
EMPTY='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
rows=[]
def case(name, cur, pro, want):
    rows.append((name, cur, pro, want, 'OK' if pro==want else 'FAIL'))

# 1 live FP: regular usr/bin/busy vs symlink bin/busy
f=[('firmware.bin_extract/usr/bin/busy','e'*64,40000)]
case('suffix-deep-regular-vs-symlink',
     cc.nonregular_published(f,N),
     [p for p,_,_ in f if any(R.same_entry(p,r,root) for r,_ in N)], [])
# 2 deeper copy satisfies oracle
o=[('usr/bin/busy','e'*64)]
f2=[('firmware.bin_extract/mnt/usr/bin/busy','e'*64,40000)]
case('suffix-deep-copy-satisfies-oracle',
     cc.oracle_hits(o,f2), sum(1 for r,s in o if any(R.same_entry(p,r,root) and s==fs for p,fs,_ in f2)),0)
# 3 empty digest elsewhere
o3=[('zero',EMPTY)]; f3=[('firmware.bin_extract/tmp/zero',EMPTY,0)]
case('suffix-empty-digest-elsewhere',
     cc.oracle_hits(o3,f3), sum(1 for r,s in o3 if any(R.same_entry(p,r,root) and s==fs for p,fs,_ in f3)),0)
# 4 gap on a regular file satisfies the symlink requirement
g=[{'kind':'depth-limited','relative_path':None},
   {'kind':'unpublished-entry','relative_path':'firmware.bin_extract/usr/bin/busy'},
   {'kind':'unpublished-entry','relative_path':'firmware.bin_extract/usr/bin/ls'}]
def gap_exact(gs):
    seen=[]
    for g in gs:
        rp=g.get('relative_path')
        if rp is None: continue
        h=[r for r,_ in N if R.same_entry(rp,r,root)]
        if len(h)!=1: return False,'unresolved %r'%rp
        seen.append(h[0])
    miss=[r for r,k in N if model['required'].get(k) and r not in seen]
    return (not miss), miss
case('gap-on-regular-satisfies-symlink', cc.gap_check(g,N,model)[0], gap_exact(g)[0], False)
# 5 nested non-regular rels
N5=[('bin','dir'),('bin/busy','symlink'),('busy','symlink')]
g5=[{'kind':'unpublished-entry','relative_path':'bin_extract/bin/busy'},{'kind':'unpublished-entry','relative_path':'bin_extract/busy'}]
def gap5():
    seen=[r for g in g5 for r,_ in N5 if R.same_entry(g['relative_path'],r,'bin_extract')]
    return len(seen)==2
case('gap-nested-nonreg-ambiguity', cc.gap_check([{'kind':'unpublished-entry','relative_path':'bin/busy'},{'kind':'unpublished-entry','relative_path':'busy'}],N5,model)[0], gap5(), True)
# 6 trailing slash
case('gap-trailing-slash', cc.same_rel('bin/busy/','bin/busy'), R.entry_rel('bin_extract/bin/busy/','bin_extract'), 'bin/busy')
# 7 absolute form (input_path style): root is not first component
case('gap-absolute-path', cc.same_rel('/fast/x/firmware.bin_extract/bin/busy','bin/busy'),
     R.entry_rel('/fast/x/firmware.bin_extract/bin/busy','firmware.bin_extract'),'bin/busy')
# 8 in-image dir named *_extract must be preserved
case('in-image-extract-dir-preserved',
     cc.rel_suffix('$output/firmware.bin_extract/opt/x_extract/y'),
     R.entry_rel('$output/firmware.bin_extract/opt/x_extract/y','firmware.bin_extract'),'opt/x_extract/y')
# 9 entry at the root is name-independent
case('entry-at-root', cc.rel_suffix('firmware.bin_extract'), R.entry_rel('firmware.bin_extract','firmware.bin_extract'),'')
# 10 rootless receipt is not attributable
case('rootless-path', cc.rel_suffix('usr/bin/busy'), R.entry_rel('usr/bin/busy','firmware.bin_extract'),None)
# 11 traversal
case('dotdot-escape', cc.rel_suffix('$output/a_extract/../../etc/passwd'), R.entry_rel('$output/a_extract/../../etc/passwd','a_extract'),None)
# 12 two roots in one receipt
e=json.loads(json.dumps(env2)); nr=e['normalized_result']
nr['derivations'].append({'parent_path':'$input','child_path':'$output/other_extract','handler':'x'})
case('two-roots', 'accepted', R.chunk_root(e)[1], 'mult_root:'+"['firmware.bin_extract', 'other_extract']")
for n,c,p,w,s in rows:
    print('%-34s current=%-28r proposed=%-28r want=%-28r %s' % (n,c,p,w,s))
print('FAILS:',[r[0] for r in rows if r[4]!='OK'])
