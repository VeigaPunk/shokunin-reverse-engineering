# ReviewerGates — scoped findings

Axes: calibration / operability / coverage.

**Observation — freeze:** all four committed and working instrument SHA-256 values match claims.json pins; operative-freeze-to-main tools diff is empty. Evidence: `ReviewerGates/freeze-integrity.json`.

**Blocking findings (observed executable attacks):**
1. C2 probe accepts a foreign instrument/revision receipt with fabricated packing argv and wrong names: complete probe exit 0, arms_passed 6, failed []. `tools/round-69/contract-probe.py:100-160,167-175,211-216` never binds receipt provenance to selected instrument/revision.
2. C3 checker accepts missing identity arm; also a single shared-object-shaped carrier with empty arms while top-level totals assert three. Exit 0/met true. `tools/round-69/packed-elf.py:280-309` trusts totals and only visits provided arms, without checking canonical carrier IDs or libz pin.
3. C3 ratio NaN passes `> 0.75` rejection although it does not satisfy `<= 0.75`; checker exit 0/met true. `tools/round-69/packed-elf.py:302-304`. Finite .75 passes; .7501 fails.

**Advisory findings (observation/inference distinguished in full review):** nonempty invented rows defeat both structural validators; battery aggregate ok does not enforce pristine.cases; supplied --upx is validated/recorded while actual operations use constant UPX. Older literal identity and locally constructed skip-run selftests are vacuous for production wiring, but the five arm-false cases genuinely reach the seam.

**Observation — C1:** isolated battery against frozen r69 gives pristine cases 20/ok true, zero survivors and five named correct-case kills. Same battery against r68 at the literal base gives pristine cases 13/ok true and exactly the five declared survivors. Commands and full output: `ReviewerGates/attacks.json`.

**Inference — recommendation:** do not treat C2/C3 counter green as sufficient evidence of their frozen receipt predicates. Preserve/report defects without editing or narrowing the freeze. This is a recommendation, not claim judgment or admission.

**Unknown / gaps:** eventual L1 landing hash and actual three-carrier measured receipt; no full REA route measurement performed by this seat. Existing reported base C2/C3 failures were read, not rerun. LSP device unavailable (“No such tool: xd://lsp”), so semantic references/definition/diagnostics could not be obtained. No installations/updates, tracked lane edits, index writes, commits, pushes, or nested agents.

Full clause map, defect evidence and residual risks: `.ufo/waves/round-69/w1/ReviewerGates/review.md`. Inputs, outputs and base-to-freeze actual diff are alongside it. Scratch removed before terminal handoff.

Report: .ufo/waves/round-69/w1/ReviewerGates.md
