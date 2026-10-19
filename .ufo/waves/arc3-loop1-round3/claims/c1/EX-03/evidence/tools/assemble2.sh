#!/usr/bin/env bash
# arc3-loop1-round3 c1/EX-03 — (re)assemble the claim artifact tree.
set -eu
S=/var/tmp/ex03-r3
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
D=$REPO/.ufo/waves/arc3-loop1-round3/claims/c1/EX-03
rm -rf "$D"
mkdir -p "$D/source" "$D/carrier-A/evidence" "$D/carrier-A-alt/evidence" "$D/carrier-A-alt/paired" "$D/evidence/tools"

# ---- primary: plan §1.A carrier A (OptVault), optimizer ON runs=200 ----
cp "$S/ov-a/OptVault.sol"                          "$D/source/OptVault.sol"
cp "$S/ov-cli-out/OptVault_sol_OptVault.bin"       "$D/carrier-A/OptVault.cli.bin"
cp "$S/ov-cli-out/OptVault_sol_OptVault.abi"       "$D/carrier-A/OptVault.cli.abi"
cp "$S/ov-stdjson-out/OptVault.creation.hex"       "$D/carrier-A/OptVault.creation.hex"
cp "$S/ov-stdjson-out/OptVault.runtime.hex"        "$D/carrier-A/OptVault.runtime.hex"
cp "$S/ov-stdjson-out/OptVault.abi.json"           "$D/carrier-A/OptVault.abi.json"
cp "$S/ov-stdjson-out/OptVault.metadata.json"      "$D/carrier-A/OptVault.metadata.json"
cp "$S/ov-stdjson-out/OptVault.methodIdentifiers.json" "$D/carrier-A/OptVault.methodIdentifiers.json"
python3 - <<'PY'
import hashlib
S='/var/tmp/ex03-r3'; D=S.replace('/var/tmp/ex03-r3','/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-03')
for src,dst in [('ov-stdjson-out/OptVault.creation.hex','carrier-A/OptVault.creation.bin'),
                ('ov-stdjson-out/OptVault.runtime.hex','carrier-A/OptVault.runtime.bin')]:
    h=open(f'{S}/{src}').read().strip()
    open(f'{D}/{dst}','wb').write(bytes.fromhex(h))
PY
cp "$S/ov-cli-out/stdout.txt"                      "$D/carrier-A/evidence/cli-stdout.txt"
cp "$S/ov-cli-out/stderr.txt"                      "$D/carrier-A/evidence/cli-stderr.txt"
cp "$S/ov-stdjson-out/solc-input.json"             "$D/carrier-A/evidence/solc-input.json"
cp "$S/ov-stdjson-out/diagnostics.txt"             "$D/carrier-A/evidence/diagnostics.txt"
cp "$S/ov-stdjson-out/summary.txt"                 "$D/carrier-A/evidence/summary.txt"
cp "$S/transcript-optvault.txt"                    "$D/carrier-A/evidence/transcript-optvault.txt"
cp "$S/pl1-premeasurement-match.txt"               "$D/carrier-A/evidence/pl1-premeasurement-re-derivation.txt"

# ---- alternate: EX-02's CarrierA (optimizer ON runs=200) + paired off leg ----
cp "$S/a/carrierA.sol"                             "$D/source/carrierA.sol"
cp "$S/a-out/carrierA_sol_CarrierA.bin"            "$D/carrier-A-alt/carrierA.cli.bin"
cp "$S/a-out/carrierA_sol_CarrierA.abi"            "$D/carrier-A-alt/carrierA.cli.abi"
cp "$S/work/carrierA.creation.bin"                 "$D/carrier-A-alt/carrierA.creation.bin"
cp "$S/work/carrierA.creation.hex"                 "$D/carrier-A-alt/carrierA.creation.hex"
cp "$S/work/carrierA.runtime.bin"                  "$D/carrier-A-alt/carrierA.runtime.bin"
cp "$S/work/carrierA.runtime.hex"                  "$D/carrier-A-alt/carrierA.runtime.hex"
cp "$S/a-stdjson-out/carrierA.abi.json"            "$D/carrier-A-alt/carrierA.abi.json"
cp "$S/a-stdjson-out/carrierA.methodIdentifiers.json" "$D/carrier-A-alt/carrierA.methodIdentifiers.json"
cp "$S/planted-selectors.txt" 2>/dev/null "$D/carrier-A-alt/planted-selectors.txt" || true
cp "$S/work/planted-selectors.txt"                 "$D/carrier-A-alt/planted-selectors.txt"
cp "$S/a-out/stdout.txt"                           "$D/carrier-A-alt/evidence/cli-leg-stdout.txt"
cp "$S/a-out/stderr.txt"                           "$D/carrier-A-alt/evidence/cli-leg-stderr.txt"
cp "$S/a-stdjson-out/carrierA.solc-input.json"     "$D/carrier-A-alt/evidence/solc-input.json"
cp "$S/a-stdjson-out/carrierA.metadata.json"       "$D/carrier-A-alt/evidence/metadata.json"
cp "$S/a-stdjson-out/carrierA.creation.sourceMap"  "$D/carrier-A-alt/evidence/creation.sourceMap"
cp "$S/a-stdjson-out/carrierA.runtime.sourceMap"   "$D/carrier-A-alt/evidence/runtime.sourceMap"
cp "$S/a-stdjson-out/solc-version.txt"             "$D/carrier-A-alt/evidence/solc-version.txt"
cp "$S/transcript-main.txt"                        "$D/carrier-A-alt/evidence/transcript-main.txt"
cp "$S/transcript-stdjson.txt"                     "$D/carrier-A-alt/evidence/transcript-stdjson.txt"
cp "$S/transcript-verify.txt"                      "$D/carrier-A-alt/evidence/transcript-verify.txt"
cp "$S/transcript-paired.txt"                      "$D/carrier-A-alt/paired/transcript-paired.txt"
cp "$S/evidence-optimizer-delta.txt"               "$D/carrier-A-alt/paired/optimizer-delta.txt"
cp "$S/a-cli-off-out/carrierA_sol_CarrierA.bin"    "$D/carrier-A-alt/paired/carrierA.cli-off.bin"
cp "$S/a-cli-off-out/carrierA_sol_CarrierA.abi"    "$D/carrier-A-alt/paired/carrierA.cli-off.abi"
cp "$S/a-stdjson-opt-off/carrierA.runtime.hex"     "$D/carrier-A-alt/paired/carrierA.runtime-off.hex"
cp "$S/a-stdjson-opt-off/carrierA.creation.hex"    "$D/carrier-A-alt/paired/carrierA.creation-off.hex"

# ---- shared evidence + tools ----
cp "$S/sweep-both-carriers.txt"                    "$D/evidence/sweep-both-carriers.txt"
cp "$S/push4-attribution-notes.txt"                "$D/evidence/push4-attribution-notes.txt"
cp "$S/a-legacy-assembly.json"                     "$D/evidence/carrierA-legacy-assembly.json"
{
  echo "cross-leg comparison, 2026-10-19T13:08Z — EX-02 canonical stdjson leg (/var/tmp/ex02-r3/out) vs EX-03 stdjson leg"
  E=/var/tmp/ex02-r3/out
  for f in runtime.hex creation.hex metadata.json abi.json methodIdentifiers.json; do
    a=$(sha256sum "$E/carrierA.$f" | cut -d' ' -f1)
    b=$(sha256sum "$S/a-stdjson-out/carrierA.$f" | cut -d' ' -f1)
    if [ "$a" = "$b" ]; then verdict=IDENTICAL; else verdict=DIFFERS; fi
    echo "$f  EX-02=$a  EX-03=$b  $verdict"
  done
  echo "EX-02 source sha256 (unchanged at 13:16Z): $(sha256sum /var/tmp/ex02-r3/src/carrierA.sol | cut -d' ' -f1)"
  echo "EX-03 pinned copy sha256:                  $(sha256sum "$D/source/carrierA.sol" | cut -d' ' -f1)"
} > "$D/evidence/cross-leg-EX02-comparison.txt"
for f in sweep.js paired-delta.py verify.js compile-stdjson.js run-main.sh run-optvault.sh run-paired.sh run-paired-opt.js assemble2.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/evidence/tools/$f"
done
cp "$S/run.sh" "$D/evidence/tools/run.sh" 2>/dev/null || true

cd "$D"
find . -type f ! -name 'MANIFEST.sha256' -print0 | sort -z | xargs -0 sha256sum | sed 's|\./||' > MANIFEST.sha256
echo "files: $(find . -type f | wc -l); manifest lines: $(wc -l < MANIFEST.sha256)"
cat MANIFEST.sha256