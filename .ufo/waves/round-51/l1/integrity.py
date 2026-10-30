#!/usr/bin/env python3
"""Read-only structural counts, not a verdict on either R51 claim."""
import argparse
import collections
import difflib
import hashlib
import json
import pathlib
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', required=True)
parser.add_argument('--base', required=True)
parser.add_argument('--rev', required=True)
args = parser.parse_args()


def get(rev, path):
    return subprocess.check_output(['git', '-C', args.root, 'show', f'{rev}:{path}'], text=True)


def paths(rev, path):
    return subprocess.check_output(['git', '-C', args.root, 'ls-tree', '-r', '--name-only', rev, '--', path], text=True).splitlines()


def measure(rev):
    files = {pathlib.PurePosixPath(p).stem for p in paths(rev, 'corpus/knowledge') if p.endswith('.md')}
    section = get(rev, 'corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
    skill = get(rev, 'SKILL.md')
    craft = skill.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    resolved = 0
    pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            try:
                count = len(get(rev, 'corpus/knowledge/' + name).splitlines())
                start, end = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= start <= end <= count
            except subprocess.CalledProcessError:
                valid = False
        resolved += bool(valid)
    rows = []
    for line in get(rev, 'corpus/SOURCES.md').splitlines():
        if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
            rows.append([cell.strip() for cell in line.strip().strip('|').split('|')])
    return {'revision': rev, 'knowledge_files': len(files), 'mapped': len(files & mapped),
            'missing': sorted(files-mapped), 'dangling': sorted(mapped-files),
            'rule_blocks': len(rules), 'citation_resolved_rules': resolved,
            'sources_rows': len(rows), 'sources_tiers': dict(collections.Counter(row[3] for row in rows)),
            'sources_statuses': dict(collections.Counter(row[7] for row in rows)),
            'R51_core_heading': '## Round-51 additions to Core' in get(rev, 'PROVINCE.md'),
            'R51_data_files': len(paths(rev, 'corpus/evidence/round-51/c1')),
            'R51_v6_landed': 'tools/round-51/sqfs-triage-v6.py' in paths(rev, 'tools/round-51')}

old_registry = get(args.base, 'corpus/SOURCES.md')
new_registry = get(args.rev, 'corpus/SOURCES.md')
delta = list(difflib.ndiff(old_registry.splitlines(), new_registry.splitlines()))
old_log, new_log = get(args.base, 'LOG.md'), get(args.rev, 'LOG.md')
result = {'base': measure(args.base), 'after': measure(args.rev),
          'registry_deleted_lines': sum(line.startswith('- ') for line in delta),
          'registry_added_lines': sum(line.startswith('+ ') for line in delta),
          'LOG_append_only': new_log.startswith(old_log),
          'PROVINCE_byte_identical': get(args.base, 'PROVINCE.md') == get(args.rev, 'PROVINCE.md'),
          'claim_targets': {'R51-C1': 'unverified (not a fresh 4/4 measurement)',
                            'R51-C2': 'unverified (not a v6/executability measurement)'}}
print(json.dumps(result, indent=2, sort_keys=True))
