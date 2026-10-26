#!/usr/bin/env python3
"""report-content-gate -- a lane report must carry the PROTOCOL minimum-content items.

Round-39 routed defect R39-CL6 (first half): `/home/vgpnk/Projects/shokunin/.ufo/reports/
round-39/kaidoku.md` has no explicit "cross-domain evidence encountered" line. PROTOCOL.md:155
lists it as minimum content ("cross-domain evidence encountered, with the domain it belongs
to;"). Its only near-match is SHONEN box 4 ("No cross-domain bleed"), which asserts the
absence of an event, not the disposition of one encountered.

Rule: for each required item below, the report must carry a line matching its regex.
  1. cross-domain evidence (PROTOCOL.md:155)
  2. `## Sources & frontier` heading (PROTOCOL.md:157-158)
  3. `## SHONEN` heading (PROTOCOL.md:164)
Exit 0 all present; 1 findings; 2 usage. Red on the round-39 fleet report; green on the same
report with one cross-domain line added.
"""
import argparse
import re
import sys

REQUIRED = (
    ('cross-domain evidence line', re.compile(r'(?i)cross-domain\s+evidence')),
    ('## Sources & frontier heading', re.compile(r'(?m)^##\s+Sources\s*&\s*frontier\s*$')),
    ('## SHONEN heading', re.compile(r'(?m)^##\s+SHONEN\s*$')),
)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', required=True)
    args = ap.parse_args(argv)
    try:
        text = open(args.report, encoding='utf-8').read()
    except OSError as exc:
        print(f'USAGE {exc}', file=sys.stderr)
        return 2

    findings = []
    for name, rx in REQUIRED:
        hit = rx.search(text)
        print(f'{"PRESENT" if hit else "MISSING":<8} {name}')
        if not hit:
            findings.append(name)
    print(f'report={args.report} findings={len(findings)}')
    for f in findings:
        print(f'FINDING missing {f}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
