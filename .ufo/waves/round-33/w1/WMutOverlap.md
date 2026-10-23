# WMutOverlap — range-overlap instrument probe

**Verdict: KILLED.** One character changed in one private range-overlap guard. The existing selftest passed pristine, failed on the mutant, and passed after byte-exact restoration. Production source was untouched.

## Axes and scope

- Depth: sensitivity to the half-open range-overlap boundary.
- Detector validity: the same existing `--selftest` on pristine, mutated and restored bytes.
- Isolation: unchanged original sibling, production digests, exact restoration and bounded process cleanup.

This is instrument/repair evidence only, not an admission benchmark or outside/non-author verification. R33-C1 remains **STOPPED UNPROVABLE**; no replacement for its stopped 32-independent-row target is supplied and no numeric claim gain is asserted. The 107 selftest checks below are not independent carrier rows.

Read `claim-stop.json`, `safety-holds.json` and `quarantine-record.json` as boundary metadata only. No quarantine contents, held findings, old carrier seeds, k01/k02/k08 derivatives, new fixture generator, carrier-study manifest or carrier counter were opened or used. The only fixture recipes executed were those already in the retained, original `selftest_pegen.py` sibling.

## Revision and source provenance

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Observed read-only `git rev-parse HEAD`:

`d7076120e4f00c6d18aa77b8764d14861e820eb2` — the assigned admissible revision.

The revision's source blob IDs from `git rev-parse HEAD:<path>` matched read-only `git hash-object <path>`:

| Source under `tools/round-33/` | Git blob ID |
|---|---|
| `chpe_profile.py` | `0ca6c1d5afad2fe5b8a2ca868ce634838e22a233` |
| `selftest_pegen.py` | `d61d522bb04e4cb905385fa56132df1b90ff4718` |

Task-supplied base: `428315a8f5674b952def862910af6e07a6c2224b`; no before/after carrier measurement was performed.

All scratch files and receipts are exclusively under:

`/fast/scratch/hyaku/kaidoku-r33/w1/WMutOverlap/`

Only the two retained modules were copied there. `selftest_pegen.py` imports only `struct`, not the parser. The detector's original `selftest()` explicitly imports that sibling, bounds each fixture below 1 MiB before writing, and invokes Python parsing only; no native carrier execution occurred.

## Mutant and expected detector

Private `chpe_profile.py:286`, in the adjacent sorted-range overlap check:

```diff
-        if int(ranges[a]["rva"], 16) + ranges[a]["length"] > int(ranges[z]["rva"], 16):
+        if int(ranges[a]["rva"], 16) + ranges[a]["length"] >= int(ranges[z]["rva"], 16):
```

Plausible defect: treating equal endpoints as overlap rejects adjacent half-open ranges. Expected detector: the existing `green_adjacent_ranges` recipe in both existing layouts should change from `candidate.structural`/exit 0 to `outside_profile.range_overlap`/exit 11, making the overall selftest exit 1. Neither the sibling nor its expected IDs were changed.

The exact pristine source, mutant source and one-line patch are retained as `chpe_profile.pristine`, `chpe_profile.mutant` and `overlap.patch`.

## Actual bounded execution

Receipt-only `probe.py` ran these harness commands exactly once each, from the scratch directory, with a 55-second tool deadline:

```text
/usr/bin/python3 -I -B probe.py pristine
/usr/bin/python3 -I -B probe.py mutated
/usr/bin/python3 -I -B probe.py restored
```

All three launched the identical detector argv:

```text
/usr/bin/prlimit --as=536870912 --cpu=30 --nproc=4096 --fsize=1048575 -- /usr/bin/timeout --signal=TERM --kill-after=2s 40s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WMutOverlap/chpe_profile.py --selftest
```

Environment overrides, identical in all phases:

```text
TMPDIR=/fast/scratch/hyaku/kaidoku-r33/w1/WMutOverlap/tmp
LC_ALL=C.UTF-8
TZ=UTC
```

Bounds: 512 MiB address space per detector process; 30 CPU seconds per process; inherited UID process ceiling 4096 (not a private per-seat quota); individual file ceiling 1,048,575 bytes; 40-second GNU timeout with 2-second kill escalation; wrapper communication deadline 45 seconds with process-group cleanup. The existing two-layout, 52-recipe loop and three final CLI invocations provide a finite source-level bound of 107 child CLI launches per phase, sequentially. No selftest or child spawning logic was altered. No deadline or resource limit fired.

| Phase | Start UTC | End UTC | Scheduling duration (s) | Detector exit | Actual summary |
|---|---|---|---:|---:|---|
| Pristine | 2026-10-23T09:33:05.889303+00:00 | 2026-10-23T09:33:08.268035+00:00 | 2.378734179001185 | 0 | `pass=true`, `cases=107`, `failed=[]` |
| Mutated | 2026-10-23T09:33:29.245907+00:00 | 2026-10-23T09:33:31.614031+00:00 | 2.3681259470031364 | 1 | `pass=false`, `cases=107`, exactly two failures |
| Restored | 2026-10-23T09:33:47.275248+00:00 | 2026-10-23T09:33:49.627888+00:00 | 2.352639728007489 | 0 | `pass=true`, `cases=107`, `failed=[]` |

Actual mutant `failed` output:

```json
[
  {"case":"green_adjacent_ranges","exit":11,"got":"outside_profile.range_overlap","layout":"L0","pass":false,"want":"candidate.structural","want_exit":0},
  {"case":"green_adjacent_ranges","exit":11,"got":"outside_profile.range_overlap","layout":"L1","pass":false,"want":"candidate.structural","want_exit":0}
]
```

All three summaries reported 45 finding IDs produced and defined, no uncovered IDs, no unknown recipe IDs, and `vocabulary_ok=true`. These vocabulary figures alone did not kill the mutant: the existing recipe assertions did. Pristine success rules out classifying a baseline failure as a kill.

## Retained outputs and SHA-256

Each phase has `<phase>.receipt.json`, `<phase>.stdout` and `<phase>.stderr` in the scratch directory. Receipts retain exact argv, cwd, environment overrides, UTC boundaries, elapsed scheduling time, limits, exit, summaries, before/after source hashes and cleanup evidence. Complete stdout is retained, not only the excerpts above.

| Stream | Bytes | SHA-256 |
|---|---:|---|
| `pristine.stdout` | 21794 | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` |
| `mutated.stdout` | 22204 | `938f43495b394dc6004f670a524dcbe8369866bd07f64a328e0e4ceef45a4856` |
| `restored.stdout` | 21794 | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` |
| Each of the three `.stderr` files | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

| Source/artifact state | SHA-256 |
|---|---|
| Production parser, private pristine parser, immutable `chpe_profile.pristine`, restored private parser | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| Mutated parser and retained `chpe_profile.mutant` | `a1215b5de202b43f43399d4125af008affe29616589284847ad8a0e95d4b3511` |
| Original and private `selftest_pegen.py`, all phases | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |
| `overlap.patch` | `027a17a657f3c7db6bcef77a8c0a27a5ac56b0b1bb05a5add79263294df5cffe` |
| Receipt-only `probe.py` | `d84cb888c3511f02a042edfc90ee57b08b7f0c015c4702618cf43998804fc8da` |

## Restoration and containment

The guard was reversed after the mutated detector returned exit 1 and before the restored detector ran. Its restored SHA-256 exactly equals the pristine backup and original production SHA-256. Production parser and sibling hashes were recorded before and after every run and remained unchanged. Restored stdout is also byte-identical by SHA-256 to pristine stdout.

Dedicated process groups were 2392931 (pristine), 2420360 (mutated), and 2430626 (restored). Every receipt records `cleanup_signal="process group already absent"` and `process_group_absent_after_cleanup=true`; no experiment process tree remains. Temporary fixture files were managed by the original selftest's `TemporaryDirectory` under private `TMPDIR`. No background jobs or subagents were launched.

Tools already present: Python 3.14.8, GNU timeout/coreutils 9.12, prlimit/util-linux 2.42.4. No installs, updates, package transactions, service changes, Git/JJ writes, builds, linters or formatters. An initial unqualified `timeout --version` discovery command returned usage/exit 125 (required COMMAND missing); the detector used the explicitly located and version-checked `/usr/bin/timeout` throughout. This was not a behavioral detector run or retry.

The scoped result is only that the existing isolated selftest detects this one overlap-boundary defect. It does not establish correctness for other mutants or revive the stopped carrier claim.

Report: .ufo/waves/round-33/w1/WMutOverlap.md
