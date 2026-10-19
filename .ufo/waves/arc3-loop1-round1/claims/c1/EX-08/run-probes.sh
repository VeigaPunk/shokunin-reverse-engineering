#!/bin/bash
# EX-08 probe runner (arc3-loop1-round1, chain c1). Run from the EX-08 dir.
# Invokes the npx-cached rea-agents binaries directly (no install, no network):
#   6.4.0 = the version recorded by the r3-07 entry (true regression control)
#   6.7.0 = the version cached for the current wave
# TMPDIR is redirected into this artifact dir: the system /tmp tmpfs is
# usrquota-exhausted on this host and the EVMole worker dies with EDQUOT
# (system error -122) otherwise. A no-TMPDIR control probe documents that.
# Writes <name>.json / <name>.err / <name>.exit per probe. Never fails the shell.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REA64="$HOME/.npm/_npx/dea9475797100b20/node_modules/rea-agents/scripts/rea.mjs"
REA67="$HOME/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs"
export TMPDIR="$HERE/tmp"
mkdir -p "$TMPDIR"

probe() { # probe <label> <rea-js> <path> <encoding>
  local label="$1" rea="$2" p="$3" enc="$4"
  node "$rea" inspect-evm-interface "$p" "$enc" --format json > "$HERE/$label.json" 2> "$HERE/$label.err"
  echo "$?" > "$HERE/$label.exit"
  printf '%-34s exit=%s  stdout=%s B  stderr=%s B\n' "$label" "$(cat "$HERE/$label.exit")" \
    "$(wc -c < "$HERE/$label.json")" "$(wc -c < "$HERE/$label.err")"
}

echo "== reconstruction =="
node "$HERE/reconstruct.js" | tee "$HERE/reconstruct-output.json"
sha256sum "$HERE/r3-07-recon.hex" "$HERE/r3-07-recon.bin" "$HERE/nonbytecode.txt" > "$HERE/carrier-sha256.txt"
cat "$HERE/carrier-sha256.txt"

echo "== carriers for probe (b) =="
node -e 'require("fs").writeFileSync(process.argv[1], Buffer.from("7f454c46020101000000000000000000","hex"))' "$HERE/nonbytecode.bin"
node -e 'require("fs").writeFileSync(process.argv[1], require("fs").readFileSync(process.argv[2]).toString("hex")+"\n")' "$HERE/nonbytecode.hex" "$HERE/nonbytecode.txt"
: > "$HERE/empty.bin"
sha256sum "$HERE/nonbytecode.bin" "$HERE/nonbytecode.hex" "$HERE/empty.bin" >> "$HERE/carrier-sha256.txt"
tail -3 "$HERE/carrier-sha256.txt"

echo "== (a) regression control: reconstructed 81-byte dispatcher =="
probe probe-recon-hex-6.4.0 "$REA64" "$HERE/r3-07-recon.hex" hex
probe probe-recon-raw-6.4.0 "$REA64" "$HERE/r3-07-recon.bin" raw
probe probe-recon-hex-6.7.0 "$REA67" "$HERE/r3-07-recon.hex" hex
probe probe-recon-raw-6.7.0 "$REA67" "$HERE/r3-07-recon.bin" raw

echo "== (b) typed-refusal shape on non-bytecode inputs =="
probe probe-txt-hex-6.4.0      "$REA64" "$HERE/nonbytecode.txt" hex
probe probe-txt-raw-6.4.0      "$REA64" "$HERE/nonbytecode.txt" raw
probe probe-elfmagic-raw-6.4.0 "$REA64" "$HERE/nonbytecode.bin" raw
probe probe-elfmagic-hex-6.4.0 "$REA64" "$HERE/nonbytecode.bin" hex
probe probe-nonbc-hex-6.4.0    "$REA64" "$HERE/nonbytecode.hex" hex
probe probe-empty-raw-6.4.0    "$REA64" "$HERE/empty.bin" raw
probe probe-empty-hex-6.4.0    "$REA64" "$HERE/empty.bin" hex
probe probe-missing-6.4.0      "$REA64" "$HERE/does-not-exist.bin" raw

echo "== host-condition control: same input with TMPDIR unset (EDQUOT class) =="
env -u TMPDIR node "$REA64" inspect-evm-interface "$HERE/r3-07-recon.bin" raw --format json \
  > "$HERE/probe-recon-raw-noTMPDIR.json" 2> "$HERE/probe-recon-raw-noTMPDIR.err"
echo "$?" > "$HERE/probe-recon-raw-noTMPDIR.exit"
printf '%-34s exit=%s  stdout=%s B\n' "probe-recon-raw-noTMPDIR" \
  "$(cat "$HERE/probe-recon-raw-noTMPDIR.exit")" "$(wc -c < "$HERE/probe-recon-raw-noTMPDIR.json")"

echo "== summary =="
for f in "$HERE"/probe-*.exit; do
  printf '%-40s exit=%s\n' "$(basename "$f" .exit)" "$(cat "$f")"
done
