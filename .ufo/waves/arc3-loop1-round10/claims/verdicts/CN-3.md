# CN-3 — arc3-loop1-round10 convergence verdict

**Chain:** verdicts/convergence (`claims-frozen.md:67-72`). This report separates each claim’s evidence verdict from whether the required change has landed. It assigns no scalar round verdict. No source, corpus, gate, custody tool, or Git history was changed.

## Revision and control measurements

The measured records revision is `5694506a862c32d2f7aac44935778bce4b6184f2`; its work parent is `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`. I ran SCORECARD Command A from `SCORECARD.md:88-124` against both immutable Git trees. Exact output:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "eb5a2c4af9d910bb7a3d4fced780f4641e341a24", "rule_blocks": 15}
```

A fresh `python3 .ufo/gates/c1-census-v10.py` run at HEAD reported `PROVINCE.md lines=162`, `SCORECARD.md lines=1924`, `SKILL.md lines=413`, `FRONTIER register (G21): 14 rows asserted, errors: []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS` (exit 0). `sha256sum .ufo/gates/c1-census-v10.py` returned `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`. The census gate worktree copy is identical to HEAD. These are pre-integration controls, not C1/C2 after-measurements.

## C1 — coverage / close one corpus Unknown

**REPRODUCED — bounded EX-3 K8 compile/probe. UNVERIFIABLE — corpus admission and the required 88→89 after-state.**

I re-ran `bash .ufo/waves/arc3-loop1-round10/claims/c1/EX-3/evidence/rederive.sh` using the retained Vyper executable and cached REA 6.7.0. Its recorded output (`claims/c1/EX-3/evidence/reproduction.txt:1-13`) shows source SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`, Vyper `0.4.3+commit.bff19ea2`, and compiler SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`. Paris, Cancun, and Prague double-compiles were deterministic. Each target yielded 8 ABI functions, 8 compiler IDs, 8 REA functions and exact 8/8 selector agreement. Paris is 423 bytes, SHA-256 `d1af44a952ac9775dd45eae83e2f4d167d311f9f7f3db8bf762592eb979060d2`; Cancun and Prague are byte-identical at 418 bytes, SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`. The static analysis reports no runtime execution (`EX-3.md:11-14`, `:22`). This is a bounded compiler-target result, not deployed-contract or runtime evidence.

This seat independently re-derived EX-3, also selected by VZ-1, CR-6, VZ-3, and CN-2 (`claims/verdicts/VZ-1.md:7-15`; `CR-6.md:11-21`; `VZ-3.md:15-27`; `CN-2.md:18-27`). EX-4 is a separate, independently measured candidate recommended by CN-1, CN-4, VZ-2, and VZ-4 (`CN-1.md:18-34`; `CN-4.md:18-26`; `VZ-2.md:24-40`; `VZ-4.md:19-34`). **The verdict peers do not agree on one C1 choice:** CR-8 independently recompiled EX-2’s alternate-solc 0.8.28 viaIR fixture and selects it (`claims/verdicts/CR-8.md:18-24`); CR-5 and CR-7 do not choose one. I did not independently rebuild EX-2, so I report its result only as CR-8’s peer measurement. EX-3, EX-4, and EX-2 are distinct bounded Unknowns, not additive closures. EX-5 and CR-4 overlap on London/Prague, EX-7 on Paris, and EX-6 proposes a broader K8 matrix; integrate one entry and token only. EX-8 is a different source fixture and must remain separately scoped.

I also ran EX-4’s retained, read-only `node .ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids.mjs`. All four envelope IDs matched the artifact’s canonical-projection recomputation; two same-byte copies had distinct reported IDs, display-field mutation left the base ID unchanged, and substituting the three path-bearing fields reproduced copyA’s ID. This reproduces that retained-envelope calculation, but I did not independently inspect the installed package implementation; it does not make EX-4 the selected C1 closure (`claims/c1/EX-4/evidence/recompute-ids.mjs:14-35,36-69`; `claims/c1/EX-4/evidence/identity.txt:1-13`).

The frozen C1 condition requires one corpus entry plus its EVM-map token and a fresh Command A after-run (`claims-frozen.md:16-29`). Neither is present in the measured tree: both Command A runs remain 88 files / 88 mapped with no missing or dangling tokens. **UNVERIFIABLE:** do not claim 89/89 until verdict peers resolve the single-candidate choice, one bounded draft and map token land together, and Command A is rerun at that landing revision.

**DISCREPANCY — the EX-8 locator warning does not reproduce.** CR-5 and CR-7 say EX-8 lines 27 and 29 duplicate the repository-rooted `.ufo/waves/.../claims/c1/EX-8/` locator (`claims/verdicts/CR-5.md:23`; `CR-7.md:34-41`). I checked the root-relative convention used by existing corpus entries (`corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md:1-3`) and the paths directly: the single-prefix `HardforkVault.vy` and `rederive.sh` paths exist; the doubled-prefix path does not. VZ-3 reaches the same correction at `claims/verdicts/VZ-3.md:27`. No locator correction is supported by this check.

## C2 — depth / Queue-drain rule #16

**REPRODUCED — baseline and parser projections. UNVERIFIABLE — landed rule #16.**

Command A establishes 15 rule blocks and 15 citation-resolved rules at both measured revisions. I projected the exact candidate bullets from EX-9, SC-2, and SC-3 in memory against HEAD’s Queue-drain section, applying the same `^- \*\*` split and corpus path/range resolver. Exact compact result:

```json
{"before":{"rule_blocks":15,"citation_resolved_rules":15},"projections":{"EX-9":{"projected_rule_blocks":16,"projected_citation_resolved_rules":16,"candidate_refs":[["2026-10-19-arc3-r4-evm-vyper-leg.md",28,30,63],["2026-10-19-arc3-r4-evm-vyper-leg.md",51,57,63],["2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md",9,17,17]]},"SC-2":{"projected_rule_blocks":16,"projected_citation_resolved_rules":16,"candidate_refs":[["2026-10-19-arc3-r4-evm-vyper-leg.md",51,57,63],["2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md",5,6,17],["2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md",17,17,17]]},"SC-3":{"projected_rule_blocks":16,"projected_citation_resolved_rules":16,"candidate_refs":[["2026-10-19-arc3-r4-evm-vyper-leg.md",51,56,63],["2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md",17,17,17]]}}
```

The R4 and R8 citation ranges shown are within the immutable corpus files. The proposal family converges on conditional, same-revision co-landing of artifacts whose presence makes a claim true. I recommend EX-9’s conditional “truth-dependent repair” formulation; SC-2/SC-3 are parser-compatible alternatives. EX-10’s identity proposal and EX-14’s dispatcher-prologue proposal are different topics, not the common dependency rule.

**R4 dependency-label nuance.** The frozen shorthand and R4 verdict use F5b; the R4 plan labels F5b “real solc/vyper-compiled bytecode untested” and F5c “selectors stay bare hashes” (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187`). The plan separately labels an optional C1-coupled Vyper-naming variant F5c (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:255-259`), while the historical verdict says the broader Vyper clause depends on the C1 entry (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`). Preserve both source labels and their differing scope: the broad F5b wording is reported as C1-dependent, and the narrower naming variant is explicitly F5c. The proposed rule should state the dependency generically as Vyper wording ↔ C1 corpus entry, not imply F5b never depended on C1 or F5c was the only coupling. R8 independently documents the receipt/pointer plus instrument-extension coupling (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:37-50`).

**UNVERIFIABLE:** no rule was added to `SKILL.md`; the measured source remains at 15/15. The projections are not a landed 16/16 result. Integration must add one selected rule with its citations, then rerun Command A at the landing revision.

## C3 — operability / G21 Frontier append guard

**REPRODUCED — append-past-register gap and RV-1 dash/plus behavior. REPRODUCED — matcher correction on scratch for all three markers. UNVERIFIABLE — complete or live gate change.**

The live gate declares 14 G21 spans, with the final span at `PROVINCE.md:161-162` (`.ufo/gates/c1-census-v10.py:292-308`). `frontier_check()` grades those fixed spans only (`:422-444`); the shared matcher is `BULLET = re.compile(r"^\s*[-*] ")` (`:318`). I applied the exact RV-1 patch artifact to copied input roots under `/var/tmp` and ran the copied gate. The clean case passed. An appended `-` bullet at line 163 failed with `FRONTIER-UNEVALUABLE`; the `+` case passed silently. The current unmodified gate also passed the seeded `+` case. This residual follows from the shared matcher. PL-3’s proposed guard also calls `BULLET.match()` (`claims/c3/PL-3.md:104-107`), and VZ-1 independently records the plus-marker residual (`claims/verdicts/VZ-1.md:27-35`).

I then changed only the matcher in a scratch copy to `re.match(r"^\s*[-*+]\s+", lines[i])`, ran `python3 -m py_compile`, and tested the clean input plus line-163 `-`, `*`, and `+` seeds. Exact results:

```text
clean:       exit=0; PASS
line 163 -:  exit=1; FAIL; FRONTIER-UNEVALUABLE
line 163 *:  exit=1; FAIL; FRONTIER-UNEVALUABLE
line 163 +:  exit=1; FAIL; FRONTIER-UNEVALUABLE
```

This proves the matcher-only scratch correction preserves the clean control and catches the three seeded Markdown markers; it is not an integrated or complete gate patch. Prefer an exact registered-start predicate over RV-1’s range-based coverage, which can treat any bullet inside a multi-line registered span as covered. The demonstrated cases do not cover non-bullet prose or inserted claims inside registered spans. No gate or custody source was edited.

**PARTIAL / UNVERIFIABLE — C3 overall.** The original RV-1 patch closes the seeded dash case but not plus; the corrected matcher passes the tested scratch matrix only. The frozen after-condition and any live change remain unverified.

## Roster and write boundary

At the latest roster sweep, C1 reports are present for 11/12 seats (EX-1 absent); C2 and C3 reports are 12/12 each. All 12 convergence verdicts are now present: CN-1 through CN-4, CR-5 through CR-8, and VZ-1 through VZ-4. C1 recommendations remain split among EX-3, EX-4, and EX-2; the peer evidence and this seat’s independent measurements are summarized above. This is a roster snapshot, not a claim that an absent report failed.

The only file written by CN-3 is this artifact. Git was read-only. The pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification was left untouched, and source paths (`.ufo/gates/c1-census-v10.py`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/README.md`, `corpus/knowledge/`) remained clean against HEAD.
