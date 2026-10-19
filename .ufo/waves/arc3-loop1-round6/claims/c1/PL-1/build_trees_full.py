#!/usr/bin/env python3
"""Build every PL-1 fault tree from git HEAD / 40de383~1. Deterministic;
asserts the pre-state text before seeding. Scratch-only (no repo writes)."""
import os, subprocess, shutil, sys
L = os.path.dirname(os.path.abspath(__file__)); R = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def git_show(rev, path):
    return subprocess.run(["git","show",f"{rev}:{path}"],cwd=R,capture_output=True,text=True,check=True).stdout.splitlines()
head = git_show("HEAD","PROVINCE.md"); pre = git_show("40de383~1","PROVINCE.md")
assert len(head)==162 and len(pre)==162
assert pre[91].startswith("  (Core, r3-07); real solc/vyper-compiled bytecode untested")
assert pre[138].startswith("- **>90 MB PE scale wall** — 91.6 MB")
assert pre[156].startswith("- **Cross-version residuals** — `compare-application-versions` still")
skill=open(os.path.join(R,"SKILL.md")).read(); score=open(os.path.join(R,"SCORECARD.md")).read()
def mk(name, prov):
    d=os.path.join(L,"trees",name); shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    open(os.path.join(d,"PROVINCE.md"),"w").write("\n".join(prov)+"\n")
    open(os.path.join(d,"SKILL.md"),"w").write(skill); open(os.path.join(d,"SCORECARD.md"),"w").write(score)
def copy(name): mk(name, list(head))
copy("clean")
x=list(head); x[91:93]=pre[91:93]; mk("seed-evm", x)
x=list(head); x[91]=x[91]+" — untested"; mk("seed-evm-only", x)
x=list(head); x[138:144]=pre[138:144]; mk("seed-wall", x)
x=list(head); x[138]="- **>90 MB PE scale wall** — hits REA's ~900s internal session deadline (STALE TEST)"; mk("seed-wall-oneline", x)
x=list(head); x[142]=x[142]+" The wall still hits REA's ~900s internal session deadline on rerun."; mk("seed-wall-tokens", x)
x=list(head); x[156:160]=pre[156:160]; mk("seed-cross", x)
x=list(head); x[159]=x[159]+" `compare-application-versions` still probe-refused since r2."; mk("seed-cross-tokens", x)
mk("trunc161", head[:161]); mk("trunc160", head[:160])
for at in (92,133,134,140,150,157):
    x=list(head); x[at-1:at-1]=[""]; mk(f"reflow133" if at==133 else f"insert-{at}", x)
x=list(head); x.insert(132,""); x.insert(133,""); mk("reflow133-2", x)
x=list(head); x[132:132]=[""]*3; mk("reflow133-3", x)
x=list(head); x[87]="- **Alternate providers** — REA lane pins rea-agents@6.3.0 on all engines (STALE TEST)"; mk("seed-pin", x)
mk("append", list(head)+["- **New frontier claim** — locus-free text appended past the declared bound."])
print("built", len(os.listdir(os.path.join(L,"trees"))), "trees")
