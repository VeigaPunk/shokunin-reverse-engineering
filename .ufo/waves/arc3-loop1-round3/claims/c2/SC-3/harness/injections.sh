#!/usr/bin/env bash
# SC-3 injection harness — chain c2, wave arc3-loop1-round3.
# Four holes (D2 / D3 / write-guard / D6) as injections, one run per tool revision.
# usage: injections.sh <custody-pair.py> <out-root>
# Writes one NN-name.out per injection + summary.txt. Scratch-only: never touches
# a custody path; /tmp never used.
set -u
TOOL="$1"
OUT="$2"
WORK="$OUT/work"
mkdir -p "$OUT" "$WORK"
PY=python3

{
  echo "# SC-3 injection harness"
  echo "# date: $(date -Is)"
  echo "# tool: $TOOL"
  echo "# tool-sha256: $(sha256sum "$TOOL" | cut -d' ' -f1)"
  echo "# tool-lines: $(wc -l < "$TOOL")"
  echo "# python: $($PY -V 2>&1)"
} > "$OUT/summary.txt"

run() { # run <name> <cmdfile-text>
  local name="$1"; shift
  {
    echo "### $name"
    echo "\$ $*"
    "$@"
    echo "exit=$?"
  } > "$OUT/$name.out" 2>&1
  tail -n 3 "$OUT/$name.out" | sed "s/^/  /" >> "$OUT/summary.txt"
}

# ---------- I0 control: selftest on an existing scratch dir (case count) -------
mkdir -p "$WORK/scratch-ok"
run i0-selftest-control $PY "$TOOL" selftest --scratch "$WORK/scratch-ok"

# ---------- I1  D2a: exists-but-EACCES path (fail-open) ------------------------
D="$WORK/d2a"; mkdir -p "$D/blocked_dir"
printf 'inner payload\n' > "$D/blocked_dir/inner.txt"
chmod 000 "$D/blocked_dir"
run i1a-capture-eacces $PY "$TOOL" capture --out "$D/blocked-pre.txt" --paths "$D/blocked_dir/inner.txt"
run i1b-verify-live-eacces $PY "$TOOL" verify "$D/blocked-pre.txt" --live
chmod 755 "$D/blocked_dir"

# ---------- I2  D2a': both-sides-absent path (plain ghost) ---------------------
D="$WORK/d2b"; mkdir -p "$D"
run i2a-capture-ghost $PY "$TOOL" capture --out "$D/ghost-pre.txt" --paths "$D/ghost.txt"
run i2b-verify-live-ghost $PY "$TOOL" verify "$D/ghost-pre.txt" --live

# ---------- I3  D2b: unreadable file -> crash outside the declared map ---------
D="$WORK/d2c"; mkdir -p "$D"
printf 'secret payload\n' > "$D/unreadable.txt"
chmod 000 "$D/unreadable.txt"
run i3a-capture-unreadable $PY "$TOOL" capture --out - --paths "$D/unreadable.txt"
chmod 644 "$D/unreadable.txt"
run i3b-capture-unreadable-readable-control $PY "$TOOL" capture --out "$D/ok-pre.txt" --paths "$D/unreadable.txt"
chmod 000 "$D/unreadable.txt"
run i3c-verify-live-unreadable $PY "$TOOL" verify "$D/ok-pre.txt" --live
chmod 644 "$D/unreadable.txt"

# ---------- I4  D3: partial-reference coverage ---------------------------------
D="$WORK/d3"; mkdir -p "$D"
for i in 1 2 3 4 5; do printf 'p%s\n' "$i" > "$D/f$i.txt"; done
run i4a-capture-1of5 $PY "$TOOL" capture --out "$D/pre-1of5.txt" --paths "$D/f1.txt"
run i4b-verify-1of5-live $PY "$TOOL" verify "$D/pre-1of5.txt" --live
run i4c-verify-1of5-live-require5 $PY "$TOOL" verify "$D/pre-1of5.txt" --live --require-paths 5
run i4d-cover-default-flag $PY "$TOOL" verify "$D/pre-1of5.txt" --live --cover-default-paths

# ---------- I5  write-guard scope: --paths X --out X ---------------------------
D="$WORK/wg"; mkdir -p "$D"
printf 'victim payload: the file the receipt measures\n' > "$D/victim.txt"
BEFORE_SHA=$(sha256sum "$D/victim.txt" | cut -d' ' -f1)
run i5a-capture-out-over-scoped $PY "$TOOL" capture --paths "$D/victim.txt" --out "$D/victim.txt"
AFTER_SHA=$(sha256sum "$D/victim.txt" | cut -d' ' -f1)
{
  echo "### i5b-write-guard-scope-delta"
  echo "before-sha=$BEFORE_SHA"
  echo "after-sha=$AFTER_SHA"
  echo "victim-first-line-after: $(head -1 "$D/victim.txt")"
  [ "$BEFORE_SHA" = "$AFTER_SHA" ] && echo "verdict=UNCHANGED" || echo "verdict=CLOBBERED"
} > "$OUT/i5b-write-guard-scope-delta.out" 2>&1
tail -n 4 "$OUT/i5b-write-guard-scope-delta.out" | sed "s/^/  /" >> "$OUT/summary.txt"

# canonical-set control (tool-internal guard already declared for CUSTODY_PATHS):
# selftest case refuses-to-write-over-custody-path exercises it without writing.
grep -c "refuses-to-write-over-custody-path" "$OUT/i0-selftest-control.out" > /dev/null || true

# ---------- I6  D6: selftest --scratch <missing dir> ---------------------------
D="$WORK/d6"; mkdir -p "$D"
run i6a-selftest-missing-scratch $PY "$TOOL" selftest --scratch "$D/does-not-exist"
run i6b-selftest-existing-scratch-after $PY "$TOOL" selftest --scratch "$WORK/scratch-ok"

# ---------- I7  CLI surface (flags added by a revision) ------------------------
run i7a-capture-help $PY "$TOOL" capture --help
run i7b-verify-help $PY "$TOOL" verify --help
run i7c-selftest-help $PY "$TOOL" selftest --help

echo "done: $OUT" >> "$OUT/summary.txt"