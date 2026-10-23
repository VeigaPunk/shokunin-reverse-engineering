# WTimestampSameLine — exact-line allowance mutation

## Scope and axes

- **Verdict: KILLED.** Inserting one synthetic event into the fifth allowed receipt line made the unchanged outer wrapper exit **1**, with `allowance_line_changed`, `detail=line_hash_mismatch`, and `tool_run=false`. The preceding four verified pins did not cause partial forwarding.
- Probe axes: **depth** (whole-line exemption integrity), repeatability (same CLI/spec/root across three byte states), and containment (private text-only fixtures and bounded processes). No lane score or admission gain is asserted.
- Observed admissible revision: `d7076120e4f00c6d18aa77b8764d14861e820eb2`; preserved receipt base: `428315a8f5674b952def862910af6e07a6c2224b`.
- Read `.ufo/waves/round-33/claim-stop.json`: **R33-C1 remains stopped/unprovable**. This is instrument/repair evidence only, not a carrier measurement or replacement study.
- All experiment files are beneath `S=/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampSameLine`. The only lane write is this report. No lane/fleet Git or jj writes, source edits, native artifacts, held outputs, classifier runs, REA/MCP, service changes, or subagents.

## Existing assets and mutation

Materialized the four existing timestamp selftest assets directly from the pinned revision into `S/assets/`. Ran the **unchanged** `build-hashed-fixture.sh` with `HASHED_FIXTURE_BASE=S/hashed-fixture`; its exit was 0, stderr empty, UTC `2026-10-23T09:33:25.070236Z`–`2026-10-23T09:33:25.123556Z`. This is the existing timestamp text fixture builder, not the held native-fixture item. Its other derived control clones were not tested.

Used only `S/hashed-fixture/clone-green` for the three detector invocations. The single mutation changed line 3 of `.ufo/waves/round-32/a2after/timestamps-strict-at-9ef97f08.txt`:

```diff
-{"allow":[],"findings":...
+{"utc_end":"2001-02-03T04:05:06Z","allow":[],"findings":...
```

The displayed hunk is abbreviated; **the complete actual patch** is retained at `S/commit-mutated.patch`, SHA256 `0010f0678cac329190e2f3acb00bd01d22af396f921b5465eaa3db00b2451e60`. It changes one line, adding 33 bytes, exactly the event insertion used by the existing selftest asset. No source/spec edits or re-pinning occurred.

Mutation commit `3adfeda72bf27123394024090cfd733ad7f69108` has author and committer time `2000-01-01T00:00:00Z`. Thus the inserted 2001 instant is historic wall-clock and later only than its synthetic introducing commit; it is **not observed execution evidence**. Commit argv, output, timestamps, and dates are retained under `S/receipts/commit-mutated*/` and `S/mutated-state.json`.

## Same bounded outer detector

For each state, the driver invoked this same command, changing only the output directory while `HEAD` selected the corresponding committed bytes:

```text
/usr/bin/timeout --kill-after=2s 90s /usr/bin/prlimit --nproc=4096 --as=1073741824 --cpu=90 --fsize=1048575 --core=0 --nofile=128 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WTimestampSameLine/assets/run-gate-hashed.py --root /fast/scratch/hyaku/kaidoku-r33/w1/WTimestampSameLine/hashed-fixture/clone-green --rev HEAD --path .ufo/waves/round-32 --spec /fast/scratch/hyaku/kaidoku-r33/w1/WTimestampSameLine/assets/allowances-hashed.json --out /fast/scratch/hyaku/kaidoku-r33/w1/WTimestampSameLine/wrapper-runs/STATE
```

Expected detector: unchanged bytes apply all five allowances and remain strict-green; the insertion must return exit 1 with `error.code=allowance_line_changed`, `tool_run=false`, and no `findings`. No baseline failure is counted as a kill.

| State | Actual start UTC | Actual end UTC | CLI exit | Observed output |
|---|---|---|---:|---|
| pristine | 2026-10-23T09:33:38.961753Z | 2026-10-23T09:33:39.040045Z | 0 | 5 allowances applied; 5 files; 6 findings; 0 unexempted; 0 skipped |
| mutated | 2026-10-23T09:34:26.178269Z | 2026-10-23T09:34:26.216929Z | 1 | `allowance_line_changed`; `line_hash_mismatch`; `tool_run=false`; no `findings` |
| restored | 2026-10-23T09:34:45.937606Z | 2026-10-23T09:34:46.022589Z | 0 | 5 allowances applied; 5 files; 12 findings; 0 unexempted; 0 skipped |

**All three stderr streams were empty.** Full argv, stdout, stderr, exit, UTC boundaries, stream hashes and process-cleanup observations are retained at `S/receipts/{pristine,mutated,restored}-wrapper/{command.json,stdout.txt,stderr.txt}`. Wrapper-generated receipts are separately retained at `S/wrapper-runs/{pristine,mutated,restored}/`.

Actual mutant stdout:

```json
{"error":{"actual_sha256":"cccf4e79322bd4e8b3dd7e64e2d0eb15e171afa9f264784ef3f5a01fe4798f01","code":"allowance_line_changed","detail":"line_hash_mismatch","expected_sha256":"3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03","file":"a2after/timestamps-strict-at-9ef97f08.txt","line":3,"message":"a2after/timestamps-strict-at-9ef97f08.txt:3 changed at 3adfeda72bf27123394024090cfd733ad7f69108; no allowance forwarded","verified_before_failure":["a2audit-gate.json:14","a2audit-settle.json:3","a2residual-dispatch.json:17","a2residual-settle.json:3"]},"schema":"r33-hashed-allow-gate-v1","tool_run":false}
```

The failure receipt contains `exit=1` and `tool_run=false`, with no forwarded tool argv. Source corroboration: `tools/round-33/timestamps/run-gate-hashed.py:213-245` verifies the complete pin loop before building the tool argv/`--allow` arguments; the mismatch returns from that loop. This probe exercised failure **after four successful pin checks**, not merely failure on the first entry. No syscall-level forwarding trace was added.

## Before/after hashes and exact restoration

| State | Receipt bytes | Whole-file SHA256 | Line-3 SHA256 (LF excluded) |
|---|---:|---|---|
| pristine | 1868 | `4619faa04e09ba87e0ef759d881147912c140c0552411856ffef83d6bd4306e4` | `3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03` |
| mutated | 1901 | `48ddfb72412c350b855d76831298b42aea730842010076d3551773c4f3023c46` | `cccf4e79322bd4e8b3dd7e64e2d0eb15e171afa9f264784ef3f5a01fe4798f01` |
| restored | 1868 | `4619faa04e09ba87e0ef759d881147912c140c0552411856ffef83d6bd4306e4` | `3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03` |

Restored the captured original line exactly, then committed restoration as `edf2b12e26fe0ba5d908cf366eaa06cb0bb68a11`. `S/restoration.json` records `exact_file_bytes_equal=true` and `whole_tree_equal=true`. Pristine commit `13493f8c29f4f6f8057160725694896f12b0158b` and restored commit have the identical tree `8443cd6b998a68ec3e6f54f7530fbb8320c52e37`; mutant tree was `bf11c4acbc83badac33d0b52363f12ae57a2d67a`. Full byte snapshots, state records and inverse patch remain in `S/{pristine,mutated,restored}-receipt-bytes.txt`, `S/{pristine,mutated,restored}-state.json`, and `S/commit-restored.patch`.

**Restoration limitation:** bytes/tree were restored, not commit history. The restoration commit also uses synthetic 2000 time; restored output attributes the receipt line to that time. [INFERENCE] This explains the 12 rather than 6 findings: more unchanged 2026 echo tokens are now later than their blame timestamp. All remain on the exact pinned line and all five allowances apply, so strict exit is still 0 with zero unexempted findings. This is not output-identical replay, nor a new contract or a surviving inserted-event mutant. No extra detector run or changed predicate was used to hide the difference.

## Instrument identity, bounds and retained evidence

Pinned source digests are retained in `S/sources.json`:

| Source | SHA256 |
|---|---|
| `run-gate-hashed.py` | `e011ed69e72bed408de30211712b2e65d69fd01b9c002a45eb7ce5acf6055bb0` |
| `allowances-hashed.json` | `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332` |
| `build-hashed-fixture.sh` | `37206762bb48cbdd7b7758b46eda3e8129728077a32c9d71bc98d96088465152` |
| `run-hashed-selftest.sh` | `d60840374bc75a4bc67d526248786405b00a4b6456dbfcbe7d38ccd03785770e` |
| original `evidence-timestamps.py` | `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00` |

A final SHA256 fact command found the scratch wrapper/spec, installed lane wrapper/spec, and original detector unchanged from these pins. The outer wrapper still read the original detector at its existing hardcoded lane path; it did not modify it. Receipt driver retained as `S/receipt-driver.py`, SHA256 `e9bb820b54c4a8b24953f34e7e8a29c43be32f28f0ceafc6f8f27f296bf60c83`; it only materializes trusted assets, invokes their builder/CLI, records results, and makes path-limited scratch commits. It does not author replacement fixtures.

Every driver subprocess had a 90-second GNU timeout plus 2-second kill grace, 1 GiB address-space cap, CPU 90 seconds, `RLIMIT_NPROC=4096`, no core dumps, 128 descriptors, and per-file writes capped below 1 MiB. The driver additionally caps its direct subprocess launches at 32 per invocation; this is not a measured tree-wide launch count. `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were removed; Git global/system configuration was disabled for scratch commands. All recorded process groups were absent after cleanup; no timeout fired and no background jobs remain. The full three-case selftest was **not** run; only this assigned pristine/mutant/restored outer-CLI probe was exercised.

Tools observed: Python 3.14.8, Git 2.56.0, GNU coreutils timeout 9.12, util-linux prlimit 2.42.4. **No installations or updates.** Preparation calls to unqualified `timeout --version` and `timeout --help` returned exit 125 (`<COMMAND>` required); measured commands used the working absolute `/usr/bin/timeout` instead. No detector failure or missed resource limit was retried.

## Result

**KILLED:** the event could not inherit the old line allowance, including when four earlier pins already verified. Pristine was green; mutant was refused before the underlying gate; exact receipt bytes and whole tree were restored and the restored strict gate was green. This is scoped lane advice, not independent outside verification, integration, or revived R33-C1 evidence.
