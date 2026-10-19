#!/usr/bin/env bash
# CR-4 poller — wait for EX-21's write-guard extension to land in
# .ufo/gates/custody-pair/custody-pair.py (chain c2's real target), logging every
# observed revision. Exits early when the inode arm is wired into cmd_capture AND
# the file hash is stable across two consecutive checks (D8 churn discipline).
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
LOG=/dev/shm/cr4-arc3-r3/poll.log
prev=""; landed=0
for i in $(seq 1 25); do
  h=$(sha256sum "$TOOL" 2>/dev/null | cut -c1-12)
  body=$(sed -n '/^def cmd_capture/,/^def cmd_verify/p' "$TOOL" 2>/dev/null)
  inode=$(printf '%s' "$body" | grep -c "_same_file")
  sidecar=$(printf '%s' "$body" | grep -c "sha256\")" )
  printf '%s check=%02d sha=%s inode_arm_in_capture=%s bytes=%s\n' \
      "$(date -Is)" "$i" "$h" "$inode" "$(stat -c %s "$TOOL" 2>/dev/null)" >> "$LOG"
  if [ "$inode" -ge 1 ] && [ "$h" = "$prev" ]; then
    echo "$(date -Is) LANDED-STABLE sha=$h inode_arm_in_capture=$inode" >> "$LOG"
    landed=1; break
  fi
  prev="$h"
  sleep 60
done
echo "$(date -Is) poller done landed=$landed" >> "$LOG"