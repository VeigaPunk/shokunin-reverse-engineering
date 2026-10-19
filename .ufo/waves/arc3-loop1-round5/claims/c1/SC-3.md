# SC-3 — C1 calibration sweep (arc3-loop1-round5)

Seat SC-3 is assigned to `c1` by `.ufo/waves/arc3-loop1-round5/claims-frozen.md:81-86`. I re-derived the checks below from Git objects, the landed tree, and the cited artifact bytes. HEAD resolved to `71668cc`.

## Findings

- **Command A measurements — REPRODUCED.** Re-ran the recipe at `SCORECARD.md:88-124` against each named revision and HEAD. Exact JSON output:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "HEAD", "rule_blocks": 14}
```

  Parentage check (`git show -s --format='%h parent=%p %s'`): `28aa7a9` is R2 work; `c418be0` is R3 work; `5be4a26` has parent `c418be0` and subject `hygiene: drop committed pyc...`; `520341d` has parent `015e1ba` and is the R4 custody follow-on; `40de383` has parent `520341d` and is R4 work. **DISCREPANCY in the supplied revision grouping:** `5be4a26` is not an R2 commit. Its 83/83 result is the post-R3 corpus, consistent with its parent and hygiene-only change. The R2 work result is 82/82 at `28aa7a9`.

- **Custody-pair selftest — REPRODUCED.** The checked-in CLI has a `selftest` subcommand and `--scratch`; ran `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp/kaidoku-round5-SC3-custody` (avoids `/tmp`). Output: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. All 28 named cases printed `PASS`.

- **Citation-drift probe — REPRODUCED in both modes.**
  - `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.
  - Same command with `--strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.

- **Census v10 — REPRODUCED.** `python3 .ufo/gates/c1-census-v10.py --root .` exited 0. Output ended `SCOPE-ERRORS (marker assertions): []`, `UNREADABLE (could-not-evaluate): []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`. Re-derived floors: `PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3`; live anchors `devin=6.5.0, omp=6.5.0, kimi=6.7.0`.

- **PROVINCE line-count hold — REPRODUCED.** `wc -l PROVINCE.md`, `git show c418be0:PROVINCE.md | wc -l`, and `git show 40de383:PROVINCE.md | wc -l` each returned `162`. This agrees with the work-commit record at `SCORECARD.md:1602-1604`.

- **Nine stale-literal absences — DISCREPANCY.** I checked the nine literal needles enumerated at `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:1-10` against the current file using escaped literal-pattern searches. Eight were absent; one matched:

```text
kaidoku-shokunin/PROVINCE.md:88:  JEB (unprobed). Engine installs are operator-owned.
```

  That phrase is explicitly adjudicated NO-CHANGE at `SCORECARD.md:1606`, so its presence is intentional; it is not a stale literal to remove. Corrected disposition: **8/9 listed needles absent; retain JEB as NO-CHANGE and exclude it from the stale-literal absence set.** The fixed needle list also omits the old `~/.kimi-code/config.toml:3298` and `423-file asar` text even though both are changed in `git diff c418be0 40de383 -- PROVINCE.md` (hunks at `PROVINCE.md:18` and `:49`); both exact old strings are absent now. Do not edit PROVINCE from this seat.

- **Vyper entry spot-check — REPRODUCED.** Independently ran the cached REA CLI against `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex` (no installation; `TMPDIR` under `/var/tmp`):
  - REA 6.4.0: exit 0, Evidence `ev_d1792f577ae3611615fd8dbcb1ce2e71dae4e0346b66d72b41321f4644df963f`, decoded bytecode `1562` bytes / SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`, `15` functions, all `dispatch: "abi"`.
  - REA 6.7.0: exit 0, Evidence `ev_62e1b9e6e4d254f3a0a7f874bc068847b2fcc00f47b85151f540ab879bfbae47`, same decoded size/hash, `15` functions, all `dispatch: "abi"`.
  - Both fresh runs returned the same selector set as `EX-05/planted-full.json` (`K=15`, `all_agree=true`, no duplicates): `0776076f, 0c751377, 1aa02d59, 27e235e3, 2e1a7d4d, 3f4ba83a, 4643c56b, 48a3ef5c, 5c975abb, 6e8efde2, 8456cb59, 8da5cb5b, b144adfb, d0e30db0, e0749a6a`.
  - Direct file hashing: `out/runtime.bin` = `1562` bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; `out/runtime.hex` = `3124` bytes, SHA-256 `e0b1021c68f8de8c3f049f4242769548b6f8271a00986f2ab20f049f8748a192`.
  - Dispatch bytes re-derived from `runtime.bin`: prologue `5f3560e01c6002600d820660011b61060001601e395f5156`; `MOD` path indexes a 13-entry table at `0x600`, and all 13 decoded destinations point to byte `0x5b` (`JUMPDEST`). A separate opcode walk found 15 unique XOR compare sites matching `63 <selector:4> 81 18 61 <next:2> 57`; the raw scan's one additional unique `PUSH4` is `08c379a0` (`Error(string)`), consistent with `EX-08/evidence-vyper-dispatcher.txt:33-35`, not a planted function selector. The entry’s byte-level shape claim is supported at `EX-08/evidence-vyper-dispatcher.txt:1-7,21-24` and `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:19-23`.
  - REA observation is static/inferred; it does not execute the bytecode or establish deployed-contract behavior.

## Overall

C1's command-A numbers, three gates, line-count hold, and Vyper spot-check reproduce. The literal-absence subclaim needs reconciliation (one of its claimed-absent strings is a documented NO-CHANGE), and the provided R2/R3 commit grouping needs correction as shown above. No tracked source or custody path was written; this seat's sole repository write is this artifact.
