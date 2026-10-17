# QA8 — luna-round-6 LANE B | report-completeness

## CLAIM
At the 19:04:14 -03:00 snapshot, lane A holds 54/54 commissioned seat reports; lane B 34/58, with 24 seats in flight (list below). Against the round's nominal 64+64 neither lane was fully dispatched: lane A was commissioned 53 seats +1 backfill (XA), lane B 58 — so 16 of the 128 expected reports have no seat to produce them.

## METHOD
- Snapshot `date -Is` → 2026-10-16T19:04:14-03:00; top-level `*.md` in `.ufo/waves/luna-round-6` counted (`receipts*/` excluded).
- Expected sets from the parent's dispatch arrays in its session wire (`~/.kimi-code/sessions/wd_shokunin_8c4a99c6228c/session_5dcc2935-1c2e-430f-9636-758a86a8a6d4/agents/main/wire.jsonl`): lane A line 2684 (53 items; identical repeat 2781) + backfills 3036/3045 (EX7 completion, XA); lane B line 3062 (58 items). Python set-difference vs on-disk names; all 14 AgentSwarm calls scanned — no further dispatches.

## FINDINGS
- Lane A: 54/54 present (incl. EX7 completion 18:53, XA 18:58). No gaps.
- Lane B missing at snapshot (24): BB5, CC3, CC4, CC5, CC6, CC10, RB3, CB1, CB2, CB3, CB4, CB6, CB7, CB10, SB1, SB3, PB1, XB1, ZB1, QA2, QA4, QA5, QA6, QA8 (this file). Lane B lands ~1 report/minute; `receipts-B/` is already 10/10 legs.
- Structural: both dispatch descriptions say "64 seats" but the arrays hold 53 and 58 → at most 112/128; the 16 unreported seats were never named, so they cannot appear in a by-name missing list. Repeats round-5's recorded short-count defect, now in both lanes.

## THREATS
- Point-in-time: lane B is still writing and a parent backfill may add seats after this count; final completeness needs a re-sweep at wave close.
- Expected sets come from the orchestrator session wire, not a frozen manifest; a seat dispatched via another channel would undercount my lane-B set. Two identical lane-A calls exist (2684/2781); the commissioned name set is 53+XA either way.
- The lane-B missing list is a floor as of 19:04, not a final tally.

## VERDICT
FINDING: lane A complete (54/54); both lanes under-dispatched (A 53+1/64, B 58/64) — 16 reports cannot exist; lane B 34/58 in flight at 19:04:14.
