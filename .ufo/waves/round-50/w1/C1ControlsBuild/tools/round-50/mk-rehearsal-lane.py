#!/usr/bin/env python3
"""Build a SMALL rehearsal lane for R50-C1 so the whole control pipeline runs in minutes.

The real carriers are 24-36 MB vendor images whose REA run needs ~50 s of 7 CPU-minutes
and trips REA 6.5.0's fixed 120 s deadline on a loaded host; every counter-time rerun is
that run again.  This tool builds four *synthetic* little-endian xz SquashFS v4 carriers
(host `mksquashfs` 4.7.5, `mkfs_time` patched to `bytes_used`, i.e. the AVM marker), with
regular files, relative symlinks, an absolute symlink, a link chain REA removes and an empty directory, commits them
into a throwaway `git clone --shared` of the lane as a stand-in freeze (carrier table,
gap rule, the counter under test at its frozen path, oracle tables, the carriers themselves at `<afterdir>/<id>/carrier.sqsh`), and
prints the freeze revision.  A counter, the controls driver and the positive control can
then run end to end against it.  Nothing here is vendor firmware and nothing here is the
round-50 evidence: it proves the PIPELINE, not the AVM images.

  mk-rehearsal-lane.py --lane CLONE --base-rev REV --counter PATH --gap-rule FILE \
                       --out DIR [--ids a7530,a7590,c6490,c6430]

The carrier table path, evidence dir and ids come from the counter's own constants (the
same AST scrape the driver uses).  Exit 0 and the new freeze on stdout; 2 on any failure.
"""
import argparse
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_driver():
    spec = importlib.util.spec_from_file_location('c1_controls', os.path.join(HERE, 'c1-controls.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_tree(root, seed):
    rng = random.Random(seed)
    os.makedirs(os.path.join(root, 'bin'))
    os.makedirs(os.path.join(root, 'etc'))
    os.makedirs(os.path.join(root, 'usr', 'lib'))
    os.makedirs(os.path.join(root, 'usr', 'www', 'cgi-bin'))
    os.makedirs(os.path.join(root, 'var', 'empty'))
    with open(os.path.join(root, 'bin', 'busybox'), 'wb') as fh:
        fh.write(bytes(rng.randrange(256) for _ in range(20000 + seed)))
    with open(os.path.join(root, 'etc', 'inittab'), 'w') as fh:
        fh.write('::sysinit:/etc/init.d/rcS # rehearsal carrier %d\n' % seed)
    with open(os.path.join(root, 'usr', 'lib', 'libfoo.so.1.0'), 'wb') as fh:
        fh.write(bytes(rng.randrange(256) for _ in range(3000)))
    with open(os.path.join(root, 'usr', 'www', 'cgi-bin', 'system_status'), 'w') as fh:
        fh.write('#!/bin/sh\necho %d\n' % seed)
    open(os.path.join(root, 'etc', 'empty.conf'), 'w').close()
    # the AVM-image shape REA's unblob removes: a chain of links ending at an absolute target
    # outside the tree (MaliciousSymlinkRemoved), as in a7530 `lib/libbroadbandcfg.so*`
    os.makedirs(os.path.join(root, 'lib'))
    os.symlink('/usr/share/ctlmgr/libx.so.1.0.0', os.path.join(root, 'lib', 'libx.so.1.0.0'))
    os.symlink('libx.so.1.0.0', os.path.join(root, 'lib', 'libx.so.1'))
    os.symlink('libx.so.1', os.path.join(root, 'lib', 'libx.so'))
    os.symlink('busybox', os.path.join(root, 'bin', 'ash'))
    os.symlink('libfoo.so.1.0', os.path.join(root, 'usr', 'lib', 'libfoo.so'))
    os.symlink('/usr/www/cgi-bin/system_status',
               os.path.join(root, 'usr', 'www', 'cgi-bin', 'status'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--base-rev', required=True)
    ap.add_argument('--counter', required=True)
    ap.add_argument('--gap-rule', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--ids')
    a = ap.parse_args()
    drv = load_driver()
    try:
        c = drv.consts(os.path.abspath(a.counter))
        k = drv.scrape(os.path.abspath(a.counter))
        ids = [x for x in (a.ids.split(',') if a.ids else list(k.get('IDS') or ())) if x]
        if not ids:
            raise drv.Uneval('no carrier ids (--ids, or an IDS constant in the counter)')
        for need in ('mksquashfs', 'unsquashfs'):
            if not shutil.which(need):
                raise drv.Uneval('%s not on PATH' % need)
        out = os.path.abspath(a.out)
        if os.path.isdir(out):
            shutil.rmtree(out)
        work = out + '.build'
        if os.path.isdir(work):
            shutil.rmtree(work)
        os.makedirs(work)
        p = subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--quiet',
                            os.path.abspath(a.lane), out], capture_output=True)
        if p.returncode:
            raise drv.Uneval('clone failed: ' + p.stderr.decode()[:200])
        drv.assert_toplevel(out)
        for key, val in (('user.name', 'r50-rehearsal'), ('user.email', 'rehearsal@r50.invalid'),
                         ('commit.gpgsign', 'false')):
            drv.git(out, 'config', key, val)
        drv.git(out, 'checkout', '--quiet', '--detach', a.base_rev)
        files, entries = {}, []
        for n, cid in enumerate(ids):
            src = os.path.join(work, 'src-' + cid)
            build_tree(src, 1000 + 7 * n)
            sq = os.path.join(work, cid + '.sqsh')
            r = subprocess.run(['mksquashfs', src, sq, '-comp', 'xz', '-noappend', '-all-root',
                                '-no-xattrs', '-b', '131072', '-quiet', '-mkfs-time', '1700000000'],
                               capture_output=True)
            if r.returncode:
                raise drv.Uneval('mksquashfs failed: ' + r.stderr.decode()[:200])
            with open(sq, 'rb') as fh:
                raw = bytearray(fh.read())
            used = int.from_bytes(raw[40:48], 'little')
            raw[8:12] = (used & 0xFFFFFFFF).to_bytes(4, 'little')   # the AVM marker
            carve = bytes(raw[:used])
            reg, non = drv.oracle_from_squashfs(work, carve)
            pin = drv.sha256_bytes(carve)
            base = '%s/%s' % (c['afterdir'], cid)
            files[base + '/carrier.sqsh'] = carve
            files[base + '/oracle.tsv'] = drv.tsv_bytes(reg)
            files[base + '/nonregular.tsv'] = drv.tsv_bytes(non)
            entries.append({'id': cid, 'sha256': pin, 'kind': 'lane-built',
                            'path': base + '/carrier.sqsh', 'oracle': base + '/oracle.tsv',
                            'nonregular': base + '/nonregular.tsv'})
        table = {'claim': 'R50-C1', 'target': len(entries), 'projection': 'plus-extractor',
                 'rea_parameters': {'max_depth': 1, 'max_output_bytes': 536870912,
                                    'max_output_files': 100000},
                 'note': 'REHEARSAL table: synthetic carriers, not the frozen vendor chain',
                 'carriers': entries}
        files[c['carriers']] = drv.jbytes(table)
        with open(a.gap_rule, 'rb') as fh:
            files[c['gaprule']] = fh.read()
        # the counter binds `running counter == tools/round-50/c1-counter.py at the freeze`
        with open(a.counter, 'rb') as fh:
            files['tools/round-50/c1-counter.py'] = fh.read()
        rev = drv.plant_and_commit(out, files, 'rehearsal freeze: synthetic LE AVM-marker carriers')
        shutil.rmtree(work, ignore_errors=True)
        print(json.dumps({'rehearsal_lane': out, 'freeze': rev, 'ids': ids,
                          'carriers': {e['id']: e['sha256'] for e in entries}}, sort_keys=True))
        return 0
    except drv.Uneval as e:
        print('could not build: %s' % e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
