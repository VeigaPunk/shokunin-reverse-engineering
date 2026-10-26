#!/usr/bin/env python3
"""Test-only semantic comparator for R39-C1 after-receipts.

Compares two REA extract-firmware `data` objects on the payload the round-39
counter grades: the published-file set (relative path, sha256), the gap
multiset (kind, relative-path suffix, handler), the chunk handler multiset and
the subject/selection pins. Volatile fields (evidence_id, output_directory,
published file absolute paths, provider blob ids, raw_result) are reported but
never graded.

usage: compare-after.py A.json B.json [--json-out PATH]
exit: 0 identical payload, 1 payload differs, 2 unreadable input.
The JSON report labels A as "left" and B as "right".
"""
import argparse
import json
import sys


def load(path):
    with open(path, encoding='utf-8') as fh:
        env = json.load(fh)
    if isinstance(env, dict) and isinstance(env.get('data'), dict):
        env = env['data']
    if not isinstance(env, dict) or 'normalized_result' not in env:
        raise ValueError(f'{path}: not a REA evidence object')
    return env


def payload(env):
    nr = env.get('normalized_result') or {}
    chunks = [c for c in (nr.get('chunks') or []) if isinstance(c, dict)]
    files = sorted(
        ((f.get('relative_path') or '', f.get('sha256') or '')
         for f in (nr.get('files') or [])),
        key=lambda r: (r[0].encode(), r[1]))
    gaps = sorted(
        (json.dumps({'kind': g.get('kind'),
                     'relative_path': g.get('relative_path'),
                     'handler': g.get('handler'),
                     'dependencies': sorted(g.get('dependencies') or [])},
                    sort_keys=True)
         for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)))
    handlers = sorted(c.get('handler') or '' for c in chunks)
    return {
        'operation': env.get('operation'),
        'provider_id': (env.get('provider') or {}).get('id'),
        'provider_version': (env.get('provider') or {}).get('version'),
        'subject_sha256': ((env.get('subject') or {}).get('digest') or {}).get('sha256'),
        'selection_sha256': (nr.get('selection') or {}).get('sha256'),
        'coverage': nr.get('coverage'),
        'published_bytes': nr.get('published_bytes'),
        'handlers': handlers,
        'files': files,
        'file_count': len(files),
        'gaps': gaps,
        'gap_count': len(gaps),
        'chunk_failed': sorted(c.get('handler') or '' for c in chunks
                               if c.get('extraction_failed')),
        'unpublished_entries': sorted(
            (u.get('relative_path') or '') for u in (nr.get('unpublished_entries') or [])
            if isinstance(u, dict)),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('left')
    ap.add_argument('right')
    ap.add_argument('--json-out')
    a = ap.parse_args(argv)
    try:
        left, right = payload(load(a.left)), payload(load(a.right))
    except (OSError, ValueError) as e:
        print(f'compare-after: {e}', file=sys.stderr)
        return 2
    graded = ('operation', 'provider_id', 'provider_version', 'subject_sha256',
              'selection_sha256', 'handlers', 'files', 'gaps', 'chunk_failed')
    diff = {k: {'left': left[k], 'right': right[k]}
            for k in graded if left[k] != right[k]}
    report = {
        'left': a.left,
        'right': a.right,
        'graded_fields': list(graded),
        'ungraded_fields': ['coverage', 'published_bytes', 'unpublished_entries',
                            'evidence_id', 'output_directory', 'file absolute paths',
                            'provider blob ids', 'raw_result'],
        'equal': not diff,
        'diff': diff,
        'left_summary': {k: left[k] for k in
                         ('coverage', 'handlers', 'file_count', 'gap_count',
                          'published_bytes', 'unpublished_entries')},
        'right_summary': {k: right[k] for k in
                          ('coverage', 'handlers', 'file_count', 'gap_count',
                           'published_bytes', 'unpublished_entries')},
    }
    text = json.dumps(report, indent=2, sort_keys=True) + '\n'
    print(text, end='')
    if a.json_out:
        with open(a.json_out, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
    return 0 if report['equal'] else 1


if __name__ == '__main__':
    sys.exit(main())
