#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
COMP="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
REA=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs
S=$(mktemp -d /var/tmp/kaidoku-cr3-r10-recheck.XXXXXX)
trap 'rm -rf "$S"' EXIT
mkdir -p "$S/tmp" "$S/source" "$S/out/london" "$S/out/prague" "$S/probe"
export TMPDIR="$S/tmp"
cp "$SCRIPT_DIR/K8.vy" "$S/source/K8.vy"
"$COMP" --version > "$S/compiler-version.txt"
node "$REA" --version > "$S/rea-version.txt"
for target in london prague; do
  "$COMP" --evm-version "$target" -O gas -f bytecode_runtime "$S/source/K8.vy" > "$S/out/$target/runtime.hex" 2> "$S/out/$target/runtime.stderr"
  "$COMP" --evm-version "$target" -O gas -f abi "$S/source/K8.vy" > "$S/out/$target/abi.json" 2> "$S/out/$target/abi.stderr"
  "$COMP" --evm-version "$target" -O gas -f method_identifiers "$S/source/K8.vy" > "$S/out/$target/method-identifiers.json" 2> "$S/out/$target/method-identifiers.stderr"
  "$COMP" --evm-version "$target" -O gas -f opcodes_runtime "$S/source/K8.vy" > "$S/out/$target/opcodes-runtime.txt" 2> "$S/out/$target/opcodes-runtime.stderr"
  "$COMP" --evm-version "$target" -O gas -f settings "$S/source/K8.vy" > "$S/out/$target/settings.json" 2> "$S/out/$target/settings.stderr"
  node "$REA" inspect-evm-interface "$S/out/$target/runtime.hex" hex --format json > "$S/probe/$target.json" 2> "$S/probe/$target.stderr"
  for file in abi.json method-identifiers.json opcodes-runtime.txt runtime.hex settings.json; do
    cmp "$SCRIPT_DIR/out/$target/$file" "$S/out/$target/$file"
  done
done
printf 'compiler='; tr -d '\n' < "$S/compiler-version.txt"; printf '\nREA='; tr -d '\n' < "$S/rea-version.txt"; printf '\nrecompiled_outputs=byte-identical\n'
python3 "$SCRIPT_DIR/byte-walk.py" "$S"
