#!/bin/bash
# Build a fixture from the bytes published in rows.md, run the real counter on it.
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1Tokens
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
F=5017e1f7299c3a812e87e7950148f54313dd279e
export HYAKU_SCRATCH="$S" TMPDIR="$S"
D=$(mktemp -d -p "$S" fx-rows-XXXXXX) || exit 9
git -C "$D" init -q || exit 9
TOP=$(git -C "$D" rev-parse --show-toplevel)
[ "$TOP" = "$D" ] || { echo "TOPLEVEL MISMATCH: $TOP != $D"; exit 9; }
python3 -I -B - "$D" <<'PY' || exit 9
import subprocess, sys
D = sys.argv[1]
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
F = "5017e1f7299c3a812e87e7950148f54313dd279e"
rows = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-47/w1/C1Tokens/rows.md"
t = open(rows).read()
blk = t.split("```markdown\n", 1)[1].split("\n```", 1)[0] + "\n"
skill = subprocess.run(["git", "-C", L, "show", f"{F}:SKILL.md"],
                       capture_output=True, text=True, check=True).stdout
sep = "\n## Config custody for live-probe rounds (SOP)"
assert skill.count(sep) == 1
open(D + "/SKILL.md", "w").write(skill.replace(sep, blk + sep, 1))
for p in ("plans/round-47-claims.md", "tools/round-47/exact.py", "tools/round-46/gate.py",
          "corpus/lessons/round-46.md", "corpus/lessons/round-45.md"):
    body = subprocess.run(["git", "-C", L, "show", f"{F}:{p}"],
                          capture_output=True, text=True, check=True).stdout
    import os
    os.makedirs(os.path.dirname(D + "/" + p), exist_ok=True)
    open(D + "/" + p, "w").write(body)
PY
git -C "$D" add -A || exit 9
git -C "$D" -c user.name=fixture -c user.email=fixture@round47 commit -q -m "block 24 from rows.md" || exit 9
REV=$(git -C "$D" rev-parse HEAD)
TOP2=$(git -C "$D" rev-parse --show-toplevel)
[ "$TOP2" = "$D" ] || { echo "TOPLEVEL MISMATCH after commit"; exit 9; }
printf '%s\n%s\n' "$D" "$REV" > "$S/fx-rows.txt"
python3 -I -B "$L/tools/round-47/exact.py" --root "$D" --freeze "$REV" --rev "$REV" \
  --json-out "$D/receipt.json" > "$S/cli-rows.stdout" 2>&1
C=$?
printf 'fixture=%s rev=%s exit=%s utc=%s stdout_sha256=%s\n' \
  "$D" "$REV" "$C" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(sha256sum "$S/cli-rows.stdout" | cut -d' ' -f1)"
cp "$D/receipt.json" "$S/receipt-cli-rows.json"
python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
print("failing:", json.dumps(d["failing"]))
print("met_target:", d["met_target"], "rows:", d["rows"], "refs:", d["refs"], "arms:", d["arm_tokens"])
print("battery:", json.dumps({k: d["battery"].get(k) for k in ("forgeries_total","v2_green","v3_green","genuine_green","crash")}))
' "$S/receipt-cli-rows.json"
