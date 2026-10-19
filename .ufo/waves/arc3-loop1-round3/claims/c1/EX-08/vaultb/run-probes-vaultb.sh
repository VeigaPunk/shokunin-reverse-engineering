#!/usr/bin/env bash
# EX-08 seat (arc3-loop1-round3, chain c1) — chain carrier B (VaultB, EX-04-authored)
# probe legs on the pin EX-04 left unexamined: rea-agents@6.7.0.
# Carrier bytes: EX-04's pinned runtime files, identity re-derived before use
# (opt200 bin sha256 aaf85cea..., noopt bin 679678e9...).
# No installs: the npx-cache rea.mjs for 6.7.0 is invoked directly (no network).
# Disk-backed TMPDIR required on this host (/tmp quota EDQUOT - r1 entry).
set -u
EV=/var/tmp/ex08-r3/evidence
TMPDIR=/var/tmp/ex08-r3/tmp
export TMPDIR
REA670=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin

# identity of the EX-04 carrier files this seat probed (re-derived at read)
sha256sum "$REPO/.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-opt200.bin" \
          "$REPO/.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-noopt.bin"

probe() { # tag path enc
  node "$REA670" inspect-evm-interface "$2" "$3" --format json > "$EV/$1.json" 2> "$EV/$1.err"
  echo $? > "$EV/$1.exit"
  echo "$1 exit=$(cat $EV/$1.exit) bytes=$(wc -c < "$EV/$1.json") err=$(wc -c < "$EV/$1.err")"
}
probe probe-VaultB-opt200-hex-6.7.0 "$EV/carrierB.runtime-opt200.hex" hex
probe probe-VaultB-opt200-raw-6.7.0 "$EV/carrierB.runtime-opt200.bin" raw
probe probe-VaultB-noopt-hex-6.7.0 "$EV/carrierB.runtime-noopt.hex" hex
probe probe-VaultB-trap-raw-on-hexfile-6.7.0 "$EV/carrierB.runtime-opt200.hex" raw
probe probe-VaultB-rerun-a-hex-6.7.0 "$EV/carrierB.runtime-opt200.hex" hex
echo "DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"