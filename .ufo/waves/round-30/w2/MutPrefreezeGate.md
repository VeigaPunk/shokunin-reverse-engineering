# MutPrefreezeGate: own-selftest mutation probe

## Result and scope

**Observation — 14 independent, single-clause mutants: 8 killed, 6 survived, 0 inconclusive.** All 14 pristine baselines and all 14 restored runs exited 0 with the exact stdout line `selftest cases=20 failures=0`. There were 42 detector invocations in total. Every mutant changed one production-logic line; the selftest and its expected results were unchanged.

**Attack verdict: fails to detect all selected regressions.** The concrete counterexamples are surviving mutants M06, M07, M08, M09, M12 and M14. This is a selftest-coverage finding, not a finding that the pristine gate accepts those invalid inputs. No contract was changed and no fix was integrated.

Axes: detection sensitivity; isolated exact-byte restoration; reproducible bounded evidence.

Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/prefreeze-gate.py`.

Scratch: `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/`.

Observation — source SHA-256 before and after the probe, pristine-copy SHA-256, and every mutant-copy SHA-256 before mutation and after restoration:

```text
1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542
```

## Detector and bounds

Observation — the two orchestration commands were:

```sh
timeout --signal=TERM --kill-after=10s 850s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/probe.py baseline
timeout --signal=TERM --kill-after=10s 850s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/probe.py mutated
```

Both orchestration commands exited 0. The latter printed this exact final line:

```text
{"counts": {"killed": 8, "survived": 6}, "errors": []}
```

The baseline phase completed at `2026-10-23T03:15:16.951367Z`; the mutation/restoration phase completed at `2026-10-23T03:15:52.386541Z`. Each worker invoked only the assigned `--selftest`, with at most four isolated workers active. Git writes made by the selftest were confined to its scratch temporary fixture repositories. Every detector was bounded by GNU timeout, with a 90-second deadline and a five-second kill grace. No invocation timed out. Restoration was in a `finally` block, including a final exact-byte copy for every mutant.

The working directory for every detector command was `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/`. For each ID, the **same literal command below** was used on pristine, mutated and restored bytes:

```sh
# D01
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M01.py --selftest
# D02
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M02.py --selftest
# D03
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M03.py --selftest
# D04
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M04.py --selftest
# D05
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M05.py --selftest
# D06
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M06.py --selftest
# D07
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M07.py --selftest
# D08
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M08.py --selftest
# D09
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M09.py --selftest
# D10
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M10.py --selftest
# D11
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M11.py --selftest
# D12
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M12.py --selftest
# D13
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M13.py --selftest
# D14
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/tmp timeout --signal=TERM --kill-after=5s 90s python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M14.py --selftest
```

Complete stdout, stderr, literal argv, start/end UTC timestamps and per-phase hashes are retained in `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/results.json`, under `runs.M01` through `runs.M14`. Every detector stderr was empty. An exit 1 was counted as a kill only with a passing baseline, an actual `FAIL` selftest row, and a passing exact-byte-restored run; harness errors and timeouts would have been inconclusive.

## Mutant table

Line numbers refer to the target source snapshot above. Changes are independent, not cumulative. Expected checks are predictions from the pristine selftest source; actual results are observations.

| ID / command | Line | Single-clause change | Expected detector case or missing coverage | Actual exit / exact stdout summary | Verdict |
|---|---:|---|---|---|---|
| M01 / D01 | 194 | `at_freeze is None` → `at_freeze == ''` | `pin_absent`, `r29_keys`, `r30_list_absent` | 1; `selftest cases=20 failures=3` | killed |
| M02 / D02 | 199 | `digest != at_freeze` → `digest == at_freeze` | `pin_mismatch`, `clean` | 1; `selftest cases=20 failures=6` | killed |
| M03 / D03 | 124 | envelope directory slice `parts[:-1]` → `parts[:1]` | `envelope_at_freeze`, `runs_before_freeze` | 1; `selftest cases=20 failures=2` | killed |
| M04 / D04 | 124 | filename `'runs.tsv'` → `'run.tsv'` | `runs_before_freeze` | 1; `selftest cases=20 failures=1` | killed |
| M05 / D05 | 212 | unpinned condition `and` → `or` | `clean`, `tool_pinned`, `tool_superseded` | 1; `selftest cases=20 failures=5` | killed |
| M06 / D06 | 157 | remove `.strip()` from supersession-reason predicate | Whitespace-only reason case missing | 0; `selftest cases=20 failures=0` | survived |
| M07 / D07 | 113 | pin-group node type `list` → `tuple` | Top-level list-valued pin-group case missing | 0; `selftest cases=20 failures=0` | survived |
| M08 / D08 | 90 | reject `!= b'blob'` → reject `not in (b'blob', b'tree')` | Tree/directory pin rejection case missing | 0; `selftest cases=20 failures=0` | survived |
| M09 / D09 | 177 | first-add selector `added[-1]` → `added[0]` | Claims deletion/re-addition case missing | 0; `selftest cases=20 failures=0` | survived |
| M10 / D10 | 179 | read claims at `freeze` → `measured` | `late_pin_not_counted` | 1; `selftest cases=20 failures=1` | killed |
| M11 / D11 | 223 | return `1 if findings else 0` → `0 if findings else 1` | All evaluable clean/flagged cases | 1; `selftest cases=20 failures=16` | killed |
| M12 / D12 | 222 | verdict condition `if findings` → `if not findings` | Returned verdict consistency assertion missing | 0; `selftest cases=20 failures=0` | survived |
| M13 / D13 | 157 | nonempty supersession-reason conjunct → `True` | `tool_supersession_no_reason` | 1; `selftest cases=20 failures=1` | killed |
| M14 / D14 | 51 | supported key `'frozen_inputs'` → `'frozen_input'` | `frozen_inputs` pin-group case missing | 0; `selftest cases=20 failures=0` | survived |

### Exact killed-mutant output excerpts

Observation — these excerpts came from the indicated producing commands. Exact mutated-run completion UTC times are in the next table. Full output, including every other failing row, is in the raw record.

```text
D01: FAIL r30_list_absent got=code=0 codes=[]
D02: FAIL pin_mismatch got=code=0 codes=[]
D03: FAIL envelope_at_freeze got=code=0 codes=[]
D04: FAIL runs_before_freeze got=code=1 codes=['DATA_BEFORE_FREEZE']
D05: FAIL tool_pinned got=code=1 codes=['TOOL_UNPINNED']
D10: FAIL late_pin_not_counted got=code=0 codes=[]
D11: FAIL pin_absent got=code=0 codes=['PIN_ABSENT']
D13: FAIL tool_supersession_no_reason got=code=0 codes=[]
```

Inference — D04 is killed despite its retained finding category and exit code because the mixed fixture's required `runs.tsv` path is missing. The pristine detector also checks required finding paths at target line 299; the companion envelope finding alone is insufficient.

### UTC and restoration evidence

Observation — all times below are on **2026-10-23 UTC** and are actual command completion times. Every pristine and restored invocation had exit 0 and the exact line `selftest cases=20 failures=0`; the mutant exit and summary are in the mutant table. Each row uses its D-command unchanged for all three phases.

| ID | Pristine completed UTC | Mutated completed UTC | Restored completed UTC |
|---|---|---|---|
| M01 | 03:15:16.080590Z | 03:15:50.164587Z | 03:15:50.459045Z |
| M02 | 03:15:16.066699Z | 03:15:50.170892Z | 03:15:50.467583Z |
| M03 | 03:15:16.077694Z | 03:15:50.172268Z | 03:15:50.463670Z |
| M04 | 03:15:16.105962Z | 03:15:50.172559Z | 03:15:50.471751Z |
| M05 | 03:15:16.366735Z | 03:15:50.750398Z | 03:15:51.063342Z |
| M06 | 03:15:16.376840Z | 03:15:50.758639Z | 03:15:51.069211Z |
| M07 | 03:15:16.376494Z | 03:15:50.752675Z | 03:15:51.062856Z |
| M08 | 03:15:16.399188Z | 03:15:50.760523Z | 03:15:51.072033Z |
| M09 | 03:15:16.655794Z | 03:15:51.374375Z | 03:15:51.713906Z |
| M10 | 03:15:16.672233Z | 03:15:51.381922Z | 03:15:51.723997Z |
| M11 | 03:15:16.674243Z | 03:15:51.382795Z | 03:15:51.721487Z |
| M12 | 03:15:16.690818Z | 03:15:51.386354Z | 03:15:51.729501Z |
| M13 | 03:15:16.928002Z | 03:15:52.047386Z | 03:15:52.350995Z |
| M14 | 03:15:16.950883Z | 03:15:52.057749Z | 03:15:52.362762Z |

Observation — every `before_sha256`, `restored_sha256` and `final_sha256` in the raw record equals the common pristine hash stated above. Mutated bytes had these distinct hashes before restoration:

| ID | Mutated SHA-256 |
|---|---|
| M01 | `ad1f39a079caa556bd0baa05f94b89190342655be53cd973ecf9e0943da059bb` |
| M02 | `951d7e1223cfcfa29d9de6d61465c74b32a6e0922210ea27bc7967dcdac925ed` |
| M03 | `7723a4a7b123d69e53720645699ef5e230dd649134ee7707ca524db236097b0a` |
| M04 | `3d85d64ac097978915b71b0c071a91ab84ded4d2212420d5ff790c1218c1e0fc` |
| M05 | `3fda2cdd9360690a83e44d3e3b2cc33eb39402d5662902fafede5cbe3576587a` |
| M06 | `3fcc79d59bfbcff3c0c08f1a28808130cdacf65f01a638068e966168a0343353` |
| M07 | `b18aba9be5a4d77d41713f39283bab1e62d5700052d2b4fa8aea21554ee6172d` |
| M08 | `3618247a5e7ad31e669d38eef7ceee1434a68031d70a0d0d30546a9419223b01` |
| M09 | `634dade3395cb2c1b6897b69d2f0ad9ac15043f01dceb3482e88f7b6bccbcc7b` |
| M10 | `2acea370116ebf891982c2a5126a66b58cdfddf732a1db249d1d23d82be55607` |
| M11 | `794f2604acc04d81d44a2dc553582f64bd9aa18ec5a55b7d56a32a9285df4692` |
| M12 | `6bc289853540c2e8664810b3fdff82b77780a74f5984be4d26dd5a5db4b7ae09` |
| M13 | `5580ccb728382694761cab3b908e08ce26e6c25ab333d16d142c711604cad969` |
| M14 | `ea27fbb73c6db171f47f46e0f774cb982b4a968eec2036af9331dde1ede393ff` |

## Survivors as missing cases

Observation — D06, D07, D08, D09, D12 and D14 each exited 0 with `selftest cases=20 failures=0` on changed production bytes. The following are **inferred missing fixtures/assertions**, not additional tests executed in this assignment:

| Survivor | Missing case / expected contract assertion |
|---|---|
| M06 | A supersession with a reason such as spaces or a tab must not excuse an otherwise unpinned named tool: expect `TOOL_UNPINNED`, exit 1. The existing empty-string reason case does not exercise whitespace normalization. |
| M07 | A top-level JSON list-valued `loaded_by_counter` containing an absent path must produce `PIN_ABSENT`, exit 1. Existing round-30 list cases exercise lists nested inside a dictionary, not the `elif isinstance(node, list)` branch. |
| M08 | Record an existing directory/tree path in a nested list-valued pin group: it must still produce `PIN_ABSENT`, exit 1, because the contract requires a blob, not merely an existing Git object. This avoids relying on a digest mismatch to reject the wrong object type. |
| M09 | Add the claims file, delete it, and re-add it with different pin state. Assert the original first-add freeze commit is retained, e.g. an absent original pin is still `PIN_ABSENT` even when the re-added claims omit it. Existing fixtures have only one claims-file addition. |
| M12 | For existing clean and flagged fixtures, assert `result['verdict']` agrees with both findings and the returned exit code. The selftest checks code, finding categories and required paths, but not the verdict field; the inverted output verdict therefore survives even on already exercised inputs. |
| M14 | Put an absent or mismatched pin under `frozen_inputs`, with no duplicate pin in another group: expect `PIN_ABSENT` or `PIN_MISMATCH`, exit 1. No current fixture supplies this supported pin key. |

Unknown — no expanded selftest, repaired gate, live R30 counter or REA behavior was evaluated. Survival is not permission to narrow the gate's documented contract.

## Retained artifacts and hashes

Observation — the following is the complete retained file inventory under the assigned scratch directory. The temporary-fixture and unused log directories were empty after the probe. All mutation-source copies listed here contain restored pristine bytes; exact single-line mutation recipes are retained in the manifest, and pre-restoration mutant hashes and raw output are retained in the results record.

| Absolute artifact path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/pristine.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/probe.py` | `65b0bffa4129ab315e1f9c8cac18c39595df0b1fb5255d4c58b3f570ee3d93bc` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/manifest.json` | `0e43d1b239d4890581955a4ecbce2df0eb716de1e07ffb17401db246f932498a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/results.json` | `6a9e50f3ad61f4bfb6d73f19b20392eda117d676cd1f73b42d7a18780739573a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M01.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M02.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M03.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M04.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M05.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M06.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M07.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M08.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M09.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M10.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M11.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M12.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M13.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutPrefreezeGate/mutants/M14.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` |

## Opened local sources

Observation — these sources were opened by ordinary local file reads, not browser automation. Access date for all entries: **2026-10-23**. Hashes cover the full file bytes; each located quote is at most 25 contiguous words.

| Source URL | SHA-256 | Located quote |
|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/prefreeze-gate.py` | `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` | Line 33: “`--selftest` builds throwaway Git fixture repositories in a temp dir and runs the same” |
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | Line 13: “2. **Iterate cheap, in parallel.**” |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | Line 5: “`sudo` is available.” |

## Tooling and boundary record

Observation — existing tools reported Python `3.14.8`, Git `2.56.0`, and GNU coreutils timeout `9.12`; the producing version commands and their exit-0 full output are in the raw record. **No tools were installed or updated.** No pacman transaction, REA invocation, carrier/mutant-binary execution, subagent dispatch, lane Git/JJ write, fleet mutation, or sibling-source edit was performed. Only the requested report was written inside the lane. The lane target's before/after source hashes are identical. All detector processes completed synchronously and their child Git commands were waited for; no background service or job was started.
