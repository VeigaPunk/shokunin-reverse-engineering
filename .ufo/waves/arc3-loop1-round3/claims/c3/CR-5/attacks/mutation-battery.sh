#!/bin/bash
# CR-5 mutation battery: measure which needles fire under which drift class.
# Runs in the scratch clone only (no repo mutation). Real table = negative control.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
CLONE=/var/tmp/cr5-r3/scratch/clone
H=/var/tmp/cr5-r3/attacks/harness.sh
OUT=/var/tmp/cr5-r3/attacks/receipts/mutation-battery.txt
: > "$OUT"
git -C "$REPO" show HEAD:.ufo/gates/citation-drift/pointer-table.json > /var/tmp/cr5-r3/attacks/baseline-31.json
cp "$REPO/.ufo/gates/citation-drift/pointer-table.json" /var/tmp/cr5-r3/attacks/landed-table.json

run_case() {
  local label="$1"
  git -C "$CLONE" -c user.email=e@x -c user.name=e commit -qam "$label"
  local rev; rev=$(git -C "$CLONE" rev-parse HEAD)
  echo "#### MUTATION: $label  rev=$rev" >> "$OUT"
  for t in baseline-31.json landed-table.json cr5-candidates.json ex43-candidates-as-table.json; do
    echo "-- table=$t" >> "$OUT"
    bash "$H" "/var/tmp/cr5-r3/attacks/$t" "$rev" "$CLONE" 2>&1 | grep -E "CITATION_DRIFT:|VERDICT" >> "$OUT"
  done
  echo >> "$OUT"
}

# reset clone to pristine HEAD
git -C "$CLONE" reset -q --hard c07af80

# A) citing re-point out of range (my choice: entry:26 r3-evm :93-96 -> :100-104)
python3 - "$CLONE" <<'PY'
import sys
p=sys.argv[1]+'/corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md'
s=open(p).read(); assert 'r3-evm-interface.md:93-96' in s
open(p,'w').write(s.replace('r3-evm-interface.md:93-96','r3-evm-interface.md:100-104',1))
PY
run_case "A citing re-point entry:26 -> :100-104 (out of content)"

# B) target content moved: insert a row above QUALITY row 14 -> :24-25 shift to :25-26
git -C "$CLONE" reset -q --hard c07af80
python3 - "$CLONE" <<'PY'
import sys
p=sys.argv[1]+'/corpus/QUALITY.md'
lines=open(p).read().split('\n')
idx=next(i for i,l in enumerate(lines) if l.startswith('| 14 |'))
lines.insert(idx, '| 13b | (scratch-inserted row for mutation battery) | x | 13 |')
open(p,'w').write('\n'.join(lines))
PY
run_case "B target shift: QUALITY row 14 inserted above (cited :24-25 now lacks the row)"

# C) range end stale: SHONEN.md:6 81-255 -> 81-243 (keeps rule #13 in range)
git -C "$CLONE" reset -q --hard c07af80
python3 - "$CLONE" <<'PY'
import sys
p=sys.argv[1]+'/SHONEN.md'
s=open(p).read(); assert 'SKILL.md:81-255' in s
open(p,'w').write(s.replace('SKILL.md:81-255','SKILL.md:81-243',1))
PY
run_case "C stale range end: SHONEN:6 81-255 -> 81-243 (rule 13 still inside)"

# D) SCORECARD citing re-point SHONEN.md:6 -> SHONEN.md:7
git -C "$CLONE" reset -q --hard c07af80
python3 - "$CLONE" <<'PY'
import sys
p=sys.argv[1]+'/SCORECARD.md'
s=open(p).read().split('\n')
s[1434]=s[1434].replace('SHONEN.md:6 refreshed','SHONEN.md:7 refreshed')
open(p,'w').write('\n'.join(s))
PY
run_case "D citing re-point SCORECARD:1435 -> SHONEN.md:7"

# E) SKILL rule-14 re-point LOG.md:1411-1412 -> 1413-1414
git -C "$CLONE" reset -q --hard c07af80
python3 - "$CLONE" <<'PY'
import sys
p=sys.argv[1]+'/SKILL.md'
s=open(p).read(); assert 'LOG.md:1411-1412' in s
open(p,'w').write(s.replace('LOG.md:1411-1412','LOG.md:1413-1414',1))
PY
run_case "E citing re-point SKILL:254 -> LOG.md:1413-1414"

git -C "$CLONE" reset -q --hard c07af80
echo "battery written: $OUT"