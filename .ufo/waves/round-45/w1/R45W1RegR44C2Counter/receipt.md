# Receipt — `tools/round-44/c2-counter.py` at the round-45 freeze

Seat `R45W1RegR44C2Counter`, lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
UTC window 2026-10-28T15:41:46Z–15:43:46Z. Read-only on the lane tree; every write below is
under this seat directory or the scratch root `/fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C2Counter`
(removed before yield). Scratch receipts were copied into `receipts/` **before** removal.

Lane HEAD at measurement: `faa875bc0eb839d15b83c4afa6078819e5a7b381` (untracked `.ufo/` only;
`git status --porcelain` showed no modified tracked file). Freeze: `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`.

## Frozen bytes verified first

| path | sha256 at `f762b72` (via `git show`) | sha256 of the worktree file | equal |
|---|---|---|---|
| `tools/round-44/c2-counter.py` | `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277` | same | yes |
| `tools/round-44/c2-rubric.json` | `e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e` | same | yes |

Command: `sha256sum tools/round-44/{c2-counter.py,c2-rubric.json}` and
`git show f762b72:<path> | sha256sum`; both pairs agree. `git diff --stat f762b72 -- tools/round-44 plans/round-44-claims.md`
printed nothing (exit 0). `085192ea…` is also the `counter_sha256_at_freeze` recorded inside the
instrument's own selftest output, so counter identity is consistent across three independent records.

## Commands (exact argv, exit code, stdout sha256, UTC)

`python3` is `/usr/lib/python3.14`. `TMPDIR` and `HYAKU_SCRATCH` both pointed at the scratch root.

| # | command | UTC | exit | stdout sha256 |
|---|---|---|---|---|
| 1 | `python3 -I -B tools/round-44/c2-counter.py --selftest` | 15:41:46Z | 0 | `a5e942a1efa3172ba522a2174c68f62f80b01c009f9495027d4bbfde7558fbc3` |
| 2 | `python3 -I -B tools/round-44/c2-counter.py --root <lane> --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --work <scratch>/wa --json-out <scratch>/rc-55.json` | 15:41:47Z | 0 | `dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3` |
| 3 | same with `--rev c48f8a4bfd449300c975668e59aae5b5538b6a84` (`--freeze` the same) | 15:41:57Z | 1 | `e53d0d1df63a17970efd9872bb988c4e0388e6f5822fbc2b0be5e8642237a34d` |
| 4 | same with `--rev f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | 15:42:04Z | 2 | `b4563607d70bc5e2a208f6f15a0e56ec8bf50974ff2be76725949b282ec32513` |
| 5 | `python3 -I -B tools/round-44/c2-counter.py --help` | 15:42:04Z | 0 | `fadef8d76dc280c2916d232db43953808569375418edf3ff00c1a007f978c48f` |
| 6 | rubric introspection through the counter's own `parse_rubric` (importlib, read-only) | 15:42Z | 0 | `8da0f64cc2223762c3f57cae74bd404eed1d25775ce0426dc1ac98e41d1ac5e2` |
| 7 | `python3 -I -B restore_probe.py` (fixture: plain frozen path, touch → commit → restore → commit) | 15:42:25Z | 0 | `d2674c4f8319a45e9f783d6260651e8e99a8f828fffa291bd1e2bb584a9619d2` |
| 8 | `python3 -I -B restore_bound_probe.py` (fixture: `expected_edit`-bound path, append → commit → restore → commit) | 15:43:23Z | 0 | `ba165e6673f82f67cf6b9c68e5a583da8e92ae5f2ca23907bbdeebc6555f8524` |
| 9 | draft row parsed with `tools/round-45/c2-counter.py` `parse_rows`/`exits_ok` | 15:43:46Z | 0 | `receipts/row-final.txt` |

Machine table: `receipts/receipt.tsv`.

## 1 — `--selftest`: exit 0, 24 arms, every arm `ok`

`{"selftest": "P44-C2", "ok": true, "arms": [ … ]}` — 24 arms, `expected_exit == exit_code`
for all 24 (`receipts/selftest.json`). The stdout is byte-identical to the round-44 L1's
committed receipt `.ufo/waves/round-44/l1/selftest-c2-counter.txt`
(sha256 `a5e942a1…` both), i.e. the selftest is deterministic across hosts and runs.

| # | arm | expected | got | red clause it pins |
|---|---|---|---|---|
| 1 | `clean` | 0 | 0 | green baseline |
| 2 | `seeded_mismatch_reality` | 1 | 1 | mismatch on the observed side |
| 3 | `seeded_mismatch_claim` | 1 | 1 | mismatch on the asserted side |
| 4 | `missing_command` | 2 | 2 | malformed rubric (`entry_0_missing_command`) |
| 5 | `claim_run_clean` | 0 | 0 | `claim_gate.usable_as_claim_score == true` |
| 6 | `claim_run_mismatch_gate` | 1 | 1 | a failing run cannot be a claim score |
| 7 | `rubric_edited_after_freeze` | 2 | 2 | rubric byte-compare → `frozen_path_changed` |
| 8 | `bound_append_repair` | 0 | 0 | `expected_edit` append binds the repair |
| 9 | `unbound_append` | 2 | 2 | an append without a bound edit |
| 10 | `note_alone_does_not_repair` | 1 | 1 | a note is never evidence |
| 11 | `note_with_rederived_value` | 0 | 0 | repair only through re-derivation |
| 12 | `empty_rubric` | 2 | 2 | `no_evaluable_entries` |
| 13 | `frozen_dir_changed` | 2 | 2 | file edited under `frozen_dirs` |
| 14 | `frozen_dir_added` | 2 | 2 | file added under `frozen_dirs` |
| 15 | `weak_expected_edit` | 2 | 2 | `expected_edit_binds_no_content` |
| 16 | `bound_row_insertion` | 0 | 0 | mid-file insert bound by anchor line |
| 17 | `unbound_row_insertion` | 2 | 2 | the same insert without a bound clause |
| 18 | `uppercase_placeholders` | 0 | 0 | `{REV}`-style substitution |
| 19 | `script_pin_mismatch` | 2 | 2 | declared script digest mismatch |
| 20 | `inline_pin_match` | 0 | 0 | inline payload digest pin (match) |
| 21 | `inline_pin_mismatch` | 2 | 2 | inline payload digest pin (mismatch) |
| 22 | `self_referential_check` | 2 | 2 | a check that reads the rubric is refused |
| 23 | `pre_freeze_with_declared_freeze` | 1 | 1 | census with a declared freeze |
| 24 | `pre_freeze_census` | 1 | 1 | census reports the mismatch |

Fixture repos are created under `$HYAKU_SCRATCH/kaidoku-r44`; each sets its own
`user.email`/`user.name` locally before the first commit (no throwaway identity is used
anywhere else, and no fixture lands in the lane tree).

## 2 — exit 0 reproduced on real bytes (`--rev 55bcce69`)

`--rev 55bcce69` (the revision the round-44 L1 recorded) with `--freeze c48f8a4`:
`exit 0`, `met_target true`, `entries_evaluated 80`, `mismatches []`, `unevaluable []`,
`frozen_path_changed []`, `rubric_source "freeze"`, `exported_path_count 3204`,
`claim_gate.usable_as_claim_score true`. All six fields compared against
`.ufo/waves/round-44/l1/c2-score-at-55bcce69.json` (sha256 `1c55af14…`): identical, including
`rubric_sha256_at_freeze e8cc0ded…`. The three `## Owned axes` corrections are accepted through
`freeze_notes` state `bound_edit_applied` on `SCORECARD.md` (the only bound edit in the rubric).

## 3 — exit 1 do-nothing control on real bytes (`--rev c48f8a4`, the freeze itself)

`exit 1`, `met_target false`, `entries_evaluated 80`, `mismatches
['C2-a1-owned-coverage-count', 'C2-a2-owned-depth-count', 'C2-a4-owned-depth-craft-range']`,
`frozen_path_changed []`. Exactly the three target mismatches the claim repairs, i.e. the
"before" is measurable and names its entries. Nothing was touched to obtain it.

## 4 — exit 2 `frozen_path_changed` on real bytes (`--rev f762b72`)

`exit 2`, `met_target false`, `entries_evaluated 0`, `unevaluable [{id: null, reason:
frozen_path_changed, paths: […8…]}]`, `freeze_notes` states `{bound_edit_applied,
changed_under_frozen_dir, unchanged}`, `ancestor_ok true`. The eight paths are the
`tools/round-44/control-fixtures/{c3,pos}/…` files, i.e. the round-44 directory freeze binds
the control fixtures that later waves rewrote. The set is **identical** to the one the round-44
L1 recorded at `--rev 923fa87` (`.ufo/waves/round-44/l1/c2-score-at-final-tip.json`,
sha256 `de0a7e65…`): `sorted(mine) == sorted(recorded)` → `True`, exit codes and `met_target`
also equal.

## 5 — the `frozen_path_changed` path read from source

`freeze_integrity()` (`tools/round-44/c2-counter.py:641-712`) walks two ways and unions them:

- `changed_paths()` → `git log --pretty=format: --name-only --no-renames` **and**
  `git log --diff-merges=first-parent --pretty=format: --name-only --no-renames` over
  `FREEZE..REV` (the round-43 merge-aware walk).
- per frozen path, `path_status_changes()` → `git log --diff-merges=first-parent --no-renames
  --name-status --format=%x01%H FREEZE..REV -- <path>`; `M/D/T/R/U` change, `A` changes when the
  path existed at FREEZE.
- `frozen_dirs`: every path under the prefix that appears in the union walk that existed at
  FREEZE is `changed` whether or not the blob still matches (`changed_under_frozen_dir`,
  `added_under_frozen_dir`, `touched_under_frozen_dir` all red).
- plain frozen path (`edit is None`): blob inequality → `blob_changed`; blob equality **but**
  the path appeared in the walk → `touched_after_freeze` → still red.
- `expected_edit`-bound path: `verify_expected_edit()` (append byte-for-byte / append line
  identity / anchored insert, plus `preserve` digests, `marker`). Any violation →
  `bound_edit_violation` and exit 2.
- rubric self-check: the blob at FREEZE must equal the blob at REV, else `rubric_changed`.
- `finalize()` sets `met_target` from the conjunction and `claim_gate.usable_as_claim_score`
  only when `claim_score and rubric_source == 'freeze' and counter_sha256_at_freeze and
  rubric_sha256_at_freeze and exit_code == 0 and met_target and not frozen_path_changed and
  not unevaluable`. A changed frozen path is therefore exit 2 with **no** `met_target`.

## 6 — the rubric binding read from source

`parse_rubric()` (`:330-495`) returns `(doc, entries, frozen_spec, declared, frozen_dirs,
malformed)`; `score()` refuses to proceed (`Unevaluable`, exit 2) on any of: missing entry
list, entry without a string `check`, entry without `command`, entry without `asserted`,
duplicate id, empty `repair_command`, an `expected_edit` that is not an object, an
`expected_edit` binding no content (marker/preserve alone is refused). Rubric objects are read
from the **freeze blob** by default (`show(root, freeze, RUBRIC_PATH)`), and only
`--rubric` / `--pre-freeze` can change that; `rubric_source` is recorded, and any source other
than `freeze` makes `claim_score` false, so `--rubric` runs can never be a claim score.

`frozen_spec` for the shipped rubric (measured with the counter's own parser):

```
frozen_spec    ['SCORECARD.md', 'SHONEN.md', 'SKILL.md',
                'tools/round-44/c2-counter.py', 'tools/round-44/c2-rubric.json']
edit_bound     ['SCORECARD.md']            # the only expected_edit
declared       ['SCORECARD.md', 'SHONEN.md', 'SKILL.md']
frozen_dirs    ['tools/round-44']
entries        80   checks {'json'}   repair_commands 0
claims_file_in_frozen_spec False   claims_file_in_surface False
malformed      None
```

Entry subjects: `SCORECARD.md` 55, `SHONEN.md` 22, `corpus/README.md` 3
(`C2-h1/h2/h3`). Runtime export surface (`C2_DEFAULT_SURFACE` ∩ repo + rubric
`export_paths`): `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `SKILL.md`, `LOG.md`,
`MANIFEST.json`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*`,
`corpus/lessons/*`, `corpus/evidence/*.json`. `plans/round-44-claims.md` is **not** frozen and
not exported by this counter: `grep -n 'plans/round-44-claims.md' tools/round-44/c2-counter.py`
→ `4:` (docstring) and `129:` (comment); `tools/round-44/c1-counter.py:273` is where the
claims file is pinned.

## 7 — restore arms (fixtures)

| arm | seq | exit | `frozen_path_changed` | `freeze_notes` for the path | verdict |
|---|---|---|---|---|---|
| plain frozen path, `restore_probe.py` | freeze → touch (`claim: 9`) → restore (`claim: 3`) | 2 | `['doc.md']` | `touched_after_freeze` | restore does **not** un-block ✔ |
| plain frozen path, at the freeze / touched alone | — | 0 / 2 | `[]` / `['doc.md']` | `unchanged` / `blob_changed` | ✔ |
| `expected_edit`-bound path, `restore_bound_probe.py` | freeze → bound append → restore to freeze bytes | **0**, `met_target true` | `[]` | **`unchanged`** (reason `bound_edit` only on the append arm) | restore **is** indistinguishable from never-left ✘ |

`restored_blob_equals_freeze == true` in both fixtures (asserted on `git show <rev>:doc.md`).
Row 3 is the measured confirmation of the open item R44-CL10
(`corpus/lessons/round-44.md`, "C2's bound-edit freeze arm … does not implement the claim's
'a later restore does not un-block'"), on the exact arm that carries the round-44 repair:
`expected_edit` short-circuits to `unchanged` when `rev_bytes == freeze_bytes`
(`tools/round-44/c2-counter.py:704-707`) without consulting the walk. Both fixture repos were
`git rev-parse --show-toplevel`-verified to equal their own scratch dir before the first commit.

## Findings

- **F1 (row correction, pinned-value path).** The counter freezes 5 paths + 1 directory; it
  never freezes `plans/round-44-claims.md`. The claims file is pinned by the C1 counter.
  Evidence: §6, and `git show f762b72:plans/round-44-claims.md` is untouched by this counter's
  walk (`frozen_path_changed` at `--rev c48f8a4` is `[]` while `plans/round-44-claims.md`
  exists at both revisions — the path is simply not in `frozen_spec`).
- **F2 (row correction, selftest cell).** 24 arms, all green; the landed row omits the count.
- **F3 (instrument defect, calibration).** The **stdout summary** prints
  `claim_gate.usable_as_claim_score: true` on exit 1 and exit 2 runs, because `main()` builds
  the summary's gate from `claim_score ∧ rubric_source ∧ both digests` only, dropping
  `exit_code`, `met_target`, `frozen_path_changed` and `unevaluable`
  (`tools/round-44/c2-counter.py:1695-1705`). The `--json-out` receipt computed by
  `finalize()` is correct (`False` on both). Measured: exit-1 run stdout says `true`
  (`score-c48f8a4-freeze.out`), exit-2 run stdout says `true`
  (`score-f762b72-r45freeze.out`), while both receipts say `false`. Anyone quoting the printed
  summary as a verdict can record a false claim score; only `--json-out` is authoritative.
- **F4 (freeze design, carry to R45).** At the round-45 freeze the instrument is exit 2 on the
  eight `tools/round-44/control-fixtures/**` paths. A directory freeze over a `tools/` dir that
  holds control fixtures is invalidated by the next wave's control rewrite — the R44-C2 score
  is only admissible inside `c48f8a4..<first control-fixture rewrite>`. R45's frozen set is
  `plans/round-45-claims.md` + `tools/round-45/` (directory): it is safe only while no wave
  writes a control fixture or dev input under `tools/round-45/` — wave-2 falsification inputs
  must land under `.ufo/waves/round-45/` (as the claims file already requires of the control
  receipts).
- **F5 (disclosed limit).** A `C2_DEFAULT_FROZEN` path that is **absent at the freeze** and
  appears later is recorded `absent_at_freeze` and is **not** a change (fixture §7, where
  `SCORECARD.md`/`SHONEN.md`/`SKILL.md` do not exist). Inert for this lane (all three exist at
  `c48f8a4`) but the default list is not existence-strict. `frozen_dirs` has no such hole
  (`added_under_frozen_dir` reds).
- **F6 (honest scope).** The shipped rubric carries **no** `repair_command`, so in this rubric
  the "note is never evidence" machinery is only exercised by selftest arms 10/11; the three
  repairs are accepted solely through `SCORECARD.md`'s bound append. Stated so the row is not
  read as claiming a re-derivation path is in use.

## Not run

- The full 80-entry per-check records are cited but not committed (each `--json-out` is ~750 KB);
  the two big receipts are represented by key-projected copies
  (`receipts/score-55bcce69.exit0.projection.json`,
  `receipts/score-c48f8a4.exit1.projection.json`) whose `_projection_of` and the digests above
  bind them to the originals. The exit-2 receipt is small and committed whole.
- `tools/round-45/c2-counter.py` was exercised only as a library (`parse_rows`/`exits_ok`) to
  validate the draft row; its own score was not run (out of scope for this seat, and its
  do-nothing control is already committed at `.ufo/waves/round-45/controls/ctl-c2-0-do-nothing.json`).
- No install or upgrade was needed or performed.
