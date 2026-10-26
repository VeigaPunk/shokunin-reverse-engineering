#!/usr/bin/env python3
"""Projection comparison used by seat R41W2C1Run.

Implements the frozen rerun projection of tools/round-41/c1-counter.py
(plus-extractor profile: derivations, engine, published_bytes, coverage added to
the core six fields). Usage:

  python3 project-compare.py AFTER_JSON ENVELOPE_JSON  # second is a raw REA envelope {ok,data,meta}

Prints True when both project equal (same bytes, different runs).
"""
import json
import sys


def load(path, key=None):
    d = json.load(open(path))
    return d[key] if key else d


def suffix(path):
    parts = path.split('/')
    for i, p in enumerate(parts):
        if p.endswith('_extract'):
            return '/'.join(parts[i + 1:])
    return path


def project(data):
    nr = data['normalized_result']
    files = sorted((suffix(f['relative_path']), f['sha256'], f['size'])
                   for f in nr.get('files', []))
    chunks = sorted((c['handler'], c.get('range', {}).get('offset'),
                     c.get('range', {}).get('length'), c.get('extraction_failed'))
                    for c in nr.get('chunks', []))
    gaps = sorted((g['kind'], suffix(g.get('relative_path') or ''),
                   tuple(sorted(g.get('dependencies') or [])))
                  for g in nr.get('extraction_gaps', []))
    unpub = sorted((u['kind'], suffix(u.get('relative_path') or ''))
                   for u in nr.get('unpublished_entries', []))
    diag = sorted(d['report']['__typename__'] for d in nr.get('diagnostics', []))
    return {
        'subject_sha256': data['subject']['digest']['sha256'],
        'files': files, 'chunks': chunks, 'gaps': gaps,
        'unpublished_entries': unpub, 'diagnostics': diag,
        'derivations': sorted((d['handler'], d['parent_path'], d['child_path'])
                              for d in nr.get('derivations', [])),
        'engine': nr.get('engine'),
        'published_bytes': nr.get('published_bytes'),
        'coverage': nr.get('coverage'),
    }


def main():
    h = project(load(sys.argv[1]))
    d = project(load(sys.argv[2], 'data'))
    print('equal:', h == d)
    if h != d:
        for k in h:
            if h[k] != d[k]:
                print('DIFF', k)
    print('files:', len(h['files']), 'gaps:', len(h['gaps']),
          'unpublished:', len(h['unpublished_entries']))
    print('subject_sha256:', h['subject_sha256'])
    print('engine:', h['engine'])
    print('published_bytes:', h['published_bytes'], 'coverage:', h['coverage'])
    return 0 if h == d else 1


if __name__ == '__main__':
    sys.exit(main())
