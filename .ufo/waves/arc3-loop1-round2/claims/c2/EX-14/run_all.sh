#!/bin/bash
# EX-14 receipts: every command, its exit code, and its verdict line.
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SCRATCH=/var/tmp/ex14
run() {  # run <label> <census> <root>
  local label="$1" census="$2" root="$3"
  local out="$SCRATCH/receipts-$label.out"
  python3 "$census" --root "$root" > "$out" 2>&1
  local ec=$?
  printf '%-34s exit=%d  | %s | %s\n' "$label" "$ec" \
    "$(grep -m1 'G2 positive-assertion guard' "$out" | sed 's/^ *//')" \
    "$(grep -m1 '^VERDICT' "$out" | sed 's/^ *//')"
}
mkdir -p "$SCRATCH/receipts"
printf '%s\n' "census HEAD sha256: $(sha256sum $REPO/.ufo/gates/c1-census-v10.py | cut -d' ' -f1)"
printf '%s\n' "fixtures: $(sha256sum $SCRATCH/census-*.py | awk '{printf "%s=%s ", $2, substr($1,1,8)}')"
echo
run head-v10 "$REPO/.ufo/gates/c1-census-v10.py" "$REPO"
run atk-nullskill-v10 "$SCRATCH/census.py" "$SCRATCH/atk-nullskill"
run atk-missing-v10 "$SCRATCH/census.py" "$SCRATCH/atk-missing"
run ver-neutered-v10 "$SCRATCH/census-ver-neutered.py" "$REPO"
run head-v11floorA "$SCRATCH/census-v11-floorA.py" "$REPO"
run ver-neutered-v11floorA "$SCRATCH/census-v11-floorA-ver-neutered.py" "$REPO"
run all-neutered-v11floorA "$SCRATCH/census-v11-floorA-all-neutered.py" "$REPO"
run atk-missing-v11floorA "$SCRATCH/census-v11-floorA.py" "$SCRATCH/atk-missing"
