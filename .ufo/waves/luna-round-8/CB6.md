## CLAIM
Diff leg-9's six absent MCP names against `.ufo/waves/luna-round-2/A6.md`'s 6.5-only list; decide corroboration per name.

## METHOD
- sha256 recompute: `receipts/leg-9.md` = `8377d652…537c2ee` (matches `receipts/MANIFEST.txt:9`); `receipts/leg-2-tools.txt` = 170 lines. A6 receipts recompute to A6.md's cited hashes (`eec79d46…` 6.5.0, `2717c87b…` 6.4.0).
- Re-ran leg-9's exact probes `grep -nFw -- <name> receipts/leg-2-tools.txt`: all six rc=1, stdout empty, stdout sha256 `e3b0c442…`.
- Parsed A6's two MCP receipts (JSON): 170/207 names; leg-2-tools set-equals A6-6.4.0 (170); computed 6.5-only = 37 = A6.md list count, and A6.md list set-equals computed 6.5-only.
- Per-name membership: A6.md:8, A6-6.5.0 receipt, A6-6.4.0 receipt.
- Read round-8 `RE6.md` (stale early read) for context.

## FINDINGS
6/6 corroborated. Per name — in A6.md 6.5-only MCP list: 1; in A6-6.5.0 receipt: 1; in A6-6.4.0 receipt: 0; leg-2-tools replay: rc=1, empty. Names: `inspect_go_binary`, `inspect_rust_binary`, `inspect_electron_fuses`, `inspect_sqlite_database`, `search_bytes`, `inspect_with_objdump`. Kebab CLI counterparts all present in A6.md's CLI 6.5-only list (26 entries). `RE6.md:19,25` ("leg-9 not present / unverified") is superseded: both files now exist with matching hashes.

## THREATS
- Circularity: the six probed names were selected from A6's list, so agreement is consistency, not independent discovery; the new observation is leg-9's per-name absence against the round-8 6.4.0 list, whose set equals A6's 6.4.0 receipt (same pinned package lineage).
- A6's receipts are round-2 `npx rea-agents@6.4.0/@6.5.0` runs; no live probe run here, no fresh version claim.
- leg-3's display-hash defect does not touch leg-9 (hash recomputed clean).

## VERDICT
CLEAN: 6/6 corroborated per-name — all six leg-9 absences are in A6's 6.5-only list and 6.5.0 receipt, absent from both 6.4.0 lists, and leg-9's probes replay exactly.
