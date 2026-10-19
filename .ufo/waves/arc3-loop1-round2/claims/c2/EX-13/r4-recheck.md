# EX-13 (executor, chain c2) — re-check on R4: per-file floor vs class-conditioned silence

Companion to [`h3-analysis.md`](h3-analysis.md). Written after EX-16's **R4** landing
(`df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43`, 09:11:50,
uncommitted), which replaced the tree-level floor (R3) with **EX-14's
per-readable-file floor**. All numbers below are from `tools/r4-recheck.py`
(receipts in `receipts-r4/`, `summary.txt`).

## 1. What R4 changed, relative to the R3 revision analysed in §2 of the companion

| aspect | R3 (`82fb807e`) | R4 (`df9ffdf9`) |
|---|---|---|
| floor unit | `len(out["current-ok"]) > 0` (tree-level, block-level count) | `>= 1 current-ok **assertion/det** per **readable file** (`c1-census-v10.py:545-553`) |
| unreadable files | counted as floor zeros (⇒ spurious `BLIND-INSTRUMENT`, my M3) | exempt (`filelines[f] is not None`) — **M3 discharged** |
| audit substrate | `current-ok loci=…, total loci=…` | `current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3` + `--json.current_ok_per_file` |
| row-class sensitivity | none (dets/blocks indistinguishable) | **none** — still counts dets, regardless of the det's own `scope` |

## 2. R4 re-measurement (12 runs, `receipts-r4/`)

| run | root | exit | verdict | G2 line (current-ok per file) | declared classes |
|---|---|---|---|---|---|
| `r4-live` | repo HEAD | 0 | PASS 0/0/0/0 | `PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3` | `[]` |
| `r4-silenced` | F1: all CURRENT rows blanked | 1 | **FAIL** | `PROVINCE.md=2, SCORECARD.md=10, SKILL.md=0` | `['BLIND-INSTRUMENT']` |
| `r4-allsilent2` | F2: every declared row blanked (markers kept) | 1 | **FAIL** | `PROVINCE.md=2, SCORECARD.md=1, SKILL.md=0` | `['BLIND-INSTRUMENT']` |
| `r4-f4` | **F4: only SCORECARD.md CURRENT row 56-60 blanked** | 0 | **PASS** | `PROVINCE.md=17, SCORECARD.md=10, SKILL.md=3` | `[]` |
| `r4-skillGone` | SKILL.md absent | 1 | FAIL | `SKILL.md=0` (exempt) | `['UNREADABLE']` |
| `r4-empty` | no scoped files | 1 | FAIL | `0/0/0` | `['UNREADABLE']` |

**Verdicts.**
- R4 **closes F1 and F2** — a real improvement over R3, and it closes them through
  `SKILL.md`, the file whose declared rows are 100 % CURRENT: a CURRENT-only file
  collapsing to zero dets is now declared.
- R4 **keeps** both round-1 closures and adds no regression on the ordinary run
  (17/14/3 dets), and it discharges my M3 (empty root declares only `UNREADABLE`).
- R4 **does not close** the class-conditioned residual: in **F4** the declared CURRENT
  surface of SCORECARD.md is silent, `FAIL` is not declared, and the file's per-file
  count is held at 10 by its DATED rows. The floor's unit is still "some current-ok
  det anywhere in the file", and G16 keeps DATED rows supplying exactly that.

## 3. Variant C prototype (measured, NOT applied)

`tools/census-r4-variantC.py` — R4 plus one additional conjunct, expressed on the same
counting loop R4 already runs (so it counts dets, including dets inside `info`/mixed
blocks, which is where SCORECARD.md's CURRENT-class dets live):

> every **readable file that declares CURRENT rows** must contribute **≥ 1 current-ok
> assertion whose own `scope` is `CURRENT`**.

Measured behaviour:

| run | root | exit | verdict | CURRENT-class per file |
|---|---|---|---|---|
| `r4C-live` | repo HEAD | 0 | PASS | `PROVINCE.md=15, SCORECARD.md=4, SKILL.md=3` |
| `r4C-f4` | F4 | 1 | **FAIL** (`BLIND-INSTRUMENT`) | `PROVINCE.md=15, SCORECARD.md=0, SKILL.md=3` |
| `r4C-silenced` | F1 | 1 | FAIL | `0, 0, 0` |
| `r4C-allsilent2` | F2 | 1 | FAIL | `0, 0, 0` |
| `r4C-skillGone` | SKILL.md absent | 1 | FAIL | `['UNREADABLE']`, no spurious class |
| `r4C-empty` | no scoped files | 1 | FAIL | `['UNREADABLE']`, no spurious class |

So C holds on the ordinary run (all three files ≥ 1; tightest is SCORECARD.md = 4),
fails every fixture that R4 fails, and additionally fails F4 — the residual. It is a
2-line extension of the landed counting loop; it needs **no per-row floor** (EX-14's
occupancy map refutes those: DATED rows are legitimately zero-locus) and no scope-table
change, so the creep audit signature is unchanged in kind.

**Live re-confirmation (09:15:02 R4, 09:16:38 R5).** The live target read `df9ffdf9…`
at 09:15:02 and `a4c16763…` at 09:16:38 (R5 differs only in docstring/usage hygiene);
run against F4 both print `DECLARED FAIL CLASSES: []` and `VERDICT: PASS`, exit 0 —
i.e. the residual below is a property of the landed bytes, not of a scratch copy.
Receipt: `receipts-r4/r5-live-recheck.txt`.

**Caveat, stated against this seat's own proposal.** EX-14's map refutes per-row and
per-CURRENT-row floors (`seats/EX-14.md`, rows D/E). C is neither — it constrains
*files*, not rows — but its tightest margin at HEAD is small: SCORECARD.md's 4
CURRENT-class dets all come from the single declared CURRENT block 56-60, so a later
commit that legitimately rewrites that block needle-free would false-FAIL C. C is
offered as a measured option, not as a defect in R4; if the chain prefers not to carry
that risk, option (b) — naming the residual in the records — is fully defensible for
this round's frozen claim.

## 4. Recommendation

Either (a) land C (or an equivalent class-restricted conjunct) in the r9 commit, or
(b) keep R4 and **name the residual** in the records, precisely: *"the floor is
per-readable-file and class-blind; a CURRENT surface that goes silent inside a file
whose DATED rows stay loud is not declared — F4 receipt `r4-f4.out`"*. Option (b) is
acceptable for this round's claim as frozen (which asks for absence + zero-loci
failures, both delivered); option (a) is what this seat would ship, given C is measured
to hold at HEAD and to close the residual without a new class of false FAIL.

## 5. Reproduction

```
python3 tools/r4-recheck.py     # rebuilds F4 + variant C, writes receipts-r4/
```
Pinned inputs: `tools/census-landed-r4.py` (R4, `df9ffdf9…`), `tools/census-before.py`
(R0, `6f1d19ff…`); fixture roots under `/var/tmp/ex13-r2`. No repo target is written.
