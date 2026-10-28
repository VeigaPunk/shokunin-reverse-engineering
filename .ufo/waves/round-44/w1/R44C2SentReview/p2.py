import re,subprocess
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'; B='c29360e3ba5381a5ab69e372d0d9577970f85018'
def has(h):
    r=subprocess.run(['git','-C',L,'cat-file','-t',h],capture_output=True,text=True)
    return r.stdout.strip()=='commit'
docs={'SCORECARD':'SCORECARD.md.base','SHONEN':'SHONEN.md.base','README':'README.md.base','LOG':'LOG.md.base','SKILL':'SKILL.md.base','PROVINCE':'PROVINCE.md.base'}
hexre=re.compile(r'(?<![0-9a-zA-Z/_.-])([0-9a-f]{8,40})(?![0-9a-zA-Z_])')
for n,f in docs.items():
    t=open(f).read()
    hs=set(h for h in hexre.findall(t) if re.search(r'[a-f]',h) and re.search(r'\d',h))
    bad=[];ok=0;nc=0
    for h in sorted(hs):
        r=subprocess.run(['git','-C',L,'cat-file','-t',h],capture_output=True,text=True)
        k=r.stdout.strip()
        if k=='commit': ok+=1
        elif k: nc+=1
        else: bad.append(h)
    print(n,'hex tokens',len(hs),'commits',ok,'other-objects',nc,'unresolved',len(bad),bad[:12])
