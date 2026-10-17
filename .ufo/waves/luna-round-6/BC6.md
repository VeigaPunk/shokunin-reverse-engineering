## CLAIM
Wave census luna-round-6: 127 named seat reports — luna 63, deepseek 64 — from the parent's own dispatch arrays; at this snapshot all 127 are on disk (125 at 19:47; BC2 landed, BC6 = this file). The 128-seat contract is unreachable by name: luna's 64th seat never existed in any array; both descriptions say "64 seats" but arrays hold 53 and 58.

## METHOD
Read-only; no tracked writes. Parsed every luna-round-6 AgentSwarm call in the parent session wire (`~/.kimi-code/sessions/wd_shokunin_8c4a99c6228c/session_5dcc2935-1c2e-430f-9636-758a86a8a6d4/agents/main/wire.jsonl`), extracted seat tokens from each call's `items`, diffed against `.ufo/waves/luna-round-6/*.md` stems. Ledger (wire line → description → array size):
- 2685, 2782 (identical duplicate dispatch) → lane A "64 luna seats" → 53 names
- 3037 → lane A backfill 1 → EX7 (re-dispatch; EX7 already inside the 53)
- 3046 → lane A backfill 2 → EX7, XA
- 3063 → lane B "64 deepseek-flash seats" → 58 names
- 3351 → lane A backfill 9 → AC1–AC9
- 3397 → lane B backfill 6 → BC1–BC6

Cross-checks: QA8.md (same wire, 19:04), XA.md (53-report scan, 18:58), PB2.md (54 lane-A files, 19:05).

## FINDINGS
- Named seats: 127 = luna 63 (53 + XA + AC1–AC9) + deepseek 64 (58 + BC1–BC6); no on-disk name outside the roster.
- Present now: 127/127 (deepseek gap filled mid-audit: BC1, BC3, BC4, BC5 at 19:43–19:45; BC2 after 19:47; BC6 = this file).
- Luna cannot reach 64: no 64th luna name exists in any dispatch array; the expectation "53 + EX7/XA + AC1–AC9 = 64" double-counts EX7.
- Reconciles with seats' own snapshots (QA8: lane B 34/58 in flight; PB2: 54 lane-A files = 53 + XA).

## THREATS
Roster source is the parent's session wire, not a frozen manifest: a seat dispatched outside this session would be invisible (QA8's caveat); all six round-6 AgentSwarm calls were scanned and totals reconcile to disk exactly — unlikely, not excluded. Snapshot 19:5x; late-arriving files would change the total; re-sweep at wave close. Duplicate 2685/2782 dispatched the same 53 lane-A names twice; seat-slot vs name-count readings differ there.

## VERDICT
FINDING: the wave names 127 seat reports, not 128 — luna 63 (not 64; EX7 double-counted) + deepseek 64; all 127 present.
