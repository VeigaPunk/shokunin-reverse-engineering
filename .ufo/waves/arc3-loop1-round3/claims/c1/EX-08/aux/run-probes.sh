#!/usr/bin/env bash
# EX-08 arc3-loop1-round3 probe runner. Pins: rea-agents 6.4.0 (core) + 6.7.0 (cross-pin attack).
# npx-cache binaries only — no install, no network. Disk-backed TMPDIR (host /tmp is EDQUOT).
set -u
EV=/var/tmp/ex08-r3/evidence
TMPDIR=/var/tmp/ex08-r3/tmp
export TMPDIR
REA640=/home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/rea-agents/scripts/rea.mjs
REA670=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs

probe() { # tag path enc bin
  local tag=$1 p=$2 enc=$3 rea=$4
  echo "== $tag [$enc @ $(basename $rea)] $(date -u +%H:%M:%SZ)"
  node "$rea" inspect-evm-interface "$p" "$enc" --format json > "$EV/$tag.json" 2> "$EV/$tag.err"
  echo $? > "$EV/$tag.exit"
  echo "   exit=$(cat $EV/$tag.exit) bytes=$(wc -c < $EV/$tag.json) err=$(wc -c < $EV/$tag.err)"
}

probe probe-CarrierB-runtime-hex-6.4.0 "$EV/CarrierB.runtime.hex" hex "$REA640"
probe probe-CarrierB-runtime-raw-6.4.0 "$EV/CarrierB.runtime.bin" raw "$REA640"
probe probe-CarrierBNoOpt-runtime-hex-6.4.0 "$EV/CarrierBNoOpt.runtime.hex" hex "$REA640"
probe probe-HarborLib-runtime-hex-6.4.0 "$EV/HarborLib.runtime.hex" hex "$REA640"
probe probe-CarrierB-runtime-hex-6.7.0 "$EV/CarrierB.runtime.hex" hex "$REA670"
echo "DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"