#!/bin/bash
# Build the separability state set inside a scratch clone. Mutates $R only.
# usage: build.sh <clone> <index-file>
set -eu
R=${1:?clone}; IDX=${2:?index file}
S=/fast/scratch/hyaku/kaidoku-r47/ConnSeparability
BASE=13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5
TOP=$(git -C "$R" rev-parse HEAD)
case "$(git -C "$R" log -1 --format=%s)" in state*) echo "REFUSING: clone HEAD is a fixture state"; exit 9;; esac
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo TOPLEVEL_MISMATCH; exit 9; }
git -C "$R" config user.email sep@r47
git -C "$R" config user.name "r47 separability fixture"
: > "$IDX"
echo "S00_both $TOP" >> "$IDX"

snap() { # name
  git -C "$R" add -A SKILL.md SCORECARD.md
  git -C "$R" commit -q -m "state $1"
  echo "$1 $(git -C "$R" rev-parse HEAD)" >> "$IDX"
}
restore() { git -C "$R" checkout -q "$TOP" -- SKILL.md SCORECARD.md tools/round-47; }

# C1 surface out: craft block 24 removed (SKILL.md at the round's base)
git -C "$R" checkout -q "$BASE" -- SKILL.md
snap S10_c1out
restore

# C2 surface out, minimal: only the corrections section removed
python3 - "$R/SCORECARD.md" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read(); h="## Record corrections \u2014 round 47"
i=t.index(h); j=t.find("\n## ", i+len(h)); assert j>i
open(p,"w").write(t[:i]+t[j+1:])
PY
snap S01_c2out_min
restore

# both out, minimal
git -C "$R" checkout -q "$BASE" -- SKILL.md
python3 - "$R/SCORECARD.md" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read(); h="## Record corrections \u2014 round 47"
i=t.index(h); j=t.find("\n## ", i+len(h)); assert j>i
open(p,"w").write(t[:i]+t[j+1:])
PY
snap S11_both_min
restore

# C2 surface out, full: SCORECARD.md at the round's base
git -C "$R" checkout -q "$BASE" -- SCORECARD.md
snap S01_c2out_full
restore

# both out, full
git -C "$R" checkout -q "$BASE" -- SKILL.md SCORECARD.md
snap S11_both_full
restore

# C1 artefact edited inside its own surface but not its count: one citation range out of bounds
python3 - "$R/SKILL.md" <<'PY'
import sys, re
p=sys.argv[1]; t=open(p).read()
m=re.search(r"(corpus/lessons/round-46\.md):(\d+)-(\d+)", t)
assert m, "no round-46 citation"
t=t[:m.start()]+m.group(1)+":900-960"+t[m.end():]
open(p,"w").write(t)
PY
snap S20_c1refout
restore

# C1 out + an axes correction that would repair the depth atom if the parser read it
git -C "$R" checkout -q "$BASE" -- SKILL.md
python3 - "$R/SCORECARD.md" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read(); h="## Record corrections \u2014 round 47"
assert h in t
i=t.index(h)+len(h)
t=t[:i]+"\n\n- corrects axes depth: 23/23 \u2014 the head the C1-out state actually derives"+t[i:]
open(p,"w").write(t)
PY
snap S12_axes_corr
restore

# the interpreter file deleted: C2's depth atom resolves block 24's self-citation
git -C "$R" rm -q tools/round-47/exact.py
git -C "$R" commit -q -m "state S30_noexact"
echo "S30_noexact $(git -C "$R" rev-parse HEAD)" >> "$IDX"
restore

# SCORECARD.md deleted: is C1 dependent on C2's artefact at all
git -C "$R" rm -qf SCORECARD.md
git -C "$R" commit -q -m "state S02_nocard"
echo "S02_nocard $(git -C "$R" rev-parse HEAD)" >> "$IDX"
restore
git -C "$R" status --porcelain | head -3
echo "TOP $TOP"
cat "$IDX"
