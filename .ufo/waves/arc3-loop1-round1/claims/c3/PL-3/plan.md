# PL-3 — C3 plan: census v10 scope-table re-key at HEAD (measurement-first design)

Seat PL-3, chain c3, wave arc3-loop1-round1, 2026-10-19.
Repo HEAD (immobile — seats do not commit): `e845c2b524ad2e59871e004c51a1386e192a74ab`.
Instrument under test: `.ufo/gates/c1-census-v10.py`, sha256
`36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`.
Frozen claim C3: the E22 finding is dispositioned by measurement — census v10 is run
at HEAD; if any scope row is undeclared/stale the scope table is re-keyed (or the row
retired with cause recorded in the census header); the census then reports PASS
0/0/0/0 at the records commit with the disposition stated in the instrument's own
header; command A unchanged (no corpus/knowledge edit in this claim).

## 0. Headline: the measurement phase has already resolved the branch

- **v10 at HEAD → PASS 0/0/0/0, exit 0**, stdout sha256
  `3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418`, byte-identical
  across five independent runs (EX-26 ×2, EX-29, SC-6, RV-11) and re-verified by PL-3
  (`python3 .ufo/gates/c1-census-v10.py | sha256sum` → same digest).
- **The frozen "before" (FAIL undeclared=2 at HEAD) does not reproduce with v10 at
  HEAD.** It reproduces only on the old tree with the old instrument:
  - v9 (recovered) at tree `679af5d` (766-line SCORECARD): **FAIL undeclared=2** at
    blocks 731-737 / 747-766 — round-2's records append past v9's declared bound
    (`claims/c3/RV-11/scratch/v9-at-679af5d.txt`; this is the E22 finding verbatim).
  - v9 at `b21c0da` (701-line card): PASS (`.../v9-at-b21c0da.txt`).
  - v9 at HEAD (1336-line card), re-run first-hand by PL-3: **FAIL, exit 1** —
    `SCOPE-ERRORS: ["SCORECARD.md:635 marker '2026-10-18' absent from ''"]`,
    undeclared=2 at blocks 732-738 / 748-767.
- **Consequence for the chain:** at HEAD the re-key branch does **not** fire (no scope
  row is undeclared or stale); the deliverable is the *disposition* — and the
  discriminating before→after is the **instrument-revision flip on one tree**:
  v9@HEAD FAIL → v10@HEAD PASS (treatment = the round-4 v10 re-key + round-8 +1
  shift, both load-bearing), plus the E22-tree reproduction above. Do not manufacture
  a re-key to force a FAIL→PASS story; record PASS→PASS with the flip as the
  falsifiable unit (EX-26 §3 reaches the same flag independently).

## 1. Measurement-first procedure (designed; execution status marked)

| step | command / method | artifact | status |
|---|---|---|---|
| M1 verdict at HEAD | `python3 .ufo/gates/c1-census-v10.py` (+ `--json`, `--quiet`, rerun) | `claims/c3/EX-26/census-at-HEAD.{txt,json,quiet.txt,rerun.txt,exit}`; `claims/c3/EX-29/census-head-verbose.txt`; `claims/c3/SC-6/census-v10-at-head.txt`; `claims/c3/RV-11/census-head.out` | DONE (5-way identical) |
| M2 E22 reproduction | recovered v9 vs trees `679af5d` / `b21c0da` / HEAD | `claims/c3/RV-11/scratch/v9-at-*.txt`; PL-3 counter-run (§0) | DONE |
| M3 row classification | per-row bounds vs section headings, marker assertion, locus attribution | `claims/c3/EX-26/scope-alignment.txt`; `claims/c3/EX-29/{scope-audit,row-locus-counts}.txt`; PL-3 §2 | DONE |
| M4 tail scan | gated loci in undeclared tails | EX-26 §4.1 (instrument `classify()` probe + raw grep): 0 gated loci; PL-3 §3 | DONE |
| M5 records-commit re-measurement | re-run at the records commit; declare any new locus in the same commit | to be produced by parent / SC-7 / EX-31 | **PENDING** |

## 2. Row classification at HEAD — 20/20 aligned; 0 stale-bound; 0 retire-candidates

Method per row: (a) the row range lies inside exactly one section
(`[heading .. next heading − 1]`); (b) the row's first content line is the section
heading (row 19 leads its heading by exactly one blank line, SCORECARD:703 — intended,
a blank carries no locus); (c) the declared marker line matches its regex
(`SCOPE-ERRORS: []` at HEAD, G15 green); (d) every locus is attributed to a declared
row (EX-29 `row-locus-counts.txt`: "Blocks NOT attributed to any row: (empty)").

| # | file | range | class | marker | section | loci | action |
|---|---|---|---|---|---|---|---|
| 1 | PROVINCE.md | 8-13 | CURRENT | — | title..38 | 3 | keep |
| 2 | PROVINCE.md | 15-26 | CURRENT | — | ..38 | 9 | keep |
| 3 | PROVINCE.md | 40-43 | DATED | :40 "verified on this host 2026-10-13" | ## Core (38)..73 | 0 | keep |
| 4 | PROVINCE.md | 44-44 | CURRENT | — | ..73 | 1 | keep |
| 5 | PROVINCE.md | 45-62 | DATED | :40 (shared with row 3) | ..73 | 1 | keep |
| 6 | PROVINCE.md | 64-71 | CURRENT | — | ..73 | 1 | keep |
| 7 | PROVINCE.md | 119-131 | DATED | :119 "### Round-4 additions to Core (verified 2026-10-13)" | 119..133 | 1 | keep |
| 8 | SKILL.md | 10-16 | CURRENT | — | ## Domain (8)..28 | 1 | keep |
| 9 | SKILL.md | 18-20 | CURRENT | — | ..28 | 2 | keep |
| 10 | SCORECARD.md | 56-60 | CURRENT | — | ## Open gaps (51)..86 | 4 | keep |
| 11 | SCORECARD.md | 273-326 | DATED | :273 luna-round-2 header, 2026-10-16 | 273..327 | 2 | keep |
| 12 | SCORECARD.md | 417-466 | DATED | :417 luna-round-5 header | 417..467 | 0 | keep |
| 13 | SCORECARD.md | 467-502 | DATED | :467 luna-round-6 header | 467..503 | 0 | keep |
| 14 | SCORECARD.md | 503-533 | DATED | :503 luna-round-7 header | 503..534 | 1 | keep |
| 15 | SCORECARD.md | 534-560 | DATED | :534 luna-round-8 header | 534..561 | 1 | keep |
| 16 | SCORECARD.md | 619-619 | DATED | :619 capability row ("REA 6.5.0") | 615..626 | 1 | keep |
| 17 | SCORECARD.md | 620-620 | DATED | :620 capability row ("REA 6.4.0") | 615..626 | 1 | keep |
| 18 | SCORECARD.md | 636-702 | DATED | :636 round-1 header, 2026-10-18 | 636..704 | 1 | keep |
| 19 | SCORECARD.md | 703-768 | DATED | :704 round-2 header | 703..769 | 6 | keep (leads heading by 1 blank line) |
| 20 | SCORECARD.md | 769-855 | DATED | :769 round-3 header | 769..857 | 0 | keep |

Counts: 7 CURRENT + 13 DATED = 20; **stale-bound = 0; retire-candidates = 0**.
Re-key spec: not triggered. Retire-with-cause: no row's target content is gone
(every DATED row's section still exists and carries its marker). This is the
"re-key or retire" branch resolving to *neither*, on measurement, at HEAD.

## 3. Undeclared tails at HEAD — named, measured locus-free

| file | last declared end | tail | tail lines | gated loci in tail |
|---|---|---|---|---|
| PROVINCE.md | 131 | 132-162 | 31 | 0 |
| SKILL.md | 20 | 21-371 | 351 | 0 |
| SCORECARD.md | 855 | 856-1336 | 481 | 0 |

Evidence: EX-26 §4.1 (instrument `classify()` probe + raw grep: 0 `rea-agents` hits and
0 `6.x.y` hits beyond SCORECARD:855); PL-3 §5 A2/A5c independently. The tail is the
E22 hazard class's current home: **benign now, fail-closed later** — an append carrying
a gated locus fails the run (measured, A2) and must be declared in the appending
commit. The instrument's L1 intent ("file growth can never silently shrink the
census") is honored for loci; growth that adds no locus needs no row.

## 4. Records-commit coupling — the actionable core (EX-28 + parent)

Precedent rule (Z1, arc2-loop1-round4 §4d, verbatim): *"The census bound must be
re-keyed to the new EOF in this commit — the commit that appends the round-4 records
section is the commit that moves the bound."* Applied to this round: the commit that
appends the arc3-loop1-round1 records section is the commit that re-measures the census
and, if needed, declares the new loci.

Measured decision tree (PL-3 in-memory harness, §5):

- **(i) token-free append** — no PIN/VER/PTR in any gate-matching unit of the new
  section → PASS, **no scope change** (A5c). Preferred form (r3 E5 precedent:
  "a version-token-free append → undeclared stays").
- **(ii) append carrying loci** → add **one fixed-bound DATED row** covering exactly
  the new section, in the same commit, plus receipt language in each appended locus
  block (G11; G16 makes live-equal values `current-ok` even inside a DATED row) →
  PASS (A5b). Template:

  ```text
  # records-commit re-key template (apply only if (ii) fires)
  start=$(grep -n '^## arc3-loop1-round1' SCORECARD.md | head -1 | cut -d: -f1)
  end=$(wc -l < SCORECARD.md)          # last line at the records commit
  # SCOPE += ("SCORECARD.md", start, end, "DATED", start, r"2026-10-19"),
  #   - marker regex must match the heading line verbatim (G15 asserts it in the same run)
  #   - fixed bounds only: end is the commit's EOF; the next append starts at end+1
  #     and is undeclared again → re-key per commit (fail-closed, the r4 fork)
  #   - the appended blocks cite the round receipt / 2026-10-18 language (G11)
  ```
- **(iii) refused, with cause** — never in a re-key:
  - extending an existing row's end past its section (laundering by overshoot);
  - overshoot/sentinel bounds: **A6 reproduced the r4-refused path** — bound 768→10**9
    swallows a fresh stale claim into `historical (dated scope)` → PASS. The r4 wave
    measured the same both ways (E14 §3.6, E15 §…, P3, P4:204, Z1:40,301); v10 chose
    fixed bounds; keep that.
  - rewriting dated text (r3 adjudicated-not-edited precedent) — the fix for a dated
    record is a current note/row, never an edit of the record.

## 5. Attacks run (first-hand, in-memory harness — zero filesystem writes) and verdicts

Harness: `importlib` load of the instrument + `copy.deepcopy` of the three files +
instrument's own `classify()`/`assert_markers()`; SCOPE rows patched in memory only.

| id | attack | verdict |
|---|---|---|
| A0 | baseline, HEAD content in memory | PASS 0/0/0/0 — matches the on-disk run |
| A1 | strip marker `2026-10-18` from SCORECARD:636 | FAIL — `SCOPE-ERROR: SCORECARD.md:636 marker '2026-10-18' absent` (G15 fires) |
| A2 | append a records section carrying `rea-agents@6.5.0` into the undeclared tail | FAIL — UNDECLARED=1 at the appended line (fail-closed holds) |
| A3 | same append tagged inline `historical, superseded` | **FAIL — still UNDECLARED=1**: G16 re-labels the live-equal value `current-ok` (c1-census-v10.py:336-338) before the inline-marker branch (:344-345) can excuse it — the escape hatch is narrower than its name |
| A4 | insert one blank line at SCORECARD:636 (shift drift) | FAIL — 3 SCOPE-ERRORs (markers 636/704/769 all missed) |
| A5 | corrected re-key: new fixed-bound DATED row [1338,1340], marker 1338 = heading | FAIL on **G11 alone** (`g11=['SCORECARD.md:1340']`) — live-equal value reads current-ok and the block lacks receipt language |
| A5b | A5 + receipt language in the appended block | **PASS** — the re-key template of §4(ii) |
| A5c | token-free append, no new row | PASS — the preferred records-commit form |
| A6 | overshoot bound 768→10**9 (r4-refused path) + fresh stale claim at EOF | **PASS — laundering reproduced**; the fresh claim reads `historical (dated scope)` |
| A7 | modest overshoot 769→900 + same fresh claim | FAIL — overshoot only launders up to its bound; not a durable fix either |
| A8 | baseline restored | PASS (harness side-effect-free) |

## 6. EX-28 edit spec — header disposition (the claim's "disposition stated in the instrument's own header")

Target: `.ufo/gates/c1-census-v10.py`, module docstring (the file's own header).
EX-26's advisory hunk (`claims/c3/EX-26/proposed-census-header-disposition.patch.md`)
is the base; extend it to carry the measured evidence:

1. E22 disposition: **DISCHARGED BY MEASUREMENT at HEAD `e845c2b`** — v10 PASS
   0/0/0/0 exit 0 (stdout sha `3b677b8e…`, 5-way identical); E22 reproduced at its
   own tree (v9@679af5d FAIL undeclared=2, blocks 731-737/747-766) and v9@HEAD FAILs
   (marker@635 + undeclared=2) — the r4 v10 re-key + r8 +1 shift are load-bearing.
2. Row classification: 20 rows, 7 CURRENT / 13 DATED, **0 stale-bound, 0 retired**;
   re-key not required at HEAD.
3. Tail statement: PROVINCE 132-162, SKILL 21-371, SCORECARD 856-1336 are outside
   every row and locus-free at this commit; an append carrying a gated locus fails
   closed (UNDECLARED) and the appending commit must declare it in the same commit
   (fixed-bound DATED row, marker = its heading line; open-ended bounds refused per
   the arc2-loop1-round4 laundering measurements).
4. Restate at the records commit if line counts move (EX-26's note).

Verification of the edit (falsifiable):
- **Behavioral identity**: a header-only edit must leave stdout byte-identical —
  re-run and `sha256sum` → `3b677b8e…` unchanged; census verdict PASS unchanged;
  `git diff` on the file touches the docstring only.
- **Command A unchanged**: EX-30 T0 81/81, 13/13, 10.0/10.0; T1 must reproduce it
  (`claims/c3/EX-30/invariance.md`).
- **No corpus/knowledge edit** in this claim: `git status --porcelain -- corpus/` empty.

## 7. Constraints honored

- **r4 laundering-refusal**: every re-key form in this plan is fixed-bound; the
  open-ended/overshoot path is refused *with a first-hand reproduction* (§5 A6), not
  by citation alone; the fork ("fail-closed re-keying each round vs durability") is
  kept on the fail-closed side, as v10 shipped.
- **r3 adjudicated-not-edited**: no dated record is rewritten; the disposition lives
  in the instrument header + the records; a drifted dated row would be adjudicated
  (cause in the header), never silently edited.

## 8. Remaining work, owners, blockers

- **EX-28** (only census writer): land the §6 header disposition + the §4(ii) re-key
  template as patch text; re-run after the edit (behavioral identity).
- **Parent (records commit)**: re-run the census; if the append carries a locus, apply
  the §4 template in the same commit (Z1 r4 §4d rule).
- **SC-6/SC-7, RV-9..11, CR-5, VZ-3**: score/attack/verify — the strongest available
  charges are (a) "PASS→PASS is a no-op disposition" (answer: §0's v9@HEAD flip +
  the E22-tree reproduction are the discriminating measurements; the re-key branch
  fired and was recorded at r4/r8 — this round records the *disposition at HEAD*),
  (b) the G16/G11 interaction on live-equal values inside DATED rows (§5 A5/A5b),
  (c) the escape-hatch narrowness (§5 A3).
- **Blockers**: `/tmp` is EDQUOT-blocked for this user (standing hazard; EX-30 moved
  scratch to `/dev/shm/ex30`); PL-3 ran every attack in memory, zero scratch writes.
  Module imports recreate `.ufo/gates/__pycache__/` (shared side effect across c3
  seats; EX-26 recorded the class; PL-3 removes it at close).

## 9. Addendum — landings after this plan was written (measured, in-tree)

- **CR-5 (critic)** landed three attacks with receipts (`claims/c3/CR-5/…`):
  independent line-level re-derivation (20 rows, **0 out-of-range** occurrences,
  `tools/independent-census.py`); E22 reproduced at the 766-line tree / PASS at 701
  (matches §0); **r8 necessity proven** — the pre-r8 instrument at the
  post-insertion tree `6bc4c29` → 3 SCOPE-ERRORs, post-re-key → PASS, so the +1
  shift was a genuine alignment repair in the clean form; and
  **self-certification** — with a widened row the census still reports PASS
  0/0/0/0 (`receipts/census-widened-at-head.out`): the SCOPE table is both object
  and oracle, so the instrument's own PASS cannot certify a re-key. Certificates
  are external: the diff audit (`tools/scope-diff.py`), the independent checker,
  the historical reproductions. This strengthens §6: the header disposition must
  cite the external causal chain (v9 three-tree runs + the r8 necessity proof),
  never the instrument's own PASS alone — CR-5's own recommendation.
- **SC-6 (scribe)** landed the disposition draft with P1 (header stanza) and P2
  (round-records sentence), `claims/c3/SC-6/e22-disposition.draft.md`; P1 is
  compatible with §6 — extend it with the r8-necessity line and the CR-5
  self-certification caveat. SC-6's PTR note: the tail's two relative-path
  pointers (`rubric.json:61`) are outside the PTR unit by construction (PTR
  requires a `~` or `/` prefix) — a stated unit boundary, not a defect.
- **RV-11 (reviewer)** landed the instrument×tree matrix
  (`claims/c3/RV-11/e22-reproduction.md`): v10@HEAD PASS; matched instrument/tree
  pairs PASS; v10 at off-calibration trees FAIL (3 scope errors) — fixed bounds
  report off-calibration trees, never launder them.
- **EX-28 had NOT landed** at this addendum's write time (census sha256 unchanged
  `36e96cd5…`); the §6 header edit and the §4 re-key template remain open. M5
  (records-commit re-measurement) is parent-side by construction.
