#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
E="$ROOT/.ufo/waves/arc3-loop1-round11/claims/c1/EX-6/evidence"
T=/var/tmp/kaidoku-arc3-r11-ex6
mkdir -p "$T/tmp"
: > "$E/probe-results.txt"
for fork in cancun prague; do
  input="$E/compiled/BlobFork-$fork.runtime.hex"
  output="$E/probe-$fork.json"
  err="$E/probe-$fork.stderr"
  if env TMPDIR="$T/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$input" hex --format json > "$output" 2> "$err"; then
    printf 'REA 6.7.0 %s rc=0\n' "$fork" | tee -a "$E/probe-results.txt"
    python3 - "$output" <<'PY' | tee -a "$E/probe-results.txt"
import json, pathlib, sys
record = json.loads(pathlib.Path(sys.argv[1]).read_text())
functions = record.get("raw_result", {}).get("functions", [])
normalized = record.get("normalized_result", {})
bytecode = normalized.get("bytecode", {})
print("evidence_id", record.get("evidence_id"))
print("function_count", len(functions))
print("selectors", ",".join(row.get("selector", "") for row in functions))
print("bytecode_bytes", bytecode.get("bytes"))
print("decoded_bytecode_sha256", bytecode.get("sha256"))
print("authority", record.get("authority"))
print("confidence", record.get("confidence"))
print("limitations", json.dumps(record.get("limitations", []), sort_keys=True))
PY
  else
    rc=$?
    printf 'REA 6.7.0 %s rc=%s\n' "$fork" "$rc" | tee -a "$E/probe-results.txt"
    cat "$err" >> "$E/probe-results.txt"
  fi
done
