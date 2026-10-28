#!/usr/bin/env python3
"""R44-C1 documentation gate: the corpus/README.md coverage-map invariant.

This reproduces, byte for byte, the map leg of ``SCORECARD.md`` command A (recipe A,
``SCORECARD.md:85-121``): the knowledge-file stems at REV are the set of
``corpus/knowledge/**.md`` stems; the mapped stems are
``re.findall(r'2026-10-\\d{2}-[a-z0-9-]+', <## Coverage map section>)``. There is no
literal "row count" comparison in command A: one row may name several stems, so the
invariant is set equality (``missing == []`` and ``dangling == []`` and
``mapped == knowledge_files``), and ``map_rows`` is reported for humans only.

Exit codes: 0 invariant holds, 1 invariant broken, 2 could-not-evaluate (bad usage or
unreadable git object). Read-only: git objects only, no worktree writes, no network.

Usage
-----
  check-map-invariant.py --root LANE --rev REV [--json-out OUT]
  check-map-invariant.py --root LANE --rev REV --simulate-row FILE --simulate-new-stem STEM
  # controls (each must exit 1):
  ... --simulate-row FILE --simulate-new-stem STEM --corrupt-stem
  ... --simulate-row FILE --simulate-new-stem STEM --placement after-knowledge
  ... without --simulate-row (knowledge file added, map row missing)
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

STEM = r'2026-10-\d{2}-[a-z0-9-]+'


def git_show(root, rev, path):
    return subprocess.run(['git', '-C', root, 'show', f'{rev}:{path}'],
                          check=True, capture_output=True, text=True).stdout


def knowledge_stems(root, rev):
    out = subprocess.run(['git', '-C', root, 'ls-tree', '-r', '--name-only', rev,
                          '--', 'corpus/knowledge'],
                         check=True, capture_output=True, text=True).stdout
    return {pathlib.PurePosixPath(p).stem for p in out.splitlines() if p.endswith('.md')}


def split_readme(text):
    head, rest = text.split('\n## Coverage map\n', 1)
    section, tail = rest.split('\n## ', 1)
    return head, section, tail


def map_rows(section):
    return [ln for ln in section.splitlines()
            if ln.startswith('|') and not set(ln) <= set('|-: ')]


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--simulate-row')
    ap.add_argument('--simulate-new-stem', action='append', default=[])
    ap.add_argument('--corrupt-stem', action='store_true',
                    help='control: split the new stem with an extra hyphen')
    ap.add_argument('--placement', choices=['map', 'after-knowledge'], default='map',
                    help='control: after-knowledge appends the row outside ## Coverage map')
    ap.add_argument('--json-out')
    args = ap.parse_args(argv)

    if (args.simulate_row or args.corrupt_stem or args.placement != 'map') and not args.simulate_row:
        print('exit2: simulation flags need --simulate-row', file=sys.stderr)
        return 2
    if args.simulate_row and not args.simulate_new_stem:
        print('exit2: --simulate-row needs --simulate-new-stem (a landing adds both)', file=sys.stderr)
        return 2

    try:
        stems = knowledge_stems(args.root, args.rev)
        readme = git_show(args.root, args.rev, 'corpus/README.md')
    except subprocess.CalledProcessError as exc:
        print(f'exit2: git object unreadable at {args.rev}: {exc}', file=sys.stderr)
        return 2

    head, section, tail = split_readme(readme)
    stems |= set(args.simulate_new_stem)
    if args.simulate_row:
        row_lines = [ln for ln in pathlib.Path(args.simulate_row).read_text().splitlines() if ln]
        if args.corrupt_stem:
            row_lines = [ln.replace(s, s.replace('-v1v2-', '-v1-v2-'))
                         for ln in row_lines for s in args.simulate_new_stem]
        stems |= set(args.simulate_new_stem)
        if args.placement == 'after-knowledge':
            readme = head + '\n## Coverage map\n' + section + '\n## ' + tail + \
                '\n' + '\n'.join(row_lines) + '\n'
        else:
            readme = head + '\n## Coverage map\n' + section.rstrip('\n') + '\n' + \
                '\n'.join(row_lines) + '\n\n## ' + tail
        head, section, tail = split_readme(readme)

    mapped = set(re.findall(STEM, section))
    report = {
        'revision': args.rev,
        'mode': 'simulate' if args.simulate_row else 'measure',
        'placement': args.placement,
        'corrupt_stem': args.corrupt_stem,
        'knowledge_files': len(stems),
        'mapped': len(stems & mapped),
        'map_stems': len(mapped),
        'map_rows': len(map_rows(section)),
        'missing': sorted(stems - mapped),
        'dangling': sorted(mapped - stems),
    }
    report['ok'] = not report['missing'] and not report['dangling'] \
        and report['mapped'] == report['knowledge_files']
    text = json.dumps(report, indent=1, sort_keys=True)
    print(text)
    if args.json_out:
        pathlib.Path(args.json_out).write_text(text + '\n')
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
