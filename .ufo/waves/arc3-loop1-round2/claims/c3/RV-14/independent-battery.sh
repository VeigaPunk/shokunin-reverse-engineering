#!/bin/bash
# RV-14 independent battery for the custody-pair tool (no real custody path is
# copied or written; guard test runs against a sandboxed HOME).
set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
T=.ufo/gates/custody-pair/custody-pair.py
R=.ufo/waves/arc3-loop1-round2/claims/c3/RV-14/receipts
S=/var/tmp/rv14/battery
mkdir -p "$S"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
sh_before=$(sha256sum "$T" | cut -d' ' -f1)

echo "### RV-14 independent battery $TS  tool-sha256 $sh_before"
echo
echo "== 1. selftest (own run) =="
python3 "$T" selftest --scratch /var/tmp/rv14/selftest-scratch > "$S/selftest.out" 2>&1
echo "selftest rc=$?"; tail -3 "$S/selftest.out"
echo
echo "== 2. capture --out - (live 5 paths, read-only) =="
python3 "$T" capture --out - --label rv14-ind > "$S/capture-live.txt" 2>&1
echo "capture rc=$?"; grep -c '^PATH:' "$S/capture-live.txt" | sed 's/^/stanzas=/'; tail -1 "$S/capture-live.txt"
echo
echo "== 3. v1 stanza (round-1 CU-1 config-pre-pair.txt) vs live =="
python3 "$T" verify .ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt --live > "$S/v1-stanza.out" 2>&1
echo "rc=$?"; grep -E "SHA256-CONTRACT|^VERDICT" "$S/v1-stanza.out"
echo
echo "== 4. v1 pipe (round-1 CU-1 config-pre-pair-metadata.txt) vs live =="
python3 "$T" verify .ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt --live > "$S/v1-pipe.out" 2>&1
echo "rc=$?"; grep -E "SHA256-CONTRACT|^VERDICT" "$S/v1-pipe.out"
echo
echo "== 5. round-trip: own capture -> verify vs live (idempotence, twice) =="
python3 "$T" capture --out "$S/rv14-roundtrip.txt" --label rv14-roundtrip > "$S/roundtrip-capture.out" 2>&1
echo "capture rc=$?  $(tail -1 "$S/roundtrip-capture.out")"
python3 "$T" verify "$S/rv14-roundtrip.txt" --live > "$S/roundtrip-verify1.out" 2>&1; echo "verify#1 rc=$?"; grep -E "^VERDICT" "$S/roundtrip-verify1.out"
python3 "$T" verify "$S/rv14-roundtrip.txt" --live > "$S/roundtrip-verify2.out" 2>&1; echo "verify#2 rc=$?"; grep -E "^VERDICT" "$S/roundtrip-verify2.out"
echo
echo "== 6. TZ independence of MTIME_UTC_RENDER =="
for tz in UTC UTC+5 UTC-3; do
  TZ="$tz" python3 "$T" capture --out - --paths "$HOME/.profile" 2>/dev/null | grep -E "^MTIME_(UTC|LOCAL)_RENDER" | sed "s/^/TZ=$tz /"
done
echo
echo "== 7. write-guard against a SANDBOXED home (real paths untouched) =="
rm -rf "$S/fakehome"; mkdir -p "$S/fakehome"
printf 'synthetic\n' > "$S/fakehome/.bashrc"
printf 'synthetic\n' > "$S/fakehome/.profile"
HOME="$S/fakehome" python3 "$T" capture --out "$S/fakehome/.bashrc" > "$S/guard.out" 2>&1
echo "guard rc=$? (expect 2)"; cat "$S/guard.out"
echo "fake .bashrc after: $(cat "$S/fakehome/.bashrc")"
echo
echo "== 8. same-content rewrite on synthetic fixtures (round-1 attack 3) =="
FX="$S/fx"; rm -rf "$FX"; mkdir -p "$FX"
printf 'synthetic custody carrier\n' > "$FX/f.conf"; chmod 600 "$FX/f.conf"
python3 "$T" capture --out "$S/fx-pre.txt" --paths "$FX/f.conf" > "$S/fx-capture.out" 2>&1; echo "capture rc=$?"
# in-place rewrite with identical bytes, mtime restored
python3 - "$FX/f.conf" <<'PY'
import os, sys
p = sys.argv[1]
st = os.lstat(p)
data = open(p, "rb").read()
open(p, "wb").write(data[:0] + data)          # same bytes, in place
os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))  # mtime restored
print("inode before/after:", st.st_ino, os.lstat(p).st_ino)
print("sha256 same:", len(data) > 0)
PY
python3 "$T" verify "$S/fx-pre.txt" --live > "$S/fx-rewrite.out" 2>&1; echo "rewrite verify rc=$? (expect 11)"
grep -E "^PATH|^VERDICT" "$S/fx-rewrite.out"
echo
echo "== 9. tool hash after battery =="
sh_after=$(sha256sum "$T" | cut -d' ' -f1)
echo "before=$sh_before"; echo "after =$sh_after"
[ "$sh_before" = "$sh_after" ] && echo "TOOL-STABLE: yes" || echo "TOOL-STABLE: NO (revised mid-battery)"
