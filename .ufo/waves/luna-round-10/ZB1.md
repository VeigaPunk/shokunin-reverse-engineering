## CLAIM
Independent final-disposition list for the kaidoku luna arc (rounds 1–9), diffed against lane-A merge seat R8 (`.ufo/waves/luna-round-10/R8.md`). All 57 lane-A notes read; load-bearing claims re-verified first-hand.

## METHOD
Read all lane-A seats, then verified from primary sources: `git diff --numstat` per records commit; parent `../MANIFEST.json` rows 5–13 parsed as JSON; `BC6.md`; `SHONEN.md`; `git show 3395b6d:corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md`; recomputed the B2 receipt SHA-256; read tameshi/tsukuroi files read-only; re-ran the `SCORECARD.md:92-123` Command A recipe at the real HEAD `c343939`.

## FINDINGS
Dispositions; Δ = diff vs R8.
- D1 Append-only: five of nine records commits rewrite existing SCORECARD text — r1 `a4bd355` (−4), r2 `a9580eb` (−8), r3 `0772d54` (−7), r4 `cfc84c2` (−1), r7 `6e2ee8f` (−1); LOG deletions 0 everywhere; r5/r6/r8/r9 clean. Δ: r1 is absent from R8's "rounds 2, 3, 4 and 7" list.
- D2 MANIFEST: six prose-decorated values across five luna rows (`:2791,2805,2819,2846-2847,2860`); the leading token is the enum. Δ: R8's "six fields in five rows" is exact; "six rows" would be imprecise. Pre-luna rows `:1506-1550` also carry non-enum `verified (…)` prose and `train+audit` types (P2) — visible, outside luna scope.
- D3 Dispatch: r6 closed at 127 distinct seats (63+64; the 64th luna name never existed, `BC6.md:16-18`). Short-counts r2/r4/r5/r6 are labelled 1st–4th; r7 (59+5) is arithmetic-inferred, never labelled. Δ: say "four labelled plus one inferred", not "five labelled".
- D4 Outbound, sibling-verified read-only: Tameshi's `verification-patterns-fleet.md` still cites superseded QUALITY #14 and leaves U4 open, while #15 supersedes it (`SCORECARD.md:353-357`) — append-only correction owed by that owner. tsukuroi `PROVINCE.md:42,70-71` and `adjacency-handoffs-fleet-r1.md:54` leave ADJ-06 kaidoku/revenger ownership with the protocol integrator. Δ: R8's outline omits both items.
- D5 SHONEN: 4×`[~]`, no named non-author verifier (`SHONEN.md:5-12`). Δ: R8 agrees.
- D6 Debt chain: D4 raced D1–D3; D6 raced D4 (`D6.md:5`, exit 2); D1–D6 now all exist and D5's B2 hash mismatch is confirmed (claimed `a910c6…`; actual `dc740c46…`). Δ: R8's "D5 absent" is a stale snapshot, not an error.
- D7 Command A at the real HEAD `c343939` (append-only +16/+12): 79/79, 9/9, 10.0/10.0, identical to round 9.

## THREATS
Record-based; no live probes; MANIFEST read-only; K1 sibling claims read as text only; R8 and lane-A seats were measured before `c343939`; domain semantics unverified.

## VERDICT
FINDING: R8 confirmed on enums, SHONEN, and r6's 127 seats; correct it to five records-commit rewrites (add r1) and four-labelled-plus-one-inferred short-counts; fold K1's two outbound items into the closeout list.
