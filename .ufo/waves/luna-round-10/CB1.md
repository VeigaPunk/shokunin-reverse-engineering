## CLAIM
The arc should not be declared complete. A "complete" verdict would assert two invariants the arc's artifacts refute; round 10 cannot cure either, only disclose: (1) records append-only — five of nine records commits delete pre-existing SCORECARD text; (2) the wave seat contract — five of nine rounds under-delivered their nominal roster, with round 6 capped at 127 named seats (no 64th luna name existed in any dispatch array).

## METHOD
Read-only. `git diff --numstat <work> <records> -- LOG.md SCORECARD.md` across all nine luna records commits (`2abd30f5→a4bd355` … `40162fc→6e83a20`); `git diff --unified=0` spot checks; `MANIFEST.json` kaidoku rows parsed with python; read `.ufo/waves/luna-round-6/BC6.md`, `SHONEN.md`, sibling files read-only. No probes, network, or deletions.

## FINDINGS
- SCORECARD deletions per records commit: r1 4, r2 8, r3 7, r4 1, r7 1; r5/r6/r8/r9 and post-round `c343939` append with zero deletions. LOG.md: zero deletions in all nine. `a4bd355` replaces the live coverage row ("9.72 → 9.72 … r1 measurement; no coverage change" → luna-round-1) and deletes the Open-gaps coverage bullet; `6e2ee8f` deletes that row text again. Lane A's round-1 seat (`W1.md`) never checked append-only, so its r2/3/4/7 rewrite census missed the first instance; lane-B `WB1`/`WB3` reach it independently.
- Seat contract: `BC6.md:2,16,25` — "127 named seat reports"; "The 128-seat contract is unreachable by name: luna's 64th seat never existed in any array." MANIFEST notes record backfills in luna rounds 2 (58/64), 4 (58+6), 5 (58/64), 6 (127/128), 7 (59+5): five rosters are parent arithmetic, not executed seats. The defect recurred after four recordings; round 6's self-check "continues to miss".
- Corroborating uncured gaps: six prose-decorated axis values in five MANIFEST luna rows (8,9,10,12,13); SHONEN 4×`[~]`, no named non-author verifier; outbound sibling debt live — `tameshi-shokunin/corpus/knowledge/verification-patterns-fleet.md:35,73,102` carries the superseded `f(content, path, params)` universal with U4 unresolved; `tsukuroi-shokunin/PROVINCE.md:42` ADJ-06 still "kaidoku/revenger ownership unresolved".

## THREATS
The goal text is not in-repo (A6), so the criterion is read from lane artifacts; if adjudicated as "living rows may be updated", only the undisclosed rewrites (r2/r3/r4) remain defects — the r1 deletion count is a diff fact either way. Round 10's report and MANIFEST row do not exist yet and are not counted.

## VERDICT
FINDING: five of nine records commits rewrite SCORECARD (lane A missed the first) and five of nine waves missed their seat contract with round 6 capped at 127/128 — the arc can close only as "complete with disclosed nonconformances", never as conformant-complete.
