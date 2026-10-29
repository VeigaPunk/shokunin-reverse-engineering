#!/usr/bin/env bash
# ExecCounterSelftest — offline frozen-instrument selftest runner (wave 3, round 50 attempt 2).
# Runs ONLY the four frozen round-50 instruments' offline selftests plus one
# calibration attack (a bogus --pkg65 pin). No REA run, no carrier fetch, no network.
# Every run is recorded with: exact argv, cwd, env overrides, UTC start/end,
# wall seconds, exit code, stdout/stderr sha256.
set -u

LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
T=$LANE/tools/round-50
S=/fast/scratch/hyaku/kaidoku-r50/w3-ExecCounterSelftest
PKG=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
export TMPDIR="$S"

mkdir -p "$S/runs" "$S/wk-c1" "$S/wk-ctrl" "$S/wk-c2" "$S/wk-49" "$S/wk-bogus"
cd "$S" || exit 2

RUNS_JSON="$S/runs.json"
: > "$RUNS_JSON.part"
echo '[' > "$RUNS_JSON.part"

first=1
run() {
  label="$1"; shift
  out="$S/runs/$label.out"; err="$S/runs/$label.err"
  t0=$(date -u +%Y-%m-%dT%H:%M:%SZ); s=$(date -u +%s.%N)
  nice -n 19 "$@" > "$out" 2> "$err"
  ec=$?; e=$(date -u +%s.%N)
  osha=$(sha256sum "$out" | cut -d' ' -f1); esha=$(sha256sum "$err" | cut -d' ' -f1)
  wall=$(python3 -c "print(round($e-$s,3))")
  if [ $first -eq 0 ]; then echo ',' >> "$RUNS_JSON.part"; fi; first=0
  python3 - "$RUNS_JSON.part" "$label" "$out" "$err" "$ec" "$t0" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$wall" "$osha" "$esha" "$S" "$@" <<'PY'
import json, os, sys
(part, label, out, err, ec, t0, t1, wall, osha, esha, cwd, *argv) = sys.argv[1:]
rec = {
    "label": label,
    "argv": ["python3", "-I", "-B"] + argv[1:] if False else argv,
    "cwd": cwd,
    "env_overrides": {"TMPDIR": "/fast/scratch/hyaku/kaidoku-r50/w3-ExecCounterSelftest"},
    "utc_start": t0,
    "utc_end": t1,
    "wall_sec": float(wall),
    "exit_code": int(ec),
    "stdout_sha256": osha,
    "stderr_sha256": esha,
    "stdout": os.path.relpath(out, cwd),
    "stderr": os.path.relpath(err, cwd),
}
with open(part, 'a') as fh:
    fh.write(json.dumps(rec))
PY
  printf '%-34s exit=%s wall=%ss utc=%s stdout_sha=%s\n' "$label" "$ec" "$wall" "$t0" "${osha:0:16}"
}

# --- as-dispatched spellings (from the seat dispatch text) -------------------
run dispatch-c2-record-selftest python3 -I -B "$T/c2-record.py" --selftest
run dispatch-r49-selftest-root python3 -I -B "$T/selftest-r49-c2.py" --root "$LANE"

# --- registry-pinned spellings (SKILL.md instrument-registry v2) ------------
run registry-c1-counter-selftest python3 -I -B "$T/c1-counter.py" --selftest --pkg65 "$PKG" --work "$S/wk-c1"
run registry-c1-controls-selftest python3 -I -B "$T/c1-controls.py" selftest --work "$S/wk-ctrl"
run registry-c2-record-selftest python3 -I -B "$T/c2-record.py" --selftest --root "$LANE" --work "$S/wk-c2"
run registry-r49-selftest python3 -I -B "$T/selftest-r49-c2.py" --lane "$LANE" --work "$S/wk-49"

# --- calibration attack: a bogus --pkg65 pin must NOT be green --------------
run attack-c1-counter-bogus-pkg65 python3 -I -B "$T/c1-counter.py" --selftest --pkg65 /nonexistent/pkg --work "$S/wk-bogus"

echo ']' >> "$RUNS_JSON.part"
mv "$RUNS_JSON.part" "$RUNS_JSON"
echo "wrote $RUNS_JSON"
