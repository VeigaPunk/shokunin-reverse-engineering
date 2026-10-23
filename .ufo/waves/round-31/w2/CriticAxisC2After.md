# CriticAxisC2After — R31-C2 after data: depth ruling, discrimination re-check, predictor ceiling, pre-freeze observation

Reviewed: lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `c369242f`, freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`,
measured rev `0007731eec3a00c19808e6d522dc4e91e07e71b3`, lane tip `1288285eed81395e6af7c279a173b117b2c2eaa3`. Read-only on the lane.
No counter ran in this seat and no REA run was made on a carrier, mutant or request; REA was used only for `--help`, `--schema` and
`--llms-full`, which take no target file. No tool was installed or updated.

## Verdicts

| attacked item | verdict |
|---|---|
| depth-axis fit of R31-C2 after the data | **holds** (classification fit; the lane's depth *score proxy* is not moved — see §2) |
| discrimination re-check of the 23 rows | **holds** for the 23 tuples; **fails** for the frozen sentence "each pair on distinct code branches" (claims.json `limits`; entry line 55) — §3 |
| cheapest non-code predictor reaching ≥20/23 | **fails**: best honest score 7/23 (measured, §4). The committed "at most 3 of 23" is not a ceiling — same section |
| any row observable before the freeze | **none**; but the disclosed probe ran **three** times at scope `database`, not twice — §5 |
| frozen C2 acceptance predicate vs its counter | **wording defect**: C2 says "report equals the oracle", the counter compares the oracle-comparable subset (drops `engine.version` and `limitations`), which C1's predicate states and C2's does not — §6 |

## 1. Data state re-derived offline (no REA)

Producing command, exit 0, `2026-10-23T04:34:26Z` (`offline_check.out`):

```
TMPDIR=<seat>/tmp timeout 300 python3 -I -B offline_check.py
```

It applies the counter's `judge()` rule to the **committed** envelopes (refusal: exit/ok/code and exactly
`[{path, reason, message}]`; acceptance: subject sha = file sha, oracle-comparable report equality, or the `q-ok-rows`
row check). Full stdout ends:

```
requests=23 matches=23 target=23
```

Excerpt of the per-row lines (all 23 `P2-match`), refusal extras:

```
q-view-as-table	P2-match		{"category": "invalid_input", "operation": "inspect_sqlite_database"}
m-wal-over	P2-match		{"category": "invalid_input", "operation": "inspect_sqlite_database"}
q-ok-rows	P2-match		{}
```

The counter's own document gates were also re-run offline at the measured rev (its `entry_ok` / `skill_ok`, which read
only Git objects), exit 0, `2026-10-23T04:38Z`:

```
rows 23
entry_ok (True, 'ok')
skill_ok (True, 'ok')
```

The L1 receipt `.ufo/waves/round-31/after/c2-sqlite-refusals-at-0007731e.txt` (read, not re-run) ends
`requests=23 matches=23 target=23 entry_ok=1 (ok) skill_ok=1 (ok)` / `exit=0`. [observation]

## 2. Ruling: depth fit after the data

**Ruling: fit.** [observation + inference]

- The frozen row set is 20 refusals and 3 acceptances, and the committed envelopes reproduce every frozen tuple; the
  three acceptances are backed by the independent oracle (`offline_check.py` read the committed `m-journal-empty`,
  `m-journal-zero28` and `q-ok-rows` envelopes and re-derived `P2-match` from `sqlite_oracle.py`, host libsqlite3 3.54.0).
  The 20 refusal envelopes carry `error.category: invalid_input` and `details.operation: inspect_sqlite_database`.
- Depth, not coverage and not calibration, is the right classification: the artifact is branch-level behaviour of one
  operation (exact refusal code, argument path, reason and literal message, plus three edge acceptances), obtained by
  reading the shipped 6.5.0 JavaScript (S092) and tested live. The operation's happy path belongs to C1 and was already
  named in `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md`.
- **Qualification 1 (score):** the lane's depth row is the proxy "17/17 queue-drain rule blocks have resolvable
  file/range citations" over `SKILL.md:81-314` (`SCORECARD.md:24` at `c369242f`). The round-31 table sits at
  `SKILL.md:1008` and changes neither numerator nor denominator, so this claim adds no numeric depth score. The
  SCORECARD's "target met as measured" is consistent; a reader must not read "fit" as a score change.
- **Qualification 2 (what the depth delta is):** the pinned 6.5.0 guide and `--help` already state or imply the
  accept/refuse *outcome* for essentially every row (§6 sources; e.g. `sqlite-databases-6.5.0.md:66` "View,
  virtual-table and shadow-table row reads are unsupported", `:88` empty/fully-zeroed journals accepted, `:100`
  combined 256 MiB). They state none of the 20 refusal tuples. So the code-only increment is the signature
  (code, path, reason, literal message), not the outcome. That is still depth, but the honest description is
  "signatures predicted from code", not "behaviour predicted from code".

## 3. Discrimination re-check

Observation — statistics of the frozen rows (`trivial_predictor.py`-adjacent count, exit 0, `2026-10-23T04:39Z`):

```
refusals 20 distinct tuples 16 distinct messages 16
reasons Counter({'invalid_format': 13, 'invalid_value': 5, 'out_of_range': 2})
paths Counter({'["path"]': 11, '["table"]': 5, '["columns"]': 2, '["row_limit"]': 1, '["schema_scope"]': 1})
duplicate tuple groups: n=2 m-not-sqlite/m-bad-pagesize; n=2 m-journal-hot/m-journal-short;
n=2 m-db-symlink/m-directory; n=2 m-over-256mib/m-wal-over
```

**Holds.** The carriers really contain the selected objects, checked read-only with the host sqlite3
(`2026-10-23T04:32Z`, exit 0): `proj-371.db` `coordinate_operation_view` is `type=view` (and four more views);
`gpkg-curve.gpkg` `PRAGMA table_list` gives `rtree_curve_geometry` = `virtual`, `rtree_curve_geometry_node` = `shadow`;
`chinook.sqlite` has `Album` as a table and no lower-case `album`. So `q-view-as-table`, `q-virtual-rows`,
`q-shadow-rows`, `q-case-table` and `q-missing-column` address real objects and a real case variant. The 16 messages are
each either a literal template in `dist/` (14 of 16), a template with the node error code interpolated
(`m-enotdir`, `SqliteDatabaseFailures.js:78-85` builds `(${String(cause.code)})`), or SQLite's own errmsg
(`file is not a database`, `SqliteDatabaseWorker.js:24-33` passes `cause.message` for every non-memory,
non-output-limit errcode) — exactly the provenance the claims' `limits` disclose.

**Fails — "each pair on distinct code branches".** The frozen `limits` sentence (and the C2 entry line 55,
"The shared pairs sit on distinct code branches") is false for every shared group. Producing commands: `grep -n` on the
installed 6.5.0 package, exit 0, `2026-10-23T04:37Z`.

| group | one shared condition, not distinct branches |
|---|---|
| `m-db-symlink` + `m-directory` | one condition, `readStableArtifact.js:33` `if (!before.isFile() \|\| before.isSymbolicLink()) throw ... "Expected a regular file without a symlink: ${path}"` |
| `m-over-256mib` + `m-wal-over` | one comparison, `SqliteDatabaseSnapshot.js:119` `if (selectedSize > BigInt(SQLITE_DATABASE_LIMITS.inputBytes)) throw ... "exceed the combined ..."` |
| `m-journal-hot` + `m-journal-short` | one condition, `SqliteDatabaseSnapshot.js:77-79` `(bytesRead !== header.length \|\| header.some(...))` → one message |
| `m-not-sqlite` + `m-bad-pagesize` | one mapping, `SqliteDatabaseWorker.js:24-33` (any errcode except 7/18 → `format`); both frozen rows carry the identical pointer `SqliteDatabaseWorker.js:24-34` |
| `q-missing-table` + `q-case-table` | one site, `SqliteDatabaseInspection.js:187/189` (`metadata.get` miss → `missingSelectedTable`, definition line 74) |
| `q-view-as-table` | a second site, `SqliteDatabaseInspection.js:302-303` (`readRows`, `table === undefined`), same function and message |

So the 23 requests are 23 distinct *input conditions* over 16 distinct signature tuples, and fewer than 16 distinct
decision sites. Also, the wave-1 statement "for those 4 pairs the `code_pointer` column is the only branch discriminator"
(`w1/CriticAxisFitC2.md` §5) is false for at least three pairs, whose pointers coincide or overlap
(`m-not-sqlite`/`m-bad-pagesize` identical; both budget rows `Snapshot.js:117-119`; both regular-file rows
`readStableArtifact.js:30-33`).

Two limits of what the envelopes prove, for the record [observation + inference]:

- `q-view-as-table`'s live envelope is an error envelope with no `data` block, so it cannot show that the view row was
  *listed* before rows were refused. The row proves the outcome and the message reuse; the mechanism ("a view row sets no
  selectedTable") is code-read, not envelope-verified.
- `q-virtual-rows` / `q-shadow-rows` do discriminate the reported kind (`virtual` vs `shadow` appears verbatim in the
  message) even though both come from one site, `Inspection.js:307`.

This does not change the predicate, the target or the 23/23 result; it changes only how many independent branches the
table is evidence for.

## 4. Cheapest non-code predictor: measured ceiling 7/23

Sources allowed: the pinned 6.5.0 CLI surfaces (`--help`, `--schema`, `--llms-full`), the shipped README and skill
reference, `docs/sqlite-databases.md` at tag `rea-agents-6.5.0`, generic SQLite knowledge, and the lane's base tree
(round-30 patterns and committed `.ufo` artifacts). No `dist/` code read, no REA run. Producing command
`python3 -I -B trivial_predictor.py`, exit 0, `2026-10-23T04:39:28Z`:

```
tier A: 3/23  q-ok-rows,m-journal-empty,m-journal-zero28
tier B: 5/23  q-ok-rows,m-not-sqlite,m-bad-pagesize,m-journal-empty,m-journal-zero28
tier C: 7/23  q-ok-rows,m-not-sqlite,m-bad-pagesize,m-journal-empty,m-journal-zero28,m-db-symlink,m-directory
```

| tier | what it adds | rows |
|---|---|---|
| A "docs only" | pinned guide: ordinary-table row reads work; "Empty rollback journals and fully zeroed journal headers ... are accepted" (`sqlite-databases-6.5.0.md:88`); `--help` "requires table" (lines 10, 12) | 3 acceptances |
| B "+ SQLite errmsg" | SQLITE_NOTADB is "file is not a database" (host `sqlite3`); the `["path"]`/`invalid_format` shape is visible in the base tree for another verb | +2 malformed |
| C "+ base-tree transfer" | the exact tuple `invalid_request` / `["path"]` / `invalid_format` / "Expected a regular file without a symlink: {P}" is already at the base: `c369242f:.ufo/waves/arc3-loop1-round4/claims/c1/EX-07/legs/D3-symlink-hex-6.4.0.json:1` (and EX-09 lines 44-49 show the directory case) | +2 regular-file |

Why it stops at 7: the 16 distinct messages reduce to 13 distinct literal fragments; re-measured at `c369242f` with a
per-fragment `git grep -c -F` (exit 0 when a fragment has hits, 1 otherwise, 2026-10-23T04:41Z), **12 of the 13
fragments have 0 base hits**, and the one exception is the regular-file fragment (10 files / 14 lines) already in tier C.
The same fragments are absent from the published docs/help/schema/manifest. The option-dependency messages, the exact-name and
column messages, the virtual/shadow wording, the journal wording and the budget wording are code literals (or, for
`ENOTDIR`, a code template around the node error code); no non-code source yields them. Reaching 20/23 would require
essentially every refusal tuple.

**The recorded number is wrong.** `corpus/lessons/round-31.md` and the C2 entry both say "trivial predictors ... score
at most 3 of 23", and wave-1's own arithmetic ceiling was 5/23. The all-accept baseline *is* 3/23; it is not a ceiling.
The largest mistake wave-1 itself found (its §3 row "Expected a regular file without a symlink" — 14 base hits / 10
files; its §5 "2 are already in base .ufo artifacts") was left out of its own 5/23 arithmetic. Correct figures:
3/23 docs-only, 5/23 without base-tree transfer, **7/23 measured ceiling**. The ≥20/23 attack therefore fails, but by
more than the committed records claim.

## 5. Pre-freeze observation check

Timeline (observations; `jj` read-only with `--ignore-working-copy`, `git show -s`, and file mtimes in UTC):

| UTC | event | source |
|---|---|---|
| 03:30:44.6 | base commit `c369242f` point operation | `jj op log`: `2026-10-23 00:30:44.536 -03:00 point bookmark main to commit c369242fee...` |
| 03:55:52-03:56:30 | carrier downloads under `/fast/scratch/hyaku/kaidoku-r31/dl` | mtimes |
| 03:56:38-39 | `probe/p.db` written; `probe/out.json` written (TOON, `scope: database`, `evidence_id ev_47f6849…`) | mtimes; file read |
| 03:59:23 | 12 carriers extracted to `/fast/scratch/hyaku/kaidoku-r31/carriers` | mtimes |
| 03:59:53-54 | `probe/o1.json`, `probe/o2.json` (JSON, `scope: database`, meta durations 116ms / 107ms) | mtimes; file read |
| 04:01:47 | `corpus/evidence/round-31/c2/predictions.tsv` mtime | mtime |
| 04:04:03 | mutants built (the `--build` path, which runs no REA) | mtimes |
| 04:04:54 | `.ufo/waves/round-31/claims.json` mtime | mtime |
| 04:05:07.811-924 | **freeze commit created**: `commit e17b7a66…`, `point bookmark main to commit 35ba7c52…` | `jj op log` |
| 04:10:28 and 04:11:02 | wave-1 `CtlC1AllFalse` live REA refusal on its own nonexistent path (probe, then capture) | its report line 27 (command run at 04:10:28Z and again at 04:11:02Z); `seats/w1/CtlC1AllFalse/refusal.json` content read |
| 04:11:12-24 | wave-1 `CtlC1Placement` live REA on all 12 C1 carriers | its report's UTC table |
| 04:18:47 | control receipts commit `7474d269` | `jj op log` |
| 04:19:10-27 | 23 C2 runs, the committed data | `corpus/evidence/round-31/c2/runs.tsv` |
| 04:19:35 | data commit `f368a101` | `jj op log` |

- **No row was observable before the freeze.** The pre-freeze window [03:30Z, 04:05:07Z) holds 50 non-Git files under
  `/fast/scratch/hyaku/kaidoku-r31` (downloads, probe, carriers, mutants) and **no envelope**; the only REA outputs are
  the three probe artifacts. No predicted message string appears in `probe/o1.json` or `probe/out.json` (checked all 16
  prefixes, exit 0). The 23 requests were first run at 04:19:10Z, 14 minutes after the freeze commit was created.
  [observation]
- **Disclosure count understated.** `claims.json` `pre_freeze_probe` says REA ran on `probe/p.db` "twice at scope
  database". The artifacts show **three** scope-database invocations: `out.json` (03:56:39, TOON, `schema_scope:
  database`, same `evidence_id` as o1/o2) and `o1`/`o2` (03:59:53/54). The substantive assertions hold: only `p.db`, not
  a carrier; exit 0; the oracle's report equals REA's (re-derived here with `sqlite_oracle.py`, `True`); `o1` and `o2`
  differ only in `meta.duration`; `p.db` holds one table, one index, one view, one trigger and an rtree virtual table plus
  three shadow tables. [observation]
- **Conditions vs signatures.** The probe's own pre-freeze output states prose conditions for four rows — limitation 3
  "Views, triggers, and virtual/shadow table rows are not executed" (covers the view/virtual/shadow premise) and
  limitation 5 "combined input 256 MiB per inspection" (both budget rows) — and the pinned guide states the outcomes for
  the rest (§4). The signatures were not observable before the freeze. [observation]
- **Post-freeze, pre-data live runs.** `CtlC1AllFalse` ran a real REA refusal at 04:10:28Z (probe) and 04:11:02Z
  (capture) on `.../CtlC1AllFalse/nonexistent.sqlite`, yielding exactly the `m-missing` tuple (`invalid_request` /
  `["path"]` / `invalid_value` / "Selected SQLite database does not exist: …"). This is a different path from the frozen
  `m-missing` request and it is *after* the freeze, so it is not a freeze violation; but the data commit was not the
  first live observation of that branch, and `CtlC1Placement` likewise ran all 12 C1 carriers at 04:11:12-24Z. The C2
  entry's phrase "before any REA run on a request" holds only for the 23 frozen request paths, not for "the first live
  observation of every branch". [observation + inference]

## 6. Frozen predicate vs counter, and sources

**Wording defect (defect, not measurement hole).** The C2 predicate says an acceptance's "report equals the oracle". The
counter's acceptance path is `load_oracle().comparable(nr) != exp` (`c2-sqlite-refusals.py`, `judge`), and
`comparable()` pops `limitations` and `engine.version` (`sqlite_oracle.py:222-229`); the oracle cannot emit either
(its report keys are `artifact, wal, engine, database_encoding, schema, rows`, engine `{'name': 'SQLite'}`), and the
engine versions genuinely differ (REA reports SQLite 3.53.4; host libsqlite3 is 3.54.0). So the C2 text as frozen is
not literally satisfiable for the two journal acceptances, and the counter silently applies the exclusion that C1's
predicate states ("without engine.version and limitations") and C2's omits. The measurement is still sound because the
committed-envelope rule pins the live `limitations` text; only the description is off.

Sources opened (all 2026-10-23; primary/plain fetch only):

| source | access | sha256 of bytes read | located quote (≤25 words, line) |
|---|---|---|---|
| `https://raw.githubusercontent.com/morluto/rea/rea-agents-6.5.0/docs/sqlite-databases.md` (HTTP 200, 8,128 bytes) | 2026-10-23T04:30Z | `f7b0c57b03c2874059cfacabb0dd9bc0ee994f89694274eab89d2e9392736d16` | `:66` "View, virtual-table and shadow-table row reads are unsupported." |
| same | same | same | `:88` "Empty rollback journals and fully zeroed journal headers left by successful" |
| same | same | same | `:100` "The database and WAL together are limited to 256 MiB. SQLite values/records," |
| local installed pin `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/README.md` | 2026-10-23T04:30Z | `005e4c8acaa5a2a56f17bfac8f68b9fc9b3531bb370ed5f410154b65aa3ff124` | `:177` "Local database/WAL snapshot; Node.js 24.x >=24.15 or 26+ with native SQLite limits" |
| local installed pin `…/rea-agents/skills/reverse-engineer-anything/references/native-and-artifacts.md` | 2026-10-23T04:30Z | `1d2ac5f64feb5ad6ef8b98d803d570e1c48aa588281ff91a4bbf50d40f924450` | `:36-37` "Virtual tables, shadow tables and views are schema facts, not row-read targets." |
| `npx -y rea-agents@6.5.0 inspect-sqlite-database --help` (no target file) | 2026-10-23T04:30:42Z | `e8e63c5e259833f464f3adc76b028c3e1ffa3778cd3715ad1975278b18c3b87e` | `:12` "Positive safe integer row count; default 20; requires table" |

Tag observed: `git ls-remote --tags https://github.com/morluto/rea` prints
`3b79af28e80785afce9f5998d8f03289402a1847 refs/tags/rea-agents-6.5.0` (2026-10-23T04:31Z, exit 0).

## 7. Impacted axes and smallest safe correction

- **depth (primary): fit, score unchanged.** Correct the two annotations, not the claim: (1) replace the shared-pairs
  sentence with "shared *input conditions* on shared branches", naming the five groups and their single sites
  (`readStableArtifact.js:33`, `Snapshot.js:119`, `Snapshot.js:77-79`, `Worker.js:24-33`,
  `Inspection.js:187/189` vs `302-303`); (2) record that 23 requests yield 16 distinct signature tuples over fewer than
  16 decision sites. Append as a correction (M31-5 style); `claims.json` and `predictions.tsv` stay frozen.
- **depth records: the predictor ceiling is 7/23, not 3/23.** Fix the lesson sentence and the entry's repeat, with the
  three tiers and the base-tree receipt path for the regular-file pair; also correct wave-1 §5's "code_pointer is the
  only branch discriminator" if it is reused.
- **freeze disclosure: probe ran 3× at scope database.** Correct `pre_freeze_probe`'s "twice" to "three invocations
  (`out.json` TOON 03:56:39, `o1`/`o2` JSON 03:59:53/54)" in the entry/lesson; the probe's other assertions hold.
- **acceptance wording:** add one line to the C2 entry that its oracle comparison is on `engine.version`- and
  `limitations`-free fields (as C1's predicate states), because REA reports 3.53.4 and the oracle 3.54.0.
- **coverage / calibration:** untouched by this item. Context only: wave-1 controls ran live REA on the 12 C1 carriers
  at 04:11:12-24Z (before the C1 data commit 04:18:47Z), so the C1 data commit was not the first live run either; the
  C1 after-ruling belongs to another seat.

## 8. Artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/CriticAxisC2After/`)

| file | sha256 |
|---|---|
| `help.txt` (`--help` capture) | `e8e63c5e259833f464f3adc76b028c3e1ffa3778cd3715ad1975278b18c3b87e` |
| `schema.json` (`--schema`) | `0d69644e2d25d3b30a6584240438481135dceef4ac1e208e4885d14d1e74476b` |
| `llms-full.txt` (`--llms-full`) | `54c2fecd8ae358ffac3ffa98a8db74f77073feca067694f32c6c0c9f2c6a1061` |
| `sqlite-databases-6.5.0.md` (tag fetch) | `f7b0c57b03c2874059cfacabb0dd9bc0ee994f89694274eab89d2e9392736d16` |
| `offline_check.py` / `offline_check.out` | `b4844b8fa7e0ed16861aa95ab43abe79567b2d596b459d1d67cecaec6a7d370d` / `fcb77139f41d17029d4cf9bc5cb0c5068ca2d7e2fb230eef4bea327b52615e5c` |
| `trivial_predictor.py` / `trivial_predictor.out` | `509eb0b4402cb35310300e824e6e527d46387f2cef9e8ba6e714101d905f1310` / `9c35a250d8e32af945480f5e30dfaec310be96227d228cc75591b288b0f2240b` |

Nothing was written inside the lane except this report. No process started by this seat is still running.
