# R44W2C2Rescore — independent re-derivation of the R44-C2 score (identical), plus three instrument defects: six `steered` entries are constant-observed green generators, the M44-2 preflight has no bound-edit arm, and the C1 "no run can satisfy" cause is falsified

Seat `R44W2C2Rescore`, round 44 wave 2 (falsification of the landing and the record).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`; measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; base `c29360e3ba5381a5ab69e372d0d9577970f85018`;
lane tip at dispatch `c86ea508188c50e2645b1f9bba65df4177cda6b1`; record commit `8bb1090af3fef64477c4337855e4347472db2701`.

**Record bytes I reviewed.** `HEAD` = `8bb1090a` throughout; the lesson blob at HEAD is
`10648469567ffff7846f13516e5f0ba43ae3caa` (sha256
`d48af63c72b52b68be11607c1a5b9bfb812e551acf5ea59d2edeb29447837cb0`). While this seat ran, the L1
amended `LOG.md`, `SCORECARD.md` and `corpus/lessons/round-44.md` in the **worktree** (mtimes
11:26:55 / 11:26:55 / 11:27:18; lesson worktree sha256
`0bdca5b942fc7162ab8bc636b8f0553efd3e9be629d2d333b0c79e6f2b24b08b`). Those uncommitted amendments
already fold in parts of wave 2 (the R44-CL2 qualifier and R44-CL7); every record quote below is
pinned to `8bb1090a` and each place where the live worktree already answers the finding is said so.

No claim, counter, rubric, frozen byte or production doc was changed. Every mutation lived inside
this seat's own clone at `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C2Rescore/` (one `git clone
--shared` for the baseline, seven throwaway clones for the arms); `git rev-parse --show-toplevel`
was asserted on every fixture before its commit, and every fixture commit carries
`user.name=R44W2C2Rescore-fixture` / `user.email=rescore@fixture.invalid`. No tool was installed,
upgraded or removed (nothing was needed; pacman is paused host-wide). Scratch tree deleted at the
end of the seat.

---

## 1. Verdict table

| # | Question | Verdict |
|---|---|---|
| 1 | Does the frozen C2 counter reproduce `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, exit 0, `met_target true` at `55bcce69`? | **CONFIRMED** — byte-identical gate, zero non-path entry differences vs `l1/c2-score-at-55bcce69.json`. |
| 2 | Does the counter/rubric sha256 pair match at freeze, rev and tip? | **CONFIRMED** — counter `085192ea…`, rubric `e8cc0ded…` identical at all three. |
| 3 | Is the score non-vacuous (can it fail)? | **CONFIRMED** by four independent reds, incl. the exact three BASE values reappearing when the correction block is deleted (§3). |
| 4 | Is a note ever evidence? | **CONFIRMED NO** — a wrong correction value reds `C2-a1` with `UNSUPPORTED:137/999` (§3, mut1). |
| 5 | Are all 80 entries real checks? | **FALSIFIED for 6 of them** — the `expected:"superseded"` entries emit a constant `observed` equal to `asserted`; the counter never reads the `derived` field they compute (D-1, §5). |
| 6 | Does the tip really exit 2 with the 8 frozen paths? | **CONFIRMED** — identical list in my run, in `l1/c2-score-at-tip.json`, and in `l1/preflight-c86ea508.json`. |
| 7 | Is M44-2 recorded honestly and is `tools/round-45/frozen-path-preflight.py` sufficient? | **Honest and sufficient for the M44-2 instance**; **not sufficient as a gate**: it has no bound-edit arm, so it false-reds the claim's own lawful `SCORECARD.md` append (D-2, §6). |
| 8 | Does the record state the C1 red's cause exactly? | **NO** — the red at `55bcce69` is the three withdrawn documentation bindings, not provenance; the same receipts scored exit **0** at `4cc1ac11` (D-3, §7). Corroborates `w2/R44W2C1Rescore.md` D-1/D-2 by an independent route. |

---

## 2. Independent re-derivation of R44-C2 at `55bcce69`

One clone, one run, no rubric/counter edits:

```
git clone --shared <LANE> /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C2Rescore/lane
git -C lane reset --hard 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac
python3 -I -B tools/round-44/c2-counter.py --root . \
    --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac \
    --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
    --work <SCRATCH>/work --json-out <SCRATCH>/score.json
→ exit 0 · entries_evaluated 80 · mismatches [] · frozen_path_changed [] · met_target true
  claim_score true · usable_as_claim_score true · entries_count 80 · unevaluable 0
  counter_sha256 085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277
  counter_sha256_at_freeze  ==  same
  rubric_sha256           e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e
  rubric_sha256_at_freeze ==  same          rubric_sha256_at_rev == same      rubric_source "freeze"
  stdout sha256 dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3
  counter wall_seconds 4.391943 (outer 4.44 s) · exported_path_count 3204 · export_mode auto
```

| field | mine | `l1/c2-score-at-55bcce69.json` | |
|---|---|---|---|
| `exit_code` | 0 | 0 | same |
| `entries_evaluated` / `entries_count` | 80 / 80 | 80 / 80 | same |
| `mismatches` / `mismatches_count` | `[]` / 0 | `[]` / 0 | same |
| `frozen_path_changed` / `frozen_dirs` | `[]` / `["tools/round-44"]` | `[]` / `["tools/round-44"]` | same |
| `claim_score` / `met_target` / `usable_as_claim_score` | true / true / true | true / true / true | same |
| `entries_count`, `unevaluable`, `unevaluable_count` | 80, `[]`, 0 | 80, `[]`, 0 | same |
| `counter_sha256`, `counter_sha256_at_freeze` | `085192ea…` | `085192ea…` | same |
| `rubric_sha256`, `…_at_freeze`, `…_at_rev` | `e8cc0ded…` | `e8cc0ded…` | same |
| `rubric_source` / `pre_freeze` / `declared_freeze` | freeze / false / null | freeze / false / null | same |
| `exported_path_count` / `export_mode` | 3204 / auto | 3204 / auto | same |

Entry-level comparison (all 80 ids, every field): **zero non-path differences**. The only fields
that differ are `command` (absolute scratch tree/repo paths), `argv_digests` (their consequence) and
`wall_seconds`. The `match` vector and the `observed` vector are identical for all 80 entries.

**Sha256 at three points.** `git show <rev>:tools/round-44/c2-counter.py | sha256sum` and the same
for `c2-rubric.json`:
freeze `c48f8a4` → `085192ea…` / `e8cc0ded…`; measured rev `55bcce69` → identical; tip `c86ea508` →
identical. The instrument is the same object everywhere; only the tree moves.

**Admissibility.** `git log -m --diff-merges=first-parent --name-only c48f8a4..55bcce69` lists six
commits (`fee6e98a`, `4cc1ac11`, `9d3d1862`, `75a5cb42`, `e9e3abd1`, `55bcce69`) and, over the
frozen set, only `SCORECARD.md` — and that only as the rubric-bound append
(`git diff --stat c48f8a4 55bcce69 -- SCORECARD.md` → `8 insertions(+)`). `tools/round-44/`,
`SHONEN.md` and `SKILL.md` are untouched. The score is admissible under the claim's freeze rule.

---

## 3. Non-vacuity ladder (the same frozen instrument, four independent reds)

| arm | command shape | exit | `entries_evaluated` | mismatches | what it proves |
|---|---|---|---|---|---|
| A. at the freeze (`--rev c48f8a4 --freeze c48f8a4`) | as §2 | **1** | 80 | `C2-a1-owned-coverage-count`, `C2-a2-owned-depth-count`, `C2-a4-owned-depth-craft-range` | the rubric's own base census; the claim's "STOPS if zero mismatches at BASE" gate did not fire |
| B. pre-landing `--rev fee6e98a --freeze c48f8a4` | as §2 | **1** | 80 | the same three ids | after the freeze but before the correction, the instrument is red on exactly the three repaired statements |
| C. mut2 — the 6-line correction block deleted from `SCORECARD.md`, `--rev=--freeze=<mutant be338c53>` | as §2 | **1** | 80 | the same three ids | the values are re-derived, not restated: `observed` = `UNSUPPORTED:133/133`, `UNSUPPORTED:20/20`, `UNSUPPORTED:81-449` — the BASE values come back |
| D. mut1 — correction value changed to `137/999`, `--rev=--freeze=<mutant c967ce2e>` | as §2 | **1** | 80 | `C2-a1-owned-coverage-count` (observed `UNSUPPORTED:137/999`) | **a note is never evidence**: the note's value is compared with the independent derivation and a wrong note reds |
| E. mut4 — capability Evidence path `…/luna-round-6/receipts/` → `…/receipts-Z/`, `--rev=--freeze=<mutant 0024b5a9>` | as §2 | **1** | 80 | `C2-c01-cap-pointer` (observed `UNSUPPORTED:unresolved:.ufo/waves/luna-round-6/receipts-Z/`) | the category-(a) pointer checks resolve paths, they do not merely parse them |

Arms C–E also carry one `C2-h1-readme-coverage-map-complete` mismatch each. That is an artifact of
the **technique**, not of the instrument: `--freeze=<mutant>` makes the freeze tree the
`55bcce69` tree, which already carries the round-44 knowledge entry, so command A counts
`138/138` while the rubric asserts the freeze-tree `137/137`. Stated here so the extra red is not
misread. The three target ids' verdicts are unaffected (their assertions are `137/137`, `21/21`,
`81-543` of the *freeze* tree, and arm C shows them failing on the BASE values).

`python3 -I -B tools/round-44/c2-counter.py --selftest` → **exit 0**, `"ok": true`, `"selftest":
"P44-C2"` (stdout sha256 `a5e942a1efa3172b…`, receipt `artifacts/R44W2C2Rescore/c2-selftest.txt`).

---

## 4. The tip: `frozen_path_changed`, exactly 8 paths

```
python3 -I -B tools/round-44/c2-counter.py --root . --rev c86ea508… --freeze c48f8a4… \
        --work <SCRATCH>/work-tip --json-out <SCRATCH>/score-tip.json
→ exit 2 · entries_evaluated 0 · unevaluable_count 1 (reason frozen_path_changed) · met_target false
  claim_score true · usable_as_claim_score false · wall 0.050081 s
  frozen_path_changed (8):
    tools/round-44/control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json
    tools/round-44/control-fixtures/c3/manifest.json
    tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1be/after.json
    tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json
    tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v2be/after.json
    tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v2le/after.json
    tools/round-44/control-fixtures/pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md
    tools/round-44/control-fixtures/pos/manifest.json
  freeze_notes: 8 × changed_under_frozen_dir; SCORECARD.md bound_edit_applied (8 lines);
                SHONEN.md / SKILL.md / c2-counter.py / c2-rubric.json unchanged
```

The list is identical to `l1/c2-score-at-tip.json`, to `l1/preflight-c86ea508.json` (`touched`, all
`status M`), and to the C1 counter's own `frozen_path_changed` at the tip. `git log --oneline
c48f8a4..main -- tools/round-44/` → only `c86ea508`. The record's M44-2 statement ("8 files", "both
counters exit 2", "admissible revision is `55bcce69`") matches what I measure.

---

## 5. D-1 — six rubric entries are green generators: `observed` is a constant and `derived` is never compared

**Severity: medium (instrument model; does not touch the three target repairs).**

The rubric's own `check_contract` says each check prints `{"observed", "derived", "detail"}` and
that *observed* is "the statement's value at REV when it equals the independent derivation, else
`UNSUPPORTED:` + the statement's value". The counter compares only `record['observed']`
(`tools/round-44/c2-counter.py:1253`:

```python
matched, reason = compare_values(record['observed'], entry['asserted'], entry['compare'])
```

and the string `derived` occurs in that file only in comments/help and in the
`repaired_by_rederived_value` label — it is never read from the check's stdout).

Six entries therefore pass whatever their derivation says. Their payload contains

```python
steered="steer" in marker.lower()
if steered:
    emit("steered","steered" if txt.strip() else "steered-declaration-absent", …)
    raise SystemExit(0)
```

so `observed` is the literal `"steered"` — equal to `asserted` — **and the `derived` field carries
the very disagreement the check found**. Entries (`tools/round-44/c2-rubric.json`):
`C2-g1-planned-r34-to-35` (`:4226`), `C2-g4-planned-r39-to-40` (`:4356`),
`C2-g5-planned-r40-to-41` (`:4400`), `C2-g6-planned-r41-to-42` (`:4444`),
`C2-g7-planned-r42-to-43` (`:4488`), `C2-g8-planned-r43-to-44` (`:4532`) — all six carry
`"expected": "superseded"` and `"asserted": "steered"`. A static scan of all 80 payloads for
`emit(<string-literal>, …)` whose literal equals `asserted` returns exactly these six.

**Falsification witness.** mut3 = a clone at `55bcce69` whose `## Round 35 — stopped on frozen
counter falsification` heading was renamed to `## Quarter 35 — …` (so the round-35 declaration the
entry claims to check is gone), committed as `c0742325ad891a7bab58a73b862d7d6d59784684`:

```
python3 -I -B tools/round-44/c2-counter.py --root . --rev c0742325… --freeze c0742325… \
        --work <SCRATCH>/w-m3 --json-out <SCRATCH>/mut3.json
→ exit 1 (other reds present), C2-g1 ABSENT from mismatches
  entry C2-g1: match TRUE · observed "steered" · derived "steered-declaration-absent"
  stdout: {"id":"C2-g1-planned-r34-to-35","observed":"steered","derived":"steered-declaration-absent",
           "detail":"planned row carries an explicit steer marker; next-round declaration not yet present at the freeze"}
```

The check *knew* the declaration was absent and the entry still passed. Its own note ("superseded by
the explicit steer marker; the round-35 declaration exists") is therefore half-unchecked, and the
fitness claim "every entry must be shown able to FAIL on its own statement" holds only for the
`steer`-marker half (which the rubric's `mutation_witness` does exercise).

This extends `w2/R44W2ScoutDebt.md` D-22 (which flags the `steer` hatch as "does not require the
marker to cite a resolving receipt path") with an executed green. It does **not** change the
`55bcce69` verdict: the three target entries and 71 others are unaffected, so `mismatches 0` stands.

**Fix direction (round 45, instrument):** have the counter compare the check's `derived` against
`asserted` when a check emits one (or reject `observed` that is a bare literal equal to `asserted`),
then re-score the frozen rubric as a *new* rubric — never by editing the round-44 bytes.

---

## 6. D-2 — the M44-2 preflight has no bound-edit arm: it false-reds the claim's own lawful append

**Severity: medium (the fix cannot be wired as R44-CL1 says without producing a false red on the
round's own landing).**

`tools/round-45/frozen-path-preflight.py` walks `FREEZE..REV` and flags **every** `M/D/R/T/U/A/C`
status on the pathspec (`tools/round-45/frozen-path-preflight.py:63-65`), then adds a tree-blob
backstop (`:67-79`). It has no
`expected_edit`/bounds concept, so it cannot express the one frozen path whose edit the rubric
*binds* (`SCORECARD.md`, `expected_edits.SCORECARD.md`, 8 exact lines).

```
python3 -I -B <LANE>/tools/round-45/frozen-path-preflight.py --root <clone> \
    --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
    --rev    55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac \
    --pathspec SCORECARD.md
→ exit 1 · verdict "frozen_path_changed" · touched [(M, SCORECARD.md)] · blob_changed ["SCORECARD.md"]
  stdout sha256 cfd07d85ba3e663bdd96d5c1ec728bb3fc58eabefac147c9a950d4c33b011359
```

At the same revision the C2 counter reports `SCORECARD.md bound_edit_applied appended_lines 8` and
overall exit 0. So the gate and the scorer disagree about the same bytes, and the gate is the one
that is wrong for this claim. The demonstrated green arm only avoids this because its pathspec is
`tools/round-44` — i.e. it omits every frozen file the claim edits. The lesson's R44-CL1 ("wire it
into the round's commit sequence before the next freeze") is therefore not yet actionable as
written; the record's live worktree amendment already adds the missing arms (dirty-tree, mandatory
pathspec, sweep placement) but not this one.

Positive results, for balance (all reproduced by me, stdout sha256 in
`artifacts/R44W2C2Rescore/preflight/`):

| case | rev | pathspec | exit | verdict | touched / blob_changed | stdout sha256 |
|---|---|---|---|---|---|---|
| green | `55bcce69` | `tools/round-44` | **0** | `clean` | 0 / 0 | `c8a03c26…0a870f` |
| red (M44-2) | `c86ea508` | `tools/round-44` | **1** | `frozen_path_changed` | 8 / 8 | `20a87d4d…a28896` |
| red (tip) | `8bb1090a` | `tools/round-44` | **1** | `frozen_path_changed` | 8 / 8 | `c302813c…8a1cdf99` |
| false red | `55bcce69` | `SCORECARD.md` | **1** | `frozen_path_changed` | 1 / 1 | `cfd07d85…011359` |

The first three match `w2/R44W2Preflight.md`'s table byte for byte, so the two seats agree
independently on the gate's behaviour.

---

## 7. D-3 — the recorded C1 cause is falsified; the stop is a withdrawal, not an impossibility

**Severity: medium (record accuracy). Being fixed in the uncommitted worktree; still wrong at
`8bb1090a`.**

Recorded at HEAD:

- `LOG.md:3201` — "…the four real receipts carry `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…/rea-out`, so no run can satisfy the whole f…"
- `SCORECARD.md:3525` — "…the frozen claim requires `parameters.output_directory` to name BOTH a committed `corpus/evidence/round-44/c1/` path and the `/kaidoku-r44/` scratch segment, so no real run can sat…"
- `corpus/lessons/round-44.md` (HEAD) `R44-CL2`, line 69 — "The frozen R44-C1 text is internally unsatisfiable on one field…"

What the instrument actually does:

1. `tools/round-44/c1-counter.py:1176-1182` — `provenance_ok()` requires only an **absolute** path
   **containing** `/kaidoku-r44/` and no `..`. It does not test for a `corpus/evidence/round-44/c1/`
   path. A path naming both clauses passes:
   `provenance_ok('/fast/scratch/hyaku/kaidoku-r44/rex/corpus/evidence/round-44/c1/v1le/rea-out')`
   → **True** (also `/kaidoku-r44/…/corpus/evidence/round-44/c1/v1le/rea-out` → True; the committed
   `…/rea-out` → True; a lane-absolute evidence path → False). The two clauses are co-satisfiable;
   only the frozen **runner** (`c1-run.py:329-345`, modes `evidence` and `scratch`) produces one
   clause at a time.
2. The red at `55bcce69` is **not** a provenance failure. My independent run:

```
python3 -I -B tools/round-44/c1-counter.py --root . --rev 55bcce69… --freeze c48f8a4… \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
    --work <SCRATCH>/w-c1 --json-out <SCRATCH>/c1-score.json
→ exit 1 · carriers_matched 4 · met_target false · frozen_path_changed []
  bindings_false ["province_core_section","province_core_row","frontier_note"]
  all 4 carrier records: matched true, run_provenance_ok true, projection_ok true, projection_diff []
  every binding, and every per-carrier field, identical to l1/c1-score-at-55bcce69.json
```

3. The same receipts, unchanged, scored **green** earlier in the same round. Re-running the same
   counter at the landing commit (the lane's own `corpus/evidence/round-44/c1/counter-at-4cc1.json`):

```
python3 -I -B tools/round-44/c1-counter.py --root . --rev 4cc1ac11… --freeze c48f8a4… --pkg65 … \
    --work <SCRATCH>/w-c1b --json-out <SCRATCH>/c1-at-4cc1.json
→ exit 0 · carriers_matched 4 · met_target true · bindings_false []
```

4. The flip between the two revisions is caused by the documents alone:
   `git diff --stat 4cc1ac11 55bcce69` over the frozen set → `PROVINCE.md` 6 lines,
   `corpus/README.md` 6 lines, `SCORECARD.md` (not C1-frozen), plus added receipts;
   `git diff --stat 4cc1ac11 55bcce69 -- corpus/evidence/round-44/c1/v1le corpus/evidence/round-44/c1/v1be
   corpus/evidence/round-44/c1/v2le corpus/evidence/round-44/c1/v2be` → **empty**. Commit `9d3d1862`
   rewrote `## Round-44 additions to Core` into `## Round-44 measured, not promoted (R44-C1 honest
   stop)` in `PROVINCE.md:424-425`, which is exactly what turns the three doc bindings false.

So: `carriers_matched 4`, every carrier binding true, `met_target false`, exit 1 at `55bcce69` —
**confirmed**. "The stop is the only correct reading of the frozen text" — **not established**: the
instrument was met at `4cc1ac11` and nothing about the receipts changed; the stop is a choice to
honour a prose clause the instrument does not implement (defensible, and the safer of the two
readings), not a contradiction forced by an unsatisfiable field. This is the same conclusion
`w2/R44W2C1Rescore.md` reaches by appending a PROVINCE landing to `55bcce69` (its D-2); my route is
independent (re-run at the commit where that landing existed) and adds the co-satisfying-path
demonstration.

The worktree amendment to the lesson already adds this qualifier ("the frozen counter implements
only the scratch clause … its red at `55bcce69` is the three withdrawn documentation bindings, not
provenance … a loophole, not a legitimate route"). That correction is right and should be committed;
until it is, the record at `8bb1090a` says the opposite.

---

## 8. D-4 (low) — `claim_score` reads `true` on an exit-2 receipt

`finalize()` sets `gate['claim_score'] = bool(result['claim_score'])`
(`tools/round-44/c2-counter.py:1052`) from the *pre-freeze* flag, not from the outcome, so the tip
receipt carries `"claim_score": true` at top level **and** in `claim_gate` while
`"usable_as_claim_score": false`, `exit_code 2`, `met_target false`. A reader who greps
`claim_score` gets "true" from a receipt that must not be used. The record is clean here (no line of
`LOG.md`, `corpus/lessons/round-44.md` or `SCORECARD.md` at `8bb1090a` contains `claim_score` —
3 × `grep -c` = 0), so this is a receipt-schema wart, not a record error. Fix: rename the field
(e.g. `claim_mode`) or derive it from `usable_as_claim_score`.

---

## 9. Attacks that did **not** land (so the verdict is not overstated)

- **Bound-append overrun is caught.** mut5 = `55bcce69` + one extra line appended after the bound
  block (commit `ef35b588…`), scored against the **real** freeze `c48f8a4`:
  `exit 2`, `frozen_path_changed ["SCORECARD.md"]`, `freeze_notes` `state
  bound_edit_violation, reason appended_block_differs_from_expected_edit`. The exact-bytes binding
  works.
- **The three repaired values really are the measured values.** mut2 restores the BASE assertions;
  arm C's `observed` values are `133/133`, `20/20`, `81-449`.
- **Target entries do not silently score at REV.** `C2-a1/a2/a4` are `pin: HYAKU_FREEZE` /
  `__SCORING_REV__: FREEZE_TREE`; the record says so (`SCORECARD` correction paragraph) and the
  current-tree count (138/138 at `c86ea508`) is reported separately in the Owned-scores line. No
  contradiction found, though see §10 for the residual.
- **README/SOURCES are not frozen — confirmed, but already recorded.** mut6 (`4edfc6aa…`, an
  arbitrary unbound sentence appended to `corpus/README.md`) and mut7 (`d895a377…`, an unbound
  `corpus/SOURCES.md` append) both score `exit 0`, `met_target true`, `frozen_path_changed []`
  against the real freeze. This reproduces `w2/R44W2C2Freeze.md` F-1/F-2 (its R44-CL7) — the
  internal contradiction is between `plans/round-44-claims.md:60-62` (README "NOT byte-frozen")
  together with `:64` ("SOURCES.md IS byte-frozen") and the Separability sentence at
  `plans/round-44-claims.md:274` ("any additional change to either file reds
  `frozen_path_changed`"). Not renumbered here.
- **No evidence that the 80/80 at `55bcce69` depends on the tip commit.** The measured tree is
  `55bcce69`; nothing in `c86ea508..8bb1090a` is read by the score.

---

## 10. Residual risk and verification gaps

- **Fitness sampling.** I re-executed five entries end to end (`a1`, `a2`, `a4`, `c01`, `g1`) and
  the selftest; the rubric's `fitness.fails_as_required 80` / `not_demonstrated []` is a *declared*
  measurement whose harness (`w1/artifacts/R44C2Rubric/…/mutation-witness.json`) I did not rebuild.
  D-1 is a counter-example to the spirit of that gate for six entries (they fail on one conjunct
  only), even though each has a passing witness.
- **C1 provenance is still unproven** (carried R44-CL3/D-13): my run re-derives the projection of
  each receipt with a live REA 6.5.0 run on this host, which shows the receipts are reproducible
  from the bytes, not that the committed receipt was written by that process.
- **Host-state dependence.** My C1 run used the same `--pkg65`
  (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, 6.5.0) and the same
  `/usr/bin/unsquashfs` (4.7.5, sha256 `461e1fd9…` frozen in `carriers.json`) as the lane's receipt;
  a different package/tool build would be a different measurement.
- **The record moved under the seat.** My record findings are pinned to `8bb1090a`; the worktree
  carries uncommitted amendments at 11:26–11:27 that answer D-3 and re-state R44-CL1/R44-CL7. A
  reviewer must read the committed bytes, not the worktree, or re-pin the hash.
- **`claim_gate.claim_score`** (D-4) will keep reading `true` on every exit-2 receipt until the
  field is renamed, including the round's own tip receipts.

## 11. Receipts

`artifacts/R44W2C2Rescore/` (lane-relative `.ufo/waves/round-44/w2/artifacts/R44W2C2Rescore/`):
`receipts.json` (every run: exact command, exit code, stdout sha256, wall seconds),
`c2-at-55bcce69.summary.json`, `c2-at-tip.summary.json`, `c2-at-freeze.summary.json`,
`c2-at-fee6e98a.summary.json`, `mut1..mut7.summary.json` + `mut1..mut7.detail.json`,
`c1-at-55bcce69.summary.json`, `c1-at-4cc1ac11.summary.json`, `c2-selftest.txt`,
`preflight/{green-55bcce69-tools-round-44,red-c86ea508-tools-round-44,red-8bb1090a-tools-round-44,red-55bcce69-SCORECARD-md}.json`.

Fixture revisions (all throwaway, all inside this seat's scratch, all deleted with it):
`mut1 c967ce2e` (wrong note value), `mut2 be338c53` (block removed), `mut3 c0742325` (round-35
heading renamed), `mut4 0024b5a9` (capability pointer substituted), `mut5 ef35b588` (extra append
past the bound block), `mut6 4edfc6aa` (unbound README sentence), `mut7 d895a377` (unbound SOURCES
append). Arms 1–4 scored with `--freeze=<mutant>`; arms 5–7 scored against the real freeze
`c48f8a4`, so the freeze walk is live.

Scratch `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C2Rescore/` was removed at the end of the seat
(nothing cited above lives there; every receipt is in `artifacts/`).
