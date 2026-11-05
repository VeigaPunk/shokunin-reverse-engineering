#!/bin/bash
# SentinelInputs reproducers for the two violations (run in a scratch dir; needs /usr/bin/prlimit, timeout).
# T is the repair tool at Bk (c19d57cd2e65a036478b9e78f6c5397dedfb2bcb); P is a UPX 5.2.0 pack of t32.exe.
set -u
T="${T:?set T to the path of upx-pe-repair.py at c19d57cd}"
P="${P:?set P to a UPX-packed PE (e.g. upx --best -o t32.upx t32.exe)}"
S="$(mktemp -d)"; trap 'rm -rf -- "$S"' EXIT; cd "$S"
mkfifo in.fifo
timeout 5 python3 -I -B "$T" --in in.fifo --out out.bin; echo "V1 fifo-no-writer rc=$? (124 = hang killed)"
prlimit --as=1073741824 --cpu=15 timeout 30 python3 -I -B "$T" --in /dev/zero --out z.bin 2>err.txt; echo "V2 devzero-capped rc=$?"; tail -n 1 err.txt
