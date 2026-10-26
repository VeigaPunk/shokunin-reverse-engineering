#!/bin/sh
# R39-C1 carrier K6 — standard big-endian SquashFS v4, xz, 4096-byte blocks.
#
# Authors a fresh tree (deterministic bytes, fixed seeds), writes the
# independent oracle (oracle.tsv: regular files; symlinks.tsv: link table),
# then builds the image with the round-37 generator:
#   gen-squashfs.py TREE OUT --endian be --comp xz
#
# usage: ./build.sh [TREE] [OUT]
#   TREE default <script dir>/src   OUT default <script dir>/carrier.sqsh
#   GEN  overrides the generator path.
# The build is deterministic: same TREE bytes -> same image bytes.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TREE=${1:-$here/src}
OUT=${2:-$here/carrier.sqsh}
GEN=${GEN:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-37/gen-squashfs.py}

case $TREE in
  /|.|..|"") echo "build.sh: refusing unsafe TREE '$TREE'" >&2; exit 2 ;;
esac

rm -rf -- "$TREE"
mkdir -p -- "$TREE"

python3 - "$TREE" "$here/oracle.tsv" "$here/symlinks.tsv" <<'PY'
import hashlib
import os
import posixpath
import random
import sys

tree, oracle_path, links_path = sys.argv[1], sys.argv[2], sys.argv[3]

# Content: fixed, deterministic. blob.bin is 13579 bytes = 4 x 4096-byte
# blocks (3 full + 1291), i.e. strictly more than two blocks, from seed 39.
FILES = {
    'bin/tool.sh': b'#!/bin/sh\necho k6-tool\n',
    'etc/config.ini': b'[k6]\nmode = carrier\nendian = big\ncompression = xz\n',
    'a/b/note.txt': b'note: two levels down\n',
    'data/manifest.txt': b'blob.bin 13579\n',
    'docs/deep/notes.txt': b'deep notes\n',
    'var/log/app.log': b'2026-10-26 boot k6\n',
}
BLOB_LEN = 13579
BLOB_SEED = 39
LINKS = {
    # exactly one in-tree link: two directories up (a/b -> root) and back down
    'a/b/link-in': '../../etc/config.ini',
    # exactly two escaping links: one shallow, one deep
    'outside': '../outside',
    'data/escape-deep': '../../../../etc/passwd',
}

rnd = random.Random(BLOB_SEED)
FILES['data/blob.bin'] = bytes(rnd.getrandbits(8) for _ in range(BLOB_LEN))

for rel, data in FILES.items():
    p = os.path.join(tree, rel)
    os.makedirs(os.path.dirname(p) or tree, exist_ok=True)
    with open(p, 'wb') as f:
        f.write(data)
for rel, target in LINKS.items():
    p = os.path.join(tree, rel)
    os.makedirs(os.path.dirname(p) or tree, exist_ok=True)
    os.symlink(target, p)

# Safety: a link target that resolves to a live host directory would make the
# generator's os.walk descend into the host filesystem. Refuse such a tree.
for rel, target in LINKS.items():
    p = os.path.join(tree, rel)
    if os.path.isdir(p):  # isdir() follows the link
        sys.exit('build.sh: symlink %s resolves to a host directory' % rel)

# Symlinks must contain no absolute target.
for rel, target in LINKS.items():
    if target.startswith('/'):
        sys.exit('build.sh: absolute symlink target at %s' % rel)

def classify(rel, target):
    """POSIX resolve of target against the link's own directory in the image."""
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(rel), target))
    return 'escaping' if (resolved == '..' or resolved.startswith('../')
                          or resolved.startswith('/')) else 'in-tree'

rows = []
for root, dnames, fnames in os.walk(tree):
    dnames.sort()
    for name in fnames:
        p = os.path.join(root, name)
        if os.path.islink(p):
            continue
        data = open(p, 'rb').read()
        rel = os.path.relpath(p, tree).replace(os.sep, '/')
        rows.append('%s\t%s\t%d' % (rel, hashlib.sha256(data).hexdigest(), len(data)))
rows.sort()
with open(oracle_path, 'w') as f:
    f.write('\n'.join(rows) + '\n')

links = sorted((rel, target) for rel, target in LINKS.items())
with open(links_path, 'w') as f:
    for rel, target in links:
        f.write('%s\t%s\t%s\n' % (rel, target, classify(rel, target)))

print('authored %d regular files, %d symlinks under %s' % (len(rows), len(links), tree))
PY

python3 "$GEN" "$TREE" "$OUT" --endian be --comp xz

# Image truth: the generator only ever sees what os.walk yields, so an entry it
# never yields (e.g. a symlink whose target is a directory lands in dnames and
# is never reached by the islink branch) would be dropped silently. Re-extract
# the built image with sasquatch-v4be - the same binary and argv unblob's
# SquashFSExtractor uses for a non-AVM big-endian v4 image - and assert the
# extracted inventory equals the tables derived from the tree. Never REA/unblob.
python3 - "$OUT" "$here/oracle.tsv" "$here/symlinks.tsv" <<'PY'
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

carrier, oracle, links = sys.argv[1:4]
tmp = tempfile.mkdtemp(prefix='k6-image-truth.')
try:
    out = os.path.join(tmp, 'x')
    os.makedirs(out)
    r = subprocess.run(['sasquatch-v4be', '-be', '-no-exit-code', '-f',
                        '-d', out, carrier], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('build.sh: sasquatch-v4be failed on %s (exit %d): %s'
                 % (carrier, r.returncode, r.stderr.strip()))

    files, got_links, others = {}, {}, []
    for root, dnames, fnames in os.walk(out):
        dnames.sort()
        for name in fnames + dnames:
            p = os.path.join(root, name)
            rel = os.path.relpath(p, out).replace(os.sep, '/')
            if os.path.islink(p):
                got_links[rel] = os.readlink(p)
            elif os.path.isfile(p):
                data = open(p, 'rb').read()
                files[rel] = (hashlib.sha256(data).hexdigest(), len(data))
            elif not os.path.isdir(p):
                others.append(rel)

    want_files = {}
    for line in open(oracle):
        rel, sha, size = line.rstrip('\n').split('\t')
        want_files[rel] = (sha, int(size))
    want_links = {}
    for line in open(links):
        rel, target, _cls = line.rstrip('\n').split('\t')
        want_links[rel] = target

    bad = []
    for rel in sorted(set(want_files) | set(files)):
        if want_files.get(rel) != files.get(rel):
            bad.append('file %s: table=%r image=%r'
                       % (rel, want_files.get(rel), files.get(rel)))
    for rel in sorted(set(want_links) | set(got_links)):
        if want_links.get(rel) != got_links.get(rel):
            bad.append('link %s: table=%r image=%r'
                       % (rel, want_links.get(rel), got_links.get(rel)))
    if others:
        bad.append('non-regular entries: %r' % (others,))
    if bad:
        sys.exit('build.sh: built image disagrees with the tables\n  '
                 + '\n  '.join(bad))
    print('image truth: %d regular files, %d symlinks match the tables'
          % (len(files), len(got_links)))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
PY

sha256sum "$OUT"
