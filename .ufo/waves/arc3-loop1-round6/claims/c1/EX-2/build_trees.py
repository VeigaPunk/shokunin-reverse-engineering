import os, subprocess, shutil
LAB="/var/tmp/ex2-arc3r6"
REPO="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
cur = open(os.path.join(REPO,"PROVINCE.md"),encoding="utf-8").read()
pre = subprocess.check_output(["git","-C",REPO,"show","40de383^:PROVINCE.md"]).decode()

def block(text, header):
    lines = text.splitlines(keepends=True)
    for i,l in enumerate(lines):
        if l.startswith("- **"+header):
            j=i+1
            while j < len(lines) and lines[j].strip() and not lines[j].startswith("- **") and not lines[j].startswith("#"):
                j+=1
            return "".join(lines[i:j])
    raise SystemExit("header not found: "+header)

def replace_once(text, old, new, label):
    n = text.count(old)
    assert n == 1, (label, n)
    return text.replace(old, new)

arms={}
arms["clean"]=cur
# 1 frozen seed: historical EVM before-state
evm_cur=block(cur,"EVM bytecode"); evm_pre=block(pre,"EVM bytecode")
print("EVM current lines", evm_cur.count("\n"), "pre lines", evm_pre.count("\n"))
arms["evm-revert"]=replace_once(cur,evm_cur,evm_pre,"evm")
# 2 case seed
arms["evm-revert-upper"]=replace_once(cur,evm_cur,evm_pre.replace("untested","UNTESTED"),"evm-upper")
# 3 appended stale literal (required intact)
arms["evm-append"]=replace_once(cur,evm_cur,evm_cur.rstrip("\n")+" Real solc/vyper-compiled bytecode untested.\n","evm-append")
# 4 required stripped, line-count neutral
arms["evm-strip"]=replace_once(cur,evm_cur,"- **EVM bytecode (extended)** — see corpus.\n  Selectors recorded in the corpus entry.\n  Naming deferred.\n","evm-strip")
# 5 PE wall revert
pe_cur=block(cur,">90 MB PE scale wall"); pe_pre=block(pre,">90 MB PE scale wall")
print("PE current lines", pe_cur.count("\n"), "pre lines", pe_pre.count("\n"))
arms["pe-revert"]=replace_once(cur,pe_cur,pe_pre,"pe")
# 6 PE appended stale remedy (required intact)
arms["pe-append"]=replace_once(cur,pe_cur,pe_cur.rstrip("\n")+" Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS to ~3.6Ms.\n","pe-append")
# 7 cross-version revert
xv_cur=block(cur,"Cross-version residuals"); xv_pre=block(pre,"Cross-version residuals")
print("XVER current lines", xv_cur.count("\n"), "pre lines", xv_pre.count("\n"))
arms["xver-revert"]=replace_once(cur,xv_cur,xv_pre,"xver")
# 8 PE subtypes revert
st_cur=block(cur,"PE subtypes"); st_pre=block(pre,"PE subtypes")
arms["subtypes-revert"]=replace_once(cur,st_cur,st_pre,"subtypes")
# 9 crashes revert
cr_cur=block(cur,"Recorded crashes >32 MiB"); cr_pre=block(pre,"Recorded crashes >32 MiB")
arms["crashes-revert"]=replace_once(cur,cr_cur,cr_pre,"crashes")
# 10 novel stale claim (not on any register)
arms["novel-stale"]=replace_once(cur,evm_cur,evm_cur.rstrip("\n")+" No real carriers have ever been compiled.\n","novel")
# 11 RISC-V citation stripped
arms["riscv-strip"]=replace_once(cur,"(r5-01:","(r5-XX:","riscv")
# 12 truncations / past-bound append
arms["trunc161"]="\n".join(cur.splitlines()[:161])+"\n"
arms["trunc140"]="\n".join(cur.splitlines()[:140])+"\n"
arms["past162"]=cur.rstrip("\n")+"\n- **New frontier bullet** — real solc/vyper-compiled bytecode untested.\n"

for name,txt in arms.items():
    d=os.path.join(LAB,"trees",name); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,"PROVINCE.md"),"w",encoding="utf-8").write(txt)
    for f in ("SKILL.md","SCORECARD.md"): shutil.copy(os.path.join(REPO,f),d)
    print(name, "PROVINCE lines", len(txt.splitlines()))
