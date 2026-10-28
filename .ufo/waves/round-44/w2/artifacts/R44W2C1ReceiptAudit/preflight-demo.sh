#!/usr/bin/env bash
# R44W2C1ReceiptAudit — independent red/green proof for tools/round-45/frozen-path-preflight.py
#
# Each case builds its OWN throwaway fixture repo (git init under $TMPDIR, never
# the lane) so no case's history leaks into another's freeze..rev range. Every
# git call names -C "$D" and the toplevel is asserted before the first commit.
#
# Usage: preflight-demo.sh <gate.py> <out-dir> <scratch-dir>
set -u
GATE=${1:?gate path}
OUT=${2:?out dir}
SCRATCH=${3:?scratch dir}
mkdir -p "$OUT" "$SCRATCH"
export TMPDIR=$SCRATCH

newfix() { # newfix <tag> -> prints $D, sets FZ
  D=$(mktemp -d "$SCRATCH/pf.$1.XXXXXX") || exit 1
  git -C "$D" init -q || exit 1
  local top
  top=$(git -C "$D" rev-parse --show-toplevel) || exit 1
  [ "$top" = "$D" ] || { echo "REFUSING: toplevel $top != $D" >&2; exit 1; }
  mkdir -p "$D/tools/round-44" "$D/corpus/evidence/round-44/oracle"
  printf 'claims-v1\n' > "$D/plans.md"
  printf 'v1\n'        > "$D/tools/round-44/tool.py"
  printf 'o1\n'        > "$D/corpus/evidence/round-44/oracle/m.txt"
  git -C "$D" add -A
  git -C "$D" -c user.name=fixture -c user.email=fixture@local commit -qm freeze
  FZ=$(git -C "$D" rev-parse HEAD)
}
commit() { git -C "$D" add -A && git -C "$D" -c user.name=fixture -c user.email=fixture@local commit -qm "$1" && git -C "$D" rev-parse HEAD; }
run() { # run <label> <rev> <expect> <pathspec...>
  local label=$1 rev=$2 expect=$3; shift 3
  local out="$OUT/pf-$label.json"
  python3 -I -B "$GATE" --root "$D" --freeze "$FZ" --rev "$rev" "$@" --json-out "$out" >/dev/null 2>&1
  local rc=$?
  local verdict touched
  verdict=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['verdict'])" "$out")
  touched=$(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))['touched']))" "$out")
  printf '%-34s exit=%s verdict=%-20s touched=%s expect=%s\n' "$label" "$rc" "$verdict" "$touched" "$expect"
  rm -rf -- "$D"
}

newfix freeze;                          run clean-at-freeze              "$FZ" "exit=0 clean"            --pathspec tools/round-44
newfix mod;  printf 'v2\n' > "$D/tools/round-44/tool.py"; M=$(commit mod); run modify-frozen-tool "$M" "exit=1 violation" --pathspec tools/round-44
newfix add;  printf 'new\n' > "$D/tools/round-44/new.py";  A=$(commit add); run add-under-frozen-dir "$A" "exit=1 violation" --pathspec tools/round-44
newfix del;  git -C "$D" rm -q tools/round-44/tool.py;     L=$(commit del); run delete-frozen-tool    "$L" "exit=1 violation" --pathspec tools/round-44
newfix res;  printf 'v2\n' > "$D/tools/round-44/tool.py"; commit mod >/dev/null
             printf 'v1\n' > "$D/tools/round-44/tool.py"; R=$(commit restore)
             run restore-endpoints-equal "$R" "exit=1 violation (log, not endpoints)" --pathspec tools/round-44
newfix pln;  printf 'claims-v2\n' > "$D/plans.md"; P=$(commit plans)
             run claims-only-narrow-pathspec "$P" "exit=0 = FALSE GREEN as recorded" --pathspec tools/round-44
newfix pln2; printf 'claims-v2\n' > "$D/plans.md"; P=$(commit plans)
             run claims-only-right-pathspec  "$P" "exit=1 violation" --pathspec plans.md
newfix orc;  printf 'o2\n' > "$D/corpus/evidence/round-44/oracle/m.txt"; O=$(commit oracle)
             run oracle-only-narrow-pathspec "$O" "exit=0 = FALSE GREEN as recorded" --pathspec tools/round-44
newfix orc2; printf 'o2\n' > "$D/corpus/evidence/round-44/oracle/m.txt"; O=$(commit oracle)
             run oracle-only-right-pathspec  "$O" "exit=1 violation" --pathspec corpus/evidence/round-44/oracle
