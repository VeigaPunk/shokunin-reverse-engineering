import os, subprocess, shutil
L="/var/tmp/pl1-arc3r6"; R="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def git_show(rev, path):
    return subprocess.run(["git","show",f"{rev}:{path}"],cwd=R,capture_output=True,text=True,check=True).stdout.splitlines()
head = git_show("HEAD","PROVINCE.md")
pre  = git_show("40de383~1","PROVINCE.md")
assert len(head)==162 and len(pre)==162, (len(head),len(pre))
# sanity: pre-state blocks
assert pre[91].startswith("  (Core, r3-07); real solc/vyper-compiled bytecode untested"), pre[91]
assert pre[138].startswith("- **>90 MB PE scale wall** — 91.6 MB"), pre[138]
assert pre[156].startswith("- **Cross-version residuals** — `compare-application-versions` still"), pre[156]

def mk(name, prov, extra=None):
    d=os.path.join(L,"trees",name); shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    open(os.path.join(d,"PROVINCE.md"),"w").write("\n".join(prov)+"\n")
    for f in ("SKILL.md","SCORECARD.md"):
        open(os.path.join(d,f),"w").write(text[f])
    if extra: extra(d)

text={f:open(os.path.join(L,"trees","clean",f)).read() for f in ("SKILL.md","SCORECARD.md")}
mk("clean", head)
evm=list(head); evm[91:93]=pre[91:93]; mk("seed-evm", evm)
wall=list(head); wall[138:144]=pre[138:144]; mk("seed-wall", wall)
cross=list(head); cross[156:160]=pre[156:160]; mk("seed-cross", cross)
mk("trunc161", head[:161])
mk("trunc160", head[:160])
refl=list(head); refl[132:132]=[""]; mk("reflow133", refl)
pin=list(head); pin[87]="- **Alternate providers** — REA lane pins rea-agents@6.3.0 on all engines (STALE TEST)"
mk("seed-pin", pin)
app=list(head)+["- **New frontier claim** — locus-free text appended past the declared bound."]
mk("append", app)
print("trees built")
for n in sorted(os.listdir(os.path.join(L,"trees"))):
    p=os.path.join(L,"trees",n,"PROVINCE.md")
    print(f"{n:12s} lines={len(open(p).read().splitlines())}")
