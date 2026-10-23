# ReviewC2EnvD — C2 rows m-journal-symlink, m-db-symlink, m-directory, m-over-256mib, m-wal-over

Reviewer seat, Kaidoku round 31 wave 2. Lane read-only; no artifacts written outside this report (no scratch items created; sha256 list therefore empty). No tool installs performed. Report time 2026-10-23T04:35:55Z. No `PIN ... absent or altered` was observed (the counter itself was not run by this seat; pins were re-measured directly, below).

## Method

Producing commands (all read-only, run 2026-10-23 ~04:20–04:36 UTC, all exit 0):

1. `read` of the five committed envelopes `corpus/evidence/round-31/c2/envelopes/<id>.json`, `corpus/evidence/round-31/c2/predictions.tsv`, `corpus/evidence/round-31/c2/runs.tsv`, `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md`, `SKILL.md:1008-1040`, `.ufo/waves/round-31/claims.json`.
2. `grep '^m-(journal-symlink|db-symlink|directory|over-256mib|wal-over)\t' corpus/evidence/round-31/c2/predictions.tsv` — exact frozen message templates (lines 20–24).
3. `grep '\{P\}|replace|journal' tools/round-31/c2-sqlite-refusals.py` — substitution rule, line 164: `"message": row["message"].replace("{P}", path)`; full-envelope compare at 163–166; SKILL row gate at 266–270; pin gate at 305–314.
4. `nl -ba` over the cited REA 6.5.0 dist files under `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` (read-only): `sqlite/SqliteDatabaseSnapshot.js`, `sqlite/SqliteDatabaseFailures.js`, `sqlite/SqliteDatabaseLimits.js`, `artifacts/readStableArtifact.js`.
5. Mutant ground truth: `stat -c '%n | %F | size=%s' /fast/scratch/hyaku/kaidoku-r31/mutants/<id>/*`, `readlink` on both symlinks, `sha256sum` of m-over-256mib/db.sqlite, m-wal-over/db.sqlite, m-wal-over/db.sqlite-wal, m-journal-symlink/db.sqlite, m-journal-symlink/db.sqlite-journal, carriers/chinook.sqlite, and `stat -c '%n blocks=%b size=%s'` for the two sparse members.

Freeze identity: `sha256sum corpus/evidence/round-31/c2/predictions.tsv` → `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8` = `claims.json` `frozen_inputs` value (observation). The rows reviewed are the frozen ones.

## Per-id verdicts

Common facts (observation, all five): envelope `ok:false`; `error.code:"invalid_request"`; `error.category:"invalid_input"`; `error.details.issues` exactly one entry with `path:["path"]`; **no `details.captured_output`** in any of the five — required, since the entry marks all five rows stage `snapshot / input` and states only "worker" rows carry `captured_output`; `meta.command:"inspect-sqlite-database"` (meta excluded from comparison). `runs.tsv`: exit 1, verdict `P2-match` for all five, inside the entry's verified-at window 04:19:10–04:19:27+00:00 at pkg 6.5.0. No acceptance rows in this seat's set, so the evidence_id / subject-sha acceptance checks are N/A.

| id | verdict | cross-walk |
|---|---|---|
| `m-journal-symlink` | **holds** | Envelope issue `{["path"], invalid_format, "Expected a regular journal without a symlink: /fast/scratch/hyaku/kaidoku-r31/mutants/m-journal-symlink/db.sqlite-journal"}`. Frozen row 20 message `Expected a regular journal without a symlink: {P}-journal`; with counter line 164 (`{P}` → request path) this substitutes to the envelope message byte-for-byte. SKILL row and entry row both say `path` / invalid_format, message `Expected a regular journal without a symlink: <path>-journal`, stage snapshot/input — all match. Mutant: `db.sqlite` regular 1,067,008 B, sha256 `bdf635be…4a61a` = claims `mutant_sha256` pin; `db.sqlite-journal` is a symlink → `carriers/chinook.sqlite` = claims sibling pin string `symlink:/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite` (observation). |
| `m-db-symlink` | **holds** | Envelope issue `{["path"], invalid_format, "Expected a regular file without a symlink: /fast/…/m-db-symlink/db.sqlite"}` = frozen row 21 with `{P}`→path. SKILL row "the database path is a symlink to a valid database" — `readlink` → `/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite`, a valid C1 carrier (observation). Entry row matches; stage snapshot/input, no captured_output — consistent. |
| `m-directory` | **holds** | Envelope issue `{["path"], invalid_format, "Expected a regular file without a symlink: /fast/…/m-directory/db.sqlite"}` = frozen row 22. SKILL/entry rows match. Mutant: `stat` reports `%F` = `directory` for `db.sqlite` (observation). Message text is shared with m-db-symlink (regular-file ×2), exactly as the entry's Limits section states. |
| `m-over-256mib` | **holds** | Envelope issue `{["path"], out_of_range, "Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: /fast/…/m-over-256mib/db.sqlite"}` = frozen row 23. Mutant: regular file size 268,435,457 = 268,435,456 + 1, `blocks=8` (4 KiB allocated for a 256 MiB+1 file — sparse, as SKILL/entry/prediction `build=sparse-268435457` say); sha256 `8a14e15c…0fc5b` = claims pin. SKILL row "sparse database of 268,435,457 bytes" verified. |
| `m-wal-over` | **holds** | Envelope issue `{["path"], out_of_range, "Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: /fast/…/m-wal-over/db.sqlite"}` = frozen row 24. Mutant: db 1,067,008 B (sha `bdf635be…` = pin) + `-wal` 267,368,449 B (`blocks=0`, fully sparse; sha `e1945862…24292` = claims `mutant_sibling_sha256["m-wal-over-wal"]`). Sum 1,067,008 + 267,368,449 = 268,435,457 = budget + 1 — exactly the SKILL/entry row text "(sum = budget + 1)" (observation, arithmetic re-checked). |

## Stage/code-line claims vs the installed 6.5.0 dist (read-only)

- `SqliteDatabaseSnapshot.js:52-54` — exact: `verifyInactiveJournal` head, `if (!before.isFile() || before.isSymbolicLink()) throw new ArtifactReaderFailure("path", \`Expected a regular journal without a symlink: ${path}\`)`; called at 115-116 with `` `${path}-journal` `` (m-journal-symlink). ✓
- `readStableArtifact.js:30-33` — the regular-file check sits at 31–33 (`lstat`, `!before.isFile() || isSymbolicLink()` → `"Expected a regular file without a symlink"`); 30 is the preceding `assertReadActive` (m-db-symlink, m-directory). Construct contained, as the entry's pointer audit ("21 exact, 14 contain the construct") describes. ✓
- `SqliteDatabaseSnapshot.js:44-51,121` — the `readObservedArtifact` wrapper (43–51) and its call at 121 with `SQLITE_DATABASE_LIMITS.inputBytes`. ✓
- `SqliteDatabaseLimits.js:4` — exact: `inputBytes: 256 * 1024 * 1024` = 268,435,456. ✓
- `SqliteDatabaseSnapshot.js:117-119` — exact: size sum `database.size + (wal?.size ?? 0n)`, compare against `BigInt(inputBytes)`, budget message throw. Checked from `optionalStat`/`lstat` values (line 108) before any read — backs the entry's "checked from `lstat` sizes before reading, so a sparse file triggers it". ✓
- `SqliteDatabaseFailures.js:46-54` — contains the projection at 49–54: `reason: cause.reason === "limit" ? "out_of_range" : "invalid_format"` on `path:["path"]` — grounds out_of_range for the budget rows and invalid_format for the three regular-file/journal rows, all as `AnalysisInputError` (`invalid_request` / `invalid_input`, matching every envelope). ✓
- Entry teaching bullet order (absence 113–114 → journal 115–116 → budget 117–119 → regular-file check inside `readStableArtifact` via 121) matches the code order; all before any SQLite open — no worker, hence no `captured_output`. Envelopes agree. ✓
- "REA never follows either symlink" is backed by `O_NOFOLLOW` opens (Snapshot.js:55; readStableArtifact.js:36) in addition to the lstat checks. ✓

## Wording audit (SKILL / entry vs envelopes)

- SKILL.md:1010 blanket claim "Every refusal exits 1 with `error.category: invalid_input` and exactly one `details.issues` entry" — verified for all five rows here (exit from runs.tsv; the rest from envelopes). No overstatement found in any SKILL or entry sentence for these five ids; input-condition text (symlink targets, directory, sparse sizes, sum arithmetic) matches the measured mutant ground truth.
- Known and honestly handled: frozen `predictions.tsv` row 24 code-pointer note says "WAL 267367449 bytes"; the measured WAL is 267,368,449. The entry's "Corrections to the frozen predictions file" section states exactly this with the correct figure, notes the frozen file stays as frozen, and that the matched message carries no size — verified accurate (SKILL row already carries the correct 267,368,449). This is a documented typo in a frozen pointer note, not a mismatch in any compared field.
- Entry pin-drift ("at 6.7.0 the budget refusal becomes `resource_constraint` … Not run live at 6.7.0") and SKILL's "(static reading, not run)" are flagged as static, not observed — honest.

## Residual risk / verification gaps

- This seat did not re-run the counter; live-envelope equality (`ReRunC2`) and counter-internals sweeps (`MutC2Counter`) are sibling seats'. The `{P}` substitution and full-envelope-minus-meta compare were verified by reading `tools/round-31/c2-sqlite-refusals.py`, not by executing it.
- `m-journal-symlink/db.sqlite` and `m-wal-over/db.sqlite` were hashed directly (both `bdf635be…`, matching pins); `m-db-symlink`'s target was verified by `readlink` + the carrier's hash, not by hashing through the symlink.
- Statement "the counter prints `PIN ... absent or altered`" is unknown here (counter not run by this seat); direct pin re-measurement found every pin for these five ids intact.

**Conclusion: all five assigned rows hold. No unbacked or overstated wording found in SKILL.md or the entry for these ids.**
