#!/usr/bin/env python3
"""avm-mode-gate -- a fixture writer mode named for the AVM layout must emit that layout.

Round-39: `tools/round-39/gen-squashfs.py --endian avm` is byte-identical to `--endian be`
with bytes 8..12 overwritten by `bytes_used` (`.ufo/waves/round-39/w1/R39AssimAvmCritic.md`:
0 differing bytes, sha256 762c06a6...). Its metadata block-length headers are written with
`struct.pack('>H', ...)` because `pack(e, ...)` maps 'avm' to big-endian. The genuine AVM
layout is a big-endian superblock with LITTLE-endian metadata block-length headers (Freetz;
S114). So the mode's name advertises a capability the writer does not have, and any carrier
built with it silently tests the marker transform instead of the layout.

Rule: for every `--endian` choice whose name contains "avm", build a tiny fresh tree, generate
an image, read the 2-byte metadata block header at inode_table_start, and require the
little-endian decode to be the plausible one (0 < len <= 8192) and the big-endian decode not
to be. Also report the marker state (mkfs_time == bytes_used) so "marker present" cannot be
mistaken for "layout present".

Exit 0 pass; 1 findings; 2 usage. Red on tools/round-39/gen-squashfs.py; green on
gen-squashfs-avm-mode-fixed.py (this dir), whose avm mode writes little-endian block headers.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

META_MAX = 8192


def choices(text):
    match = re.search(r'--endian[^\n]*?choices\s*=\s*\[([^\]]*)\]', text)
    if not match:
        return []
    return re.findall(r"['\"]([^'\"]+)['\"]", match.group(1))


def plausible(value):
    return 0 < value <= META_MAX


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--gen', required=True, help='gen-squashfs.py style writer')
    ap.add_argument('--comp', default='gzip', choices=('gzip', 'xz'))
    ap.add_argument('--work', default=os.environ.get('TMPDIR') or tempfile.gettempdir())
    args = ap.parse_args(argv)

    try:
        text = open(args.gen, encoding='utf-8').read()
    except OSError as exc:
        print(f'USAGE {exc}', file=sys.stderr)
        return 2
    modes = [m for m in choices(text) if 'avm' in m.lower()]
    if not modes:
        print(f'{args.gen}: no --endian choice claims the AVM layout; nothing to verify')
        return 0

    work = tempfile.mkdtemp(prefix='avm-mode-', dir=os.path.abspath(args.work))
    findings = []
    try:
        tree = os.path.join(work, 'tree')
        os.makedirs(os.path.join(tree, 'etc'))
        os.makedirs(os.path.join(tree, 'bin'))
        with open(os.path.join(tree, 'bin', 'run'), 'w', encoding='utf-8') as fh:
            fh.write('#!/bin/sh\necho hi\n')
        with open(os.path.join(tree, 'etc', 'a.txt'), 'w', encoding='utf-8') as fh:
            fh.write('hello avm\n')
        for mode in modes:
            out = os.path.join(work, f'probe-{mode}.sqsh')
            proc = subprocess.run([sys.executable, '-I', '-B', args.gen, tree, out,
                                   '--endian', mode, '--comp', args.comp],
                                  capture_output=True, text=True)
            if proc.returncode != 0 or not os.path.exists(out):
                findings.append(f'mode {mode!r}: writer failed exit {proc.returncode} '
                                f'{proc.stderr.strip()[:120]}')
                continue
            blob = open(out, 'rb').read()
            if blob[:4] not in (b'sqsh', b'hsqs'):
                findings.append(f'mode {mode!r}: magic {blob[:4]!r} is not squashfs')
                continue
            inode_table_start = int.from_bytes(blob[64:72], 'big')
            mkfs = int.from_bytes(blob[8:12], 'big')
            bytes_used = int.from_bytes(blob[40:48], 'big')
            hdr = blob[inode_table_start:inode_table_start + 2]
            raw = int.from_bytes(hdr, 'big')
            le = (int.from_bytes(hdr, 'little') & 0x7fff)
            be = (raw & 0x7fff)
            state = 'LE' if plausible(le) and not plausible(be) else (
                'BE' if plausible(be) and not plausible(le) else 'AMBIGUOUS')
            print(f'mode {mode!r}: marker={mkfs == bytes_used} mkfs={mkfs} '
                  f'bytes_used={bytes_used} hdr={hdr.hex()} len LE={le} BE={be} -> {state}')
            if state != 'LE':
                findings.append(f'mode {mode!r} claims the AVM layout but its metadata block '
                                f'length decodes {state} (LE={le}, BE={be}); a carrier built '
                                f'with it tests the marker, not the layout')
    finally:
        shutil.rmtree(work, ignore_errors=True)

    for f in findings:
        print(f'FINDING {f}')
    print(f'gen={args.gen} avm_modes={modes} findings={len(findings)}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
