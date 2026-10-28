#!/bin/bash
# Mutate the LANDED block 24 (at tip) and score it with the frozen counter.
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1Tokens
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
TIP=1e2c3102952dc636650095643c1963c833859019
export HYAKU_SCRATCH="$S" TMPDIR="$S"
for V in allorder swapped; do
  D=$(mktemp -d -p "$S" "fx-landed-$V-XXXXXX") || exit 9
  git -C "$D" init -q || exit 9
  TOP=$(git -C "$D" rev-parse --show-toplevel)
  [ "$TOP" = "$D" ] || { echo "TOPLEVEL MISMATCH"; exit 9; }
  V="$V" D="$D" python3 -I -B - <<'PY' || exit 9
import os, subprocess
D, V = os.environ["D"], os.environ["V"]
L, TIP = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "1e2c3102952dc636650095643c1963c833859019"
files = {}
for p in ("SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
          "tools/round-46/gate.py", "corpus/lessons/round-46.md",
          "corpus/lessons/round-45.md"):
    files[p] = subprocess.run(["git", "-C", L, "show", f"{TIP}:{p}"],
                              capture_output=True, text=True, check=True).stdout
skill = files["SKILL.md"]
cells = {"symbol": "| `symbol` | 1 |", "once": "| `once` | 1 |",
         "digest": "| `digest` | 1 |", "order": "| `order` | 1 |"}
for tok, pat in cells.items():
    assert skill.count(pat) == 1, (tok, skill.count(pat))
if V == "allorder":
    for tok in ("symbol", "once", "digest"):
        skill = skill.replace(cells[tok], "| `order` | 1 |", 1)
elif V == "swapped":
    skill = skill.replace(cells["symbol"], "| `TMP` | 1 |", 1)
    skill = skill.replace(cells["order"], cells["symbol"], 1)
    skill = skill.replace("| `TMP` | 1 |", cells["order"], 1)
files["SKILL.md"] = skill
for p, t in files.items():
    full = os.path.join(D, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(t)
PY
  git -C "$D" add -A || exit 9
  git -C "$D" -c user.name=fixture -c user.email=fixture@round47 \
      commit -q -m "landed block 24, arms $V" || exit 9
  REV=$(git -C "$D" rev-parse HEAD)
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo MISMATCH2; exit 9; }
  python3 -I -B "$L/tools/round-47/exact.py" --root "$D" --freeze "$REV" --rev "$REV" \
    --json-out "$D/receipt.json" > "$S/cli-landed-$V.stdout" 2>&1
  C=$?
  printf 'landed/%s fixture=%s rev=%s exit=%s utc=%s stdout_sha256=%s\n' "$V" "$D" "$REV" "$C" \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(sha256sum "$S/cli-landed-$V.stdout" | cut -d' ' -f1)"
  cp "$D/receipt.json" "$S/receipt-landed-$V.json"
  python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
print(" failing:", json.dumps(d.get("failing")))
print(" arms:", d.get("arm_tokens"), "routed:", d.get("routed_counts"))
b=d.get("battery")
print(" battery:", json.dumps({k:b.get(k) for k in ("forgeries_total","v2_green","v3_green","genuine_green","crash")}) if isinstance(b,dict) and "forgeries_total" in b else b)
' "$S/receipt-landed-$V.json"
done
