#!/usr/bin/env python3
"""MH-5 — vendor-restricted bytes were left inside the lane worktree as a wave-1
artifact; only a sentinel's size survey, three minutes before the freeze commit,
kept them out of the tree.

Round-40 bytes:
  `w1/R40Sentinel.md:108-109` measured `artifacts/R40C1VendorV1/carrier-v1-be.sqsh`
  at 5,442,392 B (= the whole V1 carrier, AVM vendor bytes) in the worktree.
  `git log --all -- <that path>` is empty and the freeze tree carries only
  `carrier-v1-be.sqsh.REMOVED-by-L1.sha256`, so the rename happened before the
  commit — no gate, a reader.

Fix shape: a pin-keyed scan.  A carrier that must never be redistributed is
registered by sha256 *and* length; any file in the tree, and any blob reachable from
any commit, whose length equals a pinned length is hashed and refused on a sha256
match.  Length-first keeps the scan cheap on a 27k-object repository.

Usage: mh5-vendor-bytes.py --rig RIG.json --root TREE [--git] [--json]
Exit 0 = clean; 1 = a pinned payload is present; 2 = usage.
Red/green: a fixture tree holding a same-length dummy named like the carrier is red;
the same tree with the file removed is green.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys


def load_rig(path):
    with open(path) as fh:
        data = json.load(fh)
    pins = []
    for row in data.get('pins') or data:
        if row.get('sha256') and row.get('length'):
            pins.append((row['sha256'], int(row['length'])))
    return pins


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def scan_tree(root, lengths):
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__')]
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                st = os.lstat(path)
            except OSError:
                continue
            if not os.path.isfile(path) or st.st_size not in lengths:
                continue
            hits.append({'where': 'tree', 'path': path, 'length': st.st_size,
                         'sha256': sha256_file(path)})
    return hits


def scan_git(root, lengths):
    """Blob sizes reachable from any ref; hash only the ones whose length is pinned."""
    proc = subprocess.run(['git', '-C', root, 'cat-file', '--batch-all-objects',
                           '--batch-check=%(objecttype) %(objectsize) %(objectname)'],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return [{'where': 'git', 'error': proc.stderr.decode().strip()[:200]}]
    hits = []
    for line in proc.stdout.decode().splitlines():
        parts = line.split()
        if len(parts) != 3 or parts[0] != 'blob':
            continue
        size = int(parts[1])
        if size not in lengths:
            continue
        blob = subprocess.run(['git', '-C', root, 'cat-file', 'blob', parts[2]],
                              stdout=subprocess.PIPE).stdout
        digest = hashlib.sha256(blob).hexdigest()
        hits.append({'where': 'git', 'object': parts[2], 'length': size,
                     'sha256': digest})
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--rig', required=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--git', action='store_true')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    pins = load_rig(args.rig)
    if not pins:
        print('no pins in %s' % args.rig)
        return 2
    by_sha = {sha: length for sha, length in pins}
    lengths = {length for _sha, length in pins}
    hits = scan_tree(args.root, lengths)
    if args.git:
        hits += scan_git(args.root, lengths)
    fatal = [h for h in hits if h.get('sha256') in by_sha]
    if args.json:
        print(json.dumps({'pins': len(pins), 'lengths': sorted(lengths),
                          'candidates': hits, 'fatal': fatal}, indent=1))
    else:
        for h in hits:
            mark = 'PINNED' if h.get('sha256') in by_sha else 'same-length'
            print('%-12s %-6s %s %s' % (h.get('where'), mark, h.get('sha256', '')[:16],
                                        h.get('path') or h.get('object') or h.get('error')))
        print('pins=%d candidates=%d fatal=%d' % (len(pins), len(hits), len(fatal)))
    return 1 if fatal else 0


if __name__ == '__main__':
    sys.exit(main())
