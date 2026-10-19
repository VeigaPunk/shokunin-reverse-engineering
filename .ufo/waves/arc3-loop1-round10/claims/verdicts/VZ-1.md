# VZ-1 — arc3-loop1-round10 reconciliation verdict

Independent convergence seat. I read `claims-frozen.md` before evaluating the claims and re-derived the measurements below. This file is the only repository artifact written by VZ-1. Compiler/probe and gate-patch experiments used scratch under `/var/tmp`; Git was not mutated.

## Verdicts

### C1 — coverage / Vyper hardfork Unknown

**REPRODUCED — bounded compile/probe result. UNVERIFIABLE — coverage closure and 88→89 after-state.**

I independently recompiled the frozen K8 fixture (`62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`) with the existing Vyper `0.4.3+commit.bff19ea2` executable (`615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`) and reprobed with REA 6.7.0 / `evmole-interface` / `evmole@0.9.3`. Paris compiled to 423 bytes (`d1af44a952ac9775dd45eae83e2f4d167d311f9f7f3db8bf762592eb979060d2`); Cancun and Prague were byte-identical at 418 bytes (`72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`). Each target had 8 ABI functions, 8 compiler method IDs, and 8 raw/normalized REA rows with exact selector-set agreement. The peer reproduction packet records deterministic double-compiles and the same target deltas (`.ufo/waves/arc3-loop1-round10/claims/c1/EX-3/evidence/reproduction.txt:1-13`). This is static selector/compiler evidence, not runtime execution or deployment evidence.

EX-3 is the strongest canonical draft: it compares the same K8 source across Paris/Cancun/Prague; EX-5 and CR-4 add London/Prague, and EX-7 overlaps Paris. Keep EX-8's different source digest (`324691744d49965ade54e513a18d7df61a15803a242897ecd57cc3542f8bf284`) scoped as a separate fixture; do not merge its byte digests into the K8 result. The open target limitation is explicit in the existing r8 entry (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:15`).

Command A, re-derived over immutable Git objects at HEAD `5694506a862c32d2f7aac44935778bce4b6184f2` and work revision `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`, returns 88 knowledge files, 88 mapped, empty missing/dangling sets, and 15/15 resolved rules at both revisions (`SCORECARD.md:88-124`; corroborating HEAD output: `.ufo/waves/arc3-loop1-round10/claims/c1/EX-3/evidence/command-a-before.json:1`). No draft or map token is landed. Therefore the frozen 88→89 coverage result remains **UNVERIFIABLE** until integration lands both and Command A is rerun at that commit.

### C2 — depth / Queue-drain rule #16

**REPRODUCED — baseline and in-memory projection. UNVERIFIABLE — landed rule.**

The current immutable HEAD baseline is 15 rule blocks and 15 citation-resolved rules (Command A output above). I appended the proposed dependency-coupled rule in memory and ran Command A's exact split/citation-range logic against HEAD's immutable corpus: baseline 15/15; projected 16 blocks / 16 resolved; both cited ranges are in bounds (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57`, 63 lines; `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:9-17`, 17 lines). This projection writes no source file.

The coupled-landing rule is the best fit to the frozen candidate and the peer convergence: r4's entry records a scope statement contradicted by its own landing commit (`r4 entry:51-57`), while the r8 entry explicitly leaves entry/map landing and the after-count pending (`r8 entry:9-17`). Read-only `git diff-tree` checks confirm r4 commit `40de383` includes both the PROVINCE change and Vyper entry, and r8 commit `53fcf0c` includes the gate extension, receipt, PROVINCE/map changes, and entry. One label needs care: the R4 record identifies the actual C1-dependent variant as **F5c**, not the frozen shorthand's F5b (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187,255-259`). The rule should state the dependency discipline without relying on the mislabel.

No `SKILL.md` edit was made. Thus 16/16 is a projection, not a landed result; accept rule #16 only after integration and a fresh Command A run against the resulting revision (`.ufo/waves/arc3-loop1-round10/claims/c2/EX-12.md:28-44`).

### C3 — operability / G21 append-past-register guard

**REPRODUCED — existing gap and dash/star candidate behavior. RESIDUAL — plus-marker bypass.**

The live census gate (`a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`) currently passes on the 162-line `PROVINCE.md` with 14 G21 rows. Its register grades only declared spans (`.ufo/gates/c1-census-v10.py:292-308,422-444`); the declared last span ends at line 162. On a scratch copy, appending a dash bullet as line 163 to the unmodified gate still returned `PASS`, 14 rows, no frontier errors, exit 0.

I applied the RV-1 patch text only to scratch (`.ufo/waves/arc3-loop1-round10/claims/c3/RV-1/evidence/g21-frontier-coverage.patch`) and tested a clean baseline plus three line-163 marker variants. Clean: PASS/0. `-` and `*`: each failed with `FRONTIER-UNEVALUABLE`, exit 1. `+`: silently PASS/0. The plus case is a real residual: the candidate reuses the current `BULLET` expression at gate line 318, `^\s*[-*] `, which does not recognize Markdown's `+` bullet marker. PL-4/RV-6 patch text also uses that expression. The scratch result proves the exact seeded dash case, not complete coverage of Markdown bullets.

Recommendation: retain the named-section/heading checks, but extend the local bullet matcher to `[-*+]` (and fail closed for missing or duplicate target headings); then rerun clean plus `-`, `*`, and `+` line-163 cases. Until that is done, the patch is useful but does not fully close the frozen “new Frontier bullet” scope. No live gate change was made, as required by the seat boundary. Separately, the custody-pair selftest passed 28/28 (`CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`); that is a clean tool selftest, not evidence that the G21 patch closes its residual.

## Integration disposition

- **C1:** use one tightly scoped K8 corpus draft plus map token; rerun Command A for the actual 89/89 after-state.
- **C2:** add the dependency-coupled rule with the verified corpus citations; rerun Command A for the actual 16/16 after-state.
- **C3:** revise the scratch-tested candidate for `+` bullets and prove the clean / three-marker matrix before accepting the patch text as complete.

No corpus, map, SKILL, PROVINCE, SCORECARD, LOG, gate, custody source, or peer artifact was changed by VZ-1.
