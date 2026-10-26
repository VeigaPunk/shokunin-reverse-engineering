#!/usr/bin/env python3
"""R39-C2 recon: deterministic development carriers for non-extractable
SquashFS-like inputs. Never used on held-out carriers; never touches K5/K6.

    python3 dev-carriers.py TREE_ROOT OUTDIR [--gen PATH]

Every carrier is (tree, endian, comp, mutation) with a deterministic recipe:
  - the tree is authored byte-for-byte by write_tree() (xorshift fill, fixed names)
  - the image comes from tools/round-37/gen-squashfs.py
  - each mutation is a pure function of the image bytes and its superblock
    bytes_used field (offset 40, uint64, endian-matched)

Prints a JSON manifest {id: {path, sha256, size, bytes_used, recipe, ...}}.
"""
import argparse
import hashlib
import json
import os
import struct
import subprocess
import sys

FILES = {
    'boot/cmdline.txt': b'console=ttyS0,115200 root=/dev/mtdblock3 rootfstype=squashfs\n',
    'boot/vmlinux.bin': None,      # 6000 bytes, xorshift
    'etc/config.ini': b'[net]\niface=eth0\ndhcp=1\n[log]\nlevel=info\n',
    'etc/conf.d/network.conf': b'NET_IFACE=eth0\nNET_DHCP=yes\n',
    'usr/bin/run': b'#!/bin/sh\nexec /bin/true\n',
    'usr/share/blob.bin': None,    # 20000 bytes, xorshift
}
SIZES = {'boot/vmlinux.bin': 6000, 'usr/share/blob.bin': 20000}
EMPTY_DIRS = ['empty']
HOST_ELF = b''          # set from --elf in main(); recorded by sha256 in the manifest


def xorshift(seed, n):
    out = bytearray()
    x = seed & 0xFFFFFFFF
    while len(out) < n:
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        out += struct.pack('<I', x)
    return bytes(out[:n])


def write_tree(root):
    if os.path.isdir(root):
        subprocess.run(['rm', '-rf', '--', root], check=True)
    os.makedirs(root)
    for rel, data in FILES.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if data is None:
            data = xorshift(0xC0FFEE + len(rel) * 7919, SIZES[rel])
        with open(p, 'wb') as f:
            f.write(data)
    for d in EMPTY_DIRS:
        os.makedirs(os.path.join(root, d), exist_ok=True)
    return {rel: hashlib.sha256((FILES[rel] if FILES[rel] is not None
                                 else xorshift(0xC0FFEE + len(rel) * 7919, SIZES[rel]))
                                ).hexdigest() for rel in FILES}


def bytes_used(img, endian):
    return struct.unpack(('>' if endian == 'be' else '<') + 'Q', img[40:48])[0]


def patch_bytes_used(img, endian, value):
    e = '>' if endian == 'be' else '<'
    return img[:40] + struct.pack(e + 'Q', value) + img[48:]


def prefix4k(img, endian):
    """4 KiB deterministic garbage prefix; the image chunk starts at 4096."""
    del endian
    pre = bytes(((i * 131 + 7) & 0xFF) for i in range(4096))
    assert img.startswith((b'hsqs', b'sqsh'))
    assert b'hsqs' not in pre and b'sqsh' not in pre
    return pre + img


def recipes():
    """(id, endian, comp, mutation) with mutation a function (img, endian)."""
    def trunc_half(img, endian):
        return img[:bytes_used(img, endian) // 2]

    def trunc_quarter(img, endian):
        return img[:bytes_used(img, endian) // 4]

    def trunc_3q(img, endian):
        return img[:bytes_used(img, endian) * 3 // 4]

    def trunc_minus1(img, endian):
        return img[:bytes_used(img, endian) - 1]

    def oversize_x2(img, endian):
        return patch_bytes_used(img, endian, len(img) * 2)

    def oversize_plus4096(img, endian):
        return patch_bytes_used(img, endian, len(img) + 4096)

    def oversize_plus1(img, endian):
        return patch_bytes_used(img, endian, len(img) + 1)

    def trunc_half_resized(img, endian):
        """Body cut to half, header amended so the declared extent fits."""
        cut = img[:bytes_used(img, endian) // 2]
        return patch_bytes_used(cut, endian, len(cut))

    def trailing4k(img, endian):
        del endian
        return img + bytes(((i * 197 + 29) & 0xFF) for i in range(4096))

    def elf_wrap(img, endian):
        del endian
        return HOST_ELF + img

    def elf_wrap_trunc(img, endian):
        return HOST_ELF + img[:bytes_used(img, endian) // 2]

    def prefix4k_trunc(img, endian):
        return prefix4k(img, endian)[:4096 + bytes_used(img, endian) // 2]

    return [
        ('be-base-gzip',       'be',  'gzip', None),
        ('be-trunc-half',      'be',  'gzip', trunc_half),
        ('be-trunc-quarter',   'be',  'gzip', trunc_quarter),
        ('be-trunc-3q',        'be',  'gzip', trunc_3q),
        ('be-trunc-minus1',    'be',  'gzip', trunc_minus1),
        ('be-prefix4k',        'be',  'gzip', prefix4k),
        ('be-oversize-x2',     'be',  'gzip', oversize_x2),
        ('be-oversize-plus4096','be', 'gzip', oversize_plus4096),
        ('be-oversize-plus1',  'be',  'gzip', oversize_plus1),
        ('be-base-xz',         'be',  'xz',   None),
        ('be-xz-trunc-half',   'be',  'xz',   trunc_half),
        ('le-base-gzip',       'le',  'gzip', None),
        ('le-trunc-half',      'le',  'gzip', trunc_half),
        ('le-oversize-x2',     'le',  'gzip', oversize_x2),
        ('le-prefix4k',        'le',  'gzip', prefix4k),
        ('be-xz-prefix4k',     'be',  'xz',   prefix4k),
        ('le-base-xz',         'le',  'xz',   None),
        ('be-trunc-half-resized', 'be', 'gzip', trunc_half_resized),
        ('be-trailing4k',      'be',  'gzip', trailing4k),
        ('be-elfwrap',         'be',  'gzip', elf_wrap),
        ('be-elfwrap-trunc',   'be',  'gzip', elf_wrap_trunc),
        ('be-prefix4k-trunc',  'be',  'gzip', prefix4k_trunc),
        ('le-prefix4k-trunc',  'le',  'gzip', prefix4k_trunc),
    ]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('tree_root')
    ap.add_argument('outdir')
    ap.add_argument('--gen', default=None)
    ap.add_argument('--elf', default='/bin/true')
    a = ap.parse_args(argv)
    global HOST_ELF
    with open(a.elf, 'rb') as f:
        HOST_ELF = f.read()
    gen = a.gen or os.path.join(
        '/home/vgpnk/Projects/shokunin/kaidoku-shokunin', 'tools/round-37/gen-squashfs.py')
    os.makedirs(a.outdir, exist_ok=True)
    tree = os.path.join(a.tree_root, 'devtree')
    tree_sha = write_tree(tree)
    manifest, builds = {}, []
    base_imgs = {}
    for cid, endian, comp, mut in recipes():
        key = (endian, comp)
        if key not in base_imgs:
            base = os.path.join(a.outdir, f'_base-{endian}-{comp}.img')
            cmd = [sys.executable, gen, tree, base, '--endian', endian, '--comp', comp]
            subprocess.run(cmd, check=True)
            with open(base, 'rb') as f:
                base_imgs[key] = f.read()
            builds.append({'id': f'_base-{endian}-{comp}', 'argv': cmd[1:]})
        img = base_imgs[key]
        out_img = img if mut is None else mut(img, endian)
        path = os.path.join(a.outdir, cid + ('.bin' if cid.endswith('prefix4k') or 'elfwrap' in cid else '.sqsh'))
        with open(path, 'wb') as f:
            f.write(out_img)
        bu = bytes_used(img, endian)
        decl = None
        try:
            decl = bytes_used(out_img, endian) if out_img[:4] in (b'hsqs', b'sqsh') else None
        except struct.error:
            decl = None
        manifest[cid] = {
            'path': path,
            'sha256': hashlib.sha256(out_img).hexdigest(),
            'size': len(out_img),
            'base_sha256': hashlib.sha256(img).hexdigest(),
            'endian': endian, 'comp': comp,
            'base_bytes_used': bu,
            'declared_bytes_used': decl,
            'recipe': ('base' if mut is None else mut.__name__),
            'chunk_offset': 4096 if mut is prefix4k else 0,
        }
    # Deterministic garbage control: no squashfs magic anywhere.
    garbage = xorshift(0xBADC0DE, 4096)
    gp = os.path.join(a.outdir, 'garbage-control.bin')
    with open(gp, 'wb') as f:
        f.write(garbage)
    manifest['garbage-control'] = {'path': gp, 'sha256': hashlib.sha256(garbage).hexdigest(),
                                   'size': len(garbage), 'recipe': 'xorshift(0xBADC0DE,4096)'}
    meta = {'tree': tree, 'tree_files_sha256': tree_sha,
            'host_elf': {'path': a.elf, 'sha256': hashlib.sha256(HOST_ELF).hexdigest(),
                         'size': len(HOST_ELF)},
            'carriers': manifest, 'builds': builds}
    mp = os.path.join(a.outdir, 'manifest.json')
    with open(mp, 'w') as f:
        json.dump(meta, f, indent=1, sort_keys=True)
    print(json.dumps(meta, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
