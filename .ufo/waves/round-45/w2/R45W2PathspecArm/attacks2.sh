#!/usr/bin/env bash
# R45W2PathspecArm second pass: predicate direction, fail-closed controls, file-freeze history.
S=/fast/scratch/hyaku/kaidoku-r45/R45W2PathspecArm
export TMPDIR="$S"
PF="$S/preflight.py"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

newrepo() {
  local D
  D=$(mktemp -d -p "$S" repo.XXXXXX) || return 1
  git -C "$D" init -q
  git -C "$D" config user.email a@b.c
  git -C "$D" config user.name t
  mkdir -p "$D/tools/x/sub" "$D/tools/xy" "$D/plans"
  printf 'alpha\n' > "$D/tools/x/a.txt"
  printf 'sub\n'   > "$D/tools/x/sub/s.txt"
  printf 'sib\n'   > "$D/tools/xy/k.txt"
  printf 'plan\n'  > "$D/plans/c.md"
  git -C "$D" add -A
  git -C "$D" commit -q -m freeze
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$(realpath "$D")" ] || echo "TOPLEVEL_MISMATCH $D" >&2
  printf '%s\n' "$D"
}
commit() { git -C "$1" add -A && git -C "$1" commit -q -m "$2" && git -C "$1" rev-parse HEAD; }
run() {
  local name=$1 expect=$2 root=$3 freeze=$4 rev=$5
  shift 5
  local out rc
  out=$(python3 -I -B "$PF" --root "$root" --freeze "$freeze" --rev "$rev" "$@" 2>&1); rc=$?
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$expect" "$rc" "$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)" "$TS" "$out"
}

# O: two frozen dirs, one pathspec -> must fail closed
D=$(newrepo); F=$(git -C "$D" rev-parse HEAD)
run O-two-dirs-one-pathspec 2 "$D" "$F" "$F" --freeze-path tools/x --freeze-path tools/xy --require-pathspec --pathspec tools/x/

# P: sibling with a shared character prefix as pathspec -> must not be accepted
run P-sibling-prefix 2 "$D" "$F" "$F" --freeze-path tools/x --require-pathspec --pathspec tools/xy

# Q: freeze-path spelled with a trailing slash
run Q-freeze-path-trailing-slash 2 "$D" "$F" "$F" --freeze-path tools/x/ --require-pathspec

# Q2: same trailing-slash freeze path, covered pathspec
run Q2-freeze-path-trailing-slash-covered 0 "$D" "$F" "$F" --freeze-path tools/x/ --require-pathspec --pathspec tools/x/

# R: FILE freeze + whole-tree pathspec is accepted (row 5 scopes the rule to directories)
run R-file-freeze-dot-pathspec 0 "$D" "$F" "$F" --freeze-path plans/c.md --require-pathspec --pathspec .

# R2: FILE freeze, no pathspec, restore must be seen by the whole-tree scan
printf 'plan2\n' > "$D/plans/c.md"; commit "$D" "tamper c" >/dev/null
printf 'plan\n'  > "$D/plans/c.md"; R2=$(commit "$D" "restore c")
run R2-file-freeze-restore-whole-tree 1 "$D" "$F" "$R2" --freeze-path plans/c.md --require-pathspec

# S: whole tree plus the covered dir (W1 c7 shape) -> accepted, whole-tree scope
run S-dot-plus-dir 0 "$D" "$F" "$R2" --freeze-path tools/x --require-pathspec --pathspec . --pathspec tools/x/

# T: file freeze excluded from a dir-only pathspec, file changed and restored (history arm)
D2=$(newrepo); F2=$(git -C "$D2" rev-parse HEAD)
printf 'plan2\n' > "$D2/plans/c.md"; commit "$D2" "tamper c" >/dev/null
printf 'plan\n'  > "$D2/plans/c.md"; R3=$(commit "$D2" "restore c")
run T-file-restore-dir-only-pathspec 1 "$D2" "$F2" "$R3" --freeze-path tools/x --freeze-path plans/c.md --require-pathspec --pathspec tools/x/
run T2-file-restore-both-pathspecs 1 "$D2" "$F2" "$R3" --freeze-path tools/x --freeze-path plans/c.md --require-pathspec --pathspec tools/x/ --pathspec plans/c.md
run T3-file-restore-no-pathspec 2 "$D2" "$F2" "$R3" --freeze-path tools/x --freeze-path plans/c.md --require-pathspec

# U: dir-restore hidden by a descendant pathspec that names an existing subdir (W1 F-7 replication)
D3=$(newrepo); F3=$(git -C "$D3" rev-parse HEAD)
printf 'beta\n' > "$D3/tools/x/a.txt"; commit "$D3" "tamper a" >/dev/null
printf 'alpha\n' > "$D3/tools/x/a.txt"; R4=$(commit "$D3" "restore a")
run U-dir-restore-descendant-pathspec 1 "$D3" "$F3" "$R4" --freeze-path tools/x --require-pathspec --pathspec tools/x/sub/
run U2-dir-restore-exact-pathspec 1 "$D3" "$F3" "$R4" --freeze-path tools/x --require-pathspec --pathspec tools/x/

# V: live lane, read-only, claim-shaped invocation vs both-frozen-paths invocation at current tip
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
H=$(git -C "$L" rev-parse HEAD)
run V1-live-claim-shaped 0 "$L" f762b7273e3f6ca3c710bb37d5de92a4a4417aec "$H" --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec
run V2-live-both-paths 0 "$L" f762b7273e3f6ca3c710bb37d5de92a4a4417aec "$H" --pathspec tools/round-45/ --pathspec plans/round-45-claims.md --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --require-pathspec
