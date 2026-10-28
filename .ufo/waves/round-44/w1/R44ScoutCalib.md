# R44-C2 wave-1 census — candidate rubric statements (R44ScoutCalib)

Seat: `R44ScoutCalib`. Task: enumerate candidate self-assessment statements for the
R44-C2 frozen rubric (`plans/round-44-claims.md` §R44-C2, categories a–f), each with a
check command and its asserted-vs-observed verdict at the base. Recon only; nothing
modified. Machine form: `.ufo/waves/round-44/w1/R44ScoutCalib.json` (98 rows, same
schema: `{file, line, asserted, check, observed, mismatch}` — `note` fields are in
the scratch copy, condensed into `observed` here where decisive).

Base `c29360e3ba5381a5ab69e372d0d9577970f85018`. The three target files
(SCORECARD.md, SHONEN.md, corpus/README.md) are byte-identical at base and tip —
`git diff c29360e3 HEAD` touches only `plans/round-44-claims.md`.
All checks are read-only `git show`/`ls-tree`/`cat-file`/`diff` against lane git
objects (plus one out-of-lane fleet file where flagged). No network, no REA, no
writes inside the lane. `<REV>` = the statement's own pinned revision where the
text carries one, else `c29360e3`. `<command_a.py>` = the SCORECARD.md:93-123
command-A recipe, verbatim (copy at scratch `probe-R44ScoutCalib/command_a.py`).

## Headline

**16 of 98 candidate statements mismatch repo state at the base** → the wave-1
census does NOT find zero mismatches; the C2 claim does not stop on CTL-C2-0
grounds. Several flags carry convention notes a rubric author must decide
(scope of "living" vs "historical" text, line-pin vs revision pinning,
marker-free discharge). All are listed so the rubric can refuse or accept each.

Command A was re-derived at 10 revisions (raw log `probe-R44ScoutCalib/cmdA.log`,
sha256 `42b50809…`): base 137/137 files+21/21 rules; `8de80f1d` 137/137;
`6b9e64fe` 135/135; `d4b4b4fb` 135/135 but citation_resolved **20**/21
(depth_score 9.52 — the round-42 row's "command A resolves 21/21" is true at
base, NOT at `d4b4b4fb`; the row itself says "measured in the report", holds);
`e1c83313` 133/133 + 20/20; `4d62ee5a` 130/130 + 19/19; `52b0eb29` 128/128 +
18/18; `cab59f22` 122/122 + 17/17; `c369242f` 116/116 + 17/17; `ebe2cb4a`
109/109 + 17/17. Every pinned count in the `## Owned axes` rows reproduces at
its own pin.

## Flagged mismatches (candidates for the frozen rubric)

| # | file:line | asserted | observed at BASE | class |
|---|---|---|---|---|
| 1 | SCORECARD.md:23 | coverage headline opens on "133/133 … after the round-41 landing" | command A at base: 137/137 (135 at d4b4b4fb, 137 at 8de80f1d); headline cell leads with the round-41 pin | stale-headline / pinned-true |
| 2 | SCORECARD.md:24 | depth headline opens on "20/20 … at e1c83313" | command A at base: 21/21 | stale-headline / pinned-true |
| 3 | SHONEN.md:16 | "the frozen C2 score tool stops on an overstrict raw line-count check" | SHONEN.md:18's own correction: scorer+plan both require `3\t0`, actual `4\t0` — "not an overstrict-counter false negative"; frozen text contradicts the repo fact and the later line | frozen-text vs appended-correction |
| 4 | SCORECARD.md:152-154 | "**planned:** calibration — reconcile province/skill vs live REA inventory" | done by luna-round-2 (:56 "closed by", :275 executes it); field never marked done/superseded (C2Cherrypick #6) | marker-free discharge |
| 5 | SCORECARD.md:3072 | planned (r26): "counting script and expected values committed before any REA run" | r26 ran a pre-freeze `inspect-binary-layout` probe 11:59:16Z and `tools/round-26` absent at freeze c27f445 — self-disclosed at :3077/:3096 | clause deviation, self-disclosed |
| 6 | SCORECARD.md:3213 | planned (r30): "blind naming test … lists drawn by a rule the L1 does not control" | round 30 worked `inspect-rust-binary`; no `(after a steer)` marker on the row; departure recorded only in round-30's own text (:3218) | unmarked deviation |
| 7 | SCORECARD.md:3250 | planned (r31): "`inspect-rust-binary` refusal signatures on PE and Mach-O" | round 31 worked `inspect-sqlite-database`; "Anti-loop: leaves REA's Rust reader" :3255; unmarked on the row | unmarked deviation |
| 8 | SCORECARD.md:3400 | "planned (round 37)" — BE SquashFS v4 via sasquatch-v4be | **no `## Round 37` section exists**; round 38 worked exactly this surface — numbering anomaly, unexplained in card | numbering |
| 9 | SCORECARD.md:3466 | planned (r42): "keep the v3 table bytes" while refreezing R41-C2 | round 42 scored a NEW table v4 (block 21) — v3 bytes do remain at :440, but the scored artifact isn't v3 | sub-clause deviation |
| 10 | SCORECARD.md:3498 | "**planned (round 43, after a steer):** depth — refreeze R42-C2 …" | bullet sits INSIDE the round-43 section (after the R43 table); the round-42 section (:3469-3486) has no planned row — misplaced row; content does match round-43 work | placement/numbering |
| 11 | SCORECARD.md:3489 | "wave 2: 32 seats dispatched and pending final settlement" | at base: 26 w2 reports + `r43-w2-results.json` committed; LOG:3189 "32/32 settled"; verifier spot-check is an ancestor of base — sentence stale | temporal staleness |
| 12 | SCORECARD.md:46 | C6 "Current map is 70/72, missing r14-01 and r14-02" | command A at base: 137/137 missing [] (70/72 was true at baseline a79945c4) | historical phrased as present |
| 13 | SCORECARD.md:78 | "the old entry remains correction debt" (jq 'benign') | entry carries a Safety-verdict scope qualification since luna-round-9; bullet has no closed-by note (C2Cherrypick #4) | discharge-without-marker |
| 14 | SCORECARD.md:81-83 | "real compiled EVM input, oversized cores, large PE analysis … remain as documented" | PROVINCE:139 "CLOSED (arc2-r7)"; real-solc Core :91-92; oversized cores still open :83-86 — partial (C2Cherrypick #5) | partial discharge |
| 15 | SCORECARD.md:12 | "calibration is the lowest axis" ([INFERENCE], 2026-10-15) | all three axes tie at 10 — self-tagged inference contradicting the record (C2Cherrypick #1) | historical inference |
| 16 | SCORECARD.md:14 | "Numeric axis fields satisfy fleet `AXES.md:33-39`" | AXES.md:33-39 = admission/lowest-axis rule; the 0–10 rule is at :79 (sha256 04ea5c9e, unchanged). NOTE: check leaves the lane tree (fleet file) | wrong-section pointer; out-of-tree |

## Holding statements (all verified at BASE or their own pin)

Categories follow the draft's (a)–(f). JSON has the full row set; condensed here.

- **(a) Capabilities pointers** — all 13 `## Capabilities` rows (:619-631) + the
  two round-42 appended rows (:3484-3485): every named file/dir resolves at BASE.
  Value-bearing spot checks reproduce: r40 c2 score 26/26 exit 0; r41 c1 4/4 exit 0
  with `frozen_path_changed []`; r42 c1 4/4 exit 0, `counter_sha256 0f5052f9` ==
  `sha256(tools/round-42/c1-counter.py)`; r43 c1 78/78 exit 0; r43 gen selftest
  receipts "tuple-check selftest: 17/17 passed exit=0". Line-pins inside pointer
  cells (e.g. `SKILL.md:316-343`) resolve at their own-era revisions only
  (baseline-citation rule, SCORECARD:17).
- **(b) Owned axes** — every pinned count reproduces (command-A table above);
  calibration 9/9 + `measured_revision c265db9b` in result.json; baseline rev
  `66455858` cited. The two headline cells are flagged (#1/#2) only as
  leading-value staleness — all sub-pins true.
- **(c) SHONEN** — :6 v4 table shape (marker :525, 13 cols, 15 rules), R42-C2
  stop (exit 1, 78/78, `observed_features_match_declared` false), craft
  `SKILL.md:81-449`+20/20 at e1c83313, R41-C2 exit 1 52/52, 19/19 at 4d62ee5a;
  :7 command A 21/21 at base (region-hash `92540586` NOT re-derived — recipe
  lives in round-43 instrumentation, rubric must enumerate it or skip); R43-C1
  78/78 exit 0; R43-C2 exit 1. :9 r42 4/4 + four carrier dirs + LOG:3174; r41
  4/4 + `R41W2Repro{L,V3,V4}.md`; r40 dir present (3/4 consistent with `[~]`).
  :10 r43 78/78 + LOG entry. :12 r40 26/26 exit 0 + IndepEval.md; r39 tools +
  20/20 score (selftest counts are re-runnable arms, not re-run here). :15
  PROVINCE :97-125 Adjacent range — safety refusal at :116-118, byte-identical
  52b0eb29→BASE (`f1a5cfc6`); r39 additions at :378-384, r40 at :386-394, r38
  note :376 — all exact. :16 flagged (#3). :18 numstat `4 0` reproduces.
- **(d) planned rows** — holding: :275→luna-3, :3092→r27, :3131 superseded-by-:3138,
  :3138→r28, :3306/:3322/:3374/:3434/:3452 (markers or true match),
  :3414→r39 exact, :3507→r44 draft consistent. Flagged: #4-#10 above.
- **(e) verdict vs receipt exit** — consistent for every cited receipt: R36-C1/C2
  (4, met true; 0 mismatches), R38-C1 v1 3/false + v3-NOT-THE-RULE 4/false +
  efd5c47a control, R39-C1 6/true + ctl 0 + base unevaluable, R39-C2 20/20,
  R40-C1 3/4 exit 1 + c1-extra met, R40-C2 26/26 exit 0 + freeze ctl exit 2,
  R41-C1 4/4 exit 0 + both ctls exit 1, R41-C2 52/52 exit 1, R42-C1 4 exit 0,
  R42-C2 78/78 exit 1, R43-C1 78/78 exit 0, R43-C2 exit 1×2 + numstat 4/0,
  R30-C1/C2 + R31-C1/C2 txt tails exit=0, R34-C1/C2 stop receipts, R35-C1/C2
  pass:false. **Receipt-schema warning for the counter: r36–r39 receipts carry
  no `exit_code` field (r38 ctl uses `exit`); r40+ use `exit_code`.** The
  claim-table "exit 0/1" text for r36–r39 is asserted but not machine-stored.
- **(f) coverage map** — command A at base: mapped 137 == knowledge_files 137,
  `missing []`, `dangling []` — clean. Rubric-boundary notes: literal `|` row
  count is 88 data rows (sectioned layout) — a naive row-count check would
  misfire; the `## Knowledge` index holds 115 rows < 137 files but asserts no
  completeness claim (boundary decision, not a mismatch); R29 provenance
  correction line present (README:290 ↔ SCORECARD:3240).
- **SHONEN structure** — four `[~]` boxes, zero `[x]` — consistent with
  un-promoted state.

## What a rubric author must decide (scope notes)

1. Headline-vs-pin semantics (#1, #2): every sub-pinned count is true; the
   leading figure trails the tip by two landings. If the rubric scores "leading
   headline == command A at REV" these are mismatches; if it scores
   "each pinned sub-claim at its rev" they all pass. Same shape as #11.
2. Marker-free discharge class (#4, #6, #7, #13, #14): the work was done or the
   departure is recorded in the very next section, but the statement row lacks
   `(after a steer)`/`superseded`/`closed by`. Draft rule (d) as written flags them.
3. Numbering anomalies (#8 missing `## Round 37`; #10 misplaced planned row;
   #9 v3-bytes sub-clause; #5 instrument-order clause, already self-disclosed).
4. Frozen-text contradictions repaired by appended lines (#3, plus the
   SCORECARD:3487 'overstrict' heading superseded by :3503/:3509 — listed inside
   row #3's note; under the C2 landing mechanics an appended correction counts
   as repaired iff the rubric check reads it).
5. Historical-section scope (#12-#16): round-1/Open-gaps statements phrased as
   present tense; C2Cherrypick already flagged 8 of the same class in round 26.
   #16 also leaves the lane tree — exclude or scope `AXES.md` explicitly.
6. Value checks that are re-runnable arms, not re-derived here: r39 selftest
   35/35+27/27 (two `--selftest` invocations in a scratch clone), the
   `92540586` region hash (recipe must be pulled from round-43 instrumentation).

## Receipts (seat self-check)

| command | exit | stdout sha256 | wall |
|---|---|---|---|
| `git diff c29360e3 HEAD --stat` | 0 | only plans/round-44-claims.md added | <1s |
| command A × 10 revs (`cmdA.log`) | 0 | `42b5080914e0674e2c8a1d58488a78c65bd6d6bce49be33b5324067fe96cc890` | ~2s |
| receipt-exit sweep (24 score/control JSONs) | 0 | shown inline above | <1s |
| pointer existence sweep (~120 paths) | 0 | all present except none missing | <2s |
| census generator → this table + R44ScoutCalib.json | 0 | `23f818325cbb472fd7816d1d8dec9445e51f50aeb697649e833b316db2ef436d` (census-out.json incl. notes) | <1s |

Tool installs: none. No writes outside `.ufo/waves/round-44/w1/` and scratch
`/fast/scratch/hyaku/kaidoku-r44/probe-R44ScoutCalib/`.
