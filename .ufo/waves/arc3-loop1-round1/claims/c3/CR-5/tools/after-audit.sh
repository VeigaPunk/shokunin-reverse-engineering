#!/usr/bin/env bash
# CR-5 after-audit: run this the moment EX-28's edit lands (or the parent
# integrates). All read-only except nothing; prints verdicts.
# Usage: bash after-audit.sh [before-census.py]
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
BEFORE=${1:-$REPO/.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/census-before.py}
TOOLS=$REPO/.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools
AFTER=$REPO/.ufo/gates/c1-census-v10.py
echo "== 1. scope diff (creep flags) =="
python3 "$TOOLS/scope-diff.py" "$BEFORE" "$AFTER"; echo "diff-exit=$?"
echo "== 2. behavioral identity (stdout sha; header-only edit must keep 3b677b8e…) =="
python3 "$AFTER" 2>/dev/null | sha256sum
echo "== 3. locus-count invariance (expect PROVINCE 6 / SCORECARD 9 / SKILL 2; current-ok 10) =="
python3 "$AFTER" 2>/dev/null | head -5
python3 "$AFTER" 2>/dev/null | grep -c "current-ok"
echo "== 4. falsifiability suite against the after-instrument =="
python3 "$TOOLS/run-injections.py" "$AFTER" after
echo "== 5. blind-instrument check (expect FAIL/SUSPECT after the G2 patch, PASS before it) =="
sed -e 's/PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)/PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)/' "$AFTER" > /dev/shm/cr5/after-blind.py
python3 /dev/shm/cr5/after-blind.py --root /dev/shm/cr5/root-before 2>/dev/null | grep -E "G2|VERDICT"
echo "== 6. independent coverage checker =="
python3 "$TOOLS/independent-census.py" "$AFTER" /dev/shm/cr5/root-before 2>/dev/null | tail -3
