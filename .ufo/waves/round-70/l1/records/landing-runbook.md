# Round-70 landing runbook (L1; executed after the wave settles and the landing commit exists)

Freeze: 4737a542ae3b1b910d8fe43efbd572bc578b07c6. Declaration fix: 8b82516182a269482f3a7dc96b50cd2ac349f3a6.
The landing commit carries the wave outputs (`.ufo/waves/round-70/w1/**`) and no instrument edit
(assert `git diff 4737a542..landing -- tools/round-70` is empty; the six pins in claims.json must
equal the landing blobs).

1. Landing run (4 carriers, --upx pinned-copy for the A2 threading evidence):
   cp /usr/bin/upx $SCRATCH/landing/upx-pinned-copy
   python3 -I -B tools/round-70/packed-elf.py --root . --rev <landing> --pkg <REA 6.5.0 root> \
     --work $SCRATCH/landing --upx $SCRATCH/landing/upx-pinned-copy \
     --json-out .ufo/waves/round-70/l1/scores/c3-at-landing.json
2. C1 after: forged-receipts.py --root . --rev <landing> --base-rev 5cc845ca ... (the P1 command,
   --landing-material .ufo/waves/round-70/l1/scores/c3-at-landing.json) \
     --json-out .ufo/waves/round-70/l1/scores/c1-at-landing.json   (exit 0)
3. C2 after: seam-probe.py --root . --rev <landing> --tool tools/round-70/packed-elf.py \
     --battery tools/round-70/mutation-check.py --pkg <REA> --work $SCRATCH/landing \
     --receipt .ufo/waves/round-70/l1/scores/c3-at-landing.json \
     --expect-upx $SCRATCH/landing/upx-pinned-copy \
     --json-out .ufo/waves/round-70/l1/scores/c2-at-landing.json   (exit 0, 7 of 7)
4. C3 after: packed-elf.py --check-receipt .ufo/waves/round-70/l1/scores/c3-at-landing.json \
     --root . --rev <landing>  (exit 0, met true) -> tee scores/c3-check-at-landing.json
5. Controls re-run at the landing rev -> scores/controls-at-landing.json (exit 0).
6. Freeze-integrity: git diff 4737a542..<landing> -- tools/round-70 must be empty; the r29 gate
   re-run at <landing> with --disclosures AFTER the round-70 ledger row lands (record commit)
   exits 0 with 45/45 exact.
7. Record commit: SCORECARD round-70 section (capabilities table rows enter here), LOG landing
   entry, corpus/lessons/round-70.md (Gate + Mistakes), corpus/knowledge/2026-11-04-r70-*.md,
   corpus/SOURCES.md S272 (+ any screened row), corpus/QUALITY.md row 115, corpus/README.md
   (map + index + frontier note), PROVINCE.md round-70 Core additions, SKILL.md registry rows,
   corpus/claim-freezes-v2.tsv round-70 row (verbatim from the gate audit), census-end receipt.
8. Close commit: LOG close entry, prefile receipt (tools/round-29/prefile-check.sh on the lane),
   registry-drift census receipt; scratch cleanup; ls-remote gate; report; fleet commit.
