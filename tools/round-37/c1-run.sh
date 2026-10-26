#!/usr/bin/env bash
# R37-C1 carrier harness: one REA extract-firmware run (before|after) for one
# big-endian SquashFS v4 carrier. Writes only under OUTDIR and a private
# scratch dir (SCRATCH, default $HYAKU_SCRATCH/kaidoku-r37/c1-run.XXXX).
#
#   c1-run.sh before|after K OUTDIR [SCRATCH]
#     before: PATH with every directory holding a `sasquatch` or
#             `sasquatch-v4be` executable removed
#     after:  PATH as given; `sasquatch-v4be` must resolve
#     K is a carrier id from corpus/evidence/round-37/c1/carriers.json
#     writes OUTDIR/<mode>.json (REA --format json envelope) and
#     OUTDIR/<mode>-run.json
#
# REA pin: rea-agents@6.5.0 (lane carrier pin). REA_UNBLOB_COMMAND defaults to
# ~/.local/bin/unblob. Exit 0 ok, 2 usage/environment error, 3 tool failure.
set -euo pipefail
mode=${1:-}; k=${2:-}; outdir=${3:-}
lane=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
carriers="$lane/corpus/evidence/round-37/c1/carriers.json"
[[ $mode =~ ^(before|after)$ && -n $k && -n $outdir ]] || { echo "usage: $0 before|after K OUTDIR [SCRATCH]" >&2; exit 2; }
carrier=$(python3 -I - "$carriers" "$k" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
k = sys.argv[2]
if k not in d:
    sys.exit(f"unknown carrier {k}")
print(f"{sys.argv[1].rsplit('/carriers.json', 1)[0]}/{d[k]['file']}")
PY
)
[[ -f $carrier ]] || { echo "missing carrier $carrier" >&2; exit 2; }
mkdir -p "$outdir"; outdir=$(realpath "$outdir")
root=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r37
mkdir -p "$root"
scratch=${4:-$(mktemp -d "$root/c1-run.XXXXXX")}
mkdir -p "$scratch"
trap 'rm -rf -- "$scratch"' EXIT
export TMPDIR=$scratch
sha=$(sha256sum "$carrier" | cut -d' ' -f1)
now=$(date -u +%FT%TZ)

path=$PATH
if [[ $mode == before ]]; then
  path=$(python3 -I -c 'import os,sys; print(":".join(d for d in sys.argv[1].split(":") if d and not os.access(os.path.join(d,"sasquatch"), os.X_OK) and not os.access(os.path.join(d,"sasquatch-v4be"), os.X_OK)))' "$PATH")
  if PATH=$path command -v sasquatch-v4be >/dev/null; then echo "sasquatch-v4be still on PATH" >&2; exit 2; fi
else
  command -v sasquatch-v4be >/dev/null || { echo "sasquatch-v4be not on PATH" >&2; exit 2; }
fi
sq=$(PATH=$path command -v sasquatch-v4be || true)
sqsha=""; sqver=""
if [[ -n $sq ]]; then sqsha=$(sha256sum "$sq" | cut -d' ' -f1); sqver=$("$sq" -version 2>&1 | sed -n 1p || true); fi
export REA_UNBLOB_COMMAND=${REA_UNBLOB_COMMAND:-$HOME/.local/bin/unblob}
set +e
PATH=$path timeout 900 npx -y rea-agents@6.5.0 extract-firmware --format json "$carrier" "$scratch/out" > "$outdir/$mode.json" 2> "$scratch/rea.err"
rc=$?
set -e
rea_root=$(realpath -m ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents 2>/dev/null || echo unknown)
jq -n --arg m "$mode" --arg k "$k" --arg c "$carrier" --arg s "$sha" --arg t "$now" --argjson rc "$rc" \
  --arg sq "$sq" --arg sqsha "$sqsha" --arg sqver "$sqver" --arg u "$REA_UNBLOB_COMMAND" \
  --arg rr "$rea_root" \
  --arg err "$(grep -v 'npm warn' "$scratch/rea.err" | cut -c1-300 | sed -n 1,10p)" \
  '{mode:$m,carrier_id:$k,carrier:$c,carrier_sha256:$s,utc:$t,rea:"rea-agents@6.5.0",exit:$rc,sasquatch_v4be:$sq,sasquatch_v4be_sha256:$sqsha,sasquatch_v4be_version:$sqver,unblob:$u,rea_package_root:$rr,stderr_head:$err}' > "$outdir/$mode-run.json"
[[ $rc == 0 ]] || exit 3
