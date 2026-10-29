#!/usr/bin/env python3
"""DRAFT (C1GapRule seat). Replays a candidate gap-rule.json through the round-41 counter's own
gap_rule_model() / disposition_check() against what unblob 26.6.4 + REA 6.5.0 publication rules produce from
a REAL unblob extraction tree + report.json (REA is NOT run; its unpublished-entry / depth-limited /
unknown-chunk-handler gap construction is reproduced from FirmwarePublication.js:66-110,273-310).
usage: gap-rule-check.py RULE.json NONREG.tsv UNBLOB_OUT_DIR(chunk extract root dir) UNBLOB_REPORT.json CHUNK_ROOT_NAME [--unknown-chunks N] [--battery]
exit 0 all expectations met, 1 not, 2 could-not-evaluate"""
import sys, os, json, importlib.util, copy, stat
R='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/c1-counter.py'
spec=importlib.util.spec_from_file_location('c141',R); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
a=sys.argv[1:]
rule,nonreg,tree,report,rootname=a[:5]
unk=int(a[a.index('--unknown-chunks')+1]) if '--unknown-chunks' in a else 0
battery='--battery' in a
model,probs=c.gap_rule_model(open(rule,'rb').read().replace(b'"R50-C1"',b'"R41-C1"'))  # r41 counter pins claim==R41-C1; the port changes this string
if probs: print('rule problems',probs); sys.exit(2)
nr,err=c.parse_nonregular(open(nonreg,'rb').read())
if err: print('nonreg',err); sys.exit(2)
rep=json.load(open(report))
removed=[]
def w(x):
    if isinstance(x,dict):
        if x.get('__typename__')=='MaliciousSymlinkRemoved': removed.append(x)
        [w(v) for v in x.values()]
    elif isinstance(x,list): [w(v) for v in x]
w(rep)
# REA inventory: every lstat entry of the output that is not a directory and not a regular file => unpublished
gaps=[]
for dp,dn,fn in os.walk(tree):
    for n in dn+fn:
        p=os.path.join(dp,n); m=os.lstat(p).st_mode
        if stat.S_ISDIR(m) and not stat.S_ISLNK(m): continue
        if stat.S_ISREG(m): continue
        rel=os.path.relpath(p,tree)
        gaps.append({'kind':'unpublished-entry','relative_path':rootname+'/'+rel,'input_path':'$output/'+rootname+'/'+rel})
gaps.append({'kind':'depth-limited','relative_path':None,'input_path':'$output/'+rootname})
for _ in range(unk): gaps.append({'kind':'unknown-chunk-handler','relative_path':None,'input_path':'$output'})
diags=[{'report':{'__typename__':'MaliciousSymlinkRemoved','link':d['link'],'target':d['target']}} for d in removed]
root=rootname
def chk(g,d,n,m=model,label=''):
    ok,why=c.disposition_check(g,d,n,m,root); return ok,why
ok,why=chk(gaps,diags,nr)
print('REAL',ok,why); fails=0 if ok else 1
if battery:
    def exp(name,res,want_ok):
        global fails
        good=(res[0]==want_ok); fails+=0 if good else 1
        print('MUT %-46s want=%s got=%s %s'%(name,want_ok,res[0],'' if good else '<<<< UNEXPECTED'), '' if res[0] else '| '+res[1][:110])
    sym=[r for r in nr if r[1]=='symlink']
    present=[g for g in gaps if g['kind']=='unpublished-entry']
    ps=[g for g in present if any(g['relative_path']==root+'/'+r[0] for r in sym)]
    # 1 drop one symlink gap (present link without a record)
    if ps: exp('drop a published-symlink gap',chk([g for g in gaps if g is not ps[0]],diags,nr),False)
    # 2 gap AND removal on same entry
    if diags:
        rel=c.diagnostic_rel(diags[0],root); gg=gaps+[{'kind':'unpublished-entry','relative_path':root+'/'+rel,'input_path':'$output/'+root+'/'+rel}]
        exp('removed entry also gapped',chk(gg,diags,nr),False)
        exp('removal diag kept, entry gap dropped = fine (exclusive)',chk(gaps,diags,nr),True)
        # 3 removal diag on a dir
        d0=[x for x in nr if x[1]=='dir'][0][0]
        dd=diags+[{'report':{'__typename__':'MaliciousSymlinkRemoved','link':'/x/'+root+'/'+d0}}]
        exp('removal diag resolving to a dir',chk(gaps,dd,nr),False)
        # 4 removal diag for a path not in the table
        dd=diags+[{'report':{'__typename__':'MaliciousSymlinkRemoved','link':'/x/'+root+'/nope/at/all'}}]
        exp('removal diag for unknown path',chk(gaps,dd,nr),False)
        # 5 removed link left with no diagnostic (silent removal of a symlink)
        exp('symlink removed with no diagnostic',chk(gaps,diags[1:],nr),False)
    # 6 symlink published AND entry is a regular-file gap kind unknown
    if ps:
        gg=[dict(g) for g in gaps]; 
        for g in gg:
            if g is not None and g.get('relative_path')==ps[0]['relative_path']: g['kind']='extractor-failure'
        exp('symlink gap of a kind the rule does not allow',chk(gg,diags,nr),False)
    # 7 structural
    exp('extra depth-limited gap',chk(gaps+[{'kind':'depth-limited','relative_path':None,'input_path':'x'}],diags,nr),False)
    exp('extra unknown-chunk-handler gap',chk(gaps+[{'kind':'unknown-chunk-handler','relative_path':None,'input_path':'x'}],diags,nr),unk>=1 and model['structural'].get('unknown-chunk-handler',0)>=unk+1)
    exp('no depth-limited gap is fine (<= allowance)',chk([g for g in gaps if g['kind']!='depth-limited'],diags,nr),True)
    # 8 device rows
    dev=[r for r in nr if r[1]=='char-device']
    if dev:
        # silent device accepted (REAL) ; mutate detail so rule's exact silent label no longer matches
        nr2=[(r[0],r[1],'999:9') if r[1]=='char-device' else r for r in nr]
        exp('char-device with a detail the rule does not list',chk(gaps,diags,nr2),False)
        # privileged run: device materialised -> unpublished-entry gap on it => allowed
        exp('char-device published as special (root run)',chk(gaps+[{'kind':'unpublished-entry','relative_path':root+'/'+dev[0][0],'input_path':'x'}],diags,nr),True)
        exp('char-device with extractor-failure gap',chk(gaps+[{'kind':'extractor-failure','relative_path':root+'/'+dev[0][0],'input_path':'x'}],diags,nr),False)
    # 9 gap on a dir
    d0=[x for x in nr if x[1]=='dir'][0][0]
    exp('unpublished-entry gap on a directory',chk(gaps+[{'kind':'unpublished-entry','relative_path':root+'/'+d0,'input_path':'x'}],diags,nr),False)
    # 10 gap outside any entry
    exp('gap for a path not in the table',chk(gaps+[{'kind':'unpublished-entry','relative_path':root+'/zz/none','input_path':'x'}],diags,nr),False)
    # 11 empty-target symlink: not silently admissible under this rule (no silent symlink label)
    nr3=nr+[('zz/empty','symlink','')]
    exp('empty-target symlink with no record (r41 silent label NOT carried)',chk(gaps,diags,nr3),False)
    # 12 the round-41 rule vs this one: both accept the real unprivileged tree; they differ only on the two device mutations
    r41=c.gap_rule_model(open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-41/c1/gap-rule.json','rb').read())[0]
    exp('round-41 rule accepts the real tree (device silent: required=false)',chk(gaps,diags,nr,r41),True)
    if dev:
        exp('round-41 rule REJECTS a privileged-run device gap (false-fail)',chk(gaps+[{'kind':'unpublished-entry','relative_path':root+'/'+dev[0][0],'input_path':'x'}],diags,nr,r41),False)
        nr2=[(r[0],r[1],'999:9') if r[1]=='char-device' else r for r in nr]
        exp('round-41 rule ACCEPTS a device row with unlisted detail (laxer)',chk(gaps,diags,nr2,r41),True)
print('FAILS',fails); sys.exit(0 if fails==0 else 1)
