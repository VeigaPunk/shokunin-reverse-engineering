#!/usr/bin/env bash
# Round-2 fixtures: ambiguity probes (seat R38W2FreezeDriftFixtures).
set -u
S=/fast/scratch/hyaku/kaidoku-r38/R38W2FreezeDriftFixtures
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/freeze-drift.py
export TMPDIR="$S"

mkrepo() {
  local D; D=$(mktemp -d "$S/fx2.$1.XXXX")
  git -C "$D" init -q
  local top; top=$(git -C "$D" rev-parse --show-toplevel)
  if [ "$(realpath "$top")" != "$(realpath "$D")" ]; then echo "FATAL: toplevel $top != $D" >&2; exit 9; fi
  git -C "$D" config user.email fx@example.invalid
  git -C "$D" config user.name fx
  git -C "$D" config commit.gpgsign false
  mkdir -p "$D"/{plans,tools/round-38,.ufo/waves/round-38/c1,corpus/evidence/round-37/c1/K1}
  printf 'claims v1\n' > "$D/plans/round-38-claims.md"
  printf '# c1 counter\nprint(1)\n' > "$D/tools/round-38/c1-counter.py"
  printf '# c2 counter\nprint(2)\n' > "$D/tools/round-38/c2-counter.py"
  printf '{"carriers":[]}\n' > "$D/.ufo/waves/round-38/c1/carriers.json"
  printf 'id\tval\nK1\t1\n' > "$D/corpus/evidence/round-37/c1/K1/oracle.tsv"
  echo "$D"
}
run() {
  local D="$1" L="$2"; shift 2
  local out; out=$(python3 "$TOOL" --root "$D" "$@" 2>&1); local rc=$?
  printf '\n### %s\n$ python3 freeze-drift.py --root %s %s\nEXIT %d\n%s\n' "$L" "$D" "$*" "$rc" "$out"
}

log() { printf '\n===== %s =====\n' "$*"; }

# ---- (c-deep) oracle below a deeper directory, clean range ----
log "(c-deep) deeper oracle path, clean range"
D=$(mkrepo cdeep)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
mkdir -p "$D/corpus/evidence/round-37/c1/K2/deep"
printf 'id\nK2d\n' > "$D/corpus/evidence/round-37/c1/K2/deep/oracle.tsv"
git -C "$D" add -A && git -C "$D" commit -qm "add oracle two levels down"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(c-deep1) default set, only deeper oracle added: $F..$R" --freeze "$F" --rev "$R"
run "$D" "(c-deep2) same, explicit K*/oracle.tsv glob" --freeze "$F" --rev "$R" 'corpus/evidence/round-37/c1/K*/oracle.tsv'
git -C "$D" show --stat --oneline "$R" | sed 's/^/  /'

# ---- (d3) rename INTO a frozen path name that did not exist at freeze ----
log "(d3) rename into frozen path (destination absent at freeze)"
D=$(mkrepo d3)
git -C "$D" rm -q tools/round-38/c2-counter.py
printf 'other body\nprint(3)\n' > "$D/tools/round-38/other.py"
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
git -C "$D" mv tools/round-38/other.py tools/round-38/c2-counter.py
git -C "$D" commit -qm "rename other.py onto c2-counter path"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(d3a) rename into frozen path: $F..$R" --freeze "$F" --rev "$R"
# destination existed at freeze, forced overwrite rename
D=$(mkrepo d3b)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
printf 'other body\n' > "$D/tools/round-38/other.py"
git -C "$D" add -A && git -C "$D" commit -qm "add other"
git -C "$D" mv -f tools/round-38/other.py tools/round-38/c2-counter.py
git -C "$D" commit -qm "rename other over c2-counter"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(d3b) rename over existing frozen path: $F..$R" --freeze "$F" --rev "$R"

# ---- (e-revert) linear edit then revert; evil-merge revert ----
log "(e-revert) edit then revert"
D=$(mkrepo erev)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
printf 'claims v2 (amended)\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -qm "amend claims"
printf 'claims v1\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -qm "revert claims"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(e-rev1) linear edit+revert, rev bytes == freeze bytes: $F..$R" --freeze "$F" --rev "$R"
echo "  bytes identical: $( [ "$(git -C "$D" show "$F:plans/round-38-claims.md")" = "$(git -C "$D" show "$R:plans/round-38-claims.md")" ] && echo yes || echo no )"

log "(e-revert2) evil merge reverts the claims edit"
D=$(mkrepo erev2)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
printf 'claims amended\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -qm "amend claims"
git -C "$D" checkout -q -b side
printf 'side doc\n' > "$D/plans/side.md"
git -C "$D" add -A && git -C "$D" commit -qm "side adds doc"
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main
git -C "$D" merge -q --no-ff side -m "merge side" >/dev/null 2>&1
# evil merge: silently restore the freeze claims bytes inside the merge commit
printf 'claims v1\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -q --amend --no-edit
M=$(git -C "$D" rev-parse HEAD)
echo "  MERGE_PARENTS=$(git -C "$D" rev-list --parents -n1 "$M")"
run "$D" "(e-rev2) evil merge reverts claims, rev bytes == freeze: $F..$M" --freeze "$F" --rev "$M"
echo "  bytes identical at rev: $( [ "$(git -C "$D" show "$F:plans/round-38-claims.md")" = "$(git -C "$M:plans/round-38-claims.md")" ] && echo yes || echo no )"
echo "  raw git log --name-only over claims:"
git -C "$D" log --format='  %h %s' --name-only "$F..$M" -- plans/round-38-claims.md
echo "  raw git log -m --name-only over claims:"
git -C "$D" log --format='  %h %s' --name-only -m "$F..$M" -- plans/round-38-claims.md

# ---- (e-merge) merge where claims change is only reachable through second parent ----
log "(e-merge) merge, claims edit on side only, rev = merge"
D=$(mkrepo emerge)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q -b side
printf 'claims side\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -qm "side amends claims"
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main
printf 'main doc\n' > "$D/plans/main.md"
git -C "$D" add -A && git -C "$D" commit -qm "main adds doc"
git -C "$D" merge -q --no-ff side -m "merge side" >/dev/null 2>&1
M=$(git -C "$D" rev-parse HEAD)
run "$D" "(e-m1) side-only claims edit merged: $F..$M" --freeze "$F" --rev "$M"

# ---- (g4+) metadata-only and type-change drift ----
log "(g4) mode change only / symlink swap"
D=$(mkrepo g4)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
chmod +x "$D/tools/round-38/c1-counter.py"
git -C "$D" add -A && git -C "$D" commit -qm "chmod +x counter"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(g4a) chmod-only change to counter: $F..$R" --freeze "$F" --rev "$R"
git -C "$D" rm -q tools/round-38/c2-counter.py
ln -s /etc/passwd "$D/tools/round-38/c2-counter.py"
git -C "$D" add -A && git -C "$D" commit -qm "replace c2 counter with symlink"
R2=$(git -C "$D" rev-parse HEAD)
run "$D" "(g4b) frozen counter replaced by symlink: $F..$R2" --freeze "$F" --rev "$R2"

# ---- (g8) directory pathspec ----
log "(g8) directory pathspec"
D=$(mkrepo g8)
git -C "$D" add -A && git -C "$D" commit -qm freeze
F=$(git -C "$D" rev-parse HEAD)
printf '# c1 edited\n' > "$D/tools/round-38/c1-counter.py"
git -C "$D" add -A && git -C "$D" commit -qm "edit c1"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(g8) pathspec 'tools/round-38' (a directory)" --freeze "$F" --rev "$R" 'tools/round-38'

# ---- (g9) ref instead of sha, and shallow clone ----
log "(g9) refs and shallow clone"
git -C "$D" tag freezetag "$F"
run "$D" "(g9a) --freeze is a tag name" --freeze freezetag --rev "$R"
SH="$S/shallow.git"
git clone -q --depth 1 "file://$D" "$SH"
if [ "$(realpath "$(git -C "$SH" rev-parse --show-toplevel)")" = "$(realpath "$SH")" ]; then :; fi
echo "  shallow repo commits: $(git -C "$SH" rev-list --count HEAD), has freeze object: $(git -C "$SH" cat-file -e "$F^{commit}" 2>/dev/null && echo yes || echo no)"
run "$SH" "(g9b) shallow clone, freeze object absent" --freeze "$F" --rev "$R"
echo DONE2
