# R44W2C2Corrections — the three C2 landing corrections re-derived, and the `## Owned axes` statements the frozen rubric never names

Seat `R44W2C2Corrections` (reviewer). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`; measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; tip at dispatch `c86ea508188c50e2645b1f9bba65df4177cda6b1`;
record commit under review `8bb1090af3fef64477c4337855e4347472db2701`; lane tip at the end of the
review `923fa87072cc1a728efd88f7038ecb2b8f8af8ff` — the L1's record correction landed at 11:32Z
while I was reviewing, so every finding below is measured against the revision it names, and C-1 is
re-verified against the corrected tip.

Method: read-only git only (`show`, `ls-tree`, `diff`, `log`, `rev-parse`). No clone was needed —
every byte I cite is a committed blob, read by revision. Counter runs used
`--work /fast/scratch/hyaku/kaidoku-r44/R44W2C2Corrections/work`; scratch
`/fast/scratch/hyaku/kaidoku-r44/R44W2C2Corrections/` was created and deleted inside this run
(`trap`-equivalent cleanup after the receipts were written). No mutating git/jj call; no fixture
repo; no tool install (nothing was missing; pacman untouched). Nothing outside
`.ufo/waves/round-44/w2/R44W2C2Corrections.md` and `.ufo/waves/round-44/w2/artifacts/R44W2C2Corrections/`
was written.

---

## 1. The three landed corrections: **a2 and a4 confirmed, a1 confirmed only at its declared anchor**

| marker | land lines (`55bcce69`) | value | declared anchor | re-derived at the anchor | re-derived at `55bcce69` | verdict |
|---|---|---|---|---|---|---|
| `C2-a1-owned-coverage-count` | `SCORECARD.md:3512-3513` (same at `923fa870`) | `137/137` | round-44 freeze tree (`c48f8a4b`) | **137/137** (`knowledge_files 137`, `mapped 137`, `missing []`, `dangling []`) | **138/138** (`knowledge_files 138`, `mapped 138`) | value true at its declared anchor; **stale at the measured revision** → C-3 |
| `C2-a2-owned-depth-count` | `SCORECARD.md:3514-3515` | `21/21` | round-44 freeze tree | **21/21** (`rule_blocks 21`, `citation_resolved_rules 21`) | **21/21** | confirmed |
| `C2-a4-owned-depth-craft-range` | `SCORECARD.md:3516-3517` | `81-543` | round-44 freeze tree | **81-543** (heading `## Queue-drain craft` at line 81, last non-blank line 543, next `## ` at 547) | **81-543** | confirmed |

Derivation is the lane's command A (`SCORECARD.md:86-124`, copied verbatim into
`artifacts/…/commandA.py`), run at `c48f8a4b`, `55bcce69` and `8bb1090a` as well as at every pin
quoted in the two cells (see §3). The a4 range is the recipe's own section rule — heading line to
last non-blank line before the next `## ` — not a hand-picked end.

The landing mechanics are clean at the measured revision:

- `git diff c48f8a4b 55bcce69 -- SCORECARD.md` → **8 insertions, 0 deletions**; the 7 non-blank
  inserted lines are byte-identical to `expected_edits["SCORECARD.md"].append` in
  `tools/round-44/c2-rubric.json:182-196` (blank separator ignored by the counter's
  `verify_expected_edit`, `c2-counter.py:538-593`);
- both `preserve` digests are present at REV: `81e06b81…` = sha256 of `SCORECARD.md:23`,
  `b99cc56d…` = sha256 of `SCORECARD.md:24`, so no cited row was rewritten (artifact
  `scorecard-declared-append.diff`, `b2-gate-evidence.txt`).

## 2. Independent rescores of the frozen instrument

All six runs use `tools/round-44/c2-counter.py` exactly as frozen (counter sha256
`085192ea…36c277` = `counter_sha256_at_freeze`; rubric sha256 `e8cc0ded…e755e`).

| run | exit | observed | receipt |
|---|---|---|---|
| `--rev 55bcce69 --freeze c48f8a4b` | **0** | `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, `met_target true`, `claim_score true` | `artifacts/…/c2-score-55bcce69.json` (stdout sha256 `dd7c529b…`) |
| `--rev c29360e3 --freeze c48f8a4b --pre-freeze` **without** `--rubric` (the claim's command shape, `plans/round-44-claims.md:249`) | **2** | `entries_evaluated 0`, `mismatches []`, unevaluable `frozen_path_changed` = `[tools/round-44/c2-rubric.json]` (`freeze_notes: rubric_changed`) | `c2-pre-freeze-base-norubric.json` (`aff2e955…`) |
| same `--pre-freeze` **with** `--rubric <lane>/tools/round-44/c2-rubric.json` | **1** | `entries_evaluated 80`, `mismatches` = exactly `["C2-a1-own...","C2-a2-own...","C2-a4-own..."]`, `unevaluable 0` | `c2-pre-freeze-base-rubric.json` (`1ac9e922…`) |
| `--rev 8bb1090a --freeze c48f8a4b` (record commit) | **2** | `frozen_path_changed` = **9** paths: the 8 `tools/round-44/control-fixtures/**` files **plus `SCORECARD.md`** (`state: bound_edit_violation`, `reason: appended_block_differs_from_expected_edit`) | `c2-score-tip.json` (`0a81b8b2…`) |
| `--rev 923fa870 --freeze c48f8a4b` (corrected tip) | **2** | `frozen_path_changed` = **8** paths (M44-2 only); `SCORECARD.md` now `state: bound_edit_applied`, `reason: bound_edit`, `appended_lines 8` | `c2-score-tip-923fa870.json` (`83705252…`) |
| `--selftest` | **0** | `{"ok": true, "selftest": "P44-C2"}` | `c2-selftest.txt` (`a5e942a1…`) |

The base census is therefore non-vacuous: the frozen rubric, at the base, on the shipped counter,
mismatches **only** the three claimed targets. The round's landing turned exactly those three reds
into greens. That part of R44-C2 stands.

## 3. The `## Owned axes` census at `55bcce69` (`SCORECARD.md:21-26`)

Full catalog: `artifacts/…/owned-axes-assertion-census.tsv` (31 rows: 12 coverage values, 14 depth
values, 3 calibration statements, and the 2 `Last-change` lists).

- **Every pinned numeric/range assertion reproduces at its pin.** Command A at each pin:
  `133/133@e1c83313`, `130/130@4d62ee5a`, `128/128@52b0eb29`, `126/126@0fc61133` (round 38),
  `124/124@ffc81341` (round 36), `122/122@cab59f22`, `116/116@c369242f`, `109/109@ebe2cb4a`,
  `78/78@3395b6d`, `107/107@7ef837a4`, `108/108@08c7a729`, baseline `70/72@a79945c4`
  (missing `r14-01`, `r14-02`, consistent with `## Reconciled current state` C6);
  depth `20/20@e1c83313`, `19/19@4d62ee5a`, `18/18@52b0eb29`, `17/17@c369242f`,
  `17/17@ebe2cb4a`, `9/9@638fb211`; block ranges `387-449@e1c83313`, `348-375@4d62ee5a`,
  `316-343@52b0eb29`; craft ranges `81-449@e1c83313`, `81-343@52b0eb29`, `77-191@a79945c4`;
  "grew 9→17 in eight commits `58116aa1`→`4072ebb3`" (parent 9; exactly eight rule-adding commits;
  17 at `4072ebb3`); calibration `9/9` (rubric 9 obligations, result `aligned 9`) at
  `result.json.measured_revision = c265db9b…`.
- **Five** of these 31 cell assertions are named by a rubric entry: `b1` (133/133), `b2` (20/20),
  `b3` (81-343), `b9` (81-449), `a3` (9/9). `a1`/`a2`/`a4` bind the *replacement* values, which exist
  only in the appended correction block and in no cell. **Zero** of the 31 are named by a `dropped`
  id. (The SHONEN box-1 pins `b4`/`b8` read the "earlier: … at `e1c83313`" sentence at
  `SHONEN.md:6`, a genuinely historical statement, so they are not laundered current values.)
- **Two statements disagree with the repo and are named nowhere** — the `Last-change` cells
  (C-5). One prose fragment (`the row said 75af886a until round 26`) is not re-derived by me.

So: no *numeric* assertion in the two cells is wrong; the undispositioned mismatch is the
`Last-change` round list, plus two record defects outside the table (C-1, closed at the corrected
tip; C-7, still open).

## 4. Findings (numbered, for the L1; I changed nothing)

### C-1 (was high; **confirmed at `8bb1090a`, fixed and disclosed at `923fa870`**) — the record commit was a ninth freeze violation, and the cited "tip" receipt was not a tip receipt

- At the record commit `8bb1090a`, `SCORECARD.md:3530` said "Both counters exit 2
  `frozen_path_changed` at `c86ea508` (and at the tip) because that commit wrote 8 files under the
  frozen `tools/round-44/control-fixtures/`", citing
  `.ufo/waves/round-44/l1/{c1,c2}-score-at-tip.json`. The committed
  `l1/c2-score-at-tip.json` has `"revision": "c86ea508…"` — a `c86ea508` run, not a tip run.
- Measured at `8bb1090a`:
  `python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev 8bb1090a… --freeze c48f8a4b… --work <SCRATCH> --json-out <OUT>`
  → **exit 2**, `frozen_path_changed` had **9** entries; the ninth was `SCORECARD.md` with
  `state: bound_edit_violation`, `reason: appended_block_differs_from_expected_edit`
  (`artifacts/…/c2-score-tip.json`). The `## Round 44` record section appended at `8bb1090a` was
  outside the frozen `expected_edits` block, which the rubric's note says is "The only post-freeze
  change to SCORECARD.md that this claim tolerates. The round-44 landing section cannot ALSO be
  appended to SCORECARD.md under the current counter contract … the L1 must either land it elsewhere
  or re-freeze with it bound" (`tools/round-44/c2-rubric.json:196`).
- **Fixed at `923fa870`** ("restore SCORECARD to the frozen-bounded blob", −16 lines): the same
  command at `923fa870` → **exit 2**, `frozen_path_changed` = **8** paths (M44-2 only) and
  `SCORECARD.md` `state: bound_edit_applied`, `reason: bound_edit`, `appended_lines 8`
  (`artifacts/…/c2-score-tip-923fa870.json`, stdout sha256 `83705252…`).
- **Disclosed**: `corpus/lessons/round-44.md` M44-3 ("freeze-violation (self-inflicted by the
  record)") and `LOG.md:3209-3216` ("Why the round-44 ledger lives here and not in `SCORECARD.md`");
  the ledger moved to `LOG.md` (`### Round 44 claim ledger`, row at `LOG.md:3225`, owned-scores line
  `:3227`). I found the same violation independently before reading M44-3; the record's account and
  my measurement agree on 9 paths and on the cause.
- Status: closed. The only residual from this finding is C-7, which the ledger move carried with it.

### C-2 (high) — the frozen claim's B2 gate (`asserted_not_in_base_line`) has no instrument, and its literal rule fails on all three target entries

- `plans/round-44-claims.md:214-215`: "`asserted` must be a byte substring of the BASE blob's
  `line_at_base` and `line_sha256 == sha256(that line)`; else exit 2 `asserted_not_in_base_line`".
- `grep -rn "asserted_not_in_base_line" tools/` → **no match** (exit 1). The frozen counter and the
  controls never emit it.
- The three targets cannot satisfy it: base line 23 (`sha256 81e06b81…`, the rubric's own
  `line_sha256` for a1) does **not** contain `137/137`; base line 24 (`b99cc56d…`, a2/a4's
  `line_sha256`) contains neither `21/21` nor `81-543` (`artifacts/…/b2-gate-evidence.txt`).
- Consequence: the anti-fabrication property the claim names does not exist. What actually holds is
  a different property — the base census re-derives each check at BASE (3 mismatches) and the
  correction block's value is compared to a freeze-tree derivation — so the *outcome* is not
  fabricated, but the *clause* is another internally unsatisfiable frozen sentence (same class as
  R44-CL2, which the lesson already routed for C1).
- Action: freeze the gate the instrument can compute next time ("`asserted` must equal the value the
  entry's check derives at the declared anchor, and the entry must be red in the base census"), not
  the substring rule.

### C-3 (medium) — "current observables" is false at the measured revision, and R2 makes the check blind to it

- `SCORECARD.md:3511` calls `137/137` the `## Owned axes` "current observables", "re-derived from the
  round-44 freeze tree". At `55bcce69` command A reports `knowledge_files 138, mapped 138`
  (`artifacts/…/commandA-55bcce69.json`); the tip is the same (`commandA-8bb1090a.json`).
- a1 is scored at the freeze tree (`__SCORING_REV__: FREEZE_TREE`, `c2-rubric.json:417`), and R2
  (`c2-rubric.json:159`) states the rationale: "a sibling landing after the freeze (C1's knowledge
  entry) cannot move the number under them." So `mismatches []` at REV says nothing about the row's
  value at REV; the value is guaranteed stale in exactly the round where the claim is measured.
- The number itself is not fabricated: 137/137 is true at the freeze, and the tip's own line
  `SCORECARD.md:3528` discloses both "137/137 before the round's entry" and `knowledge_files=138` at
  `c86ea508`. The defect is the label and the claim boundary.
- Action: in an appended correction, call it the **freeze-tree count**, and add the measured-revision
  value next to it; leave `c2-correction-value: 137/137` in place (it is what the counter reads).

### C-4 (medium) — CTL-C2-0 is not reproducible from the frozen command line

- `plans/round-44-claims.md:251`: "CTL-C2-0 do-nothing (counter `--pre-freeze` at BASE: non-zero
  **iff** frozen rubric shows mismatches > 0 at base; if 0, claim stops)". The counting command
  (`:249`) has no `--rubric`.
- The frozen command shape at BASE → **exit 2**, `entries_evaluated 0`, `mismatches []`, one
  unevaluable (`frozen_path_changed: [tools/round-44/c2-rubric.json]`, `rubric_changed`)
  (`c2-pre-freeze-base-norubric.json`). A 2 is could-not-evaluate, which the round's own rule says
  never counts, and the "iff" is then false (non-zero with no census).
- Adding `--rubric <lane>/tools/round-44/c2-rubric.json` → **exit 1**, 80 evaluated, exactly the
  three target ids (`c2-pre-freeze-base-rubric.json`) — matching the committed
  `.ufo/waves/round-44/w1/artifacts/R44C2Rubric/receipts/base-census-summary.json`
  (`entries_evaluated 80`, `mismatches 3`, the same ids, exit 1).
- Action: name the rubric argument (or a rubric-export step) in the claim's control text and counting
  command; a control whose pass depends on an argument the claim does not name is not reproducible
  from the claim.

### C-5 (medium) — the `## Owned axes` `Last-change` cells are stale, and the class is named by no rubric entry and no `dropped` id

- `SCORECARD.md:23` (`Last-change` cell): "count refreshed rounds 25, 26, 31, 36, 38, 39 and 40".
  The same cell's first clause is the round-41 refresh: "133/133 … command A at `e1c83313`", and
  `SCORECARD.md:3464` records "map proxy 130/130 → 133/133; command A at `e1c83313`". Round 41 is
  missing from the list.
- `SCORECARD.md:24` (`Last-change` cell): "count refreshed rounds 25, 26, 39 and 40". The same cell
  cites `17/17 at c369242f` ("prior recount … round 31") and the round-41 20/20, so rounds **31 and
  41** are missing.
- Neither cell is named by any of the 80 `entries` ids nor by any of the 10 `dropped` ids
  (`jq` over `tools/round-44/c2-rubric.json`). The claim's sentence at
  `plans/round-44-claims.md:204-205` — "all other candidates are explicitly dispositioned by id" —
  therefore does not cover this class. The wave-1 sentinel measured exactly this class and recorded
  it as not reached: `.ufo/waves/round-44/w1/R44C2SentReview.md:23` ("Owned-axes revision-pin triad
  consistency … reached by draft: **no** … internal disagreement at BASE") and `:48`
  (`TRI-1..TRI-3`; `:91` repeats them in its ">=9 BASE mismatches" list).
- This is a self-assessment statement that disagrees with the repo, inside the cells the claim
  repairs, and the C2 0-mismatch result cannot see it. Action: either add a fourth target (an
  append-only correction line naming rounds 31 and 41), or put the class in `dropped` with an exact
  `not-checkable-because`/out-of-scope disposition before the next freeze.

### C-6 (low) — the M44-2 fix cannot be wired as a general gate: it has no bound-edit mode

- `tools/round-45/frozen-path-preflight.py` compares FREEZE..REV touched paths against the
  `--pathspec`s it is given; it knows nothing about `expected_edits`/`preserve`.
- At the **clean** measured revision, with `--pathspec tools/round-44/ --pathspec SCORECARD.md`, it
  exits **1** on C2's declared append (`touched: [{"commit":"9d3d1862…","path":"SCORECARD.md",
  "status":"M"}]`; `artifacts/…/preflight-55bcce69-scorecard.json`).
- At the real tip with `--pathspec tools/round-44/` it exits 1 with the 8 fixture paths
  (`preflight-tip-tools44.json`), i.e. it does reproduce M44-2 under the record's own invocation.
- So the demonstrated invocation cannot see C2's bound paths, and adding them false-reds the
  declared landing. R44-CL1's "wire it into the commit sequence" therefore needs the tool taught the
  rubric's accepted edits (or one invocation per claim with that claim's path set and its own
  accepted edits). The pathspec matrix and the bare-run 557-path false red are in
  `R44W2C2Freeze.md` §F-6; this finding is the bound-edit half.

### C-7 (medium) — the record's pointer to the C2 base census resolves to a C1 control

- `LOG.md:3225` (R44-C2 ledger row; it was `SCORECARD.md:3526` at `8bb1090a` and moved with the
  ledger at `923fa870`): "the rubric's own base census (80 entries, per-id verdict vector) is
  committed with the rubric (`.ufo/waves/round-44/controls/c2/receipt.json`)".
- The pointer still resolves to the wrong artifact at the corrected tip. That path holds `{"title": "oracle-only fabrication with a re-minted evidence id", "claim":
  "R44-C1", "control": "CTL-C1-2", "verdict": "as_expected", "exit_code": 1}` — the C1 fabrication
  control, not a C2 census (`artifacts/…/record-pointer-evidence.txt`).
- The census exists at `.ufo/waves/round-44/w1/artifacts/R44C2Rubric/receipts/base-census-summary.json`
  (80 evaluated, exit 1, the 3 ids) and `…/census-base.json`; the lesson already cites the right
  family (`corpus/lessons/round-44.md:96` at `923fa870`; `:87` at `8bb1090a`).
- Action: re-aim the pointer (append a correction line to the ledger, or fix it in the round report).
  This is a record defect at a revision after the measured one — it does not change the score — but
  it sends a reader to the wrong artifact to check the claim's own control, and the ledger move
  carried it unchanged into `LOG.md`.

## 5. What survives falsification

- a2 (`21/21`) and a4 (`81-543`) are exactly what the recipe and the section-bounds rule derive at
  both the freeze and the measured revision.
- a1 (`137/137`) is exactly the freeze-tree value; it is not a fabricated number, and the record
  discloses the measured-revision value elsewhere in the same section.
- The base census is non-vacuous: exactly the three target ids are red at BASE, on the shipped
  counter with the shipped rubric (80 evaluated).
- The REV score is reproducible byte-for-byte from the frozen counter and rubric: exit 0, 80/80,
  `mismatches []`, `frozen_path_changed []`, counter and rubric hashes equal to their freeze hashes.
- The declarative landing is append-only and byte-exact at `55bcce69`; the two cited rows' digests are
  preserved; the pinned history was not rewritten.
- No numeric assertion in the two `## Owned axes` cells is wrong at its pin (31 rows catalogued).

## 6. Residual risk and verification gaps

- I re-derived the (b)/(c) values of the three Owned-axes rows and the calibration row's command-B
  facts. I did **not** re-derive the (a) capability pointers, the (d) planned rows, the (e) round
  verdicts, or the SHONEN/README families; their green status rests on the counter, not on my runs.
- `--pre-freeze` reproduced the committed census in aggregate and per id, but I did not diff stdout
  byte-for-byte against the committed `base-census.json` (the committed summary carries only a
  stdout sha256; my run's `--json-out` path and wall time differ, so an exact stdout match is not
  expected). The three mismatching ids are the observable that matters and they match.
- The prose "the row said `75af886a` until round 26" is not re-derived.
- C1's verdict and the M44-2 classification are peers' surfaces; my only C1-adjacent claim is that
  the C2 freeze walk does not include the claim file/SOURCES families (already `R44W2C2Freeze.md`
  F-1..F-4) and that the preflight has no bound-edit mode (C-6).
- The lane moved under me: the record commit `8bb1090a` was superseded by `923fa870` at 11:32Z. I
  measured C-1 at both, and re-read the moved ledger (`LOG.md:3225-3227`) at the new tip; every
  other finding was measured at the revision it names (`55bcce69` for the claim, `8bb1090a` for the
  record as dispatched).
- The pre-existing untracked files `.ufo/waves/round-44/l1/sources-census-end.txt`,
  `.ufo/waves/round-44/w2.ready`, `.ufo/waves/round-44/w2.ready.dispatched` were present before my
  first read; they are not mine. My only writes are this file and
  `.ufo/waves/round-44/w2/artifacts/R44W2C2Corrections/` (untracked).
- I ran no mutation and built no fixture repo, so no throwaway identity can exist.

## 7. Receipts

Full machine-readable receipts: `artifacts/…/receipts.json` (26 runs),
`artifacts/…/receipts-supplement.json` (2 pin runs) and
`artifacts/…/receipts-supplement2.json` (the corrected-tip rescore). Every entry carries seat, exact argv, cwd,
exit code, stdout sha256/bytes, stderr sha256, wall seconds and the artifact path.

Key runs (stdout sha256 prefix, wall):

| run | exit | sha256 | wall s |
|---|---|---|---|
| command A @ `55bcce69` | 0 | `b17d3c1c9b7214bd` | 0.079 |
| command A @ `c48f8a4b` (freeze) | 0 | `2aecd61e59a42a4d` | 0.077 |
| command A @ `8bb1090a` (tip) | 0 | `80a7e3474942eed0` | 0.079 |
| command A @ `e1c83313` | 0 | `4a2477e76613147b` | 0.076 |
| command A @ `4d62ee5a` | 0 | `85af1dba815b21e1` | 0.081 |
| command A @ `52b0eb29` | 0 | `3d39507a7ad59808` | 0.078 |
| c2 counter @ `55bcce69` (frozen) | 0 | `dd7c529bb6340c36` | 4.328 |
| c2 `--pre-freeze` @ base, no `--rubric` | 2 | `aff2e95504a9ce60` | 0.047 |
| c2 `--pre-freeze` @ base, `--rubric` | 1 | `1ac9e9225ee8b975` | 4.367 |
| c2 `--selftest` | 0 | `a5e942a1efa3172b` | 0.745 |
| c2 counter @ `8bb1090a` (record commit) | 2 | `0a81b8b2e85b0891` | 0.083 |
| c2 counter @ `923fa870` (corrected tip) | 2 | `837052522731aaef` | 0.112 |
| preflight tip `--pathspec tools/round-44/` | 1 | `dae13b0acb4810b6` | 0.088 |
| preflight `55bcce69` `--pathspec tools/round-44/ --pathspec SCORECARD.md` | 1 | `c8b7a69f12805178` | 0.090 |
| `git diff c48f8a4b 55bcce69 -- SCORECARD.md` | 0 | `5e1ca390013cac8d` | 0.002 |
| `git log --oneline c48f8a4b..8bb1090a -- tools/round-44/` | 0 | `b0d3ed0640b82bc3` | 0.001 |
