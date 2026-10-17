## CLAIM
The G4-design pre-state census runs clean at HEAD `a280e07` in lane B: command A 79/79 + 9/9 + 10.0/10.0, token-set SHA matches G3's claim, and the G4 append-guard BASE freeze is recorded. The "G5" half is absent from the round and unrun.

## METHOD
Read `G4.md`, lane-A `receipts/census-pre.txt`, `G2.md`, `G3.md`. Ran the census via a stdin script (no `/tmp` artifact) at `REV=a280e07133f52f719b0805fc73c0b997e77b5062`, sourced from the pinned SCORECARD blob: Recipe A verbatim, token census, knowledge aggregate, BASE freeze (recursive tree hash + allowlist blob hashes). After writing, extracted the embedded script from the receipt and re-ran it twice; all three core hashes agree. Full commands, script, output, and hash record: `receipts/census-laneB-pre.txt`.

## FINDINGS
- Recipe A: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07…", "rule_blocks": 9}` exit 0; stdout sha `6e110fde…`.
- Tokens: 79 occurrences / 79 unique, sha `bd70aa5f…750c` = `G3.md:24` claim; empty missing/dangling; token set equals file stems.
- BASE freeze: TREE_OID `9e509118…`; allowlist blobs r4-16 `622e3661…` (64080 B/925 L), jq-shadow `541f3499…` (16295 B/242 L), SCORECARD `0c722936…` (34819 B/559 L); PROVINCE `fe7f3f61…` frozen-clean.
- Determinism: core (`[1]`-`[5]`) sha `544a9f5e…` identical for canonical run plus two extraction re-runs; only volatile `[6]` lines vary (wave report count 91→103). Receipt SELFTEST PASS at 22:01:58.
- Design sources: `G4.md` sha `1dbef2d7…` (landed 21:50, after lane A's 21:47 blocker); `G5.md` absent (`G5_EXISTS=False`).

## THREATS
Non-blind: lane-A and G2/G3 values were read during recon; every value was recomputed independently from pinned Git objects. `[6]` snapshot values are volatile by construction. `[5]` TREE_* are BASE-HEAD material - after integration they become the AFTER comparison, not a reproduction. The allowlist is this seat's interpretation (`G4.md:8` x `X4.md:2`), not a parent-issued list. The census covers source-derived controls only, no semantics.

## VERDICT
CLEAN — G4-design census reproduced at `a280e07` (79/79, 9/9, 10.0/10.0; token SHA matches G3); G5 half absent, unrun, not substituted.
