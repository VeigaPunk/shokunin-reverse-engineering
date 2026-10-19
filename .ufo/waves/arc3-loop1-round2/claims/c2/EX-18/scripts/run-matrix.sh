#!/usr/bin/env bash
# EX-18 arc3-loop1-round2 — absent-PROVINCE.md control matrix.
# All scratch under /dev/shm; repo read-only. Usage: run-matrix.sh
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=/dev/shm/ex18-r2
CENSUS="$REPO/.ufo/gates/c1-census-v10.py"
CENSUS_H1="$R/census-h1-candidate.py"
S="$R/scratch"
L="$R/logs"
mkdir -p "$S" "$L"

fresh() {  # fresh() <dir> : copy the three scoped files from the repo
  rm -rf "$1"; mkdir -p "$1"
  cp "$REPO/PROVINCE.md" "$REPO/SKILL.md" "$REPO/SCORECARD.md" "$1/"
}

run() {  # run() <label> <instrument> <root>
  local lab="$1" instr="$2" root="$3"
  python3 "$instr" --root "$root" > "$L/$lab.out" 2>&1
  local rc=$?
  python3 "$instr" --root "$root" --json > "$L/$lab.json" 2>&1
  local rcj=$?
  { echo "=== $lab  instrument=$(sha256sum "$instr" | cut -c1-16)  root=$root"
    echo "--- text exit=$rc"; cat "$L/$lab.out"
    echo "--- json exit=$rcj"; python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
print(json.dumps({"verdict":d["verdict"],"counts":d["counts"],
 "stale":len(d["stale"]),"ambiguous":len(d["ambiguous"]),
 "undeclared":len(d["undeclared"]),"unresolved":len(d["unresolved"]),
 "scope_errors":d["scope_errors"],"g11":d["g11"],"g2_ok":d["g2_ok"],
 "live":d["live"]}))' "$L/$lab.json" 2>&1
  } > "$L/$lab.summary"
  echo "[$lab] exit=$rc json_exit=$rcj verdict=$(grep -o 'VERDICT: [A-Z]*' "$L/$lab.out" | head -1)"
}

echo "== sha256 identity at capture =="
sha256sum "$CENSUS" "$REPO/PROVINCE.md" "$REPO/SKILL.md" "$REPO/SCORECARD.md" | tee "$L/identity.txt"
git -C "$REPO" rev-parse HEAD | tee -a "$L/identity.txt"

echo "== B0 baseline: census at repo root (real tree) =="
python3 "$CENSUS" > "$L/B0.out" 2>&1; echo "B0 exit=$?" | tee "$L/B0.summary"

echo "== build H1 candidate from RV-11 patch text =="
python3 "$R/apply-h1.py" "$CENSUS" "$CENSUS_H1" > "$L/apply-h1.log" 2>&1
echo "apply rc=$?  ($(head -1 "$L/apply-h1.log"))"

echo "== S0 positive control: intact scratch root =="
fresh "$S/S0"; run S0 "$CENSUS" "$S/S0"

echo "== S1 injection: PROVINCE.md absent =="
fresh "$S/S1"; rm "$S/S1/PROVINCE.md"; run S1 "$CENSUS" "$S/S1"

echo "== S2 PROVINCE.md present but empty (0 bytes) =="
fresh "$S/S2"; : > "$S/S2/PROVINCE.md"; run S2 "$CENSUS" "$S/S2"

echo "== S3 PROVINCE.md truncated to 30 lines =="
fresh "$S/S3"; head -n 30 "$REPO/PROVINCE.md" > "$S/S3/PROVINCE.md"; run S3 "$CENSUS" "$S/S3"

echo "== S4 a DIRECTORY at PROVINCE.md =="
fresh "$S/S4"; rm "$S/S4/PROVINCE.md"; mkdir "$S/S4/PROVINCE.md"; run S4 "$CENSUS" "$S/S4"

echo "== S5 dangling symlink at PROVINCE.md =="
fresh "$S/S5"; rm "$S/S5/PROVINCE.md"; ln -s /dev/shm/ex18-r2/nonexistent "$S/S5/PROVINCE.md"; run S5 "$CENSUS" "$S/S5"

echo "== S6 contrast (H1 debt): SKILL.md absent =="
fresh "$S/S6"; rm "$S/S6/SKILL.md"; run S6 "$CENSUS" "$S/S6"

echo "== S7 contrast: SCORECARD.md absent =="
fresh "$S/S7"; rm "$S/S7/SCORECARD.md"; run S7 "$CENSUS" "$S/S7"

echo "== P0 H1 candidate, intact root (no-regression) =="
fresh "$S/P0"; run P0 "$CENSUS_H1" "$S/P0"

echo "== P1 H1 candidate, PROVINCE.md absent =="
fresh "$S/P1"; rm "$S/P1/PROVINCE.md"; run P1 "$CENSUS_H1" "$S/P1"

echo "== P2 H1 candidate, SKILL.md absent (debt closure) =="
fresh "$S/P2"; rm "$S/P2/SKILL.md"; run P2 "$CENSUS_H1" "$S/P2"

echo "== P3 H1 candidate, SCORECARD.md absent =="
fresh "$S/P3"; rm "$S/P3/SCORECARD.md"; run P3 "$CENSUS_H1" "$S/P3"

echo "== DONE =="
ls -la "$L"
