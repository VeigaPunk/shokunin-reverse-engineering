#!/usr/bin/env python3
"""R44-C1 documentation landing dry-run (pre-freeze, no repo writes).

Composes the three blocks onto scratch copies of PROVINCE.md and corpus/README.md, then
checks the composed text: the (a) heading + row, the (b) frontier note, the (c) map row, and
the command-A map invariant over the composed README (regex port, knowledge stems from git at
REV plus the new stem). Scratch only: reads lane files at --root, writes only under --work.

Exit 0 = composed docs satisfy every check; 1 = a check failed; 2 = could not evaluate.
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys

STEM_RE = r'2026-10-\d{2}-[a-z0-9-]+'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--blocks', required=True, help='dir with block-a/b/c + companion-readme-rows.md')
    ap.add_argument('--stem', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--json-out')
    args = ap.parse_args(argv)

    root, blocks = pathlib.Path(args.root), pathlib.Path(args.blocks)
    work = pathlib.Path(args.work)
    work.mkdir(parents=True, exist_ok=True)

    try:
        block_a = (blocks / 'block-a-province-round-44-core-row.md').read_text()
        block_b = (blocks / 'block-b-province-frontier-note.md').read_text()
        block_c = (blocks / 'block-c-readme-coverage-map-row.md').read_text().rstrip('\n')
        companions = (blocks / 'companion-readme-rows.md').read_text()
        province = (root / 'PROVINCE.md').read_text()
        readme = (root / 'corpus/README.md').read_text()
        listing = subprocess.run(['git', '-C', str(root), 'ls-tree', '-r', '--name-only',
                                  args.rev, '--', 'corpus/knowledge'],
                                 check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f'exit2: {exc}', file=sys.stderr)
        return 2

    stems = {pathlib.PurePosixPath(p).stem for p in listing.splitlines() if p.endswith('.md')}
    stems.add(args.stem)

    # companion rows, extracted from the fenced example lines
    comp = [ln for ln in companions.splitlines()
            if ln.startswith('- sasquatch') or ln.startswith('| `2026-10-28-')]
    comp_frontier = [ln for ln in comp if ln.startswith('- sasquatch')]
    comp_knowledge = [ln for ln in comp if ln.startswith('|')]
    if len(comp_frontier) != 1 or len(comp_knowledge) != 1:
        print('exit2: companion rows not parseable', file=sys.stderr)
        return 2

    # --- compose PROVINCE: block (a) then (b) at end of file
    rendered_province = province.rstrip('\n') + '\n\n' + block_a.rstrip('\n') + '\n\n' + \
        block_b.rstrip('\n') + '\n'

    # --- compose README by content anchors (line numbers shift; anchors do not)
    last_map_row = '| SquashFS triage v4 score (round 43) |'
    last_knowledge_row = '| `2026-10-27-sasquatch-release-matrix` |'
    last_frontier_row = '- Blocked-on-operator: IDA (`REA_IDA_MCP_CONFIG`), Hopper '
    lines = readme.splitlines()
    def index_of(prefix):
        hits = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
        if len(hits) != 1:
            raise SystemExit(f'exit2: anchor {prefix!r} has {len(hits)} hits')
        return hits[0]
    for prefix, new_lines in ((last_map_row, [block_c]),
                              (last_knowledge_row, comp_knowledge),
                              (last_frontier_row, comp_frontier)):
        i = index_of(prefix)
        lines[i + 1:i + 1] = new_lines
        lines.insert(i + 1 + len(new_lines), '')  # keep a blank separator before what follows
    rendered_readme = '\n'.join(lines) + '\n'

    (work / 'PROVINCE.rendered.md').write_text(rendered_province)
    (work / 'README.rendered.md').write_text(rendered_readme)

    checks = {}
    pa = rendered_province
    checks['province_heading_round44'] = pa.count('## Round-44 additions to Core') == 1
    row = [ln for ln in pa.splitlines() if ln.startswith('| `squashfs_v1`')]
    checks['province_row_names_both_handlers'] = len(row) == 1 and \
        'squashfs_v1' in row[0] and 'squashfs_v2' in row[0]
    checks['province_row_cites_entry'] = len(row) == 1 and args.stem in row[0]
    checks['province_row_names_four_carriers'] = len(row) == 1 and all(
        h in row[0] for h in ('V1LE', 'V1BE', 'V2LE', 'V2BE'))
    checks['province_frontier_note'] = pa.count('Round-44 frontier note, 2026-10-28') == 1
    checks['province_round42_note_intact'] = \
        'Still Frontier: SquashFS v1/v2, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, ' \
        'gzip v3 bodies, v4 Broadcom, LE AVM members, AVM kernels, nested sub-images below depth 1.' in pa

    rb = rendered_readme
    section = rb.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(STEM_RE, section))
    checks['readme_maps_new_stem'] = args.stem in mapped
    checks['readme_missing_empty'] = not (stems - mapped)
    checks['readme_dangling_empty'] = not (mapped - stems)
    checks['readme_mapped_equals_knowledge'] = len(stems & mapped) == len(stems)
    markers = rb.count('AFTER-DATA')
    checks['readme_after_data_markers_at_most_one'] = markers <= 1

    report = {'revision': args.rev, 'stem': args.stem,
              'knowledge_files': len(stems), 'mapped': len(stems & mapped),
              'missing': sorted(stems - mapped), 'dangling': sorted(mapped - stems),
              'map_rows': len([ln for ln in section.splitlines()
                               if ln.startswith('|') and not set(ln) <= set('|-: ')]),
              'after_data_markers': markers,
              'checks': checks,
              'ok': all(v is True for v in checks.values())}
    text = json.dumps(report, indent=1, sort_keys=True)
    print(text)
    if args.json_out:
        pathlib.Path(args.json_out).write_text(text + '\n')
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
