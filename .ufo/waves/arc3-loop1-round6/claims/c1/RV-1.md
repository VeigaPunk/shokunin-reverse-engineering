# RV-1 — c1 (census instrument): independent verification of PL-4's r10 frontier register, plus a measured peer comparison

Seat RV-1, chain c1, wave arc3-loop1-round6. Measured 2026-10-19 on this host
(transcripts regenerated 13:58–13:59 -03:00). Every number below is first-hand
this session (rule #14); the commands and the scratch trees are listed in §7,
and no prior seat's or round's value is quoted as evidence.

Repo state: HEAD `c625d5de57e045188b5ce8cd450a57b349f90785` (`c625d5d`, records
of round 5), work `58c3db7`; gate `.ufo/gates/c1-census-v10.py` sha256
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 lines;
PROVINCE.md 162 lines, SKILL.md 390, SCORECARD.md 1696. Scratch:
`/var/tmp/rv1-c1/`. The repo gate was never modified (`git status` at end:
only the pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` and the untracked
wave directory; git used read-only).

Peer artifacts visible at write time: `c1/PL-4.md`, `c1/PL-2.md`, `c1/RV-3.md`,
plus evidence dirs `c1/PL-1/`, `c1/EX-3/` (no `.md` from those two yet — they
landed while this seat measured). PL-2's files moved to `PL-2/prior-attempt/`
mid-run; the patch sha is unchanged (verified, §4.1).

## 0. Verdict in one line

**PL-4's patch is VERIFIED against the frozen claim's three requirements** —
(a) clean tree PASS, (b) seeded stale-literal reintroduction FAILs with a named
class, (c) every SCOPE row and every counter is intact. **One residual sentence
in PL-4 §6.1 is CORRECTED**: insertions/reflows inside the post-unlock frontier
(`:132-162`) are *not* caught by PL-4's instrument; four clean insertion arms
and two reflow-plus-stale-literal arms read PASS exit 0. The frozen falsifier
itself (direct reintroduction into `:91-93`, no reflow) is caught, so the claim
stands; the residual claim about insertion coverage does not. The measured
matrix also shows a mid-flight successor (`PL-1/patch-pl4-to-pl1.diff`) closes
both this gap and the two historical-literal gaps (§4.4).

## 1. First-hand re-derivations (the frozen claim's "before" facts)

| # | Frozen C1 fact | Measurement this session | Verdict |
|---|---|---|---|
| 1 | HEAD records `c625d5d` (work `58c3db7`) | `git rev-parse HEAD` → `c625d5de57e0…`; `git log --oneline -5` → `c625d5d`, then `58c3db7` | VERIFIED |
| 2 | Instrument at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce8…`; `wc -l` → 610 | VERIFIED |
| 3 | SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131 | gate `:216-222` holds exactly those 7 PROVINCE rows (20 SCOPE rows total); grep for a row reaching 73-93 or 133-162 → none (`E16` in the frozen grep is docstring prose, not a row) | VERIFIED |
| 4 | Frontier region = 73-93 + 133-162 | `grep -n '^## Frontier$\|^### Round-4 frontier (post-unlock)$' PROVINCE.md` → `73:## Frontier`, `133:### Round-4 frontier (post-unlock)`; `wc -l` → 162 | VERIFIED |
| 5 | Instrument reads PASS identically whether or not those bullets are stale | v10 on six seeded trees (literal, forbidden-only, required-stripped, riscv, 161-line truncation, wall-literal): **all PASS exit 0**, `PROVINCE loci=6` in every arm (the truncation arm reports `lines=161, loci=6`) | REPRODUCED |
| 6 | v10 baseline PASS at HEAD | repo-root `--quiet`: live `{'devin':'6.5.0','omp':'6.5.0','kimi':'6.7.0'}`, `PROVINCE=162/loci 6`, `SCORECARD=1696/loci 9`, `SKILL=390/loci 2`, floor `17/14/3`, `VERDICT: PASS`, exit 0 | REPRODUCED |
| 7 | "R4/R5 PROVINCE repairs were clause-audited by hand, not instrument-graded" | operative half reproduced (items 3+5); the historical by-hand audit is not re-derivable from artifacts | PARTLY (operative REPRODUCED, process UNVERIFIABLE) |

Provenance of the seeded literal, re-derived: `git show 40de383~1:PROVINCE.md`
lines 91-93 read "…(Core, r3-07); real solc/vyper-compiled bytecode untested;
selectors stay / bare hashes…", and `git log --oneline -S 'real solc-0.8.37
carriers' -- PROVINCE.md` → `40de383` (arc3-loop1-round4 work). So the seed is
the actual pre-repair before-state, not a paraphrase.

## 2. PL-4 deliverable verification (the mandate)

### 2.1 Patch identity — VERIFIED

`cp .ufo/gates/c1-census-v10.py rt.py; patch rt.py < PL-4/patch-v10-to-r10.diff`
→ patch exit 0; `sha256sum` → `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`
(713 lines, 8 hunks, `py_compile` OK), byte-identical to `PL-4/c1-census-v10-r10.py`
(`diff -q` → identical). This matches PL-4 §4's claimed sha and §8's recipe.
Evidence: `RV-1/patch-roundtrip.txt`.

### 2.2 Requirement (a): clean tree still PASS — VERIFIED

Scratch `clean/` shas equal the repo's (`11a5c604…`, `8e56f3d9…`, `0d10e18f…`).
`r10-pl4 --root clean --quiet` → exit 0, `FRONTIER register (G21): 14 rows
asserted, errors: []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS`.
Same on the real repo root. Evidence: `RV-1/arms.txt`, arm "r10-pl4 on clean".

### 2.3 Requirement (b): seeded reintroduction FAILs, named disposition — VERIFIED

| Arm | v10 | r10 (PL-4) | r10 declared classes |
|---|---|---|---|
| `seed-literal` (pre-`40de383` before-state back into `:91-93`) | PASS exit 0 | **FAIL exit 1** | `['FRONTIER-STALE']` |
| `seed-forbidden-only` (tokens kept, "untested" added) | PASS exit 0 | **FAIL exit 1** | `['FRONTIER-STALE']` — exactly one error: `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)` |
| `seed-required` (earning tokens stripped) | PASS exit 0 | **FAIL exit 1** | `['FRONTIER-UNEVALUABLE']` |
| `seed-riscv` (`r5-01` citation removed at `:137`) | PASS exit 0 | **FAIL exit 1** | `['FRONTIER-UNEVALUABLE']` |
| `seed-trunc` (161 lines) | PASS exit 0 | **FAIL exit 1** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` |

The `seed-literal` run produces the FORBIDDEN match *and* the two REQUIRED-absent
errors (the historical before-state carries no `solc-0.8.37`/`vyper-0.4.3`
tokens); `declared_fail_classes` reports only `FRONTIER-STALE` because
`any("FORBIDDEN" ...)` wins. That is a cosmetic classification nuance, not a
miss — the run exits 1 either way. Evidence: `RV-1/arms.txt`, `RV-1/arms-matrix.txt`.

### 2.4 Requirement (c): SCOPE rows and counters intact — VERIFIED

- `--json` on the real repo, v10 vs r10: **17 shared keys, mismatched `[]`**;
  r10 adds only `frontier_errors`/`frontier_rows`; `counts` equal; `historical`
  and `current_ok` lists equal; `current_ok_per_file` `PROVINCE 17 / SCORECARD 14 /
  SKILL 3` unchanged.
- Imported-module comparison: `SCOPE_equal=True` (20 rows), all 12 needle/class
  regexes equal.
- Text output diff at repo root is exactly **one added line**
  (`FRONTIER register (G21): 14 rows asserted, errors: []`).
Evidence: `RV-1/counter-integrity.txt`.

### 2.5 The blindness mechanism — VERIFIED

`classify()` on PROVINCE.md yields 6 records / 24 asserts, **0 asserts inside
73-93 or 133-162**; the frontier lines carry no PIN, no bare `6.x.y`, no
`path:line` pointer (`frontier_has_PIN=False VER=False PTR=False`). A SCOPE row
alone therefore cannot grade these bullets — PL-4's design conclusion is
mechanically reproduced, not just asserted.

## 3. Correction: the insertion/reflow residual does not hold as stated

PL-4 §6.1 (their artifact, lines 330-333) says: "Insertions anywhere inside
:73-162 are caught: above :119 they shift the DATED marker row (G15 SCOPE-ERROR
…), inside :132-162 they shift register spans (REQUIRED-absent — measured via
the seeded arms)."

Measured on PL-4's instrument (scratch trees, one line-count-neutral blank-line
insertion):

| Tree | v10 | r10 (PL-4) | PL-4 frontier errors |
|---|---|---|---|
| `seed-ins134` (blank at 134) | PASS | **PASS exit 0** | `[]` |
| `seed-ins137` (blank at 137) | PASS | **PASS exit 0** | `[]` |
| `seed-ins140` (blank at 140) | PASS | **PASS exit 0** | `[]` |
| `seed-ins150` (blank at 150) | PASS | **PASS exit 0** | `[]` |
| `seed-wall-ins139` (stale wall literal at `:144`, shifted to `:145` by a blank at 139) | PASS | **PASS exit 0** | `[]` |
| `seed-cross-ins160` (stale cross-version literal at `:160`, shifted to `:161` by a blank at 160) | PASS | **PASS exit 0** | `[]` |

Mechanism: PL-4's `FRONTIER[]` rows are span-keyed (`start,end`) with no anchor
line. An insertion shifts the bullets but the shifted span still contains each
row's REQUIRED tokens; a stale literal that moves one line past `end` is no
longer scanned. The last two arms are the sharp case: a declared-stale literal
in the post-unlock region is invisible after a single blank-line reflow. All
six insertion arms are **below** `:119`, so the pre-existing G15 DATED-marker
machinery is silent; an insertion above `:119` (e.g. inside `:73-93`) would
shift the marker row and fail via `scope_errors`, as PL-4 says.

Scope of the correction: the frozen claim's falsifier is a direct reintroduction
into `:91-93` with no reflow, and that is caught (§2.3). So requirement (b) is
met. What is falsified is PL-4's additional sentence about insertion coverage,
and the design intent "a frontier edit re-keys the register in the same commit"
is not enforced — it is silently absorbed. This is a real false-PASS on stale
text, not merely a mis-grade.

## 4. Peer reconciliation on a common arm matrix (measured first-hand)

VZ/CN seats own the formal verdict reconciliation; this section is c1 evidence
they can use, and a landing recommendation.

### 4.1 Peer patch identity — both VERIFIED

- PL-2 patch (now at `PL-2/prior-attempt/c1-census-v10-r10.patch`, sha
  `976188cc…`, unchanged from the pre-move path) applies to the pristine gate
  → instrument sha `2d7ee95ba2743bde0b658c91d867a46e04e3e9e14de41d2cb60f2ff46238ce7b`
  = PL-2's claimed proposed-instrument sha.
- RV-3's inline diff (extracted from `RV-3.md` §4) applies to the pristine gate
  → sha `8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf`
  = RV-3's claimed working-gate sha.

### 4.2 Matrix — 15 trees × 4 instruments (60 runs, exit code + verdict)

Full transcript: `RV-1/arms.txt`; compact table: `RV-1/arms-matrix.txt`; seed
definitions: `RV-1/seed-construction.txt`, `RV-1/seed-diffs.txt`.

| Tree | v10 | r10-PL4 | r10-PL2 | r10-RV3 |
|---|---|---|---|---|
| clean | PASS | PASS | PASS | PASS |
| seed-literal | PASS | FAIL STALE | FAIL STALE | FAIL STALE+UNATTESTED |
| seed-forbidden-only | PASS | FAIL STALE | FAIL STALE | FAIL STALE |
| seed-required | PASS | FAIL UNEVALUABLE | **PASS** | FAIL UNATTESTED |
| seed-riscv | PASS | FAIL UNEVALUABLE | **PASS** | FAIL UNATTESTED |
| seed-trunc | PASS | FAIL UNREADABLE+UNEVALUABLE | FAIL UNREADABLE | FAIL UNATTESTED |
| seed-wall | PASS | **PASS** | FAIL STALE | **PASS** |
| seed-cross | PASS | **PASS** | FAIL STALE | **PASS** |
| seed-ins134 | PASS | **PASS** | **PASS** | FAIL ANCHOR |
| seed-ins137 | PASS | **PASS** | **PASS** | FAIL ANCHOR |
| seed-ins140 | PASS | **PASS** | **PASS** | FAIL ANCHOR |
| seed-ins150 | PASS | **PASS** | **PASS** | FAIL ANCHOR |
| seed-cross-ins160 | PASS | **PASS** | FAIL STALE | FAIL ANCHOR |
| seed-wall-ins139 | PASS | **PASS** | FAIL STALE | FAIL ANCHOR |
| seed-append (`:163`) | PASS | PASS | PASS | PASS (named residual for all) |

Reading, against each design's own declared contract:

- **v10: 15/15 PASS.** The blind spot is wider than any single seed: stale
  literals, silent bullet rewrites, a 161-line truncation, reflows — all
  invisible.
- **PL-4**: meets its declared arms 5/5 (literal, forbidden-only, required,
  riscv, trunc) and the frozen falsifier; misses its own §6.1 insertion claim
  6/6 (four reflows + two reflow-plus-stale).
- **PL-2**: its 3-literal register catches 6/6 literal arms including the two
  reflowed ones (its wall/cross ranges are the whole `133-162` region, so span
  shifts do not matter); it has no positive floor, so a silent bullet rewrite
  (`seed-required`, `seed-riscv`) reads PASS. No insertion anchoring by design.
- **RV-3**: anchor-line rows catch 4/4 reflows and both reflow-plus-stale arms,
  and its REQUIRED spans catch silent rewrites; it declares only the EVM
  `untested` literal, so `seed-wall`/`seed-cross` read PASS. Truncation is
  caught as `FRONTIER-UNATTESTED` rather than `UNREADABLE` (its patch does not
  raise the G19 max-end; the lost `:162` token trips the last row instead).
- All four instruments PASS the append-past-bound arm — the named residual is
  common, not a PL-4-specific flaw.

### 4.3 Convergence observation (for VZ/CN, not a landed change)

The measured dominance order for frontier staleness fidelity on this matrix is:
a design with **anchor lines + REQUIRED spans + all three historical forbidden
literals** > RV-3 ≈ PL-4 > PL-2. RV-3 alone fixes the reflow class; PL-2 alone
fixes the historical-literal class; PL-4 has the complete REQUIRED span set but
neither anchors nor the other two literals. No single delivered c1 patch
dominates the matrix.

### 4.4 Mid-flight successor (observed, not a delivered artifact)

While this seat measured, `c1/PL-1/` landed `patch-pl4-to-pl1.diff` (PL-4
container → successor). Applied on scratch to PL-4's built instrument: exit 0,
sha `7724adccdf6391cffc622b8fa3144ede421eb24aedc1431893c2482f892c12a1`, 748
lines, 16 register rows. On the same 15-tree matrix it fails **13/14 seeded
trees** (clean PASS; the named append-past-bound arm the only other PASS),
including `seed-wall`,
`seed-cross`, all four reflows, and both reflow-plus-stale arms. Evidence:
`RV-1/pl1-successor-matrix.txt`. There was no `PL-1.md` at write time, so this
is measured behavior of a mid-flight patch, not a verdict on a delivered
artifact — VZ/CN should re-check identity when it lands.

## 5. Per-item verdicts

| Item | Verdict | Evidence |
|---|---|---|
| Frozen fact 1 (HEAD/work) | VERIFIED | §1 item 1 |
| Frozen fact 2 (gate path/sha/lines) | VERIFIED | §1 item 2 |
| Frozen fact 3 (SCOPE rows, frontier undeclared) | VERIFIED | §1 item 3, §2.4 |
| Frozen fact 4 (frontier spans, 162 lines) | VERIFIED | §1 item 4 |
| Frozen fact 5 (v10 blind on stale frontier) | REPRODUCED | §1 item 5, §4.2 |
| Frozen fact 6 (v10 baseline PASS) | REPRODUCED | §1 item 6 |
| Frozen fact 7 (by-hand audit) | PARTLY: operative REPRODUCED, process UNVERIFIABLE | §1 item 7 |
| PL-4 patch identity (sha/713 lines/round-trip) | VERIFIED | §2.1 |
| PL-4 requirement (a) clean PASS | VERIFIED | §2.2 |
| PL-4 requirement (b) catch + named disposition | VERIFIED | §2.3 |
| PL-4 requirement (c) counters/SCOPE intact | VERIFIED | §2.4 |
| PL-4 §6.1 "insertions inside :132-162 caught" | **CORRECTED** (6/6 measured counterexamples) | §3 |
| PL-4 §3 arm table (literal / forbidden-only / required / riscv / trunc) | REPRODUCED | §2.3 |
| PL-4 blindness mechanism (no loci in frontier) | VERIFIED | §2.5 |
| PL-2 patch identity | VERIFIED | §4.1 |
| PL-2 behavior on common matrix | REPRODUCED (own arms; their claimed numbers not re-quoted) | §4.2 |
| RV-3 patch identity | VERIFIED | §4.1 |
| RV-3 behavior on common matrix | REPRODUCED | §4.2 |
| PL-1 successor (mid-flight, no .md) | UNVERIFIABLE as a delivered artifact; scratch behavior measured | §4.4 |
| Append-past-`:162` residual | VERIFIED (all four instruments PASS) | §4.2 |

## 6. Residuals and what this seat did not do

1. **No competing patch authored.** The mandate offered verify-or-propose; I
   verified, and measured the peers' designs for the convergence seats. I did
   not write or land a gate, and no tracked file was modified.
2. **The correction in §3 is a coverage fact, not a claim failure.** The frozen
   falsifier (direct reintroduction) passes. A landing seat that wants
   reflow-robustness must take an anchor-keyed design (RV-3/PL-1 style) or
   re-key on every insertion; the current PL-4 text's residual sentence should
   not be repeated as if measured.
3. **Register coverage is earned, not exhaustive** in every design: only
   literals on record are forbidden; brand-new stale claims and appends past the
   bound remain with round audit. RV-3/PL-4 declare this; PL-2 declares it.
4. **Insertion arms above `:119`** were not part of the correction: they are
   caught by the pre-existing G15 DATED-marker machinery, as PL-4 says. My
   counterexamples are all below `:119`, where that machinery is silent.
5. **c2/c3 chains were not re-derived** (outside this seat's chain); VZ/CN own
   the cross-chain reconciliation.
6. **The historical by-hand audit of R4/R5** cannot be verified from artifacts;
   only its operative consequence (frontier was not instrument-graded) was
   reproduced.

## 7. Evidence inventory and reproduction

Under `claims/c1/RV-1/`:

- `arms.txt` — 61-section full transcript: v10 repo-root baseline + 15 trees ×
  4 instruments, text output and exit codes.
- `arms-matrix.txt` — the 60-run compact matrix (instrument, tree, exit, verdict,
  declared classes).
- `counter-integrity.txt` — v10 vs r10-PL4 JSON key comparison, structural
  module comparison, text diff, peer patch round-trips.
- `patch-roundtrip.txt` — pristine-gate → PL-4 patch → sha/line/compile/identity.
- `seed-diffs.txt` — PROVINCE.md diffs clean → literal / required / riscv /
  wall / cross / combined seeds.
- `seed-construction.txt` — every seed described and the tree shas.
- `pl1-successor-matrix.txt` — mid-flight successor run and sha.

Reproduction skeleton (scratch `/var/tmp/rv1-c1`, nothing under `/tmp`):

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
cp .ufo/gates/c1-census-v10.py /var/tmp/rv1-c1/bin/
cp .ufo/gates/c1-census-v10.py /var/tmp/rv1-c1/bin/r10-pl4.py
patch /var/tmp/rv1-c1/bin/r10-pl4.py < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum /var/tmp/rv1-c1/bin/r10-pl4.py   # 8002757078a685f5…e18d14aecca
python3 .ufo/gates/c1-census-v10.py --quiet          # PASS exit 0
python3 /var/tmp/rv1-c1/bin/r10-pl4.py --quiet       # PASS exit 0, 14 rows, errors []
python3 /var/tmp/rv1-c1/bin/r10-pl4.py --root /var/tmp/rv1-c1/seed-literal --quiet
                                                      # FAIL exit 1, FRONTIER-STALE
```
