#!/bin/sh
# build.sh -- exact reproduction of every development carrier and REA run in
# this seat's round-40 wave-1 C2 recon.  Development inputs only: three fresh
# trees authored here, an empty-directory tree, and one development image; no
# vendor image, no C1 carrier, no C2 held-out carrier is built or run.
#
#   S   scratch root (default /fast/scratch/hyaku/kaidoku-r40/R40C2ReconPartial)
#   A   this artifacts directory (default: next to this script)
#   L   lane root
#
# Every `python3` call here is run with -B (no .pyc into the lane) and every
# REA/unblob run happens with cwd inside $S, so no log lands in the lane.
set -eu
S=${S:-/fast/scratch/hyaku/kaidoku-r40/R40C2ReconPartial}
A=${A:-$(cd "$(dirname "$0")" && pwd)}
L=${L:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
GEN=$L/tools/round-39/gen-squashfs.py
ORACLE=$L/tools/round-39/sqfs-list.py

mkdir -p "$S"/{trees,img,corrupt,env,oracle,run}
export TMPDIR=$S A

# --- 1. source trees (compressible bodies; the recipe needs compressed data blocks)
for t in t1 t2 t3; do
  python3 -B "$A/make-tree.py" "$S/trees/$t" "r40-partial-$t"
done
mkdir -p "$S/trees/empty/onlydir" "$S/trees/one" "$S/trees/rawtail"
# one-file tree (class boundary: P=1 is still P>0) and a tree whose last file is
# incompressible (raw data blocks), so the recipe has to fall back to an earlier file
python3 -B - "$S/trees" <<'EOF'
import hashlib, os, sys
root = sys.argv[1]
stream = b''.join(hashlib.sha256(b'one#%d' % i).digest() for i in range(200))
open(os.path.join(root, 'one', 'only.txt'), 'wb').write((b'alpha bravo charlie delta ' * 400 * 3)[:6000])
open(os.path.join(root, 'rawtail', 'aaa.txt'), 'wb').write((b'kilo lima juliet ' * 300)[:2400])
open(os.path.join(root, 'rawtail', 'zzz.bin'), 'wb').write(stream[:9000])
EOF

# --- 2. images: 3 trees x {be,le} x {gzip,xz}, plus one empty-dir BE image
for t in t1 t2 t3; do
  for e in be le; do
    for c in gzip xz; do
      python3 -B "$GEN" "$S/trees/$t" "$S/img/$t-$e-$c.sqfs" --endian $e --comp $c
    done
  done
done
python3 -B "$GEN" "$S/trees/empty" "$S/img/empty-be-gzip.sqfs" --endian be --comp gzip
python3 -B "$GEN" "$S/trees/one" "$S/img/one-be-gzip.sqfs" --endian be --comp gzip
python3 -B "$GEN" "$S/trees/rawtail" "$S/img/rawtail-be-gzip.sqfs" --endian be --comp gzip

# --- 3. parser cross-check: my reader vs the independent lane oracle
for f in "$S"/img/*.sqfs; do
  b=$(basename "$f" .sqfs)
  python3 -B "$ORACLE" "$f" --files "$S/oracle/$b.files.tsv" \
    --symlinks "$S/oracle/$b.links.tsv" > /dev/null
  python3 -B "$A/sqfs-corrupt.py" "$f" --verify-trees "$S/trees/$(basename "$b" | cut -d- -f1)"
done
python3 -B "$A/cross-check.py" "$S/img" "$S/oracle"

# --- 4. damage recipes
for f in "$S"/img/{t1,t2,t3}-*.sqfs; do
  b=$(basename "$f" .sqfs)
  python3 -B "$A/sqfs-corrupt.py" "$f" --corrupt partial \
    --out "$S/corrupt/$b-partial.sqfs"
done
# one-file image: the recipe's own >=2-file guard is bypassed inline (see report §3.4)
python3 -B - "$S" <<'EOF'
import importlib.util, os, sys
S = sys.argv[1]
spec = importlib.util.spec_from_file_location('sq', os.path.join(os.environ['A'], 'sqfs-corrupt.py'))
sq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sq)
buf = open(os.path.join(S, 'img', 'one-be-gzip.sqfs'), 'rb').read()
img = sq.Image(buf)
target = img.files()[0]
block = [b for b in target['blocks'] if b['compressed']][-1]
out = bytearray(buf)
out[block['offset']:block['offset'] + block['length']] = b'\xff' * block['length']
open(os.path.join(S, 'corrupt', 'one-be-gzip-partial.sqfs'), 'wb').write(bytes(out))
EOF
for spec in "t1-be-gzip zero-id-table" "t1-le-gzip zero-id-table" \
            "t1-be-xz zero-id-table" "t1-le-xz zero-id-table" \
            "t2-be-gzip zero-id-table" "t1-be-gzip bad-minor"; do
  set -- $spec
  python3 -B "$A/sqfs-corrupt.py" "$S/img/$1.sqfs" --corrupt "$2" \
    --out "$S/corrupt/$1-$2.sqfs"
done

# --- 5. REA 6.5.0 extract-firmware on every carrier (never on C1/hold-out inputs)
run() { sh "$A/runrea.sh" "$1" "$2" "$S/env/$1.json"; }
for f in "$S"/corrupt/*.sqfs; do
  run "$(basename "$f" .sqfs)" "$f"
done
run t1-be-gzip-clean  "$S/img/t1-be-gzip.sqfs"
run t3-be-xz-clean    "$S/img/t3-be-xz.sqfs"
run empty-be-gzip-clean "$S/img/empty-be-gzip.sqfs"
run one-be-gzip-partial "$S/corrupt/one-be-gzip-partial.sqfs"
run rawtail-be-gzip-partial "$S/corrupt/rawtail-be-gzip-partial.sqfs"
run t1-be-gzip-partial-repeat "$S/corrupt/t1-be-gzip-partial.sqfs"

# --- 6. direct extractor probes (fill-pattern choice) and feature tables
python3 -B "$A/probe-fills.py" "$S/img/t1-be-gzip.sqfs" --be || true
python3 -B "$A/probe-fills.py" "$S/img/t1-le-xz.sqfs" --le || true
python3 -B "$A/feat.py" --table "$A/tables/feature-table.md" \
  "$A/tables/features.json" "$S"/env/*.json
python3 -B "$A/sqfs-triage-v2-dev.py" --selftest
