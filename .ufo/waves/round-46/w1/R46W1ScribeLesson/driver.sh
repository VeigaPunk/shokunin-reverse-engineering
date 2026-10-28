#!/bin/sh
# R46W1ScribeLesson measurement driver. Read-only on the lane tree:
# every write target is under $S.
set -u
S=/fast/scratch/hyaku/kaidoku-r46/R46W1ScribeLesson
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
T=$L/tools/round-46
EXPR_FREEZE=31820472784284727546808acc31b3ea1e73919b
MEAS_FREEZE=65678df0f1666e83cdeea7233bfb31ffe73ec709
A3=7bf33e312d75ad09d55df399814e9ae3ef7cee49
REGREV=781e19ae674225b6be0b5de56ee8574679bac0b6
mkdir -p "$S"
cd "$S" || exit 1
export TMPDIR="$S" HYAKU_SCRATCH="$S"
: > "$S/receipts.tsv"

run() {
  name=$1; shift
  utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  "$@" >"$S/$name.out" 2>"$S/$name.err"
  code=$?
  sha=$(sha256sum "$S/$name.out" | cut -d' ' -f1)
  printf '%s\texit=%s\tsha256=%s\tutc=%s\tcmd=%s\n' "$name" "$code" "$sha" "$utc" "$*" >> "$S/receipts.tsv"
  echo "== $name exit=$code sha256=$sha"
}

# R1: the dispatch-named freeze (3182047) scored at the tip.
run R1-attest-v2-dispatch-freeze \
  python3 -I -B "$T/attest.py" --root "$L" --freeze $EXPR_FREEZE --rev $REGREV \
  --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R1-attest-v2-dispatch-freeze.json"

# R2: the lane's measured freeze (65678df0) at A3, full battery.
run R2-attest-v2-measured-freeze \
  python3 -I -B "$T/attest.py" --root "$L" --freeze $MEAS_FREEZE --rev $A3 \
  --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R2-attest-v2-measured-freeze.json"

# R3: the value ctl-c1-1-v1-profile.json claims, requested at the freeze itself.
run R3-attest-v1-at-freeze \
  python3 -I -B "$T/attest.py" --root "$L" --freeze $MEAS_FREEZE --rev $MEAS_FREEZE \
  --profile v1 --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R3-attest-v1-at-freeze.json"

# R4: the same v1 profile post-landing (structural only).
run R4-attest-v1-post-landing \
  python3 -I -B "$T/attest.py" --root "$L" --freeze $MEAS_FREEZE --rev $A3 \
  --profile v1 --no-battery --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R4-attest-v1-post-landing.json"

# R5: C2 measured exactly as the claims' counting command says.
run R5-registry-v2 \
  python3 -I -B "$T/registry.py" --root "$L" --freeze $MEAS_FREEZE --rev $REGREV \
  --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R5-registry-v2.json"

# R6: C2 v1 profile at the freeze (the ctl-c2-1-v1-profile value).
run R6-registry-v1-at-freeze \
  python3 -I -B "$T/registry.py" --root "$L" --freeze $MEAS_FREEZE --rev $MEAS_FREEZE \
  --profile v1 --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R6-registry-v1-at-freeze.json"

# R7: C2 v2 at the freeze (the do-nothing control).
run R7-registry-v2-at-freeze \
  python3 -I -B "$T/registry.py" --root "$L" --freeze $MEAS_FREEZE --rev $MEAS_FREEZE \
  --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R7-registry-v2-at-freeze.json"

# R8: C2 v1 *structural* profile on the landed section (no battery).
run R8-registry-v1-structural \
  python3 -I -B "$T/registry.py" --root "$L" --freeze $MEAS_FREEZE --rev $REGREV \
  --profile v1 --no-battery --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R8-registry-v1-structural.json"

# R9: C1 v2 at the freeze (do-nothing control shape at the measured freeze).
run R9-attest-v2-at-freeze \
  python3 -I -B "$T/attest.py" --root "$L" --freeze $MEAS_FREEZE --rev $MEAS_FREEZE \
  --json-out "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1ScribeLesson/R9-attest-v2-at-freeze.json"

echo "== receipts =="
cat "$S/receipts.tsv"
