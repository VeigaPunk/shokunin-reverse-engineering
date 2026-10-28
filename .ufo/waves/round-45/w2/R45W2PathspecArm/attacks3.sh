#!/usr/bin/env bash
# Third pass: row-5 clause "a whole-tree scan is refused"; real-name narrow pathspec on the lane.
S=/fast/scratch/hyaku/kaidoku-r45/R45W2PathspecArm
export TMPDIR="$S"
PF="$S/preflight.py"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
FROZEN=f762b7273e3f6ca3c710bb37d5de92a4a4417aec

newrepo() {
  local D; D=$(mktemp -d -p "$S" repo.XXXXXX)
  git -C "$D" init -q; git -C "$D" config user.email a@b.c; git -C "$D" config user.name t
  mkdir -p "$D/tools/x/sub" "$D/plans"
  printf 'alpha\n' > "$D/tools/x/a.txt"; printf 'sub\n' > "$D/tools/x/sub/s.txt"; printf 'plan\n' > "$D/plans/c.md"
  git -C "$D" add -A; git -C "$D" commit -q -m freeze
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$(realpath "$D")" ] || echo "TOPLEVEL_MISMATCH $D" >&2
  printf '%s\n' "$D"
}
run() {
  local name=$1 expect=$2 root=$3 freeze=$4 rev=$5; shift 5
  local out rc
  out=$(python3 -I -B "$PF" --root "$root" --freeze "$freeze" --rev "$rev" "$@" 2>&1); rc=$?
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$expect" "$rc" "$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)" "$TS" "$out"
}

# S2: clean repo, dir freeze, whole-tree pathspec plus the covered dir -> accepted whole-tree scan?
D=$(newrepo); F=$(git -C "$D" rev-parse HEAD)
run S2-whole-tree-plus-dir-clean 0 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec --pathspec . --pathspec tools/x/
# S3: whole-tree pathspec alone -> refused (the only case row 5's clause is true for)
run S3-whole-tree-alone 2 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec --pathspec .
# S4: dir freeze, one instrument file inside the dir as the accepted pathspec
run S4-single-file-inside-dir 0 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec --pathspec tools/x/a.txt

# W: live lane, read-only. A single instrument file satisfies the requirement on real bytes.
H=$(git -C "$L" rev-parse HEAD)
run W1-live-single-file-pathspec 0 "$L" "$FROZEN" "$H" --freeze-path tools/round-45 --require-pathspec --pathspec tools/round-45/c1-counter.py
run W2-live-single-file-plus-file-freeze 0 "$L" "$FROZEN" "$H" --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --require-pathspec --pathspec tools/round-45/c1-counter.py
run W3-live-both-exact 0 "$L" "$FROZEN" "$H" --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --require-pathspec --pathspec tools/round-45/ --pathspec plans/round-45-claims.md
