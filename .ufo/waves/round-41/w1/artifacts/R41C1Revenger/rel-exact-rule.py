#!/usr/bin/env python3
"""R41C1Revenger: demonstrate the exact receipt-path -> oracle-relative mapping.

Three matchers are compared on live REA 6.5.0 receipts:

  split     rel = path.split('_extract/', 1)[1]        (the naive rule in the seat brief)
  suffix    rel = first `*_extract` path segment dropped (tools/round-40/c1-counter.py
            `rel_suffix`, c1-counter.py:746-762)
  exact     rel = path with the receipt's own chunk extract root removed
            (root taken from normalized_result.derivations, never from text search)

and the oracle-side comparison is done two ways:

  exact-only   receipt rel == oracle rel  (required by the round-41 P41-C1 wording)
  suffix       `same_rel` of tools/round-40/c1-counter.py:606-607
               (candidate == rel or candidate.endswith('/' + rel)) -- R40-CL1

Usage: rel-exact-rule.py RECEIPT_JSON ROOT_ORACLE_TSV [--root-relative-to ROOT_PATH]

The oracle TSV has rows: kind<TAB>rel<TAB>sha256<TAB>size   (kind in file|symlink).
Exit 0 when the exact matcher reproduces the oracle exactly, 1 otherwise (a
demonstration failure of a naive matcher alone never changes the exit status;
it is reported, not scored).
"""
import hashlib
import json
import os
import sys

OUTPUT_PREFIX = '$output/'


def strip_output(p):
    if not isinstance(p, str):
        return None
    while p.startswith(OUTPUT_PREFIX):
        p = p[len(OUTPUT_PREFIX):]
    return p


def chunk_roots(nr):
    """Every chunk extract root the receipt itself names, longest first.

    A derivation edge whose handler is a filesystem handler and whose parent is
    the selected input is the chunk's extract root; edges from a published
    nested file are nested roots. `$input` itself is never a root.
    """
    roots = []
    for d in nr.get('derivations') or []:
        child = strip_output(d.get('child_path'))
        parent = strip_output(d.get('parent_path'))
        if not child or child == '$input':
            continue
        if d.get('handler') and str(d.get('handler')).startswith('squashfs_v4'):
            roots.append((child, parent, d.get('handler')))
    roots.sort(key=lambda r: (-len(r[0]), r[0]))
    return roots


def rule_exact(path, root):
    p = strip_output(path)
    if p is None or not root:
        return None, 'no-root'
    if p == root:
        return '', 'root-itself'
    prefix = root + '/'
    if p.startswith(prefix):
        return p[len(prefix):], 'under-root'
    return None, 'outside-root'


def rule_split(path):
    p = strip_output(path)
    if p is None:
        return None
    if '_extract/' in p:
        return p.split('_extract/', 1)[1]
    return p


def rule_suffix(path):
    """Copy of tools/round-40/c1-counter.py rel_suffix (lines 746-762)."""
    p = strip_output(path)
    if p is None:
        return None
    parts = [x for x in p.split('/') if x not in ('', '.')]
    for i, part in enumerate(parts):
        if part.endswith('_extract') and i + 1 < len(parts):
            return '/'.join(parts[i + 1:])
    return '/'.join(parts)


def same_rel(candidate, rel):
    """Copy of tools/round-40/c1-counter.py same_rel (lines 606-607)."""
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))


def load_oracle(path):
    rows = []
    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            f = line.split('\t')
            rows.append({'kind': f[0], 'rel': f[1],
                         'sha256': f[2] if len(f) > 2 else '',
                         'size': int(f[3]) if len(f) > 3 and f[3] else None})
    return rows


def main(argv):
    if len(argv) < 3:
        sys.stderr.write(__doc__)
        return 2
    receipt = json.load(open(argv[1], 'r', encoding='utf-8'))
    nr = (receipt.get('data') or receipt).get('normalized_result') or \
        (receipt.get('result') or {}).get('normalized_result')
    if nr is None:
        sys.stderr.write('no normalized_result in %s\n' % argv[1])
        return 2
    oracle = load_oracle(argv[2])
    root = None
    for i, a in enumerate(argv[3:]):
        if a == '--root' and i + 1 < len(argv[3:]):
            root = argv[3:][i + 1].lstrip('/')
    roots = chunk_roots(nr)
    if root is None:
        root = roots[0][0] if roots else None

    files = [(f.get('relative_path') or '', f.get('sha256') or '', f.get('size'))
             for f in nr.get('files') or []]
    unpub = [(u.get('relative_path') or '', u.get('kind'))
             for u in nr.get('unpublished_entries') or []]

    print('receipt      :', argv[1])
    print('chunk roots  :', json.dumps(roots))
    print('scoring root :', root)
    print('published    :', len(files), 'regular,', len(unpub), 'non-regular')
    print()

    reg = [r for r in oracle if r['kind'] == 'file']
    non = [r for r in oracle if r['kind'] != 'file']

    exact_map = {}
    split_map = {}
    suffix_map = {}
    for fp, fs, fsz in files:
        exact_rel, why = rule_exact(fp, root)
        if exact_rel is not None:
            exact_map.setdefault(exact_rel, []).append((fp, fs, fsz, why))
        split_map.setdefault(rule_split(fp), []).append((fp, fs, fsz))
        suffix_map.setdefault(rule_suffix(fp), []).append((fp, fs, fsz))

    def score(label, mapping):
        hit = 0
        missing = []
        wrong_sha = []
        for r in reg:
            bucket = mapping.get(r['rel'])
            if not bucket:
                missing.append(r['rel'])
                continue
            if any(b[1] == r['sha256'] for b in bucket):
                hit += 1
            else:
                wrong_sha.append(r['rel'])
        extra = sorted(set(mapping) - {r['rel'] for r in reg})
        coll = {k: len(v) for k, v in mapping.items() if len(v) > 1}
        print('[%s] oracle regular files matched %d/%d' % (label, hit, len(reg)))
        if missing:
            print('   not published at its exact oracle path:', json.dumps(missing))
        if wrong_sha:
            print('   path present, digest differs          :', json.dumps(wrong_sha))
        if extra:
            print('   published paths outside the oracle    :', json.dumps(extra))
        if coll:
            print('   oracle rel claimed by >1 published path:', json.dumps(coll))
        return hit, len(reg), missing

    h1 = score('exact', exact_map)
    h2 = score('split', split_map)
    h3 = score('suffix', suffix_map)
    print()

    # Direction 2: does a regular file get reported at a non-regular oracle path?
    for label, mapping in (('exact', exact_map), ('split', split_map), ('suffix', suffix_map)):
        fp_exact = sorted({r for r in mapping if r in {n['rel'] for n in non}})
        fp_suffix = sorted({rel for rel in (non and [n['rel'] for n in non] or [])
                            for cand in mapping if same_rel(cand, rel)})
        print('[%s] non-regular oracle paths claimed by a published regular file:' % label)
        print('   exact-name hits :', json.dumps(fp_exact))
        print('   same_rel hits   :', json.dumps(fp_suffix))

    # Direction 3: non-regular entries themselves.
    unpub_maps = {
        'exact': [rule_exact(p, root)[0] for p, _ in unpub],
        'split': [rule_split(p) for p, _ in unpub],
        'suffix': [rule_suffix(p) for p, _ in unpub],
    }
    want_non = {n['rel'] for n in non}
    for label, vals in unpub_maps.items():
        got = {v for v in vals if v is not None}
        print('[%s] non-regular oracle paths published as metadata: %d/%d%s'
              % (label, len(got & want_non), len(want_non),
                 '' if not (want_non - got) else '  missing=' + json.dumps(sorted(want_non - got))))

    ok = h1[0] == h1[1] and not h1[2]
    print()
    print('exact matcher verdict:', 'OK' if ok else 'MISMATCH')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
