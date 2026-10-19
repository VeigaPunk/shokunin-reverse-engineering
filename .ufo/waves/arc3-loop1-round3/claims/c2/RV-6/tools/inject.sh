#!/usr/bin/env bash
# RV-6 D2 injection harness — same fixture + same commands per arm.
# usage: inject.sh <arm-name> <tool.py>
set -u
ARM="$1"; TOOL="$2"
FX=/var/tmp/rv6/fx
RUN=/var/tmp/rv6/runs/$ARM
rm -rf "$RUN"; mkdir -p "$RUN"

chmod 000 "$FX/blocked" "$FX/unreadable.conf"
echo "=== ARM $ARM  tool $TOOL ==="
echo "tool-sha256: $(sha256sum "$TOOL" | cut -d' ' -f1)"

echo "--- case1: capture of EACCES-at-lstat path (blocked dir) ---"
python3 "$TOOL" capture --out "$RUN/blocked-pre.txt" --paths "$FX/blocked/inner.conf" 2>&1
echo "case1-exit=$?"
if [ -f "$RUN/blocked-pre.txt" ]; then grep -E '^(EXISTS|STAT-ERROR|READ-ERROR|SHA256):' "$RUN/blocked-pre.txt"; fi

echo "--- case2: verify blocked-pre.txt --live (both sides EACCES) ---"
python3 "$TOOL" verify "$RUN/blocked-pre.txt" --live 2>&1
echo "case2-exit=$?"

echo "--- case2rr: receipt-vs-receipt, both captured while EACCES ---"
python3 "$TOOL" capture --out "$RUN/rr-b.txt" --paths "$FX/blocked/inner.conf" >/dev/null 2>&1
echo "case2rr-b-capture-exit=$?"
python3 "$TOOL" verify "$RUN/blocked-pre.txt" "$RUN/rr-b.txt" 2>&1
echo "case2rr-exit=$?"

echo "--- case3: capture while readable, then chmod 000, then verify --live ---"
chmod 644 "$FX/unreadable.conf"
python3 "$TOOL" capture --out "$RUN/unreadable-pre.txt" --paths "$FX/unreadable.conf" >/dev/null 2>&1
echo "case3-pre-exit=$?"
chmod 000 "$FX/unreadable.conf"
python3 "$TOOL" verify "$RUN/unreadable-pre.txt" --live 2>&1
echo "case3-exit=$?"

echo "--- case4: mixed capture good+unreadable (receipt survival) ---"
python3 "$TOOL" capture --out "$RUN/mixed.txt" --paths "$FX/good.conf" "$FX/unreadable.conf" 2>&1
echo "case4-exit=$?"
if [ -f "$RUN/mixed.txt" ]; then echo "receipt-exists=yes stanzas=$(grep -c '^PATH:' "$RUN/mixed.txt")"; grep -E '^(EXISTS|STAT-ERROR|READ-ERROR):' "$RUN/mixed.txt"; else echo "receipt-exists=no"; fi

chmod 755 "$FX/blocked"; chmod 644 "$FX/unreadable.conf"
echo "=== ARM $ARM done ==="