# WMutOverflow — one range-u32-overflow mutation

## Scope and axes

- **Depth:** sensitivity of the existing instrument selftest to omission of range length from its u32-overflow guard.
- **Containment/restoration:** one private source mutation, original independent generator, bounded execution, exact-byte restoration.
- **Verdict: KILLED.** This is instrument/repair evidence only. R33-C1 remains **STOPPED UNPROVABLE**; no 32-row target was measured, replaced, or revived. This is lane advice, not outside/non-author verification or admission.

Production lane was read-only except this assigned report. Only `chpe_profile.py` and its original `selftest_pegen.py` sibling were materialized into `/fast/scratch/hyaku/kaidoku-r33/w1/WMutOverflow`. No generator edits, carrier-study counters, manifests, held fixtures, builder outputs, old carrier seeds, native carrier execution, REA/MCP calls, or replacement study were used. Independence is grounded in `prep/R33ChpeParser-independent.json` and exact `parser-pins.json` matches. The authorized safety metadata and `claim-stop.json` were read; quarantine and held findings were not opened.

Observed lane HEAD: `d7076120e4f00c6d18aa77b8764d14861e820eb2` (`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD`). Claim base: `428315a8f5674b952def862910af6e07a6c2224b`. No Git/JJ writes or other lane source changes were made.

## Mutant and expected detector

At `tools/round-33/chpe_profile.py:273`, omit the range length from the overflow comparison, a plausible end-vs-start arithmetic defect:

```diff
-        if start + length > RVA_LIMIT:
+        if start > RVA_LIMIT:
```

This leaves the guard unable to reject a range whose decoded u32 start fits but whose end exceeds 2^32. Expected detector: the existing `--selftest`, unchanged, with its original `range_rva_overflow` recipes in both L0 and L1. Each expects `malformed.range_rva_overflow`, classifier exit 12; no new fixture, assertion, or scoring predicate was introduced.

The same bounded argv, cwd, environment and limits were used for pristine, mutated and restored bytes:

```text
/usr/bin/timeout --signal=KILL --kill-after=2s 45s /usr/bin/prlimit --as=268435456 --fsize=1048575 --nproc=4096 --nofile=64 --cpu=30 /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutOverflow/chpe_profile.py --selftest
```

- cwd: `/fast/scratch/hyaku/kaidoku-r33/w1/WMutOverflow`.
- Environment overrides: `TMPDIR=/fast/scratch/hyaku/kaidoku-r33/w1/WMutOverflow/tmp`, `LC_ALL=C`, `TZ=UTC`; removed `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `PYTHONPATH`, `PYTHONHOME`.
- Wall bound: GNU timeout 45 s, KILL signal, 2 s kill-after; outer supervisor bound 50 s.
- Inherited bounds per process: address space 268435456 bytes, file size 1048575 bytes (<1 MiB), CPU 30 s, descriptors 64; UID-wide NPROC ceiling 4096.
- Foreground session supervisor capped session processes at 3. Peak sampled count was 3 for every run; no resource stop occurred.
- The untouched selftest has 52 recipes × 2 layouts + 3 fixed CLI checks: 107 serialized parser child invocations per completed run. Its fixture writes already assert size <1 MiB; the file-size limit additionally bounded writes. No extra detector or external carrier invocation was used.
- Session groups were cleaned with SIGKILL where present and parents reaped after each run; all post-run session snapshots were empty. Selftest temporary fixture directories were removed; the private `tmp` directory was empty afterward.

## Actual outputs

All timestamps below are observed UTC; durations are measured scheduling durations, not forecasts.

| Bytes | Start UTC | End UTC | Seconds | Exit | `pass` | Cases | Failed |
|---|---|---|---:|---:|---|---:|---:|
| pristine | 2026-10-23T09:32:41.507015+00:00 | 2026-10-23T09:32:43.946419+00:00 | 2.439406 | 0 | true | 107 | 0 |
| mutated | 2026-10-23T09:33:26.263668+00:00 | 2026-10-23T09:33:28.599362+00:00 | 2.335694 | 1 | false | 107 | 2 |
| restored | 2026-10-23T09:33:28.632903+00:00 | 2026-10-23T09:33:30.956750+00:00 | 2.323847 | 0 | true | 107 | 0 |

Pristine and restored stdout reported `selftest="chpe_profile"`, `pass=true`, `cases=107`, `failed=[]`, and `finding_ids_uncovered=[]`. Mutated stdout reported `pass=false`, `cases=107`, exactly these two failures, and `finding_ids_uncovered=["malformed.range_rva_overflow"]`:

```json
[
  {
    "case": "range_rva_overflow",
    "exit": 11,
    "got": "outside_profile.range_unmapped",
    "layout": "L0",
    "pass": false,
    "want": "malformed.range_rva_overflow",
    "want_exit": 12
  },
  {
    "case": "range_rva_overflow",
    "exit": 11,
    "got": "outside_profile.range_unmapped",
    "layout": "L1",
    "pass": false,
    "want": "malformed.range_rva_overflow",
    "want_exit": 12
  }
]
```

All three stderr streams were empty (0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Full actual stdout/stderr and exit/timing/argv/limit receipts are retained below, not reconstructed.

| Stage | Stdout bytes | Stdout SHA-256 | Stderr bytes |
|---|---:|---|---:|
| pristine | 21794 | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` | 0 |
| mutated | 22237 | `89e42ec79113aae829103c471b984ca6e419c6098729afc7a814c3f2980bf0b1` | 0 |
| restored | 21794 | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` | 0 |

The mutant still rejects these inputs, but under the wrong structural finding and exit class (`outside_profile.range_unmapped`, exit 11). Exact existing expectation matching therefore kills it. This does not establish general overflow coverage or carrier correctness.

## Hashes and restoration

| Artifact | SHA-256 |
|---|---|
| Original / scratch pristine / scratch restored `chpe_profile.py` | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| Mutated `chpe_profile.py` | `1cad289c957f1aa0a002bf2eafea3f08d3656c35ec3a4917615ea3c95edd71a9` |
| Original and all stage `selftest_pegen.py` | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |
| `range-overflow.patch` | `6f87a784eeec4bf9688de58e865e5521b1dbdb3d717e6cc8716ecbf5f66d47a2` |

Parser source size was 21617 bytes; original generator size was 13908 bytes. Restoration occurred in a `finally` block before the restored detector run. Both private files matched their original bytes exactly afterward; direct final digest/byte comparisons also showed both production files unchanged. There was no mutation probe exception or baseline failure. Baseline pass → mutant behavioral mismatch → restored pass supports **KILLED**, not inconclusive.

## Retained evidence

All non-report artifacts are only under `/fast/scratch/hyaku/kaidoku-r33/w1/WMutOverflow/`:

- `provenance.json`: source paths, pins, sizes, revision, independence/fixture scope.
- `range-overflow.patch` and `mutated-chpe_profile.py.txt`: the one mutation and preserved mutant source.
- `pristine.stdout.json`, `mutated.stdout.json`, `restored.stdout.json`: full actual stdout.
- `pristine.stderr.txt`, `mutated.stderr.txt`, `restored.stderr.txt`: empty actual stderr streams.
- `pristine.receipt.json`, `mutated.receipt.json`, `restored.receipt.json`: exact argv, start/end UTC, exit, source/output digests, resource bounds and process cleanup.
- `restoration.json`: original before/after hashes, private restored hashes, exact byte equality and empty temporary-directory evidence.
- `probe-result.json`: consolidated actual receipts and verdict.
- `chpe_profile.py`, `selftest_pegen.py`: exact pristine bytes, restored in place.

Tools used: `/usr/bin/python3` 3.14.8, `/usr/bin/timeout` GNU coreutils 9.12, `/usr/bin/prlimit` util-linux 2.42.4. No tool was installed or updated; no package-manager transaction or host-service change occurred. Initial unqualified `timeout --version` was intercepted by a shell command and exited 125 (required COMMAND argument missing); this was tooling discovery only, before any detector run. All actual detector executions used the absolute GNU timeout path shown above.

No checks beyond the assigned existing selftest were run. No further check is proposed: the assigned one-mutant probe is complete.

Report: `.ufo/waves/round-33/w1/WMutOverflow.md`
