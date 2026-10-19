import os, subprocess, shutil
LAB="/var/tmp/ex2-arc3r6"; REPO="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
cur=open(os.path.join(REPO,"PROVINCE.md"),encoding="utf-8").read()
def block(text,header):
    lines=text.splitlines(keepends=True)
    for i,l in enumerate(lines):
        if l.startswith("- **"+header):
            j=i+1
            while j<len(lines) and lines[j].strip() and not lines[j].startswith("- **") and not lines[j].startswith("#"): j+=1
            return "".join(lines[i:j])
    raise SystemExit(header)
def rep(t,o,n,l):
    assert t.count(o)==1,(l,t.count(o)); return t.replace(o,n)
arms={}
evm=block(cur,"EVM bytecode"); pe=block(cur,">90 MB PE scale wall"); xv=block(cur,"Cross-version residuals")
# appended exact historical literals (required text intact)
arms["pe-append-wall"]=rep(cur,pe,pe.rstrip("\n")+" The 91.6 MB Godot ARM64 PE hits REA's ~900s internal session deadline.\n","pe-wall")
arms["xver-append-refused"]=rep(cur,xv,xv.rstrip("\n")+" `compare-application-versions` still probe-refused since r2.\n","xv-refused")
# stronger RISC-V citation strip (both token and path)
arms["riscv-strip-both"]=cur.replace("r5-01","r5-XX")
# new bullet inserted inside the post-unlock region (:139), line-count shifting
lines=cur.splitlines(keepends=True)
ins=-1
for i,l in enumerate(lines):
    if l.startswith("- **>90 MB PE scale wall**"): ins=i; break
assert ins>0
lines2=lines[:ins]+["- **New post-unlock bullet** — real solc/vyper-compiled bytecode untested.\n"]+lines[ins:]
arms["insert-inside"]="".join(lines2)
# instrument-visible stale pin in the Frontier (the v10 UNDECLARED boundary)
arms["frontier-pin"]=rep(cur,"- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),",
                        "- **Alternate providers** — REA lane pins rea-agents@6.3.0 on all engines (STALE TEST); IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),","pin")
for name,txt in arms.items():
    d=os.path.join(LAB,"trees",name); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,"PROVINCE.md"),"w",encoding="utf-8").write(txt)
    for f in ("SKILL.md","SCORECARD.md"): shutil.copy(os.path.join(REPO,f),d)
    print(name,len(txt.splitlines()))
