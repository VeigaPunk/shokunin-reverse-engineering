# ProbePin670 — live check: at rea-agents@6.7.0 does the 256 MiB budget refusal become `resource_constraint`?

Seat: KaidokuR31.ProbePin670 (wave 2, falsify). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin, read-only.
Attacks: R31-C2's **Pin drift** paragraph, `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md:50` (and its
one-line echo in `SKILL.md:1038`), whose source is wave-1 `ScoutPinDrift.md`.

## Verdict

**Holds on its main claim; one sentence is overstated.** Live 6.7.0 runs of `m-over-256mib`, `m-wal-over` and
`m-journal-hot` confirm the budget refusal becomes `resource_constraint` / `file-size` at 6.7.0 and that both
budget rows' committed 6.5.0 envelopes would not match; `m-journal-hot` is byte-identical outside
`meta.duration`. The sentence "The other 21 rows' code paths are unchanged" is literally false (4 of the 21
rows' source files did change, and only 1 of the 21 was run live); "their outcomes are unchanged" is what the
static analysis supports. "The journal check also moves after the budget check" is correct in source but
**could-not-evaluate live**: no frozen mutant is both over-budget and journal-hot, and this item forbids any
other REA command (no synthetic dual mutant was run).

## Commands (2026-10-23, UTC; three runs launched concurrently, first shell timestamp 04:30:01Z)

```
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w2/ProbePin670/tmp timeout 300 npx -y rea-agents@6.7.0 \
  inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-over-256mib/db.sqlite --format json --full-output
TMPDIR=… npx -y rea-agents@6.7.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-wal-over/db.sqlite --format json --full-output
TMPDIR=… npx -y rea-agents@6.7.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-hot/db.sqlite --format json --full-output
```

Exit code **1** for each of the three; stdout JSON sha256s below; stderr empty (0 bytes) for all three.
Mutants were opened read-only; `stat` at run time: `m-over-256mib/db.sqlite` 268435457 B,
`m-wal-over/db.sqlite` 1067008 B + `db.sqlite-wal` 267368449 B (= 268435457), `m-journal-hot/db.sqlite`
1067008 B + `db.sqlite-journal` 28 B.

## 6.7.0 envelopes

### m-over-256mib (observation, full, `jq -S`; `meta.duration` = "4ms")

```json
{"ok":false,"error":{"code":"resource_constraint","category":"resource_constraint",
 "message":"Selected SQLite database and WAL total 268435457 bytes, exceeding the combined 268435456-byte offline snapshot budget: /fast/scratch/hyaku/kaidoku-r31/mutants/m-over-256mib/db.sqlite",
 "retryable":false,
 "remediation":{"action":"Use the application's supported export workflow to create a consistent, smaller offline SQLite snapshot containing only the relevant data, then inspect that snapshot. REA will not truncate or modify the selected source."},
 "details":{"operation":"inspect_sqlite_database","resource":"file-size",
  "reason":"Selected SQLite database and WAL total 268435457 bytes, exceeding the combined 268435456-byte offline snapshot budget: /fast/scratch/hyaku/kaidoku-r31/mutants/m-over-256mib/db.sqlite",
  "reported_limits":{"observed_sqlite_snapshot_input_bytes":"268435457","sqlite_snapshot_input_bytes":268435456}}},
 "meta":{"command":"inspect-sqlite-database","duration":"4ms"}}
```

### m-wal-over (observation, identical field-for-field except the path; `duration` = "4ms")

```json
"message":"Selected SQLite database and WAL total 268435457 bytes, exceeding the combined 268435456-byte offline snapshot budget: /fast/scratch/hyaku/kaidoku-r31/mutants/m-wal-over/db.sqlite"
"code":"resource_constraint","category":"resource_constraint","retryable":false,
"details":{"operation":"inspect_sqlite_database","resource":"file-size",
 "reported_limits":{"observed_sqlite_snapshot_input_bytes":"268435457","sqlite_snapshot_input_bytes":268435456}}
```
The WAL is counted from `lstat` size (1,067,008 + 267,368,449 = 268,435,457), so the sparse `-wal` still
trips the budget, as at 6.5.0.

### m-journal-hot (observation, full; `duration` = "4ms")

```json
{"ok":false,"error":{"code":"invalid_request","category":"invalid_input",
 "message":"Analysis input is invalid. Check the arguments and try again.","retryable":true,
 "remediation":{"action":"Correct the listed arguments and retry."},
 "details":{"operation":"inspect_sqlite_database","issues":[{"path":["path"],"reason":"invalid_format",
  "message":"Rollback journal may require recovery: /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-hot/db.sqlite-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported."}]}},
 "meta":{"command":"inspect-sqlite-database","duration":"4ms"}}
```

## Differences against the committed 6.5.0 envelopes (observation)

`jq -S 'del(.meta.duration)'` on each committed envelope vs each live one, then `diff -u`:

| row | result |
|---|---|
| `m-journal-hot` | **IDENTICAL outside `meta.duration`** — journal refusal unchanged at 6.7.0 |
| `m-over-256mib` | 6.5.0 `code`/`category` `invalid_request`/`invalid_input` → `resource_constraint`/`resource_constraint`; `error.message` generic ("Analysis input is invalid…") → the specific byte-total sentence; `details.issues[0]{path:["path"],reason:"out_of_range",message}` → `details{resource:"file-size",reason,reported_limits}` (no `issues` key); `remediation.action` → export-workflow remedy; `retryable` `true` → `false` |
| `m-wal-over` | same seven-field change, same message apart from its own path |

New-in-6.7.0 details the entry does not name (omissions, not errors):
`details.reported_limits.sqlite_snapshot_input_bytes` = number `268435456`, while
`observed_sqlite_snapshot_input_bytes` is the **string** `"268435457"`; `retryable:false`; the new
`remediation.action`; and `code === category === "resource_constraint"` (the entry names the code and the
`resource` but not the category or `retryable`).

Provenance of the live binary (inference, two independent checks): `npx -y rea-agents@6.7.0` resolved to the
cached `~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` (`package.json` version `6.7.0`, sha256
`3f6c47fb…`); the emitted text `… total ${n} bytes, exceeding the combined … offline snapshot budget` and the
`reported_limits` block exist only in that pin's code
(`dist/sqlite/SqliteDatabaseSnapshot.js:137-143`, sha256 `87858b4a…`) and in the bundled
`dist/cli-runtime/cli.js:6180`, and nowhere in 6.5.0's `dist/sqlite/` (`grep "offline snapshot budget"` over
the 6.5.0 package: no match; 6.5.0 throws `ArtifactReaderFailure("limit", … "snapshot budget")` at
`dist/sqlite/SqliteDatabaseSnapshot.js:119`, sha256 `c8af51f8…`). `npm view rea-agents@6.7.0 version` → `6.7.0`.

## Sub-claim verdicts (entry line 50)

1. "the budget refusal becomes `AnalysisResourceConstraintError` (`resource_constraint`, resource `file-size`,
   a new message with the observed byte total, no `issues`)" — **holds** (observation, both budget rows).
2. "so `m-over-256mib` and `m-wal-over` would not match under 6.7.0" — **holds** (observation; the diffs above
   differ in code, category, message, details, remediation and retryable).
3. "the journal check also moves after the budget check" — **source-confirmed, live could-not-evaluate.**
   6.5.0: `verifyInactiveJournal` at `SqliteDatabaseSnapshot.js:116` precedes the size throw at `:117-119`;
   6.7.0: same file, size throw at `:137-143` precedes `verifyInactiveJournal` at `:145` (same order in the
   bundled `cli.js`: throw at `:6180`, journal verify after `:6184`). Discriminating it live needs a request
   that is both over budget and journal-hot; the frozen 23 contain no such row (`m-over-256mib` has no
   journal, `m-wal-over` has a `-wal`, not a `-journal`), and this item forbids other REA commands.
4. "The other 21 rows' code paths are unchanged." — **overstated / fails as written.** The arrival outcomes are
   unchanged in the one row measured live (`m-journal-hot`, above), but the code is not: against 6.5.0,
   `SqliteDatabaseFailures.js` has 37 changed lines (the `"limit" ? "out_of_range" : "invalid_format"`
   fallback at 6.5.0 `:52` becomes unconditional `"invalid_format"` at 6.7.0 `:62`), `SqliteDatabaseInspection.js`
   39 (column BLOB decoding), `SqliteDatabaseWorkerExecution.js` 21 (reply/cleanup branch) — files that the
   `m-not-sqlite`, `m-bad-pagesize`, `q-missing-table`, `q-missing-column`, journal and symlink rows traverse.
   The defensible statement is "no other row's committed envelope changes", which wave-1 argued statically for
   20 rows and this seat did **not** test live; only 1 of the 21 (plus 0 of the 20 remaining) was run.
5. "Not run live at 6.7.0." — was true when written; now stale. Three rows have live 6.7.0 envelopes
   (artifacts below). The L1 should replace that clause and the matching `SKILL.md:1038` "(static reading, not
   run)" with the live result and note that only these 3 of 23 rows are live-verified at 6.7.0.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r31/seats/w2/ProbePin670/)

| file | bytes | sha256 |
|---|---|---|
| `out/m-over-256mib-670.json` | 985 | `a46522110e4825bc57ddee578de198bab4b26a3c6b0929256749c6d444a3d3b6` |
| `out/m-over-256mib-670.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `out/m-wal-over-670.json` | 979 | `1b4a0eea6ddc021eba904be23d0126499754af2c82eff58bd347b5bfcf44e2e2` |
| `out/m-wal-over-670.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `out/m-journal-hot-670.json` | 617 | `f356b09d843b08c1f194146313cc72d212fe92376e96b7811e4f0ba8b85853bc` |
| `out/m-journal-hot-670.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

`tmp/` is the empty `TMPDIR` used by the runs. No install or update was performed (both pins were already in
the npx cache; `npm view` is a metadata read).

## Sources (local reads; no network source was opened)

| read | sha256 |
|---|---|
| `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseSnapshot.js` (6.5.0) | `c8af51f8496703a1992e7e7646c8bf8b6c56796a7571f5f8e9c84a284740ce19` |
| `~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/sqlite/SqliteDatabaseSnapshot.js` (6.7.0) | `87858b4ad45551fd034eb5d7c94a72cb412292e8a8b2ce54ad4acc7cae36d277` |
| `…/ad9a3fdbcad992c6/…/rea-agents/package.json` | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` |
| `…/a1722018f28f9df2/…/rea-agents/package.json` | `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570` |
| `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` | `bfcfeed190c7d5f4c15cd0a3c5c5a05d785ba109eee7a4158ecc804d511ff55c` |
| `corpus/evidence/round-31/c2/envelopes/m-over-256mib.json` | `1f6e73e630d7652f7ec39f82ea2d4bcae75a2cb1fc1fee69083a8724b5f23314` |

Located quote (6.5.0 ordering, `SqliteDatabaseSnapshot.js:116-119`):
`await verifyInactiveJournal(…, "initial", signal);` then `const selectedSize = database.size + (wal?.size ?? 0n);`
then `throw new ArtifactReaderFailure("limit", …-byte snapshot budget…)`. Located quote (6.7.0,
`SqliteDatabaseSnapshot.js:137-145`): `throw new AnalysisResourceConstraintError("inspect_sqlite_database",
"file-size", …offline snapshot budget…` and only later `await verifyInactiveJournal(…, "initial", signal);`.

## Limits

- 3 of 23 rows live at 6.7.0; the other 20 remain static-only (no envelope equality claim is made here for
  them). No dual over-budget/hot-journal mutant exists in the frozen set, so sub-claim 3 is source-only.
- The 6.7.0 identifier of the run is inferred from the cached package contents and the 6.7.0-only strings in
  the envelope, not from a version banner (`meta` carries only `command` and `duration`).
