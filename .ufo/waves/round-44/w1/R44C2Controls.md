# R44C2Controls — the C2 controls (CTL-C2-0…4), their receipts and the per-entry fitness gate

**Seat:** `R44C2Controls` (wave 1, pre-freeze). **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
**Base:** `c29360e3ba5381a5ab69e372d0d9577970f85018` (claims base, lane `main`).
**Authored tool:** `.ufo/waves/round-44/w1/artifacts/R44C2Controls/c2-controls.py`
(sha256 `a169dec1bf37522d5255f2c4cd0f595a60ab8eb318c042f53e5d153306b5800e`) —
**installed** by this seat at L1's request to `tools/round-44/c2-controls.py`, same
sha256 (`cp` of the artifact, no commit; the L1 commits it in the freeze).
**Receipts:** `.ufo/waves/round-44/w1/artifacts/R44C2Controls/receipts/{dev-stale,dev-consistent,real-base}/`.

**Nothing here is a claim score.** This seat authored and exercised the *controls*;
the C2 claim score at the measured revision is the L1's to run after the freeze.
No file outside my seat's artifacts and this report was written; no C1 data
procedure (`tools/round-44/c1-run.sh`) was run — it does not exist yet and is
forbidden to me in any case.

**Axes:** calibration (C2). Depth/coverage are untouched by this seat.

---

## 1. The controls, and the counter they drive

The controls are the ones `plans/round-44-claims.md` `## R44-C2` names (the file
was amended by the L1 during wave 1; the amended `## Controls` line adds
**CTL-C2-4**, and the rubric design section adds a **per-entry fitness gate** —
both are implemented here). Each control is scored by running the **frozen
counter** (`tools/round-44/c2-counter.py`; wave-1 artifact
`.ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py`, sha256
`085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277`) as a
subprocess; the control reads the counter's own JSON receipt. **No control is
decided by a hand-written verdict.**

| id | arm | expected | measured (`real-base`) |
|---|---|---|---|
| **CTL-C2-0** | do-nothing / honest-stop gate: the census at the base with the frozen rubric | exit 1 iff `mismatches > 0`; exit 0 iff 0 mismatches (then R44-C2 **STOPS**); exit 2 = could-not-evaluate | **exit 1** — `mismatches 3`, `entries_evaluated 80/80`, ids `[C2-a1-owned-coverage-count, C2-a2-owned-depth-count, C2-a4-owned-depth-craft-range]`, `unevaluable []` |
| **CTL-C2-1** | seeded mismatch: one rubric-named statement made wrong in a scratch clone | exit 1 with the seeded mismatch reported by id | **exit 1** — newly-mismatching `[C2-d17-sharpen-log-round43-entry]` (the rubric's own declared seed), attribution `seed_induced` |
| **CTL-C2-2** | malformed rubric: one entry's check command dropped | exit 2 `rubric_malformed: entry_0_missing_command` — never a score | **exit 2** — `unevaluable: rubric_malformed: entry_0_missing_command` |
| **CTL-C2-3** | rubric immutability: the rubric (a frozen path) edited mid-round | exit 2 with `frozen_path_changed` naming `tools/round-44/c2-rubric.json` | **exit 2** — `frozen_path_changed: ["tools/round-44/c2-rubric.json"]` |
| **CTL-C2-4** | wrong-value note: a correction note carrying a wrong value | never a pass — enforced arm refuses (exit 2, `frozen_path_changed`), scored arm keeps the entry a mismatch (`UNSUPPORTED:<note value>`) | **exit 2** on the enforced arm; the scored arm exits 1 with `note_observation: UNSUPPORTED:137/137 [WRONG]` |

Exit codes are semantic: 0 met/clean, 1 failed, 2 could-not-evaluate. **An exit 2
never counts toward the target** — it is the refusal of a malformed rubric, of a
rubric edit and of an unbound note, not a "not a pass".

### The honest-stop gate did **not** fire

CTL-C2-0 found **3 mismatches at the base** — `C2-a1-owned-coverage-count`,
`C2-a2-owned-depth-count`, `C2-a4-owned-depth-craft-range` — with 80/80 entries
evaluable, no unevaluable entry and `frozen_path_changed []`. The do-nothing
control therefore **fails** (the counter can still see the drift), so the C2
claim is **not** stopped on the base census. The three ids are exactly the
rubric's own declared CTL-C2-0 vector
(`control_vectors["CTL-C2-0 do-nothing (base census, --rev BASE --pre-freeze)"]`:
`counter_exit_code 1`, `entries_evaluated 80`, `unevaluable 0`,
`mismatch_count 3`, the same three ids); my control checks that vector field by
field — `declared_vector_checks` in the receipt is all-true. The three
observations are `UNSUPPORTED:133/133`, `UNSUPPORTED:20/20` and
`UNSUPPORTED:81-449` against the asserted `137/137`, `21/21`, `81-543`: the
`## Owned axes` rows still quote the round-41 counts while the tree holds the
round-42+ values.

Had the census found **zero** mismatches, this control would have exited 0 and
reported `claim_stops: true`; the tool's `--dev-variant consistent` arm
demonstrates that path end-to-end (§5), so the stop is a reachable, exercised
branch, not a hypothetical. **The rubric is not loosened to make the claim
scoreable.**

---

## 2. How each control is implemented (`c2-controls.py`)

* **CTL-C2-0** — runs the counter in `--pre-freeze` mode at the base with the
  frozen rubric (the freeze walk is reported, not enforced: at the base the
  freeze is not yet an ancestor of the measured revision). The counter refuses a
  rubric whose declared `freeze` differs from the `--freeze` argument, so the
  attempts run a fixed ladder and the first attempt that produces a census is
  scored: `--rev BASE --freeze <FREEZE> --pre-freeze`, then
  `--rev BASE --pre-freeze`, then `--rev BASE --freeze <the rubric's declared
  freeze> --pre-freeze`. The score is the census: `mismatches > 0` ⇒ exit 1;
  `mismatches == 0` ⇒ exit 0 **and `claim_stops: true`**. When the rubric
  declares a `control_vectors` entry for CTL-C2-0, the observed census is also
  checked against that frozen vector (per-id, not just the aggregate count, as
  the amended claims require).
* **CTL-C2-1** — two arms, both in a scratch **clone** of the lane
  (`git clone --shared --no-checkout`, then `checkout` the freeze; the clone's
  `git rev-parse --show-toplevel` is asserted to equal the clone dir before any
  mutation).
  * *arm A, reality side*: a **non-frozen** file the rubric points at is mutated
    (a count decremented, an evidence value changed) and committed. When the
    rubric declares its own seed (`seeded_mismatch.primary`), that declared seed
    is used first — here: rename the `LOG.md` round-43 heading
    (`## 2026-10-27 - round 43 …` → `… round 43x …`); `LOG.md` is not a frozen
    path of this claim, so the entry is scored and must report the mismatch.
  * *arm B, rubric side*: a scratch copy of the rubric whose seeded entry
    carries a wrong asserted value (a count decremented, an evidence path
    deleted). A fabricated rubric must not pass.
  * An **unseeded baseline** is run at the same freeze first, so the seed is
    *attributable*: a mismatch counts as seed-induced only when the seeded id is
    reported now and was **not** reported in the baseline. In the real-base run
    `baseline_mismatch_ids` = the three census ids and
    `newly_mismatching_ids` = `[C2-d17-sharpen-log-round43-entry]` — the seed
    caused exactly one new mismatch and nothing else moved.
  * The rubric's own `seeded_mismatch.secondary` (an in-place edit of a
    `SCORECARD.md` evidence pointer) is deliberately **not** the primary arm:
    `SCORECARD.md` is frozen with an append-only bound edit, so an in-place
    statement edit is a freeze violation (exit 2 `frozen_path_changed`), not an
    entry-level mismatch. The tool scores what actually happens; it does not
    fake an entry-level result.
* **CTL-C2-2** — the rubric is copied, the first entry's command key is dropped
  (`dropped_keys: ["command"]`), and the counter is asked to score the broken
  copy. The refusal (`rubric_malformed: entry_0_missing_command`) is read from
  the counter's own receipt.
* **CTL-C2-3** — the rubric is a **frozen path**. A clone is committed with the
  rubric bytes at a freeze commit and then **edited in place** mid-round (an
  `"asserted"` key renamed, not an append). The counter is then asked to score
  `FREEZE..REV` and must refuse: exit 2, `frozen_path_changed` naming
  `tools/round-44/c2-rubric.json`. When the rubric is committed at the real
  freeze the real freeze is used (`freeze_arrangement: real_freeze`); before the
  L1 installs it, a synthetic freeze commit inside the clone holds the rubric
  bytes (`freeze_arrangement: synthetic_freeze`, as in the real-base run). A
  later restore does not un-block: the walk compares FREEZE..REV.
* **CTL-C2-4** — the rubric's `expected_edits` bind the exact appended block of
  the correction note. The control appends that block to the rubric-named frozen
  file with the bound `c2-correction-value:` line **replaced** by a wrong value
  (replacing, not appending after: the check reads the *first*
  `c2-correction-value:` after its marker, so an appended second line would
  leave the correct value in force and the note would never be wrong — my first
  implementation made exactly that mistake and the scored arm caught it).
  * *arm A, enforced*: the freeze walk is enforced — the note is not the bound
    edit, so the counter refuses with exit 2 `frozen_path_changed: ["SCORECARD.md"]`.
  * *arm B, scored*: the same note with the freeze walk reported but not
    enforced (census mode), so the **entry** is scored: the check re-derives the
    value from the tree, the note's value disagrees with the derivation, and the
    observation is `UNSUPPORTED:137/137 [WRONG]` — the entry stays a mismatch.
    **A note is never evidence.** The amended claims name this outcome
    `note_value_disagrees`; the counter's observation rule renders it as
    `UNSUPPORTED:<note value>` (the receipt field is `note_observation`), so the
    name in the claims and the string in the receipt are the same event.
  * The control passes when **neither** arm yields a pass.

### Modes

`--mode dev` builds two self-contained synthetic fixtures (a statement, a tree
and a check script): `stale` (the statement claims 7, the tree holds 6 → the
census reports one mismatch) and `consistent` (both 6 → zero mismatches). The
controls other than CTL-C2-0 are scored on the `consistent` fixture, so a green
baseline makes a seeded mismatch attributable. `--mode real` is the lane with the
real rubric; `--mode auto` picks `real` when `tools/round-44/c2-rubric.json` is
present, else `dev`. The tool never runs the after-side C2 data procedure (there
is none) and never scores the claim.

---

## 3. Receipts — `real-base` (the lane, the authored rubric, at the base)

Command (identical for all five controls; the per-control `--json-out` differs):

```
python3 -I -B .ufo/waves/round-44/w1/artifacts/R44C2Controls/c2-controls.py \
  --counter .ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py \
  --mode real --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rubric .ufo/waves/round-44/w1/artifacts/R44C2Rubric/tools/round-44/c2-rubric.json \
  --rev c29360e3ba5381a5ab69e372d0d9577970f85018 \
  --freeze c29360e3ba5381a5ab69e372d0d9577970f85018 \
  --work <scratch> --out <out> --json-out <out>/summary.json
```

Tool exit **0**; tool stdout sha256
`441cf48d1f34080d112d7360653ea71d7d0fdd315dfc6827d963475f8b7a4530`; tool wall
**37.676525 s**. Counter sha256
`085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277`; rubric
sha256 **at the time of the run** `e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e`.

| control | counter exit | stdout sha256 | wall s | receipt |
|---|---|---|---|---|
| CTL-C2-0 | 1 | `27b6c7d018def8882346506c6a6d15c644f648cc244446062fda84eba01551c8` | 7.036751 | `receipts/real-base/CTL-C2-0.json` |
| CTL-C2-1 | 1 | `05e6770f41d233883a4b1695ab2ae0ce0dcfa00bc53863162694939d7b177347` | 6.421506 | `receipts/real-base/CTL-C2-1.json` |
| CTL-C2-2 | 2 | `c3ce7439937677a80e5000836395daaa63ac1675033555084903711ae29d83eb` | 0.055386 | `receipts/real-base/CTL-C2-2.json` |
| CTL-C2-3 | 2 | `78aec5f603d6a55d9c209da280b2520273072307be46282bdad9ac717a1ac7a7` | 0.070510 | `receipts/real-base/CTL-C2-3.json` |
| CTL-C2-4 | 2 | `e4afbf1a5531760284b864093a5be1cebf174e3a253111fd8251ea8101cc070e` | 0.072513 | `receipts/real-base/CTL-C2-4.json` |

Each receipt is `{control, command, exit_code, expected, seat, argv, stdout_sha256,
stdout_bytes, stdout_head, stderr_head, wall_seconds, tool_command,
tool_stdout_sha256, tool_wall_seconds, tool_exit_code, …control detail}`.

### receipt.json per control (verbatim, `real-base`)

<details><summary>CTL-C2-0 — do-nothing / honest-stop gate</summary>

```json
{
  "control": "CTL-C2-0",
  "command": "/usr/bin/python3 -I -B …/R44C2Counter/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c29360e3ba5381a5ab69e372d0d9577970f85018 --freeze c29360e3ba5381a5ab69e372d0d9577970f85018 --work <scratch> --rubric …/R44C2Rubric/tools/round-44/c2-rubric.json --json-out <out>/ctl-c2-0.json --pre-freeze --seat R44C2Controls",
  "exit_code": 1,
  "expected": "exit 1 iff the frozen rubric shows mismatches > 0 at the base; exit 0 iff 0 mismatches (then R44-C2 STOPS); exit 2 = could-not-evaluate",
  "seat": "R44C2Controls",
  "stdout_sha256": "27b6c7d018def8882346506c6a6d15c644f648cc244446062fda84eba01551c8",
  "wall_seconds": 7.036751,
  "mismatches": 3,
  "mismatch_ids": ["C2-a1-owned-coverage-count", "C2-a2-owned-depth-count", "C2-a4-owned-depth-craft-range"],
  "entries_evaluated": 80,
  "entries_count": 80,
  "unevaluable": [],
  "frozen_path_changed": [],
  "pre_freeze": true,
  "claim_score": false,
  "expected_exit_code": 1,
  "kill_rule_fired": false,
  "claim_stops": false,
  "declared_vector_checks": {
    "counter_exit_code_matches": true,
    "entries_evaluated_matches": true,
    "mismatch_count_matches": true,
    "mismatch_ids_match": true
  },
  "verdict": "ok"
}
```

</details>

<details><summary>CTL-C2-1 — seeded mismatch</summary>

```json
{
  "control": "CTL-C2-1",
  "command": "/usr/bin/python3 -I -B …/R44C2Counter/c2-counter.py --root <scratch>/ctl-c2-1-clone --rev 9a4f587b6c6b91e3dd9c1c5cd18f87a217d7bb3c --freeze c29360e3ba5381a5ab69e372d0d9577970f85018 --work <scratch> --rubric …/R44C2Rubric/tools/round-44/c2-rubric.json --json-out <out>/ctl-c2-1.json --seat R44C2Controls",
  "exit_code": 1,
  "expected": "the counter must report the seeded mismatch by id and exit non-zero (1) at the seeded revision",
  "seat": "R44C2Controls",
  "stdout_sha256": "05e6770f41d233883a4b1695ab2ae0ce0dcfa00bc53863162694939d7b177347",
  "wall_seconds": 6.421506,
  "seeded_entry": "C2-d17-sharpen-log-round43-entry",
  "seeded_entry_reported_in_mismatches": true,
  "baseline_mismatch_ids": ["C2-a1-owned-coverage-count", "C2-a2-owned-depth-count", "C2-a4-owned-depth-craft-range"],
  "newly_mismatching_ids": ["C2-d17-sharpen-log-round43-entry"],
  "attribution": "seed_induced",
  "verdict": "ok"
}
```

</details>

<details><summary>CTL-C2-2 — malformed rubric</summary>

```json
{
  "control": "CTL-C2-2",
  "command": "/usr/bin/python3 -I -B …/R44C2Counter/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c29360e3… --freeze c29360e3… --work <scratch> --rubric <scratch>/ctl-c2-2-malformed-rubric.json --json-out <out>/ctl-c2-2.json --seat R44C2Controls",
  "exit_code": 2,
  "expected": "a rubric with a dropped check command must be refused: exit 2 (rubric_malformed), never a score",
  "seat": "R44C2Controls",
  "stdout_sha256": "c3ce7439937677a80e5000836395daaa63ac1675033555084903711ae29d83eb",
  "wall_seconds": 0.055386,
  "dropped_keys": ["command"],
  "unevaluable": "rubric_malformed: entry_0_missing_command",
  "verdict": "ok"
}
```

</details>

<details><summary>CTL-C2-3 — rubric immutability</summary>

```json
{
  "control": "CTL-C2-3",
  "command": "/usr/bin/python3 -I -B …/R44C2Counter/c2-counter.py --root <scratch>/ctl-c2-3-clone --rev 499458fa33a38e1c00fcb951e26303184c472150 --freeze 1ab744dd5dbcbfc82ab042e115423e7de72ef97d --work <scratch> --json-out <out>/ctl-c2-3.json --seat R44C2Controls",
  "exit_code": 2,
  "expected": "a mid-round edit of the frozen rubric must re-red: exit 2 with frozen_path_changed naming tools/round-44/c2-rubric.json",
  "seat": "R44C2Controls",
  "stdout_sha256": "78aec5f603d6a55d9c209da280b2520273072307be46282bdad9ac717a1ac7a7",
  "wall_seconds": 0.07051,
  "freeze_arrangement": "synthetic_freeze",
  "freeze_used": "1ab744dd5dbcbfc82ab042e115423e7de72ef97d",
  "edited_revision": "499458fa33a38e1c00fcb951e26303184c472150",
  "frozen_path_changed": ["tools/round-44/c2-rubric.json"],
  "unevaluable": [{"id": null, "reason": "frozen_path_changed"}],
  "verdict": "ok"
}
```

</details>

<details><summary>CTL-C2-4 — wrong-value note</summary>

```json
{
  "control": "CTL-C2-4",
  "command": "/usr/bin/python3 -I -B …/R44C2Counter/c2-counter.py --root <scratch>/ctl-c2-4-clone --rev ee66409920e7419460d41d5689b2c94ebdfc5d29 --freeze c29360e3… --work <scratch> --rubric …/R44C2Rubric/tools/round-44/c2-rubric.json --json-out <out>/ctl-c2-4-enforced.json --seat R44C2Controls",
  "exit_code": 2,
  "expected": "a correction note carrying a wrong value must never pass: the counter refuses it (enforced arm) and the entry stays a mismatch (scored arm, note_value_disagrees)",
  "seat": "R44C2Controls",
  "stdout_sha256": "e4afbf1a5531760284b864093a5be1cebf174e3a253111fd8251ea8101cc070e",
  "wall_seconds": 0.072513,
  "target_file": "SCORECARD.md",
  "wrong_value": "81-543 [WRONG]",
  "arm_A_passed": false,
  "arm_B_passed": false,
  "arms": {
    "A_enforced": {"exit_code": 2, "frozen_path_changed": ["SCORECARD.md"], "unevaluable": [{"id": null, "paths": ["SCORECARD.md"], "reason": "frozen_path_changed"}]},
    "B_scored": {"exit_code": 1, "mismatches": ["C2-a1-owned-coverage-count", "C2-a2-owned-depth-count", "C2-a4-owned-depth-craft-range"], "note_observation": "UNSUPPORTED:137/137 [WRONG]"}
  },
  "verdict": "ok"
}
```

</details>

The full receipts (every attempt, every arm, the declared-vector checks and the
tool-level digests) are in `receipts/real-base/`.

---

## 4. The per-entry fitness gate

The amended claims require, at the freeze, that **every check is shown able to
fail on its own entry** (one mutation per entry; the entry must then be
reported as a mismatch). `c2-controls.py --fitness` implements it: for each
rubric entry, one mutation of that entry's `asserted` value is applied to a
scratch copy of the rubric and the counter is asked to score it; the entry must
then appear in `mismatches`.

Measured on the lane's rubric — **all 80 of 80 entries** (not a sample):

* `entries_scored 80`, `entries_failing_to_fail []`, `ok true`;
* every one of the 80 counter runs exited **1** and reported the mutated entry
  by id (`reported_in_mismatches` is true in all 80 rows);
* tool exit **0**, tool stdout sha256
  `3b6bf21694ec8d5b6bf36a24a2b06cf0e9f7302eac886944515b88be6c97b982`, wall
  **462.893311 s**; counter sha256 `085192ea…`, rubric sha256 `e8cc0ded…`.

Receipts: `receipts/fitness-full/summary.json` (every row with its counter
stdout sha256 and wall time) and `receipts/fitness-full/fitness-rows.md` (the
per-entry table). The 80 raw per-entry counter receipts (~60 MB) are left in
scratch, not in the lane; the summary carries every row's digest, so any single
row is re-runnable from its recorded command and sha256. **A check that cannot
fail on its own statement is not a check**, and none of the 80 is in that
state.

## 5. The `dev` arms — each control shown able to fail

`--mode dev` builds the two synthetic fixtures described in §2.

| variant | CTL-C2-0 census | tool exit | meaning |
|---|---|---|---|
| `dev-stale` (the statement is wrong) | `mismatches 1` → counter exit 1 | **0** | the do-nothing control fails, as it must |
| `dev-consistent` (the statement is right) | `mismatches 0` → counter exit 0, `claim_stops: true` | **1** | the do-nothing control reaches the target ⇒ **R44-C2 would STOP** |

The `dev-consistent` arm is the honest-stop branch, exercised: the census
returns 0, the tool reports `kill_rule_fired: ["CTL-C2-0"]` and exits 1. The
`dev-stale` arm is the branch that lets the claim proceed. Both are in
`receipts/dev-stale/` and `receipts/dev-consistent/` (tool stdout sha256
`dde4ecdf26814a430d07b09cc767640d0661c025341f77225ba1e3ecc8b4baea` and
`309673eabeb7ccfa0707c493838ccec94ca8fbdb56e8ebfca92f6d168e8143dd`).

---

## 6. What the L1 must run at the freeze (and what I could not run)

* **I did not run the after-side C2 score.** That is the L1's, after the freeze.
* **CTL-C2-0 at the freeze** must be re-run against the *installed*
  `tools/round-44/c2-rubric.json` at the *real* freeze commit. My `real-base`
  run used the wave-1 rubric artifact and the claims base as both `--rev` and
  `--freeze`, so it is a **census**, not a score: the counter itself reports
  `pre_freeze: true`, `claim_score: false`.
* **CTL-C2-3's real-freeze path** (`freeze_arrangement: real_freeze`) becomes
  reachable once the L1 installs the rubric under `tools/round-44/` and freezes
  it; until then the synthetic-freeze arrangement is used, which exercises the
  same freeze walk over the same path.
* **The counter artifact changed twice during wave 1** (`c80f2586…` at 08:17,
  `a6896459…` later, `085192ea…` when these receipts were taken). The counter's
  sha256 is recorded in every receipt and in the summary, so a stale receipt is
  detectable. **Resolved at install time:** the bytes the L1 installed are
  byte-identical to the bytes these receipts measured —
  `tools/round-44/c2-counter.py` = `085192ea…` (the receipt's counter sha256)
  and `tools/round-44/c2-rubric.json` = `e8cc0ded…` (the receipt's rubric
  sha256). So the `real-base` receipts and the 80-entry fitness gate are **not**
  stale against the installed pair; they still need re-running only if the L1
  re-freezes different bytes.
* **What I did not do:** I did not evaluate the rubric's own `CTL-C2-POS`
  positive vector (bound correction block appended to `SCORECARD.md` ⇒ counter
  exit 0, `met_target true`). That is a post-landing measurement on the real
  tree, not a control; the rubric seat owns that arm.

## 7. Honest limits

* The `real-base` census measures the **wave-1 rubric artifact** at the
  **claims base**, not the frozen rubric at the freeze. It is a *census*, and
  the counter marks it `claim_score: false`.
* The three base mismatches (`C2-a1`, `C2-a2`, `C2-a4`) are the rubric's own
  declared findings; my control confirms the counter reports them, it does not
  adjudicate them.
* The seeded arm's baseline is the base census (which already has 3
  mismatches), so `attribution` is a **set difference**, not an exit-code
  comparison: the seed is credited only for ids absent from the baseline.
* The fitness gate scored all 80 rubric entries (one asserted-value mutation
  each), but it ran against the rubric sha256 `e8cc0ded…` — if the rubric
  changes again before the freeze, the gate must be re-run (the receipt records
  the sha, so the staleness is detectable, not silent).
* My controls never write to the lane tree: the mutations happen in scratch
  clones under `--work`; the lane's working tree is untouched by this seat
  (`git status --porcelain` shows no change under `SCORECARD.md`, `SHONEN.md`,
  `corpus/README.md` or `tools/`).
