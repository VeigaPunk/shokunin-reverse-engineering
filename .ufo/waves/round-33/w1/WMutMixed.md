# WMutMixed — isolated ARM64EC mix-guard mutation

**Verdict: KILLED.** The unchanged existing selftest passed pristine bytes, rejected the one-line mutant, and passed exact restored bytes. This is instrument sensitivity/restoration evidence only. R33-C1 remains stopped/unprovable; no replacement 32-row measurement, admission judgment, or numeric depth gain is claimed.

Axes: defect sensitivity, provenance isolation, bounded execution, exact restoration.

## Scope and provenance

- Measured lane HEAD: `d7076120e4f00c6d18aa77b8764d14861e820eb2` (`git --no-optional-locks rev-parse HEAD`). Declared base in `claim-stop.json`: `428315a8f5674b952def862910af6e07a6c2224b`.
- Both permitted modules' working-tree SHA-256 values matched the pinned revision's `git show <pin>:<path> | sha256sum` output before materialization.
- Private directory: `/fast/scratch/hyaku/kaidoku-r33/w1/WMutMixed/` (abbreviated `S` below). Only `tools/round-33/chpe_profile.py` and its original `selftest_pegen.py` sibling were materialized. The sibling was never changed.
- Read `claim-stop.json` and only permitted hold/quarantine metadata. No quarantined material, carrier seeds, excluded builder outputs, manifests, counters, REA/MCP, or native fixture execution was used. Provenance authorization is the assignment's independent/unfiltered-module declaration; no wider independence claim is made.
- Only this report was written in the lane. No lane/fleet Git writes, subagents, background jobs, or tool installations/updates. Existing runtime: `/usr/bin/python3`, Python 3.14.8.

## Mutant and expected detector

At original `tools/round-33/chpe_profile.py:292`, introduce a plausible copied-tag mistake in the second required-kind guard:

```diff
-    if "ARM64EC" not in kinds:
+    if "ARM64" not in kinds:
```

The preceding ARM64 guard remains intact. The second check consequently duplicates it and no longer rejects a code map missing ARM64EC. No expectation, fixture recipe, other guard, or selftest code was edited.

Expected detector: the original `selftest_pegen.py:258` case `only_arm64_amd64` in both existing layouts must report `not_candidate.no_arm64ec_range`, exit 10. The existing `chpe_profile.py:329-336` finding/exit comparisons should fail when the mutant instead reports `candidate.structural`, exit 0. This expectation was stated from source before the mutant run. The converse `only_arm64ec_amd64` case should remain rejected by the intact ARM64 guard.

## Exact bounded execution

Same detector argv in all three phases:

```text
/usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutMixed/chpe_profile.py --selftest
```

Actual harness argv, once per phase:

```text
/usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutMixed/run_selftest.py pristine
/usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutMixed/run_selftest.py mutated
/usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutMixed/run_selftest.py restored
```

CWD `S`; environment override `TMPDIR=S/tmp`. The harness records actual detector stdout, stderr, exit, UTC endpoints, source hashes, and cleanup. Bounds were identical: `communicate(timeout=120)` with process-group SIGKILL on timeout/final cleanup; address space 536870912 bytes/process; CPU 60 seconds/process; file size 1048575 bytes/process; `RLIMIT_NPROC=4096` per UID; 64 open files/process; core size zero. Existing child calls retain their own 30-second timeouts. Static inspection of the unchanged two layouts × 52 recipes plus three CLI calls bounds each detector run to 107 sequential child launches, at most one direct child active. This count is a frozen-code bound, not a process trace; NPROC is per UID, not an isolated per-job quota. The existing selftest asserts every fixture is below 1 MiB before writing. No new fixture generator was authored.

| Phase | Start UTC | End UTC | Measured seconds | Detector exit | Actual selftest result |
|---|---|---|---:|---:|---|
| Pristine | 2026-10-23T09:31:55.764853+00:00 | 2026-10-23T09:31:57.992450+00:00 | 2.22760075199767 | 0 | `pass=true`, 107 cases, failed `[]`, 45/45 finding ids |
| Mutated | 2026-10-23T09:32:32.226118+00:00 | 2026-10-23T09:32:34.655483+00:00 | 2.4293671769992216 | 1 | `pass=false`, 107 cases, exactly two failed rows, 44/45 finding ids |
| Restored | 2026-10-23T09:32:46.191368+00:00 | 2026-10-23T09:32:48.621749+00:00 | 2.430384024992236 | 0 | `pass=true`, 107 cases, failed `[]`, 45/45 finding ids |

All three stderr files were empty; no timeout occurred. Each harness exited 0 (receipt collection succeeded); the mutant **detector** exited 1. All receipts report `process group absent; no remaining process tree` after final group cleanup.

Actual mutant failed rows, extracted without changing the detector:

```json
[
  {"case":"only_arm64_amd64","layout":"L0","want":"not_candidate.no_arm64ec_range","got":"candidate.structural","want_exit":10,"exit":0,"pass":false},
  {"case":"only_arm64_amd64","layout":"L1","want":"not_candidate.no_arm64ec_range","got":"candidate.structural","want_exit":10,"exit":0,"pass":false}
]
```

The mutant summary also reported `finding_ids_uncovered=["not_candidate.no_arm64ec_range"]`; vocabulary checks remained true. In pristine and restored outputs these two rows had the expected finding/exit. The converse `only_arm64ec_amd64` rows retained `not_candidate.no_arm64_range`, exit 10, in every phase. Thus failure is the assigned semantic defect, not baseline or infrastructure failure. The 107 checks comprise existing instrument recipes and controls, not independent carrier rows.

## Hashes and exact restoration

SHA-256:

| Bytes | Digest |
|---|---|
| Parser pristine, backup, restored, production before and after | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| Parser mutant, retained as `S/chpe_profile.py.mutant` | `4716972c68b6d1f555fdc31bf9b3ace60c64395519dfad7198df540d21fecf5f` |
| Original sibling, all phases and production before/after | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |
| Retained `S/mutation.patch` (421 bytes) | `4ae89b44c953156dec155b5ef417772389397a84a516e86a3ea539e63bc49167` |
| Retained `S/run_selftest.py` | `800727a9c752f9304d772d5484c838cb2dffd1607b15b409f45796d92b3c7c51` |
| Pristine/restored stdout (21794 bytes each) | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` |
| Mutated stdout (22191 bytes) | `ab2af7cbbeb006e381e42e18968e2f8862d9285731ef78c428413e64c1c47807` |
| Every stderr (0 bytes) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Restoration ran in `finally` immediately after the mutant detector. `S/restoration.json`, recorded at `2026-10-23T09:33:14.932221+00:00`, records actual byte-equality checks: private parser equals original materialized bytes and pristine backup; private sibling equals original; both production originals equal their original materialized bytes. All were true. The restored detector stdout also exactly matched pristine stdout by SHA-256.

Raw complete evidence retained under `S`: `{pristine,mutated,restored}.receipt.json`, matching `.stdout`/`.stderr`, `chpe_profile.py.pristine`, `chpe_profile.py.mutant`, `mutation.patch`, `run_selftest.py`, unchanged `selftest_pegen.py`, restored `chpe_profile.py`, and `restoration.json` containing artifact sizes/digests. No additional test, build, linter, formatter, alternate predicate, or carrier-study experiment was run.
