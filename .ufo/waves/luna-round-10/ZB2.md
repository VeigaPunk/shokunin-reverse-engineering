## CLAIM
On-disk lane-split counts for luna-rounds 1–10 (lane convention: seat-ID second char `B` ⇒ lane B; `.ufo/waves/luna-round-8/ZB4.md:5-8`, restated `.ufo/waves/luna-round-9/ZB2.md:5`) plus the arc's final seat tally. Rounds 1–9 frozen: 857 top-level `.md` files. Round 10, live at cutoff 22:47:14 -0300: 96 files (57 A + 39 B) of 128 nominal, lane B still landing (this report excluded).

## METHOD
Read-only; no probes, no tracked writes. HEAD `c343939` (see FINDINGS). Python stdin census (nothing written): per round `Path.glob("*.md")`, lane B=`stem[1:2]=="B"`, sorted-name SHA-256 prefixes; round-10 snapshots 22:44:56→22:47:14. Cross-read `SCORECARD.md:475-477`, `../MANIFEST.json:2756-2865` (kaidoku rows 1–9; no row 10), `-6/BC6.md:15-18`, `-7/BB5.md:2`, `-7/FINAL-MANIFEST.md:1,3`, `-10/W8.md:13`.

## FINDINGS
- Files / lane A / lane B (digest A|B): r1 64/64/0; r2 64/64/0; r3 64/64/0; r4 64/64/0; r5 126/69/57 `14d0ab8b|4b021e10`; r6 127/87/40 `7d02b65b|8e38d608`; r7 127/65/62; r8 100/52/48 `cc09c569|22cf030b` (= `W8.md:13`); r9 121/66/55, lane-A digest `1337a56a` = r9 `ZB2.md:9`'s static digest.
- r7 self-ID correction: `FINAL-MANIFEST.md` is seat BB1's artifact (`:1,3`), so r7 = 64 A + 63 B.
- Record vs disk (`MANIFEST.json:2756-2865`): r1–r4 64 ✓; r5 128 vs 126 (−2); r6 127 vs 127 ✓ (EX7 double-count, `BC6.md:15-18`); r7 128 vs 127 (BB3 absent; BB1–BB4 planned, `BB5.md:2`); r8 128 vs 100 (−28); r9 128 vs 121 (−7). Arc shortfall 38 vs 895 recorded.
- Convention validity: self-ID-certified r8/r9/r10; fails r6 — wire roster is 63 A + 64 B (`BC6.md:15-25`), name split gives 87/40 (24 lane-B names carry other prefixes). r5/r7 splits are heuristic-only; no roster/dispatch file on disk (find for `*roster*`/`*dispatch*` → empty; ZB4 r8 same).
- Round-10 progression (files/A/B): 57/57/0 → 60/57/3 → 65/57/8 → 74/57/17 → 96/57/39; lane A static (digest `554e818cf62e086f`).
- Arc to-date: 953 files vs 1024 nominal (4×64 + 6×128); 432 distinct seat IDs r1–r9, 456 through r10.
- HEAD is `c343939` (additive LOG+SCORECARD scaffolds, 22:42:01), child of the briefed `6e83a20`.

## THREATS
Point-in-time; lane B mid-flight (39 and climbing), so round 10 and the arc tally are lower bounds. Splits r5–r7 provisional. File counts do not prove dispatch or completion ("128 seats" ≠ "128 files", ZB4 r8 caveat). r2/r3 count 6 descriptive-suffix filenames (e.g. `S3-sentinel.md`) as seats. All top-level seat files are untracked; only 43 r6/r8 receipt files are tracked.

## VERDICT
FINDING: arc r1–r9 frozen at 857 on-disk files vs 895 recorded (r5 −2, r7 −1 = BB3, r8 −28, r9 −7; r6's 127 reproduces); r10 live at 96/128 (57 A + 39 B) at 22:47:14, lane B climbing.
