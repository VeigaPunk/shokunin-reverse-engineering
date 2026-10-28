# R49-C2 plan <-> counter match — seat C2PlanMatch (wave 1, pre-freeze)

Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Drafts read-only. Dev clone built by `mkclone.sh`; no lane, fleet or draft file was written. Artifacts: `.ufo/waves/round-49/w1/C2PlanMatch/` (receipts, forgery runners and results, live-source bytes, `receipts/artifact-sha256.txt`).

## Verdict

**Not freeze-ready for C2 as drafted.** The arithmetic matches the plan (9 atoms, 11 mutations, `mismatches 9` / exit 1 at FREEZE, `mismatches 0` / exit 0 at the dev REV, battery 11/11, do-nothing 9 red, freeze-integrity exit 2). But:

1. Five forgeries that do not correct the record turn the counter green (`mismatches 0`, exit 0): a fabricated round-48 seat report (A4), a rewritten receipt with updated digests (A5), a rewritten non-author closure that keeps two tokens (A9), a re-declared SCORECARD freeze (A1), a 40-hex "unnamed" hash whose 8-hex prefix is named in LOG (A3), and a dropped LOG pointer key (A3). Two more pass: a fabricated search-log count (A8) and a self-authored snapshot with its row pin updated (A6).
2. A7's predicate is token presence (`\b64\b`). The inverted teaches "EX_USAGE is 2, not 64" gives `mismatches 0`. The battery only fails because the mutation no longer applies (`mutation set incomplete: 10 of 11`), not because A7 turns red.
3. Round-48 inputs (receipts, `.ufo/waves/round-48/w1/**`, results JSON, the round-48 closure file, the SCORECARD round-48 section) are read at REV, not bound to base. The plan's "each counter binds what it reads" is false for them.
4. Eight plan sentences disagree with the counter or docstring (table below), including "re-derived every number" for A8 and "one per defect class" for the 11 mutations.

Fix list (before the single freeze) is at the end. Items 1–3 are blocking; the rest are plan wording or disclosure.

## Commands and receipts (exit codes; stdout sha256 is over the printed JSON)

| # | Command (clone = `/fast/scratch/hyaku/kaidoku-r49/C2PlanMatch/clone`) | Exit | Observed | stdout sha256 |
|---|---|---|---|---|
| R0 | `bash .../draft/mkclone.sh <clone>` | 0 | `DEV_FREEZE=0ce6f7611c274955d626501ac576f94892e2daf9` (throwaway commit; hash not reproducible) | — |
| R1 | `python3 .../draft/c2-after.py <clone>` | 0 | `DEV_AFTER=895d2833837aacb06db96995a4090149e0d166e3` (dev GREEN fixture: lesson, S147/S148, search log, SCORECARD section) | — |
| R2 | `python3 -I -B tools/round-49/c2-mismatch.py --root <clone> --rev 0ce6f761… --freeze 0ce6f761…` | **1** | `atoms_total 9`, `mismatches 9`; every atom red for an *absent* correction (table F8) | `4aea754e1c24d0b22dee882bed2ca6ad85e4a572c5454f97b1147cc14fa27819` |
| R3 | same with `--rev 895d2833… --freeze 0ce6f761…` | **0** | `atoms_total 9`, `mismatches 0` | `0159e327b316df077eb9211fd453a3f435187ba45dd28097db35a7671b6566f1` |
| R4 | same with `--battery` | **0** | `mismatches 0`; `battery.failing []`; 11 mutations each `red == [atom]`, `noop []`; do-nothing red = all nine, `do_nothing_paths 5` | `ed346c986fd39ed95df3ff7d059d50128f06b0de5f840058d4c107241d5a293e` |
| R5 | counter sha256 (`draft/tools/round-49/c2-mismatch.py`) | — | `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f` (= `counter_sha256` in the JSON) | — |
| R6 | forgery battery (below), `forge/run.py`, `forge/run2.py` | 0/1/2 per row | see table F | results: `forge/results.json` `679c07ab…`, `forge/results2.json` `313eafb4…` |
| R7 | live re-open: `curl -sSL https://plato.stanford.edu/entries/popper/` and `…/man7.org/linux/man-pages/man3/sysexits.h.3head.html` (2026-10-28T21:15:03Z) | 0 | HTTP 200, 118135 B and 12725 B; sha256 `2c2d48c6…ec207` and `d9db4b96…340` — **identical** to the draft snapshots `popper.html` / `sysexits.html` and to the S145/S147 pins | — |

Plan files: `plans/round-49-claims.md` sha256 `984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492`. Clone-level dev commits are not reproducible; the freeze must re-run on the landed REV.

## Sentence table: plan vs counter

Key: AGREES / DISAGREES / UNCHECKED (the counter does not implement it, or the plan does not state it). `plan` = `plans/round-49-claims.md`; `ctr` = `draft/tools/round-49/c2-mismatch.py`.

| # | Plan sentence (plan line) | Counter location | Verdict | Evidence |
|---|---|---|---|---|
| P1 | "nine round-48 self-assessment mismatches … from the round-48 closure `Routed defects`" (118–119) | ctr 8–9 "one per defect … ('Routed defects') named" | **DISAGREES** | Routed defects are 8 items. A9 has no Routed source; it comes from the closure's per-axis calibration row and closure verdict. Item 8 bundles A2, A3, A5 plus out-of-set items (C2 receipt timestamp, cross-domain statement). |
| P2 | "evaluates nine atoms and counts those whose re-derivation disagrees with the record or whose correcting record is absent" (121–123) | `score` 490–498; `main` 622–624 | AGREES | At FREEZE all nine are "absent correction" reasons (F8). |
| P3 | "Atoms A1–A9 are listed in the counter's docstring, which is this claim's predicate verbatim" (123) | ctr 17–47 | **DISAGREES** | Plan 124–129 is a summary, not verbatim. Docstring 42 says "every number is re-derived from the registry"; code 463 checks only rows and included/excluded (see A8). |
| P4 | "with FREEZE an ancestor of REV and the frozen paths untouched" (131–132) | `freeze_check` 501–512; `Git.touched` 112–116 | AGREES | F_FREEZE_edit and F_FREEZE_restore both exit 2 `frozen_path_changed`. |
| P5 | "`--battery` reports `atoms_total 9`" (133) | `main` 621 | AGREES | R3/R4 JSON `atoms_total 9`. |
| P6 | "`mismatches 0`" (133) | `main` 624 | AGREES | R3/R4. |
| P7 | "each of eleven single-mutation overlays turns exactly its own atom red (and none is a no-op)" (134) | `mutations` 515–571; `battery` 574–598 (len check 579, `red == [atom]` 585, noop 582) | AGREES | R4: 11 entries, all `ok`, `noop []`. |
| P8 | "a do-nothing overlay (every path changed since FREEZE restored) turns all nine red" (135) | `battery` 589–597 | AGREES, weak control | R4: 9 red, 5 paths. Each red is an absence reason (`lesson line A1 absent` etc.), so the control cannot show content disagreement. |
| P9 | "and exits 0" (136) | `main` 625–630 | AGREES | R4 exit 0. |
| P10 | "At FREEZE … reports `mismatches 9`, exit 1" (135–136) | `main` 624–625 | AGREES on arithmetic; the meaning is UNCHECKED | R2 exit 1 mismatches 9; see F8 on what the nine measure. |
| P11 | Target "exit 0 with `mismatches 0`, `battery.failing []`" (138) | `main` 629–631 | AGREES | R4. |
| P12 | Counting command "before = FREEZE (9), after = REV (0)" (139) | — | AGREES on dev pair | R2/R3. Landed REV not yet built. |
| P13 | Controls "do-nothing at the freeze (`mismatches 9`)" (140) | — | AGREES; **UNCHECKED** receipt path | Plan names no C2 control receipt path; C1 names `.ufo/waves/round-49/controls/` (plan 96–104). |
| P14 | Controls "eleven mutations, one per defect class" (141) | `mutations` 515–571 | **DISAGREES** (wording) | 11 mutations for 9 atoms: A6 has two (549, 555), A7 has two (553, 559). |
| P15 | Kill rule: mutation leaves atom green / turns another red / overlay byte-identical → miss (143) | `battery` 582–588 | AGREES | `ok = red == [atom] and not noop`. |
| P16 | Disclosed limit "counter re-derives numbers and cross-references, it does not judge prose" (146) | A8 463 | **DISAGREES** (partial) | `identified`/`screened` are checked only as `idn >= scr == inc+exc`, not re-derived. |
| P17 | Disclosed limit "A8 counts the registry rows and the included/excluded split" (149–150) | `a8` 442–466, `_derived` 433–439 | AGREES | This is the honest version; P16/docstring 42 are the overclaim. |
| P18 | "Routed, not repaired: census2.json, record2.py" (147–148) | not read | AGREES | Out of counter scope. |
| P19 | Freeze text: "C2: `git log -m --diff-merges=first-parent` … plus the blob comparison" (36–37, 29–37) | `touched` 112–116; blobs 509–511 | AGREES | F_FREEZE_* exit 2. |
| P20 | "Every receipt records exit code, stdout sha256 and counter sha256" (37) | `main` 612, 631 | AGREES for exit code and counter sha; **UNCHECKED** stdout sha | Stdout sha is harness-side. |
| P21 | "C2 reads `corpus/lessons/round-49.md`, `SCORECARD.md`, SOURCES S145–S148 and the search log, `LOG.md`, and committed round-48 receipts" (23–27) | a1 237 (`corpus/lessons/round-48.md` at base); a9 477 (`…round-48-verifier-spotcheck.md`); a4 309–314 (`.ufo/waves/round-48/w1/**`, `r48-w1-results.json`); a6/a7 374, 411 (`corpus/evidence/round-49/c2/*.html`) | **DISAGREES** (incomplete) | The counter reads at least five further inputs the plan does not list. |
| P22 | Frozen paths: "Not frozen (each counter binds what it reads)" (168–170) | a4 309–314; a5 336–337; a9 477; a1 234 (SCORECARD round 48) | **DISAGREES** (binding gap) | Round-48 inputs are read at REV, not checked against LANE_BASE. F_A4, F_A5, F_A9, F_A1 all green. |
| P23 | "Neither counter reads a path the other's landing writes, except SOURCES … each is measurable at a REV with or without the other's landing" (22–27) | `_derived` 433–439; `a8` 447–450 | AGREES (current drafts); caveat | S138/S139 pre-exist at base (rows 144–145), so C1's edits do not change C2's counts. C1 drafts (`R49C1Doc`, `R49EntryDraft`) add no registry id and no search-log line (grep). Any new id, or a second `- 2026-10-28 round 49` line, turns A8 red. |
| P24 | Frontier: "R49-C2 adds S147/S148 from re-opened sources with committed sha256-pinned snapshots" (154–156) | a6 374–381 (pin); a7 411–428 | AGREES on current bytes; **UNCHECKED** provenance | Live re-open (R7) matches the snapshots byte-for-byte. The counter checks only the pin: F_A6_row_only is green. |
| P25 | Frozen paths list (`tools/round-49/` "including control-fixtures/**") (165) | — | UNCHECKED (C2) | C2 has no fixture file in `tools/round-49/`; its controls are in-counter. Acceptable if the plan says so. |

Atom-level sentences (plan 124–129 vs ctr 17–47 and the function):

| Atom | Plan summary (plan) | ctr docstring / code | Verdict | Forgery or evidence |
|---|---|---|---|---|
| A1 | declared-freeze header (124) | 17–20 / `a1` 229–256 | AGREES on lesson line; SCORECARD side **DISAGREES** (not bound) | F_A1_scorecard_redeclare: SCORECARD `## Round 48` set to `0ce6f761…`, lesson A1 matched → green. The round-48 lesson is protected (F_CTL_round48_lesson_rewrite → red, A1). Base witness: base `corpus/lessons/round-48.md:4` = `0f06251b…`, base SCORECARD `**Declared freeze:**` = `b6f7ca2a…`, so the defect exists at base. Section header `## Corrections to round 48` (ctr 74) is in neither plan nor docstring: UNCHECKED. |
| A2 | dead commit hash (125) | 21–23 / `a2` 259–275 | AGREES on the lesson line; **UNCHECKED** correction | Fleet report `.ufo/reports/round-48/kaidoku.md` still cites `663f30ee7516942a0120e7de68fe88356e680822` (2 occurrences, grep). A2 is green while the record it names is still wrong. The counter never reads the fleet report. |
| A3 | LOG.md pointer line sets (126) | 24–26 / `a3` 278–302 | **DISAGREES** | Keys use an 8-hex needle (294). Unnamed check uses the supplied string (299–301). F_A3_unnamed_8hex_control `33f65a91` → red (correct). F_A3_unnamed_40hex_fake `33f65a9100000000000000000000000000000000` → green. F_A3_drop_log_key (removes `log_33f65a91=…`) → green: no completeness check. Docstring "the hashes the round-48 entry never named" is implemented as "named nowhere in LOG at base" (299–301). |
| A4 | wave accounting (127) | 27–29 / `a4` 305–328 | AGREES on counting; **DISAGREES** on binding | F_A4_fake_seat_report: adds `w1/C1Battery.md`, lesson `reports=73 missing=C1Meaning,ScribeReportNumbers` → green. |
| A5 | receipt digests raw vs stripped (128) | 30–31 / `a5` 331–350 | AGREES on digests (341–342, 348); **DISAGREES** on binding | F_A5_receipt_rewrite: receipt `c1-final-33f65a91.json` rewritten, lesson digests updated → green. The fleet report's quoted digests are not read (quotes UNCHECKED). |
| A6 | S145 wrong locator → row S147 (128) | 32–35 / `a6` 384–406; `_snapshot_row` 353–381 | AGREES on row, pin, quotes, locator, used-by; **extra** constraints not in plan (370–371: kind `docs`, tier `A`, status `mined`, opened `2026-10-28`) | F_A6_forged_snapshot_row_only: `popper.html` replaced by fabricated HTML carrying the quote and heading, S147 pin updated → green. The first attempt also rewrote S145's pin and went red ("S145 was rewritten") — append-only works. S145's pin is not checked against the snapshot file. Live re-open shows the committed snapshot is currently genuine. |
| A7 | S146 wrong rationale → row S148 (128) | 36–39 / `a7` 409–430 | **DISAGREES** (predicate too weak) | Teaches check `'EX_USAGE' in c[6] and re.search(r'\b64\b', c[6])` (428). F_A7_inverted_teaches: "EX_USAGE is 64, not 2" → "EX_USAGE is 2, not 64" → `mismatches 0`. Battery exit 1 only from `mutation set incomplete: 10 of 11`. |
| A8 | search-log entries for rounds 48 (late) and 49 with re-derived counts (129) | 40–43 / `a8` 442–466 | **DISAGREES** (docstring 42 "every number is re-derived") | Rows and included/excluded are derived (449, 461, 463–465). `identified`/`screened` are only inequalities (463). F_A8_identified_inflate (`identified 2 → 40`) → green. |
| A9 | SCORECARD calibration record vs closure verdict (129) | 44–47 / `a9` 469–483 | **DISAGREES** (literal, not derived) | Checks a SCORECARD literal `calibration=harmed` (473–474) and two tokens in the closure (479, 481–482). F_A9_closure_rewrite: closure "Both claims verify…" → "Both claims FAIL…" (tokens kept) → green. The closure file is not bound to base. |

Counts check: 9 atoms (ctr 83, 486–487); 11 mutations (ctr 579 enforces exactly 11); 1 do-nothing overlay (ctr 589–597).

## F8: what "mismatches 9 at FREEZE" measures

All nine FREEZE reasons (R2 `atoms.*.why`): A1–A5 `lesson line … absent`; A6/A7 `lesson line … names no row`; A8 `0 matching search-log entries` for both rounds; A9 `SCORECARD … absent`. So the "before" count counts absent corrections, not the base defects. The base defects are real but unmeasured by the counter: base lesson `0f06251b…` vs base SCORECARD `b6f7ca2a…` (A1); fleet report still cites the dead hash (A2); base search log ends at round 33, `2026-10-23` (A8). Recommend a per-atom base witness evaluated at LANE_BASE, so "before" counts defects present in the base record.

## Forgery battery (clone forks from dev REV; counter run without `--battery` unless noted)

| Id | Change committed in fork | Result | Kind |
|---|---|---|---|
| F_A4_fake_seat_report | add `.ufo/waves/round-48/w1/C1Battery.md`; lesson `reports=73 missing=C1Meaning,ScribeReportNumbers` | exit 0, mismatches 0 | **defect** |
| F_A5_receipt_rewrite | c1 receipt `+ " \n"`; lesson `c1_raw`/`c1_stripped`/`report_c1` updated | exit 0, mismatches 0 | **defect** |
| F_A9_closure_rewrite | closure "Both claims verify…" → "Both claims FAIL…" | exit 0, mismatches 0 | **defect** |
| F_A1_scorecard_redeclare | SCORECARD `## Round 48` declared → `0ce6f761…`; lesson A1 matched | exit 0, mismatches 0 | **defect** |
| F_A3_unnamed_40hex_fake | `unnamed` adds `33f65a9100000000000000000000000000000000` | exit 0, mismatches 0 | **defect** |
| F_A3_drop_log_key | remove `log_33f65a91=3440,3441,3444` | exit 0, mismatches 0 | **defect** (completeness) |
| F_A8_identified_inflate | round-49 `identified 2 → 40` | exit 0, mismatches 0 | **defect** |
| F_A6_forged_snapshot_row_only | `popper.html` replaced with fabricated HTML; only S147 pin updated | exit 0, mismatches 0 | **defect** |
| F_A7_inverted_teaches | "EX_USAGE is 64, not 2" → "EX_USAGE is 2, not 64" (battery mode) | mismatches 0; exit 1 only from `mutation set incomplete: 10 of 11` | **defect** |
| F_A6_forged_snapshot (first try, both pins) | as above, but replaced every occurrence of the old sha, including S145's | exit 1, A6 red: "S145 was rewritten (append-only)" | control (append-only works) |
| F_A3_unnamed_8hex_control | `unnamed` adds `33f65a91` | exit 1, A3 red: "33f65a91 is named in LOG.md at the base" | control (correct) |
| F_CTL_round48_lesson_rewrite | `corpus/lessons/round-48.md` header changed | exit 1, A1 red (not byte-identical to base) | control (correct) |
| F_FREEZE_edit | append to `tools/round-49/c2-mismatch.py` | exit 2 `frozen_path_changed` | control (correct) |
| F_FREEZE_restore | edit, then restore to FREEZE blob | exit 2 `frozen_path_changed` | control (correct; restore does not un-block) |
| Battery A7 | (R4 dev) | 11/11 | control |

## Fix list before the single freeze

Blocking:
1. **Bind round-48 inputs to LANE_BASE.** Compare to base blobs for: `.ufo/waves/round-48/**` (receipts, `r48-w1-results.json`, the `w1/` tree that A4 counts), `corpus/lessons/round-48-verifier-spotcheck.md` (A9), and the SCORECARD `## Round 48` section (A1, or the whole section byte-equal to base). Add a forgery arm for each (F_A4, F_A5, F_A9, F_A1 above) to the battery. Correct plan 168–170 to name them.
2. **A7: replace token presence with the value.** Use `EX_USAGE\W{0,4}(?:is|=|:)\s*64\b` on the teaches cell and reject `EX_USAGE is 2`. Add the inverted-teaches mutation to the battery so A7 must flip. Plan 36–37 "teaches cell names EX_USAGE and 64" → "teaches cell states EX_USAGE is 64, not 2".
3. **A3: one needle, plus completeness.** Unnamed checks should use the same 8-hex prefix as the keys (`h[:8]`). Either require every hash the round-48 entry names to appear in a `log_` key, or reword plan 126 to "the stated hashes". Add the dropped-key and 40-hex-unnamed arms.

Plan or docstring fixes (non-blocking, but they change what is claimed):
4. **A8 "every number re-derived" (docstring 42; plan 129).** Derive rows and included/excluded only; say identified and screened are not derivable from the registry. Align plan 146 and docstring.
5. **Plan 123 "predicate verbatim".** Say the docstring (ctr 17–47) is the predicate; fix A9's "against the closure verdict" to "literal check of the two verdict tokens".
6. **Plan 118–119 and the A9 source.** A9 comes from the closure's calibration row and closure verdict, not Routed defects. Routed defects are 8 items; say which atoms come from which item.
7. **Plan 23–27 reads list.** Add round-48 lessons, the w1 tree, the results JSON, and the two snapshot files. Add the counter-enforced A6/A7 constraints (kind `docs`, tier `A`, status `mined`, opened `2026-10-28`) and the `## Corrections to round 48` header (ctr 74).
8. **Plan 141 "one per defect class".** Say "eleven mutations: one per atom, A6 and A7 with two each".
9. **A2 and fleet-report corrections.** The fleet report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kaidoku.md`) still cites the dead hash twice. State that A2 measures only the lesson line, and that the fleet correction is an L1 item the counter does not measure.
10. **A6 provenance.** Add to plan 146–150 that snapshot provenance is the lane's claim; the counter checks the pin and quotes only. Optional: a pin-consistency check for S145 against `popper.html`, so a forged row-only update is caught.
11. **F8 base witnesses.** Evaluate the defects at LANE_BASE (A1 `0f06251b` vs `b6f7ca2a`; A8 base log ends at round 33) so "before 9" counts defects, not absent corrections. If this is not done, plan 135–136 should say "nine absent corrections".
12. **Control receipts.** Name a C2 do-nothing receipt path (e.g., `.ufo/waves/round-49/controls/c2-do-nothing.json`), as C1 does at plan 96–104.

## Residual risk and gaps

- Not verified: the counter on a landed REV (no real lesson exists yet). All "GREEN" results come from my dev fixture (`c2-after.py`) and the forgeries built on it.
- The do-nothing control and the FREEZE count are absence-based (F8), so they do not test content disagreement.
- The live re-open proves only that the committed snapshots match the pages as of 2026-10-28T21:15Z. It does not verify SOURCES row prose beyond the two quotes and the EX_USAGE line.
- Tools installed: none. No pacman, no `~/.local/bin` writes. Disk guard: 37% used on `/fast/scratch/hyaku`.
- Scratch `/fast/scratch/hyaku/kaidoku-r49/C2PlanMatch` removed after receipts were copied; the forgery runners and results are in `w1/C2PlanMatch/forge/`.
