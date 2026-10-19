#!/usr/bin/env bash
# EX-33 final canonical leg — run only after watch-tool.sh reports STABLE.
# Captures twice with the stable revised tool; audits both; re-runs the old-receipt
# battery; cross-checks the pre-revision receipt (pin 112d01dc) against the post one.
set -u
S=/var/tmp/ex33-selfpin
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
TOOL=$R/.ufo/gates/custody-pair/custody-pair.py
OLD=112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa
exec > >(tee "$S/out/legC2.log") 2>&1

echo "=== EX-33 legC2 (final canonical) $(date -u +%FT%TZ) ==="
SHA=$(sha256sum "$TOOL" | cut -d' ' -f1)
echo "FINAL-REVISED-SHA: $SHA"
[ "$SHA" = "$OLD" ] && { echo "ABORT: revision not landed"; exit 1; }
git -C "$R" status --porcelain -- .ufo/gates/custody-pair/ 2>&1 | head -5
stat -c 'mtime=%y size=%s' "$TOOL"

# two consecutive captures with the same revision
python3 "$TOOL" capture --out "$S/out/final-a.receipt" --label EX33-final-a
echo "capture A exit=$?"
sleep 2
python3 "$TOOL" capture --out "$S/out/final-b.receipt" --label EX33-final-b
echo "capture B exit=$?"
python3 "$S/selfpin-audit.py" --tool "$TOOL" --receipt "$S/out/final-a.receipt" --expect-not "$OLD" --label FINAL-A
echo "audit A exit=$?"
python3 "$S/selfpin-audit.py" --tool "$TOOL" --receipt "$S/out/final-b.receipt" --expect-not "$OLD" --label FINAL-B
echo "audit B exit=$?"
echo "-- pins in the two captures (same revision expected) --"
grep -h '^# tool: ' "$S/out/final-a.receipt" "$S/out/final-b.receipt"

# old receipts through the final tool: baseline battery + cross-revision pairs
R2A=$R/.ufo/waves/arc3-loop1-round2/claims/c3/EX-33/receipts/custody-live.v2.json
R2B=$R/.ufo/waves/arc3-loop1-round2/claims/c3/EX-33/receipts/custody-live-2.v2.json
V1C=$R/.ufo/waves/arc3-loop1-round2/claims/c3/EX-34/v1-canonical-round1-receipt.txt
# receipt stores are read-only inputs: hash before/after the battery
sha256sum "$R2A" "$R2B" "$V1C" > "$S/out/oldreceipts-before.sha256"
cat "$R2A" "$R2B" >/dev/null  # touch-read, no modification
echo "-- old-receipt sidecars still match their receipt bytes (independent) --"
for f in "$R2A" "$R2B"; do
  want=$(cut -d' ' -f1 "$f.sha256"); got=$(sha256sum "$f" | cut -d' ' -f1)
  [ "$want" = "$got" ] && echo "  SIDECAR-MATCH  $f" || echo "  SIDECAR-MISMATCH $f want=$want got=$got"
done
python3 "$S/oldreceipts-probe.py" --tool "$TOOL" --out "$S/out/legO-final.log" --label final-revised-tool \
 --probe "r2pair|$R2A|$R2B|" \
 --probe "r2live1-vs-live|$R2A||--live" \
 --probe "v1canon-vs-live|$V1C||--live" \
 --probe "r2-vs-v1canon|$R2A|$V1C|" \
 --probe "old-pre-vs-new-final|$S/out/canon-pre.receipt|$S/out/final-a.receipt|" \
 --probe "midrev-post-vs-final|$S/out/canon-post.receipt|$S/out/final-a.receipt|" \
 --probe "arc2-sums-pre-vs-post|$R/.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt|$R/.ufo/waves/arc2-loop1-round2/receipts/config-post-pair.txt|"
echo "legO-final exit=$?"
sha256sum "$R2A" "$R2B" "$V1C" > "$S/out/oldreceipts-after.sha256"
diff "$S/out/oldreceipts-before.sha256" "$S/out/oldreceipts-after.sha256" \
  && echo "OLD-RECEIPTS-UNCHANGED-BY-VERIFY: yes" || echo "OLD-RECEIPTS-UNCHANGED-BY-VERIFY: NO — verify wrote to its inputs"

# instrument sanity at the final revision + declared-case count
python3 "$TOOL" selftest --scratch "$S" > "$S/out/selftest-final.log" 2>&1
echo "selftest exit=$?  tail:"
tail -2 "$S/out/selftest-final.log"

# sha of the tool AFTER everything — must equal FINAL-REVISED-SHA
sha256sum "$TOOL"
echo "=== legC2 done $(date -u +%FT%TZ) ==="