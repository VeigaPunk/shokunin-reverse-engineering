#!/bin/bash
# RV-9 extended attacks (harness2) against the revised custody-pair tool.
# usage: harness2.sh TOOL OUTDIR SCRATCH
set -u
TOOL="$1"; OUT="$2"; SCR="$3"
mkdir -p "$OUT" "$SCR"
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin || exit 3

hdr() { echo "----- $1" | tee -a "$OUT/harness2.log"; }

hdr "B0 pin"; sha256sum "$TOOL" | tee -a "$OUT/harness2.log"

hdr "B1 hardlink alias write-guard (D7-shape)"
echo alpha > "$SCR/hl-src.txt"; ln -f "$SCR/hl-src.txt" "$SCR/hl-alias.txt"
python3 "$TOOL" capture --paths "$SCR/hl-src.txt" --out "$SCR/hl-alias.txt" > "$OUT/B1-hardlink-guard.out" 2>&1
echo "rc=$? (expect 2)" | tee -a "$OUT/harness2.log"; tail -1 "$OUT/B1-hardlink-guard.out" | tee -a "$OUT/harness2.log"
echo "content-after: $(head -c 40 "$SCR/hl-src.txt")"

hdr "B2 require-paths gate on EX-35 1-of-5 fixture"
F=.ufo/waves/arc3-loop1-round2/claims/c3/EX-35/fixtures/v1-partial-1of5.txt
python3 "$TOOL" verify --require-paths 5 "$F" --live > "$OUT/B2-require5.out" 2>&1; echo "rc=$? (expect 2)" | tee -a "$OUT/harness2.log"; tail -2 "$OUT/B2-require5.out" | tee -a "$OUT/harness2.log"
python3 "$TOOL" verify "$F" --live > "$OUT/B2b-noflag.out" 2>&1; echo "rc=$? (no flag: record)" | tee -a "$OUT/harness2.log"; tail -2 "$OUT/B2b-noflag.out" | tee -a "$OUT/harness2.log"
python3 "$TOOL" verify --require-paths 1 "$F" --live > "$OUT/B2c-require1.out" 2>&1; echo "rc=$? (expect 0)" | tee -a "$OUT/harness2.log"; tail -1 "$OUT/B2c-require1.out" | tee -a "$OUT/harness2.log"

hdr "B3 UNEVALUABLE receipt: format tag + unusable-as-anchor"
mkdir -p "$SCR/unev" && echo x > "$SCR/unev/u.conf" && chmod 000 "$SCR/unev/u.conf"
python3 "$TOOL" capture --paths "$SCR/unev/u.conf" --out "$SCR/unev/u-rcpt.txt" > "$OUT/B3a-capture-unev.out" 2>&1; echo "rc=$? (expect 14)" | tee -a "$OUT/harness2.log"; tail -1 "$OUT/B3a-capture-unev.out" | tee -a "$OUT/harness2.log"
python3 "$TOOL" verify "$SCR/unev/u-rcpt.txt" "$SCR/unev/u-rcpt.txt" > "$OUT/B3b-self-verify.out" 2>&1; echo "rc=$? (expect 14)" | tee -a "$OUT/harness2.log"; head -2 "$OUT/B3b-self-verify.out" | tee -a "$OUT/harness2.log"; tail -1 "$OUT/B3b-self-verify.out" | tee -a "$OUT/harness2.log"
chmod 600 "$SCR/unev/u.conf"
python3 "$TOOL" verify "$SCR/unev/u-rcpt.txt" --live > "$OUT/B3c-unev-vs-live.out" 2>&1; echo "rc=$? (after chmod back: record)" | tee -a "$OUT/harness2.log"; tail -2 "$OUT/B3c-unev-vs-live.out" | tee -a "$OUT/harness2.log"

hdr "B4 declared exit map + classes list"
grep -n "UNEVALUABLE\|READ-ERROR\|STAT-ERROR" "$TOOL" | head -8 | tee -a "$OUT/harness2.log"

hdr "B5 selftest case inventory"
mkdir -p "$SCR/st"
python3 "$TOOL" selftest --scratch "$SCR/st" 2>&1 | grep -E "^case |^CUSTODY_PAIR_SELFTEST" | tee "$OUT/B5-selftest-cases.out" | tail -25 | tee -a "$OUT/harness2.log"
echo "HARNESS2 DONE" | tee -a "$OUT/harness2.log"