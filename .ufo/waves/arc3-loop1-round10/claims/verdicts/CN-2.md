# CN-2 — arc3-loop1-round10 per-item convergence verdict

This is an evidence reconciliation for frozen claims C1–C3 (`claims-frozen.md:16-65`), not an aggregate pass or an integration. I changed only this verdict artifact; all compile, probe, projection, and gate-patch experiments were scratch-only under `/var/tmp`. No Git mutation was performed.

## Revision and baseline controls

HEAD is `5694506a862c32d2f7aac44935778bce4b6184f2`; the named work revision is `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`. I independently ran SCORECARD Command A (`SCORECARD.md:88-124`) against each immutable tree:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "HEAD", "rule_blocks": 15}
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "eb5a2c4af9d910bb7a3d4fced780f4641e341a24", "rule_blocks": 15}
```

These are before-state controls only. A scoped `git status --short` check for the gate, corpus/map, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, and `LOG.md` returned no paths; none has a measured after-state in this worktree.

## C1 — coverage / one named Unknown

**REPRODUCED — EX-3's bounded K8 compile/probe. UNVERIFIABLE — canonical corpus/map landing and 88→89 after-state. Candidate selection is not converged.**

I independently ran `npm_config_offline=true bash .ufo/waves/arc3-loop1-round10/claims/c1/EX-3/evidence/rederive.sh` (exit 0). The copied source SHA-256 is `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; the Vyper executable is `0.4.3+commit.bff19ea2`, SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`. Paris, Cancun, and Prague double-compiles were deterministic. Each target had 8 ABI functions, 8 compiler method IDs, and 8 REA rows with selector sets matching 8/8; REA used `evmole-interface` / `evmole@0.9.3` and did not execute runtime behavior.

- Paris: 423 runtime bytes, SHA-256 `d1af44a952ac9775dd45eae83e2f4d167d311f9f7f3db8bf762592eb979060d2`.
- Cancun and Prague: byte-identical 418-byte runtimes, SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`.

This supports EX-3 as one tightly bounded Vyper-target candidate, not as a landed corpus result or a general Vyper claim. The entry and map token are absent; Command A still measures 88/88. The frozen 89/89 after-condition is **UNVERIFIABLE** until one entry and its token land together and Command A is rerun at that commit.

C1 inventory: 11/12 top-level reports are present (`CR-1..CR-4`, `EX-2..EX-8`); `EX-1.md` is absent (its nested evidence directory is not a top-level seat report). All 12 verdict-seat artifacts have now arrived. Their C1 recommendations remain split: VZ-1, VZ-3, CR-6, and CN-3 favor EX-3; VZ-2, VZ-4, CN-1, and CN-4 favor EX-4; CR-8 selects EX-2; CR-5 and CR-7 leave the choice open. CN-2 independently substantiates EX-3 only; EX-4's reported measurements remain peer evidence here. The two fresh candidate families EX-3 and EX-4 therefore have no converged selection.

CR-8's EX-2 result repeats the R9 EX-5 measurement for the same ViaIrVault source digest and solc 0.8.28 / viaIR / optimizer-runs-200 setting (`.ufo/waves/arc3-loop1-round9/claims/c2/EX-5.md:7-9`; R10 EX-2 carries the same runtime digest at `claims/c1/EX-2/evidence/rederive-output.txt:1`). The frozen claim itself notes 0.8.28 as already characterized at R9 (`claims-frozen.md:18-20`). R9 EX-5 was a draft, and no corresponding canonical knowledge file or map token exists at HEAD; thus EX-2 may be a carry-forward of existing evidence for integration, but its R10 rerun is not a new empirical slice. The integrator should resolve whether to carry that evidence forward or choose one of the fresh EX-3 / EX-4 candidates; do not combine them.

CR-5/CR-7's warning that EX-8 repeats its repository-root prefix is **NOT REPRODUCED** by the current file: direct inspection of `claims/c1/EX-8.md:27-29` shows one root-relative prefix in each locator, and the referenced source exists.

## C2 — depth / Queue-drain rule #16

**REPRODUCED — baseline and SC-2 in-memory projection. UNVERIFIABLE — integrated rule.**

The Command A results above establish 15/15 at both revisions. I appended SC-2's exact proposed bullet in memory to HEAD's Queue-drain craft section and applied Command A's rule split and corpus citation-range resolver: baseline `15` blocks / `15` resolved; projection `16` / `16`. The new references resolve at r4 `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57` (63 lines) and r8 `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-6,17` (17 lines). `SKILL.md` was not edited, so 16/16 is a projection, not a landing.

All 12 C2 reports are present. CR-7 counts ten drafts converging on dependency-coupled landing; EX-10 proposes pointer/content semantics and EX-14 proposes completing selector-route analysis. Recommend one generic coupled-landing rule, not a composition of competing rules. The r4 label is inconsistent across records: the frozen shorthand and round-4 verdict refer to F5b, while PL-2's plan identifies the C1-dependent Vyper-naming variant as F5c (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187,255-259`; round-4 verdict `:332-335`). CR-7 also reports a broader F5b dependency. Avoid choosing a disputed hunk label; describe the demonstrated dependency neutrally as “r4 Vyper wording ↔ C1 corpus entry.” Accept rule #16 only after integration and a fresh Command A result of 16 blocks with resolving citations.

## C3 — operability / G21 append-past-register guard

**REPRODUCED — existing gap and RV-1's dash/star behavior. DISCREPANCY — RV-1 still misses `+`. REPRODUCED — a scan-local `+` matcher closes the tested three-marker gap on scratch. UNVERIFIABLE — live gate change.**

The gate declares 14 fixed Frontier spans (`.ufo/gates/c1-census-v10.py:292-308`); the last ends at `PROVINCE.md:161-162`, and the existing check grades those spans (`:422-444`). On scratch copies of the gate inputs, the unmodified gate returned PASS/exit 0 with 14 rows and no frontier errors for both the 162-line baseline and line-163 `-`, `*`, and `+` bullets.

I applied the exact current RV-1 patch artifact (`claims/c3/RV-1/evidence/g21-frontier-coverage.patch`) to a scratch gate:

- Clean: PASS / exit 0.
- Line-163 `-` and `*`: each FAIL / exit 1 with `FRONTIER-UNEVALUABLE` and `PROVINCE.md:163 unregistered Frontier bullet`.
- Line-163 `+`: silently PASS / exit 0 with no frontier errors. The patch reuses the gate's `BULLET` expression at `:318`, `^\s*[-*] `, which does not match `+`.

I then changed only the candidate scan expression in scratch to `re.match(r"^\s*[-*+] ", lines[i])`, leaving the shared `BULLET` matcher unchanged (it is also used elsewhere at `:349`). The clean candidate remained PASS/0, and each of the three line-163 marker seeds failed with `FRONTIER-UNEVALUABLE` / exit 1. This establishes the tested local matcher behavior, not a live patch or general closure of non-bullet or in-span content changes. Other PL/RV patch variants should not be composed; retain one scanner, its heading checks, and add the marker case locally before acceptance.

VZ-1, VZ-2, VZ-3, VZ-4, CR-7, CR-8, CN-1, CN-3, CN-4, and my independent matrix agree on the `+` residual; the dash-only checks reported by CR-5/CR-6 are insufficient to close the full unordered-bullet case. No gate, `PROVINCE.md`, custody tool, or peer artifact was changed.

## Integration disposition

- **C1:** baseline and EX-3 measurement reproduced; EX-3 and EX-4 remain the distinct fresh candidates without a converged choice. EX-2 repeats the 0.8.28/ViaIrVault result characterized in R9; if carried forward, treat it as prior evidence, not a new R10 measurement. Land only one entry plus map token and prove 89/89.
- **C2:** SC-2's generic coupled-landing draft projects to 16/16; land exactly one reviewed rule and rerun Command A. Keep the r4 example label-neutral.
- **C3:** append-past-:162 gap reproduced; current RV-1 patch is partial because `+` passes. A scan-local matcher for `-`, `*`, and `+` passes the clean scratch control and rejects all three seeded markers; landing remains unverified.

All 12 verdict-seat artifacts are now present (`CR-5..CR-8`, `VZ-1..VZ-4`, `CN-1..CN-4`). C1/C2/C3 seat-report inventories are 11/12, 12/12, and 12/12 respectively; the missing C1 top-level report is EX-1.md. Only CN-2.md was written by this seat.
