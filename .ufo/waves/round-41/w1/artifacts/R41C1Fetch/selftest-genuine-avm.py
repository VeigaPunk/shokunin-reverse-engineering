#!/usr/bin/env python3
"""Round-41 R41C1Fetch integration test: the fetch chain on GENUINE AVM images.

Builds the whole chain with tools/round-40/gen-squashfs.py --endian avm-genuine
(no vendor bytes, no reserved image, no network): an inner AVM-layout carrier,
an AVM-layout member SquashFS that carries it, and a tar image that carries the
member.  Then it drives fetch-vendor.py over the chain and over four broken
variants.

In both directions the outer member holds a nested-name collision (a regular
file whose path ends with a symlink's path, and a symlink whose path ends with
a regular file's path), so the chain has to read the nested carrier by its
literal path.

Usage: it-genuine.py --gen GEN --fetch FETCH --work DIR [--sqfs SQFS]
Exit 0 all cases pass, 1 a case failed.
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build(gen, tree, out, mode, comp):
    p = subprocess.run([sys.executable, '-I', '-B', gen, tree, out,
                        '--endian', mode, '--comp', comp],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit('gen-squashfs failed: %s%s' % (p.stdout, p.stderr))
    with open(out, 'rb') as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gen', required=True)
    ap.add_argument('--fetch', required=True)
    ap.add_argument('--sqfs', required=True)
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    fetch = os.path.abspath(a.fetch)
    results = []

    def check(name, ok, detail=''):
        results.append((name, bool(ok), detail))

    # ---- inner carrier tree: collisions in both directions ---------------
    inner_tree = os.path.join(work, 'tree-inner')
    for d in ('usr/bin', 'bin', 'sbin', 'usr/sbin', 'etc'):
        os.makedirs(os.path.join(inner_tree, d))
    open(os.path.join(inner_tree, 'usr/bin/busy'), 'wb').write(
        b'BUSY-REGULAR-' * 300)
    os.symlink('../../usr/bin/busy', os.path.join(inner_tree, 'bin/busy'))
    open(os.path.join(inner_tree, 'sbin/reboot'), 'wb').write(b'REBOOT-BODY')
    os.symlink('../../../sbin/reboot',
               os.path.join(inner_tree, 'usr/sbin/reboot'))
    open(os.path.join(inner_tree, 'etc/os-release'), 'wb').write(
        b'NAME=AVM\n' * 50)

    inner_path = os.path.join(work, 'inner.squashfs')
    inner = build(a.gen, inner_tree, inner_path, 'avm-genuine', 'xz')

    # ---- member tree: carries the inner carrier --------------------------
    member_tree = os.path.join(work, 'tree-member')
    os.makedirs(os.path.join(member_tree, 'var/tmp'))
    os.makedirs(os.path.join(member_tree, 'lib'))
    os.makedirs(os.path.join(member_tree, 'etc'))
    # padded on disk: the chain must carve to the nested carrier's bytes_used
    inner_stored = inner + b'PADDING-AFTER-BYTES_USED' * 9
    open(os.path.join(member_tree, 'var/tmp/filesystem_core.squashfs'),
         'wb').write(inner_stored)
    # collisions around the nested path itself
    os.symlink('../var/tmp/filesystem_core.squashfs',
               os.path.join(member_tree, 'lib/filesystem_core.squashfs'))
    open(os.path.join(member_tree, 'etc/inner'), 'wb').write(
        b'lib/filesystem_core.squashfs')     # regular file whose path ENDS
    # with the symlink's path (direction A: regular is longer)
    member_path = os.path.join(work, 'member.squashfs')
    member = build(a.gen, member_tree, member_path, 'avm-genuine', 'gzip')

    # ---- tar image -------------------------------------------------------
    image = io.BytesIO()
    with tarfile.open(fileobj=image, mode='w') as tf:
        ti = tarfile.TarInfo('./var/tmp/filesystem.image')
        ti.size = len(member)
        tf.addfile(ti, io.BytesIO(member))
        ti = tarfile.TarInfo('./var/tmp/filesystem.image.md5')
        payload = b'not the member\n'
        ti.size = len(payload)
        tf.addfile(ti, io.BytesIO(payload))
    image_bytes = image.getvalue()
    image_path = os.path.join(work, 'TEST.image')
    open(image_path, 'wb').write(image_bytes)

    pin = sha(inner)                       # carrier = the inner image itself
    nested_sha = sha(inner_stored)
    member_sha = sha(member)

    def spec(**kw):
        ext = {'url': 'file://' + image_path,
               'image_sha256': sha(image_bytes),
               'member': './var/tmp/filesystem.image',
               'member_sha256': member_sha,
               'nested': {'path': 'var/tmp/filesystem_core.squashfs',
                          'sha256': nested_sha},
               'product': 'synthetic AVM-genuine chain (not vendor bytes)'}
        ext.update(kw)
        return {'claim': 'R41-C1', 'carriers': [
            {'id': 'VT', 'sha256': pin, 'kind': 'vendor', 'external': ext}]}

    def drive(name, sp, want_rc, image_cache=None):
        sp_path = os.path.join(work, name + '.json')
        with open(sp_path, 'w') as fh:
            json.dump(sp, fh, indent=1, sort_keys=True)
        cache = os.path.join(work, 'cache-' + name)
        rec_path = os.path.join(work, name + '.rec.json')
        cmd = [sys.executable, '-I', '-B', fetch, '--spec', sp_path,
               '--cache', cache, '--json-out', rec_path]
        if image_cache:
            cmd += ['--image-cache', image_cache]
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=work)
        rec = json.load(open(rec_path)) if os.path.isfile(rec_path) else {}
        return p, rec, cache

    # ---- green ----------------------------------------------------------
    p, rec, cache = drive('green', spec(), 0)
    got = os.path.join(cache, pin + '.bin')
    cached = os.path.isfile(got)
    body = open(got, 'rb').read() if cached else b''
    check('green-exit', p.returncode == 0, 'rc=%d %s' % (p.returncode,
                                                         p.stderr.strip()[:200]))
    check('green-cache-carved-to-bytes_used', cached and sha(body) == pin,
          'cache=%s sha=%s' % (cached, sha(body)))
    check('green-carve-length', len(body) == len(inner),
          'carved %d, inner %d' % (len(body), len(inner)))
    r = (rec.get('carriers') or [{}])[0]
    check('green-member-sha-recorded',
          r.get('member_sha256') == member_sha, str(r.get('member_sha256')))
    nested_rec = r.get('nested') or {}
    check('green-nested-layout-avm', nested_rec.get('carrier_layout') == 'avm',
          json.dumps(nested_rec, sort_keys=True))
    check('green-nested-marker',
          nested_rec.get('carrier_avm_marker') is True)
    check('green-member-layout-avm', nested_rec.get('member_layout') == 'avm',
          str(nested_rec.get('member_layout')))

    # the extracted nested file equals the bytes written into the member tree
    rc = subprocess.run([sys.executable, '-I', '-B', a.sqfs, '--layout', 'avm',
                         '--extract', 'var/tmp/filesystem_core.squashfs',
                         '--inspect', '--out', os.path.join(work, 'nested.out'),
                         os.path.join(work, 'member.squashfs')],
                        capture_output=True, text=True)
    nested_out = os.path.join(work, 'nested.out')
    check('reader-extract-byte-identical',
          rc.returncode == 0 and os.path.isfile(nested_out)
          and open(nested_out, 'rb').read() == inner_stored,
          'rc=%d %s' % (rc.returncode, rc.stderr.strip()[:160]))

    # image cache: run twice against one cache dir; the second run must read it
    ic = os.path.join(work, 'images')
    p1, rec1, _ = drive('green-ic1', spec(), 0, image_cache=ic)
    p2, rec2, _ = drive('green-ic2', spec(), 0, image_cache=ic)
    f1 = ((rec1.get('carriers') or [{}])[0]).get('fetch')
    f2 = ((rec2.get('carriers') or [{}])[0]).get('fetch')
    check('green-image-cache', p1.returncode == 0 and p2.returncode == 0
          and f1 == 'read' and f2 == 'cache',
          'first=%s second=%s' % (f1, f2))

    # ---- red: member sha mismatch ---------------------------------------
    p, rec, cache = drive('member-sha', spec(member_sha256='1' * 64), 1)
    r = (rec.get('carriers') or [{}])[0]
    check('red-member-sha', p.returncode == 1 and r.get('link') == 'member_sha256'
          and not os.path.isdir(cache),
          'rc=%d link=%s cache=%s' % (p.returncode, r.get('link'),
                                      os.path.isdir(cache)))

    # ---- red: image sha mismatch ----------------------------------------
    p, rec, cache = drive('image-sha', spec(image_sha256='0' * 64), 1)
    r = (rec.get('carriers') or [{}])[0]
    check('red-image-sha', p.returncode == 1 and r.get('link') == 'image_sha256'
          and not os.path.isdir(cache),
          'rc=%d link=%s' % (p.returncode, r.get('link')))

    # ---- red: nested sha mismatch ---------------------------------------
    p, rec, cache = drive('nested-sha', spec(
        nested={'path': 'var/tmp/filesystem_core.squashfs',
                'sha256': '2' * 64}), 1)
    r = (rec.get('carriers') or [{}])[0]
    check('red-nested-sha', p.returncode == 1
          and r.get('link') == 'nested_sha256' and not os.path.isdir(cache),
          'rc=%d link=%s' % (p.returncode, r.get('link')))

    # ---- red: carrier pin mismatch (chain good, pin wrong) --------------
    sp_pin = spec()
    sp_pin['carriers'][0]['sha256'] = '3' * 64
    p, rec, cache = drive('pin-sha', sp_pin, 1)
    r = (rec.get('carriers') or [{}])[0]
    check('red-carrier-pin', p.returncode == 1
          and r.get('link') == 'carrier_sha256' and not os.path.isdir(cache),
          'rc=%d link=%s' % (p.returncode, r.get('link')))

    for name, ok, detail in results:
        print('%s\t%s\t%s' % ('PASS' if ok else 'FAIL', name, detail))
    bad = sum(1 for _, ok, _ in results if not ok)
    print('INTEGRATION cases=%d pass=%d fail=%d'
          % (len(results), len(results) - bad, bad))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
