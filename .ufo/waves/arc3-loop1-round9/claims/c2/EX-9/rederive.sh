#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SEAT="$ROOT/.ufo/waves/arc3-loop1-round9/claims/c2/EX-9"
EVIDENCE="$SEAT/evidence"
SRC="$ROOT/.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
RUN="$(mktemp -d /var/tmp/kaidoku-ex9-r9.XXXXXX)"

mkdir -p "$EVIDENCE" "$RUN/tmp"
cp "$SRC" "$EVIDENCE/K8.vy"

{
  printf 'git_head='
  git rev-parse HEAD
  printf 'source_path=%s\n' "$SRC"
  sha256sum "$SRC" "$EVIDENCE/K8.vy"
  printf 'compiler_path=%s\n' "$VYPER"
  sha256sum "$VYPER"
  "$VYPER" --version
  printf 'scratch=%s\nTMPDIR=%s\n' "$RUN" "$RUN/tmp"
} 

for mode in noopt none; do
  case "$mode" in
    noopt) args=(--no-optimize) ;;
    none) args=(-O none) ;;
  esac
  for pass in 1 2; do
    env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f bytecode_runtime "$EVIDENCE/K8.vy" > "$RUN/$mode.$pass.runtime.hex"
  done
  cmp "$RUN/$mode.1.runtime.hex" "$RUN/$mode.2.runtime.hex"
  cp "$RUN/$mode.1.runtime.hex" "$EVIDENCE/$mode.runtime.hex"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f abi "$EVIDENCE/K8.vy" > "$RUN/$mode.abi.json"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f method_identifiers "$EVIDENCE/K8.vy" > "$RUN/$mode.methodids.json"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f settings "$EVIDENCE/K8.vy" > "$RUN/$mode.settings.json"
  cp "$RUN/$mode.abi.json" "$EVIDENCE/$mode.abi.json"
  cp "$RUN/$mode.methodids.json" "$EVIDENCE/$mode.methodids.json"
  cp "$RUN/$mode.settings.json" "$EVIDENCE/$mode.settings.json"
done

cmp "$EVIDENCE/noopt.runtime.hex" "$EVIDENCE/none.runtime.hex"
cmp "$EVIDENCE/noopt.abi.json" "$EVIDENCE/none.abi.json"
cmp "$EVIDENCE/noopt.methodids.json" "$EVIDENCE/none.methodids.json"
cmp "$EVIDENCE/noopt.settings.json" "$EVIDENCE/none.settings.json"

TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 --version
for mode in noopt none; do
  env TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$EVIDENCE/$mode.runtime.hex" hex --format json > "$EVIDENCE/$mode.probe.json"
done

printf 'repeat_runtime_passes=PASS\n'
printf 'runtime_exact_bytes_noopt_vs_none=PASS\n'
printf 'abi_exact_bytes_noopt_vs_none=PASS\n'
printf 'method_identifiers_exact_bytes_noopt_vs_none=PASS\n'
printf 'settings_exact_bytes_noopt_vs_none=PASS\n'
printf 'rea_probe_inputs=%s,%s\n' "$EVIDENCE/noopt.runtime.hex" "$EVIDENCE/none.runtime.hex"
printf 'scratch_preserved=%s\n' "$RUN"
sha256sum "$EVIDENCE"/{K8.vy,noopt.runtime.hex,none.runtime.hex,noopt.abi.json,none.abi.json,noopt.methodids.json,none.methodids.json,noopt.settings.json,none.settings.json,noopt.probe.json,none.probe.json}
