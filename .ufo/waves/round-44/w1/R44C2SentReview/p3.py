import re,subprocess
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
kw=re.compile(r'(?i)\b(base|freeze|frozen at|controls?|measured revision|measured at|scores?|assimilation|landing|data|revision|at|commit|rev)\b[^`\n]{0,40}`([0-9a-f]{8,40})`')
for n,f in [('SCORECARD','SCORECARD.md.base'),('SHONEN','SHONEN.md.base'),('LOG','LOG.md.base'),('SKILL','SKILL.md.base')]:
    seen={}
    for ln,l in enumerate(open(f).read().split('\n'),1):
        for m in kw.finditer(l):
            h=m.group(2)
            if h not in seen:
                k=subprocess.run(['git','-C',L,'cat-file','-t',h],capture_output=True,text=True).stdout.strip()
                seen[h]=(k,ln,m.group(1))
    bad=[(h,v) for h,v in seen.items() if v[0]!='commit']
    print(n,len(seen),'unresolved/non-commit',len(bad)); 
    for b in bad[:15]: print('  ',b)
