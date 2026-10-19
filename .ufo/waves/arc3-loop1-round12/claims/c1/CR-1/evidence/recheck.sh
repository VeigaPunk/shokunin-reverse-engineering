#!/usr/bin/env bash
set -euo pipefail
repo="$(git rev-parse --show-toplevel)"
evidence="$repo/.ufo/waves/arc3-loop1-round12/claims/c1/CR-1/evidence"
rea="/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs"
scratch="$(mktemp -d /var/tmp/kaidoku-cr1-goid-recheck.XXXXXX)"
trap 'rm -rf -- "$scratch"' EXIT
mkdir -p "$scratch/tmp" "$scratch/copy-a" "$scratch/copy-b"
cp --reflink=auto /usr/bin/docker "$scratch/copy-a/docker"
cp --reflink=auto /usr/bin/docker "$scratch/copy-b/docker"
run_probe() {
  local name="$1" target="$2"
  mkdir -p "$scratch/tmp/$name"
  TMPDIR="$scratch/tmp/$name" node "$rea" inspect-go-binary "$target" --format json --full-output > "$scratch/go-$name.json" 2> "$scratch/go-$name.stderr"
  test ! -s "$scratch/go-$name.stderr"
}
run_probe base1 /usr/bin/docker
run_probe base2 /usr/bin/docker
run_probe copyA "$scratch/copy-a/docker"
run_probe copyB "$scratch/copy-b/docker"
sha256sum /usr/bin/docker "$scratch/copy-a/docker" "$scratch/copy-b/docker"
node "$evidence/recompute-ids.mjs" "$scratch"
