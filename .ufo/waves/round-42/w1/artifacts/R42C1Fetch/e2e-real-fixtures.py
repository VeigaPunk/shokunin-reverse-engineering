#!/usr/bin/env python3
"""End-to-end drive of fetch-carrier.py over real SquashFS v3 test fixtures.

The fixtures are unblob 26.6.4 integration inputs (MIT, 129-byte git-LFS pointers in the
repo; fetched from media.githubusercontent.com).  They are *development* inputs: the
round-42 C1 carriers are published third-party images, which this drive never touches.

Each scenario builds a carriers.json around a real fixture, runs the tool exactly as a
frozen run would (`python3 -I -B <tool> --spec ... --cache ... --json-out ...`) and checks
the exit code, the named chain link and what landed in the cache.  Nothing is written
outside --scratch.

Usage:
  e2e-real-fixtures.py --tool <fetch-carrier.py> --fixtures DIR --scratch DIR

Exit 0 when every scenario agrees with its expectation.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import io

LE = 'squashfs_v3_le.bin'          # squashfs_v3/ddwrt little_endian fixture, 4096 B on disk
BE = 'squashfs_v3_be.lzma.bin'     # squashfs_v3_adaptive big_endian fixture, 4096 B
LFS_BASE = ('https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/'
            'tests/integration/filesystem/squashfs/')
URL_LE = LFS_BASE + 'squashfs_v3_ddwrt/little_endian/__input__/' + LE

CASES = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def record(name, ok, detail):
    CASES.append((name, ok, detail))
    print('%s\t%s\t%s' % ('PASS' if ok else 'FAIL', name, detail))


def cli(tool, argv, env=None, cwd=None):
    cmd = [sys.executable, '-I', '-B', tool] + argv
    p = subprocess.run(cmd, capture_output=True, env=env, cwd=cwd)
    print('  $ %s -> %d' % (' '.join(argv), p.returncode))
    return p


def receipt(path):
    with open(path) as fh:
        return json.load(fh)


def write_spec(path, carriers):
    with open(path, 'w') as fh:
        json.dump({'claim': 'R42-C1 (e2e)', 'carriers': carriers}, fh, indent=1)
        fh.write('\n')


def tar_bytes(items):
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode='w') as tf:
        for name, body in items:
            ti = tarfile.TarInfo(name)
            ti.size = len(body)
            tf.addfile(ti, io.BytesIO(body))
    return bio.getvalue()


def unsquashfs_lls(path):
    p = subprocess.run(['unsquashfs', '-lls', path], capture_output=True)
    return p.returncode, p.stdout.decode('utf-8', 'replace')


def sevenzip_list(path):
    p = subprocess.run(['7z', 'l', '-ba', path], capture_output=True)
    return p.returncode, p.stdout.decode('utf-8', 'replace')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tool', required=True)
    ap.add_argument('--fixtures', required=True)
    ap.add_argument('--scratch', required=True)
    a = ap.parse_args()
    tool = os.path.abspath(a.tool)
    fx = os.path.abspath(a.fixtures)
    base = os.path.abspath(a.scratch)
    le = open(os.path.join(fx, LE), 'rb').read()
    be = open(os.path.join(fx, BE), 'rb').read()
    carve_le, carve_be = le[:258], be[:256]
    pin_le, pin_be = sha(carve_le), sha(carve_be)
    image_le, image_be = sha(le), sha(be)

    work = os.path.join(base, 'work')
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ, TMPDIR=work)
    print('# fixtures  %s %d B sha256 %s' % (LE, len(le), image_le))
    print('# fixtures  %s %d B sha256 %s' % (BE, len(be), image_be))
    print('# carve     %d B pin %s / %d B pin %s' % (len(carve_le), pin_le,
                                                     len(carve_be), pin_be))

    # ---- scenario 1: no container, real HTTPS, carve drops the 4 KiB pad -------
    d = os.path.join(base, 's1')
    os.makedirs(d)
    cache, rec = os.path.join(d, 'cache'), os.path.join(d, 'rec.json')
    write_spec(os.path.join(d, 'carriers.json'), [{
        'id': 'LE-RAW', 'url': URL_LE, 'image_sha256': image_le,
        'carve': {'offset': 0, 'bytes_used': len(carve_le), 'sha256': pin_le}}])
    p = cli(tool, ['--spec', os.path.join(d, 'carriers.json'), '--cache', cache,
                   '--json-out', rec], env=env)
    got = receipt(rec)['carriers'][0] if os.path.isfile(rec) else {}
    entry = os.path.join(cache, pin_le + '.bin')
    ok = (p.returncode == 0 and got.get('ok') and got.get('fetch') == 'http 200'
          and os.path.isfile(entry) and sha_file(entry) == pin_le
          and os.path.getsize(entry) == len(carve_le)
          and not os.path.islink(entry))
    record('01-raw-https-carve-to-bytes_used', ok,
           'rc=%d fetch=%s entry=%d B %s' % (p.returncode, got.get('fetch'),
                                             os.path.getsize(entry)
                                             if os.path.exists(entry) else -1,
                                             sha_file(entry)[:16] if ok else 'n/a'))

    # ---- scenario 2: tar container + carve offset (boot header in front) ------
    member = b'H' * 512 + le + b'T' * 64
    image_tar = tar_bytes([('./tqsh.bin', member), ('./readme.txt', b'fixture\n')])
    d = os.path.join(base, 's2')
    os.makedirs(d)
    with open(os.path.join(d, 'image.tar'), 'wb') as fh:
        fh.write(image_tar)
    spec2 = os.path.join(d, 'carriers.json')
    write_spec(spec2, [{
        'id': 'LE-TAR', 'url': 'file://' + os.path.join(d, 'image.tar'),
        'image_sha256': sha(image_tar),
        'container': {'kind': 'tar', 'member': './tqsh.bin',
                      'member_sha256': sha(member)},
        'carve': {'offset': 512, 'bytes_used': len(carve_le), 'sha256': pin_le}}])
    cache, rec = os.path.join(d, 'cache'), os.path.join(d, 'rec.json')
    p = cli(tool, ['--spec', spec2, '--cache', cache, '--json-out', rec], env=env)
    got = receipt(rec)['carriers'][0] if os.path.isfile(rec) else {}
    entry2 = os.path.join(cache, pin_le + '.bin')
    ok = (p.returncode == 0 and got.get('ok')
          and got.get('container', {}).get('kind') == 'tar'
          and got.get('container', {}).get('member') == './tqsh.bin'
          and got.get('carve', {}).get('offset') == 512
          and sha_file(entry2) == pin_le)
    record('02-tar-container-carve-offset', ok,
           'rc=%d container=%s carve=%s entry %d B' %
           (p.returncode, got.get('container'), got.get('carve'),
            os.path.getsize(entry2) if os.path.exists(entry2) else -1))

    # ---- scenario 3: range container, second real fixture ---------------------
    junk = b'K' * 65536
    image_range = junk + be + b'END'
    d = os.path.join(base, 's3')
    os.makedirs(d)
    with open(os.path.join(d, 'kamikaze.img'), 'wb') as fh:
        fh.write(image_range)
    spec3 = os.path.join(d, 'carriers.json')
    write_spec(spec3, [{
        'id': 'BE-RANGE', 'url': 'file://' + os.path.join(d, 'kamikaze.img'),
        'image_sha256': sha(image_range),
        'container': {'kind': 'range', 'offset': len(junk), 'length': len(be),
                      'member_sha256': image_be},
        'carve': {'offset': 0, 'bytes_used': len(carve_be), 'sha256': pin_be}}])
    cache, rec = os.path.join(d, 'cache'), os.path.join(d, 'rec.json')
    p = cli(tool, ['--spec', spec3, '--cache', cache, '--json-out', rec], env=env)
    got = receipt(rec)['carriers'][0] if os.path.isfile(rec) else {}
    entry3 = os.path.join(cache, pin_be + '.bin')
    ok = (p.returncode == 0 and got.get('ok')
          and got.get('container', {}).get('kind') == 'range'
          and sha_file(entry3) == pin_be and os.path.getsize(entry3) == 256)
    record('03-range-container-second-fixture', ok,
           'rc=%d container=%s entry %d B' %
           (p.returncode, got.get('container'),
            os.path.getsize(entry3) if os.path.exists(entry3) else -1))

    # ---- scenario 4: carve pin off by one -> fail closed, nothing cached ------
    d = os.path.join(base, 's4')
    os.makedirs(d)
    bad = os.path.join(d, 'carriers.json')
    sp = json.load(open(spec2))
    sp['carriers'][0]['carve']['sha256'] = '0' * 64
    json.dump(sp, open(bad, 'w'))
    cache, rec = os.path.join(d, 'cache'), os.path.join(d, 'rec.json')
    p = cli(tool, ['--spec', bad, '--cache', cache, '--json-out', rec], env=env)
    got = receipt(rec)['carriers'][0] if os.path.isfile(rec) else {}
    listed = sorted(os.listdir(cache)) if os.path.isdir(cache) else []
    ok = (p.returncode == 1 and got.get('link') == 'carve_sha256' and listed == []
          and not os.path.isdir(cache))
    record('04-carve-pin-mismatch-fails-closed', ok,
           'rc=%d link=%s cache_dir_created=%s' %
           (p.returncode, got.get('link'), os.path.isdir(cache)))

    # ---- scenario 5: planted symlinks in the cache (round-41 D5) -------------
    d = os.path.join(base, 's5')
    os.makedirs(d)
    cache = os.path.join(d, 'cache')
    os.makedirs(cache)
    victim_a = os.path.join(d, 'victim-a.txt')
    victim_b = os.path.join(d, 'victim-b.txt')
    with open(victim_a, 'wb') as fh:
        fh.write(b'A' * 4096)
    with open(victim_b, 'wb') as fh:
        fh.write(b'B' * 4096)
    os.symlink(victim_a, os.path.join(cache, pin_le + '.bin'))
    os.symlink(victim_b, os.path.join(cache, pin_le + '.bin.part'))
    rec = os.path.join(d, 'rec.json')
    p = cli(tool, ['--spec', spec2, '--cache', cache, '--json-out', rec], env=env)
    got = receipt(rec)['carriers'][0] if os.path.isfile(rec) else {}
    entry = os.path.join(cache, pin_le + '.bin')
    ok = (p.returncode == 0 and got.get('cache_entry') == 'symlink-replaced'
          and not os.path.islink(entry) and sha_file(entry) == pin_le
          and open(victim_a, 'rb').read() == b'A' * 4096
          and open(victim_b, 'rb').read() == b'B' * 4096
          and os.path.islink(os.path.join(cache, pin_le + '.bin.part')))
    record('05-planted-cache-symlinks-not-written-through', ok,
           'rc=%d cache_entry=%s victim-a %d B victim-b %d B part_is_link=%s' %
           (p.returncode, got.get('cache_entry'),
            os.path.getsize(victim_a), os.path.getsize(victim_b),
            os.path.islink(os.path.join(cache, pin_le + '.bin.part'))))

    # ---- scenario 6: image cache round trip, second run offline ---------------
    d = os.path.join(base, 's6')
    os.makedirs(d)
    ic = os.path.join(d, 'imgcache')
    cache = os.path.join(d, 'cache')
    rec = os.path.join(d, 'rec.json')
    p1 = cli(tool, ['--spec', spec3, '--cache', cache, '--image-cache', ic,
                    '--json-out', rec], env=env)
    first = receipt(rec)['carriers'][0] if os.path.isfile(rec) else {}
    shutil.rmtree(cache)
    p2 = cli(tool, ['--spec', spec3, '--cache', cache, '--image-cache', ic,
                    '--json-out', rec], env=env)
    second = receipt(rec)['carriers'][0] if os.path.isfile(rec) else {}
    ok = (p1.returncode == 0 and p2.returncode == 0
          and first.get('fetch') == 'read' and second.get('fetch') == 'cache'
          and sha_file(os.path.join(cache, pin_be + '.bin')) == pin_be)
    record('06-image-cache-hit-second-run', ok,
           'first=%s second=%s rc=%d/%d' % (first.get('fetch'), second.get('fetch'),
                                            p1.returncode, p2.returncode))

    # ---- scenario 7: usage / environment exits are 2 ------------------------
    d = os.path.join(base, 's7')
    os.makedirs(d)
    with open(os.path.join(d, 'broken.json'), 'w') as fh:
        fh.write('{not json')
    cases = [
        ('no-cache', ['--spec', spec3], env),
        ('broken-spec', ['--spec', os.path.join(d, 'broken.json'), '--cache',
                         os.path.join(d, 'c1')], env),
        ('bogus-work', ['--spec', spec3, '--cache', os.path.join(d, 'c2'),
                        '--work', os.path.join(d, 'nope')], env),
        ('bogus-tmpdir', ['--spec', spec3, '--cache', os.path.join(d, 'c3'),
                          '--work', None], dict(os.environ, TMPDIR=os.path.join(d, 'nope'))),
        ('rev-injection', ['--root', d, '--rev', 'master:../../etc/passwd',
                           '--cache', os.path.join(d, 'c4')], env),
        ('rev-missing', ['--root', d, '--rev', 'deadbeef', '--cache',
                         os.path.join(d, 'c5')], env),
    ]
    bad = []
    for name, argv, e in cases:
        if argv[-1] is None:
            argv = argv[:-1]
        q = cli(tool, argv, env=e)
        if q.returncode != 2:
            bad.append('%s=%d' % (name, q.returncode))
        if '--cache' in argv and os.path.isdir(argv[argv.index('--cache') + 1]):
            bad.append('%s-created-cache' % name)
    record('07-exit-2-family', not bad, ','.join(bad) or 'all six exit 2, no cache dir')

    # ---- scenario 8: --root/--rev reads the frozen spec from git ------------
    d = os.path.join(base, 's8')
    os.makedirs(d)
    clone = os.path.join(d, 'lane')
    p = subprocess.run(['git', 'clone', '-q', '--shared',
                        '/home/vgpnk/Projects/shokunin/kaidoku-shokunin', clone],
                       capture_output=True)
    top = subprocess.run(['git', '-C', clone, 'rev-parse', '--show-toplevel'],
                         capture_output=True).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(clone), (top, clone)
    specdir = os.path.join(clone, '.ufo/waves/round-42/c1')
    os.makedirs(specdir, exist_ok=True)
    with open(os.path.join(specdir, 'carriers.json'), 'wb') as fh:
        fh.write(open(spec2, 'rb').read())
    subprocess.run(['git', '-C', clone, 'add', '.ufo/waves/round-42/c1/carriers.json'],
                   check=True, capture_output=True)
    subprocess.run(['git', '-C', clone, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                    'commit', '-q', '-m', 'fixture: r42 carriers spec'],
                   check=True, capture_output=True)
    rev = subprocess.run(['git', '-C', clone, 'rev-parse', 'HEAD'],
                         capture_output=True).stdout.decode().strip()
    cache = os.path.join(d, 'cache')
    rec = os.path.join(d, 'rec.json')
    p = cli(tool, ['--root', clone, '--rev', rev, '--cache', cache,
                   '--json-out', rec], env=env)
    entry = os.path.join(cache, pin_le + '.bin')
    ok = (p.returncode == 0 and os.path.isfile(entry) and sha_file(entry) == pin_le)
    record('08-rev-mode-committed-spec', ok,
           'rev=%s rc=%d entry=%s' % (rev[:12], p.returncode, sha_file(entry)[:16]
                                      if os.path.exists(entry) else 'absent'))

    # ---- scenario 9: the carve is the whole filesystem for both readers -----
    d = os.path.join(base, 's9')
    os.makedirs(d)
    le_carve = os.path.join(base, 's2', 'cache', pin_le + '.bin')
    be_carve = os.path.join(base, 's3', 'cache', pin_be + '.bin')
    report = []
    ok = True
    for label, carved, original in (('LE', le_carve, os.path.join(fx, LE)),
                                    ('BE-lzma', be_carve, os.path.join(fx, BE))):
        u_carve, u_orig = unsquashfs_lls(carved), unsquashfs_lls(original)
        z_carve, z_orig = sevenzip_list(carved), sevenzip_list(original)
        same_u = u_carve == u_orig
        same_7 = z_carve == z_orig
        ok = ok and same_u and same_7
        report.append('%s unsquashfs rc=%d/%d %s; 7z rc=%d/%d %s'
                      % (label, u_carve[0], u_orig[0], 'same' if same_u else 'DIFF',
                         z_carve[0], z_orig[0], 'same' if same_7 else 'DIFF'))
    record('09-carve-reads-as-the-whole-filesystem', ok, '; '.join(report))

    # ---- scenario 11: transport-level short read (Content-Length lies) ------
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Short(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith('/missing'):
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Length', '4096')
            self.end_headers()
            self.wfile.write(b'X' * 512)
            self.wfile.flush()
            self.close_connection = True

        def log_message(self, *a):
            pass

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Short)
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    try:
        d = os.path.join(base, 's11')
        os.makedirs(d)
        url = 'http://127.0.0.1:%d/image.bin' % srv.server_address[1]
        spec11 = os.path.join(d, 'carriers.json')
        write_spec(spec11, [{
            'id': 'SHORT', 'url': url, 'image_sha256': sha(b'X' * 4096),
            'carve': {'offset': 0, 'bytes_used': 16, 'sha256': sha(b'X' * 16)}}])
        cache, rec = os.path.join(d, 'cache'), os.path.join(d, 'rec.json')
        p = cli(tool, ['--spec', spec11, '--cache', cache, '--json-out', rec], env=env)
        got = receipt(rec)['carriers'][0] if os.path.isfile(rec) else {}
        ok = (p.returncode == 1 and got.get('link') == 'url'
              and 'short read' in (got.get('detail') or '')
              and not os.path.isdir(cache))
        record('11-http-short-read-is-a-url-link', ok,
               'rc=%d link=%s detail=%s' % (p.returncode, got.get('link'),
                                            (got.get('detail') or '')[:60]))
        spec11b = os.path.join(d, 'carriers404.json')
        write_spec(spec11b, [{
            'id': 'MISSING', 'url': 'http://127.0.0.1:%d/missing' % srv.server_address[1],
            'image_sha256': sha(b'y'), 'carve': {'offset': 0, 'bytes_used': 1,
                                                 'sha256': sha(b'y')}}])
        rec404 = os.path.join(d, 'rec404.json')
        p404 = cli(tool, ['--spec', spec11b, '--cache', os.path.join(d, 'cache404'),
                          '--json-out', rec404], env=env)
        got404 = receipt(rec404)['carriers'][0] if os.path.isfile(rec404) else {}
        ok404 = (p404.returncode == 1 and got404.get('link') == 'url'
                 and '404' in (got404.get('detail') or '')
                 and not os.path.isdir(os.path.join(d, 'cache404')))
    finally:
        srv.shutdown()
        srv.server_close()
    record('11b-http-404-is-a-url-link', ok404,
           'rc=%d link=%s detail=%s' % (p404.returncode, got404.get('link'),
                                        (got404.get('detail') or '')[:60]))

    # ---- scenario 12: relative --spec/--cache resolve against the cwd ------
    d = os.path.join(base, 's12')
    os.makedirs(d)
    with open(os.path.join(d, 'carriers.json'), 'wb') as fh:
        fh.write(open(spec3, 'rb').read())
    p = cli(tool, ['--spec', 'carriers.json', '--cache', 'rel/cache',
                   '--json-out', 'rec.json'], env=env, cwd=d)
    entry = os.path.join(d, 'rel', 'cache', pin_be + '.bin')
    ok = (p.returncode == 0 and os.path.isfile(entry) and sha_file(entry) == pin_be)
    record('12-relative-spec-and-cache', ok,
           'rc=%d entry=%s' % (p.returncode, sha_file(entry)[:16]
                               if os.path.exists(entry) else 'absent'))

    # ---- staging hygiene ---------------------------------------------------
    leftovers = [n for n in os.listdir(work) if n.startswith('fetch-carrier-')]
    record('13-no-staging-leftovers', not leftovers, ','.join(leftovers) or 'none in TMPDIR')

    total = len(CASES)
    passed = sum(1 for c in CASES if c[1])
    print('E2E cases=%d pass=%d fail=%d' % (total, passed, total - passed))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
