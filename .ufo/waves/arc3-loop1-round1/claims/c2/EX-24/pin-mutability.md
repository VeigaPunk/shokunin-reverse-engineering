# EX-24 — pin-mutability attack on the citation-drift frozen-run guard

Seat EX-24, chain c2, wave `arc3-loop1-round1`, 2026-10-19. Role: executor
(attack + threat analysis). **Recommendation only — no implementation.** No repo
file other than this artifact and my seat report was written; every experiment
ran on `/var/tmp/ex24/` scratch copies of the three instrument files.

Leg base revision `e845c2b524ad2e59871e004c51a1386e192a74ab` (HEAD at leg start
and at report time, re-checked). Instrument files at that revision, committed
blob == worktree for all three (verified `git show HEAD:<path> | sha256sum`):

| file | sha256 |
|---|---|
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f` |
| `.ufo/gates/citation-drift/expected.json` | `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33` |
| `.ufo/gates/citation-drift/pointer-table.json` | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` |

## 1. Answer to the seat question

**The guard does not protect the pin. It detects table drift *relative to* the
pin — and only for a writer who edits the table and not the pin.**

C2's pin (frozen claim, `claims-frozen.md:46-54`) lives in `expected.json`, which
sits in the same directory, at the same write authority, and lands in the same
commit as `pointer-table.json`. Measured on the exact design (both the
`table.sha256` and EX-21's `table_sha256` key shapes):

- the accident class closes (stale pin + edited table → `exit 2`, never silent);
- **the co-mutation class does not**: edit the table, recompute the pin in the
  same edit → `findings=0 exit=0`;
- **and a one-line variant is worse than co-mutation**: delete the pin key
  entirely (no digest arithmetic) → with the skip-on-unpinned shape that EX-21's
  prototype diff ships (`claims/c2/EX-21/logs/proto-probe.diff:32-36`), the
  guard is silently off.

So the pin's strength is bounded by the write-authority boundary around its
location, and today that boundary is zero: whoever can write the pinned artifact
can write the pin. Its real, measurable value is different from "protection" —
see §4.

## 2. Threat model — who can write what in this fleet

| actor | can write | cannot write |
|---|---|---|
| any seat (incl. the gate's own author) | any **worktree** file (no commits: `claims-frozen.md:80-83`) | commits, `LOG.md`, `SCORECARD.md`, `SKILL.md` (parent-integrated) |
| parent / integrator | commits; `LOG.md`, `SCORECARD.md`, `SKILL.md` | — |
| operator | `~/.config/...` custody set | — |

`expected.json` is in the seat-writable row. Therefore, in the C2 design as
specified, the pin is protected from exactly nothing that the table is protected
from. The defect class that motivates the debt is a *seat* behaviour (R6 finding
#1: "The probe's frozen-run guard cannot see hand-edits of the table it grades",
`.ufo/waves/arc2-loop1-round4/R6.md:25-33`; carried as named debt at
`SCORECARD.md:925-926`), so the realistic attackers are seats, and seats can
write both files.

## 3. Measurements (before → after, and the attacks)

Prototype used: scratch copies only, `/var/tmp/ex24/`. The injected guard is the
C2 design as written — pin digest in `expected.json`, checked as a **preflight**
(return before any entry is graded), digest mismatch → could-not-evaluate class
`pointer_table_tampered`; two variants of the unpinned case, A = skip (EX-21's
shape), B = fail-closed. Injected diff (variant B, `table_sha256` shape):

```diff
--- a/citation-drift-probe.py
+++ b/citation-drift-probe.py
@@ -70,7 +70,8 @@
         if any(f in ("snapshot_tampered", "snapshot_missing",
                      "pointer_table_unreadable", "unpinned_legacy",
+                     "pointer_table_tampered", "table_pin_absent",
                      "root_unreadable", "revision_unresolvable", "internal_error")
@@ -287,6 +288,8 @@
     except (OSError, ValueError) as exc:
         expected = {}
         findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
+    if not pin_table(expected, table_path, findings):
+        return findings
     tree = Tree(root, rev, snapshot_dir, expected, findings)
@@  (pin_table body, variant B)
+    pinned = expected.get("table_sha256")
+    if pinned is None:                      # variant A: `return True` instead
+        findings.add("table_pin_absent", ..., "(unpinned_legacy class: refuse to grade)")
+        return False
+    if sha256_bytes(open(table_path, "rb").read()) != pinned:
+        findings.add("pointer_table_tampered", ...)
+        return False
+    return True
```

Two tampered tables, both semantically meaningful (the R6 class): `emptied`
(`entries`/`quoted` dropped, sha256 `36a00fc6…191dc`) and `silent-weak`
(one needle weakened to text actually present at the cited line — still matches,
no longer pins, sha256 `0eb4b418…333a2`).

**Before (pristine probe at HEAD):**

```
T0   pristine / emptied table              rc=0  CITATION_DRIFT_VERDICT: reported findings=0 exit=0
T0c  pristine / silently weakened needle   rc=0  CITATION_DRIFT_VERDICT: reported findings=0 exit=0
     (the same mutation against an honest needle reddens: findings=1 citation_dead — so T0c
      is a genuine silent-pass, not an unfired needle)
T9   pristine / absent table               rc=2  CITATION_DRIFT: pointer_table_unreadable … exit=2
```

`T9` is pre-existing behaviour: the claim's "absent-table" leg already holds at
HEAD (`citation-drift-probe.py:281-284`), and its selftest case already exists
(`expected.json` case `table_unreadable`, `:1`). The genuinely new case in the
11 → 13 count is the *tampered* one.

**After (pinned prototype):**

```
T1   pinned / emptied table / STALE pin    rc=2  pointer_table_tampered: sha256 36a00fc6… != pinned 738b3a56…; exit=2
T1w  pinned / silent-weak table / STALE    rc=2  pointer_table_tampered: sha256 0eb4b418… != pinned 738b3a56…; exit=2
T1s  same as T1 with --strict              rc=2  could-not-evaluate findings=1 exit=2   (both modes agree)
T4   pinned / emptied table / PIN DELETED  rc=2  table_pin_absent … (fail-closed, variant B)
E21A emptied table / PIN DELETED           rc=0  reported findings=0 exit=0              (skip shape, variant A)
```

**The attacks (all succeed against the C2 design as specified):**

```
T2   emptied table + pin RECOMPUTED        rc=0  reported findings=0 exit=0   ← co-mutation
T3   emptied table + pin key DELETED       rc=0  reported findings=0 exit=0   ← one-line, no arithmetic (variant A)
T5   --expected points at a forged pin     rc=0  reported findings=0 exit=0   ← invocation is part of the trust boundary
T6   pin-check CODE removed + re-pinned    rc=0  reported findings=0 exit=0   ← the script is in the mutable set
T8   committed table via git show, worktree tampered
                                           rc=0  reported findings=0 exit=0   ← grades committed state, not the worktree
```

T2/T3/T5/T6 are silent re-baselining: the pair (table, pin) is rewritten in one
edit, and no verdict changes. T6 is the general form — the pin adds a *second
file* to the mutation set, not a second authority.

**Selftest interaction (implementation constraint, measured):** fail-closed
(variant B) against the *unmodified* harness breaks the selftest 9/11
(`SELFTEST: FAILED cases=11 passed=2 failed=9 exit=1`), because the harness
builds its own `expected.json` per fixture case with no pin
(`citation-drift-probe.py:415-417`). With the harness pinning its fixture table
(one line, and EX-21's prototype already does this:
`claims/c2/EX-21/logs/proto-probe.diff:78-81`), variant B is 11/11 and variant A
is 11/11 — the fail-closed choice costs one condition and zero harness work.

## 4. What the pin does buy (the honest value statement)

Measured gain, and it is real: a *stale-pin* table edit is converted from a
silent pass (T0/T0c) into `exit 2` (T1/T1w), i.e. the PROTOCOL "Two evidences"
clause's intent — "so a later hand-edit of that artifact contradicts the frozen
run" (`PROTOCOL.md:375-378`) — is satisfied for the hand-edit that does not also
re-baseline the pin. The pin also makes the deliberate version *visible*: it can
no longer be laundered by editing one file, because re-baselining forces a diff
to `expected.json`, the file reviewers read. That is a diff-forcer, not a
protection. The clause's own words assume the later edit is by a different actor
than the one who committed the pair; the co-mutation case is outside it.

## 5. Recommendation (ranked; recommendation only, no implementation)

**R1 — registry-level pin, parent-written (recommended).** Put the sha256 of the
three instrument files (probe, table, `expected.json`) in the `SKILL.md`
registry row at the records commit. `SKILL.md` is parent-integrated and seats
are forbidden to write it, so the pin moves across the one real write-authority
boundary this fleet has, and re-baselining becomes a parent action rather than a
seat action. Cost: one row cell; no new mechanism. Precedents already in the
lane: the capability row carries a rev-qualified claim (`SCORECARD.md:918-919`,
"selftest 10/10 at `265e1aa`") and the custody receipts are sha256-capture files
verified with `sha256sum -c`.

**R2 — fail-closed on an unpinned table (recommended, one condition).** An
absent pin must be the `unpinned (legacy)` class → exit 2, exactly as the
snapshot path already does (`citation-drift-probe.py:145-150`, `unpinned_legacy`)
and as `PROTOCOL.md:381-382` states ("a baseline without digests is reported
`unpinned (legacy)`"). Without it, T3 — deleting one JSON key — disables the
guard. EX-20's row patch already requires this
(`claims/c2/EX-20/registry-row.patch.md:85-90`); this seat supplies the measured
attack (T3 vs T4) and the measurement that the switch is free given EX-21's
harness.

**R3 — the registry row must state the limit, not just the mechanism.**
EX-20's patch text says "a tampered table can never read as silent findings"
(`registry-row.patch.md:51`). True against a stale pin; false against a
co-mutated pin (T2). Recommend the row say: *drift detector against hand-edits;
re-baselining requires editing the pin in the same commit, which is what makes
the change reviewable; the pin is not self-protecting.* A one-clause addition.

**R4 — out-of-band digest: record the option, do not take it now.** An
operator-owned digest outside the repo (custody-set extension, or a wave receipt
written by the CU/VZ seats, re-baselined per round) is the only construction
that survives T2/T6. It costs an operator action per round and buys protection
against an adversary this lane has no evidence of; the lane's actual threat is
self-deception by seats, which R1+R2 already bound. Recommend R1 now, R4 only if
adversary-grade is ever demanded.

**R5 — optional strict mode: grade the committed pair.** Read table+expected as
Git objects at `--rev` (`git show`), so the instrument's own inputs come from the
same immutable source it grades; measured, a worktree tamper then cannot alter
the verdict (T8). Tension to state plainly: mid-round, a *new* table must be
worktree-readable to be tested, so this is a post-commit mode for the parent's
integration, not the default.

Priority order: **R2 > R1 > R3 > R5 > R4.**

## 5b. Convergence with sibling seats (same wave, independent measurement)

- **RV-7** reached the co-mutation boundary independently: `X6-consistent-repin`
  (tampered table + matching pin) → `reported findings=0 exit=0`, annotated
  "scope boundary: pin guards drift, not an author re-pin"
  (`claims/c2/RV-7/verify-extra-pre.log`). Same for the unpinned path
  (`X3-unpinned-expected-tampered-table` → `rc=0 findings=0`, "residual hole").
  My T2/T3 are the same two measurements against a *prototype that has the
  guard*, so the pair reads: the guard changes nothing about those two paths.
- **RV-8** scopes which table path the pin binds to (D1 committed-path digest vs
  D2 any `--table`), with the S2 consumer breakage measured
  (`claims/c2/RV-8/guard-compat-matrix.md`). Complementary axis: RV-8 covers the
  `--table` side of the invocation boundary, this seat covers the `--expected`
  side (T5).
- **EX-23**'s guard shapes confirm the exit-class distinction this artifact
  measures: a guard that only *reports* the mismatch yields probe-mode
  `reported findings=1 exit=0` (guardA), a guard that puts it in the
  could-not-evaluate class yields `exit=2` in both modes (guardB)
  (`claims/c2/EX-23/harness/census-results.json`, scenario `H1-rekey-line`). The
  frozen claim's wording ("yields the declared preflight could-not-evaluate
  class (exit 2), never silent findings") is satisfied only by the CNE-class
  shape.

## 6. Gaps and what was not verified

- EX-16's real landing had not appeared by report time (`claims/c2/EX-16/` absent,
  gate files unchanged at their 2026-10-18 mtimes). My after-state is a scratch
  prototype in two shapes (`table.sha256`, and EX-21's `table_sha256`), not the
  landed instrument; if EX-16's identifiers differ, the exit *classes* measured
  here are unchanged but the finding ids must be reconciled (EX-20's patch lists
  the same three coupling points).
- Not attacked: a pin stored as a digest of a *normalised* table (no such design
  proposed); a pin whose comparison is `str.startswith`-style (implementation
  defect class, not a design class).
- The 13-case count: the claim's parenthetical names clean-tree / tampered-table
  / absent-table for a +2 delta; measured, `absent-table` duplicates the existing
  `table_unreadable` class (T9), so the consistent reading is one new case plus
  the guard-pass path on the existing `clean` fixture — flagging for the verifiers
  rather than asserting EX-16's intent.

## 7. Scratch custody

All scratch under `/var/tmp/ex24/` (moved off `/tmp`, which hit its quota
mid-setup — `cp: error writing …: Disk quota exceeded`, the same ceiling R6
documented in r4). Nothing under `/tmp` remains from this leg; `/var/tmp/ex24/`
was removed at report time. No git mutation, no custody-path read/write, no
install. Repo reads only: `git show`/`rev-parse`/`status --porcelain`.
