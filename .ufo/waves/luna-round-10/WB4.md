## CLAIM
Seat WB4: re-audit luna-round-4 records commit `cfc84c2` (work commit `6a71cd5`), independently verifying lane-A seat W4's finding that cfc84c2 rewrote the SCORECARD README pointer `:157`→`:160` before appending round 4.

## METHOD
Read-only Git review: `git show --numstat --format='' cfc84c2`; blob diffs vs parent `6a71cd5`; `corpus/README.md` line-drift trace over `b04b19e..6a71cd5` (21 commits); reflog recovery of pre-amend work commit `35c81b5`; direct reads of the round-4 report, LOG and SCORECARD blobs. No network, no live probes, siblings untouched.

## FINDINGS
- W4's rewrite claim CONFIRMED byte-level. numstat cfc84c2: SCORECARD.md `46 1`, LOG.md `36 0`. SCORECARD.md:68 edited in place (`:160` text) + 2-line disclosure (:71-72), then the round-4 block appends; LOG hunk is EOF-only append (`@@ -711,3 +711,39 @@`), 0 deletions. So SCORECARD is not append-only — and the edit is disclosed (SCORECARD:71-72, `LOG.md:748`, report:53).
- New: the corrected value mispoints at its own commit. At `cfc84c2`, `corpus/README.md:160` is the "sasquatch (AUR)…" row; the described "process/managed/call-target" content ("Runtime-obs extended…") is at :163. Drift trace: 6645585:157 → c265db9:158 (that commit's own 1-line insert) → … → 6a71cd5:163; value 160 held only at round-1-era a3f2e1b/a79945c. Pre-amend `35c81b5` also had 160=sasquatch/163=Runtime-obs (amend was 7±7 wording, no shift) — the amend does not explain it.
- Sibling `:128` left stale: at `cfc84c2`, README:128 = r12-02-queue-b-ledger row; the "4 nits fixed" lessons row is :131. The LOG entry and report repeat the wrong `:160`.
- W4's cited range ":68-73" vs actual rewrite region :68-72 — immaterial.

## THREATS
Git-object evidence only; no live state verified. Even `:163` is stale at HEAD (`corpus/README.md:177` now reads "Runtime-obs depth — … held, not frontier"; the debt was repaired in a later round), so the bullet's live claim is obsolete regardless of pointer value. W4's other round-4 findings (MANIFEST enum prose, SHONEN collapse, untracked seat files) are outside this seat, not re-audited. The "appended, never rewritten" criterion comes from the round-10 goal, not restated in-repo.

## VERDICT
FINDING: W4's pointer-rewrite claim is exact, but the round-4 "record hygiene" correction itself mispoints — README:163, not :160 — and leaves :128 stale; disclosed, yet numerically wrong and formally non-append.
