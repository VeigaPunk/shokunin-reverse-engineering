import json, re, subprocess, collections
ROOT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV='0fc6113376a156fddc3ec385386d71c3a4a9f690'
def show(p):
    r=subprocess.run(['git','-C',ROOT,'show',f'{REV}:{p}'],capture_output=True)
    return r.stdout.decode() if r.returncode==0 else None
# --- knowledge files
out=subprocess.run(['git','-C',ROOT,'ls-tree','-r','--name-only',REV,'--','corpus/knowledge'],capture_output=True,text=True).stdout.split()
mds=[x for x in out if x.endswith('.md')]
stems=[x.rsplit('/',1)[1][:-3] for x in mds]
print('knowledge .md files:', len(mds), 'distinct basenames:', len(set(stems)))
dup=[s for s,c in collections.Counter(stems).items() if c>1]
print('duplicate basenames:', dup)
print('non-md entries:', [x for x in out if not x.endswith('.md')][:10], len([x for x in out if not x.endswith('.md')]))
# --- README coverage map section(s)
rd=show('corpus/README.md')
heads=[i for i,l in enumerate(rd.splitlines()) if l.strip()=='## Coverage map']
print('Coverage map headings at lines:', [h+1 for h in heads])
lines=rd.splitlines()
start=heads[0]
sec=[]
for l in lines[start+1:]:
    if l.startswith('\n## ') or l.startswith('## '): break
    sec.append(l)
body='\n'.join(sec)
rows=[l for l in sec if l.strip().startswith('|')]
mapstems=re.findall(r'2026-\d{2}-\d{2}-[a-z0-9-]+', body)
print('map rows:', len(rows), 'stem occurrences:', len(mapstems), 'distinct:', len(set(mapstems)))
missing_files=sorted(set(mapstems)-set(stems))
print('map stems with NO knowledge file:', missing_files)
unmapped=sorted(set(stems)-set(mapstems))
print('knowledge files NOT in map:', unmapped)
print('intersection:', len(set(stems)&set(mapstems)))
print('duplicate map stems:', [s for s,c in collections.Counter(mapstems).items() if c>1])
# is every map row anchored by a file? check row-level
bad_rows=[r[:80] for r in rows if not re.search(r'2026-\d{2}-\d{2}-[a-z0-9-]+',r)]
print('map rows without a stem:', len(bad_rows), bad_rows[:3])
