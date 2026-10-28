#!/usr/bin/env bash
# R44Watchdog receipt harness: seat, command, exit code, stdout sha256, wall time.
set -u
SEAT=R44Watchdog
OUT=out
: > receipts.tsv
printf 'seat\tid\texit\tstdout_sha256\twall_s\tbytes\tcommand\n' >> receipts.tsv
i=0
rec() { # rec <id> <command...>
  local id="$1"; shift
  local f="$OUT/$id.stdout.txt" e="$OUT/$id.stderr.txt"
  local t0 t1 rc sha bytes wall
  t0=$(date +%s.%N)
  "$@" >"$f" 2>"$e"; rc=$?
  t1=$(date +%s.%N)
  wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
  sha=$(sha256sum "$f" | cut -d' ' -f1)
  bytes=$(stat -c%s "$f")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$SEAT" "$id" "$rc" "$sha" "$wall" "$bytes" "$*" >> receipts.tsv
  echo "[$id] rc=$rc wall=${wall}s sha256=$sha"
  return 0
}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
WL=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log

rec W1-launch-lines        grep -nE "(launch|complete|lane-dead-no-report) kaidoku round=44" "$WL"
rec W2-kaidoku-all-r44     grep -nE "kaidoku" "$WL" -A0
rec W3-round44-fleet       grep -nE "round=44" "$WL"
rec W4-watchdog-tail       tail -n 14 "$WL"
rec W5-lane-unblob-hash    sha256sum "$LANE/unblob.log"
rec W6-lane-unblob-log     cat "$LANE/unblob.log"
rec W7-lane-unblob-tracked git -C "$LANE" log --format=%h%x09%cI%x09%s -- unblob.log
rec W8-scratch-unblob-logs find /fast/scratch/hyaku/kaidoku-r44 -name 'unblob.log' -newermt '2026-10-28 00:00'
rec W9-scratch-extract-cmd grep -rh "Running extract command" /fast/scratch/hyaku/kaidoku-r44/probe-R44C1Revenger
rec W10-head-vs-origin      git -C "$LANE" rev-list --left-right --count origin/main...HEAD
rec W11-lsremote            git -C "$LANE" ls-remote origin refs/heads/main
rec W12-pgid-alive          bash -c 'ps -eo pid,pgid,args | awk "\$2==3257226"'
rec W13-dispatcher-spawn    grep -nE "kaidoku 44" /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log
rec W14-report-absent       ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-44/kaidoku.md
