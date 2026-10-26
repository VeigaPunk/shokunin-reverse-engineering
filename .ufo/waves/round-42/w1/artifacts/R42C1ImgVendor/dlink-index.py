#!/usr/bin/env python3
"""Read-only crawler for the D-Link legacy firmware host index (directory listings).

Fetches http://legacyfiles.us.dlink.com/<MODEL>/[<REV>/]FIRMWARE/ listing pages and
prints one TSV row per firmware file: model, rev, name, bytes, url.

Usage: dlink-index.py MODEL [MODEL ...]
"""
import re
import sys
import urllib.request

BASE = 'http://legacyfiles.us.dlink.com'
HREF = re.compile(r'HREF="([^"]+)"')
DIRMARK = re.compile(r'&lt;dir&gt;')
SIZE = re.compile(r'^\s*(\d+)\s+<A HREF')


def get(path):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('latin-1'), r.status


def entries(path):
    """[(href, bytes|None-for-dir)] for a listing page."""
    body, _ = get(path)
    out = []
    for line in body.replace('<br>', '\n').splitlines():
        href = HREF.search(line)
        if not href:
            continue
        if DIRMARK.search(line):
            out.append((href.group(1), None))
            continue
        m = SIZE.match(line)
        if m:
            out.append((href.group(1), int(m.group(1))))
    return out


def main(models):
    for model in models:
        try:
            revs = [n for n, sz in entries(f'/{model}/') if sz is None and n != '/']
        except Exception as exc:                                  # noqa: BLE001
            print(f'# {model}: model index failed: {exc}', file=sys.stderr)
            continue
        revs = sorted({r.strip('/').rsplit('/', 1)[-1] for r in revs})
        if not revs:
            revs = ['']
        for rev in revs:
            path = f'/{model}/{rev}/FIRMWARE/' if rev else f'/{model}/FIRMWARE/'
            try:
                files = entries(path)
            except Exception:                                     # noqa: BLE001
                continue
            for name, size in files:
                if size is None:
                    continue
                print(f'{model}\t{rev or "-"}\t{name.rsplit("/", 1)[-1]}\t{size}\t{BASE}{name}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
