import re, subprocess, collections
ROOT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'; REV='0fc6113376a156fddc3ec385386d71c3a4a9f690'
import sys; sys.path.insert(0,'/fast/scratch/hyaku/kaidoku-r38/R38W2C2Rederive')
from indep import units, PTR, TOK, LANE
U=units(REV)
def exists(p):
    return subprocess.run(['git','-C',ROOT,'cat-file','-e',f'{REV}:{p}'],capture_output=True).returncode==0
skipped=collections.Counter(); examples={}
for k,pieces in U.items():
    for text,_ in pieces:
        for tok in TOK.findall(text):
            t=tok.strip()
            if PTR.match(t): continue           # PTR-accepted (checked elsewhere)
            looks = re.match(r'^([A-Za-z0-9_.][A-Za-z0-9_./+-]*(?::[0-9,\-]+)?)$', t)
            if not looks: continue
            path=t.split(':')[0].rstrip('/')
            if t.startswith(('/', '~')): continue
            if not LANE.match(path): continue
            skipped[t]+=1
            examples.setdefault(t,k)
print('PTR-skipped tokens that look like lane pointers:', len(skipped))
for t,c in sorted(skipped.items()):
    path=t.split(':')[0].rstrip('/')
    ok=exists(path)
    print(('  RESOLVES ' if ok else '  **DANGLING** '), repr(t), '<<', examples[t])
