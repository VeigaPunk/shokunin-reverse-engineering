#!/usr/bin/env python3
"""CR-2 independent worktree variant of SCORECARD recipe A (for overlay rehearsal).
Reads files from a scratch tree; self-tested identical to recipe A on the unmodified worktree."""
import json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
def get(rel):
    return (root / rel).read_text()
kl = root / 'corpus/knowledge'
files = {p.stem for p in kl.glob('*.md')}
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
        p = kl / name
        if not p.exists():
            valid = False
            continue
        count = len(p.read_text().splitlines())
        start, end = int(first or 1), int(last or first or 1)
        valid = valid and 1 <= start <= end <= count
    resolved += valid
print(json.dumps({'root': str(root), 'mapped': len(files & mapped), 'knowledge_files': len(files),
 'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
 'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))
