#!/usr/bin/env python3
"""features.py -- derive the round-41/42 REA envelope feature tuple from a
rea-agents 6.5.0 `extract-firmware --format json --full-output` receipt.

Feature definitions are the round-41 frozen text (plans/round-41-claims.md:109-115):

  OP = normalized_result.operation            (operation at the envelope top level)
  PR = provider.id
  H  = set(chunks[].handler) | set(extraction_gaps[].handler), nulls dropped
  G  = set(extraction_gaps[].kind)
  D  = union of extraction_gaps[].dependencies (exact names)
  BE = 'yes' if a recorded diagnostics[].report.command carries the token '-be',
       'no' if argvs are recorded and none does, 'n/a' if none is recorded
  SR = 'yes' iff a MaliciousSymlinkRemoved report is in diagnostics
  P  = len(files)
  F  = the SquashFS handler names in H (prefix 'squashfs_'), the round-42 addition

Also derived, because the round-42 C1 predicate needs them:
  roots      = child_path of every derivations[] edge whose handler is a
               squashfs_v3* handler, `$output/` stripped once, longest first
  carve      = (chunks[].range.offset, .length, extraction_failed) of every
               squashfs_v3* chunk
  unknown    = any chunk with handler == null

Reads receipts only; writes nothing.  Usage:
  features.py RECEIPT.json [RECEIPT.json ...]
"""
import json
import re
import sys

V3_PREFIX = 'squashfs_v3_'
V3_EXACT = 'squashfs_v3'
BE_TOKEN = re.compile(r'(?:^|\s)-be(?:\s|$)')


def strip_output(path):
    if not isinstance(path, str):
        return path
    return path[len('$output/'):] if path.startswith('$output/') else path


def is_v3(handler):
    if not isinstance(handler, str):
        return False
    return handler == V3_EXACT or handler.startswith(V3_PREFIX)


def features(doc):
    data = doc.get('data', doc)
    nr = data.get('normalized_result') or {}
    chunks = nr.get('chunks') or []
    gaps = nr.get('extraction_gaps') or []
    files = nr.get('files') or []
    diags = nr.get('diagnostics') or []
    deriv = nr.get('derivations') or []

    H = {c.get('handler') for c in chunks if c.get('handler')}
    H |= {g.get('handler') for g in gaps if g.get('handler')}
    G = {g.get('kind') for g in gaps}
    D = set()
    for g in gaps:
        D |= set(g.get('dependencies') or [])
    cmds = [d['report'].get('command') for d in diags
            if isinstance(d.get('report'), dict) and d['report'].get('command')]
    if not cmds:
        BE = 'n/a'
    elif any(BE_TOKEN.search(c) for c in cmds):
        BE = 'yes'
    else:
        BE = 'no'
    SR = 'yes' if any(
        isinstance(d.get('report'), dict)
        and d['report'].get('__typename__') == 'MaliciousSymlinkRemoved'
        for d in diags) else 'no'
    roots = sorted({strip_output(d.get('child_path')) for d in deriv
                    if is_v3(d.get('handler')) and d.get('child_path')},
                   key=lambda r: (-len(r), r))
    carve = [(c['range']['offset'], c['range']['length'], c.get('extraction_failed'))
             for c in chunks if is_v3(c.get('handler'))]
    return {
        'OP': data.get('operation'),
        'PR': (data.get('provider') or {}).get('id'),
        'H': sorted(H),
        'G': sorted(G),
        'D': sorted(D),
        'BE': BE,
        'SR': SR,
        'P': len(files),
        'F': sorted(h for h in H if h.startswith('squashfs_')),
        'unpublished': len(nr.get('unpublished_entries') or []),
        'unknown_handler_chunks': sum(1 for c in chunks if c.get('handler') is None),
        'v3_roots': roots,
        'v3_carve': carve,
        'coverage': nr.get('coverage'),
        'published_bytes': nr.get('published_bytes'),
    }


if __name__ == '__main__':
    rows = []
    for path in sys.argv[1:]:
        with open(path) as fh:
            rows.append({'receipt': path, **features(json.load(fh))})
    json.dump(rows, sys.stdout, indent=1, sort_keys=True)
    print()
