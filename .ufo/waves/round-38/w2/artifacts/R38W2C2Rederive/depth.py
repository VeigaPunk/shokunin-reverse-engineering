import re, subprocess
ROOT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'; REV='0fc6113376a156fddc3ec385386d71c3a4a9f690'
def show(p):
    r=subprocess.run(['git','-C',ROOT,'show',f'{REV}:{p}'],capture_output=True)
    return r.stdout.decode() if r.returncode==0 else None
sk=show('SKILL.md'); lines=sk.splitlines()
starts=[i for i,l in enumerate(lines) if l.startswith('## Queue-drain craft')]
print('craft heading lines:', [s+1 for s in starts])
print('craft heading text:', [lines[s][:70] for s in starts])
s=starts[0]; end=len(lines)
for i in range(s+1,len(lines)):
    if lines[i].startswith('## '): end=i; break
craft=lines[s+1:end]
last=max(i for i in range(s,end) if lines[i].strip())+1
print('craft range (heading..last nonblank):', s+1, last)
blocks=[l for l in craft if l.startswith('- **')]
print('rule blocks (^- \\*\\*):', len(blocks))
pat=re.compile(r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?')
ok=0; det=[]
# split into blocks preserving intervening lines
idxs=[i for i,l in enumerate(craft) if l.startswith('- **')]
for n,i in enumerate(idxs):
    j=idxs[n+1] if n+1<len(idxs) else len(craft)
    body='\n'.join(craft[i:j])
    refs=pat.findall(body)
    good=True
    for name,f,g in refs:
        t=show('corpus/knowledge/'+name)
        if t is None: good=False; det.append(('missing file',name)); continue
        a=int(f or 1); b=int(g or f or 1)
        if not (1<=a<=b<=len(t.splitlines())): good=False; det.append(('bad range',name,f,g,len(t.splitlines())))
    ok+=good
print('resolvable rule blocks:', ok, '/', len(blocks))
print('details:', det)
