# CC4 — leg 4 cross-lane comparison (lane B seat)

## CLAIM
Leg 4 (`inspect_rust_binary` on a real Rust ELF) agrees across lanes at outcome-class level: lane A's canonical receipt and lane B's BB4 receipt both return `RESULT`, matching the frozen L4 prediction. Each lane's stdout bytes are independently reproducible.

## METHOD
- Read-only receipt integrity: recomputed lane A stdout (`.ufo/waves/luna-round-6/receipts/leg-4.md`, fenced block + LF, 8113 B) → `bc4902f7…` = recorded. Recomputed BB4's embedded block (`receipts-B/leg-4.md` + LF, 7879 B) → `84d489f7…` = recorded; live `/tmp/rea-bb4` artifacts re-hashed: harness `84d489f7…`, server stdout `15564e67…`, stderr `568cb4c3…`, script `9b40bde4…` — all match.
- Carrier hashes re-verified on disk: `/usr/bin/rg` `d006acfe…` (= SC2.md:10), Signal `.node` `1b44ed53…` (= lane A receipt:19-21).
- Replay (disclosed non-blind, see THREATS): two MCP sessions `npx -y rea-agents@6.5.0 --mcp` in `/tmp/rea-cc4`, 240s budget, servers terminated on stdin close, exit 0, no orphans: (a) rg, protocol 2024-11-05 mirroring BB4; (b) `.node`, 2025-03-26 mirroring lane A. Raw stdout: `/tmp/rea-cc4/stdout-{rg,node}.raw`.

## FINDINGS
- Lane A: RESULT, `ev_0618e7…`, Signal `.node` (24,944,200 B). Lane B BB4: RESULT, `ev_9ea97685…`, rg (4,377,936 B). Cross-lane class agreement; both match frozen class.
- Byte reproducibility: my rg stdout sha256 `15564e67…` = BB4's server stdout (identical evidence_id); my `.node` stdout sha256 `bc4902f7…` = lane A's recorded stdout (identical evidence_id). Evidence IDs are content-stable across seats.
- Targets differ by lane: lane A's canonical receipt used Signal `.node` although SC2.md:8-10 declares `/usr/bin/rg`; BB4 used rg. Lane A's own audit already flags this (XA.md:12), so L4 agreement is class-level, not target-level.

## THREATS
My replay was non-blind — lane A's receipt was read during grounding, as the compare assignment requires; the replay evidences byte-determinism, not blind prediction. Both lanes share host, node, npx cache, toolchain (common-mode). Protocol-version difference (2025-03-26 vs 2024-11-05) is client-requested and server-echoed, not config drift; no config edited, no tracked file changed.

## VERDICT
CLEAN — leg-4 cross-lane class agreement (RESULT↔RESULT, both match prediction); receipts hash-verified; per-carrier stdout byte-reproducibility demonstrated; lane A's target deviation is pre-existing and flagged.
