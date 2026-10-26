import re, subprocess, os
ROOT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def show(rev,p):
    r=subprocess.run(['git','-C',ROOT,'show',f'{rev}:{p}'],capture_output=True)
    return r.stdout.decode() if r.returncode==0 else None
def obj(rev):
    r=subprocess.run(['git','-C',ROOT,'cat-file','-t',rev],capture_output=True,text=True)
    return r.stdout.strip() or 'ABSENT'
def cmdA(rev):
    p=subprocess.run(['git','-C',ROOT,'ls-tree','-r','--name-only',rev,'--','corpus/knowledge'],capture_output=True,text=True)
    if p.returncode: return None
    files={os.path.splitext(os.path.basename(x))[0] for x in p.stdout.splitlines() if x.endswith('.md')}
    rd=show(rev,'corpus/README.md') or ''
    sec=rd.split('## Coverage map\n',1)[1].split('\n## ',1)[0] if '## Coverage map\n' in rd else ''
    mapped=set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+',sec))
    sk=show(rev,'SKILL.md') or ''
    craft=sk.split('## Queue-drain craft ',1)[1].split('\n## ',1)[0] if '## Queue-drain craft ' in sk else ''
    rules=re.split(r'(?m)^- \*\*',craft)[1:]
    pat=re.compile(r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?')
    ok=0
    for rule in rules:
        refs=pat.findall(rule); good=bool(refs)
        for name,f,g in refs:
            t=show(rev,'corpus/knowledge/'+name)
            if t is None: good=False; continue
            a,b=int(f or 1),int(g or f or 1)
            if not (1<=a<=b<=len(t.splitlines())): good=False
        ok+=good
    return dict(files=len(files), mapped=len(files&mapped), rules=len(rules), resolved=ok)
for rev,label in [('cab59f221fe19726b5692bfa4d9a9679e96b8a73','cab59f22 r36 (row: 122/122)'),
                  ('c369242fee9f559f895e3f7956b1242076c7b1be','c369242f r31 (row: 116/116, 17/17)'),
                  ('ebe2cb4a','ebe2cb4a r26 (row: 109/109, 17/17)'),
                  ('3395b6d','3395b6d luna-r7 (row: 78/78)'),
                  ('7ef837a473ae65d924b9ea34e7748f722a6cd7d5','7ef837a4 (row: 107/107)'),
                  ('08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76','08c7a729 (depth recount)'),
                  ('3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22','3e99fbd6 round-14 work (SHONEN box1)'),
                  ('a79945c4','a79945c4 baseline')]:
    t=obj(rev)
    if t!='commit':
        print(f'{label}: object {rev} -> {t}'); continue
    full=subprocess.run(['git','-C',ROOT,'rev-parse',rev],capture_output=True,text=True).stdout.strip()
    print(f'{label}: {full[:12]} {cmdA(full)}')
