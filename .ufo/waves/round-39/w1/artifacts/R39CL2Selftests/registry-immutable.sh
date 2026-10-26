#!/usr/bin/env bash
# registry-immutable.sh LANE BASE REV
# CORPUS.md SOURCES rule 2 (append-only): for every registry row present at BASE,
# only status, recheck and used-by may differ at REV. Prints each row whose other
# cells changed (id, column numbers) and exits 1; exits 0 when none changed.
# Round-38 mistake M38-8: the S110 scope cell was widened in place at 3b960fe5.
#
# registry-immutable.sh --selftest
# Builds a throwaway fixture repository under $TMPDIR and exercises five
# green/red constructs (append-only 0, in-place cell edit 1, row deletion 1,
# reorder 1, allowed-cell change 0). Prints SELFTEST cases=n pass=n fail=n and
# exits 0 only when every case passes; it touches no lane path.
set -euo pipefail

if [ "${1:-}" = "--selftest" ]; then
  SELF=$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")
  exec bash "$SELF" __selftest_inner__
fi

if [ "${1:-}" = "__selftest_inner__" ]; then
  SELF=$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")
  S=$(mktemp -d "${TMPDIR:-/tmp}/fx.XXXXXX")
  trap 'rm -rf -- "$S"' EXIT
  mkdir -p "$S/corpus"
  git -C "$S" init -q -b main
  top=$(git -C "$S" rev-parse --show-toplevel)
  if [ "$(cd "$S" && pwd -P)" != "$top" ]; then
    echo "fixture toplevel $top != $S"; exit 1
  fi

  fx_commit() {  # fx_commit MSG -> prints the new commit
    git -C "$S" add -A
    git -C "$S" -c user.name=fx -c user.email=fx@fx -c commit.gpgsign=false \
      commit -q --no-verify -m "$1"
    git -C "$S" rev-parse HEAD
  }

  # one row per registry line; each commit rewrites corpus/SOURCES.md from the
  # row list it is given, so every base/rev pair differs in exactly one way.
  write_table() {
    {
      printf '# SOURCES — fixture\n\n## Registry\n\n'
      printf '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
      printf '|---|---|---|---|---|---|---|---|---|---|---|\n'
      for r in "$@"; do printf '%s\n' "$r"; done
    } > "$S/corpus/SOURCES.md"
  }

  R1='| S001 | source one | docs | A | scope one | anchor one | teaches one | mined | 2026-10-19 | on-release | corpus/lessons/a.md |'
  R2='| S002 | source two | docs | A | scope two | anchor two | teaches two | mined | 2026-10-19 | on-release | corpus/lessons/b.md |'
  R2X='| S002 | source two | docs | A | scope two widened in place | anchor two | teaches two | mined | 2026-10-19 | on-release | corpus/lessons/b.md |'
  R3='| S003 | source three | code | A | scope three | anchor three | teaches three | mined | 2026-10-19 | on-release | corpus/lessons/c.md |'
  R4='| S004 | source four | docs | A | scope four | anchor four | teaches four | staged | 2026-10-26 | on-release | corpus/lessons/d.md |'
  R1D='| S001 | source one | docs | A | scope one | anchor one | teaches one | used | 2026-10-19 | 180d | corpus/lessons/a.md, corpus/lessons/e.md |'

  write_table "$R1" "$R2" "$R3";           C0=$(fx_commit 'base: three registry rows')
  write_table "$R1" "$R2" "$R3" "$R4";     C1=$(fx_commit 'append S004 (legal append)')
  write_table "$R1" "$R2X" "$R3" "$R4";    C2=$(fx_commit 'edit the S002 scope cell in place')
  write_table "$R1" "$R2X" "$R4";          C3=$(fx_commit 'delete the S003 row')
  write_table "$R2X" "$R1" "$R4";          C4=$(fx_commit 'reorder the S001 and S002 rows')
  write_table "$R2X" "$R1D" "$R4";         C5=$(fx_commit 'change only status, recheck and used-by of S001')

  cases=0 pass=0 fail=0
  run_case() {  # run_case NAME EXPECT BASE REV [NEEDLE]
    local name=$1 expect=$2 b=$3 r=$4 needle=${5:-} out rc why=''
    set +e
    out=$(bash "$SELF" "$S" "$b" "$r" 2>&1); rc=$?
    set -e
    cases=$((cases + 1))
    [ "$rc" = "$expect" ] || why="exit $rc != $expect"
    if [ -n "$needle" ] && ! printf '%s' "$out" | grep -qF -- "$needle"; then
      why="${why:+$why; }output does not contain '$needle'"
    fi
    if [ -z "$why" ]; then
      pass=$((pass + 1)); echo "case $name: expect exit=$expect got $rc PASS"
    else
      fail=$((fail + 1)); echo "case $name: expect exit=$expect got $rc FAIL"
      echo "  - $why"
      printf '%s\n' "$out" | sed 's/^/    out: /'
    fi
  }

  run_case append-only      0 "$C0" "$C1"
  run_case in-place-cell    1 "$C1" "$C2" 'S002 changed columns: 6'
  run_case row-deletion     1 "$C2" "$C3" 'S003'
  run_case row-reorder      1 "$C3" "$C4" 'S001'
  run_case allowed-cells    0 "$C4" "$C5"

  printf 'SELFTEST cases=%d pass=%d fail=%d\n' "$cases" "$pass" "$fail"
  [ "$fail" -eq 0 ] || exit 1
  exit 0
fi

lane=$1 base=$2 rev=$3
rows() { git -C "$lane" show "$1:corpus/SOURCES.md" | grep -E '^ {0,3}\| *S[0-9]{3,} *\|'; }
# columns (awk -F'|'): 2 id, 3 source, 4 kind, 5 tier, 6 scope, 7 anchor, 8 teaches, 9 status, 10 opened, 11 recheck, 12 used-by
awk -F'|' 'NR==FNR { id=$2; gsub(/ /,"",id); b[id]=$0; next }
  { id=$2; gsub(/ /,"",id); if (!(id in b)) next
    n=split(b[id], o, "|"); bad=""
    for (c=2; c<=12; c++) if (c!=9 && c!=11 && c!=12 && o[c]!=$c) bad=bad " " c
    if (bad!="") { print id, "changed columns:" bad; hit=1 } }
  END { exit hit ? 1 : 0 }' <(rows "$base") <(rows "$rev")
