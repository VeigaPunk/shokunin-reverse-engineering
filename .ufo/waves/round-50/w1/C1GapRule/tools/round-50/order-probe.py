#!/usr/bin/env python3
"""Replay unblob 26.6.4 extractor.fix_extracted_directory over a skeleton of the carrier's tree
(dirs + symlinks with their raw targets + empty regular files) under random readdir orders.
usage: order-probe.py ORACLE.tsv NONREG.tsv SKELDIR N OUT.json   (run with unblob's python)"""
import sys, os, json, random, shutil, pathlib, collections
sys.setrecursionlimit(10000)
import unblob.extractor as ex
oracle, nonreg, skel, n, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
files=[l.split('\t')[0] for l in open(oracle) if l.strip()]
nr=[l.rstrip('\n').split('\t') for l in open(nonreg) if l.strip()]
class TR:
    def __init__(s): s.reports=[]
    def add_report(s,r): s.reports.append(r)
def build(dst):
    if os.path.lexists(dst): shutil.rmtree(dst)
    os.makedirs(dst)
    for rel,kind,*d in nr:
        if kind=='dir': os.makedirs(os.path.join(dst,rel),exist_ok=True)
    for rel in files:
        open(os.path.join(dst,rel),'w').close()
    for rel,kind,*d in nr:
        if kind=='symlink': os.symlink(d[0] if d else '', os.path.join(dst,rel)) if (d and d[0]!='') else None
def run(order):
    build(skel)
    orig=pathlib.Path.iterdir
    rnd=random.Random(order)
    def it(self):
        l=list(orig(self))
        if order=='sorted': l.sort()
        elif order=='reverse': l.sort(reverse=True)
        elif order=='native': pass
        else: rnd.shuffle(l)
        return iter(l)
    pathlib.Path.iterdir=it
    tr=TR()
    try: ex.fix_extracted_directory(pathlib.Path(skel),tr)
    finally: pathlib.Path.iterdir=orig
    return tuple(sorted(os.path.relpath(r.link,skel) for r in tr.reports)), len(tr.reports)
res=collections.Counter(); first={}
for o in ['native','sorted','reverse']+['s%d'%i for i in range(n)]:
    k,c=run(o); res[k]+=1; first.setdefault(k,o)
    if o in('native','sorted','reverse'): print(o,c,list(k))
print('distinct removed-sets:',len(res))
for k,v in res.most_common(): print(v,'x',first[k],len(k),list(k))
json.dump([{'count':v,'first_order':first[k],'removed':list(k)} for k,v in res.most_common()],open(out,'w'),indent=1)
