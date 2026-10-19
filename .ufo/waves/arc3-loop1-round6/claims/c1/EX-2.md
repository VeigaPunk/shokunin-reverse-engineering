# EX-2 — c1: independent verification of PL-4's r10 frontier register (and a 27-arm common-fault comparison of the three delivered patches)

Seat EX-2, chain c1 (census instrument), wave arc3-loop1-round6, 2026-10-19.
Dispatched per the frozen effective roster (claims-frozen: remaining 45 seats on
opencode-go-7/deepseek-v4.1-flash). Repo HEAD re-derived first-hand:
`c625d5de57e045188b5ce8cd450a57b349f90785` (`git rev-parse HEAD`); work commit
`58c3db7` two entries below in `git log --oneline -4`. The live gate was NOT
modified: `sha256sum .ufo/gates/c1-census-v10.py` =
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` (610 lines),
re-checked after every experiment. Scratch: `/var/tmp/ex2-arc3r6/` (never `/tmp`).
I wrote only this artifact dir; git read-only. Every number below is my own
measurement (lane rule #14); peer artifacts are cited only as objects of audit.

## 0. Verdict in one line

**PL-4's patch is VERIFIED on all three frozen requirements** — patch round-trips
to its claimed sha, the clean tree still reads PASS on both scratch and the real
repo root, the frozen stale literal is caught with a named `FRONTIER-STALE`
disposition, and every existing SCOPE row/counter is byte-intact (17/17 shared
JSON keys identical). Two claims in PL-4's own residual section are **CORRECTED**
by measurement (insertion tolerance; declared-class exhaustiveness), and the
shared limits of all three delivered designs are named with arms (§6–§7).

## 1. First-hand before-state (nothing quoted from a prior seat)

| # | Fact | My measurement | Verdict |
|---|---|---|---|
| 1 | HEAD `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e045188b5ce8cd450a57b349f90785`; `git log --oneline -4` first two lines `c625d5d …records…` / `58c3db7 …work…` | VERIFIED |
| 2 | Gate path/sha/lines | `sha256sum` → `d0772ce8…97b5`; `wc -l` → 610 | VERIFIED |
| 3 | PROVINCE SCOPE rows are exactly the frozen seven | importlib dump: `8-13`, `15-26`, `40-43`, `44`, `45-62`, `64-71`, `119-131` (gate `:216-222`) | VERIFIED |
| 4 | Frontier regions UNDECLARED | covering rows for `(73,93)` → `[]`; for `(133,162)` → `[]` | VERIFIED |
| 5 | Region boundaries | `PROVINCE.md:73` = `## Frontier`; `:133` = `### Round-4 frontier (post-unlock)`; `wc -l PROVINCE.md` → 162; `:162` = last line | VERIFIED |
| 6 | Frontier bullets are locus-free (the blindness mechanism) | programmatic scan of `:75-80`, `:82-93`, `:135-162`: `PIN []`, `VER []`, `PTR []`, `REA_GATE []`; `classify()` emits **0 records** with line ∈ [73,162] | VERIFIED |
| 7 | v10 reads PASS on the seeded blind spot | 26-tree matrix (27 arms incl. `evm-append-upper`), v10 column: PASS exit 0 on every claim-bearing arm except `frontier-pin` (a pin, by design) and `insert-above119` (G15) — including the frozen EVM revert and 161/140-line truncations | REPRODUCED |
| 8 | Historical before-states are real | `git show 40de383^:PROVINCE.md` bullet blocks: EVM `…real solc/vyper-compiled bytecode untested…`; PE wall `…hits REA's ~900s internal / session deadline…`; cross-version `…still / probe-refused since r2…`; subtypes `Reserve: 91MB Godot ARM64 template`; crashes `all 3 organic cores exceed the cap` — all replaced in `40de383` | VERIFIED |
| 9 | Baseline | `python3 .ufo/gates/c1-census-v10.py --quiet` → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` exit 0; PROVINCE loci=6, G2 17/14/3 | REPRODUCED |

## 2. Patch round-trip — VERIFIED

```
git show HEAD:.ufo/gates/c1-census-v10.py > pristine/c1-census-v10.py   # sha d0772ce8…
cp pristine/c1-census-v10.py pl4-gate.py
patch -p0 pl4-gate.py < …/claims/c1/PL-4/patch-v10-to-r10.diff          # "patching file pl4-gate.py"
sha256sum pl4-gate.py    # 8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
wc -l pl4-gate.py        # 713
sha256sum …/claims/c1/PL-4/c1-census-v10-r10.py                          # same 80027570…
```

The patched gate is byte-identical to PL-4's built copy. Structural checks by
importlib against the pristine gate: `SCOPE` identical (20 rows), `REA_GATE`,
`PIN`, `VER`, `PTR` patterns identical; `FRONTIER` has 14 rows. The diff's eight
hunks touch only the docstring, the defect-class table, the new `FRONTIER[]` +
`frontier_check()`, the G19 `max_end` expression, the `frontier_errors` call,
the verdict conjunct/classes, and one text line; `classify()` and
`assert_markers()` are untouched.

## 3. Requirement (a) — PASS on clean, scratch and real tree

`python3 pl4-gate.py --root trees/clean --json` → `"verdict": "PASS"`,
`"frontier_rows": 14`, `"frontier_errors": []`, exit 0.
Real repo root (`…/EX-2/repo-root-pl4.txt`): `FRONTIER register (G21): 14 rows
asserted, errors: []`, `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
unresolved=0)`, exit 0; counts `PROVINCE.md lines=162 loci=6 / SCORECARD.md
1696/9 / SKILL.md 390/2`.

Register spans were checked against real bullet boundaries: every row's first
line is the bullet header it names, every `after` line is the next bullet or a
blank/EOF. The intro row `75-80` is the `## Frontier` claim paragraph (not a
bullet); PL-4 registers it deliberately, RV-3 does not — a design difference,
not a defect.

## 4. Requirement (b) — seeded arms (my own trees, exact strings, count-asserted)

Frozen seed = the `40de383^` EVM before-state reinserted at `:91-93`
(`evm-revert`). PL-4:

```
PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)
PROVINCE.md:91-93 REQUIRED 'vyper-0\.4\.3' absent (G21 frontier register)
PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
exit 1, declared_fail_classes ['FRONTIER-STALE']
```

| arm | what it seeds | v10 | PL-4 |
|---|---|---|---|
| `evm-append` | current EVM text + "Real solc/vyper-compiled bytecode untested." (required intact) | PASS | **FAIL** 1 err, `F-STALE` |
| `evm-append-upper` | same but `UNTESTED` | PASS | **FAIL** 1 err, `F-STALE` (case-insensitive) |
| `evm-strip` | EVM bullet rewritten without the earned tokens, line-count neutral | PASS | **FAIL** 2 err, `F-UNEVALUABLE` |
| `pe-revert` | `>90 MB PE` bullet reverted to `40de383^` | PASS | **FAIL** 1 err (`arc2-r7` absent) |
| `xver-revert` | cross-version bullet reverted to `40de383^` | PASS | **FAIL** 1 err (`r12-02|r14-01` absent) |
| `riscv-strip-both` | `r5-01` token and corpus path both renamed | PASS | **FAIL** 1 err (`r5-01` absent) |
| `trunc161`, `trunc140` | PROVINCE truncated below the register end | PASS | **FAIL** `UNREADABLE` + 14 uncheckable rows (each) |

All match PL-4 §3's per-arm error counts (forbidden-only = 1, required-evm = 2,
required-riscv = 1, truncated = `UNREADABLE` + 14) — re-derived, not quoted.
`--json` exit code is 1 on every FAIL arm.

## 5. Requirement (c) — counters/rows intact (measured)

Clean-tree JSON, v10 vs r10:

```
shared keys: 17 | r10-only: ['frontier_errors', 'frontier_rows'] | v10-only: []
shared keys with differing values: []
counts equal: True
current_ok_per_file: {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
```

Text output diff (clean tree) is exactly one added line:
`87a88 > FRONTIER register (G21): 14 rows asserted, errors: []`; the
`VERDICT:` line is byte-identical. The G19 threshold change is real and
fail-closed: a 161-line PROVINCE reads **PASS** under v10 and **UNREADABLE**
under r10; same at 140 lines (silent content loss past `:131` becomes declared).

## 6. Corrections to PL-4's artifact (both measured, neither breaks the claim)

**C1 — insertion claim is overbroad (PL-4.md:330-333).** PL-4 states
"Insertions anywhere inside `:73-162` are caught … inside `:132-162` they shift
register spans (REQUIRED-absent — measured via the seeded arms)."
Counterexample, measured: `blank-inside` (one blank line before `:139`) →
**PASS**; `insert-inside` (a new bullet carrying the retracted literal
"real solc/vyper-compiled bytecode untested" inserted at `:139`) → **PASS**.
A two-line insertion (`insert2-inside`) FAILs (`F-UNEVALUABLE`, 8 errors), and
an insertion above `:119` FAILs via the existing G15 marker machinery, as PL-4
says. So the tolerance is positional, not absolute: a one-line shift can slide
every required anchor inside its row's window. PL-4 has no per-row anchor line;
RV-3's `anchor_line` catches all three insertion arms (`F-ANCHOR`).

**C2 — declared class list is not exhaustive when both classes fire.** On
`evm-revert` the run reports three errors — two `REQUIRED … absent`
(UNEVALUABLE) and one `FORBIDDEN` (STALE) — but
`declared_fail_classes: ['FRONTIER-STALE']` only (the ternary at the
`frontier_class` expression). Nothing is silent (the error strings name both
classes and appear in text and `--json`), but a consumer reading only the
class list would not know the required floor also failed. Cosmetic/minor.

## 7. Common fault matrix — PL-4 vs PL-2 vs RV-3 (27 fault arms, 4 instruments)

All three peer instruments were re-materialized and sha-checked: PL-2
`2d7ee95b…` (copied from `claims/c1/PL-2/prior-attempt/` — a live peer moved
that directory mid-run at 13:57; the sha matches PL-2's delivered identity),
RV-3 `8e420679…` (diff extracted from the fenced block in `RV-3.md`, `patch
-p0` onto pristine; matches VZ-4's independent re-derivation). Trees:
`/var/tmp/ex2-arc3r6/trees/`; builders and raw cells in `EX-2/`.

```text
tree                   | v10                  | PL-4                               | PL-2                             | RV-3
--------------------------------------------------------------------------------------------------------------------------------------------------------
blank-inside           | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | FAIL/1 F-ANCHOR
clean                  | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | PASS/0 -
crashes-revert         | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | PASS/0 -
evm-append             | PASS/0 -             | FAIL/1 F-STALE                     | FAIL/1 F-STALE                   | FAIL/1 F-STALE
evm-append-upper       | PASS/0 -             | FAIL/1 F-STALE                     | PASS/0 -                         | PASS/0 -
evm-revert             | PASS/0 -             | FAIL/1 F-STALE                     | FAIL/1 F-STALE                   | FAIL/1 F-STALE,F-UNATTESTED
evm-revert-upper       | PASS/0 -             | FAIL/1 F-STALE                     | PASS/0 -                         | FAIL/1 F-UNATTESTED
evm-strip              | PASS/0 -             | FAIL/1 F-UNEVALUABLE               | PASS/0 -                         | FAIL/1 F-UNATTESTED
frontier-pin           | FAIL/1 -             | FAIL/1 -                           | FAIL/1 -                         | FAIL/1 -
insert-above119        | FAIL/1 -             | FAIL/1 -                           | FAIL/1 -                         | FAIL/1 F-ANCHOR
insert-inside          | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | FAIL/1 F-ANCHOR
insert2-inside         | PASS/0 -             | FAIL/1 F-UNEVALUABLE               | PASS/0 -                         | FAIL/1 F-ANCHOR
novel-stale            | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | PASS/0 -
past162                | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | PASS/0 -
pe-append              | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | PASS/0 -
pe-append-wall         | PASS/0 -             | PASS/0 -                           | FAIL/1 F-STALE                   | PASS/0 -
pe-revert              | PASS/0 -             | FAIL/1 F-UNEVALUABLE               | PASS/0 -                         | FAIL/1 F-UNATTESTED
quote-falsepos         | PASS/0 -             | FAIL/1 F-STALE                     | PASS/0 -                         | FAIL/1 F-STALE
relocate-noshift       | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | PASS/0 -
relocate-stale         | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | FAIL/1 F-ANCHOR
riscv-strip            | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | PASS/0 -
riscv-strip-both       | PASS/0 -             | FAIL/1 F-UNEVALUABLE               | PASS/0 -                         | FAIL/1 F-UNATTESTED
subtypes-revert        | PASS/0 -             | PASS/0 -                           | PASS/0 -                         | PASS/0 -
trunc140               | PASS/0 -             | FAIL/1 UNREADABLE,F-UNEVALUABLE    | FAIL/1 UNREADABLE                | FAIL/1 F-ANCHOR
trunc161               | PASS/0 -             | FAIL/1 UNREADABLE,F-UNEVALUABLE    | FAIL/1 UNREADABLE                | FAIL/1 F-UNATTESTED
xver-append-refused    | PASS/0 -             | PASS/0 -                           | FAIL/1 F-STALE                   | PASS/0 -
xver-revert            | PASS/0 -             | FAIL/1 F-UNEVALUABLE               | FAIL/1 F-STALE                   | PASS/0 -
```

Arm definitions (all from `git show 40de383^:PROVINCE.md` blocks or exact
current text; builders in `EX-2/build_trees*.py`): `evm-revert*` = historical
EVM before-state (upper = `UNTESTED`); `evm-append*` = current text + stale
literal; `evm-strip` = earned tokens removed, line-count neutral; `pe-revert`
/ `xver-revert` / `subtypes-revert` / `crashes-revert` = historical before-state
of that bullet; `pe-append-wall` / `xver-append-refused` = current text + the
exact historical stale clause on one line; `riscv-strip` = `(r5-01:` token
renamed only (path keeps `r5-01`); `riscv-strip-both` = both; `blank-inside` /
`insert-inside` / `insert2-inside` = 1 blank, 1 bullet (carrying the retracted
literal), 2 bullets before `:139`; `insert-above119` = one line above the DATED
row; `relocate-noshift` = retracted literal appended inside the RISC-V bullet;
`relocate-stale` = same as `insert-inside`; `past162` = new bullet after `:162`;
`novel-stale` = a false claim not on any register; `quote-falsepos` = the
retracted literal quoted as a warning; `frontier-pin` = `rea-agents@6.3.0` in
`:87-88`.

The consolidated `matrix-all.txt/json` holds 26 rows (header + separator + 26);
`evm-append-upper` was measured immediately afterwards with the same runner and
is retained at `cells/evm-append-upper__{v10,PL4,PL2,RV3}.json` (the table above
lists all 27 arms).

What the matrix establishes, measured:

- **PL-4 has the broadest historical-revert catch set**: EVM revert/append/
  case-variant/strip, PE-wall revert, cross-version revert, both truncations.
  It alone catches an appended case-variant literal (`evm-append-upper`) while
  required tokens survive.
- **RV-3 has the strongest structural anchors** (all insertion arms FAIL) but
  **misses the canonical cross-version revert**: `xver-revert` → PASS, because
  its REQUIRED token `compare-application-versions` survives in the stale text
  and the row declares no FORBIDDEN pattern. VZ-4's audit exercised only the
  EVM seed, so this gap was not previously measured.
- **PL-2 is literal-only and case/wrap-sensitive**: it misses `evm-strip`
  (no positive floor), `evm-revert-upper` and `evm-append-upper` (case), and the
  **canonical** `pe-revert` because the historical phrase wraps across two lines
  (`hits REA's ~900s internal\n  session deadline`), while its line-based scan
  matches only a one-line append (`pe-append-wall`). It catches
  `xver-revert` because "probe-refused since r2" sits on one line.
- **Shared residuals (all four instruments)**: novel stale claims
  (`novel-stale`), historical reverts of the PE-subtype and recorded-crash
  bullets (`subtypes-revert`, `crashes-revert`), a stale literal relocated into
  a different frontier bullet (`relocate-noshift`), and a brand-new bullet past
  `:162` (`past162`). PL-4 names the past-162 and earned-not-exhaustive
  residuals explicitly; the relocation arm is the same class (FORBIDDEN is
  span-local) and is now measured.
- **False positive by design**: a quoted warning mention of the retracted
  literal fails PL-4 and RV-3 (`quote-falsepos`); PL-2 passes only because its
  literal is the longer phrase. This is the named literal-list residual, not a
  regression.
- **Pre-existing behavior preserved**: an instrument-visible stale pin in
  `:87-88` still FAILs under v10/PL-4/RV-3 with `undeclared=1` (unchanged);
  PL-2 reclassifies it as `ambiguous=1` because it adds SCOPE `FRONTIER` rows —
  by design of the SCOPE-declaration option, and still FAIL/exit 1.

## 8. Per-item verdict table

| # | Item | Verdict |
|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7` | VERIFIED |
| 2 | Gate sha `d0772ce8…`, 610 lines | VERIFIED |
| 3 | SCOPE = seven PROVINCE rows; 73-93 and 133-162 UNDECLARED | VERIFIED |
| 4 | Frontier locus-free; `classify()` 0 records there | VERIFIED |
| 5 | v10 blind: PASS on the frozen revert + 161/140-line truncations | REPRODUCED |
| 6 | PL-4 patch round-trip → `80027570…`, 713 lines, byte-equal built copy | VERIFIED |
| 7 | Requirement (a): clean scratch + real tree PASS, 14 rows, errors `[]` | REPRODUCED |
| 8 | Requirement (b): frozen seed → FAIL exit 1, `FRONTIER-STALE`, 3 named errors | REPRODUCED |
| 9 | Requirement (b): forbidden-only arm = exactly 1 error; required arms = 2/1 | REPRODUCED |
| 10 | Requirement (b): PE/xver bullet reverts caught via required anchors | REPRODUCED |
| 11 | Case-insensitive FORBIDDEN (upper-case retracted literal caught) | REPRODUCED |
| 12 | Requirement (c): 17 shared JSON keys, 0 differing; 2 additive keys; counts/floor intact | REPRODUCED |
| 13 | Requirement (c): SCOPE 20 rows and needle regexes identical | VERIFIED |
| 14 | Requirement (c): text diff exactly +1 FRONTIER line; VERDICT byte-identical | VERIFIED |
| 15 | G19 131→162: 161/140-line trees v10 PASS → r10 UNREADABLE | REPRODUCED |
| 16 | PL-4 §6.1 "insertions anywhere inside :73-162 are caught" | **CORRECTED** — one-line insertion at `:139` (even carrying the retracted literal) PASSes; two-line insertion and any insertion above `:119` FAIL |
| 17 | PL-4 declared-class list when STALE and UNEVALUABLE both fire | **CORRECTED (minor)** — list shows `['FRONTIER-STALE']` while 2 UNEVALUABLE errors are also reported; not silent |
| 18 | PL-4 residual "forbidden coverage earned, not exhaustive" | CONFIRMED — `pe-append-wall`, `xver-append-refused` PASS under PL-4 |
| 19 | RV-3 catches the canonical cross-version revert | **DISCREPANCY** — `xver-revert` PASSes RV-3; required token survives, no FORBIDDEN row |
| 20 | PL-2 register entry 2 against its canonical before-state (PL-2 §5 marked entries 2-3 UNVERIFIABLE / not exercised) | **CORRECTED (now measured)** — `pe-revert` PASSes; the line-local scan misses the wrapped phrase `…~900s internal` / `  session deadline`; only the one-line append `pe-append-wall` FAILs. Entry 3 does catch both its one-line and reverted forms |
| 21 | PL-2 positive floor / case handling | GAP — `evm-strip`, `evm-revert-upper`, and `evm-append-upper` PASS |
| 22 | RV-3 insertion anchors | REPRODUCED — all three insertion arms FAIL `F-ANCHOR` |
| 23 | Shared: novel claim, subtype/crash reverts, relocation, past-162 | RESIDUAL CONFIRMED (all instruments) |
| 24 | Quote-as-warning false positive | RESIDUAL CONFIRMED (PL-4/RV-3) |
| 25 | Peer instruments clean-tree PASS | REPRODUCED (all three) |

## 9. Recommendation to the integrator (not a landing)

Of the three delivered patches, **PL-4 is the one I can verify end-to-end against
the frozen claim and it has the broadest measured catch set on historical
reverts**, including the cross-version revert RV-3 misses and the case variant
PL-2 misses. Its requirement (c) integrity is exact. If the lane wants the two
measured gaps closed before landing, they are (i) RV-3-style per-row anchor
lines (closes the one-line insertion tolerance) and (ii) the two additional
FORBIDDEN literals already earned in PL-2's register — `hits REA's ~900s
internal session deadline` and `probe-refused since r2` (closes appended-clause
reintroduction). I did not write that gate/patch; that is a landing-seat move.

## 10. Custody / what I did not do

- Wrote only `.ufo/waves/arc3-loop1-round6/claims/c1/EX-2.md` and `EX-2/`.
- Gate sha unchanged before/after (`d0772ce8…`); git used read-only.
- `git status --porcelain -uno` shows one pre-existing tracked modification,
  `.ufo/waves/arc2-loop1-round10/C3.md` (mtime 2026-10-18 23:01, i.e. before
  this wave; `git log -1` on it is the round-10 records commit). Not mine.
- Did not land PL-4's patch or any rule/corpus change; did not edit
  PROVINCE/SKILL/SCORECARD/corpus/gates.
- PL-2's artifact directory was reorganized by a live peer at 13:57 while I was
  measuring; I re-read the instrument from `prior-attempt/` and confirmed its
  sha still matches PL-2's delivered identity (`2d7ee95b…`). This is a
  point-in-time measurement, not a claim about later peer edits.

## 11. Evidence inventory (`EX-2/`)

- `matrix-all.txt`, `matrix-all.json` — the 26-tree × 4-instrument matrix (the
  27th arm, `evm-append-upper`, is in `cells/` as noted in §7).
- `cells/` — raw `--json` for the key arms cited above (clean invariance pair,
  frozen seed, append/upper/strip, PE/xver reverts and appends, insertions,
  truncations, relocation, false-positive, frontier pin, RV-3/PL-2 comparison).
- `build_trees.py`, `build_trees2.py`, `run_all.py` — reproducible builders and
  runner (exact-string, count-asserted seeds).
- `commands.txt` — every command, hashes, and expected outputs.
- `hashes-before.txt` — gate/PROVINCE hashes and `diff -q` proving the clean
  scratch tree is byte-identical to the repo copy.
- `repo-root-pl4.txt` — requirement (a) on the real repo root.
