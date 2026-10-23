# Wave-2 seat report — ReviewC2EnvB (C2 envelope vs prediction vs SKILL vs entry)

Seat: `KaidokuR31.ReviewC2EnvB` (leaf, no subagents). Date: 2026-10-23.
Assignment: check C2 rows `q-missing-column`, `q-virtual-rows`, `q-shadow-rows`,
`q-ok-rows`, `m-missing`, `m-enotdir` — committed envelope vs frozen prediction vs
SKILL.md round-31 row vs knowledge entry row; verify exit, `ok`, `error.code`,
`error.category`, `details.issues` (exact), `details.captured_output` presence,
and for `q-ok-rows` the `evidence_id` and subject sha; verify entry stage/code-line
claims against the installed `rea-agents@6.5.0` dist.

## Verdict: all six rows HOLD. No overstatement found.

All six committed envelopes agree exactly with the frozen predictions (exit, code,
category, single issue {path, reason, message}, and the captured_output presence/
absence predicted by the entry's worker vs non-worker rule), with the SKILL.md
table rows, and with the knowledge entry rows. One counter measure-mode run of the
full 23-request suite reported `requests=23 matches=23 target=23 entry_ok=1
skill_ok=1`, exit 0, which includes the full-envelope committed-vs-live equality
(except `meta`) for every id here.

## Per-row evidence (committed envelope → prediction → SKILL → entry)

### `q-missing-column` — HOLDS
- Envelope `.../c2/envelopes/q-missing-column.json`: `ok=false`;
  `error.code=invalid_request`; `error.category=invalid_input`; exactly one issue
  `{path:["columns"], reason:invalid_format, message:"Selected column does not exist with that exact name in table Album: Nope"}`
  (no trailing period, matches prediction/SKILL/entry verbatim); `details.captured_output`
  present `{stdout:"",stderr:"",truncated:false}`.
- runs.tsv row: exit 1, argv `... --table Album --column Nope --format json --full-output`,
  pkg 6.5.0, sha `a5003023…`, verdict `P2-match refused invalid_request invalid_format`.
- SKILL row (L1020): `invalid_request | columns / invalid_format | Selected column does not exist with that exact name in table Album: Nope` — matches.
- Entry row (L23): stage `worker`, same code/issue/message — matches; worker rows carry `captured_output` — present.
- Code pointers verified against dist (see below): `SqliteDatabaseInspection.js:313-316` exact; `SqliteDatabaseWorkerExecution.js:31-58` covers the rejection mapping (reason `column-selection` → path `columns`, invalid_format) and `AnalysisInputError` construction with `capturedOutput`.

### `q-virtual-rows` — HOLDS
- Envelope: `ok=false`, `invalid_request` / `invalid_input`, one issue
  `{path:["table"], reason:invalid_format, message:"Rows from virtual table rtree_curve_geometry are outside the ordinary-table inspection profile."}`
  (trailing period present; matches prediction/SKILL/entry), `captured_output` present.
- runs.tsv: exit 1, `P2-match refused invalid_request invalid_format`.
- SKILL row (L1021) and entry row (L24, stage worker): identical message — match.
- Code: `SqliteDatabaseInspection.js:306-307` exact (`if (table.kind !== "table") throw ... Rows from ${table.kind} table ${input.table} are outside the ordinary-table inspection profile.`; kind `virtual` → envelope text).

### `q-shadow-rows` — HOLDS
- Envelope: `ok=false`, `invalid_request` / `invalid_input`, one issue
  `{path:["table"], reason:invalid_format, message:"Rows from shadow table rtree_curve_geometry_node are outside the ordinary-table inspection profile."}`,
  `captured_output` present.
- runs.tsv: exit 1, `P2-match refused invalid_request invalid_format`.
- SKILL row (L1022) and entry row (L25, stage worker): identical message — match.
- Code: same `SqliteDatabaseInspection.js:306-307` template (kind `shadow`).

### `q-ok-rows` — HOLDS (acceptance)
- Envelope: `ok=true`; `data.evidence_id = ev_55f377bf37cf27d706e9dc2150aa89e9528bc19448ba36bef684f66f6b202481`
  (exactly the id the entry cites, L26); `data.subject = {name: chinook.sqlite,
  digest.sha256: bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a,
  local_path: /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite, format: file}`;
  `parameters={path: <carrier>, table: Album, row_limit: 3}`; `normalized_result`:
  `artifact.sha256` equals the subject sha, bytes 1067008, `schema.scope=selected_table`,
  `rows={table: Album, columns: [AlbumId, Title, ArtistId], values: 3 rows, row_limit: 3,
  returned_rows: 3, truncated: true, order: unspecified}`.
- Independent check: `sha256sum /fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite`
  = `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` — equals the
  envelope subject/digest sha. (Carrier is the frozen immutable file; the counter's PIN
  check on it also passed.)
- runs.tsv: exit 0, `P2-match accepted, 3 Album rows`.
- SKILL row (L1023): `accept | — | 3 Album rows, columns AlbumId, Title, ArtistId; order unspecified` — exactly what the envelope reports (including `order: unspecified`; `truncated: true` records the bounded sample, not an overstatement).
- Code pointers: `SqliteDatabaseInspection.js:299-330` contains the acceptance `readRows`
  path (kind check, limit default, column projection); `SqliteDatabaseService.js:9-28`
  contains `matchesSelectedDatabase` (subject-sha/report consistency used for evidence). Containing-construct pointers, not exact-equality claims — acceptable and not contradicted.

### `m-missing` — HOLDS
- Envelope: `ok=false`, `invalid_request` / `invalid_input`, one issue
  `{path:["path"], reason:invalid_value, message:"Selected SQLite database does not exist: /fast/scratch/hyaku/kaidoku-r31/mutants/m-missing/db.sqlite"}`
  (`{P}` → request path). No `captured_output` key — consistent with the entry's rule
  that only worker rows carry it.
- runs.tsv: exit 1, `P2-match refused invalid_request invalid_value`.
- SKILL row (L1024) and entry row (L27, stage `snapshot / input`): identical message — match.
- Layout check: `/fast/scratch/hyaku/kaidoku-r31/mutants/m-missing/` exists and is empty (db.sqlite absent), so the EN path has an existing parent — matches the prediction's input condition.
- Code: `SqliteDatabaseSnapshot.js:97-103` (`missingDatabase`, message template exact) and `:113-114` (`if (database === null) throw missingDatabase(path)`) — exact.

### `m-enotdir` — HOLDS
- Envelope: `ok=false`, `invalid_request` / `invalid_input`, one issue
  `{path:["path"], reason:invalid_value, message:"Selected database file set could not be read (ENOTDIR): /fast/scratch/hyaku/kaidoku-r31/mutants/m-enotdir/file/db.sqlite"}`.
  No `captured_output` key.
- runs.tsv: exit 1, `P2-match refused invalid_request invalid_value`.
- SKILL row (L1025) and entry row (L28, stage `snapshot / input`): identical message — match.
- Layout check: `m-enotdir/file` is a regular file (`stat` → `regular file`), so component `file` is not a directory — exactly the prediction's condition.
- Code: `SqliteDatabaseSnapshot.js:13-21` — `optionalStat` rethrows non-ENOENT lstat errors incl. ENOTDIR (exact); `SqliteDatabaseFailures.js:78-85` — ENOTDIR → `AnalysisInputError` with path `["path"]`, `invalid_value`, message template (the frozen pointer `79-86` is the adjacent one the entry itself discloses at L61: branch head is line 78). No overstatement.

## Counter run (measure mode, no `--write-evidence`)

Command:
```
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReviewC2EnvB/tmp timeout 900 \
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 1288285eed81395e6af7c279a173b117b2c2eaa3
```
Output excerpt (ids in scope):
```
q-missing-column	P2-match	refused invalid_request invalid_format
q-virtual-rows	P2-match	refused invalid_request invalid_format
q-shadow-rows	P2-match	refused invalid_request invalid_format
q-ok-rows	P2-match	accepted, 3 Album rows
m-missing	P2-match	refused invalid_request invalid_value
m-enotdir	P2-match	refused invalid_request invalid_value
...
requests=23 matches=23 target=23 entry_ok=1 (ok) skill_ok=1 (ok)
```
Exit code 0; completed 2026-10-23T04:32:13Z. The measure path performs the
committed-envelope check (`committed_check`) for every P2-match entry: committed
envelope at rev equals the live envelope in every field except `meta`, and was
added after the freeze commit. No PIN complaints (no mutation of frozen inputs).
No lane file was written; the only scratch writes were transient node compile-cache
files under my TMPDIR, removed after the run (scratch dir now empty).

## Tool installs
None. All checks used existing tools (python3, git read-only, npx with the already
populated `rea-agents@6.5.0` cache at `~/.npm/_npx/ad9a3fdbcad992c6`). No packages
installed or updated.

## Residual risk / verification gaps
- `evidence_id` (`ev_55f377…`) is cited by the entry and matches the committed
  envelope (and the live run via full-envelope equality), but it was not
  independently recomputed by this seat; its internal consistency (ev_<sha256>
  shape, uniqueness) was not re-derived.
- The `q-ok-rows` acceptance was not re-checked against the independent oracle's
  full schema here (the counter's q-ok-rows branch does compare the selected-table
  schema and row set against the oracle, and it passed); the broader oracle
  equality for scope-database acceptances is out of this seat's row scope.
- Code-pointer verification covered the lines cited for these six rows; the other
  17 rows' pointers were already reviewed by wave-1 `ReviewPointers.md` and are out
  of scope.

## Conclusion
None of the six examined rows is falsified; every frozen prediction, SKILL table
row, and entry statement checked for these rows is backed by the committed (and
live-reproduced) envelope, including the worker/non-worker `captured_output` rule
and the acceptance subject sha. No actionable finding remains in scope.
