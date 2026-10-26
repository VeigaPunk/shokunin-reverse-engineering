#!/usr/bin/env python3
"""check-mixed-symlinks -- an image holding both link kinds must not get the escaping-only action.

Round-39 routed defect R39-CL2. K5 (2 in-tree + 1 escaping link) and K6 (1 in-tree + 2 escaping)
are two of six round-39 Core carriers, and the frozen interpreter labels both
`escaping-symlink-removed` by row order (measured, `w2/R39W2C2AxisFit.md` C1). That row's action
says "expect the path to be absent; never materialise the link", while the same envelope carries
`unpublished-entry` gaps for the links that were KEPT — so the action contradicts its own gap
list for 2 of 6 promoted carriers.

Rule: for every envelope whose features are (unpublished-entry gap AND symlink-removed AND >0
files), the table must resolve it to a row whose label is `mixed-symlinks` (or whose cause names
both kinds). The check also requires such a row to exist at all.

Usage: check-mixed-symlinks.py --table T --envelope K5/after.json --envelope K6/after.json
Exit 0 pass; 1 findings; 2 usage. Red on SKILL.md; green on table-v2-proposed.md.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sqfs_rows  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--table', required=True)
    ap.add_argument('--envelope', action='append', required=True)
    args = ap.parse_args(argv)
    try:
        header, rows = sqfs_rows.parse_table(args.table)
    except (OSError, SystemExit) as exc:
        print(f'USAGE {exc}', file=sys.stderr)
        return 2

    findings = []
    labels = {r.get(sqfs_rows.column(header, 'label')) for r in rows}
    if 'mixed-symlinks' not in labels:
        findings.append('no `mixed-symlinks` row: a both-kinds envelope can only match the '
                        'escaping row, whose action contradicts its own gaps')

    for path in args.envelope:
        feat = sqfs_rows.features(sqfs_rows.envelope(path))
        both = ('unpublished-entry' in feat['G'] and feat['SR'] == 'yes' and feat['P'] > 0)
        label, rule, cause = sqfs_rows.classify(header, rows, feat)
        print(f'{os.path.basename(os.path.dirname(path))}/{os.path.basename(path)}: '
              f'G={sorted(feat["G"])} SR={feat["SR"]} P={feat["P"]} '
              f'both_kinds={both} label={label} rule={rule}')
        if both and label != 'mixed-symlinks':
            findings.append(f'{path}: both link kinds present but labelled {label} '
                            f'(rule {rule}); action={str(cause)[:80]!r}')

    print(f'table={args.table} findings={len(findings)}')
    for f in findings:
        print(f'FINDING {f}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
