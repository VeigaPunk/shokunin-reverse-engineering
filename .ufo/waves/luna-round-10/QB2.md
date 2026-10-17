## CLAIM
Gate DB4's final ledger: every item's status resolves to evidence, and its declared merge (D1–D6 + DB1–DB3 + DB5) retains its sources' carried items.

## METHOD
Read DB4, its merge sources, rounds 1–9 reports, GB5, QB3, CB8, SHONEN, PROTOCOL. Independent re-checks at HEAD `c343939` (tree clean): `git show --numstat` on all nine records commits; JSON scan of the 13 kaidoku MANIFEST rows; `sha256sum .ufo/waves/luna-round-2/receipts/L7-mcp-tools-6.5.0.txt` → `dc740c46…`; grep of l7-06 → 0; seat counts r4–r9; sed of N3:5, PROTOCOL:447, SCORECARD:68-72/576-589, r2:244, r3:60/136, sibling lines; DB4 grep per omitted item. No probes; sole write this file.

## FINDINGS
- Statuses backed; numbers exact. SCORECARD deletions r1 40/4, r2 60/8, r3 55/7, r4 46/1, r7 32/1; LOG 0 nine/nine; r4 disclosure `SCORECARD.md:71-72`; `PROTOCOL.md:447` binds LOG only. MANIFEST: 7 enum+prose values/6 rows (:1509,:2791,:2805,:2819,:2846-2847,:2860) + 3 `verified` rows (:1522,:1535,:1548) — DB4's split exact. B2.md:10 `a910c6…` vs `dc740c46…`; :68-72 pointers stale vs README:177/:138; r7 six headings + C9 literal absent; r9:55-56 VB3; r4:55-57 C05; r5:30-31 jmp*; r8:37-38,:42-44; r3:60,:136 bleed; :107-109 (SCORECARD:79); r6:53-67 AC2/custody; r7:55-56 SC1–SC6; SCORECARD:576-589 retest; /tmp 16 roots=1,096,013,272 B (N3:5); Tameshi :35,:73,:102 and tsukuroi :42,:70-71 resolve; retirements backed (r2:244; r9:19-24; r4/r5; r8:42-44).
- Merge gap: the stated merge drops carried items its sources name — GB5:11-15 (4 untracked `.ufo/interactive-sessions/` files, `/tmp/probe*.log`, r14-01/02 content debt, r8 pre-repair `/tmp` audit copy, r6 L9/L10), CB8:9 (RV5 lane-A manifest L1-only), DB1's misnamed `R2-reviewer-readme.md`, C4 unpersisted census, R4 no-peeking, S2 pointer-style, G9 dates, D3/DB3's :77-80 staleness. DB4 grep: 0 hits each.

## THREATS
Record-based; no wire re-parse or /tmp inspection; merge as-of 22:48. Today's-byte hash ≠ provenance. Scope bounded by DB4's declared sources; later seats may supersede.

## VERDICT
FINDING: all listed statuses are evidence-backed, but the stated merge omits ≥10 carried items (GB5:11-15, CB8:9, DB1/D3 lists) — not yet a complete final ledger.
