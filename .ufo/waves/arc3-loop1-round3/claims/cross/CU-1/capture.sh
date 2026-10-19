#!/usr/bin/env bash
# CU-1 (arc3-loop1-round3) independent custody capture.
# Read-only: sha256 via 3 implementations + GNU stat. No writes to custody paths.
# Usage: capture.sh [label]
set -u
LABEL="${1:-capture}"
PATHS=(
  "$HOME/.config/devin/mcp_config.json"
  "$HOME/.omp/agent/mcp.json"
  "$HOME/.kimi-code/config.toml"
  "$HOME/.bashrc"
  "$HOME/.profile"
)
echo "CU-1-INDEPENDENT-CAPTURE label=$LABEL host=$(uname -n) utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
for p in "${PATHS[@]}"; do
  echo "--- $p"
  if [ ! -e "$p" ]; then echo "EXISTS=no"; continue; fi
  echo "EXISTS=yes"
  # three independent sha256 implementations
  s_core=$(sha256sum -- "$p" | awk '{print $1}')
  s_openssl=$(openssl dgst -sha256 -- "$p" 2>/dev/null | awk '{print $NF}')
  s_py=$(python3 - "$p" <<'PY'
import hashlib,sys
h=hashlib.sha256()
with open(sys.argv[1],'rb') as f:
    for b in iter(lambda: f.read(1<<20), b''):
        h.update(b)
print(h.hexdigest())
PY
)
  echo "SHA256_coreutils=$s_core"
  echo "SHA256_openssl=$s_openssl"
  echo "SHA256_python=$s_py"
  if [ "$s_core" = "$s_openssl" ] && [ "$s_core" = "$s_py" ]; then echo "SHA256_AGREE=yes"; else echo "SHA256_AGREE=NO"; fi
  # GNU stat: lstat-based, epoch + ns
  stat -c 'LSTAT inode=%i type=%F mode=%a uid=%u gid=%g size=%s' -- "$p"
  stat -c 'MTIME_EPOCH=%Y MTIME_NS_EXTRA=%.9Y' -- "$p"
  stat -c 'CTIME_EPOCH=%Z CTIME_NS_EXTRA=%.9Z' -- "$p"
  stat -c 'MTIME_LOCAL_STAT=%y' -- "$p"
  stat -c 'CTIME_LOCAL_STAT=%z' -- "$p"
  python3 - "$p" <<'PY'
import os,sys,time
st=os.lstat(sys.argv[1])
mt,ct=st.st_mtime,st.st_ctime
print("MTIME_UTC_RENDER=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(mt)))
print("MTIME_LOCAL_RENDER=%s" % time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(mt)))
print("MTIME_NS=%d" % int(round(mt*1e9)))
print("CTIME_UTC_RENDER=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ct)))
print("CTIME_LOCAL_RENDER=%s" % time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(ct)))
print("CTIME_NS=%d" % int(round(ct*1e9)))
print("NANOSEC_EQ: mtime_ns==int(mtime)? check via os.stat fields: mtime_ns=%d ctime_ns=%d" % (st.st_mtime_ns, st.st_ctime_ns))
PY
  # third implementation for times: integer seconds via stat only (already above)
done
echo "CU-1-INDEPENDENT-CAPTURE-END label=$LABEL"