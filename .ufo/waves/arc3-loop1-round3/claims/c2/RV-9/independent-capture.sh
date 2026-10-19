#!/bin/bash
# RV-9 independent identity capture — does NOT use custody-pair.py.
# sha256 + stat fields for the 5 custody paths; UTC rendered from epoch via python3.
set -u
OUT="${1:?usage: independent-capture.sh OUT}"
PATHS=(
  "$HOME/.config/devin/mcp_config.json"
  "$HOME/.omp/agent/mcp.json"
  "$HOME/.kimi-code/config.toml"
  "$HOME/.bashrc"
  "$HOME/.profile"
)
{
echo "# RV-9 independent capture (stat+sha256 only; no custody-pair.py involved)"
echo "# utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)  local: $(date +%Y-%m-%dT%H:%M:%S%:z)"
for p in "${PATHS[@]}"; do
  echo "PATH: $p"
  if [ -e "$p" ]; then
    sha=$(sha256sum "$p" | cut -d' ' -f1)
    # stat: size inode mode uid gid atime mtime ctime (epoch+ns via %Y-%W? use %X)
    stat --printf='SIZE: %s\nINODE: %i\nMODE: %a\nUID: %u\nGID: %g\nMTIME_EPOCH: %Y\nCTIME_EPOCH: %Z\n' "$p"
    python3 - "$p" <<'PY'
import os, sys, time
st = os.lstat(sys.argv[1])
print("MTIME_NS: %d" % (st.st_mtime_ns,))
print("CTIME_NS: %d" % (st.st_ctime_ns,))
print("MTIME_UTC_RENDER: %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(st.st_mtime)),))
print("CTIME_UTC_RENDER: %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(int(st.st_ctime)),))
PY
    echo "SHA256: $sha"
  else
    echo "EXISTS: no"
  fi
done
} > "$OUT"
echo "wrote $OUT"