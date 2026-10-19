# CR-3 seat report — c2 critic: does the guard's preflight brick the probe on the lane's own frozen-run clause?

Wave arc3-loop1-round1, 2026-10-19. Seat CR-3 (critic, chain c2). Snapshot at write
time: HEAD `e845c2b`, gate dir untouched (`git status --short .ufo/gates/` ->
`?? .ufo/gates/__pycache__/` only, another seat's artifact; `.ufo/gates/citation-drift/`
mtimes 2026-10-18). EX-16 had **not** landed at write time (no `claims/c2/EX-16/`,
no `seats/EX-16.md`); PL-2, EX-19, EX-20, EX-21, EX-23, EX-24, EX-25, RV-5..RV-8,
SC-4 had. Read-only over the repo throughout; my only writes are this report and
`claims/c2/CR-3/*`. Scratch under `/var/tmp/cr3`.

## 1. Work performed

- Read the clause and its authority: `.ufo/gates/citation-drift/expected.json`
  `frozen_run` block (byte-identical at `265e1aa`, `045c1b8`, HEAD);
  `.ufo/waves/arc2-loop1-round10/CR2.md:13,:74` (the r10 restatement — "manual
  rerun at the pinned revision", and the stated cause: "no table digest is
  pinned — so the leg is not reproducible from committed artifacts");
  `SCORECARD.md:1297-1299`; `LOG.md:1369-1370`; `SCORECARD.md:925-926` (R6 debt).
- Read the actual code: `citation-drift-probe.py` in full, in particular that the
  table is read from the filesystem (`--table`, default `HERE/pointer-table.json`,
  :53) while `--rev` governs only *targets* (`git_show(root, rev, target)`, :122),
  and the verdict map's CNE tuple (:72-75).
- Read the chain's planned guard: `claims/c2/PL-2/frozen-run-guard.patch.md`
  (pin key `pointer_table.sha256`, table read on disk, fail-closed
  `pointer_table_unpinned`, verdict-map hunk, fixture re-pins) and
  `claims/c2/PL-2/plan.md:49`.
- Established the structural facts: the gate does not exist at the pinned revision
  (`git ls-tree 679af5d -- .ufo/gates/` -> empty; `git cat-file -e
  679af5d:.ufo/gates/citation-drift/pointer-table.json` -> "exists on disk, but not
  in '679af5d'"; gate first lands at `265e1aa`, 5 commits later).
- Enumerated the table's digest history: `edaa4e59` (265e1aa, 045c1b8; 13 entries)
  -> `bb564f13` (6bc4c29) -> `b34a1199` (dbae324) -> `36876734` (02c45d5) ->
  `38dc714e` (085ca3c) -> `738b3a56` (110cc08, HEAD) — six digests since landing.
- Built four guard variants on /tmp-class copies (`/var/tmp/cr3/probe-{A,B,C,D}.py`)
  and ran a 20-row matrix over the frozen replay, the faithful replay, stale-pin,
  unpinned-expected and the selftest. Raw output:
  `claims/c2/CR-3/matrix-evidence.txt`.
- Checked the claim's own premises: `absent table -> exit 2` **already holds** at
  HEAD (`--table /var/tmp/cr3/does-not-exist.json` -> `could-not-evaluate
  findings=1 exit=2`); both tables carry **zero** `@`-target entries (the frozen
  replay needs no `--snapshot-dir`); the `snapshots` pin `387e1f08…` is currently
  unreferenced.
- Proved the finding set is table-version dependent: `sc698-sc2-refuted-record`
  is pinned at `SCORECARD.md:698` in the r4-era table (passes at rev 679af5d) and
  at `:699` in the HEAD table (fails there) — that single line accounts for the
  r10 record's 6 findings vs today's 5 with the r4-era table.
- Reconcile with peers: EX-19 refutation #6 already observed the custom-`--table`
  break (`claims/c2/EX-19.md:84`); RV-8 T9 measured only the *admitted* reading
  (`seats/RV-8.md:83`); PL-2's design is fail-closed. My finding is the
  clause-level interaction, not a duplicate of those.

## 2. Proposed changes (patch text; none applied)

- `claims/c2/CR-3/guard-vs-frozen-run.patch.md` — makes the guard's third pin
  explicit in the frozen-run clause: `frozen_run` gains `table_sha256` (PL-2's
  value) **plus** `table_scope` (which replay reading is authoritative) and a
  re-measured `expected_findings`, and a `history[]` row carrying the r4-era table
  digest `edaa4e59…` so CR2's recorded 6-finding measurement keeps an input
  identity; the r4 E9 census-form pin is offered as the alternative. Also gives the
  corrected SKILL.md row wording (name it a *table-input* preflight; state the
  table is read from `--table` only; record the replay command verbatim) and one
  docstring sentence for the probe.
- No change to the guard's code, ids or CNE tuple is proposed: PL-2's patch
  already carries those, and my variant-D counter-example shows why they are
  load-bearing (without the verdict-map hunk a tampered table reads
  `reported findings=1 exit=0` — silent findings — and `failed exit=1` under
  `--strict`, never the declared exit 2).

## 3. Before→after measurement (chain claim: C2's guard, selftest 11→13, frozen-run leg)

Before (committed instrument, measured this session):
```
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD \
    --table .../pointer-table.json --expected .../expected.json --strict | tail -1
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
$ ... --selftest --expected .../expected.json | tail -1
CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0
$ ... --root . --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f --table .../pointer-table.json \
    --expected .../expected.json --strict | tail -1
CITATION_DRIFT_VERDICT: failed findings=16 exit=1        # admitted frozen replay reproduces
$ ... --root . --rev 679af5d… --table /var/tmp/cr3/old-table-265e1aa.json \
    --expected .../expected.json --strict | tail -1
CITATION_DRIFT_VERDICT: failed findings=5 exit=1         # faithful inputs, no guard
```
After (guard variants, same commands; full matrix in the evidence file):
```
variant A (PL-2 fail-closed)   rev-679af5d + current table   rc=1 failed findings=16   (leg intact)
                               rev-679af5d + r4-era table    rc=2 pointer_table_tampered   <- brick
                               HEAD + unpinned expected      rc=2 pointer_table_unpinned   <- brick
                               --selftest                    FAILED 2/11 (unless fixtures re-pinned)
variant B (inert when unpinned) same rows; selftest 11/11; r4-era table still rc=2 tampered
variant C (table at --rev)      rev-679af5d (either table)   rc=2 could-not-evaluate      <- permanent brick
stale pin (table edited, pin not re-committed): HEAD and rev-679af5d -> rc=2
```

**Verdict: the attack lands — the brick is real but design-conditional.** The
guard does not brick the *practiced* leg (current pinned table at the pinned
revision still yields the declared `failed`/exit 1). It does brick the leg under
the clause's **inputs reading**: the table the frozen verdict was actually
measured with (`edaa4e59…`) is now `pointer_table_tampered` exit 2, and every
pre-pin `expected.json` is `pointer_table_unpinned` exit 2. Because the gate
postdates the pinned revision by 5 commits, `revision: 679af5d` + `table_sha256:
738b3a56` describes a state that never existed, so the block cannot mean "the
frozen measurement's inputs" — yet nothing in the claim, the patch text or the
block says which reading is authoritative. Under the admitted reading the block's
`expected_findings: ["citation_dead"]` is already false (16 findings in 4 classes),
which is CR2's own recorded mismatch (`CR2.md:74`) left open by the pin: the pin
closes the *input* half of the R6 debt and leaves the *outcome* half — so the leg
is now "reproducible" only as a different measurement than the one recorded.

## 4. Attacks / refutations attempted, with verdicts

1. **"The guard cannot brick the frozen leg because the table is read on disk and
   the frozen replay uses the current table."** — PARTLY CONFIRMED (measured: A/B
   rows at current table, rc=1). Refuted as a full defence: the *faithful* replay
   (frozen-era table) and any pre-pin expected.json are refused (rc=2, measured);
   the block's inputs combination is impossible at the pinned revision (git
   evidence); so the guard defines a new leg, not the recorded one. **Verdict:
   brick reachable.**
2. **"The guard could resolve the table at `--rev` (the claim's 'absent table'
   class invites it)."** — CONFIRMED fatal: variant C, rc=2 at the pinned revision
   for both tables, permanently (no table exists there). **Verdict: brick, if that
   reading is ever adopted; the patch must say "`--table` path only".**
3. **"A 'pin required' guard breaks the selftest."** — CONFIRMED (variant A:
   2/11, because `citation-drift-probe.py:415` writes a fixture expected.json with
   no pin) and ALREADY HANDLED by PL-2's patch (fixtures re-pinned). **Verdict:
   closed by the plan, kept as a regression risk for any partial apply.**
4. **"The new finding id can be silent if the verdict map is not updated."** —
   CONFIRMED (variant D: tampered table -> `reported findings=1 exit=0` default,
   `failed exit=1` strict, never exit 2) and ALREADY HANDLED by PL-2
   (`patch.md:39-43`). **Verdict: closed by the plan; the claim's "never silent
   findings" sentence is only true because of that hunk.**
5. **"A stale pin (table edited, pin not re-committed) silently degrades the leg."**
   — CONFIRMED but fail-closed, not silent: rc=2 at HEAD and at the frozen rev.
   **Verdict: brick-by-maintenance, loud; the SKILL row's same-commit re-pin
   obligation is the mitigation and must be stated as load-bearing.**
6. **"The claim's selftest premise (absent table needs a new mechanism)."** —
   REFUTED: an absent table path already yields `could-not-evaluate exit=2` at
   HEAD (measured). Only the tampered case is new. **Verdict: the claim's
   falsifiable-before text overstates the before-state by one case.**
7. **"The frozen-run finding set mismatch is fixed by the pin."** — REFUTED: the
   pin does not touch `expected_findings`; measured 16 findings / 4 classes at the
   admitted replay vs the declared single class, and the `sc698` :698/:699 flip
   proves the set is table-version dependent. **Verdict: half-discharged debt;
   needs the block edit in the patch artifact.**
8. **"The snapshot pin matters for the frozen replay."** — REFUTED: neither table
   version carries an `@`-target entry; the replay needs no `--snapshot-dir` and
   the `387e1f08…` pin is currently unreferenced. **Verdict: no interaction.**

## 5. Blockers

- `/tmp` is quota-blocked this session: `echo hi > /tmp/cr3/t1.txt` ->
  "Disk quota exceeded", `dd` copied 0 bytes, `git show HEAD:SCORECARD.md >
  /tmp/...` -> rc=255 "unable to stream … to stdout" (tmpfs 16G, 13G used, 3.1G
  "available" but EDQUOT). Scratch moved to `/var/tmp/cr3`; nothing was written
  inside the repo. Recorded, not worked around silently.
- EX-16's real landing had not happened at write time, so every "after" number is
  from my variants and PL-2's patch text, not from the committed gate. If EX-16
  lands a design that differs from PL-2's (e.g. rev-resolved table, or a pin
  required with fixtures not re-pinned), rows 2/3 of §4 become live defects and
  the report's "closed by the plan" verdicts must be re-measured.
- Untracked `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` appeared at
  07:02:58 (another seat's import side effect, not mine) and was gone again by
  07:12 (`git status --short .ufo/gates/` now clean) — no action needed, recorded
  only for the record.
- Worktree dirty outside this wave (not mine, mtime 2026-10-18 23:01):
  `.ufo/waves/arc2-loop1-round10/C3.md` is modified (+184/-29) with an in-file
  "Revision note for the parent — land the working copy, not the committed one".
  Flagged so the parent does not mistake it for a wave defect.
