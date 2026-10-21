PARTIAL — C3 detector robustness: 3/6 assigned mutants killed, 3/6 survived; pristine and all six restored states retain 19/19 matches.

# MutateCompareFF — author-side falsification

Attacks: C3's kind/index/silence comparison and first-Go-failure extraction (`.ufo/waves/round-20/claims.json:33-39`, `contract.md:76-81`), including the recovered envelope integration defect described in `corpus/lessons/round-20.md` Mistake 5. This is a detector-coverage finding, not a claim that the original 19 forecasts are false, and not an outside review or admission judgment.

Axes: **calibration** (separate survival from successful replay), **coverage** (six specified mutation classes), **depth** (kind/index/null semantics and the real extractor interface).

## Revision and isolation evidence — observed

- B: `14f0260ad319ecc26994381b2415d5a999003375`; F: `808cbb31a1e24656da5ba4967497e602fbca7415`; measured S: `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`.
- Created `/tmp/kr20w2-MutateCompareFF-5z1aycxs` using `tempfile.mkdtemp(prefix='kr20w2-MutateCompareFF-')`, then `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin <scratch>` (exit 0), `git -C <scratch> checkout -q --detach S` (exit 0), `git -C <scratch> rev-parse HEAD` (exit 0; exact S above).
- Read revision-scoped sources with `git -C LANE --no-optional-locks show S:<path>`. Both tested tool files were byte-identical to S and F before mutation. All 19 emulator-output prediction files were byte-identical at S and F; all 19 log copies equalled their S blobs and the SHA-256 in their S `runs/<label>/comparison-log-binding.json` (`verified: true`). No live lane inputs were substituted.
- One mutant at a time, only in this private clone. After each, restored exact source bytes and reran the identical detector suite before the next mutation. Scratch was removed after final restoration; no patch/product change remains. The only lane write is this report.

## Bounded detector commands

C = `.ufo/waves/round-20/tools/compare-first-failure.py`; E = `.ufo/waves/round-20/tools/first-failure-extract.py`.

Executed from the clone, in pristine, each of six mutant states, and each of six restored states:

```text
python3 -I -B .ufo/waves/round-20/tools/compare-first-failure.py --selftest
python3 -I -B .ufo/waves/round-20/tools/first-failure-extract.py --selftest
python3 -I -B .ufo/waves/round-20/tools/compare-first-failure.py --prediction .ufo/waves/round-20/predictions/swiss-misread-v2/<label>.json --log .ufo/waves/round-20/runs/<label>/logs/<session>/ghidra.log --extractor .ufo/waves/round-20/tools/first-failure-extract.py
```

The third command ran separately for each of the 19 labels/sessions below. Commands within one unchanged state used a six-worker `ThreadPoolExecutor`, each subprocess had a 120-second timeout; no timeouts occurred. Mutations/restorations were sequential. Original selftests created/removed their own system-temp fixtures, outside the clone. No REA, Ghidra, Go binary, other agent runtime, install, or update was invoked. Existing interpreter: Python 3.14.8.

## Mutant → expected detector → observed → verdict

All coordinates below refer to S. Label columns count exits **0 / 1 / 2**, not independent forecast accuracy estimates.

| Mutant and smallest changed behavior | Expected finding | Comparator selftest: exit / stdout | Extractor selftest: exit / stdout | 19-label exits 0/1/2 | Verdict |
|---|---|---|---|---|---|
| M1 ignore index: C:34 returns kind equality only | Existing `index_mismatch` must fail | 1 / `SELFTEST: FAILED cases=6 fails=index_mismatch` | 0 / `SELFTEST: CLEAN cases=4` | 19 / 0 / 0 | **KILLED**, selftest only |
| M2 ignore kind: C:34 returns index equality only | Different kinds at equal index must mismatch; no such existing selftest | 0 / `SELFTEST: CLEAN cases=6` | 0 / `SELFTEST: CLEAN cases=4` | 19 / 0 / 0 | **SURVIVED** |
| M3 null matches anything: C:33 returns `True` when either side is null | Object/null in either direction must mismatch; existing `both_silent` does not exercise this | 0 / `SELFTEST: CLEAN cases=6` | 0 / `SELFTEST: CLEAN cases=4` | 19 / 0 / 0 | **SURVIVED** |
| M4 drop envelope unwrap: delete C:75-76 | Real extractor envelope must be accepted; regression should break integration | 0 / `SELFTEST: CLEAN cases=6` | 0 / `SELFTEST: CLEAN cases=4` | 0 / 0 / 19 | **KILLED**, real integration only; every label reports `extractor result: kind must be a non-empty string` |
| M5 take first ERROR: replace E:159-168 selection with `if record["level"] != "ERROR": continue` | `first_go_failure_with_invalid_index` and `absence_bounded_by_last_line` must reject a preceding/unrelated wrapper ERROR | 0 / `SELFTEST: CLEAN cases=6` | 1 / `SELFTEST: FAILED ... cases=4 fails=2` (exact output below) | 19 / 0 / 0 | **KILLED**, selftest only |
| M6 include AnalysisTaskWrapper: add it to E:37's component allowlist; leave I/O/summary qualification unchanged | A wrapper I/O ERROR before the Go failure, or without a Go failure, must stay in `other_errors`; absent from current fixtures | 0 / `SELFTEST: CLEAN cases=6` | 0 / `SELFTEST: CLEAN cases=4` | 19 / 0 / 0 | **SURVIVED** |

Pristine: both selftests exit 0 with the CLEAN outputs above; 19 label commands exit 0. Every restored state exactly reproduces all pristine argv/exit/stdout/stderr tuples. Thus no baseline failure was miscounted as a kill; no probe is inconclusive. All command stderr was empty, including the detected failures.

Exact M5 extractor stdout (exit 1):

```text
SELFTEST: FAILED first_go_failure_with_invalid_index expected={'kind': 'invalid_index', 'index': 41, 'line': 2, 'cause_line': 4, 'phase': 'markup', 'other_components': ['AnalysisTaskWrapper', 'GolangStringAnalyzer']} actual={'kind': 'other', 'index': None, 'line': 1, 'cause_line': 1, 'phase': 'analysis', 'other_components': ['GolangSymbolAnalyzer', 'GolangStringAnalyzer']}; absence_bounded_by_last_line expected={'kind': None, 'index': None, 'line': None, 'cause_line': None, 'phase': None, 'other_components': ['AnalysisTaskWrapper'], 'last_line': 3} actual={'kind': 'other', 'index': None, 'line': 1, 'cause_line': 1, 'phase': 'analysis', 'other_components': [], 'last_line': 3} cases=4 fails=2
```

Example M4 comparator stdout for addr2line (exit 2; all 19 have the same error/match/observed fields, preserving each original prediction):

```json
{"error":"extractor result: kind must be a non-empty string","match":null,"observed":null,"predicted":{"index":22078465,"kind":"invalid_index","phase":"markup_walk","va":5318176}}
```

## Actual 19-label replay outputs, compacted

Every row below had exit 0, `match:true`, empty stderr in pristine, M1/M2/M3/M5/M6, and all six restored states; the full comparator stdout bytes were identical across those states. `invalid_index:N` means both prediction and observation had that kind/index. For those eight rows predicted phase=`markup_walk`, observed phase=`markup`, observed va=null; the predicted va is listed. Null rows have predicted=null and observed=null. M4 instead had exit 2 / match=null for **every** row, as above.

| Label | Session under `runs/<label>/logs/` | Predicted = observed kind/index | Predicted va |
|---|---|---|---:|
| t1246-addr2line | rea-ghidra-P9tyVR | invalid_index:22078465 | 5318176 |
| t1246-asm | rea-ghidra-15p1Vy | null | — |
| t1246-buildid | rea-ghidra-qGQ7Im | null | — |
| t1246-cgo | rea-ghidra-I0zRdH | null | — |
| t1246-compile | rea-ghidra-Q6goA3 | invalid_index:36421889 | 14607072 |
| t1246-covdata | rea-ghidra-314Y9f | null | — |
| t1246-cover | rea-ghidra-mFkiDF | null | — |
| t1246-doc | rea-ghidra-wQaOa9 | null | — |
| t1246-fix | rea-ghidra-Zvh0Na | null | — |
| t1246-go | rea-ghidra-2PFXTv | invalid_index:35082496 | 10925280 |
| t1246-gofmt | rea-ghidra-jjj6WB | null | — |
| t1246-nm | rea-ghidra-xpz849 | invalid_index:22070273 | 5308992 |
| t1246-objdump | rea-ghidra-uLjgCv | invalid_index:13816064 | 6205248 |
| t1246-pack | rea-ghidra-Dhu23X | null | — |
| t1246-pprof | rea-ghidra-hCPl3X | invalid_index:27091201 | 10516608 |
| t1246-preprofile | rea-ghidra-JcCFCG | null | — |
| t1246-test2json | rea-ghidra-tU5R8R | null | — |
| t1246-trace | rea-ghidra-Vwh31x | invalid_index:25696001 | 9056416 |
| t1246-vet | rea-ghidra-AW49O8 | invalid_index:13791488 | 7484672 |

## Before/mutated/after hashes and restoration

Full SHA-256 baselines (also equal F):

```text
C0 44150d137c8ac07321da133d50e7c8f12c664bb12d64cf0a9a66c0ab9595121f  compare-first-failure.py
E0 aa4372b28d7228d07d44980c8bf3ebe3ed65b1fab5ca38bcee5d76c273b8e485  first-failure-extract.py
```

Each experiment's **before and after pair is exactly (C0,E0)**. Only the named target had the mutated hash below; its companion remained at its baseline. Direct byte equality against `git show S:<target>` was checked after every restoration, in addition to hashes.

| Mutant | Target | Mutated SHA-256 | Mutant suite completed / restored suite completed (2026-10-21, -03:00) |
|---|---|---|---|
| M1 | C | dadc5ef9ceb15cb8abbf8e25621b8796bc19a1fa4ef01832ecff99b988ac11b2 | 04:09:59 / 04:10:05 |
| M2 | C | 8f2889b4295a6805d349963b5430b83594e5fa42a8536f5f6c9794eeaa9dd547 | 04:10:11 / 04:10:17 |
| M3 | C | 66d5fac3ae33c83967c5311fd628119b156f6b32329b812031ba95745ac09b98 | 04:10:28 / 04:10:33 |
| M4 | C | 5ded82058796ae05b94c46c3a977b038e7fedbc0c1061fa78bdf0fcf75bc4f2f | 04:10:42 / 04:10:48 |
| M5 | E | e19ecb0c0b95486fa7c82c42c6f7946d979bea06d5f3ff31e81cfdbf3286d38a | 04:10:53 / 04:11:02 |
| M6 | E | ef4d8665afd2425748bcd9bbaed889f6c05917cabf33c73daaedfcafe51be940 | 04:11:08 / 04:11:16 |

Pristine suite completed at 2026-10-21T04:09:38-03:00. Final restored hashes were C0/E0. After comparing all six restored suites with pristine and confirming input copies still equalled S, removed the private clone; cleanup clock: 2026-10-21T04:12:09-03:00. All times came from the host clock.

## Coverage interpretation

**Observed:** kind/index/silence replay remains 19/19 on S, but the unchanged bounded detectors accept M2, M3 and M6. Existing comparison cases have equal kinds even in `index_mismatch`, and only symmetric nulls (`.ufo/waves/round-20/tools/compare-first-failure.py:111-125`). Its CLI selftest supplies a bare-object stub rather than the real envelope (`:127-145`); the real 19-label replay, not either selftest, kills M4. Extractor fixtures use `AnalysisTaskWrapper` with `NullPointerException`, not an I/O exception (`.ufo/waves/round-20/tools/first-failure-extract.py:201-255`), so the M6 component addition does not qualify those errors under its remaining filter (`:159-168`).

**Inference, not additional probes:** discriminating negative cases are equal-index/different-kind, asymmetric null/object in both directions, and a wrapper I/O ERROR preceding/without a Go failure. Their absence explains these survivors; survival does not authorize broadening the contract. This seat changed neither tests nor production behavior and makes no universal correctness claim beyond the six bounded mutation results.
