# EX-2 — arc3-loop1-round5 C1 correctness sweep

Assignment: `claims-frozen.md:17-33` assigns EX-2 to C1. I re-ran the requested checks; prior-round numbers below are used only as comparison targets, not as evidence for my measurements.

## (a) Command A — REPRODUCED, with commit-attribution note

I used the recipe at `SCORECARD.md:92-123`, setting `REV` to every named hash (`fbbbd45`, `28aa7a9`, `5be4a26`, `c418be0`, `40de383`, `520341d`) and landed `HEAD` (`71668ccd2c920b907672b5c40efaafe7c2e75bd1`). Exact JSON stdout:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668ccd2c920b907672b5c40efaafe7c2e75bd1", "rule_blocks": 14}
```

The actual work-commit measurements reproduce the records: r1 `fbbbd45` (82/82, 13/13; `SCORECARD.md:1389-1392`), r2 `28aa7a9` (82/82, 14/14; `:1474-1476`), r3 `c418be0` (83/83, 14/14; `:1550-1554`), and r4 `40de383` (84/84, 14/14; `:1611-1612`). All seven fresh runs have empty `missing`/`dangling` and both scores 10.0.

Commit-topology caveat: `git show -s` identifies `5be4a26` as a hygiene commit whose parent is `c418be0`, not an r2 commit; it removes a pyc and adds `.gitignore`. `520341d` is the r4 custody change (parent `015e1ba`), and `40de383` is its child. I ran Command A at both supplemental hashes as well, so none of the supplied refs was skipped. `5be4a26` and `520341d` both measure 83/83 before the Vyper corpus entry; the child `40de383` measures 84/84.

## (b) Custody-pair selftest — REPRODUCED; invocation spelling differs

The supplied command `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2 with:

```text
usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...
custody-pair.py: error: the following arguments are required: cmd
```

The script's accepted invocation, `python3 .ufo/gates/custody-pair/custody-pair.py selftest`, returned the exact final line `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` (all 28 case lines were PASS).

## (c–d) Landed-tree probes and census — REPRODUCED

Commands and exact verdict lines:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .
CITATION_DRIFT_VERDICT: reported findings=0 exit=0

$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict
CITATION_DRIFT_VERDICT: clean findings=0 exit=0

$ python3 .ufo/gates/c1-census-v10.py --root .
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1631 loci=9
SKILL.md       lines=390  loci=2
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

## (e) PROVINCE line hold and literal check — DISCREPANCY (8/9 absent)

`wc -l PROVINCE.md` returned `162 PROVINCE.md`. I ran `grep -F` against `PROVINCE.md` for the nine old literals identified by the r4 repair record (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:241-250` and `.../EX-12/proposed-core-asar-row-repair.patch.md:45-63`). Exact results:

```text
real solc/vyper-compiled bytecode untested => ABSENT (grep exit 1)
all 3 organic cores exceed the cap => ABSENT (grep exit 1)
JEB (unprobed) => 88:  JEB (unprobed). Engine installs are operator-owned.
Reserve: 91MB => ABSENT (grep exit 1)
Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` => ABSENT (grep exit 1)
absent: `7z` => ABSENT (grep exit 1)
probe-refused => ABSENT (grep exit 1)
35 features => ABSENT (grep exit 1)
423-file asar => ABSENT (grep exit 1)
```

Thus the literal-absence expectation does not reproduce: 8 are absent, but `JEB (unprobed)` remains at `PROVINCE.md:88`. This is also an internal record inconsistency: `SCORECARD.md:1603` says all nine stale literals were cleared, while `:1605-1606` explicitly adjudicates this literal `NO-CHANGE-with-cause` because the verb was probed but no JEB install exists. I made no tracked-file change; the fresh grep and retained adjudication are both recorded for the parent to reconcile.

## (f) Vyper entry spot-check — REPRODUCED

Fresh offline CLI runs (disk-backed scratch, no target execution) against `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex`:

```text
TMPDIR=/var/tmp/arc3-loop1-round5-ex2-rea npx --offline -y rea-agents@6.4.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json
TMPDIR=/var/tmp/arc3-loop1-round5-ex2-rea npx --offline -y rea-agents@6.7.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json
```

I independently derived Ethereum Keccak selectors from the 15 ABI function signatures in `EX-04/out/abi.json:1` (standalone implementation; canonical empty-input and `transfer(address,uint256)` vectors both PASS), then compared them to both fresh REA results:

```text
6.4.0 ev_d1792f577ae3611615fd8dbcb1ce2e71dae4e0346b66d72b41321f4644df963f: functions=15 dispatch_abi=True K/K=15/15 missing=[] extra=[]
6.7.0 ev_62e1b9e6e4d254f3a0a7f874bc068847b2fcc00f47b85151f540ab879bfbae47: functions=15 dispatch_abi=True K/K=15/15 missing=[] extra=[]
runtime.bin: 1562 bytes sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
runtime.hex decoded: 1562 bytes, same sha256; decoded binary equals runtime.bin
```

Direct byte checks of that runtime gave `dispatcher prologue matches=True hex=5f3560e01c6002600d820660011b61060001601e395f5156`; this includes `MOD` by 13, the shift, and the `0x600` table offset. The 13 two-byte entries occupy the final 26 bytes and all point to JUMPDESTs. Following their chains yielded 15 unique `PUSH4; DUP2; XOR; PUSH2; JUMPI` compare legs, all with the expected shape; the table-chain selector set equals the fresh REA selector set (no missing or extra). This reproduces the modulo-indexed jump-table/XOR dispatcher claim in `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:3,12,19-22`. Full CLI JSON is retained in `/var/tmp/arc3-loop1-round5-ex2-rea/probe.json` and `probe-6.7.0.json`.
