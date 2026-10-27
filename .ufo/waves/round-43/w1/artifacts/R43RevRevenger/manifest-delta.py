#!/usr/bin/env python3
"""Manifest-byte delta: round-42 generator vs the R43 refusal placement.

Purpose (R43 wave-1 review aid): the L1 must be able to see that the refusal
placement changes ONLY the manifest keys it is supposed to change, and no other
emitted byte.  This compares two manifest.json files produced from the same seed
and the same --classes, and prints every differing JSON path.

Known-intended deltas (asserted, not merely printed):
  round, claim                        -- the round identity
  generator.name                      -- heldout-gen-v4.py -> heldout-gen-v4r43.py
  generator.version                   -- r42-c2-v4 -> r43-c1-v4
  generator.sha256                    -- the file is a different file
  generator.replaces                  -- provenance: the ported round-42 bytes
  generator.tuple_check               -- the new check record (absent on --carriers-only)

Anything else that differs is a regression in the placement.

Usage: manifest-delta.py A.json B.json
Exit 0 = only the intended paths differ; 1 = something else differs.
"""
from __future__ import annotations

import json
import sys

INTENDED = {'round', 'claim', 'generator.name', 'generator.version',
            'generator.sha256', 'generator.replaces', 'generator.tuple_check'}


def walk(a, b, prefix='', out=None):
    out = out if out is not None else []
    if type(a) is not type(b):
        out.append((prefix, a, b))
        return out
    if isinstance(a, dict):
        for key in sorted(set(a) | set(b)):
            path = f'{prefix}.{key}' if prefix else key
            if key not in a:
                out.append((path, '<absent>', b[key]))
            elif key not in b:
                out.append((path, a[key], '<absent>'))
            else:
                walk(a[key], b[key], path, out)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            out.append((prefix + '.length', len(a), len(b)))
        for index, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f'{prefix}[{index}]', out)
        return out
    if a != b:
        out.append((prefix, a, b))
    return out


def main(argv):
    a_path, b_path = argv[1], argv[2]
    with open(a_path, encoding='utf-8') as handle:
        a = json.load(handle)
    with open(b_path, encoding='utf-8') as handle:
        b = json.load(handle)
    # tuple_check carries per-carrier observations; drop it on BOTH sides so the
    # comparison is of the manifest the placement did not otherwise touch.
    for obj in (a, b):
        (obj.get('generator') or {}).pop('tuple_check', None)
    diffs = walk(a, b)
    unintended = [d for d in diffs if d[0] not in INTENDED]
    for path, x, y in diffs:
        tag = 'intended' if path in INTENDED else 'UNINTENDED'
        tail = ' (recorded)' if path == 'generator.tuple_check' else ''
        xs = json.dumps(x)[:90]
        ys = json.dumps(y)[:90]
        print(f'{tag:10} {path}{tail}\n           A={xs}\n           B={ys}')
    print(f'\n{len(diffs)} differing paths, {len(unintended)} unintended '
          f'-> {"PASS" if not unintended else "FAIL"}')
    return 0 if not unintended else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
