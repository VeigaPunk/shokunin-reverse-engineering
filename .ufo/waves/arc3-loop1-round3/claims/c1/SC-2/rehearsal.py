#!/usr/bin/env python3
"""SC-2 rehearsal: command A in filesystem form over a scratch tree.
Reads a tree root (with corpus/README.md, corpus/knowledge/, SKILL.md) and
prints the same JSON keys as SCORECARD recipe A. Deviation from recipe A:
git objects are replaced by filesystem reads on a scratch copy (the lane repo
is never committed; the parent re-measures from real Git objects)."""
import json, pathlib, re, sys

root = pathlib.Path(sys.argv[1])
def get(rel):
    return (root / rel).read_text()

paths = [p for p in (root / 'corpus/knowledge').rglob('*.md')]
files = {p.stem for p in paths}
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
        f = root / 'corpus/knowledge' / name
        if not f.exists():
            valid = False
            continue
        count = len(f.read_text().splitlines())
        start, end = int(first or 1), int(last or first or 1)
        valid = valid and 1 <= start <= end <= count
    resolved += valid
print(json.dumps({'mapped': len(files & mapped), 'knowledge_files': len(files),
 'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
 'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))