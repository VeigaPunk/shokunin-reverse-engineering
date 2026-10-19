#!/usr/bin/env bash
# EX-40 declared-class matrix harness — runs the scratch oracle against every
# scratch fixture and FAILs if any measured (status, exit) differs from the
# declaration. Fixtures live under /var/tmp/ex40/fix (scratch only; the real
# custody paths are never written or opened here, only their fixtures are).
# Usage: edge-matrix.sh [path-to-oracle]
set -u
R=/var/tmp/ex40/fix
HERE=$(cd "$(dirname "$0")" && pwd)
ORACLE=${1:-$HERE/receipt-v2-scratch.py}

declare -A EXPECT_STATUS=(
  [good.txt]=ok
  [missing.txt]=MISSING
  [unreadable.txt]=UNREADABLE
  [blocked_dir/inner.txt]=UNREADABLE
  [link_ok.txt]=ok
  [link_dangling.txt]=SYMLINK_DANGLING
  [link_loop_a]=SYMLINK_LOOP
  [link_dir]=NOT_REGULAR
  [link_devnull]=NOT_REGULAR
  [pipe.fifo]=NOT_REGULAR
  [dir_target]=NOT_REGULAR
)
declare -A EXPECT_EXIT=(
  [good.txt]=0
  [missing.txt]=2
  [unreadable.txt]=2
  [blocked_dir/inner.txt]=2
  [link_ok.txt]=0
  [link_dangling.txt]=2
  [link_loop_a]=2
  [link_dir]=2
  [link_devnull]=2
  [pipe.fifo]=2
  [dir_target]=2
)

fail=0
for f in good.txt missing.txt unreadable.txt blocked_dir/inner.txt link_ok.txt \
         link_dangling.txt link_loop_a link_dir link_devnull pipe.fifo dir_target; do
  out=$(cd "$R" && timeout 5 python3 "$ORACLE" "$f" 2>&1); rc=$?
  st=$(printf '%s\n' "$out" | sed -n 's/^STATUS: //p' | head -1)
  want_st=${EXPECT_STATUS[$f]}; want_rc=${EXPECT_EXIT[$f]}
  if [ "$rc" = "$want_rc" ] && [ "$st" = "$want_st" ]; then
    printf 'OK    %-22s status=%-16s exit=%s\n' "$f" "$st" "$rc"
  else
    printf 'FAIL  %-22s status=%-16s exit=%s  (declared %s / %s)\n' "$f" "$st" "$rc" "$want_st" "$want_rc"
    fail=1
  fi
done

# aggregate run: a mixed "custody set" (one good + one dangling symlink) must
# still emit a receipt for BOTH paths and exit with the worst class (2).
out=$(cd "$R" && timeout 5 python3 "$ORACLE" good.txt link_dangling.txt 2>&1); rc=$?
agg=$(printf '%s\n' "$out" | sed -n 's/^RECEIPT: //p')
n_paths=$(printf '%s\n' "$out" | grep -c '^PATH: ')
if [ "$rc" = 2 ] && [ "$n_paths" = 2 ]; then
  printf 'OK    %-22s %s (both paths recorded)\n' "aggregate(ok+dangling)" "$agg"
else
  printf 'FAIL  %-22s rc=%s paths-recorded=%s %s\n' "aggregate(ok+dangling)" "$rc" "$n_paths" "$agg"
  fail=1
fi

# declared exit-1 (compare-mode drift) must NOT be reachable in emitter mode:
# every emitter run above is in {0,2}; assert no run returned 1.
if [ "$fail" = 0 ]; then echo "MATRIX: PASS (all classes as declared; exit=1 unreachable in emitter mode)"; else echo "MATRIX: FAIL"; fi
exit "$fail"
