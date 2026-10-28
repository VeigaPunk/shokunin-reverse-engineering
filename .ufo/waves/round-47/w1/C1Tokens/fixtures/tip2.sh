#!/bin/bash
# Usage: tip2.sh <REV>   — measure the lane at REV against the prompt's freeze and itself.
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1Tokens
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
REV=${1:?rev required}
FREEZE=5017e1f7299c3a812e87e7950148f54313dd279e
export HYAKU_SCRATCH="$S" TMPDIR="$S"
cd "$L" || exit 9
run() {  # $1 = freeze, $2 = output stem
  python3 -I -B tools/round-47/exact.py --root "$L" --freeze "$1" --rev "$REV" \
    --json-out ".ufo/waves/round-47/w1/C1Tokens/tip-$2.json" > "$S/tip2-$2.stdout" 2>&1
  local c=$?
  printf 'freeze=%s rev=%s exit=%s utc=%s stdout_sha256=%s\n' "$1" "$REV" "$c" \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(sha256sum "$S/tip2-$2.stdout" | cut -d' ' -f1)"
  python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
print(" reason:", d.get("reason"), "| failing:", json.dumps(d.get("failing")))
print(" frozen_path_changed:", d.get("frozen_path_changed"), "| arms:", d.get("arm_tokens"), "| refs:", d.get("refs"))
b=d.get("battery")
if isinstance(b,dict) and "forgeries_total" in b:
    print(" battery:", json.dumps({k:b.get(k) for k in ("forgeries_total","v2_green","v3_green","genuine_green","crash")}))
else:
    print(" battery:", json.dumps(b))
' "$L/.ufo/waves/round-47/w1/C1Tokens/tip-$2.json"
}
run "$FREEZE" "$(echo "$REV" | cut -c1-7)-at-promptfreeze"
run "$REV" "$(echo "$REV" | cut -c1-7)-at-self"
