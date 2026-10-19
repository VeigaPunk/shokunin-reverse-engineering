import json, pathlib, re, subprocess, sys
NEW='2026-10-19-arc3-r6-viair-dispatch-shape'
rule_path=sys.argv[1]
rule=pathlib.Path(rule_path).read_text()
pattern=r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
for rev in ('58c3db7','c625d5d'):
    def get(p): return subprocess.check_output(['git','show',f'{rev}:{p}'],text=True)
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',rev,'--','corpus/knowledge'],text=True).splitlines()
    files={pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')} | {NEW}
    section=get('corpus/README.md').split('## Coverage map\n',1)[1].split('\n## ',1)[0]
    mapped=set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+',section)) | {NEW}
    craft=get('SKILL.md').split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
    craft=craft.rstrip('\n')+'\n'+rule
    rules=re.split(r'(?m)^- \*\*',craft)[1:]
    resolved=0; bad=[]
    for r in rules:
        refs=re.findall(pattern,r); valid=bool(refs)
        for nm,first,last in refs:
            try:
                count=len(get('corpus/knowledge/'+nm).splitlines()); s,e=int(first or 1),int(last or first or 1)
                valid = valid and 1<=s<=e<=count
                if not (1<=s<=e<=count): bad.append((nm,s,e,count))
            except subprocess.CalledProcessError: valid=False; bad.append((nm,'MISSING'))
        resolved+=valid
    print(json.dumps({'rev':rev,'rule_file':rule_path,'rule_blocks':len(rules),'citation_resolved_rules':resolved,
      'depth_score':round(10*resolved/len(rules),2),'knowledge_files':len(files),'mapped':len(files&mapped),
      'missing':sorted(files-mapped),'dangling':sorted(mapped-files),'bad_refs':bad,
      'coverage_score':round(10*len(files&mapped)/len(files),2)},sort_keys=True))
