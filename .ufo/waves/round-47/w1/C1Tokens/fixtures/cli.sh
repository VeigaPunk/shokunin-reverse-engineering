#!/bin/bash
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1Tokens
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
export HYAKU_SCRATCH="$S" TMPDIR="$S"
cd "$S" || exit 9
for v in min full allorder; do
  D=$(sed -n 1p "$S/fx-$v.txt")
  REV=$(sed -n 2p "$S/fx-$v.txt")
  python3 -I -B "$L/tools/round-47/exact.py" --root "$D" --freeze "$REV" --rev "$REV" \
      --json-out "$D/receipt.json" > "$S/cli-$v.stdout" 2>&1
  C=$?
  STAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  SH=$(sha256sum "$S/cli-$v.stdout" | cut -d' ' -f1)
  printf '=== %s exit=%s utc=%s stdout_sha256=%s rev=%s\n' "$v" "$C" "$STAMP" "$SH" "$REV"
  cp "$D/receipt.json" "$S/receipt-cli-$v.json"
  python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
print(" failing:", json.dumps(d.get("failing")))
print(" arms:", d.get("arm_tokens"), "refs:", d.get("refs"), "met:", d.get("met_target"))
b=d.get("battery")
if isinstance(b,dict) and "forgeries_total" in b:
    print(" battery:", json.dumps({k:b.get(k) for k in ("forgeries_total","v2_green","v3_green","genuine_green","crash")}))
else:
    print(" battery:", json.dumps(b))
' "$S/receipt-cli-$v.json"
done
echo "--- receipt hashes"
sha256sum "$S"/receipt-cli-*.json
