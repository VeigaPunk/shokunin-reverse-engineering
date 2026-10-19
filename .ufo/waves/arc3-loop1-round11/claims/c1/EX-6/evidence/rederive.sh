#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
E="$ROOT/.ufo/waves/arc3-loop1-round11/claims/c1/EX-6/evidence"
V="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
T=/var/tmp/kaidoku-arc3-r11-ex6
mkdir -p "$T/tmp" "$E/compiled"
{
  sha256sum "$E/BlobFork.vy" "$E/BlobFeeOnly.vy" "$V"
  "$V" --version
} > "$E/identity.txt"
: > "$E/compile-results.txt"
for source in BlobFork BlobFeeOnly; do
  for fork in london paris shanghai cancun prague; do
    stem="$E/compiled/$source-$fork"
    if env TMPDIR="$T/tmp" "$V" --evm-version "$fork" -O gas -f bytecode_runtime "$E/$source.vy" > "$stem.runtime.hex" 2> "$stem.stderr"; then
      printf '%s %s rc=0\n' "$source" "$fork" | tee -a "$E/compile-results.txt"
      for format in abi method_identifiers settings opcodes_runtime; do
        env TMPDIR="$T/tmp" "$V" --evm-version "$fork" -O gas -f "$format" "$E/$source.vy" > "$stem.$format" 2> "$stem.$format.stderr"
      done
      if [[ "$fork" == cancun || "$fork" == prague ]]; then
        env TMPDIR="$T/tmp" "$V" --evm-version "$fork" -O gas -f bytecode_runtime "$E/$source.vy" > "$stem.runtime.repeat.hex" 2> "$stem.runtime.repeat.stderr"
        cmp "$stem.runtime.hex" "$stem.runtime.repeat.hex"
        printf '%s %s repeated_runtime=byte-identical\n' "$source" "$fork" | tee -a "$E/compile-results.txt"
        python3 - "$stem.runtime.hex" "$stem.opcodes_runtime" <<'PY' | tee -a "$E/compile-results.txt"
import hashlib, pathlib, sys
raw = bytes.fromhex(pathlib.Path(sys.argv[1]).read_text().strip().removeprefix("0x"))
ops = pathlib.Path(sys.argv[2]).read_text().split()
print(f"runtime_bytes={len(raw)} runtime_sha256={hashlib.sha256(raw).hexdigest()}")
print(f"opcode_tokens={len(ops)} PUSH4={ops.count('PUSH4')} XOR={ops.count('XOR')} MOD={ops.count('MOD')} AND={ops.count('AND')} BLOBHASH={ops.count('BLOBHASH')} BLOBBASEFEE={ops.count('BLOBBASEFEE')}")
PY
      fi
    else
      rc=$?
      printf '%s %s rc=%s\n' "$source" "$fork" "$rc" | tee -a "$E/compile-results.txt"
      cat "$stem.stderr" >> "$E/compile-results.txt"
    fi
  done
done
for source in BlobFork BlobFeeOnly; do
  for fork in cancun prague; do
    stem="$E/compiled/$source-$fork"
    if [[ -s "$stem.runtime.hex" ]]; then
      printf '%s %s selectors: ' "$source" "$fork" | tee -a "$E/compile-results.txt"
      python3 - "$stem.method_identifiers" <<'PY' | tee -a "$E/compile-results.txt"
import json, pathlib, sys
print(json.dumps(json.loads(pathlib.Path(sys.argv[1]).read_text()), sort_keys=True))
PY
    fi
  done
done
