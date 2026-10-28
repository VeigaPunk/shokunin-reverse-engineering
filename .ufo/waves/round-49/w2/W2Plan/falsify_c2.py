import importlib.util, json, sys
S='/fast/scratch/hyaku/kaidoku-r49/W2Plan'
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
R='29883d4ec35a31a8393c4ffb220888c44c0bb022'
spec=importlib.util.spec_from_file_location('c2', S+'/frz/tools/round-49/c2-mismatch.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
g=c2.Git(L)
reg=g.show(R,'corpus/SOURCES.md').decode()
def run(name, new_reg):
    over={'corpus/SOURCES.md': new_reg.encode()}
    res=c2.score(c2.Overlay(g,R,over),R)
    red=sorted(k for k,v in res.items() if v)
    print(json.dumps({'test':name,'red':red,'why':{k:v for k,v in res.items() if v}}, ensure_ascii=False))
lines=reg.split('\n')
# T1: second round-48 entry WITHOUT the late marker
i48=[i for i,l in enumerate(lines) if l.startswith('- 2026-10-28 round 48')][0]
dup=lines[i48].replace(' (late entry, written in round 49)','')
run('T1 extra non-late round-48 entry added', '\n'.join(lines[:i48+1]+[dup]+lines[i48+1:]))
# T2: S148 teaches gains a second EX_USAGE status
run('T2 S148 teaches adds "EX_USAGE = 2" (second status, no "is")',
    reg.replace('EX_USAGE is 64', 'EX_USAGE is 64 and EX_USAGE = 2 in this lane',1))
# T3 sanity: "EX_USAGE is 2" must be red
run('T3 sanity: S148 teaches says EX_USAGE is 2', reg.replace('EX_USAGE is 64','EX_USAGE is 2',1))
# T4 sanity: duplicate round-49 entry must be red
i49=[i for i,l in enumerate(lines) if l.startswith('- 2026-10-28 round 49')][0]
run('T4 sanity: duplicate round-49 entry', '\n'.join(lines[:i49+1]+[lines[i49]]+lines[i49+1:]))
