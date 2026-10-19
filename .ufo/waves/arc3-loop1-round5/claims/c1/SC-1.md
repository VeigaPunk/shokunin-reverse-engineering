# SC-1 — arc3-loop1-round5 calibration sweep

Seat SC-1, chain c1. Read-only sweep at HEAD `71668ccd2c920b907672b5c40efaafe7c2e75bd1`; only this artifact was written. Command A is the recipe at `SCORECARD.md:88-124`; the frozen checks are `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-33`.

## Re-derivations

1. **Command A at the named work/hygiene commits — REPRODUCED.** I reran the SCORECARD recipe against each Git object (not the worktree). Exact JSON output:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
```

   All have empty `missing`/`dangling` and 10.0/10.0 scores. Git parent metadata (`git show -s --format='%H %P %s' ...`) places `5be4a26` after `c418be0` as its hygiene child, and `520341d` before `40de383` as its parent; thus the 83→84 r4 transition is at `40de383`. The per-object counts reproduce; this ancestry corrects the task's shorthand grouping of `5be4a26` with r2.

2. **Custody-pair selftest — REPRODUCED; invocation discrepancy noted.** The suggested `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2 (`usage: custody-pair.py ... {capture,verify,selftest,paths} ...`; required positional `cmd`). The supported invocation `TMPDIR=/var/tmp python3 .ufo/gates/custody-pair/custody-pair.py selftest` returned exactly:

```text
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

   The parser defines a positional `selftest` subcommand at `.ufo/gates/custody-pair/custody-pair.py:1311-1333`; the test used only scratch under `/dev/shm`.

3. **Citation-drift probe, both modes — REPRODUCED.** On HEAD:

```text
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

   Commands were `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` and the same with `--strict`.

4. **Census v10 — REPRODUCED.** `python3 .ufo/gates/c1-census-v10.py --root .` returned:

```text
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

   Exit 0; the live anchors were Devin 6.5.0, OMP 6.5.0, Kimi 6.7.0.

5. **PROVINCE line hold and nine stale-literal searches — DISCREPANCY.** `wc -l PROVINCE.md` returned `162 PROVINCE.md` (line count reproduced). I ran `grep -F` for each of the nine strings in the frozen stale-literal set. The exact per-string results were:

```text
ABSENT   Reserve: 91MB Godot ARM64 template
ABSENT   all 3 organic cores
PRESENT  JEB (unprobed)
88:  JEB (unprobed). Engine installs are operator-owned.
ABSENT   real solc/vyper-compiled bytecode untested
ABSENT   Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`
ABSENT   probe-refused since r2
ABSENT   pacman pairs beyond expac unexercised
ABSENT   absent: `7z`
ABSENT   35 features incl. PyGhidra/BSim
```

   Corrected result: **8/9 absent; `JEB (unprobed)` remains at `PROVINCE.md:88`**. This conflicts with `SCORECARD.md:1603` (“all nine stale literals cleared”); the same section at `:1606` calls the JEB wording a NO-CHANGE because the verb was probed but no JEB install exists. Suggested correction, outside my write scope: replace the line-88 wording with `JEB (installation absent; inspect-jeb-client probed as capability_unavailable)` or correct the nine-absent assertion to explicitly disposition this surviving literal. No tracked file was changed.

6. **Vyper entry's own evidence — REPRODUCED.** I independently parsed `EX-04/out/runtime.bin`, `runtime.hex`, `evidence/planted-K.json`, and the saved `evidence/probe/probe-6.4.0-hex.json` (no new REA invocation or contract execution). My verification output:

```text
runtime.bin bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
runtime.hex decodes byte-identically=True
probe functions=15 dispatch_abi=15/15
probe selector set planted=15/15 missing=[] extra=[]
probe decoded bytecode bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 matches runtime.bin=True
dispatch prologue=5f3560e01c6002600d820660011b61060001601e395f5156 exact_expected=True
jump table offset=0x600 buckets=13 bytes=26 all_targets_JUMPDEST=True empty_sentinel_0x5e7=3
XOR comparison legs=15 unique selectors=15 equal_planted=True
```

   This verifies the entry's CarrierV 15/15 claim (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19,21`): planted K=15 and selector values are in `EX-04/evidence/planted-K.json:23-39`; the selected probe envelope has 15 `dispatch:"abi"` functions and the matching decoded digest; the runtime digest/size also match `EX-04/out/compile-receipt.txt:13-19`. The bytes support the modulo-13 jump-table and XOR-chain shape. Evidence establishes static bytecode shape and the recorded probe result, not runtime behavior.

## Overall

Five of the six scoped checks reproduce as recorded, including all Command A values, both citation-drift modes, census PASS, custody selftest result, and Vyper evidence. The Province line count reproduces, but its stale-literal claim is discrepant: one of nine searched strings is still present. The custody script's advertised-by-task `--selftest` spelling is also invalid; its supported subcommand passes 28/28.
