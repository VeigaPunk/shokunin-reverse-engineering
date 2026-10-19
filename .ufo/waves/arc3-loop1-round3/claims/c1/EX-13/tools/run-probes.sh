#!/bin/bash
# EX-13 probe runner — cached rea-agents binaries (no install, no network).
# Usage: run-probes.sh
set -u
OUT=/var/tmp/ex13/probes
mkdir -p "$OUT"
export TMPDIR=/var/tmp/ex13/tmp
REA640=/home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/rea-agents/scripts/rea.mjs
REA670=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs

run() { # $1=version-tag $2=rea path $3=carrier path
  local tag="$1"; shift
  local rea="$1"; shift
  local carrier="$1"; shift
  local base; base=$(basename "$carrier" .hex)
  local out="$OUT/${base}.${tag}.json"
  node "$rea" inspect-evm-interface "$carrier" hex --format json > "$out" 2>"$out.err"
  echo "$tag $base exit=$? out=$(wc -c < "$out")B"
}

echo "== rea.mjs identities =="
sha256sum "$REA640" "$REA670"

C=/var/tmp/ex13/out
for tag_rea in "6.4.0:$REA640" "6.7.0:$REA670"; do
  tag="${tag_rea%%:*}"; rea="${tag_rea#*:}"
  for f in rv2-off-Rv2Token.runtime rv2-on200-Rv2Token.runtime \
           tre-off-Treasury.runtime tre-on200-Treasury.runtime \
           gau-off-Gauge.runtime gau-on200-Gauge.runtime \
           sw8-off.runtime sw8-on200.runtime \
           sw16-off.runtime sw16-on200.runtime \
           sw32-off.runtime sw32-on200.runtime; do
    if [ "$tag" = "6.7.0" ]; then
      case "$f" in
        rv2-on200-Rv2Token.runtime|tre-on200-Treasury.runtime|gau-on200-Gauge.runtime|sw32-on200.runtime) ;;
        *) continue ;;
      esac
    fi
    run "$tag" "$rea" "$C/$f.hex"
  done
done
echo "== done =="