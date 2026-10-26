#!/usr/bin/env bash
# R36-C1 carrier harness: one REA extract-firmware run (before|after) or the
# independent unsquashfs oracle for one carrier. Writes only under OUTDIR and a
# private scratch dir (SCRATCH, default $HYAKU_SCRATCH/kaidoku-r36/c1-run.XXXX).
#
#   c1-run.sh before|after CARRIER OUTDIR [SCRATCH]
#     before: PATH with every directory holding a `sasquatch` executable removed
#     after:  PATH as given; `sasquatch` must resolve
#     writes OUTDIR/<mode>.json (REA --format json envelope) and OUTDIR/<mode>-run.json
#   c1-run.sh oracle CARRIER OUTDIR [SCRATCH]
#     unsquashfs (squashfs-tools, /usr/bin) at the squashfs offset; offset 0 for a
#     bare image, ELF end (e_shoff + e_shnum*e_shentsize) for an AppImage.
#     writes OUTDIR/oracle.tsv (relpath TAB sha256 TAB size, regular files, sorted)
#     and OUTDIR/oracle-run.json
#
# REA pin: rea-agents@6.5.0 (lane carrier pin). REA_UNBLOB_COMMAND defaults to
# ~/.local/bin/unblob. Exit 0 ok, 2 usage/environment error, 3 tool failure.
set -euo pipefail
mode=${1:-}; carrier=${2:-}; outdir=${3:-}
[[ $mode =~ ^(before|after|oracle)$ && -f $carrier && -n $outdir ]] || { echo "usage: $0 before|after|oracle CARRIER OUTDIR [SCRATCH]" >&2; exit 2; }
carrier=$(realpath "$carrier"); mkdir -p "$outdir"; outdir=$(realpath "$outdir")
root=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r36
mkdir -p "$root"
scratch=${4:-$(mktemp -d "$root/c1-run.XXXXXX")}
mkdir -p "$scratch"
trap 'rm -rf -- "$scratch"' EXIT
export TMPDIR=$scratch
sha=$(sha256sum "$carrier" | cut -d' ' -f1)
now=$(date -u +%FT%TZ)

if [[ $mode == oracle ]]; then
  off=$(python3 -I - "$carrier" <<'PY'
import struct, sys
b = open(sys.argv[1], 'rb').read(64)
if b[:4] == b'hsqs':
    print(0)
elif b[:4] == b'\x7fELF' and b[4] == 2 and b[5] == 1:
    shoff, = struct.unpack_from('<Q', b, 0x28)
    shentsize, shnum = struct.unpack_from('<HH', b, 0x3a)
    print(shoff + shentsize * shnum)
else:
    sys.exit('unsupported carrier header')
PY
)
  magic=$(dd if="$carrier" bs=1 skip="$off" count=4 status=none)
  [[ $magic == hsqs ]] || { echo "no hsqs magic at offset $off" >&2; exit 3; }
  /usr/bin/unsquashfs -no-progress -o "$off" -d "$scratch/root" "$carrier" > "$scratch/unsquashfs.log" 2>&1 || { cat "$scratch/unsquashfs.log" >&2; exit 3; }
  python3 -I - "$scratch/root" > "$outdir/oracle.tsv" <<'PY'
import hashlib, os, sys
root = sys.argv[1]
rows = []
for d, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(d, f)
        if os.path.islink(p) or not os.path.isfile(p):
            continue
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        rows.append((os.path.relpath(p, root), h, os.path.getsize(p)))
for r in sorted(rows):
    print(f'{r[0]}\t{r[1]}\t{r[2]}')
PY
  jq -n --arg c "$carrier" --arg s "$sha" --arg t "$now" --argjson o "$off" \
    --arg v "$(/usr/bin/unsquashfs -version 2>&1 | sed -n 1p)" \
    --arg n "$(wc -l < "$outdir/oracle.tsv")" \
    '{mode:"oracle",carrier:$c,carrier_sha256:$s,utc:$t,squashfs_offset:$o,unsquashfs:$v,regular_files:($n|tonumber)}' > "$outdir/oracle-run.json"
  exit 0
fi

path=$PATH
if [[ $mode == before ]]; then
  path=$(python3 -I -c 'import os,sys; print(":".join(d for d in sys.argv[1].split(":") if d and not os.access(os.path.join(d,"sasquatch"), os.X_OK)))' "$PATH")
  if PATH=$path command -v sasquatch >/dev/null; then echo "sasquatch still on PATH" >&2; exit 2; fi
else
  command -v sasquatch >/dev/null || { echo "sasquatch not on PATH" >&2; exit 2; }
fi
sq=$(PATH=$path command -v sasquatch || true)
sqsha=""; sqver=""
if [[ -n $sq ]]; then sqsha=$(sha256sum "$sq" | cut -d' ' -f1); sqver=$("$sq" -version 2>&1 | sed -n 1p || true); fi
export REA_UNBLOB_COMMAND=${REA_UNBLOB_COMMAND:-$HOME/.local/bin/unblob}
set +e
PATH=$path timeout 900 npx -y rea-agents@6.5.0 extract-firmware --format json "$carrier" "$scratch/out" > "$outdir/$mode.json" 2> "$scratch/rea.err"
rc=$?
set -e
jq -n --arg m "$mode" --arg c "$carrier" --arg s "$sha" --arg t "$now" --argjson rc "$rc" \
  --arg sq "$sq" --arg sqsha "$sqsha" --arg sqver "$sqver" --arg u "$REA_UNBLOB_COMMAND" \
  --arg err "$(grep -v 'npm warn' "$scratch/rea.err" | cut -c1-400 | sed -n 1,20p)" \
  '{mode:$m,carrier:$c,carrier_sha256:$s,utc:$t,rea:"rea-agents@6.5.0",exit:$rc,sasquatch:$sq,sasquatch_sha256:$sqsha,sasquatch_version:$sqver,unblob:$u,stderr_head:$err}' > "$outdir/$mode-run.json"
[[ $rc == 0 ]] || exit 3
