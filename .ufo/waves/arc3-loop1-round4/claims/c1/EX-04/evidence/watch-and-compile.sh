#!/usr/bin/env bash
# EX-04 watcher — poll for EX-02's authorized venv, then compile + verify + probe.
# Scratch: /var/tmp/ex04-r4 (never /tmp). Max 25 checks at 60s.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
WAVE=$REPO/.ufo/waves/arc3-loop1-round4
SEAT=$WAVE/claims/c1/EX-04
WORK=$SEAT/out
LOG=$SEAT/evidence/watch-log.txt
VYPER=$WAVE/tools/vyper-venv/bin/vyper
mkdir -p "$WORK" /var/tmp/ex04-r4

say() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG"; }

say "watcher start; waiting for $VYPER"
for i in $(seq 1 25); do
  if [ -x "$VYPER" ]; then
    say "check $i: venv present at $VYPER"
    break
  fi
  say "check $i: not yet present"
  sleep 60
done
if [ ! -x "$VYPER" ]; then
  say "TIMEOUT: venv never appeared after 25 checks (25 min). Writing gap note."
  echo "venv absent after 25 polls; EX-04 compiled nothing (honest gap)." > "$SEAT/evidence/venv-timeout.txt"
  exit 3
fi

sleep 5
say "venv present; version=$("$VYPER" --version 2>&1)"
ls -la "$WAVE/tools/" >> "$LOG" 2>&1
[ -f "$WAVE/tools/vyper-venv/install-receipt.txt" ] && cp "$WAVE/tools/vyper-venv/install-receipt.txt" "$SEAT/evidence/venv-install-receipt.txt" && say "copied EX-02 install receipt"
[ -f "$WAVE/tools/vyper-venv/RECEIPT.txt" ] && cp "$WAVE/tools/vyper-venv/RECEIPT.txt" "$SEAT/evidence/venv-install-receipt.txt" && say "copied EX-02 install receipt (RECEIPT.txt)"
find "$WAVE/tools/vyper-venv" -maxdepth 1 -type f >> "$LOG" 2>&1

say "compiling"
bash "$SEAT/evidence/compile-carrier.sh" "$WAVE/tools/vyper-venv" "$WORK" >> "$LOG" 2>&1
rc=$?
say "compile rc=$rc"
if [ $rc -ne 0 ]; then
  say "COMPILE FAILED — see $WORK/compile-receipt.txt and combined.err"
  exit 4
fi

say "verifying artifacts"
python3 "$SEAT/evidence/verify-artifacts.py" "$WORK" "$SEAT/evidence/planted-K.json" >> "$LOG" 2>&1
say "verify rc=$?"

say "done; artifacts in $WORK"
ls -la "$WORK" >> "$LOG" 2>&1
