# MutC1Committed — R30-C1 commit/revision mutation probe

## Result

**[OBSERVATION] 9 mutants killed, 0 survivors, 0 inconclusive with the sandbox behavioral detector.** The frozen built-in selftest alone killed 3/9 and survived 6/9; those six missing regression cases are named below. This is mutation evidence, not an evaluation of either frozen claim.

**[OBSERVATION]** Each mutant received the same two bounded detectors on pristine, mutated, and byte-restored code: 54 detector invocations. All 36 pristine/restored invocations exited 0. Every mutated sandbox-fixture invocation exited 1 with exactly one behavioral mismatch. No baseline failure was counted as a kill.

**Axes:** behavior-bearing minimality, detector discrimination, exact-byte restoration, and lane isolation.

## Scope and exact commands

Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py`. Source locations in the mutant table are original frozen-file line numbers. The copied source SHA-256 matches the frozen instrument: `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a`.

Only seat-owned scratch copies and sandbox Git history were changed. The lane is unchanged except for this report. No REA invocation, carrier execution, carrier-byte mutation, C2 measure run, agent dispatch, integration, or claim-data collection occurred.

**S — frozen built-in selftest; expected pristine/restored exit 0:**

```sh
timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/active/c1-rust-positive.py --selftest
```

**F — sandbox behavioral detector; expected pristine/restored exit 0 and mutant exit 1:**

```sh
timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/detect_fixture.py --tool /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/active/c1-rust-positive.py --fixture /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/fixture.json
```

Both command lines stayed identical across every phase and every mutant. Git environment variables `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were removed before execution. F imports the copied tool, calls the five assigned functions, uses real sandbox Git reads through a timeout-only wrapper, and installs a `run_rea` tripwire that raises if called. F does not invoke the score-measurement path.

Executed preparation/orchestration commands (each observed exit 0):

```sh

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 180 git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/clone

timeout 180 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/build_fixture.py

timeout --kill-after=10 600 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/run_probes.py
```

Full per-invocation argv, UTC start/end, exit code, stdout, stderr, and before/after code hashes are recorded in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/commands.json`. Full stdout/stderr are also retained as individual hashed files in the artifact inventory.

## Sandbox fixture

The fixture starts at the lane base, adds a historical entry with `source: S088` while adding S089 to the source table and a matching PROVINCE line, repairs the entry in a later commit, deletes the synthetic claims/record files, and re-adds them. Its final uncommitted entry has `source: S089`; therefore a worktree read can incorrectly rescue the earlier invalid historical entry. These are synthetic history and envelopes, not REA evidence.

| State | Commit | Synthetic committer epoch |
|---|---|---:|

| Original base | `d210fb8fa62d2af04d009cfa0c65a4e8137dc742` | inherited |

| First additions; invalid historical entry | `de97d1b5b9539f6c92c25426f6aa2c096a1cdbce` | 1800000100 |

| Valid committed entry | `4de96bed3f37be82a85c6d2ce1409b74ca290c45` | 1800000200 |

| Remove claims/record | `3a557e4b4c6b18eaad63d7d9637af3061d9fef53` | 1800000300 |

| Re-add claims/record | `949b1e1fcfe3602a18e0d7f459243ff5e327b3f4` | 1800000400 |


For inherited-row/line tests, F temporarily points the module’s `BASE` constant at the synthetic first-addition commit, then restores it. This exercises the guard with an actual Git base containing that row/line; it does not edit the frozen lane base. The valid entry and valid PROVINCE cases also run against the actual lane base. Positive committed-record cases prevent reject-everything implementations from passing.

Git writes and commits happened only inside `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/clone`; sandbox commits use `user.name=ctl` and `user.email=ctl@sandbox`. Builder Git argv, dates, outputs, and exits are preserved in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/fixture-build-commands.json`. The four new commits are packaged in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/fixture-history.bundle` with the lane base as a prerequisite.

## Mutant table

All verdicts below are **[OBSERVATION]**. S/F columns are mutated-phase exit codes; their pristine and restored counterparts are 0 for every row.

| Mutant | Function / original lines | Defect | Expected detector behavior | S exit | F exit | Verdict |
|---|---|---|---|---:|---:|---|

| M01-freeze-strict-less | `committed_check()` 186 | `env_added <= freeze_ct` → `<` | same-time envelope must be refused | 1 | 1 | killed |

| M02-drop-evidence-id-comparison | `committed_check()` 192 | retain missing-ID rejection; remove `cid != lid` | different committed/live IDs must be refused | 1 | 1 | killed |

| M03-drop-entry-id-check | `committed_check()` 202–203 | remove entry-names-evidence-ID guard | entry lacking the ID must be refused | 1 | 1 | killed |

| M04-drop-S089-base-absence | `entry_ok()` 153–154 | remove S089-at-base rejection | inherited S089 row must be refused | 0 | 1 | killed |

| M05-allow-inherited-PROVINCE | `province_ok()` 164–165 | remove matching-line-at-base rejection | inherited matching PROVINCE line must be refused | 0 | 1 | killed |

| M06-freeze-max-time | `freeze_time()` 173 | `min(times)` → `max(times)` | return first addition time 1800000100 | 0 | 1 | killed |

| M07-added-max-time | `added_time()` 179 | `min(times)` → `max(times)` | return first addition time 1800000100 | 0 | 1 | killed |

| M08-entry-reads-worktree | `entry_ok()` 143 | `show(root, rev, ENTRY)` → `open(os.path.join(root, ENTRY)).read()` | invalid entry at requested revision must not be rescued by the dirty worktree | 0 | 1 | killed |

| M09-drop-committed-package-comparison | `committed_check()` 198–199 | retain tuple/schema validation, remove comparison against expected tuples | schema-valid changed package version must be refused | 0 | 1 | killed |


## Actual output and UTC receipts

All times below are UTC (`+00:00`). Each excerpt is verbatim stdout from the indicated exact S/F command above. Full streams are retained, not inferred.

Every pristine/restored S ended with `selftest cases=25 failures=0`, exit 0; every pristine/restored F ended with `fixture cases=12 failures=0`, exit 0. Mutated S ended with `selftest cases=25 failures=1` for M01–M03 and `selftest cases=25 failures=0` for M04–M09. Every mutated F ended with `fixture cases=12 failures=1`, exit 1.

### M01-freeze-strict-less

**[OBSERVATION] S:** 2026-10-23T02:46:18+00:00 through 2026-10-23T02:46:18+00:00; exit 1.

```text
FAIL red-committed-same-commit-as-freeze got=True (ok)
```

**[OBSERVATION] F:** 2026-10-23T02:46:18+00:00 through 2026-10-23T02:46:18+00:00; exit 1.

```text
FAIL fixture-freeze-equality got=[true, "ok"] expected=[false, "committed envelope absent or not added after the freeze"]
```

### M02-drop-evidence-id-comparison

**[OBSERVATION] S:** 2026-10-23T02:46:19+00:00 through 2026-10-23T02:46:19+00:00; exit 1.

```text
FAIL red-committed-id-differs got=True (ok)
```

**[OBSERVATION] F:** 2026-10-23T02:46:19+00:00 through 2026-10-23T02:46:19+00:00; exit 1.

```text
FAIL fixture-evidence-id-mismatch got=[true, "ok"] expected=[false, "committed evidence_id 'ev_other' != live 'ev_live'"]
```

### M03-drop-entry-id-check

**[OBSERVATION] S:** 2026-10-23T02:46:19+00:00 through 2026-10-23T02:46:19+00:00; exit 1.

```text
FAIL red-entry-lacks-id got=True (ok)
```

**[OBSERVATION] F:** 2026-10-23T02:46:19+00:00 through 2026-10-23T02:46:19+00:00; exit 1.

```text
FAIL fixture-entry-id-absent got=[true, "ok"] expected=[false, "entry does not name ev_live"]
```

### M04-drop-S089-base-absence

**[OBSERVATION] S:** 2026-10-23T02:46:19+00:00 through 2026-10-23T02:46:19+00:00; exit 0.

```text
selftest cases=25 failures=0
```

**[OBSERVATION] F:** 2026-10-23T02:46:19+00:00 through 2026-10-23T02:46:19+00:00; exit 1.

```text
FAIL fixture-S089-already-at-base got=[true, "ok"] expected=[false, "S089 already present at base"]
```

### M05-allow-inherited-PROVINCE

**[OBSERVATION] S:** 2026-10-23T02:46:19+00:00 through 2026-10-23T02:46:19+00:00; exit 0.

```text
selftest cases=25 failures=0
```

**[OBSERVATION] F:** 2026-10-23T02:46:19+00:00 through 2026-10-23T02:46:20+00:00; exit 1.

```text
FAIL fixture-PROVINCE-already-at-base got=[true, "ok"] expected=[false, "PROVINCE line already at base"]
```

### M06-freeze-max-time

**[OBSERVATION] S:** 2026-10-23T02:46:20+00:00 through 2026-10-23T02:46:20+00:00; exit 0.

```text
selftest cases=25 failures=0
```

**[OBSERVATION] F:** 2026-10-23T02:46:20+00:00 through 2026-10-23T02:46:20+00:00; exit 1.

```text
FAIL fixture-freeze-first-of-two-additions got=1800000400 expected=1800000100
```

### M07-added-max-time

**[OBSERVATION] S:** 2026-10-23T02:46:20+00:00 through 2026-10-23T02:46:20+00:00; exit 0.

```text
selftest cases=25 failures=0
```

**[OBSERVATION] F:** 2026-10-23T02:46:20+00:00 through 2026-10-23T02:46:20+00:00; exit 1.

```text
FAIL fixture-record-first-of-two-additions got=1800000400 expected=1800000100
```

### M08-entry-reads-worktree

**[OBSERVATION] S:** 2026-10-23T02:46:20+00:00 through 2026-10-23T02:46:20+00:00; exit 0.

```text
selftest cases=25 failures=0
```

**[OBSERVATION] F:** 2026-10-23T02:46:20+00:00 through 2026-10-23T02:46:21+00:00; exit 1.

```text
FAIL fixture-entry-revision-not-dirty-worktree got=[true, "ok"] expected=[false, "entry source line lacks S089"]
```

### M09-drop-committed-package-comparison

**[OBSERVATION] S:** 2026-10-23T02:46:21+00:00 through 2026-10-23T02:46:21+00:00; exit 0.

```text
selftest cases=25 failures=0
```

**[OBSERVATION] F:** 2026-10-23T02:46:21+00:00 through 2026-10-23T02:46:21+00:00; exit 1.

```text
FAIL fixture-valid-packages-differ got=[true, "ok"] expected=[false, "committed package multiset differs"]
```

## Built-in-only survivors: missing cases

**[OBSERVATION]** These mutants survived the unmodified built-in selftest. **[INFERENCE]** The following are missing discriminating cases in that selftest, not permission to weaken the frozen predicate. F supplies them in scratch only; no lane instrument or contract was repaired or changed.

| Surviving mutant under S | Missing case demonstrated by F |
|---|---|

| M04-drop-S089-base-absence | Reject a valid current entry when S089 already exists at the chosen base. |

| M05-allow-inherited-PROVINCE | Reject an otherwise matching PROVINCE line inherited unchanged from base. |

| M06-freeze-max-time | Claims file is added, removed, then re-added; return the earlier addition time. |

| M07-added-max-time | Envelope record is added, removed, then re-added; return the earlier addition time. |

| M08-entry-reads-worktree | Historical entry has the wrong source while the dirty current worktree has S089. |

| M09-drop-committed-package-comparison | Committed packages are schema-valid but have a different package version, with all dependency indices still valid. |


**[OBSERVATION]** The existing test named `red-committed-packages-differ` does not reach a package-multiset rejection in pristine code. S for M09’s pristine phase, 2026-10-23T02:46:21+00:00, exit 0, printed:

```text
ok red-committed-packages-differ got=False (committed metadata shape)
```

**[INFERENCE]** Its one-package document retains dependency index 1, so tuple normalization fails before the removed comparison could matter. M09 deliberately preserves tuple/schema validation, making this a genuine comparison-coverage survivor rather than a removal of all metadata validation. F changes package b’s version from 2 to 3 while preserving both packages and valid indices, exposing the omitted comparison.

**[UNKNOWN / not exercised]** This probe does not establish score-target success, live REA behavior, or revision binding at every other callsite. The worktree mutant is specifically the `entry_ok()` entry-text read. No live score counter was run, and no target-line claim is made.

## Restoration evidence

Let **P** = `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a`. Every row had before=P, restored-active=P, and restored-snapshot=P. `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/before-hashes.json` records each pristine copy before the surgical mutations.

| Mutant | Mutated SHA-256 | Before / after |
|---|---|---|

| M01-freeze-strict-less | `3ca8ee88e4c47ba185f476c3abbcaceb6f3bc29c255000398080c5ada573da48` | P / P |

| M02-drop-evidence-id-comparison | `25a62cdddfe3a45c2df11c66a42260e553d67eb45c576700c44cd7cb75b1b007` | P / P |

| M03-drop-entry-id-check | `eec838dffc7c64ce22f5261ae107d6393e1739a71beb0417d80da5ecc3845a4d` | P / P |

| M04-drop-S089-base-absence | `c52d1ce859c6386fd2ca7d3870173664a33178da4937d6562bf7b7569d51598e` | P / P |

| M05-allow-inherited-PROVINCE | `af75f67343fca5c1eb99dcc1a0a0ab75a61e037fa607f020c0badd1f332d4020` | P / P |

| M06-freeze-max-time | `48786bfbea6c5c9d82f6413387c50e20415d742056eff3e4832a74d079fd5308` | P / P |

| M07-added-max-time | `15580ed3c2ee432e7e8fd34d9cfefa200cf711645b5e6aab8eb2584c3292bc5f` | P / P |

| M08-entry-reads-worktree | `510cffc99222855ea2f9adec6c5349f8c8404658fc80ab584c8d22a6ec8ef04b` | P / P |

| M09-drop-committed-package-comparison | `079c7265257bad34dde90d4c85a7a032162e7834e460da1e30b6cdc142540aa6` | P / P |


**[OBSERVATION]** The runner’s `finally` paths restored the active tested file and all nine edited snapshot files to exact pristine bytes. It ran S and F again on restored active bytes for each mutant. The lane source before/after hash and active final hash are all P. Mutations are retained only as the unified evidence patch `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutations.patch`; the nine `.py` snapshots themselves are restored. Per-phase source hashes and final per-snapshot hashes are in the receipts/results.

**[OBSERVATION]** All started commands completed under their bounds; no background service/process was left running. No tool was installed or updated. Existing Python and Git sufficed, and no package-manager transaction was attempted.

## Opened primary/local instruction sources

Access date for every row: **2026-10-23**. Sources were opened by local reads only; no browser, HTTP request, bot challenge, or access-control bypass was used. Hashes cover the complete source-file bytes. Quotes are at most 25 contiguous words; line numbers locate them. Generated receipts and copied/restored code are evidence artifacts listed separately.

| URL | SHA-256 | Located quote |
|---|---|---|

| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | L182: `def committed_check(committed, live, tuples, entry_text, env_added, freeze_ct):` |

| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | L6: `the first commit that adds it is the freeze commit.` |

| file:///home/vgpnk/.omp/agent/RULES.md | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | L14: `Record every install or update` |

| file:///home/vgpnk/.agents/skills/godspeed/SKILL.md | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | L12: `Name the axes.` |

| file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | L14: `complete source repository, use normal repository tools and do not run REA` |


## Artifact inventory

All 136 deliverable/supporting files below have absolute paths and SHA-256 values. Raw stdout/stderr are complete; empty stderr files are intentionally retained. The working clone’s inherited repository contents are workspace, not duplicated deliverables; its changed fixture files and transferable history bundle are listed. The standalone inventory `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/artifact-sha256.tsv` lists all other entries (excluding itself).

| Absolute artifact path | SHA-256 | Bytes |
|---|---|---:|

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/active/c1-rust-positive.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/artifact-sha256.tsv` | `d74118bb9e8f47f491f40ce55d65e8317924bc831a9a5208c126327d76e5ec7d` | 23988 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/before-hashes.json` | `61f4c9814769ecb2f2301007fc5c8098db857acae56e0d10bfd725fa21e9c847` | 1056 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/build_fixture.py` | `31829fac22120afbe85ab32fc068f3dac4a9ef3ea4acd52845a9ccd5fcf9b278` | 4742 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/bundle-command.json` | `04c1ae6a9ef488b4ab718791e582560a129a1241afdb665665d1197fb70bf40c` | 539 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/c1-rust-positive.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/clone/.ufo/waves/round-30/claims.json` | `0c69dec0c23435d5486d29edd08e93f6c90c2a45c8dd939ecb5f8e37c4328a58` | 26 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/clone/PROVINCE.md` | `9c8a102befe1270bc45d63c93df8bfec30abeb923cf383eaf01dd413cbb659a9` | 37381 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/clone/corpus/SOURCES.md` | `43f3f91d40cbeb6f5f7cbdadec4b13b526cac0e198605df2ef39dbbae78282a9` | 101824 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/clone/corpus/evidence/round-30/c1/mutation-fixture-record.json` | `0c69dec0c23435d5486d29edd08e93f6c90c2a45c8dd939ecb5f8e37c4328a58` | 26 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` | `be1ca3f1787a9fe9bf8d6fe75237518c55b985ebf334e602278d147ca3f2f338` | 59 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/commands.json` | `0a75f0fc9d27bda4045dfde4ba0a4d611043cf75320205e27be2d8f88ce8d906` | 130047 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/detect_fixture.py` | `fdf07829339f9c0fdb1930c3059a02743b7aec891ecad968ead6936b7cedf25a` | 4535 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/fixture-build-commands.json` | `399973ba1d7fe40ae6f46d9a430810782b209e5cd0babf0321e7b7da5e663e86` | 5908 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/fixture-history.bundle` | `c73c3e0d4563568b0a2fad033393bc6eb94a4ba4a591cbbe37c2adce21051118` | 2239 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/fixture.json` | `a8d9d253c36067881fc1ebf93128a523993d36c4859da5b5d29c78136b3d7e06` | 649 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M01-freeze-strict-less.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M02-drop-evidence-id-comparison.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M03-drop-entry-id-check.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M04-drop-S089-base-absence.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M05-allow-inherited-PROVINCE.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M06-freeze-max-time.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M07-added-max-time.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M08-entry-reads-worktree.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutants/M09-drop-committed-package-comparison.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | 15679 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/mutations.patch` | `bbfb42227b6601dfbb89191121987e3386e1c106da25c2cdd06ac26ebb36c695` | 4888 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.mutated.fixture.stdout` | `b7c68428f8098bf9076b58a40ddea355d3d221bd3a292bda24c2c164048baa25` | 1314 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.mutated.selftest.stdout` | `04b02d2a9d7f5aad18bbd9b99dd45b24f08310ba771c26e2386fe54ac16704b0` | 1659 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M01-freeze-strict-less.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.mutated.fixture.stdout` | `aa78447c09aba6576bf6dece24a7ecb555a08c291cc62a3bc57d2898d635cc46` | 1319 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.mutated.selftest.stdout` | `5136ada19e97bc772ba61ba6086c6a5ce9fd65294b2292a410de073e86f699c1` | 1671 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M02-drop-evidence-id-comparison.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.mutated.fixture.stdout` | `f104751b22f7785279872d4da39573e871c35fde42c8161252c89353de3b9177` | 1342 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.mutated.selftest.stdout` | `2f5c52fe023fd1632f3b232061dea03d8f7f077342ade24a4e0ff50e9920c462` | 1690 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M03-drop-entry-id-check.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.mutated.fixture.stdout` | `4accbcaa38b7dd4125403b1700fe6bc81e12f3079f10583a5c4e9b572102835f` | 1341 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.mutated.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M04-drop-S089-base-absence.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.mutated.fixture.stdout` | `6dd3c0261fad8443dccec090ddc85e8aeaa9be810d63418a487615f17cb289f6` | 1340 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.mutated.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M05-allow-inherited-PROVINCE.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.mutated.fixture.stdout` | `d7f16e75f6dd8fca6c0fba477e822a13afca91f21b3d075b89f6bf4533db36d9` | 1368 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.mutated.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M06-freeze-max-time.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.mutated.fixture.stdout` | `4c76ffc275165a780a1f1c89d0c74c39948aed72919175348cd68583f45e1353` | 1368 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.mutated.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M07-added-max-time.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.mutated.fixture.stdout` | `54b21366fe377a8b5957752cf93abf78506fc133482828add3d794f0472a629d` | 1341 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.mutated.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M08-entry-reads-worktree.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.mutated.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.mutated.fixture.stdout` | `afe6e5b9cb0d5cbedc333fb17759dfaca40ae0fca4aa94d244647c465798a3a2` | 1335 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.mutated.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.mutated.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.pristine.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.pristine.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.pristine.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.pristine.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.restored.fixture.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.restored.fixture.stdout` | `ffc9837b906c352f10562e3334a0e7b887ae927216b5cf2c1041e542c7e9aacc` | 1366 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.restored.selftest.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/outputs/M09-drop-committed-package-comparison.restored.selftest.stdout` | `bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18` | 1711 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/results.json` | `12be1895a4e760d043cc588ca138b5f77d60a9397dae09bb976624fa97812d43` | 11877 |

| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Committed/run_probes.py` | `8497db7f1559581806612e12e4de1fe36f6ef8ba74132095b001734ee5772a6d` | 6085 |


Report: .ufo/waves/round-30/w1/MutC1Committed.md
