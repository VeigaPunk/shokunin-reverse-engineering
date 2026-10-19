#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel)
EVIDENCE="$ROOT/.ufo/waves/arc3-loop1-round10/claims/c1/EX-8/evidence"
SOURCE="$EVIDENCE/HardforkVault.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
SCRATCH=$(mktemp -d /var/tmp/kaidoku-r10-ex8.XXXXXX)
trap 'rm -rf "$SCRATCH"' EXIT

printf 'scratch=%s\n' "$SCRATCH"
printf 'source=%s\n' "$SOURCE"
printf 'compiler=%s\n' "$VYPER"
printf 'compiler-version: '
"$VYPER" --version
sha256sum "$SOURCE" "$VYPER"

for fork in london prague; do
    out="$EVIDENCE/compile/$fork"
    mkdir -p "$out"
    "$VYPER" --evm-version "$fork" -O gas -f bytecode_runtime "$SOURCE" > "$out/runtime.hex"
    "$VYPER" --evm-version "$fork" -O gas -f abi "$SOURCE" > "$out/abi.json"
    "$VYPER" --evm-version "$fork" -O gas -f method_identifiers "$SOURCE" > "$out/method_identifiers.json"
    "$VYPER" --evm-version "$fork" -O gas -f settings "$SOURCE" > "$out/settings.json"
    "$VYPER" --evm-version "$fork" -O gas -f bytecode_runtime "$SOURCE" > "$SCRATCH/$fork-runtime-repeat.hex"
    cmp "$out/runtime.hex" "$SCRATCH/$fork-runtime-repeat.hex"
    printf '\n[%s]\n' "$fork"
    sha256sum "$out/runtime.hex" "$SCRATCH/$fork-runtime-repeat.hex" "$out/abi.json" "$out/method_identifiers.json" "$out/settings.json"
    wc -c "$out/runtime.hex" "$out/abi.json" "$out/method_identifiers.json" "$out/settings.json"
done

for fork in london prague; do
    TMPDIR="$SCRATCH" npx --yes --offline rea-agents@6.7.0 inspect-evm-interface "$EVIDENCE/compile/$fork/runtime.hex" hex --format json > "$EVIDENCE/probe/$fork.json"
done

python3 "$EVIDENCE/measure.py" | tee "$EVIDENCE/measure.txt"
