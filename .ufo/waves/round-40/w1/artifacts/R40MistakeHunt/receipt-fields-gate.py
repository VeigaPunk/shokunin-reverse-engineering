#!/usr/bin/env python3
"""receipt-fields-gate -- a score receipt must carry its own exit code; a wave ledger must
carry a seat status.

Round-39 routed defect R39-CL6: the cited `l1/scores/*.json` carry no exit-code field, so the
report's "exit 0" rests on prose (wave-2 rescore reports), not on the cited receipt; and both
wave ledgers (`r39-w1-results.json`, `r39-w2-results.json`) carry `status: null` for every seat
(43/43 and 39/39), so "dead seats: 0" is a report-level count with no ledger field behind it.

Rule A: every JSON under --scores that records a measurement (any of carriers_matched, matched,
        bindings) must hold an integer exit code in one of exit_code, exit, rc, returncode.
        A receipt keyed `unevaluable` must say why AND still record the exit code.
Rule B: every item of --ledgers' `results` list must carry a non-null `status` string.

Exit 0 clean; 1 findings; 2 usage. Red on the round-39 lane; green on an augmented fixture
(the same files with the missing fields added).
"""
import argparse
import glob
import json
import sys

EXIT_KEYS = ('exit_code', 'exit', 'rc', 'returncode')


def exit_code(obj):
    for key in EXIT_KEYS:
        val = obj.get(key)
        if isinstance(val, int) and not isinstance(val, bool):
            return val
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--scores', required=True, help='directory or glob of score receipts')
    ap.add_argument('--ledgers', nargs='*', default=[], help='wave result ledgers (JSON)')
    args = ap.parse_args(argv)

    patterns = [args.scores] if any(c in args.scores for c in '*?[') else [args.scores.rstrip('/') + '/*.json']
    score_paths = sorted({p for pat in patterns for p in glob.glob(pat)})
    if not score_paths:
        print(f'USAGE no score receipts matched {args.scores}', file=sys.stderr)
        return 2

    findings = []
    scored = 0
    for path in score_paths:
        with open(path, encoding='utf-8') as fh:
            obj = json.load(fh)
        if not any(k in obj for k in ('carriers_matched', 'matched', 'bindings')):
            continue
        scored += 1
        if exit_code(obj) is None:
            findings.append(f'{path}: measured receipt without exit code '
                            f'(keys tried {EXIT_KEYS})')

    seats = 0
    for path in args.ledgers:
        with open(path, encoding='utf-8') as fh:
            obj = json.load(fh)
        results = obj.get('results') if isinstance(obj, dict) else obj
        if not isinstance(results, list):
            findings.append(f'{path}: no results list')
            continue
        nulls = 0
        for item in results:
            if not isinstance(item, dict):
                findings.append(f'{path}: non-dict result item')
                continue
            seats += 1
            status = item.get('status')
            if not isinstance(status, str) or not status.strip():
                nulls += 1
        if nulls:
            findings.append(f'{path}: {nulls}/{len(results)} seats with null/empty status')

    print(f'scores measured={scored} ledgers={len(args.ledgers)} seats={seats} '
          f'findings={len(findings)}')
    for f in findings:
        print(f'FINDING {f}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
