import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
NEW = '2026-10-19-arc3-r6-viair-dispatch-shape'
def get(p): return subprocess.check_output(['git','show',f'{rev}:{p}'],text=True)
paths = subprocess.check_output(['git','ls-tree','-r','--name-only',rev,'--','corpus/knowledge'],text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')} | {NEW}
section = get('corpus/README.md').split('## Coverage map\n',1)[1].split('\n## ',1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+',section)) | {NEW}
craft = get('SKILL.md').split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
print(json.dumps({'revision':rev,'knowledge_files':len(files),'mapped':len(files&mapped),
 'missing':sorted(files-mapped),'dangling':sorted(mapped-files),
 'coverage_score':round(10*len(files&mapped)/len(files),2),'rule_blocks':len(rules)},sort_keys=True))
