#!/bin/bash
# EX-46 post-landing battery: run once EX-41 has written the real artifact pair.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
C=/var/tmp/ex46/post; mkdir -p "$C"
cd "$R"
{
  echo "== timestamp =="; date -u +%FT%TZ
  echo "== landed bytes =="; sha256sum .ufo/gates/citation-drift/pointer-table.json .ufo/gates/citation-drift/expected.json .ufo/gates/citation-drift/citation-drift-probe.py .ufo/gates/c1-census-v10.py
  stat -c '%n %s %Y %i' .ufo/gates/citation-drift/pointer-table.json .ufo/gates/citation-drift/expected.json
  echo "== entries count =="; python3 -c "import json;t=json.load(open('.ufo/gates/citation-drift/pointer-table.json'));print('entries',len(t['entries']),'quoted',len(t['quoted']),'exempt',len(t['exempt']))"
} > "$C/landed-identity.txt" 2>&1
TMPDIR=/var/tmp/ex46 python3 .ufo/gates/c1-census-v10.py --root "$R" > "$C/census-post.txt" 2>&1; echo "census_exit=$?" >> "$C/census-post.txt"
TMPDIR=/var/tmp/ex46 python3 .ufo/gates/c1-census-v10.py --root "$R" --json > "$C/census-post.json" 2>&1; echo "json_exit=$?" >> "$C/census-post.json"
TMPDIR=/var/tmp/ex46 python3 .ufo/gates/citation-drift/citation-drift-probe.py --root "$R" > "$C/probe-post-default.txt" 2>&1; echo "exit=$?" >> "$C/probe-post-default.txt"
TMPDIR=/var/tmp/ex46 python3 .ufo/gates/citation-drift/citation-drift-probe.py --root "$R" --strict > "$C/probe-post-strict.txt" 2>&1; echo "exit=$?" >> "$C/probe-post-strict.txt"
TMPDIR=/var/tmp/ex46 python3 .ufo/gates/citation-drift/citation-drift-probe.py --root "$R" --selftest > "$C/selftest-post.txt" 2>&1; echo "exit=$?" >> "$C/selftest-post.txt"
python3 .ufo/waves/arc3-loop1-round3/claims/c3/EX-46/pin-check.py > "$C/pin-check-post.txt" 2>&1; echo "exit=$?" >> "$C/pin-check-post.txt"
# command A at HEAD (git objects unchanged by seat writes; fresh execution)
bash /var/tmp/ex46/scratch/commandA.sh "$R" HEAD > "$C/commandA-HEAD-post.txt" 2>&1
# census byte-comparison vs baseline
grep -v '^census_exit=' /var/tmp/ex46/baseline/census-default.txt > "$C/baseline-census-stripped.txt"
if diff "$C/baseline-census-stripped.txt" <(grep -v '^census_exit=' "$C/census-post.txt") > "$C/census-diff.txt" 2>&1; then
  echo "CENSUS_BYTE_IDENTICAL_ACROSS_LANDING" >> "$C/census-diff.txt"
fi
# command A comparison vs baseline (mask revision)
python3 - "$C/commandA-HEAD-post.txt" > "$C/commandA-compare.txt" 2>&1 <<'PY'
import json,sys
a=json.loads(open('/var/tmp/ex46/baseline/commandA-HEAD.txt').read())
b=json.loads(open(sys.argv[1]).read().splitlines()[0])
print("baseline:", json.dumps(a,sort_keys=True))
print("post    :", json.dumps(b,sort_keys=True))
a.pop('revision'); b.pop('revision')
print("COMMAND_A_EQUAL_MODULO_REVISION:", a==b)
PY
echo POST_BATTERY_DONE
