import re, subprocess, collections
ROOT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def show(rev,p):
    r=subprocess.run(['git','-C',ROOT,'show',f'{rev}:{p}'],capture_output=True)
    return r.stdout.decode() if r.returncode==0 else None
def sect(text,heading):
    lines=text.splitlines()
    i=lines.index(heading); out=[]
    for l in lines[i+1:]:
        if l.startswith('## '): break
        out.append(l)
    return out
for rev in ('77091b492cc53f8743bd0701b1e7d5e66123dd84','0fc6113376a156fddc3ec385386d71c3a4a9f690'):
    sc=show(rev,'SCORECARD.md'); pv=show(rev,'PROVINCE.md'); sh=show(rev,'SHONEN.md')
    print('=== rev',rev[:10])
    for heading,doc in (('## Owned axes',sc),('## Capabilities',sc),('## Core',pv),('## Frontier',pv)):
        lines=sect(doc,heading)
        cells=[]
        for l in lines:
            if l.lstrip().startswith('|'):
                c=l.strip().strip('|').split('|')[0].strip()
                if c and not re.match(r'^[-: ]+$',c): cells.append(c)
            elif heading=='## Frontier' and re.match(r'^- ',l):
                cells.append(l[2:60])
        d=[k for k,v in collections.Counter(cells).items() if v>1]
        print(f'  {heading}: rows={len(cells)} distinct={len(set(cells))} dup_keys={d}')
    boxes=[re.match(r'^- \[[ x~]\] (.*)$',l).group(1)[:50] for l in sh.splitlines() if re.match(r'^- \[[ x~]\] ',l)]
    print('  SHONEN boxes:',len(boxes),'dup:',[k for k,v in collections.Counter(boxes).items() if v>1])
# craft range at round-14 commit
def craft(rev):
    sk=show(rev,'SKILL.md'); lines=sk.splitlines()
    s=next(i for i,l in enumerate(lines) if l.startswith('## Queue-drain craft'))
    e=next((i for i in range(s+1,len(lines)) if lines[i].startswith('## ')), len(lines))
    last=max(i for i in range(s,e) if lines[i].strip())
    blocks=len([l for l in lines[s+1:e] if l.startswith('- **')])
    return (s+1,last+1,blocks)
for r in ('3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22','0fc6113376a156fddc3ec385386d71c3a4a9f690'):
    print('craft at',r[:10],craft(r))
