# SC-2 — C1 correctness sweep

**Verdict:** six scoped checks completed. Command A, the landed census, citation-drift probe, and Vyper evidence reproduce. Two discrepancies are recorded below: the frozen custody-pair invocation is not accepted by the CLI, and one of the nine whole-file stale-literal searches still finds a current `JEB (unprobed)` status.

I followed `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-37`. Measurements below were freshly run against Git objects and the landed tree; I did not use another seat's reported number as measurement evidence. Command A's recipe is `SCORECARD.md:88-124`.

## 1. Command A — REPRODUCED

I re-ran the recipe's `git show` / `git ls-tree` logic at all named work revisions, including each side of the grouped revisions, and at HEAD. Exact JSON output:

```json
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668cc", "rule_blocks": 14}
```

All mapped counts equal knowledge-file counts, with empty missing/dangling lists. The work-commit rule counts reproduce: r1 `13/13`; r2 `14/14`; r3 `14/14`; r4 `14/14`. The `5be4a26` and `520341d` intermediate states also have `14/14`.

## 2. Landed-tree instrument checks

- **Census v10 — REPRODUCED.** `python3 .ufo/gates/c1-census-v10.py --root .` emitted `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; exit 0.
- **Citation drift — REPRODUCED in both modes.**
  - `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` emitted `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`; exit 0.
  - `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict` emitted `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`; exit 0.
- **Custody-pair selftest — test passes, frozen invocation is a DISCREPANCY.** The frozen command `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` emitted:

  ```text
  usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...
  custody-pair.py: error: the following arguments are required: cmd
  custody_selftest_exit=2
  ```

  The parser defines a `selftest` subcommand (`.ufo/gates/custody-pair/custody-pair.py:1309-1335`). With the accepted invocation, `python3 .ufo/gates/custody-pair/custody-pair.py selftest`, the result was `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`; process exit 0. Its scratch path was under `/dev/shm`.

## 3. PROVINCE line hold and nine stale-literal checks

`wc -l PROVINCE.md` returned `162 PROVINCE.md`: the line-count hold reproduces. I searched the full current `PROVINCE.md` for each exact needle listed at `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:77-87`:

| Literal needle | Whole-file result |
|---|---|
| `Reserve: 91MB Godot ARM64 template` | absent |
| `all 3 organic cores` | absent |
| `JEB (unprobed)` | **match at `PROVINCE.md:88`** |
| `real solc/vyper-compiled bytecode untested` | absent |
| `Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`` | absent |
| `probe-refused since r2` | absent |
| `pacman pairs beyond expac unexercised` | absent |
| `absent: `7z`` | absent |
| `35 features incl. PyGhidra/BSim` | absent |

**DISCREPANCY:** only 8/9 literal needles are absent from the whole file. The remaining text is in the current alternate-provider status: `JEB (unprobed). Engine installs are operator-owned.` (`PROVINCE.md:88`). This occurrence is contextually a present operator-gated status, not the old Frontier stale clause, so the broad substring needle cannot serve as a whole-file “stale literal absent” assertion. Correct the assertion's scope/needle; do not remove the current status on the basis of this substring hit.

## 4. Vyper entry spot checks — REPRODUCED

The entry describes its scope as RESULT-class/no Core promotion (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:1,30`), claims 15/15 selector recovery and runtime identity at lines 12, 19, and identifies the modulo-indexed dispatcher at line 21. I independently parsed the three primary probe JSON envelopes, compared their selector sets to the pre-probe `planted-K.json`, and hashed the committed `EX-04/out/runtime.bin`.

```text
runtime bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
prologue[0:24]=5f3560e01c6002600d820660011b61060001601e395f5156
table offset=0x600 entries=13 hex=029c05e7050b040005ac043f053d05e705900574038205e70018
table targets are JUMPDEST: True
{"decoded_bytes": 1562, "decoded_sha256": "57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0", "dispatch_abi_all": true, "evidence": "evidence/probe/probe-6.4.0-hex.json", "extra": [], "functions": 15, "matched": true, "missing": [], "planted": 15, "selectors_unique": 15, "sha_matches_runtime": true}
{"decoded_bytes": 1562, "decoded_sha256": "57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0", "dispatch_abi_all": true, "evidence": "evidence/probe/probe-6.4.0-raw.json", "extra": [], "functions": 15, "matched": true, "missing": [], "planted": 15, "selectors_unique": 15, "sha_matches_runtime": true}
{"decoded_bytes": 1562, "decoded_sha256": "57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0", "dispatch_abi_all": true, "evidence": "evidence/probe/probe-6.7.0-hex.json", "extra": [], "functions": 15, "matched": true, "missing": [], "planted": 15, "selectors_unique": 15, "sha_matches_runtime": true}
```

The three raw selector sets each contain 15 unique selectors and equal the 15 values in `EX-04/evidence/planted-K.json:23-40`; all dispatch labels are `abi`, and each normalized bytecode sha256 equals the digest computed from the runtime binary. The runtime's first 24 bytes contain `MOD (0x06)` after `PUSH1 13` and the selector shift; its 13 two-byte table entries are at `0x600`, and every table target byte is `JUMPDEST (0x5b)`. This confirms the entry's modulo-indexed jump-table shape from bytes, not just its prose. These are checks of the committed evidence and binary; I did not make a new REA provider probe.

## Per-item disposition

| C1 item | Verdict |
|---|---|
| Command A mapped/rule counts at named revisions | **REPRODUCED** |
| Custody-pair 28-case test | **REPRODUCED** using `selftest`; frozen `--selftest` spelling is a **DISCREPANCY** (exit 2) |
| Citation-drift default + strict modes | **REPRODUCED** |
| Census v10 landed-tree PASS | **REPRODUCED** |
| PROVINCE line count | **REPRODUCED** (162) |
| Nine whole-file stale-literal absences | **DISCREPANCY** (8 absent; `JEB (unprobed)` remains at line 88 as current status) |
| Vyper evidence spot checks | **REPRODUCED** (15/15 K/K on three legs, runtime sha256, modulo table shape) |

No corpus, gate, or tracked file was changed; this report is the only deliverable for SC-2.