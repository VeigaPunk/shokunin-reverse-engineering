# Round 99 — lesson: an exit 0 must mean the packer agrees, and a self-assessment row is checked against the bytes it names

Base `de098f51cd73d3b9b4a895840da8f2bb0a386db8`. Freeze `8fb5ac4fa8d7b0cb5123b230e5d319a765011066` (`plans/round-99-claims.md`; frozen counters `tools/round-99/self-assessment-audit.py`, `tools/round-99/pe-upx-trunc-battery.py`; red fixtures `tools/round-99/forgeries/`; C1 controls `.ufo/waves/round-99/pre/`). C2 controls scored at the freeze and committed at `5f08a78fb3b62c567a92b35c70e3ac76fa003100`. C2 candidate `01c4b79cc1cf8e6172b507edebb6a4d3125c5c6f`. C1 landing `64cc3e10c5d615c6454570674a265b7290b8919c`. C2 knowledge landing `c19d57cd2e65a036478b9e78f6c5397dedfb2bcb`.

## Motive

The round-98 non-author closure routed five defects (`corpus/lessons/round-98-verifier-spotcheck.md` §5). Two are self-assessment failures: the SCORECARD coverage head claimed 10.0 at 168/168 while the round-66 stem recipe observed 176/182 (six r93–r97 entries unmapped), and nine round-97/98 tools had no registry row (D1). Two are about the PE repair: its exit 0 on a pack truncated inside its sections (`ok intact` where `upx -t` fails), three rc-1 CLI crash paths, and a frozen battery that admitted the wave's forgeries because every carrier had its PackHeader at 992. R99-C1 takes the self-assessment (calibration); R99-C2 takes the truncation frontier (coverage), with the forgeries committed as red fixtures before the candidate landed.

## Verdict first

- **R99-C1 — met on the frozen predicate.** Base: `mismatches 17; head-score mismatch; head-fraction mismatch; map-rows 176 of 182; registry 0 of 9`, exit 1 (`.ufo/waves/round-99/pre/c1-do-nothing-at-base.json`). At `64cc3e10`: `mismatches 0; head-score ok; head-fraction ok; map-rows 182 of 182; registry 14 of 14`, exit 0; at `c19d57cd`: `map-rows 183 of 183; registry 14 of 14`, exit 0 (`.ufo/waves/round-99/l1/scores/c1-at-*.json`). The forgery control (prose tokens, stem-only rows, head edited, path-only registry rows) scores `mismatches 15`, exit 1, while the round-66 recipe alone reads its head atoms as ok. **Named discrimination limit:** CriticC1 reached `mismatches 0`, exit 0, from base with about eleven lines (nine registry rows carrying the true sha256 and false prose, one filler map row, one duplicate head row above the real one; `w1/CriticC1.md` F-ALL), and a phantom map row naming a non-existent entry passes at `64cc3e10` (F-PH; the round-66 stem recipe catches it as `dangling`). The counter certifies presence and shape, not truth. The substance was checked outside the predicate: ExecReproC1's independent recount agrees at B0, A and Bk; CriticC1 and ReviewerAudit read the six map rows as true; ScribeLesson found three landed registry rows contradicted by their tools' own source (M99-i), corrected after measurement in the integration commit and re-measured there.
- **R99-C2 — met on the frozen predicate.** At `01c4b79c` and again at `c19d57cd`: `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79`, exit 0 (`.ufo/waves/round-99/l1/scores/c2-at-*.json`). Every control scored at the freeze exits 1 (`.ufo/waves/round-99/pre/c2-controls-at-freeze.txt`): the round-98 repair `truncated 0 of 40; cli 0 of 3`; identity; g2 refuse-all; g3 truncation-only; g4 fixed offset 992; g5 size cache; g6 lazy anchor; g7 over-refusal; g8 oracle-caller. **Named discrimination limit:** four wave forgeries also meet the full label (`w1/CriticC2.md`): fa keyed on the battery's two cut lengths, fb the last raw end without FileAlignment, fg/fg3 the packer called through `import os as o; o.system` (the static leg is a text screen). MutationC2 killed 7 of 25 single-decision mutants; 15 survivors are population blind spots (FileAlignment 0, two sections, c_len bounds, unaligned cuts, a stale `<out>.tmp`, …), 3 are equivalent. The substance rests outside the predicate: ExecHeldOut on nine unpinned carriers (432 cells, seeded random cuts and overlays) found SOUND 72/72, COMPLETE 360/360 refused, OVER-REFUSAL 0/432; ReviewerRepair found 72/72 byte-identical outputs to the round-98 tool on the non-truncated surface and no temporary leak; ScoutSources re-fetched both sources (same sha256) and found no earlier length check on tail truncation; ExecReproC2 reproduced every label.

## Gate

Sources (CORPUS.md rule 1; access date 2026-11-05, opened in this round):

| row | source | URL | access date | located quote (≤25 words) | decision |
|---|---|---|---|---|---|
| S326 (new, admitted, tier A) | UPX 5.2.0 `src/packer.cpp` (`Packer::checkOverlay`) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packer.cpp (44586 bytes, sha256 `ab274d672d0985fa92d83e8c9c867d62ff30a1f31d2fb0b919e6d8826b03e040`; copy `.ufo/waves/round-99/pre/s326-packer-v5.2.0.cpp`) | 2026-11-05 | "throw OverlayException("invalid overlay size; file is possibly corrupt");" (line 433, under the test at 432) | **admit**: the packer's own refusal of a short PE; grounds R99-C2's rule |
| S324 (re-read, `used-by` changed) | UPX 5.2.0 `src/pefile.cpp` | same URL and copy as round 98 | 2026-11-05 | "file_size_u - ALIGN_UP(isection[iobjs - 1].rawdataptr + isection[iobjs - 1].size, ih.filealign); checkOverlay(overlay);" (lines 3046-3049) | kept; `used-by` old `corpus/knowledge/2026-11-05-r98-pe-upx-tamper-repair.md` → new `…r98-pe-upx-tamper-repair.md, corpus/knowledge/2026-11-05-r99-pe-upx-truncation-refusal.md` |

Row cell hygiene: the first S326 draft quoted line 432's `||` test inside the table cell, which would split the row; the cell now describes the test in words and quotes line 433 only (the full lines stay in the knowledge entry, outside any table). Census before → after (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`): before exit 0, `kaidoku ok`, 230 rows (`.ufo/waves/round-99/pre/census-start.txt`); after: exit 0, `kaidoku ok`, 231 rows (`.ufo/waves/round-99/l1/census-end.txt`).

Search log: question — what does UPX 5.2.0 do with a PE pack shorter than its sections, and by which arithmetic? Identified 2 files of the packer's source (packer.cpp, pefile.cpp), both opened; included 1 new row, 1 re-read. Stop rationale: the throwing function and its caller's computation are both located.

## Mistakes

Each row: class · evidence pointer · captured-by · fix.

- **M99-a · a repair's exit 0 that the packer does not back (round 98, own).** `tools/round-98/upx-pe-repair.py` answers `ok intact`, exit 0, on 40 of 40 truncated cuts where `upx -t` fails (`.ufo/waves/round-99/pre/c2-r98-upx-pe-repair-at-freeze.json`, `truncated 0 of 40`). Captured-by: none in round 98 (the battery had no truncated arm; SentinelInputs found it after landing). Fix: QUALITY Row 200 and the round-99 truncated arm; shown able to fail — the round-98 repair exits 1 on it.
- **M99-b · tools landed without registry rows (rounds 97–98, own; closure D1).** Nine `tools/round-97/*.py`, `tools/round-98/*.py` had no `SKILL.md` registry row (`registry 0 of 9` at base). Captured-by: none (no gate counted registry rows per round). Fix: QUALITY Row 201 and atom A4 of `tools/round-99/self-assessment-audit.py`; shown able to fail at base and on path-only rows (forgery control).
- **M99-c · a strictness rule frozen against an imagined layout (own, this round, caught before freeze).** The first A3 draft required the stem in the entries column and a 40-character state cell; at base it reported 55 legacy rows as unmapped that are mapped in the README's other two row layouts (stem in the first column; short `held — …` states). Captured-by: running the draft at base before freezing. Fix: A3 counts any table row carrying the stem with ≥ 20 characters of other text; the frozen bytes are the second draft.
- **M99-d · a text screen that matches ordinary words (own, this round, caught before freeze).** The static leg first forbade the token `pty`, which matches `empty`. Captured-by: reading the token list before the freeze. Fix: `import pty`, plus `posix_spawn`, `os.fork`, `from os import` added.
- **M99-e · the candidate was dry-run before the freeze commit (own, disclosed).** The candidate was scored once in `worktree` mode before `8fb5ac4f`; the battery bytes did not change afterwards, and the landed score reads committed bytes. Captured-by: the plan's disclosure line. Fix: none claimed; recorded so a closure can weigh it.

- **M99-f · a frozen counter that reads part of its rule from the working tree (own, this round; ScribeLesson).** `tools/round-99/self-assessment-audit.py:54-59` imports `tools/round-66/coverage-selfcheck.py` from the working tree; mutating that file flipped the label at an unchanged `--rev`. Captured-by: none (QUALITY rows on byte binding speak of receipts, not imported rules). Fix: routed — a successor reads the imported rule with `git show <rev>:` and pins its sha256 in the receipt; not shown able to fail yet.
- **M99-g · both round-99 counters write `<json-out>.partial` with a plain `open()` (own; ScribeLesson).** A planted symlink there is followed (measured for both). Captured-by: QUALITY Rows 189/192 exist but were not applied to new counters. Fix: routed (mkstemp in the receipt directory, as v7/v8); the frozen bytes are not amended.
- **M99-h · a selftest banner printed as a literal (own; ScribeLesson).** `self-assessment-audit.py:198` prints `cases=9` whatever the case list holds. Captured-by: none. Fix: routed (print `len(cases)`).
- **M99-i · registry rows written for C1 were themselves false in three places (own; ScribeLesson, ReviewerAudit).** At `64cc3e10`: the craft-citation-v2 row said 14 selftest cases (the tool prints `cases=11`), the gen-forgery-fixtures row named a directory argument the tool does not take (it writes a fixed `OUTDIR`), and the audit row called itself read-only over `git show`. A4 checks form and the sha256, not truth (CriticC1 L1, L6). Captured-by: the wave's reading of each tool, not the counter. Fix: the three rows are corrected in the integration commit, two incomplete rows completed (refusal list of the round-99 repair; its FIFO/MemoryError gaps), and the C1 counter re-run on those bytes.
- **M99-j · a forgery control whose revision exists only in a deleted scratch clone (own).** `pre/c1-forgery-control.json` names fixture commit `e2502c3d…`, which is not in the lane; only the diff is committed. ExecReproC1 re-applied the diff and reproduced `mismatches 15`. Captured-by: ScribeLesson. Fix: a control's fixture is committed as a diff plus the re-application command (done here); a revision that cannot be fetched is not cited as the control's identity.
- **M99-k · a cited receipt left untracked between commits (own; ReviewerAudit M1, CriticC1 L7).** The SCORECARD head at `64cc3e10` and `c19d57cd` cites `.ufo/waves/round-99/l1/scores/c1-at-*.json`, which were committed only in the integration commit. Captured-by: ReviewerAudit. Fix: committed in the integration commit; the head's citation resolves from then on, not at A or Bk.

## Measured

| claim | before (at base `de098f51` or at the freeze) | after | command |
|---|---|---|---|
| R99-C1 | `mismatches 17` exit 1 | `mismatches 0` exit 0 at `64cc3e10` and at `c19d57cd` | `python3 -I -B tools/round-99/self-assessment-audit.py --root . --rev <rev> --json-out <receipt>` |
| R99-C2 | round-98 repair `truncated 0 of 40; cli 0 of 3` exit 1 | full label exit 0 at `01c4b79c` and at `c19d57cd` | `python3 -I -B tools/round-99/pe-upx-trunc-battery.py --root . --repair tools/round-99/upx-pe-repair.py --rev <rev> --work <scratch> --json-out <receipt>` |

Harm check: round-66 self-check at base `de098f51`: head atoms false (claimed 10.0, 168/168; observed 9.67, 176/182), `citation_resolved_rules 36`; at `c19d57cd`: both atoms true at 183/183 (10.0), `citation_resolved_rules 36` (`.ufo/waves/round-99/l1/scores/coverage-selfcheck-at-*.json`). Depth unchanged (36 rule blocks resolved). No claim row of an earlier round was edited; the stale head statement is kept in the row after `Previous:`.

## Wave `r99-w1` — seat results

Dispatch `.ufo/waves/round-99/r99-w1-dispatch.json` (validated under `ufo-wave-policy.json`, `counts {spawn 13, resume 0, total 13}`), ready `.ufo/waves/round-99/r99-w1.ready`, results `.ufo/waves/round-99/r99-w1-results.json` (13 settled, 13 reports). Roles: executor 3, scout 1, connector 1, scribe 1, reviewer 2, critic 2, mutation-tester 2, sentinel 1; attack seats 6 of 13. Reports in `.ufo/waves/round-99/w1/`.

- **ExecReproC1** — C1 labels at B0/A/Bk and the selftest reproduced; forgery control rebuilt from the diff (`mismatches 15`); own recount agrees on A3 and A4 at all three revisions.
- **ExecReproC2** — C2 label at L and Bk; round-98, g4, g5, g6 labels equal to the freeze receipts; 18 hand cuts at own offsets agree with `upx -t`.
- **ExecHeldOut** — nine unpinned carriers, 432 cells: SOUND 72/72, COMPLETE 360/360 (354 labelled `truncated`, 6 header-region cuts refused by the earlier structural gates), OVER-REFUSAL 0/432.
- **ScoutSources** — S326/S324 bytes re-fetched equal; the rule is the packer's own computation in table order; no earlier length check on tail truncation; no further primary source found (GitHub issue search for `invalid overlay size`: 0 hits), so no row drafted beyond a rejection note.
- **ConnectorOverlap** — no sibling overlap; seven consistency findings, F1 (five older frontier notes still list packed PE) and F5 (the r94–r97 map rows omitted the depth verdicts) fixed in the integration commit, F2 (Core wording wider than the pinned population) fixed, F3/F4/F6/F7 recorded.
- **ScribeLesson** — mistakes M99-f to M99-k (above).
- **ReviewerRepair** — no medium/high; 72/72 byte-identical to round 98 on the non-truncated surface; L1 non-power-of-two FileAlignment diverges from the packer's mask arithmetic (recorded as Frontier), L2 inherited phantom-section `ok intact`.
- **ReviewerAudit** — counter sound as specified; M1 uncommitted receipts (M99-k); low: A3 accepts filler rows, the round-66 import is not pinned.
- **CriticC1** — F-ALL and F-PH admitted (named limit above); landed substance true where read.
- **CriticC2** — fa, fb, fg, fg3 admitted (named limit above); the candidate differs from fa/fb on held-out cuts.
- **MutationC1** — 12 mutants, 7 killed, 5 survive (exit-map lookbehinds, kind gate, five-cell floor, missing-heading fallback, A3 prose gate).
- **MutationC2** — 25 mutants, 7 killed, 15 blind-spot survivors, 3 equivalent.
- **SentinelInputs** — 705 CLI inputs and 20000 in-process mutants: exit only 0/2 except V1 (a FIFO `--in` without writer blocks; killed at 20 s) and V2 (`--in /dev/zero` under a 1 GiB RLIMIT_AS raises MemoryError, rc 1); no stray files; symlink victim untouched.

## Named limits (routed to round 100)

1. C1 counter: registry prose unchecked (L1/L6), filler map rows (L2), first-match head row (L3), no dangling direction (L4), hard-coded round scope (L5); working-tree import (M99-f); predictable `.partial` (M99-g); literal banner (M99-h).
2. C2 counter: cut-pattern and no-alignment forgeries (fa, fb) — needs seeded random cuts, an unaligned-gap cut and a non-512 FileAlignment carrier; static leg evaded by aliasing (fg) — needs a process-level guard, not a text screen; 15 mutation blind spots; predictable `.partial` (M99-g).
3. Repair: FIFO hang and MemoryError (SentinelInputs V1/V2); non-power-of-two FileAlignment (ReviewerRepair L1); phantom section header (L2, inherited); payload corruption at intact length.

## Assimilation

`Assimilation: none` — `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` exists (`test -e …; echo $?` → `0`, 2026-11-05) but the claim cap is spent on the routed defects; no entry adopted, no staged row appended. `test -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin/considerthese; echo $?` → `1` (no directory). No `corpus/lessons/operator-*.md` exists.

## Routed defects from the round-98 closure

1. D1 registry rows — closed by R99-C1 (rows for all nine plus the five round-99 tools; A4).
2. D2 raw selftest outputs — done as housekeeping: `.ufo/waves/round-99/l1/selftest-v7.txt` (`SELFTEST cases=23 failures=0`, exit 0), `selftest-v8.txt` (`cases=24 failures=0`, exit 0).
3. Successor counters with forgeries as red fixtures, a non-992 carrier — done for R99-C2 (g2–g8 scored at the freeze; `sevenzip64dll` PackHeader at 517).
4. Truncated `ok intact` and the three rc-1 CLI paths — closed by R99-C2.
5. Stale coverage head and the six unmapped r93–r97 entries — closed by R99-C1.
6. Round-97 defects 2–5 and 7 — still open (not claimed; named in the plan's not-claimed list).
