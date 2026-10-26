#!/usr/bin/env python3
"""Independent-ish comparison of committed C1 L-carrier receipts vs a fresh REA run."""
import importlib.util
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r40/R40W2ReproL'
COUNTER = os.path.join(LANE, 'tools/round-40/c1-counter.py')

spec = importlib.util.spec_from_file_location('c1counter', COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def walk_diff(a, b, path='', out=None):
    if out is None:
        out = []
    if type(a) is not type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        out.append((path, 'type', type(a).__name__, type(b).__name__))
        return out
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append((path + '/' + k, 'missing_committed', None, '<present>'))
            elif k not in b:
                out.append((path + '/' + k, 'missing_fresh', '<present>', None))
            else:
                walk_diff(a[k], b[k], path + '/' + k, out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((path, 'len', len(a), len(b)))
        for i in range(min(len(a), len(b))):
            walk_diff(a[i], b[i], '%s[%d]' % (path, i), out)
    else:
        if a != b:
            out.append((path, 'value', a, b))
    return out


for cid in ('L1', 'L2'):
    print('=' * 70)
    print('CARRIER', cid)
    committed = json.load(open(os.path.join(LANE, 'corpus/evidence/round-40/c1', cid, 'after.json')))
    env = json.load(open(os.path.join(S, 'rea-%s/stdout.json' % cid)))
    fresh = env['data']

    pc = mod.projection(committed, 'plus-extractor')
    pf = mod.projection(fresh, 'plus-extractor')
    ok, keys, detail = mod.projection_diff(pc, pf, 'plus-extractor')
    print('projection(plus-extractor) equal:', ok, 'differing keys:', keys)
    if keys:
        print(json.dumps(detail, indent=1, sort_keys=True)[:4000])

    print('-- committed evidence_id:', committed.get('evidence_id'))
    print('-- fresh     evidence_id:', fresh.get('evidence_id'))

    d = walk_diff(committed, fresh)
    print('full-object differing paths: %d' % len(d))
    for row in d[:80]:
        p, kind = row[0], row[1]
        a, b = row[2], row[3]
        sa = json.dumps(a)[:120] if not isinstance(a, str) else a[:120]
        sb = json.dumps(b)[:120] if not isinstance(b, str) else b[:120]
        print('  %-60s %-18s %s  ->  %s' % (p[:60], kind, sa, sb))
    if len(d) > 80:
        print('  ... %d more' % (len(d) - 80))

    # normalized_result field-by-field headline numbers
    nr = fresh.get('normalized_result') or {}
    print('-- fresh nr: files=%s chunks=[%s] gaps=%s unpub=%s published_bytes=%s coverage=%s engine=%s' % (
        len(nr.get('files') or []),
        ','.join(sorted({(ch.get('handler') or '?') + ('!' if ch.get('extraction_failed') else '')
                         for ch in nr.get('chunks') or []})),
        len(nr.get('extraction_gaps') or []),
        len(nr.get('unpublished_entries') or []),
        nr.get('published_bytes'), nr.get('coverage'),
        (nr.get('engine') or {}).get('version')))
    cnr = (committed.get('normalized_result') or {})
    print('-- committed nr: files=%s gaps=%s unpub=%s published_bytes=%s coverage=%s' % (
        len(cnr.get('files') or []), len(cnr.get('extraction_gaps') or []),
        len(cnr.get('unpublished_entries') or []), cnr.get('published_bytes'),
        cnr.get('coverage')))
