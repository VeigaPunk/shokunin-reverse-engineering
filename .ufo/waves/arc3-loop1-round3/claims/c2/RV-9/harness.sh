#!/bin/bash
# RV-9 independent verification + attack harness for the revised custody-pair tool.
# usage: harness.sh TOOL PRE_RECEIPT POST_RECEIPT OUTDIR SCRATCH
# All fixtures on scratch; never writes a custody path.
set -u
TOOL="$1"; PRE="$2"; POST="$3"; OUT="$4"; SCR="$5"
mkdir -p "$OUT" "$SCR"
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin || exit 3
TOOLPIN=$(sha256sum "$TOOL" | cut -d' ' -f1)
echo "TOOL=$TOOL sha256=$TOOLPIN"

run() { # run LABEL expected_exit cmd...
  local label="$1" expect="$2"; shift 2
  echo "----- $label: $*" | tee -a "$OUT/harness.log"
  "$@" > "$OUT/$label.out" 2>&1
  local rc=$?
  echo "EXIT $label rc=$rc (expect $expect)" | tee -a "$OUT/harness.log"
  tail -3 "$OUT/$label.out" | sed 's/^/  /' | tee -a "$OUT/harness.log"
}

echo "== A0: pin" >> "$OUT/harness.log"
echo "$TOOLPIN  $TOOL" > "$OUT/tool-pin.txt"

run A1-selftest 0 python3 "$TOOL" selftest --scratch "$SCR/st"

run A2-verify-pair 0 python3 "$TOOL" verify "$PRE" "$POST"
run A3-verify-live 0 python3 "$TOOL" verify "$PRE" --live

echo "----- A4: RV-9 own capture with revised tool" >> "$OUT/harness.log"
python3 "$TOOL" capture --out "$OUT/rv9-post-capture.txt" --label "rv9-post-revision" > "$OUT/A4-capture.out" 2>&1
echo "EXIT A4-capture rc=$? (expect 0)" | tee -a "$OUT/harness.log"; tail -2 "$OUT/A4-capture.out" | sed 's/^/  /'
run A4b-verify-mine-vs-pre 0 python3 "$TOOL" verify "$PRE" "$OUT/rv9-post-capture.txt"
run A4c-verify-mine-vs-post 0 python3 "$TOOL" verify "$POST" "$OUT/rv9-post-capture.txt"

echo "== A5: vacuity positive control (mutated copy must fire)" >> "$OUT/harness.log"
python3 - "$PRE" "$SCR/mutated.txt" <<'PY'
import sys
a, b = sys.argv[1], sys.argv[2]
lines = open(a).read().splitlines()
out = []
flipped = False
for ln in lines:
    if not flipped and ln.startswith("SHA256: "):
        h = ln[8:]
        c = h[0]
        out.append("SHA256: " + ('0' if c != '0' else '1') + h[1:]); flipped = True
    else:
        out.append(ln)
open(b, "w").write("\n".join(out) + "\n")
print("flipped-first-sha:", flipped)
PY
run A5-verify-mutated 10 python3 "$TOOL" verify "$PRE" "$SCR/mutated.txt"

echo "== A6: EACCES scratch fixture" >> "$OUT/harness.log"
grep -i "eacces\|unreadable\|declared" "$TOOL" | head -20 > "$OUT/A6-tool-grep.txt"
mkdir -p "$SCR/eacces" && echo secret > "$SCR/eacces/blocked.txt" && chmod 000 "$SCR/eacces/blocked.txt"
run A6a-capture-eacces 0 python3 "$TOOL" capture --paths "$SCR/eacces/blocked.txt" --out "$SCR/eacces/rcpt.txt"
run A6b-verify-eacces-live 0 python3 "$TOOL" verify "$SCR/eacces/rcpt.txt" --live
chmod 600 "$SCR/eacces/blocked.txt"

echo "== A7: D6 scratch-guard on missing dir" >> "$OUT/harness.log"
run A7-selftest-missing-scratch 2 python3 "$TOOL" selftest --scratch "$SCR/does-not-exist-rv9"

echo "== A8: write-guard scope" >> "$OUT/harness.log"
echo one > "$SCR/guard-src.txt"
python3 "$TOOL" capture --paths "$SCR/guard-src.txt" --out "$SCR/guard-src.txt" > "$OUT/A8a-guard-self.out" 2>&1
echo "EXIT A8a-guard-self rc=$? (old tool: clobbered; revised: refuse)" | tee -a "$OUT/harness.log"; tail -2 "$OUT/A8a-guard-self.out" | sed 's/^/  /'
echo two > "$SCR/guard-a.txt"; echo three > "$SCR/guard-b.txt"
python3 "$TOOL" capture --paths "$SCR/guard-a.txt" --out "$SCR/guard-b.txt" > "$OUT/A8b-guard-cross.out" 2>&1
echo "EXIT A8b-guard-cross rc=$? (expect 2)" | tee -a "$OUT/harness.log"; tail -2 "$OUT/A8b-guard-cross.out" | sed 's/^/  /'
echo "A8c: content preserved after attempts"; cat "$SCR/guard-src.txt"

echo "== A9: tool self-pin in receipts" >> "$OUT/harness.log"
for r in "$OUT/rv9-post-capture.txt" "$PRE" "$POST"; do
  grep -m1 "^# tool: " "$r" | awk -v f="$r" '{print "  " f ": " $0}' | tee -a "$OUT/harness.log"
done

echo "== A10: v1 receipts still sha256-verifiable (r2-era pair)" >> "$OUT/harness.log"
R2A=.ufo/waves/arc3-loop1-round2/claims/c3/EX-31/capture-pre.txt
R2B=.ufo/waves/arc3-loop1-round2/claims/c3/EX-31/capture-post.txt
run A10-v1-v1 0 python3 "$TOOL" verify "$R2A" "$R2B"

echo "== A11: --require-paths presence" >> "$OUT/harness.log"
if python3 "$TOOL" verify --help 2>&1 | grep -q "require-paths"; then
  echo "flag present" | tee -a "$OUT/harness.log"
  python3 "$TOOL" verify --help 2>&1 | tee "$OUT/A11-verify-help.txt"
else
  echo "flag ABSENT in verify --help" | tee -a "$OUT/harness.log"
  python3 "$TOOL" verify --help 2>&1 | tee "$OUT/A11-verify-help.txt"
fi

echo "HARNESS DONE" | tee -a "$OUT/harness.log"