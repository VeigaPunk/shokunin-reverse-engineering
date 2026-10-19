#!/usr/bin/env bash
# selectors-crosscheck.sh — seat EX-05 (chain c1, arc3-loop1-round4).
#
# Computes keccak256(sig)[:4] for every signature in a signature list with
# FOUR independent implementations and asserts pairwise agreement:
#   A. js-sha3@0.8.0 (round-1 receipted prefix)         [required by seat line]
#   B. node:crypto 'keccak-256' (OpenSSL-backed)
#   C. openssl dgst -keccak-256 (OpenSSL CLI)
#   D. pure-Python keccak_ref.py (seat-local, no deps)
#
# usage: selectors-crosscheck.sh <siglist.txt> <outdir>
# siglist: one signature per line; '#' comments and blank lines ignored.
set -u

SIGLIST="$1"
OUTDIR="$2"
SEATDIR="$(cd "$(dirname "$0")" && pwd)"
PREFIX=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix

mkdir -p "$OUTDIR"

echo "# selectors-crosscheck.sh — EX-05 round4" > "$OUTDIR/crosscheck.txt"
echo "# siglist: $SIGLIST (sha256 $(sha256sum "$SIGLIST" | cut -d' ' -f1))" >> "$OUTDIR/crosscheck.txt"
echo "# js-sha3 tree: $PREFIX/node_modules/js-sha3/src/sha3.js (sha256 $(sha256sum "$PREFIX/node_modules/js-sha3/src/sha3.js" | cut -d' ' -f1))" >> "$OUTDIR/crosscheck.txt"
echo "# keccak_ref.py: $SEATDIR/keccak_ref.py (sha256 $(sha256sum "$SEATDIR/keccak_ref.py" | cut -d' ' -f1))" >> "$OUTDIR/crosscheck.txt"
echo "#" >> "$OUTDIR/crosscheck.txt"
printf '%-46s %-10s %-10s %-10s %-10s %s\n' SIG js-sha3 node-crypto openssl py-ref AGREE >> "$OUTDIR/crosscheck.txt"

fails=0
count=0
while IFS= read -r sig; do
  case "$sig" in ''|'#'*) continue ;; esac
  count=$((count+1))
  A=$(node -e "
    const s3=require('$PREFIX/node_modules/js-sha3/src/sha3.js');
    process.stdout.write(s3.keccak256(process.argv[1]).slice(0,8));
  " "$sig")
  B=$(node -e "
    const c=require('crypto');
    process.stdout.write(c.createHash('keccak-256').update(process.argv[1],'utf8').digest('hex').slice(0,8));
  " "$sig")
  C=$(printf '%s' "$sig" | openssl dgst -keccak-256 | awk '{print substr($NF,1,8)}')
  D=$(python3 "$SEATDIR/keccak_ref.py" --sel "$sig" | cut -c1-8)
  if [ "$A" = "$B" ] && [ "$B" = "$C" ] && [ "$C" = "$D" ]; then AGREE=YES; else AGREE="NO"; fails=$((fails+1)); fi
  printf '%-46s %-10s %-10s %-10s %-10s %s\n' "$sig" "$A" "$B" "$C" "$D" "$AGREE" >> "$OUTDIR/crosscheck.txt"
done < "$SIGLIST"

echo "#" >> "$OUTDIR/crosscheck.txt"
echo "# signatures checked: $count | disagreements: $fails" >> "$OUTDIR/crosscheck.txt"
cat "$OUTDIR/crosscheck.txt"
exit "$fails"
