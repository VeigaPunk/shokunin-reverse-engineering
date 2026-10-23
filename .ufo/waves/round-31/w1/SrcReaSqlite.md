# Round 31 S092 source-item report

## Behavior and gate

**Observation — source opened.** Retrieved `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` on 2026-10-23. The retained tarball is 5,634,033 bytes, SHA-256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`. Its digest matches the existing S090 tarball digest.

**Gate:** https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — access date 2026-10-23; SHA-256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`; quote: “inputBytes: 256 * 1024 * 1024,” — `package/dist/sqlite/SqliteDatabaseLimits.js:4` (5 contiguous words).

**Observation — requested source files.** The seven files matching `package/dist/sqlite/*.js`, plus `package/dist/domain/sqlite/sqliteDatabase.js` and `package/dist/artifacts/readStableArtifact.js`, were extracted and hashed. `cmp -s` against the matching installed `rea-agents` files succeeded for all nine pairs; all printed `byte-identical`. The output and SHA-256s are recorded below. The SQLite implementation shows the `inspect_sqlite_database` provider, bounded SQLite inspection, artifact snapshot/worker path, and schema/error contracts; these are implementation facts, not observed REA outcomes.

## Draft `corpus/SOURCES.md` row

```markdown
| S092 | rea-agents 6.5.0 SQLite database-inspection implementation — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz (members `package/dist/...`), compared with `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/` | code | A | The 6.5.0 `inspect_sqlite_database` implementation: input contract and limits, SQLite/WAL/journal snapshot, bounded read-only worker inspection, and result/error shaping; not observed REA outcomes | Tarball SHA-256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`; byte-identical to installed copy: `SqliteDatabaseFailures.js` SHA-256 `5a908695ec398079e97750bf60ece6ac273bdc74f06f7c9c1fd5777cfa90d419` `:25-26,104-105`; `SqliteDatabaseInspection.js` SHA-256 `edfcd90f9e2e1dbde531b6aafc4efb1bd105a372df617dee619a414425354970` `:358-367`; `SqliteDatabaseLimits.js` SHA-256 `92df76ffd21386dba134051791230e9d143220854a49e3e65e72d51daa074121` `:1-8`, especially `:4`; `SqliteDatabaseProvider.js` SHA-256 `018756d9d7f620995c9b8929d268c33ff1f7c973683bd0f4ddc6d781e5268104` `:18-19,150-169`; `SqliteDatabaseSnapshot.js` SHA-256 `c8af51f8496703a1992e7e7646c8bf8b6c56796a7571f5f8e9c84a284740ce19` `:104-121,134`; `SqliteDatabaseWorker.js` SHA-256 `ebb39f583db802ccb31b3ac328b0f8dd712fa6f0e5dd5a63da6908d7fe60cf63` `:11-20,38-41`; `SqliteDatabaseWorkerExecution.js` SHA-256 `6e49c2ab222982434d769fd279ad8053b857d6747f9b1101e07163d8a5e4c203` `:59-82,94`; `domain/sqlite/sqliteDatabase.js` SHA-256 `c7a0eff5674414110085ecf0257a71c1949de7e27be392ef2d8c8bd8cf000ae1` `:90-94`; `artifacts/readStableArtifact.js` SHA-256 `06a23746346a3de150f1aa21b781fffd8a482c0f5e98900c458f3f599b9d2707` `:29-32` | Follow the pinned SQLite path from bounded input and artifact capture through read-only worker inspection and validated output; use live receipts, not implementation alone, to establish observed refusals. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r31-sqlite-refusals.md |
```

S090 registers this same tarball for `dist/rust`; S092 scopes it to `dist/sqlite` and its cited dependencies. **Inference, not a run:** the same URL across the different scopes is expected to produce a W04 duplicate-URL warning; W04 is a warning, not a validation failure. I did not run the census.

## Commands and outcomes

All commands below were bounded with `timeout`; the date capture after the source checks was `2026-10-23T04:13:03+00:00`. The exact curl wall-clock time was not separately recorded; the fetch completed before the post-fetch UTC capture returned `2026-10-23T04:10:25+00:00`.

- `timeout 300 curl -fL --output /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/rea-agents-6.5.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` — **exit 0**. Exact output excerpt: `100 5.37M 100 5.37M 0 0 ...`. Access date: 2026-10-23.
- `timeout 300 sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/rea-agents-6.5.0.tgz && timeout 300 stat -c 'size_bytes=%s' /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/rea-agents-6.5.0.tgz` — **exit 0**; exact output: `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/rea-agents-6.5.0.tgz` and `size_bytes=5634033`.
- `timeout 300 tar -xzf /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/rea-agents-6.5.0.tgz -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite --wildcards 'package/dist/sqlite/*.js' 'package/dist/domain/sqlite/sqliteDatabase.js' 'package/dist/artifacts/readStableArtifact.js'` — **exit 0**, no stdout. Only the nine requested extracted members were retained.
- `timeout 300 sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/*.js /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/domain/sqlite/sqliteDatabase.js /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/artifacts/readStableArtifact.js` — **exit 0**. Exact output:

```text
5a908695ec398079e97750bf60ece6ac273bdc74f06f7c9c1fd5777cfa90d419  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseFailures.js
edfcd90f9e2e1dbde531b6aafc4efb1bd105a372df617dee619a414425354970  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseInspection.js
92df76ffd21386dba134051791230e9d143220854a49e3e65e72d51daa074121  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseLimits.js
018756d9d7f620995c9b8929d268c33ff1f7c973683bd0f4ddc6d781e5268104  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseProvider.js
c8af51f8496703a1992e7e7646c8bf8b6c56796a7571f5f8e9c84a284740ce19  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseSnapshot.js
ebb39f583db802ccb31b3ac328b0f8dd712fa6f0e5dd5a63da6908d7fe60cf63  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseWorker.js
6e49c2ab222982434d769fd279ad8053b857d6747f9b1101e07163d8a5e4c203  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseWorkerExecution.js
c7a0eff5674414110085ecf0257a71c1949de7e27be392ef2d8c8bd8cf000ae1  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/domain/sqlite/sqliteDatabase.js
06a23746346a3de150f1aa21b781fffd8a482c0f5e98900c458f3f599b9d2707  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/artifacts/readStableArtifact.js
```

For each pair below, the command was `timeout 300 cmp -s <extracted absolute path> <installed absolute path> && printf '<basename> byte-identical\n'`; each command exited **0** and emitted the exact shown line (comparison capture by `2026-10-23T04:13:03Z`):

- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseFailures.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseFailures.js` → `SqliteDatabaseFailures.js byte-identical`
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseInspection.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseInspection.js` → `SqliteDatabaseInspection.js byte-identical`
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseLimits.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseLimits.js` → `SqliteDatabaseLimits.js byte-identical`
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseProvider.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseProvider.js` → `SqliteDatabaseProvider.js byte-identical`
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseSnapshot.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseSnapshot.js` → `SqliteDatabaseSnapshot.js byte-identical`
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseWorker.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseWorker.js` → `SqliteDatabaseWorker.js byte-identical`
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/sqlite/SqliteDatabaseWorkerExecution.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/sqlite/SqliteDatabaseWorkerExecution.js` → `SqliteDatabaseWorkerExecution.js byte-identical`
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/domain/sqlite/sqliteDatabase.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/sqlite/sqliteDatabase.js` → `domain/sqlite/sqliteDatabase.js byte-identical`
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/package/dist/artifacts/readStableArtifact.js` vs `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/artifacts/readStableArtifact.js` → `artifacts/readStableArtifact.js byte-identical`

## Touched surfaces, limits, and provenance

- **Lane surface:** only this report is written. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` was not edited; the S092 row above is a draft for L1 integration.
- **Used-by limit:** reading `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` returned `Path ... not found`. The draft has the requested `mined` status and used-by path, but the cited entry is not yet present, so this status/path pair is not currently validated against the SOURCES contract; no census was run.
- **Out of scope:** no REA invocation, carrier/mutant access, counter, tests, census, source registry edit, product-code change, tool install, or git/jj operation.
- **Retained artifact paths and SHA-256:** `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcReaSqlite/rea-agents-6.5.0.tgz` — `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`; the nine extracted paths and hashes are listed above. No other scripts, drafts, or raw command-output files were retained.

Report: `.ufo/waves/round-31/w1/SrcReaSqlite.md`
