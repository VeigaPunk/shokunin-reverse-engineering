#!/bin/bash
# One mutation per commit in the fixture clone; each mutation is scored twice:
# clause-level (--no-battery) and full (battery on).
set -u
S=/fast/scratch/hyaku/kaidoku-r47/MutCorrections
C="$S/clone"
BASE=f7d6e58d6e7f4e664bf443137c55ee08821de244
export TMPDIR="$S" HYAKU_SCRATCH="$S"
TSV="$S/out/matrix.tsv"
: > "$TSV"

top=$(git -C "$C" rev-parse --show-toplevel)
if [ "$top" != "$C" ]; then echo "FATAL toplevel $top != $C"; exit 9; fi

MUTS="wrong-round-in-window wrong-round-historical-true cross-round-total
ghost-path-exemption ghost-path-non-atom ghost-path-window-pathspec window-pair-out-of-scope
window-pair-real-other-commits window-pair-atom-range duplicate-correction
duplicate-replaces-repair false-axes-correction false-axes-bogus-axis
axes-corrections-deleted"

score () {  # $1 name  $2 rev  $3 mode(no-battery|battery)
  name="$1"; rev="$2"; mode="$3"
  extra=""; [ "$mode" = "no-battery" ] && extra="--no-battery"
  utc=$(date -u +%FT%TZ)
  ( cd "$C" && python3 -I -B tools/round-47/record.py --root "$C" --rev "$rev" $extra \
      --json-out "receipts/$name.$mode.json" ) > "$S/out/$name.$mode.stdout" 2>&1
  code=$?
  sha=$(sha256sum "$S/out/$name.$mode.stdout" | cut -d' ' -f1)
  detail=$(python3 -c "
import json
d=json.load(open('$C/receipts/$name.$mode.json'))
b=d.get('battery') or {}
print(json.dumps({'failing':d.get('failing'),'mismatches':len(d.get('mismatches') or []),
 'exempted':len(d.get('exempted') or []),'corrections':d.get('corrections'),
 'corrections_bad':len(d.get('corrections_bad') or []),
 'forgeries_green':b.get('forgeries_green')}))" 2>/dev/null)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$rev" "$mode" "$code" "$sha" "$utc" \
    "$detail" >> "$TSV"
  echo "== $name [$mode] exit=$code $detail"
}

for m in $MUTS; do
  git -C "$C" checkout -q "$BASE" -- SCORECARD.md || { echo "$m checkout failed"; exit 8; }
  python3 "$S/mutate.py" "$m" "$C/SCORECARD.md" || { echo "$m mutate failed"; continue; }
  git -C "$C" add SCORECARD.md
  git -C "$C" commit -q -m "mut: $m"
  rev=$(git -C "$C" rev-parse HEAD)
  score "$m" "$rev" no-battery
  score "$m" "$rev" battery
done

git -C "$C" checkout -q "$BASE" -- SCORECARD.md
git -C "$C" reset -q --hard "$BASE"
echo "--- restored HEAD $(git -C "$C" rev-parse HEAD)"
echo "--- card sha $(git -C "$C" show HEAD:SCORECARD.md | sha256sum | cut -d' ' -f1)"
echo "--- worktree clean: [$(git -C "$C" status --porcelain | head -5)]"
