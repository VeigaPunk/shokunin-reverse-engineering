#!/usr/bin/env bash
# EX-24 (chain c3, arc3-loop1-round4) — run the mkdir injection matrix.
#
# Usage: run-legs.sh <revision-tag> <tool-path> <outdir>
#   e.g. run-legs.sh before /var/tmp/ex24-r4/bin/custody-pair.py <claims>/before
#
# Every leg runs on scratch under /var/tmp. Custody paths are never touched:
# every capture is scoped with --paths to scratch fixtures.
set -uo pipefail

TAG="${1:?tag}"; TOOL="${2:?tool}"; OUT="${3:?outdir}"
mkdir -p "$OUT" "$OUT/logs"
S=/var/tmp/ex24-r4/legs/$TAG
rm -rf "$S"; mkdir -p "$S"
cd "$S"

printf 'x\n' > "$S/regfile"                    # a regular file used as a parent component
printf 'a\n' > "$S/measured.conf"              # a scoped fixture
mkdir -p "$S/ro"; chmod 500 "$S/ro"            # EACCES arm: read-only parent
mkdir -p "$S/deep"; printf 'd\n' > "$S/deep/f.conf"

row() { # name, exit, then a one-line classifier
  printf '%-26s exit=%-3s %s\n' "$1" "$2" "$3"
}

# L1 — parent COMPONENT is a regular file
python3 "$TOOL" capture --paths "$S/measured.conf" --out "$S/regfile/sub/r.txt" > "$OUT/logs/L1.out" 2>&1
e=$?; tb=$(grep -c '^Traceback' "$OUT/logs/L1.out")
row L1-parent-is-regular-file "$e" "traceback=$tb  $(grep -m1 -o 'USAGE: [^(]*' "$OUT/logs/L1.out" || true)"
cp "$S/regfile" "$OUT/logs/L1.regfile-after" 2>/dev/null || true

# L2 — --out is itself an existing regular file
python3 "$TOOL" capture --paths "$S/measured.conf" --out "$S/regfile" > "$OUT/logs/L2.out" 2>&1
e=$?; tb=$(grep -c '^Traceback' "$OUT/logs/L2.out")
row L2-out-is-existing-file "$e" "traceback=$tb  $(grep -m1 -o 'USAGE: [^(]*' "$OUT/logs/L2.out" || true)"
sha256sum "$S/regfile" > "$OUT/logs/L2.regfile-after.sha256"

# L3 — parent dir not writable (EACCES)
python3 "$TOOL" capture --paths "$S/measured.conf" --out "$S/ro/deep/r.txt" > "$OUT/logs/L3.out" 2>&1
e=$?; tb=$(grep -c '^Traceback' "$OUT/logs/L3.out")
row L3-parent-unwritable "$e" "traceback=$tb  $(grep -m1 -o 'USAGE: [^(]*' "$OUT/logs/L3.out" || true)"

# L4 — control: parent dir absent but creatable -> mkdir still happens, exit declared
python3 "$TOOL" capture --paths "$S/measured.conf" --out "$S/newdir/sub/r.txt" > "$OUT/logs/L4.out" 2>&1
e=$?; tb=$(grep -c '^Traceback' "$OUT/logs/L4.out")
row L4-fresh-parent-created "$e" "traceback=$tb  $(grep -m1 -o 'CUSTODY_PAIR_CAPTURE: [^ ]* paths=[0-9/]*' "$OUT/logs/L4.out" || true)"

# L5 — regression: guard still refuses --out over a scoped path (exit 2)
python3 "$TOOL" capture --paths "$S/measured.conf" --out "$S/measured.conf" > "$OUT/logs/L5.out" 2>&1
e=$?; tb=$(grep -c '^Traceback' "$OUT/logs/L5.out")
row L5-guard-scoped-out "$e" "traceback=$tb  $(grep -m1 -o 'USAGE: refusing[^(]*' "$OUT/logs/L5.out" || true)"

# L6 — regression: normal capture to a fresh file in an existing dir
python3 "$TOOL" capture --paths "$S/measured.conf" --out "$S/ok.txt" > "$OUT/logs/L6.out" 2>&1
e=$?; tb=$(grep -c '^Traceback' "$OUT/logs/L6.out")
row L6-normal-capture "$e" "traceback=$tb  $(grep -m1 -o 'CUSTODY_PAIR_CAPTURE: [^ ]* paths=[0-9/]*' "$OUT/logs/L6.out" || true)"

# L7 — regression: stdout mode unaffected
python3 "$TOOL" capture --paths "$S/measured.conf" --out - > "$OUT/logs/L7.out" 2>&1
e=$?; tb=$(grep -c '^Traceback' "$OUT/logs/L7.out")
row L7-stdout-mode "$e" "traceback=$tb  $(grep -m1 -o 'CUSTODY_PAIR_CAPTURE: [^ ]* paths=[0-9/]*' "$OUT/logs/L7.out" || true)"

# L8 — regression: --out '' (empty) stays USAGE
python3 "$TOOL" capture --paths "$S/measured.conf" --out "" > "$OUT/logs/L8.out" 2>&1
e=$?; tb=$(grep -c '^Traceback' "$OUT/logs/L8.out")
row L8-empty-out "$e" "traceback=$tb  $(grep -m1 -o 'USAGE: [^(]*' "$OUT/logs/L8.out" || true)"

# L9 — verify --live over the L6 receipt (the declared live-pair shape)
python3 "$TOOL" verify "$S/ok.txt" --live > "$OUT/logs/L9.out" 2>&1
e=$?; row L9-verify-live "$e" "$(grep -m1 -o 'VERDICT: [A-Z-]* paths=[0-9/]*' "$OUT/logs/L9.out" || true)"

# L10 — verify receipt-vs-receipt
python3 "$TOOL" capture --paths "$S/measured.conf" --out "$S/ok2.txt" > /dev/null 2>&1
python3 "$TOOL" verify "$S/ok.txt" "$S/ok2.txt" > "$OUT/logs/L10.out" 2>&1
e=$?; row L10-verify-pair "$e" "$(grep -m1 -o 'VERDICT: [A-Z-]* paths=[0-9/]*' "$OUT/logs/L10.out" || true)"

# L11 — selftest (fixture root under /var/tmp)
mkdir -p /var/tmp/ex24-r4/selftest-scratch
python3 "$TOOL" selftest --scratch /var/tmp/ex24-r4/selftest-scratch > "$OUT/logs/L11-selftest.out" 2>&1
e=$?; row L11-selftest "$e" "$(grep -m1 -o 'CUSTODY_PAIR_SELFTEST: [A-Z]* cases=[0-9]* passed=[0-9]* failed=[0-9]*' "$OUT/logs/L11-selftest.out" || true)"

# L12 — selftest --scratch missing (D6 regression)
python3 "$TOOL" selftest --scratch /var/tmp/ex24-r4/nope-missing > "$OUT/logs/L12.out" 2>&1
e=$?; row L12-selftest-missing-scratch "$e" "$(grep -m1 -o 'USAGE: [^:]*: [^ ]*' "$OUT/logs/L12.out" || true)"

# L13 — --paths X --out X.sha256 : the r3 sidecar residual, unchanged by this injection
printf 'v\n' > "$S/vic.sha256"; cp "$S/vic.sha256" "$OUT/logs/L13-vic-pre"
python3 "$TOOL" capture --paths "$S/vic.sha256" --out "$S/vic" > "$OUT/logs/L13.out" 2>&1
e=$?; row L13-sidecar-path-residual "$e" "sidecar-clobbered=$([ "$(cat "$S/vic.sha256")" != v ] && echo yes || echo no)"

chmod 700 "$S/ro" 2>/dev/null || true
echo "--- tool: $TOOL  sha256=$(sha256sum "$TOOL" | cut -d' ' -f1)"
