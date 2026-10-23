# WMutTag — isolated unnamed-tag guard mutation

## Scope and axes

Axes: detector sensitivity, isolation/exact restoration, reproducible evidence. **Verdict: KILLED (selftest crash, not a structured mismatch).**

This is one instrument probe only. R33-C1 remains stopped/unprovable under `claim-stop.json`; these results are neither independent carrier rows nor a replacement for the stopped 32-row target. Read only permitted hold metadata. No quarantined artifact, held seed, carrier-study counter/manifest, native carrier execution, replacement generator, or additional runtime was used. The original `selftest_pegen.py` sibling was copied byte-for-byte and never edited.

Observed lane HEAD: `d7076120e4f00c6d18aa77b8764d14861e820eb2` (the admissible pin); stopped-claim base: `428315a8f5674b952def862910af6e07a6c2224b`. Read-only `git ls-tree` and `git hash-object` agreed on the two source blobs:

| Source | Pinned/observed Git blob | Bytes |
|---|---|---:|
| `tools/round-33/chpe_profile.py` | `0ca6c1d5afad2fe5b8a2ca868ce634838e22a233` | 21617 |
| `tools/round-33/selftest_pegen.py` | `d61d522bb04e4cb905385fa56132df1b90ff4718` | 13908 |

All code, patch, fixture temporaries and receipts were confined to `/fast/scratch/hyaku/kaidoku-r33/w1/WMutTag/` (denoted `E/` below). This report is the only lane write. No source, index, Git/JJ history, service, routing, or configuration write was made.

## Mutant and expected detector

One behavior-bearing change at parser line 269:

```diff
--- a/chpe_profile.py
+++ b/chpe_profile.py
@@ -269 +269 @@
-        if tag not in TAGS:
+        if tag > 3:
```

Defect: confuse a two-bit representation's maximum with the allowed named-tag maximum. Since the existing extraction is `tag = start_raw & 3`, the mutant guard cannot reject unnamed tag 3. No other parser statement, expectation or selftest code changed.

Expected detector: the original `chpe_profile.py --selftest`, whose independently authored sibling already supplies `tag3` in layouts L0 and L1 and expects `outside_profile.range_tag_unrecognized`, exit 11 (`selftest_pegen.py:260-261`). Pristine stdout confirms both cases returned that finding/exit with `pass: true`.

## Identical bounded detector

Actual detector argv for all three phases:

```text
/usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutTag/chpe_profile.py --selftest
```

Actual recorder argv was `/usr/bin/python3 -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutTag/run_selftest.py PHASE`, with `PHASE` respectively `pristine`, `mutated`, `restored`. CWD was `E/`; `TMPDIR=E/tmp`. Python was 3.14.8. There were exactly three detector invocations and no other behavioral detector.

Bounds per invocation: 45 seconds wall; inherited 256 MiB address-space and 20 CPU seconds per process; inherited file-size ceiling 1,048,575 bytes; core dumps disabled; inherited `RLIMIT_NPROC=4096` (per UID, not an isolated per-probe quota). Static unchanged selftest control flow bounds child invocations at `52 cases × 2 layouts + 3 = 107`, sequentially, at most one CLI child alongside the selftest parent. This is a source-derived bound, not a measured spawn count. Existing fixture assertion and kernel file-size bound keep each fixture below 1 MiB. Each invocation used a new process group; the recorder's final whole-group SIGKILL cleanup attempt returned ESRCH in every phase (group already absent). No timeout, remaining process tree, background job or descendant runtime was observed.

| Phase | Actual UTC start | Actual UTC end | Elapsed seconds | Detector exit | Stdout / stderr bytes |
|---|---|---|---:|---:|---:|
| Pristine | 2026-10-23T09:32:37.395350+00:00 | 2026-10-23T09:32:39.813182+00:00 | 2.417835156 | 0 | 21794 / 0 |
| Mutated | 2026-10-23T09:33:04.743488+00:00 | 2026-10-23T09:33:05.208333+00:00 | 0.464847623 | 1 | 0 / 949 |
| Restored | 2026-10-23T09:33:31.983272+00:00 | 2026-10-23T09:33:34.657428+00:00 | 2.674158195 | 0 | 21794 / 0 |

Pristine and restored stdout summaries both reported `pass: true`, `cases: 107`, `failed: []`, 45 finding IDs produced/defined, no uncovered or unknown IDs, and `vocabulary_ok: true`. The 107 are the existing selftest's result records, not independent carrier rows. Complete raw stdout is retained, not replaced by this summary. Both stderr streams were empty.

Mutated stdout was empty. Its actual stderr was:

```text
Traceback (most recent call last):
  File "/fast/scratch/hyaku/kaidoku-r33/w1/WMutTag/chpe_profile.py", line 402, in <module>
    sys.exit(main(sys.argv[1:]))
             ~~~~^^^^^^^^^^^^^^
  File "/fast/scratch/hyaku/kaidoku-r33/w1/WMutTag/chpe_profile.py", line 381, in main
    return selftest()
  File "/fast/scratch/hyaku/kaidoku-r33/w1/WMutTag/chpe_profile.py", line 328, in selftest
    out = json.loads(p.stdout)
  File "/usr/lib/python3.14/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/usr/lib/python3.14/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/json/decoder.py", line 363, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

The detector notices the defect through a nonzero crash. It does **not** produce a structured failed-case summary. The original selftest captures but does not expose the child parser's stderr on this path, so the child's underlying exception and exact interrupted case are not directly observed and are not claimed here. No extra run was made to recover them. A passing baseline, changed-source failure, and passing exact-byte restoration support the killed verdict; this is not a baseline-failure/inconclusive result.

## Source hashes and restoration

SHA-256:

| Material | Digest |
|---|---|
| Original lane parser before/after; `E/chpe_profile.py.pristine`; private pristine/restored parser | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| Mutated parser; retained `E/chpe_profile.py.mutated` | `589439faafb6473f30815ceec0a8cb711a5642b463a5e803d3da924ba0e7b35d` |
| Original lane sibling before/after and unchanged private sibling in every phase | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |
| `E/tag-guard.patch` | `c393e6c1683db9b6d6a344579cd607c7de27bb91957a527d06242458e6ea3786` |
| `E/run_selftest.py` | `5b6210f646df4ad7e3a778721c3352273ffec858f371b0c3ee7988e31706ad43` |

Immediately after the mutated detector exited, the sole guard edit was reversed before the restored detector ran. Before/after digests in all three receipts show no detector-induced source change. The restored parser digest equals its pristine snapshot and the untouched original lane parser. The sibling digest is unchanged throughout.

## Retained actual evidence

Each `E/PHASE.receipt.json` retains argv, CWD, bounds, actual start/end UTC, elapsed time, exit, complete stdout/stderr, source digests before/after, Python version, and process-group cleanup. Raw streams are also retained as `E/PHASE.stdout` and `E/PHASE.stderr`.

| Receipt | SHA-256 |
|---|---|
| `pristine.receipt.json` | `6033eefd4507b2250a247dfbd0beee61aab7deb632556238dc9d1623cc05b9f3` |
| `mutated.receipt.json` | `4d82018774d67e86445a47722123c98934c4661fc2e3d04f060e58ae75dab073` |
| `restored.receipt.json` | `884f58a9b785e40dbc032c583fe46f4b5213c2ba7e089ac8c160a8007bfb8830` |

Pristine/restored stdout SHA-256: `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` (identical complete output). Mutated stderr SHA-256: `eb7e795da139f9e128c84c5bcd99643b5149f5fd7ba165e9e58d3e108f767629`. Empty streams have SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

No tools installed or updated. No production repair, integration, admission judgment, or claim-target change is proposed. Probe complete; source restored.
