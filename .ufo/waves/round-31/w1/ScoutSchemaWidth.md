# ScoutSchemaWidth — C1 carrier schema width, disclosed before data

Round 31, wave 1 seat. Question: how wide is the C1 evidence? Per carrier and per
producer: table/index/view/trigger/column counts, kinds present, the longest
`sqlite_schema.sql`, whether the oracle's byte parser descends interior b-tree
pages or reads overflow chains, and the sha256 of the canonical schema JSON.
No claim data exists yet; this is the pre-data width record.

## Method and provenance

- FROZEN_ORACLE `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/sqlite_oracle.py`,
  sha256 `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b`.
  It was imported, not modified: the instrumentation is a **copy** at
  `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ScoutSchemaWidth/oracle_instrumented.py`,
  sha256 `e299b06d4f2b1c4b1e8dc315c3e6a9ccc6daca589a1fcc42a27a3b214fd9ff3d`.
  `diff -u` (command below, exit 1 = differs) adds only a `LAST_STATS` dict and its
  updates: page-kind census in `walk`, a chain/pages counter and per-row record in the
  overflow branch, and the copy-back before `return`. No parsing logic changed.
- Command (exit 0, 2026-10-23T04:13:18Z to 2026-10-23T04:13:19Z):
  `cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/ScoutSchemaWidth && TMPDIR=$PWD/tmp timeout 900 python3 -I -B width.py`
- Equivalence gate inside that run: for every carrier, `canonical(instrumented.expected_report(p))
  == canonical(sqlite_oracle.expected_report(p))` (assert, passed 12/12), so the copy
  reports exactly the frozen oracle's `expected_report` output. Determinism: two
  consecutive runs produced byte-identical `out/width.json`
  (`cmp out/width.run1.json out/width.json`, exit 0).
- Carrier attribution: all 12 files at `/fast/scratch/hyaku/kaidoku-r31/carriers/`
  re-hashed read-only; sha256 and byte length match
  `corpus/evidence/round-31/c1/carriers.tsv` row for row (`mismatches= 0`,
  command `python3 -B -c` over the TSV, 2026-10-23T04:14Z). No file was written,
  moved or chattr'ed; REA was not run (out of scope for this seat).
- Canonical schema JSON key: `schema_sha256 = sha256(utf8(json.dumps(
  expected_report(path)["schema"], sort_keys=True, separators=(",", ":"),
  ensure_ascii=False)))`. The schema object is the oracle's scope-`database`,
  completeness-`complete` object, i.e. tables (name, sql, root_page, kind,
  without_rowid, strict, column_count, columns_completeness, columns[] with cid,
  name, declared_type, not_null, default_sql, primary_key_position, hidden),
  indexes, views, triggers. It excludes `artifact.path` (path-independent) and
  includes `root_page` (layout-dependent).
- `schema_identity` (weaker, for interpretation only) = same recipe over
  `[type, name, tbl_name, sql]` per sqlite_schema row, dropping root pages.
  `schema_shape` (weakest) = object names only, no SQL.

## Per-carrier width

`pages` is `schema pages walked` = interior + leaf pages of the sqlite_schema b-tree.
`int` lists interior page numbers; `ov` is overflow chains / overflow pages read.
`schema sha256` is the full canonical schema hash above.

| id | producer | page size | tables | idx | views | trig | columns | sqlite_schema rows | max sql (chars/B) | pages (int/leaf) | int | ov chains/pages | schema sha256 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---|
| proj-341 | proj | 4096 | 36 | 21 | 7 | 35 | 385 | 99 | 120947 / 120947 | 28 (1/27) | [1] | 2 / 30 | `9c940e14db1962347a83b816b0da38d58c13010a31750051ca6789901b044d46` |
| proj-350 | proj | 4096 | 36 | 21 | 7 | 35 | 385 | 99 | 120947 / 120947 | 29 (1/28) | [1] | 2 / 30 | `ac4f0f67b8daf639786b17b9747637cba20917e2a29f8219e20aff11d479384d` |
| proj-361 | proj | 4096 | 36 | 21 | 7 | 35 | 385 | 99 | 123436 / 123436 | 28 (1/27) | [1] | 2 / 31 | `75792393e70f4cb0798543a46dff832797c5e50365284793f837fc755b708d90` |
| proj-370 | proj | 4096 | 37 | 21 | 7 | 36 | 395 | 101 | 125615 / 125615 | 29 (1/28) | [1] | 2 / 31 | `341cfad23c14bfb289c74e044aa2296d1c20f00f9a78b9fb4ac57269231065c5` |
| proj-371 | proj | 4096 | 38 | 21 | 7 | 36 | 396 | 102 | 128117 / 128117 | 28 (1/27) | [1] | 6 / 36 | `ad1e6480904a3a238b31039498edf2be6ec8a05447f64929c4aa1fe9dcaa6773` |
| chinook | chinook | 1024 | 11 | 11 | 0 | 0 | 64 | 22 | 678 / 678 | 9 (1/8) | [1] | 0 / 0 | `c30aa0055777a688e2780e601a1a6bf207fa7e734987bf5553681978592026c0` |
| chinook-autoinc | chinook | 1024 | 12 | 11 | 0 | 0 | 66 | 23 | 651 / 651 | 8 (1/7) | [1] | 0 / 0 | `3631650b3e4eea16dd8ff7cd9feec939f122d61680841c8ae01614ca4d64f1dc` |
| gpkg-curve | gpkg | 4096 | 13 | 8 | 0 | 18 | 53 | 39 | 457 / 457 | 4 (1/3) | [1] | 0 / 0 | `d5d6c8ea489ac4c09eacb483c5e7fe7979503c5ecc47d9c68b90fca6c4160f5d` |
| gpkg-curvepolygon | gpkg | 4096 | 13 | 8 | 0 | 18 | 53 | 39 | 457 / 457 | 4 (1/3) | [1] | 0 / 0 | `28983ce91828b4c1b70d3bffaf47e1bab70af44d65894cd9f57c570c05d649d5` |
| gpkg-line-zm | gpkg | 4096 | 13 | 8 | 0 | 18 | 53 | 39 | 457 / 457 | 4 (1/3) | [1] | 0 / 0 | `6b2807b4863d46cc785db3bfd19f627718268799357324b10f4f662478666f65` |
| gpkg-multisurface | gpkg | 4096 | 13 | 8 | 0 | 18 | 53 | 39 | 457 / 457 | 4 (1/3) | [1] | 0 / 0 | `cf9358359db46e1571166e3404973251cb8ac57ed90da9d135bd278837025278` |
| gpkg-test-gpkg-nulls | gpkg | 4096 | 13 | 8 | 0 | 18 | 64 | 39 | 457 / 457 | 4 (1/3) | [1] | 0 / 0 | `dd409ed4182d777e9ac9e3e7d80c08b8b81992f49cb7f2491468f32a606e558f` |

All 12: text encoding UTF-8, reserved bytes per page 0, `wal` null, scope database,
rows null. Of the 740 sqlite_schema rows, 658 carry SQL and 82 have `sql` NULL
(40 proj, 2 chinook, 40 gpkg; all of type `index`, i.e. implicit autoindexes), so
the max is over the 658. Every SQL string on all 12 carriers is ASCII
(`str.isascii()`, 0 of 658 non-ASCII), so the char and byte maxima coincide; the
object holding the max is
`conversion_method_check_insert_trigger` for all five proj files, `Track`
(both chinook files) and `gpkg_geometry_columns` (all five gpkg files).
Canonical schema JSON size per carrier (bytes): proj 266722, 267387, 270036,
275410, 297528; chinook 15851, 15959; gpkg 18528, 18883, 18624, 18883, 20474.
Minimum 15851 (chinook), maximum 297528 (proj-371), total across 12 = 1504285.

### Kinds present

- proj (5/5): sqlite_schema row types `{table: 36-38, index: 21, view: 7,
  trigger: 35-36}`; `PRAGMA table_list` kinds all `table` (36, 36, 36, 37, 38);
  no virtual, no shadow table. All five carry `sqlite_stat1` (3 columns) and
  `versioned_auth_name_mapping` (4 columns); none carries `sqlite_sequence`.
  Table sets grow by producer version: 341/350/361 have the same 36 names;
  361 to 370 adds `coordinate_metadata` (8 columns) and widens `geodetic_datum`
  13 to 14 and `vertical_datum` 9 to 10 (385 to 395 columns); 370 to 371 adds
  `builtin_authorities` (1 column, 396).
- chinook (2/2): `{table: 11-12, index: 11}`; no views, no triggers; kinds all
  `table`. `chinook-autoinc` adds `sqlite_sequence` (12 tables, 66 columns) and
  loses 27 characters of max SQL (651 vs 678, `Track`).
- gpkg (5/5): `{table: 13, index: 8, trigger: 18}`, no views; `PRAGMA table_list`
  kinds `{table: 9, virtual: 1, shadow: 3}` — one R*Tree virtual table each
  (`rtree_curve_geometry`, `rtree_curvepolygon_geometry`,
  `rtree_line_zm_geometry`, `rtree_multisurface_geometry`,
  `rtree_test_gpkg_nulls_geom`; `column_count` 5, `columns_completeness`
  "unsupported") and its three shadow tables (`_rowid`, `_node`, `_parent`,
  2 columns each).

**Column-count caveat (observation):** the `columns` figure is
`sum(len(table.columns))` from the oracle. The one virtual R*Tree table reports no
column objects by contract, so its 5 declared columns are excluded: gpkg carriers
have 53 reported columns over 13 tables (58 declared slots), and
`gpkg-test-gpkg-nulls` 64 over 13 tables (69 slots, its feature table has 13
columns instead of 2). All other tables on all 12 carriers are
`columns_completeness: complete` (5 gpkg carriers each have exactly one incomplete
table; the other 7 carriers have none).

## Distinct schemas

- Overall: **12 distinct / 12 carriers** (no two carriers share a canonical
  schema hash).
- Per producer: proj 5 distinct / 5 carriers; chinook 2 / 2; gpkg 5 / 5.
  No cross-producer hash collision.
- Under the weaker `schema_identity` key (drops `root_page`): still 12 distinct.
- Under the weakest `schema_shape` key (object names only, no SQL): 10 groups.
  The only collapse is proj-341 + proj-350 + proj-361
  (`04bff660a827e694f7826534d2eb7901d46b23e7d9e985865cdae09382d8e55a`), which
  have identical name sets and identical counts (36/21/7/35, 385 columns).
  proj-341 and proj-350 are the closest pair: identical object names, identical
  per-table column lists and identical root pages, so the *only* difference is the
  SQL text of one object, `grid_alternatives` (plus file size, 2021 vs 2074
  pages); that single difference moves the full hash and the identity hash while
  every count and the max SQL length (120947) stay equal.  Separately,
  gpkg-multisurface and gpkg-curvepolygon share the same canonical JSON byte
  length (18883) yet are distinct schemas.
  Aggregate totals: 271 tables, 167 indexes, 35 views, 267 triggers, 2352
  reported columns, 740 sqlite_schema rows; by producer proj 183/105/35/177 and
  1946 columns, chinook 23/22/0/0 and 130, gpkg 65/40/0/90 and 276.

## Interior pages and overflow chains

- **Interior pages: all 12 carriers.** In every file the sqlite_schema root
  (page 1, offset 100) is a table b-tree **interior** page (type 5), never a leaf:
  `interior=[1]` for all 12. The walk therefore recurses into child pages for every
  carrier, reading 3 to 28 leaf pages (gpkg 3, chinook 7-8, proj 27-28).
  Depth is 2 (one interior root, leaves only): no second-level interior page exists
  on any carrier.
- **Overflow chains: the 5 proj carriers only.** Chain count / pages read:
  proj-341 2/30, proj-350 2/30, proj-361 2/31, proj-370 2/31, proj-371 6/36.
  The long chain is always `conversion_method_check_insert_trigger`
  (record payload 121010, 123499, 125678 or 128180 bytes, of which only 2342,
  739, 2918, 1328 bytes are local), the short one `other_transformation`
  (payload 4497). proj-371 adds four more single-page chains:
  `helmert_transformation_insert_trigger` (7014 B),
  `grid_transformation_insert_trigger` (7912 B),
  `other_transformation_insert_trigger` (4585 B),
  `concatenated_operation_step_insert_trigger` (5566 B).
  chinook (both) and all five gpkg carriers read **zero** overflow chains; their
  longest SQL (678 B and 457 B) fits the local-payload threshold.
- So the C1 evidence set exercises: multi-page b-tree descent everywhere, and
  overflow reassembly on 5 of 12 carriers (14 chains, 158 overflow pages; the
  longest single chain is 31 pages, proj-371's
  `conversion_method_check_insert_trigger`). It does not exercise a second
  interior level, and 7 of 12 carriers never touch the overflow path.

## Conclusions

- Observation: the 12 frozen carriers re-hash exactly to the frozen TSV; the width
  numbers above are attributed to those bytes.
- Observation: width is 12 distinct canonical schemas (proj 5, chinook 2, gpkg 5),
  ~1.50 MB of canonical schema JSON, 740 schema rows, 2352 reported columns.
  Counts alone do not identify a schema: proj-341/350 share every count yet are
  distinct; name sets alone collapse proj-341/350/361 into one group.
- Observation: the frozen oracle, on these carriers, descends interior pages for
  all 12 and reads overflow chains for 5.
- Inference: a "12-carrier" sample is 12 independent schema documents rather than
  12 views of one shape, which is what makes a per-carrier equality predicate
  (R31-C1) informative; the C1 oracle comparison covers the multi-page and
  overflow reassembly paths, but a schema b-tree deeper than two levels and a
  UTF-16 database are untested by this set.
- Unknown: whether REA 6.5.0's `inspect_sqlite_database` envelope reproduces these
  exact schema objects and how many bytes its envelopes take — C1/C2 measure that;
  this seat did not run REA. Unknown: widths of the 23 C2 mutants (not C1 carriers,
  not measured here). Unknown: whether `PRAGMA table_list` on another SQLite build
  (REA's bundled one) reports the same virtual/shadow census as the system
  libsqlite3 used by the oracle; the oracle asserts only that its own two readers
  agree on sqlite_schema rows.

## Artifacts (scratch, not committed by this seat)

Directory `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ScoutSchemaWidth/`:

| path | sha256 | note |
|---|---|---|
| `oracle_instrumented.py` | `e299b06d4f2b1c4b1e8dc315c3e6a9ccc6daca589a1fcc42a27a3b214fd9ff3d` | copy of frozen oracle + `LAST_STATS` only |
| `width.py` | `4fe6d5121d6b39fe2eb565259010a0f38e18c4b550a0790bd4f380ca90825cec` | driver (imports both oracles) |
| `out/width.json` | `ab7e25b272b2e0f8c3b4d0335d91413eb19750a42c0e8204ab284a454cb4020e` | full per-carrier record + group tables |
| `out/width.run1.json` | `ab7e25b272b2e0f8c3b4d0335d91413eb19750a42c0e8204ab284a454cb4020e` | first run, byte-identical |
| `out/width.stdout.txt` | `af4a48198391ecaa7713a962b4ee81e764c0168db75ef5ba741e3986966e3c63` | counter stdout with CMD/START/EXIT/END |

No tool was installed or updated for this seat. No processes left running.
