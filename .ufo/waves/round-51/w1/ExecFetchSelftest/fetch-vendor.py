#!/usr/bin/env python3
"""Materialise round-50 external (vendor) C1 carriers into a cache directory (ported from tools/round-41/fetch-vendor.py).

The AVM firmware licence forbids redistribution (round-40 wave-1 R40SrcAvmVendor), so the
vendor AVM-BE members are never committed. carriers.json pins each one by a chain, and every
link of that chain is checked here before anything is written:

    url
      -> sha256(image) == external.image_sha256
      -> the tar member external.member
      -> sha256(member) == external.member_sha256        (R40-CL6, round-41 fix)
      -> [optional external.nested] read nested.path out of the member SquashFS with the
         pure-Python reader (sqfs-list.py), sha256 == nested.sha256, then carve the file to
         its own superblock bytes_used
      -> carve to `length` (bytes_used for a nested carrier)
      -> sha256(carve) == the carrier pin
      -> CACHE/<pin>.bin, which `c1-counter.py --carrier-cache CACHE` and `c1-run.sh` read.

Any broken link exits 1 and writes nothing for that carrier (fail closed: the cache entry is
only created after every hash in the chain has matched).  `member_sha256` is mandatory for an
external carrier since round 41: a spec that omits it fails closed with link `member_sha256`
instead of silently trusting the carve length.

Nested carrier spec (all keys under `external`):

    "nested": {"path": "<literal path inside the member SquashFS>",
               "sha256": "<sha256 of that whole file>"}

`path` is taken literally (no symlink resolution inside the member), and the nested file must
be a regular file.  The reader is opened with the layout that parses -- `auto` first, then the
three explicit layouts -- and the file hash is the arbiter, so a wrong layout guess can never
produce a passing chain.

Usage:
  fetch-vendor.py --spec carriers.json --cache DIR [--image-cache DIR]
  fetch-vendor.py --root LANE --rev REV --cache DIR      (reads carriers.json from git)
  fetch-vendor.py --selftest

Exit: 0 every external carrier materialised and verified; 1 a chain link failed;
2 usage / unreadable spec. Stdlib only; the fetch path writes no temporary file (the image
is held in memory and the cache entry goes through <pin>.bin.part in --cache).
"""
import argparse
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request

CARRIERS = 'tools/round-51/carriers.json'
SQFS_LIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         'round-41', 'sqfs-list.py')
ALLOWED_HOST = 'download.avm.de'     # round 50, C1SentinelFetch S4: vendor origin only
MAX_IMAGE = 64 << 20                 # round 50, S4: no unbounded read
NESTED_LAYOUTS = ('auto', 'avm', 'be', 'le')


def sha256(b):
    return hashlib.sha256(b).hexdigest()


_SQFS_MOD = None


def load_sqfs():
    """Import sqfs-list.py (same directory) once and return the module.

    Cached: a second exec_module would create a second ``SqfsError`` class and
    ``except sqfs.SqfsError`` would then miss the first module's exceptions.
    """
    global _SQFS_MOD
    if _SQFS_MOD is None:
        spec = importlib.util.spec_from_file_location('sqfs_list_r41', SQFS_LIST)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _SQFS_MOD = mod
    return _SQFS_MOD


def load_spec(a):
    if a.spec:
        with open(a.spec) as fh:
            return json.load(fh)
    p = subprocess.run(['git', '-C', a.root, 'show', f'{a.rev}:{CARRIERS}'],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit(2)
    return json.loads(p.stdout)


class _AvmOnlyRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        u = urllib.parse.urlsplit(newurl)
        if u.scheme != 'https' or u.hostname != ALLOWED_HOST:
            raise urllib.error.HTTPError(newurl, code, 'redirect off %s refused' % ALLOWED_HOST, hdrs, fp)
        return super().redirect_request(req, fp, code, msg, hdrs, newurl)


_OPENER = urllib.request.build_opener(_AvmOnlyRedirect)


def fetch(url, image_cache, want):
    u = urllib.parse.urlsplit(url)
    if u.scheme != 'https' or u.hostname != ALLOWED_HOST:
        raise ValueError('url outside https://%s: %s' % (ALLOWED_HOST, url))
    if image_cache:
        fp = os.path.join(image_cache, want + '.image')
        if os.path.isfile(fp):
            with open(fp, 'rb') as fh:
                b = fh.read()
            if sha256(b) == want:
                return b, 'cache'
    with _OPENER.open(url, timeout=300) as r:
        status = getattr(r, 'status', None)
        b = r.read(MAX_IMAGE + 1)
    if len(b) > MAX_IMAGE:
        raise ValueError('image over %d bytes' % MAX_IMAGE)
    if image_cache and sha256(b) == want:
        os.makedirs(image_cache, exist_ok=True)
        with open(os.path.join(image_cache, want + '.image'), 'wb') as fh:
            fh.write(b)
    return b, ('http %d' % status) if status is not None else 'read'


def tar_member(image, member):
    """Return the whole raw bytes of the tar member ``member`` (no carving)."""
    with tarfile.open(fileobj=io.BytesIO(image), mode='r:') as tf:
        names = {m.name: m for m in tf.getmembers()}
        m = names.get(member) or names.get('./' + member.lstrip('./'))
        if m is None or not m.isfile():
            return None, 'member %r absent' % member
        data = tf.extractfile(m).read()
    return data, 'member %d bytes, sha256 %s' % (len(data), sha256(data))


def open_member(data, label):
    """Open ``data`` as a SquashFS image with the first layout that parses."""
    sqfs = load_sqfs()
    errors = []
    for layout in NESTED_LAYOUTS:
        try:
            return sqfs.SquashFS(label, layout=layout, data=data), layout
        except sqfs.SqfsError as exc:
            errors.append('%s: %s' % (layout, exc))
    raise sqfs.SqfsError('member is not a readable SquashFS image (%s)'
                         % '; '.join(errors))


def nested_body(member_bytes, nested, rec):
    """Read ``nested['path']`` out of ``member_bytes``.

    Return ``(body, link, detail)``: ``link`` is None when the step passed.
    The nested file is hashed WHOLE, then carved to its OWN superblock
    ``bytes_used`` -- not the member's, which is a different image.
    """
    sqfs = load_sqfs()
    try:
        member_img, member_probe = open_member(member_bytes, 'member')
        body = sqfs.extract_file(member_img, nested['path'])
        carrier_img, carrier_probe = open_member(body, 'nested')
    except sqfs.SqfsError as exc:
        return None, 'nested', str(exc)
    used = carrier_img.bytes_used
    rec['nested'] = {'path': nested['path'], 'sha256': sha256(body),
                     'bytes': len(body), 'carrier_bytes_used': used,
                     'carrier_layout': carrier_img.layout,
                     'carrier_avm_marker': carrier_img.avm_marker,
                     'carrier_probe_layout': carrier_probe,
                     'member_layout': member_img.layout,
                     'member_probe_layout': member_probe}
    got = sha256(body)
    if got != (nested.get('sha256') or '').lower():
        return None, 'nested_sha256', '%s extracted, want %s' % (
            got, nested.get('sha256'))
    if not 0 < used <= len(body):
        return None, 'nested', 'bytes_used %d outside the %d-byte file' % (
            used, len(body))
    return body[:used], None, 'nested %s: %d bytes, carrier slice %d bytes' % (
        nested['path'], len(body), used)


def materialise(entry, cache, image_cache, fetcher=fetch):
    ext = entry.get('external') or {}
    pin = (entry.get('sha256') or '').lower()
    rec = {'id': entry.get('id'), 'pin': pin, 'url': ext.get('url')}
    missing = [k for k in ('url', 'image_sha256', 'member') if not ext.get(k)]
    if missing or len(pin) != 64:
        rec.update(ok=False, link='spec',
                   detail='external lacks %s or the carrier pin'
                          % (', '.join(missing) or 'nothing'))
        return rec
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

    member, detail = tar_member(image, ext['member'])
    rec['member_detail'] = detail
    if member is None:
        rec.update(ok=False, link='member')
        return rec

    # R40-CL6: the member hash is a link in the chain, checked before carving.
    want_member = (ext.get('member_sha256') or '').lower()
    rec['member_sha256'] = sha256(member)
    if len(want_member) != 64:
        rec.update(ok=False, link='member_sha256',
                   detail='spec omits member_sha256 (required since round 41)')
        return rec
    if rec['member_sha256'] != want_member:
        rec.update(ok=False, link='member_sha256',
                   detail='member %s, want %s'
                          % (rec['member_sha256'], want_member))
        return rec

    nested = ext.get('nested')
    if nested:
        if not isinstance(nested, dict) or not nested.get('path') or \
                not nested.get('sha256'):
            rec.update(ok=False, link='nested',
                       detail='nested needs path and sha256')
            return rec
        body, nlink, ndetail = nested_body(member, nested, rec)
        rec['nested_detail'] = ndetail
        if body is None:
            rec.update(ok=False, link=nlink, detail=ndetail)
            return rec
        length = len(body)
    else:
        body = member
        length = ext.get('length')
        if not isinstance(length, int) or length <= 0 or length > len(body):
            rec.update(ok=False, link='length',
                       detail='length %r outside the %d-byte member'
                              % (length, len(body)))
            return rec
        body = body[:length]

    rec['carrier_sha256'] = sha256(body)
    if rec['carrier_sha256'] != pin:
        rec.update(ok=False, link='carrier_sha256',
                   detail='carve %s, want %s' % (rec['carrier_sha256'], pin))
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
def guard_selftests(cases):
    """Exercise URL and redirect guards without opening a network connection."""
    import email.message

    checks = []
    for label, url in (
            ('initial-non-https', 'http://download.avm.de/x'),
            ('initial-wrong-host', 'https://example.invalid/x')):
        try:
            fetch(url, None, '0' * 64)
            checks.append((label, False, 'accepted'))
        except ValueError as exc:
            checks.append((label, 'url outside' in str(exc), str(exc)))

    class Response:
        def geturl(self):
            return 'https://download.avm.de/x'

    req = urllib.request.Request('https://download.avm.de/x')
    response = Response()
    opener = urllib.request.build_opener(_AvmOnlyRedirect)
    try:
        opener.handle_error(
            'http', req, response, 302, 'Found',
            {'Location': 'http://example.invalid/redirect'})
        checks.append(('redirect-off-host', False, 'handler returned without refusal'))
    except urllib.error.HTTPError as exc:
        checks.append(('redirect-off-host',
                       'redirect off' in str(exc.reason), str(exc.reason)))

    for label, ok, detail in checks:
        cases.append(('guard-' + label, ok, 0 if ok else 1, None, detail))




def selftest():
    """Self-contained chain tests: synthetic tars and real SquashFS images.

    The member images are built by the reader's own independent writer inside
    this process, so the test needs no network, no sasquatch and no unblob.
    """
    sqfs = load_sqfs()
    cases = []
    # tempfile honours TMPDIR; the fetch path itself writes no temporary file.
    base = tempfile.mkdtemp(prefix='fetch-vendor-selftest-')
    try:
        work = base

        # Inner carrier: a real AVM-layout SquashFS with a trailing pad, so the
        # chain has to carve it to its own bytes_used.
        inner_img = sqfs._build_image([
            {'path': 'etc/os-release', 'type': 'file',
             'data': b'AVM=1\n' * 40, 'fragment': True},
            {'path': 'bin/busybox', 'type': 'file',
             'data': bytes(range(256)) * 12},
            {'path': 'bin/sh', 'type': 'symlink', 'target': '../bin/busybox'},
        ], endian='be', comp='xz', header_endian='<', marker=True)
        inner_used = len(inner_img)
        inner_file = inner_img + b'PAD-AFTER-BYTES_USED' * 8
        inner_pin = sha256(inner_img)
        inner_sha = sha256(inner_file)

        # Outer member: the member SquashFS that carries the inner file.
        member_img = sqfs._build_image([
            {'path': 'var/tmp/filesystem_core.squashfs', 'type': 'file',
             'data': inner_file},
            {'path': 'etc/inner', 'type': 'file', 'data': b'not-the-carrier'},
            {'path': 'lib/alt', 'type': 'symlink',
             'target': '../var/tmp/filesystem_core.squashfs'},
        ], endian='be', comp='gzip', header_endian='<', marker=True)

        # A plain member (no nested step) for the non-nested chain.
        plain = b'sqsh' + bytes(range(256)) * 40 + b'TAILPAD!'
        plain_len = len(plain) - 8
        plain_pin = sha256(plain[:plain_len])

        def tar_of(name, payload, extra=None):
            bio = io.BytesIO()
            with tarfile.open(fileobj=bio, mode='w') as tf:
                for nm, body in [(name, payload)] + list(extra or []):
                    ti = tarfile.TarInfo(nm)
                    ti.size = len(body)
                    tf.addfile(ti, io.BytesIO(body))
            return bio.getvalue()

        nested_image = tar_of('./var/tmp/filesystem.image', member_img)
        plain_image = tar_of('./var/tmp/filesystem.image', plain)

        def fake(image):
            def f(url, ic, want):
                if url == 'bad://':
                    raise OSError('unreachable')
                return image, 'fake'
            return f

        def spec(**kw):
            ext = {'url': 'x://', 'image_sha256': sha256(nested_image),
                   'member': './var/tmp/filesystem.image',
                   'member_sha256': sha256(member_img),
                   'nested': {'path': 'var/tmp/filesystem_core.squashfs',
                              'sha256': inner_sha}}
            ext.update(kw.pop('ext', {}))
            e = {'id': 'V3', 'sha256': kw.pop('pin', inner_pin), 'external': ext}
            return {'carriers': [e]}

        def plain_spec(**kw):
            ext = {'url': 'x://', 'image_sha256': sha256(plain_image),
                   'member': './var/tmp/filesystem.image',
                   'member_sha256': sha256(plain), 'length': plain_len}
            ext.update(kw.pop('ext', {}))
            e = {'id': 'V1', 'sha256': kw.pop('pin', plain_pin), 'external': ext}
            return {'carriers': [e]}

        def case(name, sp, image, want_rc, want_link=None, want_cache=None):
            outdir = os.path.join(work, name)
            recs, rc = run(sp, outdir, None, fake(image))
            link = None if rc == 0 else (recs[0].get('link') if recs else 'none')
            cached = sorted(os.listdir(outdir)) if os.path.isdir(outdir) else []
            ok = rc == want_rc
            if want_link is not None:
                ok = ok and link == want_link
            if want_cache is not None:
                ok = ok and cached == want_cache
            cases.append((name, ok, rc, link, ','.join(cached)))

        case('nested-green', spec(), nested_image, 0,
             want_cache=[inner_pin + '.bin'])
        got = os.path.join(work, 'nested-green', inner_pin + '.bin')
        wrote = os.path.isfile(got) and sha256(open(got, 'rb').read()) == inner_pin
        cases.append(('nested-writes-carved-bytes', wrote, 0, None, inner_pin))
        case('plain-green', plain_spec(), plain_image, 0,
             want_cache=[plain_pin + '.bin'])

        case('bad-url', spec(ext={'url': 'bad://'}), nested_image, 1, 'url', [])
        case('image-sha', spec(ext={'image_sha256': '0' * 64}), nested_image,
             1, 'image_sha256', [])
        case('member-sha-mismatch',
             spec(ext={'member_sha256': '1' * 64}), nested_image,
             1, 'member_sha256', [])
        case('member-sha-omitted',
             spec(ext={'member_sha256': None}), nested_image,
             1, 'member_sha256', [])
        case('member-absent',
             spec(ext={'member': './var/nope'}), nested_image, 1, 'member', [])
        case('nested-sha-mismatch',
             spec(ext={'nested': {'path': 'var/tmp/filesystem_core.squashfs',
                                  'sha256': '2' * 64}}),
             nested_image, 1, 'nested_sha256', [])
        case('nested-path-absent',
             spec(ext={'nested': {'path': 'var/tmp/absent.squashfs',
                                  'sha256': inner_sha}}),
             nested_image, 1, 'nested', [])
        case('nested-path-is-symlink',
             spec(ext={'nested': {'path': 'lib/alt', 'sha256': inner_sha}}),
             nested_image, 1, 'nested', [])
        case('nested-on-nonsquashfs-member',
             plain_spec(ext={'length': plain_len,
                             'nested': {'path': 'var/tmp/filesystem_core.squashfs',
                                        'sha256': inner_sha}}),
             plain_image, 1, 'nested', [])
        case('pin-mismatch-whole-member',
             plain_spec(ext={'length': len(plain)}), plain_image,
             1, 'carrier_sha256', [])
        case('length-overrun', plain_spec(ext={'length': len(plain) + 1}),
             plain_image, 1, 'length', [])
        case('nested-pin-mismatch', spec(pin='3' * 64), nested_image,
             1, 'carrier_sha256', [])
        case('spec-missing-image-sha',
             spec(ext={'image_sha256': None}), nested_image, 1, 'spec', [])
        guard_selftests(cases)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    for name, ok, rc, link, cached in cases:
        print('%s\t%s\trc=%s\tlink=%s\tcache=%s'
              % ('PASS' if ok else 'FAIL', name, rc, link, cached))
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
    lane = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + os.sep
    for label, path in (('--cache', a.cache), ('--image-cache', a.image_cache)):
        if path and (os.path.realpath(path) + os.sep).startswith(lane):
            print('refusing: %s is inside the lane (vendor bytes are never committed)' % label,
                  file=sys.stderr)
            return 2
    recs, rc = run(load_spec(a), a.cache, a.image_cache)
    out = {'carriers': recs, 'exit_code': rc}
    print(json.dumps(out, indent=1, sort_keys=True))
    if a.json_out:
        with open(a.json_out, 'w') as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
    return rc


if __name__ == '__main__':
    sys.exit(main())
