#!/usr/bin/env python3
"""axis-record-gate -- the living axis row must equal what the recipe measures at that revision.

Round-39 wave 2 found the landing commit did not move the row the lane scores (D1,
`w2/R39W2C1AxisFit.md`): at `6fdaf4f1` the `## Owned axes` coverage row still reads 126/126 while
the bytes hold 128 knowledge files, and the depth row still reads 17/17 while the craft section
holds 18 rule blocks. Both rows catch up only in the last wave-2 commit `2b0b6a29`.

Rule: at REV, recipe A (SCORECARD.md:92-124) is computed from git bytes; the first `N/N` pair in
the living `| coverage |` row must equal (mapped, knowledge files) and the first pair in the
living `| depth |` row must equal (resolved, rule blocks).

Usage: axis-record-gate.py --root LANE --rev REV
Exit 0 rows match; 1 drift; 2 usage.
Red: `6fdaf4f1` (coverage 126/126 vs 128/128; depth 17/17 vs 18/18). Green: `2b0b6a29`.
"""
import argparse
import pathlib
import re
import subprocess
import sys


def recipe(root, rev):
    def get(path):
        return subprocess.check_output(['git', '-C', root, 'show', f'{rev}:{path}'],
                                       text=True, stderr=subprocess.DEVNULL)
    paths = subprocess.check_output(['git', '-C', root, 'ls-tree', '-r', '--name-only', rev,
                                     '--', 'corpus/knowledge'], text=True).splitlines()
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
            except subprocess.CalledProcessError:
                valid = False
        resolved += valid
    return {'coverage': (len(files & mapped), len(files)),
            'depth': (resolved, len(rules))}


def living_pair(scorecard, axis):
    for line in scorecard.splitlines():
        if line.startswith(f'| {axis} |'):
            match = re.search(r'(\d+)/(\d+)', line)
            if match:
                return int(match.group(1)), int(match.group(2))
            return None
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    args = ap.parse_args(argv)
    try:
        computed = recipe(args.root, args.rev)
        scorecard = subprocess.check_output(
            ['git', '-C', args.root, 'show', f'{args.rev}:SCORECARD.md'],
            text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, IndexError) as exc:
        print(f'USAGE {exc}', file=sys.stderr)
        return 2

    findings = []
    for axis in ('coverage', 'depth'):
        row = living_pair(scorecard, axis)
        want = computed[axis]
        print(f'{axis}: row={row} computed={want} rev={args.rev[:8]}')
        if row is None:
            findings.append(f'{axis}: no N/N pair in the living row')
        elif row != want:
            findings.append(f'{axis}: row still reads {row[0]}/{row[1]} while the bytes measure '
                            f'{want[0]}/{want[1]}')
    print(f'findings={len(findings)}')
    for f in findings:
        print(f'FINDING {f}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
