# CR-6 — arc3-loop1-round10 per-item reconciliation

**Chain:** verdicts/convergence (`claims-frozen.md:67-72`). This report records separate evidence statuses; it assigns no scalar round verdict. Source-derived controls and candidate tests below were independently rerun. No source, corpus, map, gate, custody tool, or Git history was changed.

## Revision and baseline controls

- `git rev-parse HEAD` → `5694506a862c32d2f7aac44935778bce4b6184f2`; `eb5a2c4` → `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`.
- Re-ran SCORECARD Command A (`SCORECARD.md:88-124`) against both immutable revisions. Each returned `knowledge_files=88`, `mapped=88`, `missing=[]`, `dangling=[]`, `rule_blocks=15`, `citation_resolved_rules=15`, `coverage_score=10.0`, `depth_score=10.0`.
- The current working-tree corpus/map diff is clean. `git diff --quiet HEAD -- .ufo/gates/c1-census-v10.py SKILL.md PROVINCE.md SCORECARD.md corpus/README.md corpus/knowledge` succeeded. Therefore neither the 88→89 C1 landing nor a 16-rule C2 after-state is present here.

## C1 — coverage

**VERIFIED — EX-3's bounded compile/probe result.** I ran `bash .ufo/waves/arc3-loop1-round10/claims/c1/EX-3/evidence/rederive.sh`. It double-compiled the copied K8 source for each setting with Vyper `0.4.3+commit.bff19ea2` (executable SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`); all three determinism checks passed. The result was:

- Paris: 423 runtime bytes, SHA-256 `d1af44a952ac9775dd45eae83e2f4d167d311f9f7f3db8bf762592eb979060d2`; 5 `PUSH1 0x00`, 0 `PUSH0`.
- Cancun and Prague: byte-identical 418-byte runtimes, SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`; each has 5 `PUSH0`, 0 `PUSH1 0x00`.
- Across all three: 8 ABI functions, 8 compiler method IDs, and 8 REA functions; selector sets reconcile 8/8 with no missing or extra selectors. Each has 8 `PUSH4` sites / selector legs, one `MOD`, and one `CODECOPY`. Paris differs from Cancun/Prague; Cancun equals Prague. REA reports `evmole-interface@evmole@0.9.3` and `runtime_execution=not-performed`.

This supports selecting EX-3 as the evidence candidate for the frozen hardfork-variant Unknown (`claims-frozen.md:18-25`), bounded to this source, compiler, optimizer, and Paris/Cancun/Prague settings. It is static compile/probe evidence, not executed EVM behavior or a claim about other sources, versions, settings, or targets.

**UNVERIFIABLE — corpus admission / coverage after-state.** EX-3 remains a draft and no corpus entry or map token landed. Command A is still 88/88 at both measured revisions; the required 89/89 state must be checked after integration. Other overlapping C1 drafts are not treated as selected or verified by this reconciliation.

## C2 — depth

**VERIFIED — current baseline and proposed citation bounds.** The source-derived Command A results above give 15 rules and 15 citation-resolved rules. For the SC-2 rule draft (`claims/c2/SC-2.md:7-10`), I checked its proposed corpus ranges against HEAD: R4 lines 51-57 (63 lines total), and R8 lines 5-6 and 17 (17 lines total); all are in bounds.

**REPRODUCED — parser projection only.** In memory, I appended the exact SC-2 bullet to the current Queue-drain craft text and applied Command A's rule split and citation-range resolver. Output: baseline `15` blocks / `15` resolved; projection `16` / `16`; `projection_only=true`. No `SKILL.md` was written. SC-2 is the candidate draft selected for this check, not an integrated rule.

**VERIFIED — truth dependencies; locator wording needs care.** R8's frozen contract requires the pointer and receipt to land with C1's `ptr_check` extension (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:37-50`). The immutable `53fcf0caca7255f730fe1a1f17aefd00203a2978` tree includes the gate, receipt, PROVINCE, README, and R8 knowledge entry. R4's C2 verdict explicitly makes its Vyper clause conditional on C1's corpus entry (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`), and `40de38343398eee72aeebad7429f3bb99ab0a8dd` includes both PROVINCE and the R4 knowledge entry. The precise R4 item label is inconsistent across records: the C2 verdict/frozen shorthand calls this F5b, while PL-2's plan distinguishes the separately named C1-dependent Vyper-naming variant as F5c (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187,255-259`; `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/candidate-coupled-vyper.patch.md:217-224`). The dependency is verified as “Vyper statement ↔ C1 entry”; this report does not collapse the F5b/F5c labels into one hunk.

**UNVERIFIABLE — integrated rule #16.** No source rule was changed. The projected 16/16 result is not a post-landing measurement; rerun Command A at the integration revision.

## C3 — operability

**REPRODUCED — G21 append-past-register residual.** The current gate has 14 fixed Frontier rows (`.ufo/gates/c1-census-v10.py:292-308`), with the final registered span at `PROVINCE.md:161-162`; `frontier_check()` checks registered spans at gate lines 422-444. On a scratch copy, the unmodified gate passed both the 162-line baseline and a synthetic bullet appended at line 163, with `frontier_errors=[]`.

**REPRODUCED — candidate closure on scratch only.** I applied the exact RV-1 patch artifact (`claims/c3/RV-1/evidence/g21-frontier-coverage.patch`) to a scratch copy and ran clean/seeded cases. Results: source baseline PASS / exit 0; source seeded PASS / exit 0; candidate baseline PASS / exit 0; candidate seeded FAIL / exit 1 with `FRONTIER-UNEVALUABLE` and `PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)`. I separately applied the exact PL-4 diff (`claims/c3/PL-4.md`) to scratch; its clean case passed and the same seeded line 163 failed with the same error and class. These are patch-text tests only; the live gate is unchanged.

## Per-item disposition

- **C1:** EX-3's three-fork static measurement **VERIFIED**; corpus/map landing and 88→89 after-state **UNVERIFIABLE**.
- **C2:** SC-2 draft citation bounds **VERIFIED** and 15→16 parser projection **REPRODUCED in memory**; rule integration **UNVERIFIABLE**. R4 dependency verified with an F5b/F5c label discrepancy recorded above; R8 dependency and paired landing verified.
- **C3:** append-at-line-163 blind spot **REPRODUCED**; RV-1 and PL-4 candidate closures **REPRODUCED on scratch only**; live gate unchanged.

All scratch inputs and patched copies were under `/var/tmp`. At final source-path check, tracked claim-source paths were clean. Pre-existing unrelated status remains: `M .ufo/waves/arc2-loop1-round10/C3.md` and the untracked `arc3-loop1-round10` wave tree; neither was reverted or otherwise altered by this verdict.