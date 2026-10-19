# CR-7 — arc3-loop1-round10 verdict and convergence

Measured source trees: HEAD `5694506a862c32d2f7aac44935778bce4b6184f2`; work revision `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`. This is a verdict artifact only. No corpus, map, skill, gate, custody, PROVINCE, SCORECARD, LOG, or Git source was changed.

## Summary verdicts

- **C1 — REPRODUCED baseline; UNVERIFIABLE closure.** Command A remains 88/88 mapped with no missing/dangling entries at both measured revisions. At this audit snapshot, 11/12 C1 seat reports are drafts: overlapping Vyper EVM-target proposals, an alternate-solc viaIR proposal, and a Rust Evidence-ID proposal. No one entry/token is landed or selected by a consensus of verdict seats. I did not recompile/reprobe the peer C1 experiments, so their domain-result numbers are not independently verified here. The duplicated EX-8 draft paths are **CORRECTED** below.
- **C2 — REPRODUCED baseline and draft projection; UNVERIFIABLE landing.** All 12 C2 reports are present; 10 converge on a dependency-coupled rule, while EX-10 and EX-14 offer different craft topics. My in-memory projection of SC-2's rule gives 16 blocks / 16 citations resolved, but `SKILL.md` remains at 15. The broad R4 dependency is verified; its F5b/F5c labels need the nuance below.
- **C3 — REPRODUCED residual; DISCREPANCY in the current RV-1 patch's coverage.** The unmodified gate silently accepts a new dash bullet at line 163, and the current RV-1 patch rejects that dash case on scratch. A `+` list bullet at line 163 still silently passes under that patch. Extending the local matcher to Markdown's `-`, `*`, and `+` markers passes the clean control and fails all three seeded cases on scratch. No live gate fix is claimed.

## Command A — first-hand baseline

Recipe: `SCORECARD.md:88-124`. I reran the source-derived calculation against each immutable revision; exact JSON:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "eb5a2c4af9d910bb7a3d4fced780f4641e341a24", "rule_blocks": 15}
```

The scoped `git status` check for `corpus/knowledge`, `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `.ufo/gates/c1-census-v10.py`, and `.ufo/receipts` printed no paths; `git diff --quiet HEAD --` over those paths exited 0. These are before-state controls only, not an 89/89 or 16/16 landing result.

## C1 — coverage candidates and integration status

**REPRODUCED — canonical baseline only.** The two Command A outputs above independently establish 88 knowledge files, 88 mapped tokens, `missing=[]`, and `dangling=[]`. The frozen after-condition (one new knowledge file and map token, then 89/89) remains **UNVERIFIABLE** because neither canonical corpus file changed.

**UNVERIFIABLE — C1 candidate result and choice.** The current artifact inventory has 11 of 12 C1 top-level reports (EX-1 is not present at this snapshot):

- Vyper target drafts: CR-1, CR-2, CR-3, CR-4, EX-3, EX-5, EX-6, EX-7, and EX-8. Most overlap on K8; EX-8 identifies a different `HardforkVault.vy` fixture.
- EX-2 targets the R6 solc-version-under-viaIR Unknown (`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`).
- EX-4 targets the `inspect_rust_binary` Evidence-ID domain.

These are alternatives for the frozen one-Unknown C1 move, not eleven additive closures. The two available verdict peers do not yet yield a unanimous choice: VZ-1 prefers EX-3 (`claims/verdicts/VZ-1.md:13`); CR-5 says the drafts do not yet form one consolidated choice (`claims/verdicts/CR-5.md:21`). I did not independently rerun the compiler/REA experiments, so I do not present any candidate's reported measurements as CR-7 evidence. Choose one bounded entry plus its map token and rerun Command A at that landing revision.

**CORRECTED — EX-8 locator.** `claims/c1/EX-8.md:27,29` repeats `.ufo/waves/arc3-loop1-round10/claims/c1/EX-8/` inside an already repository-rooted path. I checked both forms directly:

```text
.ufo/waves/arc3-loop1-round10/claims/c1/EX-8/.ufo/waves/arc3-loop1-round10/claims/c1/EX-8/evidence/HardforkVault.vy: exists=False
.ufo/waves/arc3-loop1-round10/claims/c1/EX-8/evidence/HardforkVault.vy: exists=True
```

The same duplicated prefix appears in EX-8's recheck command. Correct the source/recheck locators before integrating that draft; I did not edit the peer artifact.

## C2 — coupled-landing rule #16

**REPRODUCED — baseline and SC-2 in-memory projection.** I extracted SC-2's exact proposed bullet, appended it only to the in-memory Queue-drain craft text from immutable HEAD, and applied Command A's rule split and corpus path/range resolver. Output:

```json
{"baseline_rule_blocks": 15, "new_rule_refs": [{"lines": 63, "path": "corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md", "range": [51, 57], "resolves": true}, {"lines": 17, "path": "corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md", "range": [5, 6], "resolves": true}, {"lines": 17, "path": "corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md", "range": [17, 17], "resolves": true}], "projected_citation_resolved_rules": 16, "projected_rule_blocks": 16, "revision": "5694506a862c32d2f7aac44935778bce4b6184f2"}
```

This is a parser/citation projection, not a changed `SKILL.md` result. All 12 C2 seat reports are available; the coupled-landing theme is common to 10, while EX-10 proposes pointer/content/position distinctions and EX-14 proposes walking the full selector-routing tree. Recommendation: integrate one coupled-landing bullet with its resolving corpus citations, not multiple competing rule-16 drafts. Actual `rule_blocks=16` remains **UNVERIFIABLE** until integration and a fresh Command A run.

**VERIFIED — the dependency examples; CORRECTED — the label is not exclusive.** Immutable commit-tree checks returned:

```text
# 40de38343398eee72aeebad7429f3bb99ab0a8dd
M PROVINCE.md
M corpus/README.md
A corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md
# 53fcf0caca7255f730fe1a1f17aefd00203a2978
M .ufo/gates/c1-census-v10.py
A .ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt
M PROVINCE.md
M corpus/README.md
A corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md
```

R4's C2 plan labels F5b as the real-solc/Vyper bytecode row (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:186`) and F5c as the bare-hash row (`:187`); its C1-dependent Vyper-naming variant is explicitly F5c (`:255-259`). The cross-chain verdict separately says the F5b wording depends on the C1 entry (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`). The immutable R4 commit's PROVINCE hunk changes line 92 from “real solc/vyper-compiled bytecode untested” to naming the measured solc and Vyper carriers, in the same commit that adds the R4 entry. Thus the frozen F5b coupling is supported, and there is also a separately documented F5c coupling variant; do not replace F5b with F5c as if only one label applied. R8's gate/receipt/PROVINCE/map/entry co-landing independently supports the general rule.

## C3 — G21 Frontier tail coverage

**REPRODUCED — live baseline and the named dash-bullet gap.** Gate SHA-256: `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`. `FRONTIER` has 14 fixed rows (`.ufo/gates/c1-census-v10.py:292-308`), its final row ends at `PROVINCE.md:161-162`, and `frontier_check()` iterates those spans only (`:422-444`). The source note already names the appended-bullet residual (`:114-116`). `python3 .ufo/gates/c1-census-v10.py --quiet` returned:

```text
PROVINCE.md    lines=162  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
gate_exit=0
```

On a scratch copy under `/var/tmp`, I appended a dash bullet as line 163 and ran the unmodified gate with `--root <scratch-root> --quiet`. It reported `PROVINCE.md lines=163`, `FRONTIER register (G21): 14 rows asserted, errors: []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0. Applying the current `claims/c3/RV-1/evidence/g21-frontier-coverage.patch` to a scratch gate preserves clean PASS and rejects that dash seed as `FRONTIER-UNEVALUABLE`, exit 1.

**DISCREPANCY — current RV-1 patch misses Markdown `+` bullets.** The source matcher is `BULLET = re.compile(r"^\s*[-*] ")` (`.ufo/gates/c1-census-v10.py:318`); RV-1's candidate reuses `BULLET.match`. My independent plus-marker runs returned:

```json
{"case": "source_plus", "declared_fail_classes": [], "exit": 0, "frontier_errors": [], "province_lines": 163, "verdict": "PASS"}
{"case": "rv1_plus", "declared_fail_classes": [], "exit": 0, "frontier_errors": [], "province_lines": 163, "verdict": "PASS"}
```

The candidate therefore closes the seeded dash case, but does not fully grade all ordinary Markdown unordered-list markers. A scratch-only adjustment from `BULLET.match(lines[i])` to `re.match(r"^\s*[-*+]\s+", lines[i])` preserved the clean fixture and failed each marker at line 163:

```json
{"case": "corrected_clean", "declared_fail_classes": [], "exit": 0, "frontier_errors": [], "lines": 162, "verdict": "PASS"}
{"case": "corrected_dash", "declared_fail_classes": ["FRONTIER-UNEVALUABLE"], "exit": 1, "frontier_errors": ["PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)"], "lines": 163, "verdict": "FAIL"}
{"case": "corrected_star", "declared_fail_classes": ["FRONTIER-UNEVALUABLE"], "exit": 1, "frontier_errors": ["PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)"], "lines": 163, "verdict": "FAIL"}
{"case": "corrected_plus", "declared_fail_classes": ["FRONTIER-UNEVALUABLE"], "exit": 1, "frontier_errors": ["PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)"], "lines": 163, "verdict": "FAIL"}
```

The modified matcher was applied only to the scratch copy; the gate in the repository remains unmodified. VZ-1 independently flags the same plus-marker boundary (`claims/verdicts/VZ-1.md:29-35`). Before accepting any C3 patch, retain its duplicate/missing-heading checks, include `+` in bullet recognition, rerun the clean and three-marker matrix, and update the gate's residual prose at `:114-116` in the eventual landing patch.

## Peer inventory and write boundary

At the time of this audit, all 12 C2 and all 12 C3 seat reports were present; 11/12 C1 reports were present (EX-1 absent). The only delivered verdict peers were CR-5 and VZ-1; CR-5's baseline/plus-agnostic dash checks match my independent results, while VZ-1 also identifies the `+` marker residual. No unanimous C1 candidate choice is established yet.

All scratch was created under `/var/tmp` and removed after measurement. Only this CR-7 artifact is written by this seat. The pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` worktree modification was left untouched; no Git mutation was performed.
