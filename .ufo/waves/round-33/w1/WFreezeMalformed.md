# WFreezeMalformed — malformed freeze-map boundary probe

## Scope and verdict

**Malformed/empty inputs can print CLEAN and exit 0.** This is a limit of interpreting the freeze-integrity gate as an input/schema validator, not a new admission result or a claim that valid Round-32 pin maps failed.

- Axes: input-boundary depth; distinguish CLEAN from rejection/crash; exact byte restoration; containment.
- One challenged defect: missing claims-map shape/completeness validation at `tools/round-33/freeze-integrity.py:265-267`. Fifteen input variants delimit that one boundary; no gate code was mutated or repaired.
- Seven input mutants survived the stronger input-validation expectation; eight were killed by nonzero exit, including five unhandled exceptions. No inconclusive case: all 15 pristine and all 15 restored detector runs exited 0 with `CLEAN pins=1`.
- This is seat-produced lane advice, not outside/non-author verification. R33-C1 remains **STOPPED UNPROVABLE** per `.ufo/waves/round-33/claim-stop.json`; no carrier rows, replacement benchmark, or claim gain are supplied.

## Measured source and execution

Pinned revision and observed lane HEAD at materialization: `d7076120e4f00c6d18aa77b8764d14861e820eb2` (claim-stop base `428315a8f5674b952def862910af6e07a6c2224b`). Gate bytes were obtained with read-only `git show <pinned-revision>:tools/round-33/freeze-integrity.py` and materialized only under:

`/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeMalformed/`

Gate SHA-256 before **and** after the experiment:

`a753b1d70ce8d7062fe9ffae8a31d90eb21fe26c30649d51bd95bd68ad656bb2`

The observed working file matched those pinned bytes when materialized. Round-32 gate SHA-256, read for source context only: `6b5aa1dfcaef04b8d6e58babebf826d677d6eeecc8b13906213dfd8f041804cd`.

Actual driver argv:

```text
/usr/bin/python -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WFreezeMalformed/probe.py
```

- Start UTC: `2026-10-23T09:34:13.115616+00:00`
- End UTC: `2026-10-23T09:34:14.947435+00:00`
- Duration: 1.831798 seconds; exit 0; stderr empty; no timeout. Driver exit 0 means the experiment completed, **not** that the gate rejected every mutant.
- Detector interval: `09:34:13.135644`–`09:34:14.942943` UTC, 1.807291 seconds.

Representative actual detector argv (empty-map mutant):

```text
/usr/bin/python -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WFreezeMalformed/freeze-integrity.py --root /fast/scratch/hyaku/kaidoku-r33/w1/WFreezeMalformed/repo-empty_maps --round 99 --rev 9db15487c33354fb52828b9bff199ed1befc1750
```

`receipt.json` retains every actual setup/detector argv, start/end UTC, exit, stdout, stderr, timeout flag, fixture hashes, tree/commit IDs, and restoration result. `driver.json` retains full driver stdout/stderr separately.

## Detector and mutation method

Every case starts with the same valid text-only fixture:

```json
{"frozen_inputs":{},"instruments":{"artifact.txt":"27c24cca957fdbd629282fd3e6d35af1238d1ea62db67525f5a66ae0354b916f"}}
```

The sole pin is a 37-byte text artifact, never executed. The fixture also has an inert README. Each case has its own tiny Git repository. Pristine, mutated, and restored bytes are committed as separate **parentless** snapshots using `git commit-tree`; the unchanged detector is run against each explicit commit ID. This is necessary because the gate reads claims at their first-add commit: appending a claims edit after a pristine freeze would not test malformed freeze input. No lane/fleet Git writes or checkout resets were used.

Expected detector for this probe: valid baseline/restoration produce `CLEAN pins=1`; a malformed/no-required-pin input must not produce successful CLEAN if CLEAN is to be used as an input-validation certificate. Missing claims with no reachable adding commit must produce exit 2; a referenced but absent pin must produce exit 1/FAIL. The stronger schema/completeness expectation is **not** asserted to be the gate's documented contract.

## Actual mutant results

All rows have pristine exit **0/CLEAN pins=1** and restored exit **0/CLEAN pins=1**. `I` denotes `instruments`, `F` denotes `frozen_inputs`; unchanged fields retain baseline values. Table output excerpts omit only freeze/rev suffixes; complete exact output is in the receipt.

| Case / input mutation | Mutant exit | Actual finding/output | Verdict against input-validation expectation |
|---|---:|---|---|
| `empty_maps`: replace sole nonempty `I` with `{}` | 0 | `freeze-integrity: CLEAN pins=0` | survived |
| `omitted_instruments`: remove `I` | 0 | `freeze-integrity: CLEAN pins=0` | survived |
| `no_pin_keys`: claims `{}` | 0 | `freeze-integrity: CLEAN pins=0` | survived |
| `empty_list_map`: `I=[]` | 0 | `freeze-integrity: CLEAN pins=0` | survived |
| `empty_string_map`: `I=""` | 0 | `freeze-integrity: CLEAN pins=0` | survived |
| `pair_list_map`: `I=[["artifact.txt", correct_digest]]` | 0 | `ok` artifact row; `freeze-integrity: CLEAN pins=1` | survived, non-object map coerced |
| `null_map`: `I=null` | 1 | stdout empty; `TypeError: 'NoneType' object is not iterable` | killed by exception, not controlled validation |
| `nonempty_string_map`: `I="bad"` | 1 | stdout empty; `ValueError: dictionary update sequence element #0 has length 1; 2 is required` | killed by exception |
| `malformed_json`: truncated `{"instruments":` | 1 | stdout empty; `json.decoder.JSONDecodeError: Expecting value: line 1 column 16 (char 15)` | killed by exception |
| `top_level_array`: claims `[]` | 1 | stdout empty; `AttributeError: 'list' object has no attribute 'get'` | killed by exception |
| `bad_digest`: digest `"not-a-sha256"` | 1 | `FAIL` artifact row; `freeze-integrity: FAIL pins=1 changed=1` | killed by digest mismatch, not format validation |
| `empty_list_frozen_inputs`: `F=[]` | 0 | `ok` artifact row; `freeze-integrity: CLEAN pins=1` | survived, wrong map type accepted |
| `null_frozen_inputs`: `F=null` | 1 | stdout empty; `TypeError: 'NoneType' object is not iterable` | killed by exception |
| `missing_claims`: omit claims from root snapshot | 2 | `freeze-integrity: ERROR no commit adds .ufo/waves/round-99/claims.json at e5d7d32671ccd385cb333731eb130a6d7f6cd42f` | killed, expected missing-freeze path |
| `missing_pinned_file`: omit artifact, retain correct digest | 1 | `FAIL\tartifact.txt\tsha=absent\tcommits_after_freeze=0`; `freeze-integrity: FAIL pins=1 changed=1` | killed, expected absent-pin path |

The smallest surviving mutation's complete stdout was:

```text
freeze-integrity: CLEAN pins=0 freeze=9db15487c333 rev=9db15487c33354fb52828b9bff199ed1befc1750
```

Its stderr was empty. In source, `.get(key, {})` supplies missing maps and `dict.update` accepts empty iterables or key/value-pair lists. With zero merged pins, no per-pin loop executes, `bad` remains zero, and line 281 prints CLEAN. Thus CLEAN is not a claims-schema certificate. This result is **not fixed, waived, or blessed** here.

## Exact restoration and hashes

For every case, the receipt records identical before/after hashes for all three fixture files, the same restored Git tree, and byte-for-byte restoration of the saved Git index. Scratch gate bytes were unchanged. New Git objects are retained as experiment evidence; this is byte restoration of mutated fixture files and index, not a claim that the entire Git object directory reverted.

Common pristine **and restored** SHA-256:

| Target | SHA-256 |
|---|---|
| claims (119 bytes) | `0c4872d95a9fe0ef7c5b83191b581e60e0a7889c784690b4b876f3e78744f2e1` |
| artifact (37 bytes) | `27c24cca957fdbd629282fd3e6d35af1238d1ea62db67525f5a66ae0354b916f` |
| README (48 bytes) | `2878b2bdee149c318ec1dc967b0be0acd6ac8016fd1a9a33022522c4c79ded92` |

Common pristine/restored tree: `4e8144002642ad6b6c2b8160002fa6132c940dff`.

Mutated claims SHA-256 (before/after are the common claims hash above):

| Case | Mutated SHA-256 |
|---|---|
| empty_maps | `c11182fdd8a2c3eb8c9e0d7685137d4e74f5b8ff447280a8953b4d505ba7ac90` |
| omitted_instruments | `8feffa2911479dc4333f6643c8a08bc84041514839079714cfb4d175d03a3711` |
| no_pin_keys | `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356` |
| empty_list_map | `8c8dacd5631fa2f0abc22f8f7649d78f98f603747c18fc23755e6574ee5fdcb7` |
| empty_string_map | `6f7d03d54f31b157256757decaa6af2622bd1bc4cfc9e8bd8dbb7c6fdde739a6` |
| pair_list_map | `bdce47ad3c708c450eb704d8cae0b0d72ba74292b7770bac6125fdc3d8273a49` |
| null_map | `f6ef5aa104ebbe1b013e57da5ab3fae7dbcc0e2cd12329e2661aac2d1d7d2ffe` |
| nonempty_string_map | `24b0df36f42ebda68679f1a939df979ec7b1ff2b8664da500a2d99b8faf706ac` |
| malformed_json | `07078110e18904af10b23323f6e4d53e2b7b9aa0ae3dd0bcbe28367ebd9bd79b` |
| top_level_array | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |
| bad_digest | `806b7ca710b9d20fa24c673d466b530d3953663fa11c0cd9091addcdc36405e2` |
| empty_list_frozen_inputs | `baba3085d8268b9fa82b65412e1553c9ce14be8cd4582cbb910e428a146638ae` |
| null_frozen_inputs | `ec1cafde83cef4944e0abd2c9c84f29fb4c6955c16c56974121f675621b38afa` |
| missing_claims | absent, restored exactly |
| missing_pinned_file | claims unchanged; artifact absent, then restored exactly |

## Distinction from valid Round-32 pin maps

Only selected-revision map shapes/digests were inspected; no production gate, production fixture, or carrier manifest was executed. At the pinned revision:

| Round-32 claims file | `instruments` / `frozen_inputs` counts | SHA-256 |
|---|---|---|
| `.ufo/waves/round-32/claims.json` | dictionary 4 / dictionary 4 | `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435` |
| `.ufo/waves/round-32/claims-v2.json` | dictionary 2 / dictionary 0 | `805a05146515580d644074792db3d84a241307e65fbd9c54b916b762d82e5609` |
| `.ufo/waves/round-32/claims-v3.json` | dictionary 2 / dictionary 0 | `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` |

All inspected pin keys were nonempty strings and values lowercase 64-character SHA-256 hex. Empty `frozen_inputs: {}` is therefore an observed valid form; this report does **not** propose requiring every map to be nonempty. The zero-total-pin and non-object-map probes differ from these supplied, nonempty aggregate pin maps. They do not establish a failure of valid-map digest/history checking. Nor does this shape-only inspection independently certify the Round-32 measurements or freeze-commit contents.

The experiment covers root-commit malformed/absent inputs, not claims deleted after a valid freeze, descendant tamper/restore history, custom claims paths, or arbitrary Git failures. No conclusion about those paths is inferred from these results.

## Containment, limits, and evidence custody

- Production lane was read-only except this assigned report. All fixtures, Git objects, code copies, and receipts are under the private seat directory above. Git override variables `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` were removed. System/global Git configuration, prompts, optional locks, and hooks were disabled for scratch operations.
- No native/carrier fixtures or execution, held data, R33FixtureBuilder material, held derivatives, alternate study, REA/MCP calls, source/config writes, host-service changes, subagents, or background jobs were used.
- Experiment caps: 120-second overall alarm; 5 seconds per command; 140-second outer driver timeout; inherited 256 MiB address-space, 30 CPU-second, 64-FD, no-core, and less-than-1-MiB file limits. Fixture payloads are at most 121 bytes. Process groups were SIGKILL-cleaned after every command; wrapper accounting ended with zero active groups, without an independent process census.
- Subprocess budget: 512 reserved total; 420 reserved upper-bound slots used; 195 direct commands actually recorded. Gate descendants were budgeted from the inspected source's bounded Git calls, not kernel process telemetry. Execution was sequential, with at most one detector and its one Git child. This was not a per-UID kernel process-count limit.
- Limits disclosure: preliminary read-only Git extraction/version calls had 10-second wall bounds but did not inherit the experiment's memory/file/CPU limits. No limit was retroactively repaired by adding a different detector.
- Tool installs/updates: none. Existing Git `2.56.0`, Python `3.14.8`. An auxiliary inventory command's `timeout --version` returned 125 with usage requiring `<COMMAND>`; no detector used that executable. Detector timeouts used Python `communicate(timeout=...)` plus the overall alarm.

Retained evidence, relative to the private seat directory:

| File | Bytes | SHA-256 |
|---|---:|---|
| `freeze-integrity.py` | 11777 | `a753b1d70ce8d7062fe9ffae8a31d90eb21fe26c30649d51bd95bd68ad656bb2` |
| `probe.py` | 12109 | `87f9d070ff2258963029c9b492268c65b6cdaf4ef5cc3fcc4b625bb982511dc3` |
| `preflight.json` | 38302 | `ade39ceb4f0cdafe29e1d0ff51f4f7a50c1ed10b1ef3beafe175be7145ef39d8` |
| `driver.json` | 6449 | `9d9224eac5296357880d7833f2f65807ec080e4b647a708886b458a3cb53d61d` |
| `receipt.json` | 218724 | `04e6e8d4c9ed8dc565784005551ff5d00f82566da3f7e91d2085b557a8ea2427` |

No production fix, integration, admission judgment, or further experiment was performed.
