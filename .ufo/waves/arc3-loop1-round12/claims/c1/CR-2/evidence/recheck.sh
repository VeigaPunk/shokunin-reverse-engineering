#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd -- "$(dirname -- "$0")" && pwd)"
REA=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs
SCRATCH="$(mktemp -d /var/tmp/kaidoku-cr2-r12-recheck.XXXXXX)"
mkdir -p "$SCRATCH/tmp" "$SCRATCH/a" "$SCRATCH/b"
cp /usr/bin/jq "$SCRATCH/a/jq"
cp /usr/bin/jq "$SCRATCH/b/jq"
sha256sum /usr/bin/jq "$SCRATCH/a/jq" "$SCRATCH/b/jq"
cmp -s /usr/bin/jq "$SCRATCH/a/jq"
cmp -s /usr/bin/jq "$SCRATCH/b/jq"
TMPDIR="$SCRATCH/tmp" node "$REA" function /usr/bin/jq 0x1091f0 --format json --full-output > "$SCRATCH/base.json"
TMPDIR="$SCRATCH/tmp" node "$REA" function "$SCRATCH/a/jq" 0x1091f0 --format json --full-output > "$SCRATCH/copy-a.json"
TMPDIR="$SCRATCH/tmp" node "$REA" function "$SCRATCH/b/jq" 0x1091f0 --format json --full-output > "$SCRATCH/copy-b.json"
python3 "$HERE/recompute-ids.py" "$SCRATCH"
