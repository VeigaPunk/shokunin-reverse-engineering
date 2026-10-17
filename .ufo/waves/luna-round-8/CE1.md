## CLAIM
Run a CA6-derived pre-state census at the assigned HEAD and record source controls plus host-config fingerprints for later comparison.

## METHOD
At `6e2ee8fadc4ab328ce7c8d4d82cceb9b326b94c4`, executed Command A from the immutable `SCORECARD.md:92-123` Git blob, plus sorted coverage-map and knowledge-blob digests, tracked-state check, receipt inventory and config SHA-256 fingerprints. Full command/output: `.ufo/waves/luna-round-8/receipts/census-pre.txt`. No REA/MCP probe was run. The round-6 CB6 final scorer is not reusable: it hard-pins `f0e8cde` and 6.5.0.

## FINDINGS
Command A: 78/78 mapped, no missing/dangling IDs, 9/9 rules, coverage/depth 10.0; map tokens: 78, SHA-256 `c6c025f3aee5fb93966f9da4eca22ade1ac3af9207d9ad26b8bca6807f6ae83b`; 78-file aggregate SHA-256 `00891de8600a2bf8eba44c5ecc4d32eba3d58bf2e7222124ea643fa447640076`. HEAD matched and tracked status lines were 0. Config fingerprints are recorded (`.ufo/waves/luna-round-8/receipts/census-pre.txt:83-100`). That snapshot contained main legs 1–9, three `-RV3-replay` receipts and `leg-2-tools.txt`, but no leg 10 (`:96-97`).

## THREATS
This is already post-start, not pre-probe: the snapshot records legs 1–9. It also does not satisfy the exact ten-leg final set because leg 10 is absent and replay-named receipt files are present (`.ufo/waves/luna-round-8/receipts/census-pre.txt:96-97`). Config hashes are baselines only, not a post-run drift comparison (`:98-100`). No 6.4.0 behavior or N/10 match score is established here.

## VERDICT
FINDING: Source controls measured at the pinned HEAD; the receipt snapshot already contains legs 1–9, so it cannot establish the true pre-probe state or final CA6 score.
