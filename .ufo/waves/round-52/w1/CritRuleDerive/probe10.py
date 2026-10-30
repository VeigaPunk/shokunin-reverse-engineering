#!/usr/bin/env python3
"""Probe 10: can `unsquashfs -lln` re-derive the NON-REGULAR census (F7)?

The claims require the v2 counter to "re-derive the non-regular census at
score time with the frozen reader/`unsquashfs -lln` and require the frozen
`*.nonregular.tsv` row sets in both directions".

This probe builds a synthetic little-endian SquashFS v4 image that CONTAINS a
char-device, a fifo and a socket (via the lane's own tools/round-41/sqfs-list.py
image builder), then runs `unsquashfs -lln` on it and asks:
  * does -lln list the device/fifo/socket rows at all?
  * does it print the major:minor detail the frozen table's third column holds?
  * does the row set match the frozen table's shape (rel TAB kind TAB detail)?
No REA, no network, no lane write.
"""
import importlib.util, os, subprocess, sys, tempfile, shutil

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SCRATCH = os.path.dirname(os.path.abspath(__file__))

spec = importlib.util.spec_from_file_location('sqfsl', os.path.join(LANE, 'tools/round-41/sqfs-list.py'))
sq = importlib.util.module_from_spec(spec); spec.loader.exec_module(sq)

tree = [
    {'path': 'bin/ash', 'type': 'symlink', 'target': 'busybox'},
    {'path': 'bin/busybox', 'type': 'file', 'data': b'ELF' + b'\x00' * 500},
    {'path': 'dev', 'type': 'dir'},
    {'path': 'dev/led', 'type': 'char-device', 'rdev': (247, 0)},
    {'path': 'dev/pts/0', 'type': 'char-device', 'rdev': (136, 0)},
    {'path': 'run/pipe0', 'type': 'fifo'},
    {'path': 'run/sock0', 'type': 'socket'},
]

work = tempfile.mkdtemp(prefix='lln-', dir=SCRATCH)
try:
    img = os.path.join(work, 'img.sqsh')
    with open(img, 'wb') as fh:
        fh.write(sq._build_image(tree, endian='le', comp='gzip'))
    print('built image', os.path.getsize(img), 'bytes')

    print('\n== unsquashfs -lln output (verbatim)')
    p = subprocess.run(['/usr/bin/unsquashfs', '-lln', img],
                       capture_output=True, text=True)
    print('exit', p.returncode)
    print(p.stdout[:3000])
    if p.stderr.strip():
        print('stderr:', p.stderr[:600])

    print('\n== does the listing name the device/fifo/socket rows?')
    out = p.stdout
    for want in ('led', 'pts/0', 'pipe0', 'sock0'):
        print(f'   contains {want!r}: {want in out}')
    print('   contains "247" (the major):', '247' in out)
    print('   contains "136":', '136' in out)
    print('   contains "char":', 'char' in out.lower())
    print('   contains "fifo":', 'fifo' in out.lower())
    print('   contains "socket":', 'socket' in out.lower())

    print('\n== the lane reader (tools/round-41/sqfs-list.py) on the same image')
    rows, nonreg, meta = sq._read_image(img, layout='le')
    print('   nonregular rows:', nonreg)
finally:
    shutil.rmtree(work, ignore_errors=True)

print('\n== what the FROZEN committed table shape is (g7581 device rows)')
raw = open(f'{LANE}/tools/round-50/oracle/g7581.nonregular.tsv').read().splitlines()
for line in raw:
    if 'char-device' in line or line.startswith('dev/pts'):
        print('   ', line)
