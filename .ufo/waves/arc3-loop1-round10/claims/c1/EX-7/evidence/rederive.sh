#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
ART="$ROOT/.ufo/waves/arc3-loop1-round10/claims/c1/EX-7"
EVIDENCE="$ART/evidence"
SRC="$ROOT/.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/evidence/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
REA="$HOME/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/scripts/rea.mjs"
RUN="$(mktemp -d /var/tmp/kaidoku-ex7-r10-paris.XXXXXX)"
mkdir -p "$EVIDENCE" "$RUN/tmp" "$RUN/out"
cp "$SRC" "$RUN/K8.vy"
cp "$SRC" "$EVIDENCE/K8.vy"

{
  printf 'repo_head='
  git rev-parse HEAD
  printf 'source=%s\n' "$SRC"
  sha256sum "$SRC" "$EVIDENCE/K8.vy"
  printf 'compiler=%s\n' "$VYPER"
  sha256sum "$VYPER"
  "$VYPER" --version
  printf 'rea_script=%s\n' "$REA"
  env TMPDIR="$RUN/tmp" node "$REA" --version
  printf 'scratch=%s\nTMPDIR=%s\n' "$RUN" "$RUN/tmp"
} > "$EVIDENCE/identity.txt"

for pass in 1 2; do
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version paris -O gas -f bytecode_runtime "$RUN/K8.vy" > "$RUN/out/paris.$pass.runtime.hex"
done
cmp "$RUN/out/paris.1.runtime.hex" "$RUN/out/paris.2.runtime.hex"
cp "$RUN/out/paris.1.runtime.hex" "$EVIDENCE/paris.runtime.hex"
env TMPDIR="$RUN/tmp" "$VYPER" --evm-version paris -O gas -f abi "$RUN/K8.vy" > "$EVIDENCE/paris.abi.json"
env TMPDIR="$RUN/tmp" "$VYPER" --evm-version paris -O gas -f method_identifiers "$RUN/K8.vy" > "$EVIDENCE/paris.method-identifiers.json"
env TMPDIR="$RUN/tmp" "$VYPER" --evm-version paris -O gas -f settings "$RUN/K8.vy" > "$EVIDENCE/paris.settings.json"
env TMPDIR="$RUN/tmp" "$VYPER" --evm-version paris -O gas -f opcodes_runtime "$RUN/K8.vy" > "$EVIDENCE/paris.opcodes-runtime.txt"
env TMPDIR="$RUN/tmp" node "$REA" inspect-evm-interface "$EVIDENCE/paris.runtime.hex" hex --format json > "$EVIDENCE/paris.rea.json" 2> "$EVIDENCE/paris.rea.stderr"
python3 "$EVIDENCE/measure.py" "$EVIDENCE" > "$EVIDENCE/measurement.txt"
