# WMutMetadata — metadata full-span guard mutation

**Verdict: INCONCLUSIVE.** The pristine, mutated, and restored invocations of the same bounded, original `chpe_profile.py --selftest` all exited 1 before producing a summary: the first existing fixture's CLI subprocess could not start (`BlockingIOError: [Errno 11] Resource temporarily unavailable: '/usr/bin/python3'`). This is neither a killed nor a surviving mutant. No detector retry, bound adjustment, replacement predicate, new fixture generator, or carrier-study counter was used.

## Scope and axes

Axes: depth of the metadata span guard check; detector sensitivity conditional on a passing baseline; exact-byte restoration; safety containment. This is instrument evidence only. R33-C1 remains **STOPPED UNPROVABLE**, numeric axis gain 0; this does not supply or replace the missing independent 32-row target.

Read the claim-stop record and only the permitted safety-holds/quarantine-record metadata. No held artifacts, old carrier seeds, builder derivatives, or quarantine contents were opened. Only the independently retained `chpe_profile.py` and its original `selftest_pegen.py` sibling were materialized. No production source was edited, no native carrier was executed, no subagents/background jobs were started, and no other runtime/backend was invoked.

Observed lane HEAD: `d7076120e4f00c6d18aa77b8764d14861e820eb2` (the pinned admissible revision). Claim-stop base: `428315a8f5674b952def862910af6e07a6c2224b` (declared in that record, not independently measured here).

Private evidence directory: `/fast/scratch/hyaku/kaidoku-r33/w1/WMutMetadata/`.

## One mutant

Private `chpe_profile.py:250` only:

```diff
-    msec, m = need(sections, soh, meta_rva, CHPE_METADATA_SIZE, "metadata")
+    msec, m = need(sections, soh, meta_rva, 12, "metadata")
```

This plausibly mistakes the three decoded uint32 fields (12 bytes) for the required full metadata span (`CHPE_METADATA_SIZE = 0x5c`, 92 bytes). The constant, emitted extent fact, all other guards, fixture recipes, and selftest expectations were unchanged. The exact patch and pristine/mutant source snapshots are retained as `metadata-full-span.patch`, `chpe_profile.py.pristine`, and `chpe_profile.py.mutant`.

Expected detector, **source-derived [INFERENCE], not observed**: pristine/restored exit 0 with `pass: true`; mutated exit 1 with the existing `metadata_zero_tail` and `metadata_cross_section` cases in both L0/L1 disagreeing with their pinned `outside_profile.metadata_zero_tail` / `outside_profile.metadata_cross_section` expectations (the weakened guard would allow those cases onward to `candidate.structural`). Existing recipe locations are `selftest_pegen.py:170-175,185-186,291-292`; detector comparison is `chpe_profile.py:326-336`. No fixture recipe was changed or executed independently.

## Same bounded detector, three phases

For each phase, actual launcher argv was `/usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutMetadata/run_receipt.py PHASE`, with PHASE respectively `pristine`, `mutated`, `restored`. The evidence-only runner does not import either target module; it captures the original CLI. Each launcher exited 0 after recording the detector's exit 1.

The exact detector argv was identical in all phases:

```text
/usr/bin/timeout --signal=TERM --kill-after=2s 180s /usr/bin/prlimit --as=268435456 --nproc=1024 --fsize=1048575 --cpu=120 --nofile=64 --core=0 -- /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutMetadata/chpe_profile.py --selftest
```

CWD was the private evidence directory; environment override was `TMPDIR=/fast/scratch/hyaku/kaidoku-r33/w1/WMutMetadata/tmp`. Bounds: 180-second timeout with 2-second kill grace; runner communicate deadline 190 seconds; outer tool deadline 210 seconds; address space 256 MiB per process; inherited per-UID process/task limit 1024; CPU 120 seconds per process; file size 1,048,575 bytes; 64 descriptors; no cores. The existing selftest asserts each fixture is strictly below 1 MiB before writing it. Its literal 52 cases × 2 layouts plus 3 auxiliary CLI calls bound the intended total to 107 CLI launches; this is a source-derived maximum, **not** a count of completed subprocesses. Each phase failed at the first launch. The precise cause of EAGAIN beyond the observed subprocess-start failure was not established; limits were not relaxed or retried.

| Phase | Start UTC | End UTC | Seconds | Detector exit | stdout | stderr |
|---|---|---|---:|---:|---:|---:|
| pristine | 2026-10-23T09:32:15.744310+00:00 | 2026-10-23T09:32:15.776480+00:00 | 0.032350 | 1 | 0 bytes | 1953 bytes |
| mutated | 2026-10-23T09:32:37.854024+00:00 | 2026-10-23T09:32:37.891996+00:00 | 0.038108 | 1 | 0 bytes | 1953 bytes |
| restored | 2026-10-23T09:32:50.898481+00:00 | 2026-10-23T09:32:50.933134+00:00 | 0.034742 | 1 | 0 bytes | 1953 bytes |

Actual terminal stderr ending, identical in all phases:

```text
  File "/usr/lib/python3.14/subprocess.py", line 1819, in _posix_spawn
    self.pid = os.posix_spawn(executable, args, env, **kwargs)
               ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
BlockingIOError: [Errno 11] Resource temporarily unavailable: '/usr/bin/python3'
```

The traceback begins at private `chpe_profile.py:402`, reaches `selftest()` at line 381 and its first `subprocess.run` at line 326. All stdout streams were empty, so there was no selftest JSON or case-result evidence. Empty stdout SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; identical full stderr SHA-256: `e29b8f4258bb2a08f265014e6d4269b97c47577da4957849e5beeda8becea067`.

Full actual argv, UTC timestamps, stdout/stderr digests, exits, source hashes, and cleanup results are retained in `pristine.receipt.json`, `mutated.receipt.json`, `restored.receipt.json`, with full raw `PHASE.stdout` and `PHASE.stderr` alongside them. Every child invocation had its own process group. Each final SIGKILL sweep found the dedicated group absent, and the subsequent group-existence probe also found it absent. No process tree remained in those groups.

## Hashes and restoration

SHA-256:

| Bytes | Digest |
|---|---|
| Parser: lane before/after, private pristine/restored, pristine snapshot | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| Parser: private mutant and retained mutant snapshot | `ede5fb65a206d9bfff54363e771e843ad7a1b0cd3a3a6889896a1131b8954a9e` |
| Original selftest sibling: lane/private, all phases | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |
| Mutation patch | `df62f05fe679ca73ac538fe319a857cd6e3951dec1039fc66473321a7d666891` |
| Evidence runner | `6351eda41039ebdd3a6e8387d6aaf0e99e483f378edeeab86e777f95435e198c` |

The active private parser was restored with the exact inverse one-line edit before the restored invocation. These three byte comparisons all completed successfully (exit 0, no output), in one `&&` chain followed by the recorded matching SHA-256 output:

```text
cmp /fast/scratch/hyaku/kaidoku-r33/w1/WMutMetadata/chpe_profile.py.pristine /fast/scratch/hyaku/kaidoku-r33/w1/WMutMetadata/chpe_profile.py
cmp /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/chpe_profile.py /fast/scratch/hyaku/kaidoku-r33/w1/WMutMetadata/chpe_profile.py
cmp /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/selftest_pegen.py /fast/scratch/hyaku/kaidoku-r33/w1/WMutMetadata/selftest_pegen.py
```

Comparison/hash command completion UTC: `2026-10-23T09:32:50.881485568Z`. The subsequent restored receipt independently records the same parser and sibling digests. Original source bytes remained unchanged throughout.

Existing tools used: Python 3.14.8, absolute `/usr/bin/timeout` GNU coreutils 9.12, `prlimit` util-linux 2.42.4. A preliminary unqualified `timeout --version` returned usage/exit 125; actual detector invocations consistently used the separately identified absolute GNU binary above. No tools were installed or updated; no pacman transaction or host-service/configuration change occurred.

Only this report was written inside the lane. Final finding: the assigned mutation was exercised with the unchanged bounded detector on pristine/mutated/restored bytes, but baseline subprocess failure prevents any sensitivity or mutant-kill conclusion. Restoration is exact; the original carrier claim remains stopped.
