import re,subprocess,sys
R=sys.argv[1]; src=sys.argv[2]; label=sys.argv[3]
lines=open(src,encoding='utf-8').read().split('\n')
ls=set(subprocess.run(['git','ls-tree','-r','--name-only',R],capture_output=True,text=True).stdout.split('\n'))
pat=re.compile(r'`([^`]+)`')
for i,l in enumerate(lines,1):
    for m in pat.finditer(l):
        t=m.group(1)
        if '/' in t and not t.startswith('http') and ' ' not in t and not t.startswith('2026') and not t.endswith('/'):
            c=t.rstrip('.,')
            if c.startswith('corpus/') or c.startswith('.ufo/') or c.startswith('tools/') or c.startswith('plans/') or c.startswith('LOG') or c.startswith('SCORECARD'):
                # glob-ish or prefix-ish tokens
                hit = c in ls
                if not hit and ('*' in c or '{' in c or '<' in c or '…' in c): continue
                if not hit:
                    print(f"{label}:{i}\tMISSING\t{c}")
                else:
                    print(f"{label}:{i}\tok\t{c}")
