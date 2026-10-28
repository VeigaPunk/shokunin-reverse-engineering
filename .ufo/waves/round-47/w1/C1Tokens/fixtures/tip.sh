#!/bin/bash
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1Tokens
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
TIP=1e2c3102952dc636650095643c1963c833859019
export HYAKU_SCRATCH="$S" TMPDIR="$S"
cd "$L" || exit 9
for F in 5017e1f7299c3a812e87e7950148f54313dd279e 1e2c3102952dc636650095643c1963c833859019; do
  python3 -I -B tools/round-47/exact.py --root "$L" --freeze "$F" --rev "$TIP" \
    --json-out ".ufo/waves/round-47/w1/C1Tokens/tip-freeze-$(echo $F | cut -c1-7).json" > "$S/tip-$F.stdout" 2>&1
  C=$?
  printf 'freeze=%s rev=%s exit=%s utc=%s stdout_sha256=%s\n' "$F" "$TIP" "$C" \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(sha256sum "$S/tip-$F.stdout" | cut -d' ' -f1)"
  python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
print(" reason:", d.get("reason"))
print(" failing:", json.dumps(d.get("failing")))
print(" frozen_path_changed:", d.get("frozen_path_changed"))
print(" arms:", d.get("arm_tokens"), "rows:", d.get("rows"), "refs:", d.get("refs"))
b=d.get("battery")
if isinstance(b,dict) and "forgeries_total" in b:
    print(" battery:", json.dumps({k:b.get(k) for k in ("forgeries_total","v2_green","v3_green","genuine_green","crash")}))
else:
    print(" battery:", json.dumps(b))
' "$L/.ufo/waves/round-47/w1/C1Tokens/tip-freeze-$(echo $F | cut -c1-7).json"
done
