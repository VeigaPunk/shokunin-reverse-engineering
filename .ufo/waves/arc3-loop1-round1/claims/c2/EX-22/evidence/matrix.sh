#!/usr/bin/env bash
# EX-22 before->after matrix. Scratch only: /var/tmp/ex22.
S=/var/tmp/ex22
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
REAL=$R/.ufo/gates/citation-drift
P=$S/gates-patched/citation-drift-probe.py
B=$REAL/citation-drift-probe.py
PINNED=$S/gates-patched/expected.json
E=$S/exp

mkdir -p $E
# fixtures
printf '{"entries": []}\n' > $E/evil-table.json
python3 - <<'PY'
data = open("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json","rb").read()
open("/var/tmp/ex22/exp/crlf-table.json","wb").write(data.replace(b"\n", b"\r\n"))
PY
rm -f $E/link-table.json $E/fifo-table.json
ln -s $REAL/pointer-table.json $E/link-table.json
mkfifo $E/fifo-table.json

run() {  # label probe args...
  local label=$1; shift
  echo "--- $label"
  timeout 15 "$@" > "$E/out-$label.txt" 2>&1
  local rc=$?
  echo "exit=$rc"
  grep -E "CITATION_DRIFT: |CITATION_DRIFT_VERDICT|CITATION_DRIFT_SELFTEST:" "$E/out-$label.txt" | head -6
}

echo "########## PATCHED (after) ##########"
run P-clean-tree  python3 $P --root $R --rev HEAD --table $REAL/pointer-table.json --expected $PINNED
run P-clean-copy  python3 $P --root $R --rev HEAD --table $S/gates/pointer-table.json --expected $PINNED
run P-legacy-unpinned python3 $P --root $R --rev HEAD --table $REAL/pointer-table.json --expected $REAL/expected.json
run P-tampered-table python3 $P --root $R --rev HEAD --table $E/evil-table.json --expected $PINNED
run P-absent-table python3 $P --root $R --rev HEAD --table $E/no-such-table.json --expected $PINNED
run P-crlf-table python3 $P --root $R --rev HEAD --table $E/crlf-table.json --expected $PINNED
run P-symlink-table python3 $P --root $R --rev HEAD --table $E/link-table.json --expected $PINNED
run P-fifo-table python3 $P --root $R --rev HEAD --table $E/fifo-table.json --expected $PINNED
run P-absent-expected python3 $P --root $R --rev HEAD --table $REAL/pointer-table.json --expected $E/no-such-expected.json

echo "########## PRISTINE (before) ##########"
run B-tampered-table python3 $B --root $R --rev HEAD --table $E/evil-table.json --expected $REAL/expected.json
run B-absent-table python3 $B --root $R --rev HEAD --table $E/no-such-table.json --expected $REAL/expected.json
run B-crlf-table python3 $B --root $R --rev HEAD --table $E/crlf-table.json --expected $REAL/expected.json
run B-symlink-table python3 $B --root $R --rev HEAD --table $E/link-table.json --expected $REAL/expected.json
run B-fifo-table python3 $B --root $R --rev HEAD --table $E/fifo-table.json --expected $REAL/expected.json
echo "########## DONE ##########"
