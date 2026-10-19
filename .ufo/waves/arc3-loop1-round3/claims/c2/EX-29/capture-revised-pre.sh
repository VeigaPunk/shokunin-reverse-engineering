#!/bin/bash
# EX-29: capture the revised-tool PRE receipt + bridge verifies (run once tool is stable)
set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
T=.ufo/gates/custody-pair/custody-pair.py
O=.ufo/waves/arc3-loop1-round3/claims/c2/EX-29
R=.ufo/waves/arc3-loop1-round3/claims/c2/receipts
SHA=$(sha256sum "$T" | cut -d' ' -f1)
echo "tool sha at capture: $SHA" | tee "$O/revised-pre-tool-sha.txt"
echo "captured-utc: $(date -u +%FT%TZ)" | tee -a "$O/revised-pre-tool-sha.txt"
cp "$T" "$O/custody-pair.${SHA:0:12}.py"
echo "tool snapshot: custody-pair.${SHA:0:12}.py sha256=$(sha256sum "$O/custody-pair.${SHA:0:12}.py" | cut -d' ' -f1)" | tee -a "$O/revised-pre-tool-sha.txt"
python3 "$T" capture --out "$R/config-pre-pair-v2r3-revised.txt" \
  --label "arc3-loop1-round3 PRE-PAIR revised-tool (EX-29; tool sha $SHA)" \
  > "$O/capture-pre-revised.out" 2>&1
echo "capture-exit=$?" | tee -a "$O/capture-pre-revised.out"
python3 "$T" verify "$R/config-pre-pair-v2r3.txt" "$R/config-pre-pair-v2r3-revised.txt" \
  > "$O/verify-roundstart-vs-revised-pre.out" 2>&1
echo "bridge-exit=$?" | tee -a "$O/verify-roundstart-vs-revised-pre.out"
python3 "$T" verify --require-paths 5 "$R/config-pre-pair-v2r3.txt" "$R/config-pre-pair-v2r3-revised.txt" \
  > "$O/verify-roundstart-vs-revised-pre-require5.out" 2>&1
echo "bridge-require5-exit=$?" | tee -a "$O/verify-roundstart-vs-revised-pre-require5.out"
python3 "$T" verify "$R/config-pre-pair-v2r3-revised.txt" --live \
  > "$O/verify-revised-pre-vs-live.out" 2>&1
echo "live-exit=$?" | tee -a "$O/verify-revised-pre-vs-live.out"
python3 "$T" --help > "$O/revised-tool-help.out" 2>&1
python3 "$T" verify --help >> "$O/revised-tool-help.out" 2>&1
python3 "$T" capture --help >> "$O/revised-tool-help.out" 2>&1
echo "--- capture ---"; tail -1 "$O/capture-pre-revised.out"
echo "--- bridge ---";   tail -1 "$O/verify-roundstart-vs-revised-pre.out"
echo "--- bridge-r5 ---"; tail -1 "$O/verify-roundstart-vs-revised-pre-require5.out"
echo "--- live ---";     tail -1 "$O/verify-revised-pre-vs-live.out"