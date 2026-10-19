#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
HERE=$(cd "$(dirname "$0")" && pwd)
EVIDENCE="$HERE/evidence"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
PYTHON="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/python"
SCRATCH=$(mktemp -d /var/tmp/kaidoku-r8-sc1-recheck.XXXXXX)
mkdir -p "$SCRATCH/tmp"
cp "$EVIDENCE/K8.vy" "$SCRATCH/K8.vy"
printf 'scratch=%s\n' "$SCRATCH"
printf 'source_sha256='; sha256sum "$SCRATCH/K8.vy"
printf 'vyper_sha256='; sha256sum "$VYPER"
printf 'vyper_version='; TMPDIR="$SCRATCH/tmp" "$VYPER" --version
printf 'rea_version='; TMPDIR="$SCRATCH/tmp" npx -y rea-agents@6.7.0 --version
for MODE in gas noopt codesize; do
  case "$MODE" in
    gas) FLAGS=();;
    noopt) FLAGS=(--no-optimize);;
    codesize) FLAGS=(-O codesize);;
  esac
  TMPDIR="$SCRATCH/tmp" "$VYPER" "${FLAGS[@]}" -f bytecode_runtime "$SCRATCH/K8.vy" > "$SCRATCH/$MODE.runtime.hex"
  TMPDIR="$SCRATCH/tmp" "$VYPER" "${FLAGS[@]}" -f abi "$SCRATCH/K8.vy" > "$SCRATCH/$MODE.abi.json"
  TMPDIR="$SCRATCH/tmp" "$VYPER" "${FLAGS[@]}" -f method_identifiers "$SCRATCH/K8.vy" > "$SCRATCH/$MODE.methodids.json"
  TMPDIR="$SCRATCH/tmp" "$VYPER" "${FLAGS[@]}" -f settings "$SCRATCH/K8.vy" > "$SCRATCH/$MODE.settings.json"
done
for MODE in noopt codesize; do
  TMPDIR="$SCRATCH/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$SCRATCH/$MODE.runtime.hex" hex --format json > "$SCRATCH/rea-$MODE.json"
done
"$PYTHON" "$HERE/rederive.py" "$SCRATCH"
