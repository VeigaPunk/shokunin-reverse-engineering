# R44W2Axes — independent axis verdicts for round 44, wave 2

Seat `R44W2Axes` (critic). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `c29360e3ba5381a5ab69e372d0d9577970f85018`; freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`; measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; lane tip at dispatch
`c86ea508188c50e2645b1f9bba65df4177cda6b1` (observed tip
`8bb1090af3fef64477c4337855e4347472db2701`).

Method: read-only `git show`/`git log`/`git rev-parse` over committed objects, one
`git clone --shared` per the seat rule, counters run with `--work` under
`/fast/scratch/hyaku/kaidoku-r44/R44W2Axes/`. I changed no claim, counter, rubric,
frozen byte or production doc. Every number below is reproduced from this seat's own
run; the 55bcce69 values are also in the committed L1 receipts
`.ufo/waves/round-44/l1/{c1,c2}-score-at-55bcce69.json`. The L1 `*-score-at-tip.json`
receipts are at `c86ea508`; the observed tip `8bb1090a` shows C2 with 9 frozen paths,
not 8 (D-AXES-3).

## Axes named

1. **coverage** — the command-A map proxy (knowledge files mapped / total, plus the
   `## Coverage map` integrity) and the number of Frontier→Core promotions.
2. **depth** — queue-drain rule blocks with resolvable file/range citations and the
   `## Queue-drain craft` section range.
3. **calibration** — the frozen 80-entry C2 rubric's mismatch count over the lane's
   own self-assessment statements.

## Verdicts (one per axis)

| axis | verdict | command | observed |
|---|---|---|---|
| coverage | **unchanged** | command A at base, freeze, 55bcce69, tip (`artifacts/R44W2Axes/command-a.py`) | `137/137` at base and freeze; `138/138` at 55bcce69 and tip; `missing []`, `dangling []`; `coverage_score 10.0` both sides. One knowledge file and one map row were added; **no Core row** was promoted (the C1 landing says "measured, not promoted"). The proxy count moves 137→138, the score does not move. |
| depth | **unchanged** | same command A | `rule_blocks 21`, `citation_resolved_rules 21`, `depth_score 10.0` at all four revisions; craft section content span `SKILL.md:81-543` (heading span `81-546`) identical at all four. The C2 correction changes the *statement* from 20/20 to 21/21, not the rule set. |
| calibration | **improved** | C2 counter at base (`--pre-freeze --rubric <freeze-tree rubric>`) and at 55bcce69 | base: exit 1, `entries_evaluated 80`, `mismatches_count 3` = `C2-a1-owned-coverage-count`, `C2-a2-owned-depth-count`, `C2-a4-owned-depth-craft-range`; 55bcce69: exit 0, `entries_evaluated 80`, `mismatches []`, `unevaluable_count 0`, `frozen_path_changed []`, `met_target true`. |

No axis is **harmed**. The C1 honest stop only demotes a claim (it cannot overstate);
the M44-2 freeze defect makes the *lane tip* unscorable, not the measured axis, and
the round says so (see below).

---

## Coverage (command A)

```
python3 artifacts/R44W2Axes/command-a.py <base> <freeze> <55bcce69> <tip>
```

Output (verbatim, `artifacts/R44W2Axes/command-a.stdout`):

```json
{"citation_resolved_rules": 21, "coverage_score": 10.0, "craft_span_content": "81-543", "craft_span_heading": "81-546", "dangling": [], "depth_score": 10.0, "knowledge_files": 137, "mapped": 137, "missing": [], "revision": "c29360e3ba5381a5ab69e372d0d9577970f85018", "rule_blocks": 21}
{"citation_resolved_rules": 21, "coverage_score": 10.0, "craft_span_content": "81-543", "craft_span_heading": "81-546", "dangling": [], "depth_score": 10.0, "knowledge_files": 137, "mapped": 137, "missing": [], "revision": "c48f8a4bfd449300c975668e59aae5b5538b6a84", "rule_blocks": 21}
{"citation_resolved_rules": 21, "coverage_score": 10.0, "craft_span_content": "81-543", "craft_span_heading": "81-546", "dangling": [], "depth_score": 10.0, "knowledge_files": 138, "mapped": 138, "missing": [], "revision": "55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac", "rule_blocks": 21}
{"citation_resolved_rules": 21, "coverage_score": 10.0, "craft_span_content": "81-543", "craft_span_heading": "81-546", "dangling": [], "depth_score": 10.0, "knowledge_files": 138, "mapped": 138, "missing": [], "revision": "8bb1090af3fef64477c4337855e4347472db2701", "rule_blocks": 21}
```

The C1 entry `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` and its
`corpus/README.md:104` map row are the 137→138 delta. The PROVINCE surface is
`## Round-44 measured, not promoted (R44-C1 honest stop)` (`PROVINCE.md:424`), not
`## Round-44 additions to Core`; the counter's `province_core_row` is false. No
Frontier→Core count moved. **Coverage: unchanged.**

## Depth (command A)

`rule_blocks 21`, `citation_resolved_rules 21`, `depth_score 10.0` at base, freeze,
55bcce69 and tip. The craft content span is `SKILL.md:81-543` at every revision (the
`81-546` heading span only counts the three trailing blank lines before the next
`##`). The C2 corrections at `SCORECARD.md:3513-3517` append the re-derived values
`137/137`, `21/21`, `81-543`; they do not add or remove a rule. **Depth: unchanged.**

## Calibration (frozen 80-entry rubric)

At the measured revision, the frozen counter returns:

```
python3 -I -B tools/round-44/c2-counter.py --root <clone> \
  --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
  --work <scratch>/w/c2-55 --json-out .../c2-55.json
```

exit 0; `entries_evaluated 80`, `mismatches []`, `mismatches_count 0`,
`unevaluable_count 0`, `frozen_path_changed []`, `met_target true`
(`artifacts/R44W2Axes/c2-55.json`; stdout sha256
`dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3`).

The base census with the shipped rubric (extracted from the freeze tree) returns
exit 1, `entries_evaluated 80`, exactly the three target ids, `unevaluable_count 0`
(`artifacts/R44W2Axes/c2-base-rubric.json`). So the **3 → 0** is reproduced and is
exact.

At the observed tip `8bb1090a`, C2 exits 2 with 9 `frozen_path_changed` (the 8
control-fixtures + `SCORECARD.md`, the record commit's own `## Round 44` section). A
2 never counts toward a target, and the committed record's undercount of that ninth
path is D-AXES-3; the calibration score itself is the 55bcce69 run.

### Vacuity, free-pass and note-vs-value attacks

- **Vacuity.** 80 rubric entries, 80 observed, 0 errors, 0 unevaluable; the 80 are
  the six declared scope categories (a)–(f) over SCORECARD 55, SHONEN 22, README 3.
  The receipt's `entries` vector carries a check output for every id. Not vacuous.
- **Free pass.** The frozen rubric's own fitness gate ran one mutation per entry:
  the committed wave-1 summary (`w1/artifacts/R44C2Controls/receipts/fitness-full/summary.json`)
  reports `entries_scored 80`, `entries_failing_to_fail []`, `ok true`. The six
  `expected: superseded` rows are content checks against the next-round declaration,
  not automatic passes.
- **Note vs value.** The three repairs are `c2-correction-value:` lines
  (`SCORECARD.md:3513,3515,3517`), and each check re-derives the value at REV: a1
  observes `137/137` (command A over the freeze tree), a2 `21/21`, a4 `81-543`. A
  wrong value is not a pass: the wave-1 CTL-C2-4 (wrong-value note) exits 2, and
  CTL-C2-1 (seeded non-frozen LOG edit) exits 1 with `newly_mismatching_ids
  ["C2-d17-sharpen-log-round43-entry"]` and the three baseline ids unchanged.

### Bounded proxy

This is a calibration proxy over frozen self-assessment statements only (claims
D-15): it does not cover the lesson/LOG, and check-pass is not truth (D-16). The
`137/137` correction is the freeze-tree value; at 55bcce69 command A counts `138/138`
because C1 added one entry. The claim explicitly binds the freeze-tree count, and the
README checks tolerate exactly C1's one row, so the proxy is internally consistent —
but a reader comparing SCORECARD's `137/137` to command A at 55bcce69 will see a
one-file difference. **Calibration: improved (bounded proxy).**

---

## R44-C1 honest stop — confirmed, and it is the only contract-faithful reading

### The verdict at the measured revision

```
python3 -I -B tools/round-44/c1-counter.py --root <clone> \
  --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
  --pkg65 <rea-agents 6.5.0> --work <scratch>/w/c1-55 --json-out .../c1-55.json
```

exit 1; `carriers_matched 4`, `met_target false`, `frozen_path_changed []`,
`bindings_false ["province_core_section","province_core_row","frontier_note"]`,
`failing []`. Every one of the four carrier records has an empty false-binding list
and `oracle_hits_ok true`, `oracle_ok true`, `tree_ok true`, `gaps_ok true`,
`projection_ok true`; v1be, e.g., `oracle_files 3`, `oracle_hits 3`. So the four REA
receipts publish every oracle file and the measurement is complete; the red is the
three withdrawn **documentation** bindings, not a carrier failure.

### The strongest counterexample: the counter met at `4cc1ac11`

```
python3 -I -B tools/round-44/c1-counter.py --root <clone> \
  --rev 4cc1ac11657590c25b6565d6ab220f53372a94d3 ... 
```

exit 0; `carriers_matched 4`, `met_target true`, `frozen_path_changed []`, every
binding true (`artifacts/R44W2Axes/c1-4cc1.json`; the committed
`corpus/evidence/round-44/c1/counter-at-4cc1.json` says the same). At that revision
the docs claimed a Core row, so the counter returned met. The L1 then withdrew the
Core row at `55bcce69` and the counter went red. **This does not make the stop
optional:** the frozen claim text is authoritative, and it adds a clause the counter
does not implement — the controls amendment (`plans/round-44-claims.md:34-36`)
requires the receipt's `parameters.output_directory` to name a
`corpus/evidence/round-44/c1/` path, while the predicate
(`plans/round-44-claims.md:137-139`) requires the `/kaidoku-r44/` scratch segment.
The four receipts carry the scratch form
(`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/.../rea-out`). The counter's
`provenance_ok()` (`tools/round-44/c1-counter.py:1176-1182`) checks only the
`/kaidoku-r44/` substring, so it cannot enforce the controls clause. A met claim
would therefore overstate relative to the frozen text. The substring-shaped path that
contains both segments is a loophole (the committed lesson's R44-CL2 calls the field
"internally unsatisfiable" but does not spell out that the counter enforces only the
scratch substring; an uncommitted worktree edit adds that qualifier — see below), not
a legitimate route: it would put the run inside the committed evidence tree,
against the stated data procedure ("REA's output directory is in the private
`/kaidoku-r44/` scratch segment ... the runner copies the produced tree verbatim into
`corpus/evidence/round-44/c1/<id>/`").

### The record says exactly that — with one committed gap

- `PROVINCE.md:424` — `## Round-44 measured, not promoted (R44-C1 honest stop)`, and
  the row says "The counter matched 4/4 and published every oracle file, but ... the
  claim required the committed evidence path, while the counter accepts only the
  `/kaidoku-r44/` scratch provenance. The score therefore does not satisfy the frozen
  predicate; no Core promotion is claimed."
- `corpus/README.md:104` and `:224` — the map/knowledge rows say "Measured, not
  promoted", the output-directory mismatch, "the score is not admitted and v1/v2
  remain Frontier".
- `corpus/lessons/round-44.md:57-63` (committed at `8bb1090a`) — "The frozen R44-C1
  text is internally unsatisfiable on one field ... The honest stop is correct; the
  next freeze must test each claim conjunct against the values its own instrument can
  actually compute (a satisfiability preflight) instead of freezing prose." It states
  the verdict and the two-clause conflict, but it does **not** say the counter
  enforces only the scratch clause or that its red at `55bcce69` is the three
  withdrawn documentation bindings. An **uncommitted** worktree edit
  (`git diff -- corpus/lessons/round-44.md`, which also adds M44-3) inserts that
  qualifier; the committed tip does not carry it. The worktree is another seat's/L1's
  live edit, not mine; the committed bytes are what this seat scores.
- The entry `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` (at 55bcce69)
  opens with the honest-stop status and the `4cc1ac11` exit-0 receipt, then says the
  run does not satisfy the frozen predicate.

The verdict and reason are therefore exact in PROVINCE/README/the entry, and correct
in the committed lesson's conclusion, but the lesson's causal sentence is imprecise
("internally unsatisfiable" vs "the counter enforces only the scratch clause"): see
D-AXES-4.

### Does the stop harm an axis?

No. It demotes: the measured state at 55bcce69 has the same coverage/depth
**scores** as the base (coverage 137→138 files but no Core row; depth 21/21), and the
calibration proxy is improved. The only cost is the unclaimed promotion, which is
not a regression on any axis. The stop cannot overstate, which is the point.

---

## R44-C2 — confirmed, non-vacuous, bounded

At 55bcce69 the counter is green (80/80, 0 mismatches, 0 unevaluable, exit 0); at
base it is red with exactly the three target ids (3 mismatches, 80/80, exit 1). The
negative controls are committed and behave: CTL-C2-1 exit 1 with the seeded id,
CTL-C2-2 exit 2 (`rubric_malformed`), CTL-C2-3 exit 2 (`frozen_path_changed` on the
rubric), CTL-C2-4 exit 2 (wrong-value note). The fitness gate reds all 80 entries
one mutation each. The note-vs-value rule holds because the checks re-derive the
appended values. Bounded as stated (D-15/D-16).

---

## M44-2 / freeze defect — the claim measurement is honest and sufficient; the record commit adds an undisclosed ninth C2 path

- `c86ea508` touched 8 files under the frozen directory pathspec `tools/round-44/`
  (all `tools/round-44/control-fixtures/c3|pos/...`; statuses `M`). Both counters at
  that revision exit 2 `frozen_path_changed` (8 paths). A later restore does not
  un-block.
- **The record commit `8bb1090a` adds a ninth C2 path.** At the observed tip, C1
  exits 2 with 8 paths, but C2 exits 2 with **9**: the 8 control-fixtures plus
  `SCORECARD.md`. The ninth is the record commit's own `## Round 44 ...` section at
  `SCORECARD.md:3519`, beyond the C2 rubric's bound `expected_edits["SCORECARD.md"]`
  (7 append lines; the rubric's own note says the landing section "cannot ALSO be
  appended ... the L1 must either land it elsewhere or re-freeze with it bound").
  Reproduced: `artifacts/R44W2Axes/c2-observed-tip.json` (exit 2, 9 paths, last
  `SCORECARD.md`), `c1-observed-tip.json` (exit 2, 8 paths). The L1's
  `c2-score-at-tip.json` was run at `c86ea508`, not at the observed tip, so it
  understates the tip's C2 path set (8 vs 9) and does not name the record commit as
  the ninth; the committed lesson's M44-2 attributes the tip loss to `c86ea508`
  alone. An **uncommitted** worktree edit adds M44-3 and restores `SCORECARD.md` to
  the 55bcce69 blob (ledger moved to `LOG.md`); the committed tip does not carry that
  fix. See D-AXES-3.
- **Honest and sufficient for the claim:** `55bcce69` is clean — preflight exit 0
  `clean`, C1/C2 `frozen_path_changed []` — so the measured C1/C2 scores are
  admissible. The claim surfaces (SCORECARD corrections at `9d3d1862`, the C1 docs at
  55) are at 55bcce69. The round does not claim the tip. The tip's *description* is
  incomplete (the ninth path), but the measured claim is unaffected.
- **The preflight really catches it:** at `c86ea508` exit 1 with `touched` = the 8
  `M` paths and `blob_changed` = the same 8; at `55bcce69` exit 0 `clean`. Fixture
  red/green (toplevel asserted before each commit): clean rev exit 0; a modified
  frozen file exit 1 (`touched 1 M`, `blob_changed 1`); a **new file added** under
  the frozen directory exit 1 (`touched 1 A`). The added-file case is the one the
  round-43 walk would miss; this tool catches it.
- **Caveats.** It is a pre-commit *check*, not a gate that prevents the commit (the
  lesson says to wire it into the commit sequence). It is only precise with
  `--pathspec`: with no pathspec it logs every change in `FREEZE..REV` and reports
  `frozen_path_changed` (over-broad, fails closed), so a caller must pass the claim's
  frozen pathspec(s) — the L1 receipts do.
- **Does it harm calibration?** The measured observable at `55bcce69` is 0
  mismatches, so the claim's calibration is improved at the admissible revision; the
  tip's exit 2 (C1 8 / C2 9) is a freeze-integrity failure, not a self-assessment
  mismatch. The tip is **unprovable**, and the committed record undercounts its C2
  path set (8 vs 9) while the uncommitted worktree edit discloses and fixes it. That
  is a record-disclosure defect (D-AXES-3), not a change to the 80-entry mismatch
  count. Residual: the disclosure lives in prose, not a scored rubric entry (D-15).

---

## Numbered defects for the L1

### D-AXES-1 — the frozen C2 counter's documented `--pre-freeze` base census cannot run with its default rubric

- Path/line: `tools/round-44/c2-counter.py:1186-1193` (the rubric `FREEZE -> REV`
  byte-compare returns `EXIT_CANT` unconditionally) versus
  `tools/round-44/c2-counter.py:1199` (the `pre_freeze` exemption, which is never
  reached for the rubric path).
- Command: `python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev
  c29360e3ba5381a5ab69e372d0d9577970f85018 --freeze
  c48f8a4bfd449300c975668e59aae5b5538b6a84 --work <SCRATCH> --pre-freeze
  --json-out <OUT>` (the claim's CTL-C2-0 invocation; no `--rubric`).
- Exit code: **2**. Observed: `entries_evaluated 0`, `unevaluable_count 1`,
  `frozen_path_changed ["tools/round-44/c2-rubric.json"]` — not the claimed
  `exit 1, mismatches 3`. The counter's docstring
  (`tools/round-44/c2-counter.py:39-42`) promises the base census without saying
  `--rubric` is mandatory.
- Reproduced correctly with an explicit freeze-tree rubric: exit 1, 80/80,
  `mismatches_count 3` (a1/a2/a4), `unevaluable_count 0`
  (`artifacts/R44W2Axes/c2-base-rubric.json`). The wave-1 receipt
  `w1/artifacts/R44C2Counter/receipts/shipped-rubric-census.json` used the same
  explicit `--rubric`.
- Smallest safe correction: when `pre_freeze` is set, read the rubric from `FREEZE`
  and skip the rubric-at-REV byte compare (or make `--rubric` required for the base
  census and state it in the claim/control text). This is a control-reproducibility
  defect, not a change to the 55bcce69 score (which is unaffected and reproduced).

### D-AXES-2 — the C1 score receipt does not record `counter_sha256_at_freeze`, contrary to the frozen receipt contract

- Path/line: contract at `plans/round-44-claims.md:85-87` ("Every score receipt
  records ... `counter_sha256_at_freeze` ..."); the C1 counter emits no such field
  (top-level receipt keys at
  `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`; same schema in
  `artifacts/R44W2Axes/c1-55.json`).
- Command: the C1 counter at 55bcce69 above; exit 1.
- Observed: the receipt carries `counter_sha256
  9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993` but no
  `counter_sha256_at_freeze`. The value is derivable and identical: the counter blob
  is the same at freeze and REV (`git rev-parse` both
  `9695d586b3b1a792f1ad15e8dc4b4f54b8fe1569`; sha256 of the bytes
  `9f2cc140...`). The C2 score receipt does carry the field
  (`085192ea...`), so the gap is C1-specific.
- Smallest safe correction: add a sidecar/annotation beside the C1 score receipt
  (`counter_sha256_at_freeze: 9f2cc140...`, plus the same for any cited post-freeze
  control receipt), not an edit to the frozen counter; require the field in the
  round-45 C1 counter. The absence does not change the C1 verdict, but the frozen
  receipt contract is unmet as written.

### D-AXES-3 — the record commit `8bb1090a` is itself a C2 frozen-path violation, and the committed lesson undercounts the tip's C2 path set

- Path/line: `SCORECARD.md:3519` (the committed tip's `## Round 44 — ...` section)
  versus `tools/round-44/c2-rubric.json` `expected_edits["SCORECARD.md"]` (7 append
  lines; the rubric's own note says the landing section "cannot ALSO be appended ...
  the L1 must either land it elsewhere or re-freeze with it bound").
- Command: `python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev
  8bb1090af3fef64477c4337855e4347472db2701 --freeze
  c48f8a4bfd449300c975668e59aae5b5538b6a84 --work <SCRATCH> --json-out <OUT>`.
- Exit code: **2**. Observed: `frozen_path_changed` **9** paths = the 8
  `tools/round-44/control-fixtures/...` paths + `SCORECARD.md`; the C1 counter at the
  same revision is 8. The committed lesson's M44-2 says both counters exit 2 at the
  tip but attributes the loss to `c86ea508`'s 8 files; the L1's
  `c2-score-at-tip.json` was run at `c86ea508` (8), not at the observed tip (9), so
  the tip's C2 path set is understated in the committed record.
- Smallest safe correction: commit the worktree's M44-3 fix — restore `SCORECARD.md`
  to the `55bcce69` blob and move the round-44 ledger to `LOG.md` — then re-run the C2
  counter at the new tip and record the path set; or (not preferred; the claim is
  frozen) re-freeze with the section bound. The worktree currently holds this fix
  uncommitted; the committed tip does not.

### D-AXES-4 — the committed lesson's R44-CL2 causal sentence is imprecise; the precise qualifier is only in the uncommitted worktree edit

- Path/line: `corpus/lessons/round-44.md:57-63` (committed at `8bb1090a`) — "The
  frozen R44-C1 text is internally unsatisfiable on one field ...". The counter's
  `provenance_ok()` (`tools/round-44/c1-counter.py:1176-1182`) checks only the
  `/kaidoku-r44/` substring; a path containing **both** `/kaidoku-r44/` and
  `corpus/evidence/round-44/c1/` satisfies both literal clauses, so "internally
  unsatisfiable" is a semantic, not a literal, statement. The committed lesson does
  not say the red at 55bcce69 is the three withdrawn documentation bindings; the
  uncommitted worktree edit adds that qualifier.
- Command: `git show 8bb1090a:corpus/lessons/round-44.md | sed -n '57,63p'`; the C1
  counter at 55 (exit 1, `bindings_false` = the three doc bindings).
- Observed: the committed lesson lacks the qualifier; `git diff --
  corpus/lessons/round-44.md` shows an uncommitted edit that inserts it (and M44-3).
- Smallest safe correction: commit the qualifier (the worktree text) with the M44-3
  fix; no claim, counter, rubric or frozen byte changes.

Both D-AXES-3 and D-AXES-4 are record defects, not measurement defects: the C1/C2
scores at `55bcce69` are unaffected.

---

## Receipts

Full argv, exit codes, stdout sha256 and wall times are in
`artifacts/R44W2Axes/receipts.json` (17 runs). Summary:

| run | exit | stdout sha256 (first 16) | wall (s) |
|---|---|---|---|
| command A (base, freeze, 55, tip) | 0 | `121250e0f52364f8` | 0.291 |
| C1 at 55bcce69 | 1 | `eea45d374bb450f1` | 7.010 |
| C1 at 4cc1ac11 (counterfactual) | 0 | `8742a90d9b879fbf` | 6.809 |
| C1 at c86ea508 (tip at dispatch) | 2 | `0e1c1f556d375f02` | 0.077 |
| C2 at 55bcce69 | 0 | `dd7c529bb6340c36` | 4.708 |
| C2 at c86ea508 (tip at dispatch) | 2 | `b789895baa6f59c0` | 0.094 |
| C2 base, default rubric (`--pre-freeze`) | 2 | `aff2e95504a9ce60` | 0.051 |
| C2 base, freeze-tree rubric | 1 | `1ac9e9225ee8b975` | 4.487 |
| preflight at 55bcce69 (`--pathspec tools/round-44`) | 0 | `c8a03c2673a9bfd5` | 0.094 |
| preflight at c86ea508 (`--pathspec tools/round-44`) | 1 | `20a87d4d81eedaa7` | 0.089 |
| C2 at observed tip 8bb1090a | 2 | `0a81b8b2e85b0891` | 0.109 |
| C1 at observed tip 8bb1090a | 2 | `0e1c1f556d375f02` | 0.099 |
| preflight at observed tip 8bb1090a | 1 | `c302813c8069f581` | 0.119 |
| fixture clean | 0 | `a56edf3ba3a77c1f` | 0.032 |
| fixture modify frozen file | 1 | `aec657bc433fb7c5` | 0.034 |
| fixture add file under frozen dir (`--pathspec`) | 1 | `faf2f8dfdcfa67bd` | 0.034 |
| fixture add, no `--pathspec` | 1 | `66fe5bd7b3927ba6` | 0.031 |

Artifacts: `artifacts/R44W2Axes/{command-a.py,command-a.stdout,c1-55.json,
c1-55.stdout,c1-4cc1.json,c1-4cc1.stdout,c1-tip.json,c1-tip.stdout,c2-55.json,
c2-55.stdout,c2-tip.json,c2-tip.stdout,c2-base-default.json,c2-base-default.stdout,
c2-base-rubric.json,c2-base-rubric.stdout,c2-observed-tip.json,c2-observed-tip.stdout,
c1-observed-tip.json,c1-observed-tip.stdout,pf-55.stdout,pf-c86.stdout,
pf-observed-tip.stdout,pf-fix-clean.stdout,pf-fix-mod.stdout,pf-fix-add-spec.stdout,
pf-fix-add-nospec.stdout,receipts.json}`.

## Scratch

All clones, counter `--work` dirs and fixtures were under
`/fast/scratch/hyaku/kaidoku-r44/R44W2Axes/`; the tree was removed before this
result was written. No lane or fleet file outside
`.ufo/waves/round-44/w2/R44W2Axes.md` and
`.ufo/waves/round-44/w2/artifacts/R44W2Axes/` was written. No mutating git command
was run in the lane, the fleet repo or any sibling lane; fixture commits were made
only inside `mktemp -d` repos with their toplevel asserted.
