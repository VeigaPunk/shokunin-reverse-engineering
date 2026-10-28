#!/usr/bin/env bash
# Receipt runner: one line per (artifact, command, exit, stdout sha256, UTC).
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W1C1CounterMutants
cd "$S" || exit 2
export TMPDIR="$S" HYAKU_SCRATCH="$S"
: > receipts.tsv
printf 'label\texit\tstdout_sha256\tutc\tcommand\n' >> receipts.tsv

run() { # label, command...
  local label=$1; shift
  local t0 out err rc sha
  t0=$(date -u +%FT%TZ)
  out="$S/$label.out"; err="$S/$label.err"
  "$@" >"$out" 2>"$err"; rc=$?
  sha=$(sha256sum "$out" | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\n' "$label" "$rc" "$sha" "$t0" "$*" >> receipts.tsv
  cat "$err" >> receipts.tsv 2>/dev/null || true
}

run baseline            python3 -I -B "$S/pristine.py" --selftest
run m1-rule-blocks-ge   python3 -I -B "$S/m1-rule-blocks-ge.py" --selftest
run m2-skip-marker-check python3 -I -B "$S/m2-skip-marker-check.py" --selftest
run m3-any-exit-cell    python3 -I -B "$S/m3-any-exit-cell.py" --selftest
run m4-ignore-unresolved python3 -I -B "$S/m4-ignore-unresolved.py" --selftest
run m5-skip-selftest    python3 -I -B "$S/m5-skip-selftest.py" --selftest
run m6-drop-frozen-arm  python3 -I -B "$S/m6-drop-frozen-arm.py" --selftest
run probe-holes         python3 -I -B "$S/probe_holes.py"
cat receipts.tsv
echo "--- selftest lines ---"
grep -H 'C1_SELFTEST' baseline.out m*.out