## CLAIM
Final luna-round-8 SHONEN state: all four boxes end `[~]`; none is promotable — `[x]` requires a named non-author verifier (`PROTOCOL.md:63-73`) and no box acquired one this round (lane-dispatched reviewers remain the lane, `LOG.md:456`). Two stale `PROVINCE.md` pointers and one stale manifest row are parent-side repairs.

## METHOD
Read-only. Re-ran command A (`SCORECARD.md:92-123`) at HEAD `6e2ee8f`; recomputed all ten receipt hashes vs `receipts/MANIFEST.txt`; byte-compared L3's displayed block with `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` and simulated RE1's `ac7470f9` variant; read `SHONEN.md:5-12`, `PROVINCE.md:88-116`, `SKILL.md:42,68,81,197`, `LOG.md:445-469`, `corpus/lessons/2026-10-15-round-1.md:87-153`, `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:217-219`, receipts 1-10, and seats RE1/RE4/SH1/CA2/CA6. No probes; no tracked file touched.

## FINDINGS
- Box 1 `[~]`: SKILL.md decision table `:42`, error patterns `:68`, queue-drain rules `:81`, checklists `:197`; my command A rerun at `6e2ee8f` returned `{"mapped":78,"knowledge_files":78,"citation_resolved_rules":9,"rule_blocks":9,"coverage_score":10.0,"depth_score":10.0}`. Box text satisfied; cited range `:77-191` omits the table and checklists; no non-author verifier — keep `[~]`.
- Box 2 `[~]`: libjq smoke resolvable (`LOG.md:464-469`; `lessons:87-125`; 18,991-byte bundle present). Outside review disclaimed (`LOG.md:456`; `lessons:142`). Round-8 L10 executed but unlogged in `LOG.md`; no gate movement.
- Box 3 `[~]`: executability demonstrated only by the lane itself; no independent execution review.
- Box 4 `[~]`: bleed live — jq-shadow entry `:217,219` ("benign payload … not binary compromise") vs the safety bar `PROVINCE.md:114-116`; `SHONEN.md:12`'s range `88-109` and `lessons:152`'s `107-109` both exclude 114-116.

## THREATS
- `MANIFEST.txt`'s leg-10 row is stale: current `leg-10.md` sha256 `6cd389e9…` ≠ manifest `c89eea7a…`; EX10 sections appended 21:14 post-date MANIFEST (21:02) and CA6 (21:07), so CA6:8,10's L10 hash held only pre-21:14.
- L3's display defect is not reproducible at this snapshot: block bytes equal `/tmp`, `sha256(block+LF)=5c682099…` = claimed; RE1:9's `ac7470f9…` reproduces exactly the `prompts:{}` variant — repaired (mtime 20:59:03) or a stale read.
- Receipts are untracked (`git ls-files` empty); the pending 79th-entry landing moves no box.

## VERDICT
FINDING: final boxes `[~]` ×4, no promotion; refresh MANIFEST's leg-10 row and the two stale `PROVINCE.md` pointers.
