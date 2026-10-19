# TB-2 — C1 correctness sweep

Chain assignment: c1 (TB seat prefix). Scope: `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-33`. At the start of the sweep, `git rev-parse HEAD` returned `71668ccd2c920b907672b5c40efaafe7c2e75bd1`.

## Findings

### (a) Command A at supplied revisions — REPRODUCED

Ran the SCORECARD recipe verbatim (`SCORECARD.md:88-124`) against every supplied revision, plus HEAD. Exact JSON output:

```json
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668cc", "rule_blocks": 14}
```

All rows have `missing=[]`, `dangling=[]`; counts and scores re-derived from the objects, not prior seat outputs. The `40de383` work commit is 84/84 and HEAD remains 84/84. `5be4a26` was included because supplied; `git show --stat` identifies it as the pyc/.gitignore hygiene commit.

### (b) Custody-pair 28-case selftest — DISCREPANCY (invocation only); test REPRODUCED

The frozen command spelling `./.ufo/gates/custody-pair/custody-pair.py --selftest` is rejected by the current CLI:

```text
usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...
custody-pair.py: error: the following arguments are required: cmd
Command failed with exit code: 2
```

The parser defines `selftest` as a subcommand (`.ufo/gates/custody-pair/custody-pair.py:1308-1333`). Running the source-defined form `python3 .ufo/gates/custody-pair/custody-pair.py selftest` returned exactly:

```text
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

It used `/dev/shm` scratch; no custody path was written.

### (c) Citation-drift probe, both modes — REPRODUCED

Commands: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` and the same with `--strict`.

```text
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

### (d) Census v10 at landed tree — REPRODUCED

Command: `python3 .ufo/gates/c1-census-v10.py --root .`. Relevant exact output:

```text
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1631 loci=9
SKILL.md       lines=390  loci=2
SCOPE-ERRORS (marker assertions): []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

### (e) PROVINCE line hold and nine literal searches — DISCREPANCY (literal absence)

`wc -l PROVINCE.md` returned `162 PROVINCE.md` (line hold reproduced). I derived these nine exact needles from `git show 520341d:PROVINCE.md`, then searched the landed `PROVINCE.md` with literal-pattern Grep queries and independently counted occurrences in both prior and current text:

| Literal needle | At `520341d` | Landed `PROVINCE.md` |
|---|---:|---:|
| `Reserve: 91MB Godot ARM64 template` | 1 | 0 |
| `all 3 organic cores` | 1 | 0 |
| `JEB (unprobed)` | 1 | **1 — `PROVINCE.md:88`** |
| `real solc/vyper-compiled bytecode untested` | 1 | 0 |
| `Next: raise \`REA_GHIDRA_STARTUP_TIMEOUT_MS\`` | 1 | 0 |
| `probe-refused since r2` | 1 | 0 |
| `pacman pairs beyond expac unexercised` | 1 | 0 |
| `absent: \`7z\`` | 1 | 0 |
| `35 features incl. PyGhidra/BSim` | 1 | 0 |

Corrected whole-file result: **8/9 absent**, not 9/9. The hit is the current alternate-provider status `JEB (unprobed). Engine installs are operator-owned.` at `PROVINCE.md:87-88`. The records also say `JEB (unprobed)` was adjudicated **NO-CHANGE-with-cause** (`SCORECARD.md:1605-1606`), while the immediately preceding line claims “all nine stale literals cleared” (`SCORECARD.md:1603-1604`). This is a report/scope inconsistency; I did not edit `PROVINCE.md` or any protected file.

### (f) Vyper entry spot-check against its evidence — REPRODUCED

The entry claims are at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19,21-22`; source evidence is the CarrierV runtime/compiler outputs under `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/`, including `out/runtime.bin`, `out/abi.json`, `out/method-identifiers.json`, `evidence/planted-K.json:23-39`, and `evidence/probe/probe-6.4.0-hex.json:1`.

I recomputed runtime SHA-256 and compared the selector sets from the probe envelope, pre-probe planted-K file, and compiler method identifiers (excluding the non-function `__default__()` key). I also scanned the runtime bytes for the prologue, jump-table entries, and `PUSH4/DUP2/XOR/PUSH2/JUMPI` compare sites. Exact output:

```text
runtime_size=1562 runtime_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 probe_decoded_size=1562 probe_decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 hash_match=True
probe_functions=15 all_dispatch_abi=True ABI_function_entries=15 planted_K=15
probe_planted_compiler_sets_equal=True unique=15 missing_vs_planted=[] extra_vs_planted=[] missing_vs_compiler=[] extra_vs_compiler=[]
prologue=5f3560e01c6002600d820660011b61060001601e395f5156 jump_table_offset=0x600 buckets=13 table_end=0x61a runtime_end=0x61a target_all_jumpdest=True sentinel_0x5e7_buckets=[1, 7, 11] compare_sites=15 compare_selectors_equal_probe=True
```

Thus 15/15 set equality, 15 `dispatch:"abi"` results, the decoded runtime digest, and the modulo-13 jump-table/XOR-compare shape reproduce. This is a static check of the sealed envelope and underlying compiler/runtime artifacts; I did not run a new REA operation or execute the contract.
