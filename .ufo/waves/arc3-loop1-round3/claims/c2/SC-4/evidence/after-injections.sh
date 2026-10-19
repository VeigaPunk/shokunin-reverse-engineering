#!/usr/bin/env bash
# SC-4 (chain c2, arc3-loop1-round3): AFTER-state injection harness for the
# REVISED custody tool. Runs against a scratch COPY of whatever revision is in
# the repo at run time; names that revision in the output. Scratch fixtures
# only — the canonical write-guard aim is refused by design before any write.
set -u
S=/var/tmp/sc4-r3
T=$S/after
rm -rf "$T"; mkdir -p "$T/home" "$T/bin"
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
# keep the tool's own basename: some selftest cases re-invoke it by name
cp "$REPO/.ufo/gates/custody-pair/custody-pair.py" "$T/bin/custody-pair.py"
chmod +x "$T/bin/custody-pair.py"
SHA=$(sha256sum "$T/bin/custody-pair.py" | cut -d' ' -f1)
LINES=$(wc -l < "$T/bin/custody-pair.py")
echo "== AFTER harness =="
echo "tool-after.py sha256=$SHA lines=$LINES"
echo "captured-utc $(date -u +%Y-%m-%dT%H:%M:%SZ)"
H(){ echo; echo "### $* ###"; }
run(){ echo "--- \$ custody-pair.py $*"; (cd "$T/bin" && python3 "$T/bin/custody-pair.py" "$@") 2>&1; echo "--- exit=$?"; }

printf 'alpha\n' > "$T/home/plain.txt"
printf 'secret\n' > "$T/home/noread.txt"; chmod 000 "$T/home/noread.txt"
mkdir -p "$T/home/locked"; printf 'hidden\n' > "$T/home/locked/f.txt"; chmod 000 "$T/home/locked"

H "A-D2a: capture over an exists-but-EACCES file"
run capture --out "$T/d2a-receipt.txt" --paths "$T/home/noread.txt" --label "SC-4 after D2a"
[ -f "$T/d2a-receipt.txt" ] && grep -E "PATH|EXISTS|READ-ERROR|STAT-ERROR|SHA256" "$T/d2a-receipt.txt"

H "A-D2b: verify that receipt vs itself and vs live (fail-open check)"
run verify "$T/d2a-receipt.txt" "$T/d2a-receipt.txt"
run verify "$T/d2a-receipt.txt" --live

H "A-D2-stat: path inside an EACCES dir"
run capture --out "$T/d2stat-receipt.txt" --paths "$T/home/locked/f.txt" --label "SC-4 after D2stat"
[ -f "$T/d2stat-receipt.txt" ] && grep -E "PATH|EXISTS|READ-ERROR|STAT-ERROR" "$T/d2stat-receipt.txt"
run verify "$T/d2stat-receipt.txt" --live

H "A-D2c: --live against a candidate that became unreadable"
chmod 644 "$T/home/noread.txt"
run capture --out "$T/d2c-receipt.txt" --paths "$T/home/noread.txt" --label "SC-4 after D2c readable"
chmod 000 "$T/home/noread.txt"
run verify "$T/d2c-receipt.txt" --live

H "A-D3: reference coverage (1 of the canonical 5) — plain and --require-paths"
run capture --out "$T/d3-receipt.txt" --paths "$T/home/plain.txt" --label "SC-4 after D3"
run verify "$T/d3-receipt.txt" --live
run verify "$T/d3-receipt.txt" --live --require-paths 5

H "A-WG: write-guard scope (canonical aim, override --paths X --out X, hardlink alias)"
run capture --out "$HOME/.bashrc" --paths "$T/home/plain.txt" --label "SC-4 after WG canonical"
run capture --out "$T/home/plain.txt" --paths "$T/home/plain.txt" --label "SC-4 after WG override"
echo "== plain.txt after --paths X --out X (first line) =="; head -1 "$T/home/plain.txt"
ln -f "$HOME/.profile" "$T/home/alias-profile" 2>/dev/null && run capture --out "$T/home/alias-profile" --paths "$T/home/plain.txt" --label "SC-4 after WG hardlink"

H "A-D6: selftest with a missing scratch parent"
run selftest --scratch "$T/no/such/dir"

H "A-selftest: ordinary scratch run"
run selftest --scratch /dev/shm

H "A-header: receipt self-pin line"
run capture --out "$T/header-receipt.txt" --paths "$T/home/plain.txt" --label "SC-4 after header"
grep -E "^# tool:|^# receipt-version:|^# captured-utc:" "$T/header-receipt.txt" 2>/dev/null

H "A-pair: revised tool verifies the round pre-pair receipt vs live"
run verify "$REPO/.ufo/waves/arc3-loop1-round3/claims/c2/receipts/config-pre-pair-v2r3.txt" --live

H "A-v1: v1 receipts remain sha256-verifiable (round-1 stanza + pipe shapes)"
run verify "$REPO/.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt" --live
run verify "$REPO/.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt" --live

H "A-r2pair: r2 pre-pair vs r3 pre-pair (in-window drift statement)"
run verify "$REPO/.ufo/waves/arc3-loop1-round2/claims/c3/receipts/config-pre-pair-v2.txt" "$REPO/.ufo/waves/arc3-loop1-round3/claims/c2/receipts/config-pre-pair-v2r3.txt"

chmod 755 "$T/home/locked"