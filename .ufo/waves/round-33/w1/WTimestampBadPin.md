# WTimestampBadPin — wrong hash and missing allowed path

**Verdict: both assigned mutants killed.** Both pristine controls and both exact-byte-restored controls passed. On either fifth-row failure the outer CLI exited 1, reported `allowance_line_changed`, and executed neither the underlying timestamp gate nor any command carrying `--allow`, despite four earlier rows verifying successfully.

## Scope and axes

- Axes: whole-line integrity; atomic allowance forwarding; bounded reproducibility; exact-byte restoration.
- Observed lane HEAD and source pin: `d7076120e4f00c6d18aa77b8764d14861e820eb2`.
- Old text-receipt source: `428315a8f5674b952def862910af6e07a6c2224b`, `.ufo/waves/round-32`.
- Private root (all generated code copies, fixtures, patches and receipts): `/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampBadPin` (denoted **R** below).
- Private fixture clone pristine/restored revision: `13493f8c29f4f6f8057160725694896f12b0158b`.
- Only the green text fixture from shipped `tools/round-33/timestamps/build-hashed-fixture.sh:21-48` was materialized, then cloned with `--no-hardlinks`. Its five files are exact old Git blobs; the four source commit dates/messages follow that asset. No same-line/unlisted controls were generated or run. The deletion mutation commit is synthetically dated `2000-01-01T00:00:00+00:00`; no new event timestamp was inserted.
- Production source was read-only. The wrapper private copy is byte-identical to the pin; its existing hard-coded `TOOL` reads the unchanged lane timestamp detector. No wrapper/gate code was patched.
- This is timestamp repair evidence only. `claim-stop.json` remains authoritative: R33-C1 is stopped/unprovable. No carrier study, excluded builder material, held-item inspection, alternative benchmark, native execution, integration or runtime judgment was performed.

## Detector and actual outer results

Same bounded outer detector for pristine, mutated and restored states: `python3 -I -B R/assets/run-gate-hashed.py --root R/clone --rev HEAD --path .ufo/waves/round-32 --spec R/active-spec.json --out R/runs/CASE/wrapper`, traced with `strace -f -e trace=execve -s 32768`.

Every exact, expanded outer argv, start/end UTC, exit, stdout/stderr digest and cleanup outcome is retained in `R/runs/CASE/outer-receipt.json`; raw bytes are `outer.stdout`, `outer.stderr`, and `execve.trace`. The wrapper's own receipt/stdout/stderr are retained under each `wrapper/`. `R/command-index.json` also retains setup/Git argv and receipt paths.

| Case | Start UTC (2026-10-23) | End UTC | Outer exit | Timestamp findings / unexempted | Applied rows | Actual Python gate executions |
|---|---|---|---:|---|---|---:|
| `hash-pristine` | 09:35:55.982794Z | 09:35:56.110513Z | 0 | 6 / 0 | 5/5 | 1 |
| `hash-mutated` | 09:36:26.511017Z | 09:36:26.564855Z | 1 | not run | none forwarded | 0 |
| `hash-restored` | 09:36:56.399411Z | 09:36:56.534539Z | 0 | 6 / 0 | 5/5 | 1 |
| `path-pristine` | 09:35:56.111767Z | 09:35:56.234057Z | 0 | 6 / 0 | 5/5 | 1 |
| `path-mutated` | 09:37:55.799445Z | 09:37:55.862190Z | 1 | not run | none forwarded | 0 |
| `path-restored` | 09:37:55.867723Z | 09:37:55.998472Z | 0 | 6 / 0 | 5/5 | 1 |

All six outer stderr files contain **0 bytes**. Each green run scanned five text files, skipped zero files, and emitted identical stdout SHA256 `e39d28320c8820f8248b4dfed9b095d0c2e8f0abcb820c06ac88882b122af68f`. Failure payloads contain no `findings` field: that is gate refusal, not a zero-finding scan.

### Exact outer argv example: wrong-hash case

```json
["/usr/bin/timeout","--kill-after=2s","25s","/usr/bin/prlimit","--as=268435456:268435456","--cpu=20:20","--nproc=8192:8192","--nofile=128:128","--fsize=1048575:1048575","--","/usr/bin/strace","-f","-e","trace=execve","-s","32768","-o","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampBadPin/runs/hash-mutated/execve.trace","/usr/bin/python3","-I","-B","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampBadPin/assets/run-gate-hashed.py","--root","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampBadPin/clone","--rev","HEAD","--path",".ufo/waves/round-32","--spec","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampBadPin/active-spec.json","--out","/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampBadPin/runs/hash-mutated/wrapper"]
```

The other five expanded commands are retained individually, not inferred from this example.

## Mutant 1: one wrong allowance line hash

Only `active-spec.json:57`, the fifth allowance's first hash nibble, changed. Source receipts and wrapper/gate bytes were unchanged.

```diff
-      "line_sha256": "3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03",
+      "line_sha256": "4bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03",
```

Expected: exit 1, `allowance_line_changed` / `line_hash_mismatch`, `tool_run:false`, no gate or allowance forwarding. Actual outer stdout:

```json
{"error":{"actual_sha256":"3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03","code":"allowance_line_changed","detail":"line_hash_mismatch","expected_sha256":"4bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03","file":"a2after/timestamps-strict-at-9ef97f08.txt","line":3,"message":"a2after/timestamps-strict-at-9ef97f08.txt:3 changed at 13493f8c29f4f6f8057160725694896f12b0158b; no allowance forwarded","verified_before_failure":["a2audit-gate.json:14","a2audit-settle.json:3","a2residual-dispatch.json:17","a2residual-settle.json:3"]},"schema":"r33-hashed-allow-gate-v1","tool_run":false}
```

- Outer exit: **1**; stdout SHA256 `b3a07ab23ad1deac4dde2776b8ede25ce7c3472374f21acacaf0fdf0f99d9bc7`.
- Full retained spec: `R/mutations/wrong-hash-spec.json`.
- Exact unified diff: `R/mutations/wrong-hash-spec.patch`, SHA256 `6fc879340bdaafe4ed2d56b72b912be58dbea455a54514a08d75e56aceee9ac2`.
- Verdict: **killed**, with valid pristine and restored controls.

## Mutant 2: one allowed path absent from the gated revision

The spec was first restored exactly. Then only the old receipt `.ufo/waves/round-32/a2after/timestamps-strict-at-9ef97f08.txt` was deleted in the private clone and committed as `3ebc9081362acf3aa5c80aa3d4627fcd7b8ee87d` (parent is the pristine revision; author/committer date is synthetic 2000). The other four receipt files, wrapper/gate code and all five spec entries were unchanged. This tests an absent Git blob, not merely a missing worktree file.

Expected: exit 1, `allowance_line_changed` / `path_missing`, `tool_run:false`, no forwarding even after earlier entries verify. Actual outer stdout:

```json
{"error":{"actual_sha256":null,"code":"allowance_line_changed","detail":"path_missing","expected_sha256":"3bcd5127ee49014d02a9c248c614e725fbc117b67e65f49f6cbcf399b462de03","file":"a2after/timestamps-strict-at-9ef97f08.txt","line":3,"message":"a2after/timestamps-strict-at-9ef97f08.txt:3 does not resolve to a blob at 3ebc9081362acf3aa5c80aa3d4627fcd7b8ee87d","verified_before_failure":["a2audit-gate.json:14","a2audit-settle.json:3","a2residual-dispatch.json:17","a2residual-settle.json:3"]},"schema":"r33-hashed-allow-gate-v1","tool_run":false}
```

- Outer exit: **1**; stdout SHA256 `eb354e90496fd05f0832c8180471d9e8429b0671304cbcb2d1e79664cee36706`.
- Exact full-file deletion diff: `R/mutations/missing-path-source.patch`, SHA256 `ba20823c87aa2061684c1381429a66dee5458e2b0aacb4c0d471853eda10ca76`.
- Raw commit object: `R/mutations/missing-path-commit.txt`, SHA256 `2db7bcd72e16fba436b385fce74f410341d3601417c37336f1919e1aa9d412fb`.
- Original deleted bytes remain in `R/pristine-fixtures/a2after/timestamps-strict-at-9ef97f08.txt` and were restored to the clone.
- Verdict: **killed**, with valid pristine and restored controls.

## Independent forwarding observation

Both failure traces contain **zero execve attempts mentioning `--allow` and zero attempts mentioning the detector script**, not just unsuccessful application flags or the wrapper's own assertion. Each failure has seven successful execve calls: wrapper plus Git verification; neither reaches the gate. The green traces show the positive instrument control: one `env` execution forwarding all five `--allow` values, followed by one actual Python gate execution with those same five values. These two execve records are one gate run, not two.

Failure trace SHA256:

- `hash-mutated/execve.trace`: `a55f09c79e73b5b9c5fee2e87e3df4cdf6caed202ac70d5eb1ef0e41b2912452`.
- `path-mutated/execve.trace`: `c8c5f57dd2f301ca5eb84887d6be59581ee4eaed009fdc31982254b3b2a3ecbd`.

This corroborates the source ordering: wrapper lines 213–239 return on a failed row before lines 241–251 construct/execute any allowance-bearing tool argv. Both assigned failures were deliberately at row five to exercise atomic refusal after four valid rows. This is not an exhaustive check of every row or every error class.

## Exact-byte restoration and source integrity

Spec SHA256 before → mutated → restored:

```text
0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332
5c05d399c5d17261150f92d0c28c0f743b48a73295e70e6cad000ab95937bd15
0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332
```

The missing-path experiment was restored in `finally` using a clean switch to the pristine commit (exit 0); all five fixture files were also compared byte-for-byte with their retained original blobs. Before and after whole-file hashes are identical:

| Receipt | Before = after SHA256 |
|---|---|
| `a2audit-gate.json` | `1463bd49eb13860e21248a307f6cff9c448bd4aa0d50e86bb9502fb03b0605af` |
| `a2audit-settle.json` | `51300e60c0473de2d1466ab570126edc72ef53aee675f713216252bbc7bc6b51` |
| `a2residual-dispatch.json` | `57f4c573ffe9dbe40485e14a6e2b7ba68e96e799c81dcaf2ab4a36bbb1400b69` |
| `a2residual-settle.json` | `5daf8d9f72aa7c7ba0b2dc1c5963802718e29cf8ea679940636881f4ede8b785` |
| `a2after/timestamps-strict-at-9ef97f08.txt` | `4619faa04e09ba87e0ef759d881147912c140c0552411856ffef83d6bd4306e4` |

Pinned source, private copy and final lane bytes all agree (no code/spec production edits):

| Asset | Before = after SHA256 |
|---|---|
| `run-gate-hashed.py` | `e011ed69e72bed408de30211712b2e65d69fd01b9c002a45eb7ce5acf6055bb0` |
| `allowances-hashed.json` | `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332` |
| `build-hashed-fixture.sh` | `37206762bb48cbdd7b7758b46eda3e8129728077a32c9d71bc98d96088465152` |
| `run-hashed-selftest.sh` | `d60840374bc75a4bc67d526248786405b00a4b6456dbfcbe7d38ccd03785770e` |
| `evidence-timestamps.py` | `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00` |

## Bounds, setup exception and retained evidence

- Python 3.14.8; Git 2.56.0; strace 7.2. **No installs/updates.** No background jobs or subagents; no builds, linters, formatters, carrier manifests or unrelated selftests.
- Each retained command: timeout 25s plus 2s kill grace; 256 MiB address-space and 20s CPU limits per process; 128 FDs; file-size bound 1,048,575 bytes. The harness budget is 80 top-level commands; 35 were used. Final per-UID process/thread ceiling: 8192 (not a per-tree cgroup cap). Green/failing traces observed 27/7 successful execve calls respectively. The five input fixtures total 64,719 bytes; largest individual fixture is 40,560 bytes.
- Every retained command had a dedicated process group. Cleanup attempted SIGKILL on the group after collection; every group was already absent, and no retained command timed out. No service or host configuration changes.
- **Setup exception retained, not counted as a killed mutant:** first clone command at 09:33:25.294075Z–09:33:25.297034Z, with initial per-UID limit 1024, exited 128: `error: cannot fork() for git-upload-pack '/fast/scratch/hyaku/kaidoku-r33/w1/WTimestampBadPin/fixture-source/.git': Resource temporarily unavailable` / `fatal: unable to fork`. [INFERENCE] The low shared-UID thread limit caused the fork failure. Native `/usr/bin/ps -eLf | wc -l` subsequently reported 4500 thread/header lines; only the failed clone step was repeated with a bounded 8192 ceiling, before any detector baseline. No detector predicate was changed. An initial shell `ps -L` diagnostic was unsupported and its printed zero was not used. Details: `R/setup-limit-adjustment.json`, `R/commands/21-private-clone/`.
- Source manifest: `R/source-manifest.json`, SHA256 `da199f1b4b206af2a07d0ff61d9bbd38d46fba7ba34d56f8ffd561069d909ecc`.
- Complete observed cases, trace-derived forwarding evidence, verdicts, before/after source digests and cleanup records: `R/final-evidence.json`, SHA256 `3bdceabe3d7e9b6900319254636b1d709343d998b7e00a79e09a734ef4c656c7`.
- Additional restoration record: `R/restoration-after-missing.json`. Original code differences: **none**; spec mutation and receipt deletion are the only experimental differences.

These bounded results support the assigned two refusal paths only; they do not revive the stopped carrier claim or constitute outside/non-author admission verification.

Trailer: `.ufo/waves/round-33/w1/WTimestampBadPin.md`
