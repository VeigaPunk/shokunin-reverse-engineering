#!/usr/bin/env bash
# Round-3 fixtures: rename construction, merge pruning, symlink retarget, subdir root.
set -u
S=/fast/scratch/hyaku/kaidoku-r38/R38W2FreezeDriftFixtures
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/freeze-drift.py
export TMPDIR="$S"
mkrepo() {
  local D; D=$(mktemp -d "$S/fx3.$1.XXXX"); git -C "$D" init -q
  local top; top=$(git -C "$D" rev-parse --show-toplevel)
  [ "$(realpath "$top")" = "$(realpath "$D")" ] || { echo "FATAL toplevel $top != $D" >&2; exit 9; }
  git -C "$D" config user.email fx@example.invalid; git -C "$D" config user.name fx
  git -C "$D" config commit.gpgsign false
  mkdir -p "$D"/{plans,tools/round-38,.ufo/waves/round-38/c1,corpus/evidence/round-37/c1/K1}
  printf 'claims v1\n' > "$D/plans/round-38-claims.md"
  printf '# c1 counter\nprint(1)\n' > "$D/tools/round-38/c1-counter.py"
  printf '# c2 counter\nprint(2)\n' > "$D/tools/round-38/c2-counter.py"
  printf '{"carriers":[]}\n' > "$D/.ufo/waves/round-38/c1/carriers.json"
  printf 'id\tval\nK1\t1\n' > "$D/corpus/evidence/round-37/c1/K1/oracle.tsv"
  echo "$D"
}
run() { local D="$1" L="$2"; shift 2; local out; out=$(python3 "$TOOL" --root "$D" "$@" 2>&1); local rc=$?
  printf '\n### %s\n$ python3 freeze-drift.py --root %s %s\nEXIT %d\n%s\n' "$L" "$D" "$*" "$rc" "$out"; }
log() { printf '\n===== %s =====\n' "$*"; }

# ---- (d3a) rename into frozen name absent at freeze ----
log "(d3a) rename INTO frozen path, destination absent at freeze"
D=$(mkrepo d3a)
rm -f "$D/tools/round-38/c2-counter.py"
printf 'other body\nprint(3)\n' > "$D/tools/round-38/other.py"
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
git -C "$D" mv tools/round-38/other.py tools/round-38/c2-counter.py
git -C "$D" commit -qm "rename other.py onto c2-counter path"
R=$(git -C "$D" rev-parse HEAD)
echo "  commit changed: $(git -C "$D" show --stat --oneline "$R" | tr '\n' '|')"
run "$D" "(d3a) rename into frozen path: $F..$R" --freeze "$F" --rev "$R"

# ---- (e-rev3) side amendment pruned by evil merge revert on mainline ----
log "(e-rev3) side amendment + evil merge restoring freeze bytes (TREESAME to main)"
D=$(mkrepo erev3)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q -b side
printf 'claims AMENDED\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -qm "side amends claims"
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main
printf 'main doc\n' > "$D/plans/main.md"
git -C "$D" add -A && git -C "$D" commit -qm "main adds doc"
git -C "$D" merge -q --no-ff side -m "merge side" >/dev/null 2>&1
printf 'claims v1\n' > "$D/plans/round-38-claims.md"   # evil: restore freeze bytes
git -C "$D" add -A && git -C "$D" commit -q --amend --no-edit
M=$(git -C "$D" rev-parse HEAD)
echo "  parents: $(git -C "$D" rev-list --parents -n1 "$M" | cut -d' ' -f2-)"
echo "  claims at freeze: [$(git -C "$D" show "$F":plans/round-38-claims.md | tr -d '\n')]"
echo "  claims at merge : [$(git -C "$D" show "$M":plans/round-38-claims.md | tr -d '\n')]"
run "$D" "(e-rev3) merge reverts side amendment: $F..$M" --freeze "$F" --rev "$M"
echo "  raw: git log --name-only $F..$M -- claims"
git -C "$D" log --format='  %h %s' --name-only "$F..$M" -- plans/round-38-claims.md
echo "  raw: git log -m --name-only $F..$M -- claims"
git -C "$D" log --format='  %h %s' --name-only -m "$F..$M" -- plans/round-38-claims.md
echo "  raw: git log --name-status -m $F..$M -- claims"
git -C "$D" log --format='  %h %s' --name-status -m "$F..$M" -- plans/round-38-claims.md

# ---- (e-m2) explain empty paths on a merge (tool command reproduction) ----
log "(e-m2) tool's exact log command on a merge with a merge-only change"
D=$(mkrepo em2)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q -b side
printf 'side doc\n' > "$D/plans/side.md"; git -C "$D" add -A && git -C "$D" commit -qm "side adds doc"
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main
printf 'main doc\n' > "$D/plans/main.md"; git -C "$D" add -A && git -C "$D" commit -qm "main adds doc"
git -C "$D" merge -q --no-ff side -m "merge side" >/dev/null 2>&1
printf 'claims changed only in merge\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -q --amend --no-edit
M=$(git -C "$D" rev-parse HEAD)
run "$D" "(e-m2) merge-only claims change: $F..$M" --freeze "$F" --rev "$M"
echo "  tool's exact git call:"
git -C "$D" log --format='%H%x09%cI%x09%s' --name-only --no-renames "$F..$M" -- ':(glob)plans/round-38-claims.md' | sed 's/^/  |/'
echo "  byte check at rev vs freeze: [$(git -C "$D" show "$M":plans/round-38-claims.md | tr -d '\n')] vs [$(git -C "$D" show "$F":plans/round-38-claims.md | tr -d '\n')]"

# ---- (s1) symlink retarget ----
log "(s1) frozen path is a symlink; target retargeted"
D=$(mkrepo s1)
git -C "$D" rm -q tools/round-38/c2-counter.py 2>/dev/null || true
printf 'real counter A\n' > "$D/tools/real-a.py"; printf 'real counter B\n' > "$D/tools/real-b.py"
ln -s ../tools/real-a.py "$D/tools/round-38/c2-counter.py"
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
rm -f "$D/tools/round-38/c2-counter.py"; ln -s ../tools/real-b.py "$D/tools/round-38/c2-counter.py"
git -C "$D" add -A && git -C "$D" commit -qm "retarget counter symlink"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(s1a) symlink retargeted (link bytes change): $F..$R" --freeze "$F" --rev "$R"
printf 'real counter A MUTATED\n' > "$D/tools/real-a.py"
git -C "$D" add -A && git -C "$D" commit -qm "mutate symlink target only"
R2=$(git -C "$D" rev-parse HEAD)
run "$D" "(s1b) symlink target mutated, link unchanged: $F..$R2" --freeze "$F" --rev "$R2"

# ---- (r1) --root pointed at a subdirectory ----
log "(r1) --root at a subdirectory of the repo"
D=$(mkrepo r1)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
printf '# c1 edited\n' > "$D/tools/round-38/c1-counter.py"
git -C "$D" add -A && git -C "$D" commit -qm "edit c1"
R=$(git -C "$D" rev-parse HEAD)
run "$D/tools" "(r1a) --root is the 'tools' subdir, default set: $F..$R" --freeze "$F" --rev "$R"
run "$D/tools" "(r1b) --root subdir, path given repo-relative" --freeze "$F" --rev "$R" 'round-38/c1-counter.py'
echo DONE3
