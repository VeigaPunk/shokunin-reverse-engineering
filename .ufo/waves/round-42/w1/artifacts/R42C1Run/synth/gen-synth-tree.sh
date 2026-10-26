#!/usr/bin/env bash
# Rebuild the R42C1Run many-symlink carrier (SquashFS v4 LE, gzip):
# 160 dirs x (4 regular files + 10 in-tree relative symlinks) = 640 regular files,
# 1600 symlinks, 160 dirs. Exact bytes: sha256 f342f747ce094e833740c45266fde158d1c21358963f44c0e3c499237004c99e,
# 188416 bytes. Requires mksquashfs 4.7.5.
set -euo pipefail
tree=${1:?usage: gen-synth-tree.sh TREE OUT.sqsh}
out=${2:?usage: gen-synth-tree.sh TREE OUT.sqsh}
rm -rf -- "$tree"; mkdir -p -- "$tree"
python3 -I - "$tree" <<'PY'
import hashlib, os, sys
root = sys.argv[1]
def stream(label, n):
    out = bytearray(); i = 0
    while len(out) < n:
        out += hashlib.sha256(('%s/%d' % (label, i)).encode()).digest(); i += 1
    return bytes(out[:n])
for d in range(160):
    dn = 'd%03d' % d
    for f in range(4):
        rel = '%s/f%02d' % (dn, f); p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(stream(rel, 256))
    for l in range(10):
        os.symlink('f00', os.path.join(root, '%s/l%02d' % (dn, l)))
PY
mksquashfs "$tree" "$out" -comp gzip -noappend -quiet
sha256sum "$out"
