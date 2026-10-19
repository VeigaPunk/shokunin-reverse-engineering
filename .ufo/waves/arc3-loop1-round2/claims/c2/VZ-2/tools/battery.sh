#!/bin/bash
# usage: battery.sh <instrument.py> <tag>
I="$1"; TAG="$2"; O=/var/tmp/vz2/out/$TAG; R=/var/tmp/vz2/roots
mkdir -p $O; rm -f $O/*.out $O/*.json 2>/dev/null
sha256sum "$I" > $O/instrument.sha
run () { # run <name> <root> [instrument-override]
  local name="$1" root="$2" instr="${3:-$I}"
  echo "###### $name  (root=$root instr=$instr)" > $O/$name.out
  python3 "$instr" --root "$root" >> $O/$name.out 2>&1
  echo "EXIT=$?" >> $O/$name.out
}
run t0-baseline          $R/baseline
run t1-absent-skill      $R/absent-skill
run t2-empty-skill       $R/empty-skill
run t3-absent-province   $R/absent-province
run t4-no-checks         $R/no-checks
python3 "$I" --root $R/baseline --json > $O/t0-baseline.json 2>&1; echo "EXIT=$?" >> $O/t0-baseline.json
# blind instrument (needles neutered), same real root
python3 /var/tmp/vz2/tools/blind.py "$I" $O/blind-census.py > $O/blind-build.log 2>&1
run t5-blind-instrument  $R/baseline $O/blind-census.py
for f in t0-baseline t1-absent-skill t2-empty-skill t3-absent-province t4-no-checks t5-blind-instrument; do
  echo "--- $f: $(grep -m1 '^VERDICT' $O/$f.out || grep -m1 -E 'ANCHOR-FAIL|Traceback' $O/$f.out || echo NOVERDICT)  $(grep -m1 '^EXIT' $O/$f.out)"
done
