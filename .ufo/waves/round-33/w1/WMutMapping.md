# WMutMapping — range mapping mutation probe

## Scope and axes

- Seat: `KaidokuR33.WMutMapping`; target axis: **depth**. Probe axes: detector sensitivity, containment, exact restoration, evidence fidelity.
- **Instrument evidence only.** R33-C1 remains **STOPPED UNPROVABLE**, as recorded in `.ufo/waves/round-33/claim-stop.json`. This probe supplies neither independent carrier rows nor a replacement admission benchmark; no original-claim gain or admission is asserted.
- Production revision observed with read-only `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD`: `d7076120e4f00c6d18aa77b8764d14861e820eb2`. Declared base: `428315a8f5674b952def862910af6e07a6c2224b`.
- Only private copies of `tools/round-33/chpe_profile.py` and its original `selftest_pegen.py` sibling were materialized. Their observed SHA-256 values match `.ufo/waves/round-33/parser-pins.json` and `.ufo/waves/round-33/prep/R33ChpeParser-independent.json`, which identifies the separate, unfiltered parser item. No held builder artifacts, old carrier seeds, k01/k02/k08 derivatives, production/control manifests, carrier-study counters, or quarantine findings were opened or used. Safety-hold metadata and the stopped-claim record were read for boundaries only.
- Private root for every source copy, patch, receipt and selftest temporary directory: `/fast/scratch/hyaku/kaidoku-r33/w1/WMutMapping/` (called `S` below). This report is the sole lane write. No source integration, Git/JJ write, subagent, background job, native carrier execution, alternate runtime, or new fixture generator was used.

## Mutant and expected detector

At private `chpe_profile.py:278`, change only the range-specific full-span mapping request:

```diff
-        rsec, roff = need(sections, soh, start, length, "range")
+        rsec, roff = need(sections, soh, start, 1, "range")
```

This is a plausible start-address-only mapping defect: a mapped first byte does not establish that the complete declared range lies in one section's file-backed prefix. The shared `resolve()` implementation and other structure mapping calls remain unchanged. Original source references: `chpe_profile.py:146-172,278`; existing recipes and expectations: `selftest_pegen.py:152-167,272-273`; existing detector: `chpe_profile.py:313-370`.

Expected before running the mutant: the unchanged existing `--selftest` should pass on pristine/restored bytes and fail on the mutant through the existing `range_zero_tail` and/or `range_cross_section` expectations. The selftest already compares both finding ID and exit status; no detector or expectation was altered.

Retained design: `S/probe-plan.json`. Retained exact patch: `S/mapping-start-only.patch` (187 bytes; SHA-256 `857734a96f9fa12e0cf7d6d72e64f53109f3ea81d3d297910c876cb266eca066`). Pristine and mutant sources remain as `S/chpe_profile.py.pristine` and `S/chpe_profile.py.mutant`; the executable private `S/chpe_profile.py` is restored.

## Identical bounded detector

Actual argv for all three runs, cwd `S`:

```text
/usr/bin/timeout --signal=TERM --kill-after=2s 30s /usr/bin/prlimit --as=268435456 --nproc=4096 --cpu=20 --fsize=1048575 --nofile=64 --core=0 -- /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutMapping/chpe_profile.py --selftest
```

Environment overrides: `TMPDIR=S`, `LC_ALL=C`, `PYTHONDONTWRITEBYTECODE=1`; unset `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `PYTHONPATH`, `PYTHONHOME`. The supervisor captured both streams, used a 35-second outer wait, reaped the launched process, and attempted process-group SIGKILL in `finally`; every cleanup attempt found **no remaining process group**. Process-group IDs were 2234286, 2346748 and 2395358 respectively.

Inherited bounds: 256 MiB address space per process; 20 CPU seconds per process; file size at most 1,048,575 bytes; 64 file descriptors; core size zero; 30-second timeout with two-second kill escalation. `RLIMIT_NPROC=4096` is a **per-UID**, not private-process-group, limit. Independently, the unchanged selftest has a source-fixed workload of 104 recipe CLI calls (52 recipes × two layouts), two filename-invariance CLI calls and one missing-file CLI call: 107 sequential CLI children per run, not an unbounded manifest. The selftest asserts each synthetic fixture is strictly below 1 MiB before writing. All its temporary writes were redirected beneath `S`. Supervisor Python reported 3.14.8. No tool installation or update was needed.

## Actual outputs

All timestamps are observed UTC. Durations are measured monotonic elapsed seconds, not forecasts.

| Phase | Start UTC | End UTC | Seconds | Exit | `pass` | Cases | Failed rows | stderr |
|---|---|---|---:|---:|---|---:|---:|---:|
| pristine | 2026-10-23T09:32:12.187768+00:00 | 2026-10-23T09:32:14.381455+00:00 | 2.193691 | 0 | true | 107 | 0 | 0 bytes |
| mutated | 2026-10-23T09:32:47.730363+00:00 | 2026-10-23T09:32:50.185378+00:00 | 2.455016 | 1 | false | 107 | 4 | 0 bytes |
| restored | 2026-10-23T09:33:06.907912+00:00 | 2026-10-23T09:33:09.324271+00:00 | 2.416359 | 0 | true | 107 | 0 | 0 bytes |

Actual mutant `failed` rows:

| Layout | Case | Expected finding / exit | Actual finding / exit |
|---|---|---|---|
| L0 | `range_zero_tail` | `outside_profile.range_zero_tail` / 11 | `candidate.structural` / 0 |
| L0 | `range_cross_section` | `outside_profile.range_cross_section` / 11 | `candidate.structural` / 0 |
| L1 | `range_zero_tail` | `outside_profile.range_zero_tail` / 11 | `outside_profile.range_overlap` / 11 |
| L1 | `range_cross_section` | `outside_profile.range_cross_section` / 11 | `outside_profile.range_overlap` / 11 |

Pristine and restored summaries both report `finding_ids_produced=45`, `finding_ids_defined=45`, `finding_ids_uncovered=[]`, `recipe_ids_unknown=[]`, `vocabulary_ok=true`. The mutant reports 43 produced IDs, with only `outside_profile.range_cross_section` and `outside_profile.range_zero_tail` uncovered; `recipe_ids_unknown=[]` and `vocabulary_ok=true` remain unchanged. The L1 failures specifically demonstrate why the existing exact finding-ID comparison matters: exit-only comparison would not distinguish the later overlap rejection.

Full, unmodified captured streams and execution metadata are retained as:

- `S/pristine.stdout.json`, `S/pristine.stderr.txt`, `S/pristine.receipt.json`
- `S/mutated.stdout.json`, `S/mutated.stderr.txt`, `S/mutated.receipt.json`
- `S/restored.stdout.json`, `S/restored.stderr.txt`, `S/restored.receipt.json`

| stdout | Bytes | SHA-256 |
|---|---:|---|
| pristine | 21794 | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` |
| mutated | 22635 | `81f8758cea2896d8202c4274421a1ddc9cea7d79cd16faf205c8f1256e4a5c7f` |
| restored | 21794 | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` |

Every stderr file is empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). None of the runs timed out.

## Verdict and restoration evidence

**KILLED.** The pristine detector passed; one behavior-bearing mutation produced four expected-finding mismatches and exit 1; exact restoration recovered the original passing output. This conclusion is limited to this single mutation and these existing isolated selftests. It is not a general parser-correctness claim, outside/non-author verification, or admission judgment.

| Source / state | SHA-256 |
|---|---|
| `chpe_profile.py` — production before and after; private pristine and restored; pristine backup | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| `chpe_profile.py` — private mutant and retained mutant copy | `95d5606fe0d05d21e8addd10431c40332f2070d997b94f540384d55c8feebf4a` |
| original `selftest_pegen.py` — production before and after; private before/after every phase | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |

`S/restoration.json`, observed at `2026-10-23T09:33:09.325033+00:00`, records direct byte equality between the restored private parser and pristine backup, unchanged production hashes, unchanged sibling hashes in all phases, identical argv, empty stderr and successful process cleanup. Restoration used the inverse one-line surgical edit; no production source was modified. Only the three assigned existing selftest invocations were exercised; no additional tests, builds, linters, formatters, carrier study or replacement predicate was run.
