## CLAIM
At this snapshot, L1–L9 match their frozen predictions; L10 is not yet evidenced. A complete ten-leg score and the global battery claim remain unverified.

## METHOD
Compared the frozen rows in `.ufo/waves/luna-round-8/P0.md:7-15` with receipts 1–9, the full tool-name list, and the per-name checks. No probes or config edits; this is a receipt snapshot, not an independent runtime rerun.

## FINDINGS
- **L1:** exact match: stdout `6.4.0`, empty stderr, exit 0 (`receipts/leg-1.md:3-11`).
- **L2/L9:** `tools/list` reports `serverInfo` `rea` 6.4.0 and count 170 (`receipts/leg-2.md:5-9`); `leg-2-tools.txt:1-170` has 170 names. All six fixed-string, whole-word absence checks are empty/exit 1 (`receipts/leg-9.md:3-23`). Both predictions match.
- **L3–L8:** each exact requested name returned JSON-RPC `Tool <name> not found` (`-32602`), with server exit 0; L7 records `open_binary` success before `search_bytes` refusal. These are the predicted unknown-tool refusals (`receipts/leg-3.md:4,8-13`; `leg-4.md:5,12-14`; `leg-5.md:5,12-14`; `leg-6.md:11-13`; `leg-7.md:13-15`; `leg-8.md:10-13`).
- **L10:** `Glob .ufo/waves/luna-round-8/receipts/leg-*.md` returned legs 1–9 only; no control receipt is present. Current scored status is 9 matches, 1 pending—not a final score.
- **Protocol caveat:** L2 negotiated MCP `2025-03-26`; L3–L5 receipts use `2024-11-05` (`leg-2.md:5-9`; `leg-3.md:4,8`; `leg-4.md:5,12`; `leg-5.md:5,12`). This does not change their observed refusal class, but protocol mode was not held constant.

## THREATS
This audit does not establish zero config drift or unchanged command A/token set; `P0.md:15` requires separate checks. Receipt inventory is time-bounded and L10 may arrive later.

## VERDICT
FINDING: L1–L9 match, but L10 and the global invariants are unverified; MCP protocol negotiation also differs between the list and call legs.