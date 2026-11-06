#!/bin/sh
# F1: --in /dev/zero -> unbounded fh.read() -> uncaught MemoryError (rc=1, traceback).
# Run with a VA cap so the host survives; without a cap it eats all RAM (OOM kill).
set -e
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
D=$(mktemp -d); trap 'rm -rf -- "$D"' EXIT
git -C "$L" show a610671d7a01e1d762eb7103e6ee9f8a2be287ed:tools/round-100/upx-pe-repair.py > "$D/repair.py"
( ulimit -v 4194304; exec python3 -I -B "$D/repair.py" --in /dev/zero --out "$D/out.bin" )
echo "rc=$? (observed: 1, 'MemoryError' traceback at line 188 data = fh.read())"
