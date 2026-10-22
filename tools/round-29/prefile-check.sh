#!/bin/sh
# Pre-file check (mistake M29-1): run on the lane after the last seat settles and the last lane
# commit lands, before the round report is filed. Exit 0 when `git status --porcelain` is empty
# (no modified, staged or untracked path); exit 1 and print the paths otherwise; exit 2 on usage.
# Read-only: it runs no git write.
[ $# -eq 1 ] || { echo "usage: prefile-check.sh <lane-root>" >&2; exit 2; }
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
out=$(git -C "$1" status --porcelain) || exit 2
if [ -n "$out" ]; then
    printf '%s\n' "$out"
    echo "prefile: NOT CLEAN ($(printf '%s\n' "$out" | wc -l) paths)"
    exit 1
fi
echo "prefile: clean"
exit 0
