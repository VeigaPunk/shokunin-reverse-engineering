#!/usr/bin/env python3
"""Scan every blob committed at REV for vendor-firmware bytes.

Three independent tests, cheapest first:

  1. pin equality   a blob whose sha256 equals any pin in the carriers spec
                    (carrier pin, member_sha256, image_sha256) -- a committed
                    carve, member or image.
  2. size            blobs over --min-bytes under --trees (the round-40 evidence
                    and wave trees); a carved member is 5.4 MB or larger, so any
                    committed copy shows up here.
  3. window sharing  N random 128-byte windows sampled from each rebuilt vendor
                    carrier, searched in every blob: a committed fragment (a
                    single extracted file, a hexdump, a buffer in a receipt)
                    shares whole windows with the source bytes.

Vendor bytes are rebuilt OUTSIDE the lane (fetch-vendor.py --cache) and are never
copied into the repository; this script only reads them.

Usage:
  scan-committed-vendor-bytes.py --lane LANE --rev REV --cache DIR
                                 [--spec SPEC] [--windows 96] [--min-bytes 1048576]
                                 [--trees PREFIX ...] [--json-out PATH]

Exit 0 clean, 1 a hit, 2 usage. Stdlib only; temporary files under TMPDIR.
"""
import argparse
import json
import os
import random
import subprocess
import sys

CARRIERS = '.ufo/waves/round-40/c1/carriers.json'


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True)


def pins_of(spec):
    pins = {}
    for c in spec.get('carriers') or []:
        if not isinstance(c, dict):
            continue
        pin = (c.get('sha256') or '').lower()
        if pin:
            pins[pin] = '%s carrier' % (c.get('id'),)
        ext = c.get('external') or {}
        for key in ('member_sha256', 'image_sha256'):
            v = (ext.get(key) or '').lower()
            if v:
                pins[v] = '%s %s' % (c.get('id'), key)
    return pins


def blobs(lane, rev):
    p = git(lane, 'ls-tree', '-r', '-l', rev)
    if p.returncode != 0:
        raise SystemExit('git ls-tree failed: ' + p.stderr.decode(errors='replace'))
    out = []
    for line in p.stdout.decode(errors='replace').splitlines():
        meta, path = line.split('\t', 1)
        mode, typ, sha, size = meta.split()
        if typ == 'blob':
            out.append((path, int(size), sha))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--cache', required=True)
    ap.add_argument('--spec')
    ap.add_argument('--windows', type=int, default=96)
    ap.add_argument('--window-bytes', type=int, default=128)
    ap.add_argument('--min-bytes', type=int, default=1048576)
    ap.add_argument('--trees', nargs='*',
                    default=['.ufo/waves/round-40/', 'corpus/evidence/round-40/'])
    ap.add_argument('--json-out')
    a = ap.parse_args()

    spec_raw = (open(a.spec, 'rb').read() if a.spec
                else git(a.lane, 'show', '%s:%s' % (a.rev, CARRIERS)).stdout)
    spec = json.loads(spec_raw)
    pins = pins_of(spec)

    carriers = []
    for name in sorted(os.listdir(a.cache)):
        if name.endswith('.bin'):
            path = os.path.join(a.cache, name)
            carriers.append((name[:-4], open(path, 'rb').read()))

    rows = blobs(a.lane, a.rev)
    res = {'revision': a.rev, 'blobs': len(rows),
           'bytes': sum(r[1] for r in rows), 'vendor_carriers': len(carriers),
           'pin_matches': [], 'large_files': [], 'window_hits': []}

    for path, size, sha in rows:
        if sha in pins:
            res['pin_matches'].append({'path': path, 'sha256': sha,
                                       'pin_of': pins[sha]})
        if size > a.min_bytes and any(path.startswith(t) for t in a.trees):
            res['large_files'].append({'path': path, 'bytes': size, 'sha256': sha})

    rnd = random.Random(41)
    wins = []
    for name, blob in carriers:
        if len(blob) <= a.window_bytes:
            continue
        for _ in range(a.windows):
            off = rnd.randrange(0, len(blob) - a.window_bytes)
            wins.append((name, off, blob[off:off + a.window_bytes]))

    scanned = 0
    for path, size, sha in rows:
        body = git(a.lane, 'cat-file', 'blob', sha).stdout
        scanned += len(body)
        for name, off, w in wins:
            if w in body:
                res['window_hits'].append({'path': path, 'carrier': name,
                                           'offset': off})
                break

    res['window_samples'] = len(wins)
    res['scanned_bytes'] = scanned
    res['clean'] = not (res['pin_matches'] or res['large_files']
                        or res['window_hits'])
    text = json.dumps(res, indent=1, sort_keys=True)
    print(text)
    if a.json_out:
        open(a.json_out, 'w').write(text + '\n')
    return 0 if res['clean'] else 1


if __name__ == '__main__':
    sys.exit(main())
