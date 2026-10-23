# R34ParserBounds — existing CHPE selftest limits

## Result and recommendation

**Count boundary SURVIVED; metadata span KILLED; unnamed tag KILLED by selftest crash.** All six pristine/restored detectors passed. None of these three probes is inconclusive.

**Recommend precise exclusion, not a successor patch:** the committed corpus has no discriminating input at `CodeMapCount == 1024`. Do not claim that the archived reader's inclusive count boundary is selftest-covered, or that all its guards are mutation-sensitive. Keep its existing `> 1024` profile contract unchanged; count 2000 is tested, equality is not. No selftest-only behavioral assertion over the same input bytes can distinguish this `>` → `>=` mutant. Lowering the bound to an existing count, changing expectations, source-text assertions, or constructing a 1024-count PE would not repair that evidence gap under this assignment.

Exclude the round-33 CHPE reader, its 107 selftest result records, and these mutation receipts from round-34 GNU ELF admission inputs, expected-result oracles, production measurements, and axis-gain counts. Metadata/tag kills may be retained only as archived instrument-sensitivity evidence. R33-C1 remains stopped/unprovable; neither the missing independent manifest nor any claim target is replaced. This is a recommendation to Main, not an admission judgment.

## Scope, axes, provenance

- Axes: **depth** (guard sensitivity), **operability** (bounded execution and exact restoration), **calibration** (distinguish finding-ID coverage from boundary coverage).
- Seat: `KaidokuR34.R34ParserBounds`; actual answering model visible in the assignment: `openai-codex/gpt-6.1-sol`. No provider refusal, automatic switch, or alternate runtime was observed in this item.
- Base: `ec3125ad3d130d92f888a4128dfaa2982f36fff7`.
- Read `/home/vgpnk/.omp/agent/RULES.md`, lane instructions, applicable skills, both permitted source modules, and the three prior mutant reports below. Only permitted stop/hold/quarantine metadata was read; excluded builder materials and held item `U064N008Hf47eb933` were not opened or used.
- Read-only `git ls-tree` at the base identified parser blob `0ca6c1d5afad2fe5b8a2ca868ce634838e22a233` and sibling blob `d61d522bb04e4cb905385fa56132df1b90ff4718`. Read-only `git show` byte comparisons confirmed both live permitted source files exactly match those committed bytes before copying.
- Source inputs: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/chpe_profile.py` and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/selftest_pegen.py`.
- All writes are confined to this assigned report and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ParserBounds-files/`. Production scripts, LOG/docs, operator configuration, routing, and VCS state were not edited. Main remains sole integrator/VCS writer.

Prior reports read:

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/w1/WMutCount.md`: survived; equality case absent.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/w1/WMutMetadata.md`: inconclusive because pristine/mutated/restored all failed to spawn their first CLI child with `BlockingIOError: [Errno 11] Resource temporarily unavailable`. That report did not establish a kill. The present authorized probe independently supplies passing baselines; no cause is assigned to the prior EAGAIN.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/w1/WMutTag.md`: killed by selftest JSON-decoding crash, not a structured mismatch.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/prep/R33MutantLimits.md`: clause coverage must be killed or honestly bounded; historical frozen instruments must not be silently repaired in place.

## Mutants and expected detector

Each private copy received one behavior-bearing line change; the sibling and every fixture recipe/expectation stayed byte-identical. Predictions were retained before mutated execution in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ParserBounds-files/mutation-plan.json`.

| Copy / source line | One-line mutation | Expected existing detector | Actual verdict |
|---|---|---|---|
| count / 258 | `if cm_count > MAX_CODE_MAP_COUNT:` → `if cm_count >= MAX_CODE_MAP_COUNT:` | Original `--selftest`; expected survival because named limit recipe writes 2000, not 1024 | SURVIVED |
| metadata / 250 | `need(..., CHPE_METADATA_SIZE, "metadata")` → `need(..., 12, "metadata")` | `metadata_zero_tail` and `metadata_cross_section`, both layouts, should disagree with pinned outside-profile findings | KILLED: four structured mismatches |
| tag / 269 | `if tag not in TAGS:` → `if tag > 3:` | Existing `tag3`, both layouts; nonzero selftest failure kills only with passing pristine/restored runs | KILLED: selftest crash |

Source-derived corpus bound: AST inspection without importing the generator found **52 recipes × 2 layouts**, plus three auxiliary CLI launches = **107 maximum sequential CLI launches per complete invocation**. The selftest records 107 results; these are not independent carrier rows. The corpus source uses `len(entries)` for ordinary counts, zero for the empty case, and literal 2000 for its count-limit case (`selftest_pegen.py:48–52,105–106,257–280`). Static inspection found no 1024 literal or existing boundary recipe. The changed comparison differs only at equality; the three count stdout files are byte-identical.

## Identical bounded detector, nine actual runs

The unchanged detector in every phase was the private `chpe_profile.py --selftest`. Example actual count argv (identical for count pristine/mutated/restored; metadata/tag differ only by their private directory):

```text
/usr/bin/timeout --signal=TERM --kill-after=2s 30s /usr/bin/prlimit --as=268435456 --cpu=20 --fsize=1048575 --nproc=8192 --nofile=128 --core=0 -- /usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ParserBounds-files/count/chpe_profile.py --selftest
```

Recorder: `/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ParserBounds-files/run_probe.py KIND PHASE`. The recorder captures existing CLI streams and never imports either target module or builds fixture bytes.

Bounds: 30 seconds wall plus two-second kill escalation; recorder wait 35 seconds; 256 MiB address space, 20 CPU seconds, 1,048,575-byte file ceiling, 128 descriptors, no core dumps. `RLIMIT_NPROC=8192` is a fixed per-UID cap, **not** an isolated tree quota. Probes ran sequentially, with at most one existing CLI child beside the selftest parent; no concurrent detectors or workers were launched. `TMPDIR` was each copy's own `tmp/`; `LC_ALL=C.UTF-8`; Git override variables were removed. Every owned process group was absent after cleanup. Existing selftest fixture writes remained under the inherited file ceiling; no new PE fixture, recipe, generator, or held builder task was authored.

Actual detector window: `2026-10-23T10:25:13.233974+00:00` through `2026-10-23T10:25:51.905443+00:00`. Each individual run and each complete three-phase mutation probe finished below 120 seconds. Sum of detector/cleanup durations: count 6.901 s, metadata 6.801 s, tag 6.015 s. Full timestamps and exact argv are retained per receipt.

| Mutant | Phase | Seconds | Exit | stdout / stderr bytes | Actual detector output |
|---|---|---:|---:|---:|---|
| count | pristine | 2.317 | 0 | 21794 / 0 | pass=true; cases=107; failed=[] |
| count | mutated | 2.317 | 0 | 21794 / 0 | pass=true; cases=107; failed=[] |
| count | restored | 2.267 | 0 | 21794 / 0 | pass=true; cases=107; failed=[] |
| metadata | pristine | 2.267 | 0 | 21794 / 0 | pass=true; cases=107; failed=[] |
| metadata | mutated | 2.267 | 1 | 22613 / 0 | pass=false; cases=107; four mismatches |
| metadata | restored | 2.267 | 0 | 21794 / 0 | pass=true; cases=107; failed=[] |
| tag | pristine | 3.334 | 0 | 21794 / 0 | pass=true; cases=107; failed=[] |
| tag | mutated | 0.414 | 1 | 0 / 1114 | JSONDecodeError; no result summary |
| tag | restored | 2.267 | 0 | 21794 / 0 | pass=true; cases=107; failed=[] |

Every passing run reported 45/45 finding IDs, none uncovered, no unknown recipe IDs, and vocabulary_ok=true. **That full finding-ID coverage did not kill the equality mutant.** Both layouts' count-limit case still returned `outside_profile.code_map_count_limit`, exit 11.

Metadata mutated output: in **L0 and L1**, both `metadata_zero_tail` and `metadata_cross_section` returned `candidate.structural`, exit **0**, rather than their pinned `outside_profile.metadata_zero_tail` / `outside_profile.metadata_cross_section`, exit **11**. Its summary produced 43 finding IDs and listed those two absent IDs.

Tag mutated stderr ended:

```text
  File "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ParserBounds-files/tag/chpe_profile.py", line 328, in selftest
    out = json.loads(p.stdout)
...
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

The unchanged selftest hides the parser child's captured stderr on this path. The exact underlying child exception/interrupted case is **not directly observed** and is not asserted. Its nonzero failure between two passing runs supports a kill, but not a structured finding-ID assertion. No extra detector was run to recover child diagnostics.

## Before/after hashes and restoration

SHA-256:

| State / artifact | Digest |
|---|---|
| Parser lane before/after; all pristine/restored private parsers | `b364de7034be5fa09210cde8e0292570e6903cd837858993338b5c0027c1b71c` |
| Count mutant before/after detector | `e2ae2ccbac921e9d9c5e500faf03f16c378eb85f5157d04007e9f238ae65f492` |
| Metadata mutant before/after detector | `ede5fb65a206d9bfff54363e771e843ad7a1b0cd3a3a6889896a1131b8954a9e` |
| Tag mutant before/after detector | `589439faafb6473f30815ceec0a8cb711a5642b463a5e803d3da924ba0e7b35d` |
| Sibling lane/private, every phase | `aea5475c0ceadbccc6c0f3a1dd3b4e7abbd1d29d9000d8080ce7b9e5347e5b51` |
| All passing/count-mutated stdout | `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd` |
| Metadata mutated stdout | `f8c25e7a9078d1af4352f7ef719a24074ff9469db2c52b42b58ca082d9e511b3` |
| Tag mutated stderr | `4420301c5f8de4ec6ef6346981897de56e793f32d7ae3456162d5be2d173c7e1` |
| Empty streams | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Each mutated recorder restored the exact original parser bytes in `finally`, including the two failing detectors, **before** its restored run. Restoration UTC: count `10:25:42.331388`, metadata `10:25:46.901903`, tag `10:25:49.619970` (all 2026-10-23, +00:00). Per-run source hashes prove the detector itself did not alter either module. Final direct byte comparisons confirmed all private modules equal their original snapshots and both lane modules remain unchanged; all nine process groups were absent.

Restoration evidence: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ParserBounds-files/restoration.json`.

## Retained evidence and limits

Evidence root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34ParserBounds-files/`.

- `inputs.json`: pinned-source byte provenance and static corpus inventory.
- `mutation-plan.json`: pre-mutation expectations and planned source hashes.
- `count/`, `metadata/`, `tag/`: private restored modules, retained mutant parser, exact `mutation.patch`, and complete `pristine`, `mutated`, `restored` stdout/stderr/exit receipts.
- `run_probe.py`: bounded evidence-only recorder.
- `results.json`: all nine actual receipts and per-mutant verdicts.
- `restoration.json`: exact-byte comparisons and source before/after digests.
- `artifact-manifest.json`: retained-file byte counts and SHA-256 digests, relative to this absolute evidence root.

Exactly nine assigned behavioral detector invocations were exercised. No production reader, round-34 ELF reader, REA/MCP call, native carrier execution, independent fixture study, build, formatter, lint run, additional test, alternate backend, or delegation occurred. No new safety error or automatic model switch was observed. The tag JSONDecodeError is the current observed instrument failure; raw stderr is retained. No tool was installed or updated. Existing tools used: Python 3.14.8; `/usr/bin/timeout` GNU coreutils 9.12; `/usr/bin/prlimit` util-linux 2.42.4. No pacman transaction occurred.

No source successor patch is proposed or applied: the survivor lacks a permitted discriminating input. This closes the assigned instrument probe without reviving the stopped CHPE claim or changing any contract.

Trailer: `.ufo/waves/round-34/prep/R34ParserBounds.md`
