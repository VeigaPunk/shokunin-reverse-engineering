#!/usr/bin/env bash
# SC-4 (chain c2, arc3-loop1-round3): BEFORE-state injections against a SCRATCH
# COPY of the HEAD custody tool. No custody path is touched (captures use
# --paths over scratch files only; the canonical-5 write-guard case is exercised
# in a sandboxed fake HOME).
set -u
S=/var/tmp/sc4-r3
T=$S/before
rm -rf "$T"; mkdir -p "$T/home"
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
cp "$TOOL" "$S/tool-head.py"
chmod +x "$S/tool-head.py"
H(){ echo; echo "### $* ###"; }
run(){ echo "--- \$ custody-pair.py $*"; python3 "$S/tool-head.py" "$@" 2>&1; echo "--- exit=$?"; }

echo "tool-head.py sha256: $(sha256sum "$S/tool-head.py" | cut -d' ' -f1)"
echo "tool-head.py lines:  $(wc -l < "$S/tool-head.py")"

# ---------- fixture: one ordinary file, one EACCES file ----------
printf 'alpha\n' > "$T/home/plain.txt"
printf 'secret\n' > "$T/home/noread.txt"
chmod 000 "$T/home/noread.txt"

H "D2a: capture over an exists-but-EACCES path"
run capture --out "$T/d2a-receipt.txt" --paths "$T/home/noread.txt" --label "SC-4 before D2a"
echo "== receipt body =="; cat "$T/d2a-receipt.txt"

H "D2b: verify a receipt whose reference side recorded EXISTS: no (both sides absent)"
run capture --out "$T/d2b-receipt.txt" --paths "$T/home/never-existed.txt" --label "SC-4 before D2b"
run verify "$T/d2b-receipt.txt" "$T/d2b-receipt.txt"

H "D2c: --live against a readable-now / unreadable-at-verify candidate"
run capture --out "$T/d2c-receipt.txt" --paths "$T/home/noread.txt" --label "SC-4 before D2c (EACCES already)"
chmod 644 "$T/home/noread.txt"
run capture --out "$T/d2c-receipt.txt" --paths "$T/home/noread.txt" --label "SC-4 before D2c readable"
chmod 000 "$T/home/noread.txt"
run verify "$T/d2c-receipt.txt" --live

H "D3: 1-of-5 reference coverage"
run capture --out "$T/d3-receipt.txt" --paths "$T/home/plain.txt" --label "SC-4 before D3"
run verify "$T/d3-receipt.txt" "$T/d3-receipt.txt"
run verify "$T/d3-receipt.txt" --live

H "write-guard: canonical 5 (guarded) vs override path (unguarded)"
run capture --out "$HOME/.bashrc" --paths "$T/home/plain.txt" --label "SC-4 before write-guard canonical"
run capture --out "$T/home/plain.txt" --paths "$T/home/plain.txt" --label "SC-4 before write-guard override"
echo "== plain.txt after --paths X --out X =="; cat "$T/home/plain.txt"; echo "(end)"

H "D6: selftest with a missing scratch parent"
run selftest --scratch "$T/no/such/dir"

H "state"
ls -l "$T" | sed 's/^/  /'