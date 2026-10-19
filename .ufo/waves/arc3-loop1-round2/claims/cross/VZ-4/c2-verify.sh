#!/usr/bin/env bash
# VZ-4 C2 fail-closure harness. Usage: c2-verify.sh <census.py> <label>
# Runs a census instrument against the round-1 silent-PASS fixtures and a
# locally-neutered "blind instrument" variant; records verdict+exit per case.
set -u
CENSUS="${1:?usage: c2-verify.sh <census.py> <label>}"
LABEL="${2:?usage: c2-verify.sh <census.py> <label>}"
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
FIX="$REPO/.ufo/waves/arc3-loop1-round1/claims/c3/RV-11/scratch"
WORK=/var/tmp/vz4/c2/$LABEL
mkdir -p "$WORK"
echo "census=$CENSUS"
echo "census_sha256=$(sha256sum "$CENSUS" | cut -d' ' -f1)"
echo "label=$LABEL  utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

run_case() {
  local name="$1" root="$2" script="$3"
  local out rc verdict
  out=$(python3 "$script" --root "$root" --quiet 2>&1); rc=$?
  verdict=$(printf '%s\n' "$out" | grep -E '^VERDICT:' | tail -1)
  printf '%-22s exit=%-3s %s\n' "$name" "$rc" "${verdict:-<no verdict line>}"
  printf '%s\n' "$out" > "$WORK/$name.out"
  printf 'exit=%s\n' "$rc" > "$WORK/$name.exit"
  printf '%s\n' "$out" | grep -E '^(UNREADABLE|SCOPE-ERRORS|G2 |G6 |G15 |G18 )' | sed 's/^/    /'
}

echo "--- A. real instrument, HEAD root (expect PASS 0/0/0/0, exit 0) ---"
run_case head-parity "$REPO" "$CENSUS"
echo
echo "--- B. round-1 silent-PASS / fail-closed fixtures (expect all FAIL after fix) ---"
for f in atk-missing atk-undecl atk-silent atk-no-province atk-no-scorecard atk-empty; do
  case "$f" in
    atk-missing|atk-no-province|atk-no-scorecard)
      # these fixtures are partial roots: only the named files exist there; the
      # census resolves absent scoped files via its own read path
      root="$FIX/$f" ;;
    *) root="$FIX/$f" ;;
  esac
  [ -d "$root" ] && run_case "$f" "$root" "$CENSUS" || echo "$f: fixture dir absent"
done
echo
echo "--- C. blind-instrument variant (needles neutered) over HEAD root (expect FAIL after fix) ---"
BLIND="$WORK/census-blind-variant.py"
python3 - "$CENSUS" "$BLIND" <<'PY'
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
subs = [
 (r'PIN = re\.compile\(r"[^"]*"', 'PIN = re.compile(r"(?!)"'),
 (r'VER = re\.compile\(r"[^"]*"', 'VER = re.compile(r"(?!)"'),
 (r'PTR = re\.compile\(r"[^"]*"', 'PTR = re.compile(r"(?!)"'),
]
n = 0
for pat, rep in subs:
    src, k = re.subn(pat, rep, src, count=1)
    n += k
open(sys.argv[2], "w", encoding="utf-8").write(src)
print("needles_neutered=%d/3" % n)
PY
run_case blind-variant "$REPO" "$BLIND"
echo
echo "--- D. scope-diff vs pinned round-1 baselines (creep audit) ---"
BASE1=/var/tmp/vz4/baseline-census-14b1682.py
if [ -f "$BASE1" ]; then
  echo "[D1] before = round-1-committed census (HEAD 14b1682, sha 6f1d19ff...)"
  python3 "$REPO/.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py" \
    "$BASE1" "$CENSUS" 2>&1 | tail -6
else
  echo "[D1] baseline copy $BASE1 absent"
fi
if [ "$CENSUS" != "$BASE1" ]; then
  echo "[D2] before = v10 pre-E22-disposition (round-1 CR-5 census-before.py, sha 36e96cd5...)"
  python3 "$REPO/.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py" \
    "$REPO/.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/census-before.py" "$CENSUS" 2>&1 | tail -6
fi
