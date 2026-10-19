#!/usr/bin/env bash
# VZ-4 independent custody capture (READ-ONLY: stat + sha256 only, no writes to
# custody paths). Emits sha256 + mtime-epoch + inode + ctime per path.
# Usage: bash custody-capture.sh <label>
set -u
LABEL="${1:-unlabeled}"
PATHS=(
  "$HOME/.config/devin/mcp_config.json"
  "$HOME/.omp/agent/mcp.json"
  "$HOME/.kimi-code/config.toml"
  "$HOME/.bashrc"
  "$HOME/.profile"
)
echo "capture_label=$LABEL"
echo "capture_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "capture_epoch=$(date +%s)"
echo "head=$(git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD 2>/dev/null || echo n/a)"
echo
n=0
fail=0
for p in "${PATHS[@]}"; do
  n=$((n+1))
  if [[ ! -e "$p" ]]; then
    echo "MISSING $p"; fail=$((fail+1)); continue
  fi
  h=$(sha256sum "$p" 2>/dev/null | cut -d' ' -f1)
  # %Y mtime epoch, %i inode, %Z ctime epoch, %s size
  read -r mt ino ct sz <<<"$(stat -c '%Y %i %Z %s' "$p")"
  echo "$h  mtime_epoch=$mt inode=$ino ctime_epoch=$ct size=$sz  $p"
done
echo
echo "files_present=$n fail=$fail"
