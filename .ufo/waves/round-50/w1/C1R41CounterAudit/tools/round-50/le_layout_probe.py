#!/usr/bin/env python3
"""DRAFT (C1R41CounterAudit, round 50 wave 1): little-endian layout probe for P50-C1.

Port of tools/round-41/c1-counter.py `layout_probe` to the R50 layout as written in
plans/round-50-claims.md (layout_ok): little-endian `hsqs` magic, v4.0, compression id
4 (xz), mkfs_time == bytes_used (the AVM marker), 0 < bytes_used <= file size.
No metadata-header endianness test: standard LE and AVM-LE images share the LE header,
so that branch cannot discriminate (see the audit report, finding F-HDR).
Pure stdlib; reads bytes only. Exit codes are not used here (library + self-test).
"""
import json
import subprocess
import sys


def layout_probe_le(raw):
    d = {'size': len(raw) if raw is not None else 0}
    if raw is None:
        d.update(ok=False, reason='absent')
        return d
    if len(raw) < 96:
        d.update(ok=False, reason='shorter than a 96-byte superblock')
        return d
    le = lambda a, b: int.from_bytes(raw[a:b], 'little')
    d['magic'] = raw[0:4].decode('latin1')
    d['le_magic'] = raw[0:4] == b'hsqs'
    d['mkfs_time'] = le(8, 12)
    d['compression'] = le(20, 22)
    d['major'] = le(28, 30)
    d['minor'] = le(30, 32)
    d['bytes_used'] = le(40, 48)
    d['marker'] = d['mkfs_time'] == d['bytes_used']
    d['bytes_used_sane'] = 0 < d['bytes_used'] <= len(raw)
    d['version_v4'] = (d['major'], d['minor']) == (4, 0)
    d['comp_xz'] = d['compression'] == 4
    if not d['le_magic']:
        reason = 'magic %r is not little-endian hsqs' % (d['magic'],)
    elif not d['version_v4']:
        reason = 'version %d.%d is not 4.0' % (d['major'], d['minor'])
    elif not d['comp_xz']:
        reason = 'compression id %d is not 4 (xz)' % d['compression']
    elif not d['marker']:
        reason = 'AVM marker absent (mkfs_time %d != bytes_used %d)' % (
            d['mkfs_time'], d['bytes_used'])
    elif not d['bytes_used_sane']:
        reason = 'bytes_used %d outside 1..%d' % (d['bytes_used'], len(raw))
    else:
        reason = None
    d['ok'] = reason is None
    d['reason'] = reason
    return d


def self_test(member_path, be_image_path=None):
    """Run the probe on real bytes and on lane-built standard images. Returns a list of
    (case, ok_as_expected, probe_summary). Needs mksquashfs (squashfs-tools) on PATH."""
    import os
    import tempfile
    out = []
    raw = open(member_path, 'rb').read()
    out.append(('7530 member (vendor, untrimmed, 1031 trailing bytes)',
                layout_probe_le(raw), True))
    bu = int.from_bytes(raw[40:48], 'little')
    out.append(('7530 member carved to bytes_used', layout_probe_le(raw[:bu]), True))
    if be_image_path:
        out.append(('round-41 BE dev image (4096 B)',
                    layout_probe_le(open(be_image_path, 'rb').read()), False))
    scratch = os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')
    tmp = tempfile.mkdtemp(prefix='le-probe.', dir=scratch)
    src = os.path.join(tmp, 'src')
    os.makedirs(src)
    with open(os.path.join(src, 'hello.txt'), 'w') as fh:
        fh.write('hello\n' * 200)

    def mk(name, comp, epoch=None):
        p = os.path.join(tmp, name)
        env = dict(os.environ)
        env.pop('SOURCE_DATE_EPOCH', None)
        if epoch is not None:
            env['SOURCE_DATE_EPOCH'] = str(epoch)
        subprocess.run(['mksquashfs', src, p, '-comp', comp, '-noappend', '-quiet'],
                       check=True, env=env, capture_output=True)
        return open(p, 'rb').read()

    std_xz = mk('std-xz.sqsh', 'xz')
    out.append(('lane-built standard LE xz (real mkfs time)', layout_probe_le(std_xz), False))
    # forgery probe: the marker is a timestamp, and mksquashfs takes it from the environment
    forged = mk('forged-xz.sqsh', 'xz', epoch=int.from_bytes(std_xz[40:48], 'little'))
    out.append(('lane-built LE xz with SOURCE_DATE_EPOCH = bytes_used', layout_probe_le(forged),
                True))
    forged_gz = mk('forged-gz.sqsh', 'gzip',
                   epoch=int.from_bytes(mk('tmp-gz.sqsh', 'gzip')[40:48], 'little'))
    out.append(('lane-built LE gzip, marker forged (comp id 1 alone must fail)',
                layout_probe_le(forged_gz), False))
    return out


if __name__ == '__main__':
    member = sys.argv[1]
    be = sys.argv[2] if len(sys.argv) > 2 else None
    rows = []
    for name, probe, want in self_test(member, be):
        rows.append({'case': name, 'ok': probe['ok'], 'want_ok': want,
                     'match': probe['ok'] == want, 'reason': probe['reason'],
                     'mkfs_time': probe.get('mkfs_time'), 'bytes_used': probe.get('bytes_used'),
                     'compression': probe.get('compression'), 'size': probe.get('size')})
    print(json.dumps(rows, indent=1, sort_keys=True))
    sys.exit(0 if all(r['match'] for r in rows) else 1)
