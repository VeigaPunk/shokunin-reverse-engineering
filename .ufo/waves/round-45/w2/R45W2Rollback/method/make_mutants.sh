#!/bin/bash
# Mutant + receipt driver. Everything writes inside $S only.
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2Rollback
export TMPDIR="$S" HYAKU_SCRATCH="$S/counterscratch"
mkdir -p "$S/receipts" "$S/counterscratch"
C="$S/clone"
cd "$C" || exit 9
TOP=$(git rev-parse --show-toplevel)
[ "$TOP" = "$C" ] || { echo "REFUSING: toplevel $TOP"; exit 9; }

receipt() { # receipt <name> <cmd...>
  local name=$1; shift
  local out="$S/receipts/$name.out" err="$S/receipts/$name.err"
  local utc; utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  "$@" >"$out" 2>"$err"; local rc=$?
  local sha; sha=$(sha256sum "$out" | cut -d' ' -f1)
  local esha; esha=$(sha256sum "$err" | cut -d' ' -f1)
  printf 'name=%s\nutc=%s\ncmd=%q ' "$name" "$utc" "$1" >"$S/receipts/$name.receipt"
  shift; printf '%q ' "$@" >>"$S/receipts/$name.receipt"
  printf '\nexit=%s\nstdout_sha256=%s\nstderr_sha256=%s\nstdout_bytes=%s\n' \
    "$rc" "$sha" "$esha" "$(wc -c <"$out")" >>"$S/receipts/$name.receipt"
  echo "[$name] exit=$rc sha=$sha"
  return 0
}

mutant() { # mutant <branch> <srcfile> <msg>
  local br=$1 src=$2 msg=$3
  git checkout -q -B "$br" e715263cb51b713c342ab992d527fe9d61d6f8ff || exit 8
  cp "$src" "$C/SKILL.md"
  git add SKILL.md
  git -c user.name='R45W2Rollback mutant' -c user.email='w2@scratch' commit -q -m "$msg" || exit 8
  git rev-parse HEAD
}

M1=$(mutant mut-block22-only "$S/SKILL.m1.md" "mutant: remove block 22 only (landing e715263)") || exit 8
M2=$(mutant mut-registry-only "$S/SKILL.m2.md" "mutant: remove the six registry rows only") || exit 8
M3=$(mutant mut-full-revert "$S/SKILL.m3.md" "mutant: remove block 22 and the registry section") || exit 8
echo "M1=$M1"; echo "M2=$M2"; echo "M3=$M3"
printf '%s\n' "$M1" "$M2" "$M3" >"$S/mutants.txt"
