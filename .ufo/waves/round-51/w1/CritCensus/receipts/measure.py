import re,subprocess,json,sys,hashlib
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def git(rev,*a): return subprocess.run(["git","-C",L,*a],capture_output=True,text=True).stdout
def reg_at(rev):
    sk=git(rev,"show",f"{rev}:SKILL.md")
    i=sk.find("<!-- instrument-registry v2 -->"); j=sk.find("<!-- /instrument-registry -->")
    return set(re.findall(r"^\|\s*`(tools/[^`]+)`\s*\|",sk[i:j],re.M))
def present(rev,p): return subprocess.run(["git","-C",L,"cat-file","-e",f"{rev}:{p}"],capture_output=True).returncode==0
def ls(rev,pfx): return git(rev,"ls-tree","-r","--name-only",rev,"--",pfx).split()
out={}
for REV in ("1aa27369","f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab"):
    reg=reg_at(REV)
    c2=set(json.loads(git(REV,"show",f"{REV}:tools/round-48/census2.json"))["paths"])
    TOOL=re.compile(r"tools/round-(?:4[1-9]|5[01])/[A-Za-z0-9._/-]+\.(?:py|sh)")
    named=set()
    for n in range(41,52):
        b=git(REV,"show",f"{REV}:plans/round-{n}-claims.md")
        if b: named|=set(TOOL.findall(b))
    A={p for p in named if present(REV,p)}
    TOOL49=re.compile(r"tools/round-(?:4[1-9]|50)/[A-Za-z0-9._/-]+\.(?:py|sh)")
    namedB=set()
    for n in range(41,51):
        b=git(REV,"show",f"{REV}:plans/round-{n}-claims.md")
        if b: namedB|=set(TOOL49.findall(b))
    whole={p for p in ls(REV,"tools/round-49")+ls(REV,"tools/round-50") if p.endswith((".py",".sh")) and "/control-fixtures/" not in p+"/"}
    B={p for p in namedB if present(REV,p)}|whole
    allrows=set(re.findall(r"^\|\s*`(tools/[^`]+)`\s*\|",git(REV,"show",f"{REV}:SKILL.md"),re.M))
    out[REV]={"registry_marker_rows":len(reg),"census2_paths":len(c2),
      "comparator_census2_outside":len(reg-c2),
      "comparator_census2_outside_list":sorted(reg-c2),
      "comparator_ported_ruleA_outside":len(reg-A),"comparator_ported_ruleA_list":sorted(reg-A),
      "comparator_round50draft_ruleB_outside":len(reg-B),"comparator_round50draft_list":sorted(reg-B),
      "comparator_registry_derived_outside":0,
      "skill_all_tool_rows":len(allrows),"skill_rows_outside_marker_block":len(allrows-reg)}
print(json.dumps(out,indent=1))
