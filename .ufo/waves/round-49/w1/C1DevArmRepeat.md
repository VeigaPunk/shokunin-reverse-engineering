# C1DevArmRepeat — R49-C1 positive dev arm x3 on real REA 6.5.0

## Verdict

**No run-to-run difference in anything the claim scores.** Three independent `--dev-arm --run-rea` runs gave exit 0, `dev_matched 4`, `failing []`, and byte-identical stdout and `--json-out`. A deeper harness (below) captured the raw REA envelopes over four runs (three distinct work dirs, plus one repeat of the first work path). Across them, handler, published set (path, sha256, size), gap kinds, unpublished entries and the counter's full `plus-extractor` semantic projection were identical for all four carriers. The counter-time rerun-projection clause is **not flaky on this evidence**.

Gaps in the dev arm itself, reported for folding (not defects in the verdict):
- F2 the dev arm cannot test projection stability (the clause is exempt).
- F3 it does not print evidence ids, published files or gap kinds.
- F4 evidence ids are not reproducible even from an identical work path (by design).

Not run: the real (non-dev) `measure()` rerun path, which needs a committed receipt and `--data-run`; I did not run that. The harness exercises the same `make_real_runner`, `projection` and `evidence_ids` functions, but not the `projection_diff` call inside `measure`.

## Setup

- Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Clone built with `mkclone.sh $S/clone`, printing `DEV_FREEZE=3d7f248cbe641fbeaefe3cba868ce0a04556ffda`. `git -C $S/clone rev-parse --show-toplevel` equals `$S/clone`.
- `S=/fast/scratch/hyaku/kaidoku-r49/C1DevArmRepeat` (removed at the end; receipts copied here).
- `c1-counter.py` sha256 in the clone: `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779` (matches `counter_sha256` in the receipts).
- No tools installed. No pacman. Disk guard OK (/fast/scratch 36%).

## Findings

| # | Finding | Evidence |
|---|---|---|
| F1 | Three dev-arm runs identical | see table below |
| F2 | **The dev arm exempts `projection_ok` and `receipt_fresh`** (`c1-counter.py` L2095–2135, `core` list excludes both; docstring L2417). So `--dev-arm` cannot detect rerun flakiness at all. It only proves the receipt-side clauses on fresh envelopes. The rerun clause was exercised only by my harness, which calls `make_real_runner`, then `projection(env,'plus-extractor',handler)` and compares. The real `projection_diff(...)` path inside `measure()` was not executed. | harness.py, a/b/c/d.json |
| F3 | Dev-arm stdout/JSON prints only booleans plus `oracle_hits/oracle_files`: no handler-chunk list, published files, gap kinds or evidence ids. `--work` is the parent of a `mkdtemp` (`c1-devarm.*`) that is `rmtree`d in `finally` (L2438, L2491–2492), so `$S/devarm<N>` is empty after the run and nothing can be inspected post hoc. A seat comparing "evidence ids" across dev-arm runs from the counter's own output cannot. | `ls devarm1` empty; L2438/2492 |
| F4 | **Evidence ids differ on every run, even with the same work path** (run `d` reused `hw-a` after `rm -rf`): e.g. v1le `ev_cd5f09…` (a) vs `ev_efba43…` (d). Every id is re-minted per run because `output_directory` is in the hash, and also because REA's tmp dir `rea-firmware-<6 random>` and `blob_id`/`provider_id` (`<pid>:1`) change. This is correct for the plan (ids compared by recompute, not equality; projection excludes them), but it means the committed receipt cannot be reproduced byte-for-byte at the counter-time rerun and nothing in the plan may ever say "same evidence id". Plan P49-C1 says "recomputes its evidence id" only — consistent. | a.json vs d.json |
| F5 | Residual-difference check: of all leaves differing between envelopes, after normalising the work-dir segment (`hw-*`), the `rea-firmware-XXXXXX` tmp name and the `\d+:1` blob ids, plus `evidence_id`, **0 differing leaves remain** for all four carriers (a vs b/c/d). | inline Python in this session; reproduced by `envelopes/*.env.json` |
| F6 | `output_directory` in my harness runs is `<work>/rerun-<id>/out`, which satisfies the `/kaidoku-r49/` scratch-segment test only because my work root sits under `.../kaidoku-r49/`. The counter's `scratch_root()` default (`$HYAKU_SCRATCH/kaidoku-r49/counter`) also contains it. Not a defect, but it means the provenance clause is tied to `--work`/`HYAKU_SCRATCH`; a counter-time run with `--work` outside `/kaidoku-r49/` would fail `run_provenance_ok`. Not tested by me. | `output_directory` in a.json |

### F1 detail: the three dev-arm runs

Command (run 1, 2, 3, same shape; clone cwd; `TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku`):

```
python3 -I -B tools/round-49/c1-counter.py --dev-arm --root $S/clone --run-rea \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work $S/devarm<N> --json-out $S/devarm<N>.json
```

| run | start UTC | exit | stdout sha256 | json-out sha256 | wall |
|---|---|---|---|---|---|
| 1 | 2026-10-28T21:05:18Z | 0 | `068d6c3a…0a33` | `47243b7e…1e1d` | ~13 s (from timestamps; bc missing so not stopwatch-measured) |
| 2 | 21:05:31Z | 0 | same | same | ~10 s |
| 3 | 21:05:41Z | 0 | same | same | ~12 s |
| T1 | (timed rerun) | 0 | – | `47243b7e…1e1d` | 16.23 s |
| T2 | (timed rerun) | 0 | – | same | 16.24 s |
| T3 | (timed rerun) | 0 | – | same | 14.93 s |

Full sha256 of stdout: `068d6c3acc8f6a79689059f93c463465b26d68ac95ebaf3b8662af46faee0a33`; json-out `47243b7e68964017830f453776e884f380040dccfed5fb235fee9d7118a11e1d`. Same JSON as the first batch (`cmp` equal). Each run's stderr was empty.

Identical content in all runs: `dev_matched 4`, `scored 4`, `failing []`, `bindings_false` = `province_core_section, province_core_row, frontier_note, entry_present, sourced, coverage_map_row` (expected at the dev freeze), per carrier `dev_matched/layout_ok/tree_ok/gaps_ok/evidence_id_ok` all true:

| carrier | handler | oracle_hits/files |
|---|---|---|
| v1le | squashfs_v1 | 3/3 |
| v1be | squashfs_v1 | 3/3 |
| v2le | squashfs_v2 | 4/4 |
| v2be | squashfs_v2 | 4/4 |

### Harness comparison (runs a, b, c = distinct work dirs; d = same path as a)

Command: `python3 -I -B harness.py <tag> <workroot>` (copy at `C1DevArmRepeat/harness.py`, sha256 `201e343c…a51a`). It imports the draft counter module, calls `make_real_runner(work,None,900)` with `{'max_depth':3}` (the dev-arm params), then `evidence_ids(...)` (the same xpin tool as the counter), then the counter's own `projection(...,'plus-extractor',handler)`. Outputs: `a.json…d.json` (sha256 `ccf929b6…`, `279349c5…`, `3307a9ca…`, `3c0b67f0…`), raw envelopes under `envelopes/`.

| carrier | handler (all runs) | published (path,sha256,size) | gap kinds | unpublished | projection sha (a,b,c,d) | evidence id (a≠b≠c≠d) |
|---|---|---|---|---|---|---|
| v1be | `['squashfs_v1']` | 3 files, equal | `[]` | `[]` | `b8ec757f0ccf…` all equal | differ (4 distinct) |
| v1le | `['squashfs_v1']` | 3 files, equal | `[]` | `[]` | `d95513f8a04a…` all equal | differ |
| v2be | `['squashfs_v2']` | 4 files, equal | `[]` | `[]` | `aba30717c37c…` all equal | differ |
| v2le | `['squashfs_v2']` | 4 files, equal | `[]` | `[]` | `198852e32739…` all equal | differ |

Published: v1* = `apple.txt` (6 B, `303980bc…`), `banana.txt` (7, `5a81483d…`), `cherry.txt` (7, `86baf352…`), under `firmware.bin_extract/`; v2* = `apple1..4.txt` (7 B each), same hashes in LE and BE. Each evidence id also equals its own recompute (`[x,x]` per run).

Per-carrier REA wall (run a): v1be 3.79 s, v1le 2.90, v2be 3.75, v2le 3.38 (b: 3.1–3.5; c: 3.7–6.2 for v2be; d: 2.8–4.2).

Evidence ids (run a): v1be `ev_a3e778d2…`, v1le `ev_cd5f091d…`, v2be `ev_350e5129…`, v2le `ev_f2d6fc47…` (full values in `a.json`).

## Implication for the plan

- The rerun-projection clause as written ("same semantic projection as the committed receipt") is stable on four repeats of real REA 6.5.0, so it is not expected to flap at counter time for these four carriers.
- Nothing needs changing for flakiness. Suggested, optional: say in the plan or docstring that the dev arm does not exercise the rerun clause (the plan's Controls paragraph says only CTL-C1-POS "real scratch receipts + landing blocks, exit 0"; that control also uses committed receipts, so it goes through the real rerun path, which I did not run), and that evidence ids are never compared run to run.
- Files: `.ufo/waves/round-49/w1/C1DevArmRepeat/` (harness.py, a–d.json, devarm{1,2,3}.out/.json, devarmT1.json, envelopes/).
