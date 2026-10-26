#!/usr/bin/env python3
"""check-domain-guard -- a triage table must carry the operation/provider guard its own prose states.

Round-39 routed defect R39-CL1. The base prose table (SKILL.md:1231-1243 at a2f64e1d) ends with
"`operation` != extract_firmware, or `provider.id` != unblob ... the receipt is not comparable ...
do not relabel". The executable table that replaced it has no such column, and no such guard:
the frozen interpreter labels a ghidra `analyze_function` envelope `no-squashfs-chunk`
(measured by `w2/R39W2C2AxisFit.md` C2; re-measured here), and the instrument registry row says
it "labels REA envelopes" with no precondition.

Rule: the table must expose `operation` and `provider` columns, and every row that can match a
squashfs envelope must pin them, so an out-of-domain envelope falls through to `unclassified`.

Usage:
  check-domain-guard.py --table T [--envelope E ...]
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
    ap.add_argument('--envelope', action='append', default=[])
    args = ap.parse_args(argv)

    try:
        header, rows = sqfs_rows.parse_table(args.table)
    except (OSError, SystemExit) as exc:
        print(f'USAGE {exc}', file=sys.stderr)
        return 2

    findings = []
    op_c = sqfs_rows.column(header, 'operation')
    prov_c = sqfs_rows.column(header, 'provider')
    if not op_c:
        findings.append('no `operation` column: an analyze_function envelope is still labelled')
    if not prov_c:
        findings.append('no `provider` column: a non-unblob envelope is still labelled')
    if op_c and prov_c:
        wild = [r.get(sqfs_rows.column(header, 'label'), '?') for r in rows
                if r.get(op_c, '*') == '*' or r.get(prov_c, '*') == '*']
        if wild:
            findings.append(f'{len(wild)} row(s) leave the domain as *: {", ".join(wild)}')

    for path in args.envelope:
        try:
            feat = sqfs_rows.features(sqfs_rows.envelope(path))
        except (OSError, ValueError) as exc:
            print(f'USAGE {exc}', file=sys.stderr)
            return 2
        label, rule, _cause = sqfs_rows.classify(header, rows, feat)
        in_domain = feat['operation'] in ('extract_firmware', 'extract-firmware') and feat['provider'] == 'unblob'
        print(f'{os.path.basename(path)}: operation={feat["operation"]} '
              f'provider={feat["provider"]} label={label} rule={rule}')
        if not in_domain and label != 'unclassified':
            findings.append(f'{os.path.basename(path)}: out-of-domain envelope labelled {label} '
                            f'by rule {rule}, expected unclassified')

    print(f'table={args.table} rows={len(rows)} findings={len(findings)}')
    for f in findings:
        print(f'FINDING {f}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
