#!/usr/bin/env python3
"""depth-delta-gate -- a depth claim needs a score that can move.

SCORECARD.md:92-124 recipe A computes `depth_score = 10*resolved/rule_blocks` where a block
"resolves" if it cites at least one existing corpus/knowledge file at an in-range line. Once
every block resolves, the score is pinned at 10.00 and any added block resolves too: the
recipe cannot register a depth increment.

Round-39 claimed depth 17 -> 18 blocks, score 10.00 -> 10.00 (`w2/R39W2C2AxisFit.md` QUALITY 75
finding). Measured here: the round-40 base fa6a8a3f is already 18 blocks / depth 10.00, so
R40-C2's rule block 19 inherits the same non-measurement.

Rule: refuse a depth improvement whose base score is already 10.00 (zero headroom); otherwise
require a strictly positive delta.
Exit 0 measurable delta; 1 no headroom or no delta; 2 usage.
Red: lane --base a2f64e1d --tip 52b0eb29 (round 39) and --base fa6a8a3f (round 40).
Green: a fixture repo whose base leaves one rule unresolved and whose tip resolves it.
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
    return {
        'rule_blocks': len(rules),
        'resolved': resolved,
        'coverage_score': round(10 * len(files & mapped) / len(files), 2) if files else 0.0,
        'depth_score': round(10 * resolved / len(rules), 2) if rules else 0.0,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--base', required=True)
    ap.add_argument('--tip', required=True)
    args = ap.parse_args(argv)
    try:
        base = recipe(args.root, args.base)
        tip = recipe(args.root, args.tip)
    except (subprocess.CalledProcessError, IndexError) as exc:
        print(f'USAGE recipe failed: {exc}', file=sys.stderr)
        return 2
    delta = round(tip['depth_score'] - base['depth_score'], 2)
    print(f'base {args.base[:8]}: blocks={base["rule_blocks"]} resolved={base["resolved"]} '
          f'depth={base["depth_score"]}')
    print(f'tip  {args.tip[:8]}: blocks={tip["rule_blocks"]} resolved={tip["resolved"]} '
          f'depth={tip["depth_score"]}')
    print(f'delta={delta}')
    if base['depth_score'] >= 10.0:
        print('FINDING base depth_score is already 10.00: the recipe has no headroom, so added '
              'blocks resolve by construction; cite a measurement that can fail, not a block count')
        return 1
    if delta <= 0:
        print('FINDING no positive depth delta between base and tip')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
