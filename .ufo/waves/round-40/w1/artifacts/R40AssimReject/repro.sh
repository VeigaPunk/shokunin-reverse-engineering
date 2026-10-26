#!/usr/bin/env bash
# Rebuild the three development runs behind verdicts.md (R40AssimReject, round 40 wave 1).
# Inputs are read-only lane fixtures under /home/vgpnk/Projects/shokuknow (copied, never modified).
# Every output goes under $TMPDIR (default: a fresh mktemp dir). No REA run, no frozen carrier touched.
set -u
S="${1:-${TMPDIR:-}}"
if [ -z "$S" ]; then S=$(mktemp -d "${TMPDIR:-/tmp}/r40-assim.XXXXXX"); fi
mkdir -p "$S"/{runA,runB,runC}
UNBLOB=$HOME/.local/bin/unblob
W11=/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work
W13=/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work

cp "$W11/avm-be.squashfs"        "$S/dev-avm-be.squashfs"
cp "$W13/avm-le-genuine.squashfs" "$S/dev-avm-le-genuine.squashfs"

# Counterfactual: same bytes as the AVM-BE fixture with only the 4-byte marker field rewritten.
python3 - "$S/dev-avm-be.squashfs" "$S/dev-avm-be-nomarker.squashfs" <<'PY'
import struct, sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src, "rb").read())
mk = struct.unpack(">I", b[8:12])[0]
bu = struct.unpack(">Q", b[40:48])[0]
assert mk == bu, (mk, bu)                     # the source must carry the marker
b[8:12] = struct.pack(">I", 1792847340)       # a plausible timestamp: marker off
open(dst, "wb").write(bytes(b))
print("counterfactual: mkfs_time %d -> 1792847340, bytes_used %d" % (mk, bu))
PY

# unblob writes unblob.log into its cwd, so each run gets its own directory.
( cd "$S/runA" && "$UNBLOB" "$S/dev-avm-be.squashfs"         >/dev/null 2>&1; echo "A unblob_exit=$?" )
( cd "$S/runB" && "$UNBLOB" "$S/dev-avm-be-nomarker.squashfs" >/dev/null 2>&1; echo "B unblob_exit=$?" )
( cd "$S/runC" && "$UNBLOB" "$S/dev-avm-le-genuine.squashfs"  >/dev/null 2>&1; echo "C unblob_exit=$?" )

for r in runA runB runC; do
  echo "--- $r"
  grep -E "Found valid chunk|Running extract command|Extract command failed" "$S/$r/unblob.log" \
    | sed -E 's/^(.*\[)(debug|error) *(\].*command=.?)/\2 \3/'
  echo "    files=$(find "$S/$r" -mindepth 2 -type f 2>/dev/null | wc -l)"
done

# Direct extractor matrix (no unblob), to show the flag is what decides success.
cd "$S"
sasquatch-v4be -no-exit-code -f -d "$S/x1" "$S/dev-avm-be.squashfs"          >/dev/null 2>"$S/x1.err"; echo "v4be noflag on AVM-BE exit=$? files=$(find "$S/x1" -type f 2>/dev/null|wc -l)"
sasquatch-v4be -be        -f -d "$S/x2" "$S/dev-avm-be-nomarker.squashfs"    >/dev/null 2>"$S/x2.err"; echo "v4be -be    on no-marker exit=$? files=$(find "$S/x2" -type f 2>/dev/null|wc -l)"
sasquatch-v4be -no-exit-code -f -d "$S/x3" "$S/dev-avm-le-genuine.squashfs"  >/dev/null 2>"$S/x3.err"; echo "v4be noflag on LE       exit=$? files=$(find "$S/x3" -type f 2>/dev/null|wc -l)"
echo "x2.err: $(head -1 "$S/x2.err")"
echo "x3.err: $(tail -1 "$S/x3.err")"
echo "scratch: $S"
