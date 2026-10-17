# FB2 — receipt format audit

## CLAIM
All 10 lane-A receipts (`receipts/leg-1.md`…`leg-10.md`) carry the 5 required receipt fields: command, full stdout, stderr, exit code, stdout SHA-256 — the set fixed at `.ufo/waves/luna-round-8/RV8.md:2`, matching `.ufo/waves/luna-round-6/QA3.md:4`.

## METHOD
Read-only audit of the worktree (HEAD `6e2ee8f` + untracked wave files). Per receipt: line-anchored label greps; full reads of legs 1, 3, 4, 5, 6, 7, 8, 9; legs 2 (1.9 MB) and 10 (40 KB) via fence/label maps and 130-char-capped line views, never dumped. Cross-check: extracted each receipt's displayed stdout block (content lines between fences, re-joined with LF) and recomputed SHA-256 against its claimed stdout hash. Read `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B). No servers, no writes except this file.

## FINDINGS
5 fields present in 10/10; none missing. Field lines: leg-1:3/5/9/10/11; leg-2:1/10/15/16/17; leg-3:4/18/7/17/6; leg-4:4/9/7/8/6; leg-5:3/6/11/12/13; leg-6:3/15/21/12/13; leg-7:3-4/17/24/14/15; leg-8:3/15/21/11/13; leg-9:18-23 (per-name command / stdout `[empty]` / stderr `[empty]` / exit 1 / hash; summary :5); leg-10:3/12/18/23/24 plus repeats :30/42/51/58/59 and :63/72/78/83/84.
Hash cross-check: 10/10 claimed stdout SHA-256 values reproduce from the displayed blocks — leg-1 `375436…`, leg-2 `0bbe6b…`, leg-3 `5c6820…`, leg-4 `0fbd3b…`, leg-5 `adfb73…`, leg-6 `5bc135…`, leg-7 `866f8b…`, leg-8 `65d740…`, leg-9 `e3b0c4…` (empty string), leg-10 `61450b…` (block 2 `6abdf8…` also reproduces).
leg-3 correction: block content lines 21-22 + LF hash to the claimed `5c682099…` and are byte-identical to the /tmp file (`diff` identical). A mismatch appears only if the fence line is included (`2bebb011…`) or the trailing LF dropped (`225d67cc…`) — a hashing-convention error, not display corruption; no parent-side repair is needed.

## THREATS
- leg-9's stdout field is deliberately empty (`[empty]`; empty-string hash): present but contentless by design.
- leg-10 block 3 (:72-76) self-declares "incomplete transcription; not raw" and its displayed bytes hash `b2012fcf…`; its claimed hash at :84 repeats block 1's (which reproduces) — a labeled duplicate, not new evidence.
- `RV8.md:8-14` (leg-10 then absent) is superseded by this 10/10 audit; ~10 stale lane-A verdicts noted in round context are likewise superseded.
- Field labels vary cosmetically (FULL STDOUT / Full MCP server stdout / SERVER STDOUT); field presence, not byte-completeness of raw captures, was verified (no live probes authorized).

## VERDICT
CLEAN — 10/10 receipts carry all 5 fields and all 10 claimed stdout hashes reproduce; the leg-3 "display corruption" is not reproducible.
