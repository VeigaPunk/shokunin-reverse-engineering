#!/bin/bash
# RV-3 scenario runner. Usage: run-suite.sh <outdir-tag>
# Runs every instrument in /var/tmp/rv3-mutation/instr/*.py against the two
# fixtures, capturing stdout+exit code per run.
set -u
TAG="${1:-run}"
BASE=/var/tmp/rv3-mutation
OUT=$BASE/receipts/$TAG
mkdir -p "$OUT"

# fixture with all three scoped files present (SKILL.md copied in)
mkdir -p "$BASE/fixture-full"
cp "$BASE/fixture/PROVINCE.md" "$BASE/fixture/SCORECARD.md" "$BASE/fixture-full/" 2>/dev/null
cp /home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md "$BASE/fixture-full/"

printf '%-22s %-10s %-14s %-6s %s\n' INSTRUMENT FIXTURE EXIT UNREADABLE VERDICT
for instr in "$BASE"/instr/*.py; do
  name=$(basename "$instr" .py)
  for fx in fixture-full fixture-noskill fixture; do
    [ -d "$BASE/$fx" ] || continue
    out="$OUT/${name}__${fx}.txt"
    python3 "$instr" --root "$BASE/$fx" >"$out" 2>&1
    rc=$?
    verdict=$(grep -m1 -o 'VERDICT: [A-Z]*' "$out" | head -1)
    unread=$(grep -m1 '^UNREADABLE' "$out" | cut -c1-60)
    printf '%-22s %-10s %-6s %-14s %s\n' "$name" "$fx" "$rc" "${unread:-<none>}" "$verdict"
  done
done
echo "receipts: $OUT"
