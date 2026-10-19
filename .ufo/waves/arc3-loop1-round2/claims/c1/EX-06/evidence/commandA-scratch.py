#!/usr/bin/env python3
"""Command A (SCORECARD.md Measurement recipes) translated to read a scratch
tree on disk instead of `git show REV:path`. Logic is otherwise byte-for-byte
the recipe:
  - corpus/knowledge file set  = *.md files under <tree>/corpus/knowledge
  - corpus/README.md coverage-map section  (split semantics identical)
  - SKILL.md queue-drain craft section     (split semantics identical)
Usage: commandA-scratch.py <tree-dir> <label>
"""
import json, pathlib, re, sys

tree = pathlib.Path(sys.argv[1])
label = sys.argv[2]

def get(path):
    return (tree / path).read_text()

paths = sorted(str(p.relative_to(tree)) for p in (tree / 'corpus/knowledge').rglob('*'))
files = {pathlib.PurePosixPath(p).stem for p in paths
         if p.endswith('.md') and (tree / p).is_file()}
section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
for rule in rules:
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        if not (tree / 'corpus/knowledge' / name).is_file():
            valid = False
            continue
        count = len(get('corpus/knowledge/' + name).splitlines())
        start, end = int(first or 1), int(last or first or 1)
        valid = valid and 1 <= start <= end <= count
    resolved += valid
print(json.dumps({'revision': label, 'mapped': len(files & mapped),
 'knowledge_files': len(files), 'missing': sorted(files - mapped),
 'dangling': sorted(mapped - files), 'citation_resolved_rules': resolved,
 'rule_blocks': len(rules), 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))
