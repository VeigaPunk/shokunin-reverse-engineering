# PB2 — lane-B scribe, census-pre-B (luna-round-7)

## CLAIM
Run the lane-B pre-state census at HEAD `411175e` and record it as `receipts/census-pre-B.txt`: Command A baseline, map-token and 72-file digests, and the six l7 IDs' absence.

## METHOD
- The assigned design source `CB7` did not exist: `ls .ufo/waves/luna-round-7/CB7.md` → No such file; `find -iname '*CB7*'` → empty at 20:14:27, re-polled through 20:17:22 while CB1–CB6/CB8/CB9/CB11/CB12 landed. Fell back to the canonical census-pre design, same shape as lane-A `receipts/census-pre.txt` (round-6 precedent `receipts/census-laneB-pre.txt`).
- Read-only Git-object reads; no probes, MCP, network, or tracked-file writes. Recipe A body extracted at HEAD (`SCORECARD.md:93-123`), worktree extraction diffed identical; run twice.

## FINDINGS
- Command A, exit 0, two runs byte-identical: 72/72 mapped, missing/dangling `[]`, 9/9 rules, 10.0/10.0; stdout sha256 `77b10639…` diffs clean against lane-A `census-pre.txt:11` and equals TB1's recorded hash (`receipts/census-pre-B.txt:18-33`).
- Baselines reproduce lane A independently: 72 map tokens `c538284b…`; 72-md-file aggregate `3adf3bc2…` (73 tracked paths incl. `.gitkeep`); full per-file SHA-256 baseline embedded (`:35-117`). CB6:9 records the same aggregate — three-way agreement.
- Six hyphenated l7 IDs absent: `knowledge_file=false`, 0 map rows, 0 Knowledge rows (`:119-128`).
- Version-pin appendix (round-6 CB7 method, legs 3-8 both lanes): every `rea-agents@…` token is exactly `rea-agents@6.5.0`; the 3 bare-name mentions are prose only (`:130-160`).
- Post-state: 134 untracked lines, 0 tracked-dirty, both diffs exit 0, HEAD unchanged (`:162-174`).

## THREATS
- Design-provenance gap: no CB7 artifact existed at run time; the executed design is the canonical fallback, not CB7's. Reconcile if a CB7 design lands later.
- Non-blind: lane-A `census-pre.txt` was read during recon before the run.
- Snapshot only: round-7 drafts keep appearing (CB4/CB12 at 20:17); this census covers Git objects at HEAD, not those drafts. Post-integration 78/78 remains unverified.

## VERDICT
FINDING: no round-7 CB7 artifact existed to run (polled through 20:17:22); canonical census-pre design executed instead — result CLEAN (72/72, 9/9 rules, 10.0/10.0, six l7 IDs absent, lane-A digests reproduced).
