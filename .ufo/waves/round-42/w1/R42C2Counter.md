# R42C2Counter — the round-42 C2 counter (`c2-counter.py`), ported to v4 and amendment A1

**Verdict: DONE.** `c2-counter.py` is written, `--selftest` passes 79/79 (17 green, 62 red, 0 fail), and the
QUALITY-84 end-to-end dry run scores **96/96 envelopes with all 36 bindings evaluated and true** (counter exit 0)
on a sandbox clone whose freeze-like commit holds the counter plus this seat's stand-in drafts of the interpreter,
evaluator and generator. Nothing in the lane was written outside this report and
`.ufo/waves/round-42/w1/artifacts/R42C2Counter/`.

## Axes (godspeed)

1. **Coverage of the frozen predicate** — every sentence of `plans/round-42-claims.md` `## R42-C2` (A1) that names
   a check is a binding, and every binding is exercised at least once green and once red.
2. **Unflippability (R41-CL1 / round-41 w2 M05)** — the declared tuple is read from `declared_features` only, and
   a manifest that writes it anywhere else fails the binding closed and lists the carriers.
3. **Controls that bite** — the exact lookup control (CTL-C2-7) and the majority-fallback variant (CTL-C2-7b) are
   scored against the held-out combos; 7 is bound, 7b is reported.
4. **Freeze integrity / receipt honesty (D4)** — frozen paths, the writers and fixtures the frozen generator names,
   the SKILL v4 block at every touching commit, plus `counter_sha256` and `exit_code` in the receipt.

## Deliverable

| file | sha256 |
|---|---|
| `artifacts/R42C2Counter/c2-counter.py` (install as `tools/round-42/c2-counter.py`) | `c01573f5c921839a62f9fbba88ff0aa4075349d4a2794addd0512c4a61be542e` |
| `artifacts/R42C2Counter/dryrun.py` (rebuild command for the dry run) | `becb318b9f40e384183d62129a6837e3175444a3c67cf3dd9a4f4d7a2ad6d02c` |
| `artifacts/R42C2Counter/dryrun-receipt.json` (the dry-run receipt, 151 kB) | `2a6f962205db858862784338671050782bd6f631bf8c5c8682743c146693604a` |
| `artifacts/R42C2Counter/dryrun-summary.json` (its printed summary) | `c96460369f22808ab98751ebcee11f7174e213b292566707fcadb5e5b5d5687e` |
| `artifacts/R42C2Counter/selftest-summary.json` | `31455ebbe1e3934fbd36bcd0261ad1a82c71a0ee9722418d3e0269f7c20d3d39` |
| `artifacts/R42C2Counter/standin-sqfs-triage-v4.py` (dry-run stand-in, not the frozen interpreter) | `a7be44ca829f99a92441a5d93b00c5a3b292cfa24bdf0b0ffe7c363d094bf002` |
| `artifacts/R42C2Counter/standin-indep-eval-v4.py` (dry-run stand-in, not the frozen evaluator) | `e7cd79741ac9af19ded8ce4c87aa664a8ab5f04591b0929ee79e196aa8d72041` |
| `artifacts/R42C2Counter/standin-heldout-gen-v4.py` (dry-run stand-in, not the frozen generator) | `80370cd227a5a8d5ba967e7d0e2dfae501a329b12dc462127998806e4479d9c9` |
| `artifacts/R42C2Counter/standin-skill-block21.md` (13-column stand-in block 21) | `24837975348dd2dc5f6ea2a6896ec15e9c1551446f5aeaa37173de2e8055c667` |
| `artifacts/R42C2Counter/standin-controls.py` (writes CTL-C2-7 / CTL-C2-7b in the draft grammar) | `37a3c30b18453035ed3321e90641f138fdad3a03e9f631a80ccb7f0892ae71d1` |

The stand-ins exist only because QUALITY 84 demands a dry run before the freeze. The owning seats'
(`R42C2Interp`, `R42C2Eval`, `R42C2Gen`, `R42C2ControlTables`, `R42C2TableDraft`) drafts replace them byte for
byte at install; the counter **probes** every tool interface instead of assuming one, so a different (but
documented) CLI shape still works and the interface that answered is recorded in the receipt.

## Bindings (22 claim + 14 instrument)

Claim: `seed_matches_freeze`, `manifest_generator_path`, `generator_sha_matches_freeze`,
`writer_matches_manifest`, `regenerated_seed_matches_freeze`, `carriers_regenerated`, `carriers_committed`,
`envelopes_valid`, `manifest_after_freeze`, `manifest_before_envelopes`, `v4_block_present`,
`v4_block_identical`, `evaluator_covers_all`, `observed_features_match_declared`,
`legacy_chunks_not_no_squashfs`, `new_legacy_label_exercised`, `handler_families_exercised`,
`lookup_combo_below_half`, `lookup_control_identical`, `combo_unseen_majority`,
`real_receipts_depth_limited`, `legacy_dev_envelopes`.

Instrument: `classes_unique`, `classes_two_each`, `n_equals_twice_classes`, `combo_family_wellformed`,
`ids_unique`, `arms_valid`, `carrier_paths_unique`, `envelope_paths_unique`, `v4_block_columns`,
`v4_actions_declared`, `observed_actions_declared`, `decisions_reported`, `row_decisions_consistent`,
`bindings_complete`.

`bindings_complete` is the ledger check (`bindings_undeclared == []` and `bindings_declared_unset == []`), so a
binding added to the code but not to the ledger (or the reverse) cannot pass silently. Target:
`matched == n` **and** every binding true; exit 0/1/2 as round 41 (`met_target` / not met / unevaluable, the
last carrying `frozen_path_changed`, `no_manifest_at_rev`, `generator_failed`, `evaluator_*`,
`interpreter_*`, `met_target_inconsistent`).

## Round-42 changes and the A1 delta

- **R41-CL1.** `declared_features` is the ONLY declared-tuple key: `declared_features()` reads
  `carriers[].declared_features` and returns `None` for everything else — no `declared`, no `features`, no
  `class_expected.features`, no manifest-level map. Missing key ⇒ binding false, carrier listed in
  `declared_features.missing`. Red cases cover all three wrong placements.
- **R41-CL4.** `legacy_chunks_not_no_squashfs`: no envelope whose declared handler set holds a v1–v3 handler may
  be labelled `no-squashfs-chunk` by either side, and the table's `no-squashfs-chunk` row must carry handler
  `none`. (A1 step 3 keeps the row; step 2 steals the depth-limited case into `container-depth-limited`.)
- **A1 (L1 amendment, 15 steps).** `observed_features` now unions `chunks[].handler` with
  `extraction_gaps[].handler` for H and derives F/L/HF; `handler_families_exercised` filters F; the stand-in
  table/evaluator implement the 15 steps (container-depth-limited at step 2, unknown-residue at step 9 before
  depth-limited, legacy-body-failure by HF∩L at step 7, dependency step by membership at step 4).
- **A1 grammar (L1 decision, 2026-10-26).** 13 columns: `failing handler` right after `handler`; `handler` globs
  over F (`none` = F empty), `failing handler` globs over HF (`*` = anything, including an empty HF), and
  `dependencies` accepts the contains form `name+`. `COLUMNS` now requires `failing handler`, so a table without
  it fails `v4_block_columns`.
- **`combo_unseen_majority`.** ≥ ceil(n_combo/2) combos have an observed tuple outside the union of the frozen dev
  arm's named-class declared tuples. Source order: `<dev>/manifest.json` `carriers[].declared_features` (the
  generator writes one), then `<dev>/*/envelope.json` `declared_features`; both empty ⇒ binding false.
- **`lookup_combo_below_half`.** The frozen CTL-C2-7 run through the frozen interpreter must *answer* (a refused
  or crashed control scores 0 but the binding is false — hardened after the first dry run found the vacuous-true
  hole) and `score * 2 < n_combo`.
- **CTL-C2-7b** is scored (`lookup_7b.score`, `below_half`) with `binding: False` — reported, never a veto.
  Both control tables are in the frozen-path set.
- **D4.** The receipt carries `counter_sha256` (at REV), `counter_sha256_at_freeze`, `counter_path`,
  `exit_code`, `frozen_units` (8 units), `frozen_paths_changed`, and per-attempt interface/exit records.

## Evidence (exact commands, outputs, exit codes)

Scratch: `S=/fast/scratch/hyaku/kaidoku-r42/R42C2Counter` (removed at the end; nothing cited lives there).

1. **Selftest** (`HYAKU_SCRATCH=$S/hs TMPDIR=$S python3 -I -B <artifacts>/c2-counter.py --selftest`), 74 s:
   `{"selftest": "c2-counter r42 (v4)", "cases": 79, "green": 17, "red": 62, "pass": 79, "fail": 0,
   "failures": []}` / `SELFTEST cases=79 pass=79 fail=0`, exit 0 (`selftest-summary.json`).
   Required red cases present and passing: **key `declared` only** (binding false, `declared_features.missing`
   non-empty — the round-41 w2 M05 mutant is now killed), key `features` only, table changed after the freeze
   (exit 2 `frozen_path_changed`), lookup table at full score (`lookup_combo_below_half` false), lookup table the
   interpreter refuses (false), v3 marker only, mutated-then-restored block, evidence rewritten, writer touched
   but unnamed (exit 0), real receipt missing/mislabelled/evaluator-disagrees, dev arm absent/short/disagreeing,
   v1–v3 class labelled `no-squashfs-chunk`, `no-squashfs-chunk` row handler not `none`, legacy-failure row
   absent, evaluator never exercises `legacy-body-failure`, v1/v2 handlers absent, catch-all table, block without
   the action column, two carriers sharing a path, generator sha wrong, writer outside the freeze tree.
2. **End-to-end dry run** (`TMPDIR=$S HYAKU_SCRATCH=$S python3 -I -B <artifacts>/dryrun.py --lane
   /home/vgpnk/Projects/shokunin/kaidoku-shokunin --artifacts <artifacts> --scratch $S/dry`), 7 s, exit 0:
   freeze-like commit `7740be1a212a44f7b3b00c46bac5a338ac89443f`, measured revision
   `ede13bdd25f4267ce73543536822c534bc094642`; generator draft wrote 96 held-out carriers (36 named classes × 2 +
   24 combos) and 7 dev carriers, both arms `--verify` byte-identical (`n_diffs 0`); the counter ran
   `--rev … --freeze … --json-out dryrun-receipt.json` and returned **exit 0**, `n 96`, `matched 96`
   (`matched_classes 72`, `matched_combos 24`), `bindings_evaluated 36`, `bindings_declared 36`,
   `bindings_missing []`, `bindings_extra []`, `bindings_undecided []`, `bindings_false []`,
   `met_target true`, `counter_sha256 == counter_sha256_at_freeze ==
   c01573f5c921839a62f9fbba88ff0aa4075349d4a2794addd0512c4a61be542e`; `frozen_paths_changed []`,
   `skill_block_commits_scanned 0`, `bindings_undeclared []`, `bindings_declared_unset []`.
   Every binding's value in that receipt (all `true`): see `dryrun-summary.json.bindings`, reproduced by category
   above.
3. **Controls on the dry run.** CTL-C2-7 (16 rows, exact named-class tuples, v4 marker): `score 0`, `half 12.0`,
   `identical_to_freeze true`, interpreter answered `json/json+table_only`, `missing_expected []`.
   CTL-C2-7b (same rows minus the majority row plus a `*` fallback row): `score 0`, `below_half true`,
   `binding false`.
4. **Real receipts.** `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json` → interpreter and evaluator both
   `depth-limited`/`raise-depth`, 4/4 `ok`, `missing []`.
5. **Dev arm.** `corpus/evidence/round-42/c2/dev`, 7 envelopes, legacy handler seen; rows: D01–D04 `clean`,
   D05 `legacy-body-failure/cross-read-legacy`, D06 `dep-missing-le/install-extractor-le`,
   D07 `partial-body-failure/salvage-partial`; interpreter and evaluator agree on every row.
6. **Combo calibration.** `combo_unseen_majority`: 24/24 combos outside the 7 dev named-class tuples,
   `need 12`; source recorded as `<dev>/manifest.json (carriers[].declared_features)`.
7. **Family and label coverage in the dry run.** 16 distinct decisions, one row per precedence branch; 43 legacy
   carriers carry a v1–v3 handler and none is `no-squashfs-chunk` (row handler cell `none`); handler families seen
   `squashfs_v1/v2/v3/v3_be/v3_broadcom/v3_ddwrt/v4_be/v4_le` plus `trx_v1` (container); declared-tuple mismatch
   `[]`, missing `[]`; v4 block 3930 bytes at REV == freeze.
8. **Inert on the unfrozen lane** (`--root LANE --rev c4a38ea2… --freeze c4a38ea2…`): exit 2,
   `{"unevaluable": "no_manifest_at_rev", …}` — the counter cannot mint a score before the freeze.
9. **Stand-in cross-checks** (they are not the frozen tools, but they show the dry run is not self-fulfilling):
   evaluator `--selftest` 18/18 hand-built envelopes across all 15 steps; generator `--selftest` green (36 named
   classes, 24 combos, ≥2 factors each, no forbidden manifest key); interpreter vs evaluator agree on 96/96
   held-out and 7/7 dev envelopes.

## Findings and freeze-time risks (calibration)

1. **R41-CL1 is now structurally dead.** The `declared`-only selftest case fails the binding and lists every
   carrier; no lookup fallback exists in the code path. [INFERENCE] A future manifest that documents another key
   in `declared_schema` cannot flip the claim — it fails closed instead, which is the honest direction.
2. **The 13-column grammar is now a scoring dependency.** `COLUMNS` requires `failing handler`. If the frozen
   block drops it (or the table draft keeps the 12-column shape), `v4_block_columns` is false and the target is
   unreachable. The table draft must carry the column exactly as the L1 decided.
3. **The dev arm must commit its manifest.** `combo_unseen_majority` needs the dev arm's named-class
   `declared_features`; the counter prefers `<dev>/manifest.json` and only falls back to per-envelope
   `declared_features`. A dev arm committed as envelopes alone without that key fails closed. The dev directory
   is discovered at `corpus/evidence/round-42/c2/dev` first, then `.ufo/waves/round-42/controls/c2/dev`; the
   receipt names which one was used, so the L1 must commit exactly one of them (otherwise the binding reads the
   first that exists).
4. **Control tables must be v4-marked, exact and duplicate-label-free.** Both are frozen paths
   (`.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md`, `…CTL-C2-7b-lookup-fallback.md`); a lookup table the
   frozen interpreter refuses now scores 0 **and** fails the binding (no vacuous pass), and a table committed
   outside those two paths gets no freeze protection (no false failure, but no drift detection either).
5. **The dry run proves plumbing, not data.** The carriers are synthetic stand-ins; the frozen run must use the
   owning seats' generator on the pinned unblob fixtures, and the interpreter/evaluator must be the frozen bytes.
   The dry run's 96/96 is evidence that every binding can be satisfied and is evaluated — not evidence that the
   real held-out set will pass.
6. **Combo reachability is the real depth question.** The dry run's combos are factor draws in the generator
   draft; `R42C2ReconCombo` owns whether those tuples are *reachable* on real REA envelopes. If they are not, the
   generator must not claim them — the counter will report the pair misses class by class
   (`pair_mismatches`), so the failure is legible rather than silent.
7. **`n_equals_twice_classes` + `combo_count`.** Exactly two carriers per named class and `combo_count` equal to
   the actual combo count; a third replicate or a stub `combo` missing one envelope fails the instrument, by
   design (the round-41 shape).
8. **No tooling changed.** No install, upgrade, pacman/uv/npx transaction, and no write into `~/.local/bin` or any
   PATH directory; the only executables used were `python3` (stdlib), `git` (read-only in the lane) and `sha256sum`.

## What the L1 still owns

1. Install the four tools at `tools/round-42/{c2-counter.py,sqfs-triage-v4.py,indep-eval-v4.py,heldout-gen-v4.py}`
   from the owning seats' bytes (the stand-ins here are scaffolds only).
2. Freeze `plans/round-42-claims.md`, the `tools/round-42` subtree, `corpus/evidence/round-42/c2/heldout`, the two
   control tables, the writers the frozen generator names and any in-lane fixture it pins.
3. Commit the dev arm (manifest + envelopes) and the held-out arm (after the freeze), then score at REV with
   `c2-counter.py --root LANE --rev REV --freeze FREEZE --json-out …`; the receipt is the score.

## A1 delta (recorded because the amendment landed mid-build)

The counter, the stand-in table/evaluator/generator and the selftest were built against the first draft and then
re-cut for A1 in the same wave: 15-step precedence, `container-depth-limited` and `unknown-residue` rows,
H = chunks ∪ gap handlers, HF for the failure rows, the 13th `failing handler` column, `combo_unseen_majority`,
the hardened `lookup_combo_below_half`, the reported-only `lookup_7b`, and eight new selftest cases (declared-key
variants, lookup-at-full-score, refused lookup, no/short/disagreeing dev arm, legacy-family and container/residue
coverage). The dry run and the selftest numbers above are post-A1.
