# CriticOracleIndep — R31-C1 oracle independence after data

**Seat:** critic, wave 2. **Attack:** whether C1's 12/12 agreement is trivially guaranteed because REA and the oracle both relay SQLite. **Lane revision read:** `1288285eed81395e6af7c279a173b117b2c2eaa3`; claims frozen at `35ba7c52`. Read-only; no REA invocation, no lane/fleet writes, no installs.

## Verdict

- **“12/12 is trivially guaranteed because both sides relay SQLite”: fails.** The oracle reads the `sqlite_schema` b-tree with a separate pure-Python parser, derives encoding from header bytes, and independently hashes the source. Those fields, plus order comparison, provide real checks; the two SQLite implementations also differ (system SQLite 3.54.0 vs REA's Node SQLite 3.53.4).
- **“The oracle is independent field for field”: fails.** Most leaf values (86.5% by a leaf-weighted count) are cross-build comparisons of the same SQLite catalog. Every REA-invented output rule is copied into the oracle; the rules for `kind: unknown`, null `column_count`, and trigger target folding were not exercised by these carriers.
- **Carrier exercise of logic:** `columns_completeness` (both values) and omission of virtual-table columns are exercised; the `unknown` kind override, null-count rule, and trigger-case-fold path are not. A local probe of the oracle on the wave-1 `ghost.db` fixture shows the prefix heuristic can label a `table_list`-ordinary table `unknown`.

**Conclusion:** 12/12 is not tautological. It supports faithful projection/ordering of the published files' catalog and byte identity of REA's snapshot copy. It does not independently validate SQLite's catalog values or the semantics of REA's special classification rules. The entry's independence wording should distinguish these scopes.

## Compared report and field map

The C1 judge compares `comparable(normalized_result)` with the oracle report using Python dict equality (`c1-sqlite-positive.py:74-80`), so keys and list order matter. `comparable()` removes only `limitations` and `engine.version`; all other normalized-result fields are compared. The committed-envelope check is separate. In the compared report, top-level keys are `artifact`, `wal`, `engine`, `database_encoding`, `schema`, and `rows`; `schema` has `scope`, `completeness`, `tables`, `indexes`, `views`, and `triggers`.

Legend: **RELAY** = both sides ask SQLite for the catalog value (different SQLite builds); this tests REA's query/projection, not an independent authority on that value. **INDEP** = oracle uses non-SQLite file parsing/hashing. **RULE** = REA-defined mapping/output convention; the oracle copies the rule. **CONST** = fixed or forced at database scope. REA line numbers refer to the pinned `dist/sqlite/SqliteDatabaseInspection.js` unless stated otherwise.

| Compared field | REA code that computes it | Class / oracle computation | Carrier exercise? |
|---|---|---|---|
| `artifact.path` | Provider passes `snapshot.artifact` (`SqliteDatabaseProvider.js:170`); snapshot stores `path` (`SqliteDatabaseSnapshot.js:127-131`) | Input-path echo; oracle uses `os.path.abspath(path)` | Yes, 12/12; absolute paths make this a low-information echo. |
| `artifact.sha256`, `artifact.bytes` | Snapshot `readObservedArtifact` result (`SqliteDatabaseSnapshot.js:127-131`) | **INDEP:** `hashlib` and `os.path.getsize` on the original file | Yes, 12/12; bytes/hash equal the frozen pins, checking that the copied snapshot matches the source. |
| `wal` | Snapshot detects/captures a WAL and returns null or `{path, sha256, bytes}` (`SqliteDatabaseSnapshot.js:132-155`); provider relays it (`SqliteDatabaseProvider.js:171`) | Oracle returns `None` or the string `"present"` from `lexists` | **No branch exercise:** all 12 are null. The oracle's non-null shape is incompatible with REA's; any WAL-bearing input would expose a latent oracle defect, not a REA mismatch. |
| `engine.name` | Literal `"SQLite"` (`Inspection.js:411`) | Same literal | Compared, but constant on both sides. |
| `engine.version` | `SELECT sqlite_version()` (`Inspection.js:403-406`) | Absent | Dropped by `comparable()`, not compared. |
| `database_encoding` | `PRAGMA encoding` (`Inspection.js:408-410`) | **INDEP:** header bytes 56–59 in `read_header` | Yes, 12/12, but all are UTF-8; UTF-16 mapping is not exercised. |
| `schema.scope` | `sqliteSchemaScope(input)` (`Inspection.js:146`) | Literal `"database"` | Compared, but constant for this input. |
| `schema.completeness` | Literal `"complete"` (`Inspection.js:198-204`) | Same literal | Compared, but constant. |
| `rows` | `readRows()` returns null when `input.table` is absent (`Inspection.js:298-301`); database scope has no selected table | Literal `None` | Compared, but forced null for every carrier; no row-inspection evidence. |
| `limitations` | Static/conditional REA messages, including the unresolved-shadow message (`Inspection.js:243-244`, 386-400) | Not in oracle | Dropped; the conditional shadow explanation is not compared. |
| `schema.tables[].name`, `.sql`, `.root_page` | `SELECT ... FROM main.sqlite_schema`, blob cast/decode and `rootpage` (`Inspection.js:212-227`) | **INDEP:** Python file-format parser reads sqlite_schema records and b-tree order | Yes: 271 tables; long SQL/overflow also exercised. |
| `schema.tables[].kind` | `listed.type`, except `shadowParentOf(...) ? "unknown"` (`Inspection.js:181-188, 231-236`) | Base type from `table_list`; `unknown` override is a transcription of REA's prefix rule | Base types yes: 251 `table`, 15 `shadow`, 5 `virtual`; **override no** (zero unresolved virtual tables; N3 survives 12/12). |
| `schema.tables[].without_rowid` | `listed.wr !== 0n` (`Inspection.js:237`) | **RELAY:** `PRAGMA table_list` `wr`, same boolean mapping | Yes: 133 true, 138 false. |
| `schema.tables[].strict` | `listed.strict !== 0n` (`Inspection.js:238`) | **RELAY:** `PRAGMA table_list` `strict` | False only (271); no true/STRICT table. |
| `schema.tables[].column_count` | `listed.ncol`, except `virtual && ncol === 0 ? null` (`Inspection.js:239`) | Base count from `table_list`; null rule copied from REA | Counts yes: 271 non-null, including five R*Tree tables with count 5; **null branch no** (N2 survives 12/12). |
| `schema.tables[].columns_completeness` | Starts `complete`; virtual database-scope tables become `unsupported` (`Inspection.js:240, 247-250`) | **RULE:** oracle copies `unsupported if virtual else complete` | Yes: 266 `complete`, 5 `unsupported`. Both values occur; N1 changes the five GeoPackages. |
| `schema.tables[].columns` | `readColumns()` uses `PRAGMA table_xinfo` (`Inspection.js:121-140`); virtual tables skip expansion (`Inspection.js:249-256`) | **RELAY** for ordinary/shadow columns; oracle also returns `[]` for virtual tables by the same branch | Yes: 2,352 columns across non-virtual tables; five virtual empty lists. N4 changes all five GeoPackages. |
| `schema.tables[].columns[]`: `cid`, `name`, `declared_type`, `not_null`, `default_sql`, `primary_key_position`, `hidden` | `PRAGMA main.table_xinfo`; REA maps `notnull !== 0n`, keeps the other fields and validates `hidden` (`Inspection.js:121-140`) | **RELAY:** Python `table_xinfo` from system SQLite 3.54.0 vs Node SQLite 3.53.4 | Yes: 2,352 columns; `not_null` 1,237 true/1,115 false; 15 non-null defaults; 369 nonzero PK positions; 42 empty declared types. `hidden` is 0 for all 2,352, so nonzero hidden flags are not tested. |
| `schema.indexes[]`: `name`, `table`, `sql`, `root_page` | sqlite_schema query/dispatch (`Inspection.js:212-227, 265-272`) | **INDEP:** byte-parser sqlite_schema row (`type`, `name`, `tbl_name`, rootpage, SQL) | Yes: 167 indexes; 82 have `sql: null`. |
| `schema.views[]`: `name`, `sql` | sqlite_schema query/dispatch (`Inspection.js:212-227, 273-278`) | **INDEP:** byte-parser rows | Yes: 35 views. |
| `schema.triggers[]`: `name`, `sql` | sqlite_schema query/dispatch (`Inspection.js:212-227, 279-290`) | **INDEP:** byte-parser rows | Yes: 267; maximum trigger SQL is 128,117 characters. |
| `schema.triggers[].table` | `triggerTable(value.tbl_name)` (`Inspection.js:167-174, 289`) | **RULE:** same ASCII-fold/canonical-name mapping as REA | **No:** all 267 targets already exactly equal a listed name; zero case-fold decisions. |
| List ordering | REA iterates sqlite_schema query without `ORDER BY` (`Inspection.js:212-214`) | **INDEP:** oracle walks b-tree keys in row order | Yes. `table_list` order and schema-table order differ at position 0 for all 12; report comparison is order-sensitive. |

## Independence and exercise evidence

**[OBSERVATION]** The carrier census command was `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 -B tally.py`; exit 0 at 2026-10-23T04:36:29Z. Exact output excerpts:

```text
tables                       271
indexes                      167
views                        35
triggers                     267
cols                         2352
kind_shadow                  15
kind_table                   251
kind_virtual                 5
wr_True                      133
wr_False                     138
strict_False                 271
cc_null_False                271
completeness_complete        266
completeness_unsupported     5
hidden_0                     2352
trigger_targets exact=267 fold=0 else=0
enc_UTF-8                    12
wal_None                     12
```

**[OBSERVATION]** An illustrative leaf-weighted accounting across the 12 reports yields 20,279 scalar leaves plus 14 empty-list values. Of those 20,293 values: 17,548 are SQLite-relay fields (86.5%); 2,121 are byte-parser/header/hash fields (10.5%); 538 are explicit REA-rule fields plus 5 empty virtual-column lists (543, 2.7%); 72 fixed/echo leaves plus 9 empty view/trigger lists (81, 0.4%). This weights every field equally, not by semantic importance. The 17,548 relay leaves comprise 16,464 `table_xinfo` values, 813 table-list flags/counts, and 271 base kinds. The 2,121 independent leaves comprise 2,085 sqlite_schema fields plus 36 artifact hash/size/encoding values.

**[OBSERVATION]** I made four single-point mutations to scratch copies of the oracle and compared each report with pristine `expected_report` on all 12 carriers. Command: `PYTHONDONTWRITEBYTECODE=1 timeout 600 python3 -B logic_mutants.py`; exit 0, 2026-10-23T04:34:13Z–04:34:14Z. Exact output:

```text
N1-completeness-always-complete  changed=5 gpkg-curve,gpkg-curvepolygon,gpkg-line-zm,gpkg-multisurface,gpkg-test-gpkg-nulls
N2-drop-column-count-null-rule   changed=0 -
N3-drop-kind-unknown-rule        changed=0 -
N4-expand-virtual-columns        changed=5 gpkg-curve,gpkg-curvepolygon,gpkg-line-zm,gpkg-multisurface,gpkg-test-gpkg-nulls
RESTORED_CHECK mismatches=0 -
```

The mutant hashes and complete stdout are listed under Artifacts. N2/N3 are the counterexample to any implication that 12/12 covered the unresolved-virtual rules: removing either oracle rule changes no carrier report.

**[OBSERVATION]** A separate read-only oracle probe of `/fast/scratch/hyaku/kaidoku-r31/seats/w2/CriticOracleIndep/ghost.db` (copied from the wave-1 scratch fixture, not a C1 carrier; sha256 `718b6bec0d31efe26573a16cc74669af417ea9d8aaf5caae8cddf841f515554d`) returned:

```text
table_list ('main', 'ghost_node_extra', 'table', 1, 0, 0)
schema ('table', 'ghost_node_extra', 'ghost_node_extra', 4, 'CREATE TABLE ghost_node_extra(z)')
oracle unknown ghost_node_extra column_count 1 complete
```

It also returned `oracle virtual ghost column_count None unsupported`. **[INFERENCE]** The `unknown` output is not independently derived from SQLite: the SQLite list says `ghost_node_extra` is an ordinary `table`; the oracle applies REA's `<unresolved-virtual-name>_` prefix heuristic. The heuristic can conservatively over-classify a similarly named ordinary table. **[UNKNOWN]** I did not run REA on this fixture, and this is not a frozen carrier; this observation demonstrates the oracle's rule, not a live REA result.

## What the 12/12 establishes—and does not

**[OBSERVATION]** The 12 envelope comparisons are not merely SQLite comparing itself to itself. The independent parser supplies sqlite_schema names, SQL text, root pages and row order; the counter requires exact dict/list equality. The five PROJ files exercise large overflow-carried schema text; 82 auto-index records exercise null SQL; the artifact digest/size check compares REA's copied bytes with the original file; ordering is tested against a different independent b-tree traversal. REA's query/type/boolean projections are also checked against a separate SQLite build, with both `without_rowid` boolean values and both `not_null` values present.

**[INFERENCE]** The strongest supported statement is: *on these 12 UTF-8, no-WAL published files, REA 6.5.0 faithfully maps SQLite's catalog into the expected report shape and preserves the independent reader's sqlite_schema content/order; its copied input bytes match the source.* This is a useful relay/conformance result, not a trivial tautology.

It does **not** establish:

- that SQLite's own `table_list`/`table_xinfo` values are independently correct; both readers share SQLite lineage, albeit different builds;
- that REA's `kind: unknown`, null `column_count`, or trigger-fold rules are correct: they are copied into the oracle and unexercised by carriers;
- that `columns_completeness` has an independently mandated meaning: both values are exercised, but `complete`/`unsupported` are REA conventions copied into the oracle;
- any non-ASCII/UTF-16 decoding, WAL-present handling, STRICT table, nonzero hidden/generated-column flag, reserved-byte, or unresolved-virtual behavior;
- that the live bundle/module is correct on an unexercised branch. The source-derived expected rule is not a live observation of that branch.

## Smallest safe corrections to the record

1. **Entry Method/Limits:** qualify “Kind ... comes from libsqlite3”: base kinds do; the `unknown` override is the oracle's transcription of REA's shadow-prefix rule. Also say `columns_completeness` and omission of virtual columns are REA conventions, not SQLite PRAGMA fields. The Inference paragraph already mentions the `unknown` rule, but the Method/Limits currently read more broadly.
2. **Entry Inference, “in table order”:** say “in `sqlite_schema` row order.” The output follows the sqlite_schema scan, not `table_list` order; the two orders differ at the first element on all 12 carriers. This wording correction makes the real order check explicit.
3. **Entry Limits mutant list:** add the null-`column_count` and `kind: unknown` rules; the wave-2 N2/N3 mutations both survive 12/12 because no carrier has unresolved `virtual, ncol=0` metadata.
4. **Frozen claim limits / lesson:** do not amend frozen `claims.json`. Record the narrowness in the lesson: the phrase “independent oracle for the positive class” (lesson line 9) should read as independent for byte-level catalog fields, cross-build for PRAGMA fields, and REA-transcribed for wrapper rules. The frozen limits' “kinds ... come from ... libsqlite3” describes the observed carrier values, not the oracle's full rule set.
5. **Vacuous compared fields:** note that `wal` and `rows` are null on every carrier; `engine.name`, `schema.scope`, and `schema.completeness` are constants. In particular, the oracle's WAL-present branch is the wrong shape for REA, so it must not be treated as tested by the 12 nulls.

**Impacted axes:** coverage (C1 evidence supports a narrower claim than full semantic independence), calibration (record the relay/rule split). No C2 verdict is made; C2's accepted-report comparisons use the same oracle and inherit this report-field independence split.

## Execution provenance

**[OBSERVATION]** REA's `scripts/rea.mjs` loads `dist/cli-runtime/cli.js`. The bundled CLI worker-launch code rewrites its worker URL to `../sqlite/SqliteDatabaseWorker.js`; that unbundled worker imports `./SqliteDatabaseInspection.js`. Therefore schema, encoding, and row behavior cited above comes from the same pinned inspection file the oracle transcribes. The artifact/WAL provider and snapshot are bundled into `cli.js` (`SqliteDatabaseSnapshot.js` region at line 5860; provider region at 6098); the bundle contains the same `{path, sha256, bytes}` WAL object shape. This supports the code-path mapping but does not prove unexercised runtime behavior.

## Evidence commands

All commands were read-only with respect to lane/fleet files. Probe scripts and outputs are under the scratch path below; no REA command was run.

| Finding | Command | Exact excerpt | Exit / UTC |
|---|---|---|---|
| Mutant sensitivity of logic rules | `PYTHONDONTWRITEBYTECODE=1 timeout 600 python3 -B logic_mutants.py` | `N2-drop-column-count-null-rule changed=0`; `N3-drop-kind-unknown-rule changed=0`; N1/N4 each changed the five GeoPackages | 0; 04:34:13–04:34:14Z |
| Carrier field counts | `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 -B tally.py` | `wr_True 133`; `strict_False 271`; `completeness_unsupported 5`; `trigger_targets exact=267 fold=0 else=0` | 0; 04:36:29Z |
| Rule/relay leaf census | `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 -B census2.py` | `R-column 16464`; `R-table_list 813`; `I-byteparser 2085`; `L-trigger-fold 267` | 0; 04:34:13Z |
| Ordering | `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 -B probe_order.py` | `proj-341 equal=False first_diff_pos=0 n=37/36`; `gpkg-curve equal=False first_diff_pos=0 n=14/13` | 0; 04:34:13Z |
| Compared key sets | `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 -B shape.py` | `keyset_equal_top True`; exact table/column/index/trigger keys printed in `out/shape.txt` | 0; 04:34:13Z |
| Ghost counterexample | `PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 -B -` (query table_list/schema and run oracle on scratch `ghost.db`) | `table_list ... ghost_node_extra ... 'table'`; `oracle unknown ghost_node_extra ...` | 0; 04:38:31Z |

## Local sources and receipts

Access date for all local sources: **2026-10-23**. No external URL was fetched. Quotes are contiguous and at most 25 words.

| Local URL / source | SHA-256 | Located quote |
|---|---|---|
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseInspection.js` | `edfcd90f9e2e1dbde531b6aafc4efb1bd105a372df617dee619a414425354970` | L236: `kind: possibleShadowParent === undefined ? listed.type : "unknown",` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseSnapshot.js` | `c8af51f8496703a1992e7e7646c8bf8b6c56796a7571f5f8e9c84a284740ce19` | L140: `walArtifact = {` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseProvider.js` | `018756d9d7f620995c9b8929d268c33ff1f7c973683bd0f4ddc6d781e5268104` | L171: `wal: snapshot.wal,` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseWorker.js` | `ebb39f583db802ccb31b3ac328b0f8dd712fa6f0e5dd5a63da6908d7fe60cf63` | L4: `import { inspectSqliteDatabaseSnapshot } from "./SqliteDatabaseInspection.js";` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/cli.js` | `168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204` | L6061: `fileURLToPath(new URL("./SqliteDatabaseWorker.js", new URL("../sqlite/SqliteDatabaseWorkerExecution.js", import.meta.url).href)),` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseInspection.js` | same as above | L239: `column_count: listed.type === "virtual" && listed.ncol === 0 ? null : listed.ncol,` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` | L197: `"columns_completeness": "unsupported" if virtual else "complete",` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py` | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | L75: `if got != expected:` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | `9cb98595417c927bd223aadba4f582fffca5b39e43a52a7213c3830977aee3e2` | L51: `REA reads PRAGMA main.table_list then main.sqlite_schema in table order` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | L21: `kinds, without_rowid, strict and columns come from the system libsqlite3 3.54.0 through Python` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-31.md` | `70afbffd8a079d6f86925ffb5f4e475b14ec8796e19ab20ea21212011ddd2409` | L9: `an independent oracle for the positive class` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md` | `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3` | L3251: `on 12 published files vs an independent reader` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | L9: `pyogrio-0.11.1/pyogrio/tests/fixtures/curve.gpkg` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` | L4: `"version": "6.5.0"` |

## Scratch artifacts

All retained files are under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/CriticOracleIndep/`; no artifacts were written elsewhere. Scripts, probe outputs, errors, the copied ghost fixture, and the four mutated oracle copies are listed with SHA-256:

| Artifact | SHA-256 |
|---|---|
| `probe_fields.py` | `e098e2c44fee9f6d58f01ed3f868c5712e8df7e6b370c7f1a4fbe4065f3bb98f` |
| `probe_wr.py` | `4ac269357ab2597602f15bbf516b0f99e664ef535b159d4d64b66b1b8ad7fe59` |
| `probe_order.py` | `9d530b18bf35d1eac28a9a207b2f0965ae3257fa3eee791f5bab0c9c14f4d1df` |
| `census2.py` | `e293c336615aca1c67f2ada6cc2e1c4870f004f819b821fb01721c79619b535b` |
| `shape.py` | `f9b7c29c91e778a18f0087dbf017d65f56f5454aa42d4ca46860c152d85f760b` |
| `logic_mutants.py` | `c9d8bb2533b15bd310911391565c4d5047743f0e345f5da13925b7187f6efc12` |
| `tally.py` | `a08b3ecc1e52475f9897aae7c2b3b192cabbbda2282982b9dd2ae43bfa5afdc8` |
| `ghost.db` | `718b6bec0d31efe26573a16cc74669af417ea9d8aaf5caae8cddf841f515554d` |
| `out/probe_fields.txt` | `86293a038a3cc55aa20b5a55e995d26877ce928909872afe43a6168587040252` |
| `out/probe_wr.txt` | `c0a3cee460181810d1199d803d891b102d86d34c14420f2f2744776413db5a49` |
| `out/probe_order.txt` | `ca24d3b400ba2e57aed701a52bbe99eed10c8a8c7e8f4f390ea7927a84fab125` |
| `out/census2.txt` | `9873dbda5efaade9dc9d045a52f0d7dacf2a4d9c2b484409cbb41261326684c2` |
| `out/shape.txt` | `247e94c18f32e22e97c71885b3b9dd8bbcb9d796488b9c2952facac7dc8c5530` |
| `out/logic_mutants.txt` | `b109d1176a22337b436ce9808c88baa982ef982ee34fd47c2b1ff3d8156f03f3` |
| `out/tally.txt` | `938d147d1b4aee3819fe1bdbfe9b4f868563b28dbdf3f506026e9cd7f2d43a18` |
| `out/ghost.txt` | `81c911a4523a33252ee6f6642984626803edd7b5425f62e97975d38ce4e17b7a` |
| `mutants/N1-completeness-always-complete/sqlite_oracle.py` | `6ad785c3f8f5a2a94226d4e1ff141fbf8fc8688db510eaf849df061dd35a2e33` |
| `mutants/N2-drop-column-count-null-rule/sqlite_oracle.py` | `7d4b46146d04eeae003abc9945902b7c92108aadaa9dd218627fd5859e72f09f` |
| `mutants/N3-drop-kind-unknown-rule/sqlite_oracle.py` | `309b2b179ea98dac5a932c4bcbe2807b1712762c76a871bab07a0be1ad73610d` |
| `mutants/N4-expand-virtual-columns/sqlite_oracle.py` | `00e99547e499a602fca9444b6f3d395bade48d93715335409ec0373f8445aa86` |

**Installs/updates:** none.
