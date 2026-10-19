#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
EVID="$ROOT/.ufo/waves/arc3-loop1-round10/claims/c1/EX-6/evidence"
SRC="$EVID/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
PYTHON="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/python"
RUN="$(mktemp -d /var/tmp/kaidoku-ex6-r10.XXXXXX)"
mkdir -p "$RUN/tmp" "$RUN/out" "$RUN/probe"
export TMPDIR="$RUN/tmp"

{
  printf 'head=%s\n' "$(git -C "$ROOT" rev-parse HEAD)"
  printf 'source=%s\n' "$SRC"
  sha256sum "$SRC"
  printf 'vyper_executable=%s\n' "$VYPER"
  sha256sum "$VYPER"
  "$VYPER" --version
  "$PYTHON" --version 2>&1
  "$PYTHON" -c 'import sys,vyper; print("vyper_module_version="+vyper.__version__); print("python_executable="+sys.executable)'
  npx -y rea-agents@6.7.0 --version
  printf 'scratch=%s\nTMPDIR=%s\n' "$RUN" "$TMPDIR"
} > "$EVID/identity.txt"

for evm in london paris shanghai cancun prague; do
  for pass in 1 2; do
    "$VYPER" --evm-version "$evm" -f bytecode_runtime "$SRC" > "$RUN/out/$evm.$pass.runtime.hex"
  done
  cmp "$RUN/out/$evm.1.runtime.hex" "$RUN/out/$evm.2.runtime.hex"
  cp "$RUN/out/$evm.1.runtime.hex" "$EVID/$evm.runtime.hex"
  "$VYPER" --evm-version "$evm" -f abi "$SRC" > "$EVID/$evm.abi.json"
  "$VYPER" --evm-version "$evm" -f method_identifiers "$SRC" > "$EVID/$evm.methodids.json"
  "$VYPER" --evm-version "$evm" -f settings "$SRC" > "$EVID/$evm.settings.json"
  "$VYPER" --evm-version "$evm" -f opcodes_runtime "$SRC" > "$EVID/$evm.opcodes.txt"
  npx -y rea-agents@6.7.0 inspect-evm-interface "$EVID/$evm.runtime.hex" hex --format json > "$EVID/$evm.probe.json" 2> "$EVID/$evm.probe.stderr"
  printf '%-9s runtime-two-pass-cmp=PASS sha256=' "$evm"
  sha256sum "$RUN/out/$evm.1.runtime.hex" | cut -d' ' -f1
  printf '%-9s REA-probe=PASS evidence_id=' "$evm"
  "$PYTHON" -c 'import json,sys; print(json.load(open(sys.argv[1]))["evidence_id"])' "$EVID/$evm.probe.json"
done > "$EVID/reproduction.txt"

"$PYTHON" "$EVID/measure.py" "$EVID" > "$EVID/measure.json"
printf 'measurement=PASS\n' >> "$EVID/reproduction.txt"
sha256sum "$EVID/measure.json" >> "$EVID/reproduction.txt"
