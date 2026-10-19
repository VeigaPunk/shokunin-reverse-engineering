# VZ-4 — arc3-loop1-round5 convergence verdict

HEAD at direct checks: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. This is the verdict-chain artifact. Values below are my own measurements; peer reports are used only for convergence comparison. I wrote no other file.

## Summary

| Claim | Ruling |
|---|---|
| C1 calibration | **DISCREPANCY**: command-A counts, landed census/probes, custody test result, and Vyper evidence reproduce; frozen `--selftest` syntax is invalid and only 8/9 claimed PROVINCE literal absences hold. The round/hash grouping also needs correction. |
| C2 coverage | **UNVERIFIABLE-with-cause**: no C2 audit Markdown was present on the last check; raw EX-7 JSONs do not constitute the required per-entry audit. |
| C3 freshness | **DISCHARGED / STOPPED / CARRIED-forward** per item below, with a current-vs-recorded roster identity discrepancy and a counting-lesson rationale discrepancy. |

## C1 — calibration

### Command A — REPRODUCED per object

I replayed `SCORECARD.md:88-124` against all six hashes named in the frozen contract and current HEAD. Exact JSON output:

```json
{"citation_resolved_rules":13,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":82,"mapped":82,"missing":[],"revision":"fbbbd45","rule_blocks":13}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":82,"mapped":82,"missing":[],"revision":"28aa7a9","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":83,"mapped":83,"missing":[],"revision":"5be4a26","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":83,"mapped":83,"missing":[],"revision":"c418be0","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":84,"mapped":84,"missing":[],"revision":"40de383","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":83,"mapped":83,"missing":[],"revision":"520341d","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":84,"mapped":84,"missing":[],"revision":"71668cc","rule_blocks":14}
```

Every measured hash has `missing=[]`, `dangling=[]`, and coverage/depth `10.0`. **Revision-label discrepancy, not a count discrepancy:** `git show -s --format='%H%n%P%n%s' 5be4a26` gives parent `c418be0` and subject `hygiene: drop committed pyc + root-ignore __pycache__`; `git diff --stat c418be0 5be4a26` shows only `.gitignore` and generated pyc deletion. Thus `5be4a26` is a hygiene child of r3, not an r2 work commit as grouped in the supplied key facts. `520341d` is parent of r4 work commit `40de383`; both are r4 snapshots, with independently measured 83/83 then 84/84. Round record pointers for the work measurements are `SCORECARD.md:1389-1393,1474-1476,1550-1554,1611-1613`.

### Landed-tree gates — REPRODUCED, with a command-syntax correction

- `python3 .ufo/gates/c1-census-v10.py --root .` → `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; output also reports `PROVINCE.md lines=162`, `SCORECARD.md lines=1631`, `SKILL.md lines=390`.
- `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.
- Same command with `--strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
- The requested `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` is a **DISCREPANCY**: argparse exits 2 with `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` / `error: the following arguments are required: cmd`. The supported positional form `python3 .ufo/gates/custody-pair/custody-pair.py selftest` → `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. The test result reproduces; only the frozen spelling is wrong.

### PROVINCE hold and stale-literal scan — DISCREPANCY

`wc -l PROVINCE.md` → `162 PROVINCE.md`, so the line hold reproduces. I searched the nine exact literals in `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:2-10` with escaped literal patterns through the dedicated Grep tool. Eight had no match; the one match was:

```text
PROVINCE.md:88:  JEB (unprobed). Engine installs are operator-owned.
```

Correct whole-file result is **8/9 absent**, not 9/9. The r4 record says “all nine stale literals cleared” at `SCORECARD.md:1603-1605`, then explicitly rules JEB NO-CHANGE at `:1605-1606`; the broad `JEB (unprobed)` needle therefore cannot be counted absent. This is a literal-sweep/reporting discrepancy, not a basis for deleting the current operator-gated status.

### Vyper evidence spot-check — VERIFIED from retained artifact bytes

The r4 entry claims the runtime identity, 15/15 selector set, and modulo-indexed dispatch at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19,21-22`; it scopes the entry as RESULT-only/no Core promotion at `:30`. I hashed the evidence runtime and ran its local byte-level parser against the planted set and saved probe:

```text
$ sha256sum .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin
57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0  .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin
runtime bytes: 1562
assumed jump table at 0x600 (13 buckets x 2 B) -> tail 26 B
execution reached the leg-derived body: 15/15
agreement: 15/15
probe recovered 15 selectors; leg chains carry 15
probe set == leg-chain set: True
probe extras: []
leg-chain only: []
```

The same output says every reported offset agrees with its byte-derived body entry (`JUMPDEST@probe=False`). This is a static check of the retained binary/evidence, not a fresh REA provider call or runtime/chain observation. `PROVINCE.md:73,91-93` keeps Vyper in Frontier, consistent with no Core promotion.

**C1 verdict:** scope checks reproduce except the frozen custody command spelling and the all-nine whole-file absence assertion. Command-A values reproduce; `5be4a26` attribution is misgrouped in the supplied round list.

## C2 — coverage audit not yet adjudicable

Last `Glob .ufo/waves/arc3-loop1-round5/claims/c2/**/*.md` returned **No matches found**. There are raw per-carrier EX-7 JSON files, but no `.ufo/waves/arc3-loop1-round5/claims/c2/audit.md` or other C2 Markdown verdict. I did not treat a partial evidence set or my C1 Vyper spot-check as a substitute for the frozen per-entry audit across selector counts, hashes, dispatch claims, byte counts, and no-Core disclaimers. **UNVERIFIABLE-with-cause: required C2 audit artifact absent at inspection.**

The current corpus inventory has three `2026-10-19-arc3-r*.md` files (r1, r3, r4); the ghidra erratum is a separate older-named knowledge entry and must be included in the audit scope as the frozen claim says. No C2 correction is proposed from this incomplete review.

## C3 — arc2 carried-debt disposition and peer reconciliation

1. **Mid-leg faithful retest — STOPPED-with-reason.** My bounded `free -b` sample showed `free=1044598784` bytes and `available=22141669376` bytes. The `available` interpretation clears 20 GiB; the literal free bucket does not. In either case I have no affirmative operator host-cost authorization in the available instructions/records, so the conjunction in `claims-frozen.md:60-66` is not met. I did not launch the >18.3G/uncapped retest. C3 peers PL-3, PL-4, EX-13, EX-14, and EX-15 make the same stop ruling; their samples likewise do not establish operator approval.
2. **r10 five-seat deficit — DISCHARGED-BY-PRECEDENT, with a reconciliation discrepancy.** I expanded `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:2-4` and enumerated current top-level reports directly:

   ```text
   expanded_roster=64; reports=59; absent=5
   absent_names=CR1,E1,E17,E28,R7
   unrostered_reports=
   ```

   The stored `.ufo/waves/arc2-loop1-round10/receipts/roster-reconciliation.txt:1` instead names P1, CR1, E1, E17, and one unnamed seat; P1.md is present now. The count still differs by five, but the seat identities do not reconcile. The frozen roster also abbreviates `SC1-S2`, a range-format ambiguity noted by EX-14. `SCORECARD.md:1330-1332` records the no-backfill precedent, but `corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51` says to re-dispatch for a true unresolved roster shortfall and contains no operator-interruption exception. Therefore the disposition is recorded as discharged per the frozen option, while the stated “per the counting lesson” rationale and exact missing-seat list remain **DISCREPANCIES** for the parent; I did not re-dispatch.
3. **Full hyper-vs-Devin C3 census — CARRIED-forward (partial).** The required table is visibly still incomplete at `.ufo/waves/arc2-loop1-round10/E19.md:212-217` (`<fill>` cells). My read-only searches for arc2 rounds 1–4 dispatch/roster captures (`dispatch*`, `*.jsonl`) returned no matches in the checked-in wave tree. This establishes only the absence of those retained local files; it does not exclude external session logs. Without the arrays/cutoff evidence, report-file totals cannot establish full-wave delivery or convergence. C3 peers PL-3, EX-13, EX-14, and EX-15 also carry the table forward for missing primary records.

## Peer convergence

- C1 reports TB-4, RV-1, SC-7, SC-2, TB-1, SC-1, SC-5, RV-2, and TB-3 agree with my direct counts/gates, Vyper spot-check, custody syntax finding, and JEB literal discrepancy. TB-4’s revision-label caution is independently supported by the parent/subject output above. I found no competing C1 measurement that changes these rulings.
- C3 reports PL-3, PL-4, EX-13, EX-14, and EX-15 converge on no retest without operator clearance and a partial census carried forward. They reproduce the 64-versus-59 cardinality; EX-14 explicitly limits confidence in exact IDs, while the live report set and stored reconciliation do conflict. EX-15 also identifies the counting-lesson attribution conflict noted above.
- CN-2’s `claims/verdicts/CN-2.md:5,34-38` recorded no peer reports at its earlier inspection. That was a valid point-in-time snapshot but is superseded by the C1/C3 artifacts now present. C2 remains the missing convergence input.

**Overall:** C1 has two invocation/content-scope discrepancies plus a commit-attribution correction; C3 has recorded dispositions with the stated roster/rationale caveats; C2 remains UNVERIFIABLE pending its per-entry audit. No all-chain convergence verdict is justified yet.