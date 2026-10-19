# EX-18 — absent-table injection results (chain c2, arc3-loop1-round1)

Seat: EX-18, role executor, chain c2. Task: absent-table injection — delete
`pointer-table.json` in a /tmp copy and run (expect the declared exit-2); also a
DIRECTORY in its place; also a symlink to a stale copy.

Instrument under test (real target, READ-ONLY this seat):

| file | sha256 at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab` |
| --- | --- |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f` |
| `.ufo/gates/citation-drift/expected.json` | `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33` |
| `.ufo/gates/citation-drift/pointer-table.json` | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` |

Same three sha256 re-read after the matrix: unchanged. No write landed on the
real gate dir (EX-16 owns that target); every mutated table is a scratch copy.

## 0. Scratch-location deviation (recorded, not silent)

`/tmp` is a 16G tmpfs mounted `usrquota` (`findmnt /tmp` →
`rw,nosuid,nodev,nr_inodes=1048576,inode64,huge=advise,usrquota`) whose user
quota is exhausted by other wave seats (13G used; `du -sh /tmp/d23` = 2.2G).
Every write this seat attempted there failed with `EDQUOT`:

```
cp: error writing '/tmp/ex18-absent/gate/citation-drift-probe.py': Disk quota exceeded
$ printf 'x' > /tmp/ex18-tiny-test
bash: printf: write error: Disk quota exceeded
```

Scratch therefore lives in `/dev/shm/ex18-absent` (also a tmpfs, 9.9G free at
run time) — same disposable-temp role, different mount. SC-4 and RV-6 hit the
same wall independently (`claims/c2/SC-4/verify-changeset.sh:5` comment:
"TMPDIR is redirected here because /tmp hit the user quota this wave").
Nothing in the repo is used as scratch.

## 1. What "declared exit-2" means here (the class being tested)

* `citation-drift-probe.py:34` — "VERDICT exit 0 clean, 1 failed, 2 could-not-evaluate".
* `citation-drift-probe.py:72-75` — the CNE id set includes `pointer_table_unreadable`.
* `citation-drift-probe.py:280-284` — the table is loaded with
  `json.load(open(table_path))`; the only guard is the `(OSError, ValueError)`
  catch. **No digest of the table is read or verified anywhere in the probe.**
* `expected.json` pins snapshots (`"snapshots": {"config-toml-landmarks": …}`)
  but carries **no** digest for `pointer-table.json`; the current table has zero
  snapshot targets, so the snapshot-pin machinery never runs for it
  (`snapshots` key is the only pin field).
* `SKILL.md:371` (registry row) — "probe semantics: 0 reported … and 2
  could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2
  could-not-evaluate".
* `expected.json` selftest case `table_unreadable` → `exit_code: 2`,
  `finding: pointer_table_unreadable` (the malformed-JSON variant of the class).

## 2. Matrix — 8 injection shapes, both semantics

Harness: `scripts/matrix-run.sh` (generic runner, `PROBE/EXP/TBL/OUTDIR/LABEL`
env). The mutated artifact is always the table path; `--root` stays the real
repo and the probe only ever runs `git show`/`rev-parse` against it (read-only).
Each shape is run twice: default probe semantics and `--strict` gate semantics.
Raw logs: `logs/matrix-before.log` (pristine probe + unpinned expected),
`logs/matrix-candidate.log` (candidate guard), per-case files in `logs/`.

"stale copy" = the round-4-era table from git history
(`git show 265e1aa:.ufo/gates/citation-drift/pointer-table.json`, 13 entries /
6918 bytes vs HEAD's 31 entries / 14694 bytes), sha256
`edaa4e59c804bc0fd424c68daafa38a1bdef5fb395b3c10b3d61e614f5bef641`.

| # | shape (object at the table path) | BEFORE probe/gate exit | class reached | AFTER (candidate) probe/gate exit |
| --- | --- | --- | --- | --- |
| R0 | pristine file, 14694 B | 0 / 0 | clean, findings=0 | 0 / 0 |
| R1 | **absent** (deleted) | **2 / 2** | CNE `pointer_table_unreadable` `[Errno 2]` | 2 / 2 |
| R2 | **directory** (`mkdir`) | **2 / 2** | CNE `pointer_table_unreadable` `[Errno 21] Is a directory` | 2 / 2 |
| R3 | **symlink → stale round-4 copy** | **0 / 1** | `reported findings=2` / `failed findings=2` | **2 / 2** |
| R4 | symlink → nonexistent target (dangling) | 2 / 2 | CNE `[Errno 2]` | 2 / 2 |
| R5 | symlink → the live pinned table (control) | 0 / 0 | clean, findings=0 | 0 / 0 |
| R6 | current table, one needle altered in place | 0 / 1 | `reported findings=1` / `failed` | **2 / 2** |
| R7 | current table, last 5 entries dropped | **0 / 0** | `clean findings=0` | **2 / 2** |
| R8 | round-4 table with a needle altered (bonus) | 0 / 1 | `reported findings=3` / `failed` | (same class as R6) |

Selftest: pristine `cases=11 passed=11 failed=0 exit=0`; candidate
`cases=13 passed=13 failed=0 exit=0` (`logs/` — see the candidate artifact).

## 3. Verdicts on the three shapes this seat was sent to test

1. **Absent table (R1): CONFIRMED.** Deleting `pointer-table.json` reaches the
   declared preflight could-not-evaluate class, exit 2, in both semantics, with
   the declared id `pointer_table_unreadable` and the OS cause in the detail
   (`[Errno 2] No such file or directory`). Log: `logs/R1-absent.probe.txt`.
2. **Directory in its place (R2): CONFIRMED.** `IsADirectoryError` is an
   `OSError` subclass, so the same catch and the same exit-2 class hold;
   detail reads `[Errno 21] Is a directory`. Log: `logs/R2-directory.probe.txt`.
   (A directory is the shape a `mkdir -p $(dirname $TABLE)` slip leaves behind,
   so the guard holding here is load-bearing.)
3. **Symlink to a stale copy (R3): REFUTED at HEAD.** The stale table is
   *readable*, so the probe silently evaluates the stale contract as if it were
   the pinned one: probe exit 0 ("reported", 2 findings), `--strict` exit 1
   ("failed"). Neither is the declared exit-2 class; worse, the two findings
   (`citation_dead entry=sc698-sc2-refuted-record`, `record_word_missing
   entry=log1005-quoted-claim`) are artifacts of the *stale table*, not of the
   tree — a reader cannot tell them apart from genuine drift.
   Log: `logs/R3-symlink-stale.probe.txt` / `.gate.txt`.

R7 (bonus, strongest): a table with the last 5 entries dropped evaluates to
**exit 0 clean** at HEAD — the gate prints `CITATION_DRIFT_VERDICT: clean
findings=0` while the contract has silently lost 5 pins. That is the exact
failure the c2 claim names ("never silent findings") and it is reachable with a
single `json.dump` edit, no path trickery.

## 4. After-state proof (scratch candidate, NOT the landed artifact)

To show the declared property is reachable (not merely demanded), this seat
built a candidate guard in scratch: pin `sha256` of the table bytes in
`expected.json` (`"pointer_table": {"sha256": …}`) and verify it in `run_check`
before evaluating any entry; mismatch/absent pin → `pointer_table_unreadable`
→ CNE. Patch text: `candidate-guard.patch.md` / `candidate-guard.diff`
(proposal for EX-16; **not applied to the real target**).

Result with the candidate: every attack shape R1–R4, R6–R7 lands in exit 2
(`table sha256 … != pinned …`), while both controls stay clean — R0 baseline
and **R5 (symlink → live table) exit 0, findings=0**. That last one is the
constraint EX-16's patch must not break: the digest is over table *content*, so
an identical-content symlink stays green, while stale/tampered/shrunk content
reddens regardless of how the path resolves.

Selftest under the candidate: 13/13 exit 0 — the two new cases are
`absent_table` (table path never created) and `tampered_table` (digest pinned
before the needle is altered), both exit 2 / `pointer_table_unreadable`, matching
the claim's "selftest 11 → 13 cases".

## 5. Attacks/refutations attempted, with verdicts

| attack | verdict |
| --- | --- |
| delete table (R1) | guard holds — declared exit 2 |
| directory at the table path (R2) | guard holds — declared exit 2 |
| dangling symlink (R4) | guard holds — declared exit 2 |
| symlink → stale copy (R3) | **guard fails at HEAD** (0/1, silent findings); fixed by the landed guard (§7) |
| symlink → live table (R5) | must stay clean; green before, under the candidate and under the landed guard |
| needle tamper in place (R6) | **guard fails at HEAD** (0/1); fixed by the landed guard (§7) |
| shrink table −5 entries (R7) | **guard fails worst at HEAD** (0/0 clean); fixed by the landed guard (§7) |
| malformed JSON (pre-existing case) | holds at HEAD (exit 2) — not re-run here, covered by selftest `table_unreadable` |
| `--expected` with no pin (R9) | new shape the guard introduces; verified fail-closed — exit 2 `pointer_table_unpinned` (§7) |

## 6. Gaps / handoff notes

* EX-16 landed mid-wave (gate dir mtimes 07:15; probe sha `e2665074a685…`,
  expected.json `ff47bfd60b38…`). The "after" column of §2 is this seat's
  scratch-candidate measurement taken before that landing; §7 re-measures the
  same matrix against the landed artifact, which is the column that counts.
* Peer cross-check: EX-25 independently measured absent-table → exit 2 and
  tampered-needle → exit 0 "reported", and probed `expected.json` for a table
  digest with the result `NO-PIN`
  (`claims/c2/EX-25/logs/before-{absent-table,tampered-table,digest-check}.txt`).
  Consistent with this matrix; EX-18 adds the directory, symlink-stale,
  symlink-dangling, symlink-live-control and shrunk-table shapes.
* `--root` was kept on the real repo for fidelity (read-only). If a reviewer
  wants a fully isolated tree, the harness accepts any `REPO` with a git dir.
