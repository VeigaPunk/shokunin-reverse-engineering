#!/usr/bin/env bash
# Build read-only census fixtures under scratch and run the standing SOURCES parser.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r76/ScribeRows
FIX=$S/fixture
ROWS=$S/rows-draft.md
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh

build_fixture() { # $1 = fixture root
  local root=$1 top
  rm -rf -- "$root"; mkdir -p -- "$root/corpus"
  while IFS= read -r top; do
    case "$top" in corpus|.git|.fast) continue;; esac
    ln -s -- "$LANE/$top" "$root/$top"
  done < <(ls -A "$LANE")
  while IFS= read -r top; do
    [ "$top" = SOURCES.md ] && continue
    ln -s -- "$LANE/corpus/$top" "$root/corpus/$top"
  done < <(ls -A "$LANE/corpus")
}

insert_rows() { # $1 = SOURCES.md path, $2 = rows file
  python3 - "$1" "$2" <<'PY'
import sys
target, rowsf = sys.argv[1], sys.argv[2]
lines = open(target, encoding='utf-8').read().splitlines(True)
last = max(i for i, l in enumerate(lines) if l.startswith('| S'))
rows = open(rowsf, encoding='utf-8').read().rstrip('\n').splitlines()
lines[last+1:last+1] = [r + '\n' for r in rows]
open(target, 'w', encoding='utf-8').writelines(lines)
print('inserted at', last + 2)
PY
}

run() { # $1 label, $2 fixture root, $3 out suffix
  local out=$S/census-$3.txt
  "$CENSUS" validate --file "$2/corpus/SOURCES.md" --today 2026-11-04 >"$out" 2>"$out.err"
  local rc=$?
  printf 'label=%s rc=%s lines=%s\n' "$1" "$rc" "$(wc -l < "$out")" | tee -a "$S/census-exits.txt"
}

: >"$S/census-exits.txt"

# --- HEAD copy: baseline and with my three rows appended -------------------
build_fixture "$FIX/head"
git -C "$LANE" show HEAD:corpus/SOURCES.md >"$FIX/head/corpus/SOURCES.md"
run head-baseline "$FIX/head" head-baseline
insert_rows "$FIX/head/corpus/SOURCES.md" "$ROWS" >"$S/insert-head.txt"
run head-with-rows "$FIX/head" head-with-rows
diff -u "$S/census-head-baseline.txt" "$S/census-head-with-rows.txt" >"$S/census-head-diff.txt"
echo "head-diff-rc=$?" >>"$S/census-exits.txt"

# --- worktree copy (carries the uncommitted S286-S288 block) ---------------
build_fixture "$FIX/worktree"
cp "$LANE/corpus/SOURCES.md" "$FIX/worktree/corpus/SOURCES.md"
run worktree-baseline "$FIX/worktree" worktree-baseline
insert_rows "$FIX/worktree/corpus/SOURCES.md" "$ROWS" >"$S/insert-worktree.txt"
run worktree-with-rows "$FIX/worktree" worktree-with-rows
diff -u "$S/census-worktree-baseline.txt" "$S/census-worktree-with-rows.txt" >"$S/census-worktree-diff.txt"
echo "worktree-diff-rc=$?" >>"$S/census-exits.txt"

# --- collision proof: rows with my ids against the worktree file -----------
grep -n 'E03' "$S/census-worktree-with-rows.txt" >"$S/census-e03.txt" || true
cat "$S/census-exits.txt"
