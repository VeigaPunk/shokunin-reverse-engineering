#!/usr/bin/env python3
"""Materialise round-40 external (vendor) C1 carriers into a cache directory.

The AVM firmware licence forbids redistribution (round-40 wave-1 R40SrcAvmVendor), so the
vendor AVM-BE members are never committed. carriers.json pins each one by a chain:

    external = {url, image_sha256, member, length}   +   sha256 (the carrier pin)

This tool downloads `url`, requires sha256(image) == image_sha256, reads the tar member
`member`, carves bytes [0, length) and requires sha256(carve) == the carrier pin; it then
writes CACHE/<pin>.bin, which `c1-counter.py --carrier-cache CACHE` and `c1-run.sh` read.
Any broken link exits 1 and writes nothing for that carrier.

Usage:
  fetch-vendor.py --spec carriers.json --cache DIR [--image-cache DIR]
  fetch-vendor.py --root LANE --rev REV --cache DIR      (reads carriers.json from git)
  fetch-vendor.py --selftest

Exit: 0 every external carrier materialised and verified; 1 a chain link failed;
2 usage / unreadable spec. Stdlib only; temporary files under TMPDIR / --cache.
"""
import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

CARRIERS = '.ufo/waves/round-40/c1/carriers.json'


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def load_spec(a):
    if a.spec:
        return json.load(open(a.spec))
    p = subprocess.run(['git', '-C', a.root, 'show', f'{a.rev}:{CARRIERS}'],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit(2)
    return json.loads(p.stdout)


def fetch(url, image_cache, want):
    if image_cache:
        fp = os.path.join(image_cache, want + '.image')
        if os.path.isfile(fp):
            b = open(fp, 'rb').read()
            if sha256(b) == want:
                return b, 'cache'
    with urllib.request.urlopen(url, timeout=300) as r:
        status = r.status
        b = r.read()
    if image_cache and sha256(b) == want:
        os.makedirs(image_cache, exist_ok=True)
        open(os.path.join(image_cache, want + '.image'), 'wb').write(b)
    return b, 'http %d' % status


def carve(image, member, length):
    with tarfile.open(fileobj=io.BytesIO(image), mode='r:') as tf:
        names = {m.name: m for m in tf.getmembers()}
        m = names.get(member) or names.get('./' + member.lstrip('./'))
        if m is None or not m.isfile():
            return None, 'member %r absent' % member
        data = tf.extractfile(m).read()
    if not isinstance(length, int) or length <= 0 or length > len(data):
        return None, 'length %r outside member (%d bytes)' % (length, len(data))
    return data[:length], 'member %d bytes, sha256 %s' % (len(data), sha256(data))


def materialise(entry, cache, image_cache, fetcher=fetch):
    ext = entry.get('external') or {}
    pin = (entry.get('sha256') or '').lower()
    rec = {'id': entry.get('id'), 'pin': pin, 'url': ext.get('url')}
    try:
        image, how = fetcher(ext['url'], image_cache, ext['image_sha256'])
    except Exception as e:  # network or URL error is a broken link, not a pass
        rec.update(ok=False, link='url', detail=str(e))
        return rec
    rec['fetch'] = how
    rec['image_sha256'] = sha256(image)
    if rec['image_sha256'] != ext['image_sha256']:
        rec.update(ok=False, link='image_sha256')
        return rec
    body, detail = carve(image, ext['member'], ext['length'])
    rec['member_detail'] = detail
    if body is None:
        rec.update(ok=False, link='member')
        return rec
    rec['carrier_sha256'] = sha256(body)
    if rec['carrier_sha256'] != pin:
        rec.update(ok=False, link='carrier_sha256')
        return rec
    os.makedirs(cache, exist_ok=True)
    out = os.path.join(cache, pin + '.bin')
    with open(out + '.part', 'wb') as fh:
        fh.write(body)
    os.replace(out + '.part', out)
    rec.update(ok=True, path=out, bytes=len(body))
    return rec


def run(spec, cache, image_cache, fetcher=fetch):
    recs = [materialise(c, cache, image_cache, fetcher)
            for c in spec.get('carriers') or [] if isinstance(c, dict) and 'external' in c]
    return recs, (0 if recs and all(r['ok'] for r in recs) else 1)


def selftest():
    cases = []
    with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as d:
        body = b'sqsh' + bytes(range(256)) * 40 + b'TAILPAD!'
        bio = io.BytesIO()
        with tarfile.open(fileobj=bio, mode='w') as tf:
            ti = tarfile.TarInfo('./var/tmp/filesystem.image')
            ti.size = len(body)
            tf.addfile(ti, io.BytesIO(body))
        image = bio.getvalue()
        good_len = len(body) - 8
        pin = sha256(body[:good_len])

        def fake(url, ic, want):
            if url == 'bad://':
                raise OSError('unreachable')
            return image, 'fake'

        def spec(**kw):
            ext = {'url': 'x://', 'image_sha256': sha256(image),
                   'member': './var/tmp/filesystem.image', 'length': good_len}
            ext.update(kw.pop('ext', {}))
            e = {'id': 'V1', 'sha256': kw.pop('pin', pin), 'external': ext}
            return {'carriers': [e]}

        def case(name, sp, want_rc, want_link=None):
            recs, rc = run(sp, os.path.join(d, name), None, fake)
            link = None if rc == 0 else recs[0].get('link') if recs else 'none'
            ok = rc == want_rc and (want_link is None or link == want_link)
            cases.append((name, ok, rc, link))

        case('green', spec(), 0)
        case('bad-url', spec(ext={'url': 'bad://'}), 1, 'url')
        case('image-sha', spec(ext={'image_sha256': '0' * 64}), 1, 'image_sha256')
        case('member-absent', spec(ext={'member': './var/nope'}), 1, 'member')
        case('length-overrun', spec(ext={'length': len(body) + 1}), 1, 'member')
        case('pin-mismatch-whole-member', spec(ext={'length': len(body)}), 1, 'carrier_sha256')
        case('no-external', {'carriers': [{'id': 'L1', 'sha256': pin, 'path': 'x'}]}, 1)
        recs, rc = run(spec(), os.path.join(d, 'out'), None, fake)
        wrote = os.path.isfile(os.path.join(d, 'out', pin + '.bin')) and \
            sha256(open(os.path.join(d, 'out', pin + '.bin'), 'rb').read()) == pin
        cases.append(('writes-verified-bytes', wrote, rc, None))
    for name, ok, rc, link in cases:
        print('%s\t%s\trc=%s\tlink=%s' % ('PASS' if ok else 'FAIL', name, rc, link))
    n = len(cases)
    p = sum(1 for c in cases if c[1])
    print('SELFTEST cases=%d pass=%d fail=%d' % (n, p, n - p))
    return 0 if p == n else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec')
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--cache')
    ap.add_argument('--image-cache')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.cache or not (a.spec or (a.root and a.rev)):
        print('usage: --cache DIR and --spec FILE or --root LANE --rev REV', file=sys.stderr)
        return 2
    recs, rc = run(load_spec(a), a.cache, a.image_cache)
    out = {'carriers': recs, 'exit_code': rc}
    print(json.dumps(out, indent=1, sort_keys=True))
    if a.json_out:
        json.dump(out, open(a.json_out, 'w'), indent=1, sort_keys=True)
    return rc


if __name__ == '__main__':
    sys.exit(main())
