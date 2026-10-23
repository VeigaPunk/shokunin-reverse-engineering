# R31-C2 pre-data control — CtlC2DoNothing

Seat: critic (attack). Attack target: the C2 counter's resistance to a seat that commits no
receipt at all. Question: **can a do-nothing tree meet the frozen C2 target line
`requests=23 matches=23 target=23 entry_ok=1 skill_ok=1` with exit 0?**

**Verdict: holds. It cannot.** Every one of the 23 requests is rejected by the committed-record
gate (`c2-sqlite-refusals.py:236`, "committed envelope absent"), and both doc gates are false.
The counter exits 1.

**CONTROL CtlC2DoNothing: met=no score=0/23**

## 1. Control built

Sandbox clone (lane file `tools/round-31/c2-sqlite-refusals.py` at the freeze commit is the
instrument; the lane itself was only read):

```
D=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2DoNothing
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin $D/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $D/clone checkout -q -B ctl 35ba7c522dba55f9be27eb161d4254eacaa24330
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $D/clone -c user.name=ctl -c user.email=ctl@local commit -q --allow-empty -m "CtlC2DoNothing: empty control commit (no envelopes, no entry, no SKILL table)"
```

| fact | value |
|---|---|
| control commit | `8253ab559726be869d0b8f5e457fe6edabe48ee7` on branch `ctl` (2026-10-23 01:10:59 -0300) |
| parent / freeze | `35ba7c522dba55f9be27eb161d4254eacaa24330` |
| tree of HEAD | `0063d2b6c8ae3fc50047e1a8c3ff5772a72c0c9c` |
| content change | none: `git diff --numstat 35ba7c5 HEAD` → 0 lines, exit 0 (04:11:00Z) |
| `git status --porcelain` in clone | 0 lines before and after both counter runs (04:11:30Z) |
| `corpus/evidence/round-31/c2/` at HEAD | `predictions.tsv` only — no `envelopes/` directory |
| `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` | absent at HEAD |
| `grep -c inspect-sqlite-database clone/SKILL.md` | `0`; `grep -c S092 clone/SKILL.md` → `0` (04:10:29Z) |

Instrument identity in the clone equals the `instruments`/`frozen_inputs` pins in
`.ufo/waves/round-31/claims.json` (sha256sum, 04:10:28Z) — **[observation]**:

```
d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223  clone/tools/round-31/c2-sqlite-refusals.py
aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b  clone/tools/round-31/sqlite_oracle.py
acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8  clone/corpus/evidence/round-31/c2/predictions.tsv
46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211  clone/corpus/evidence/round-31/c1/carriers.tsv
6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51  clone/.ufo/waves/round-31/claims.json
```

REA pin honoured: `PKG_JSON` version check passed inside both counter runs (no `PIN package
version` line), and `timeout 120 npx -y rea-agents@6.5.0 --version` → `6.5.0` (04:10:24Z,
exit 0). No `PIN ...` line of any kind was printed by either run, so carrier/mutant integrity
at `/fast/scratch/hyaku/kaidoku-r31/{carriers,mutants}` is intact — nothing to escalate.

## 2. Counter run A — clone before the control commit

Exact command, run 2026-10-23T04:10:30Z → 2026-10-23T04:11:XX (see `run-pre.utc` 04:10:30Z /
04:10:49Z), **exit code 1**:

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2DoNothing && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2DoNothing/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2DoNothing/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

(stderr empty.) Full stdout:

```
q-rowlimit-no-table	P2-miss	committed envelope absent
q-columns-no-table	P2-miss	committed envelope absent
q-scope-no-table	P2-miss	committed envelope absent
q-missing-table	P2-miss	committed envelope absent
q-case-table	P2-miss	committed envelope absent
q-view-as-table	P2-miss	committed envelope absent
q-missing-column	P2-miss	committed envelope absent
q-virtual-rows	P2-miss	committed envelope absent
q-shadow-rows	P2-miss	committed envelope absent
q-ok-rows	P2-miss	committed envelope absent
m-missing	P2-miss	committed envelope absent
m-enotdir	P2-miss	committed envelope absent
m-not-sqlite	P2-miss	committed envelope absent
m-bad-pagesize	P2-miss	committed envelope absent
m-journal-hot	P2-miss	committed envelope absent
m-journal-short	P2-miss	committed envelope absent
m-journal-empty	P2-miss	committed envelope absent
m-journal-zero28	P2-miss	committed envelope absent
m-journal-symlink	P2-miss	committed envelope absent
m-db-symlink	P2-miss	committed envelope absent
m-directory	P2-miss	committed envelope absent
m-over-256mib	P2-miss	committed envelope absent
m-wal-over	P2-miss	committed envelope absent
requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)
```

## 3. Counter run B — control commit (`--rev HEAD`)

Exact command, run 2026-10-23T04:11:03Z → 2026-10-23T04:11:27Z, **exit code 1**:

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2DoNothing && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2DoNothing/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2DoNothing/clone --rev HEAD
```

(stderr empty.) Full stdout — byte-identical to run A (`sha256` of both files
`cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0`):

```
q-rowlimit-no-table	P2-miss	committed envelope absent
q-columns-no-table	P2-miss	committed envelope absent
q-scope-no-table	P2-miss	committed envelope absent
q-missing-table	P2-miss	committed envelope absent
q-case-table	P2-miss	committed envelope absent
q-view-as-table	P2-miss	committed envelope absent
q-missing-column	P2-miss	committed envelope absent
q-virtual-rows	P2-miss	committed envelope absent
q-shadow-rows	P2-miss	committed envelope absent
q-ok-rows	P2-miss	committed envelope absent
m-missing	P2-miss	committed envelope absent
m-enotdir	P2-miss	committed envelope absent
m-not-sqlite	P2-miss	committed envelope absent
m-bad-pagesize	P2-miss	committed envelope absent
m-journal-hot	P2-miss	committed envelope absent
m-journal-short	P2-miss	committed envelope absent
m-journal-empty	P2-miss	committed envelope absent
m-journal-zero28	P2-miss	committed envelope absent
m-journal-symlink	P2-miss	committed envelope absent
m-db-symlink	P2-miss	committed envelope absent
m-directory	P2-miss	committed envelope absent
m-over-256mib	P2-miss	committed envelope absent
m-wal-over	P2-miss	committed envelope absent
requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)
```

## 4. Which clause stops it (and the counterexample attempts that failed)

**[observation]** No clause let it through. The three independent stops:

1. `committed_check` (`:232`) — `show(root, rev, "corpus/evidence/round-31/c2/envelopes/<rid>.json")`
   is `None`, so `:236` returns `committed envelope absent`, 23/23. Reached only because the
   live half produced `LABEL`; the printed reason is the gate's, not the judge's.
2. `entry_ok` (`:251`) — `show(root, rev, ENTRY)` is `None` → `entry absent`.
3. `skill_ok` (`:260`) — no SKILL row per request id, and `inspect-sqlite-database` / `ENTRY`
   absent from SKILL.md.

`return 0 if matches == TARGET and e_ok and s_ok else 1` (`:363`) is therefore 1. The printed
target line is `requests=23 matches=0 target=23 entry_ok=0 (…) skill_ok=0 (…)`, which is not the
frozen line `requests=23 matches=23 target=23 entry_ok=1 skill_ok=1`.

Counterexamples I tried and why they fail — **[observation]** unless marked:

- *Put the receipts in the working tree, leave them uncommitted.* Every gate (`committed_check`,
  `entry_ok`, `skill_ok`) and the predictions identity check read through `show()`, i.e.
  `git -C root show rev:rel`; working-tree bytes are never consulted. The clone stayed
  `status --porcelain` empty and the counter wrote nothing (no `--write-evidence`), so run B
  proves the tree must be committed. **[inference from code + observation of the clean tree]**
- *Rely on the empty control commit to move `freeze_ct`.* `freeze_ct` comes from
  `git log rev --diff-filter=A -- .ufo/waves/round-31/claims.json` (`:305-307`), i.e. still the
  freeze commit `35ba7c52`; the empty commit changes neither it nor the tree sha
  (`0063d2b6…`, identical to the freeze tree).
- *Score a `--write-evidence` pass.* `:342` skips the receipt gate only when `write` is true, but
  the scored invocation is the one without the flag (both runs here). The L1's collection mode
  and the scored mode must stay distinct; nothing in this control lets the collection mode count
  as the measurement. **[inference]**
- *Benefit from a stale carrier/mutant pin silently.* Not available: `measure`'s PIN block would
  print `PIN … absent or altered` and return 2, and no such line appeared in either run.

**[observation, material for the family]** The live half of `judge()` already returned `LABEL`
for all 23 requests at the freeze — every line's reason is the receipt gate's, not a P2-miss.
So CtlC2DoNothing isolates the receipt and doc gates and exercises **zero** live-judge
discrimination; the discriminating power of `judge()` against the live CLI is only tested by the
all-false / no-reader / shortcut-keyed-on-ids controls. This is the intended split, not a defect:
a do-nothing tree is exactly the case where the live half should have nothing to say.

## 5. Impacted axes

- **depth (R31-C2)** — confirmed: the counter cannot be satisfied without committed receipts and
  both doc gates. No other axis is touched; no lane file, carrier, mutant or download byte was
  written (all reads; `chattr +i` paths only read).

## 6. Smallest safe correction

None. The counter rejects the do-nothing tree on three independent gates and exits 1; the frozen
target was not met and must not be re-scaled.

## 7. Artifacts (all under /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2DoNothing/)

| file | sha256 |
|---|---|
| `pre.stdout` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |
| `pre.stderr` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `pre.exit` (`EXIT=1`) | `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b` |
| `post.stdout` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |
| `post.stderr` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `post.exit` (`EXIT=1`) | `4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b` |
| `run-pre.utc` (04:10:30Z / 04:10:49Z) | `be1cfcd4cc4edfdc2796f326d2a1e91c23e82c5cd1d89d580b4acf37a3cd8a27` |
| `run-post.utc` (04:11:03Z / 04:11:27Z) | `4bab0339c460816b92bea3305863b626da08cbea5b3613d0ed97b864be0de38b` |
| `clone/` (git sandbox, branch `ctl`) | HEAD `8253ab559726be869d0b8f5e457fe6edabe48ee7`, tree `0063d2b6c8ae3fc50047e1a8c3ff5772a72c0c9c`, working tree clean |

## 8. Tooling and bounds

- Installs: **none**. `npx -y rea-agents@6.5.0` ran from the existing npx cache (0.8 s warm;
  version `6.5.0` at 04:10:24Z); no pacman, no `uv`/`cargo`/`npm -g`, no service touched.
- Lane bounds: read-only on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; no `git`/`jj` write
  anywhere in the lane or the fleet repo; the only lane write is this report. The clone's git
  commands ran with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset. Both counter runs are
  bounded by `timeout 900` and finished in 19 s and 24 s; no process left running. No agents
  spawned.
