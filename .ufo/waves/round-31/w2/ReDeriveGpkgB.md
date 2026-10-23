# R31-C1 independent re-derivation: gpkg-curvepolygon and gpkg-line-zm

**Scope:** the two assigned C1 envelopes only. **Run date:** 2026-10-23. No REA/counter was run and no tool was installed.

## Result

**Observation:** independent SQLite CLI inspection matched the carrier digests, byte lengths, schema record counts, and all compared schema fields except the virtual RTree column fields explicitly marked unsupported in each envelope. Each carrier therefore has **2 field mismatches**, at the exact JSON paths below. All other compared values match. The independent reader does recover five virtual-table columns where the envelopes store `columns: []`; this does not change the knowledge document's 53-column total, which is expressly over non-virtual tables.

**Inference:** these are reported as field-for-field differences, not as evidence that the envelope claims complete virtual-table columns: it marks their completeness `unsupported` and the knowledge document records the same limitation.

## Reader, fields, and commands

Reader: `/usr/bin/sqlite3` CLI, version **3.54.0**, invoked read-only with URI `file:<absolute carrier path>?immutable=1`. This is independent of `tools/round-31/sqlite_oracle.py`. The driver queried `sqlite_schema` for type/name/table/sql/rootpage, `PRAGMA table_list` for kind/ncol/without-rowid/strict, and `PRAGMA table_xinfo("<each table>")` for column fields. It compared entries by identity and compared column lists in cid order.

Fields compared:

- Schema: `scope`, `completeness`.
- Every table: `name`, `sql`, `root_page`, `kind`, `without_rowid`, `strict`, `column_count`, `columns_completeness`, `columns`.
- Every derived column: `cid`, `name`, `declared_type`, `not_null`, `default_sql`, `primary_key_position`, `hidden`.
- Every index: `name`, `table`, `sql`, `root_page`; every view and trigger: `name`, `table`, `sql`.
- Separately, `subject.digest.sha256`, `normalized_result.artifact.sha256`, and `normalized_result.artifact.bytes` against the actual carrier.

Main command (cwd `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveGpkgB`):

```text
timeout 300 python3 -I -B rederive.py
```

The driver checks the return code for every SQLite subprocess and aborts on any nonzero code. It completed both carriers; its **overall exit code was 1** because it found the two listed mismatch paths for each carrier. Run time: **2026-10-23T04:34:26Z** (start and end).

Explicit confirmation commands, each with `timeout 10 /usr/bin/sqlite3 -readonly -json "file:<carrier>?immutable=1" <SQL>`:

```sql
SELECT name,type,ncol,wr,strict FROM pragma_table_list WHERE name LIKE 'rtree_%' ORDER BY name;
PRAGMA table_xinfo("rtree_curvepolygon_geometry");
PRAGMA table_xinfo("rtree_line_zm_geometry");
```

The `table_list` and `table_xinfo` calls returned **exit code 0** for both carriers at **2026-10-23T04:35:09Z**. The complete queries and output are in `cli-probe.out`. Exact output excerpt for curvepolygon:

```text
[{"name":"rtree_curvepolygon_geometry","type":"virtual","ncol":5,"wr":0,"strict":0},
 {"name":"rtree_curvepolygon_geometry_node","type":"shadow","ncol":2,"wr":0,"strict":0},
 {"name":"rtree_curvepolygon_geometry_parent","type":"shadow","ncol":2,"wr":0,"strict":0},
 {"name":"rtree_curvepolygon_geometry_rowid","type":"shadow","ncol":2,"wr":0,"strict":0}]
[{"cid":0,"name":"id","type":"INT","notnull":0,"dflt_value":null,"pk":0,"hidden":0},
 {"cid":1,"name":"minx","type":"REAL","notnull":0,"dflt_value":null,"pk":0,"hidden":0},
 {"cid":2,"name":"maxx","type":"REAL","notnull":0,"dflt_value":null,"pk":0,"hidden":0},
 {"cid":3,"name":"miny","type":"REAL","notnull":0,"dflt_value":null,"pk":0,"hidden":0},
 {"cid":4,"name":"maxy","type":"REAL","notnull":0,"dflt_value":null,"pk":0,"hidden":0}]
SQLITE_EXIT=0
```

The line-zm output has the same five column rows, with `rtree_line_zm_geometry` and its three corresponding shadow names; its `SQLITE_EXIT=0` is recorded in the same output file.

## Per-carrier findings

### `gpkg-curvepolygon`

- Carrier: `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-curvepolygon.gpkg`.
- Evidence id: `ev_4c282804977b2f03c53715d6d736277713e471ba1744e8eeb5fd1471754d7e3e`.
- Digest: envelope `subject.digest.sha256` and `normalized_result.artifact.sha256` both `00a1309ab0f29f97a4c5f6cb9cd3bde27143fc936712d5101767f60f0c96bac7`; actual SHA-256 matches both. `artifact.bytes` expected/actual: `98304/98304`.
- Compared 13 tables (58 CLI xinfo columns, including 5 virtual), 8 indexes, 0 views, and 18 triggers, plus schema scope/completeness and the listed table/column/index/view/trigger fields.
- **Mismatches (2):**
  - `data.normalized_result.schema.tables[rtree_curvepolygon_geometry].columns`: envelope `[]`; CLI returned five columns `id INT`, `minx REAL`, `maxx REAL`, `miny REAL`, `maxy REAL` (all `notnull=0`, `dflt_value=null`, `pk=0`, `hidden=0`; cids 0–4).
  - `data.normalized_result.schema.tables[rtree_curvepolygon_geometry].columns_completeness`: envelope `unsupported`; CLI-derived `complete`.
- Remaining fields match. Counts: T/I/V/Tr `13/8/0/18`; non-virtual columns `53`; kinds `9 table / 3 shadow / 1 virtual`.

Producing comparison command and evidence: `timeout 300 python3 -I -B rederive.py`, **exit 1**, **2026-10-23T04:34:26Z**. Exact output excerpts:

```text
FIELD-COMPARISON mismatches=2
MISMATCH VALUE schema.tables[rtree_curvepolygon_geometry].columns envelope=[] derivation=[{'cid': 0, 'name': 'id', 'declared_type': 'INT', 'not_null': False, 'default_sql': None, 'primary_key_position': 0, 'hidden': 0}, ...]
MISMATCH VALUE schema.tables[rtree_curvepolygon_geometry].columns_completeness envelope='unsupported' derivation='complete'
COUNTS T/I/V/Tr=13/8/0/18; nonvirtual-columns=53
KIND-COUNTS table=9, shadow=3, virtual=1
```

The omitted portion of the exact `columns` output contains the four remaining xinfo records shown in the explicit CLI output above. The CLI table-list and table-xinfo commands for this carrier each exited 0 at 04:35:09Z.

### `gpkg-line-zm`

- Carrier: `/fast/scratch/hyaku/kaidoku-r31/carriers/gpkg-line-zm.gpkg`.
- Evidence id: `ev_92b9b645011eb1aec86970a4fdf108da99f4598143ef9b9e739042979af03580`.
- Digest: envelope `subject.digest.sha256` and `normalized_result.artifact.sha256` both `9563e513b064476ee7ab8c66858f3f434307ca554f7495652d09674d2747c70c`; actual SHA-256 matches both. `artifact.bytes` expected/actual: `98304/98304`.
- Compared 13 tables (58 CLI xinfo columns, including 5 virtual), 8 indexes, 0 views, and 18 triggers, plus schema scope/completeness and the listed table/column/index/view/trigger fields.
- **Mismatches (2):**
  - `data.normalized_result.schema.tables[rtree_line_zm_geometry].columns`: envelope `[]`; CLI returned five columns `id INT`, `minx REAL`, `maxx REAL`, `miny REAL`, `maxy REAL` (all `notnull=0`, `dflt_value=null`, `pk=0`, `hidden=0`; cids 0–4).
  - `data.normalized_result.schema.tables[rtree_line_zm_geometry].columns_completeness`: envelope `unsupported`; CLI-derived `complete`.
- Remaining fields match. Counts: T/I/V/Tr `13/8/0/18`; non-virtual columns `53`; kinds `9 table / 3 shadow / 1 virtual`.

Producing comparison command and evidence: `timeout 300 python3 -I -B rederive.py`, **exit 1**, **2026-10-23T04:34:26Z**. Exact output excerpts:

```text
FIELD-COMPARISON mismatches=2
MISMATCH VALUE schema.tables[rtree_line_zm_geometry].columns envelope=[] derivation=[{'cid': 0, 'name': 'id', 'declared_type': 'INT', 'not_null': False, 'default_sql': None, 'primary_key_position': 0, 'hidden': 0}, ...]
MISMATCH VALUE schema.tables[rtree_line_zm_geometry].columns_completeness envelope='unsupported' derivation='complete'
COUNTS T/I/V/Tr=13/8/0/18; nonvirtual-columns=53
KIND-COUNTS table=9, shadow=3, virtual=1
```

The omitted portion of the exact `columns` output contains the four remaining xinfo records shown in `cli-probe.out`. The CLI table-list and table-xinfo commands for this carrier each exited 0 at 04:35:09Z.

## Knowledge-document check

`corpus/knowledge/2026-10-23-r31-sqlite-positive.md` names both exact evidence ids in its Carriers table and gives the independently re-derived T/I/V/Tr counts:

- Line 25: `gpkg-curvepolygon` — `ev_4c282804977b2f03c53715d6d736277713e471ba1744e8eeb5fd1471754d7e3e`, `13/8/0/18`, 53 columns, `shadow, table, virtual`.
- Line 26: `gpkg-line-zm` — `ev_92b9b645011eb1aec86970a4fdf108da99f4598143ef9b9e739042979af03580`, `13/8/0/18`, 53 columns, `shadow, table, virtual`.

The doc's line 13 defines its column total as over non-virtual tables; my independent total is 53 for each. Its line 45 also describes the RTree virtual table as `column_count` 5, `columns_completeness: unsupported`, and `columns: []`, consistent with the two envelope values that differ from the CLI's richer xinfo result.

## Scratch artifact hashes

All scratch files are under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReDeriveGpkgB/`:

- `rederive.py` — `fae0fa33115b89135f99250cfbc4645f0afde6655f3c93c40c5360ac3b1c922e`
- `rederive.out` — `d3fb29e0898c9dc5ec6e208f4c7daf0755f8eadb0dc098589cf4e93a8170282c`
- `cli-probe.out` — `14b90e61fa6a3578084d28d556d4779de09bf4aed48999e5c24dda0caf15af7f`
- `knowledge-r31-sqlite-positive.md` (copied read-only from lane) — `9cb98595417c927bd223aadba4f582fffca5b39e43a52a7213c3830977aee3e2`
- `envelopes/gpkg-curvepolygon.json` (copied read-only from lane) — `28b8f99baa2dc2660ac5999977fa24fb4d734308425073cbfb32089ae94442b7`
- `envelopes/gpkg-line-zm.json` (copied read-only from lane) — `58c9fea04b318bef5d5fce6a4fff7d797f015acda73b671faaa1d3e8b689e490`

The copied envelope and knowledge-file hashes match their lane-source hashes. No carrier, lane file other than this report, or other repository state was modified.
