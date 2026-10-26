#!/usr/bin/env bash
# R40-C1 rerun matrix driver (pre-freeze draft evidence).
#
# 3 REA 6.5.0 extract-firmware runs per carrier (K1, K2, K4, K5, K6) into three
# independent scratch roots (r1/r2/r3, each with its own TMPDIR), plus one
# extra K5 run under a deliberately different input basename to prove the
# projection is basename-invariant.  Nothing is written outside $S and $OUT.
#
# usage: run-matrix.sh <lane-root> <scratch-root> <artifacts-dir>
set -u
LANE=${1:?lane root}
S=${2:?scratch root}
OUT=${3:?artifacts dir}
REA_PKG=${REA_PKG:-$HOME/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents}
UNBLOB_BIN=${UNBLOB_BIN:-$HOME/.local/share/uv/tools/unblob/bin/unblob}

mkdir -p "$OUT/receipts" "$OUT/logs"
MATRIX="$OUT/run-matrix.tsv"
printf 'carrier\trun\troot\ttmpdir\tinput\tbasename\toutdir\texit\tduration_ms\tenvelope_bytes\tenvelope_sha256\treceipt_bytes\treceipt_sha256\tstderr_bytes\tstderr_head\n' > "$MATRIX"

declare -A SRC=(
  [K1]="$LANE/corpus/evidence/round-37/c1/K1/carrier.sqsh"
  [K2]="$LANE/corpus/evidence/round-37/c1/K2/carrier.sqsh"
  [K4]="$LANE/corpus/evidence/round-37/c1/K4/carrier.bin"
  [K5]="$LANE/corpus/evidence/round-39/c1/K5/carrier.sqsh"
  [K6]="$LANE/corpus/evidence/round-39/c1/K6/carrier.sqsh"
)
declare -A PIN=(
  [K1]=1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e
  [K2]=403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154
  [K4]=a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed
  [K5]=5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228
  [K6]=00152518a3902a1a13892ec4bfd280a258f162d8fdf77260ea2b41f4f482b25b
)

run_one() { # carrier run root basename
  local c=$1 n=$2 root=$3 base=$4
  local dir="$S/$root/$c"
  local tmp="$dir/tmp"
  local inp="$dir/$base"
  local outdir="$dir/extract-$c-r$n"
  mkdir -p "$tmp"
  cp -f "${SRC[$c]}" "$inp"
  # pin the copy, never trust the source path
  local got
  got=$(sha256sum "$inp" | cut -d' ' -f1)
  if [ "$got" != "${PIN[$c]}" ]; then
    echo "PIN MISMATCH $c $got" >&2
    return 9
  fi
  local t0 t1 start end
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  t0=$(date +%s%N)
  ( cd "$dir" && TMPDIR="$tmp" REA_UNBLOB_COMMAND="$UNBLOB_BIN" \
      npx -y "rea-agents@6.5.0" extract-firmware --format json --full-output \
      "$inp" "$outdir" > "$dir/out-$c-r$n.json" 2> "$dir/err-$c-r$n.txt" )
  local rc=$?
  t1=$(date +%s%N)
  end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  local env="$dir/out-$c-r$n.json"
  local envb envsha recb recsha errb errhead
  envb=$(stat -c %s "$env" 2>/dev/null || echo -1)
  envsha=$(sha256sum "$env" 2>/dev/null | cut -d' ' -f1 || echo -)
  errb=$(stat -c %s "$dir/err-$c-r$n.txt" 2>/dev/null || echo -1)
  errhead=$(head -c 160 "$dir/err-$c-r$n.txt" 2>/dev/null | tr '\t\n' '  ')
  local rec="$OUT/receipts/$c-r$n.json"
  python3 - "$env" "$rec" <<'PY'
import json,sys
env=json.load(open(sys.argv[1]))
data=env["data"]
json.dump(data,open(sys.argv[2],"w"),indent=1,sort_keys=True)
PY
  if [ $? -ne 0 ]; then recb=-1; recsha=-; else
    recb=$(stat -c %s "$rec"); recsha=$(sha256sum "$rec" | cut -d' ' -f1)
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$c" "r$n" "$root" "$tmp" "$inp" "$base" "$outdir" "$rc" \
    "$(( (t1 - t0) / 1000000 ))" "$envb" "$envsha" "$recb" "$recsha" "$errb" "$errhead" \
    >> "$MATRIX"
  cp -f "$dir/out-$c-r$n.json" "$OUT/logs/envelope-$c-r$n.json" 2>/dev/null
  cp -f "$dir/err-$c-r$n.txt" "$OUT/logs/stderr-$c-r$n.txt" 2>/dev/null
  echo "$c r$n exit=$rc ${start}..${end} outdir=$outdir"
}

# three concurrent lanes, one scratch root each
for c in K1 K2 K4 K5 K6; do
  run_one "$c" 1 r1 carrier.sqsh &
  run_one "$c" 2 r2 carrier.sqsh &
  run_one "$c" 3 r3 carrier.sqsh &
done
wait
# basename probe: same bytes, different input name, fourth root
run_one K5 4 r4 r40-probe.bin
wait
{ head -1 "$MATRIX"; tail -n +2 "$MATRIX" | sort; } > "$MATRIX.sorted" && mv "$MATRIX.sorted" "$MATRIX"
echo "matrix: $MATRIX"
