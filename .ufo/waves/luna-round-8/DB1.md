## CLAIM
Legs 1-5: every claim in PR1's battery table (`PR1.md:10-14`) is derivable from the receipts. PR1's L2-L5 rows are stale ("Pending") although landed receipts support exact matches; the documented leg-3 "display-layer corruption" does not reproduce in file bytes.

## METHOD
Read-only: recomputed sha256 of `receipts/leg-1..5.md` against `receipts/MANIFEST.txt`; extracted each displayed stdout block and recomputed its digest; parsed leg-2's raw stdout JSON and diffed names against `leg-2-tools.txt`; `cmp` against `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`; reproduced RE1's `ac7470f9…` variant by deleting `"listChanged":true` from `prompts`. No probes, no tracked-file edits.

## FINDINGS
- **L1** fully derivable: cited `receipts/leg-1.md:3-11` carries command, stdout `6.4.0`, empty stderr, exit 0; `printf '6.4.0\n' | sha256sum` → `37543669…bcafd` = claim; file hash `af959f64…` = MANIFEST.
- **L2** fully derivable, PR1 says Pending: raw stdout block (`leg-2.md:12-13`) sha256 → `0bbe6bc7…` = claim; parses to exactly 170 unique tool names; `leg-2-tools.txt` (170 lines) byte-identical in name+order; serverInfo `rea` `6.4.0`.
- **L3-L5** derivable, PR1 rows stale: each block recomputes to its claimed digest (`5c682099…a569`, `0fbd3bd0…0d5f`, `adfb7370…b115`); each call id 2 returns `{"code":-32602,"message":"Tool <name> not found"}` (`leg-3.md:22`, `leg-4.md:13`, `leg-5.md:9`) — the predicted TYPED-REFUSAL (unknown tool); all six 6.5-only names absent from the 170-list.
- **Leg-3 defect not reproducible**: block is byte-identical (`cmp`) to the surviving 623 B `/tmp` mirror and hashes to claimed `5c682099…a569`; file mtime `20:59:03` predates RE1's `20:59:42` read; `ac7470f9…2223` reproduces only when `"prompts":{"listChanged":true}` is replaced by `"prompts":{}` — bytes absent on disk. Reader artifact, not file corruption.

## THREATS
Derivability rests on retained files, not re-execution. Legs 4-5 assert a 240-second ceiling without showing `timeout 240` (contrast `leg-1.md:3`); leg-2 ran under RV1 client identity/cache (`leg-2.md:1`) with protocol 2025-03-26 vs 2024-11-05 on L3-L5. `-32602` is spec code "Invalid params" repurposed as unknown-tool. Stale PR1 rows are a known seat artifact, not counter-evidence.

## VERDICT
FINDING: Legs 1-5 claims all receipt-derivable; PR1's L2-L5 rows are stale; leg-3 display defect is a reader artifact — on-disk bytes verify.
