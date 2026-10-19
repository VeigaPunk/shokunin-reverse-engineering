# EX-11 — BEFORE-STATE baseline: census injection classes on the pre-edit instrument (c2, executor)

Round: arc3-loop1-round2. Date: 2026-10-19. Seat: EX-11 (chain c2, executor).
Deliverable of this artifact: verbatim silent-PASS/FAIL baseline of the PRE-EDIT
census under four injection classes, plus matched controls, plus a projection of
the round-1 H1/H3 patch texts. Receipts: `receipts/` (SHA256SUMS there).

## 0. Identity pins (the before-state this baseline speaks about)

| item | sha256 | notes |
|---|---|---|
| census instrument (pre-edit) | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` | 490 lines. Repo `.ufo/gates/c1-census-v10.py` had this sha at session start; `wc -l` = 490. |
| PROVINCE.md | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` | 162 lines |
| SKILL.md | `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb` | 371 lines |
| SCORECARD.md | `a7c72950094ecae0e67204668dac21138c1d5d613bb9e36f1bec241b834f4a93` | 1417 lines |
| live anchors (re-derived by the instrument) | `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}` | read-only reads of the 3 client configs |

**Mid-wave collision (recorded):** while this baseline was in flight, EX-16 landed
the v11 edit — the repo census is now 560 lines, sha
`82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa` (one in-flight
`shutil.copy2` caught a torn 557-line intermediate; those receipts were discarded).
The pinned pre-edit instrument is preserved byte-identical in the round-1 tree at
`.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/census-after.py` (sha verified
= `6f1d19ff…`), and a copy of it ships with this artifact:
`tools/census-pre-6f1d19ff.py`. Every receipt below was re-run against that pinned
copy after the collision. Collision note for verifiers: any claim quoting "the
census" in this wave must name the sha it used; `6f1d19ff…` = before, `82fb807e…` = after.

## 1. Method

Harness: `tools/run-before-injections.py` (this dir). It copies the 3 scoped files
to `/var/tmp/ex11/root-before/`, then for each case materializes
`/var/tmp/ex11/cases/<case>/root/`, mutates it, and runs the instrument with
`--root <case root>` under the real `HOME` (anchors re-derived). stdout+stderr+
exit captured verbatim to `receipts/<case>.out`. Instruments that differ from the
pinned census (needle/gate/scope variants, hand-applied patch text) are archived
under `tools/` and hash-recorded. All census `live_pins` reads of the custody
configs are open-for-read only; no custody byte was written, no git mutation was
run, `/tmp` untouched (scratch `/var/tmp/ex11` only).

Pre-edit code anchors (line numbers in the 490-line before-state): `:438`
`out, counts, filelines = {}, {}, {}`; `:442` `except OSError:`; `:447`
`counts[f] = {"lines": 0, "loci": 0}`; `:453` the G2 disjunction; `:454-455` the
verdict expression.

## 2. Baseline at HEAD (no injection) — c0

```
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
EXIT=0
```

JSON capture (`receipts/c0-baseline.json`): total loci 17; current-ok 5 blocks /
11 dets; historical 5 blocks. This is the "ordinary run stays PASS 0/0/0/0" datum
for the chain claim.

## 3. Injection classes — verbatim captures

### A. Absent SKILL.md (H1 class) — cA → **silent PASS**

```
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=0    loci=0
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
EXIT=0
```

Reproduces RV-11's attack A5 exactly (round-1 `proposed-missing-file-guard.patch.md`).
Because every SKILL.md row is CURRENT (`c1-census-v10.py:147-148`, pre-edit), the
absent file reads `lines=0 loci=0` and the run still PASSes.

Variant cA2 (SKILL.md present but zero-byte): identical silent PASS, `EXIT=0` —
the before-state cannot distinguish "absent" from "truncated to 0 bytes".

### B. Absent PROVINCE.md (control) — cB → **FAIL**

```
SCOPE-ERRORS (marker assertions): ['PROVINCE.md:40 marker uncheckable (file unreadable)', 'PROVINCE.md:45 marker uncheckable (file unreadable)', 'PROVINCE.md:119 marker uncheckable (file unreadable)']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
EXIT=1
```

cB2 (absent SCORECARD.md): FAIL, 10 `marker uncheckable` scope-errors
(`SCORECARD.md:273,417,467,503,534,619,620,636,704,769`), EXIT=1. Control verdict:
the H1 defect is specific to files whose declared rows are all CURRENT — files
carrying DATED rows already fail via `assert_markers` (`c1-census-v10.py:255-272`).
So "absent scoped file" fails only *incidentally* for 2 of 3 files.

### C. Neutered needles (H3 class) — cC → **silent PASS**

Instrument `tools/census-neutered.py` (PIN/VER/PTR replaced with never-matching
patterns; sha in SHA256SUMS). Verbatim tail:

```
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
EXIT=0
```

`SKILL.md lines=371 loci=0`, PROVINCE/SCORECARD also `loci=0`. Reproduces CR-5's
blind-instrument receipt on the pinned instrument: vacuously-passing G2
(`c1-census-v10.py:453`, second disjunct true exactly when nothing was asserted,
`EXIT=0`.

### D. Weakened regex — matrix

| case | instrument (sha in SHA256SUMS) | root mutation | exit | verdict | detection of the plant |
|---|---|---|---|---|---|
| cD0 control | pre-edit | plant `rea-agents@6.3.0` at SKILL.md:19 | 1 | FAIL stale=1 | caught (`:19 [bare] devin/omp=6.3.0 -> STALE`) |
| cD1a | PIN `rea-agents@6\.5\.\d+` (no group) | same plant | 1 | crash | IndexError `m.group(1)` at `classify` — non-silent, but sees nothing |
| cD2a | same, no plant | — | 1 | crash | — |
| cD1b | PIN `rea-agents@(6\.5\.\d+)` | plant | 1 | FAIL stale=1 | **still caught** via VER backstop (`:19 [bare]=6.3.0 -> STALE`) |
| cD2b | same, no plant | — | 0 | PASS | loci count unchanged vs c0 (2/6/9) |
| cD3 | REA_GATE narrowed to `rea-agents` only | append `~/.kimi-code/config.toml:9999` ptr line to SCORECARD.md | 0 | **PASS (silent)** | plant absent from output (0 hits) |
| cD4 control | pre-edit | same append | 1 | FAIL undeclared=1 | `SCORECARD.md:1419 [ptr] __ptr__=~/.kimi-code/config.toml:9999 -> UNRESOLVED`, then UNDECLARED |
| cD5 control | pre-edit | append stale-pin sentence (round-1 t2 recipe) | 1 | FAIL undeclared=1 | caught |
| cD6 | weak gate (cD3's) | same stale-pin append | 1 | FAIL undeclared=1 | still caught (`rea-agents` token survives the weakened gate) |
| cD7 | PIN `(6\.5\.\d+)` + VER `6\.5\.\d+` | plant | 1 | FAIL (collateral) | **NOT detected** — 0 hits of `6.3.0`; SKILL.md `loci=0`; FAIL cause = G11 `['SCORECARD.md:530']`, present identically in cD8 without any plant |
| cD8 | same, no plant | — | 1 | FAIL (same G11) | — |

Readings (see §5 for the falsification verdicts):
- The **clean silent PASS** of the weakened-regex class is cD3 (weakened gate;
  matched control cD4 FAILs loudly). A `REA_GATE` narrowing that drops
  `config.toml`/paths from the gate makes a planted undeclared pointer statement
  invisible end-to-end, exit 0, all declared counters zero.
- Weakening PIN alone is **not** enough for pins (cD1b: VER backstops; the plant
  is still caught) and a careless narrowing that drops the capture group crashes
  loudly (cD1a/2a). The dangerous partial form is needle-set narrowing that
  preserves the positive floor (cD7: floor intact, plant invisible, verdict
  determined by unrelated G11 collateral).
- cD7's FAIL is a *plant-independent* property of the weakened instrument (cD8
  has no plant and fails identically) — a caution against reading a FAIL as
  "detected" without a no-plant control.

## 4. Projection: the round-1 H1/H3 patch texts, hand-applied (NOT the landed v11)

Instruments: `tools/census-projected-h1h3.py` (both drafts), `census-h1-only.py`,
`census-h3-only.py`; weakened combinations also archived. Hand-application of the
draft diffs from round-1
`claims/c3/RV-11/proposed-missing-file-guard.patch.md` (H1) and
`claims/c3/CR-5/proposed-g2-positive-floor.patch.md` (H3, first form:
`g2_ok = len(out.get("current-ok", [])) > 0`).

| case | instrument | exit | verdict | note |
|---|---|---|---|---|
| cP0 | H1+H3 | 0 | PASS | baseline unbroken (c0 identical) |
| cP1 | H1+H3, absent SKILL.md | 1 | FAIL `UNREADABLE: ['SKILL.md: FileNotFoundError']` | H1 covers class A |
| cP2 | H1+H3, neutered | 1 | FAIL `G2 … SUSPECT` | H3 covers class C |
| cP5 | H1-only, absent SKILL.md | 1 | FAIL | |
| cP6 | H3-only, absent SKILL.md | 0 | **PASS (silent)** | H3 alone does not close A |
| cP7 | H1-only, neutered | 0 | **PASS (silent)** | H1 alone does not close C |
| cP8 | H3-only, neutered | 1 | FAIL G2 SUSPECT | |
| cP3 | H1+H3, weakened gate + ptr append | 0 | **PASS (silent)** | H1+H3 do not close the weakened-gate class |
| cP4 | H1+H3, weak PIN+VER + plant | 1 | FAIL | plant still invisible (SKILL `loci=0`); same collateral |
| cP9 | H1+H3, **zero-byte** SKILL.md | 0 | **PASS (silent)** | H1 keys on `OSError` only; truncation to 0 bytes remains silent |

Isolation verdict: H1 and H3 are each necessary and neither is sufficient; the
drafts close exactly the two round-1 classes (A, C). The weakened-regex class
(cD3) and the zero-byte variant (cP9) survive H1+H3.

Context (not verified by this seat): the landed v11 (`82fb807e…`) advertises
declared classes `UNREADABLE`/`BLIND-INSTRUMENT` and a rows-beyond-EOF check
(`grep -n` hits at `:519` `declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"])`
and `:501` rows-beyond-EOF append). The recipes below are the ones this seat
measured to be silent in the before-state; re-running them (plus c0) against the
landed v11 is the after-state/verifier exercise.

### 4b. Post-landing spot-check against v11 (after-state; receipts `receipts-v11-spotcheck/`)

Read-only copy of the landed file to `/var/tmp/ex11-after/` (sha verified
`82fb807e…`, archived as `tools/census-v11-landed.py`); same root-before. This is
a spot-check by an executor seat, not the chain's verification.

| case | root | exit | declared classes | verdict |
|---|---|---|---|---|
| c0 | clean | 0 | `[]` | PASS; floor line `G2 … ok (current-ok loci=5, total loci=17, floor=1)` |
| absent SKILL.md | missing file | 1 | `['UNREADABLE']` (`SKILL.md: FileNotFoundError`) | FAIL — H1 class closed |
| zero-byte SKILL.md | `: > SKILL.md` | 1 | `['UNREADABLE']` (`0 lines < declared max 20 (rows beyond EOF)`) | FAIL — cP9 residual closed |
| neutered needles | clean | 1 | `['BLIND-INSTRUMENT']` (`current-ok loci=0, total loci=0, floor=1`) | FAIL — H3 class closed |
| **weakened gate + ptr append (cD3 recipe)** | append `~/.kimi-code/config.toml:9999` | **0** | **`[]`** | **PASS — F3a class survives v11** |

So: every class this seat measured silent *and* covered by the frozen claim (the
two round-1 classes + the zero-byte variant) is a declared FAIL at v11, and the
ordinary run stays PASS with the positive floor intact. The weakened-gate class
(F3a) is a new, measured silent-PASS channel that v11 does not close — it should
be named as residual or addressed in a next instrument touch; it is outside the
frozen claim's literal promise ("every round-1 silent-PASS injection"), which
holds as measured.

## 5. Attacks attempted, with verdicts

1. **F1 — H1 class reproduced.** Verdict: CONFIRMED silent PASS (cA, cA2);
   controls show files with DATED rows already fail (cB, cB2) → the defect is
   CURRENT-only-scoped files, matching the drafted H1.
2. **F2 — H3 class reproduced.** Verdict: CONFIRMED silent PASS (cC), `G2 ok`
   at `loci=0`, exit 0, on the pinned instrument.
3. **F3a — weakened gate → silent PASS.** Verdict: CONFIRMED clean silent PASS
   (cD3) with a stock control that FAILs on the identical root (cD4). This class
   is not H1/H3-shaped; H1+H3 projection still PASSes it (cP3).
4. **F3b — weakened PIN alone = silent?** Verdict: REFUTED. cD1b FAILs; VER
   backstops pin weakening; the no-group narrowing crashes (cD1a/2a, exit 1,
   non-silent but also non-detecting).
5. **F3c — weakened PIN+VER = verdict carries no detection info.** Verdict:
   CONFIRMED (cD7 vs cD8: identical FAIL via G11 `SCORECARD.md:530`; zero
   occurrences of the planted `6.3.0` in either output).
6. **F4 — H1 catches zero-byte?** Verdict: REFUTED (cP9 PASS under the H1+H3
   projection; H1 keys on `OSError`).
7. **Control discipline check.** Every silent-PASS finding above is bracketed by
   a matched stock-census run on the identical root (cA↔cB/cB2; cD3↔cD4;
   cD7↔cD8/cD0) so the verdict delta is attributable to the instrument change or
   file change, not to the root.

## 6. Before → after (for the chain's claim)

Before (this artifact): A silent PASS (exit 0); C silent PASS (exit 0); D3 clean
silent PASS (exit 0) with control FAIL; D7 detection-silent; ordinary run PASS
0/0/0/0 with 17 loci / 11 current-ok dets.

After (claim text, frozen): absent scoped file → declared FAIL; zero loci in a
non-empty scope → FAIL; every round-1 silent-PASS injection reproduces as a
declared FAIL; ordinary run PASS; scope bounds byte-stable. Recommended
after-state recipes from this seat's matrix — re-run against the landed v11
(`82fb807e…`): `cA`/`cA2` (expect FAIL, class UNREADABLE), `cC` (expect FAIL,
class BLIND-INSTRUMENT), `cD3`-recipe and `cP9`-recipe (these two were silent in
the before-state and are NOT closed by H1+H3-as-drafted — if they still PASS on
v11, they should be either closed or explicitly named as residual in the round
report), `c0` (expect PASS 0/0/0/0).

Measured after (§4b): `cA` → FAIL `UNREADABLE`; `cA2`/zero-byte → FAIL
`UNREADABLE` (rows-beyond-EOF); `cC` → FAIL `BLIND-INSTRUMENT`; `c0` → PASS with
floor `current-ok loci=5, total loci=17, floor=1`; **`cD3`-recipe → still PASS
exit 0, declared classes `[]`** (F3a not closed — residual for the round report
and the next instrument touch; it is outside the literal claim text, which names
only the round-1 silent-PASS injections).

## 7. Blockers

None material. One recorded collision: EX-16 landed v11 mid-baseline; the
before-state is therefore pinned to the frozen round-1 copy of the instrument
(`6f1d19ff…`) rather than the live repo file, per the wave rule that only EX-16
writes the chain's real target.
