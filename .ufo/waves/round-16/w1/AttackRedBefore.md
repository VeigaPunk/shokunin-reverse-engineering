# AttackRedBefore — documentation markers are not semantic repair evidence

**Axes:** calibration (direct), depth (do not transfer this control's credit to the selector). Author-seat advisory only; no judgment or admission.

All anchors below are absolute paths under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Counterexample

The retained red command cannot distinguish a real producing-command implementation from a file containing only `# argv\n`. Its exact predicate is `bool(co) and 'argv' in co`, where `co` is the Git-object text of `controls.py`; the command never imports or invokes that file. **[INFERENCE, direct evaluation of the displayed predicate; not executed]** Both texts satisfy `producing_command_retained`, although the comment-only file produces no report and retains no executed argv.

Likewise, appending a heading `Round-16 correction` followed by “Do not use `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py`; keep the original recheck” satisfies `invocation_correction` while recommending the opposite of the intended repair. Holding the other predicates fixed, either substitution leaves the command unable to distinguish the semantic defect. These are static counterexamples, not observed candidate contents or fabricated runs.

## Evidence

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/documentation-red.json:6` retains the complete `python3 -I -c` program: substring checks over four immutable Git objects, a sum labelled `resolved`, and exit based on those checks. There is no producer-output comparison, inventory invocation, or behavioral oracle. Lines 8–12 retain baseline `6235498b4112350eebce0812a74af1781fc0ee88`, exit 1 and false flags. I read that record; I did not reproduce it.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/claims.json:12-14` expressly calls this a **documentation control**, but its after-state says “all four resolved with reproducible command evidence.” The red record alone establishes missing markers, not that route resolution was behaviorally falsified.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-15-verifier-spotcheck.md:185-188` routes invocation consistency, supplemental discoverability, producing-command provenance and historical wording. Line 185 explicitly declines unobserved argv equivalence. These are bounded documentation/provenance obligations, not a demand for changed Ghidra behavior.
- The actual correction draft is stronger than the predicate: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/w1/CorrectionDraft.candidate.md:23-27` withdraws the literal executed-string overstatement, distinguishes the unrecorded spelling and directs future rechecks to recorded argv. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/verification.json:29-40` supplies that historical argv. This supports a substantive provenance correction; it does not establish an output difference caused by `-I`.

## Smallest safe correction

Keep this control documentation-only and call its fields **markers present**, not semantic resolution. Pair the immutable before/after marker evidence with a short route-by-route content adjudication: exact recorded argv versus corrected guidance, supplemental path in the pinned-values cell, the retained producer invocation/output and immutable inputs, and the correctly historical SHONEN evidence line. A source file merely containing `argv` cannot discharge producing-command provenance.

**Exact missing semantic evidence:** this command supplies no fixed-input, behavior-sensitive before/after comparison in which changing the documentation changes an exercised decision or producer result. Do not claim that it does. No target experiment or new classifier is needed to repair the stated documentation/provenance claim. If a semantic-behavior claim is nevertheless made, renaming markers cannot support it; that stronger claim needs its own evidence or must be withdrawn, not traded for C1 depth credit.

**Limits:** read-only review of retained source/records and the available invocation draft; no assertion about later integration or uninspected receipts. No checks, target/source execution, builds, tests, linters, formatters, separate runtime, installs or updates. Only this report was written.
