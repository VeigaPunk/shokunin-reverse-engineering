#!/bin/sh
# Rebuild the round-47 gold-plated forgery from the lane and score it with both frozen counters.
# Usage: sh rebuild.sh            (scratch: /fast/scratch/hyaku/kaidoku-r47/CritGold-rebuild)
set -eu
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=${S:-/fast/scratch/hyaku/kaidoku-r47/CritGold-rebuild}
BASE=1e2c3102952dc636650095643c1963c833859019   # lane HEAD at review time (genuine artifact)
FREEZE=$BASE                                     # exact.py/record.py unchanged at $BASE
mkdir -p "$S"; export TMPDIR="$S" HYAKU_SCRATCH="$S"
D=$(mktemp -d -p "$S" fx-XXXXXX)
git clone -q --no-hardlinks "$LANE" "$D/lane"
D="$D/lane"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$(cd "$D" && pwd -P)" ] || { echo "toplevel mismatch"; exit 2; }
git -C "$D" checkout -q "$BASE"
git -C "$D" config user.email fx@round47
git -C "$D" config user.name "round47 fixture"

python3 - "$D" <<'PY'
import re, sys
d = sys.argv[1]
# 1. block 24: permute the four arm tokens, blank the v2 holes, claim exit 0 on every row.
skill = open(d + "/SKILL.md").read()
for rid, arm in (("R46-CL2", "order"), ("R46-CL3", "digest"),
                 ("R46-CL4", "symbol"), ("R46-CL6", "once")):
    pat = re.compile(r"(?m)^\| " + rid + r" .*\n")
    old = skill
    skill = pat.sub(lambda m: f"| {rid} | n/a | `{arm}` | 0 |\n", skill, count=1)
    assert skill != old, rid
open(d + "/SKILL.md", "w").write(skill)
# 2. record: both round sections -> tautologies (seats read off the dispatch, a self-window,
#    one existing path, one backticked tip); the placeholder window on its own line.
card = open(d + "/SCORECARD.md").read()
heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## Round (\d+)", card)]
pos45, pos46 = heads[-2][0], heads[-1][0]
end46 = card.find("\n## ", pos46 + 1)
g45 = ("## Round 45 — gutted\n\nWaves: 40 + 36 = 76 seats. "
       "`git log 1e2c3102..1e2c3102 -- corpus/knowledge/` is empty. "
       "See `.ufo/waves/round-45/w1-dispatch.json`.\n\n")
g46 = ("## Round 46 — gutted\n\nWaves: 40 + 40 = 80 seats. "
       "`git log 1e2c3102..1e2c3102 -- corpus/knowledge/` is empty. "
       "See `.ufo/waves/round-46/w1-dispatch.json`. Base `1e2c3102`.\n\n"
       "The round-46 sentence above keeps its placeholder: "
       "`git log 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty.\n\n")
card = card[:pos45] + g45 + g46 + card[end46 + 1:]
i = card.index("## Record corrections — round 47")
j = card.find("\n## ", i + 1)
body = ("## Record corrections — round 47\n\n"
        "- corrects seats round-45: 2 waves, 76 seats total\n"
        "- corrects path .ufo/waves/round-45/w1-dispatch.json: present at the measured revision\n"
        "- corrects window round-46: empty in 1e2c3102..1e2c3102 -- corpus/knowledge/\n"
        "- corrects window round-3: empty in 1e2c3102..1e2c3102 -- corpus/knowledge/\n"
        "- corrects axes depth: 24/24\n")
tail = card[j + 1:] if j >= 0 else ""
open(d + "/SCORECARD.md", "w").write(card[:i] + body + ("\n" + tail if tail else ""))
print("patched")
PY

git -C "$D" add SKILL.md SCORECARD.md
git -C "$D" commit -q -m "gold-plated forgery: permuted arms, blanked holes, gutted record, idle corrections"
REV=$(git -C "$D" rev-parse HEAD)
mkdir -p "$D/receipts"
echo "fixture=$D"; echo "rev=$REV"; echo "freeze(C1)=$FREEZE"

python3 -I -B "$LANE/tools/round-47/exact.py" --root "$D" --freeze "$FREEZE" --rev "$REV" \
  --json-out "$D/receipts/c1.json" > "$D/receipts/c1.stdout.json"; C1=$?
python3 -I -B "$LANE/tools/round-47/record.py" --root "$D" --rev "$REV" \
  --json-out "$D/receipts/c2.json" > "$D/receipts/c2.stdout.json"; C2=$?
echo "C1 exit=$C1 stdout_sha256=$(sha256sum "$D/receipts/c1.stdout.json" | cut -d' ' -f1)"
echo "C2 exit=$C2 stdout_sha256=$(sha256sum "$D/receipts/c2.stdout.json" | cut -d' ' -f1)"
echo "invoice: 0/0 means the predicates accept a block whose arms are all wrong and a record emptied to five tautologies"
