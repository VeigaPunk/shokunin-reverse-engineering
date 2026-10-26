#!/usr/bin/env python3
"""R38W2ReproK4: compare the independent K4 re-run envelopes against the committed
round-38 C1 receipts and the round-37 oracle. Read-only; prints a diff report.

Usage: python3 compare.py
Paths are absolute on purpose (artifacts are committed outside the scratch dir).
"""
import json
import re

HERE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-38/w2/artifacts/R38W2ReproK4'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
AFTERDIR = f'{LANE}/corpus/evidence/round-38/c1/K4'
ORADIR = f'{LANE}/corpus/evidence/round-37/c1/K4'

SEM = ('handler', 'coverage', 'published_bytes', 'files', 'gaps', 'engine', 'chunks')


def scrub(o):
    """Canonicalize only identity/path noise: scratch+output paths, REA staging dir
    names, provider blob ids and the evidence id (a digest of the whole record)."""
    if isinstance(o, dict):
        return {k: scrub(v) for k, v in o.items() if k != 'evidence_id'}
    if isinstance(o, list):
        return [scrub(v) for v in o]
    if isinstance(o, str):
        o = re.sub(r'rea-firmware-[A-Za-z0-9]{5,8}', '$REA', o)
        o = re.sub(r'/fast/scratch/hyaku/kaidoku-r38/[^"\s]*', '$SCRATCH', o)
        o = re.sub(r'\b\d{5,}:\d+\b', '$BLOB', o)
        return o
    return o


def semantic(d):
    nr = d['normalized_result']
    return {
        'engine': {k: nr['engine'][k] for k in
                   ('name', 'version', 'executable_sha256', 'worker_count')},
        'selection': nr['selection'],
        'coverage': nr['coverage'],
        'published_bytes': nr['published_bytes'],
        'chunks': [{k: c.get(k) for k in ('handler', 'input_path', 'range',
                                         'root_file_range', 'encrypted',
                                         'extraction_failed')} for c in nr['chunks']],
        'files': sorted((f['relative_path'], f['sha256'], f['size']) for f in nr['files']),
        'gaps': sorted((g.get('kind'), g.get('relative_path'),
                        tuple(g.get('dependencies') or []), g.get('handler'))
                       for g in nr['extraction_gaps']),
        'diagnostics': sorted((d.get('stage'), tuple(d.get('missing_dependencies') or []))
                              for d in nr['diagnostics']),
        'unpublished_entries': nr['unpublished_entries'],
        'depth_limited_paths': nr['depth_limited_paths'],
        'derivations': sorted(d.get('child_path') for d in nr['derivations']),
        'continuations': sorted(c.get('id') for c in nr['extraction_continuations']),
    }


def main():
    diffs = 0
    for arm in ('before', 'after'):
        mine = json.load(open(f'{HERE}/env_{arm}.json'))
        com = json.load(open(f'{AFTERDIR}/{arm}.json'))
        a, b = semantic(mine), semantic(com)
        print(f'== {arm}: semantic payload ==')
        for k in a:
            if a[k] != b[k]:
                diffs += 1
                print(f'  DIFF {k}\n    mine: {json.dumps(a[k], sort_keys=True)}'
                      f'\n    committed: {json.dumps(b[k], sort_keys=True)}')
        print(f'  semantic diffs: {sum(1 for k in a if a[k] != b[k])}')
        full_a, full_b = scrub(mine), scrub(com)
        for d in (full_a, full_b):
            if d['subject']:
                d['subject'].pop('name', None)
                d['subject'].pop('local_path', None)
        top = [k for k in full_a if full_a[k] != full_b[k]]
        print(f'  full-envelope top-level diffs (paths/blobids/id canonicalized): {top}')
        if 'parameters' in top:
            pa, pb = full_a['parameters'], full_b['parameters']
            print(f'    parameters differing keys: '
                  f'{[k for k in pa if pa[k] != pb[k]]}')
        print()

    # after-arm files vs the frozen round-37 oracle
    ora = {}
    for line in open(f'{ORADIR}/oracle.tsv'):
        rel, sha, size = line.rstrip('\n').split('\t')
        ora[rel] = (sha, int(size))
    after = json.load(open(f'{HERE}/env_after.json'))['normalized_result']
    got = {f['relative_path'].rsplit('/', 1)[-1]: (f['sha256'], f['size'])
           for f in after['files']}
    print('== after-arm files vs round-37 oracle.tsv ==')
    print(f'  oracle rows: {len(ora)}  extracted: {len(got)}  sets equal: '
          f'{set(ora) == set(got)}')
    for rel in sorted(ora):
        print(f'  {rel}: oracle={ora[rel][0][:16]}…/{ora[rel][1]}B  '
              f'got={got.get(rel, ("MISSING",))[0][:16]}…  match={ora[rel] == got.get(rel)}')
    extra = sorted(set(got) - set(ora))
    print(f'  extra published files not in oracle: {extra}')
    print(f'\nTOTAL semantic diffs across both arms: {diffs}')


if __name__ == '__main__':
    main()
