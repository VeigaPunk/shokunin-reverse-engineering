# PL-2 — c1 chain (census instrument): Frontier blind-spot closure, patch text + seeded-fault proof

Seat: PL-2, wave arc3-loop1-round6, chain c1. Date: 2026-10-19.
Repo HEAD measured: `c625d5de57e045188b5ce8cd450a57b349f90785` (`git rev-parse HEAD`;
work commit `58c3db7` two entries below in `git log --oneline`). Everything below is
re-derived first-hand at this HEAD per rule #14; no prior seat's value is quoted as
evidence. All scratch work in `/var/tmp/pl2-arc3r6-c1` (never `/tmp`). The live gate
`.ufo/gates/c1-census-v10.py` was NOT edited (sha256 before = after all my work:
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`).

## 1. What I re-derived first-hand

### 1.1 v10 baseline at HEAD (instrument unchanged)

Command: `python3 .ufo/gates/c1-census-v10.py --quiet` at the repo root. Output
(full transcript in `PL-2/arms.txt` §"v10 baseline"):

```
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1696 loci=9
SKILL.md       lines=390  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit=0
```

### 1.2 The blind spot is real (programmatic, not eyeball)

Loaded the gate's SCOPE via `importlib` and computed coverage:

- PROVINCE.md rows: exactly `8-13, 15-26 (CURRENT); 40-43, 45-62, 119-131 (DATED); 44, 64-71 (CURRENT)`
  — matches claims-frozen C1's list.
- `covering rows for (73,93) = []` and `covering rows for (133,162) = []` → both
  Frontier regions UNDECLARED. VERIFIED.
- Line identity: `PROVINCE.md:73` = `## Frontier`; `PROVINCE.md:133` = `### Round-4 frontier (post-unlock)`
  (file is exactly 162 lines, `wc -l PROVINCE.md` → 162).
- At HEAD neither region holds any instrument-visible unit: no `REA_GATE` match, no
  PIN/VER/PTR occurrence, and the literal `untested` is absent from both regions.
  This is WHY v10 reads PASS identically whether or not the locus-free bullets are
  stale — L3 never sees a locus there.

### 1.3 The seeded-fault literal is grounded in measured history

`git show 40de383 -- PROVINCE.md` (arc3-loop1-round4 work commit) shows the exact
before→after at :91-93:

```
-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
-  bare hashes (no signature DB → no name resolution).
+  (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3
+  carrier (arc3-r4); selectors stay bare hashes (no signature DB → no name resolution).
```

The same commit's diff shows two more measured-stale before-states in the post-unlock
region: the `>90 MB PE` wall form ("hits REA's ~900s internal session deadline … Next:
raise REA_GHIDRA_STARTUP_TIMEOUT_MS…" — measured false at arc2-r7, now CLOSED/held) and
the cross-version form ("`compare-application-versions` still probe-refused since r2;
multi-version pacman pairs beyond expac unexercised" — exercised r12-02/r14-01). These
three literals are the register entries, each cited to `40de383`.

## 2. Decision: in-place extension (r10), not a v11 fork

Recorded choice per claims-frozen C1 ("a v11 or an in-place extension is the lane's
choice"): **in-place additive extension, revision tag r10**, because (a) the claim's
constraint "keep every existing SCOPE row and every current counter intact" is
mechanically auditable on an additive-only diff (below: zero shared `--json` key
drift); (b) the instrument's own convention is in-place revision blocks (r9 was one);
(c) a v11 fork would duplicate the digest identity the landing receipts track
(sha256-per-revision in SCORECARD/LOG receipts) without adding structure. The patch
below applies to `.ufo/gates/c1-census-v10.py` as-is.

## 3. Patch text (deliverable)

Unified diff, `HEAD c625d5d` gate → proposed r10 (also on file as
`PL-2/c1-census-v10-r10.patch`; full proposed instrument as
`PL-2/c1-census-v10-r10-proposed.py`, sha256
`2d7ee95ba2743bde0b658c91d867a46e04e3e9e14de41d2cb60f2ff46238ce7b`):

```diff
--- .ufo/gates/c1-census-v10.py   (HEAD c625d5d, sha256 d0772ce8…)
+++ .ufo/gates/c1-census-v10.py   (proposed r10, seat PL-2)
@@ -1,4 +1,32 @@
-"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d.
+"""C1 census v10 — r10 (arc3-loop1-round6, seat PL-2): Frontier blind-spot
+closure (rounds 4-5 R1 residual, claims-frozen C1). Additive in-place
+extension, measured at HEAD c625d5d (instrument sha256 before this edit
+d0772ce8…): the SCOPE table covered PROVINCE.md only at 8-13/15-26/40-43/44/
+45-62/64-71/119-131; the `## Frontier` section (73-93) and the post-unlock
+frontier (133-162) were UNDECLARED, and neither region held any REA_GATE
+unit or PIN/VER/PTR occurrence at HEAD — so L3 never saw a locus there and
+v10 read PASS identically whether or not the locus-free frontier bullets
+were stale (reproduced: seeded before-state "real solc/vyper-compiled
+bytecode untested" back into :92-93 reads v10 PASS exit 0). Closure, three
+additive pieces:
+  1. Two SCOPE rows classed FRONTIER (73-93, 133-162). The class rides the
+     CURRENT grading path in classify() (a drift reads STALE, never
+     DATED-sheltered — the t5 shelter lesson) and each row declares a
+     structural header marker asserted like a DATED marker (G15/G18
+     machinery), so a reflow that moves the section fails declared, not
+     silently mis-graded. At HEAD both markers match, scope_errors stays [].
+  2. FRONTIER_STALE, a declared claim register for locus-free bullets: each
+     entry is a literal whose staleness a past round MEASURED, cited to the
+     repairing commit (rule #14). A hit inside its declared range is the
+     declared FRONTIER-STALE class (text + --json, exit 1).
+  3. G19 max-end for PROVINCE.md rises 131 -> 162 with the declared row —
+     the same could-not-evaluate strictness every scoped file already has.
+Every pre-existing SCOPE row, counter and classify() branch is untouched;
+clean-tree invariance (PASS 0/0/0/0, counters and floor map identical) is
+the r10 acceptance arm, the seeded register hit and a seeded reflow are the
+falsification arms.
+
+E22 DISPOSITION — arc3-loop1-round1, EX-28 (measured 2026-10-19 at HEAD
 e845c2b; instrument sha256 before this edit 36e96cd5…). The arc2-loop1-round3
```
*(the remaining hunks are identical to `PL-2/c1-census-v10-r10.patch`; the full
195-line file is the authoritative patch text — summary of hunks: docstring
title `v10-r9` → `v10-r10`; DEFECT CLASSES gains G21/G22 and the Verdict line
gains "AND frontier register clean (r10)"; SCOPE gains the two FRONTIER rows;
`FRONTIER_STALE` register (3 cited entries) + `frontier_scan()` added;
`assert_markers` guard widened `!= "DATED"` → `not in ("DATED", "FRONTIER")`;
`main()` gains `frontier_hits`, the `FRONTIER-STALE` declared class, `--json`
keys `frontier_stale`/`frontier_register`, a FRONTIER-STALE report line, and
`frontier=%d` in the VERDICT line. `classify()` is untouched.)*

Design notes a reviewer needs:

- **FRONTIER rides the CURRENT grading path.** `scope_of()` returns
  `("FRONTIER", ml, mr)` for the new rows; every `classify()` branch tests
  `cls == "DATED"`, so a FRONTIER locus that misses a live anchor reads STALE
  (exit 1), never `historical` — no DATED-shelter (the t5 lesson), and no new
  `classify()` code at all.
- **Locus-free staleness is the register's job.** The region's bullets carry no
  pin/version/path occurrence (measured, §1.2), so no scope change alone can
  grade them; `frontier_scan()` checks each declared literal line-by-line
  inside its declared range.
- **Structural markers.** The FRONTIER rows declare their section headers
  (`^## Frontier$` at :73, `^### Round-4 frontier \(post-unlock\)$` at :133);
  `assert_markers` (G15/G18) now also asserts them, so a reflow that moves a
  section fails declared instead of silently mis-grading shifted lines.
- **Register hygiene is append-only with citations** (rule #14); widening a
  pattern requires a measured clean-tree run.

## 4. Demonstration (scratch trees, all in `/var/tmp/pl2-arc3r6-c1`)

Trees built by copying PROVINCE.md/SKILL.md/SCORECARD.md at HEAD and seeding;
`tree-seeded-literal/PROVINCE.md` differs from HEAD by exactly the 2-line
before-state reintroduction (`PL-2/seed-fault.diff`, hunk at :89-93). Transcripts:
`PL-2/arms.txt`.

| Arm | Gate | Tree | Result | Exit |
|---|---|---|---|---|
| baseline | v10 | real repo | PASS, counters as §1.1 | 0 |
| A (blind spot) | v10 | seeded-literal | **PASS, all counters zero — blindness REPRODUCED** | 0 |
| B (invariance) | r10 | clean scratch | PASS, counters identical to baseline | 0 |
| D (invariance) | r10 | real repo | PASS, counters identical to baseline | 0 |
| C (seeded fault) | r10 | seeded-literal | **FAIL, `DECLARED FAIL CLASSES: ['FRONTIER-STALE']`, hit = `PROVINCE.md:92 'solc/vyper-compiled bytecode untested' (r4 before-state, repaired in 40de383)`, verdict line `frontier=1`** | 1 |
| E (reflow) | r10 | blank line before :133 | FAIL via `scope_errors`: `PROVINCE.md:133 marker '^### Round-4 frontier \\(post-unlock\\)$' absent from ''` | 1 |
| F0 (locus drift, v10) | v10 | stale pin `rea-agents@6.4.0` in bullet :82-83 | FAIL `undeclared=1` (coarse class) | 1 |
| F1 (locus drift, r10) | r10 | same tree | FAIL `stale=1 undeclared=0`, locus line `PROVINCE.md block 82-83 [scope FRONTIER] / :83 [pin] kimi=6.4.0 -> STALE (live kimi=6.7.0)` | 1 |

**JSON invariance (claim constraint (c)):** `--json` of v10 vs r10 on the real
tree — shared keys with differing values: **NONE**; keys only in r10:
`frontier_register: 3`, `frontier_stale: []` (`PL-2/json-v10-head.json` vs
`PL-2/json-r10-real.json`). Every existing SCOPE row is present and byte-identical
in the patch (the SCOPE hunk is pure insertion after the last row).

## 5. Per-item verdicts

| Item | Verdict | Evidence |
|---|---|---|
| HEAD `c625d5d` (work `58c3db7`) | VERIFIED | `git rev-parse HEAD` / `git log --oneline -3`, §1 header |
| v10 baseline PASS 0/0/0/0 at HEAD | REPRODUCED | §1.1 transcript, exit 0 |
| SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131 | VERIFIED | importlib dump, §1.2 |
| Frontier 73-93 + 133-162 UNDECLARED (no covering row) | VERIFIED | covering rows `[]` for both regions, §1.2 |
| Neither frontier region holds any REA_GATE unit or PIN/VER/PTR locus at HEAD | VERIFIED | programmatic scan, §1.2 (this is the mechanism of the blindness) |
| v10 reads PASS on a stale Frontier literal (the R1 residual) | REPRODUCED | Arm A: seeded before-state at :92-93 → PASS exit 0 |
| Seeded literal `real solc/vyper-compiled bytecode untested` is the r4 before-state of :91-93 | VERIFIED | `git show 40de383 -- PROVINCE.md`, §1.3 |
| r10 patch: clean tree still PASS, counters/rows intact | REPRODUCED | Arms B/D + JSON invariance §4 |
| r10 catches the seeded reintroduction, named disposition | REPRODUCED | Arm C: FAIL exit 1, FRONTIER-STALE, names :92 + citation |
| Register entries 2-3 (`~900s` wall form, `probe-refused since r2`) catch their own literals | UNVERIFIABLE (not exercised) | only entry 1 was arm-tested (the claim's named seed); entries 2-3 are grounded in the same `40de383` diff but have no seeded arm in this seat — cheap to add if the lane wants all three exercised |
| FRONTIER class semantics (drift → STALE, never DATED-sheltered) | REPRODUCED | Arm F1 vs F0: `stale=1 undeclared=0` with `[scope FRONTIER]` vs v10's `undeclared=1` |
| Reflow of a frontier section fails declared | REPRODUCED | Arm E: scope_errors names the FRONTIER marker at :133 |

## 6. Residuals (named, not silently absorbed)

1. **Register is a literal list, not a semantics engine.** A quoted mention of a
   stale literal (e.g. "never claim: 'bytecode untested'") inside a declared
   range would false-positive. Same class of residual as any census needle; the
   disposition names file:line + pattern + citation, so it is reviewable. The
   three post-unlock ranges only carry patterns scoped to their own bullets.
2. **Register entries 2-3 unexercised by a seeded arm** (see §5) — entry 1
   carries the claim's falsifier and is demonstrated end-to-end.
3. **G19 max-end for PROVINCE.md rises 131 → 162** with the declared row: a
   future truncation below 162 lines becomes UNREADABLE (declared) instead of
   silently in-scope-shorter. Strictness increase, measured clean at HEAD
   (162 lines).
4. **The claim-register vocabulary is deliberately narrow.** It does not
   detect *novel* frontier staleness — only re-introductions of literals the
   arc already measured stale. Novel-claim staleness in the region stays with
   the round audit + REA-of-the-art external checks, as today.

## 7. File inventory (this seat's writes)

- `…/waves/arc3-loop1-round6/claims/c1/PL-2.md` — this artifact.
- `…/claims/c1/PL-2/arms.txt` — all arm transcripts (fresh runs, final r10).
- `…/claims/c1/PL-2/c1-census-v10-r10.patch` — authoritative 195-line unified diff.
- `…/claims/c1/PL-2/c1-census-v10-r10-proposed.py` — full proposed instrument
  (sha256 `2d7ee95b…38ce7b`).
- `…/claims/c1/PL-2/seed-fault.diff` — seeded tree vs HEAD PROVINCE.md (2-line before-state).
- `…/claims/c1/PL-2/json-v10-head.json`, `…/json-r10-real.json` — the invariance pair.

No tracked file, gate, corpus, PROVINCE/SKILL/SCORECARD, or custody path was
modified; git used read-only throughout.
