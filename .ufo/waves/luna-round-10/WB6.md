## CLAIM
Final adjudication of the arc's dispatch count defect: five short-count/backfill incidents (rounds 2, 4, 5, 6, 7) and round 6's 127-of-128 distinct-seat closure, verified from tracked records and wave artifacts at HEAD c343939. Read-only; only this file written.

## METHOD
Census `for d in .ufo/waves/luna-round-{2,4,5,6,7}; do ls -1 $d/*.md | wc -l; done` → 64, 64, 126, 127, 127. Roster spot-checks: r2's six named backfill seats all present (`S5.md` absent; landed as `S5-sentinel.md`); r6 holds `XA.md`, `AC1–AC9.md`, `BC1–BC6.md` (127 total); r7 holds BB2/BB4/BB5 + `FINAL-MANIFEST.md` (BB1, `:3`) + `receipts/census-final-B.txt` (BB3, `:1`) = 128 artifacts. Read round reports, `SCORECARD.md`, `LOG.md`, fleet ledger `../MANIFEST.json:2769,2796,2810,2824,2837`.

## FINDINGS
- Four incidents self-numbered: r2 FIRST 58/64 +6 (`.ufo/reports/luna-round-2/kaidoku.md:57-59`; `LOG.md:660`; `SCORECARD.md:283-286`); r4 SECOND (`.ufo/reports/luna-round-4/kaidoku.md:61-63`; `SCORECARD.md:385-389`); r5 THIRD lane-B 58/64 +6 (`.ufo/reports/luna-round-5/kaidoku.md:60-62`; `SCORECARD.md:427-430`); r6 FOURTH lane-A 53/64 (`.ufo/reports/luna-round-6/kaidoku.md:47-52`; `SCORECARD.md:475-478`).
- Fifth: r7 lane-B 59+5 (`.ufo/reports/luna-round-7/kaidoku.md:3-4`; `BB5.md:2,9`; `SCORECARD.md:510-512`) — never labeled a parent short-count in any record; name it in the closeout so 5-of-9 is explicit, not inferred (A4.md:8; D4.md:11 agree).
- r6: 127 distinct = luna 63 (53+XA+AC1–AC9) + deepseek 64 (58+BC1–BC6); the 64th luna name never existed in any dispatch array; EX7 double-counted on re-dispatch (`BC6.md:2,16-18`; fleet `MANIFEST.json:2824`). Disk holds 127/127.
- Disposition text for the closeout: "Five of nine rounds carried a parent dispatch-arithmetic shortfall repaired in-round by backfill — r2, r4 (58/64, +6), r5 (lane B 58/64, +6), r6 (lane A 53/64), r7 (lane B 59/64, +5; recorded without the label). Round 6 remains the only measured distinct-seat shortfall: 127/128, structural (the 64th luna name never existed); its operability admission stands separately. All disclosed in round records and the fleet ledger; the defect stayed ungated (r5's self-check still missed in r6). Carry visibly; do not infer seat-level repairs for r5/r8/r9 from seat-file counts (126/100/121) — not dispatch rosters."

## THREATS
Seat files are untracked and are not dispatch ledgers; r7's fifth-slot label is inference from the recorded 59+5 split plus BB5's arithmetic, not a self-recorded short-count. Fleet ledger lives outside this checkout. A late wave-10 seat could supersede.

## VERDICT
FINDING: five backfill incidents verified (r2/r4/r5/r6 self-named; r7 unlabeled fifth); r6 stands at 127 of 128 — carry as named, ungated process debt; never smooth.
