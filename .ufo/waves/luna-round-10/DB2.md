## CLAIM
Ledger collector for kaidoku rounds 4–6: every named debt/carry item with its later evidence, plus the in-tranche record checks (SCORECARD append-only, MANIFEST enums, seat counts). Read-only at HEAD `c343939`.

## METHOD
Read rounds 4–6 reports, `LOG.md:715-814`, `SCORECARD.md:60-90,370-625`, round-9 wave F1/F2/R6/GB5, round-6 `BC6.md`, `MANIFEST.json:2760-2867`. Ran `git show --numstat cfc84c2 f0e8cde 411175e`; counted wave-dir seat files. No probes, network, or sibling edits.

## FINDINGS
**Closed at r5** (r5 report:11-39; `SCORECARD.md:417-448`): r1-asar framing, r4u-01 decimals, PROVINCE request-byte pin, r9-02 tension, r5-02 `~283`, r12-01 L197.
**Documented, unrepair** — census instrument limits (r4 F18; r5 comma/opener): `SCORECARD.md:576-589` ADJUDICATED-not-PASS, retest trigger; /tmp litter → operator hygiene (`:591-599`).
**Carried, no closure through r9** — C05 re-verification method (r4 report:55-57; `.ufo/waves/luna-round-9/F1.md:9`); both `jmp *` untested (r5 report:30-31; `corpus/README.md:177`); `SCORECARD.md:68-72` is itself stale at HEAD — its `:160`/`:128` pointers now hit unrelated rows (README has 187 lines; reconciled content sits at :177/:138) and r6–9 never updated it; r6 AC2 chronology (r6 report:66; `luna-round-9/F2.md:8`, `R6.md:9`); RV5 lane-A manifest lists L1 only (`.ufo/waves/luna-round-7/CB8.md:9`); L9 class-level evidence and L10 route detour (`luna-round-9/GB5.md:15`); BB7/BB8 custody recorded, originals unrecoverable (`luna-round-7/CB8.md:10`); SHONEN 4×`[~]` (`MANIFEST.json:2865`).
**Short counts:** r4 second (`SCORECARD.md:385-388`), r5 third (`:427-430`), r6 fourth + EX7 double-count → 127/128 (`:475-478`; `BC6.md:15-25`); r7 fifth (`:510-513`).
**Record integrity:** `git show --numstat` → cfc84c2 `SCORECARD.md 46/1` — mid-file hunk `@@ -65,9 +65,11 @@` rewrote the living row (`:157`→`:160`, disclosed in-row): append-only deviation. f0e8cde `50/0` and 411175e `36/0` (single EOF hunks); LOG 36/0, 33/0, 27/0. MANIFEST r4/r5/r6 verdicts append prose after enum tokens (`MANIFEST.json:2791,2805,2819`; 3 of the 6 flagged rows). Seat files on disk: r4 64 (`V27.md` misnamed V11a), r6 127, r5 **126 vs 128 claimed — unreconciled; no r5 wire audit exists**.

## THREATS
Reports are bounded; round-5's untracked dir is mutable, so 126 is a snapshot, not a roster. No wire audit for r4/r5 totals. "No closure found" ≠ proved open. Command A not re-run; the MANIFEST enum call belongs to the parent.

## VERDICT
FINDING: r4 records rewrote one living SCORECARD row (in-row disclosed deviation); r4–r6 MANIFEST verdicts are prose-decorated; r5 seat files 126≠128 unreconciled; carried items above lack closure evidence.
