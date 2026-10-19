# PL-1 seat report — chain c1 (planner), wave arc3-loop1-round2

Seat: PL-1 | chain c1 | role planner. Task: plan C1 (queue-drain rule #14,
self-identity re-derivation discipline) — draft the rule text skeleton, choose
its corpus citations in rule-#11 form (arc3-r1 incident), list adversarial
questions. Artifact: `claims/c1/PL-1/plan.md`. HEAD throughout:
`14b1682b1128d2e41085ebc79c9addeb8786d420` (lane repo untouched by this seat).

## 1. Work performed (evidence pointers)

- Read the frozen claim + roster (`claims-frozen.md`), the round-1 c1 plan and
  verdict, CR-2's F2 bundle, the landed entry, SHONEN.md, the round-1 connector
  sweep, SCORECARD's recipes + arc3-round-1 section, and the citation-drift
  pointer table/expected.
- Measured the before-state: command A at HEAD → `{"citation_resolved_rules":
  13, ..., "rule_blocks": 13, "mapped": 82, "knowledge_files": 82,
  "coverage_score": 10.0, "depth_score": 10.0}`; enumerated the 13 craft blocks.
- Re-derived the incident identities first-hand (not from prose): landed entry
  10,225 B / 33 lines / sha256 `dd986f56…`; CR-2 receipt 890 B / `d1128ec6…`
  (claims 8,316 B / `f95c5a05…` vs applied 8,598 B / `d8d85949…`); current
  `EX-12/knowledge-entry.patch.md` 18,701 B / `d662c195…` whose step 4 still
  claims 9,513 B / 32 lines / `a5119120…` (VZ-1's §D9 third identity).
- Wrote the rule text (23 lines; block sha256 `51a87ef6…`), drafted the patch
  text, and rehearsed the whole change on scratch clones (`/var/tmp/pl1r5`),
  including two non-vacuity controls and the SHONEN.md:6 coupling.
- Artifacts: `claims/c1/PL-1/{plan.md, rule-14.patch.md, rule-14.diff,
  rule-14-block.txt, rule-14-sim.txt, command-a-recipe.py,
  shonen-refresh.patch.md, shonen-refresh.diff}`.

## 2. Proposed changes (patch-text paths)

- `claims/c1/PL-1/rule-14.patch.md` — the SKILL.md queue-drain rule #14 hunk
  (24 inserted lines / 1,738 B; base `SKILL.md` 371 lines / 27,390 B /
  `483b0eba…`; rehearsed result 395 lines / 29,128 B / `11647e6d…`).
- `claims/c1/PL-1/shonen-refresh.patch.md` — `SHONEN.md:6` refresh
  (`13/13 → 14/14`, `SKILL.md:81-243 → 81-265`); **same-commit companion**.
- No repo file was written or modified by this seat. No pointer-table, census,
  corpus, LOG or SCORECARD change is proposed.

## 3. Before → after measurement for the chain's claim (commands + outputs)

Recipe A verbatim, run with a scratch clone as cwd (`--root` = clone for the
instruments). Raw transcript: `claims/c1/PL-1/rule-14-sim.txt`.

| # | Measurement | Before | After |
|---|---|---|---|
| 1 | command A (`rule_blocks` / `citation_resolved_rules`) | 13 / 13 | **14 / 14** (82/82, 10.0/10.0; missing [], dangling []) |
| 2 | byte contract (`git diff --numstat`, `-U0` deletions, prefix/suffix identity) | — | `24 0 SKILL.md`; 0 deleted lines; every base byte survives (first divergence byte 17,215, insert 1,738 B) |
| 3 | prior rules | — | raw-identical 12/13, **rstrip-normalized 13/13** (the section's trailing blank run moves to the new last block — measurement trap, see plan §9 Q7) |
| 4 | citation-drift probe (default / `--strict`) | `reported findings=0 exit=0` | `reported findings=0 exit=0` / `clean findings=0 exit=0` |
| 5 | census (instrument sha256 `df9ffdf9…` at read time) | `PASS 0/0/0/0`, SKILL.md loci=2, current-ok=3 | `PASS 0/0/0/0`, SKILL.md loci=2, current-ok=3 |
| 6 | controls | — | out-of-range citation (`:5-99`) → 13/14, depth 9.29; citation removed → 13/14 (non-vacuity: the citation is load-bearing) |
| 7 | SHONEN coupling | `SHONEN.md:6` says `13/13`, `81-243` (stale after the append) | refreshed → command A 14/14; probe 0 findings; needle inside 81-265 hits 1 |

## 4. Attacks / refutations attempted, with verdicts

- *"The rule is an anecdote / duplicates rules #7 or #11."* Attempted to absorb
  it; **refuted** — neither rule names self-identity under revision. Verdict:
  separable; residual: compliance is not machine-graded (reviewer-enforced).
- *"The rule text itself carries a stale self-identity."* **Sustained and
  measured**: the current EX-12 patch text still claims 9,513 B / `a5119120…`
  while the landed bytes are 10,225 B / `dd986f56…` — i.e. the premise reproduced
  itself today. Draft wording fixed accordingly ("three self-identities in ~20
  minutes", not "one stale claim").
- *"Prior 13 rules byte-identical" as literally stated.* **Refuted as phrased**:
  raw block equality is 12/13 (trailing blank attribution). Verdict: the claim
  must be stated as pure-insertion + rstrip-normalized 13/13.
- *"The change disturbs an instrument."* Probe (both modes) and census at base vs
  after: **refuted** — findings 0, census PASS, loci/loci-per-file unchanged.
- *"The countable citation is decorative."* **Refuted by control**: deleting the
  `corpus/knowledge/…:5-7` citation drops command A to 13/14 even though all
  other citations remain.
- *"`:5-7` proves what it claims."* Checked against CR-2's `entry-version-diff`
  — the mid-wave revision's `-`/`+` pairs are exactly the header lines
  (`source:`, `recheck:`); **verdict: the range is the revised block**, and it
  stays resolvable under append-only growth.
- *"Census FAILs on the change."* **Refuted after investigation**: one reading
  returned `FAIL / BLIND-INSTRUMENT` (SKILL.md=0) while
  `.ufo/gates/c1-census-v10.py` was mid-rewrite in the worktree (other seat this
  round; `M`, mtime 12:11:50Z). Version-pinned re-runs (sha
  `df9ffdf9…`) read PASS at both base and after. Recorded as a live hazard, not
  a verdict.

## 5. Blockers

None for this seat. Named gaps/couplings for the parent:

1. **The instrument is moving**: `.ufo/gates/c1-census-v10.py` is
   worktree-modified this round (C2's EX-16 target); every census reading in the
   round records must carry the instrument's sha256 at read time.
2. **C1's landing is parent-side**: seats are barred from `SKILL.md`/`SHONEN.md`,
   so the claim's after-state is rehearsed-on-a-clone until the parent lands
   both patch texts in one commit — the rehearsal is a projection, not a landing
   proof, until command A is re-run at the work commit.
3. **Freeze-scope flag**: the draft's final clause extends the discipline to
   numbers about a produced file (plan §9 Q6); strike it if strict freeze-scope
   is preferred — the acceptance test is unaffected either way.

## 6. Reconciliation with the chain's landed work (added after the wave ran ahead) — amends §2

The chain executed while this plan was being written. **§2's rank changes: the
landing candidate is EX-01's payload** (`claims/c1/EX-01/rule14.patch.md`),
peer-measured by EX-02/EX-04/RV-1 and attacked by CR-1; this seat's draft
(`rule-14.patch.md` here) is a **merge candidate** (plan §11 ranks the deltas).

- **Independent replication of EX-01's payload by this seat** (scratch
  `/var/tmp/pl1r6/repo-ex01`; payload extracted strictly between EX-01's HTML
  markers, inserted after `SKILL.md:239`, committed in the clone): payload
  **1,071 B / sha256 `6cc388cb…`** and patched `SKILL.md` **387 lines / 28,462 B
  / sha256 `a8170b96…`** — both byte-identical to EX-01's claims; command A
  **14 rules / 14/14 / 82-82 / 10.0 / 10.0**; lines 1–239 byte-identical to
  base; citation-drift probe `reported findings=0 exit=0`; census `PASS 0/0/0/0`
  with `SKILL.md lines=387 loci=2` (instrument sha at read time
  `a4c16763…`). Geometry: rule #14 at `:240-254`, next heading `:258`.
- **Unresolved chain contradiction (named, not smoothed):** EX-04 measured a
  *different* patched artifact for the same append — **385 lines /
  sha256 `19057c13…`**, rule #14 at `:240-252` → SHONEN proposal `81-252`.
  EX-01's payload re-applies to **387 lines**, rule #14 ending at **:254**.
  The two differ by two lines; the SHONEN end must be re-derived from the bytes
  that actually land (254 if EX-01's payload lands unmodified).
- **Delta worth merging into EX-01's payload** (ranked in plan §11): replace its
  two bare refs (`SCORECARD.md:1366-1368`, `LOG.md:1411-1412`) with
  section/entry-key form (rule #11 discipline; no instrument grades them — probe
  0 findings either way); add the deletion-closure clause (CR-1's "norm with no
  instrument" objection has no other anchor); add the one-line re-derivation cost
  (optional). Do **not** merge this seat's cross-file clause — EX-01's "claim
  binds the bytes it describes" already covers it.
- **Instrument state moved again** during the reconciliation
  (`df9ffdf9…` → `a4c16763…`), confirming §5.1: pin the instrument sha with
  every census reading.
- **Merged variant measured, not just recommended**: `merged-rule-14.patch.md`
  (+ `merged-rule-14-block.txt`) applies deltas 1 and 2 to EX-01's payload —
  patched `SKILL.md` 392 lines / `0cf18464…`, command A 14/14, rule #14 at
  `:240-259` (SHONEN end 259), probe 0 findings, census PASS 0/0/0/0
  (`SKILL.md lines=392 loci=2`, instrument sha `d0772ce8…` at read), block
  1,319 B / sha256 `5a235f18…`, 0 needle tokens. EX-01's text remains the
  landing candidate unless the chain accepts the deltas.
