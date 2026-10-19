#!/usr/bin/env bash
# arc3-loop1-round3 c1/EX-03 — carrier A = PL-1 plan §1.A (OptVault) compile legs.
set -u
S=/var/tmp/ex03-r3
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SOLCJS=$REPO/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/.bin/solcjs
PL1=$REPO/.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence
export TMPDIR=$S/tmp
OV=$S/ov-a
rm -rf "$OV" "$S/ov-cli-out" "$S/ov-cli-out2" "$S/ov-stdjson-out" "$S/ov-stdjson-out2"
mkdir -p "$OV" "$S/tmp"
cp "$PL1/OptVault.sol" "$OV/OptVault.sol"

echo "== host =="; date -u +"captured-at %Y-%m-%dT%H:%M:%SZ"; uname -srm; node --version
echo "== source (carrier A := PL-1 plan §1.A OptVault) =="
sha256sum "$OV/OptVault.sol"; wc -c < "$OV/OptVault.sol"
echo "== compiler =="; node "$SOLCJS" --version
cd "$OV" || exit 1

echo "== leg 1 (PRIMARY): literal flags form =="
mkdir -p "$S/ov-cli-out" "$S/ov-cli-out2"
echo "cmd: node <prefix>/node_modules/.bin/solcjs --bin --abi --optimize --optimize-runs 200 -o $S/ov-cli-out OptVault.sol   (cwd=$OV, TMPDIR=$S/tmp)"
node "$SOLCJS" --bin --abi --optimize --optimize-runs 200 -o "$S/ov-cli-out" OptVault.sol >"$S/ov-cli-out/stdout.txt" 2>"$S/ov-cli-out/stderr.txt"
echo "leg1 exit=$?"
echo "--- leg1 stdout (verbatim) ---"; cat "$S/ov-cli-out/stdout.txt"
echo "--- leg1 stderr (verbatim) ---"; cat "$S/ov-cli-out/stderr.txt"
ls -la "$S/ov-cli-out"; sha256sum "$S/ov-cli-out"/*

echo "== leg 1 rerun (determinism) =="
node "$SOLCJS" --bin --abi --optimize --optimize-runs 200 -o "$S/ov-cli-out2" OptVault.sol >"$S/ov-cli-out2/stdout.txt" 2>"$S/ov-cli-out2/stderr.txt"
cmp "$S/ov-cli-out/OptVault_sol_OptVault.bin" "$S/ov-cli-out2/OptVault_sol_OptVault.bin" && echo "RERUN: creation bin byte-identical"
cmp "$S/ov-cli-out/OptVault_sol_OptVault.abi" "$S/ov-cli-out2/OptVault_sol_OptVault.abi" && echo "RERUN: abi byte-identical"

echo "== leg 2 (SUPPLEMENTARY): standard JSON, source key OptVault.sol, optimizer on runs=200 =="
node "$S/compile-stdjson.js" "$OV" OptVault.sol "$S/ov-stdjson-out" on
echo "leg2 exit=$?"
ls -la "$S/ov-stdjson-out"

echo "== leg 2 rerun (determinism) =="
node "$S/compile-stdjson.js" "$OV" OptVault.sol "$S/ov-stdjson-out2" on >/dev/null
for f in OptVault.runtime.hex OptVault.creation.hex OptVault.abi.json OptVault.methodIdentifiers.json OptVault.metadata.json; do
  cmp -s "$S/ov-stdjson-out/$f" "$S/ov-stdjson-out2/$f" && echo "leg2 rerun $f byte-identical" || echo "leg2 rerun $f DIFFERS"
done

echo "== equivalence anchor: CLI creation == stdjson creation =="
cmp <(tr -d '\n' < "$S/ov-cli-out/OptVault_sol_OptVault.bin") <(tr -d '\n' < "$S/ov-stdjson-out/OptVault.creation.hex") && echo "ON: CLI creation == stdjson creation (hex text)"

echo "== re-derivation vs PL-1 pre-measurement (plan §1.A / §2) =="
cmp -s "$S/ov-stdjson-out/OptVault.runtime.hex" "$PL1/OptVault.runtime.hex" && echo "runtime.hex IDENTICAL to PL-1 pre-measured" || echo "runtime.hex DIFFERS from PL-1 pre-measured"
sha256sum "$S/ov-stdjson-out/OptVault.runtime.hex" "$PL1/OptVault.runtime.hex"
python3 - <<'PY'
print('creation hex len (chars) =', len(open('/var/tmp/ex03-r3/ov-stdjson-out/OptVault.creation.hex').read().strip()))
PY
echo "== done =="; date -u +"finished-at %Y-%m-%dT%H:%M:%SZ"