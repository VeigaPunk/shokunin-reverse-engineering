#!/usr/bin/env bash
# RV-1 r3 — final pass. Recomputes every carrier source present at capture time,
# with planted artifacts where they exist, and the EX-13 shape family in both legs.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=$R/.ufo/waves/arc3-loop1-round3/claims/c1
O=/var/tmp/rv1-r3/out/final
mkdir -p "$O"
cd "$R" || exit 1
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ); echo "# capture $TS" | tee "$O/capture-time.txt"

rc() { # rc <label> <src> <planted|-> <runtime|-> [--optimize [--optimize-runs N]]
  local label=$1 src=$2 planted=$3 runtime=$4; shift 4
  local args=(--label "$label" --src "$src")
  [ "$planted" != "-" ] && args+=(--planted "$planted")
  [ "$runtime" != "-" ] && args+=(--runtime-hex "$runtime")
  args+=("$@")
  echo "######## $label"
  TMPDIR=/var/tmp/rv1-r3 python3 /var/tmp/rv1-r3/tools/recompute.py "${args[@]}" \
    2>&1 | tee "$O/$label.txt" | grep -v PLANTED_SET_JSON
}

echo "===== PRIMARY (claim carriers) ====="
rc A1-EX03-alt-opt200 "$W/EX-03/source/carrierA.sol" "$W/EX-03/carrier-A-alt/planted-selectors.txt" \
   "$W/EX-03/carrier-A-alt/carrierA.runtime.hex" --optimize --optimize-runs 200
rc A2-EX02-opt200 "$W/EX-02/carrierA.sol" "$W/EX-02/planted-A.txt" \
   "$W/EX-02/evidence/carrierA.runtime.hex" --optimize --optimize-runs 200
rc B1-EX04-opt200 "$W/EX-04/carrierB.sol" "$W/EX-04/planted-B.txt" \
   "$W/EX-04/evidence/carrierB.runtime-opt200.hex" --optimize --optimize-runs 200
rc B2-EX04-noopt "$W/EX-04/carrierB.sol" "$W/EX-04/planted-B.txt" \
   "$W/EX-04/evidence/carrierB.runtime-noopt.hex"

echo "===== other planted-bearing carriers ====="
rc OptVault-EX03-opt200 "$W/EX-03/source/OptVault.sol" "$W/EX-03/carrier-A/OptVault.planted-selectors.txt" \
   "$W/EX-03/carrier-A/OptVault.runtime.hex" --optimize --optimize-runs 200
rc CarrierB-EX05-opt200 "$W/EX-05/src/CarrierB.sol" "$W/EX-05/planted-K.json" - --optimize --optimize-runs 200
rc CarrierBErr-EX05-opt200 "$W/EX-05/src/attack/CarrierBErr.sol" "$W/EX-05/expected-selectors.txt" - --optimize --optimize-runs 200
rc Rv2TokenOpt-EX07-opt200 "$R/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.sol" \
   "$W/EX-07/Rv2TokenOpt.planted-K.json" - --optimize --optimize-runs 200
rc VaultB-EX10-noopt "$W/EX-10/VaultB.sol" "$W/EX-10/planted-K.json" -
rc VaultB-EX10-opt200 "$W/EX-10/VaultB.sol" "$W/EX-10/planted-K.json" - --optimize --optimize-runs 200
rc VaultA-EX12-opt200 "$W/EX-12/VaultA.sol" "$W/EX-12/planted-selectors.txt" - --optimize --optimize-runs 200
rc VaultCourt-SC1-opt200 "$W/SC-1/src/VaultCourt.sol" "$W/SC-1/evidence/planted-K-VaultCourt.json" - --optimize --optimize-runs 200
rc Rv2Token-SC1-opt200 "$W/SC-1/src/Rv2Token.sol" "$W/SC-1/evidence/planted-K-Rv2Token.json" - --optimize --optimize-runs 200
rc KdxToken-SC1-noopt "$W/SC-1/src/KdxToken.sol" - -
rc CarrierB-EX08-opt200 "$W/EX-08/aux/CarrierB.sol" "$W/EX-08/aux/planted-K.json" - --optimize --optimize-runs 200
rc MutMix-PL1 "$W/PL-1/evidence/MutMix.sol" - -
rc OptVault-PL1-opt200 "$W/PL-1/evidence/OptVault.sol" - - --optimize --optimize-runs 200

echo "===== EX-13 shape family (both legs) ====="
for f in $W/EX-13/src/*.sol; do
  b=$(basename "$f" .sol)
  rc "EX13-$b-noopt" "$f" - - --optimize-runs 200  # no --optimize
  rc "EX13-$b-opt200" "$f" - - --optimize --optimize-runs 200
done
echo "######## final pass done"