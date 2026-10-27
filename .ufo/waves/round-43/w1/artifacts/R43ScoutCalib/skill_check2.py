import subprocess
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def lines(rev, path):
    return subprocess.check_output(['git','-C',LANE,'show',f'{rev}:{path}'], text=True).splitlines()
def find_marker(ls, marker):
    for i,l in enumerate(ls,1):
        if marker in l: return i
    return None
def block_range(ls, marker):
    m = find_marker(ls, marker)
    start=None
    for i in range(m-1,0,-1):
        if ls[i-1].startswith('- **'): start=i; break
    # table end
    end=None
    for i in range(m, len(ls)):
        if ls[i].strip().startswith('|'): end=i+1
        elif end is not None and not ls[i].strip().startswith('|'): break
    return start, end, m
def craft_info(ls):
    h = find_marker(ls,'## Queue-drain craft ')
    nxt=None
    for i in range(h, len(ls)):
        if ls[i].startswith('## '): nxt=i+1; break
    lastnb=None
    for i in range(nxt-2, h-1, -1):
        if ls[i].strip(): lastnb=i+1; break
    return h, nxt, lastnb
for rev,mk,label in (('4d62ee5a86b4692a13f682b29ed7975e8d7e5326','<!-- sqfs-triage-table v2 -->','block19/v2'),
                     ('52b0eb2907c704ed5f184c47b14c723208e5cbbc','<!-- sqfs-triage-table v1 -->','block18/v1')):
    ls=lines(rev,'SKILL.md')
    s,e,m=block_range(ls,mk)
    h,nxt,lastnb=craft_info(ls)
    print(rev[:8], label, "block_start,table_marker,table_end:", s, m, e, "craft heading/next/lastnb:", h, nxt, lastnb, "total:", len(ls))
# v3 at e1c83313 already verified; also verify v1 marker eight labels claim -> count labels in table
ls=lines('52b0eb2907c704ed5f184c47b14c723208e5cbbc','SKILL.md')
s,e,m=block_range(ls,'<!-- sqfs-triage-table v1 -->')
rows=[l for l in ls[m-1:e] if l.strip().startswith('|')]
print("v1 header:", rows[0][:200])
