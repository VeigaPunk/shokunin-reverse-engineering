#!/usr/bin/env bash
# RV-1 r3 — batch recompute of every round-3 c1 carrier found on disk.
# Each leg: path A + B + C over the carrier SOURCE, reconciled against the
# seat's planted artifact and (where present) the seat's runtime bytes.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=$R/.ufo/waves/arc3-loop1-round3/claims/c1
O=/var/tmp/rv1-r3/out
mkdir -p "$O"
cd "$R" || exit 1

run() { # label src planted [runtime-hex] [extra flags...]
  local label=$1 src=$2 planted=$3; shift 3
  local args=(--label "$label" --src "$src")
  [ -n "$planted" ] && args+=(--planted "$planted")
  for p in "$@"; do
    case "$p" in
      --opt*) args+=("$p") ;;
      *) args+=(--runtime-hex "$p") ;;
    esac
  done
  echo "######## $label"
  TMPDIR=/var/tmp/rv1-r3 python3 /var/tmp/rv1-r3/tools/recompute.py "${args[@]}" \
    2>&1 | tee "$O/r3-recompute-$label.txt" | grep -v PLANTED_SET_JSON
}

run carrierA-EX03-opt200 "$W/EX-03/source/carrierA.sol" "$W/EX-03/planted-selectors.txt" \
    "$W/EX-03/carrierA.runtime.hex" --optimize --optimize-runs 200
run carrierB-EX04-noopt "$W/EX-04/carrierB.sol" "$W/EX-04/planted-B.txt" \
    "$W/EX-04/evidence/carrierB.runtime-noopt.hex"
run carrierB-EX04-opt200 "$W/EX-04/carrierB.sol" "$W/EX-04/planted-B.txt" \
    "$W/EX-04/evidence/carrierB.runtime-opt200.hex" --optimize --optimize-runs 200
run CarrierB-EX05 "$W/EX-05/src/CarrierB.sol" "$W/EX-05/planted-K.json"
run CarrierBErr-EX05 "$W/EX-05/src/attack/CarrierBErr.sol" "$W/EX-05/expected-selectors.txt"
run Rv2TokenOpt-EX07 "$R/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.sol" \
    "$W/EX-07/Rv2TokenOpt.planted-K.json"
run VaultB-EX10 "$W/EX-10/VaultB.sol" "$W/EX-10/planted-K.json"
run VaultA-EX12 "$W/EX-12/VaultA.sol" "$W/EX-12/planted-selectors.txt"
run VaultCourt-SC1 "$W/SC-1/src/VaultCourt.sol" "$W/SC-1/evidence/planted-K-VaultCourt.json"
run Rv2Token-SC1 "$W/SC-1/src/Rv2Token.sol" "$W/SC-1/evidence/planted-K-Rv2Token.json"
run MutMix-PL1 "$W/PL-1/evidence/MutMix.sol" ""
run OptVault-PL1 "$W/PL-1/evidence/OptVault.sol" ""
echo "######## batch done"