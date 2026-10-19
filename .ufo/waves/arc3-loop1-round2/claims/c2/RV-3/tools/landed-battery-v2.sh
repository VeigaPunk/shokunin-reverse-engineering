#!/bin/bash
# RV-3 landed-v11 mutation battery (v2). Reads the real census, writes nothing there.
set -u
BASE=/var/tmp/rv3-mutation
LAND=$BASE/landed
OUT=$BASE/receipts/landed
mkdir -p "$OUT/instr" "$OUT/receipts"

cp "$LAND/landed.py" "$OUT/instr/10-landed.py"
cp "$BASE/work/v10.py" "$OUT/instr/09-v10-baseline.py"
python3 "$BASE/mutate-h1-v2.py" "$LAND/landed.py" "$BASE/landed/mut" > "$OUT/mutation-footprint.txt" 2>&1
cat "$OUT/mutation-footprint.txt"
cp "$LAND/mut/mutant-m-term.py"  "$OUT/instr/11-m-term.py"
cp "$LAND/mut/mutant-m-eof.py"   "$OUT/instr/12-m-eof.py"
cp "$LAND/mut/mutant-m-full.py"  "$OUT/instr/13-m-full.py"
cp "$LAND/mut/mutant-m-h3.py"    "$OUT/instr/14-m-h3.py"

for d in 11-m-term 12-m-eof 13-m-full 14-m-h3; do
  python3 -c "import ast;ast.parse(open('$OUT/instr/$d.py').read())" || echo "SYNTAX FAIL $d"
done
for m in m-term m-eof m-full m-h3; do
  diff -u "$LAND/landed.py" "$LAND/mut/mutant-$m.py" > "$OUT/diff-landed-vs-$m.diff" || true
done

# --- fixtures (fresh HEAD copies of the three scoped files) ---
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
mkdir -p "$BASE/fx-head"
cp "$REPO/PROVINCE.md" "$REPO/SCORECARD.md" "$REPO/SKILL.md" "$BASE/fx-head/"
mk() {  # mk <name> <files...> ; SKILL.md optionally mutated by the caller
  d="$BASE/$1"; rm -rf "$d"; mkdir -p "$d"; shift
  for f in "$@"; do cp "$BASE/fx-head/$f" "$d/"; done
}
mk fixture-full PROVINCE.md SCORECARD.md SKILL.md
mk fixture-noskill PROVINCE.md SCORECARD.md
mk fixture-noprovi SCORECARD.md SKILL.md
mk fixture-noscore PROVINCE.md SKILL.md
mk fixture-allabsent
mk fixture-emptyskill PROVINCE.md SCORECARD.md SKILL.md; : > "$BASE/fixture-emptyskill/SKILL.md"
mk fixture-shortskill PROVINCE.md SCORECARD.md SKILL.md; head -10 "$BASE/fx-head/SKILL.md" > "$BASE/fixture-shortskill/SKILL.md"
mk fixture-dirskill PROVINCE.md SCORECARD.md; mkdir -p "$BASE/fixture-dirskill/SKILL.md"
mk fixture-permskill PROVINCE.md SCORECARD.md SKILL.md; chmod 000 "$BASE/fixture-permskill/SKILL.md"

FIXTURES="fixture-full fixture-noskill fixture-emptyskill fixture-shortskill fixture-dirskill fixture-permskill fixture-noprovi fixture-noscore fixture-allabsent atk-silent atk-undecl"
printf '%-14s %-18s %-5s %-8s %s\n' INSTRUMENT FIXTURE EXIT VERDICT UNREADABLE
for fx in $FIXTURES; do
  d="$BASE/$fx"; [ -d "$d" ] || continue
  for instr in "$OUT"/instr/*.py; do
    name=$(basename "$instr" .py)
    rec="$OUT/receipts/${name}__${fx}.txt"
    python3 "$instr" --root "$d" >"$rec" 2>&1
    rc=$?
    verdict=$(grep -m1 -o 'VERDICT: [A-Z]*' "$rec" | cut -d' ' -f2)
    unread=$(grep -m1 '^UNREADABLE' "$rec" | cut -c24-70)
    printf '%-14s %-18s %-5s %-8s %s\n' "$name" "$fx" "$rc" "${verdict:-<n/a>}" "${unread:--}"
  done
done
echo "receipts: $OUT/receipts"
