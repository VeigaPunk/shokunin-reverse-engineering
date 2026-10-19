#!/bin/bash
# EX-29: close — capture POST receipt with the revised tool, verify the pair MATCH 5/5
set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
T=.ufo/gates/custody-pair/custody-pair.py
O=.ufo/waves/arc3-loop1-round3/claims/c2/EX-29
R=.ufo/waves/arc3-loop1-round3/claims/c2/receipts
SHA=$(sha256sum "$T" | cut -d' ' -f1)
{ echo "tool sha at close: $SHA"; echo "close-utc: $(date -u +%FT%TZ)"; echo "HEAD: $(git rev-parse HEAD)"; } | tee "$O/close-tool-sha.txt"
python3 "$T" capture --out "$R/config-post-pair-v2r3.txt" \
  --label "arc3-loop1-round3 POST-PAIR close (EX-29; tool sha $SHA)" \
  > "$O/capture-post.out" 2>&1
echo "capture-exit=$?" | tee -a "$O/capture-post.out"
python3 "$T" verify "$R/config-pre-pair-v2r3-revised.txt" "$R/config-post-pair-v2r3.txt" \
  > "$O/verify-pre-vs-post.out" 2>&1
echo "pair-exit=$?" | tee -a "$O/verify-pre-vs-post.out"
python3 "$T" verify --require-paths 5 "$R/config-pre-pair-v2r3-revised.txt" "$R/config-post-pair-v2r3.txt" \
  > "$O/verify-pre-vs-post-require5.out" 2>&1
echo "pair-require5-exit=$?" | tee -a "$O/verify-pre-vs-post-require5.out"
python3 "$T" verify "$R/config-post-pair-v2r3.txt" --live \
  > "$O/verify-post-vs-live.out" 2>&1
echo "post-live-exit=$?" | tee -a "$O/verify-post-vs-live.out"
python3 "$T" verify --require-paths 5 "$R/config-post-pair-v2r3.txt" --live \
  > "$O/verify-post-vs-live-require5.out" 2>&1
echo "post-live-require5-exit=$?" | tee -a "$O/verify-post-vs-live-require5.out"
python3 "$T" verify "$R/config-pre-pair-v2r3.txt" "$R/config-post-pair-v2r3.txt" \
  > "$O/verify-roundstart-vs-post.out" 2>&1
echo "roundstart-post-exit=$?" | tee -a "$O/verify-roundstart-vs-post.out"
python3 "$T" verify --require-paths 5 "$R/config-pre-pair-v2r3.txt" "$R/config-post-pair-v2r3.txt" \
  > "$O/verify-roundstart-vs-post-require5.out" 2>&1
echo "roundstart-post-require5-exit=$?" | tee -a "$O/verify-roundstart-vs-post-require5.out"
echo "--- capture ---";   tail -1 "$O/capture-post.out"
echo "--- pair ---";      tail -1 "$O/verify-pre-vs-post.out"
echo "--- pair-r5 ---";   tail -1 "$O/verify-pre-vs-post-require5.out"
echo "--- post-live ---"; tail -1 "$O/verify-post-vs-live.out"