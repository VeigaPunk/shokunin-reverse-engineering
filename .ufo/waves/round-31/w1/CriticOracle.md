# CriticOracle — attack on the R31-C1 independent oracle

Seat: critic. Target: `tools/round-31/sqlite_oracle.py` at lane commit
35ba7c522dba55f9be27eb161d4254eacaa24330 (read-only). No REA invocation was made
(the assignment forbids it for this seat); REA semantics below come from reading the
frozen package on disk, labelled as such. All work happened 2026-10-23 between
04:10Z and 04:35Z.

**Bottom line.** The pure-Python byte parser holds on every assigned spec item and
agrees with four independent readers on 24 files. Two latent model defects exist in
the oracle's wrapper (`wal` shape; the `rows` docstring), one robustness gap (an
unbounded overflow-loop shape on a truncated page), and one structural limit: the
schema-inventory half (`kind`, flags, columns) is verified against the same upstream
SQLite, and the wrapper *rules* are transcribed from REA, so a REA rule bug that the
oracle copies is invisible by construction. C1 is not trivially met, but it is not
independent for the fields the claim's limits already concede.

## 1. What I ran

Every command ran from
`/fast/scratch/hyaku/kaidoku-r31/seats/w1/CriticOracle` with `TMPDIR=$PWD/tmp`,
capped by `timeout`, never touching the lane.

| # | Command (abridged) | Exit | UTC | Output |
|---|---|---|---|---|
| 1 | `python3 -I -B <lane>/tools/round-31/sqlite_oracle.py /fast/scratch/hyaku/kaidoku-r31/carriers/*.{db,sqlite,gpkg}` | 0 | 04:11:40Z | `out/oracle-carriers.txt` |
| 2 | `python3 -I -B oracle_instr.py <same 12>` (copy with b-tree-path counters; lane file untouched) | 0 | 04:12:51Z | `out/oracle-instr.jsonl` |
| 3 | `.venv/bin/python xcheck.py <12 carriers> fx/{deep,ghost,idxcase,ps65536,ps65536r32,reserve512,rowid1,shapes,trigcase,u16be,u16le,varint9}.db` (byte parser vs apsw vs sqlite3 CLI vs stdlib) | 0 | 04:30:04Z | `out/xcheck.txt`, `out/xcheck.json` |
| 4 | `.venv/bin/python xderived.py <same 24 files>` (oracle's PRAGMA fields vs apsw's SQLite 3.54.1) | 0 | 04:30:16Z | `out/xderived.txt`, `out/xderived.json` |
| 5 | `.venv/bin/python mutate.py` (14 oracle mutants x 23 files) | 0 | 04:17:56Z | `out/mutate.json` |
| 6 | `.venv/bin/python` field-coverage census over the 12 carriers | 0 | 04:16:17Z | `out/coverage.txt` |
| 7 | `_varint` vectors (spec-derived encoder) + hand-built `fx/varint9.db` vs apsw | 0 | 04:23:04Z | transcript below |

Exit codes are the shell's `$?` for each pipeline; none produced stderr
(`out/*.err` are empty, sha256 `e3b0c442…`). `spec.html` was fetched at
04:10:40Z, `trig.html` at 04:19:31Z.

Cross-check summary lines (verbatim):

```
checked=24 disagreements=0 []          # out/xcheck.txt  (4 readers)
checked=24 disagreements=0 []          # out/xderived.txt (cross-build PRAGMA fields)
```

Readers: (A) the oracle's byte parser; (B) apsw 3.54.1.0 with its own bundled SQLite
3.54.1; (C) `/usr/bin/sqlite3` 3.54.0, a separately linked CLI binary (`ldd` shows no
`libsqlite3.so`); (D) Python 3.14 stdlib `sqlite3` 3.54.0 against system
`libsqlite3.so.0`. C and D share upstream source but not linkage; B is a distinct
build. The 24 files are the 12 frozen carriers plus 12 locally built fixtures (three further
probe files — `fx/negrowid.db`, `fx/waldb.db`, `fx/walsnap.db` — are deliberately
outside the four-reader set; see §8).

## 2. Spec-item verdicts

Source for items 1-6: <https://www.sqlite.org/fileformat2.html> (opened 2026-10-23,
sha256 `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2`); line
numbers are raw-HTML lines of the served bytes.

### 2.1 Page size 1 means 65536 — HOLDS

Spec, spec.html:278: `value 1 representing a page size of 65536`. Oracle:
`read_header` maps `ps = 65536 if ps == 1 else ps` and rejects non-power-of-two
`ps < 512`. Counterexample search: `fx/ps65536.db` has page-size field `1`; the oracle
reads `page_size: 65536`, `usable: 65536`, and its single 70,051-byte schema row
matches apsw, the CLI and stdlib (`out/xcheck.txt`, row `ps65536.db`,
`"apsw_match": true, "stdlib_match": true, "cli_match": true`). Mutant
`page1-magic-ignored` (treat any field as itself) is detected on the two 64 KiB
fixtures, and on **0/12 carriers** (out/mutate.json) — no carrier uses this encoding.

### 2.2 Reserved bytes / usable size — HOLDS

Spec, spec.html:371: `"reserved space" size in the 1-byte integer at offset 20`; the
usable size is the page size less that byte. Oracle: `return ps, ps - data[20], enc`
and every payload computation uses `usable`. Counterexample: `fx/reserve512.db`
(page 512, reserved 32, usable 480) parses identically to all three SQLite readers,
including two overflow rows and an interior root. Mutant `reserved-ignored`
(`usable = ps`) **raises "byte parser and libsqlite3 disagree"** on both fixtures and
on 0/12 carriers (all carriers have reserved 0 — `out/xcheck.txt`). The oracle does
not enforce the spec's usable-size floor (spec.html:381-382: `allowed to be less
than 480.`); a file violating it is rejected by libsqlite3 at open, so
`expected_report` still aborts rather than misreport.

### 2.3 Interior vs leaf table pages — HOLDS

Spec, spec.html:795-800: the two-byte cell count at offset 3, the array after the
8-byte leaf header or the 12-byte interior header. Oracle: page-1 header offset 100,
`hdr = 12 if kind in (2, 5) else 8`, recurses through every interior child and the
rightmost pointer. Every frozen carrier takes this path: each `sqlite_schema` root is
page 1 of type 5 (interior) with type-13 leaves — e.g. `proj-341.db`
`{"interior": 1, "leaf": 27, "states": {"5": 1, "13": 27}}`, `gpkg-curve.gpkg`
`{"interior": 1, "leaf": 3, "states": {"5": 1, "13": 3}}` (out/oracle-instr.jsonl).
Mutant `interior-header-8` raises on **12/12 carriers**; `page1-offset-0` raises on
12/12. A 3-level tree is also handled: `fx/deep.db` (512-byte pages, 12,000 tables)
reports `"max_depth": 3, "interior": 32, "leaf": 1715` and matches all readers.
Index b-tree page types (2, 10) are correctly refused for `sqlite_schema`.

Not applicable by construction: the spec's "cell content offset 0 means 65536"
(spec.html:801) — the parser never consults the cell-content-area field, so the
rule cannot be mis-applied.

### 2.4 Overflow formula X = U-35, M, K — HOLDS

Spec, spec.html:977: `Let X be U-35.`; 979-981: `M = ((U-12)*32/255)-23`,
`K = M+((P-M)%(U-4))`, local is `K if K <= X else M`. Oracle:
```python
x = usable - 35
m = ((usable - 12) * 32 // 255) - 23
k = m + ((size - m) % (usable - 4))
local = k if k <= x else m
```
and interior table pages skip payload entirely (matching "Interior pages of table
b-trees have no payload"). `/` truncation and `//` agree for U >= 480.

Carrier evidence that both branches of the `K`-vs-`M` choice are exercised: the
proj family has 2-6 overflowing `sqlite_schema` rows each (max payload 121010,
121010, 123499, 125678, 128180 bytes at U=4096, X=4061, M=489). Mutant
`local-always-K` raises on all 5 proj carriers; mutant `local-always-M` raises on all
5 — so at least one carrier row takes `K <= X` and one takes `K > X`. Fixtures pin
each branch explicitly: `fx/reserve512.db` (U=480, X=445, M=35) has two overflowing
schema rows with K=71 and K=209, both local K (mutant `local-always-M` raises on it),
and `fx/ps65536.db` / `fx/ps65536r32.db` (U=65536 / 65504, X=65501 / 65469, M=8199 /
8195) have K=70051 > X, local M (mutant `local-always-K` raises on both).
Mutant `overflow-final-page-uncapped` (`payload += op[4:]`) raises on
`fx/reserve512.db`: the `min(usable-4, ...)` cap is load-bearing because the reserved
region would otherwise be spliced into the payload mid-string. No frozen carrier
depends on that cap for its parsed values.

### 2.5 Varint 9th byte — HOLDS

Spec, spec.html:869-870: `The lower seven bits of each of the first eight bytes and
all 8 bits of the ninth byte are used to reconstruct the 64-bit twos-complement
integer.` Oracle returns `(v << 8) | b[i+8]` after eight 7-bit groups, terminating at
nine bytes even when the ninth has its high bit set. Spec-derived vectors
(0, 127, 128, 16383, 16384, 2^35-1, 2^56-1, 2^56, 2^56+1, 2^63, 2^64-1) all decode
correctly and consume exactly the encoded length (transcript, 04:23Z). End-to-end:
`fx/varint9.db` is a hand-built 512-byte database whose `sqlite_schema` rowid uses the
9-byte form for 2^56 = 72057594037927936; the oracle returns that rowid and apsw
returns `[(72057594037927936, 't', 'CREATE TABLE t(x)')]`; `expected_report` builds a
report with no disagreement. Reserved corner: a *negative* schema rowid (also a
9-byte varint) is rejected by SQLite as `CorruptError database disk image is
malformed`, while the same hand-built layout with rowid 1 is accepted and matches the
oracle; the oracle's unsigned decode of the negative form returns 2^64-1 and
`expected_report` aborted with `DatabaseError database disk image is malformed`
(observation: the abort is at the libsqlite3 reader, so no wrong rowid is emitted).
Conclusion: not reachable in a well-formed `sqlite_schema` except the >=2^56 rowid
case, which the fixture exercises.

### 2.6 Serial types — HOLDS

Spec, spec.html:1180-1181: odd N>=13 `Value is a string in the text encoding and
(N-13)/2 bytes in length`; even N>=12 blobs; 8/9 are 0/1; 10/11 `Reserved for
internal use ... will never appear in a well-formed database file`. Oracle maps
0/1-6/7/8/9/12+/13+ exactly and raises `OracleError` for 10 and 11. Carrier census
(out/mutate.json `serial_types`): types 0, 1, 2, 8 and odd text types are exercised;
mutant `serial-8-as-null` raises on **10/12 carriers** (the two Chinook files are old
schema-format databases that store those integers as type 1/2, so they do not
discriminate). Types 3-6 need a root page > 65535 (no carrier); 7 and blob types
cannot occur in `sqlite_schema`; 9 cannot (rootpage 1 is the schema itself). So the
well-formed reachable set is covered.

### 2.7 Text decoding per header encoding — HOLDS

Spec, spec.html:308-309 (encoding field 1=UTF-8, 2=UTF-16le, 3=UTF-16be) and 1181
("in the text encoding"). Oracle keys `PY_CODEC` off header bytes 56..60. Fixtures
`fx/u16le.db` and `fx/u16be.db` (created with `PRAGMA encoding`, non-ASCII table,
index, view and trigger names) round-trip through the oracle exactly as apsw and the
CLI decode them (`oracle_encoding` == `apsw_encoding`, all row fields equal). Mutant
`text-always-utf8` raises on both fixtures and on **0/12 carriers** — every frozen
carrier is UTF-8 (`"oracle_encoding": "UTF-8"` on all 12), so C1 does not exercise
this branch. BOM handling also matches REA: Node `TextDecoder(..., {ignoreBOM: true})`
preserves U+FEFF, and so does Python's codec.

### 2.8 Trigger case-folding rule — HOLDS AS A TRANSCRIPTION, NOT INDEPENDENTLY

The spec's only folding statement is the NOCASE rule, spec.html:1239: `Only ASCII
characters are case-folded.` The oracle's `_fold` maps `A-Z` to lowercase only, which
matches that rule; `sqlite_schema.tbl_name` for a trigger stores the spelling written
after `ON` (lang_createtrigger.html:4424: `A trigger normally exists in the same
database as the table named`), so normalization is a semantic choice, not a spec
mandate. Observation: SQLite canonicalizes *index* `tbl_name` at CREATE time
(`fx/idxcase.db`: `CREATE INDEX i_upper ON FOO(x)` stored as `Foo`), so for
SQL-created schema only triggers can carry a non-canonical target spelling
(`PRAGMA writable_schema` or a non-SQL writer could still do it).

Fixture `fx/trigcase.db` (`CREATE TRIGGER trg_upper ... ON FOO` over table `Foo`,
`... ON casetab` over `CaseTab`) makes the rule observable: the oracle reports the
canonical `Foo`/`CaseTab`; mutant `fold-identity` differs on this fixture and on no
carrier. That mutant is detected on **0/12 carriers** because, per `out/coverage.txt`,
`triggers_fold_diff` is `[]` for all 12 — every carrier trigger's stored `tbl_name`
already equals a table name exactly. The implementation is a faithful transcription
of `sqliteIdentifierKey` at
`rea-agents/dist/sqlite/SqliteDatabaseInspection.js:76` (identical ASCII-only fold)
and `triggerTable` at :167-174; it is not an independent derivation of the rule.

## 3. Cross-check outputs and path coverage

Per carrier (out/xcheck.txt; `apsw_match/stdlib_match/cli_match` all true):
`rows` = sqlite_schema rows; page size; interior/leaf pages; overflow rows.

| carrier | rows | page | interior/leaf | overflow rows | max payload |
|---|---|---|---|---|---|
| proj-341/350/361/370/371 | 99/99/99/101/102 | 4096 | 1 / 27,28,27,28,27 | 2,2,2,2,6 | 121010-128180 |
| chinook.sqlite / chinook-autoinc | 22 / 23 | 1024 | 1 / 8,7 | 0 | 702 / 675 |
| gpkg-* (5 files) | 39 | 4096 | 1 / 3 | 0 | 512 |

So: **all 12 carriers take the interior-page path**; **5 of 12 (the proj family) take
the overflow path**, with both local-length rules exercised; none takes the
reserved-byte, 64 KiB, UTF-16, WAL or 3-level paths. Full per-file b-tree records are
in `out/oracle-instr.jsonl`; the fixture that takes each uncovered path is listed in
§8.

Cross-build agreement of the PRAGMA-derived fields (out/xderived.txt, 24/24
identical) means system libsqlite3 3.54.0 and apsw's 3.54.1 return the same
`table_list` type/ncol/wr/strict and the same `table_xinfo` rows for every file,
including the 26-28 WITHOUT ROWID proj tables, the 3 shadow + 1 virtual tables per
GeoPackage, generated-column hidden flags in `fx/shapes.db`, and the `unknown` kinds
in `fx/ghost.db`.

## 4. Independence split: which fields come from where

From libsqlite3 (system 3.54.0 through Python; REA's own node:sqlite is a different
build of the same upstream, 3.53.4 per claims.json — I did not verify that version):

- `schema.tables[].kind`, `.without_rowid`, `.strict`, `.column_count` — `PRAGMA table_list`;
- `schema.tables[].columns[]` — `cid, name, declared_type, not_null, default_sql,
  primary_key_position, hidden` — `PRAGMA table_xinfo`;
- the table-name set used to canonicalize a trigger's target, and the unresolved
  virtual-table set (`type=virtual, ncol=0`) used by the shadow heuristic.

From code with no SQLite in it:

- `artifact.path` (`os.path.abspath`; REA uses Node `resolve` at
  `dist/cli/sqliteCommands.js:41`, equal for absolute paths), `artifact.sha256`
  (`hashlib`; matches `sha256sum` on 12/12 carriers and the frozen `carriers.tsv`),
  `artifact.bytes` (`getsize`);
- `database_encoding` (header bytes 56..60);
- every `sqlite_schema` row: `type`, `name`, `tbl_name`, `rootpage`, `sql`, and their
  row order — hence table/index/view/trigger `name`, `sql`, `root_page`, index
  `table`, view `sql`, and the trigger `name`/`sql`; the trigger `table` is this value
  after the oracle's fold;
- `wal` presence (`lexists`, but see §6.1);
- the shadow-prefix matcher and the `kind`/`column_count`/`completeness` mapping
  rules — plain code, but copied from REA.

The oracle also **refuses** to answer if libsqlite3's rows differ from the byte
parser's (`OracleError("byte parser and libsqlite3 disagree on sqlite_schema")`).
That guard is live: every misparse mutant raises it (10-12 of 12 carriers for the
row/offset mutants), so on the frozen input the report's row fields are double-read.

**Is the C1 bar trivially met by REA?** No. The byte-level half (file opened, pages
walked, records decoded, `sql` text, root pages, encoding, digests) is genuinely
independent code checked against two other engines, and REA must reproduce it exactly
on 12 files with 39-102 schema rows each, including 100+ KB overflowing statements.
But the field-for-field bar is **weak for the schema-inventory half**: kind and
columns are compared against the same upstream SQLite, so it proves REA's SQL calls
return what SQLite returns, not that REA's interpretation is right; and the wrapper
rules are transcriptions, so a REA rule bug that the oracle copied is undetectable by
construction. For those fields the oracle is a conformance harness, not an oracle.

## 5. REA wrapper bugs this control would not detect

The assignment asks which wrapper bugs the oracle cannot see. There are two grades:
one that C1's frozen input cannot discriminate (the oracle would catch it on an input
no carrier provides), and one the oracle cannot catch even in principle because it
implements the same rule.

**Named example: `triggerTable` returns the stored spelling instead of resolving it.**
REA resolves a trigger's written `tbl_name` against `PRAGMA table_list` with an
ASCII-only fold (`triggerTable`, Inspection.js:167-174; `sqliteIdentifierKey`:76). If
that lookup were dropped — an easy regression, since the index branch deliberately
keeps the raw spelling — C1 would still pass 12/12: no carrier trigger's stored
`tbl_name` differs from its table name even in case (`triggers_fold_diff: []` for
12/12, `out/coverage.txt`), so raw and resolved values coincide on every carrier.
`fx/trigcase.db` is the discriminating input (stored `FOO`, `foo`, `casetab` over
tables `Foo`, `CaseTab`); the `fold-identity` mutation changes its report and no
carrier's. A Unicode-`toLowerCase()` variant is even less observable: both sides of
the lookup are folded with the same function, so it can only surface when two stored
names collide under the faulty fold, and no carrier or fixture has non-ASCII names.
The same blind spot covers every unexercised branch with a *correct* oracle: strict
flag (no carrier has a STRICT table), hidden columns (all hidden=0), UTF-16 decoding,
64 KiB pages, reserved bytes, WAL, and virtual tables with `ncol=0` (GeoPackage's
rtree reports ncol=5, so the `unknown`/`column_count:null` path never fires).

**Second, harder case (undetectable even with ideal input): the shadow-prefix
classification rule.** Both REA (Inspection.js:181-188, 236) and the oracle classify
any ordinary table whose ASCII-folded name starts with `<unresolved virtual>_` as
`kind:"unknown"`. `fx/ghost.db` proves the rule over-reaches: `ghost_node_extra` is a
plain table yet is reported `kind: unknown` (and REA would refuse row inspection on
it), while `ghost` is `virtual, column_count null, columns_completeness unsupported`.
Because the oracle re-implements the same heuristic rather than an independent
definition of a shadow table, a defect in that rule is invisible to C1 by
construction. I classify this as a **tradeoff** (fail-closed when SQLite cannot
resolve a virtual table's module) that the canonical Rust judge must own, not as a
defect the oracle can be patched into exposing — patching it alone would manufacture
a false counter failure.

## 6. Defects and smallest safe corrections

1. **`wal` is modelled with the wrong shape (latent; not exercised by C1).**
   `expected_report` returns `None` or the string `"present"`. REA's field is
   `artifact | null` — `dist/domain/sqlite/sqliteDatabase.js:94
   wal: artifactSchema.nullable()`, populated at `dist/sqlite/SqliteDatabaseProvider.js:171`
   from `SqliteDatabaseSnapshot.js:140-145` as
   `{path: "<path>-wal", sha256, bytes}`. Observed (command
   `python3 -I -B -c "import sys;sys.path.insert(0,'<lane>/tools/round-31');import sqlite_oracle as o;print(o.expected_report('fx/walsnap.db')['wal'])"`,
   exit 0, 04:18Z): `wal field: 'present'`. Worse, the oracle reads only the
   main file (`open()` and `immutable=1`), so a schema change living only in the WAL
   would be silently invisible to the expected report while REA sees it. No carrier
   has a `-wal` (carrier directory holds 12 files only), so C1 is unaffected.
   Smallest safe fix: if `os.path.lexists(path + "-wal")`, raise `OracleError` ("WAL
   present: the oracle does not model a WAL snapshot") instead of emitting a string
   REA can never produce. Alternative: compute `{path, sha256, bytes}` and open
   libsqlite3 *without* `immutable=1` so the WAL is applied — more work, and the
   byte parser would need a WAL reader.
2. **`comparable()` docstring is false.** It says `engine.version`, `limitations` and
   `rows` are dropped; the code drops only `limitations` and `engine.version`.
   Harmless today because REA returns `rows: null` at database scope
   (`readRows` returns null when `input.table` is undefined), but it will mislead the
   next editor. Smallest fix: correct the docstring (or pop `rows`, which would also
   work since `expected["rows"]` is null).
3. **Counter, not oracle: an oracle exception aborts the counter.** `measure()` calls
   `oracle.expected_report(r["path"])` outside its try/except, so a malformed or
   changed carrier produces a traceback instead of `P1-fail` for that row. Carriers
   are sha256-pinned and chattr +i, so this is belt-and-braces; the smallest fix is
   to catch `Exception` per carrier and record `P1-fail`, keeping the target-line
   accounting honest.
4. **Overflow chain can spin on a truncated page.** `while len(payload) < size` reads
   `op = data[(ov-1)*ps:ov*ps]`; if `op` is shorter than 5 bytes, `payload` does not
   grow while `ov` can remain nonzero, so nothing forces progress. A malformed file
   (not a carrier, not a mutant) would hang the counter, which does not time-bound
   `expected_report`. Smallest fix:
   `if not ov or len(op) < 5: raise OracleError("overflow chain ends early")` before
   appending, or cap iterations by `size // (usable - 4) + 2`.
5. **No usable-size floor.** The spec says the usable size is not allowed to be less
   than 480 (spec.html:381-382: `allowed to be less than 480.`). The oracle accepts
   smaller values; libsqlite3 rejects the file at open, and `expected_report` then
   aborts, so no wrong expectation escapes. Optional check.
6. **Tradeoff, do not "fix" in the oracle alone:** the shadow-prefix heuristic (§5)
   and the trigger-fold rule are REA semantics. Any change here must land with a
   matching REA-side decision and a committed input that discriminates it.

## 7. Sources opened

1. <https://www.sqlite.org/fileformat2.html> — accessed 2026-10-23, sha256
   `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2`. Quotes
   (raw-HTML line): line 278 `value 1 representing a page size of 65536`; line 371
   `"reserved space" size in the 1-byte integer at offset 20`; line 801
   `A zero value for this integer is interpreted as 65536`; line 869 `The lower seven
   bits of each of the first eight bytes and all 8 bits of`; line 977 `Let X be U-35.`;
   line 1181 `and (N-13)/2 bytes in length`; line 1239 `Only ASCII characters are
   case-folded`.
2. <https://www.sqlite.org/lang_createtrigger.html> — accessed 2026-10-23, sha256
   `e9fee81d281f5bb8dc62f665d90a63a61ac943ef7da740f2ffbba99a8f73d257`. Quote
   (raw-HTML line 4424): `A trigger normally exists in the same database as the table
   named`; and line 4208 `must be an unqualified table name`.
3. Local frozen package `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`
   (rea-agents 6.5.0, `version` field verified 6.5.0; read only, never run):
   `dist/sqlite/SqliteDatabaseInspection.js:76,167,236,239,249`;
   `dist/domain/sqlite/sqliteDatabase.js:94,99`;
   `dist/sqlite/SqliteDatabaseProvider.js:171`;
   `dist/sqlite/SqliteDatabaseSnapshot.js:140-145`;
   `dist/cli/sqliteCommands.js:41`.

## 8. Artifacts

All under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CriticOracle/`; every file
(scripts, fixtures, raw outputs, mutants, fetched pages, transcripts) is listed with
sha256 and UTC mtime in `manifest.sha256`, whose own sha256 is
`b0c50afc80d19725a5d1fd16d4d9fbdd721e64691e2ed3bcac8dfae136cf5940` (55 file
entries; `.venv/`, `tmp/` and Python bytecode caches excluded). Key items:

- `oracle_instr.py` `d14ca001efd94e0b5deadc21ee91c3a893a18d4bb1d00951885439149a0f8753`
  — copy of the lane oracle plus b-tree-path counters; `out/oracle-instr.diff`
  `a10681f849b99761fc2a3b6d9b1e1c5ed4ace65b6781af67131a1732f65891e5` (30
  changed lines plus the two file headers, instrumentation only; the lane file was
  not modified).
- `xcheck.py` `8cb4acf383e7b63e098ae02ba75a37df369487cf4d8e84a77e38e6ff3ea69d57`
  — four-reader `sqlite_schema` comparison (accepts an explicit file list).
- `xderived.py` `034de3e5f8b5144c165aa2fb03482dc10762574355cf2c7f61c1c16a31df5be5`
  — cross-build check of kind/flags/columns (accepts an explicit file list).
- `mutate.py` `429212121b3048485a88aeec3570cefa89d1e1c7b10def64acb2192288bfc339`
  — 14 mutants; `out/mutate.json` `3934dbe38a822b7ba0c45cb2dc010b435c724939037e536a5d3776058a55fe11`
  is the detection matrix.
- `out/xcheck.json` `396d4ac95969ba9c278ae63e0c9c9481f64254f8c18c555031c1eae926b2333c`
  and `out/xcheck.txt` `6d0dd0a96543959bca2574abbf829be0ce3682897f987868add8a0ce6d85fb26`;
  `out/xderived.json` `859cb696fcd6d10c347258b8854c38b9b05a2f787ec56cb983346555c7e6db43`
  and `out/xderived.txt` `04309d2ba363ca235eab5780a94d92907edddae95bbad191b99a85fe5bbd820b`;
  `out/coverage.txt` `a3ca6c2e963b2e5e0763546df915b3b3e5cd7410fc195ad304e37d30ed8a8f1a`;
  `out/oracle-instr.jsonl` `0b0b4205c97ed5c2cdede88f6a7dea2b4bad86d6ee0147be44f29d1eb694bb3c`;
  `out/oracle-carriers.txt` `1698faa82121e982cf41e9488bfd5d4372b00658bc9f14e71663c7e7680063fe`.
- Fixtures in the four-reader set: `fx/ps65536.db`, `fx/ps65536r32.db`,
  `fx/reserve512.db`, `fx/u16le.db`, `fx/u16be.db`, `fx/shapes.db`,
  `fx/trigcase.db`, `fx/idxcase.db`, `fx/ghost.db`, `fx/deep.db`, `fx/varint9.db`,
  `fx/rowid1.db`. Probe files outside that set: `fx/negrowid.db` (SQLite rejects the
  file by design) and `fx/waldb.db`/`fx/walsnap.db` with their `-wal`/`-shm`
  siblings. All hashes are in the manifest.

## 9. Installs

- `apsw` 3.54.1.0 (bundled SQLite 3.54.1), installed 2026-10-23 04:11Z via
  `uv venv .venv` + `uv pip install --python .venv/bin/python apsw` (PyPI, official
  channel), reason: a second, separately built SQLite reader for the cross-check.
  No pacman transaction was attempted.

## 10. Verdict to the L1

- Oracle byte parser: **holds** on page-size magic, reserved bytes, interior/leaf
  pages, overflow X/M/K and the K/M branch choice, varint 9th byte, serial types, and
  per-encoding text. **Holds as transcription** on trigger folding.
- Oracle wrapper: **one fixable defect before any WAL-bearing input**
  (`wal: "present"`, §6.1) and **one cosmetic defect** (`comparable` docstring).
  Neither touches the frozen 12 carriers, so C1's target line is not at risk from
  them.
- C1's independence: full for bytes/text/root pages/digest/encoding; cross-build,
  not independent, for kind/flags/columns; self-referential for the wrapper mapping
  rules. If the claim's `limits` are read as covering exactly this, the claim is
  honest; if any sentence suggests the oracle independently derives
  classification or column projection, it overstates.
- If a counter prints `PIN … absent or altered`, stop, as instructed. No such output
  occurred here; all 12 carrier sha256 values match `carriers.tsv` (04:15Z) and
  `sha256sum`.
