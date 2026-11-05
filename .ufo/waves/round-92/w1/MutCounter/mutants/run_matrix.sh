#!/usr/bin/env bash
# MutCounter kill-matrix driver (scratch only). Runs each mutant through the frozen counter
# it targets, with the frozen --expect label. Counters are NOT edited; mutants live in
# $S/clone/.ufo/mut/. One receipt + one stdout/stderr pair per run; one log line per run.
set -u
S=/fast/scratch/hyaku/kaidoku-r92/MutCounter
C=$S/clone
R=$S/rec
REV=11f8606178dfd9e72001b31daf412c5463106a63
V2_COUNTER=tools/round-92/stop-boundary-battery-v2.py
C1_COUNTER=tools/round-92/stop-boundary-repair-battery.py
V2_EXPECT="refused 10 of 10; typed 10; unsafe 0; intact 5 of 5"
C1_EXPECT="repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10"
mkdir -p "$R" "$S/tmp" "$S/work"
: > "$R/matrix.log"
cd "$C" || exit 2

run() {
  # run <id> <counter-rel-path> <repair-cmd-rel-to-clone> <expect>
  local id="$1" counter="$2" cmd="$3" expect="$4" rc label
  TMPDIR="$S/tmp" python3 -I -B "$counter" --root "$C" --repair-cmd "$cmd" \
    --work "$S/work/$id" --rev "$REV" --expect "$expect" --json-out "$R/$id.json" \
    > "$R/$id.stdout" 2> "$R/$id.stderr"
  rc=$?
  label=$(tail -n 1 "$R/$id.stdout")
  printf '%s\t%s\t%s\texit=%s\t%s\n' "$id" "$counter" "$cmd" "$rc" "$label" >> "$R/matrix.log"
}

# R92-C2 counterfeits against the calibration counter (v2); X1 is an extra (v2 unsafe gate)
for m in M1 M2 M3 M4 M5 M6 CA CB CC X1; do
  run "$m" "$V2_COUNTER" ".ufo/mut/$m.py" "$V2_EXPECT"
done
# R92-C1 mutants against the coverage counter (repair battery)
for n in N1 N1i N2 N3 N4 N4i N5; do
  run "$n" "$C1_COUNTER" ".ufo/mut/$n.py" "$C1_EXPECT"
done
echo "DRIVER DONE $(wc -l < "$R/matrix.log") runs"
