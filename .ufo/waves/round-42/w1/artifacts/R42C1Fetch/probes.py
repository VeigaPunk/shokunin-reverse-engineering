#!/usr/bin/env python3
"""Adversarial / scale probes for fetch-carrier.py, reproducible from a bare checkout.

Each probe builds its own inputs from a real SquashFS v3 fixture (unblob 26.6.4, MIT) and
drives the tool exactly as the CLI would.  Nothing is written outside --scratch.

  a  3 MiB carve offset inside a tar member (boot header in front of the rootfs)
  b  40 MiB flat image, range container at 40 MiB (memory must not scale with the image)
  c  4 concurrent CLI runs into one cache (no lock, no half-written entry)
  d  cache/<pin>.bin already a directory (stale cache dir must fail closed, not crash)
  e  cache/<pin>.bin planted as a hardlink (rename must detach, never write through)

Usage:
  probes.py --tool fetch-carrier.py --fixtures DIR --scratch DIR
"""
import argparse
import hashlib
import io
import json
import os
import resource
import shutil
import subprocess
import sys
import tarfile

RESULTS = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rec(name, ok, detail):
    RESULTS.append((name, ok))
    print('%s\t%s\t%s' % ('PASS' if ok else 'FAIL', name, detail))


def run(tool, spec, cache, recout, extra=None):
    return subprocess.run([sys.executable, '-I', '-B', tool, '--spec', spec,
                           '--cache', cache, '--json-out', recout] + list(extra or []),
                          capture_output=True)


def write(path, text):
    with open(path, 'w') as fh:
        fh.write(text)


def dump(path, obj):
    write(path, json.dumps(obj, indent=1) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tool', required=True)
    ap.add_argument('--fixtures', required=True)
    ap.add_argument('--scratch', required=True)
    a = ap.parse_args()
    tool, fx, base = os.path.abspath(a.tool), os.path.abspath(a.fixtures), os.path.abspath(a.scratch)
    os.makedirs(base, exist_ok=True)
    env = dict(os.environ, TMPDIR=base)
    os.environ['TMPDIR'] = base
    image = open(os.path.join(fx, 'squashfs_v3_le.bin'), 'rb').read()   # 4096 B, 258 used
    carve = image[:258]
    pin = sha(carve)

    # ---- a: 3 MiB offset inside a tar member -------------------------------
    d = os.path.join(base, 'a')
    os.makedirs(d)
    pad = hashlib.sha512(b'pad').digest() * (3 * 1024 * 1024 // 64)
    member = pad + image + b'\0' * 4096
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode='w') as tf:
        ti = tarfile.TarInfo('./ddwrt.bin')
        ti.size = len(member)
        tf.addfile(ti, io.BytesIO(member))
        ti2 = tarfile.TarInfo('./README')
        ti2.size = 5
        tf.addfile(ti2, io.BytesIO(b'note\n'))
    img = bio.getvalue()
    write(os.path.join(d, 'image.bin'), '')  # placeholder to create the file
    with open(os.path.join(d, 'image.bin'), 'wb') as fh:
        fh.write(img)
    spec = {'claim': 'R42-C1 (probe)', 'carriers': [{
        'id': 'BIG-OFFSET', 'url': 'file://' + os.path.join(d, 'image.bin'),
        'image_sha256': sha(img),
        'container': {'kind': 'tar', 'member': './ddwrt.bin',
                      'member_sha256': sha(member)},
        'carve': {'offset': len(pad), 'bytes_used': len(carve), 'sha256': pin}}]}
    dump(os.path.join(d, 'carriers.json'), spec)
    p = run(tool, os.path.join(d, 'carriers.json'), os.path.join(d, 'cache'),
            os.path.join(d, 'rec.json'))
    got = json.load(open(os.path.join(d, 'rec.json')))['carriers'][0]
    entry = os.path.join(d, 'cache', pin + '.bin')
    ok = (p.returncode == 0 and got['ok'] and os.path.isfile(entry)
          and sha(open(entry, 'rb').read()) == pin)
    rec('a-3MiB-carve-offset-tar', ok,
        'image=%d member=%d offset=%d rc=%d entry_sha=%s'
        % (len(img), len(member), len(pad), p.returncode,
           sha(open(entry, 'rb').read())[:16] if os.path.exists(entry) else 'absent'))

    # ---- b: 40 MiB flat image, range container -----------------------------
    # The image is streamed to disk one MiB at a time and never held in this process:
    # RUSAGE_CHILDREN counts the child's fork-time footprint, so a 40 MiB buffer here
    # would be charged to the tool and make the memory number meaningless.
    d = os.path.join(base, 'b')
    os.makedirs(d)
    img_path = os.path.join(d, 'flat.img')
    h = hashlib.sha256()
    chunk = b'\xa5' * (1024 * 1024)
    with open(img_path, 'wb') as fh:
        for _ in range(40):
            fh.write(chunk)
            h.update(chunk)
        fh.write(image)
        h.update(image)
        tail = b'\0' * 4096
        fh.write(tail)
        h.update(tail)
    flat_sha = h.hexdigest()
    flat_size = 40 * 1024 * 1024 + len(image) + 4096
    spec = {'claim': 'R42-C1 (probe)', 'carriers': [{
        'id': 'HUGE', 'url': 'file://' + img_path,
        'image_sha256': flat_sha,
        'container': {'kind': 'range', 'offset': 40 * 1024 * 1024, 'length': len(image),
                      'member_sha256': sha(image)},
        'carve': {'offset': 0, 'bytes_used': len(carve), 'sha256': pin}}]}
    dump(os.path.join(d, 'carriers.json'), spec)
    p = run(tool, os.path.join(d, 'carriers.json'), os.path.join(d, 'cache'),
            os.path.join(d, 'rec.json'))
    got = json.load(open(os.path.join(d, 'rec.json')))['carriers'][0]
    rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    entry = os.path.join(d, 'cache', pin + '.bin')
    ok = (p.returncode == 0 and got['ok'] and os.path.isfile(entry)
          and sha(open(entry, 'rb').read()) == pin)
    rec('b-40MiB-flat-range', ok, 'image=%d rc=%d max_child_rss=%d KiB (all children so far)'
        % (flat_size, p.returncode, rss))

    # ---- c: 4 concurrent runs into one cache -------------------------------
    d = os.path.join(base, 'c')
    os.makedirs(os.path.join(d, 'cache'), exist_ok=True)
    specp = os.path.join(base, 'a', 'carriers.json')
    procs = [subprocess.Popen([sys.executable, '-I', '-B', tool, '--spec', specp,
                               '--cache', os.path.join(d, 'cache'),
                               '--json-out', os.path.join(d, 'rec%d.json' % i)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
             for i in range(4)]
    rcs = [p.wait() for p in procs]
    listed = sorted(os.listdir(os.path.join(d, 'cache')))
    ok = (rcs == [0, 0, 0, 0] and listed == [pin + '.bin']
          and sha(open(os.path.join(d, 'cache', pin + '.bin'), 'rb').read()) == pin)
    rec('c-four-concurrent-runs', ok, 'rcs=%s cache=%s' % (rcs, ','.join(listed)))

    # ---- d: cache/<pin>.bin is a directory ---------------------------------
    d = os.path.join(base, 'd')
    os.makedirs(os.path.join(d, 'cache', pin + '.bin'))
    p = run(tool, specp, os.path.join(d, 'cache'), os.path.join(d, 'rec.json'))
    got = json.load(open(os.path.join(d, 'rec.json')))['carriers'][0]
    listed = sorted(os.listdir(os.path.join(d, 'cache')))
    ok = (p.returncode == 1 and got.get('link') == 'cache'
          and listed == [pin + '.bin']
          and os.path.isdir(os.path.join(d, 'cache', pin + '.bin')))
    rec('d-cache-entry-is-directory', ok, 'rc=%d link=%s cache=%s' %
        (p.returncode, got.get('link'), ','.join(listed)))

    # ---- e: cache/<pin>.bin planted as a hardlink --------------------------
    d = os.path.join(base, 'e')
    os.makedirs(os.path.join(d, 'cache'))
    victim = os.path.join(d, 'victim.txt')
    with open(victim, 'wb') as fh:
        fh.write(b'hardlink victim\n')
    os.link(victim, os.path.join(d, 'cache', pin + '.bin'))
    entry = os.path.join(d, 'cache', pin + '.bin')
    p = run(tool, specp, os.path.join(d, 'cache'), os.path.join(d, 'rec.json'))
    ok = (p.returncode == 0 and open(victim, 'rb').read() == b'hardlink victim\n'
          and os.stat(victim).st_nlink == 1
          and os.stat(entry).st_ino != os.stat(victim).st_ino
          and sha(open(entry, 'rb').read()) == pin)
    rec('e-cache-entry-hardlink-detached', ok,
        'rc=%d victim_nlink=%d entry_inode_differs=%s'
        % (p.returncode, os.stat(victim).st_nlink,
           os.stat(entry).st_ino != os.stat(victim).st_ino))

    leftovers = [n for n in os.listdir(base) if n.startswith('fetch-carrier-')]
    rec('f-no-staging-leftovers', not leftovers, ','.join(leftovers) or 'none')

    total = len(RESULTS)
    passed = sum(1 for _, ok in RESULTS if ok)
    print('PROBES cases=%d pass=%d fail=%d' % (total, passed, total - passed))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
