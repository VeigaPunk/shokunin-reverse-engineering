import json,subprocess,re,pathlib,sys
def cmdA(rev):
    def get(path):
        return subprocess.check_output(['git','show',f'{rev}:{path}'],text=True,cwd='.')
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',rev,'--','corpus/knowledge'],text=True).splitlines()
    files={pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
    section=get('corpus/README.md').split('## Coverage map\n',1)[1].split('\n## ',1)[0]
    mapped=set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+',section))
    craft=get('SKILL.md').split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
    rules=re.split(r'(?m)^- \*\*',craft)[1:]
    pattern=r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved=0
    for rule in rules:
        refs=re.findall(pattern,rule); valid=bool(refs)
        for name,first,last in refs:
            try:
                count=len(get('corpus/knowledge/'+name).splitlines())
                start,end=int(first or 1),int(last or first or 1)
                valid=valid and 1<=start<=end<=count
            except subprocess.CalledProcessError: valid=False
        resolved+=valid
    skill=get('SKILL.md').splitlines()
    start=next(i for i,l in enumerate(skill,1) if l.startswith('## Queue-drain craft '))
    end=next(i for i in range(start+1,len(skill)+1) if i<=len(skill) and skill[i-1].startswith('## '))
    content_end=max(i for i in range(start,end) if skill[i-1].strip())
    print(json.dumps({'revision':rev,'mapped':len(files&mapped),'knowledge_files':len(files),
      'missing':sorted(files-mapped),'dangling':sorted(mapped-files),
      'citation_resolved_rules':resolved,'rule_blocks':len(rules),
      'coverage_score':round(10*len(files&mapped)/len(files),2),
      'depth_score':round(10*resolved/len(rules),2),
      'craft_span_heading':f'{start}-{end-1}','craft_span_content':f'{start}-{content_end}'},sort_keys=True))
for rev in sys.argv[1:]: cmdA(rev)
