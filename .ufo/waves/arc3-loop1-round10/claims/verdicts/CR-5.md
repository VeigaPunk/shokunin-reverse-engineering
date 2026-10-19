# CR-5 — arc3-loop1-round10 verdict reconciliation

**Chain:** verdicts/convergence (`claims-frozen.md:67-72`). This artifact re-derives the source-derived baselines and the C3 gate boundary. Numeric C1/C2 experiment results in peer artifacts are not treated as my measurements.

## Revision and baseline controls

- `git rev-parse HEAD` → `5694506a862c32d2f7aac44935778bce4b6184f2`; `git rev-parse eb5a2c4` → `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`. `HEAD` is the records commit whose parent is the named work commit.
- I independently ran SCORECARD Command A (`SCORECARD.md:88-124`) against both immutable trees. Exact outputs:

  ```json
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "HEAD", "rule_blocks": 15}
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "eb5a2c4af9d910bb7a3d4fced780f4641e341a24", "rule_blocks": 15}
  ```

- Source-path status check: `git status --short -- .ufo/gates/c1-census-v10.py corpus/knowledge corpus/README.md SKILL.md PROVINCE.md SCORECARD.md` printed no lines; `git diff --quiet` over the same paths exited 0. Therefore no C1/C2/C3 source after-state is present in the measured worktree.

## C1 — coverage

**VERIFIED — baseline only.** At both revisions, the independently derived result is 88 knowledge files, 88 mapped, no missing or dangling tokens. This is the pre-integration state; it does not establish the frozen 88→89 after-condition.

**UNVERIFIABLE — selected/landed C1 result.** The available C1 artifacts are drafts and do not yet represent one consolidated choice: `CR-1.md`, `EX-3.md`, `EX-5.md`, `EX-7.md`, `EX-8.md`, and `CR-4.md` investigate overlapping Vyper EVM-target cases, while `EX-4.md` proposes a different `inspect_rust_binary` Evidence-ID Unknown. They name different candidate entries/map tokens; the corpus and map remain unchanged. Their individual compiler/REA result numbers were not re-run by this verdict seat and are not accepted here as independently verified findings. Integration must select one bounded Unknown, land one entry plus its map token, then rerun Command A at that commit before claiming 89/89.

**DISCREPANCY — EX-8 draft locator.** `claims/c1/EX-8.md:27,29` repeats `.ufo/waves/arc3-loop1-round10/claims/c1/EX-8/` inside an already repository-rooted path, for both the source and recheck command. Correct the proposed locator before integration; I did not edit the peer artifact.

## C2 — depth

**VERIFIED — baseline.** The source-derived Command A results above independently establish `rule_blocks=15` and `citation_resolved_rules=15` at both revisions.

**REPRODUCED — one draft is parser-compatible, in memory only.** I projected the exact rule bullet from `claims/c2/SC-2.md` into the HEAD Queue-drain craft text and applied Command A's rule split and citation path/range resolver. Output:

```json
{"before": {"citation_resolved_rules": 15, "rule_blocks": 15}, "in_memory_projection": {"citation_resolved_rules": 16, "rule_blocks": 16}, "new_rule_refs": [{"lines": 63, "path": "2026-10-19-arc3-r4-evm-vyper-leg.md", "range": [51, 57], "valid": true}, {"lines": 17, "path": "2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md", "range": [5, 6], "valid": true}, {"lines": 17, "path": "2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md", "range": [17, 17], "valid": true}], "source_revision": "5694506a862c32d2f7aac44935778bce4b6184f2"}
```

The cited co-landing examples also resolve in the immutable commit trees. `git diff-tree --no-commit-id --name-status -r 40de38343398eee72aeebad7429f3bb99ab0a8dd -- PROVINCE.md corpus/README.md corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` returned `M PROVINCE.md`, `M corpus/README.md`, and `A corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`. The corresponding R8 command for the gate, receipt, PROVINCE, README, and R8 knowledge entry returned `M .ufo/gates/c1-census-v10.py`, `A .ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt`, `M PROVINCE.md`, `M corpus/README.md`, and `A corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md`.

**UNVERIFIABLE — landed C2 move.** The current `SKILL.md` remains at 15 blocks. Peer drafts mostly converge on dependency-coupled landing; `EX-10.md` and `EX-14.md` propose different craft topics. No single canonical rule was integrated. The projection is not an after-measurement; the integration check remains Command A reporting 16 blocks with the new rule citation-resolved.

## C3 — operability

**REPRODUCED — current G21 residual.** The current gate hash is `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`. The gate declares 14 fixed rows at `.ufo/gates/c1-census-v10.py:292-308`; the final span covers `PROVINCE.md:161-162`. `frontier_check()` tests those declared spans at `:422-444`, while `PROVINCE.md` ends at line 162. I copied the three gate inputs to scratch under `/var/tmp`, appended one locus-free bullet at line 163, and ran the unmodified gate with `--json`. Exact selected output:

```text
seeded_bullet_line=163
{"case": "baseline", "command": "python3 .ufo/gates/c1-census-v10.py --root SCRATCH --json", "declared_fail_classes": [], "exit_code": 0, "frontier_errors": [], "frontier_rows": 14, "verdict": "PASS"}
{"case": "seeded", "command": "python3 .ufo/gates/c1-census-v10.py --root SCRATCH --json", "declared_fail_classes": [], "exit_code": 0, "frontier_errors": [], "frontier_rows": 14, "verdict": "PASS"}
```

**REPRODUCED — candidate closure on scratch only.** I applied the current `RV-1` patch text (SHA-256 `c0e9e9ca69031e973b872e70ac68548697117eaec7dd7b2ad5e1118b21f4493c`) to a scratch copy of the gate. `patch --batch -p1` exited 0. On copied clean/seeded inputs, the candidate returned:

```text
seeded_bullet_line=163
{"case": "candidate_clean", "declared_fail_classes": [], "exit_code": 0, "frontier_errors": [], "frontier_rows": 14, "verdict": "PASS"}
{"case": "candidate_seeded", "declared_fail_classes": ["FRONTIER-UNEVALUABLE"], "exit_code": 1, "frontier_errors": ["PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)"], "frontier_rows": 14, "verdict": "FAIL"}
```

This verifies the frozen before/after instrument gap for the appended-bullet case and a scratch candidate closure. It does not establish a live gate change: the gate remains untouched. The candidate test does not cover an unregistered claim inserted inside an already registered span or prose that is not a bullet; neither is claimed closed here.

## Reconciliation

- C1: baseline **VERIFIED**; one selected and integrated corpus/map closure **UNVERIFIABLE**. Fix the EX-8 duplicated locator before any integration that uses that draft.
- C2: baseline **VERIFIED**; the projected SC-2 rule/citations **REPRODUCED** in memory; actual rule #16 integration **UNVERIFIABLE**.
- C3: append-past-:162 gap **REPRODUCED**; current RV-1 patch closes the seeded case **REPRODUCED on scratch only**; live gate remains unchanged.

All scratch trees created by this seat were under `/var/tmp` and removed after their runs. No gate, custody path, corpus file, README, SKILL, PROVINCE, SCORECARD, or LOG was changed. No Git mutation was performed.