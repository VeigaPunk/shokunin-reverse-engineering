#!/usr/bin/env bash
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=$R/.ufo/waves/arc3-loop1-round3/claims/c1
O=/var/tmp/rv1-r3/out
cd "$R" || exit 1
one() { local label=$1; shift; echo "######## $label"; }
opt=()
runopt() {
  local label=$1 src=$2 planted=$3 runtime=$4
  echo "######## $label"
  TMPDIR=/var/tmp/rv1-r3 python3 /var/tmp/rv1-r3/tools/recompute.py --label "$label" --src "$src" \
    ${planted:+--planted "$planted"} ${runtime:+--runtime-hex "$runtime"} \
    --optimize --optimize-runs 200 2>&1 | tee "$O/r3-recompute-$label.txt" | grep -v PLANTED_SET_JSON
}
runopt carrierA-EX03-opt200 "$W/EX-03/source/carrierA.sol" "$W/EX-03/planted-selectors.txt" "$W/EX-03/carrierA.runtime.hex"
runopt carrierB-EX04-opt200 "$W/EX-04/carrierB.sol" "$W/EX-04/planted-B.txt" "$W/EX-04/evidence/carrierB.runtime-opt200.hex"
runopt Rv2TokenOpt-EX07 "$R/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.sol" "$W/EX-07/Rv2TokenOpt.planted-K.json" ""
runopt VaultCourt-SC1 "$W/SC-1/src/VaultCourt.sol" "$W/SC-1/evidence/planted-K-VaultCourt.json" ""
runopt Rv2Token-SC1 "$W/SC-1/src/Rv2Token.sol" "$W/SC-1/evidence/planted-K-Rv2Token.json" ""
runopt OptVault-PL1 "$W/PL-1/evidence/OptVault.sol" "" ""
