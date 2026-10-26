#!/usr/bin/env python3
"""Restricted semantic projection of an REA 6.5.0 extract_firmware receipt (v2: + bounds/exit codes).

Run: python3 projection.py <receipt.json> [<receipt.json> ...]

Each receipt is an envelope ({"data": {...}}) or a bare record. Every path that
lives under the run's own extraction root is rewritten relative, and every
run-local identifier (blob/provider ids, report ids, evidence_id) is dropped.
Exit 0 and prints `INVARIANT` when all receipts project equal, exit 1 otherwise.
"""
import json, os, sys

def load(p):
    d = json.load(open(p, encoding='utf-8'))
    return d.get('data', d)

def rel(p, root):
    if not isinstance(p, str):
        return p
    return p[len(root):].lstrip('/') if root and p.startswith(root) else p

def project(ev):
    nr = ev['normalized_result']
    root = (nr.get('output_directory') or '') + '/firmware.bin_extract'
    gaps = []
    for g in nr.get('extraction_gaps') or []:
        item = dict(g)
        item.pop('provider_blob_id', None)
        if isinstance(item.get('path'), str):
            item['path'] = rel(item['path'], root)
        gaps.append(item)
    diags = sorted((d.get('report') or {}).get('__typename__') for d in nr.get('diagnostics') or [])
    return {
        'subject_sha256': ev['subject']['digest']['sha256'],
        'subject_format': ev['subject']['format'],
        'provider': [ev['provider']['id'], ev['provider']['version']],
        'operation': ev['operation'],
        'engine': [nr['engine']['name'], nr['engine']['version'], nr['engine']['executable_sha256']],
        'selection': [nr['selection']['offset'], nr['selection']['length'], nr['selection']['sha256']],
        'coverage': nr['coverage'],
        'published_bytes': nr['published_bytes'],
        'chunks': [[c.get('handler'), c.get('start_offset'), c.get('end_offset')] for c in nr['chunks']],
        'files': sorted([[rel(f['path'], root), f.get('sha256'), f.get('size')] for f in nr['files']]),
        'gaps': gaps,
        'unpublished': [rel(u, root) if isinstance(u, str) else u for u in nr.get('unpublished_entries') or []],
        'diagnostics': diags,
        'depth_limited': nr.get('depth_limited_paths') or [],
        'derivations_n': len(nr.get('derivations') or []),
        # v2 additions: the extraction bounds actually applied, paths reduced to the
        # subject basename, plus the child exit codes (never its stdout/args).
        'bounds': [os.path.basename(str(ev['parameters'].get('path') or '')),
                   ev['parameters'].get('max_depth'),
                   ev['parameters'].get('max_output_bytes'),
                   ev['parameters'].get('max_output_files')],
        'receipt_exit': [(ev.get('raw_result') or {}).get('execution', {}).get('exit_code'),
                         (ev.get('raw_result') or {}).get('execution', {}).get('signal'),
                         (ev.get('raw_result') or {}).get('version_execution', {}).get('exit_code')],
        'limitations_n': len(ev.get('limitations') or []),
    }

def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    projs = [(p, project(load(p))) for p in argv[1:]]
    canon = [json.dumps(p, sort_keys=True) for _, p in projs]
    for path, proj in projs:
        print('== %s' % path)
        print(json.dumps(proj, sort_keys=True, indent=1)[:4000])
    same = all(c == canon[0] for c in canon)
    print('\nRESULT: %s (%d receipts, %d leaves each)' % ('INVARIANT' if same else 'DIVERGENT',
          len(projs), len(json.dumps(projs[0][1], sort_keys=True).split(','))))
    return 0 if same else 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
