#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
E="$ROOT/.ufo/waves/arc3-loop1-round10/claims/c1/CR-2/evidence"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
REA_NODE="$HOME/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/scripts/rea.mjs"
ORIGINAL="$ROOT/.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/evidence/K8.vy"
RUN="$(mktemp -d /var/tmp/kaidoku-cr2-r10.XXXXXX)"
mkdir -p "$RUN/tmp" "$RUN/pycache"

{
  printf 'measurement_utc='
  date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'scratch=%s\n' "$RUN"
  printf 'source_sha256s:\n'
  sha256sum "$ORIGINAL" "$E/K8.vy"
  cmp "$ORIGINAL" "$E/K8.vy"
  printf 'source_copy_cmp=0\n'
  printf 'compiler_sha256='; sha256sum "$VYPER"
  printf 'compiler_version='; PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$RUN/pycache" TMPDIR="$RUN/tmp" "$VYPER" --version
  printf 'rea_version='; TMPDIR="$RUN/tmp" node "$REA_NODE" --version
  printf 'compiler_command=vyper --evm-version TARGET -f FORMAT K8.vy (TARGET=prague,london; FORMAT=bytecode_runtime,abi,method_identifiers,settings,opcodes_runtime)\n'
  for target in prague london; do
    for pass in 1 2; do
      PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$RUN/pycache" TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -f bytecode_runtime "$E/K8.vy" > "$RUN/$target.$pass.runtime.hex"
    done
    cmp "$RUN/$target.1.runtime.hex" "$RUN/$target.2.runtime.hex"
    printf '%s_repeated_runtime_cmp=0\n' "$target"
    cp "$RUN/$target.1.runtime.hex" "$E/compile/$target.runtime.hex"
    for format in abi method_identifiers settings opcodes_runtime; do
      PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$RUN/pycache" TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -f "$format" "$E/K8.vy" > "$E/compile/$target.$format.$([[ "$format" == opcodes_runtime ]] && printf txt || printf json)"
    done
    TMPDIR="$RUN/tmp" node "$REA_NODE" inspect-evm-interface "$E/compile/$target.runtime.hex" hex --format json > "$E/probe/$target.json" 2> "$E/probe/$target.stderr"
  done
  printf 'analysis_command=/usr/bin/python3 %s/measure.py %s/compile %s/probe\n' "$E" "$E" "$E"
  /usr/bin/python3 "$E/measure.py" "$E/compile" "$E/probe" | tee "$E/measurement.txt"
  printf 'selector_command=%s %s/keccak-check.py %s/compile\n' "$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/python" "$E" "$E"
  PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$RUN/pycache" TMPDIR="$RUN/tmp" "$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/python" "$E/keccak-check.py" "$E/compile" | tee "$E/keccak-check.txt"
} > "$E/reproduction.txt"
printf 'reproduction saved: %s\n' "$E/reproduction.txt"
