#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SEAT="$ROOT/.ufo/waves/arc3-loop1-round10/claims/c1/EX-1"
EVID="$SEAT/evidence/vyper"
SRC="$EVID/source/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
RUN="/var/tmp/kaidoku-ex1-vyper-r10"
REA="/home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/scripts/rea.mjs"

mkdir -p "$RUN/tmp" "$RUN/out" "$RUN/probe" "$EVID/compile" "$EVID/probe"

for target in cancun paris; do
  for pass in 1 2; do
    env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -O gas -f bytecode_runtime "$SRC" > "$RUN/out/$target.$pass.runtime.hex"
  done
  cmp "$RUN/out/$target.1.runtime.hex" "$RUN/out/$target.2.runtime.hex"
  cp "$RUN/out/$target.1.runtime.hex" "$EVID/compile/$target.runtime.hex"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -O gas -f abi "$SRC" > "$EVID/compile/$target.abi.json"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -O gas -f method_identifiers "$SRC" > "$EVID/compile/$target.method-identifiers.json"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -O gas -f settings "$SRC" > "$EVID/compile/$target.settings.json"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -O gas -f opcodes_runtime "$SRC" > "$EVID/compile/$target.opcodes.txt"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -O gas --no-bytecode-metadata -f bytecode_runtime "$SRC" > "$EVID/compile/$target.no-metadata.runtime.hex"
done

for target in cancun paris; do
  env TMPDIR="$RUN/tmp" node "$REA" inspect-evm-interface "$EVID/compile/$target.runtime.hex" hex --format json > "$RUN/probe/$target.json" 2> "$RUN/probe/$target.stderr"
  cp "$RUN/probe/$target.json" "$EVID/probe/$target.json"
  cp "$RUN/probe/$target.stderr" "$EVID/probe/$target.stderr"
done

python3 "$EVID/verify-hardfork.py" > "$EVID/verification.json"

{
  printf 'run=/var/tmp/kaidoku-ex1-vyper-r10\n'
  printf 'TMPDIR=/var/tmp/kaidoku-ex1-vyper-r10/tmp\n'
  printf 'compiler=%s\n' "$VYPER"
  printf 'repeat_compile=both passes compared byte-identically with cmp\n'
  printf 'compile_commands=\n'
  printf '  %s --evm-version cancun -O gas -f bytecode_runtime %s\n' "$VYPER" "$SRC"
  printf '  %s --evm-version paris -O gas -f bytecode_runtime %s\n' "$VYPER" "$SRC"
  printf '  %s --evm-version cancun -O gas -f opcodes_runtime %s\n' "$VYPER" "$SRC"
  printf '  %s --evm-version paris -O gas -f opcodes_runtime %s\n' "$VYPER" "$SRC"
  printf '  %s --evm-version cancun -O gas --no-bytecode-metadata -f bytecode_runtime %s\n' "$VYPER" "$SRC"
  printf '  %s --evm-version paris -O gas --no-bytecode-metadata -f bytecode_runtime %s\n' "$VYPER" "$SRC"
  printf 'REA_commands=\n'
  printf '  node %s inspect-evm-interface %s/compile/cancun.runtime.hex hex --format json\n' "$REA" "$EVID"
  printf '  node %s inspect-evm-interface %s/compile/paris.runtime.hex hex --format json\n' "$REA" "$EVID"
  printf 'verify_command=python3 %s/verify-hardfork.py > %s/verification.json\n' "$EVID" "$EVID"
  printf 'runtime_hex_sha256=\n'
  sha256sum "$EVID/compile/cancun.runtime.hex" "$EVID/compile/paris.runtime.hex"
  printf 'opcode_transcript_sha256=\n'
  sha256sum "$EVID/compile/cancun.opcodes.txt" "$EVID/compile/paris.opcodes.txt"
} > "$EVID/reproduction.txt"
