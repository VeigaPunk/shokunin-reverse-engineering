# WMutHeader — isolated optional-header guard mutation

## Scope and verdict

**KILLED.** One private-copy mutation changed the raw optional-header extent guard from `or` to `and`. The original `--selftest` passed before mutation, failed on exactly two expected-finding checks while mutated, and passed after byte-exact restoration. Production source was untouched.

Axes: **depth** (finding-specific detector sensitivity), **containment**, and **reproducibility/exact restoration**. This is instrument/repair evidence only. R33-C1 remains **STOPPED UNPROVABLE**: no replacement for the missing independent 32-row target, no admission measurement, and no claimed numeric axis gain.

Observed production HEAD: `d7076120e4f00c6d18aa77b8764d14861e820eb2`; declared base: `428315a8f5674b952def862910af6e07a6c2224b`. Source bytes were materialized from `tools/round-33/chpe_profile.py` and its original `selftest_pegen.py` sibling. Only the permitted `claim-stop.json`, `safety-holds.json`, and `quarantine-record.json` metadata were consulted about the hold. No excluded artifact, held seed, carrier manifest/counter, replacement generator, native carrier execution, REA/MCP call, or other runtime was used.

Private evidence root: `/fast/scratch/hyaku/kaidoku-r33/w1/WMutHeader/`.

## Single mutant and expected detector

At `chpe_profile.py:196`, the valid guard rejects an optional header that is **either** shorter than 112 bytes **or** extends past the file. Replacing the disjunction with a conjunction is one plausible boolean-operator defect; it bypasses the guard when only one extent condition is violated.

```diff
-    if opt_size < 112 or opt + opt_size > n:
+    if opt_size < 112 and opt + opt_size > n:
```

Expected detector: the existing `optional_header_truncated` recipe in layouts L0 and L1 (`selftest_pegen.py:305-306`) sets the declared optional-header size to `0x40`. Its pinned expected finding is `malformed.optional_header_truncated`. With this mutant, the later data-directory extent check instead reports `malformed.data_directories_truncated`. Both are exit 12; the selftest must detect the **finding-id mismatch**, not merely a changed error status.

No test, recipe, expected finding, or sibling helper was modified. The mutation affects both disjuncts, but this probe demonstrates sensitivity to the **too-short-header** branch only; it does not independently establish past-file-end boundary coverage.

## Identical bounded detector

Each phase invoked this exact argv, with the same working directory and environment:

```text
/usr/bin/timeout --signal=TERM --kill-after=2s 90s /usr/bin/prlimit --as=536870912 --cpu=30 --fsize=1048575 --nofile=64 --nproc=4096 -- /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutHeader/chpe_profile.py --selftest
```

Working directory: the private evidence root. `TMPDIR` was its `tmp/` child; `PYTHONDONTWRITEBYTECODE=1`; `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset. The bounded supervisor was invoked as:

```text
/usr/bin/python3 /fast/scratch/hyaku/kaidoku-r33/w1/WMutHeader/run_bounded_selftest.py pristine
/usr/bin/python3 /fast/scratch/hyaku/kaidoku-r33/w1/WMutHeader/run_bounded_selftest.py mutated
/usr/bin/python3 /fast/scratch/hyaku/kaidoku-r33/w1/WMutHeader/run_bounded_selftest.py restored
```

Limits: 90-second detector wall time, TERM then KILL after 2 seconds, 95-second supervisor communication deadline, 512 MiB address space and 30 CPU seconds per process, 1,048,575-byte file-size limit, 64 descriptors, and NPROC 4096 per real UID. NPROC is not a per-tree cumulative counter. The unchanged source has 2 layouts × 52 cases plus 3 serial CLI calls: a fixed bound of 107 child executions per phase and one live CLI child at a time. Each fixture write is preceded by the original `< 1 MiB` assertion. No new counting predicate or generator was added.

The supervisor used a new process session, cleaned its entire detector process group in `finally`, and retained stdout/stderr and JSON receipts. Every phase recorded `detector process group already absent; no process group remains`. No timeout occurred.

## Actual output

All timestamps below are observed UTC; durations are elapsed scheduling time, not a performance claim.

| Phase | Start UTC | End UTC | Elapsed seconds | Exit | Original selftest output |
|---|---|---|---:|---:|---|
| Pristine | 2026-10-23T09:32:53.867723+00:00 | 2026-10-23T09:32:56.318620+00:00 | 2.451186 | 0 | `pass=true`, `cases=107`, `failed=[]`, 45/45 finding IDs produced |
| Mutated | 2026-10-23T09:33:18.188856+00:00 | 2026-10-23T09:33:20.779668+00:00 | 2.591052 | 1 | `pass=false`, `cases=107`, exactly 2 failures, 44/45 finding IDs produced |
| Restored | 2026-10-23T09:33:29.078490+00:00 | 2026-10-23T09:33:31.437134+00:00 | 2.358867 | 0 | `pass=true`, `cases=107`, `failed=[]`, 45/45 finding IDs produced |

The two actual mutated failure records were:

```json
[
  {"case":"optional_header_truncated","exit":12,"got":"malformed.data_directories_truncated","layout":"L0","pass":false,"want":"malformed.optional_header_truncated","want_exit":12},
  {"case":"optional_header_truncated","exit":12,"got":"malformed.data_directories_truncated","layout":"L1","pass":false,"want":"malformed.optional_header_truncated","want_exit":12}
]
```

The mutated summary listed only `malformed.optional_header_truncated` as uncovered. Every phase reported `recipe_ids_unknown=[]` and `vocabulary_ok=true`. All three stderr files were empty. Pristine and restored stdout were byte-for-byte identical.

| Retained stdout | Bytes | SHA-256 |
|---|---:|---|
| `pristine/stdout.txt` | 21794 | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` |
| `mutated/stdout.txt` | 22282 | `0094c923ebda8da995983b1f56991dd0b699113734666df0be2bfc5fb91f3f48` |
| `restored/stdout.txt` | 21794 | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` |

Each corresponding `stderr.txt` has 0 bytes and SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Full actual JSON output and argv/start/end/exit/limits/source hashes are retained in each phase's `stdout.txt`, `stderr.txt`, and `receipt.json`.

## Hashes and restoration evidence

| Artifact/state | SHA-256 |
|---|---|
| Parser, production/pristine/restored | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| Parser, mutated | `3c8d11d5bded0ab3153773e6f0ffaec9df6d0d5da0f9b4958188acfe92bcc844` |
| Original helper, all phases and production | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |
| `mutant.patch` | `74ba4eacf4dfb8be345ce5766186d14417f5a2f555f3c0ec32a511cee2227a6d` |
| `run_bounded_selftest.py` | `3ebb9dd8417e8363a63df8366ba6d36ac26c403790d16b0ae75cc3d9c4d98387` |

At `2026-10-23T09:34:00.555388+00:00`, direct byte comparisons recorded all of the following as true:

- Restored private parser equals both the initial bytes and retained pristine snapshot.
- Private helper equals its original bytes.
- Production parser and helper equal their initial bytes.
- All three detector argv arrays are identical.
- Pristine and restored stdout are identical.

Each phase's source hashes also remained unchanged across its own run. Retained artifacts include `chpe_profile.pristine.py`, `chpe_profile.mutant.py`, the restored `chpe_profile.py`, original `selftest_pegen.py`, `mutant.patch`, `mutation.json`, `provenance.json`, `restoration.json`, the bounded runner, all phase receipts/logs, and `artifacts.json` with hashes and sizes.

## Interpretation and tooling

The mutant is killed because the pristine baseline passes and the mutated finding-specific expectations fail; restoration then reproduces the baseline exactly. This is evidence that the existing detector can reject this one guard regression even when classification and per-fixture exit codes stay unchanged. It is not independent fixture-author verification, complete raw-extent coverage, source conformance, hybrid authenticity, Windows loadability, or the stopped 32-row benchmark.

No tools were installed or updated. Existing tools: Python 3.14.8, GNU coreutils timeout 9.12, util-linux prlimit 2.42.4. An initial tooling-identification command exited 125 when unqualified `timeout --version` returned `error: the following required arguments were not provided: <COMMAND>...`; no detector ran in that command. Its command resolution was not investigated. All three recorded detectors used the explicit GNU `/usr/bin/timeout` path. No additional test/build/lint/formatter or mutation probe was run.

Report: `.ufo/waves/round-33/w1/WMutHeader.md`
