# RV-4 — c1 chain: independent verification of PL-4's G21 frontier register

Seat RV-4, chain c1 (census instrument), wave arc3-loop1-round6, 2026-10-19.
Repo HEAD measured this session: `c625d5de57e045188b5ce8cd450a57b349f90785`
(`c625d5d`, records of round 5; work commit `58c3db7`). Live gate
`.ufo/gates/c1-census-v10.py` sha256
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 lines.
Scratch lab `/var/tmp/rv4-arc3r6` (never `/tmp`). The live gate, PROVINCE.md,
SKILL.md, SCORECARD.md and every tracked file were **not** modified; git was
used read-only (`rev-parse`, `log`). All runs below are first-hand (rule #14);
no prior seat's or round's value is quoted as evidence.

## 0. Verdict in one line

PL-4's patch is **reproduced byte-for-byte and works as delivered on the frozen
C1 falsifier**: clean tree PASS, seeded reintroduction of the retracted EVM
literal FAILs exit 1 with a named `FRONTIER-STALE` disposition, and requirement
(c) holds (SCOPE table and every pre-existing counter identical). Two measured
boundaries are reported, one of which **corrects a claim in the artifact**:
a line-count-neutral reflow that appends the retracted literal as a further
line of the same Frontier bullet (`PROVINCE.md:94`) reads **PASS** under r10,
so PL-4 §6.1's "insertions anywhere inside :73-162 are caught" is overstated;
and only the EVM literal is stale-gradable — the two other retracted
post-unlock literals read PASS when their REQUIRED tokens are retained.
Recommendation: do not land an r10 register with fixed `end` spans without an
end-boundary assertion (measured fix below), and land exactly **one** of the
four r10 builds now in the tree (§6.4).

## 1. First-hand re-derivations (the frozen C1 "before" facts)

| # | Frozen fact | My measurement (this session) | Verdict |
|---|---|---|---|
| 1 | HEAD `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e0…`; `git log --oneline -5` shows `c625d5d … (measured at work commit 58c3db7)` | VERIFIED |
| 2 | Instrument at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce8…d97b5`; `wc -l` → 610 | VERIFIED |
| 3 | SCOPE covers PROVINCE only 8-13/15-26/40-43/44/45-62/64-71/119-131 | gate `:216-222` (read): exactly those 7 PROVINCE rows; importlib comparison later shows the whole 20-row SCOPE table byte-identical between v10 and r10 | VERIFIED |
| 4 | Frontier region = 73-93 + 133-162 | `PROVINCE.md:73` `## Frontier`, intro 75-80, bullets 82-93; `:133` `### Round-4 frontier (post-unlock)`, bullets 135-162; `wc -l` = 162 | VERIFIED |
| 5 | v10 reads PASS identically whether or not the bullets are stale | planted the pre-`40de383` literal back into :91-93 (my tree `tree-seeded-forbidden`): v10 `VERDICT: PASS`, exit 0, counters byte-identical; same for a post-unlock retraction (`tree-postunlock-stale2`) and for a 161-line PROVINCE | REPRODUCED |
| 6 | (a) extended instrument still PASS on the current tree | r10 on `/var/tmp/rv4-arc3r6/clean` and on the real repo root: `VERDICT: PASS`, exit 0, `FRONTIER register (G21): 14 rows asserted, errors: []` | REPRODUCED |
| 7 | (b) seeded stale literal is caught with a named disposition | `tree-seeded-forbidden`: v10 PASS exit 0 → r10 FAIL exit 1, `DECLARED FAIL CLASSES: ['FRONTIER-STALE']`, 3 errors naming :91-93; `tree-seeded-forbidden-only`: exactly one error, `FORBIDDEN 'untested' matched 'untested'` | REPRODUCED for the frozen arm; **CORRECTED as a general statement** (finding F1) |
| 8 | (c) every SCOPE row / current counter intact | SCOPE lists identical (20/20 rows); 17 shared `--json` keys all equal, 0 mismatches; only `frontier_rows` / `frontier_errors` added; verbose text output identical apart from the one added `FRONTIER register` line | REPRODUCED |
| 9 | Patch identity claimed in PL-4 §4–§8 | pristine copy + `patch` → sha256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`, 713 lines = the delivered built instrument; embedded diff block in PL-4.md == `patch-v10-to-r10.diff` (10,574 bytes each); `patch --dry-run -p0` against the real path exits 0 with no offset/fuzz | REPRODUCED |
| 10 | PL-4 §6.1 "insertions anywhere inside :73-162 are caught" | counterexample measured: a line-count-neutral insertion at :94 (bullet extended by one line, one Adjacent line merged so `:119` keeps its marker) → v10 **PASS**, r10 **PASS**, `frontier_errors []`, while `PROVINCE.md:94` carries the retracted literal | **CORRECTED** |
| 11 | PL-4 §6.3 "only literals on record … are declared" | true as self-description, but the post-unlock retractions `~900s internal session deadline` (:139-144) and `probe-refused since r2` (:157-160) read PASS when their REQUIRED tokens are retained | boundary measured (F2) |

## 2. Patch application and custody

Commands and raw output: `RV-4/patch-apply.txt`. Key facts:

- Live gate before and after all work: `d0772ce8…d97b5` (610 lines) — unchanged.
- `patch --dry-run -p0 c1-census-v10.py < patch-v10-to-r10.diff` from
  `.ufo/gates/` → `checking file c1-census-v10.py`, exit 0 (exact, no fuzz).
- Applied to a pristine copy: sha `80027570…e18d14aecca`, 713 lines — equal to
  `claims/c1/PL-4/c1-census-v10-r10.py`.
- PL-4's landing recipe (`PL-4.md:355-361`) is correct; note the diff has no
  path prefix, so plain `patch <file>` (or `-p0`) works and `-p1` does not.
- The patch never touches the SCOPE rows: the `@@ -236,6 +275,37 @@` hunk is an
  insertion after the table's last row; a constant-level import comparison
  confirms `SCOPE` identical (20 rows) and every compiled pattern
  (`PIN/VER/PTR/CACHE/REA_GATE/INLINE_MARKER/RECEIPT/SECTION/BULLET/
  CLAUSE_SPLIT/HOLDING/HOLDING_OK`) identical.

## 3. Fault matrix — my trees × both instruments

All trees are byte-copies of HEAD's PROVINCE.md / SKILL.md / SCORECARD.md with
one content-asserted edit (builder: `/var/tmp/rv4-arc3r6/make_trees.py`; the
seeded-forbidden trees are byte-identical to PL-4's preserved scratch trees —
`diff -q` → identical). Full outputs: `RV-4/arms.txt`,
`RV-4/arm-matrix.tsv`, `RV-4/exit-codes.txt`.

| tree | v10 | r10 | r10 declared class | key r10 error |
|---|---|---|---|---|
| clean | PASS 0 | PASS 0 | [] | — |
| seeded-forbidden (frozen example) | PASS 0 (blind) | FAIL 1 | `['FRONTIER-STALE']` | `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested'` + 2 REQUIRED-absent |
| seeded-forbidden-only | PASS 0 (blind) | FAIL 1 | `['FRONTIER-STALE']` | exactly one error: `:91-93 FORBIDDEN 'untested' matched` |
| stripped-required (`22/24`→`2x/2x`) | PASS 0 (blind) | FAIL 1 | `['FRONTIER-UNEVALUABLE']` | `:149-150 REQUIRED '22/24' absent` |
| truncated-161 | PASS 0 (blind) | FAIL 1 | `['UNREADABLE','FRONTIER-UNEVALUABLE']` | `PROVINCE.md: 161 lines < declared max 162`; 14 uncheckable |
| reflow-insert (blank line before :133) | PASS 0 | PASS 0 | [] | register silently grades shifted lines (spans all still match) |
| **reflow-bullet** (EVM bullet extended to :94, one Adjacent merge, 162 lines) | **PASS 0** | **PASS 0** | **[]** | **stale literal present at :94, missed — F1** |
| extend-evm (+1 line at :94, 163 lines) | FAIL 1 (G15 marker shift) | FAIL 1 | [] | `FRONTIER register … errors: []`; FAIL is the old `:119` marker, not the stale literal |
| postunlock-stale (`arc2-r7` removed too) | PASS 0 | FAIL 1 | `['FRONTIER-UNEVALUABLE']` | REQUIRED absent — not a stale catch |
| **postunlock-stale2** (both retractions, tokens kept) | **PASS 0** | **PASS 0** | **[]** | **F2: both literals ungraded** |
| append-163 (new bullet past :162) | PASS 0 | PASS 0 | [] | PL-4 residual #1, reproduced |

PL-4's own five preserved scratch trees, run with my applied r10, reproduce
their §3 table exactly (`RV-4/arms.txt`, `pl4scratch-*`): clean PASS;
seeded-forbidden / seeded-forbidden-only `FRONTIER-STALE`; seeded-required-evm
and -riscv `FRONTIER-UNEVALUABLE`; clean-truncated
`['UNREADABLE','FRONTIER-UNEVALUABLE']`.

## 4. Counter identity (requirement c)

`RV-4/json-identity.txt`, clean scratch, `--json` on both instruments:

```
shared keys: 17
mismatched: []
v10-only: []
r10-only: ['frontier_errors', 'frontier_rows']
counts equal: True {'PROVINCE.md': {'lines': 162, 'loci': 6},
                    'SCORECARD.md': {'lines': 1696, 'loci': 9},
                    'SKILL.md': {'lines': 390, 'loci': 2}}
current_ok_per_file equal: True {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
g2_ok: True True | g11: [] [] | g7: [] []
verdict: PASS PASS
r10 frontier_rows: 14 frontier_errors: []
```

PL-4's stored `v10-clean.json` (17 keys) and `r10-clean.json` (19 keys) were
also compared key-by-key against my fresh runs: 0 mismatches, no one-sided
keys. The verbose text output of r10 equals v10's byte-for-byte after deleting
the single added `FRONTIER register (G21): …` line.

## 5. Register audit (the 14 rows)

`RV-4/register-audit.txt`. At HEAD:

- 14 rows, spans 75-80, 82-83, 84-86, 87-88, 89-90, 91-93, 135-138, 139-144,
  145-146, 147-148, 149-150, 151-156, 157-160, 161-162; every REQUIRED regex
  matches in its span, no FORBIDDEN match; spans do not overlap.
- Every non-blank line of `## Frontier` 73-93 and of the post-unlock section
  133-162 is inside a registered span except the two section headers
  (`:73`, `:133`) — deliberate in the design (the artifact registers bullets,
  not headers).
- End-boundary property at HEAD: for every row, the line after its `end` is
  blank, a bullet start, a header, or EOF — 0 violations. The reflow-bullet
  tree violates exactly this for row 91-93 (line 94 is a continuation), which
  is the mechanism behind F1.

## 6. Findings

### F1 — CORRECTED: a line-count-neutral intra-bullet extension reads PASS

`RV-4/reflow-fail-open.txt`. Tree `tree-reflow-bullet` is 162 lines. The EVM
bullet is re-wrapped from 3 to 4 lines and the retracted claim is appended as
the bullet's new last line at `:94`; to keep the tree at 162 lines and line
`:119` stable, two lines of the (unregistered) Adjacent bullet at :100-101 are
merged. Result:

```
PROVINCE.md:91  - **EVM bytecode (extended)** — …
PROVINCE.md:92    (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a
PROVINCE.md:93    vyper-0.4.3 carrier (arc3-r4); … (no signature
PROVINCE.md:94    DB → no name resolution). real solc/vyper-compiled bytecode untested.

v10: VERDICT PASS (exit 0), SCOPE-ERRORS []
r10: VERDICT PASS (exit 0), FRONTIER register (G21): 14 rows asserted, errors: []
```

The literal named by the frozen claim is present inside the Frontier bullet
(:94, a two-space-indented continuation of the bullet that starts at :91), yet
the register's fixed span 91-93 never reads it. Note the contrast with the
simple +1 variant (`tree-extend-evm`, 163 lines): there the register also
reports `errors: []`, and the overall FAIL comes only from the pre-existing G15
marker shift at `:119` — a class that names neither the bullet nor the stale
literal. PL-4's §6.1 sentence "Insertions anywhere inside `:73-162` are caught"
is therefore false in the sense that matters: an insertion at :94 can be
invisible to the register, and with a compensating line-count move the whole
run returns PASS.

Root cause is structural, not a coding slip: every row's `end` is a fixed line
number, so text appended *inside* the same list item beyond that line is out of
scope. A cheap closure that I measured (not landed; no gate edit by this seat):

> For every row, assert that the line after `end` is blank, a new bullet, a
> header, or EOF (i.e. the span ends on the bullet's last line). At HEAD this
> property holds for all 14 rows; on `tree-reflow-bullet` it fires on row
> 91-93 (`(91, 93, '  DB → … untested.')`), turning the run FAIL. A more
> robust variant derives each bullet's end by scanning from `start` to the
> next blank/next bullet instead of hard-coding it.

### F2 — boundary: only the EVM literal is stale-gradable

`RV-4/postunlock-boundary.txt`. `tree-postunlock-stale2` restores the two
post-unlock retractions that the round-4 history measured stale and repaired in
`40de383` — `hits REA's ~900s internal session deadline` at :139 and
`probe-refused since r2` at :157 — while keeping each row's REQUIRED tokens
(`arc2-r7`, `r12-02`). Both gates read PASS, `frontier_errors []`. This is
covered by PL-4 residual #3 (FORBIDDEN coverage is earned, not exhaustive), so
it is not a contradiction of the artifact; it is the measured extent of "the
Frontier-region staleness claims become gradable." If the lane wants the other
two claims gradable, the literals are already on record in `40de383~1` and can
be added as FORBIDDEN patterns (the in-flight PL-1 build does exactly this —
§6.4).

### F3 — minor: declared-class precedence loses information

`frontier_class` (PL-4 patch hunk `@@ -564,15 +661,19 @@`) is an `if/else`
chain: when a row has both a FORBIDDEN match and REQUIRED-absent errors, only
`FRONTIER-STALE` is reported (measured on `tree-seeded-forbidden`: 3 register
errors, declared class only `['FRONTIER-STALE']`). Functionally fail-closed and
not wrong for the frozen arm, but the class list drops `FRONTIER-UNEVALUABLE`.
A sorted set over error kinds reports both (the in-flight PL-1 build does this).

### F4 — design deltas and convergence note

The c1 chain now holds four builds that each label the result "r10". PL-1 is a
successor applied on top of PL-4; PL-2 and RV-3 are independent designs applied
to the pristine gate, so they cannot be stacked with each other or with the
PL-4→PL-1 chain. Landing must pick one line of descent:

| build | artifact | digest of the gate it produces | anchors | FORBIDDEN literals | stale catch on my arms |
|---|---|---|---|---|---|
| PL-4 | `claims/c1/PL-4.md` (+ patch) | `80027570…` (applied, verified) | no | 1 (`untested`) | frozen arm yes; F1/F2 no |
| PL-2 | `claims/c1/PL-2.md` + `prior-attempt/` (reorganised in-flight) | stated `2d7ee95b…` (not applied by me) | header markers via SCOPE rows | 3 (cited) | not verified by me |
| RV-3 | `claims/c1/RV-3.md` | stated `8e420679…` (not applied by me) | per-row anchor line + cite | 1 (`untested`) | not verified by me |
| PL-1 | `claims/c1/PL-1/patch-pl4-to-pl1.diff` (in-flight) | `7724adcc…` (applied by me, read-only probe) | per-row anchor + section headers | 3 (cited to `40de383~1`) | frozen arm yes; F2 yes; +1 extension yes (`FRONTIER-ANCHOR`); **F1 still PASS** |

PL-1 probe (`RV-4/pl1-successor-probe.txt`): applied cleanly to my PL-4 r10
copy; clean PASS; seeded-forbidden catches; `tree-postunlock-stale2` catches
both literals; `tree-extend-evm` fails loudly via shifted anchors; but
`tree-reflow-bullet` (intra-bullet extension, no line moves) still reads PASS
with the literal at :94. This confirms the gap is the fixed span *end*, not the
lack of anchors alone. I did not verify PL-2's or RV-3's builds; their digests
above are quoted only as identifiers, not as evidence.

## 7. Recommendation to the landing seat

1. PL-4's patch is safe to land only if the register's fixed ends are
   strengthened first, or if the wave accepts F1/F2 as named residuals. It
   meets the frozen claim's lettered falsifier under the measured arm; it does
   not meet "no silent PASS on a reintroduced Frontier claim" in general.
2. Minimum strengthening: the end-boundary assertion of F1 (one check per row;
   at HEAD 0 violations, on the counterexample 1) plus the two `40de383~1`
   literals from F2. Both are measured here; neither requires touching SCOPE or
   any existing counter.
3. Land exactly one r10 build. Re-derive the post-landing gate sha in the
   landing receipt (the gate's own rule-#14 discipline, `c1-census-v10.py:89-93`).
4. If an r10 build is landed, re-run the frozen arm plus F1/F2 on scratch and
   require: clean PASS, frozen arm `FRONTIER-STALE`, F1 arm FAIL naming :94 or
   the row, F2 arm FAIL naming both literals.

## 8. What I did NOT do

- Did not modify the gate, PROVINCE.md, SKILL.md, SCORECARD.md, corpus, or any
  tracked file; the live gate sha is unchanged before/after (`d0772ce8…`).
  `git status --porcelain` at hand-off shows one pre-existing modified tracked
  file, `.ufo/waves/arc2-loop1-round10/C3.md` (mtime 2026-10-18 23:01, before
  this session; not touched by RV-4) and the round-6 wave tree as untracked.
- Did not write the gate or land any patch; all instrument work was on scratch
  copies under `/var/tmp/rv4-arc3r6`.
- Did not re-derive c2 (command-A counts) or c3 (`rule_blocks`) numbers — other
  chains.
- Did not independently apply or verify PL-2's and RV-3's builds; the PL-1
  successor probe is a read-only measurement on my trees, not a seat verdict on
  PL-1's artifact.
- Did not claim the historical "R4/R5 clause audit was by hand" process fact;
  only the operative half (the region was ungraded) is measurable from the tree.

## 9. Evidence inventory

All under `.ufo/waves/arc3-loop1-round6/claims/c1/RV-4/`:

- `patch-apply.txt` — live-gate sha/line count, exact dry-run, applied sha
  `80027570…`, built-instrument equality, post-work gate sha.
- `baseline-clean.txt` — clean scratch v10 and r10 full reports.
- `arm-matrix.tsv`, `exit-codes.txt`, `arms.txt` — the full 11-tree matrix
  with exit codes, declared classes, and register error lists.
- `reflow-fail-open.txt` — F1 and F1b trees, both gate outputs, literal proof.
- `postunlock-boundary.txt` — F2 tree and both gate outputs.
- `json-identity.txt` — 17-key identity, counts, floor map.
- `register-audit.txt` — 14 rows, coverage, overlaps, end-boundary property at
  HEAD vs the counterexample tree.
- `pl1-successor-probe.txt` — in-flight PL-1 build on my arms (peer probe).
- `commands.txt` — reproduction recipe.

Scratch: `/var/tmp/rv4-arc3r6/` (trees, seeder `make_trees.py`, applied r10
copy). PL-4's preserved scratch `/var/tmp/pl4-arc3r6/` was read only (its
seeded-forbidden trees are byte-identical to mine).
