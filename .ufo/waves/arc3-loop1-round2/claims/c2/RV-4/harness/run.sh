#!/bin/bash
# RV-4 mutation matrix. Runs each instrument variant against the LIVE repo root
# (read-only: the census only reads). Captures stdout+exit per run.
W=/var/tmp/rv4-mutation/work
R=/var/tmp/rv4-mutation/receipts
ROOT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
for v in instr-head instr-h3 instr-h3-nog2 instr-head-neut instr-h3-neut instr-h3-nog2-neut \
         instr-head-gate instr-h3-gate instr-h3-nog2-gate \
         instr-h3-pinonly instr-h3-nog2-pinonly instr-head-pinonly; do
  out="$R/$v.out"
  python3 "$W/$v.py" --root "$ROOT" > "$out" 2>&1
  rc=$?
  printf '%-26s exit=%-3s %s | %s\n' "$v" "$rc" \
    "$(grep -h 'G2 positive-assertion guard' "$out" | sed 's/^ *//')" \
    "$(grep -h 'VERDICT:' "$out" | sed 's/^ *//')"
  printf '%-26s %s\n' "" "$(grep -hE 'loci=' "$out" | tr '\n' ' ')"
done
