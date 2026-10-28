# R44W2Wave — wave-1 accounting audit

Seat `R44W2Wave`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. HEAD observed `8bb1090af3fef64477c4337855e4347472db2701`. Measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`. Freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`. No tools installed.

Axes: advertised-seat identity, role identity, evidence-path existence, lane-write byte identity. A move is kept only when it checks another source without dropping a prior check.

## Verdict on the round-shape sentence

`corpus/lessons/round-44.md:108` says the wave-1 seat outputs are `.ufo/waves/round-44/w1/`, **37 seats**, `r44-w1-results.json`. That count is true. It is not true that every file a seat's result names is present, and it is not true that every sha256 inside `r44-w1-results.json` is the blob on disk. Do not promote the sentence to "37 seats, every cited file present, every result digest current."

## Seat identity (confirmed)

| source | count | unique | vs `w1-spec.json` `items` |
|---|---|---|---|
| `w1-spec.json` `items` | 37 | 37 | — |
| `w1-dispatch.json` `taskCall.tasks` | 37 | 37 | same names, same order |
| `w1-dispatch.json` `registry.members` | 37 | 37 | same names, same order |
| `w1-dispatch.json` `counts` | spawn 37, resume 0, total 37 | — | matches |
| `w1/swarm-registry.json` `members` | 37 | 37 | same names, same order |
| `r44-w1-results.json` `results` | 37 | 37 | same names, same order |
| `r44-w1-results.json` `seats` | 37 | — | matches `len(results)` |

Roles are identical across spec `role`, dispatch `agent`, registry `role`, and results `agent`: executor 8, scribe 8, scout 7, reviewer 4, critic 3, connector 3, revenger 1, sentinel 1, mutation-tester 1, simplifier 1. Zero role mismatches.

## Dead seats

None. All 37 result `output` values are non-empty JSON (`note` is null on every row). All 37 canonical reports `.ufo/waves/round-44/w1/<Name>.md` exist. No result status is `error` / `failed` / `blocked` / `incomplete`.

`swarm-registry.json` has `agentId: null` and `item: null` on all 37 members, `kind: spawn`. That is the dispatch snapshot, not a dead run: the same 37 names have results and reports.

`R44Watchdog`'s result says `dispatched_as: R44Watchdog-2`. There is still one advertised seat and one result. No second watchdog seat is in the 37.

Sixteen seats have no `w1/artifacts/<Name>/` directory. Each of those sixteen has its `<Name>.md`. Absence of an artifact directory is not a dead seat.

One extra markdown is not a 38th seat: `.ufo/waves/round-44/w1/R44C1Oracle-r48-ready.md` (5506 bytes) is named in `R44C1Oracle`'s `files_changed` and exists. `w1/*.md` is therefore 38 files = 37 seat reports + that advisory.

## Evidence paths

Concrete write-claims parsed from result fields (`files_changed`, `deliverables`, `files_written`, `installed`, `lane_writes`, `written`, `artifact_paths`, `report` / `report_path` plus sibling sha256): 87 unique seat+path pairs after dropping globs. **0 of those 87 are absent.** 21 sha256 pins match the worktree; 64 exist with no full sha256 on the claim; 2 pins do not match the worktree (defects 2 and 3).

Brace/glob claims that resolve: `R44C1Controls` control-fixtures `c1,c2,c3,c4,c5,pos` (files present; `c0` was not in that brace); seven `CTL-C1-{0,1,2,3,4,5,POS}.json`; `R44ScoutCalib.json`; 9 files under `artifacts/R44C2Rubric/`; 14 `artifacts/R44C2Counter/receipts/*.json` and 15 top-level json there; four `R44MistakeHunt` bodies; 20 `R44C1Doc` receipts; `R44Assim` `A01`–`A11.json` plus `receipts.tsv`, `slice-rederived.txt`, `slice-sha256.txt`. `R44SrcOracle` oracle tree `corpus/evidence/round-44/oracle/` has 23 files. Scratch globs under `/fast/scratch/hyaku/kaidoku-r44/` were not treated as retained evidence.

### Sample of 10 (all exist)

Command (cwd = lane), exit 0, wall 0.001065 s, stdout sha256 `1591e6fe72fb645a83a12378b8776b511a08d4343640588d58b4a0281c4338c5`:

`sha256sum` of the ten evidence paths plus the two `c1-controls.py` copies. Receipt: `.ufo/waves/round-44/w2/artifacts/R44W2Wave/receipt.json`.

| path | bytes | sha256 | result pin |
|---|---|---|---|
| `.ufo/waves/round-44/w1/R44C1Revenger.md` | 30956 | `eb0e168e4519ca3c9a944dd0691e5073c16b8c5fb856850a3d0d8de32f448816` | match |
| `.ufo/waves/round-44/w1/R44C1Oracle.md` | 21059 | `db3d6801151e2c1a68f36728a7ec7959060bbeaace172f16bb3155718625cde7` | none in yield |
| `.ufo/waves/round-44/w1/R44C1Counter.md` | 17325 | `f2a8ccfd29225501f13c81bbf156d8d621f7a95d6443d02c15b699a35a9f4150` | match |
| `.ufo/waves/round-44/w1/R44SrcOracle.md` | 20887 | `fe977ef731617983659105a7ac6b3e448b49cbdbbc983a8d543b6289bddd7c99` | none in yield |
| `.ufo/waves/round-44/w1/R44C2Rubric.md` | 16973 | `e6b37b28bfb8688df28497013bc5829f8c97746d195d3c372ab92de6ce878174` | none in yield |
| `.ufo/waves/round-44/w1/R44C2Sentinel.md` | 42299 | `f569a3766e4df5e5a11781d6eb6bb5ab2bb136ce813720097f5c0a6a097a6225` | match |
| `.ufo/waves/round-44/w1/R44CritC1.md` | 8674 | `4b5ae8ddf4f554d574d843d403d08a44c4f7c50c507781894fa8c5707b165896` | none in yield |
| `.ufo/waves/round-44/w1/R44ConnRouted/receipts.json` | 20959 | `3773c3cf436705b08579d7fb3f1d399f1617c425dc5a37bccd72de09e1c760f1` | match |
| `.ufo/waves/round-44/w1/R44Debt.md` | 32603 | `ea38d49b9f61b0b89ae4f5cedcaf5c5f0b2045c5212c96a66ae327d9e2defe78` | seat said recompute |
| `.ufo/waves/round-44/w1/R44Watchdog.md` | 16644 | `95e1ecb5b4006969539bd1326d2e91a3c432c7a1d9c076b6b012e26827e49555` | match |

Pinned reports checked outside this sample also match the worktree: `R44EntryDraft.md` `e901d5c7…`, `R44Shonen.md` `d742abaf…` (22100 bytes, as claimed), `R44Assim.md` sha256 `e43087da…` (lines 211 as claimed).

## Lane writes

Every concrete non-`.ufo` path a result lists as written exists:

| path | result sha256 | worktree sha256 | same as artifact copy |
|---|---|---|---|
| `tools/round-44/c1-oracle.py` | `455c8a55…` | match (60104) | yes |
| `tools/round-44/c1-counter.py` | `9f2cc140…` (prose in `final_state`) | match (152655) | yes |
| `tools/round-44/c1-run.py` | `55e2692a…` | match | — |
| `tools/round-44/c1-run.sh` | `c35d4b9b…` | match | — |
| `tools/round-44/c2-counter.py` | `085192ea…` | match (76597) | yes |
| `tools/round-44/c2-rubric.json` | `e8cc0ded…` | match (680016) | — |
| `tools/round-44/c2-controls.py` | no pin | exists | — |
| `tools/round-44/c1-controls.py` | `32003f28…` in the results JSON | **`b8c55f9b…` (76389)** | yes, both copies are `b8c55f9b` |

No seat's result claims a `PROVINCE.md` / `SCORECARD.md` / `SHONEN.md` / `README` / `SOURCES` write that is missing. `R44C1Doc` says those tracked files were untouched.

`git diff --name-only 55bcce69 c86ea508 -- tools/round-44/control-fixtures` is 8 paths. That matches the lesson's M44-2 count. It is not the whole `c86ea508` commit: that commit also adds `r44-w1-results.json` and rewrites the entry-draft artifact (defect 3).

## Numbered defects

### 1. R44C1Controls names `receipts/selftest.json`; the file is absent

- Claim: `r44-w1-results.json:34` (`files_changed` path `.../receipts/CTL-C1-{0,1,2,3,4,5,POS}.json + selftest.json`) and `.ufo/waves/round-44/w1/R44C1Controls.md:42` and `:209` (`receipts/selftest.json`, "11 cases, 11 passed").
- Command: `test -f /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1/artifacts/R44C1Controls/receipts/selftest.json`
- Exit: **1**. `find` under `artifacts/R44C1Controls` for `*selftest*` prints nothing (exit 0, empty). `git log --all --oneline --` that path prints nothing (exit 0): not in history.
- Observed: the receipts directory contains only `CTL-C1-0.json`, `CTL-C1-1.json`, `CTL-C1-2.json`, `CTL-C1-3.json`, `CTL-C1-4.json`, `CTL-C1-5.json`, `CTL-C1-POS.json`. The seven scored control receipts are present. The driver selftest receipt is not.
- This is the only named evidence file a wave-1 result says it wrote that is absent. `artifacts/R44C2Counter/receipts/selftest.json` is a different seat and is present. Do not confuse them.

### 2. Results pin for `tools/round-44/c1-controls.py` is not the landed bytes

The lane write **was made**. The digest in the results entry was not.

- Claim: `r44-w1-results.json:34` sha256 `32003f281a32cb19089f01a376c52654f2ee6b46b3a71e76d9ccf6ebe98e7dee`, note "identical to the artifact copy".
- Command: `sha256sum tools/round-44/c1-controls.py .ufo/waves/round-44/w1/artifacts/R44C1Controls/c1-controls.py` (included in the sample command above).
- Exit: **0**.
- Observed: both files `b8c55f9b9d8af47e56f6bc8c11b21018b7fb1997c4fd399355c045a16aafa402`, 76389 bytes. `git show c48f8a4b:tools/round-44/c1-controls.py`, `55bcce69:`, `c86ea508:`, and `HEAD:` are the same digest. The file was added in `c48f8a4b` and never had content `32003f28…` in git. The two copies are identical to each other, so the "identical to the artifact copy" clause is true and the sha256 value is false.
- The seat report's install table is the one that matches disk: `.ufo/waves/round-44/w1/R44C1Controls.md:37` records `b8c55f9b…`. The same report's residual table `.ufo/waves/round-44/w1/R44C1Controls.md:220` still says `32003f28…`. The results JSON kept the stale pin; it did not keep the corrected one.
- L1 must not cite `32003f28…` as the controls-driver pin. The pin since the freeze is `b8c55f9b…`.

### 3. Entry-draft pin matches the measured revision and not the commit that recorded it

- Claim: `r44-w1-results.json:46` and `.ufo/waves/round-44/w1/R44EntryDraft.md:16` sha256 `4d26a052d98a532762221f044628936029554abffd0c3c115a123c5613ef55c2` for `.ufo/waves/round-44/w1/artifacts/R44EntryDraft/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`.
- Command: `git show 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac:.ufo/waves/round-44/w1/artifacts/R44EntryDraft/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md | sha256sum`
- Exit: **0**. Observed at `55bcce69`: `4d26a052…`, 16880 bytes. The pin is true at the measured revision.
- Same path at `c86ea508` and at HEAD: `ee04ffc7144f3d5c04a3a355711f483e6c424f03cb0a36f728a646aec291b7db`, 20280 bytes. `git diff --stat 55bcce69 c86ea508 --` that path is 143 insertions, 104 deletions. `r44-w1-results.json` was **added in that same commit** (`git log --oneline -- .ufo/waves/round-44/r44-w1-results.json` → only `c86ea508`). The commit that introduces the results record rewrites the blob the record pins.
- The landed knowledge entry is a third digest: `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` is `f75353207b920d432cd33b335b9b6da7999cc6be8550fa65c42d831f69fc2f62`, 20164 bytes, at `55bcce69` and HEAD. The seat called the artifact `lands_as` that path; it did not claim the landed bytes equal the draft pin.
- L1 must not quote `4d26a052…` as the entry-draft blob at HEAD or at `c86ea508`. Quoting it as the blob at `55bcce69` is correct.

## Not defects

- `R44Assim` result says the report is 13439 bytes and sha256 `e43087dad745adfae87c00e7debd1b56b956b8c6e04c3f7efe25d25c5273beea`. The file is 13218 bytes and that sha256 matches. Lines field 211 matches. The byte count is stale; the content pin is not. The file exists.
- `tools/round-44/control-fixtures/c0` does not exist. `artifacts/R44C1Controls/controls/c0/` has `receipt.json` and `counter.json` only. The results brace listed `c1,c2,c3,c4,c5,pos`, not `c0`. Not an unmade claim of that brace.
- No dead seat, no missing canonical report, no advertised name absent from results, no role drift.

## Confidence

High on the 37-way name and role identity (parsed JSON, order compared). High on existence and digests (filesystem `test` / `sha256sum`, `git show` of the same paths). Unresolved: whether `receipts/selftest.json` was written and then deleted before `c86ea508`, or never written. It is in neither the worktree nor `git log --all`.
