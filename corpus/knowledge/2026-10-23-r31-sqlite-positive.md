# `inspect-sqlite-database` at scope `database` on published SQLite files: REA 6.5.0 reports every table, column, index, view and trigger exactly as an independent reader does (12 of 12)

source: S096 (SQLite file format, the spec the oracle's byte parser implements); S097 (SQLite PRAGMA table_list/table_xinfo, the meaning of kind, ncol, wr, strict, hidden); S093 (PyPI pyproj 3.4.1–3.7.1 records, wheel digests behind 5 carriers); S094 (Chinook v1.4.5 release assets, 2 carriers); S095 (PyPI pyogrio 0.11.1 record and sdist, 5 GeoPackage carriers); S092 (REA 6.5.0 SQLite reader code, for the inferences below)
verified-at: 2026-10-23, round 31 (R31-C1); 12 live `rea-agents@6.5.0` `inspect-sqlite-database --schema-scope database` calls 2026-10-23T04:18:57+00:00–2026-10-23T04:19:09+00:00 (`corpus/evidence/round-31/c1/runs.tsv`), after the freeze commit `35ba7c52` (04:05Z) and the control receipts `7474d269`
recheck: `python3 -I -B tools/round-31/c1-sqlite-positive.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>` (re-runs REA live on the 12 carriers at `/fast/scratch/hyaku/kaidoku-r31/carriers/`; an absent or altered carrier exits 2 — re-extract it from the container named in `corpus/evidence/round-31/c1/carriers.tsv`); target `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0. Quote only a run without `--write-evidence` (that flag skips the committed-record clause; wave-1 `CtlC1DoNothing.md`).

## Claim

R31-C1, coverage: PROVINCE Core gains REA operation `inspect_sqlite_database` (CLI `inspect-sqlite-database`). At the base `c369242f` PROVINCE.md names the operation 0 times under either spelling, and no Core row owns SQLite reading. The lane already held one path-only run of this operation: `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` (luna-round-6/7, one pnpm index copy, scope `inventory`, columns not requested, `rows:null`). Correction to the frozen claim text: `claims.json` says "a verb the lane has never run or named"; that is false — the zero count holds only for the hyphenated CLI spelling (wave-1 `CriticAxisFitC1.md`, `CriticAxisFitC2.md`; mistake M31-1). What this round adds is the first Core row for the operation and the database-scope reading (every column, kind, root page and declaration) on 12 published files from three producers, against an independent reader.

## Carriers

Frozen list `corpus/evidence/round-31/c1/carriers.tsv` (12 rows; files at `/fast/scratch/hyaku/kaidoku-r31/carriers/`, `chattr +i`). Counts are tables/indexes/views/triggers and columns over all non-virtual tables.

| id | producer | sha256 prefix | bytes | evidence_id | T/I/V/Tr | columns | table kinds | verdict |
|---|---|---|---:|---|---|---:|---|---|
| proj-341 | pyproj wheel (S093) | `97a04533b1e7` | 8278016 | `ev_52a9b4951d991aeead1fab8ed0374b3d22b5632e7927442f289df8f2ad4d1835` | 36/21/7/35 | 385 | table | P1-pass |
| proj-350 | pyproj wheel (S093) | `deaa7e9db95e` | 8495104 | `ev_55b3f96bbc31f16782c8bde3ba06acd4646178224bd3e225b9b10e1457ec76aa` | 36/21/7/35 | 385 | table | P1-pass |
| proj-361 | pyproj wheel (S093) | `79b660eb3c09` | 8581120 | `ev_64b5feb7dadec43ad7eeb4f1972a845e697a36615ee6b505fa8f60e980349350` | 36/21/7/35 | 385 | table | P1-pass |
| proj-370 | pyproj wheel (S093) | `976d427f0377` | 9154560 | `ev_4bd51490c5d690a628d39e9217a635985d57fea0a7d5d65d2f8c2a5253d526da` | 37/21/7/36 | 395 | table | P1-pass |
| proj-371 | pyproj wheel (S093) | `a25d85a2ebfc` | 9261056 | `ev_4a9d1724322141214d9678dcb36a5075036b6eee9b75c46996e045aca21a495f` | 38/21/7/36 | 396 | table | P1-pass |
| chinook | Chinook v1.4.5 release (S094) | `bdf635be6985` | 1067008 | `ev_fe9589c14b3445f946d1b213dd9915b44e67101a000ec14a92c5fb2fff303d52` | 11/11/0/0 | 64 | table | P1-pass |
| chinook-autoinc | Chinook v1.4.5 release (S094) | `ca157cb58cb3` | 1067008 | `ev_979cf0eb91af644ab3e6033917ccead5a4684dd71127d070346c085d94b92cce` | 12/11/0/0 | 66 | table | P1-pass |
| gpkg-curve | pyogrio 0.11.1 sdist (S095) | `03a9c5904fd3` | 98304 | `ev_4e5aa3c972f950b6e84a5ec33b123e7fdc896064db38809b035b7009eabac35f` | 13/8/0/18 | 53 | shadow, table, virtual | P1-pass |
| gpkg-curvepolygon | pyogrio 0.11.1 sdist (S095) | `00a1309ab0f2` | 98304 | `ev_4c282804977b2f03c53715d6d736277713e471ba1744e8eeb5fd1471754d7e3e` | 13/8/0/18 | 53 | shadow, table, virtual | P1-pass |
| gpkg-line-zm | pyogrio 0.11.1 sdist (S095) | `9563e513b064` | 98304 | `ev_92b9b645011eb1aec86970a4fdf108da99f4598143ef9b9e739042979af03580` | 13/8/0/18 | 53 | shadow, table, virtual | P1-pass |
| gpkg-multisurface | pyogrio 0.11.1 sdist (S095) | `898a238bc119` | 98304 | `ev_c836ccb09a6ac28a7e719a1e4682c088068c8ed73e1ad14392affe159b1f5af0` | 13/8/0/18 | 53 | shadow, table, virtual | P1-pass |
| gpkg-test-gpkg-nulls | pyogrio 0.11.1 sdist (S095) | `4281d3c55f20` | 98304 | `ev_699901859c0d92f8c46a05dfbb9ce51d0e4e7d53aea78bf16c55d2e1450ec99e` | 13/8/0/18 | 64 | shadow, table, virtual | P1-pass |

The pyproj 3.7.2 wheel's `proj.db` is byte-identical to 3.7.1's and is not a carrier (wave-1 `ReviewCarrierProvenance.md`). Every carrier re-derives from its published container (same report, 12 of 12).

## Method

- **Oracle** (`tools/round-31/sqlite_oracle.py`): the `sqlite_schema` rows (type, name, tbl_name, rootpage, sql) come from a pure-Python reader of the file format (S096: header, table b-tree pages, overflow chains, record serial types) — no SQLite code. Kind, `without_rowid`, `strict`, `ncol` and the columns come from the system libsqlite3 3.54.0 through Python (`PRAGMA table_list`, `PRAGMA table_xinfo`, S097), opened `mode=ro&immutable=1`. REA runs SQLite 3.53.4 bundled in node v24.21.0. The library's own `sqlite_schema` rows must equal the byte parser's, or the oracle raises.
- **REA**: the counter runs `npx -y rea-agents@6.5.0 inspect-sqlite-database <carrier> --schema-scope database --format json --full-output` live per carrier and compares `normalized_result` minus `engine.version` and `limitations` with the oracle report field for field. The committed envelope must equal the live one in every field except `meta` (only `meta.duration` varies between runs).
- **Predicate P1-pass** (verbatim, `.ufo/waves/round-31/claims.json`):

> A carrier passes when its live REA 6.5.0 inspect-sqlite-database --schema-scope database run exits 0 with an ok envelope whose operation is inspect_sqlite_database and whose subject sha256 equals the carrier's frozen sha256, and whose normalized_result, without engine.version and limitations, equals the independent oracle's report field for field (artifact, wal, engine name, database_encoding, and every table, index, view and trigger with name, sql, root page, kind, without_rowid, strict, column count, column completeness and all column fields; rows null); and its committed envelope, first added after the freeze commit, equals the live envelope in every field except meta, and the round-31 entry names that evidence_id.

## Results

Observation: 12 of 12 carriers pass P1 (`.ufo/waves/round-31/after/`). Across them REA's report equals the oracle on 271 tables, 167 indexes, 35 views, 267 triggers and 2,352 columns (sums of the table above; 740 schema rows).

Observation, what the reports show:
- Kinds follow SQLite's `PRAGMA table_list` (S097): each GeoPackage has one R*Tree `virtual` table (`rtree_<table>_<geom>`, `column_count` 5, `columns_completeness: unsupported`, `columns: []`, `root_page` 0) and three `shadow` tables (`_node`, `_parent`, `_rowid`) with complete columns. PROJ and Chinook files hold only `table`.
- Auto-indexes appear in `indexes` with `sql: null` (82 of the 740 schema rows have no SQL, wave-1 `ScoutSchemaWidth.md`).
- Trigger `table` is the stored target; on these files all 267 targets name a listed table or view exactly, so REA's case-folding path is not exercised.
- `declared_type` is SQLite's own `table_xinfo` type string; REA does not rewrite it.
- The long PROJ trigger declarations (up to 128,117 characters of SQL, carried on overflow chains of up to 31 pages in the file) come back whole in `sql`.

Inference (S092 code, `dist/sqlite/SqliteDatabaseInspection.js:144-294`): REA reads `PRAGMA main.table_list` then `main.sqlite_schema` in table order and asks `table_xinfo` per non-virtual table, so its report is SQLite's catalog relayed without reinterpretation, plus its own `kind: unknown` rule for tables that may shadow an unresolved virtual table (not exercised: no carrier has an unresolved virtual table). Agreement here shows the relay drops, reorders and rewrites nothing on these inputs; it does not show SQLite's own catalog is right, and both readers share upstream SQLite for kinds and columns.

## Limits

- Width: three producers, 12 distinct schemas (canonical schema hashes, `ScoutSchemaWidth.md`), but 3 schema families: proj-341/350/361 share table names and differ only in declarations, and the five GeoPackages share one layout. All UTF-8, no WAL, no journal, every page-1 an interior page of depth 2, overflow only in the five PROJ files.
- Independence: the oracle's names, declarations, root pages and order come from code that shares no SQLite source; kinds, flags and columns come from libsqlite3 (a different build from REA's). A SQLite bug in `table_xinfo` common to 3.53.4 and 3.54.0 would pass unseen.
- Oracle mutants that these carriers cannot see (wave-1 `MutOracle.md`, 4 of 12 survive): reserved-byte handling, trigger case folding, hidden-column flags and strict flags — no carrier has reserved bytes, a case-variant trigger target, a hidden column or a STRICT table.
- One REA pin (6.5.0). At 6.7.0 the column read moves to `pragma_table_xinfo` with byte decoding; a static check found the two forms byte-equal on these 12 files (`ScoutPinDrift.md`), not a live 6.7.0 run.
- The report is the schema only (`rows: null`); row reading is R31-C2's `q-ok-rows`.

## Supersedes / pointers

Extends, does not replace, `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` (one inventory-scope run). Refusal and edge signatures: `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md`. Pre-data controls (`.ufo/waves/round-31/controls/receipts.tsv`, committed at `7474d269` before the data `f368a101`): do-nothing, junk-row, all-false, no-reader and id-rotated shortcut all scored pass 0 of 12, exit 1; a Core-placement shortcut with real envelopes failed `province_ok` in both variants.
