# VZ-2 — arc3-loop1-round5 convergence verdict

HEAD at the checks: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. I re-derived the C1/C3 measurements below from Git objects, the live tree, or direct file enumeration. Peer reports are used for reconciliation only; peer-only C2 corrections are identified as such. This seat wrote only this artifact.

## Summary

| Frozen claim | Ruling |
|---|---|
| C1 calibration | **DISCREPANCY**: most measurements reproduce, but the custody invocation and 9-needle absence assertion are false as written; revision grouping is also wrong. Required `claims/c1/sweep-report.md` was absent at inspection. |
| C2 coverage | **UNVERIFIABLE-with-cause**: C2 seat audits now exist, but the required consolidated `claims/c2/audit.md` was absent; peer reports flag correction candidates not yet consolidated/adjudicated. |
| C3 freshness | **Partial dispositions recorded**: STOPPED-with-reason / DISCHARGED-BY-PRECEDENT with caveats / CARRIED-forward. Required `claims/c3/disposition.md` was absent. |

The frozen claim files require `sweep-report.md`, `audit.md`, and `disposition.md` (`claims-frozen.md:29-53,75-79`). A final lookup for these three names under `claims/` returned `No matches found`; individual seat reports do not substitute for the named claim artifacts.

## C1 — calibration

### Command A — REPRODUCED, with revision-label correction

I reran the `SCORECARD.md:88-124` recipe against the named Git objects and HEAD. All rows had `missing=[]`, `dangling=[]`, and coverage/depth scores `10.0/10.0`:

```text
revision   knowledge_files/mapped   citation_resolved_rules/rule_blocks
fbbbd45    82/82                    13/13
28aa7a9    82/82                    14/14
5be4a26    83/83                    14/14
c418be0    83/83                    14/14
520341d    83/83                    14/14
40de383    84/84                    14/14
71668cc    84/84                    14/14
```

**DISCREPANCY (grouping only):** `git show -s --format='%H %P %s' 5be4a26` identifies `c418be0` as its parent and a hygiene-only subject; `git diff --stat c418be0 5be4a26` is `.gitignore` plus generated-pyc removal. `520341d` is the custody-pair follow-on parent of `40de383`. Thus the measurements reproduce by hash, but the supplied grouping of `5be4a26` as r2 and the unqualified grouping of `520341d` as r4 work are misleading. `28aa7a9` is the r2 work state; `c418be0` and `40de383` are the r3/r4 work states.

### Landed gates — REPRODUCED, with one invocation discrepancy

- `python3 .ufo/gates/c1-census-v10.py --root .` → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; the output reports `PROVINCE.md lines=162`, `SCORECARD.md lines=1631`, `SKILL.md lines=390`.
- `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `reported findings=0 exit=0`; with `--strict` → `clean findings=0 exit=0`.
- Frozen `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` → argparse error, exit 2 (`the following arguments are required: cmd`). The supported `python3 .ufo/gates/custody-pair/custody-pair.py selftest` → `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. The 28-case test reproduces; the frozen CLI spelling is a **DISCREPANCY**.

### PROVINCE and Vyper — one literal discrepancy; bounded static check

`wc -l PROVINCE.md` → `162 PROVINCE.md`, reproducing the line hold. I rechecked the nine literal needles in `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:2-10` against the full current `PROVINCE.md`: eight are absent; `JEB (unprobed)` remains at `PROVINCE.md:88` (“JEB (unprobed). Engine installs are operator-owned.”). The correct whole-file result is **8/9 absent**, not 9/9 (`SCORECARD.md:1603-1606` also records JEB as NO-CHANGE). This is a literal-reporting discrepancy, not a reason to remove the current operator-gated status.

The bounded Vyper spot-check **VERIFIED** the retained-byte claims: `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin` is 1,562 bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; the saved probe JSONs at `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/{probe-6.4.0-hex,probe-6.4.0-raw,probe-6.7.0-hex}.json` each recover the same 15-selector set with no missing/extra selectors and the same decoded digest. The local byte parser identifies a 13-entry, two-byte table at `0x600` and 15/15 agreement with the saved leg chains (`.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/dispatch-census.py`; entry claims at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19-22`). This is static evidence/parser-model checking, not a fresh REA provider call or execution of a deployed contract.

## C2 — coverage audit remains incomplete

At the final directory check, `claims/c2/` contained `EX-12.md` and `RV-6.md`; neither `claims/c2/audit.md` nor a one-row-per-load-bearing-claim consolidated audit existed. The frozen audit scope at `claims-frozen.md:38-53` requires the four-entry claim audit; individual evidence-envelope checks cannot substitute for it.

The two new C2 reports materially advance the work: EX-12 reports selector/hash/dispatch checks and flags r3/r4 initcode wording for append-only correction (`claims/c2/EX-12.md:27-35`); RV-6 reports byte-size/unit, CBOR-vs-opcode, and corpus-scope/PROVINCE conflicts for parent adjudication (`claims/c2/RV-6.md:21-29`). I have not independently re-audited those correction candidates, so they remain **peer-reported**, not verified findings of this verdict. They must be resolved or explicitly dispositioned in the required audit. CN-2 and VZ-4's earlier statements that no C2 Markdown report existed were valid snapshots, but are stale now that EX-12 and RV-6 have appeared; the missing consolidated `audit.md` remains current.

**C2 ruling: UNVERIFIABLE-with-cause** — substantive partial reports exist, but the required consolidated audit and its complete coverage/disposition do not.

## C3 — arc2 carried-debt disposition

1. **Mid-leg faithful retest — STOPPED-with-reason.** My fresh bounded `free -b` sample returned `free=1007775744` bytes and `available=21584584704` bytes. `available` is barely above 20 GiB, while the literal `free` column is far below it; the wording “free RAM” is ambiguous. More decisively, no affirmative operator host-cost authorization was present (`claims-frozen.md:60-66`). No retest was launched.

2. **r10 five-seat deficit — DISCHARGED-BY-PRECEDENT, with discrepancies.** My direct enumeration command expanded the frozen ranges in `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:3` and compared them to current top-level Markdown reports:

```text
roster_count=64 report_count=59 matched=59 missing_count=5 extras=[]
missing=CR1,E1,E17,E28,R7
```

The count is reproduced; exact identities are not stable: the frozen receipt contains malformed/ambiguous `SC1-S2`, while `.ufo/waves/arc2-loop1-round10/receipts/roster-reconciliation.txt:1` says P1 is missing although `.ufo/waves/arc2-loop1-round10/P1.md` is present. The recorded operator interruption/no-backfill precedent is at `SCORECARD.md:1277-1281,1330-1332`, and the frozen R5 disposition permits discharge by precedent (`claims-frozen.md:67-70`). However, `corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51` does not state an interruption exception and instead requires re-dispatch for a true unresolved shortfall. I therefore accept the recorded discharge as the selected frozen disposition, not as proof of 64/64 delivery; its cited rationale and exact missing-seat list remain **DISCREPANCIES**. Re-open the choice if the missing C2/corpus adjudication establishes that r10 findings are needed.

3. **Full hyper-vs-Devin census — CARRIED-forward (partial).** The table still has `<fill>` cells at `.ufo/waves/arc2-loop1-round10/E19.md:212-217`. My bounded searches returned `No matches found` for `.ufo/waves/arc2-loop1-round{1,2,3,4}/**/dispatch*` and `.ufo/waves/arc2-loop1-round{1,2,3,4}/**/*.jsonl`. These observations do not recover the historical dispatch arrays or establish a full-wave denominator; report-file counts cannot replace them. No workload was launched.

## Peer reconciliation

- **C1:** SC-2, SC-3, and TB-4 converge with my Command-A results, the corrected positional custody subcommand, and the 8/9 JEB literal result. VZ-4 and CN-2 independently document the same discrepancies and bounded Vyper corroboration. Their static-byte findings do not imply runtime/deployment behavior.
- **C2:** EX-12 and RV-6 are substantive audit reports with correction candidates, not an empty chain. They do not yet satisfy the frozen `audit.md` deliverable. Earlier CN-2/VZ-4 C2-absence claims are superseded only as to the existence of seat reports, not as to the missing consolidated audit.
- **C3:** PL-2, PL-3, PL-4, and EX-14 converge on stopping the retest without operator clearance, retaining a partial census, and recording discharge by interruption precedent. Their direct roster checks preserve the five-report count but identify inconsistencies in the exact roster slots. CN-2 leaves discharge conditional on the absent sweep result; I treat the frozen discharge option as recorded while keeping that condition and the lesson-attribution conflict explicit.

**Overall:** no all-claim completion verdict is justified yet. C1 has verified measurements plus specific discrepancies; C2 remains UNVERIFIABLE-with-cause pending its consolidated audit; C3 has recorded item-level dispositions but its required aggregate disposition file is absent and two details remain unresolved. No tracked source, corpus, custody path, or other seat artifact was modified.
