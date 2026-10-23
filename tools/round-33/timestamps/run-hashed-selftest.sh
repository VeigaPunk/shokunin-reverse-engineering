#!/usr/bin/env bash
# Selftest for the hash-bound allowance wrapper, on bounded scratch clones only.
# Cases: green known-line echo, red same-line inserted future execution, red unlisted future.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
WRAP=$HERE/run-gate-hashed.py
SPEC=$HERE/allowances-hashed.json
FIX=${HASHED_FIXTURE_BASE:-$HERE/hashed-fixture}
RUNS=$HERE/hashed-selftest-runs
SCOPE=.ufo/waves/round-32
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
FAILS=0

bash "$HERE/build-hashed-fixture.sh" || { echo "HASHED_SELFTEST: FAILED fixture_build"; exit 1; }
rm -rf "$RUNS"; mkdir -p "$RUNS"

run_case() {
  local name=$1 root=$2
  local out=$RUNS/$name; mkdir -p "$out"
  local start end rc
  start=$(date -u +%FT%TZ)
  timeout 120 python3 -I -B "$WRAP" --root "$root" --rev HEAD --path "$SCOPE" --spec "$SPEC" --out "$out" \
    >"$out/wrapper.stdout" 2>"$out/wrapper.stderr"
  rc=$?
  end=$(date -u +%FT%TZ)
  printf '%s\n' "$rc" >"$out/exit.txt"
  printf 'utc_start=%s\ncase=%s\nexit=%s\nutc_end=%s\nroot=%s\n' "$start" "$name" "$rc" "$end" "$root" >"$out/case.txt"
}

check() {
  local name=$1 program=$2
  if python3 -I -B - "$RUNS/$name" <<<"$program"; then
    echo "PASS $name"
  else
    echo "FAIL $name"
    FAILS=$((FAILS + 1))
  fi
}

run_case green "$FIX/clone-green"
check green "$(cat <<'PY'
import json, sys
out = sys.argv[1]
payload = json.load(open(out + "/stdout.json"))
rc = int(open(out + "/exit.txt").read())
ok = (rc == 0 and payload["summary"]["finding_count"] == 6
      and payload["summary"]["unexempted_finding_count"] == 0
      and len(payload["allow"]) == 5 and all(a["applied"] for a in payload["allow"]))
print(f"green exit={rc} findings={payload['summary']['finding_count']} "
      f"unexempted={payload['summary']['unexempted_finding_count']} "
      f"applied={[a['applied'] for a in payload['allow']]}")
sys.exit(0 if ok else 1)
PY
)"

run_case sameline "$FIX/clone-sameline"
check sameline "$(cat <<'PY'
import json, sys
out = sys.argv[1]
payload = json.load(open(out + "/stdout.json"))
rc = int(open(out + "/exit.txt").read())
err = payload.get("error", {})
ok = (rc == 1 and err.get("code") == "allowance_line_changed"
      and payload.get("tool_run") is False and "findings" not in payload
      and err.get("file") == "a2after/timestamps-strict-at-9ef97f08.txt" and err.get("line") == 3)
print(f"sameline exit={rc} code={err.get('code')} tool_run={payload.get('tool_run')} "
      f"actual={str(err.get('actual_sha256'))[:16]}")
sys.exit(0 if ok else 1)
PY
)"

run_case unlisted "$FIX/clone-unlisted"
check unlisted "$(cat <<'PY'
import json, sys
out = sys.argv[1]
payload = json.load(open(out + "/stdout.json"))
rc = int(open(out + "/exit.txt").read())
findings = payload.get("findings", [])
unexempted = [f for f in findings if not f["exempted"]]
ok = (rc == 1 and payload["summary"]["unexempted_finding_count"] == 1
      and len(findings) == 7
      and len(unexempted) == 1
      and unexempted[0]["path"] == "a2extra/unlisted.json"
      and unexempted[0]["line"] == 1
      and all(a["applied"] for a in payload["allow"]))
print(f"unlisted exit={rc} findings={len(findings)} unexempted={len(unexempted)} "
      f"path={unexempted[0]['path'] if unexempted else None}")
sys.exit(0 if ok else 1)
PY
)"

echo "HASHED_SELFTEST: $([ "$FAILS" -eq 0 ] && echo CLEAN || echo "FAILED fails=$FAILS") cases=3"
exit "$([ "$FAILS" -eq 0 ] && echo 0 || echo 1)"
