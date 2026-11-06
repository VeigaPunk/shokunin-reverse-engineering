#!/bin/sh
# F2: --in FIFO with no writer -> open() blocks forever, process never exits.
set -e
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
D=$(mktemp -d); trap 'rm -rf -- "$D"' EXIT
git -C "$L" show a610671d7a01e1d762eb7103e6ee9f8a2be287ed:tools/round-100/upx-pe-repair.py > "$D/repair.py"
mkfifo "$D/in.fifo"
timeout 5 python3 -I -B "$D/repair.py" --in "$D/in.fifo" --out "$D/out.bin"
echo "rc=$? (observed: 124 = timeout kill; tool never exits on its own)"
