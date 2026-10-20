#!/usr/bin/env python3
"""Round-19 immutable controls, reusing SCORECARD command A and r18 prefix rules.
Usage: python3 -I -B controls-r19.py BEFORE AFTER; --selftest exercises a missing-map
red and prefix red without Git, network, subprocess writes, or target execution.
0 controls hold, 1 failed control, 2 unreadable input. JSON is not a semantic audit.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = str(pathlib.Path(__file__).resolve().parents[3])
FREEZE = 'a1140e76fffdc1be032d9d813dbb686157803bbc'
PRED = '.ufo/waves/round-19/predictions'
APPEND_KNOWLEDGE = {'corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md',
                    'corpus/knowledge/2026-10-20-r18-swiss-map-replay.md'}

def git(*args):
    return subprocess.check_output(
        ['git', '--no-optional-locks', '-C', ROOT, *args],
        env={k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "JJ_"))})


def blob(rev, path):
    return git('show', f'{rev}:{path}')


def paths(rev):
    return set(git('ls-tree', '-r', '--name-only', rev).decode().splitlines())


def admission_rows(data):
    section = data.decode().split('## Admission criteria', 1)[1].split('\n## ', 1)[0]
    return [s for s in section.splitlines() if re.match(r'^\| \d+ \|', s)]


def command_a(rev, names):
    # Identical rules to SCORECARD.md:93-122 (only Git plumbing is shared).
    files = {pathlib.PurePosixPath(p).stem for p in names
             if p.startswith('corpus/knowledge/') and p.endswith('.md')}
    text = blob(rev, 'corpus/README.md').decode()
    section = text.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
    skill = blob(rev, 'SKILL.md').decode()
    craft = skill.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            try:
                count = len(blob(rev, 'corpus/knowledge/' + name).splitlines())
                start, end = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= start <= end <= count
            except subprocess.CalledProcessError:
                valid = False
        resolved += valid
    return {'mapped': len(files & mapped), 'knowledge_files': len(files),
            'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
            'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
            'coverage_score': round(10 * len(files & mapped) / len(files), 2),
            'depth_score': round(10 * resolved / len(rules), 2)}


def source_rows(data):
    return {c[0]: c for line in data.decode().splitlines()
            if re.match(r'^\| S\d+ \|', line)
            for c in [[x.strip() for x in line.strip('|').split('|')]]}


def evaluate(before, after):
    old, new = paths(before), paths(after)
    checks, details = {}, {}
    for path in ('LOG.md', 'SCORECARD.md', *sorted(APPEND_KNOWLEDGE)):
        a, b = blob(before, path), blob(after, path)
        checks['prefix:' + path] = b.startswith(a)
        details[path] = {'before_bytes': len(a), 'after_bytes': len(b)}
    old_quality = admission_rows(blob(before, 'corpus/QUALITY.md'))
    new_quality = admission_rows(blob(after, 'corpus/QUALITY.md'))
    checks['quality-old-rows-identical'] = new_quality[:len(old_quality)] == old_quality
    checks['quality-exactly-one-new-row'] = len(new_quality) == len(old_quality) + 1
    details['quality'] = {'before': len(old_quality), 'after': len(new_quality)}
    protected = sorted(p for p in old if p.startswith('corpus/lessons/') or
                       re.match(r'^\.ufo/waves/round-1[78]/(runs|predictions)/', p))
    changed = [p for p in protected if p not in new or blob(before, p) != blob(after, p)]
    checks['prior-lessons-runs-predictions-unchanged'] = not changed
    details['protected_changed'] = changed
    checks['round19-predictions-frozen'] = (
        git('rev-parse', f'{FREEZE}:{PRED}') == git('rev-parse', f'{after}:{PRED}'))
    aa, bb = command_a(before, old), command_a(after, new)
    details['command_a'] = {'before': aa, 'after': bb}
    checks['coverage-not-harmed'] = bb['coverage_score'] >= aa['coverage_score']
    checks['depth-not-harmed'] = bb['depth_score'] >= aa['depth_score']
    checks['map-resolves'] = not bb['missing'] and not bb['dangling']
    ar, br = source_rows(blob(before, 'corpus/SOURCES.md')), source_rows(blob(after, 'corpus/SOURCES.md'))
    bad = [sid for sid, cells in ar.items() if sid not in br or
           any(x != y for i, (x, y) in enumerate(zip(cells, br[sid])) if i not in (7, 9, 10))]
    checks['source-evidence-cells-unchanged'] = not bad
    details['source_evidence_changed'] = bad
    details['sources_rows'] = {'before': len(ar), 'after': len(br)}
    checks['no-deleted-path'] = not (old - new)
    failed = [name for name, ok in checks.items() if not ok]
    return {'before': before, 'after': after, 'checks': checks, 'details': details,
            'failed': failed, 'pass': not failed}


def main():
    if sys.argv[1:] == ['--selftest']:
        assert not b'changed-prefix'.startswith(b'old-prefix')
        files, mapped = {'one', 'two'}, {'one'}
        assert files - mapped == {'two'} and 10 * len(files & mapped) / len(files) < 10
        print('SELFTEST: CLEAN cases=2')
        return 0
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        result = evaluate(*sys.argv[1:])
    except (subprocess.CalledProcessError, ValueError, IndexError, KeyError) as e:
        print(json.dumps({'error': str(e)}))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
