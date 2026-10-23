# ReDeriveGpkgC — independent re-derivation of C1 envelopes for gpkg-multisurface and gpkg-test-gpkg-nulls

Seat: `KaidokuR31.ReDeriveGpkgC` (leaf — no subagents spawned).
Date: 2026-10-23 (UTC timestamp of runs: 2026-10-23T04:31:58Z and 04:31Z).
Target: falsify the committed R31-C1 envelopes for the two named GeoPackage carriers by
re-deriving the schema from the immutable carrier files with a **non-oracle** reader
(Python `sqlite3` module on system libsqlite3 3.54.0, read-only immutable URI; plus
`sqlite3 -readonly` CLI spot-checks). The lane oracle
`tools/round-31/sqlite_oracle.py` was **not** used or read.

## Verdict

**Holds.** Every compared field of both committed envelopes reproduces exactly from an
independent re-derivation of the frozen carrier files. No mismatch found; no actionable
finding in scope.

## Method
Independent reader (authored for this seat):

- Python `sqlite3` (system libsqlite3 **3.54.0**, differs from REA's bundled SQLite
  3.53.4 reported in `provider.version`), connection `file:<path>?immutable=1` (read-only,
  no journal writes).
- Queries: `SELECT type,name,tbl_name,rootpage,sql FROM sqlite_schema ORDER BY rowid`
  (stored order), `PRAGMA table_list`, `PRAGMA table_xinfo('<table>')` per non-virtual
  table, `PRAGMA encoding`.
- Rebuilt structures: tables (name, sql, root_page, kind, without_rowid, strict,
  column_count, columns_completeness, columns[cid,name,declared_type,not_null,
  default_sql,primary_key_position,hidden]), indexes (name, table, sql, root_page),
  views (name, table, sql), triggers (name, table, sql).
- Compared element-wise against envelope `data.normalized_result` (`schema.tables`,
  `schema.indexes`, `schema.views`, `schema.triggers`, `schema.scope`,
  `schema.completeness`, `artifact.sha256`, `artifact.bytes`, `database_encoding`) and
  `data.subject.digest.sha256`.

### Commands, outcomes, exit codes

| # | Command | Exit | UTC | Output excerpt |
|---|---------|------|-----|----------------|
| 1 | `timeout 300 python3 -I -B rederive_gpkg.py` (script below) | 0 | 2026-10-23T04:31:58Z | `MISMATCHES: 0` for both carriers; `counts mine: tables=13 indexes=8 views=0 triggers=18` for both; `column sum table: 47 / virtual: 5 / shadow: 6` (multisurface), `table: 58 / virtual: 5 / shadow: 6` (nulls) |
| 2 | `timeout 300 sqlite3 -readonly "file:…/gpkg-multisurface.gpkg?immutable=1" "SELECT count(*) … type='table'…"` | 0 | 2026-10-23T04:31Z | `13 8 18 0` (tables, indexes, triggers, views) |
| 3 | `timeout 300 sqlite3 -readonly "file:…/gpkg-test-gpkg-nulls.gpkg?immutable=1" "SELECT name,type FROM sqlite_schema WHERE type='table' ORDER BY rowid;"` | 0 | 2026-10-23T04:31Z | 13 tables in identical order: `gpkg_spatial_ref_sys … gpkg_contents … gpkg_tile_matrix … sqlite_sequence … gpkg_extensions … test_gpkg_nulls … rtree_test_gpkg_nulls_geom(_rowid/_node/_parent)` |

Full canonical stdout: `work/rederive.out` (sha256 `9ae4d4cf07036c9c3278d942f014139f05116ce456d15014d2d9ae9495e3c96b`).

## Results per carrier

### gpkg-multisurface (carrier `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-multisurface.gpkg`)

- `sha256`: mine `898a238bc119f051622c22de973899f501466a33a6a6c0cc405122802c6d648d` =
  envelope `artifact.sha256` = envelope `subject.digest.sha256` = frozen `carriers.tsv`
  line 12 digest. **Observation.**
- `artifact.bytes`: 98304 = envelope 98304 = tsv size. **Observation.**
- `database_encoding`: UTF-8 = envelope. **Observation.**
- Schema: 13 tables (9 table + 1 virtual + 3 shadow), 8 indexes, 0 views, 18 triggers —
  counts match envelope; element-wise comparison of every field of every entry: **0
  mismatches** (ordering identical, including autoindex `sql`=null, virtual table
  `column_count`=5 with `columns_completeness`="unsupported" and `columns`=[], shadow
  table columns incl. empty `declared_type` on rtree `_node.data`). **Observation.**
- Envelope `evidence_id` `ev_c836ccb09a6ac28a7e719a1e4682c088068c8ed73e1ad14392affe159b1f5af0`
  = knowledge entry `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` line 27;
  knowledge row T/I/V/Tr **13/8/0/18**, columns **53** = my non-virtual column total
  (47 table + 6 shadow); virtual table's 5 declared columns are excluded from the
  knowledge "columns" figure (58 total incl. virtual). **Observation.**
- `.stderr` envelope sidecar: empty. **Observation.**

### gpkg-test-gpkg-nulls (carrier `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-test-gpkg-nulls.gpkg`)

- `sha256`: mine `4281d3c55f2042e2174ab9a13c5c5a06d13841071c1aa3ea2cc131afaf71e1d8` =
  envelope `artifact.sha256` = envelope `subject.digest.sha256` = frozen `carriers.tsv`
  line 13 digest. **Observation.**
- `artifact.bytes`: 98304 = envelope = tsv size. **Observation.**
- `database_encoding`: UTF-8 = envelope. **Observation.**
- Schema: 13 tables (9 table + 1 virtual + 3 shadow), 8 indexes, 0 views, 18 triggers;
  element-wise comparison: **0 mismatches**. Feature table `test_gpkg_nulls`
  (13 columns) and virtual `rtree_test_gpkg_nulls_geom` reproduced identically. **Observation.**
- Envelope `evidence_id` `ev_699901859c0d92f8c46a05dfbb9ce51d0e4e7d53aea78bf16c55d2e1450ec99e`
  = knowledge line 28; knowledge row T/I/V/Tr **13/8/0/18**, columns **64** = my
  non-virtual column total (58 table + 6 shadow; 69 incl. virtual). **Observation.**
- `.stderr` envelope sidecar: empty. **Observation.**

## Artifacts (sha256)

Under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveGpkgC/`:

- `work/rederive_gpkg.py` — `de9dbd0a3b872fa6e44bc83f3c452985656b3191673cadefde56f3115e81e157`
- `work/rederive.out` — `9ae4d4cf07036c9c3278d942f014139f05116ce456d15014d2d9ae9495e3c96b`
- `work/gpkg-multisurface.json`, `work/gpkg-test-gpkg-nulls.json` — byte copies of the
  committed envelopes (sha256 of copies: same as lane files; not recomputed separately
  beyond `cp`).

Tool installs: **none** (system `python3` + `sqlite3` module used; no `uv`/`npx`/binary
installs needed).

## Residual risk / verification gaps

- Schema reported by REA 6.5.0 was produced with its bundled SQLite 3.53.4; independent
  reader used system libsqlite3 3.54.0. Both agree on every compared field for both
  carriers, so no forward/backward incompatibility observed. Row content is out of scope
  (`normalized_result.rows` = null; predicate is schema coverage).
- Knowledge-entry "columns" figures (53/64) are interpreted as non-virtual column totals;
  the +5 virtual-table declared columns are not counted there. Envelope
  `column_count`=5 on the virtual table is reproduced.
- The counters' committed-record rule (full-envelope equality) was not run from this
  seat; this report validates the two envelopes' contents directly against the frozen
  carrier files.
