#!/usr/bin/env bash
# CR-4 round-3 poller v2 — wait for the C2 landing to settle: log revision,
# selftest case count (proxy: run_case( occurrences) and the guard line every 60s.
# Exit when selftest >= 17 AND the hash is unchanged across two consecutive checks.
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
LOG=/dev/shm/cr4-arc3-r3/poll2.log
prev=""; landed=0
for i in $(seq 1 20); do
  h=$(sha256sum "$TOOL" 2>/dev/null | cut -c1-16)
  cases=$(grep -c "run_case(cases" "$TOOL" 2>/dev/null)
  guard=$(sed -n '/^def cmd_capture/,/^def cmd_verify/p' "$TOOL" 2>/dev/null | grep -c "_same_file")
  sidecar_guard=$(sed -n '/^def cmd_capture/,/^def cmd_verify/p' "$TOOL" 2>/dev/null | grep -c "with_name(out.name")
  printf '%s check=%02d sha=%s selftest_cases=%s inode_arm=%s bytes=%s\n' \
      "$(date -Is)" "$i" "$h" "$cases" "$guard" "$(stat -c %s "$TOOL" 2>/dev/null)" >> "$LOG"
  if [ "$cases" -ge 17 ] && [ "$h" = "$prev" ]; then
    echo "$(date -Is) SETTLED sha=$h selftest_cases=$cases" >> "$LOG"; landed=1; break
  fi
  prev="$h"; sleep 60
done
echo "$(date -Is) poller2 done landed=$landed" >> "$LOG"