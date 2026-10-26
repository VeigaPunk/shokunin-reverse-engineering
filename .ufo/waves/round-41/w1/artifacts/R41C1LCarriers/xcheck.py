#!/usr/bin/env python3
"""Exact cross-check of an extracted tree against a round-40-grammar oracle pair.

Reads `oracle.tsv` (relpath TAB sha256 TAB size) and `nonregular.tsv`
(relpath TAB kind TAB detail) and compares every row EXACTLY (no suffix
matching, no normalisation) with what an extractor really wrote:

  * every oracle row: the file exists, is a regular file, sha256 and size equal;
  * every non-regular row: kind (dir|symlink|...) and, for symlinks, the link
    target equal byte-for-byte;
  * nothing extra: every regular / symlink / directory found on disk is a row.

Usage: xcheck.py --root DIR --oracle oracle.tsv --nonregular nonregular.tsv
Exit 0 on zero mismatches (prints them otherwise), 2 usage.
"""
import argparse
import hashlib
import os
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path, ncols):
    rows = []
    with open(path) as fh:
        for ln, line in enumerate(fh, 1):
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) < ncols:
                raise SystemExit('%s:%d: want >= %d columns, got %d'
                                 % (path, ln, ncols, len(parts)))
            rows.append(tuple(parts[:ncols] + [''] * (ncols - len(parts))))
    return rows


def scan(root):
    reg, link, dirs = {}, {}, set()
    for dirpath, dnames, fnames in os.walk(root, followlinks=False):
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir != '.':
            dirs.add(rel_dir)
        for dn in list(dnames):
            p = os.path.join(dirpath, dn)
            r = os.path.normpath(os.path.join(rel_dir, dn))
            if os.path.islink(p):
                link[r] = os.readlink(p)
                dnames.remove(dn)
        for fn in fnames:
            p = os.path.join(dirpath, fn)
            r = os.path.normpath(os.path.join(rel_dir, fn))
            if os.path.islink(p):
                link[r] = os.readlink(p)
            elif os.path.isfile(p):
                reg[r] = (sha256_file(p), os.path.getsize(p))
            else:
                dirs.add(r)
    return reg, link, dirs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--oracle', required=True)
    ap.add_argument('--nonregular', required=True)
    ap.add_argument('--label', default='')
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print('root missing: %s' % root, file=sys.stderr)
        return 2
    oracle = read_tsv(a.oracle, 3)
    nonreg = read_tsv(a.nonregular, 3)
    reg, link, dirs = scan(root)
    bad = []
    for rel, sha, size in oracle:
        if rel not in reg:
            bad.append('MISSING regular %s' % rel)
            continue
        got_sha, got_size = reg[rel]
        if got_sha != sha:
            bad.append('SHA mismatch %s: %s != %s' % (rel, got_sha, sha))
        if int(size) != got_size:
            bad.append('SIZE mismatch %s: %d != %s' % (rel, got_size, size))
    seen_reg = set()
    for rel, kind, detail in nonreg:
        if kind == 'dir':
            if rel not in dirs:
                bad.append('MISSING dir %s' % rel)
            continue
        if kind == 'symlink':
            if rel not in link:
                bad.append('MISSING symlink %s (detail %r)' % (rel, detail))
            elif link[rel] != detail:
                bad.append('TARGET mismatch %s: %r != %r' % (rel, link[rel], detail))
            continue
        bad.append('unhandled non-regular kind %r at %s' % (kind, rel))
    oracle_paths = {r[0] for r in oracle}
    nonreg_paths = {r[0] for r in nonreg if r[1] != 'dir'}
    dir_paths = {r[0] for r in nonreg if r[1] == 'dir'}
    for rel in sorted(reg):
        if rel not in oracle_paths:
            bad.append('EXTRA regular %s' % rel)
    for rel in sorted(link):
        if rel not in nonreg_paths:
            bad.append('EXTRA symlink %s -> %r' % (rel, link[rel]))
    for rel in sorted(dirs):
        if rel not in dir_paths:
            bad.append('EXTRA dir %s' % rel)
    tag = ('%s ' % a.label) if a.label else ''
    print('%sfiles=%d symlinks=%d dirs=%d oracle=%d nonregular=%d mismatches=%d'
          % (tag, len(reg), len(link), len(dirs), len(oracle), len(nonreg), len(bad)))
    for b in bad:
        print('  %s' % b)
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
