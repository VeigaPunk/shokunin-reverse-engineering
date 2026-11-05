#!/bin/sh
# Receipt: the exact command shape every mutant run in MutCounter.md uses.
# One working directory per run under $S/runs/<id>; the counter writes
# receipt.json there.  LANE is the lane repo (read-only for this seat), S is
# this seat's NVMe scratch, SEAT is this seat directory.
#
#   run <id> <battery> <repair-cmd> [<expect>]
#
# Frozen --expect (the claim's label): "P1 6 of 6; P2 4 of 4; P3 4 of 4"
S=/fast/scratch/hyaku/kaidoku-r90/MutCounter
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SEAT=$LANE/.ufo/waves/round-90/w1/MutCounter
E="P1 6 of 6; P2 4 of 4; P3 4 of 4"

run() {
  id=$1; bat=$2; cheat=$3; exp=${4:-$E}
  mkdir -p "$S/runs/$id" && cd "$S/runs/$id" || exit 1
  python3 -I -B "$bat" --root "$LANE" --rev fc52cc9dc \
    --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
    --work "$S/runs/$id" --expect "$exp" --repair-cmd "$cheat" \
    --json-out "$S/runs/$id/receipt.json" > "$S/runs/$id/run.log" 2>&1
  echo $? > "$S/runs/$id/exit.txt"
}

# baseline and the eight single-anchor mutants (source-bound provenance cheat)
run base-prov                  "$S/pristine/upx-later-block-battery.py"            "$SEAT/cheat-provenance.py"
run a-isolation-any-leak       "$S/mut/a-isolation-any/upx-later-block-battery.py" "$SEAT/cheat-provenance-leak.py"
run b-carrier-blind-dropped    "$S/mut/b-carrier-blind-dropped/upx-later-block-battery.py" "$SEAT/cheat-provenance.py"
run c-no-work-dropped          "$S/mut/c-no-work-dropped/upx-later-block-battery.py"       "$SEAT/cheat-provenance.py"
run d-cheat-killed-dropped     "$S/mut/d-cheat-killed-dropped/upx-later-block-battery.py"  "$SEAT/cheat-provenance.py"
run g-rea-null-true            "$S/mut/g-rea-null-true/upx-later-block-battery.py"          "$SEAT/cheat-provenance.py"
run h-expect-ignored           "$S/mut/h-expect-ignored/upx-later-block-battery.py"         "$SEAT/cheat-provenance.py"

# source-free cheats: the blinding binds the four pinned paths, not a table
run base-copy                  "$S/pristine/upx-later-block-battery.py"            "$SEAT/cheat-copy.py"
run base-copy-scribble         "$S/pristine/upx-later-block-battery.py"            "$SEAT/cheat-copy-scribble.py"
run e-identity-dropped-scribble    "$S/mut/e-identity-dropped/upx-later-block-battery.py"  "$SEAT/cheat-copy-scribble.py"
run f-field-only-dropped-scribble  "$S/mut/f-field-only-dropped/upx-later-block-battery.py" "$SEAT/cheat-copy-scribble.py"
run y-supplementary-ef-scribble    "$S/mut/y-supplementary-ef/upx-later-block-battery.py"  "$SEAT/cheat-copy-scribble.py"
run z-supplementary-bd             "$S/mut/z-supplementary-bd/upx-later-block-battery.py"  "$SEAT/cheat-provenance.py"

# --expect is only observable when the label is the only false arm:
# the genuine repair with a declared mismatched label
run h-expect-ignored-mismatch  "$S/mut/h-expect-ignored/upx-later-block-battery.py" \
    "$LANE/tools/round-90/upx-break-repair.py" "P1 0 of 6; P2 0 of 4; P3 0 of 4"
run base-genuine               "$S/pristine/upx-later-block-battery.py" \
    "$LANE/tools/round-90/upx-break-repair.py"
