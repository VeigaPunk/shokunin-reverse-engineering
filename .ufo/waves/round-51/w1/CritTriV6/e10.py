import re,subprocess,sys,json
LANE=sys.argv[1]
def show(p,rev='f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab'):
    r=subprocess.run(['git','-C',LANE,'show',f'{rev}:{p}'],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
def reg_rows(sk):
    body=sk.split("<!-- instrument-registry v2 -->",1)[1].split("<!-- /instrument-registry -->",1)[0]
    out=[]
    for line in body.splitlines():
        if re.match(r"^\|\s*`",line.strip()):
            cs=[c.strip() for c in line.strip().strip("|").split("|")]
            if len(cs)==7: out.append(cs[0].strip("` "))
    return out
sk=show('SKILL.md'); reg=set(reg_rows(sk))
TOOL=re.compile(r"tools/round-(?:4[1-9]|5[0-1])(?:-[a-z0-9]+)?/[A-Za-z0-9._/-]+\.(?:py|sh)")
def census(claims_files, tool_re):
    named={}
    for cf in claims_files:
        b=show(cf)
        if b is None: continue
        for m in tool_re.finditer(b): named.setdefault(m.group(0),[]).append(cf)
    return sorted(p for p in named if show(p) is not None), named
files_all=[f'plans/round-{n}-claims.md' for n in range(41,52)]+[f'plans/round-{n}-attempt2-claims.md' for n in range(41,52)]
files_noatt=[f'plans/round-{n}-claims.md' for n in range(41,52)]
for label,files in (('A: rounds 41..51, BOTH -claims.md and -attempt2-claims.md',files_all),
                    ('B: rounds 41..51, only -claims.md (attempt2 IGNORED)',files_noatt)):
    paths,named=census(files,TOOL)
    extra=sorted(reg-set(paths))
    print(f'--- variant {label}')
    print('    census3_paths',len(paths),' registry_rows',len(reg),' EXTRA(census_outside floor)',len(extra))
    for e in extra: print('       ',e,'| named_in:',named.get(e,'NOWHERE'))
print()
print('--- variant C: registry-derived census3 (census3 := registry rows) -> census_outside is 0 by construction')
print('    registry_rows',len(reg))
print()
print('--- round-51 tools named in plans/round-51-claims.md (the {py,sh} census regex matches)')
b=show('plans/round-51-claims.md')
print('   ',sorted(set(m.group(0) for m in TOOL.finditer(b))))
print('--- round-50 attempt2 named:')
b=show('plans/round-50-attempt2-claims.md')
print('   ',sorted(set(m.group(0) for m in TOOL.finditer(b))))
