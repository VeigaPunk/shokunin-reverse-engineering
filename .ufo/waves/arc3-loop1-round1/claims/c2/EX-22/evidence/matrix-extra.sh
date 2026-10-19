#!/usr/bin/env bash
# EX-22 extra parity rows: dir table (EX-23 C8) and non-UTF8 table (EX-23 C9).
S=/var/tmp/ex22
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
REAL=$R/.ufo/gates/citation-drift
P=$S/gates-patched/citation-drift-probe.py
B=$REAL/citation-drift-probe.py
PINNED=$S/gates-patched/expected.json
E=$S/exp

printf '\xff\xfe not utf8' > $E/nonutf8-table.json

run() {
  local label=$1; shift
  echo "--- $label"
  timeout 15 "$@" > "$E/out-$label.txt" 2>&1
  echo "exit=$?"
  grep -E "CITATION_DRIFT: |CITATION_DRIFT_VERDICT" "$E/out-$label.txt" | head -4
}

run P-dir-table      python3 $P --root $R --rev HEAD --table $E --expected $PINNED
run P-nonutf8-table  python3 $P --root $R --rev HEAD --table $E/nonutf8-table.json --expected $PINNED
run B-dir-table      python3 $B --root $R --rev HEAD --table $E --expected $REAL/expected.json
run B-nonutf8-table  python3 $B --root $R --rev HEAD --table $E/nonutf8-table.json --expected $REAL/expected.json
