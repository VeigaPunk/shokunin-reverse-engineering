# EX-20 — SKILL.md citation-drift registry-row patch text (guard semantics)

Seat EX-20, chain c2, wave arc3-loop1-round1, 2026-10-19.
Target: `SKILL.md:371` (the `citation-drift` row of the "Local round-evidence gate
registry" table, `SKILL.md:368-371`). **NOT APPLIED by this seat** — patch text
only, per the wave's seat discipline (seats never write SKILL.md).

Base revision: `e845c2b524ad2e59871e004c51a1386e192a74ab` (HEAD, worktree clean
apart from the wave dir itself). Old row sha256
`6413e8dc6384b9e0e34fca9903b55a4b8bba96066c26ca28789dc1939361d57f`.

## 1. Revision history of this artifact (read this first)

| rev | row sha256 | status | why superseded |
|---|---|---|---|
| v1 | `08be1ec2…6d07a8` (diff `dc99484b…c59067`) | superseded | named the digest-mismatch id `table_tampered` (r3 E14 precedent) and phrased the guard as "absent, unreadable, unpinned, or digest-mismatch". RV-6/RV-8 reviewed this text as the consumer contract; PL-2's landed design uses different ids. |
| v2 | `aeb279a4…f3f774` (diff `9783fd80…c3f73ed`) | superseded | aligned to EX-21's *prototype*, which **skips** the guard when the pin is absent (`pinned_table is not None and …`). Dropping the unpinned clause was wrong: EX-24 measured the skip shape as a bypass (T3 `findings=0 exit=0`) and the chain converged fail-closed. |
| **v3** | `8946c156…d1bb01` (diff `4631e11c…6f259186`) | **primary, verified** | PL-2's `claims/c2/PL-2/frozen-run-guard.patch.md` "Patch 3" row text **byte-for-byte**, plus one inserted clause (`in both probe and --strict modes`). PL-2 is the chain's planner and its patch text is what EX-16 lands. |
| v3b | `2d239264…ed2058` (diff `71590923…d8ece81`) | optional addendum | v3 plus the RV-6 §4.9 note ("`frozen_run`/`exempt` are read by nothing — say so in the row"). Apply v3 or v3b, not both. |

## 2. Why the row must change

`SCORECARD.md:925-926` (arc2-loop1-round4 carried debt, r5 disposition): "the
probe's frozen-run guard (R6: expected.json pins no digest of
pointer-table.json — probe-exempt by kind, gate-blocking if ever promoted)".
C2's frozen claim (`claims-frozen.md:46-54`) closes that debt and requires the
row to state the guard semantics. Before this patch the row declares no guard at
all — RV-6 §4.8 verified clause-by-clause that its verdict map and its
`revision_unresolvable` clause match the code, and that the guard strings are
absent.

Measured hole at HEAD (real probe, scratch table with `entries` emptied), and
independently reproduced by RV-6 (`harness-pre.out` cases B/C/F/G), RV-7, SC-4
and EX-24:

```
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD \
    --table /dev/shm/ex20/tampered-table.json \
    --expected .ufo/gates/citation-drift/expected.json
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
$ … --strict
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

## 3. The patch (v3, primary) — unified diff, applies to `SKILL.md` at HEAD

Apply from the repo root: save the fenced body to a file and run
`patch -p1 < registry-row-v3.diff` (or `git apply`).

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -368,4 +368,4 @@
 | Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
 |---|---|---|---|---|
 | interactive-r1-recovery | gate / kaidoku | `python3 .ufo/rounds/interactive-r1/verify-recovery.py`; 0 clean, 1 failed, 2 could-not-evaluate; `--admission` checks this recovery's unresolved prerequisites and returns 2, never native judgment | same command with `--selftest`; asserts isolated subprocess exit codes and stable finding IDs | `.ufo/rounds/interactive-r1/expected.json` pins every snapshot input and expected outcome; normal entry read-only in this repo; selftest creates and removes only its isolated fixture directory under `.ufo/rounds/interactive-r1/` |
-| citation-drift | probe / kaidoku | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate** | same command with `--selftest`; 11 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
+| citation-drift | probe / kaidoku | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate**; **frozen-run preflight: the table's sha256 must match the digest pinned in `expected.json` — a tampered table (exit 2, finding `pointer_table_tampered`) or an absent table (exit 2, finding `pointer_table_unreadable`) is could-not-evaluate before any entry is graded, in both probe and `--strict` modes; a baseline that pins no digest is exit 2, finding `pointer_table_unpinned`; drift reporting is unchanged (rc 0)** | same command with `--selftest`; 13 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`; the twelfth is a tampered table → exit 2, finding `pointer_table_tampered`; the thirteenth is an absent table → exit 2, finding `pointer_table_unreadable`), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table **and the sha256 of `pointer-table.json` (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
```

## 4. Optional addendum (v3b) — RV-6 §4.9 note

RV-6 §4.9: "`pointer-table.json`'s `exempt` block and `expected.json`'s
`frozen_run` block are read by nothing in the probe … Worth one line in the row
so no reader believes the frozen verdict is machine-checked." Verified by this
seat: `grep -n "frozen_run\|exempt" citation-drift-probe.py` → no match. v3b
inserts, in the pinned-values cell, between the guard sentence and
"normal entry read-only":

```diff
-… (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**; normal entry read-only
+… (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**; `frozen_run` and `exempt` blocks are documentation, not machine-checked; normal entry read-only
```

Full v3b diff body is the v3 diff with that one insertion (row sha256
`2d239264…ed2058`, diff sha256 `71590923…d8ece81`). This clause is **not** part
of the C2 claim's required semantics; it is an operability improvement the
parent may take or drop.

## 5. Required semantics → row clause (traceability to the C2 claim)

| C2 claim wording | Clause in the patched row (v3) |
|---|---|
| guard failures = preflight exit 2 | "frozen-run preflight: the table's sha256 must match the digest pinned in `expected.json` — a tampered table (exit 2, …) or an absent table (exit 2, …) is could-not-evaluate before any entry is graded, in both probe and `--strict` modes" |
| drift still rc 0 | "**probe semantics: 0 reported (drift is reported, never failed)**" (kept verbatim) + "drift reporting is unchanged (rc 0)" |
| `--strict` gate semantics unchanged | "`--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate" (kept verbatim) + the "in both probe and `--strict` modes" clause (the guard lands in the 2 bucket, so the map is unchanged) |
| selftest 11 → 13 | "13 isolated-fixture cases" + "the twelfth … `pointer_table_tampered`; the thirteenth … `pointer_table_unreadable`" |
| pin lives in expected.json | pinned-values cell: "**and the sha256 of `pointer-table.json` (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**" |

## 6. Convergence and coupling

- **The v3 row is PL-2's "Patch 3" row byte-for-byte, plus exactly one inserted
  clause.** Checked mechanically: splitting both rows on `|` yields 7 pieces
  each; exactly one cell (index 3) differs; deleting the string
  `, in both probe and `--strict` modes` from v3 reproduces PL-2's row
  byte-for-byte (`True`). So the parent may apply either; the delta is one
  clause that states the claim's "`--strict` semantics unchanged" requirement
  explicitly.
- **The row text is deliberately pin-shape-agnostic.** It says "the digest
  pinned in `expected.json`" and names no JSON key, because three shapes are
  live in this wave: PL-2 `pointer_table.sha256` (the planner's, what EX-16
  lands), EX-21 prototype top-level `table_sha256`, EX-23 harness
  `frozen_run.table_sha256`. Whichever lands, the row stays true — only the two
  finding ids must match the code.
- **Coupling tokens (must match EX-16's landed code):**
  1. digest-mismatch id — written `pointer_table_tampered` (PL-2 §3; EX-21
     prototype; EX-24 measured `pointer_table_tampered … exit=2` in both modes).
     *Not* `table_tampered` (that was v1's r3-E14-precedent guess).
  2. absent-table id — `pointer_table_unreadable`, already an emitted id today
     (measured at HEAD: `CITATION_DRIFT: pointer_table_unreadable … exit=2`).
  3. unpinned id — `pointer_table_unpinned`, fail-closed exit 2 (PL-2 §3; EX-24
     T4 refused the deletion; RV-6 §4.7 requires it "or the row's `unpinned`
     token must be deleted"). If EX-16 instead lands EX-21's skip-on-unpinned
     shape, **delete the unpinned clause from the row** — do not apply as
     written.
  4. case count — written 13 (11 + `table_tampered` + `table_absent`, PL-2 §4).
     If EX-16 lands a different count, correct the number and the ordinals.
- **Selftest harness coupling (for EX-16, not for the row):** all 11 existing
  cases only stay exit 0 if the per-case fixture `expected.json` also pins the
  fixture table's digest (PL-2 §4 harness change). RV-8 §4.5 flags this as the
  open internal-consumer question.

## 7. Verification evidence (all on scratch copies; SKILL.md never written)

Scratch root `/dev/shm/ex20` (the wave's `/tmp` is quota-exhausted for this
user — `cp` failed with `Disk quota exceeded`; `/dev/shm` has its own tmpfs).

```
$ python3 mkrow3.py                     # build v3 from HEAD's SKILL.md
cells: 7 | single line: True
v3 row sha256: 8946c15618c6b52d4e7ad063f6a715d5274c64a369813b4c82dc572a14d1bb01
PL-2 delta: v3 minus the added clause == PL-2 row byte-for-byte: True

$ diff -u --label a/SKILL.md --label b/SKILL.md SKILL.md.orig SKILL.md.v3 > registry-row-v3.diff
diff_rc=1 (differs, expected)          # 8 lines: 1 hunk, one -/+ pair, 3 context lines
$ sha256sum registry-row-v3.diff → 4631e11c8b018bff17af590163ed303bfe6a004548baab61cd66a2056f259186

$ cp SKILL.md v3t.md; TMPDIR=/dev/shm/ex20 patch --dry-run v3t.md < registry-row-v3.diff
dryrun_rc=0
$ cp SKILL.md v3t2.md; TMPDIR=/dev/shm/ex20 patch -s v3t2.md < registry-row-v3.diff
apply_rc=0
$ cmp -s v3t2.md SKILL.md.v3 → BYTE_IDENTICAL_TO_INTENDED: yes
$ wc -l SKILL.md → 371 ; wc -l v3t2.md → 371      # line-neutral: no line shifts
```

Collateral checks (does the row edit break any instrument that pins SKILL.md?):

```
$ python3 -c "…simulate the two table entries that touch SKILL.md…"
anchor hits: [370]        # skill-registry-row anchors the SIBLING row, unpinned line
shonen range 81 243 must_match ok: True   # shonen-skill-range (SHONEN.md:6) unaffected
```

Census: `python3 .ufo/gates/c1-census-v10.py` at HEAD → `VERDICT: PASS
(stale=0 ambiguous=0 undeclared=0 unresolved=0)`; its SKILL.md scope rows are
`c1-census-v10.py:94-95` (`SKILL.md` 10-16, 18-20) — line-neutral, untouched.

## 8. Attacks / refutations attempted on this artifact

1. **"The row edit breaks the citation-drift table's own pin"** — REFUTED twice
   (independently by RV-8 §4.8). The table's only SKILL.md entries are
   `skill-registry-row` (an anchor on the sibling `interactive-r1-recovery` row,
   no `pin_line`) and `shonen-skill-range` (range 81-243, does not contain 371).
   Both re-simulated against the patched file: pass.
2. **"A single-cell rewrite changes the table's structure"** — REFUTED: the new
   row splits into 7 pieces = 5 cells like every other row; it is one line;
   file length unchanged.
3. **"`patch --dry-run` failed"** — investigated, not a patch defect: the first
   dry-run exited 2 with `patch: **** write error : Disk quota exceeded` from
   the host's per-user `/tmp` quota. Re-run with `TMPDIR=/dev/shm/ex20` → rc=0.
   The real apply + `cmp` byte-identity was already green before that.
4. **"v2 (skip-on-unpinned) is right because EX-21's prototype skips"** —
   REFUTED by EX-24's T3 (`findings=0 exit=0`, the guard silently off) and by
   RV-6 §4.7; PL-2 fail-closes. v3 follows the planner.
5. **"The row can promise more than the code"** — PARTIALLY TRUE and handled:
   the row is currently *ahead* of the code by two ids (RV-6 §4.8). This is the
   declared coupling; if EX-16 lands other tokens, the row must be corrected
   before it is applied. Unverified until EX-16 lands — EX-16 produced no
   artifact in this seat's window (polled: no `claims/c2/EX-16/` directory,
   gate file mtimes still 2026-10-18, `claims/c2/` holds EX-19/20/21/23/24/25,
   PL-2, RV-5..8, SC-4).
6. **"The pin chain is complete"** — REFUTED, residual recorded: `expected.json`
   carries no self-digest, so a same-privilege writer editing table + pin
   together re-silences the run (EX-24 T2 `findings=0 exit=0`; RV-6 §4.11). The
   row's "can never read as silent findings" must be read as "while the pin is
   in force". Out of scope for this row; not silently claimed away.

## 9. What this patch does NOT do

- It does not touch `expected.json`, the probe, or any gate file (EX-16 owns
  `.ufo/gates/citation-drift/`).
- It does not touch SCORECARD's capability row (SC-4/SC-5 own those patches).
- It does not claim the after-state: selftest 13/13, tampered/absent → exit 2,
  findings=0 at the work commit are EX-16's to measure.
