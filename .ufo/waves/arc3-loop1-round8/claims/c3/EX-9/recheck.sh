#!/usr/bin/env bash
set -eu

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$ROOT" rev-parse --show-toplevel)
SOURCE="$REPO/.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy"
VYPER="$REPO/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
WORK=$(mktemp -d /var/tmp/kaidoku-r8-vyper-recheck-XXXXXX)
mkdir -p "$WORK/tmp"

cmp "$SOURCE" "$ROOT/build/K8.vy"
cp "$ROOT/build/K8.vy" "$WORK/K8.vy"
sha256sum "$SOURCE" "$WORK/K8.vy" "$VYPER"
printf 'vyper_version='; "$VYPER" --version

for form in gas noopt none codesize; do
  case "$form" in
    gas) args=(-O gas) ;;
    noopt) args=(--no-optimize) ;;
    none) args=(-O none) ;;
    codesize) args=(-O codesize) ;;
  esac
  TMPDIR="$WORK/tmp" "$VYPER" "${args[@]}" -f bytecode_runtime "$WORK/K8.vy" > "$WORK/$form.runtime.hex"
  TMPDIR="$WORK/tmp" "$VYPER" "${args[@]}" -f abi "$WORK/K8.vy" > "$WORK/$form.abi.json"
  TMPDIR="$WORK/tmp" "$VYPER" "${args[@]}" -f method_identifiers "$WORK/K8.vy" > "$WORK/$form.methodids.json"
  TMPDIR="$WORK/tmp" "$VYPER" "${args[@]}" -f settings "$WORK/K8.vy" > "$WORK/$form.settings.json"
  TMPDIR="$WORK/tmp" "$VYPER" "${args[@]}" -f bytecode_runtime "$WORK/K8.vy" > "$WORK/$form.repeat.runtime.hex"
  cmp "$WORK/$form.runtime.hex" "$WORK/$form.repeat.runtime.hex"
done
TMPDIR="$WORK/tmp" "$VYPER" -f bytecode_runtime "$WORK/K8.vy" > "$WORK/default.runtime.hex"
cmp "$WORK/default.runtime.hex" "$WORK/gas.runtime.hex"
printf 'default_equals_explicit_gas=true\n'

python3 "$ROOT/rederive.py" "$WORK"
TMPDIR="$WORK/tmp" npx -y rea-agents@6.7.0 --version
for form in gas noopt codesize; do
  TMPDIR="$WORK/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$WORK/$form.runtime.hex" hex --format json > "$WORK/probe-$form.json"
done
python3 "$ROOT/verify-probes.py" "$WORK"
printf 'scratch=%s\n' "$WORK"
