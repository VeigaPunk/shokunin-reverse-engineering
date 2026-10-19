#!/bin/bash
# EX-09 (arc3-loop1-round3, chain c1) reconciliation driver — reproducible run.
#
# Inputs: this seat dir (carrier/planted/sigs copies + leg lists) and the wave-tree
# probe envelopes listed in the legs-*.txt files (frozen 2026-10-19T13:16:30Z).
# Legs lists were produced mechanically by the census rule stated in their headers.
# Run from the repo root:  bash .ufo/waves/arc3-loop1-round3/claims/c1/EX-09/run-recon.sh
set -u
D=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-09
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin

python3 "$D/ex09-recon.py" keccak-test > "$D/keccak-self-test.txt"; echo "keccak-self-test exit=$?"

# --- carrier A primary: EX-02/EX-03 CarrierA.sol compile, runtime 9f7392ac… (optimizer runs=200)
python3 "$D/ex09-recon.py" extract "$D/target-carrierA-r3.runtime.hex" hex > "$D/extract-carrierA-r3.json"
python3 "$D/ex09-recon.py" scan "$D/target-carrierA-r3.runtime.hex" hex "$D/sigs-carrierA-r3.txt" > "$D/scan-carrierA-r3.json"
python3 "$D/ex09-recon.py" jumpdests "$D/target-carrierA-r3.runtime.hex" hex 164 214 235 266 297 331 383 437 470 88 > "$D/jumpdests-carrierA-r3.txt"
python3 "$D/ex09-recon.py" reconciler "$D/target-carrierA-r3.runtime.hex" hex \
  --planted "$D/planted-carrierA-r3.copy.txt" --sigs "$D/sigs-carrierA-r3.txt" \
  --probe $(cat "$D/legs-carrierA-r3.txt" | grep -v '^#') > "$D/recon-carrierA-r3.txt" 2>&1
echo "recon-carrierA-r3 exit=$?"

# --- carrier A third reading: PL-1 OptVault, runtime 544469b7… (optimizer runs=200)
python3 "$D/ex09-recon.py" extract "$D/target-OptVault.runtime.hex" hex > "$D/extract-OptVault.json"
python3 "$D/ex09-recon.py" scan "$D/target-OptVault.runtime.hex" hex "$D/sigs-OptVault.txt" > "$D/scan-OptVault.json"
python3 "$D/ex09-recon.py" jumpdests "$D/target-OptVault.runtime.hex" hex 75 106 137 182 248 > "$D/jumpdests-OptVault.txt"
python3 "$D/ex09-recon.py" reconciler "$D/target-OptVault.runtime.hex" hex \
  --planted "$D/planted-OptVault.copy.txt" --sigs "$D/sigs-OptVault.txt" \
  --probe $(cat "$D/legs-OptVault.txt" | grep -v '^#') > "$D/recon-OptVault.txt" 2>&1
echo "recon-OptVault exit=$?"

# --- legacy control reading: r1 CR-1 hand-assembled carrier-A.hex, decoded a92ba152…
python3 "$D/ex09-recon.py" extract "$D/target-carrier-A-control.hex" hex > "$D/extract-control.json"
python3 "$D/ex09-recon.py" scan "$D/target-carrier-A-control.hex" hex "$D/sigs-A-control.txt" > "$D/scan-control.json"
python3 "$D/ex09-recon.py" jumpdests "$D/target-carrier-A-control.hex" hex 38 48 58 40 50 60 > "$D/jumpdests-control.txt"
python3 "$D/ex09-recon.py" reconciler "$D/target-carrier-A-control.hex" hex \
  --planted "$D/planted-A-control.json" --sigs "$D/sigs-A-control.txt" \
  --probe $(cat "$D/legs-control.txt" | grep -v '^#') > "$D/recon-control.txt" 2>&1
echo "recon-control exit=$?"