# Round 31 C2 envelope review — six targeted rows

## Verdict

**No actionable finding in scope; all six rows hold.** For each ID, the committed envelope agrees with the frozen prediction and the corresponding SKILL and knowledge-entry rows. No unsupported wording was found in those rows. All refusals have `error.code=invalid_request`, `error.category=invalid_input`, and exactly the predicted single issue. Captured-output presence agrees with the entry’s worker distinction. Both acceptance records’ evidence IDs and subject digests agree with the entry and frozen pins.

## Per-ID results

The committed live-run records are in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c2/runs.tsv`; frozen expectations are in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c2/predictions.tsv`. Each listed live verdict is `P2-match`.

| ID | Live exit / envelope | Exact issue or acceptance identity | `details.captured_output` | SKILL / entry comparison |
|---|---|---|---|---|
| `m-not-sqlite` | exit 1; `ok=false`; code `invalid_request`; category `invalid_input` | One issue: `path / invalid_format / file is not a database` | Present: `{"stdout":"","stderr":"","truncated":false}` | Holds: both rows state refusal, `path / invalid_format`, same message; entry calls it a worker row. |
| `m-bad-pagesize` | exit 1; `ok=false`; code `invalid_request`; category `invalid_input` | One issue: `path / invalid_format / file is not a database` | Present: `{"stdout":"","stderr":"","truncated":false}` | Holds: both rows state refusal, `path / invalid_format`, same message; entry calls it a worker row. |
| `m-journal-hot` | exit 1; `ok=false`; code `invalid_request`; category `invalid_input` | One issue: `path / invalid_format`; message: `Rollback journal may require recovery: /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-hot/db.sqlite-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported.` | Absent | Holds: prediction, SKILL and entry agree on a nonzero 28-byte journal header and the refusal/message; entry correctly labels snapshot/input, not worker. |
| `m-journal-short` | exit 1; `ok=false`; code `invalid_request`; category `invalid_input` | One issue: `path / invalid_format`; message: `Rollback journal may require recovery: /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-short/db.sqlite-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported.` | Absent | Holds: prediction, SKILL and entry agree on a 10-byte zero journal and the refusal/message; entry correctly labels snapshot/input, not worker. |
| `m-journal-empty` | exit 0; `ok=true`; no error | Evidence `ev_0ab137e3b8e59bb99203c9750cf05e3fa763733d6032b5b93020b17175cba2f4`; subject SHA-256 `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` | Not applicable: accepted envelope has no error/details | Holds: SKILL and entry say accepted, full database schema equals oracle, journal not copied; entry evidence ID matches envelope. Subject SHA matches the artifact digest, frozen mutant pin, and subject file. |
| `m-journal-zero28` | exit 0; `ok=true`; no error | Evidence `ev_b0856f85613341b0950f625803edb435e39f1fc71e5fe69a8e0b0ff765773ff3`; subject SHA-256 `bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a` | Not applicable: accepted envelope has no error/details | Holds: SKILL and entry say accepted, full database schema equals oracle, journal not copied; entry evidence ID matches envelope. Subject SHA matches the artifact digest, frozen mutant pin, and subject file. |

For both acceptances, `normalized_result.schema` has `scope=database` and `completeness=complete`; a read-only comparison of the committed normalized result with `sqlite_oracle.py`’s `comparable(expected_report(...))` returned equal. The prediction TSV has no evidence-ID or subject-digest columns; the acceptance IDs in the knowledge entry and the envelope are identical.

## Evidence and source checks

**Committed-record audit:** `functions.eval`, Python, title “Auditing six C2 envelope rows”, timeout 60 seconds. It read the six frozen prediction rows, six `runs.tsv` rows, six envelopes, the two documentation tables and the frozen claim pins; it used the independent local oracle only for the two accepted database files. UTC `2026-10-23T04:33:23.759638+00:00`; exit 0 (`AUDIT_EXIT 0`). Exact output excerpt:

```text
m-not-sqlite ... "code": true, "category": true, "one_exact_issue": true, "worker_output_presence": true ... exit=1 ok=False code=invalid_request category=invalid_input ... captured_output_present=True
m-bad-pagesize ... "code": true, "category": true, "one_exact_issue": true, "worker_output_presence": true ... exit=1 ok=False code=invalid_request category=invalid_input ... captured_output_present=True
m-journal-hot ... "code": true, "category": true, "one_exact_issue": true, "worker_output_presence": true ... exit=1 ok=False code=invalid_request category=invalid_input ... captured_output_present=False
m-journal-short ... "code": true, "category": true, "one_exact_issue": true, "worker_output_presence": true ... exit=1 ok=False code=invalid_request category=invalid_input ... captured_output_present=False
m-journal-empty ... "entry_evidence_id": true, "sha_matches_frozen_pin": true, "sha_matches_subject_file": true, "full_schema_equals_independent_oracle": true ... exit=0 ok=True evidence_id=ev_0ab137e3b8e59bb99203c9750cf05e3fa763733d6032b5b93020b17175cba2f4 subject_sha256=bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a ... oracle_equal=True
m-journal-zero28 ... "entry_evidence_id": true, "sha_matches_frozen_pin": true, "sha_matches_subject_file": true, "full_schema_equals_independent_oracle": true ... exit=0 ok=True evidence_id=ev_b0856f85613341b0950f625803edb435e39f1fc71e5fe69a8e0b0ff765773ff3 subject_sha256=bdf635be69850bd3be09c9a2dbeef7ddfb80036bd3ef3381383cd03b61e4a61a ... oracle_equal=True
ALL_CHECKS PASS
AUDIT_EXIT 0
```

**Fixture-byte audit:** read-only Python check of the six pinned fixture files, timeout 30 seconds. UTC `2026-10-23T04:34:08.182637+00:00`; exit 0. Exact output excerpt:

```text
m-not-sqlite ... bytes=1067008 predicate=True
m-bad-pagesize ... bytes=1067008 predicate=True
m-journal-hot ... bytes=28 predicate=True
m-journal-short ... bytes=10 predicate=True
m-journal-empty ... bytes=0 predicate=True
m-journal-zero28 ... bytes=28 predicate=True
BYTE_FIXTURE_CHECK PASS
AUDIT_EXIT 0
```

The envelopes match the runs recorded 2026-10-23 04:19:19–04:19:23 UTC. The byte audit confirms the claimed fixtures: first 16 database-header bytes zero; page-size bytes `03 00` (=768); hot journal nonzero and 28 bytes; short journal ten zero bytes; empty journal zero bytes; zero28 journal 28 zero bytes.

**REA dist stage/code-line check (read-only):** inspected `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`.

- `sqlite/SqliteDatabaseProvider.js:149-153` calls snapshot acquisition before worker execution. `sqlite/SqliteDatabaseSnapshot.js:105-121` observes the file set and checks the journal at `115-116` before copying/opening the snapshot. `SqliteDatabaseSnapshot.js:63-80` accepts an empty journal or exactly 28 read zero bytes and rejects a nonempty short read; its failure message matches the two journal envelopes. `SqliteDatabaseFailures.js:29-55` projects this pre-worker snapshot failure to an input error with a `path / invalid_format` issue and no captured worker output. This supports both journal rows’ stage and absent `captured_output`.
- `sqlite/SqliteDatabaseWorker.js:20-34` calls the SQLite inspection and maps non-memory/non-output-limit worker exceptions to `format`; `sqlite/SqliteDatabaseInspection.js:359-370` opens the snapshot through `DatabaseSync`. `SqliteDatabaseWorkerExecution.js:90-110` captures worker output and projects a failed worker reply with that captured output. This supports both database-format rows’ worker stage and present (empty) `captured_output`.
- `SqliteDatabaseSnapshot.js:120-150` copies the database and optional WAL, not the rollback journal. This supports the acceptance wording that the journal is not copied.

The six requested SKILL rows are at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md:1026-1031`; the corresponding entry rows and worker/stage explanation are at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md:13,29-34,43-45`. No overstatement or field mismatch was found in this scope.

## Residual risk / verification gaps

No gap for the six requested record/document comparisons or static stage checks. No REA invocation or C2-counter rerun was made; conclusions use the committed live-run receipts and envelopes, as scoped. No tools were installed, and no scratch artifacts were created.

Report: `.ufo/waves/round-31/w2/ReviewC2EnvC.md`
