# ScoutTools — round 47 frozen counters

Axes: coverage of both CLIs and every selftest case, depth of each claim clause against the freeze bytes, calibration of digests and exit codes. No installs. No frozen file was modified. Counters below are the blobs at `5017e1f7299c3a812e87e7950148f54313dd279e` unless a row says HEAD.

## Inventory

`tools/round-47/` at the freeze is two files. Worktree bytes matched those blobs at 2026-10-28T17:49:13Z (`git diff` empty). `exact.py` is still that blob. `record.py` and `plans/round-47-claims.md` are not: HEAD `1e2c3102952dc636650095643c1963c833859019` contains four later commits that edit the frozen paths (see the last section).

| object | git blob | mode | bytes | sha256 | command |
|---|---|---|---|---|---|
| `plans/round-47-claims.md` | `81aeb65eca45d3e05de18167717073ffa4bfd368` | 100644 | 12322 | `c8615eb811f598a35cad514523225e320185ec3c6481035fc95f844071e41f67` | `git cat-file blob 81aeb65e \| sha256sum` at 2026-10-28T17:49:13Z |
| `tools/round-47/exact.py` | `fb21a16686633fc3b2d0f6d82910bf9e5eb8b0ac` | 100755 | 23607 | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | same |
| `tools/round-47/record.py` | `1f8e792898fd8d28ae4e63668eaebe07fa7a788d` | 100755 | 25401 | `af666ce26c72e209e165779958489ed53182a1e68270aa9353da32ca2c8abe9d` | same |
| tree `tools/round-47/` | `d3f310ff8afa49bbdcd3035bfc814528566a5f3a` | — | — | — | `git rev-parse 5017e1f7:tools/round-47/` |
| freeze re-derived | `5017e1f7299c3a812e87e7950148f54313dd279e` | — | — | — | `git log --format=%H -1 -- plans/round-47-claims.md` at 17:49:13Z, equal to the named freeze |

`MUTATIONS` names, in order: `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift`. Digest `sha256("\n".join(names))` = `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` (`exact.MUT_DIGEST`, probe2 / probe.json). Same formula the claims require. Claims do not pin the hex in advance.

### CLI

No `EXIT_*` constants in either module. The contract is the docstring sentence `Exit codes: 0 met; 1 not met; 2 could-not-evaluate.` and literal `return 0/1/2`. Argparse usage errors also exit 2.

| command | exit | stdout sha256 | UTC |
|---|---|---|---|
| `python3 -I -B tools/round-47/exact.py --help` | 0 | `a474e7dff6ab8e223137d90d5d5fe54fe31dc6ab68f718e6895f95a6ce3cacb0` | 2026-10-28T17:49:19Z |
| `python3 -I -B tools/round-47/record.py --help` | 0 | `491d85c34797ca8469da1eeb2995f4016c118c86cfcf6e1086a1046972c26dea` | 2026-10-28T17:49:19Z |
| `exact.py` with no args | 2 | `d7017b6eeacb82b83b61b9156e9aad675d0ed80d420a777941ee79a6b619666a` | 2026-10-28T17:49:19Z |
| `record.py` with no args | 2 | `f94558f4901a2962bdaa8a1e6b4b2393f1ea9aa0f9289336ed317d0231523974` | 2026-10-28T17:49:19Z |

`exact.py` usage: `--root --freeze --rev [--profile {v2,v3}] [--no-battery] [--selftest] [--json-out] [-h]`. Default profile `v3`.

`record.py` usage: `--root --rev [--no-battery] [--selftest] [--json-out] [-h]`. No `--freeze`, no `--profile`.

The claims' counting commands name `--root/--freeze/--rev/--json-out` (C1) and `--root/--rev/--json-out` (C2). Those flags exist. The claims do not mention `--profile`, `--no-battery`, `--selftest`, or `-h`. `--json-out` must sit inside the lane and outside `GRADED` (`gate.out_path`); a path outside the lane is exit 2, not a score.

`record.py --help` (freeze bytes) describes seats, window, path, and rev. It does not mention `axes`. The claims predicate and `CLASSES` do.

### Selftest case counts (source of the freeze blobs)

Counted by regex over `def selftest(` in the extracted freeze blobs (`probe2.py`, record sha `af666ce2…`, exact sha `dcef54f1…`). Claims do not state a case count.

`exact.py`: 16. Fifteen `run(...)` calls plus appended `battery-discriminates`.

`green`, `red-marker-missing`, `red-two-markers`, `red-title-unnumbered`, `red-header-inexact`, `red-rows-not-four`, `red-duplicate-routed-id`, `red-arm-substring`, `red-digest-stale`, `red-ref-no-selector`, `red-ref-outside-allowlist`, `red-pin-mismatch`, `red-malformed-heading-is-exit-2`, `red-flag-order-swapped`, `red-battery-green-forgery`, `battery-discriminates`.

`red-battery-green-forgery` is the same row mutation as `red-arm-substring` and calls `score(..., battery=None)`. It does not run `run_battery`. Expectation 1, not a battery aggregate.

`record.py`: 9. Seven `run(...)` calls plus `red-non-empty-window` and `battery-discriminates`.

`red-seats-false-no-correction`, `green-seats-false-superseded`, `red-unverifiable-window-uncorrected`, `red-ghost-exemption`, `red-correction-total-false`, `red-one-correction`, `green`, `red-non-empty-window`, `battery-discriminates`.

No selftest case feeds an `axes` correction. Selftests were not executed (counts are from source). Not run as a process: both `--selftest` entry points.

### What matches the claims

| claim | freeze bytes | evidence |
|---|---|---|
| C1 marker, header, four routed ids, four arm tokens | `MARKER`, `HEADER`, `ROUTED`, `VOCAB` in `exact.py` | source |
| mutation names and digest formula | `MUTATIONS` / `MUT_DIGEST` | digest above |
| flag-order literals | `ORDER` / `REVERSED` | source |
| C1 before: exit 1, `block_present 0`, `rule_blocks 23`, `marker_occurrences 0` | measured | `receipts/exact-freeze-nobattery.json` sha256 `5f42beab2200f9ca168cee395470d79eca4225b59a98c04952ef076055cfa33b`, exit 1, 2026-10-28T17:52:51Z. Command: `python3 -I -B tools/round-47/exact.py --root <lane> --freeze 5017e1f7 --rev 5017e1f7 --no-battery --json-out <that file>` |
| C2 before: exit 1, mismatches 4 (round-45 wave 2 claimed 32 vs dispatched 36; round-46 `<tip>` window; coverage 133/133 vs 138/138; depth 20/20 vs 23/23) | measured on the freeze blob | `receipts/record-freezeblob-at-freeze.json` sha256 `7c93ef7e37dab44c5c29ae0cf99c58df97c34ef43074104f55138fae92897218`, exit 1, 2026-10-28T17:54:38Z. `sections` = `round-45`, `round-46`. `atoms_by_class` seats 2, window 1, path 12, rev 33, axes 2. `corrections` 0. |
| C1 does exit 2 `frozen_path_changed` once frozen bytes move | measured at HEAD | `receipts/exact-head-nobattery.json` sha256 `706cf11c4b17acb95c78afc1ac690addc3de81a0d479685ba4f11cd66625790f`, exit 2, 2026-10-28T17:53:40Z. `blob_changed` = `plans/round-47-claims.md`, `tools/round-47/`. `touched` includes `tools/round-47/record.py`. |

## Discrepancies (freeze bytes vs the freeze claims)

### D1. C2's target is unreachable on the frozen counter. The only in-scope window cannot be repaired.

Claims (R47-C2 clause 3 and the exemption sentence): a window correction states `empty in A..B -- paths` and re-derives empty; a window exemption may cover an atom that names no concrete window. The before-state's only window atom is the `<tip>` placeholder.

Freeze `record.py` then does a second check the claims do not state (`evaluate_text`, the `known_pairs` branch): if the correction's `A..B` is not already a pair on some in-scope window atom, it appends `corrections_bad` / `window pair names no atom in scope`. The one window atom has `pair is None` (`atoms_by_class.window == 1`). Every syntactically valid window correction therefore fails that check, and without a window correction the placeholder stays a mismatch.

Measured with the freeze blob against HEAD, where `SCORECARD.md` already contains the two correction lines the landing would add:

`python3 -I -B <freeze-blob record.py> --root <lane> --rev HEAD --no-battery`

exit 1 at 2026-10-28T17:54:38Z. Receipt `receipts/record-freezeblob-at-head.json` sha256 `250236e781563a5fa8f9bf5da42d368ef07d3d601a61090e7e6d25a2deaea41f`. `mismatches []` (the placeholder was exempted), `corrections_bad` = the line `- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` with detail `window pair names no atom in scope`. `failing == ["corrections that do not re-derive: 1"]`. Not met.

So `failing == []` is not reachable for this scorecard on the frozen counter. The later HEAD claims text calls this amendment A1. That paragraph is not in the freeze blob (sha `c8615eb8…`).

### D2. `record.py` does not exit 2 when frozen paths change.

Claims line 11: a change to this file or `tools/round-47/` makes **both** counters exit 2 `frozen_path_changed`.

`git grep freeze_state 5017e1f7 -- tools/round-47/record.py` is empty. `probe2.json` `has_freeze_state: false`. The freeze blob has no `--freeze` argument.

Same HEAD run as D1: exit 1, reason is the window-pair clause, not `frozen_path_changed`. The amended worktree `record.py` at HEAD exits **0** (`receipts/record-worktree-at-head.json` sha256 `b9f528cb821cd9f8b013a0f9218206038c58740dba4a900c7e309491098b0dae`, 2026-10-28T17:54:39Z) while `exact.py` exits 2. C2 can score a revision whose frozen paths already moved.

### D3. A `rev` correction drops the ancestry check. Exit 0 with a non-ancestor exempted.

Claims: every backticked 7–40 hex token is `git rev-parse --verify` plus ancestor-of-branch. Freeze code checks ancestor of the resolved `--rev` (`merge-base --is-ancestor`), not of a named branch. The correction re-derive (`corrects`, class `rev`) is only `rev-parse --verify`. A token that resolves and is not an ancestor is exempted, and `corrections_bad` stays empty.

Fixture (scratch, deleted after this report; toplevel asserted equal to the fixture dir before commit):

- main `7dc09357633e058541e2bf74ab36d135131a1719`
- side `e98344e164376caa7131b2134618b95f4b6fe14c` (`merge-base --is-ancestor` exit non-zero)
- card cites `` `e98344e16437` `` and carries `- corrects rev e98344e16437: cited` plus two real seats/window corrections and a false `- corrects axes coverage: 0/1`

`record.evaluate_text` on the freeze blob: exit 0, `met_target true`, `mismatches []`, `corrections_bad []`, `exempted` = that rev token, `corrections` = 3 (the axes line was not parsed). Receipt `receipts/probe2.json` sha256 `b7c6756d230add2f2e831ad4d1addb2ec839c291586eb8d0d5a5e81ec8202ec4`, 2026-10-28T17:54:38Z.

### D4. An `axes` correction is invisible. The two axes mismatches cannot be exempted by the syntax the claims specify.

`CORR` (freeze `record.py:50`, still the same pattern at HEAD) is `^- corrects (seats|window|path|rev) …`. `axes` is not a class. `corrections()` therefore drops `- corrects axes coverage: 0/1` and `- corrects axes depth: 0/1`. `probe2.json` `axes_parsed` contains only the seats and window lines from a four-line sample.

`corrects()` has a real `axes` branch and, after it, a second `if cls == "axes"` that names `atom`, which is not in scope (`NameError` if that line were ever reached). The parser makes both unreachable. The second branch is dead even if the regex grew `axes`, because the first branch returns.

The freeze before-state's coverage `133/133` vs `138/138` and depth `20/20` vs `23/23` are real (`record-freezeblob-at-freeze.json`). A correction line cannot clear them and does not count toward `corrections >= 2`. Clearing them requires editing the Owned-axes cells. At HEAD those two atoms are no longer mismatches (D1 receipt: `mismatches []`), which is consistent with an edit of the cells, not with an axes correction.

### D5. Kill-rule `blobberish` does not pass v2. `order-ish` and `symbolic` do.

Claims kill rule: a v3-arm cell `blobberish` fails clause 5 while profile v2 passes it. v2 is `any(token in cell.lower() for token in {symbol, once, digest, order})` (`exact.py` clause 5, `else` branch). None of those tokens occur in `blobberish`.

In-memory `exact.score` on a four-row block whose arm cells are the candidate (freeze `exact.py`; other clauses held green). 2026-10-28T17:52:51Z, `probe.json` (scratch; the exact.py half is the freeze blob):

| arm cell | v2 exit | v3 exit |
|---|---|---|
| `blobberish` | 1 `arm cells outside the vocabulary` | 1 exact-token failure |
| `order-ish` | 0 | 1 |
| `symbolic` | 0 | 1 |

The frozen substring mutation writes `order-ish`, which does discriminate. The kill rule's concrete token does not.

### D6. Battery forgery `duplicate-routed-id` is two defects, not one.

`_m_duplicate_id` inserts a fifth row (`R46-CL2` again). Scored on the freeze module: `row_count 5`, v2 exit 0, v3 exit 1 with both `rows 5 != 4` and the cardinality failure (`probe.json` `duplicate_mutation`). Clause 9 only requires v3 exit ≠ 0. A counter with clause 4 deleted would still paint this forgery red via the row-count clause. The isolated four-row duplicate is selftest `red-duplicate-routed-id` only, and selftest is not clause 9.

### D7. `tools/round-47/exact.py` cited with no line selector still scores 0.

Claims clause 8: every reference carries a line selector. `check_refs` skips the line-selector requirement when `name == SELF` (`exact.py`, the `continue` under `if name == SELF`). A block whose three citations are `tools/round-47/exact.py` (no `:line`), `corpus/lessons/round-46.md:10-30`, and `:40-60` scored v3 exit 0, `failing []` (`probe.json` `interpreter_without_line_selector`).

### D8. Causal-separability paragraph contradicts the C2 predicate and the code.

Claims: C2 never reads the craft section. `depth_pair` reads `SKILL.md` at `## Queue-drain craft ` and counts citation-resolved blocks. The same claims file's axes row says that is the derivation. C2 also reads `corpus/README.md` and `git ls-tree` of `corpus/knowledge`, not only `SCORECARD.md` and `.ufo/waves/`. C1 does not read `SCORECARD.md` (no such reference in `exact.py`). That half of the separability sentence holds.

### D9. Seats are not read from `*-dispatch.json` in file order.

Claims: `.ufo/waves/round-<N>/*-dispatch.json` → `counts.spawn`, file order. Code walks `.ufo/waves/round-<N>/w{i}-dispatch.json` from `i = 1` and stops at the first miss (`dispatch_counts`).

At the freeze, rounds 45 and 46 have only `w1-dispatch.json` and `w2-dispatch.json`, and the counter's derived round-45 spawns are `[40, 36]`, which is the claims' before figure. The narrower walk does not change this card. It would drop any non-`wN` file. `git ls-tree -r --name-only 5017e1f7` finds 61 `*dispatch.json` paths; 26 are not `w<N>-dispatch.json` (round-14 `dispatch.json`, round-16 `wave1-dispatch.json`, round-24 `residual-dispatch.json`, and others). List is in the first probe's `dispatch_not_wN`. Those rounds are outside the current two sections.

### D10. No-op battery credit is a source branch the frozen mutations do not hit.

`run_battery` (`exact.py`): if a mutation returns the same block and no overrides, it increments `forgeries_total` and `v2_green` and does not score v3. Executed by temporarily replacing `MUTATIONS` with four no-ops (`receipts/noop2.json` sha256 `502f8a94f3b721e112656687d0d37c60d463aa46035b342ea71b2f3911b47fb8`, 2026-10-28T17:55:10Z): `forgeries_total 4`, `v2_green 4`, `v3_green 0`, `crash 0`, fixtures `mutation was a no-op`. `genuine_green` was 0 because clause 6 then required the block to name `noop-0`…`noop-3`. The full clause-9 conjunction was **not** observed true. The frozen four functions are not no-ops (duplicate and substring rewrite rows, stale digest rewrites the pin, flag-order sets an override). Latent accounting hole, not a demonstrated green forgery of the frozen list.

## Freeze already moved (observed, not part of the freeze blob)

`git log --format='%H %ci %s' 5017e1f7..HEAD -- tools/round-47 plans/round-47-claims.md` at 2026-10-28T17:53:40Z:

| commit | subject |
|---|---|
| `9018c53b16503c8d06d398b75503406508119946` | A1 — drop the unreachable window-pair clause |
| `62e33f7dd75c8e3285967b26419842c106f6c965` | A2 — window forgery uses root..tip |
| `2e4ae43463aabdae707f8c8a4daa41441ad67a71` | A3 — a seats/window correction for an older round stays valid |
| `1e2c3102952dc636650095643c1963c833859019` | A4 — historical-correction selftest gets a round-3 dispatch |

Diff: `receipts/frozen-vs-head.diff` sha256 `23dbb7a8e6f3e0c4d00552461cabb244947b9846905804caee655874fe5f4e42` (103 lines). `exact.py` has no diff. HEAD `record.py` sha256 `c704c3d407325264f8e2d990a8873524b0c5bbbf52d5dcc10ee8df411c9d6fa7` (not the freeze blob). HEAD claims sha256 `2b5d1bef4c0339325331f0197631b7580657337bde1b5311dd94365f085c6460`.

A3 changes a clause (historical seats/window corrections no longer fail "exempts an atom that does not exist") and is not described by the A1/A2 paragraphs added to the claims file. A3's `record.py` selftest has a tenth case, `green-historical-correction`, which is **not** in the freeze blob.

Scoring C1 at HEAD against freeze `5017e1f7` exits 2 (table above). Scoring the amended C2 at HEAD exits 0. Those are different instruments from the freeze.

## Not run

- `exact.py --selftest` and `record.py --selftest` (case lists are from source only).
- C1 battery on a real block-24 landing (no block at the freeze: `marker blocks` cannot be built; claims' `ctl-c1-2` statement. Not re-run here).
- C2 battery (`--no-battery` on every counter invocation above).

## Receipts

`.ufo/waves/round-47/w1/ScoutTools/receipts/` — help text, both freeze-blob JSON scores, the HEAD exact.py exit-2 score, the worktree record.py exit-0 score, `probe2.json`, `noop2.json`, `frozen-vs-head.diff`.
