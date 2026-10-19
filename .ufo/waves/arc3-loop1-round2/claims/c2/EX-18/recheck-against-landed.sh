#!/usr/bin/env bash
# EX-18 r2 re-run protocol: absent-PROVINCE.md control against the LANDED
# instrument. Read-only on the repo; scratch under /dev/shm.
# Usage: bash recheck-against-landed.sh [REPO_ROOT]
set -u
REPO="${1:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}"
W=/dev/shm/ex18-r2/recheck
CENSUS="$REPO/.ufo/gates/c1-census-v10.py"
rm -rf "$W"; mkdir -p "$W"

echo "== landed identity =="
git -C "$REPO" rev-parse HEAD
sha256sum "$CENSUS" "$REPO/PROVINCE.md" "$REPO/SKILL.md" "$REPO/SCORECARD.md"

fresh() { rm -rf "$1"; mkdir -p "$1"; cp "$REPO/PROVINCE.md" "$REPO/SKILL.md" "$REPO/SCORECARD.md" "$1/"; }
case_run() { # case_run <label> <drop-file|none>
  local lab="$1" drop="$2" root="$W/$1"
  fresh "$root"; [ "$drop" != none ] && rm -f "$root/$drop"
  python3 "$CENSUS" --root "$root" > "$W/$lab.out" 2>&1; local rc=$?
  python3 "$CENSUS" --root "$root" --json > "$W/$lab.json" 2>&1
  local cls jsoncause
  cls=$(grep -o "SCOPE-ERRORS.*" "$W/$lab.out" | head -c 130)
  jsoncause=$(python3 - "$W/$lab.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print("verdict=%s scope_errors=%d unreadable=%r" % (
      d["verdict"], len(d["scope_errors"]), d.get("unreadable", "<absent key>")))
PY
)
  printf "%-14s exit=%-2s %s\n" "$lab" "$rc" "$cls"
  printf "%-14s %s\n" "" "$jsoncause"
}
echo "== repo root (baseline) =="
python3 "$CENSUS" > "$W/B0.out" 2>&1; echo "B0 exit=$? $(grep -o 'VERDICT: [A-Z]*.*' "$W/B0.out" | head -1)"
case_run S1 PROVINCE.md
case_run S6 SKILL.md
case_run S7 SCORECARD.md
echo "== logs: $W =="
