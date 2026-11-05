# ReviewerScope.md — contract-conformance review of the frozen round-96 declaration

**Verdict: PASS on all four review items.** Two disclosed-only deltas (the supersession
amendment + R95-VD-2 attribution omit) and three residual, documentation-level
observation items (see `ReviewerScope/scope.md` for the full itemized review with
evidence pointers per PASS).

## Summary of evidence per item

1. **Plan ↔ claims.json agreement** — PASS. Cross-checked: base revision
   `0ea695e826f2dca53dd55ac0bafead93de26b173`, pins path, both frozen labels (battery and
   C1 target labels, verbatim), all six before-receipt paths, S321 source + sha256 +
   evidence receipt (closes the round-93 carried limit), expect-blocks 35, mutant table
   and forgery-fixture paths, after-receipt placeholder paths, kill-rule clauses. No
   contradictions. Two declared-only additions (not contradictions): `instrument_supersessions`
   and `kill_rule_amendment` exist only in the supersession commit's claims.json (verified
   additive diff, never silently patched into the declaration); R95-VD-2 is stated in the
   plan but not referenced in claims.json (attribution-level gaps only, no conflicting
   statement).

2. **Structural facts from committed bytes** — PASS.
   - `git rev-parse` + `git log --format='%H %P'`: declaration commit
     `e4d1f7de9deae83e6d5f78d2d7f0157196002af0` has parent exactly the base revision;
     supersession commit `3baac2ef4b9b2830d299125b8184ca06d9e6584d` has parent exactly the
     declaration; lane HEAD = the supersession commit.
   - Three C1 before receipts: killed 5 of 10 with survivors exactly
     {M2, M3, M4, M6, M10}; accepted 5 of 6 with a bare `KeyError: 'fresh_scored'` on
     forge-unlabelled and nojson exit 0 without a receipt; probe before leg victim_intact
     false (followed the planted link), after leg victim_intact true. All match plan.
   - Three C2 base receipts all exit 1 with expect 35 (block 35 missing / blocks 34
     resolved 34 / blocks 34 resolved 34 required-shaped 0/0). All match plan.
   - Mutants.json: M0 identity control + M1..M10; every `find` string occurs EXACTLY ONCE
     in its target's committed bytes, in BOTH the declaration and supersession trees
     (checked programmatically; 0 bad counts).
   - Six forgery fixtures × {json,stdout,rc} exist in both trees; each forge-<name>.json
     deviates from the honest template in exactly one field — the designated lie. The
     .stdout/.rc files are synthetic template exports written by the pinned generator
     (gen-forgery-fixtures.py), not counter runs.
   - S321 receipt: exit 0, met true, {} counts repaired 2 / far_refused 2; source sha256
     re-verified live against /usr/bin/printf — still matches exactly.

3. **Pins** — PASS. `sha256sum -c .ufo/waves/round-96/pins.sha256`: 0 mismatches in the
   declaration tree (51 entries) and 0 mismatches in the supersession tree (60 entries,
   regenerated per the disclosed fixture refresh). Coverage: all 13 tool paths named in
   the claims, plus mutants.json and both C2 manifests, plus the round-95 instruments
   (battery-v5, c1-agreement-v2, c1-forgery-refusal, symlink-probe) and round-94 names —
   all pinned. The three C2 kill-rule sha256 prefixes (34cf65…, 359f15…, bcf6c4…) all
   appear verbatim. Declared supersession hash deltas verified exactly for
   kill-rule-v2.py and battery-v6.py; symlink-probe-v2.py pin unchanged (matches "probe
   unedited by the supersession").

4. **Supersession disclosure** — PASS. The superseded claim's json names the supersession
   commit hash three times (one per disclosed `of` clause). Red evidence
   `honest-pos-red-head-not-bound.{json,stdout,stderr,rc}` exists, is honest, and carries
   the intended selfverify reason: rc=1, stderr `selfverify reason: head-not-bound`,
   stdout `selfverify ok=False reasons=1`, receipt verdict met True exit 1 — the
   fail-closed gate firing as designed. Its `counter_sha256` records the PRE-fix v6
   bytes, coherent with the disclosure (the fixing run executed the pre-fix bytes). Green
   evidence `honest-pos.json` also committed (exit 0, selfverify ok=True reasons=0, head
   bound to the declaration revision). v6 `verify_receipt` implements every binding the
   plan names (schema-valid counts, label recompute, met direction, revision-not-bound,
   head-not-bound, counter/verdict/repair-pin-not-bound).

## Residual observations (not blockers, documentation-level)

1. The frozen C1 target label's "forgeries refused 10 of 10" counts only the six
   round-96 fixtures; the r95 forgery battery re-run is a separate gate, so the wording
   is ambiguous if read as "all forgeries."
2. Forge fixtures carry world revision = base, not the declaration — deliberate, but
   they bind to baked pins, not to declaration bytes.
3. `verdict_sha256` (round-93 battery bytes) is receipt-bound but has no *.py path pin —
   carried as a named limit in the plan itself (disclosed, not new).
4. `c1-at-decl-worktree.json` (kill-rule green at working bytes, counts 10/10 across all
   gates, world_revision = declaration, revision = null — worktree measurement) sits in
   l1/scores but is not itemized in either file's evidence lists; acknowledged only in
   the supersession commit subject as "kill rule green at working bytes."

## Method notes

- Read-only lane discipline held throughout; only `ReviewerScope/scope.md` and this file
  written inside the lane.
- Scratch `/fast/scratch/hyaku/kaidoku-r96/ReviewerScope` used for extracted decl/sup
  trees and removed at finish (with trap-EXIT, no residue).
- No git mutation anywhere; no subagent spawns; no host-state changes; no tool installs
  (RULES.md read, none needed).
