# WMutCount — one code-map count guard mutation

## Scope and axes

Instrument check only. R33-C1 remains **stopped / unprovable**, as recorded in `.ufo/waves/round-33/claim-stop.json`; these selftests are not an independent carrier study, a 32-row measurement, replacement admission evidence, or outside/non-author verification.

Axes: **depth** (count-boundary detector sensitivity), **reproducibility** (exact bytes and identical detector), and **containment** (private copy; existing isolated selftest only).

Observed lane HEAD: `d7076120e4f00c6d18aa77b8764d14861e820eb2`. Declared base from claim-stop: `428315a8f5674b952def862910af6e07a6c2224b`. Both copied source SHA-256 values match the corresponding `git show d7076120e4f00c6d18aa77b8764d14861e820eb2:tools/round-33/<file> | sha256sum` output. No lane/fleet Git writes were made.

Private evidence root: `/fast/scratch/hyaku/kaidoku-r33/w1/WMutCount/`.

## Mutant and expected detector

Smallest behavior-bearing change at `tools/round-33/chpe_profile.py:258`, applied only to the private `chpe_profile.py`:

```diff
-    if cm_count > MAX_CODE_MAP_COUNT:
+    if cm_count >= MAX_CODE_MAP_COUNT:
```

This is a plausible inclusive/exclusive upper-bound error. **[INFERENCE]** A count of exactly 1024 would now stop at `outside_profile.code_map_count_limit` rather than proceed to table-span validation. That boundary input was **not constructed or run**.

Detector: the unmodified existing `chpe_profile.py --selftest` with the original `selftest_pegen.py` sibling. A selftest mismatch/nonzero exit would kill this mutant only with passing pristine and restored runs. Prediction recorded before the mutated run in `mutation.json`: survival, because the existing named count-limit recipe (`selftest_pegen.py:279–280`) writes 2000 in each layout; both comparisons reject it. No existing recipe explicitly asserts the 1024 boundary.

Retained `mutation.patch`, `mutation.json`, `chpe_profile.py.mutant`, and both `*.pristine` snapshots. The sibling was never edited or imported by the evidence harness; only the original selftest imports it.

## Identical bounded invocation

Actual argv for all three runs (cwd is the private evidence root):

```text
/usr/bin/timeout --signal=TERM --kill-after=5s 120s /usr/bin/prlimit --as=268435456 --cpu=90 --fsize=1048575 --nproc=8192 --nofile=128 -- /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutCount/chpe_profile.py --selftest
```

Runtime: Python 3.14.8. Environment overrides: `TMPDIR=/fast/scratch/hyaku/kaidoku-r33/w1/WMutCount/tmp`, `LC_ALL=C.UTF-8`; Git override variables unset. Each detector had a private process session, 120-second wall limit with five-second kill escalation, 256 MiB per-process address-space limit, 90-second per-process CPU limit, file-size limit 1,048,575 bytes, and 128 file descriptors. An additional supervisor timeout was 132 seconds. Existing selftest asserts every fixture is below 1 MiB.

Subprocess bound: static AST counting, without importing the sibling, found 52 recipes × 2 layouts. The existing selftest makes 107 sequential CLI child invocations per run, including its filename and missing-file controls. `--nproc=8192` is a fixed **per-UID** resource cap, not a measured per-tree count. The preliminary `ps -u vgpnk -L -o lwp= | wc -l` attempt printed `ps: unsupported option '-L'` and `0`; that `0` was not treated as a usable count. Individual child processes were not separately traced, and no new behavioral predicate was substituted.

## Actual output and verdict

| Bytes | Start UTC | End UTC | Duration seconds | Exit | Selftest output |
|---|---|---|---:|---:|---|
| Pristine | 2026-10-23T09:33:46.005767+00:00 | 2026-10-23T09:33:48.326567+00:00 | 2.320802455 | 0 | pass=true, cases=107, failed=[] |
| Mutated | 2026-10-23T09:34:43.017533+00:00 | 2026-10-23T09:34:45.285729+00:00 | 2.268219230 | 0 | pass=true, cases=107, failed=[] |
| Restored | 2026-10-23T09:34:45.293581+00:00 | 2026-10-23T09:34:47.518111+00:00 | 2.224537222 | 0 | pass=true, cases=107, failed=[] |

All three additionally reported `finding_ids_produced=45`, `finding_ids_defined=45`, `finding_ids_uncovered=[]`, `recipe_ids_unknown=[]`, and `vocabulary_ok=true`. In both layouts, `code_map_count_limit` returned the expected `outside_profile.code_map_count_limit`, exit 11, on all three runs.

Each stdout is 21,794 bytes, byte-identical across all three runs; SHA-256:

```text
bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd
```

Each stderr is empty (0 bytes), SHA-256:

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

**Mutation verdict: SURVIVED.** The baseline and restoration passed, so this is not a baseline-failure ambiguity. It is a coverage finding: reaching every finding ID did not detect this count-limit equality defect. No contract change, detector repair, second mutant, or new fixture was attempted.

Complete actual streams and receipts are retained at the evidence root:

- `pristine.stdout`, `pristine.stderr`, `pristine.receipt.json`
- `mutated.stdout`, `mutated.stderr`, `mutated.receipt.json`
- `restored.stdout`, `restored.stderr`, `restored.receipt.json`
- `setup.json`, `mutation.json`, `restoration.json`, `probe.json`

## Source hashes and exact restoration

SHA-256:

| Artifact/state | Hash |
|---|---|
| Original / pristine / restored `chpe_profile.py` | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| Mutated `chpe_profile.py` | `e2ae2ccbac921e9d9c5e500faf03f16c378eb85f5157d04007e9f238ae65f492` |
| Original / all phases `selftest_pegen.py` | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |
| `mutation.patch` | `a88389a08c11a91fc71590dae7f855b2c5cf3717a54b4b0acf7fc86ffb4121fd` |

Restoration occurred in a `finally` block at `2026-10-23T09:34:45.292663+00:00`, before the restored detector run. Direct byte equality confirmed both private live modules exactly equal their original snapshots, and both original lane modules remained exactly unchanged. Every run receipt records before/after source digests. All three owned process groups were already absent after their detector finished; final cleanup probes confirmed no surviving owned process group.

## Safety and handoff boundary

Read only the permitted hold metadata in `safety-holds.json` and `quarantine-record.json`. The assignment identifies these two retained modules as separately authored by the unfiltered parser seat; this probe does not independently certify author provenance. No excluded builder code, reports, findings, fixtures, manifests, k01/k02/k08 derivatives, held item, carrier-study counter, native carrier execution, REA/MCP call, alternate runtime, or service/configuration change was used. No new policy refusal or auto-switch was observed in this item.

Exactly the three authorized existing selftest invocations were exercised; no other build, test, lint, formatter, or smoke run. No tools were installed or updated. Production code was untouched; the only lane write is this assigned report. This is lane advice about instrument coverage, not an admission judgment.
