#!/usr/bin/env bash
# Round-19 L1 sequential carrier runs (predictions frozen in Git before any
# measured run). Never executes a carrier: REA analyze imports a copy into
# Ghidra headless (static analysis). Reuses the round-17 tools unchanged
# (TOOLS_DIR default W17/tools) and the round-18 emulator unchanged
# (SWISS_MISREAD default W18/tools/swiss-misread.py, H1). Labels come from
# W19/predictions/carriers.tsv (columns: label, carrier path, kind, sha256);
# the frozen sha256 column is the ONLY carrier-integrity source — no
# SHA256SUMS store is read. Output goes to ${RUNS_DIR:-runs}/<label> resolved
# against W19; use RUNS_DIR=/tmp/<dir> for a non-destructive recheck.
# W is the directory this script lives in (not a hardcoded wave path), so a
# copy under /tmp cannot silently write the real wave's runs/. TOOLS_DIR,
# PREDICTIONS_DIR, SWISS_MISREAD, SELECTION_PY and RUNS_DIR env overrides
# exist only so the script can be dry-checked against fake dirs under /tmp;
# defaults are the contract paths.
#
# REA is pinned to rea-agents@6.5.0 through REA_VERSION and passed explicitly
# as --rea-version: carrier-run.py's own default is also 6.5.0, so relying on
# it would leave this driver's pin unstated (and silently follow a future
# default bump).
#
# TIMEOUT_S is carrier-run.py's per-step timeout (inspect-go-binary, analyze,
# and each --search), so it bounds one carrier, and the analyze step includes
# the `npx -y rea-agents@6.5.0` call for a cold cache. Derivation from the 15
# W18/runs/*/receipt.json steps: analyze wall time 20.59-70.74 s for carriers
# 2.21-20.69 MB; least squares t = 16.98 + 2.967*MB (max residual 13.4 s)
# predicts 80.8 s at the largest W19 carrier (compile, 21.52 MB), and the most
# pessimistic per-MB reading (10.01 s/MB at 2.25 MB) predicts 215 s.
# TIMEOUT_S=1200 is 14.9x the fitted estimate and 5.6x the pessimistic one,
# and covers the whole REA_GHIDRA_STARTUP_TIMEOUT_MS=900000 startup budget
# plus 300 s of analysis. This is a per-step budget, not a whole-wave ceiling:
# inspect, analyze and optional searches run sequentially for each carrier.
# Round-18 used 1500, i.e. 21.2x its own observed maximum.
#
# Exit 0 only if every selected carrier-run and compare exited 0; exit 1 when
# any run/compare/preflight failed; exit 2 when carriers.tsv is unusable
# (zero carrier rows, missing trailing newline, or a row whose sha256 column
# is not 64 lowercase hex).
# `--selftest` builds stub tools + fixtures under /tmp, re-execs this script
# against them, accumulates failures, prints `SELFTEST: CLEAN cases=N`
# (exit 0) or `SELFTEST: FAILED ... cases=N fails=M` (exit 1), and removes the
# fixtures. It never touches LANE beyond reading the Go data dir listing and
# a read-only `git rev-parse`, and never invokes REA.
set -u
W=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
W18=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18
W17=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
G=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang
TOOLS_DIR="${TOOLS_DIR:-$W17/tools}"
PREDICTIONS_DIR="${PREDICTIONS_DIR:-$W/predictions}"
SWISS_MISREAD="${SWISS_MISREAD:-$W18/tools/swiss-misread.py}"
SELECTION_PY="${SELECTION_PY:-$LANE/.ufo/waves/round-16/selection.py}"
REA_VERSION=6.5.0
TIMEOUT_S=1200
TSV="$PREDICTIONS_DIR/carriers.tsv"
W17_TOOLS=(carrier-run.py pins.py log-extract.py compare.py receipt-validate.py)

selftest() {
  local root cases=0 fails=0
  root=$(mktemp -d /tmp/r19-run-carriers-selftest.XXXXXX) || {
    echo "SELFTEST: FAILED setup (mktemp)"; return 1; }
  trap 'rm -rf "$root"' RETURN
  mkdir -p "$root/tools" "$root/predictions" "$root/predictions-nonl" \
          "$root/predictions-empty" "$root/predictions-badsha" \
          "$root/carriers" "$root/runs"

  fail() { echo "SELFTEST: FAILED $1"; fails=$((fails + 1)); }
  chk() { cases=$((cases + 1)); [ "$2" = "$3" ] || fail "$1 (expected $2, got $3)"; }

  # Stub carrier-run.py: records its argv (so the pin and timeout the driver
  # passes are observable), verifies every --pin is a real file (mirrors the
  # real tool's pin-failed exit 2), writes receipt.json with a bound session
  # and the ghidra.log the driver expects. No REA is ever invoked.
  cat > "$root/tools/carrier-run.py" <<'PY'
import json, os, sys
a = sys.argv[1:]
out = a[a.index("--out-dir") + 1]
open(os.path.join(out, "stub-argv.txt"), "w").write("\n".join(a) + "\n")
for i, x in enumerate(a):
    if x == "--pin" and not os.path.isfile(a[i + 1]):
        json.dump({"error": "pin failed for %s" % a[i + 1]},
                  open(os.path.join(out, "receipt.json"), "w"))
        sys.exit(2)
os.makedirs(os.path.join(out, "logs", "sess1"), exist_ok=True)
open(os.path.join(out, "logs", "sess1", "ghidra.log"), "w").write("stub log\n")
json.dump({"bound_sessions": ["sess1"]},
          open(os.path.join(out, "receipt.json"), "w"))
sys.exit(0)
PY
  cat > "$root/tools/log-extract.py" <<'PY'
import sys
a = sys.argv[1:]
log = a[a.index("--log") + 1]
try:
    open(log).read()
except OSError:
    sys.exit(2)
print("{}")
PY
  # Stub compare.py: exits 1 when the prediction fixture carries COMPARE_FAIL.
  cat > "$root/tools/compare.py" <<'PY'
import sys
a = sys.argv[1:]
pred = a[a.index("--prediction") + 1]
if "COMPARE_FAIL" in open(pred).read():
    print('{"all_match": false}')
    sys.exit(1)
print('{"all_match": true}')
PY
  printf 'stub\n' > "$root/tools/pins.py"
  printf 'stub\n' > "$root/tools/receipt-validate.py"
  printf 'stub\n' > "$root/tools/swiss-misread.py"
  printf 'stub\n' > "$root/selection.py"

  printf 'fakeA\n'      > "$root/carriers/fakeA"
  printf 'fakeBad\n'   > "$root/carriers/fakeBad"
  printf 'fakeNoPred\n'> "$root/carriers/fakeNoPred"
  printf 'fakeBadSha\n'> "$root/carriers/fakeBadSha"
  printf '{}' > "$root/predictions/fakeA.prediction.json"
  printf '{"mark": "COMPARE_FAIL"}' > "$root/predictions/fakeBad.prediction.json"
  printf '{}' > "$root/predictions/fakeBadSha.prediction.json"

  # The integrity oracle is the tsv's own sha256 column: correct for fakeA and
  # fakeNoPred; the entry for fakeBadSha is deliberately the sha of different
  # bytes (mismatch case).
  shaA=$(sha256sum "$root/carriers/fakeA" | awk '{print $1}')
  shaNoPred=$(sha256sum "$root/carriers/fakeNoPred" | awk '{print $1}')
  shaBad=$(sha256sum "$root/carriers/fakeBad" | awk '{print $1}')

  {
    printf 'fakeA\t%s/carriers/fakeA\tsynthetic-minimal-pair\t%s\n' "$root" "$shaA"
    printf 'fakeBad\t%s/carriers/fakeBad\tcalibration\t%s\n' "$root" "$shaBad"
    printf 'fakeNoPred\t%s/carriers/fakeNoPred\tsynthetic-minimal-pair\t%s\n' "$root" "$shaNoPred"
    printf 'fakeBadSha\t%s/carriers/fakeBadSha\tsynthetic-minimal-pair\t%s\n' "$root" "$shaBad"
  } > "$root/predictions/carriers.tsv"
  # carriers.tsv with no trailing newline, zero rows, and one row whose
  # sha256 column is not 64 lowercase hex.
  printf 'x\t/nonexistent\tk\tabc' > "$root/predictions-nonl/carriers.tsv"
  : > "$root/predictions-empty/carriers.tsv"
  printf '# comment row\noops\t%s/carriers/fakeA\tk\tNOT-A-SHA\n' "$root" \
    > "$root/predictions-badsha/carriers.tsv"

  envbase=(env "TOOLS_DIR=$root/tools" "SWISS_MISREAD=$root/tools/swiss-misread.py"
            "SELECTION_PY=$root/selection.py" "RUNS_DIR=$root/runs")

  # Case selector: run only fakeA; must exit 0 and touch only its dir.
  "${envbase[@]}" "PREDICTIONS_DIR=$root/predictions" bash "$0" fakeA \
    > "$root/sel.stdout" 2> "$root/sel.stderr"
  chk "selector-run exit" 0 "$?"
  chk "selector-run compare.json present" 0 "$([ -f "$root/runs/fakeA/compare.json" ]; echo $?)"
  chk "selector-run left fakeBad alone" 1 "$([ -e "$root/runs/fakeBad" ]; echo $?)"
  chk "selector-run producer.json present" 0 "$([ -f "$root/runs/fakeA/producer.json" ]; echo $?)"
  chk "producer.json has branch_tip" 1 "$(grep -c '"branch_tip"' "$root/runs/fakeA/producer.json" 2>/dev/null)"
  chk "producer.json has tool_sha256" 1 "$(grep -c '"tool_sha256"' "$root/runs/fakeA/producer.json" 2>/dev/null)"
  chk "producer.json parses" 0 "$(python3 -I -c 'import json,sys; json.load(open(sys.argv[1]))' "$root/runs/fakeA/producer.json" 2>/dev/null; echo $?)"
  chk "producer.json records all 7 tools" 7 "$(python3 -I -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["tool_sha256"]))' "$root/runs/fakeA/producer.json" 2>/dev/null)"
  # The REA pin and per-carrier timeout must reach carrier-run.py explicitly.
  chk "carrier-run got --rea-version 6.5.0" "6.5.0" \
    "$(awk 'p{print; exit} /^--rea-version$/{p=1}' "$root/runs/fakeA/stub-argv.txt" 2>/dev/null)"
  chk "carrier-run got --timeout 1200" "1200" \
    "$(awk 'p{print; exit} /^--timeout$/{p=1}' "$root/runs/fakeA/stub-argv.txt" 2>/dev/null)"
  # Pin list: carrier, prediction, swiss-misread, r16 selection, 5 W17 tools,
  # and every Go data file.
  chk "carrier-run pin count" "$((9 + $(find "$G" -type f | wc -l)))" \
    "$(grep -c '^--pin$' "$root/runs/fakeA/stub-argv.txt" 2>/dev/null)"

  # Case mixed: all four rows. fakeA green; fakeBad compare=1 (red: stub
  # prediction carries COMPARE_FAIL); fakeNoPred skipped exit 2 (red: no
  # prediction); fakeBadSha skipped exit 2 (red: tsv sha256 mismatch).
  "${envbase[@]}" "PREDICTIONS_DIR=$root/predictions" bash "$0" \
    > "$root/all.stdout" 2> "$root/all.stderr"
  chk "mixed-run exit" 1 "$?"
  chk "fakeA carrier-run exit" 0 "$(cat "$root/runs/fakeA/carrier-run.exit" 2>/dev/null)"
  chk "fakeA compare exit" 0 "$(cat "$root/runs/fakeA/compare.exit" 2>/dev/null)"
  chk "fakeBad compare exit" 1 "$(cat "$root/runs/fakeBad/compare.exit" 2>/dev/null)"
  chk "fakeNoPred carrier-run exit" 2 "$(cat "$root/runs/fakeNoPred/carrier-run.exit" 2>/dev/null)"
  chk "fakeNoPred has no compare.exit" 1 "$([ -e "$root/runs/fakeNoPred/compare.exit" ]; echo $?)"
  chk "fakeBadSha carrier-run exit" 2 "$(cat "$root/runs/fakeBadSha/carrier-run.exit" 2>/dev/null)"
  chk "fakeBadSha has no compare.exit" 1 "$([ -e "$root/runs/fakeBadSha/compare.exit" ]; echo $?)"
  chk "fakeBad producer.json present" 0 "$([ -f "$root/runs/fakeBad/producer.json" ]; echo $?)"

  # Case tsv shape: missing trailing newline, zero rows and a malformed sha256
  # column all exit 2 before any carrier dir is created.
  "${envbase[@]}" "PREDICTIONS_DIR=$root/predictions-nonl" bash "$0" \
    > "$root/nonl.stdout" 2> "$root/nonl.stderr"
  chk "no-trailing-newline exit" 2 "$?"
  "${envbase[@]}" "PREDICTIONS_DIR=$root/predictions-empty" bash "$0" \
    > "$root/empty.stdout" 2> "$root/empty.stderr"
  chk "zero-rows exit" 2 "$?"
  "${envbase[@]}" "PREDICTIONS_DIR=$root/predictions-badsha" bash "$0" \
    > "$root/badsha.stdout" 2> "$root/badsha.stderr"
  chk "bad-sha-column exit" 2 "$?"
  chk "bad-sha-column ran nothing" 1 "$([ -e "$root/runs/oops" ]; echo $?)"

  # Case rm guard: RUNS_DIR outside W19/runs or /tmp must be refused. $root is
  # under /tmp (allowed), so use a $HOME path that must never be created.
  guard="$HOME/.r19-run-carriers-guard-$$"
  "${envbase[@]}" "PREDICTIONS_DIR=$root/predictions" "RUNS_DIR=$guard" \
    bash "$0" fakeA > "$root/guard.stdout" 2> "$root/guard.stderr"
  chk "rm-guard exit" 1 "$?"
  chk "rm-guard left no dir" 1 "$([ -e "$guard" ]; echo $?)"

  "${envbase[@]}" "PREDICTIONS_DIR=$root/predictions" bash "$0" nonexistent \
    > "$root/unknown.stdout" 2> "$root/unknown.stderr"
  chk "unknown-selector exit" 2 "$?"
  mkdir -p "$root/predictions-traversal"
  printf '../escape\t%s/carriers/fakeA\tk\t%s\n' "$root" "$shaA" \
    > "$root/predictions-traversal/carriers.tsv"
  "${envbase[@]}" "PREDICTIONS_DIR=$root/predictions-traversal" bash "$0" \
    > "$root/traversal.stdout" 2> "$root/traversal.stderr"
  chk "traversal-label exit" 2 "$?"
  chk "traversal-label no output" 1 "$([ -e "$root/escape" ]; echo $?)"

  if [ "$fails" -gt 0 ]; then
    echo "SELFTEST: FAILED cases=$cases fails=$fails"
    return 1
  fi
  echo "SELFTEST: CLEAN cases=$cases"
  return 0
}

if [ "${1:-}" = "--selftest" ]; then
  selftest
  exit $?
fi

# Preflight the shared inputs so a wave-level misconfiguration fails once,
# loudly, instead of surfacing as N identical pin failures mid-run.
missing=0
for f in "$TOOLS_DIR/carrier-run.py" "$TOOLS_DIR/pins.py" "$TOOLS_DIR/log-extract.py" \
         "$TOOLS_DIR/compare.py" "$TOOLS_DIR/receipt-validate.py" \
         "$SWISS_MISREAD" "$SELECTION_PY" "$TSV"; do
  [ -f "$f" ] || { echo "run-carriers: missing required path: $f" >&2; missing=1; }
done
[ -d "$G" ] || { echo "run-carriers: missing Go data dir: $G" >&2; missing=1; }
[ "$missing" = 0 ] || exit 1

# carriers.tsv must be well-formed before the first REA call, since each row
# costs minutes: a missing trailing newline means the last row may be
# silently dropped by `read`, zero carrier rows means nothing to do, and a
# row without a 64-hex sha256 column has no integrity oracle. All three are
# could-not-evaluate → exit 2.
if [ -n "$(tail -c 1 "$TSV")" ]; then
  echo "run-carriers: $TSV has no trailing newline" >&2; exit 2
fi
rows=0
while IFS=$'\t' read -r label path kind sha4 extra; do
  [ -z "$label" ] && continue
  case "$label" in \#*) continue ;; esac
  rows=$((rows + 1))
  if [[ ! "$label" =~ ^[A-Za-z0-9][A-Za-z0-9_-]*$ ]]; then
    echo "run-carriers: unsafe label '$label' (single basename required)" >&2
    exit 2
  fi
  case "$sha4" in
    ""|*[!0-9a-f]*)
      echo "run-carriers: $TSV row $rows ($label): sha256 column is not lowercase hex: '$sha4'" >&2
      exit 2 ;;
  esac
  if [ "${#sha4}" -ne 64 ]; then
    echo "run-carriers: $TSV row $rows ($label): sha256 column is ${#sha4} hex chars, want 64" >&2
    exit 2
  fi
done < "$TSV"
if [ "$rows" -eq 0 ]; then
  echo "run-carriers: $TSV has zero carrier rows" >&2; exit 2
fi

cd "$W"
mapfile -t GOFILES < <(find "$G" -type f | sort)
[ "${#GOFILES[@]}" -gt 0 ] || { echo "run-carriers: no Go data files under $G" >&2; exit 1; }
PINARGS=()
for f in "${GOFILES[@]}"; do PINARGS+=(--pin "$f"); done
TOOLPINARGS=()
for t in "${W17_TOOLS[@]}"; do TOOLPINARGS+=(--pin "$TOOLS_DIR/$t"); done

only="${1:-}"
overall=0
selected=0
while IFS=$'\t' read -r label path kind sha4 extra; do
  [ -z "$label" ] && continue
  case "$label" in \#*) continue ;; esac
  [ -n "$only" ] && [ "$only" != "$label" ] && continue
  selected=$((selected + 1))
  out="${RUNS_DIR:-runs}/$label"
  case "$out" in /*) outabs="$out" ;; *) outabs="$W/$out" ;; esac
  outabs=$(realpath -m "$outabs")
  case "$outabs" in
    "$W/runs/"*|/tmp/*) ;;
    *) echo "run-carriers: refusing out dir outside W19/runs or /tmp: $outabs" >&2
       overall=1; continue ;;
  esac
  rm -rf "$outabs"; mkdir -p "$outabs"
  pred="$PREDICTIONS_DIR/$label.prediction.json"
  if [ ! -f "$path" ] || [ ! -f "$pred" ]; then
    echo "run-carriers: skipping $label (missing carrier or prediction: $pred)" >&2
    echo 2 > "$outabs/carrier-run.exit"
    overall=1
    continue
  fi
  # Carrier integrity before the run: the frozen tsv sha256 column (preflight
  # already proved it is 64 hex). Mismatch → carrier-run.exit=2, skip.
  actual=$(sha256sum "$path" | awk '{print $1}')
  if [ "$actual" != "$sha4" ]; then
    echo "run-carriers: $label: carrier sha256 mismatch (frozen $sha4, got $actual)" >&2
    echo 2 > "$outabs/carrier-run.exit"; overall=1; continue
  fi
  # Producer identity before the run: lane branch tip + sha256 of every tool
  # byte that produces this run's receipts.
  branch_tip=$(git -C "$LANE" rev-parse --verify "refs/heads/main^{commit}" 2>/dev/null || true)
  if [ -n "$branch_tip" ]; then tipjson="\"$branch_tip\""; else tipjson=null; fi
  {
    echo "{"
    echo "  \"label\": \"$label\","
    echo "  \"recorded_at_utc\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
    echo "  \"branch\": \"main\","
    echo "  \"branch_tip\": $tipjson,"
    echo "  \"tool_sha256\": {"
    sep=""
    for t in "${W17_TOOLS[@]}" "$SWISS_MISREAD" "$SELECTION_PY"; do
      case "$t" in /*) tp="$t" ;; *) tp="$TOOLS_DIR/$t" ;; esac
      h=$(sha256sum "$tp" | awk '{print $1}')
      printf '%s    "%s": "%s"\n' "$sep" "$tp" "$h"
      sep=","
    done
    printf '\n  }\n}\n'
  } > "$outabs/producer.json"
  echo "== $label start $(date -Iseconds)"
  # carrier-run.py already pins [carrier(realpath), R16_SELECTION] by default
  # and dedupes exact paths; the explicit --pin set below is the contract C3
  # list (carrier, prediction, swiss-misread.py, r16 selection.py, all five
  # W17 tools, Go data). --rea-version and --timeout are stated here so the
  # pin and the per-carrier bound are auditable in receipt.json's orig_argv.
  env REA_GHIDRA_STARTUP_TIMEOUT_MS=900000 \
  python3 -I -B "$TOOLS_DIR/carrier-run.py" --carrier "$path" --label "$label" --out-dir "$outabs" \
     --rea-version "$REA_VERSION" --timeout "$TIMEOUT_S" --poll 0.5 \
     --pin "$(realpath "$path")" --pin "$pred" --pin "$SWISS_MISREAD" --pin "$SELECTION_PY" \
     "${TOOLPINARGS[@]}" "${PINARGS[@]}" \
     > "$outabs/carrier-run.stdout" 2> "$outabs/carrier-run.stderr"
  rc=$?
  echo "$rc" > "$outabs/carrier-run.exit"
  bound=$(jq -r '.bound_sessions[0] // empty' "$outabs/receipt.json" 2>/dev/null)
  if [ -n "$bound" ]; then
    log="$outabs/logs/$(basename "$bound")/ghidra.log"
    python3 -I -B "$TOOLS_DIR/log-extract.py" --log "$log" > "$outabs/observation.json"; echo $? > "$outabs/observation.exit"
    python3 -I -B "$TOOLS_DIR/compare.py" --prediction "$pred" --observation "$outabs/observation.json" > "$outabs/compare.json"; echo $? > "$outabs/compare.exit"
  fi
  echo "== $label end $(date -Iseconds) carrier-run=$rc compare=$(cat "$outabs/compare.exit" 2>/dev/null)"
  [ "$rc" = 0 ] && [ "$(cat "$outabs/compare.exit" 2>/dev/null)" = 0 ] || overall=1
done < "$TSV"
if [ "$selected" -eq 0 ]; then
  echo "run-carriers: label selector '${only}' matched no carrier" >&2
  exit 2
fi
exit $overall
