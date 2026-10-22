# CriticTargets — round 29, wave 1

Seat: `KaidokuR29.CriticTargets` (critic). This seat attacks how the targets were sized and any edits made after the freeze for R29-C1 and R29-C2.
Freeze `dbd87cfa09eb89306c4e07d3171a4556eb732024`, data `4fcea97875a7fe1d816fb871cbc60a1c3632efa0`, measured tip `18be864a528873b2b70d8c94e31f880290249e90`.
Everything this seat did in the lane was read-only: git show, diff, log, ls-tree and rev-parse, `jj op log --ignore-working-copy`, sha256sum, and the freeze gate run with `--rev`, which only reads git. No network, no REA, no installs.

## Verdict

- **Post-freeze edits to the frozen inputs: holds.** None of the frozen paths changed between the freeze and the tip. Every round-29 data file was newly added and none was modified.
- **Narrowing after the freeze: holds.** The target denominators (16, 152, 178) and the target values are byte-identical at freeze and tip, and the after receipts report exactly those denominators.
- **Re-run of collection: holds.** There is one pass per collector: every lookup and fetch has `tries` 1, and no selector or URL appears twice in the manifests or the L1 logs. Nothing was collected before the freeze commit.
- **Target sizing: holds with one tradeoff for the judge.** The C1 target only requires that the work be complete and reproduce. It has no accuracy threshold, so any score would have met it (see A6). This is disclosed before the freeze, so it is not a defect.
- **Minor defects (fixable, no effect on any number):** see A7 and A8.

## Findings

### A1. Requested diff of the frozen claims, counters and inputs — observation

- Command: `git diff --stat dbd87cfa 18be864a528873b2b70d8c94e31f880290249e90 -- .ufo/waves/round-29/claims.json tools/round-29/c1-fresh-naming.py tools/round-29/c2-filtered-unseen.py corpus/evidence/round-29/c1/carriers.tsv corpus/evidence/round-29/c1/heldout.tsv corpus/evidence/round-29/c2/selectors.tsv corpus/evidence/round-29/c2/canonical-signatures.json`
- Output: empty, `exit=0`, run at 2026-10-22T20:20:52Z.
- Hash check, run at 2026-10-22T20:22:23Z, exit 0. For each file I took the sha256 of the blob at `dbd87cfa`, the blob at `18be864a`, the working-tree file, and the value pinned in `claims.json`:
  - Counters `c1-fresh-naming.py` (`6ad79d10…`) and `c2-filtered-unseen.py` (`00ca0a3d…`): `SAME CLAIMOK`.
  - Pinned inputs `carriers.tsv` (`94438ede…`), `heldout.tsv` (`2db9e658…`), `selectors.tsv` (`3a93f783…`), `canonical-signatures.json` (`5572beb5…`) and `tools/round-25/a2/resolve-selectors.py` (`4be91566…`): `SAME CLAIMOK`.
  - All five producers (`make-carriers.py`, `select-heldout.py`, `preseen.py`, `collect-c1.py`, `collect-c2.py`): `SAME CLAIMOK`.
  - `claims.json` itself: `76bc0d8f…` at freeze, tip and working tree.

### A2. Everything that changed after the freeze — observation

- Command: `git diff --name-status dbd87cfa 18be864a…` (run at 20:21:37Z, exit 0) gives `514 A`, `7 M`.
- The 7 modified paths are all outside the R29 claim inputs: `.ufo/waves/round-27/claims.json`, `.ufo/waves/round-28/a2w/ExecR27SelftestFix.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/claim-freezes.tsv` and `tools/round-27/c2-xpin-check.py`. That is the disclosed round-27 hygiene plus the rows the claims need. Another seat (ReviewR27Supersession) owns the round-27 change.
- Every path under `corpus/evidence/round-29/` was added, none modified:
  - c1: `db/` 305 files (304 lookups plus `manifest.json`), 16 envelopes, `runs.tsv` and `tally.json`.
  - c2: `db/` 179 files (178 responses plus `manifest.json`).
- `git diff --stat 4fcea978 18be864a -- corpus/evidence/round-29/` is empty (exit 0, 20:23:45Z), so nothing was edited after the data commit.
- `git diff --stat dbd87cfa 7431096b -- corpus/evidence/round-29/ <both counters>` is also empty (exit 0), so the hygiene commit touched none of it.

### A3. Strongest counterexample tried: data collected before the freeze was finalised — fails to break the claim (holds)

- **The attack.** The freeze commit has `author=2026-10-22T16:30:33-03:00` (19:30:33Z) but `committer=2026-10-22T17:03:06-03:00` (20:03:06Z). Its content was therefore settled only at 20:03:06Z. If any data had been collected between those two times, the inputs could have been tuned to it.
- **Op log.** `jj op log --ignore-working-copy` (exit 0) shows no operations between `7cf9e43d1f54 2026-10-22T19:30:33Z push bookmark main` (the base) and `c0c5e1fce422 2026-10-22T20:03:06Z track paths` / `644f56a52dba 2026-10-22T20:03:06Z commit e087cf37…`. No later operation rewrites `dbd87cfa`: after it there are only snapshot, commit, bookmark and push operations.
- **Which time the counters use.** Both counters take committer time: `git log --diff-filter=A --format=%ct` (c1 line 106, c2 line 78). That is 1792699386, i.e. 2026-10-22T20:03:06Z.
- **Data timestamps (observation):**
  - `runs.tsv`: utc_start runs from `n01 2026-10-22T20:03:21Z` to `n16 2026-10-22T20:03:37Z`, all exit 0.
  - c1 manifest: `n 304 min 2026-10-22T20:03:39Z max 2026-10-22T20:08:52Z dupfiles 0 dupurls 0 status Counter({200: 304})`.
  - c2 manifest: `n 178 min 2026-10-22T20:03:21Z max 2026-10-22T20:06:17Z dupfiles 0 dupurls 0 status Counter({200: 178})`.
  - Every timestamp is later than 20:03:06Z and earlier than the data commit at 20:09:09Z.
- **L1 scratch.** `find /fast/scratch/hyaku/kaidoku-r29 -newermt '19:30:33Z' ! -newermt '20:03:06Z'` (excluding seats) finds only `l1/src/{189cd726,0966a3bc}-{handlers.ts,canonical-signatures.json}` and `l1/src/erc-4626.md`. These are the source reads disclosed under `pre_freeze_probe`. The lookup-shaped files in `l1/prefile-demo/` are copies of round-25 lane data dated 20:13:49Z.
- **Inference.** Unobserved edits to the working copy could have happened between 19:30 and 20:03, because jj only snapshots when a command runs. None of them could have used this round's data, which did not exist until 20:03:21Z.

### A4. Re-runs — observation (holds)

- Both manifests have `tries` 1 on every entry: c1 `Counter({1: 304})`, c2 `Counter({1: 178})`.
- The L1 logs (`l1/tmp/c1-lookups.log`, 152 lines, sha256 `cc72991c…`; `l1/tmp/c2-fetch.log`, 178 lines, sha256 `5f7730b1…`) have no duplicate selectors (`uniq -d` gives 0 for both). The c2 log reads `178 200 1` for every line. The 9 lines that matched my `5xx` pattern were hex selectors such as `1a686502 200 1`, not errors.
- There is one after receipt per counter: c1 at `utc=2026-10-22T20:16:35Z`, c2 at `utc=2026-10-22T20:16:37Z`. Both counters read the lane through `git show <rev>:<path>` (c1 line 91, c2 line 73), so these receipts reflect committed bytes at the tip.
- Unknown: whether the counters were run, without a receipt, against `4fcea978` before the tip. That would be harmless, because no evidence or counter byte changed between `4fcea978` and the tip (A2).

### A5. Targets compared with the after receipts — observation

| Claim | Frozen target (claims.json at dbd87cfa) | After receipt at 18be864a |
|---|---|---|
| R29-C1 | runs_ok 16/16, rows_complete 152/152, tally_equal 1, entry_ok 1, exit 0 | `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1`, `exit=0`; `named 122, right 122, wrong 0, no_name 30` |
| R29-C2 | responses_complete 178/178, entries ≥ 1, mismatches 0, predicted_true ≥ 1, predicted_false ≥ 1, entry_ok 1, exit 0 | `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1`, `exit=0` |

- The denominators match what the selection step recorded before the freeze. `.ufo/waves/round-29/before/select-heldout.txt`, committed in `dbd87cfa`, reads `"abi_selectors": 178, … "excluded": 26, "c1_heldout": 152, "canonical_keys": 36, "canonical_unseen": 26, "c2_selectors": 178, "c1_heldout_that_are_canonical": 0`.
- The before receipts were run at `utc=2026-10-22T20:01:31Z` and exited 2 with `PIN pinned input absent`. That is before the freeze committer time, consistent with their being committed in the freeze.

### A6. Target sizing — inference; a tradeoff, not a defect

- **C1.** The target consists only of completeness and reproducibility counts. A rule that named nothing, or named everything wrong, would still have met it. The frozen claim says this itself: `"hypothesis_reported_not_target": "H1 … H2 … Both are reported as observed; neither decides the claim."` So the coverage claim is a measurement on a fresh set, not a test the rule could fail.
- The knowledge entry stays within that framing. Lines 45–46 read `named 122, right 122, wrong 0. Both reported hypotheses hold: H1 … and H2 …`, which is arithmetically true (0 ≤ 6.1 and 122 ≥ 76). The entry does not present them as targets.
- Impacted axis: coverage. Whether a coverage learning claim with no accuracy threshold can be admitted is the canonical judge's decision. This seat cannot correct it.
- **C2.** `mismatches 0` is a real bar the counter can fail. The `≥ 1` branch minimums are weak but satisfied by wide margins (38 and 214).
- By the claim's own `separation` text, every predicted-true entry comes from the 26 canonical keys, and the 152 C1 selectors exercise only the false branch. That is disclosed and does not reduce the claim.

### A7. Minor defect: stale docstring in a frozen counter — observation

- `tools/round-29/c1-fresh-naming.py` lines 14 and 27 still say `corpus/evidence/round-28/c1/carriers.tsv` and `corpus/evidence/round-28/c1/tally.json`. The code uses `EVDIR = "corpus/evidence/round-29/c1"` (line 57).
- This affects provenance and readability only, never a count. The counter is pinned, so the smallest safe fix is to correct the docstring in the next round's copy of the counter and note it there. Do not edit this file.

### A8. Minor point: a "before" receipt produced after the freeze — observation

- `.ufo/waves/round-29/before/census.txt` was added in `18be864a`, not in the freeze commit. It reads `utc=2026-10-22T20:07:16Z lane=bacbe9cc-tree (SOURCES.md unchanged since base)`, `exit=0`.
- It is a census of the base tree, not a receipt for either claim, and no counter reads it. Putting it under `before/` makes it look as if it was committed with the freeze.
- Smallest safe correction: disclose in the lesson or SCORECARD that it was generated after the freeze, from the base tree.
- `before/r27-c2-xpin-selftest-unpatched.txt` (added in `7431096b`) belongs to the round-27 hygiene and is outside this seat's scope.

### A9. Freeze gate on round 29 — observation

- Command: `python3 -I -B tools/round-29/freeze-gate.py --root . --rev 18be864a…`, exit 0, 2026-10-22T20:22:46Z.
- Round-29 result: `"findings": [{"finding": "INSTRUMENT_UNPINNED", "path": "tools/round-28/c1-heldout-naming.py"}]`, `"verdict": "FLAGGED"`. There is no `INSTRUMENT_REVISED` finding, so no commit between `dbd87cfa` and the tip touched any named instrument.
- The flagged file is named only as the source of the "unchanged" rule. I checked that claim: `diff` of `rule_outputs` in round 28 (lines 135–152) against round 29 (lines 141–158) is empty (exit 0). Both extracts hash to `7055d5b6…`.
- The finding is disclosed in `corpus/claim-freezes-v2.tsv` row `round-29 FLAGGED INSTRUMENT_UNPINNED … (M29-3)`.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticTargets/`)

| File | sha256 |
|---|---|
| `freeze-gate-tip.json` | `ab4316a370194bbf164ec84fe2f822082f9b332035bf64ca4b0a36580efcaec1` |
| `r28-rule.txt` | `7055d5b6e2eaf45b3134447b71eb0a9232540af8d7b8803ab89571c3bd7adaac` |
| `r29-rule.txt` | `7055d5b6e2eaf45b3134447b71eb0a9232540af8d7b8803ab89571c3bd7adaac` |

Lane files read, with sha256 at read time: `after/c1-at-18be864a.txt` `6987bd99…fcbdae`, `after/c2-at-18be864a.txt` `6f34bc6b…c87487`, `claims.json` `76bc0d8f…60cf79`.

Installs: none.
