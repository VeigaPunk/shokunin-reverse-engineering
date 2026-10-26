#!/bin/sh
# build-dev-carriers.sh — rebuild every development carrier this seat used (R40C2ReconDomain).
#
# Development inputs only.  None of these is a C1 carrier and none is a held-out
# carrier; nothing here touches V1/V2 or the lane's frozen paths.
#
#   sh build-dev-carriers.sh <workdir>
#
# Carrier bytes are reproducible from this script: the blob is generated from a
# counter, not from /dev/urandom, and gen-squashfs.py stamps a fixed mkfs_time.
# Verified: two independent runs of the tree/clean + `--endian be --comp gzip`
# step both give sha256 78a078b6a587f4c416f5155545195e449012624a0569ac065bff54e2ce486058.
#
# CAVEAT: the envelopes committed in dev-envelopes/ were produced from an earlier
# build of the same trees whose single opaque blob came from /dev/urandom.  Their
# carrier sha256 are recorded in carriers.sha256; this script rebuilds a set that is
# *feature-equivalent*, not byte-equal, to those.  Each envelope's own subject digest
# is authoritative for what it measured.
set -eu
W=${1:?usage: build-dev-carriers.sh WORKDIR}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
GEN="$LANE/tools/round-39/gen-squashfs.py"
REA='npx -y rea-agents@6.5.0'
mkdir -p "$W"
cd "$W"

mkblob() { python3 -c 'import sys;n=int(sys.argv[1]);sys.stdout.buffer.write(bytes((i*37+11)%256 for i in range(n)))' "$1"; }

# --- tree A: clean, four entries -------------------------------------------------
mkdir -p tree/clean/sub/deep
printf 'alpha\n' > tree/clean/a.txt
mkblob 4096 > tree/clean/sub/b.bin
printf 'gamma\n' > tree/clean/sub/deep/c.txt

python3 "$GEN" tree/clean car-be-gzip.sqsh --endian be  --comp gzip
python3 "$GEN" tree/clean car-le-gzip.sqsh --endian le  --comp gzip
python3 "$GEN" tree/clean car-avm-gzip.sqsh --endian avm --comp gzip

# --- trees 1..3: three different carriers per endian, for the determinism probe ---
for i in 1 2 3; do
  mkdir -p "treedet/t$i/dir-$i/empty"
  printf 'file-%s\n' "$i" > "treedet/t$i/f$i.txt"
  mkblob $((1000 + i * 777)) > "treedet/t$i/dir-$i/blob$i.bin"
  printf 'nested %s\n' "$i" > "treedet/t$i/dir-$i/empty/x.log"
  for e in be le; do
    python3 "$GEN" "treedet/t$i" "car-$i-$e.sqsh" --endian "$e" --comp gzip
  done
done

# --- a non-squashfs blob, for the in-domain no-squashfs-chunk contrast -------------
mkblob 8192 > blob-random.bin

# --- the zip-wrapped carrier (second out-of-domain shape) --------------------------
mkdir -p wrap && cp car-be-gzip.sqsh wrap/ && (cd wrap && zip -q ../wrap-be.zip car-be-gzip.sqsh)

# --- REA runs ---------------------------------------------------------------------
# unblob path is only needed by extract-firmware; inspect-firmware-regions needs no
# REA_UNBLOB_COMMAND (measured: identical features with the variable unset).
export REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob"

# in-domain: extract-firmware always needs an ABSENT output directory.
$REA extract-firmware --format json --full-output car-be-gzip.sqsh  out/ef-be
$REA extract-firmware --format json --full-output car-le-gzip.sqsh  out/ef-le
$REA extract-firmware --format json --full-output car-avm-gzip.sqsh out/ef-avm
$REA extract-firmware --format json --full-output blob-random.bin   out/ef-none

# out-of-domain, primary: a non-extract-firmware operation on the same carriers.
for i in be le; do
  $REA inspect-firmware-regions --format json --full-output "car-$i-gzip.sqsh"
done
for i in 1 2 3; do for e in be le; do
  $REA inspect-firmware-regions --format json --full-output "car-$i-$e.sqsh"
done; done

# out-of-domain, secondary: a non-extract-firmware operation on a wrapped carrier.
$REA inspect-artifact --format json --full-output wrap-be.zip

# format-gated operations: every one exits 1 with no `data` object on a SquashFS blob.
for op in inspect-artifact extract-artifact inspect-binary-layout analyze inspect \
          inspect-go-binary inspect-rust-binary inspect-wasm-artifact inspect-plist \
          inspect-sqlite-database inspect-managed-artifact inspect-managed-members \
          inspect-managed-native-boundaries inspect-native-dispatch-metadata \
          inspect-native-load-image inspect-pe-resources inspect-macho \
          inspect-signature inspect-keyed-archive inspect-asset-catalog \
          inspect-dart-aot inspect-electron-fuses inspect-electron-page \
          inspect-evm-interface inspect-pcap-capture decode-android-resources \
          decode-interface-builder identify-flutter-build demangle-swift \
          inspect-recorded-crash list-architectures; do
  $REA "$op" --format json --full-output car-be-gzip.sqsh || true
  $REA "$op" --format json --full-output car-le-gzip.sqsh  || true
done
