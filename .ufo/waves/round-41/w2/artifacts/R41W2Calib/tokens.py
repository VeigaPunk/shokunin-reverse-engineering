#!/usr/bin/env python3
"""R41W2Calib: extract mechanical tokens (hashes, paths) from SHONEN.md and SCORECARD Owned axes/Capabilities at REV and resolve them against git objects. Read-only. usage: tokens.py LANE REV"""
import re, subprocess, sys, itertools
L, R = sys.argv[1], sys.argv[2]
def git(*a): return subprocess.run(["git","-C",L,*a],capture_output=True,text=True)
def show(p): return git("show",f"{R}:{p}").stdout
sh=show("SHONEN.md").split("\n"); sc=show("SCORECARD.md").split("\n")
# SCORECARD owned axes = from '## Owned axes' to next '## '; capabilities likewise
def sect(lines,h):
    i=next(k for k,l in enumerate(lines) if l.startswith(h)); j=next((k for k in range(i+1,len(lines)) if lines[k].startswith("## ")),len(lines)); return i,j
oi,oj=sect(sc,"## Owned axes"); ci,cj=sect(sc,"## Capabilities")
segs=[("SHONEN",i+1,l) for i,l in enumerate(sh)]+[("SC",i+1,sc[i]) for i in itertools.chain(range(oi,oj),range(ci,cj))]
tree=set(git("ls-tree","-r","--name-only",R).stdout.splitlines())
dirs={p.rsplit("/",1)[0] for p in tree if "/" in p}|{p.rsplit("/",2)[0] for p in tree if p.count("/")>1}
alldirs=set()
for p in tree:
    parts=p.split("/")
    for k in range(1,len(parts)): alldirs.add("/".join(parts[:k]))
def expand(s):
    m=re.search(r"\{([^{}]*)\}",s)
    if not m: return [s]
    out=[]
    for alt in m.group(1).split(","): out+=expand(s[:m.start()]+alt+s[m.end():])
    return out
hashes={}; paths={}
for f,n,l in segs:
    for m in re.finditer(r"(?<![0-9a-f])([0-9a-f]{7,40})(?![0-9a-f])",l):
        h=m.group(1)
        if re.search(r"\d",h) and re.search(r"[a-f]",h): hashes.setdefault(h,[]).append(f"{f}:{n}")
    for m in re.finditer(r"`([^`]+)`",l):
        t=m.group(1)
        if re.match(r"(\.ufo|corpus|tools|plans|evidence|PROVINCE|SKILL|SCORECARD|SHONEN|LOG|QUALITY|AXES|MANIFEST)[A-Za-z0-9_./{},*<>:\-+]*",t) and not t.startswith(("python","bash")):
            t0=re.sub(r":\d+(-\d+)?$","",t.split()[0])
            paths.setdefault(t0,[]).append(f"{f}:{n}")
print("== hashes",len(hashes))
for h,w in sorted(hashes.items()):
    p=git("rev-parse","--verify",h+"^{commit}")
    if p.returncode: 
        p2=git("cat-file","-t",h)
        print(f"UNRESOLVED-AS-COMMIT {h} {w[:3]} cat-file:{p2.stdout.strip() or 'none'}"); continue
    full=p.stdout.strip(); anc=git("merge-base","--is-ancestor",full,R).returncode==0
    print(f"ok {h} -> {full[:12]} ancestor_of_REV={anc} refs={len(w)} first={w[0]} :: {git('log','-1','--format=%s',full).stdout.strip()[:70]}")
print("== paths",len(paths))
import os
for t,w in sorted(paths.items()):
    if any(c in t for c in "<>*"): print(f"SKIP-pattern {t} {w[:2]}"); continue
    for e in expand(t):
        e=e.rstrip("/")
        st = "file" if e in tree else ("dir" if e in alldirs else None)
        if not st: st="MISSING-in-tree"+(" (in worktree)" if os.path.exists(os.path.join(L,e)) else "")
        if st.startswith("MISSING"): print(f"{st} {e} <- {w[:3]}")
print("tokens done")
