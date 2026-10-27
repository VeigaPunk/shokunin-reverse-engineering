import subprocess, sys, hashlib
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def show(rev, path):
    return subprocess.check_output(['git','-C',LANE,'show',f'{rev}:{path}'], text=True)
def lines(rev, path):
    return show(rev,path).splitlines()

def find_marker(ls, marker):
    for i,l in enumerate(ls,1):
        if marker in l: return i
    return None

def table_region(ls, marker):
    """from marker line through end of first markdown table after it"""
    m = find_marker(ls, marker)
    if m is None: return None
    end = None
    for i in range(m, len(ls)):
        l = ls[i]
        if l.strip().startswith('|'):
            end = i+1
        elif end is not None and not l.strip().startswith('|'):
            break
    return (m, end)

def table_shape(ls, start, end):
    rows = [l for l in ls[start-1:end] if l.strip().startswith('|')]
    hdr = rows[0]
    cols = hdr.count('|')-1
    body = [r for r in rows[1:] if not set(r.replace('|','').replace('-','').replace(':','').strip())==set()]
    sep = [r for r in rows[1:] if set(r.replace('|','').replace('-','').replace(':','').strip())==set()]
    return cols, len(body), len(rows)

base='6b9e64fe7e0de202d9383baad5792fbfe039a743'
lsb = lines(base,'SKILL.md')
print("BASE SKILL.md total lines:", len(lsb))
print("BASE craft heading line:", find_marker(lsb,'## Queue-drain craft'))
for mk in ['<!-- sqfs-triage-table v4 -->','<!-- sqfs-triage-table v3 -->','<!-- sqfs-triage-table v2 -->','<!-- sqfs-triage-table v1 -->']:
    print(f"BASE marker {mk!r}:", find_marker(lsb,mk))

# v4 region at base vs d1681696
for rev in (base,'d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b'):
    ls = lines(rev,'SKILL.md')
    reg = table_region(ls,'<!-- sqfs-triage-table v4 -->')
    print(rev[:8], "v4 region:", reg)
    if reg:
        m,e = reg
        chunk = '\n'.join(ls[m-1:e])+'\n'
        print(rev[:8], "v4 region sha256:", hashlib.sha256(chunk.encode()).hexdigest()[:16], "bytes:", len(chunk))
        print(rev[:8], "v4 table shape (cols, body_rules, total_rows):", table_shape(ls,m,e))

# v3 region at e1c83313
for rev,mk in (('e1c83313f33a3d97edbd8fef402db2d06172fcdc','<!-- sqfs-triage-table v3 -->'),
               ('4d62ee5a86b4692a13f682b29ed7975e8d7d5326','<!-- sqfs-triage-table v2 -->'),
               ('52b0eb2907c704ed5f184c47b14c723208e5cbbc','<!-- sqfs-triage-table v1 -->')):
    ls = lines(rev,'SKILL.md')
    print(rev[:8], "craft heading:", find_marker(ls,'## Queue-drain craft'), "total lines:", len(ls))
    reg = table_region(ls,mk)
    print(rev[:8], mk, "region:", reg)
    # rule block extents: find the '- **' line at or before marker and the next '- **' or '## ' after table end
    if reg:
        m,e = reg
        blk_start = None
        for i in range(m-1,0,-1):
            if ls[i-1].startswith('- **'): blk_start=i; break
        blk_end = None
        for i in range(e, len(ls)):
            if ls[i].startswith('- **') or ls[i].startswith('## '): blk_end=i; break
        print(rev[:8], "rule block line range:", blk_start, "-", blk_end)
        # last non-blank line of craft section
        craft_end = None
        for i in range(len(ls),0,-1):
            if ls[i-1].startswith('## ') and i != find_marker(ls,'## Queue-drain craft'):
                pass
        # craft section: from heading to next '## '
        h = find_marker(ls,'## Queue-drain craft ')
        nxt = None
        for i in range(h, len(ls)):
            if ls[i].startswith('## '): nxt=i+1; break
        lastnb = None
        for i in range(nxt-2, h-1, -1):
            if ls[i].strip(): lastnb=i+1; break
        print(rev[:8], "craft section heading:", h, "next heading:", nxt, "last non-blank:", lastnb)
