# ReviewerClaims — round-73 frozen predicates

Recommendation: **do not verify as written**. Detailed findings and evidence: `.ufo/waves/round-73/w1/ReviewerClaims/findings.md`.

## Findings by severity

1. **High — frozen C3 experiment is broken.** Declaration-to-working-tree diff shows that the frozen readelf mutant changes a caller the new selftest never exercises, while the frozen base implicit-capsule patch names a nonexistent block. See `tools/round-73/mutation-check.py:110-138,233-236`, `tools/round-73/packed-elf.py:1334-1347`; frozen predicate `plans/round-73-claims.md:114-127`. Current patch-site repairs are not the frozen experiment.
2. **High — C3 no-case control can pass without testing deleted cases.** `tools/round-73/controls.py:187-209` supplies an uncommitted absolute scratch file to `git show` and accepts its generic rc=2 refusal. It proves neither the promised three survivors nor pristine-red rejection.
3. **High — C1 negative arm switches route, not observer.** Claims `:51-53` names the old route but reasons about the old probe; `seam-probe.py:1018-1028` still runs A12. Reusing the new route's receipt also breaks producer binding (`:649-668`). The control actually runs the old probe and expects target 11 (`controls.py:110-124`), a different experiment.
4. **High — C2 accepts substitute repairs.** D1 permits deleting the incorrect hash instead of appending its correction (`record-audit.py:121-128`); D2 accepts internally consistent pin assertions without resolving the target blob (`:139-150`); D7 permits deleting all but one before pointer and does not require report agreement (`:206-224`). The validator checks aggregate arithmetic, not frozen atom identities or evidence (`:262-291`). Fresh audit execution still has seven fixed atoms, so validator acceptance alone is not fulfillment of the full predicate.
5. **Medium — C1 boolean is weaker than its sentence.** Forged kernel evidence needs only one dirty tool and child dumps only a nonempty clean map (`seam-probe.py:475-486`); the selftest accepts git-only forged kernel evidence (`:1188-1190`). First-sample collapsing (`:544-555`) can omit later dirty genuine samples.
6. **Medium — apply the frozen-edit kill rule honestly.** The declaration diff shows substantive mutation-battery and route-selftest edits; C1 expressly kills post-freeze instrument edits (`claims:58-61`), and C3 requires the frozen battery. Repaired results must not overwrite the original outcome.

## Axes, counters, and residual risks

Coverage moves witness-class coverage; calibration moves record/evidence agreement; operability moves executable reader-seam regression protection. They are distinct surfaces. Coverage is tied-lowest at the bounded 10.0 numeric proxy, not domain saturation (`SCORECARD.md:21-31`). Numeric owned axes are coverage/depth/calibration, not all three claim axes.

The three printed counters derive from their rows, but C3 zero survivors is insufficient without the wrong-case/pristine/pin conjuncts. Main target/record reads use Git; C1/C3 import `capsule_audit.py` from live worktree bytes (`seam-probe.py:125-132`, `mutation-check.py:204-211`), so target pinning is not whole-execution pinning. All predicates have genuine failure paths; specific promised kill conditions remain under-enforced as above. No unrelated canonical-runtime, reroute, or resume-continuity contract is certified.

Potential dirty probe receipts retain environment values (`seam-probe.py:533-540`); key-names/canary-only filing requires redaction. No environment values were emitted or filed by this review.

Verification: static source and read-only Git diff only; no target runtime, selftest, battery, validator or native analysis run. LSP unavailable: `xd://lsp` returned “No such tool”; no semantic references/definitions/diagnostics claim is made. Scratch created and deleted by EXIT trap. No tool installs, Git/JJ mutations, broadcasts or out-of-lane report writes.

Report: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ReviewerClaims.md
