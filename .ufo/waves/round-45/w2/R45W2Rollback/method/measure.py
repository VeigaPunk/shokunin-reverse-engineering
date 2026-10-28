#!/usr/bin/env python3
"""Command A (SCORECARD.md ## Measurement recipes, verbatim logic) + per-block citation detail.

Usage: measure.py <rev>   (run with cwd = the clone)
Prints one JSON object: command A's own keys, plus per-block detail:
  idx, sha256 of the block text, refs (count), resolved (bool), unresolved list,
  marker presence.  The per-block part is what command A aggregates.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

rev = sys.argv[1]


def get(path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)


paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev,
                                 '--', 'corpus/knowledge'], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
blocks = []
for i, rule in enumerate(rules, 1):
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    bad = []
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            if not (1 <= start <= end <= count):
                valid = False
                bad.append(name + ':' + str(first or 1) + '-' + str(last or first or 1))
        except subprocess.CalledProcessError:
            valid = False
            bad.append(name)
    resolved += valid
    blocks.append({
        'idx': i,
        'head': rule.splitlines()[0][:48],
        'sha256': hashlib.sha256(rule.encode()).hexdigest()[:16],
        'refs': len(refs),
        'ref_names': sorted({n for n, _, _ in refs}),
        'resolved': bool(valid),
        'unresolved': bad,
        'marker': '<!-- freeze-integrity-table v1 -->' in rule,
    })
print(json.dumps({'revision': rev, 'mapped': len(files & mapped),
                  'knowledge_files': len(files), 'missing': sorted(files - mapped),
                  'dangling': sorted(mapped - files), 'citation_resolved_rules': resolved,
                  'rule_blocks': len(rules), 'coverage_score': round(10 * len(files & mapped) / len(files), 2),
                  'depth_score': round(10 * resolved / len(rules), 2),
                  'blocks': blocks}, sort_keys=True))
