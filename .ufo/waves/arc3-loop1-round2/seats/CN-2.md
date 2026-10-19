# SEAT CN-2 — chain cross, role connector — arc3-loop1-round2

Status: complete (v1). Artifacts: `claims/cross/records-outline.md` (v1),
`claims/cross/CN-2/{merged-SCORECARD-section.md, merged-LOG-entry.md,
pin-free-check.py, receipts/*}`.

## 1. Work performed (evidence pointers)

1. **Reconciled the three chains' records drafts into one parent-records
   package.** Read all six drafts (`claims/{c1,c2,c3}/records-drafts/`), the
   round-1 committed records as the shape precedent (`SCORECARD.md:1338-1417`,
   `LOG.md:1398-1430`), the round-1 connector package
   (`.ufo/waves/arc3-loop1-round1/claims/cross/{records-outline.md,consistency.md}`),
   and the frozen claims. Produced:
   - `claims/cross/records-outline.md` v1 — package inventory R1–R8, commit
     sequence + gates, skeletons, single-source-numbers contract, line-shift /
     digest couplings, merge-slot map, **merge-delta table** (§7.1), parent
     preflight recipe, named gaps, receipt index;
   - `claims/cross/CN-2/merged-SCORECARD-section.md` — literal R2 section,
     **re-folded after the C2/C3 draft revisions and the CN-1 alignment edit:
     187-line body sha256 `ce83a08cc92a063e…`** (first fold 145 lines
     `5e0a5312d973bbec…`, second 180 lines `a474efeb60249885…` — each revision
     re-gated);
   - `claims/cross/CN-2/merged-LOG-entry.md` — literal R1 entry, 105-line body
     sha256 `26b9ebf6bda2d269…`.
2. **Independently verified C2's after-legs** (before/after matrix at HEAD
   `14b1682b`, scratch roots under `/dev/shm/cn2`):
   `claims/cross/CN-2/receipts/census-h1h3-settled-matrix.txt` — before
   instrument `6f1d19ff…`: absent SKILL.md → silent PASS exit 0
   (`lines=0 loci=0`), full needle-neuter → all-zero loci, old vacuous guard,
   PASS exit 0; after instrument `df9ffdf9…`: `UNREADABLE
   ['SKILL.md: FileNotFoundError']` + `DECLARED FAIL CLASSES: ['UNREADABLE']`
   exit 1; `BLIND-INSTRUMENT` + `G2 … SUSPECT` (per-file floor, zero
   substrate) exit 1; ordinary HEAD run PASS 0/0/0/0 unchanged
   (`receipts/ordinary-head-settled.txt`).
3. **Independently verified C3's after-legs**: selftest CLEAN 15/15; live
   read-only capture 5/5; label defect measurably gone (`MTIME_EPOCH
   1792011200` → `MTIME_UTC_RENDER 2026-10-14T20:53:20Z`, local render kept
   separate); same-content rewrite detected — in-place with mtime rolled back
   → `REWRITE-DRIFT moved=ctime_ns` exit 11, remove-and-recreate → `moved=
   inode,mtime_ns` exit 11, both with `SHA256-CONTRACT: 1/1 paths agree`;
   v1 back-compat: round-1 canonical receipt → `SHA256-CONTRACT: 5/5 agree`
   with the v1 label defect surfaced as a declared LABEL-DEFECT →
   METADATA-DRIFT class (exit 12).
4. **Built and ran the PIN-FREE gate** (`claims/cross/CN-2/pin-free-check.py`)
   over the six chain drafts (all CLEAN) and the merged texts (both CLEAN).

## 2. Proposed changes

No repo file change is proposed by this seat (connector role). The parent's
landing material is the merged text at
`claims/cross/CN-2/{merged-SCORECARD-section.md, merged-LOG-entry.md}`
(pasteable blocks only — **not** the artifacts' prose: the outline's and the
merged files' notes sections contain an example pin literal inside the
injection-control recipe, and pasting those into SCORECARD would FAIL the
census). Remaining `[[FILL]]` slots are named with their producing seats.

## 3. Before → after measurement (this seat's claim: records reconciliation holds under the PIN-FREE gate)

Commands (cwd = repo root; scratch `/dev/shm/cn2`, never `/tmp`):

```
# extract literal block from the merged artifact (bounded by the BEGIN/END markers)
python3 - <<'PY'  # as in §10 of the outline
PY
python3 claims/cross/CN-2/pin-free-check.py /dev/shm/cn2/sec-merged.md
# rebuild projection root from git objects at HEAD, append the extracted block, run census
/dev/shm/cn2/proj-test.sh /dev/shm/cn2/sec-merged.md
```

Measurements:

| Reading | Before | After |
|---|---|---|
| chains folded into one package | 0/3 (no draft existed at seat start) | **3/3 folded**; six drafts read and spliced; C2/C3 blocks re-folded after their revisions; merge deltas recorded |
| PIN-FREE on the pasteable R2 text | rule existed as prose (round-1 injection) | merged **180-line** section (body `a474efeb…`): `PIN_FREE_VERDICT: CLEAN`, exit 0 |
| PIN-FREE on the six chain drafts (independent of their self-checks) | — | CLEAN 6/6 (all four chain draft files + the C1 rule-text candidates) |
| census projection, merged section appended (instrument `a4c16763…` at final run) | — | `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 — `receipts/merged-section-projection.txt` |
| discrimination control, unmarked pin appended | — | `VERDICT: FAIL (undeclared=1)`, exit 1 — `receipts/merged-section-injection-control.txt` |

## 4. Attacks / refutations attempted

1. **Unmarked pin in appended text** (round-1's demonstrated hazard): injection
   A reproduces `FAIL undeclared=1 exit 1` on both the before-instrument and the
   settled one — verdict: **confirmed live**, the merged text's PASS is
   evidence, not vacuity.
2. **Bare version in a client clause**: injection B → `FAIL undeclared=1` —
   verdict: confirmed (the detector covers bare `6.x.y`, not only `@`-pins).
3. **Chains' own drafts vs my checker**: all six CLEAN — verdict: their
   pin-free claims hold under an independent implementation of the token
   families (`c1-census-v10.py:163-167`). Also checked C1's three candidate
   rule-#14 texts on disk (EX-05 fallback, EX-03 scoped, CR-1 candidate set) —
   all CLEAN, so the pending SKILL.md append is cleared on the census side.
4. **Instrument churn (W1)**: during measurement the census moved through seven
   observed revisions (`6f1d19ff…` → `2a89793a…` → `59975ae0…` → `82fb807e…` →
   `762bfebe…` → `c95a5cf3…` → `df9ffdf9…` → `a4c16763…`). At `2a89793a…` the
   unreadable-file print path raised `TypeError` (counts `lines=None` formatted
   with `%d`); at `762bfebe…`/`c95a5cf3…` the per-file floor counted current-ok
   *blocks*, SKILL.md's mixed block read 0, and **the ordinary HEAD run FAILed**
   (`BLIND-INSTRUMENT`), contradicting the frozen claim's "ordinary runs at HEAD
   stay PASS 0/0/0/0". From `df9ffdf9…` on, the floor counts asserts per file
   and passes (`PROVINCE 17 / SCORECARD 14 / SKILL 3`), stable across ≥10 checks
   30 s apart (`/dev/shm/cn2/sha-watch.log`). Verdict: **transient red states
   were real and are recorded**; the parent must land only a revision that
   passes the ordinary HEAD run, and re-derive the landed identity (C2's own
   after-receipts pin `82fb807e…`, not the current file — an instance of the
   rule-#14 class this round admits).
5. **Chain-draft churn caught**: C2's and C3's literal blocks were revised
   after my first fold (their scribes closed their own `[[FILL]]`s with measured
   receipts). Re-extracting and diffing against the folded shas caught it;
   the merged text was re-folded and the gates re-run — verdict: the re-fold
   holds (180-line body `a474efeb…`, gates green). This is the same class as
   the round's C1 rule: a fold is only as fresh as the identity check that
   follows it.
6. **Merged-text self-attack**: pasting the merged artifact *including* its
   notes (which embed an example pin in the control recipe) would FAIL the
   census — verdict: **caveat confirmed and flagged** (paste the literal block
   only; §2 above).
7. **C3's v1 back-compat**: re-ran the round-1 canonical v1 receipt against
   live — sha256 contract 5/5, label defect surfaced as declared class —
   verdict: C3's claim clause holds as stated.
8. **C3's rewrite attack, strongest form**: rewrite + `os.utime` mtime rollback
   → detected (`moved=ctime_ns`, exit 11) — verdict: the ctime pin is the load-
   bearing field, as the tool's own header claims.

## 5. Blockers / gaps

- **R5 (C1's rule #14) has not landed** (`git status`: SKILL.md clean at seat
  close): the depth axis's before→after (13/13 → 14/14) and its verdict-table
  row stay `[[FILL]]`; my merged text does not assert 14/14 as measured. When
  the rule text lands, run the checker on it too (the census scans the whole
  file; a locus in the craft section is UNDECLARED unless it matches a live
  anchor with receipt language).
- **R6 is uncommitted and was churning**; quote/re-derive the landed revision
  at the records commit (W1).
- **R7 is untracked** and contains a `__pycache__/` — exclude from the work
  commit.
- Delivery count (VZ-4 roster reconciliation) and the custody post-pair are
  pending; both are `[[FILL]]` slots in the merged texts, not assumptions.
