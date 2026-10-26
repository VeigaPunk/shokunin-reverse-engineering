#!/bin/bash
# dev-build.sh OUTDIR — build the eight round-39 w1 development carriers for the C2 triage recon.
#
# Everything is derived from fresh trees in OUTDIR with the lane's minimal writer
# (tools/round-37/gen-squashfs.py); no committed carrier and no held-out material is read.
# GEN may override the writer path.
#
# Carriers (sha256 of the copies retained in ./dev-carriers):
#   C-clean-be.sqsh     standard big-endian v4, no symlinks            -> clean
#   C-clean-le.sqsh     standard little-endian v4, no symlinks         -> dep-missing-le with PATH stripped
#   C-intree-be.sqsh    BE v4 with an in-tree symlink var/lib/run-link -> in-tree-symlink-metadata
#   C-escape-be.sqsh    BE v4 with an escaping symlink escape-link     -> escaping-symlink-removed
#   C-avm-be.sqsh       BE v4 with mkfs_time := bytes_used (AVM mark)  -> avm-marker-be-dropped
#   C-bodyfail-be.sqsh  BE v4 with the inode-table head XOR 0xff       -> body-extractor-failure
#   C-nochunk.bin       sixty lines of ASCII prose, no filesystem      -> no-squashfs-chunk
#
# Symlink-boundary probes (see features-dev.tsv and the round-39 w1 report):
#   C-abs-escape-be.sqsh  link target /etc/passwd, absolute            -> KEPT (unpublished-entry)
#   C-abs-intree-be.sqsh  link target /hello.txt, absolute             -> KEPT (unpublished-entry)
#   C-climb-be.sqsh       a/b/climb-link -> ../../../hello.txt          -> REMOVED (MaliciousSymlinkRemoved)
# Absolute targets never escape: fix_symlink lstrips the leading slash and only checks the
# relative remainder against the chunk extraction directory, so it is always inside.
set -eu

OUT=${1:?usage: dev-build.sh OUTDIR}
GEN=${GEN:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-37/gen-squashfs.py}
mkdir -p "$OUT"
cd "$OUT"

mkdir -p t-clean/bin t-clean/docs/deep/nested
printf 'hello world\n' > t-clean/hello.txt
printf '#!/bin/sh\necho hi\n' > t-clean/bin/run
printf 'readme\n' > t-clean/docs/readme.md
printf 'binary\x00data\x01\n' > t-clean/docs/deep/nested/file.dat

rm -rf t-intree t-escape
cp -r t-clean t-intree
mkdir -p t-intree/var/lib
printf 'd\n' > t-intree/var/lib/data.bin
ln -s ../../bin/run t-intree/var/lib/run-link

cp -r t-clean t-escape
ln -s ../../outside/secret t-escape/escape-link

python3 "$GEN" t-clean        C-clean-be.sqsh    --endian be --comp gzip
python3 "$GEN" t-clean        C-clean-le.sqsh    --endian le --comp gzip
python3 "$GEN" t-intree       C-intree-be.sqsh   --endian be --comp gzip
python3 "$GEN" t-escape       C-escape-be.sqsh   --endian be --comp gzip
python3 "$GEN" t-clean        C-avm-be.sqsh      --endian avm --comp gzip
python3 "$GEN" t-clean        C-bodyfail-be.sqsh --endian be --comp gzip

# body damage: keep the standard BE superblock (mkfs_time != bytes_used) and destroy the
# head of the inode table, so the extractor is reached with -be and fails on the body.
python3 - "$PWD/C-bodyfail-be.sqsh" <<'PY'
import struct, sys
path = sys.argv[1]
b = bytearray(open(path, 'rb').read())
fields = struct.unpack('>4sIIIIHHHHHHQQQQQQQQ', bytes(b[:96]))
assert fields[0] == b'sqsh', 'not a big-endian v4 superblock'
assert fields[2] != fields[12], 'superblock must not carry the AVM marker'
inode_start = fields[13]
for i in range(inode_start, min(inode_start + 24, len(b))):
    b[i] ^= 0xFF
open(path, 'wb').write(bytes(b))
print('patched inode table head at', inode_start)
PY

printf 'not a filesystem at all\n%.0s' $(seq 1 20) > C-nochunk.bin

rm -rf t-abs-escape t-abs-intree t-climb
cp -r t-clean t-abs-escape
ln -s /etc/passwd t-abs-escape/abs-escape-link
cp -r t-clean t-abs-intree
ln -s /hello.txt t-abs-intree/abs-intree-link
cp -r t-clean t-climb
mkdir -p t-climb/a/b
ln -s ../../../hello.txt t-climb/a/b/climb-link

python3 "$GEN" t-abs-escape C-abs-escape-be.sqsh --endian be --comp gzip
python3 "$GEN" t-abs-intree C-abs-intree-be.sqsh --endian be --comp gzip
python3 "$GEN" t-climb      C-climb-be.sqsh      --endian be --comp gzip

sha256sum C-*.sqsh C-nochunk.bin
