#!/usr/bin/env python3
"""Emit the frozen R39-C1 carrier manifest (.ufo/waves/round-39/c1/carriers.json).

Inputs are 4-tuples of (id, carrier, oracle, symlinks) given either as
positional groups or as TSV lines in --spec:

    mk-carriers.py --root LANE --out .ufo/waves/round-39/c1/carriers.json \
        K1 corpus/evidence/round-37/c1/K1/carrier.sqsh \
           corpus/evidence/round-37/c1/K1/oracle.tsv \
           corpus/evidence/round-37/c1/K1/symlinks.tsv \
        ... (one 4-tuple per carrier)

    --spec FILE       one carrier per line: id TAB carrier TAB oracle TAB
                      symlinks [TAB kind]; blank lines and '#' lines ignored

Every path is resolved against --root, must stay inside it, must be a regular
file; the carrier pin is the sha256 of its bytes. The emitted entry keys are
exactly the ones the round-39 counter reads -- id, path, sha256, oracle,
symlinks, receipt -- plus provenance (kind, size_bytes, oracle_sha256,
oracle_files, symlinks_sha256, symlinks_in_tree, symlinks_escaping) that the
counter ignores. repo-relative paths, byte-sorted JSON, no timestamps, so a
regeneration is byte-identical unless an input changed.

Validation (any failure is exit 2 and nothing is written):
  * ids are unique and form a contiguous K1..KN run (--allow-gaps disables);
  * each carrier starts with the big-endian SquashFS magic `sqsh` at offset 0
    (--endian {be,le,any});
  * oracle.tsv rows are `relpath TAB sha256 TAB size` with normalised relative
    paths, lowercase 64-hex digests, non-negative sizes and no duplicates;
  * symlinks.tsv rows are `relpath TAB target TAB in-tree|escaping` with the
    same path rules and no duplicates;
  * no path is both a regular file and a symlink (neither in-tree nor escaping
    symlinks are ever published, so listing one in oracle.tsv is a freeze bug);
  * receipt is derived, never supplied: corpus/evidence/round-39/c1/<id>/after.json.

Exit: 0 manifest written, 2 usage/validation error, 3 I/O error.
"""
import argparse
import hashlib
import json
import os
import re
import sys

ID_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,15}$')
HEX64_RE = re.compile(r'^[0-9a-f]{64}$')
MAGIC = {'be': b'sqsh', 'le': b'hsqs'}
CLAIM = 'R39-C1'
RECEIPT_TMPL = 'corpus/evidence/round-39/c1/{id}/after.json'


class Bad(Exception):
    pass


def real_under(root, path, what):
    """Resolve `path` (relative to root or absolute) and require it inside root."""
    cand = path if os.path.isabs(path) else os.path.join(root, path)
    real = os.path.realpath(cand)
    root_real = os.path.realpath(root)
    if real != root_real and not real.startswith(root_real + os.sep):
        raise Bad(f'{what} escapes --root: {path}')
    if not os.path.isfile(real):
        raise Bad(f'{what} is not a regular file: {path}')
    return real


def rel_to(root, real):
    rel = os.path.relpath(real, os.path.realpath(root)).replace(os.sep, '/')
    if rel.startswith('../') or rel == '..':
        raise Bad(f'not under --root: {real}')
    return rel


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def bad_rel(rel, what, line):
    if not rel or rel.startswith('/') or rel.endswith('/'):
        raise Bad(f'{what}:{line}: relative path must be non-empty, not absolute, no trailing slash: {rel!r}')
    parts = rel.split('/')
    if any(p in ('', '.', '..') for p in parts):
        raise Bad(f'{what}:{line}: relative path not normalised: {rel!r}')


def parse_oracle(path):
    rows, seen = [], set()
    with open(path, encoding='utf-8') as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            fields = line.split('\t')
            if len(fields) != 3:
                raise Bad(f'{path}:{n}: want 3 tab-separated fields, got {len(fields)}')
            rel, digest, size = fields
            bad_rel(rel, path, n)
            if not HEX64_RE.match(digest):
                raise Bad(f'{path}:{n}: sha256 is not 64 lowercase hex: {digest!r}')
            if not size.isdigit():
                raise Bad(f'{path}:{n}: size is not a non-negative integer: {size!r}')
            if rel in seen:
                raise Bad(f'{path}:{n}: duplicate path {rel!r}')
            seen.add(rel)
            rows.append({'path': rel, 'sha256': digest, 'size': int(size)})
    if not rows:
        raise Bad(f'{path}: no oracle rows')
    return rows


def parse_symlinks(path):
    rows, seen = [], set()
    with open(path, encoding='utf-8') as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            fields = line.split('\t')
            if len(fields) != 3:
                raise Bad(f'{path}:{n}: want 3 tab-separated fields '
                          '(relpath, target, in-tree|escaping), got '
                          f'{len(fields)}; a header or note row is not allowed')
            rel, target, kind = fields
            bad_rel(rel, path, n)
            if kind not in ('in-tree', 'escaping'):
                raise Bad(f'{path}:{n}: classification must be in-tree|escaping: {kind!r}')
            if not target:
                raise Bad(f'{path}:{n}: empty link target')
            if '\t' in target:
                raise Bad(f'{path}:{n}: tab in link target')
            if rel in seen:
                raise Bad(f'{path}:{n}: duplicate path {rel!r}')
            seen.add(rel)
            rows.append({'path': rel, 'target': target, 'class': kind})
    return rows


def parse_spec(path):
    tups = []
    with open(path, encoding='utf-8') as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            fields = [f.strip() for f in line.split('\t')]
            if len(fields) not in (4, 5):
                raise Bad(f'{path}:{n}: want 4 or 5 tab-separated fields '
                          '(id, carrier, oracle, symlinks[, kind])')
            tups.append(tuple(fields))
    return tups


def natural_key(cid):
    m = re.match(r'^([A-Za-z]+)([0-9]+)$', cid)
    return (m.group(1), int(m.group(2))) if m else (cid, 0)


def build(root, tuples, endian, allow_gaps):
    carriers, ids = [], set()
    for tup in tuples:
        cid, carrier_p, oracle_p, symlinks_p = tup[:4]
        kind_text = tup[4] if len(tup) > 4 and tup[4] else None
        if not ID_RE.match(cid):
            raise Bad(f'invalid carrier id {cid!r}')
        if cid in ids:
            raise Bad(f'duplicate carrier id {cid!r}')
        ids.add(cid)
        carrier = real_under(root, carrier_p, f'{cid} carrier')
        oracle = real_under(root, oracle_p, f'{cid} oracle')
        symlinks = real_under(root, symlinks_p, f'{cid} symlinks')
        with open(carrier, 'rb') as fh:
            head = fh.read(4)
        if endian != 'any' and head != MAGIC[endian]:
            want = {v: k for k, v in MAGIC.items()}[MAGIC[endian]]
            raise Bad(f'{cid} carrier does not start with the {want.upper()} '
                      f'squashfs magic {MAGIC[endian]!r}: head={head!r}')
        orows = parse_oracle(oracle)
        srows = parse_symlinks(symlinks)
        oset = {r['path'] for r in orows}
        clash = sorted(oset & {r['path'] for r in srows})
        if clash:
            raise Bad(f'{cid}: path(s) listed as both regular file and symlink: {clash}')
        entry = {'id': cid}
        if kind_text:
            entry['kind'] = kind_text
        entry.update({
            'path': rel_to(root, carrier),
            'sha256': sha256_file(carrier),
            'size_bytes': os.path.getsize(carrier),
            'oracle': rel_to(root, oracle),
            'oracle_sha256': sha256_file(oracle),
            'oracle_files': len(orows),
            'symlinks': rel_to(root, symlinks),
            'symlinks_sha256': sha256_file(symlinks),
            'symlinks_in_tree': sum(1 for r in srows if r['class'] == 'in-tree'),
            'symlinks_escaping': sum(1 for r in srows if r['class'] == 'escaping'),
            'receipt': RECEIPT_TMPL.format(id=cid),
        })
        carriers.append(entry)
    carriers.sort(key=lambda e: natural_key(e['id']))
    for field, what in (('sha256', 'carrier pins'), ('path', 'carrier paths')):
        vals = [e[field] for e in carriers]
        if len(set(vals)) != len(vals):
            dup = sorted({v for v in vals if vals.count(v) > 1})
            raise Bad(f'duplicate {what}: {dup}')
    got = [e['id'] for e in carriers]
    if not allow_gaps:
        want = [f'K{i}' for i in range(1, len(got) + 1)]
        if got != want:
            raise Bad(f'carrier ids are not a contiguous K1..K{len(got)} run: {got} '
                      '(pass --allow-gaps to override)')
    return {
        'claim': CLAIM,
        'schema': 'kaidoku-r39-c1-carriers-v1',
        'note': ('Carriers and oracles frozen before any round-39 after-run. sha256 is the '
                 'carrier pin; oracle.tsv holds the regular-file oracle '
                 '(relpath, sha256, size); symlinks.tsv holds every in-image symlink '
                 '(relpath, target, in-tree|escaping); receipt is the round-39 REA '
                 'extract-firmware after-receipt path for that carrier.'),
        'carriers': carriers,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description='emit the R39-C1 carrier manifest')
    ap.add_argument('--root', required=True, help='lane root (carrier paths are relative to it)')
    ap.add_argument('--out', required=True, help='manifest path, e.g. .ufo/waves/round-39/c1/carriers.json')
    ap.add_argument('--spec', action='append', default=[],
                    help='TSV list: id<TAB>carrier<TAB>oracle<TAB>symlinks[<TAB>kind]')
    ap.add_argument('--endian', choices=('be', 'le', 'any'), default='be',
                    help='required squashfs magic at offset 0 (default be: sqsh)')
    ap.add_argument('--allow-gaps', action='store_true',
                    help='do not require a contiguous K1..KN id run')
    ap.add_argument('tuples', nargs='*',
                    help='positional 4-tuples: ID CARRIER ORACLE SYMLINKS [ID ...]')
    a = ap.parse_args(argv)

    root = os.path.realpath(a.root)
    if not os.path.isdir(root):
        print(f'mk-carriers: --root is not a directory: {a.root}', file=sys.stderr)
        return 2
    tuples = []
    try:
        for spec in a.spec:
            tuples.extend(parse_spec(spec))
        if a.tuples:
            if len(a.tuples) % 4:
                raise Bad('positional carriers must come in groups of 4: '
                          'ID CARRIER ORACLE SYMLINKS')
            tuples.extend(tuple(a.tuples[i:i + 4]) for i in range(0, len(a.tuples), 4))
        if not tuples:
            raise Bad('no carriers given (pass --spec FILE and/or 4-tuples)')
        manifest = build(root, tuples, a.endian, a.allow_gaps)
    except Bad as e:
        print(f'mk-carriers: {e}', file=sys.stderr)
        return 2

    text = json.dumps(manifest, indent=2) + '\n'
    out = a.out if os.path.isabs(a.out) else os.path.join(root, a.out)
    try:
        os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
        tmp = out + f'.tmp.{os.getpid()}'
        with open(tmp, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        os.replace(tmp, out)
    except OSError as e:
        print(f'mk-carriers: cannot write {out}: {e}', file=sys.stderr)
        return 3

    for c in manifest['carriers']:
        print(f"{c['id']}  {c['sha256']}  files={c['oracle_files']}  "
              f"symlinks={c['symlinks_in_tree']}+{c['symlinks_escaping']}  {c['path']}")
    print(f'wrote {out} ({len(manifest["carriers"])} carriers, '
          f'{len(text.encode())} bytes, sha256={hashlib.sha256(text.encode()).hexdigest()})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
