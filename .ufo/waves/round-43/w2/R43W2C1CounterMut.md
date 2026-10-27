# R43W2C1CounterMut — C1 counter mutation probe

**Verdict: INCONCLUSIVE for the four real-data mutants; positive supporting evidence from the counter selftest.** The pristine frozen score passes. Each actual mutant was rejected before scoring its intended binding because the counter correctly stops at `frozen_path_changed` for a post-freeze rewrite of the held-out subtree. Therefore none of those four results is counted as a killed mutant. The committed source independently shows that observed features and tuple-check consistency are computed against envelope bytes, not accepted from `generator.tuple_check`; see evidence below.

## Scope and measured revision

Read the frozen plan first: `plans/round-43-claims.md` (sha256 `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`). The scored receipt is at revision **77d196c66f4fea00d7d543728b190ebdfaf6d0f0**; current lane tip observed during this probe was **5856614ac4bf7f2363bbcd1956644474a82108e5**. The mutations were scored at their own scratch revisions listed below, all descending from the freeze `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`.

Key read inputs and hashes:

- `tools/round-43/c1-counter.py` — `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`
- `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` — `13a495dbb6862d6cfbdd1f41e4a09460740f86bf93e8bb08e313b06d92b8a55c`
- `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-4.json` — `ed41a5e1da2b20cfc006d1c4dd8dc855a954646807b1871880c5e5327b919` (hash output as recorded; report does not rely on this receipt's summary alone)
- held-out `manifest.json` — `980eafa59ca3890bf45945a02a6e608da511435d972d1ec978a38fd068ef2555`
- held-out `H01/run.json` — `14f518ec034b559f613b4cd3d2d1e30fce17a02359173f151ecc92ade2424a51`

## Detector runs and outputs

The scratch location was `/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C1CounterMut/`. Five independent `git clone --shared` scratch copies were checked out at the scored revision; before any scratch commits, `git rev-parse --show-toplevel` returned the exact corresponding scratch directory for each. No lane data was edited.

Pristine detector command (exit **0**):

`python3 -I -B <lane>/tools/round-43/c1-counter.py --root <scratch>/pristine --rev 77d196c66f4fea00d7d543728b190ebdfaf6d0f0 --freeze f3f8db389416d094b1ddeb1215ddcf914bfc0d1c --scratch <scratch>/pristine-scratch --json-out <scratch>/pristine-out.json`

Actual stdout: `{"bindings_false": [], "counter_sha256": "3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79", "distinct_decisions": 16, "exit_code": 0, "freeze": "f3f8db389416d094b1ddeb1215ddcf914bfc0d1c", "matched": 78, "matched_classes": 54, "matched_combos": 24, "met_target": true, "met_target_consistent": true, "n": 78, "revision": "77d196c66f4fea00d7d543728b190ebdfaf6d0f0"}`

One mutation per separate scratch copy, then a commit in that clone so `git show` reads the changed committed bytes:

| Case | Mutation | Scratch revision | Mutated file sha256 (before = pristine lane hash above) | Counter output / exit | Verdict |
|---|---|---|---|---|---|
| features | `manifest.json` H01 `declared_features.published`: `nonzero` → `zero` | `2417ba286a168c4da4d7dc9c2caa94890967e6c7` | `b099eb8b517e7ad670c182cb4e09a07a7644f8ec7620d3615570fab9aed49dbc` | exit 2; `frozen_paths_changed:["corpus/evidence/round-43/c1/heldout"]`, `unevaluable:"frozen_path_changed"` | Inconclusive; intended `observed_features_match_declared` never evaluated |
| extras | `manifest.json` H01 `declared_extras.max_depth`: `3` → `99` | `b134b7e21f106c0aa1c6e46363fb83208bc7d61d` | `45adad562fc36785823f704e131715bf28d1d87d5b55bcfe7cb0fd3150747feb` | exit 2; same `frozen_path_changed` output | Inconclusive; intended `declared_extras_match` never evaluated |
| handlers | H01 `run.json.handlers` → `["forged-handler"]` | `fafaa4060696de5683a0499980c764521e7d0579` | `321d3ba25e57fbe3af9e9c630364742a4aed9e7c315cacf760912387db95b997` | exit 2; same `frozen_path_changed` output | Inconclusive; intended `runjson_digests` never evaluated |
| subject digest | H01 `run.json.subject_sha256` → 64 zeroes | `6b23a2177365f57e1e3c5f703290f07c123b93ab` | `938217dbba609e4fa3730e2d60d98437d8299aba526b0144e98e713444fab43a` | exit 2; same `frozen_path_changed` output | Inconclusive; intended `runjson_digests` never evaluated |

Each was run using the same counter command shape with that scratch revision and isolated `--scratch`/`--json-out` paths. All four stderr streams were empty. The scratch mutant hashes above are the after-mutation values; the exact original manifest and run-record hashes remained observable in the untouched lane. These scratch copies were disposable under the assignment's mandatory scratch-cleanup requirement and were removed before yield.

## Binding and tuple-check evidence

The committed counter source at the measured revision computes `observed_features_match_declared` by iterating manifest carriers, calling `observed_features(env_objs.get(cid))`, and comparing the extracted envelope tuple with `declared_features(c)` (counter lines 2057–2098). Its separate `generator_tuple_check_consistent` loop extracts `mine = observed_features(env_objs.get(cid))`, compares the recorded `observed` value against `mine`, and separately compares the record's `declared` value against the carrier declaration (lines 2106–2148). Thus the code does **not** consume `generator.tuple_check` as observed truth. The score receipt also records `generator_tuple_check_all_equal` and `generator_tuple_check_consistent` true, and `observed_features_match_declared` true; the code path, not those summary fields, establishes the distinction.

Ran the counter's built-in detector on its authored scratch fixtures:

`HYAKU_SCRATCH=<scratch>/selftest python3 -I -B <lane>/tools/round-43/c1-counter.py --selftest`

Exit **0**; actual output: `{"selftest":"c1-counter r43 (v4)","cases":91,"green":18,"red":73,"pass":91,"fail":0,"failures":[]}` and `SELFTEST cases=91 pass=91 fail=0`. The selftest includes a manifest declaration/envelope mismatch expecting `observed_features_match_declared` red, plus run-record bad-digest and bad-handler cases expecting `runjson_digests` red. It does not include a `declared_extras` mismatch case, so it does not close that probe gap. This is supporting evidence for those predicates, not a substitute for the four real-data mutants.

The committed CTL-C1-4 receipt independently describes a manifest-only H01 `published` mutation on the round-42 dev arm, with envelopes untouched, and records `observed_features_match_declared:false`. Its recorded counter exit is 1 and `ok:true`. This was read as contextual evidence; it was not re-executed here.

## Environment, cleanup, and limitations

No tools installed or updated. Disk check: `df -h /fast/scratch/hyaku /home/vgpnk/Projects/shokunin` showed 574G and 590G available respectively; `df -i /fast/scratch/hyaku` showed 418620510 free inodes. The requested `disk-guard-status` command was unavailable (`error: command not found`); no heavy probe was run. No REA, unblob, sasquatch, or extractor was invoked.

The lane's pre-existing status at inspection included modifications to `.ufo/waves/round-43/w2.ready`, `SCORECARD.md`, `SHONEN.md`, and untracked wave-2 files; they were left untouched. No install, lane production edit, or VCS mutation was made. Scratch copies and probe artifacts were removed as required.

**Conclusion:** pristine P43-C1 scoring is green at `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`. The counter's freeze-integrity check prevents changing its frozen held-out bytes for these four real-data probes. Accordingly the four mutation verdicts remain inconclusive; do not count them as killed or as evidence of a surviving mutant. The tuple-check independence is supported by direct counter implementation and the selftest/CTL-C1-4 evidence, while direct real-data mutation coverage for `declared_extras_match` remains unproven in this seat.