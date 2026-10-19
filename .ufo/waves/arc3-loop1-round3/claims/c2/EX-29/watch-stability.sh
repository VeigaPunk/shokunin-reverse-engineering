#!/bin/bash
# EX-29: watch the revised tool until sha is stable across 4 consecutive 20s checks
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
LOG=.ufo/waves/arc3-loop1-round3/claims/c2/EX-29/stability-watch.txt
: > "$LOG"
prev=""; stable=0
for i in $(seq 1 60); do
  sha=$(sha256sum .ufo/gates/custody-pair/custody-pair.py | cut -d' ' -f1)
  mtime=$(stat -c %y .ufo/gates/custody-pair/custody-pair.py | cut -d. -f1)
  rp=$(grep -c "require-paths" .ufo/gates/custody-pair/custody-pair.py)
  seats=$(ls .ufo/waves/arc3-loop1-round3/seats/ 2>/dev/null | tr '\n' ' ')
  echo "$(date -u +%FT%TZ) check=$i sha=$sha mtime=$mtime require_paths_hits=$rp seats=[$seats]" >> "$LOG"
  if [ -n "$prev" ] && [ "$sha" = "$prev" ]; then stable=$((stable+1)); else stable=0; fi
  prev=$sha
  if [ $stable -ge 4 ]; then
    echo "STABLE after check=$i sha=$sha" | tee -a "$LOG"
    exit 0
  fi
  sleep 20
done
echo "WATCH-TIMEOUT last_sha=$prev" | tee -a "$LOG"
