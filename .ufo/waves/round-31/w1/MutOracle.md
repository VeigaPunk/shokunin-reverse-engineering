# R31 wave 1 — MutOracle

## Result and scope

**[OBSERVATION] 12 single-point mutants: 8 killed, 4 survived, 0 inconclusive.** The pristine and restored modules each matched all 12 frozen carriers for every mutant seat (144/144 comparisons in each phase). The mutation phase made another 144 comparisons; the canonical reference required 12 additional calls. No REA command, C1 claim counter, external runtime, network fetch, subagent, Git/JJ command, or tool installation was used.

Attack target: the 12-carrier corpus's sensitivity to oracle defects, not the truth of R31-C1. **Verdict: fails to distinguish all 12 tested mutants**, with the four surviving source changes below as the counterexamples. This is a coverage finding, not permission to alter the frozen carrier list, predicate, target, or oracle. **[UNKNOWN]** R31-C1 itself was not evaluated here.

Axes: detection sensitivity, carrier-feature coverage, and byte-exact isolation/restoration. Only the assigned scratch copies were mutated. The only lane write is this report.

## Expected detector and method

1. Copied the lane oracle, carrier inventory and claims into `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle`; checked their full-byte SHA-256 against the frozen pins. The oracle hash was `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b`.
2. Created 12 isolated module copies, one per mutant. The detector first obtained JSON reports for all carriers from the pristine oracle, then exercised every still-pristine module. Any reference/baseline failure would make the probe inconclusive, never a kill.
3. Applied exactly one replacement or insertion per module. `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutations.json` records the original line, exact before/after text and expected mutated hash. The detector checked source equality against that one-point derivation and parsed the Python AST before loading each module. No mutations were stacked.
4. For each module/carrier, called `expected_report(absolute_path)`, JSON-round-tripped the result, and compared full JSON objects with the unmutated reference. Object key order was irrelevant; arrays and every field/value remained significant. A changed report **or an exception** killed a mutant. Report hashes are receipts, not a substitute for JSON equality.
5. Restored each edited point, then ran the same bounded detector again. All 12 module files were byte-identical to the pristine oracle and produced the original reports on all 12 carriers.

Bound: 300 seconds per command and a 10-second in-process alarm per `expected_report` call. All commands finished synchronously; no started process tree remained. Runtime: Python 3.14.8, system SQLite 3.54.0; the oracle opened carriers with `mode=ro&immutable=1`. Carrier hashes and byte counts matched before and after each phase; the lane oracle also retained its frozen hash.

## Mutation table

**[OBSERVATION]** Produced by the mutation command below, 2026-10-23T04:13:51Z, exit 0. “Changed” counts returned but unequal reports; “Raised” is separate because a raising oracle returns no report. Both are detector hits. Original line numbers refer to the frozen oracle.

| Mutant | Description / original point | Reports changed: count and ids | Oracle raised: count and ids | Verdict |
|---|---|---|---|---|
| `M01-ignore-overflow` | L133: Skip schema-record overflow-chain continuation. | 0: — | 5: `proj-341`, `proj-350`, `proj-361`, `proj-370`, `proj-371` | **killed** |
| `M02-interior-as-leaf` | L112: Parse interior table b-tree pages as leaf pages. | 0: — | 12: `proj-341`, `proj-350`, `proj-361`, `proj-370`, `proj-371`, `chinook`, `chinook-autoinc`, `gpkg-curve`, `gpkg-curvepolygon`, `gpkg-line-zm`, `gpkg-multisurface`, `gpkg-test-gpkg-nulls` | **killed** |
| `M03-ignore-reserved-bytes` | L93: Ignore reserved bytes when computing usable page size. | 0: — | 0: — | **survived** |
| `M04-swap-index-view` | L176: Swap index and view dispatch at the schema-row classification point. | 12: `proj-341`, `proj-350`, `proj-361`, `proj-370`, `proj-371`, `chinook`, `chinook-autoinc`, `gpkg-curve`, `gpkg-curvepolygon`, `gpkg-line-zm`, `gpkg-multisurface`, `gpkg-test-gpkg-nulls` | 0: — | **killed** |
| `M05-skip-trigger-fold` | L206: Skip trigger-target ASCII case-fold normalization. | 0: — | 0: — | **survived** |
| `M06-lowercase-declared-type` | L189: Lowercase declared column types instead of preserving their spelling. | 12: `proj-341`, `proj-350`, `proj-361`, `proj-370`, `proj-371`, `chinook`, `chinook-autoinc`, `gpkg-curve`, `gpkg-curvepolygon`, `gpkg-line-zm`, `gpkg-multisurface`, `gpkg-test-gpkg-nulls` | 0: — | **killed** |
| `M07-drop-hidden-field` | L191: Omit the hidden field from every column record. | 12: `proj-341`, `proj-350`, `proj-361`, `proj-370`, `proj-371`, `chinook`, `chinook-autoinc`, `gpkg-curve`, `gpkg-curvepolygon`, `gpkg-line-zm`, `gpkg-multisurface`, `gpkg-test-gpkg-nulls` | 0: — | **killed** |
| `M08-virtual-count-zero` | L196: Report zero columns for every virtual table, including unresolved ones. | 5: `gpkg-curve`, `gpkg-curvepolygon`, `gpkg-line-zm`, `gpkg-multisurface`, `gpkg-test-gpkg-nulls` | 0: — | **killed** |
| `M09-ignore-without-rowid` | L195: Always report without_rowid=false. | 5: `proj-341`, `proj-350`, `proj-361`, `proj-370`, `proj-371` | 0: — | **killed** |
| `M10-root-page-plus-one` | L193: Increment each table root_page by one. | 12: `proj-341`, `proj-350`, `proj-361`, `proj-370`, `proj-371`, `chinook`, `chinook-autoinc`, `gpkg-curve`, `gpkg-curvepolygon`, `gpkg-line-zm`, `gpkg-multisurface`, `gpkg-test-gpkg-nulls` | 0: — | **killed** |
| `M11-zero-hidden-value` | L191: Erase nonzero hidden/generated column flags while retaining the field. | 0: — | 0: — | **survived** |
| `M12-ignore-strict` | L195: Always report strict=false. | 0: — | 0: — | **survived** |

**Total killed: 8/12 (66.7%); survivors: M03, M05, M11, M12.** The mutation phase recorded 58 changed reports and 17 raised calls (75 detector hits), with 69 equal reports. In particular, removing the `hidden` key (M07) is detected, while incorrectly zeroing its value (M11) is not.

## What would expose each survivor

These are **[INFERENCE] carrier designs**, not additions to the frozen corpus and not extra executed carrier tests. Their present absence is grounded by `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/baseline.json` feature receipts and the mutation outcomes above.

| Survivor | Observation on these 12 carriers | Carrier that would expose it / expected distinction |
|---|---|---|
| M03 — reserved bytes | Every carrier's SQLite header reserved-byte count is 0. | A valid SQLite snapshot with nonzero reserved space (for example 64 bytes per page) and a long `sqlite_schema` record that uses overflow pages. Its cell-local and overflow payload boundaries must depend on the reduced usable page size. The original subtracts the reserve; M03 uses the full page size and misreads those boundaries, changing the report or raising. Merely changing header byte 20 without rebuilding a valid database is not a valid witness. |
| M05 — trigger folding | Skipping trigger target canonicalization changed no carrier report. | A readable schema-edited snapshot with a table named `CamelCase`, but a trigger row whose stored `sqlite_schema.tbl_name` is `camelcase`; `PRAGMA table_list` must retain `CamelCase`. The original reports trigger table `CamelCase`, M05 reports `camelcase`. A deliberate `writable_schema` fixture retaining correct trigger SQL is the input design; its construction/loadability was not tested. Ordinary mixed-case `CREATE TRIGGER` alone is not asserted sufficient because SQLite may canonicalize the stored target. |
| M11 — hidden/generated flags | All reported ordinary-table columns have `hidden=0`; virtual-table columns are deliberately omitted by the original oracle. | An ordinary table containing generated columns, e.g. `CREATE TABLE t(a INTEGER, b INTEGER GENERATED ALWAYS AS (a+1) VIRTUAL, c INTEGER GENERATED ALWAYS AS (a+2) STORED);`. `table_xinfo` supplies flags 2 and 3; the original preserves them, M11 emits 0. |
| M12 — strict flag | No table in any carrier has `strict=true`. | A snapshot containing `CREATE TABLE t(a INTEGER) STRICT;`. The original reports `strict=true`, M12 emits false. |

**[UNKNOWN]** The proposed witness databases were not constructed or run; their distinctions above follow from the selected source expressions and stated input conditions. In particular, no claim is made that an ordinary DDL-only database necessarily reaches M05's fallback branch.

## Commands, actual outputs and time receipts

**[OBSERVATION]** All three detector invocations exited 0. That means the probe completed; it is not a claim-counter pass. No frozen target line was run or claimed. All stderr files are empty. The full stdout follows without elision.

| Phase | Producing command | UTC interval | Exit |
|---|---|---|---|
| baseline | `timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/probe.py --phase baseline` | 2026-10-23T04:13:25Z – 2026-10-23T04:13:26Z | 0 |
| mutated | `timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/probe.py --phase mutated` | 2026-10-23T04:13:51Z – 2026-10-23T04:13:51Z | 0 |
| restored | `timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/probe.py --phase restored` | 2026-10-23T04:14:17Z – 2026-10-23T04:14:18Z | 0 |

### baseline: exact stdout

```text
UTC_START 2026-10-23T04:13:25Z
COMMAND timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/probe.py --phase baseline
DETECTOR phase=baseline carriers=12 modules=12 per_call_timeout=10s
M01-ignore-overflow calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M02-interior-as-leaf calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M03-ignore-reserved-bytes calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M04-swap-index-view calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M05-skip-trigger-fold calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M06-lowercase-declared-type calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M07-drop-hidden-field calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M08-virtual-count-zero calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M09-ignore-without-rowid calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M10-root-page-plus-one calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M11-zero-hidden-value calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
M12-ignore-strict calls=12 equal=12 changed=0 raises=0 verdict=baseline-ok changed_ids=- raised_ids=-
RESULT phase=baseline mutants=12 killed=0 survived=0 inconclusive=0
UTC_END 2026-10-23T04:13:26Z
EXIT 0
```

### mutated: exact stdout

```text
UTC_START 2026-10-23T04:13:51Z
COMMAND timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/probe.py --phase mutated
DETECTOR phase=mutated carriers=12 modules=12 per_call_timeout=10s
M01-ignore-overflow calls=12 equal=7 changed=0 raises=5 verdict=killed changed_ids=- raised_ids=proj-341,proj-350,proj-361,proj-370,proj-371
  FIRST_EXCEPTION proj-341 OracleError: byte parser and libsqlite3 disagree on sqlite_schema
M02-interior-as-leaf calls=12 equal=0 changed=0 raises=12 verdict=killed changed_ids=- raised_ids=proj-341,proj-350,proj-361,proj-370,proj-371,chinook,chinook-autoinc,gpkg-curve,gpkg-curvepolygon,gpkg-line-zm,gpkg-multisurface,gpkg-test-gpkg-nulls
  FIRST_EXCEPTION proj-341 error: unpack requires a buffer of 8 bytes
M03-ignore-reserved-bytes calls=12 equal=12 changed=0 raises=0 verdict=survived changed_ids=- raised_ids=-
M04-swap-index-view calls=12 equal=0 changed=12 raises=0 verdict=killed changed_ids=proj-341,proj-350,proj-361,proj-370,proj-371,chinook,chinook-autoinc,gpkg-curve,gpkg-curvepolygon,gpkg-line-zm,gpkg-multisurface,gpkg-test-gpkg-nulls raised_ids=-
  FIRST_DIFFERENCE {"actual": 7, "carrier": "proj-341", "expected": 21, "path": "$.schema.indexes.length"}
M05-skip-trigger-fold calls=12 equal=12 changed=0 raises=0 verdict=survived changed_ids=- raised_ids=-
M06-lowercase-declared-type calls=12 equal=0 changed=12 raises=0 verdict=killed changed_ids=proj-341,proj-350,proj-361,proj-370,proj-371,chinook,chinook-autoinc,gpkg-curve,gpkg-curvepolygon,gpkg-line-zm,gpkg-multisurface,gpkg-test-gpkg-nulls raised_ids=-
  FIRST_DIFFERENCE {"actual": "text", "carrier": "proj-341", "expected": "TEXT", "path": "$.schema.tables[0].columns[0].declared_type"}
M07-drop-hidden-field calls=12 equal=0 changed=12 raises=0 verdict=killed changed_ids=proj-341,proj-350,proj-361,proj-370,proj-371,chinook,chinook-autoinc,gpkg-curve,gpkg-curvepolygon,gpkg-line-zm,gpkg-multisurface,gpkg-test-gpkg-nulls raised_ids=-
  FIRST_DIFFERENCE {"actual": {"__detector_missing_key__": true}, "carrier": "proj-341", "expected": 0, "path": "$.schema.tables[0].columns[0].hidden"}
M08-virtual-count-zero calls=12 equal=7 changed=5 raises=0 verdict=killed changed_ids=gpkg-curve,gpkg-curvepolygon,gpkg-line-zm,gpkg-multisurface,gpkg-test-gpkg-nulls raised_ids=-
  FIRST_DIFFERENCE {"actual": 0, "carrier": "gpkg-curve", "expected": 5, "path": "$.schema.tables[9].column_count"}
M09-ignore-without-rowid calls=12 equal=7 changed=5 raises=0 verdict=killed changed_ids=proj-341,proj-350,proj-361,proj-370,proj-371 raised_ids=-
  FIRST_DIFFERENCE {"actual": false, "carrier": "proj-341", "expected": true, "path": "$.schema.tables[0].without_rowid"}
M10-root-page-plus-one calls=12 equal=0 changed=12 raises=0 verdict=killed changed_ids=proj-341,proj-350,proj-361,proj-370,proj-371,chinook,chinook-autoinc,gpkg-curve,gpkg-curvepolygon,gpkg-line-zm,gpkg-multisurface,gpkg-test-gpkg-nulls raised_ids=-
  FIRST_DIFFERENCE {"actual": 3, "carrier": "proj-341", "expected": 2, "path": "$.schema.tables[0].root_page"}
M11-zero-hidden-value calls=12 equal=12 changed=0 raises=0 verdict=survived changed_ids=- raised_ids=-
M12-ignore-strict calls=12 equal=12 changed=0 raises=0 verdict=survived changed_ids=- raised_ids=-
RESULT phase=mutated mutants=12 killed=8 survived=4 inconclusive=0
UTC_END 2026-10-23T04:13:51Z
EXIT 0
```

### restored: exact stdout

```text
UTC_START 2026-10-23T04:14:17Z
COMMAND timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/probe.py --phase restored
DETECTOR phase=restored carriers=12 modules=12 per_call_timeout=10s
M01-ignore-overflow calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M02-interior-as-leaf calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M03-ignore-reserved-bytes calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M04-swap-index-view calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M05-skip-trigger-fold calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M06-lowercase-declared-type calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M07-drop-hidden-field calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M08-virtual-count-zero calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M09-ignore-without-rowid calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M10-root-page-plus-one calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M11-zero-hidden-value calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
M12-ignore-strict calls=12 equal=12 changed=0 raises=0 verdict=restored-ok changed_ids=- raised_ids=-
RESULT phase=restored mutants=12 killed=0 survived=0 inconclusive=0
UTC_END 2026-10-23T04:14:18Z
EXIT 0
```

## Before / mutant / restored hashes

**[OBSERVATION]** Before **and** restored SHA-256 for every one of the 12 module copies: `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` (9,247 bytes). `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/baseline.json` and `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/restored.json` record each path, measured hash and its 12 successful comparisons. The lane oracle's after hash was the same. Actual mutation-phase hashes, independently checked against the one-point specifications, were:

| Mutant | Actual mutated SHA-256 |
|---|---|
| `M01-ignore-overflow` | `c723993c59df4c17d18949b22414cbf1e922c28ab0a191e47cbe23be3b4339c6` |
| `M02-interior-as-leaf` | `1a910eb3c8a69fec8868ff91ee0b733ccb036f1a407a26bfc2b1973475fe6f33` |
| `M03-ignore-reserved-bytes` | `7625366c4c47c2183fcea7c05a4be9a251671401fb015c49388acda61e56b193` |
| `M04-swap-index-view` | `418d1abea730695d7cae83732d5dce0c1a94ae368fac133c9decab493d94e18d` |
| `M05-skip-trigger-fold` | `9a37a535e2b4c3c30b9f4377bc35899ceade8eb04ebb51aab65b552822121107` |
| `M06-lowercase-declared-type` | `f80fb843cae7898eef853b94ec0c8f03e44114cfc8a1567edd7f447663529ace` |
| `M07-drop-hidden-field` | `546f32c204c233fbfad441eaba60cc8b8e96ff7c1ef441d33ac4a24fc2897b85` |
| `M08-virtual-count-zero` | `5d54a0005654115551d15091a2da54572ab155ff6677777a1fddfd67ae5bb19e` |
| `M09-ignore-without-rowid` | `10e9f83160dc84360217406e6fb6d597b3586f5a2aed1f1f524ab8f895ac6189` |
| `M10-root-page-plus-one` | `3ade23983edf6636e54140986be7814867d2a3fc6bd7ed9f7dab2f5a1f39d8ff` |
| `M11-zero-hidden-value` | `2ba38de50d2314eb45a00df0960c35c8c27f56df46ffb90a34e7247c13e2acd1` |
| `M12-ignore-strict` | `2bdfae5294b2952c8ba4f6408b4187c8b56338b92a240c67546a960803ff528f` |

Mutated source is retained as exact reversible before/after text in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutations.json`, not left installed. Every module artifact listed below now contains restored bytes. No carrier, immutable directory, sibling source, Git index or lane state was altered.

## Frozen carrier identity receipts

**[OBSERVATION]** The detector opened only these 12 input carriers. All pins matched in baseline, mutated and restored phases, both before and after report computation. The full carrier bytes are binary SQLite artifacts, not line-oriented textual sources; the located header signature is `SQLite format 3\x00` at byte offset 0. Access date: 2026-10-23. Local source URLs are `file://` plus each absolute path below.

| Id | Absolute carrier path | Bytes | SHA-256 |
|---|---|---:|---|
| `proj-341` | `/fast/scratch/hyaku/kaidoku-r31/carriers/proj-341.db` | 8278016 | `97a04533b1e7e3bfea9be2e11cc4e43a60539020d8cdd02622203d82db4c2414` |
| `proj-350` | `/fast/scratch/hyaku/kaidoku-r31/carriers/proj-350.db` | 8495104 | `deaa7e9db95ef993358557441d33d26c24e01edb82c82021e8f639cadbb284c2` |
| `proj-361` | `/fast/scratch/hyaku/kaidoku-r31/carriers/proj-361.db` | 8581120 | `79b660eb3c09f50c0f251e958db7cbf9a2d5d18d2836e99082095b31c7e029c5` |
| `proj-370` | `/fast/scratch/hyaku/kaidoku-r31/carriers/proj-370.db` | 9154560 | `976d427f037791c88b8d051a452e1fb13157c1c14b6e56d5a868097a4813cb7e` |
| `proj-371` | `/fast/scratch/hyaku/kaidoku-r31/carriers/proj-371.db` | 9261056 | `a25d85a2ebfc4584eba65186b7c41743b084ce5d391941cbb41c805947b77109` |
| `chinook` | `/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite` | 1067008 | `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` |
| `chinook-autoinc` | `/fast/scratch/hyaku/kaidoku-r31/carriers/chinook-autoinc.sqlite` | 1067008 | `ca157cb58cb34ed2e5d4eb3418ae7a9418f0cfe8b751985b6a4482346c9548d4` |
| `gpkg-curve` | `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curve.gpkg` | 98304 | `03a9c5904fd3075c61ba96e5bf0aac381721d43799db23c06634a0c56e04f302` |
| `gpkg-curvepolygon` | `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curvepolygon.gpkg` | 98304 | `00a1309ab0f29f97a4c5f6cb9cd3bde27143fc936712d5101767f60f0c96bac7` |
| `gpkg-line-zm` | `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-line-zm.gpkg` | 98304 | `9563e513b064476ee7ab8c66858f3f434307ca554f7495652d09674d2747c70c` |
| `gpkg-multisurface` | `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-multisurface.gpkg` | 98304 | `898a238bc119f051622c22de973899f501466a33a6a6c0cc405122802c6d648d` |
| `gpkg-test-gpkg-nulls` | `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-test-gpkg-nulls.gpkg` | 98304 | `4281d3c55f2042e2174ab9a13c5c5a06d13841071c1aa3ea2cc131afaf71e1d8` |

## Local primary-source receipts

No external primary source was fetched. The consulted source bytes were captured by ordinary local reads on 2026-10-23:

| Source URL | SHA-256 of complete bytes read | Located quote (at most 25 contiguous words) |
|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` | L18–19: “The library's own sqlite_schema rows must equal the byte parser's rows, or the oracle raises.” |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | L9: `pyogrio-0.11.1/pyogrio/tests/fixtures/curve.gpkg` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | L21: “All carriers UTF-8, no WAL.” |

## Retained scratch artifacts

**[OBSERVATION]** Every retained scratch file is listed with its SHA-256. Artifact hashing used the exact command recorded in `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/evidence-manifest.json`: `timeout 30 sha256sum` followed by all 26 then-existing absolute file paths. It exited 0 at 2026-10-23T04:15:43.428Z; its complete output is `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/checksums.stdout.txt`. The checksum-output hash and the manifest's own hash were computed over their exact written UTF-8 bytes. The manifest excludes itself to avoid self-reference. No tools were installed or updated.

| Absolute artifact path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutations.json` | `ad4795da1c5495eb47db8338d6860323181d845ff56f683fb8d8a43fc04e75cb` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/probe.py` | `1c62bfaf36346e6befbe96c76d2e4c1ddf3fc40d53eeba5ad4f6fc353d092582` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/baseline.json` | `93008ef49973b76fff81c6102e61b36d341e3e879f0d6b63eeba763afb4aaffd` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/baseline.stdout.txt` | `f2d93ce0cdc4b20ec359b7df48b7387c00f1d08095dad7ec57eae4d73a71c03a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/baseline.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutated.json` | `3003e0270baf66b12bf3ee87e5875027b5a6e09b82922691314296be1b230bf2` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutated.stdout.txt` | `0c8c2a59b1885d3ca48c1a44523bb9609fab67d100f8633208be2dfd448e8b62` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutated.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/restored.json` | `280329bd7da5296759902b96bcc4e6962118a3c03b7a1cbe8c1ced8b9861b5b2` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/restored.stdout.txt` | `db0fe4412b9477419607168e61e5205b3e4d1df656ee691b40097ec707a800be` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/restored.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M01-ignore-overflow/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M02-interior-as-leaf/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M03-ignore-reserved-bytes/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M04-swap-index-view/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M05-skip-trigger-fold/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M06-lowercase-declared-type/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M07-drop-hidden-field/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M08-virtual-count-zero/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M09-ignore-without-rowid/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M10-root-page-plus-one/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M11-zero-hidden-value/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/mutants/M12-ignore-strict/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/checksums.stdout.txt` | `8bb714ab942e9d88da470600a21d883e0aad0d1545050c40c4f52e392c2a6749` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w1/MutOracle/evidence-manifest.json` | `a9dd02e3348778cb7e7bebee7e3d4392b506b17910fac21b6d745302b421978e` |

Permanent repository code, callsites, tests and documentation are intentionally unchanged: this assignment is an isolated mutation investigation only. No further checks were run beyond the three bounded behavioral detector invocations and artifact hashing.
