#!/usr/bin/env bash
# EX-26 boundary sweep for the selftest scratch-guard (D6).
# Usage: sweep.sh <tool.py> <label>
# Emits one TSV row per probe: label, probe, exit, traceback?, first-stderr-line.
set -u
TOOL="$1"; LABEL="$2"
ROOT=/dev/shm/ex26/probe
mkdir -p "$ROOT/okdir" "$ROOT/okdir-symlink-target"
rm -rf "$ROOT/missing-dir" "$ROOT/nested" "$ROOT/dangling"
touch "$ROOT/a-file"                      # existing regular file, not a dir
ln -sfn "$ROOT/does-not-exist" "$ROOT/dangling"        # dangling symlink
ln -sfn "$ROOT/okdir-symlink-target" "$ROOT/symlink-dir"
mkdir -p "$ROOT/ro-dir"; chmod 500 "$ROOT/ro-dir"      # existing dir, not writable

probe() {  # probe <name> <args...>
  local name="$1"; shift
  local out err rc tb first last
  out=$(mktemp /dev/shm/ex26/.out.XXXXXX); err=$(mktemp /dev/shm/ex26/.err.XXXXXX)
  timeout 120 python3 "$TOOL" "$@" >"$out" 2>"$err"; rc=$?
  if grep -q "Traceback" "$err"; then tb=yes; else tb=no; fi
  first=$(head -1 "$err" | cut -c1-96)
  last=$(grep -E "CUSTODY_PAIR_SELFTEST" "$out" | tail -1 | cut -c1-96)
  printf '%s\t%s\texit=%s\ttraceback=%s\tstderr1=%s\tselftest=%s\n' \
     "$LABEL" "$name" "$rc" "$tb" "${first:-<empty>}" "${last:-<none>}"
  rm -f "$out" "$err"
}

probe missing-dir        selftest --scratch "$ROOT/missing-dir"
probe nested-missing     selftest --scratch "$ROOT/nested/deeper/leaf"
probe file-as-scratch    selftest --scratch "$ROOT/a-file"
probe dangling-symlink   selftest --scratch "$ROOT/dangling"
probe readonly-dir       selftest --scratch "$ROOT/ro-dir"
probe devnull-scratch    selftest --scratch /dev/null
probe proc-missing       selftest --scratch /proc/ex26-none
probe proc-root-rw?      selftest --scratch /proc
probe existing-dir       selftest --scratch "$ROOT/okdir"
probe symlink-to-dir     selftest --scratch "$ROOT/symlink-dir"
probe empty-flag         selftest --scratch=
probe default-no-flag    selftest
chmod 700 "$ROOT/ro-dir" 2>/dev/null
rm -f "$ROOT/a-file" "$ROOT/dangling" "$ROOT/symlink-dir"