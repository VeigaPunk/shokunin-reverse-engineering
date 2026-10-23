# ReviewPredicateIdentity — round-31, wave 1

Seat: `KaidokuR31.ReviewPredicateIdentity` (UFO-FSD reviewer, leaf, no subagents).
UTC of observation session: 2026-10-23T04:05Z–04:11Z.
Scope: predicate identity for R31-C1 and R31-C2 — claims.json predicate sentence vs counter docstring vs enforcement in `judge` / `committed_check` / `entry_ok` / `province_ok` / `skill_ok` / `measure`, per the assignment.

## Frozen bytes reviewed (all hashes match the claims.json instruments / frozen_inputs)

| File | sha256 | Matches claims.json |
|---|---|---|
| `tools/round-31/c1-sqlite-positive.py` | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | instruments ✓ |
| `tools/round-31/c2-sqlite-refusals.py` | `d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223` | instruments ✓ |
| `tools/round-31/sqlite_oracle.py` | `aefd8639383bc6be7048b3e7115769c1f325a3b24fc111f3646acec83f41dc6b` | instruments ✓ |
| `.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | — |
| `corpus/evidence/round-31/c1/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | frozen_inputs ✓ |
| `corpus/evidence/round-31/c2/predictions.tsv` | `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8` | frozen_inputs ✓ |

Evidence: `bash` / `read` on the paths above; `python3 /fast/scratch/hyaku/kaidoku-r31/seats/w1/ReviewPredicateIdentity/predicate_identity_analysis.py` exited 0 and printed exactly the hashes above (no REA run needed for this review; no lane/sibling mutation).

---

## Claim R31-C1 (coverage) — clause table

Sentence: `"A carrier passes when its live REA 6.5.0 inspect-sqlite-database --schema-scope database run exits 0 with an ok envelope whose operation is inspect_sqlite_database and whose subject sha256 equals the carrier's frozen sha256, and whose normalized_result, without engine.version and limitations, equals the independent oracle's report field for field (artifact, wal, engine name, database_encoding, and every table, index, view and trigger with name, sql, root page, kind, without_rowid, strict, column count, column completeness and all column fields; rows null); and its committed envelope, first added after the freeze commit, equals the live envelope in every field except meta, and the round-31 entry names that evidence_id."`

| # | Sentence clause | Enforcement (file:line) | Status |
|---|---|---|---|
| C1-1 | live REA 6.5.0 run | `REA = ["npx","-y","rea-agents@6.5.0"]` (c1:33); PKG_JSON version `== "6.5.0"` (c1:162-164) | matched |
| C1-2 | `inspect-sqlite-database --schema-scope database` | `run_rea` argv (c1:89) | matched |
| C1-3 | exits 0 | `judge`: `code != 0` → P1-fail (c1:67) | matched |
| C1-4 | an ok envelope | `judge`: `env.get("ok") is not True` → P1-fail (c1:67) | matched |
| C1-5 | operation is `inspect_sqlite_database` | `judge`: `data["operation"] != "inspect_sqlite_database"` (c1:70) | matched |
| C1-6 | subject sha256 equals the carrier's frozen sha256 | `judge`: `data.subject.digest.sha256 != carrier_sha` (c1:72); `carrier_sha` = `r["sha256"]` from the rev-pinned carriers.tsv (c1:146-156), and the live file digest is pinned to the same value (c1:159) | matched |
| C1-7 | normalized_result, without engine.version and limitations, equals the independent oracle's report field for field: artifact, wal, engine name, database_encoding; every table/index/view/trigger with name, sql, root page, kind, without_rowid, strict, column count, column completeness, all column fields; rows null | `judge`: `comparable(normalized_result) != expected` → fail (c1:74-80). `comparable` drops only `limitations` and `engine.version` (oracle:222-229); `expected_report` emits artifact{path,sha256,bytes}, wal, engine{name}, database_encoding, schema.tables{name,sql,root_page,kind,without_rowid,strict,column_count,columns_completeness,columns(cid,name,declared_type,not_null,default_sql,primary_key_position,hidden)}, indexes{name,table,sql,root_page}, views{name,sql}, triggers{name,table,sql}, rows=None (oracle:162-219). Full-dict equality covers every listed field and `rows null` | matched |
| C1-8 | committed envelope first added after the freeze commit | `committed_check`: `first_added` > freeze add-time of claims.json (c1:106-108, 95-98) | matched |
| C1-9 | committed envelope equals live envelope in every field except meta | `committed_check`: `strip_meta(committed) == strip_meta(live)` (c1:113, 60-61) | matched |
| C1-10 | the round-31 entry names that evidence_id | `committed_check`: live `data.evidence_id` present and `in entry_text` (c1:115-117) | matched |

Sentence-only clauses: none — every clause above has an enforcement site.

Code-only conditions (not in the sentence): carrier count == 12 and carriers.tsv-at-rev == working-tree copy (PIN, c1:150-156); each carrier file exists and its sha256 == frozen (c1:159); package JSON pin (supports C1-1); entry cites S096 (entry_ok, c1:121-126 — claims.json doc_gate); PROVINCE.md table row naming verb+entry under a Core heading and not Frontier/Adjacent/exclusion (province_ok, c1:129-142 — claims.json doc_gate); verdict tokens `P1-pass`/`P1-fail`; final exit 0 only if `passed == 12 and e_ok and p_ok` with target tokens `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1` (c1:199-201). None contradict the sentence; all are stricter preconditions or doc gates.

Docstring vs sentence deltas (same semantics): docstring moves `--schema-scope database` from the sentence into the header line and drops the adjective "independent" before oracle (c1:2-16).

---

## Claim R31-C2 (depth) — clause table

Sentence: `"A request matches when its live REA 6.5.0 run agrees with its frozen prediction: for a predicted refusal the process exits 1, the envelope has ok=false, error.code equals the predicted code and error.details.issues is exactly one issue equal to the predicted {path, reason, message}; for a predicted acceptance the run exits 0 with an ok inspect_sqlite_database envelope whose subject sha256 is the request file's sha256 and whose report equals the oracle (or, for q-ok-rows, selects 3 Album rows with columns AlbumId, Title, ArtistId, each in the oracle's table); and its committed envelope, first added after the freeze commit, equals the live envelope in every field except meta (full-envelope rule, round-30 routed defect 2 / M30-3)."`

| # | Sentence clause | Enforcement (file:line) | Status |
|---|---|---|---|
| C2-1 | live REA 6.5.0 run | `REA` constant (c2:32); PKG_JSON version pin (c2:298-300) | matched |
| C2-2 | agrees with its frozen prediction | predictions read from rev-pinned TSV, tree copy equal, count == 23 (c2:279-289); per-row outcome/exit/code/issue/reason/message drive the verdict | matched |
| C2-3 | refusal: process exits 1 | `judge`: `code != int(row["exit"])` → P2-miss (c2:155). All 20 refusal rows carry `exit=1` (predictions.tsv lines 2-7,9-10,12-17,20-24) — semantically equal to "exits 1" | matched |
| C2-4 | refusal: envelope has ok=false | `judge`: `env.get("ok") is not False` → P2-miss (c2:157) | matched |
| C2-5 | refusal: error.code equals the predicted code | `judge`: `err["code"] != row["code"]` → P2-miss (c2:159-161) | matched |
| C2-6 | refusal: error.details.issues is exactly one issue equal to the predicted {path, reason, message} | `judge`: `want = {path: json.loads(row["issue_path"]), reason: row["issue_reason"], message: row["message"].replace("{P}", path)}`; `issues != [want]` → P2-miss (c2:162-166). Single-element list equality enforces "exactly one issue" and per-field equality; `{P}` substitution is the docstring's spelling of "predicted message" (8 messages carry `{P}`) | matched |
| C2-7 | acceptance: run exits 0 with an ok inspect_sqlite_database envelope | `judge`: `code != 0 or ok is not True` → P2-miss; `operation` check (c2:168-172) | matched |
| C2-8 | acceptance: subject sha256 is the request file's sha256 | `judge`: `data.subject.digest.sha256 != file_sha(path)` → P2-miss (c2:173, 216-223) | matched |
| C2-9 | acceptance (non-rows): report equals the oracle | `judge`: `load_oracle().comparable(nr) != dict(oracle["report"])` → P2-miss (c2:194-196), where `oracle["report"]` = `expected_report(path)` for that request file (c2:200-213). Covers m-journal-empty, m-journal-zero28 | matched |
| C2-10 | q-ok-rows: selects 3 Album rows with columns AlbumId, Title, ArtistId, each in the oracle's table | `judge`: `rows.table == "Album"`, `row_limit == 3`, `returned_rows == 3`, `columns == [AlbumId, Title, ArtistId]`, each `(int(vals[0].value), vals[1].value, int(vals[2].value))` in the oracle's `album_rows` set (c2:176-189); plus selected-table schema == oracle's Album table (c2:190-192) | matched |
| C2-11 | committed envelope first added after the freeze commit | `committed_check`: `first_added` > freeze add-time (c2:237-239, 226-229) | matched |
| C2-12 | committed envelope equals live envelope in every field except meta | `committed_check`: `strip_meta(committed) == strip_meta(live)` (c2:244, 143-146) | matched |

Sentence-only clauses: none.

Code-only conditions (not in the sentence): prediction count == 23 and TSV pin (c2:286-289); base chinook carrier pin (c2:294-297); mutant file pins from `mutant_sha256` (c2:305-310); mutant sibling journal/WAL pins from `mutant_sibling_sha256` incl. symlink representation (c2:311-316); per-mutant build-state checks (absent/enotdir/directory/db-symlink, c2:320-326); package JSON pin; entry cites S092 (entry_ok, c2:251-257 — claims.json doc_gate); SKILL.md names verb+entry and holds a table row per request id naming predicted code (or accept) and message prefix (skill_ok, c2:260-275 — claims.json doc_gate); **entry text must name each request id** (`rid not in entry_text` → fail, c2:246-247 — stricter than the sentence, which only requires full-envelope equality for C2); verdict tokens `P2-match`/`P2-miss`; final exit 0 only if `matches == 23 and e_ok and s_ok` with target tokens `requests=23 matches=23 target=23 entry_ok=1 skill_ok=1` (c2:361-363). None contradict the sentence.

Docstring vs sentence deltas (same semantics): docstring spells out `{P}` → request-path substitution, "(scope database)", and the q-ok-rows shape; claim adds "(round-30 routed defect 2 / M30-3)" and docstring says "repairs M30-3" (c2:5-15).

---

## Label identity

- R31-C1: claims.json `predicate_label` = `P1-pass`; docstring "Predicate P1-pass"; code `LABEL = "P1-pass"` (c1:41) and `judge` returns `LABEL` as the pass verdict (c1:82); failures are `P1-fail`. Identical.
- R31-C2: claims.json `predicate_label` = `P2-match`; docstring "Predicate P2-match"; code `LABEL = "P2-match"` (c2:41) and `judge` returns `LABEL` (c2:167,193,197); failures are `P2-miss`. Identical.
- Target lines: claims.json targets match the printed token shape (`carriers=%d pass=%d target=%d entry_ok=%d … province_ok=%d` / `requests=%d matches=%d target=%d entry_ok=%d … skill_ok=%d`), exit 0 only on target.

## Verdict

Holds. For both claims, every clause of the frozen predicate sentence is enforced in the counter code; there are **no sentence-only clauses** (nothing in the sentence lacks enforcement). The code-only conditions are stricter PIN/doc-gate/target preconditions that do not contradict the sentence. P1-pass and P2-match appear identically in claims.json, both docstrings, and the code `LABEL` constants. Docstring/claim deltas are wording-level only (CLI flag moved to a header line; `{P}` substitution and q-ok-rows shape spelled out; "independent" omitted once).

Findings (all observation-level, none actionable in scope):
1. C2 "process exits 1" is enforced as equality to the predicted exit value (c2:155); with all 20 refusal rows frozen at exit=1 the behavior is identical. Note, not a defect.
2. Both committed-checks order "first added after the freeze" by commit timestamp min (`%ct`), not ancestry (c1:95-98, c2:226-229). In this linear repo the freeze add-time is well-defined; clock skew/rebases could misrank. Low residual risk.
3. C2 `judge` assumes `error.details` is a dict when non-empty (c2:162); an unexpected truthy non-dict details would raise AttributeError instead of returning a P2-miss verdict. Robustness-only; unreachable with the frozen REA shape.
4. C1's report equality is full-dict (stricter than the sentence's field list): any extra top-level normalized_result key beyond limitations/engine.version fails. Intended strictness, not a gap.

## Verification gaps

- No REA run was performed (this item is a text review; no carrier/mutant was touched). Verdict is about predicate identity, not live counter outcomes.
- The clause tables cite code and frozen data; runtime behavior (REA envelope shape) is not exercised here, so "matched" means "enforced in code", not "REA satisfies it".

## Artifacts (seat dir: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ReviewPredicateIdentity/`)

- `predicate_identity_analysis.py` — sha256 `e2aa1f00fe8c9e3b9e640cfa9eea83f70408f14b688bb22664ac1aeccf7ba958` (reproduces the hash table and normalized sentence comparisons; ran at 2026-10-23T04:11Z, exit 0).
- No other scripts, drafts, clones, or raw outputs were produced; no lane files were modified besides this report.
