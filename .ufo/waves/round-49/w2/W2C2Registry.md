# W2C2Registry — registry and snapshots as bytes (round 49 wave 2)

Landing revision `29883d4ec35a31a8393c4ffb220888c44c0bb022` (lane HEAD = same at report time). Freeze `decc5697…`. Run 2026-10-28T22:40–22:55Z. Clean checkout: `git clone --shared <lane> $S/c && git -C $S/c checkout --detach 29883d4e…` (toplevel asserted). All counters run with `GIT_NO_REPLACE_OBJECTS=1`. Receipts: `.ufo/waves/round-49/w2/W2C2Registry/`.

## Verdict

**The landed registry bytes hold. No defect in S138/S139/S145–S149, the three snapshots, the search-log entries, or the lesson's registry claims.** Every item in the brief passed on a clean checkout. Findings are all instrument limits (what the census and the frozen C2 counter do not see), none touching landed text.

## Brief checks (all passed)

| # | Check | Command (abridged) | Result |
|---|---|---|---|
| 1 | Census awk lines from `/home/vgpnk/Projects/shokunin/CORPUS.md:135-148`, run in clean clone | row count; `NF!=13`; tier hist; status hist; dup ids; enum/tier-inflation; used-by paths | rows **149**; NF!=13 **0**; `A=138 B=7 C=4`; `mined=141 rejected=8`; dup ids: none; enum: none; used-by missing: none. Output `census-awk.txt` sha256 `306961c8ca33925aa124ab3df35227a7a8338f29b27b317973a872ba54f7aa65` |
| 2 | `sources-census.sh validate --file $S/c/corpus/SOURCES.md` | | **exit 0**; 15 `W04` (S033…S142, identical set to `l1/sources-census-start.txt`), final `ok`; stdout sha256 `ba3b86f8d232e303ee299a1831fe171269256933764468f8a86965ad5400a2af` (contains scratch path on the `ok` line); stderr empty |
| 3 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | reads the lane **worktree**, not the clone; worktree == rev for `corpus/SOURCES.md` and `corpus/evidence/round-49` (`git diff 29883d4e -- …` empty) | **exit 0**, same 15 W04 + `ok`; stdout sha256 `065a45eb8e760d65d76e55e35e49efc44ee47466c1ffa147205757ea2589a2ea` |
| 4 | Snapshot sha256 vs pins | `sha256sum corpus/evidence/round-49/c2/*` | popper.html `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207` 118135 B = S147 pin; sysexits.html `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` 12725 B = S148 pin; freebsd-sysexits.html `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` 59251 B = S149 pin. Byte counts in the rows match too |
| 5 | NF=13 and no `\|` in a cell, S145–S149 | `awk -F'\|'`, pipe count per row | all five NF=13 (12 pipes each); whole registry: all 149 rows have exactly 12 pipes; escaped `\|` in S145–S149: 0 |
| 6 | S145/S146 vs `e4f2cfa5…` | `git show e4f2cfa5:corpus/SOURCES.md \| grep '^\| S145 ' \| sha256sum` vs clone | S145 `a41d8a522b39f6a3a10a0de69b563e072b606a4ef66a2fd9c9820425e750f954` both; S146 `b28ff60c773088b28a2ac2762d27d0ecf500013464867c2c6d6a11e90efa7e61` both → **byte-identical**. `e4f2cfa5` is an ancestor of the rev |

## Beyond the brief (also passed)

- Diff `e4f2cfa5..rev` of SOURCES.md: S138/S139 differ only in the `used-by` cell (field 12; r49 entry appended); S147–S149 added; two search-log entries added; nothing else.
- Quotes re-derived from the snapshots (tag-stripped text): S147 quote 1 (21 words) and quote 2 (9 words) present once, both between `2. Backdrop to Popper’s Thought` (offset 8872 body) and `3. The Problem of Demarcation` (12986); `2. The Problem of Demarcation` (S145's locator) occurs **0** times — lesson closure ruling confirmed; SEP `substantive revision Fri Jul 31, 2026` present. S148 quote (9 words), `6.19`, `2025-09-21`, `2026-09-09`, `SYNOPSIS` present; S149 quote (7 words), `DESCRIPTION` present. The "used incorrectly" gloss in S148's teaches is present in both the 3head page and the FreeBSD page (no leak from the rejected row).
- Live re-fetch 2026-10-28: popper 200/118135/`2c2d48c6…`; 3head 200/12725/`d9db4b96…`; FreeBSD 200/59251/`1fc793a2…`; `sysexits.h.3.html` 404/196 B/`80c3fe2a…` (S146's pin) — all match.
- Row refs `corpus/SOURCES.md:151` / `:152` in S147/S148 are correct line numbers at the rev (S145 line 151, S146 line 152).
- Search-log arithmetic: round-48 late entry rows 144→146 (2/2/1/1), round 49 146→149 (3/3/2/1): consistent with the registry; lesson's `grep -cE '^ {0,3}\|…S[0-9]{3,}'` gives 146 at `e4f2cfa5` and 149 at the rev.
- No tab/CR/NBSP/zero-width/bidi characters in the SOURCES rows; non-ASCII in S145–S149 only `—` `–` `’` `§`. Lesson line 34's tab is a quoted TSV line.
- `l1/sources-census-start.txt` and `…-end.txt` are in git at the rev and are byte-identical (sha256 `653a3be854ae6f923dceb33d412ad0615a213fedcc6e4ae1f0a10b03a7890c96`, each ends `exit=0`); my run reproduces their content. The files carry no row count; the lesson's "149 rows after landing" is true but not in the receipt.
- Frozen counters re-run: C2 (`c2-mismatch.py`, no battery) at the rev in a shared clone: exit 0, `atoms_total 9`, `mismatches 0`, stdout sha256 `5f403b7479a9ee5a657c550079b5fbf54d53fe59c6d63d9e311dbaaec785be6c`. (Battery not run here; other seats own it.)

## Findings (instrument limits; none is a landed-text defect)

Mutation method: 16+3 single-point mutants of a copy of SOURCES.md run through the awk lines + `validate` (`mut-results.txt`, driver `m.py`/`run1.sh`); 20 single-commit mutants in a `--shared` clone (identity set in that clone only) run through the frozen `c2-mismatch.py --rev <mutant>` (`c2-registry-mutants.txt`, `drive.py`).

| ID | Finding | Evidence |
|---|---|---|
| F1 | **Frozen C2 counter does not cover S149 at all.** A wrong sha pin in S149 (R3), a +1-byte tamper of `freebsd-sysexits.html` (R4), and S149 tier C→A (R17) all score exit 0, mismatches 0. Consistent with the plan (C2 reads rows S145–S148, plan line 25) but the S149 pin, snapshot and tier are then verified by nothing committed; I verified them by hand above. | `c2-registry-mutants.txt` R3/R4/R17: `exit 0 \| mism 0` |
| F2 | C2 does not check S147 `recheck` (R20 `365d`→`on-request`, exit 0) — only kind/tier/status/opened. | R20 |
| F3 | Census `validate` `supersedes` is a bare mask: any `supersedes` text in teaches suppresses E04, target unchecked. `supersedes S999`, `supersedes S146` (wrong target) and `supersedes S147` (self) on S147 all give exit 0 / `ok`. Without it S147 raises `E04 duplicate url plato.stanford.edu/entries/popper` (so the mask is load-bearing for S147). The landed S147/S148 targets are correct; C2 A6/A7 pin the target text (R9). | `mut-results.txt` V1–V3, M10 |
| F4 | Census cannot see content tamper in a sourced row: S147 sha flip (M7), S145 locator edit (M12), S148 URL `.htm` (M15) all exit 0 clean. The frozen C2 does catch these (R1 R2 R5 R6 R14 R15 R18 R19 red on exactly one atom, R6/R18 via "S145 was rewritten (append-only)"). | M7/M12/M15; R1–R2, R5–R6, R14–R15, R18–R19 |
| F5 | A row indented 4+ spaces (M16, S149) silently leaves the census: rows 149→148, exit 0, no finding (documented parser behaviour; C2 R12 catches a deleted row via A8 derived counts). `recheck=tomorrow` is accepted as a symbolic cadence (M8 exit 0). | M16, M8 |
| F6 | S146's `teaches` still lacks the `REJECTED: <reason>; flip:` shape; no census code checks it (W02 only flags thin teaches). Disclosed in lesson as open; append-only. | row S146 field 8 |
| F7 | Cross-counter check: C1 (`c1-counter.py`, `--rev` = commit that removes the r49 entry from S138 `used-by`) → exit 1, `carriers_matched 4`, only `sourced` false, `opened_source_rows ["S139"]`, `frozen_path_changed []` — so C1 does guard S138/S139 `used-by` (C2 does not, R13 exit 0, correct by plan). 11.6 s wall. | `c1-r13.out` |

C2 mutants R1,R2,R5–R12,R14–R16,R18,R19 each red with `mismatches 1` on a single atom (A6 or A7; A8 for R8/R12); R3,R4,R13,R17,R20 green (F1/F2; R13 is C1's clause).

## Not run

C2 `--battery`; C1 data re-run at the rev (only the R13 mutant was scored); wave-1 reports; PROVINCE/README/QUALITY/SCORECARD text beyond S-id greps.

## Tooling

No installs. Scratch `/fast/scratch/hyaku/kaidoku-r49/W2C2Registry` removed after copying receipts.
