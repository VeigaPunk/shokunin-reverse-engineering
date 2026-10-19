#!/usr/bin/env bash
# RV-7 seat poller: seats/ inventory + real-target revision, every 60s, max 25 checks.
# Records every sample with the tool sha256 prefix so the hardening landing is
# timestamped in the evidence, not narrated.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
LOG="$REPO/.ufo/waves/arc3-loop1-round3/claims/c2/RV-7/poll-log.txt"
cd "$REPO" || exit 1
for i in $(seq 1 25); do
  seats=$(ls .ufo/waves/arc3-loop1-round3/seats/ 2>/dev/null | wc -l)
  sha=$(sha256sum .ufo/gates/custody-pair/custody-pair.py 2>/dev/null | cut -c1-16)
  lsline=$(ls .ufo/waves/arc3-loop1-round3/seats/ 2>/dev/null | tr '\n' ',' | sed 's/,$//')
  printf 'check=%02d utc=%s seats=%s tool_sha=%s [%s]\n' \
    "$i" "$(date -u +%H:%M:%SZ)" "$seats" "$sha" "$lsline" >> "$LOG"
  sleep 60
done
echo "POLL DONE utc=$(date -u +%H:%M:%SZ)" >> "$LOG"