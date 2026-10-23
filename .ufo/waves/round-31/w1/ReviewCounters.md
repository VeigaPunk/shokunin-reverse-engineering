# ReviewCounters — R31 wave-1 review of the two frozen counters (pre-data)

Reviewer: KaidokuR31.ReviewCounters (leaf; no subagents). Date: 2026-10-23 (all probes run 04:05–04:14Z).
Scope: `tools/round-31/c1-sqlite-positive.py`, `tools/round-31/c2-sqlite-refusals.py`, `tools/round-31/sqlite_oracle.py`, plus the frozen inputs (carriers.tsv, predictions.tsv, claims.json) and the installed `rea-agents@6.5.0` package (`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`). Measure mode not run (per assignment). Both `--selftest` modes run.

Verdict: the counters are sound for the frozen data as frozen today — the refusal matrix, envelope determinism, and oracle↔REA report equality all verified live — with **one high-severity anti-tamper gap** and several robustness/latent defects below. No current defect would make a pass dishonest *as long as no post-freeze commit touches the frozen instruments*; the gap is precisely that such a commit is not detectable by the counters.

---

## 1. Selftest outputs (required)

### C1 `python3 -I -B tools/round-31/c1-sqlite-positive.py --selftest` — exit 0
```
ok	exact	tables=0 indexes=0 views=0 triggers=0 columns=0
ok	exit 1	exit 1 ok True
ok	wrong sha	subject sha256 differs from the frozen carrier
ok	schema differs	report differs from the oracle: schema,schema.views
ok	refusal	exit 1 ok False
ok	no envelope	no JSON envelope (exit 0)
ok	wrong operation	operation 'inspect_artifact'
ok	row under Core heading	ok
ok	row under round Core-addition heading	ok
ok	row under Frontier	row sits under '## Frontier', not a Core heading
ok	row under Adjacent exclusion	row sits under '## Adjacent — Core exclusion', not a Core heading
ok	prose, not a table row	no PROVINCE table row names the verb and the entry
ok	verb without entry	no PROVINCE table row names the verb and the entry
ok	absent	PROVINCE absent
selftest cases=14 failures=0
EXIT=0
```

### C2 `python3 -I -B tools/round-31/c2-sqlite-refusals.py --selftest` — exit 0
```
ok	refusal exact	refused invalid_request invalid_value
ok	refusal wrong exit	exit 0 != 1
ok	refusal wrong code	code 'x' != 'invalid_request'
ok	refusal wrong message	issues [...] != [...]
ok	refusal wrong reason	issues [...] != [...]
ok	refusal extra issue	issues [...] != [...]
ok	refusal but ok	envelope ok, refusal predicted
ok	no envelope	no JSON envelope (exit 1)
ok	accept but refused	accept predicted, exit 1 ok False
ok	meta ignored
ok	data compared
ok	error compared
selftest cases=12 failures=0
EXIT=0
```

---

## 2. Findings (severity-ranked)

### F1 — HIGH: post-freeze edits to the frozen inputs or instruments are undetectable; the "frozen" contract is only checked as *tree-vs-rev*
Both counters pin `carriers.tsv` / `predictions.tsv` by comparing the blob **at `--rev`** with the **working-tree file** (c1 `measure` L147–150; c2 `measure` L280–287), never against the freeze commit's content, and never against the instrument hashes already committed in `claims.json` (`instruments`, `frozen_inputs`, `rea_pin`, L46–70). The counter and oracle code themselves run from the working tree (`load_oracle`, c1 L44–49, c2 L45–50) and are not hash-checked.
- Concrete failing scenario (dishonest pass): a post-freeze commit (e.g., the envelope commit) also edits one line of `carriers.tsv` (repoints `proj-341.db` to a crafted DB with a new sha256) or edits a row of `predictions.tsv` (relaxes a message/exit). The counter then reads the *edited* content at `--rev` and finds the tree identical → PIN passes → 12/12 or 23/23 target line, exit 0, under a different contract than the freeze. The freeze rule in claims.json ("fixed from that commit; a miss under them is reported, never amended") is then unenforced.
- Fix: verify `sha256(show(root, <freeze commit>, rel))` equals the tree hash (or compare tree files against the freeze commit, not against `--rev`), and verify the three tool files against `claims.json.instruments` before judging. This should be part of the counter (or of the L1 gate).

### F2 — MEDIUM-HIGH: freeze-time ordering uses committer timestamps, not commit topology
`first_added` and the freeze anchor use `git log —diff-filter=A --format=%ct` and take `min` of **committer clock times** (c1 L95–99, L167–170; c2 L226–230, L325–329).
- Concrete failing scenario (spurious fail): the L1 commits envelopes with a clock skewed relative to the freeze commit (e.g., commit made on a machine with a slightly wrong clock, or a future-dated rewrite of the freeze commit). Then `first_added(envelope) <= freeze_ct` even though the envelope is topologically after the freeze → every envelope fails committed_check ("committed envelope not added after the freeze") and the claim honestly but spuriously never passes. Conversely, a rebase/cherry-pick with older dates silently *weakens* the check.
- Fix: anchor by commit ID (the freeze commit is known: 35ba7c522dba55f9be27eb161d4254eacaa24330) and use `git merge-base --is-ancestor <freeze> <rev>` / walk from `rev`, not absolute clocks.

### F3 — MEDIUM (latent): REA emits `wal` as an artifact object; the oracle emits the string `"present"`; the comparison would fail on any accepted database with a `-wal` sibling
Oracle: `"wal": None if not os.path.lexists(path+"-wal") else "present"` (sqlite_oracle.py L218/return dict L212–220). REA: `wal: artifactSchema.nullable()` (dist/domain/sqlite/sqliteDatabase.js L14–18, L94) and snapshot builds `{path, sha256, bytes}` when a `-wal` exists (dist/sqlite/SqliteDatabaseSnapshot.js L140–144; provider L171).
- Concrete failing scenario (spurious fail): frozen corpus has no accepted WAL-bearing path — all 12 carriers are no-WAL (claims.json L21), and the only WAL-bearing request (`m-wal-over`) is predicted refuse — so today this never fires. If any future run in this lane is accepted with a `-wal` sidecar present, every such request fails P1/P2 with "report differs from the oracle: wal" even though semantics agree. Also the oracle's notion (existence) differs from REA's (snapshot read/hash).
- Fix: either make the oracle emit the same artifact object (hash+bytes of `-wal`) or compare `wal` presence only (boolean).

### F4 — MEDIUM: selftest covers neither acceptance branch nor the freeze/PIN logic
C2 `selftest` (L366–398) has **no accept case at all** — neither the full-report-vs-oracle branch nor the q-ok-rows branch (row decoding, `int(vals[i]["value"])`, selected-table schema equality `nr.schema.tables != album`), and no oracle_for/skill_ok/committed_check/PIN cases. C1 `selftest` (L204–243) does not exercise `comparable`, `committed_check`, `first_added`, or `measure`'s PIN logic.
- Concrete failing scenario: a future regression in the q-ok-rows judge (e.g., cell shape change, column-order assumption) or in `comparable` passes both selftests and only shows as 0/23 or 12/12 wrong at measure time.
- This is a coverage gap, not a current defect; recommend adding offline accept cases (a synthetic report plus a q-rows case).

### F5 — LOW-MEDIUM: schema arrays compared as ordered lists; REA query has no ORDER BY
`judge` compares `tables/indexes/views/triggers` as ordered arrays (c1 L70–77; c2 L187–193, and the default `comparable(nr) == exp` full-dict equality). REA reads `SELECT ... FROM main.sqlite_schema` with no `ORDER BY` (dist/sqlite/SqliteDatabaseInspection.js L212); the oracle walks b-tree key order. Empirically identical today, but the comparison is fragile to SQLite scan-order differences between the oracle's system 3.54.0 and REA's Node-bundled 3.53.4.
- Concrete failing scenario (spurious fail): a different SQLite build returns sqlite_schema rows in a different physical order; every carrier then fails on order-only diffs. Suggest comparing as multisets.

### F6 — LOW: the REA pin is version-string only; the recorded package_json hash is never enforced
`PKG_JSON` version is checked (c1 L165; c2 L299), and the package_json sha256 is *recorded* into runs.tsv, but `claims.json.rea_pin.package_json_sha256` is never compared.
- Concrete failing scenario: a modified `rea-agents@6.5.0` package (same version string, different code) slips through all PIN gates. Enforce the committed hash.

### F7 — LOW: doc-gate matchers are brittle substring checks
`province_ok` requires the literal `ENTRY` relative path inside a table row (c1 L129–143); `skill_ok` requires per-request substrings (`code`/`accept` + message prefix up to `{P}`) (c2 L260–276).
- Concrete failing scenario (spurious fail): the L1 writes the SKILL/PROVINCE rows with slightly different wording (truncated message, different quoting, path spelled differently) → doc gate fails though the substance is present. Honest stop, not a dishonest pass; still fragile.

### F8 — LOW: npx invocation relies on the pinned cache; failure mode is a traceback rather than a clean PIN
`run_rea` shells to `npx -y rea-agents@6.5.0` (c1 L87–93; c2 L135–141). If the fixed `~/.npm/_npx/ad9a3fdbcad992c6` cache is cleared, npx attempts registry resolution (network dependency) and the subsequent `PKG_JSON` read raises `FileNotFoundError` (traceback, exit 1) instead of a PIN message. Robustness note only.

---

## 3. Verified-correct evidence (what holds)

- **Oracle parses all 12 carriers.** `sqlite_oracle.py <carrier>` exit 0 on all; counts: chinook 11/11/0/0/64; chinook-autoinc 12/11/0/0/66; gpkg 5× 13 tables/8 indexes/0 views/18 triggers (one variant 64 cols); proj-341/350/361 36/21/7/35 (385 cols); proj-370 37/21/7/36 (395); proj-371 38/21/7/36 (396).
- **Oracle edge cases:** leaf-root page (type 13) small DB, interior-root (type 5) 400-table DB, UTF-16le DB, rtree virtual+shadow DB all parse; zero-byte file raises OracleError (correct).
- **Refusal matrix replayed live on scratch mirrors of every mutant class** (built exactly like `build()`): all 20 predicted refusals reproduced byte-identical messages after `{P}` → path substitution, exact `code=invalid_request`, `reason` invalid_value/invalid_format/out_of_range, issue `{path:["path"]}`, envelope `ok=false`, CLI exit 1. `m-journal-empty` and `m-journal-zero28` exit 0 with ok envelope. Examples:
  - `file is not a database` (zero-magic and pagesize-768)
  - `Rollback journal may require recovery: <path>-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported.` (hot, short)
  - `Expected a regular journal without a symlink: <path>-journal`
  - `Expected a regular file without a symlink: <path>` (db symlink and directory)
  - `Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: <path>` (db and WAL variants)
  - `Selected SQLite database does not exist: <path>`; `Selected database file set could not be read (ENOTDIR): <path>`
- **Envelope determinism:** two identical runs on the same scratch DB yielded identical `evidence_id` (`ev_860a0d8ad8b452f917ca0ef19da1c28340c3efa61b09e5eddf5be4b63ad44bb6`), identical subject digest (`722d54c9…`), confirming the full-envelope committed-vs-live rule (meta-only drift) can hold.
- **Oracle ↔ REA report equality** verified live on scratch.db at scope `database`: `normalized_result` equals `expected_report` after dropping `limitations` and `engine.version` (`equal: True`). Envelope keys observed: `[analysis_profile, authority, confidence, environment, evidence_id, evidence_links, limitations, locations, normalized_result, operation, parameters, predicate_type, provider, raw_result, relationship_coverage, subject]`; `subject.digest.sha256` exists as the judge reads it.
- **Current tree matches the freeze record:** HEAD = freeze commit `35ba7c522dba55f9be27eb161d4254eacaa24330`; claims.json/carriers.tsv/predictions.tsv all added at that commit; tree sha256 of the three tool files equal `claims.json.instruments` (aefd8639…, 048020881b…, d239489598…); carriers.tsv/predictions.tsv equal `frozen_inputs` (46f180b8…, acac45e3…); package.json sha = `rea_pin.package_json_sha256` (a5003023…) and version 6.5.0. No post-freeze commits exist yet.
- **Exit-code paths:** selftests exit 0; PIN paths return 2; non-target returns 1; unhandled exceptions propagate as tracebacks (nonzero). The kill-rule semantics are consistent.

## 4. Residual risk / verification gaps

- The WAL-present *accepted* path (F3) cannot be exercised with the frozen corpus (no accepted WAL-bearing input); the mismatch is proven from REA source + domain schema, not from a live accepted run.
- `committed_check` cannot be exercised pre-data (no envelopes committed yet); the determinism evidence above is the closest proxy.
- Measure mode intentionally not run; live REA was run only on non-carrier scratch files under the seat.
- No tools were installed (nothing needed); no lane files were modified besides this report.

## 5. Seat artifacts (sha256)

All under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ReviewCounters/tmp/`:
```
722d54c94b0f80f82ae844423d613ce50847b5e0017c3f12bfd57a48db84eaf5  scratch.db (8192 B)
679f132823abd57083bd6cbe892219132e29403cf8f1e2e5acb2040bba0d7cd7  wal.db (8192 B)
679f132823abd57083bd6cbe892219132e29403cf8f1e2e5acb2040bba0d7cd7  w2.db (8192 B)
0affc75b884c7bc21281437b2024e29137186fae458e97e30e1387d6f012efad  small.db (8192 B)
c5d26b3ad74eec28df6fb34be421cd2f998c13edf768c5dc9db8e02594018d4d  big.db (1671168 B)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  empty.db (0 B)
347fbf4d242883eed65124e76bf49a67fa1ec753f4a3550072ff6d5cccc000c6  utf16.db (8192 B)
58be929c764e7ebbe6d8711948ca2b980b26fc3f364ca8c6159d35c283431743  rtree.db (16384 B)
6284be3ec63681c8925504017be012cb64160ced4ab1f8cc6ac5838b89fd911f  rea_scratch.json (4724 B)
```
Mutant mirrors (`tmp/mut/<id>/db.sqlite` + sidecars), hashes equal the frozen `mutant_sha256`/`mutant_sibling_sha256` pins:
```
768fc036b7f2a094524104b3573ae8534087c386a4c67a975b22dd81a6253450  m-not-sqlite/db.sqlite
7dc1d180e4c996d1e5dd3ab2d08aec6a8ee50bcce3bf8ec36865909f93177395  m-bad-pagesize/db.sqlite
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  m-journal-hot/db.sqlite (+ e5e2cd476e660007e4cfd54782539fb93dc8bd4cb4c2c79a8f95682a7c287a4b journal)
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  m-journal-short/db.sqlite (+ 01d448afd928065458cf670b60f5a594d735af0172c8d67f22a81680132681ca journal)
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  m-journal-empty/db.sqlite (+ e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 journal)
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  m-journal-zero28/db.sqlite (+ 3addfb141cd7c9c4c6543a82191a3707ac29c7a041217782e61d4d91c691aee8 journal)
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  m-journal-symlink/db.sqlite (journal = symlink to chinook)
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  m-db-symlink/db.sqlite (symlink to chinook)
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  m-directory/db.sqlite (is a directory)
8a14e15c97369da109502ea5482f33fa605d47114d5f617d48d464566fc0fc5b  m-over-256mib/db.sqlite (268435457 B)
bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a  m-wal-over/db.sqlite (+ e1945862076f1d52e8984d0a342b46db37e734fe521a742cd8f5a75e83624292 wal)
```
`tmp/node-compile-cache/` is an incidental byproduct of npx runs under TMPDIR (hundreds of generated files; not authored).

## 6. Tooling directive record
No tool installs or updates performed (all needed tooling was present: python3, npx cache, sqlite3).
