import re,sys,fnmatch,itertools
tree=set(open('tree.txt').read().split('\n'))
dirs=set()
for t in tree:
    p=t.split('/')
    for i in range(1,len(p)): dirs.add('/'.join(p[:i]))
def expand(s):
    m=re.search(r'\{([^{}]*)\}',s)
    if not m: return [s]
    out=[]
    for alt in m.group(1).split(','):
        out+=expand(s[:m.start()]+alt+s[m.end():])
    return out
def sections():
    S=open('SCORECARD.md').read().split('\n')
    yield 'SHONEN', open('SHONEN.md').read().split('\n'),1
    yield 'SCORECARD Owned axes', S[18:32],19
    yield 'SCORECARD Capabilities', S[614:635],615
for name,L,off in sections():
    for i,l in enumerate(L):
        for tok in re.findall(r'`([^`]+)`',l):
            t=tok.strip()
            # strip trailing :range
            m=re.match(r'^(.*?)(?::\d+(?:-\d+)?)?$',t)
            base=m.group(1)
            if not re.search(r'[\w]/[\w]|\.(md|py|json|sh|mjs|txt|tsv)$',base) or ' ' in base or base.startswith(('http','python3','bash','/usr','--','<')): continue
            for e in expand(base):
                if '*' in e:
                    ok=any(fnmatch.fnmatch(x,e) for x in tree)
                else:
                    ok=e in tree or e.rstrip('/') in dirs
                print(('OK  ' if ok else 'MISS'),name,off+i,e)
