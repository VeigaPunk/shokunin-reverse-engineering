#!/bin/bash
# CU-1 post-install corroboration: run when C1's venv lands.
set -u
S=/dev/shm/cu1
W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4
OUT=$S/post-install-verify.out
exec > >(tee "$OUT") 2>&1
echo "=== CU-1 POST-INSTALL VERIFY  $(date -Is) ==="
echo
echo "--- [1] custody paths: baseline vs now (byte identity) ---"
for p in "$HOME/.config/devin/mcp_config.json" "$HOME/.omp/agent/mcp.json" "$HOME/.kimi-code/config.toml" "$HOME/.bashrc" "$HOME/.profile"; do
  now=$(stat -c 'SIZE=%s MTIME=%Y INODE=%i MODE=%a CTIME_NS=%z' "$p"); nowh=$(sha256sum "$p" | cut -d' ' -f1)
  base=$(grep -A2 "^--- $p$" $S/custody-baseline.txt | tail -2)
  echo "PATH $p"; echo "  now : $now"; echo "  sha : $nowh"
done
echo
echo "--- [2] custody tool + README hashes (must equal 7cd19c3c… / f30df42e…) ---"
sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/README.md
echo
echo "--- [3] system python identity (must equal baseline) ---"
sha256sum /usr/bin/python3 /usr/bin/python3.14
find /usr/lib/python3.14 -xdev -printf '%p\t%s\t%T@\n' 2>/dev/null | LC_ALL=C sort | sha256sum
echo "expect python-manifest 98317190ba98ad1c6d9d83f5bf77cd5cc07b763b0c922c6159373f92c7671a8f"
echo
echo "--- [4] system python still has no vyper / no pip ---"
/usr/bin/python3 -c "import vyper" 2>&1 | tail -1
/usr/bin/python3 -m pip --version 2>&1 | tail -1
echo
echo "--- [5] venv location + python identity ---"
ls -la "$W/tools/" 2>&1
if [ -x "$W/tools/vyper-venv/bin/python" ]; then
  "$W/tools/vyper-venv/bin/python" -VV
  readlink -f "$W/tools/vyper-venv/bin/python"
  "$W/tools/vyper-venv/bin/python" -c "import vyper; print('vyper', vyper.__version__, vyper.__file__)" 2>&1 | tail -2
  echo "--- venv pyvenv.cfg ---"; cat "$W/tools/vyper-venv/pyvenv.cfg" 2>&1
else
  echo "venv python not found at $W/tools/vyper-venv/bin/python"
fi
echo
echo "--- [6] custody dir census (unchanged?) ---"
find /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair -printf '%p\t%s\t%T@\t%m\n' | LC_ALL=C sort
echo
echo "--- [7] live custody verify via scratch copy of the tool ---"
cd $S/tool && python3 custody-pair.py capture --out $S/receipts/post.txt --label "cu1-post-install" ; echo "capture_exit=$?"
cd $S/tool && python3 custody-pair.py verify $S/receipts/pre.txt $S/receipts/post.txt --require-paths 5; echo "verify_pre_post_exit=$?"
cd $S/tool && python3 custody-pair.py verify $S/receipts/post.txt --live --require-paths 5; echo "verify_post_live_exit=$?"
echo
echo "=== CU-1 POST-INSTALL VERIFY END $(date -Is) ==="
