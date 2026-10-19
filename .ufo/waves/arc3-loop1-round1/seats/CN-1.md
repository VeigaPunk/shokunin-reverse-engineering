# SEAT CN-1 | CHAIN cross | ROLE connector — cross-chain consistency sweep

Wave arc3-loop1-round1 · 2026-10-19 · HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
(immobile; seats do not commit) · **Status: COMPLETE.** All four shared readings
re-derived independently; both real-target landings (EX-16, EX-28) caught by
poll and verified on the landed files; the records-commit pre-flight with all
three chains' drafts passes.

Task (frozen seat line): the three chains' before/after measurements must not
contradict — command A readings, custody pre-pair claims, instrument states
(citation-drift probe, census v10); reconcile discrepancies or flag them at
`claims/cross/consistency.md`.

Deliverable: `.ufo/waves/arc3-loop1-round1/claims/cross/consistency.md`
(task-named path) and the identical seat-scoped copy
`claims/cross/CN-1/consistency.md` — sha256
`8084ceaef68f04a964aab7928fe0c9c33683d3e0149da25bdce862550b05c405` at close.

## 1. Work performed (each with an evidence pointer)

**Before-state (all four shared readings re-derived by CN-1 before reading any
seat artifact):**

- HEAD pinned: `git rev-parse HEAD` → `e845c2b524ad2e59871e004c51a1386e192a74ab`
  (matches every seat's `head-sha`).
- **command A** (recipe verbatim, `SCORECARD.md:92-124`) at HEAD → `knowledge_files
  81, mapped 81, missing [], dangling [], citation_resolved_rules 13/13,
  10.0/10.0`; identical to `claims/c1/EX-11/command-A-before.txt` and
  `claims/c3/EX-30/recipeA-t0.txt`.
- **citation-drift probe** (from a /dev/shm copy of the committed gate):
  `--selftest` → `CLEAN cases=11 passed=11 failed=0 exit=0`; `--root <repo>
  --rev e845c2b… --snapshot-dir /var/tmp/arc2-l10r10-C2/frozen --strict` →
  `clean findings=0 exit=0`. Identical to `claims/c2/EX-25/logs/before-selftest.txt`
  and `before-probe.txt`.
- **census v10** at HEAD → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
  unresolved=0)`, exit 0, counts PROVINCE 162/6, SCORECARD 1336/9, SKILL 371/2;
  same verdict as `claims/c3/EX-26/census-at-HEAD.txt` (the 4-way c3 capture sha
  `3b677b8e…`). Independent non-vacuity re-check with the instrument's own
  `classify()`: `total_loci: 17  scope-None asserts: 0`.
- **custody 5-path** re-captured; all five match CU-1's pre-pair receipt, EX-01's
  recompute (3 hash impls), EX-02's pre/post pair (diff EMPTY), EX-15's T0/T1,
  EX-26's capture. Re-verified again at close (5/5 identical).
- Before-state digests pinned for the parent's after-diff (`/dev/shm/cn1/baseline/`):
  knowledge per-file sha list `d4416283…` (81 .md + .gitkeep), coverage-map
  `0c67285c…`, README `7c0cf671…`, SKILL `5c93c7c1…`, gates
  `4e28ba90…/738b3a56…/3067621a…/36e96cd5…`.

**Cross-chain verification work:**

- Extracted every probe envelope by parsing (not trusting summaries): EX-06
  `KdxToken` 6/6 (planted == hex == raw == probe, `dispatch:"abi"`, bytecode sha
  `9c40940e…`), RV-2 `Rv2Token` 5/5 on raw+hex and both client versions
  (6.4.0/6.7.0); EX-07's independent M1/M2 agree with all probe offsets.
- Projection tests in an isolated root (`/dev/shm/cn1/root`): C2's real patched
  `SKILL.md` (`fa94a469…`) + C1's draft → census PASS; injection variant with an
  unmarked `rea-agents@6.4.0` → **FAIL undeclared=1** (hazard reproduced, control
  with an inline `historical` marker → PASS).
- End-to-end rehearsal of C1's landing in a scratch git repo: EX-13's real map
  patch + a new entry → recipe A at the projected rev = **82/82, missing [],
  dangling [], 13/13**; exactly one `A` in `git diff --name-status` (prior-81
  byte-identical); README 190 → 190 lines (line-neutral).
- Probe-vs-text-edit projection (`/dev/shm/cn1/proj`, all 20 cited surfaces):
  base → clean; after C1's README patch + C2's patched SKILL.md → still
  `findings=0` (strict and default).
- **EX-16 landed mid-sweep (caught by a 60 s poll at 10:16:16Z):** expected.json
  `4e28ba90…` → `ff47bfd6…`, probe `3067621a…` → `e2665074…`, table byte-stable
  `738b3a56…`. CN-1 re-ran the selftest (**13/13 CLEAN exit 0**), the HEAD probe
  (`reported findings=0` / `clean findings=0`), and the injection battery on
  copies: emptied `entries`, weakened `must_match`, one-byte tamper →
  `pointer_table_tampered` exit 2 (the RV-6 silent class closed); absent →
  `pointer_table_unreadable` exit 2; unpinned expected → `pointer_table_unpinned`
  exit 2 (fail-closed). `expected.json`'s new `pointer_table.sha256` = the live
  table's sha.
- **EX-28 landed mid-sweep (two writes):** blob `c39beccc…` (07:17:44 local) →
  **FAIL** on its own new G18 (`SCOPE-ERRORS: ['PROVINCE.md:40 marker line
  outside its own declared range 45-62 (G18)']`, exit 1); final blob `6f1d19ff…`
  (07:18:16) with the row re-keyed to `(45, 62, DATED, 45, r"2026-10-13")` →
  **PASS 0/0/0/0, exit 0**. The transient is a live non-vacuity proof of G18.
- Records-commit pre-flight: all three chains' SCORECARD drafts appended
  (1336 → 1549 lines) + C2's patched SKILL.md, run under the **landed** census →
  `PASS (0/0/0/0)`, `SCOPE-ERRORS: []`, `UNDECLARED (0)`.
- Cross-read the landed seat reports (37 at close) and grep-swept every shared
  reading for contradictions: none (all `82/82` mentions are after-state
  expectations; all `cases=13` mentions are prototypes or the landed target after
  10:16).
- Flags raised and evidenced: F1 (C3 framing), F2 (census-tail hazard, repro),
  F3 (pin-order coupling), F6 (C2 row-vs-code: landed finding id
  `pointer_table_tampered` vs row text `table_tampered`; stale changeset shas;
  two overlapping row patches), F7 (census fail-open on absent SKILL.md),
  §3j (entry-name coupling), §5 (EX-03 gap, CU-1 time-label defect, pycache).
- Environment: `/tmp` quota-exhausted (EDQUOT) → scratch under `/dev/shm/cn1`;
  repo writes by this seat: the two consistency files + this report only.

## 2. Proposed changes

**none** — a connector sweep proposes no repo edit. All findings are flags for
the parent's integration (consistency.md §3/§4: F1-F7, projection rules in
§3b/§3d/§3j/§3o). No patch-text artifacts produced by this seat.

## 3. Before→after measurement (the cross-chain sweep)

Before (no reconciliation existed; the three chains' shared readings were
independent claims). After (CN-1 re-derived every shared reading, ran the
projections, and verified both landed real targets):

```
$ git rev-parse HEAD
e845c2b524ad2e59871e004c51a1386e192a74ab
$ # command A (recipe SCORECARD.md:92-124) at HEAD, before AND after the landings
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 81, "mapped": 81, "missing": [], "revision": "e845c2b524ad…", "rule_blocks": 13}
$ python3 <copy>/citation-drift-probe.py --selftest          # before
CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest   # after EX-16
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --strict  # after
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
$ python3 .ufo/gates/c1-census-v10.py                        # after EX-28
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)     # exit 0
$ # projection: C1 landing rehearsal (scratch repo)
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "5090fc8d…", "rule_blocks": 13}
$ # records-commit pre-flight (C1+C2+C3 drafts + patched SKILL, landed census)
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      # SCOPE-ERRORS: [], UNDECLARED (0)
```

**Verdict: no contradiction in the three chains' before-state readings; both
landed real targets verify their claims' after-legs; the records-commit
pre-flight passes.** Residual items for the parent: F6(ii) (row text must name
`pointer_table_tampered`), F6(iii) (stale changeset prototype shas), F6(iv)
(two overlapping SKILL.md:371 patches — land one merged row), F7 (census
fail-open on an absent scoped file), §3j (one entry name), F1 (C3's before is
PASS→PASS; the E22 FAIL is the debt's own revision 679af5d).

## 4. Attacks / refutations attempted (with verdicts)

1. *Single-source before-state* → **refuted** (independent re-derivation agreed
   exactly, incl. the 4-way census capture sha).
2. *Dirty-worktree misreading* → **refuted** (HEAD blobs == worktree for all
   scoped files; the one dirty path is outside every scope).
3. *Vacuous census PASS* → **refuted** (instrument's `classify()`: 0 scope-None
   asserts; raw greps of the undeclared tails: no gated loci).
4. *C2's SKILL.md row breaks the census* → **refuted** (real patch applied:
   PASS, loci unchanged, 371 lines).
5. *C1's records section breaks the census* → draft **PASS**, but an unmarked
   version token **FAILs undeclared=1** — hazard **confirmed** and now covered by
   all three scribes' pin-free discipline (verified in the pre-flight).
6. *C1's after-claim is arithmetic-only* → **refuted** (rehearsal: 82/82, prior-81
   byte-identical, line-neutral).
7. *Entry-name mismatch* → **confirmed coupling** (`missing` + `dangling` if the
   file stem differs from the map token).
8. *"command A unchanged" read as a records-commit value* → **resolved** by
   revision-scoping (F5).
9. *frozen_run / snapshot pin misread as live states* → **confirmed metadata**
   (0 `frozen` refs in the script; 0 `@` targets in the table).
10. *Prototype read as the landed instrument* → **confirmed** (all `cases=13`
    mentions before 10:16 are prototypes; the real target read 11 until EX-16).
11. *The landed C2 guard is only a selftest change* → **refuted** (the
    injection battery on the landed probe shows the tamper classes now exit 2;
    RV-6's silent class is closed).
12. *The landed census edit is cosmetic* → **refuted** (the intermediate blob's
    own G18 fired on the un-re-keyed row; the final blob passes only because the
    row was fixed — the new assertion is load-bearing).
13. *Records-commit append breaks the census* → **refuted** at seat time with all
    three drafts (PASS 0/0/0/0 at 1549 lines).

## 5. Blockers

- **None remaining for this seat's task.** Both real-target landings were caught
  and verified; the pre-flight passes.
- Named residuals (in the consistency artifact, for the parent):
  F6(ii)/F6(iii)/F6(iv) (C2 row-vs-code + changeset staleness + duplicate row
  patches), F7 (census fail-open on absent scoped file — not addressed by the
  landed header), §3j (one entry name for the C1 entry), §5 (EX-03's target
  never landed — RV-1 pivoted; CU-1's 3 h time-label defect with digests
  unaffected; `__pycache__` residue in the wave tree), F1 (C3's framing).
- Environment (shared with the wave): `/tmp` quota exhausted → `/dev/shm`
  scratch; recorded, not blocking.
