#!/bin/bash
# SentinelRepair probe D: read_input cap boundary (scratch only).
set -u
S=/fast/scratch/hyaku/kaidoku-r92/SentinelRepair
C=$S/clone/tools/round-91/upx-stop-boundary-repair.py
W=$S/work/d
mkdir -p "$W" "$S/logs"
L=$S/logs/probe_d.log
CAP=268435456   # MAX_INPUT = 256 << 20
{
echo "MAX_INPUT literal: $(python3 -c 'print(256 << 20)')"

echo "== D1 at cap+1 (sparse): expect typed refusal before any read"
truncate -s $((CAP + 1)) "$W/at-cap-plus-1"
ls -l "$W/at-cap-plus-1" | awk '{print "size:", $5}'
TMPDIR=$S/tmp HOME=$S/tmp python3 -I -B "$C" --in "$W/at-cap-plus-1" --out "$W/out1" >"$W/o1" 2>&1
echo "rc=$?"; cat "$W/o1"
echo "out1 exists: $([ -e "$W/out1" ] && echo yes || echo no)"

echo "== D2 at cap exactly (sparse, non-ELF zeros): reads fully, refuses as non-ELF"
truncate -s "$CAP" "$W/at-cap"
/usr/bin/time -f "read-wall=%es max-rss=%MkB" env TMPDIR=$S/tmp HOME=$S/tmp \
  python3 -I -B "$C" --in "$W/at-cap" --out "$W/out2" >"$W/o2" 2>"$W/e2"
echo "rc=$?"; cat "$W/o2"; cat "$W/e2"

echo "== D3 input is a directory: S_ISREG guard"
TMPDIR=$S/tmp HOME=$S/tmp python3 -I -B "$C" --in "$W" --out "$W/out3" >"$W/o3" 2>&1
echo "rc=$?"; cat "$W/o3"

echo "== D4 input is a symlink to a regular file (lstat sees the link)"
printf 'x' > "$W/real-target"
ln -s "$W/real-target" "$W/link-in"
TMPDIR=$S/tmp HOME=$S/tmp python3 -I -B "$C" --in "$W/link-in" --out "$W/out4" >"$W/o4" 2>&1
echo "rc=$?"; cat "$W/o4"

echo "== D5 missing input"
TMPDIR=$S/tmp HOME=$S/tmp python3 -I -B "$C" --in "$W/nope" --out "$W/out5" >"$W/o5" 2>&1
echo "rc=$?"; cat "$W/o5"
} 2>&1 | tee "$L"
echo "LOG=$L"
