#!/usr/bin/env bash
# SentReceipts receipt harness: every check records exact command, exit code,
# stdout sha256 and UTC time. Nothing is fabricated; "not run" is printed for
# any check whose artefact is missing.
set -u
SEAT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/SentReceipts
OUT="$SEAT/receipts"
mkdir -p "$OUT"
n=0
run() {   # run <slug> <shell-command>
  n=$((n+1))
  local slug="$1"; shift
  local cmd="$*"
  local f="$OUT/$slug.stdout"
  local e="$OUT/$slug.stderr"
  local t0 t1 rc sh
  t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( eval "$cmd" ) >"$f" 2>"$e"
  rc=$?
  t1=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  sh=$(sha256sum "$f" | cut -d' ' -f1)
  {
    echo "slug: $slug"
    echo "cmd: $cmd"
    echo "exit_code: $rc"
    echo "stdout_sha256: $sh"
    echo "stdout_bytes: $(wc -c <"$f")"
    echo "stderr_sha256: $(sha256sum "$e" | cut -d' ' -f1)"
    echo "utc_start: $t0"
    echo "utc_end: $t1"
  } >"$OUT/$slug.meta"
  echo "[$rc] $slug  sha256=$sh"
}
