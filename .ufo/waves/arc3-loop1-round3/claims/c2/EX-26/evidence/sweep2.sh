#!/usr/bin/env bash
set -u
TOOL="$1"; LABEL="$2"; ROOT=/dev/shm/ex26/probe
probe() { local name="$1"; shift; local out err rc tb first
  out=$(mktemp /dev/shm/ex26/.o.XXXXXX); err=$(mktemp /dev/shm/ex26/.e.XXXXXX)
  ( cd "$ROOT" && timeout 120 python3 "$TOOL" "$@" >"$out" 2>"$err" ); rc=$?
  if grep -q Traceback "$err"; then tb=yes; else tb=no; fi
  first=$(head -1 "$err" | cut -c1-92)
  printf '%s\t%s\texit=%s\ttraceback=%s\tstderr1=%s\tselftest=%s\n' "$LABEL" "$name" "$rc" "$tb" \
    "${first:-<empty>}" "$(grep -E 'CUSTODY_PAIR_SELFTEST' "$out" | tail -1 | cut -c1-60)"
  rm -f "$out" "$err"; }
probe relative-missing   selftest --scratch does-not-exist-rel
probe trailing-slash     selftest --scratch "$ROOT/missing-dir/"
probe dotdot-missing     selftest --scratch ../ex26-definitely-missing
