#!/bin/bash
# CR-5 robustness battery: cross-round legit-change blast radius + records emulation.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
H=/var/tmp/cr5-r3/attacks/harness.sh
TABLE=$R/.ufo/gates/citation-drift/pointer-table.json
OUT=/var/tmp/cr5-r3/attacks/receipts/robustness-battery.txt
: > "$OUT"

emit() { echo "$@" >> "$OUT"; }

# ---- (A) records emulation: workcommit state + appended round-3 records ----
C=/var/tmp/cr5-r3/scratch/workclone
emit "#### (A) records emulation on top of the work-commit emulation (gates already committed)"
python3 - "$R" "$C" <<'PY'
import sys
R,C=sys.argv[1],sys.argv[2]
sc=open(R+'/.ufo/waves/arc3-loop1-round3/claims/cross/CN-2/merged-SCORECARD-section.md').read()
sc=sc.split('<!-- BEGIN LITERAL SECTION TEXT -->')[1].split('<!-- END LITERAL SECTION TEXT -->')[0]
lg=open(R+'/.ufo/waves/arc3-loop1-round3/claims/cross/CN-2/merged-LOG-entry.md').read()
lg=lg.split('<!-- BEGIN LITERAL ENTRY TEXT -->')[1]
open(C+'/SCORECARD.md','a').write('\n'+sc)
open(C+'/LOG.md','a').write('\n'+lg)
PY
git -C $C -c user.email=e@x -c user.name=e commit -qam "records emulation: append round-3 SCORECARD section + LOG entry"
REV=$(git -C $C rev-parse HEAD)
emit "records rev=$REV"
bash "$H" "$TABLE" "$REV" "$C" 2>&1 | grep -E "CITATION_DRIFT:|VERDICT" >> "$OUT"

# ---- (B) SCORECARD head rewrite (+1 line inserted near the top) ----
C2=/var/tmp/cr5-r3/scratch/clone
git -C $C2 reset -q --hard c07af80
python3 - "$C2" <<'PY'
import sys
p=sys.argv[1]+'/SCORECARD.md'
lines=open(p).read().split('\n')
lines.insert(12,'(simulated next-round head rewrite: one inserted line)')
open(p,'w').write('\n'.join(lines))
PY
git -C $C2 -c user.email=e@x -c user.name=e commit -qam "sim: SCORECARD head rewrite +1 line"
REV=$(git -C $C2 rev-parse HEAD)
emit ""
emit "#### (B) SCORECARD head rewrite +1 line at :13  rev=$REV"
bash "$H" "$TABLE" "$REV" "$C2" 2>&1 | grep -E "CITATION_DRIFT:|VERDICT" >> "$OUT"

# ---- (C) SHONEN:6 legit refresh (81-255 -> 81-256, 14/14 -> 15/15) ----
git -C $C2 reset -q --hard c07af80
python3 - "$C2" <<'PY'
import sys
p=sys.argv[1]+'/SHONEN.md'
s=open(p).read()
s=s.replace('SKILL.md:81-255','SKILL.md:81-256',1).replace('14/14 rule blocks','15/15 rule blocks',1)
open(p,'w').write(s)
PY
git -C $C2 -c user.email=e@x -c user.name=e commit -qam "sim: SHONEN:6 refresh 81-256/15-15"
REV=$(git -C $C2 rev-parse HEAD)
emit ""
emit "#### (C) SHONEN:6 legit refresh (81-256, 15/15)  rev=$REV"
bash "$H" "$TABLE" "$REV" "$C2" 2>&1 | grep -E "CITATION_DRIFT:|VERDICT" >> "$OUT"

git -C $C2 reset -q --hard c07af80
emit ""
echo "written $OUT"