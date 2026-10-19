# SEAT CN-2 — chain cross — connector (arc3-loop1-round4)

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Lane: devin
(declared fallback — the hyper lane returned 402 out-of-credits on all 48
seats; recorded in the freeze, not a lane signal). HEAD at all measurements
`015e1bab914713568f339fd53999bc180459cc40` (no seat commits; parent
integrates).

Task as given: **records reconciliation — merge the chains' records-drafts into
one parent-records outline, PIN-FREE; run the census against a projection with
the drafted sections appended.** Artifact: `claims/cross/records-outline.md`.

Writes by this seat: this report, `claims/cross/records-outline.md`, and
`claims/cross/CN-2/**` (fold script, projection harness, PIN-FREE checker,
identity re-derivation, receipts). Scratch under `/var/tmp/cn2r4` (`/tmp` never
used); scratch Git clones are separate throwaway repos — **no git mutation in
the real repo**; custody paths read-only (hash/stat; every custody demo ran on
scratch fixtures or a scratch tool copy). No LOG/SCORECARD/SHONEN/corpus/SKILL/
PROVINCE/README writes by this seat; every target edit is referenced as patch
text.

---

## 1. Work performed (evidence pointers)

**Package delivered.** `claims/cross/records-outline.md` (v7; identity in
`CN-2/receipts/identity.txt`, rule #14) + the two pasteable literal blocks:

- `CN-2/merged-SCORECARD-section.md` — 180 lines, `fa1e2c1a…` (v7 fold).
- `CN-2/merged-LOG-entry.md` — 209 lines, `815980b9…` (v7 fold).

**Tooling built and self-tested** (all under `CN-2/`):

| file | what it does | self-test |
|---|---|---|
| `assemble-merge.py` | mechanized fold: extracts each chain's literal block, splices bullets byte-faithfully, normalizes placeholder conventions to `[[FILL: …]]`, composes the section + entry; a missing chain stubs a **named gap** (never a silent skip) | validated against the r3 drafts as a fixture; `CN2_ALLOW_GAPS=1` for the skeleton phase |
| `project.py` | appends a drafted section to a scratch tree of the three census-scoped files and runs the landed instrument; `--province-patch` / `--skill-patch` apply C2/C3 patch texts; `--inject` plants a control | smoke-tested on the r3 merged section (PASS) + planted-pin control (FAIL `undeclared=1`) |
| `pin-free-check.py` | PIN/VER/PTR/CACHE token gate mirroring the census detectors, plus `--units` replay of the census's gate reach | CLEAN on both literal bodies at every fold |
| `identity.py` | rule-#14 re-derivation of every artifact in this seat's tree + the fold sources | run at close → `receipts/identity.txt` |

**Measured baselines at HEAD `015e1ba`** (`CN-2/receipts/t0.txt`,
`census-t0.json`): command A **83/83, missing [], dangling [], 14/14,
10.0/10.0**; census (`d0772ce8…`, 610 L) **PASS 0/0/0/0**; probe
(`e2665074…`) **13/13 selftest + findings=0 both modes**; table `1b3ab955…`
(57 entries) pinned in `expected.json` `9df0452c…`; custody tool `7cd19c3c…`
(1155 L) selftest **22/22**; README `f30df42e…`.

**Fold timeline (7 folds; each re-gated):** v1 skeleton (all chains stubbed) →
v2 (C3 landed) → v3 (all three landed) → v4 (rows + trends populated) → v5/v6
(chain revisions re-folded) → **v7** (final, sources stable ≥ 50 s). Receipts:
`receipts/v1-skeleton-projection.txt` … `receipts/v7-fold.txt`.

**Independent re-derivations this seat ran (not quoted from chain reports):**

- **C3's landed tool** (`29bb45ae…`, 1343 L; README `9d9400da…`, 272 L):
  selftest **28/28 CLEAN**; residual (a) both sidecar spellings refused
  `USAGE exit 2` with victim bytes intact; (b) mkdir shape = declared usage
  class, **0 traceback lines**; (c) padded 5-stanza reference refused with the
  `REFERENCE-COVERAGE` line naming unaccounted paths, canonical-5 distinct
  reference `MATCH 5/5 exit 0`; canonical-5 receipt vs live `MATCH 5/5
  drift=0`. Receipt `receipts/c3-tool-verification.txt`.
- **C1's landing rehearsal** (scratch clone, commit `6b990397…`): entry file
  (18,166 B, `da42d9a2…`) + README PRIMARY additive token (`:38`, one line
  differs, 190 → 190) → command A **84/84**, missing [], dangling [], 14/14;
  **prior-83 files byte-identical 83/83**; added set = exactly the one entry.
  Receipt `receipts/c1-landing-rehearsal.txt`.
- **C2's census instrument** re-run by this seat over the read-only
  `PROVINCE.md`: `total=26 stale=6 adjudicated=2 current=18`;
  `STALE: F1b, F3, F5b, X1, C1, R2` — identical to C2's recorded baseline.
  Receipt `receipts/c2-census-independent.txt`.
- **Coupled landing** (scratch clones `0a60120` and `4ab031f`): C2's PROVINCE
  patch (162 → 162 L, `dfa70b42…`) + C3's SKILL.md row (`8e56f3d9…`, 390 L) +
  the v7 records section → census **PASS 0/0/0/0** and probe **findings=0
  `--strict`**; HEAD control in the same clone also clean. Receipt
  `receipts/coupled-projection.txt`.

**Cross-checks against CN-1** (peer connector, `seats/CN-1.md` +
`claims/cross/consistency.md`): agreement on every shared number — command A
83/83 · 14/14; census PASS; probe 13/13 + findings=0; custody 22 → 28; C1
landing 84/84 with 0 diffs; the coupled landing clean in both instruments.
CN-1's **F-1** (registry row unapplied) is confirmed here and carried as the
round's one landing requirement; **F-2/F-4** (re-derive README/receipt
identities at the records commit) are carried in the outline §9.

## 2. Proposed changes (patch-text paths)

- `claims/cross/records-outline.md` — **this seat's outline** (the package's
  map: inventory, commit sequence, skeletons, consistency contract, pre-flight
  recipe, receipt index).
- `claims/cross/CN-2/merged-SCORECARD-section.md` — literal section for the
  parent to append to `SCORECARD.md` after `:1580` (13 `[[FILL]]`s).
- `claims/cross/CN-2/merged-LOG-entry.md` — literal entry for `LOG.md` after
  `:1487` (8 `[[FILL]]`s).
- Tooling: `CN-2/{assemble-merge.py,project.py,pin-free-check.py,identity.py}`
  (re-runnable; not repo-surface changes).

No other file is proposed by this seat. The chains' own patch texts (C1's
entry+token, C2's PROVINCE repair, C3's SKILL.md row) are theirs; this seat
verified them by projection, not by authorship.

## 3. Before → after measurement for the chain's claim

The cross claim is the **records package + its measured gates**, not a
quantity. Before → after:

| leg | before | after |
|---|---|---|
| records package | three chains' drafts unmerged; no projection run | one outline + two literal blocks (v7: 180 L `fa1e2c1a…`, 209 L `815980b9…`); `[[FILL]]`s bounded and enumerated (13 + 8) |
| PIN-FREE | unmeasured | **CLEAN** on both literal bodies at every fold; `--units` reach reported (section 1 reachable unit, entry 1) |
| census projection | — | **PASS 0/0/0/0 exit 0** at v1–v7 and at the coupled landing; **control FAIL `undeclared=1` exit 1** (test is live) |
| coupled landing | r3 precedent guaranteed a `citation_dead` collision | **probe findings=0 `--strict`**, census PASS (measured twice, clones `0a60120`/`4ab031f`) — C3 re-anchored its own table entry, so no collision this round |
| C1 landing rehearsal | 83/83 at HEAD | **84/84** with prior-83 byte-identical; one README line differs |
| C3 tool verification | HEAD 22/22 | landed **28/28**; residuals (a)/(b)/(c) as declared classes; canonical-5 pair MATCH 5/5 |
| C2 census | 6 stale (chain's own instrument) | this seat reproduced the same 6, named; merged text carries 6 → 0 |

## 4. Attacks / refutations attempted, with verdicts

1. **"The projection harness is vacuous — any appended text would read PASS."**
   Planted a census locus (`rea-agents@6.4.0` in a gate-token unit) into the
   projection → **FAIL `undeclared=1` exit 1**, every fold.
   **Verdict: refuted; the gate is live.**
2. **"The merged text carries a locus the checker misses."** `--units` replays
   the census's own `units()`/`REA_GATE` reach over both bodies: 2 reachable
   units total, both classify clean; PIN/VER/PTR = 0. **Verdict: refuted.**
3. **"The r3 §6.5-class collision (C3's row vs the table anchor) must redden
   the probe at the coupled landing."** Ran the real probe `--strict` over two
   coupled-landing clones → **findings=0**, HEAD control also 0.
   **Verdict: refuted by measurement** — C3's own re-anchor is the repair; the
   only residual is the same-commit landing.
4. **"C2's PROVINCE repair may shift a line and break the census."** Applied
   the EX-14 patch in the coupled projection: PROVINCE **162 → 162**, census
   PASS. CN-1 independently measured that even a compensating +1/−1 at held
   total FAILs at the `:119` marker — so the outline records that **total line
   count is not sufficient; the marker line must stay put**. **Verdict: the
   naive line-count test is refuted; the stronger form is carried.**
5. **"C1's map token may be a row insert in disguise."** Applied the PRIMARY
   additive token: exactly one README line differs, 190 → 190, probe clean.
   CN-1's adversarial row-insert variant reddens the probe with 5
   `citation_dead` findings — quoted in the outline as the load-bearing
   distinction. **Verdict: the additive form is load-bearing, confirmed.**
6. **"The chains' numbers may disagree across drafts."** C2's stale count
   appeared as **7** in an earlier revision and **6** in the final one; the
   merged text was re-folded and the number checked against C2's own instrument
   (`stale=6`), which this seat re-ran. **Verdict: the earlier 7 is superseded
   by the chain's own revision; the fold carries the final value — a
   contradiction was checked, not smoothed.**
7. **"C3's tool revision may not actually close the four residuals."**
   Reproduced all four against a scratch copy of the landed revision:
   (a) both spellings refused, victim intact; (b) declared class, no traceback;
   (c) distinct-path gate; canonical-5 control passes. **Verdict: confirmed
   closed as declared classes; selftest 28/28 with the new fixtures.**

## 5. Blockers

None for this seat. Named open items for the parent (all in the outline):

- **F-1 (CN-1's, confirmed here):** C3's SKILL.md registry row is patch text,
  unapplied; the tool+README are in the worktree uncommitted. The C3 claim's
  same-commit clause is met only when the parent applies the row with the tool.
- **Chains were still revising at v7 close** (C2's SCORECARD block moved 4× in
  the fold window). A later revision voids the v7 gates — re-fold (§8 step 0)
  and re-run steps 1–3 before landing.
- **`[[FILL]]`s remain by design:** 13 in the section, 8 in the entry —
  delivery count (35/48 seat reports at close), C2's post-landing verdict row,
  C3's after-column, the custody pre/post pair, the records-commit
  measurements. An unrun check has not passed; do not fill from the frozen
  claim.
- **`__pycache__/` residue** under `.ufo/gates/` (3 dirs) and the r4 wave tree
  (`claims/c1/EX-04/evidence/`, `claims/c1/EX-08/`) — exclude from commits.
- Standing hazards: `/tmp` EDQUOT (all recipes disk-backed scratch); the
  pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` (not this round's).
