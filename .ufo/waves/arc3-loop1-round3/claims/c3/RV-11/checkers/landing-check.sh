#!/bin/bash
# RV-11 landing check for the C3 pointer-table edit (EX-41's target).
# Read-only over the repo; writes only under /var/tmp/rv11-arc3r3/.
# Usage: landing-check.sh [REPO]
set -u
REPO="${1:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}"
OUT=/var/tmp/rv11-arc3r3/runs
mkdir -p "$OUT"
cd "$REPO" || exit 3
T=.ufo/gates/citation-drift/pointer-table.json
E=.ufo/gates/citation-drift/expected.json
P=.ufo/gates/citation-drift/citation-drift-probe.py
REV=$(git rev-parse HEAD)

echo "== repo=$REPO rev=$REV"
echo "== sha256 table: $(sha256sum "$T" | cut -d' ' -f1)"
echo "== sha256 expected: $(sha256sum "$E" | cut -d' ' -f1)"
echo "== sha256 probe: $(sha256sum "$P" | cut -d' ' -f1)"
echo "== pin in expected.json: $(python3 -c "import json;print(json.load(open('$E'))['pointer_table']['sha256'])")"
echo "== entries: $(python3 -c "import json;print(len(json.load(open('$T'))['entries']))")"

echo "== probe normal mode"
python3 "$P" --root . --rev "$REV" --table "$T" --expected "$E"; echo "exit=$?"
echo "== probe strict mode"
python3 "$P" --root . --rev "$REV" --table "$T" --expected "$E" --strict; echo "exit=$?"
echo "== probe selftest"
python3 "$P" --selftest --expected "$E"; echo "exit=$?"
echo "== rule11 audit"
python3 /var/tmp/rv11-arc3r3/checker/rule11-audit.py --root . --table "$T" \
  --expected "$E" --json "$OUT/landed-audit.json"