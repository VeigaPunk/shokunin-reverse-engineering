# CtlC2AllAccept — R31-C2 pre-data all-accept control

Seat: `KaidokuR31.CtlC2AllAccept` (critic, leaf). Round 31, wave 1. Freeze rev
`35ba7c522dba55f9be27eb161d4254eacaa24330` (committer time `1792728307` =
2026-10-23T04:05:07Z). Lane was read-only for this seat; every script, clone and
output lives under
`/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/`.

Attack: can a control that commits one live `ok` `inspect-sqlite-database`
envelope under every frozen C2 request id, plus a self-declared entry naming
every id and citing S092, plus a SKILL.md table built from
`predictions.tsv`, reach the frozen target line
`requests=23 matches=23 target=23 entry_ok=1 skill_ok=1` with exit 0?

## Verdict

`CONTROL CtlC2AllAccept: met=no score=0/23`

The counter rejected the control twice over: the committed-envelope clause
failed all 23 ids, and the live half also confirmed (in a diagnostic run) that
all 23 frozen predictions match, so no fabricated commit could have influenced
it. The only target-line fields the control satisfied were the two name-presence
doc gates (`entry_ok=1`, `skill_ok=1`); the binding `matches=23` failed at 0.
No counter clause let the control through.

## Control built (clone commit `561d2d7ab8b910b64575f7f9aa09d4f8e703cf77`, 2026-10-23T04:11:54Z)

Sandbox clone: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/clone`,
branch `ctl`, started at the freeze commit per the Contract, then:

- **One live source envelope** — exactly one run, as assigned
  (2026-10-23T04:11:09Z → 04:11:10Z, exit 0, stderr empty):
  `TMPDIR=…/CtlC2AllAccept/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite --format json --full-output`
  stdout 6,708 bytes, sha256
  `f418a26ba0c2e91a5ea0d9fddd1f901c1d0e86d20d30a15982498c051679b3d3`;
  `ok=true`, `operation=inspect_sqlite_database`, scope `inventory`, `rows=null`.
- **23 committed envelopes** — `corpus/evidence/round-31/c2/envelopes/<id>.json`
  for every frozen id, each a byte copy of that single stdout (all sha256
  `f418a26ba0c2e91a5ea0d9fddd1f901c1d0e86d20d30a15982498c051679b3d3`).
- **Junk-row entry** — `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md`,
  sha256 `58b945a70b6bd39dbc86884432ce346d037cac8c94e6c2d37e7bc195fc67f0ad`;
  cites `S092`, names all 23 ids (`entry missing: []` when checked against
  `predictions.tsv`), and states in its own text that it is a control and that
  no envelope is the envelope of the request it is filed under.
- **SKILL table** — appended section
  `## inspect-sqlite-database refusal and edge table — round 31 (w1 control)` to
  `SKILL.md`, one `| \`id\` | code | message prefix |` row per prediction; final
  `SKILL.md` sha256
  `3b311621d6c355dcd93e7e05ed7482e0940db7def2ae796a92deb932ac2b62c6`
  (`skill missing: []` against all 23 ids).
- Generator: `build_control.py`, sha256
  `1492f98c4370250f3c2b92d0b1848827ca0d9cae8947cfef8d9ac7718fe46f0b`.
- Commit stat: 24 files added (23 envelopes + entry) and `SKILL.md` modified
  (+34 lines) — 25 paths in all; commit `561d2d7a…`, committer time
  2026-10-23T04:11:54Z > freeze time 04:05:07Z (`first_added` gate is satisfied
  for every id, yet no committed envelope passed).

## Counter run 1 — before the control commit (comparison)

Exact command (2026-10-23T04:10:42Z → 04:11:03Z, wall 21 s):

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept && TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/tmp timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Exit code: **1**. Full stdout:

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

Observation: every one of the 23 rows reached `committed_check` (the reason is
the committed clause, not the live judge), i.e. the live half matched all 23
frozen predictions already at the freeze commit. The miss at this revision is
purely the missing committed records and doc gates.

## Counter run 2 — against the all-accept control

Exact command (2026-10-23T04:11:57Z → 04:12:19Z, wall 22 s):

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept && TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/tmp timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/clone --rev HEAD
```

Exit code: **1**. Full stdout:

```
q-rowlimit-no-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-columns-no-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-scope-no-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-missing-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-case-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-view-as-table	P2-miss	committed envelope differs from the live envelope (full comparison)
q-missing-column	P2-miss	committed envelope differs from the live envelope (full comparison)
q-virtual-rows	P2-miss	committed envelope differs from the live envelope (full comparison)
q-shadow-rows	P2-miss	committed envelope differs from the live envelope (full comparison)
q-ok-rows	P2-miss	committed envelope differs from the live envelope (full comparison)
m-missing	P2-miss	committed envelope differs from the live envelope (full comparison)
m-enotdir	P2-miss	committed envelope differs from the live envelope (full comparison)
m-not-sqlite	P2-miss	committed envelope differs from the live envelope (full comparison)
m-bad-pagesize	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-hot	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-short	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-empty	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-zero28	P2-miss	committed envelope differs from the live envelope (full comparison)
m-journal-symlink	P2-miss	committed envelope differs from the live envelope (full comparison)
m-db-symlink	P2-miss	committed envelope differs from the live envelope (full comparison)
m-directory	P2-miss	committed envelope differs from the live envelope (full comparison)
m-over-256mib	P2-miss	committed envelope differs from the live envelope (full comparison)
m-wal-over	P2-miss	committed envelope differs from the live envelope (full comparison)
requests=23 matches=0 target=23 entry_ok=1 (ok) skill_ok=1 (ok)
```

Target-line check: `requests=23 matches=0 target=23 entry_ok=1 skill_ok=1`,
exit 1 — **not** the frozen target. `met=no score=0/23`.

## Which clause held, and what a single-envelope control can ever score

Observation, from the run-2 stdout and the counter source
(`tools/round-31/c2-sqlite-refusals.py:143-160` `strip_meta`/`judge`,
`:232-249` `committed_check` — the full-envelope compare is line 244 — and
`:342-347`, where `committed_check` runs only for a live `P2-match`):

1. The live judge is upstream of the committed check and never reads committed
   text (`judge()` then, only for a `P2-match`, `committed_check()`). A fake
   commit cannot turn a refusal into a match, nor a match into a refusal.
2. `committed_check` compares `strip_meta(committed) != strip_meta(live)` —
   every field but top-level `meta` (the M30-3 repair). The shared `ok=true`
   envelope therefore failed the 20 refusal ids immediately (`ok: true` vs
   `ok: false`, `data`/`error` sides swapped), and failed the 3 acceptance ids
   on content. Measured diffs of the stored envelope against the live envelope
   of each acceptance id (probe clone `clone2`, live envelopes from
   `--write-evidence`):
   - `q-ok-rows`: 7 differing field paths — `data.evidence_id`,
     `data.parameters.table` / `.row_limit` (missing in the stored envelope),
     `data.normalized_result.rows` (`null` vs the 3-row Album block),
     `data.normalized_result.schema.scope` (`inventory` vs `selected_table`),
     tables 11 vs 1, indexes 11 vs 1.
   - `m-journal-empty`: 52 differing paths — 1 `data.evidence_id`; 3 path
     identity fields (`data.locations.0.path`,
     `data.normalized_result.artifact.path`, `data.parameters.path`); 2 subject
     fields (`data.subject.name`, `data.subject.local_path`); the schema scope
     (`inventory` vs `database`); 11 index `sql` fields present only in the live
     envelope; and 33 table-side fields (11 × `sql` present only live, 11 ×
     `columns` length 0 vs N, 11 × `columns_completeness`), plus
     `data.parameters.schema_scope`. `subject.digest.sha256` is equal (the
     mutant db is a byte copy of chinook), which is exactly why the full-envelope
     rule must carry the path fields.
   - `m-journal-zero28`: the same 52 differing paths (identical path set to
     `m-journal-empty`).
3. Structural bound [inference from the same source plus those diffs]: a
   control that files **one** envelope under every id can match at most the one
   request whose live envelope equals it modulo `meta`. All 23 request paths are
   distinct, and `data.parameters.path` / `data.locations` / `artifact.path`
   carry the path into the compared region, so the ceiling is ≤ 1/23; with this
   particular default-`inventory` `chinook.sqlite` envelope the ceiling is
   0/23, because the only chinook request (`q-ok-rows`) runs with
   `--table Album --row-limit 3`.

The only clauses the control did satisfy are the doc gates
`entry_ok` (`ENTRY` exists and contains `S092`) and `skill_ok` (a table row per
id with its code and message prefix, plus the verb and entry path in the file).
Those are name-presence gates by design; the frozen kill rule requires the whole
target line including `matches=23`, so a junk row cannot verify C2. This is the
junk-row control's result (entry + SKILL rows without data), not a C2 loophole.

## The rejecting clause is satisfiable by honest data (control legitimacy)

Two independent `--write-evidence` runs of the same counter, each in its own
clone at the freeze tree (2026-10-23T04:12:55Z→04:13:23Z and
04:14:00Z→04:14:21Z, both exit 1 only because entry/skill are absent in that
tree), printed `requests=23 matches=23 target=23` for the live half and wrote
live envelopes; comparing the two sets modulo `meta` gives **23/23 identical**
(including `data.evidence_id`; e.g. `m-journal-empty` both times
`ev_0ab137e3b8e59bb99203c9750cf05e3fa763733d6032b5b93020b17175cba2f4`).
So the full-envelope rule that rejected the control can be met by genuine
per-request runs; the rejection is meaningful, not an unsatisfiable gate. These
probe clones are scratch diagnostics, not claim data; they were never committed
anywhere, and the lane's `corpus/evidence/round-31/c2/envelopes/` remains absent.

## Impacted axes and correction

- Impacted axis: `depth` (R31-C2). Coverage (`R31-C1`) is untouched by this
  seat: no C1 carrier was run or written.
- Smallest safe correction: **none to the counter**. The control is rejected at
  `matches=0/23` with exit 1; the frozen instruments must not be amended. The
  L1 may cite this receipt as the all-accept pre-data control: the target line's
  doc gates are satisfiable without data, the match clause is not.

## Evidence hygiene

- No write of any kind to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
  except this report. No git/jj write in the lane or the fleet repo; all git
  operations ran in the three scratch clones with `GIT_DIR`, `GIT_WORK_TREE`
  and `GIT_INDEX_FILE` unset.
- No carrier, mutant or `dl` file was modified; they were read only. The
  counter's pin checks passed on every run (no `PIN … absent or altered`
  line), and `--build` was never invoked.
- Every REA invocation and every counter invocation was wrapped in `timeout`
  (REA 300 s, counters 900 s; wall times 1 s / 21 s / 22 s / 28 s / 22 s).
  Local git setup, commit, hash and diff commands were short-lived shell calls.
  No process tree started by this seat remains (all five counter/REA calls
  returned; the `npm exec … chinook-autoinc.sqlite` and `CriticSeparability`
  counter processes visible at 04:13-04:15Z belong to other seats and were left
  untouched).
- No tool was installed or updated (npx used the already-pinned cache
  `rea-agents@6.5.0`, `package.json` sha256
  `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`,
  matching `claims.json`).
- Frozen instrument hashes at the clone: counter `d2394895…e28223`, oracle
  `aefd8639…41dc6b`, `predictions.tsv` `acac45e3…0262f8`, `carriers.tsv`
  `46f180b8…c19211` — all equal to `claims.json`.

Labels: the run outputs, hashes, exit codes and diff paths above are
**observation**; the ≤1/23 structural ceiling is **inference** from the counter
source and those diffs; what the real L1 run will print is **unknown** (no
per-request envelope exists yet in the lane).

## Artifacts and sha256 (all under /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2AllAccept/)

| path | sha256 | what |
|---|---|---|
| `build_control.py` | `1492f98c4370250f3c2b92d0b1848827ca0d9cae8947cfef8d9ac7718fe46f0b` | builds envelopes, entry, SKILL table |
| `out/chinook.json` | `f418a26ba0c2e91a5ea0d9fddd1f901c1d0e86d20d30a15982498c051679b3d3` | the one live envelope, copied 23× |
| `out/chinook.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty |
| `out/rea.run.txt` | `2c1b91e8dda016961c789dee17b7aa16af2282ecd2c4d37389d91d74265cd64c` | REA command, times, exit 0 |
| `out/pre.run.txt` | `4e8e8b0bde9a86d0cdf2bfdfdd213aaa4b94b7f3401231a3ff1ea7e09fd2c05b` | pre-control command, times, exit 1 |
| `out/pre.stdout.txt` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` | full pre-control stdout |
| `out/pre.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty |
| `out/build.txt` | `a4237f4016767427a5072c0c5884b87dcb5d6d9f68d2282fef5ec3a52ed4c01e` | hashes printed by the generator |
| `out/commit.txt` | `ceb554be911f0a48cce7b3286537c6fa39a0a2b92c00067cb72b543a940b4263` | control commit id and time |
| `out/post.run.txt` | `1fa93a39d3201c28869537f9a81dacce294c7ae87c20d543bd04940f5e39fb34` | control command, times, exit 1 |
| `out/post.stdout.txt` | `7b1be42a1d13d409178cca7b6fda6db9aac319de14611686354cb12acab011c5` | full control stdout |
| `out/post.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty |
| `out/livehalf.run.txt` | `6456e6e9130e7b7d95f96107373f208cad55f253db28f3ca6f0c0d2c77c4f414` | probe 1 command/times, exit 1 |
| `out/livehalf.stdout.txt` | `75e82a4923730ecb39ffb4586d9858957c6d575e45d08e2c2a2c3afd90dae9fa` | probe 1 stdout (live half 23/23) |
| `out/livehalf.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty |
| `out/livehalf2.run.txt` | `16686fbc4a213ebe230b1dbb74c428ba2c6142acde9530c77226cf33ca9eab88` | probe 2 command/times, exit 1 |
| `out/livehalf2.stdout.txt` | `75e82a4923730ecb39ffb4586d9858957c6d575e45d08e2c2a2c3afd90dae9fa` | probe 2 stdout (identical bytes to probe 1) |
| `out/livehalf2.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty |
| `clone/corpus/evidence/round-31/c2/envelopes/*.json` | `f418a26b…79b3d3` ×23 | all-accept control envelopes |
| `clone/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` | `58b945a70b6bd39dbc86884432ce346d037cac8c94e6c2d37e7bc195fc67f0ad` | junk-row entry (control) |
| `clone/SKILL.md` | `3b311621d6c355dcd93e7e05ed7482e0940db7def2ae796a92deb932ac2b62c6` | control table appended |
| `clone` (worktree) | HEAD `561d2d7ab8b910b64575f7f9aa09d4f8e703cf77` | control clone, branch `ctl` |
| `clone2` (worktree) | HEAD `35ba7c522dba55f9be27eb161d4254eacaa24330` | probe-1 clone; live envelopes, e.g. `m-journal-empty` `80eeab42ed9b085886645a9b86a8d2ca4d9750050aab821584427efad27ccd96`, `q-ok-rows` `fce739a65e6b1079b22a417e198ee8e959f82f433576d6958a19c9caed4b8c1d` |
| `clone3` (worktree) | HEAD `35ba7c522dba55f9be27eb161d4254eacaa24330` | probe-2 clone; envelopes identical to probe 1 modulo `meta` |
