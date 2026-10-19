#!/bin/bash
# RV-12 independent 5-path custody capture — read-only (sha256sum + stat only).
# Usage: capture-5path.sh <label>
# Emits one receipt block to stdout. Never reads file contents beyond hashing.
set -u
LABEL="${1:-unlabeled}"
PATHS=(
  "$HOME/.config/devin/mcp_config.json"
  "$HOME/.omp/agent/mcp.json"
  "$HOME/.kimi-code/config.toml"
  "$HOME/.bashrc"
  "$HOME/.profile"
)
printf '# RV-12 independent custody capture (sha256sum + stat only)\n'
printf '# label: %s\n' "$LABEL"
printf '# capture-utc: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf '# capture-local: %s\n' "$(date +'%Y-%m-%d %H:%M:%S %z')"
printf '# host: %s  user: %s\n' "$(hostname)" "$(whoami)"
printf '# sha256sum: %s\n' "$(command -v sha256sum)"
printf '# format: PATH | sha256 | size | inode | mtime_epoch | ctime_epoch | mode | uid | gid\n'
for p in "${PATHS[@]}"; do
  if [ ! -e "$p" ]; then
    printf 'ABSENT | %s\n' "$p"
    continue
  fi
  read -r sha _ < <(sha256sum -- "$p")
  # %s size, %i inode, %Y mtime epoch, %Z ctime epoch, %a mode, %u uid, %g gid
  IFS=' ' read -r size inode mtimeE ctimeE mode uid gid < <(stat -c '%s %i %Y %Z %a %u %g' -- "$p")
  printf '%s | %s | %s | %s | %s | %s | %s | %s | %s\n' \
    "$p" "$sha" "$size" "$inode" "$mtimeE" "$ctimeE" "$mode" "$uid" "$gid"
done
printf '# compact sha256 list\n'
for p in "${PATHS[@]}"; do
  [ -e "$p" ] && sha256sum -- "$p"
done
printf '# end\n'
