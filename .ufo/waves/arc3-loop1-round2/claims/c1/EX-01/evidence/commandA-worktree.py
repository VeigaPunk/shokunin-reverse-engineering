#!/usr/bin/env python3
"""Command A (recipe SCORECARD.md:88-124), worktree-adapted.

Identical counting logic to the canonical recipe; the only change is the
source: `git show REV:path` (immutable Git objects) is replaced by a direct
read of the worktree at ROOT, so the recipe can be run on an uncommitted
scratch tree. Fidelity is established by running it on the unpatched scratch
copy and reproducing the canonical numbers at HEAD (13 rules, 13/13, 82/82,
10.0/10.0).
"""
import json, pathlib, re, sys

root = pathlib.Path(sys.argv[1])

def get(path):
    return (root / path).read_text()

paths = sorted(str(p.relative_to(root)) for p in (root / "corpus/knowledge").glob("*.md"))
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
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
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except (FileNotFoundError, OSError):
            valid = False
    resolved += valid
print(json.dumps({'root': str(root), 'mapped': len(files & mapped),
 'knowledge_files': len(files), 'missing': sorted(files - mapped),
 'dangling': sorted(mapped - files), 'citation_resolved_rules': resolved,
 'rule_blocks': len(rules), 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))
