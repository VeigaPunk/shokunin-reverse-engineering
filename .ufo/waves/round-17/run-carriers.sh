#!/usr/bin/env bash
# Round-17 L1 sequential carrier runs (predictions frozen at lane commit
# 271167473d87ef710f07ecdd98caf0ce12091686 before any measured run; the two calib-*
# carriers were also seen in the earlier pilot). Never executes a carrier: REA
# analyze imports a copy into Ghidra headless (static analysis). Output goes to
# ${RUNS_DIR:-runs}/<label>; use RUNS_DIR=/tmp/<dir> for a non-destructive recheck.
# Exit 0 only if every selected carrier-run and compare exited 0.
set -u
W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17
G=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang
cd "$W"
mapfile -t GOFILES < <(find "$G" -type f | sort)
PINARGS=()
for f in "${GOFILES[@]}"; do PINARGS+=(--pin "$f"); done
only="${1:-}"
overall=0
while IFS=$'\t' read -r label path kind; do
  [ -n "$only" ] && [ "$only" != "$label" ] && continue
  out="${RUNS_DIR:-runs}/$label"
  case "$out" in /*) outabs="$out" ;; *) outabs="$W/$out" ;; esac
  rm -rf "$out"; mkdir -p "$out"
  envs=()
  [ "$label" = "pro-op" ] && envs=(env REA_GHIDRA_STARTUP_TIMEOUT_MS=900000)
  echo "== $label start $(date -Iseconds)"
  "${envs[@]}" python3 -I -B tools/carrier-run.py --carrier "$path" --label "$label" --out-dir "$outabs" \
     --timeout 1500 --poll 0.5 --pin "$W/predictions/$label.prediction.json" "${PINARGS[@]}" \
     > "$out/carrier-run.stdout" 2> "$out/carrier-run.stderr"
  rc=$?
  echo "$rc" > "$out/carrier-run.exit"
  bound=$(jq -r '.bound_sessions[0] // empty' "$out/receipt.json" 2>/dev/null)
  if [ -n "$bound" ]; then
    log="$out/logs/$(basename "$bound")/ghidra.log"
    python3 -I -B tools/log-extract.py --log "$log" > "$out/observation.json"; echo $? > "$out/observation.exit"
    python3 -I -B tools/compare.py --prediction "predictions/$label.prediction.json" --observation "$out/observation.json" > "$out/compare.json"; echo $? > "$out/compare.exit"
  fi
  echo "== $label end $(date -Iseconds) carrier-run=$rc compare=$(cat "$out/compare.exit" 2>/dev/null)"
  [ "$rc" = 0 ] && [ "$(cat "$out/compare.exit" 2>/dev/null)" = 0 ] || overall=1
done < predictions/carriers.tsv
exit $overall
