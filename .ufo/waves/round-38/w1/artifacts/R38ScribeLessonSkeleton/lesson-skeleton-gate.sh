#!/usr/bin/env bash
# Lesson-skeleton gate (fix for R37-CL3: no corpus/lessons/round-37.md at 77091b49).
# For every round named on argv, require corpus/lessons/round-N.md to exist at REV.
# Run before WAVE-DONE; exits 1 naming each round whose lesson file is missing.
# usage: lesson-skeleton-gate.sh LANE_ROOT REV ROUND...
set -euo pipefail
ROOT="${1:?lane root}"; REV="${2:?revision}"; shift 2
rc=0
for r in "$@"; do
  if git -C "$ROOT" cat-file -e "$REV:corpus/lessons/round-$r.md" 2>/dev/null; then
    echo "ok      round-$r corpus/lessons/round-$r.md"
  else
    echo "MISSING round-$r corpus/lessons/round-$r.md"; rc=1
  fi
done
exit "$rc"
