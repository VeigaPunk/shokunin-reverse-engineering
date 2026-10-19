# RV-7 cross-check — EX-11's baseline reproduction vs the round-1 recorded readings

Seat RV-7 · chain c2 · role reviewer · 2026-10-19. Question asked: does EX-11's
round-2 baseline reproduction agree with the round-1 recorded readings in
`.ufo/waves/arc3-loop1-round1/claims/c3/VZ-3/attack-log.txt` (companion full
capture `…/VZ-3/census-at-HEAD-vz3.txt`, sha256 `3b677b8e…`)? Discrepancies
listed at the end. All RV-7 runs are on byte copies in `/var/tmp/rv7-baseline`;
the repo tree was only ever read. Receipts: `claims/c2/RV-7/receipts/`
(MANIFEST.sha256).

## Inputs, pinned

| role | identity |
|---|---|
| round-1 rev | `e845c2b524ad2e59871e004c51a1386e192a74ab` |
| round-1 instrument | recovered `git show e845c2b:.ufo/gates/c1-census-v10.py` → `36e96cd5…`, 433 lines |
| round-1 scoped files | PROVINCE `d075a3c6…` 162 L · SCORECARD `30129a98…` 1336 L · SKILL `5c93c7c1…` 371 L |
| round-2 HEAD | `14b1682b1128d2e41085ebc79c9addeb8786d420` |
| round-2 pre-edit instrument | `6f1d19ff…`, 490 lines (== EX-11 `tools/census-pre-6f1d19ff.py`) |
| round-2 scoped files | PROVINCE `d075a3c6…` 162 L (unchanged) · SCORECARD `a7c72950…` 1417 L · SKILL `483b0eba…` 371 L |
| landed instrument (09:06:50, EX-16) | `82fb807e…`, 28606 B — outside this cross-check's before-state, used only for the after-state corollaries below |

`git diff --numstat e845c2b..HEAD`: SCORECARD.md +81/−0, SKILL.md +1/−1,
PROVINCE.md unchanged. The SCORECARD hunk is `@@ -1336,0 +1337,81 @@` — a pure
tail append; lines 1–1336 are byte-identical (`diff` of the two revisions,
empty over that range). The SKILL change is the line-370 citation-drift row
inside no declared row; loci stay 2.

## 1. Fidelity of the round-1 record itself (RV-7 replays)

Rebuilt VZ-3's inputs from git, replayed every class the log records.

| record class | round-1 record | RV-7 replay | verdict |
|---|---|---|---|
| control-pristine | exit 0, `PASS 0/0/0/0`; full capture sha `3b677b8e…` | **byte-identical** to `census-at-HEAD-vz3.txt` (`receipts/r1-control-pure.out` = `3b677b8e…`) | VERIFIED |
| A1 planted tail locus | exit 1, `undeclared=1`, detail `:1337 [pin] kimi=6.4.0 -> STALE (live kimi=6.7.0)` | exit 1, `undeclared=1`, identical detail line (two candidate plant texts give identical output) | VERIFIED (class + detail) |
| A2 marker-stripped | exit 1, SCOPE-ERROR `marker 'arc2-loop1-round2' absent from '## arc2-loop1-r2-STRIPPED — …'` | exit 1, SCOPE-ERROR string byte-identical | VERIFIED |
| A3 pin 6.4.0 + marker | exit 0 PASS | exit 0 PASS (same class, `:12` inline-marker) | VERIFIED |
| A3b pin 9.9.9 + marker | exit 0 PASS; `:20 [pin] kimi=9.9.9 -> historical (inline marker)` | exit 0 PASS; identical detail line | VERIFIED |
| A4 SKILL.md absent | exit 0 PASS, `SKILL.md lines=0 loci=0` | exit 0 PASS, same | VERIFIED |
| A5 PROVINCE.md absent | exit 1; errors `:40, :40, :119` | exit 1; identical three lines | VERIFIED |

Caveat (F1 below): the A-series blocks in `attack-log.txt` are a filtered
excerpt — only the control was archived in full. Class-level and detail-line
reproduction verified; the A-series stdout is not byte-checkable from the
record, and the A1 injection text is not pinned by the record.

## 2. EX-11's round-2 baseline vs the round-1 record

| reading | round-1 record (36e96cd5 @ e845c2b) | EX-11 baseline (6f1d19ff @ 14b1682) | RV-7 independent | verdict |
|---|---|---|---|---|
| control verdict | `PASS 0/0/0/0`, exit 0 | `PASS 0/0/0/0`, exit 0 (`receipts/c0-baseline.out` sha `af1600e7…`) | byte-identical to EX-11's (`receipts/ex11-c0-shadow.out` sha `af1600e7…`); my own `rv7-r2-control.out` identical modulo the harness `EXIT=` marker | MATCH |
| live anchors | devin 6.5.0 · omp 6.5.0 · kimi 6.7.0 | identical | identical | MATCH |
| PROVINCE.md | 162 L, loci 6 | 162 L, loci 6 | 162 L, loci 6; sha `d075a3c6…` both revs | MATCH (byte-identical file) |
| SCORECARD.md | **1336 L**, loci 9 | **1417 L**, loci 9 | 1417 L, loci 9 | DRIFT, EXPLAINED: +81-line tail append in the round-1 records commit; loci unchanged |
| SKILL.md | 371 L, loci 2 | 371 L, loci 2 | 371 L, loci 2 | MATCH |
| H1 class: SKILL.md absent | exit 0 PASS (`lines=0 loci=0`) | exit 0 PASS, `lines=0 loci=0` (`cA`) | exit 0 PASS (`rv7-r2-A4`, `rv7-r2-empty-skill`) | MATCH |
| H1 control: PROVINCE.md absent | exit 1; `:40, :40, :119` | exit 1; `:40, :45, :119` (`cB`) | exit 1; `:40, :45, :119` | DRIFT, EXPLAINED: EX-28's re-key moved row (45,62)'s marker 40→45 |
| H1 control: SCORECARD.md absent | not recorded round 1 | exit 1; 10 marker-uncheckable (`cB2`) | not re-run (class covered by cB) | NEW COVERAGE |
| H3 class: neutered needles | round-1 blind receipt: loci=0 ×3, `G2 … ok`, PASS exit 0 | PASS exit 0, loci=0 ×3 (`cC`) | PASS exit 0, loci=0 ×3 (`rv7-r2-blind`) | MATCH |
| A2 class (marker strip) | exit 1 SCOPE-ERROR | covered by `t3-marker-strip` in EX-16's battery, not EX-11's | r1 replay verified | not in EX-11 scope |
| A1 class (tail plant) | exit 1 `undeclared=1` | not in EX-11's battery | r2 replays `:1337` and tail both exit 1 `undeclared=1` | not in EX-11 scope |

EX-11's c0 output was independently reproduced twice: (a) by re-running their
harness in a shadow work dir (`/var/tmp/rv7-baseline/ex11-shadow`), (b) by my
own separate harness (`replay-round1-record.py`). All five H1/H3 comparables
(`c0, cA, cA2, cB, cC`) match my runs byte-for-byte apart from the harness's
trailing `EXIT=` marker line. Their extra controls also reproduce: cD0 (false
pin plant, needles intact) → exit 1 `stale=1`, my `receipts/cd0.out` agrees.

## 3. Discrepancies found (the deliverable)

1. **F1 — record form, not reading.** The round-1 A-series is excerpt-only.
   Any byte-exactness demand against `attack-log.txt` is unsatisfiable by the
   record itself; I verified class + detail-line reproduction. EX-11's report
   should compare against *classes*, not bytes, outside the control.
2. **F2 — SCORECARD count drift by construction.** Round-1's `lines=1336` is
   not reproducible at round-2 HEAD (`1417`). Any EX-11 text mixing round-1
   counts into round-2 tables (or vice versa) is wrong; the drift is the
   records commit, not an instrument defect.
3. **F3 — A5 error-line index shift** (`:40` second entry → `:45`): EX-28's
   round-1 re-key. Class and exit unchanged.
4. **F4 — a crash is not a declared FAIL.** EX-11's first harness revision
   (09:01) built its "weakened pin" variants without a capture group → the
   instrument dies with `IndexError: no such group` (exit 1, traceback). The
   current revision splits this into `cD1a/cD2a` (no-group, intentionally
   crashing) and `cD1b/cD2b` (group-preserving, genuine narrowing). Any use of
   cD1a/cD2a readings must be labelled "instrument crash", never "declared
   FAIL", or the after-state would be overstated.
5. **F5 — partial narrowing is outside the H3 floor.** Narrowing the gate to
   `rea-agents` (cD3) or the pin needle to `6.5.x` (cD7) leaves loci > 0 and
   still reads `PASS exit 0` on the pre-edit instrument; a `current-ok ≥ 1`
   floor cannot catch it. EX-16's landed header names exactly this as the H4
   residual (external scope-diff/locus-count audit is the certificate). Not a
   defect, but it bounds the claim's wording: the floor closes *full*
   blindness only.
6. **F6 — before/after boundary and identity archiving: verified.** EX-11's
   baseline is valid only at instrument `6f1d19ff…`; the digest is archived
   twice (`tools/census-pre-6f1d19ff.py`, sha verified == `6f1d19ff…`; source
   `…/round-1/claims/c3/CR-5/tools/census-after.py`, same sha — noted: pinned
   from the round-1 tree, not from a `git show HEAD:` blob, equivalent by sha).
   Their `receipts/summary.txt` archives the identity block (instrument sha +
   the three file shas) — I verified it against my own capture
   (`receipts/r2-identity-before.txt`, sha `7bde61ba…`) and re-hashed the scoped
   files after EX-16's landing: all three unchanged. Their after-state is
   re-runnable because they archived `tools/census-v11-landed.py` ==
   `82fb807e…` (sha verified against the revision I measured). (An earlier draft
   of this artifact claimed the identity block was unarchived — corrected here.)
7. **F7 — claim wording coverage.** "every round-1 silent-PASS injection now
   reproduces as a declared FAIL" holds for the H1/H3 classes (A4, blind) but
   not for the H2 class (A3/A3b marker-excused fabricated pins, round-1 PASSes
   that the C2 patch set does not close). Round-1 A3b reproduces PASS on the
   landed instrument (`:20 [pin] kimi=9.9.9 -> historical (inline marker)`,
   exit 0) — consistent with EX-16's header naming H2 as still open. The
   records text should scope the sentence to H1/H3.
8. **F8 — "identical without the plant" overstates.** EX-11 §4 item 5:
   `cD7` (plant) vs `cD8` (no plant) share the verdict and the G11 collateral
   (`['SCORECARD.md:530']`), but the outputs differ — `cD7` SKILL `loci=0` vs
   `cD8` SKILL `loci=1`, CURRENT-OK 9 vs 10. The plant is assertion-silent
   (0 occurrences of `6.3.0` in `cD7`) but leaves a count trace (a loci *drop*).
   Wording, not a reading error; also note `cD1b` shows the narrowed PIN needle
   is backstopped by the bare-version needle (dets read `[bare]`).
9. **F9 — the target is a moving artifact.** Repo `c1-census-v10.py` passed
   through three revisions inside my window: `6f1d19ff…` (490 L) → `82fb807e…`
   (560 L, 09:06:50, EX-11's and my after-state) → `df9ffdf9…` (601 L,
   09:11:50, live at my last check). EX-11's torn-intermediate catch
   (`9373964c…`, 557 L) is the same mid-landing class RV-7 caught in round 1.
   Live control at `df9ffdf9…`: PASS 0/0/0/0, `DECLARED FAIL CLASSES: []`.
   Every claim graded in this wave must name the revision it graded.
10. **F10 — spotcheck independently re-executed.** Against EX-11's archived
   `tools/census-v11-landed.py` (`82fb807e…`) and
   `tools/census-v11-neutered.py`: my runs reproduce their `c0`, `no-skill`,
   `empty-skill` and `neutered` spotcheck outputs exactly (`receipts/
   post-control.out`, `post-A4.out`, `empty-post.out`, `rv7-v11-neutered.out`
   — identical modulo the harness `EXIT=` marker). `weakgate-ptr` PASS exit 0
   with `current-ok loci=2, total loci=8` also matches my pre-edit cD3 run.

## 4. After-state corollaries (landed instrument `82fb807e…`, RV-7 checks only)

- ordinary run at HEAD: `PASS 0/0/0/0` exit 0, `G2 … ok (current-ok loci=5,
  total loci=17, floor=1)` (`receipts/post-control.out`).
- absent SKILL.md: `FAIL` exit 1, `UNREADABLE (could-not-evaluate):
  ['SKILL.md: FileNotFoundError']`, counts `lines=None loci=None`
  (`receipts/post-A4.out`).
- **zero-byte** SKILL.md (the variant the RV-11 draft did not catch): `FAIL`
  exit 1, `UNREADABLE [… 'SKILL.md: 0 lines < declared max 20 (rows beyond
  EOF)']` — the landed guard is wider than the draft (`receipts/empty-post.out`
  vs `empty-pre.out` PASS exit 0).
- H2 class still PASS (see F7), H4 residual still named.
