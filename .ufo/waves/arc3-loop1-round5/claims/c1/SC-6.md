# SC-6 — c1 correctness sweep

Scope: c1 per `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-33`. I ran Command A from `SCORECARD.md:88-124` against each named commit tree, executed the live gates, rechecked the nine PROVINCE search needles, and re-derived the Vyper evidence. No tracked file was changed; all commands read the target tree, with REA scratch/output under `/var/tmp/r5-sc6-rea`.

## Findings

### Command A — REPRODUCED on the round work states

Exact JSON output from rerunning the SCORECARD recipe (sorted keys):

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
```

The four arc3 work-state measurements reproduce the SCORECARD values: r1 `82/82, 13/13` (`SCORECARD.md:1389-1391`), r2 `82/82, 14/14` (`:1474-1476`), r3 `83/83, 14/14` (`:1550-1554`), and r4 `84/84, 14/14` (`:1611-1612`). All six values above were derived from Git objects, not copied from those claims. Supplemental commit-tree results are also recorded: `5be4a26` and `520341d` are `83/83, 14/14`; these are not alternative r2/r4 work-state results. `git show -s --format='%h parents=%p %s'` reports `5be4a26` parent `c418be0` (hygiene commit) and `40de383` parent `520341d` (r4 work commit), so the counts reflect their distinct trees.

### Custody-pair selftest — DISCREPANCY (gate spelling; corrected run passes)

The frozen command spelling `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` does not invoke a test: exact stderr was `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` then `custody-pair.py: error: the following arguments are required: cmd` (exit 2). Correcting to the CLI's positional subcommand, `python3 .ufo/gates/custody-pair/custody-pair.py selftest`, produced:

```text
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

Thus the 28-case result is REPRODUCED; the specified invocation is not.

### Citation-drift — REPRODUCED

Commands: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` and the same command with `--strict`.

```text
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

### Census and PROVINCE hold — census REPRODUCED; stale-literal count DISCREPANCY

`python3 .ufo/gates/c1-census-v10.py --root .` ended `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)` and independently printed `PROVINCE.md    lines=162  loci=6`. `wc -l PROVINCE.md` also returned `162 PROVINCE.md`.

I re-ran `grep -FnF` for all nine literal needles against the current `PROVINCE.md`. Result: **8 absent, 1 present**, not 9 absent:

```text
ABSENT  Reserve: 91MB Godot ARM64 template
ABSENT  all 3 organic cores
88:  JEB (unprobed). Engine installs are operator-owned.
PRESENT JEB (unprobed)
ABSENT  real solc/vyper-compiled bytecode untested
ABSENT  Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`
ABSENT  probe-refused since r2
ABSENT  pacman pairs beyond expac unexercised
ABSENT  absent: `7z`
ABSENT  35 features incl. PyGhidra/BSim
```

Corrected measurement: 8/9 needles absent; `JEB (unprobed)` remains at `PROVINCE.md:88`. `SCORECARD.md:1606` says this item was adjudicated NO-CHANGE because no JEB install exists, so the literal's semantic scope may be intentional; nevertheless, the frozen claim of nine literal absences does not reproduce. No PROVINCE edit was made (outside seat write scope).

### Vyper entry spot-check — REPRODUCED

Ran real REA CLI inspections on the local `CarrierV` runtime, using disk-backed `TMPDIR` as required by the entry (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:7,19-21`):

```text
TMPDIR=/var/tmp/r5-sc6-rea npx -y rea-agents@6.4.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json
inspect-6.4.json: functions=15 unique=15 matched=15 missing=[] extra=[] dispatch_abi=15/15 bytecode_bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 evidence_id=ev_d1792f577ae3611615fd8dbcb1ce2e71dae4e0346b66d72b41321f4644df963f
TMPDIR=/var/tmp/r5-sc6-rea npx -y rea-agents@6.7.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json
inspect-6.7.json: functions=15 unique=15 matched=15 missing=[] extra=[] dispatch_abi=15/15 bytecode_bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 evidence_id=ev_62e1b9e6e4d254f3a0a7f874bc068847b2fcc00f47b85151f540ab879bfbae47
```

For both fresh results, I independently compared the 15 selectors against `EX-04/evidence/planted-K.json:23-39`; set equality holds with no missing or extra selectors. I also parsed the saved 6.4-hex, 6.4-raw, and 6.7-hex result envelopes (`EX-04/evidence/probe/probe-{6.4.0-hex,6.4.0-raw,6.7.0-hex}.json:1`): each has 15 unique functions, 15/15 planted, all `dispatch:"abi"`, and the same decoded runtime digest.

Independently decoding `EX-04/out/runtime.hex:1` yielded `bytes=1562`, `SHA-256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`, matching both live REA results and saved envelopes. Byte-level dispatcher check: prefix `5f3560e01c6002600d820660011b61060001601e395f5156` is present (CALLDATALOAD/SHR then modulo-13 table lookup at `0x600`); the 26-byte table decodes to 13 targets `[0x29c, 0x5e7, 0x50b, 0x400, 0x5ac, 0x43f, 0x53d, 0x5e7, 0x590, 0x574, 0x382, 0x5e7, 0x18]`, all pointing to byte `0x5b` JUMPDESTs, with sentinel `0x5e7` occurring three times. Pattern census found 15/15 planted selectors each once in `PUSH4 selector; DUP2; XOR; PUSH2 target; JUMPI` form. This confirms the third modulo-indexed/XOR dispatcher shape claimed at the Vyper entry's `:21`; this is static evidence, not runtime execution.
