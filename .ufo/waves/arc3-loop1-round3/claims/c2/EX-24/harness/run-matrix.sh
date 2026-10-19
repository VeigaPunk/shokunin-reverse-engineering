#!/bin/bash
# EX-24 coverage-after harness. Usage: run-matrix.sh <tool.py> <phase-label>
# Reads only: tool file, scratch fixtures, and (for --live legs) the 5 custody
# paths via the tool's own read-only capture. Writes only under /var/tmp/ex24-after/<phase>/.
set +e
TOOL="$1"; PHASE="$2"
[ -z "$TOOL" ] && { echo "usage: run-matrix.sh <tool.py> <phase-label>"; exit 9; }
D=/var/tmp/ex24-after/$PHASE
mkdir -p "$D"
R=/var/tmp/ex24-after/matrix-root
rm -rf "$R"; mkdir -p "$R"
F=/var/tmp/ex24-after/fixtures/v1-partial-1of5.txt
{
echo "PHASE: $PHASE"
echo "TOOL: $TOOL"
echo "TOOL_SHA256: $(sha256sum "$TOOL" | awk '{print $1}')"
echo "DATE_UTC: $(date -u +%FT%TZ)"
echo "GIT_HEAD: $(git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD)"
echo "TARGET_SHA256_LIVE: $(sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py)"
echo "HELP_VERIFY:"
python3 "$TOOL" verify --help 2>&1 | sed 's/^/  /'
echo "HELP_SELFTEST:"
python3 "$TOOL" selftest --help 2>&1 | sed 's/^/  /'
} > "$D/00-tool-identity.out" 2>&1

run() { # run <name> <args...>
  local name="$1"; shift
  echo "### $name : custody-pair.py $* ###" >> "$D/matrix.out"
  python3 "$TOOL" "$@" > "$D/$name.out" 2>&1
  local rc=$?
  echo "EXIT=$rc" >> "$D/$name.out"
  echo "EXIT=$rc" >> "$D/matrix.out"
  cat "$D/$name.out" >> "$D/matrix.out"
  echo >> "$D/matrix.out"
}

# --- M4/M5: canonical 5/5 legs (live, read-only capture) ---
echo "### M4: canonical 5/5 capture (live) + verify vs live ###" >> "$D/matrix.out"
python3 "$TOOL" capture --out "$R/canon-pre.txt" --label "EX-24 matrix canonical" > "$D/M4a-capture.out" 2>&1
echo "EXIT=$?" >> "$D/M4a-capture.out"
python3 "$TOOL" capture --out "$R/canon-post.txt" --label "EX-24 matrix canonical post" > "$D/M4b-capture.out" 2>&1
echo "EXIT=$?" >> "$D/M4b-capture.out"
run M4c-canonical-pair verify "$R/canon-pre.txt" "$R/canon-post.txt"
run M4d-canonical-live verify "$R/canon-pre.txt" --live

# --- M1/M2: v1 1-of-5 receipt (EX-35 r2 fixture) ---
run M1-v1-1of5-live        verify "$F" --live
run M2-v1-1of5-reqpaths5   verify "$F" --live --require-paths 5

# --- M3: v2 1-of-5 receipt produced by the tool itself ---
mkdir -p "$R/one"
printf 'one-path scratch custody-like fixture\n' > "$R/one/f1.conf"
python3 "$TOOL" capture --out "$R/one/r1.txt" --paths "$R/one/f1.conf" --label "1of5 v2" > "$D/M3a-capture-1of5.out" 2>&1
echo "EXIT=$?" >> "$D/M3a-capture-1of5.out"
run M3b-v2-1of5-live        verify "$R/one/r1.txt" --live
run M3c-v2-1of5-reqpaths5   verify "$R/one/r1.txt" --live --require-paths 5

# --- M8/M9/M10: threshold legs (count vs identity; flag is a threshold) ---
mkdir -p "$R/five"
for i in 1 2 3 4 5; do printf 'five-path scratch fixture %s\n' "$i" > "$R/five/f$i.conf"; done
python3 "$TOOL" capture --out "$R/five/r5.txt" --label "5 scratch paths" \
  --paths "$R/five/f1.conf" "$R/five/f2.conf" "$R/five/f3.conf" "$R/five/f4.conf" "$R/five/f5.conf" \
  > "$D/M8a-capture-5of5-noncanonical.out" 2>&1
echo "EXIT=$?" >> "$D/M8a-capture-5of5-noncanonical.out"
run M8b-v2-5of5-noncanonical-reqpaths5 verify "$R/five/r5.txt" --live --require-paths 5
python3 "$TOOL" capture --out "$R/five/r4.txt" --label "4 scratch paths" \
  --paths "$R/five/f1.conf" "$R/five/f2.conf" "$R/five/f3.conf" "$R/five/f4.conf" \
  > "$D/M9a-capture-4of5.out" 2>&1
echo "EXIT=$?" >> "$D/M9a-capture-4of5.out"
run M9b-v2-4of5-reqpaths5 verify "$R/five/r4.txt" --live --require-paths 5
run M10-v1-1of5-reqpaths1 verify "$F" --live --require-paths 1
# alt flag spelling (SC-3's harness names both candidates)
run M11-v1-1of5-coveredefault verify "$F" --live --cover-default-paths
run M12-v2-1of5-coveredefault verify "$R/one/r1.txt" --live --cover-default-paths

# --- M13/M14: drift controls around the coverage gate ---
printf 'drifted bytes\n' > "$R/one/f1.conf"
run M13-covered-path-drift verify "$R/one/r1.txt" --live
run M13b-covered-path-drift-reqpaths5 verify "$R/one/r1.txt" --live --require-paths 5
printf 'sixth path six\n' > "$R/five/f6.conf"
python3 "$TOOL" capture --out "$R/five/r6.txt" --label "6 scratch paths" \
  --paths "$R/five/f1.conf" "$R/five/f2.conf" "$R/five/f3.conf" "$R/five/f4.conf" \
          "$R/five/f5.conf" "$R/five/f6.conf" > "$D/M14a-capture-6of6.out" 2>&1
echo "EXIT=$?" >> "$D/M14a-capture-6of6.out"
printf 'bystander drift\n' > "$R/five/f7.conf"
run M14b-six-path-under-5-name-set verify "$R/five/r6.txt" --live --require-paths 5

# --- M6: textual check — do the four unaccounted paths read as verified? ---
{
echo "### M6: unaccounted-path textual scan ###"
FOUR="/home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile"
for p in $FOUR; do
  for f in "$D"/M1-*.out "$D"/M2-*.out "$D"/M3b-*.out "$D"/M3c-*.out; do
    if grep -q -- "$p" "$f"; then echo "MENTIONED $p in $(basename $f): $(grep -- "$p" "$f" | head -2 | tr '\n' '|')"
    else echo "ABSENT-FROM-OUTPUT $p in $(basename $f)"; fi
  done
done
echo "--- any line claiming MATCH on the 1-of-5 legs ---"
grep -h "MATCH\|VERIFIED\|verified" "$D"/M1-*.out "$D"/M2-*.out "$D"/M3b-*.out "$D"/M3c-*.out
} > "$D/M6-unaccounted-scan.out" 2>&1

# --- M7: selftest, default scratch and explicit existing scratch ---
run M7a-selftest-default selftest
mkdir -p /var/tmp/ex24-after/scratch-m7
run M7b-selftest-explicit selftest --scratch /var/tmp/ex24-after/scratch-m7
run M7c-selftest-missing selftest --scratch /var/tmp/ex24-after/does-not-exist-ex24

echo "MATRIX DONE: $PHASE" >> "$D/matrix.out"
exit 0