# Sibling-recorded defect patterns relevant to round-41 counters

All entries read-only, verified 2026-10-26 at working-tree bytes. Each pattern is
one this round's C1 exact-path counter or C2 freeze-integrity rule could repeat.

## A. Suffix/basename/prefix path-comparison weakening (R40-CL1 class)

1. **tameshi `corpus/lessons/round-25.md:88-92` (MtGuardGaps)** — 17 single-edit
   weakenings of `tools/command-binding.py` `evaluate()` survive the gate selftest:
   "cwd prefix/basename/commonprefix, exit `abs()` or modulo 256, token case-fold
   or strip, unknown requirement keys, unchecked `stdout_contains`/`stderr` types,
   unchecked `schema`, revision prefix or suffix compare, case-insensitive
   membership, newline-joined argv". Routed forward, not claimed in r25.
   **Still open:** `corpus/lessons/round-26.md:78` (MtGuardGapsRecheck: 0/17 killed
   at `a08e85c`); grep of tameshi `corpus/lessons/round-27.md` … `round-48.md`
   finds no later closure under that name. Same mutation class as kaidoku's
   R40-CL1 (`same_rel` suffix test read `usr/bin/busy` as `bin/busy`).
2. **chousa `corpus/lessons/round-26.md` R26-M2** — "original prereg C3 matched
   exactly 3 digits and used-by basenames; CORPUS contract allows 3+digits ids and
   requires repo-relative paths". Fix: exact rooted paths + negative
   same-basename and S0001 controls. This is the fix *shape* the round-41
   exact-match port applies to C1 path tests.
3. **kagi `corpus/lessons/round-13.md:102`** — mutation executed: id `R12-03a`
   resolved as `R12-03` (prefix match); a comment-only id satisfied a naive grep;
   a stamped-but-deleted path passed membership-only. Fix: whole-word extraction
   (`[A-Za-z0-9_-]*R[0-9]+-[0-9]+[A-Za-z0-9_-]*`) + selftest cases
   `verify-suffixed-id`, `verify-prefixed-id`, `verify-comment-id`,
   `MISSING-POINTER`. Documented residual: range bound (head-only) not fixed.
4. **kake `corpus/lessons/round-47.md:102`** — reopen findings:
   `CriticMatrixBlindness` showed "basename-matcher and doctored-index shortcuts
   can pass" the redirect/verifier detectors.

## B. Fabricated-receipt acceptance (R39-CL5 / R40-CL6 class)

5. **revenger `corpus/lessons/round-63.md:219` (M34)**, carried in
   `SKILL.md:131,174,383,514,592-593` — a shaped JSON
   `{"evidence_id":"invented","operation":"inspect_firmware_regions",...}`
   satisfies the F presence predicate with no fixture, no producer call, no
   receipt. Kaidoku's scoring-time REA rerun (round-40 fix) is precisely the
   missing binding; revenger `corpus/lessons/round-64.md:200` routes "a future
   calibration round that registers a receipt/Evidence-ID binding check" —
   still open as of round-70 (no such round landed; r65-r70 lessons checked).

## C. Frozen-path integrity (freeze-integrity rule class)

6. **kake `.ufo/waves/round-45/w1/SentinelFrozen.md:6-13` + `ReviewScopeBound.md:30
   (F1)`** — unnamed Python bytecode-cache write landed in a frozen path between
   baseline and end guard; remediation: "preserve the original `before.sha256` …
   Do not replace the baseline to bless this drift; obtain the L1's disposition
   before any new baseline." Same principle as kaidoku's "a later restore does not
   un-block (exit 2 `frozen_path_changed`)".
7. **kake `corpus/lessons/round-20.md` + `round-24.md:8,15,21,47`** — fleet
   ruling: "suffix additions rewrite historical lines"; rejected; replaced by
   hash-bound sidecar corrections preserving original bytes/coordinates
   (non-author files unchanged).
8. **tameshi `corpus/lessons/round-48.md:404`** — a claim's own record edits moved
   a pre-registered no-harm monitor after content froze; first check that could
   see it ran post-freeze; credited counts silently fell 60 → 57. Freeze-window
   drift class: monitors pinned before the freeze must keep their pinned inputs.

## D. Independent-evaluator split (R41-C2 / D3 closure pattern precedent)

9. **kake `corpus/lessons/round-26-verifier-spotcheck.md:33`** — closure parser
   "independently written from the reviewed rule rather than importing the lane
   module". Same construction as the round-41 C2 independent evaluator (written
   from the precedence text only; never reads table/interpreter/generator).
10. **tsukuroi `corpus/lessons/round-18.md:9`** — "Same independent evaluator on
    baseline" used to reject a consolidating revision binding.

## Notes

- 1-4 corroborate that the R40-CL1 defect class survives naive selftests fleet-wide;
  tameshi's is still live in a shipped gate, so the round-41 counter's
  both-direction collision selftests (R41-C1 pre-freeze dry run) are the right
  minimum, not overkill.
- 6-8 are the closest sibling analogs to the freeze-integrity rule; none states
  the exact "later restore does not un-block" clause, so the round-41 rule is not
  anticipated anywhere else in the fleet.
- Nothing above is absorbed; report-only per seat contract.
