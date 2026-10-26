#!/usr/bin/env python3
"""R42Simplify probe: two under-bindings of tools/round-41/c1-counter.py @ c4a38ea2.

Run:
  A=kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42Simplify
  git -C kaidoku-shokunin show c4a38ea2:tools/round-41/c1-counter.py > /tmp/c1.py
  python3 -I -B "$A/probe-c1.py" /tmp/c1.py

Proves, without REA/unblob:
  1. parse_oracle() drops the oracle's third column (size), and oracle_hits()
     counts a published file whose size is wrong but whose sha256 matches.
  2. layout_probe() is an AVM/v4-only superblock probe: it rejects a v3
     superblock structurally (v3 has no compression field; its field offsets
     from 32 on differ), so no v3 carrier can ever reach its marker or
     little-endian-metadata branches.
"""
import importlib.util
import sys


def load(path):
    spec = importlib.util.spec_from_file_location('c1', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    m = load(argv[1])
    sha = 'a' * 64
    rows, err = m.parse_oracle(('usr/info.txt\t%s\t999999\n' % sha).encode())
    print('parse_oracle rows =', rows, 'err =', err)
    print('row width kept =', len(rows[0]), '(rel, sha256) - size discarded')
    files = [('$output/firmware.bin_extract/usr/info.txt', sha, 1)]
    print('oracle_hits(wrong size, right sha) =',
          m.oracle_hits(rows, files, 'firmware.bin_extract'))

    sb = bytearray(96)
    sb[0:4] = b'hsqs'
    sb[28:30] = (3).to_bytes(2, 'little')
    print('layout_probe(v3 LE) =', {k: m.layout_probe(bytes(sb))[k] for k in
                                    ('magic', 'major', 'minor', 'version_v4',
                                     'ok', 'reason')})
    sb2 = bytearray(96)
    sb2[0:4] = b'sqsh'
    sb2[28:30] = (3).to_bytes(2, 'big')
    print('layout_probe(v3 BE) =', {k: m.layout_probe(bytes(sb2))[k] for k in
                                    ('magic', 'major', 'ok', 'reason')})
    print('v3 bytes[20:22] read as v4 `compression` =',
          int.from_bytes(bytes(sb)[20:22], 'big'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
