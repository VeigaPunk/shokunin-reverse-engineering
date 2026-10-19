#!/bin/bash
# EX-08 variants2 runner: regenerate the mechanism matrix, probe each carrier
# with rea-agents 6.4.0, print selector/offset results, build the matrix files.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REA64="$HOME/.npm/_npx/dea9475797100b20/node_modules/rea-agents/scripts/rea.mjs"
export TMPDIR="$HERE/tmp"
mkdir -p "$TMPDIR"
node "$HERE/variants2-generate.js"
for f in "$HERE"/variants2/*.hex; do
  name="$(basename "$f" .hex)"
  node "$REA64" inspect-evm-interface "$f" hex --format json > "$HERE/variants2/$name.json" 2>&1
  rc=$?
  printf '%-14s exit=%s %s\n' "$name" "$rc" \
    "$(jq -c '[.raw_result.functions[]?|{s:.selector,o:.bytecodeOffset,d:.dispatch}]' "$HERE/variants2/$name.json" 2>/dev/null || head -c 150 "$HERE/variants2/$name.json")"
done
