# `inspect-sqlite-database` refusal and edge signatures at REA 6.5.0: 23 of 23 outcomes predicted from the code before any run

source: S092 (REA 6.5.0 SQLite reader code, `package/dist/sqlite/`, `dist/domain/sqlite/`, `dist/artifacts/readStableArtifact.js`, byte-identical to the installed copy); S096 and S097 for the file-format and PRAGMA terms
verified-at: 2026-10-23, round 31 (R31-C2); 23 live `rea-agents@6.5.0` calls 2026-10-23T04:19:10+00:00–2026-10-23T04:19:27+00:00 (`corpus/evidence/round-31/c2/runs.tsv`), after the freeze `35ba7c52` (predictions frozen there) and the control receipts `7474d269`
recheck: `python3 -I -B tools/round-31/c2-sqlite-refusals.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>`; the mutants live at `/fast/scratch/hyaku/kaidoku-r31/mutants/` (rebuild with `--build` from carrier `chinook`; pins in `.ufo/waves/round-31/claims.json` `mutant_sha256`/`mutant_sibling_sha256`); target `requests=23 matches=23 target=23 entry_ok=1 skill_ok=1`, exit 0. Quote only a run without `--write-evidence`.

## Claim

R31-C2, depth: a SKILL.md decision table of `inspect_sqlite_database` refusals and edge cases, every row predicted from the 6.5.0 code (S092) and frozen in `corpus/evidence/round-31/c2/predictions.tsv` before any REA run on a request. At the base SKILL.md names the operation 0 times; the lane's only prior knowledge of it (`corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md`) lists WAL inputs, corrupt files and table/row requests as unknown. Wave-1 `CriticAxisFitC2.md`: trivial predictors (all-accept, generic message, docs only, round-30 messages) score at most 3 of 23; 12 of the 13 distinct message prefixes occur 0 times in the base tree.

## Decision table (observed = predicted, 23 of 23)

Code is `error.code`; every refusal has `error.category: invalid_input` and exactly one entry in `error.details.issues` with the shown `path` / `reason` and `message`. `<path>` is the requested path as given. "worker" rows also carry `details.captured_output` (the refusal came from the owned SQLite worker); the others are refused before any SQLite open.

| id | request (base carrier `chinook` unless named) | outcome | code | issue path / reason | stage | message |
|---|---|---|---|---|---|---|
| `q-rowlimit-no-table` | `--row-limit 5` without `--table` (chinook) | refused, exit 1 | invalid_request | row_limit / invalid_value | snapshot / input | row_limit requires an explicit table selection |
| `q-columns-no-table` | `--column Name` without `--table` | refused, exit 1 | invalid_request | columns / invalid_value | snapshot / input | columns requires an explicit table selection |
| `q-scope-no-table` | `--schema-scope selected_table` without `--table` | refused, exit 1 | invalid_request | schema_scope / invalid_value | snapshot / input | selected_table schema scope requires table |
| `q-missing-table` | `--table NoSuchTable` (absent) | refused, exit 1 | invalid_request | table / invalid_format | worker | Selected ordinary table does not exist with that exact name: NoSuchTable |
| `q-case-table` | `--table album` (table is `Album`; exact-name lookup, no case folding) | refused, exit 1 | invalid_request | table / invalid_format | worker | Selected ordinary table does not exist with that exact name: album |
| `q-view-as-table` | `--table coordinate_operation_view` (a view, proj-371) | refused, exit 1 | invalid_request | table / invalid_format | worker | Selected ordinary table does not exist with that exact name: coordinate_operation_view |
| `q-missing-column` | `--table Album --column Nope` | refused, exit 1 | invalid_request | columns / invalid_format | worker | Selected column does not exist with that exact name in table Album: Nope |
| `q-virtual-rows` | `--table rtree_curve_geometry` (R*Tree virtual table, gpkg-curve) | refused, exit 1 | invalid_request | table / invalid_format | worker | Rows from virtual table rtree_curve_geometry are outside the ordinary-table inspection profile. |
| `q-shadow-rows` | `--table rtree_curve_geometry_node` (R*Tree shadow table) | refused, exit 1 | invalid_request | table / invalid_format | worker | Rows from shadow table rtree_curve_geometry_node are outside the ordinary-table inspection profile. |
| `q-ok-rows` | `--table Album --row-limit 3` | accepted, exit 0 | accept | — | — | evidence `ev_55f377bf37cf27d706e9dc2150aa89e9528bc19448ba36bef684f66f6b202481` |
| `m-missing` | path does not exist (parent directory exists) | refused, exit 1 | invalid_request | path / invalid_value | snapshot / input | Selected SQLite database does not exist: <path> |
| `m-enotdir` | a path component is a regular file | refused, exit 1 | invalid_request | path / invalid_value | snapshot / input | Selected database file set could not be read (ENOTDIR): <path> |
| `m-not-sqlite` | first 16 header bytes zeroed | refused, exit 1 | invalid_request | path / invalid_format | worker | file is not a database |
| `m-bad-pagesize` | header page size 768 (not a power of two) | refused, exit 1 | invalid_request | path / invalid_format | worker | file is not a database |
| `m-journal-hot` | sibling `-journal` with a nonzero 28-byte header | refused, exit 1 | invalid_request | path / invalid_format | snapshot / input | Rollback journal may require recovery: <path>-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported. |
| `m-journal-short` | sibling `-journal` of 10 zero bytes | refused, exit 1 | invalid_request | path / invalid_format | snapshot / input | Rollback journal may require recovery: <path>-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported. |
| `m-journal-empty` | sibling empty `-journal` | accepted, exit 0 | accept | — | — | evidence `ev_0ab137e3b8e59bb99203c9750cf05e3fa763733d6032b5b93020b17175cba2f4` |
| `m-journal-zero28` | sibling `-journal` of 28 zero bytes | accepted, exit 0 | accept | — | — | evidence `ev_b0856f85613341b0950f625803edb435e39f1fc71e5fe69a8e0b0ff765773ff3` |
| `m-journal-symlink` | sibling `-journal` is a symlink | refused, exit 1 | invalid_request | path / invalid_format | snapshot / input | Expected a regular journal without a symlink: <path>-journal |
| `m-db-symlink` | the database path is a symlink to a valid database | refused, exit 1 | invalid_request | path / invalid_format | snapshot / input | Expected a regular file without a symlink: <path> |
| `m-directory` | the database path is a directory | refused, exit 1 | invalid_request | path / invalid_format | snapshot / input | Expected a regular file without a symlink: <path> |
| `m-over-256mib` | sparse database of 268,435,457 bytes | refused, exit 1 | invalid_request | path / out_of_range | snapshot / input | Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: <path> |
| `m-wal-over` | 1,067,008-byte database + sparse `-wal` of 267,368,449 bytes (sum = budget + 1) | refused, exit 1 | invalid_request | path / out_of_range | snapshot / input | Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: <path> |

## What the table teaches (inference from S092 and the observations)

- Three stages refuse, in this order: (1) input schema — option dependencies are checked by the input schema (`dist/domain/sqlite/sqliteDatabase.js:44-61`) and projected as `reason: invalid_value` on the option's own path; (2) file-set snapshot — absence, `ENOTDIR`, journal state, the combined 256 MiB budget, then the regular-file check, all before SQLite opens anything (`dist/sqlite/SqliteDatabaseSnapshot.js:106-121`, `dist/artifacts/readStableArtifact.js:31-35`); (3) the worker — SQLite's own open error (`file is not a database`, errcode 26) and the table/column selection rules, each with `captured_output`.
- Table selection is exact-name: `album` does not find `Album`, and a view name gets the same "ordinary table does not exist" message as an absent name (the view is listed, but no table entry is built for it). Virtual and shadow tables are found and then refused by kind.
- A rollback journal is accepted only when empty or when its first 28 bytes are all zero; a shorter non-empty journal is refused like a hot one. A symlinked journal or database is refused; REA never follows either.
- The 256 MiB budget counts database plus WAL and is checked from `lstat` sizes before reading, so a sparse file triggers it; it is `invalid_request` / `out_of_range` at 6.5.0, not `resource_constraint`.

## Pin drift (static, wave-1 `ScoutPinDrift.md`)

At `rea-agents@6.7.0` the budget refusal becomes `AnalysisResourceConstraintError` (`resource_constraint`, resource `file-size`, a new message with the observed byte total, no `issues`), so `m-over-256mib` and `m-wal-over` would not match under 6.7.0; the journal check also moves after the budget check. The other 21 rows' code paths are unchanged. Not run live at 6.7.0.

## Limits

- Mutants derive from one carrier (`chinook`) plus two other carriers for the view and R*Tree rows; ELF-free, Linux only, one pin.
- Five messages are shared: missing-table ×3 (`q-missing-table`, `q-case-table`, `q-view-as-table`), not-a-database ×2, journal-recovery ×2, regular-file ×2, budget ×2. The shared pairs sit on distinct code branches, but the envelopes of `m-not-sqlite` and `m-bad-pagesize` are equal outside `meta` (same message, no path in it), so an id-rotated shortcut scored 1 of 23 (wave-1 `CtlC2ShortcutIds.md`).
- `file is not a database` is SQLite's text, not REA's; it was predicted from the worker's errcode mapping and probed with node:sqlite only on non-carrier files before the freeze (wave-1 `RevPredTraceB.md` repeated the probe).

## Corrections to the frozen predictions file (it stays as frozen)

- `m-wal-over` code-pointer note says "WAL 267367449 bytes"; the file is 267,368,449 bytes (database 1,067,008 + WAL = 268,435,457, the budget + 1). The message carries no size, so the comparison is unaffected (wave-1 `ScoutPinDrift.md`, `RevPredTraceB.md`).
- Pointer review (wave-1 `ReviewPointers.md`, 36 pointers): 21 exact, 14 contain the construct among other lines, 1 adjacent, 0 wrong. The adjacent one: `m-enotdir` `dist/sqlite/SqliteDatabaseFailures.js:79-86` → `78-85` (the `ENOENT`/`ENOTDIR` branch head is line 78).

## Supersedes / pointers

Extends `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md`; positive class `corpus/knowledge/2026-10-23-r31-sqlite-positive.md`. Pre-data controls (`.ufo/waves/round-31/controls/receipts.tsv`): do-nothing 0, junk-row 0, all-accept 0, predictions copied as observations 0 (round 30's same control scored 16 of 19; the full-envelope rule is the repair of M30-3), id-rotated shortcut 1 of 23.
