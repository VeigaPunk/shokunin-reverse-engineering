# EX-9 — C2 depth: coupled-landing rule #16

**Disposition:** rule draft and citation list delivered. This seat did not edit `SKILL.md` or any tracked source; the after-landing rule count is therefore not claimed.

## First-hand re-derivation and verdicts

- **REPRODUCED — current Command A baseline.** Ran the recipe at `SCORECARD.md:88-124` against `HEAD` (`5694506a862c32d2f7aac44935778bce4b6184f2`). Exact output:

  ```json
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
  ```

  This is the pre-change baseline only. Since this seat is authorized to deliver a draft, not change `SKILL.md`, `rule_blocks=16` and post-change citation resolution remain **UNVERIFIABLE** until the integrator lands the rule and reruns Command A.

- **CORRECTED — precise r4 hunk label; VERIFIED — dependency.** The frozen shorthand `F5b↔C1` does not match the r4 patch labels: `PL-2/plan.md:185-187` calls the real-solc repair F5b and the C1-dependent Vyper text F5c; `:255-259` says the F5c variant is true only when the C1 corpus entry lands in the same commit. The patch states the same condition at `candidate-coupled-vyper.patch.md:217-224`. Thus the demonstrated coupling is specifically **F5c↔C1**, not F5b↔C1. The work commit independently confirms the paired landing:

  ```text
  commit 40de38343398eee72aeebad7429f3bb99ab0a8dd
  subject arc3-loop1-round4: work — Vyper knowledge entry (arc3-r4), PROVINCE 9-row same-line repair (162 held), ghidra erratum, r3 entry correction
  M       PROVINCE.md
  A       corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md
  ```

  The corpus entry bounds its Vyper result to that leg at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28-30`; its append-only correction records a scope sentence contradicted by a same-commit PROVINCE promotion at `:51-57`.

- **VERIFIED — r8 receipt↔extension dependency.** `git show --name-status 53fcf0c` independently returned:

  ```text
  commit 53fcf0caca7255f730fe1a1f17aefd00203a2978
  subject arc3-loop1-round8: work — ptr_check extension landed on live :4126 anchor (gate + scope re-key + PROVINCE re-anchor + receipt, coupled), Vyper optimizer-forms entry (86->87)
  M       .ufo/gates/c1-census-v10.py
  A       .ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt
  M       PROVINCE.md
  M       corpus/README.md
  A       corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md
  ```

  The committed receipt identifies the live `~/.kimi-code/config.toml:4126` line and says the gate evaluates that pointer via the r8 `ptr_check` extension. The same-commit relationship is also described at `.ufo/reports/arc3-loop1-round8/kaidoku.md:25-33,46-48,80-87`; the commit-tree path list above is the independent co-landing check.

- **VERIFIED — proposed corpus citations resolve.** Re-derived against the same `HEAD` with `git show` line counts:

  ```text
  corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md: lines=63 ranges=[(28, 30), (51, 57)] valid=True
  corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md: lines=17 ranges=[(9, 17)] valid=True
  ```

## Proposed `SKILL.md` rule #16 — draft only

- **A truth-dependent repair is one acceptance unit, not two nearby edits.** If a source claim or instrument result is true only when a sibling artifact also lands, name that dependency in the patch's acceptance condition, co-land every truth-bearing companion in one commit, and rerun the owning check against the combined revision. If a companion is missing or the final check is not rerun, report the result as partial or unverifiable rather than closing one half. This is conditional, not blanket: couple only artifacts that affect the claim's truth. The r4 corpus scope and its same-commit correction show why the source claim must track its companion state (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28-30`; `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57`). The r8 coverage entry likewise says its post-landing count is unestablished until both entry and map token land and Command A is rerun (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:9-17`).

## Citation list

Corpus citations for the proposed rule (all verified in-bounds above):

- `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28-30` — Vyper claim scope and the specific Unknown it closes.
- `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57` — the entry's scope sentence and the same-commit correction after its companion PROVINCE change.
- `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:9-17` — bounded entry claim and explicit entry-plus-map-token landing prerequisite.

Primary coupling records used for the verdicts:

- `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187,255-259`
- `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/candidate-coupled-vyper.patch.md:5,217-224`
- `.ufo/reports/arc3-loop1-round8/kaidoku.md:25-33,46-48,80-87`
- `git show --name-status 40de383 -- PROVINCE.md corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`
- `git show --name-status 53fcf0c -- .ufo/gates/c1-census-v10.py PROVINCE.md .ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md corpus/README.md`
