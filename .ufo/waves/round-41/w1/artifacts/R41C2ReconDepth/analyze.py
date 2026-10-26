#!/usr/bin/env python3
"""R41C2ReconDepth -- tabulate and check the dev envelopes written by mkdev.py.

Reads summary.json, prints the report table, and asserts the invariants this
recon claims.  Exit 0 = every check held.
"""
from __future__ import annotations

import json
import os
import re
import sys

CARVED_UNKNOWN = re.compile(r'/\d+-\d+\.unknown$')


def main(argv):
    summary_path = argv[1] if len(argv) > 1 else 'summary.json'
    with open(summary_path, encoding='utf-8') as handle:
        summary = json.load(handle)
    cases = summary['cases']
    failures = []

    def check(cond, message):
        if not cond:
            failures.append(message)

    print('| case | d | H | G | D | BE | SR | P | depth-limited paths | inner image '
          'published | v2 label | draft-v3 label |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for case in cases:
        if 'features' not in case:
            failures.append('%s: no envelope' % case['id'])
            continue
        feat = case['features']
        inner = [f for f in case['published']
                 if os.path.basename(f['relative_path']) in
                 ('inner.sqsh', 'inner_a.sqsh', 'inner_b.sqsh')]
        oracle = dict((rel, sha) for rel, sha, _ in case['oracle_files'])
        for entry in inner:
            want = oracle.get(os.path.basename(entry['relative_path']))
            check(want is not None,
                  '%s: nested image %r absent from the oracle tree'
                  % (case['id'], entry['relative_path']))
            check(entry['sha256'] == want,
                  '%s: published nested image sha256 %s != oracle %s'
                  % (case['id'], entry['sha256'], want))
        check(case['rea_exit_code'] == 0,
              '%s: REA exit %s' % (case['id'], case['rea_exit_code']))
        check(case['ok'] is True, '%s: ok=%r' % (case['id'], case['ok']))
        check(case['digest_matches_carrier'],
              '%s: subject digest != carrier sha256' % case['id'])
        # every published file outside a depth-limited directory carries the
        # provider's own sha256 and analysis depth; every file inside one does not
        ceilings = [p[len('$output/'):] for p in case['depth_limited_paths'] or []]
        for entry in case['published']:
            under = any(entry['relative_path'] == c or
                        entry['relative_path'].startswith(c + '/')
                        for c in ceilings)
            if under:
                check(entry['reported_sha256'] is None,
                      '%s: file under the ceiling carries reported_sha256: %r'
                      % (case['id'], entry['relative_path']))
                check(entry['analysis_depth'] is None,
                      '%s: file under the ceiling carries analysis_depth: %r'
                      % (case['id'], entry['relative_path']))
            elif not CARVED_UNKNOWN.search(entry['relative_path']):
                # a carved unknown chunk is written by unblob but never reported
                # as a file task, so it carries no provider sha256 either
                check(entry['reported_sha256'] == entry['sha256'],
                      '%s: file outside the ceiling lacks the provider sha256: %r'
                      % (case['id'], entry['relative_path']))
        gap_kinds = sorted({g['kind'] for g in case['gaps'] or []})
        check(sorted(feat['G']) == gap_kinds,
              '%s: feature G %r != gap kinds %r'
              % (case['id'], feat['G'], gap_kinds))
        for gap in case['gaps'] or []:
            if gap['kind'] == 'depth-limited':
                check(gap['dependencies'] == [],
                      '%s: depth-limited gap carries dependencies %r'
                      % (case['id'], gap['dependencies']))
                check(gap['handler'] is None and gap['provider_id'] is None
                      and gap['range'] is None and gap['relative_path'] is None,
                      '%s: depth-limited gap carries a non-null locator'
                      % case['id'])
                check(gap['input_path'] in (case['depth_limited_paths'] or []),
                      '%s: depth-limited gap path not in depth_limited_paths'
                      % case['id'])
        print('| `%s` | %d | %s | %s | %s | %s | %s | %d | %s | %s | %s | %s |'
              % (case['id'], case['max_depth'],
                 ','.join(feat['H']) or '∅', ','.join(feat['G']) or '∅',
                 ','.join(feat['D']) or '∅', feat['BE'], feat['SR'], feat['P'],
                 ', '.join('`%s`' % p.replace('$output/', '')
                           for p in case['depth_limited_paths'] or []) or '∅',
                 'yes (%s)' % ','.join(e['relative_path'].rsplit('/', 1)[-1]
                                       for e in inner) if inner else 'n/a',
                 case['v2_label'], case['v3_precedence_label']))

    print()
    if failures:
        print('FAIL %d check(s):' % len(failures))
        for item in failures:
            print(' - ' + item)
        return 1
    print('OK: %d cases, every invariant held' % len(cases))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
