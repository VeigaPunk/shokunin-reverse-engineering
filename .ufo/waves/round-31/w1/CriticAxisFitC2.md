# CriticAxisFitC2 — R31-C2 axis fit and discrimination, before data

Reviewed: lane base `c369242fee9f559f895e3f7956b1242076c7b1be`, freeze `35ba7c522dba55f9be27eb161d4254eacaa24330` (= lane HEAD at review time; `corpus/evidence/round-31/c2/` holds only `predictions.tsv`, sha256 `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8`, equal to the frozen hash). No counter was run and REA was never run on a carrier or mutant.

**Verdict: fit for the depth axis — the decision table is new depth and holds against the trivial-prediction attack.** 18 of the 20 refusal-message instances (14 of 16 distinct messages) appear 0 times in the whole base tree, and the verb appears 0 times in `SKILL.md` and `PROVINCE.md`. None of the four asked trivial predictors exceeds 3/23 of the frozen rows. Two annotations, neither fatal, in §4 and §6.

## 1. The frozen rows as scored

Observation — `python3 -I -B score.py` (seat script; reads `35ba7c5:corpus/evidence/round-31/c2/predictions.tsv` via `git show`, no REA), exit 0, 2026-10-23T04:15:37Z, `score.out:2-13`:

```
rows: 23 refuse: 20 accept: 3
code {'invalid_request': 20}
issue_path {'["row_limit"]': 1, '["columns"]': 2, '["schema_scope"]': 1, '["table"]': 5, '["path"]': 11}
issue_reason {'invalid_value': 5, 'invalid_format': 13, 'out_of_range': 2}
distinct refusal signatures: 16
duplicate signature groups (frozen code+path+reason+message):
  n=2 ['m-not-sqlite', 'm-bad-pagesize'] :: file is not a database
  n=2 ['m-journal-hot', 'm-journal-short'] :: Rollback journal may require recovery: {P}-journal. …
  n=2 ['m-db-symlink', 'm-directory'] :: Expected a regular file without a symlink: {P}
  n=2 ['m-over-256mib', 'm-wal-over'] :: Selected SQLite database and WAL exceed the combined 268435456-…
```

The three accept rows (`q-ok-rows`, `m-journal-empty`, `m-journal-zero28`) have empty `code`, `issue_path`, `issue_reason` and `message`, so on the four scored fields they are indistinguishable from the all-accept guess (this is what caps predictors (a), (c), (d) at 3).

## 2. Trivial-predictor scores (exact match on code + issue path + reason + message)

| predictor | n/23 | rows reproduced | reasoning |
|---|---:|---|---|
| (a) every request accepted | **3/23** | `q-ok-rows`, `m-journal-empty`, `m-journal-zero28` | Accept rows carry no code/path/reason/message, so "accept" reproduces them; all 20 refusals are missed on outcome, not just fields. Does not predict the accept payloads the counter checks live (report == oracle, 3 Album rows), so this is a ceiling on row fields, not a passing harness. |
| (b) `invalid_request` + a generic message, best constant path/reason (`["path"]`, `invalid_format`) | **0/23** | none | All 20 refusals do use `invalid_request`, but no predicted issue message is the generic envelope text ("Analysis input is invalid…"); the issue message is always the reader's literal. The best *constant tuple* if one exact message were guessed is 2/23 (the `file is not a database` pair) — observed in `score.py` as `(b')`, 2/23. |
| (c) `--help` + REA docs only (pinned 6.5.0 guide + root manifest), no code | **3/23** | the same three accepts | The docs state outcomes, never signatures: `--help`/`--llms-full`/`--schema` contain "requires table" (2 lines) and the option semantics, and 0 of the 16 messages; the pinned guide (`sqlite-databases-6.5.0.md`) says empty/"fully zeroed" journals are accepted and other journals, view/virtual/shadow row reads are refused, but gives no code, path, reason or message. So it predicts accepts where the docs say nothing (3 hits) and 0 of the 20 refusal rows exactly. |
| (d) reuse round-30's refusal messages | **3/23** | the same three accepts | Round-30's `predictions.tsv` has 14 distinct messages; none equals any of the 16 C2 messages (checked verbatim, `score.out:42-58`), and round-30's envelope convention supplies only the shape (generic top-level text, `issues[0]`). Every refusal row is missed; 3 only if it defaults to accept elsewhere. |

Arithmetic ceiling without the REA code: **5/23** [INFERENCE]. Combine (a)'s three accepts with SQLite's own bare errmsg for the two malformed rows: `sqlite3 3.54.0` (read-only on the immutable mutants, `oracle-receipts.out`, exit 1 each) prints `file is not a database (26)` for both, and round-30 shows the `["path"]`/`invalid_format` issue shape. That yields 2 + 3 = 5/23 if the predictor guesses the bare, unprefixed message. The frozen target 23/23 requires all 16 distinct signatures, 20 path/reason assignments and the 3 accept payloads.

## 3. Base grep counts for the 20 refusal messages

Observation — `git -C <LANE> grep -c -F '<prefix>' c369242f` (full tree at base), exit 0, captured 2026-10-23T04:13:59Z–04:14:03Z in `base-grep.out`:

| frozen message prefix | base lines / files | rows covered |
|---|---:|---|
| `row_limit requires an explicit table selection` | 0 / 0 | q-rowlimit-no-table |
| `columns requires an explicit table selection` | 0 / 0 | q-columns-no-table |
| `selected_table schema scope requires table` | 0 / 0 | q-scope-no-table |
| `Selected ordinary table does not exist with that exact name` | 0 / 0 | q-missing-table, q-case-table, q-view-as-table |
| `Selected column does not exist with that exact name in table` | 0 / 0 | q-missing-column |
| `outside the ordinary-table inspection profile` | 0 / 0 | q-virtual-rows, q-shadow-rows |
| `Selected SQLite database does not exist` | 0 / 0 | m-missing |
| `could not be read (ENOTDIR)` | 0 / 0 | m-enotdir |
| `file is not a database` | 0 / 0 | m-not-sqlite, m-bad-pagesize |
| `Rollback journal may require recovery` | 0 / 0 | m-journal-hot, m-journal-short |
| `Expected a regular journal without a symlink` | 0 / 0 | m-journal-symlink |
| `Expected a regular file without a symlink` | **14 / 10** | m-db-symlink, m-directory |
| `exceed the combined 268435456-byte snapshot budget` | 0 / 0 | m-over-256mib, m-wal-over |

The 14 hits are all `.ufo/waves/arc3-loop1-round4/` artifacts for `inspect_evm_interface`/artifacts (`git grep -l`, exit 0); **0** in `corpus/knowledge`, `SKILL.md`, `PROVINCE.md` or `corpus/evidence`. A probe for the help fragment `requires table` gives 7 lines / 6 files at base, all prior `.ufo` help captures — not a refusal message.

Verb counts at base: `inspect-sqlite-database` **0** in `PROVINCE.md` (exit 1), **0** in `SKILL.md` (exit 1), **0** in `corpus/knowledge` content (exit 1), **2** in `corpus/README.md` (exit 0); `inspect_sqlite_database` **0** in `PROVINCE.md`/`SKILL.md`, **4** in `corpus/knowledge` (exit 0: 3 in `2026-10-16-l7-04-inspect-sqlite-database.md`, 1 in `2026-10-16-l8-01-6p4-symmetry-battery.md`). The generic top-level message "Analysis input is invalid…" is already at base in 106 lines / 89 files (prior envelope-shape knowledge, not a predicted field).

## 4. Prior-art counterexample (holds against the claim prose, not the axis)

The shared surface prose says "a verb the lane has never run or named". At the base this is false. `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` (base, `git show c369242f:…`) says at line 5: "call `inspect_sqlite_database({"path":...})` under `rea-agents@6.5.0`; expect Evidence `ev_7572e622…` with the complete `package_index` inventory and `rows:null`", and line 11 records the live RESULT. `corpus/README.md:65,163` indexes it under the hyphenated name.

What this defeats: the prose sentence, and any claim that C2's *accept* path is new. What it does not defeat: the frozen `unmoved_command` (`SKILL.md` hyphen count 0, exit 1 — `before/unmoved-at-c369242f.txt` prints `0`), and the depth delta — l7-04 line 13 explicitly lists the unknowns ("did not request table columns or rows, and does not establish behavior for changing databases, WAL inputs, encrypted/corrupt files, or other schemas"), which is exactly the surface the 20 refusal rows cover. Verdict on the attack: **fails**; the table is new depth, but the new entry must cite l7-04 (and l8-01's 6.4 tool-not-found) or the lane will hold two uncited authorities for the same operation.

## 5. Discrimination notes

- 20 refusals → 16 distinct `(code, path, reason, message)` tuples, of which 4 pairs are literally identical in the frozen fields. The claim's limits disclose the shared messages; the residual point is that for those 4 pairs the `code_pointer` column is the only branch discriminator and the counter does not read it. Not a defect; it caps what the table alone can prove.
- 4 of the 20 message instances are not new string knowledge: 2 are SQLite's own text (demonstrated with `sqlite3` 3.54.0 on the malformed mutants) and 2 are already in base `.ufo` artifacts. The other 16 instances and every path/reason assignment are new.
- 3 accept rows are docs-derivable from the pinned guide; the 20 refusal rows are not. The docs predict outcomes, not signatures, and the main-branch guide drifts: it says the 256 MiB refusal is `resource_constraint` (main `sqlite-databases.md:137-139`), while the frozen rows say `invalid_request`/`out_of_range`. A docs-only predictor reading `main` instead of the `rea-agents-6.5.0` tag would be *more* wrong, not less. Unknown which the live run takes; the two budget rows are the only rows where a published document contradicts the frozen code reading, and pointer/trace seats own that adjudication.
- The SKILL table is a transcription of `predictions.tsv` (the `skill_ok` gate and the junk-row control both build it from the frozen rows); it is a presentation of the prediction, not a second independent prediction. Depth evidence is the 23 live matches, not the table's existence.

## 6. Impacted axes and smallest safe correction

- **depth (R31-C2): fit.** New branch/message knowledge, 23-row live test, 16 distinct signatures, no trivial path above 5/23.
- **coverage (R31-C1): prose miss, frozen command intact.** The surface sentence "never run or named" is contradicted by l7-04/README; the frozen `unmoved_command` is literally true (0 for the hyphenated string in the three named surfaces).
- **calibration: untouched by this item.**
- Smallest safe correction (freeze rule forbids amending the claim): (1) the C2 entry cites `2026-10-16-l7-04-inspect-sqlite-database.md` and `2026-10-16-l8-01-6p4-symmetry-battery.md` as prior art and states the delta (refusals/edge signatures, not the basic inventory); (2) the round-31 report/LOG records the surface-prose overstatement as a routed correction and quotes what the frozen command actually measures; (3) no counter or `predictions.tsv` change.

## 7. Evidence ledger (all commands run from the seat dir; no REA on carriers/mutants)

| # | command | exit | UTC | excerpt |
|---|---|---:|---|---|
| 1 | `python3 -I -B score.py` (reads lane via `git show`; frozen rows at `35ba7c5`) | 0 | 04:15:37Z | `rows: 23 refuse: 20 accept: 3` … `(a) … 3/23`, `(b) … 0/23`, `(b') … 2/23`, `(c) … 3/23`, `(d) … 3/23` (`score.out:19-23,59`) |
| 2 | per-prefix `git grep -c -F` at `c369242f` (20 rows) | 0 | 04:13:59–04:14:03Z | table in §3 (`base-grep.out`) |
| 3 | `npx -y rea-agents@6.5.0 inspect-sqlite-database --help` | 0 | 04:13:42Z | help text only; no refusal message (`help.txt`) |
| 4 | `npx … --llms-full`, `--schema`, `npx … --llms-full` (root) | 0,0,0 | 04:15:08–04:15:10Z | 0 hits for every message; `requires table` 2× (`llms-full.txt`, `schema.txt`, `root-llms.txt`) |
| 5 | `git ls-remote --tags https://github.com/morluto/rea.git \| grep 6.5` | 0 | 04:16:05Z | `3b79af28… refs/tags/rea-agents-6.5.0` |
| 6 | `sqlite3 'file:…m-not-sqlite/db.sqlite?mode=ro' 'select count(*) from sqlite_schema;'` (and `m-bad-pagesize`) | 1,1 | 04:16:05Z | `Parse error …: file is not a database (26)` |
| 7 | `git show c369242f:corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` | 0 | 04:13Z | lines 1,5,7,9,11,13 quoted in §4 |

Lane state checked read-only: `git rev-parse HEAD` = `35ba7c52…`, `ls corpus/evidence/round-31/c2/` = `predictions.tsv` only (no envelopes).

## 8. Sources opened (access date 2026-10-23)

| source | how | sha256 of bytes read | located quote (≤25 words) |
|---|---|---|---|
| `https://raw.githubusercontent.com/morluto/rea/rea-agents-6.5.0/docs/sqlite-databases.md` | `curl -sS -L` (HTTP 200, 8,128 B) | `f7b0c57b03c2874059cfacabb0dd9bc0ee994f89694274eab89d2e9392736d16` | line 88: "Empty rollback journals and fully zeroed journal headers left by successful `TRUNCATE` and `PERSIST` commits are accepted after stable identity checks." |
| `https://raw.githubusercontent.com/morluto/rea/main/docs/sqlite-databases.md` | `curl -sS -L` (HTTP 200, 10,864 B) | `44c798a53a1c6146ce85dd30e819bc3f5cba38d0f458982225f3fff4763ff067` | line 137: "If the combined database and WAL exceed the snapshot budget, the refusal is a `resource_constraint` and reports both the configured byte limit" |
| `https://github.com/morluto/rea.git` tags | `git ls-remote --tags` | n/a (ref list) | `refs/tags/rea-agents-6.5.0` → `3b79af28e80785afce9f5998d8f03289402a1847` |
| installed `rea-agents@6.5.0` docs (`README.md`, `skills/…/references/native-and-artifacts.md`, `skills/…/SKILL.md`, `package.json`) | local read | `005e4c8a…f124`, `1d2ac5f6…4450`, `3456aab9…4715`, `a5003023…0a6c` (package.json matches the frozen pin) | native-and-artifacts.md:88-93 mirrors the journal rule; no message strings (0 hits for all 16) |

No message from `predictions.tsv` appears in any docs surface; the only doc/code contradiction found is the `main`-branch budget sentence in §5.

## 9. Tools installed

None. No pacman, uv, cargo or npm install; `npx -y rea-agents@6.5.0` used the already-present pin.

## 10. Seat artifacts (under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CriticAxisFitC2/`)

| artifact | sha256 |
|---|---|
| `score.py` | `aabebd4e1fc3bbc067f99294c4e2653bc5b139c552324f651f8758163a86adf0` |
| `score.out` | `a5cb1e1f667ae7c43bc55d004198978a73ac75ffdeaf182a35735d2ee7b975b7` |
| `base-grep.out` | `a88a76c7520694abf2acbd7efc9e0551c0a61e5a512a629bc2d59cfbd838d824` |
| `help.txt` | `e8e63c5e259833f464f3adc76b028c3e1ffa3778cd3715ad1975278b18c3b87e` |
| `help-receipt.txt` | `0245b5846f620b4527be8ba9460d6a4b769291736189b37583364070fb3465e9` |
| `llms-full.txt` | `b4f4cb43ac859b7e16843241f6e3c98ecd1575182196e94d3a8b0666b0db5aec` |
| `root-llms.txt` | `54c2fecd8ae358ffac3ffa98a8db74f77073feca067694f32c6c0c9f2c6a1061` |
| `schema.txt` | `0d69644e2d25d3b30a6584240438481135dceef4ac1e208e4885d14d1e74476b` |
| `sqlite-databases.md` | `44c798a53a1c6146ce85dd30e819bc3f5cba38d0f458982225f3fff4763ff067` |
| `sqlite-databases-6.5.0.md` | `f7b0c57b03c2874059cfacabb0dd9bc0ee994f89694274eab89d2e9392736d16` |
| `docs-receipts.out` | `19581112c2f829a1f627aa1379d33805b76e9141ad0404c48807097426a602b9` |
| `oracle-receipts.out` | `fe8e1da07bf232c1ce83cf9f6a921434f5509828282d8ad4216fb488d87dc233` |

Limits: one host, one pin (6.5.0), no live run (by item design), so the docs/code budget disagreement in §5 is unknown, and the 5/23 non-code ceiling is an inference. Lane writes: this report only.
