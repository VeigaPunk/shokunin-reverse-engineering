#!/usr/bin/env bash
set -euo pipefail
EVIDENCE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PACKAGE_ROOT=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents
SCRATCH="$(mktemp -d /var/tmp/kaidoku-cr3-r12-recheck.XXXXXX)"
trap 'rm -rf "$SCRATCH"' EXIT
sha256sum -c "$EVIDENCE/source-files.sha256"
mkdir -p "$SCRATCH/tmp" "$SCRATCH/alternate" "$SCRATCH/renamed"
EXPECTED=e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
ACTUAL="$(sha256sum /usr/bin/jq | cut -d' ' -f1)"
test "$ACTUAL" = "$EXPECTED"
cp -- /usr/bin/jq "$SCRATCH/alternate/jq"
cp -- /usr/bin/jq "$SCRATCH/renamed/jq-copy"
sha256sum /usr/bin/jq "$SCRATCH/alternate/jq" "$SCRATCH/renamed/jq-copy"
run_probe() {
  local name="$1" target="$2"
  if TMPDIR="$SCRATCH/tmp" node "$PACKAGE_ROOT/scripts/rea.mjs" inspect-artifact "$target" --format json --full-output > "$SCRATCH/$name.json" 2> "$SCRATCH/$name.stderr"; then
    printf '%s rc=0 stderr_bytes=%s\n' "$name" "$(wc -c < "$SCRATCH/$name.stderr")"
  else
    local rc=$?
    printf '%s rc=%s\n' "$name" "$rc"
    return "$rc"
  fi
}
run_probe base-1 /usr/bin/jq
run_probe base-2 /usr/bin/jq
run_probe alt-same-name "$SCRATCH/alternate/jq"
run_probe alt-different-name "$SCRATCH/renamed/jq-copy"
node "$EVIDENCE/rederive.mjs" "$SCRATCH"
