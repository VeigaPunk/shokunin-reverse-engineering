#!/usr/bin/env bash
# R45W2PathspecArm: attack --require-pathspec / covers() on frozen-path-preflight v2.
# Read-only on the lane: the interpreter is a scratch copy of the freeze blob.
S=/fast/scratch/hyaku/kaidoku-r45/R45W2PathspecArm
export TMPDIR="$S"
PF="$S/preflight.py"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
fail=0

newrepo() {
  local D
  D=$(mktemp -d -p "$S" repo.XXXXXX) || return 1
  git -C "$D" init -q
  git -C "$D" config user.email a@b.c
  git -C "$D" config user.name t
  mkdir -p "$D/tools/x/sub" "$D/tools/x/nested/deep" "$D/plans"
  printf 'alpha\n' > "$D/tools/x/a.txt"
  printf 'sub\n'   > "$D/tools/x/sub/s.txt"
  printf 'deep\n'  > "$D/tools/x/nested/deep/d.txt"
  printf 'plan\n'  > "$D/plans/c.md"
  printf 'other\n' > "$D/other.txt"
  git -C "$D" add -A
  git -C "$D" commit -q -m freeze
  local top
  top=$(git -C "$D" rev-parse --show-toplevel)
  if [ "$top" != "$(realpath "$D")" ]; then
    echo "TOPLEVEL_MISMATCH d=$D top=$top" >&2
    fail=1
  fi
  printf '%s\n' "$D"
}

commit() { git -C "$1" add -A && git -C "$1" commit -q -m "$2" && git -C "$1" rev-parse HEAD; }

# run NAME EXPECT ROOT FREEZE REV <extra args...>
run() {
  local name=$1 expect=$2 root=$3 freeze=$4 rev=$5
  shift 5
  local out rc h
  out=$(python3 -I -B "$PF" --root "$root" --freeze "$freeze" --rev "$rev" "$@" 2>&1)
  rc=$?
  h=$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$expect" "$rc" "$h" "$TS" "$out"
}

echo "== dir freeze tools/x, file freeze plans/c.md, extra plans/c.md =="
echo "== schema: name | expect | exit | stdout_sha256 | utc | stdout =="

# A: directory freeze, no pathspec, --require-pathspec
D=$(newrepo); F=$(git -C "$D" rev-parse HEAD)
run A-dir-no-pathspec 2 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec

# B: directory freeze with trailing-slash pathspec
run B-dir-pathspec-slash 0 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec --pathspec tools/x/

# C: directory freeze, pathspec without trailing slash
run C-dir-pathspec-noslash 0 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec --pathspec tools/x

# D: parent pathspec (covers the dir in git's own semantics)
run D-dir-pathspec-parent 0 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec --pathspec tools/

# D2: repo-root pathspec (covers everything)
run D2-dir-pathspec-dot 0 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec --pathspec .

# E: FILE freeze, no pathspec
run E-file-no-pathspec 0 "$D" "$F" "$F" --freeze-path plans/c.md --require-pathspec

# E2: FILE freeze, an actual touch must still be red
printf 'plan2\n' > "$D/plans/c.md"; R=$(commit "$D" "touch file")
run E2-file-touched 1 "$D" "$F" "$R" --freeze-path plans/c.md --require-pathspec

# F: dir freeze, correct pathspec, real touch inside
D2=$(newrepo); F2=$(git -C "$D2" rev-parse HEAD)
printf 'beta\n' > "$D2/tools/x/a.txt"; R2=$(commit "$D2" "touch a")
run F-dir-touched-in-scope 1 "$D2" "$F2" "$R2" --freeze-path tools/x --require-pathspec --pathspec tools/x/

# G: descendant pathspec, touch outside the pathspec but inside the frozen dir
D3=$(newrepo); F3=$(git -C "$D3" rev-parse HEAD)
printf 'beta\n' > "$D3/tools/x/a.txt"; R3=$(commit "$D3" "touch a")
run G-descendant-pathspec-touch-outside 1 "$D3" "$F3" "$R3" --freeze-path tools/x --require-pathspec --pathspec tools/x/sub/

# H: descendant pathspec, touch-then-restore outside the pathspec but inside the frozen dir
D4=$(newrepo); F4=$(git -C "$D4" rev-parse HEAD)
printf 'beta\n' > "$D4/tools/x/a.txt"; commit "$D4" "tamper a" >/dev/null
printf 'alpha\n' > "$D4/tools/x/a.txt"; R4=$(commit "$D4" "restore a")
run H-descendant-pathspec-restore-outside 1 "$D4" "$F4" "$R4" --freeze-path tools/x --require-pathspec --pathspec tools/x/sub/

# I: descendant pathspec, touch-then-restore INSIDE the pathspec (restore arm control)
D5=$(newrepo); F5=$(git -C "$D5" rev-parse HEAD)
printf 'tampered\n' > "$D5/tools/x/sub/s.txt"; commit "$D5" "tamper s" >/dev/null
printf 'sub\n' > "$D5/tools/x/sub/s.txt"; R5=$(commit "$D5" "restore s")
run I-descendant-pathspec-restore-inside 1 "$D5" "$F5" "$R5" --freeze-path tools/x --require-pathspec --pathspec tools/x/sub/

# J: exact pathspec, touch-then-restore (restore arm, correct scope)
D6=$(newrepo); F6=$(git -C "$D6" rev-parse HEAD)
printf 'beta\n' > "$D6/tools/x/a.txt"; commit "$D6" "tamper a" >/dev/null
printf 'alpha\n' > "$D6/tools/x/a.txt"; R6=$(commit "$D6" "restore a")
run J-exact-pathspec-restore 1 "$D6" "$F6" "$R6" --freeze-path tools/x --require-pathspec --pathspec tools/x/

# K: two frozen paths (dir + file), pathspec only names the dir; file touched then restored
D7=$(newrepo); F7=$(git -C "$D7" rev-parse HEAD)
printf 'plan2\n' > "$D7/plans/c.md"; commit "$D7" "tamper c" >/dev/null
printf 'plan\n'  > "$D7/plans/c.md"; R7=$(commit "$D7" "restore c")
run K-file-freeze-outside-pathspec 1 "$D7" "$F7" "$R7" --freeze-path tools/x --freeze-path plans/c.md --require-pathspec --pathspec tools/x/

# K2: same two frozen paths, no pathspec (whole-tree scan) - file restore must be seen
D8=$(newrepo); F8=$(git -C "$D8" rev-parse HEAD)
printf 'plan2\n' > "$D8/plans/c.md"; commit "$D8" "tamper c" >/dev/null
printf 'plan\n'  > "$D8/plans/c.md"; R8=$(commit "$D8" "restore c")
run K2-file-freeze-no-pathspec 2 "$D8" "$F8" "$R8" --freeze-path tools/x --freeze-path plans/c.md --require-pathspec

# L: glob pathspec accepted by covers(), misses the nested file in the log scope
D9=$(newrepo); F9=$(git -C "$D9" rev-parse HEAD)
printf 'tampered\n' > "$D9/tools/x/nested/deep/d.txt"; commit "$D9" "tamper d" >/dev/null
printf 'deep\n' > "$D9/tools/x/nested/deep/d.txt"; R9=$(commit "$D9" "restore d")
run L-glob-pathspec-restore-nested 1 "$D9" "$F9" "$R9" --freeze-path tools/x --require-pathspec --pathspec 'tools/x/*'

# M: freeze path that is absent at FREEZE, no pathspec (does the rule fire?)
D10=$(newrepo); F10=$(git -C "$D10" rev-parse HEAD)
run M-absent-freeze-path 2 "$D10" "$F10" "$F10" --freeze-path tools/nosuch --require-pathspec

# N: dir freeze, correct pathspec, unrelated path touched (must be green)
D11=$(newrepo); F11=$(git -C "$D11" rev-parse HEAD)
printf 'other2\n' > "$D11/other.txt"; R11=$(commit "$D11" "unrelated")
run N-dir-pathspec-unrelated 0 "$D11" "$F11" "$R11" --freeze-path tools/x --require-pathspec --pathspec tools/x/

echo "TOLEVEL_FAIL=$fail"
