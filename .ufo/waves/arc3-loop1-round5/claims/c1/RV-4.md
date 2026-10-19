# RV-4 — C1 correctness sweep

Assignment: c1, per `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-36,83-85`. Re-derived from Git objects and landed evidence; no prior seat's measurements are used below. `git rev-parse HEAD` → `71668ccd2c920b907672b5c40efaafe7c2e75bd1`.

## (a) Command A — REPRODUCED; revision-grouping DISCREPANCY

Replayed the recipe at `SCORECARD.md:88-124` against each named work snapshot plus HEAD. Full outputs:

```text
fbbbd45  {"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
28aa7a9  {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
c418be0  {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
5be4a26  {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
520341d  {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
40de383  {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
71668cc  {"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668cc", "rule_blocks": 14}
```

The measured R1/R2/R3/R4 work snapshots reproduce the recorded counts; comparison targets are `SCORECARD.md:1389-1392,1474-1476,1550-1554,1611-1612`. The supplied grouping of `5be4a26` with R2 is not supported by Git ancestry: `git show -s --format='%H%n%P%n%s' 5be4a26` identifies its parent as `c418be0` and subject as `hygiene`. The tree diff from `28aa7a9` to `5be4a26` includes `A corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`; that later tree therefore measures 83/83, while the actual R2 work hash `28aa7a9` measures 82/82. Correct association: 5be4a26 is after the R3 work snapshot, not a second R2 work result.

## (b) Custody-pair selftest — REPRODUCED; invocation DISCREPANCY

The supplied flag form, `python3 .ufo/gates/custody-pair/custody-pair.py --selftest`, exits 2 with `error: the following arguments are required: cmd`. The CLI defines a `selftest` subcommand (`custody-pair.py:1308-1333`). Re-running with safe scratch explicitly under `/dev/shm`:

```text
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

Thus the 28-case result reproduces; the short-form `--selftest` invocation does not.

## (c) Citation-drift probe — REPRODUCED, both modes

`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .`:

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
```

`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict`:

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

## (d) Census v10 — REPRODUCED

`python3 .ufo/gates/c1-census-v10.py --root .` returned exit 0. Exact summary lines:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1631 loci=9
SKILL.md       lines=390  loci=2
SCOPE-ERRORS (marker assertions): []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

## (e) PROVINCE line hold and nine stale literals — line hold REPRODUCED; absence DISCREPANCY

Independent `git show REV:PROVINCE.md | wc -l` results: `520341d=162`, `40de383=162`, `71668cc=162`; worktree `wc -l` = `162`.

Re-ran `grep -F -c -- "$literal" PROVINCE.md` for the nine strings enumerated as the test vector at `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:1-10`. Counts (zero means absent):

```text
0  Reserve: 91MB Godot ARM64 template
0  all 3 organic cores
1  JEB (unprobed)
0  real solc/vyper-compiled bytecode untested
0  Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`
0  probe-refused since r2
0  pacman pairs beyond expac unexercised
0  absent: `7z`
0  35 features incl. PyGhidra/BSim
```

Correction: 8/9 strings are absent; `JEB (unprobed)` remains at `PROVINCE.md:87-88` (`Alternate providers`). The nine-absence claim does not reproduce as written.

## (f) Vyper entry spot-check — REPRODUCED

Against `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin`, its hex twin, `evidence/planted-K.json:23-39`, and the three saved probe envelopes (`evidence/probe/probe-6.4.0-hex.json:1`, `probe-6.4.0-raw.json:1`, `probe-6.7.0-hex.json:1`), an independent Python-stdlib re-read and comparison produced:

```text
runtime.bin bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
runtime.hex decoded_bytes=1562 same_bytes=True sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
planted K=15 unique=15
probe-6.4.0-hex.json: functions=15 selectors_unique=15 K_equal=True missing=[] extra=[] dispatch={'abi': 15} bytes=1562 decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.4.0-raw.json: functions=15 selectors_unique=15 K_equal=True missing=[] extra=[] dispatch={'abi': 15} bytes=1562 decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.7.0-hex.json: functions=15 selectors_unique=15 K_equal=True missing=[] extra=[] dispatch={'abi': 15} bytes=1562 decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
```

Also ran the byte-level checker `python3 .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/dispatch-census.py .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/planted-K.json .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json`. Relevant exact output:

```text
runtime bytes: 1562
assumed jump table at 0x600 (13 buckets x 2 B) -> tail 26 B
execution reached the leg-derived body: 15/15
agreement: 15/15
probe recovered 15 selectors; leg chains carry 15
probe set == leg-chain set: True
probe extras: []
leg-chain only: []
```

The same output lists all 13 table targets at byte `0x5b` and selector chains shaped `JUMPDEST PUSH4 DUP2 XOR PUSH2 JUMPI`; this re-derives the modulo-13 jump-table/XOR dispatcher at `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex`. It agrees with the Vyper entry's stated third dispatch shape (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19,21`). This is byte-level evidence; the checker's small dispatch simulation does not run the contract on an EVM, and the saved probe envelope records `runtime_execution: not-performed`.
