import re,subprocess,json,os
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'; B='c29360e3ba5381a5ab69e372d0d9577970f85018'
sc=open('SCORECARD.md.base').read()
def ls_tree():
    return set(subprocess.check_output(['git','-C',L,'ls-tree','-r','--name-only',B]).decode().split('\n'))
T=ls_tree()
dirs=set()
for p in T:
    parts=p.split('/')
    for i in range(1,len(parts)): dirs.add('/'.join(parts[:i]))
def exists(p):
    p=p.rstrip('/')
    return p in T or p in dirs
# classes
lines=sc.split('\n')
# Capabilities rows (section and capability-addition subtables)
cap_rows=[]; in_cap=False
for i,l in enumerate(lines,1):
    if l.startswith('| Capability |'): in_cap=True; continue
    if in_cap:
        if l.startswith('|---'): continue
        if l.startswith('| '): cap_rows.append((i,l))
        else: in_cap=False
print('capability tables rows', len(cap_rows), [r[0] for r in cap_rows][:40])
# evidence pointer path tokens
tok=re.compile(r'`([^`\s]+)`')
miss=[];tot=0
for i,l in cap_rows:
    cells=l.split(' | ')
    ev=cells[-2] if len(cells)>=4 else ''
    for t in tok.findall(ev):
        if '/' in t and not t.startswith('http') and not t.startswith('<'):
            t2=t.split(':')[0]
            if re.match(r'^[\w./-]+$',t2):
                tot+=1
                if not exists(t2): miss.append((i,t2))
print('ev path tokens',tot,'missing',len(miss)); print(miss[:30])
