# ReopenS092 — SOURCES row S092 and its Gate quote, re-opened

Seat `KaidokuR31.ReopenS092` (wave 2, one v1 falsify seat). Lane base `c369242fee9f559f895e3f7956b1242076c7b1be`; row introduced at
`0007731e`; lane tip during this seat `1288285eed81395e6af7c279a173b117b2c2eaa3`; every command below ran 2026-10-23, 04:29–04:33 UTC,
read-only, no REA, no git/jj writes, no subagent, no install.

## Verdict

- **Row verdict: disagree** — not on the source, the hashes, the scope or the Gate quote (all hold, below), but on one field as written:
  the row's `used-by` cell is **incomplete** (F1), and the lesson's change-log sentence that describes `used-by` for the six new rows is
  false (F2). Admission decision "admit, tier A, status `mined`" holds after the `used-by` fix (`mined` is already satisfied by the listed path).
- **Gate quote: holds** — located at `package/dist/sqlite/SqliteDatabaseLimits.js:4` in the tarball bytes, verbatim, 6 whitespace tokens
  (≤25), grounds the "bounded input" clause of `teaches`.
- **Gate table row text (lesson:31): holds** — URL, access date, tarball SHA prefix/suffix, "nine modules byte-identical to the installed copy"
  and the duplicate-URL note all reproduce.

## Source record (CORPUS.md §*SOURCES.md*, rule 1; rule 6: no credentials)

- URL: `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`
- Access date: 2026-10-23 (fetched 2026-10-23T04:29:48Z)
- Bytes read: 5,634,033; **sha256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`**
- Located quote, ≤25 contiguous words: `inputBytes: 256 * 1024 * 1024,` — `package/dist/sqlite/SqliteDatabaseLimits.js:4`

```
$ cd /fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS092/dl && date -u +%Y-%m-%dT%H:%M:%SZ && \
  curl -sS -L --max-time 300 -o rea-agents-6.5.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz \
  -w 'http_code=%{http_code} size=%{size_download}\n' && sha256sum rea-agents-6.5.0.tgz && wc -c rea-agents-6.5.0.tgz
2026-10-23T04:29:48Z
http_code=200 size=5634033
531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699  rea-agents-6.5.0.tgz
5634033 rea-agents-6.5.0.tgz
exit 0  (curl success proven by the `&&` chain reaching sha256sum)
```

The member's own manifest re-states the pin: `tar -xzOf dl/rea-agents-6.5.0.tgz package/package.json | grep -m2 -E '"(name|version)"'`
→ `"name": "rea-agents",` / `"version": "6.5.0",` (2026-10-23T04:31:47Z, exit 0).

## Checks

### A. SHA-256 agrees with both records

```
[UTC 2026-10-23T04:32:34Z] $ sha256sum tarball
531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699  .../dl/rea-agents-6.5.0.tgz
exit=0
```

- `corpus/SOURCES.md:98` anchor cell: `Tarball SHA-256 \`531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699\`` — **equal** (observation).
- `corpus/lessons/round-31.md:31` Gate sha column: `` tarball `531717a0…e699` `` — **equal as an abbreviation** (observation; the Gate table
  abbreviates sha256 in every row, and the contract's Gate rule §1 requires URL + date + quote, not a full sha).
- Wave-1 report `.ufo/waves/round-31/w1/SrcReaSqlite.md:5,7` carries the same full digest — consistent.

### B. The nine module hashes in the anchor cell reproduce, byte-identical to the installed copy

```
[UTC 2026-10-23T04:32:34Z] $ 9 module hashes tarball vs installed
SAME sqlite/SqliteDatabaseFailures.js 5a908695ec398079e97750bf60ece6ac273bdc74f06f7c9c1fd5777cfa90d419
SAME sqlite/SqliteDatabaseInspection.js edfcd90f9e2e1dbde531b6aafc4efb1bd105a372df617dee619a414425354970
SAME sqlite/SqliteDatabaseLimits.js 92df76ffd21386dba134051791230e9d143220854a49e3e65e72d51daa074121
SAME sqlite/SqliteDatabaseProvider.js 018756d9d7f620995c9b8929d268c33ff1f7c973683bd0f4ddc6d781e5268104
SAME sqlite/SqliteDatabaseSnapshot.js c8af51f8496703a1992e7e7646c8bf8b6c56796a7571f5f8e9c84a284740ce19
SAME sqlite/SqliteDatabaseWorker.js ebb39f583db802ccb31b3ac328b0f8dd712fa6f0e5dd5a63da6908d7fe60cf63
SAME sqlite/SqliteDatabaseWorkerExecution.js 6e49c2ab222982434d769fd279ad8053b857d6747f9b1101e07163d8a5e4c203
SAME domain/sqlite/sqliteDatabase.js c7a0eff5674414110085ecf0257a71c1949de7e27be392ef2d8c8bd8cf000ae1
SAME artifacts/readStableArtifact.js 06a23746346a3de150f1aa21b781fffd8a482c0f5e98900c458f3f599b9d2707
exit=0
```
Comparison target: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`. Nine of nine equal, so both the anchor
hashes and "byte-identical to the installed copy" are observations, not inferences.

### C. Quote is verbatim, contiguous and ≤25 words

```
[UTC 2026-10-23T04:32:34Z] $ tar -xzOf dl/rea-agents-6.5.0.tgz package/dist/sqlite/SqliteDatabaseLimits.js | sed -n '4p' | cat -A
    inputBytes: 256 * 1024 * 1024,$
exit=0
[UTC 2026-10-23T04:32:34Z] $ ... | grep -cF 'inputBytes: 256 * 1024 * 1024,'
1
exit=0
[UTC 2026-10-23T04:32:34Z] $ printf '%s\n' 'inputBytes: 256 * 1024 * 1024,' | wc -w
6
exit=0
```
Line 4 is exactly `    inputBytes: 256 * 1024 * 1024,` (4-space indent, trailing comma); the quoted string is a contiguous substring
(`grep -cF` = 1) and is 6 whitespace-separated tokens / 4 alphanumeric words — **≤ 25 either way**. Location `:4` is correct; the same
constant also occurs in the bundled CLI/MCP copies (`dist/cli-runtime/cli.js:5737`, `dist/mcp/main-kBXHZ8S5.js:22344`), so the row's
choice of the source module is the honest anchor, not the bundle. **Gate quote verdict: holds.**

### D. Row columns against the CORPUS.md contract

Contract shape (CORPUS.md:86-108): 11 columns
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`, `id` unique next unused,
`kind` in the nine-value enum, `tier` scoped A/B/C with A allowed for source code, `anchor` = exact section/page/line **plus revision**,
`status` in `queued|mined|rejected`, `opened` ISO date, `recheck` ISO date or cadence, `used-by` = repo-relative paths of the entries or
lessons **citing** the row.

```
[UTC 2026-10-23T04:32:34Z] $ awk -F'|' 'NR==98{print "NF="NF; print "used-by=["$12"]"}' corpus/SOURCES.md
NF=13
used-by=[ corpus/knowledge/2026-10-23-r31-sqlite-refusals.md ]
exit=0
[UTC 2026-10-23T04:32:40Z] $ census: duplicate ids            (uniq -d over all S rows)
exit=0                                                         # prints nothing: no duplicate id
[UTC 2026-10-23T04:32:40Z] $ S092 enum fields
4=[code] 5=[A] 9=[mined] 10=[2026-10-23] 11=[on-release] 12=[corpus/knowledge/2026-10-23-r31-sqlite-r…]
exit=0
[UTC 2026-10-23T04:32:40Z] $ used-by path exists
exists_exit=0
```
Census on the whole file (receipt in `lines.log`): `[UTC 2026-10-23T04:33:24Z] malformed rows` → `malformed=0`, exit 0.
So: 11 cells, no `|` inside a cell, unique id, kind `code` ✔ enum, tier `A` ✔ (source code is A; not `community`), status `mined` ✔ and
satisfied by one cited path, `opened` matches the Gate access date, `recheck` `on-release` ✔ cadence.

**Anchor, literal reading:** the cell is `Tarball SHA-256 \`5317…e699\`; byte-identical to installed copy: \`<module>\` SHA-256 \`…\` \`:25-26,104-105\`; …`
— it pins exact line ranges and content digests but contains no version string, commit or publication date inside the `anchor` cell itself
(the revision "6.5.0" lives in `source`). Content-addressed pinning is stronger than a version string and matches lane practice
(S090's source/anchor and S096/S097's hash anchors), so I record this as a **minor literal deviation, substance holds** (F4).

**`source` cell:** title — URL — plus `(members \`package/dist/...\`), compared with \`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/…/dist/\``.
The contract's `source` is "title — canonical URL or DOI"; the extra member scope and compared local path are outside that literal form but
identical to the accepted S090/S081 pattern, and the compared path is verified identical. **Minor, no action** (F5).

**`teaches`:** two imperatives ("Follow the pinned SQLite path …; use live receipts, not implementation alone …"). The first is the
learner benefit, the second a usage caution; the Gate quote grounds only the "bounded input" clause while the rest rests on the anchor's
line pointers. Acceptable in substance, but the arrow "quote grounds teaches" is partial (F6, observation-level).

### E. `used-by` is incomplete — the defect this re-open finds

```
[UTC 2026-10-23T04:32:34Z] $ grep -n 'S092' corpus/knowledge/2026-10-23-r31-sqlite-positive.md
3:source: S096 (…); S097 (…); S093 (…); S094 (…); S095 (…); S092 (REA 6.5.0 SQLite reader code, for the inferences below)
51:Inference (S092 code, `dist/sqlite/SqliteDatabaseInspection.js:144-294`): …
exit=0
[UTC 2026-10-23T04:32:34Z] $ sed -n '3p' corpus/knowledge/2026-10-23-r31-sqlite-refusals.md
source: S092 (REA 6.5.0 SQLite reader code, `package/dist/sqlite/`, `dist/domain/sqlite/`, `dist/artifacts/readStableArtifact.js`, byte-iden…
exit=0
```
Two round-31 entries cite S092: `2026-10-23-r31-sqlite-refusals.md` (line 3) and `2026-10-23-r31-sqlite-positive.md` (line 3 `source:`
and line 51 body). The row's `used-by` lists only the refusals entry. The contract's `used-by` is "repo-relative paths of the knowledge
entries or lessons citing the row" (CORPUS.md:107-108) and lane precedent for a two-entry citation exists (S091 lists both round-30
entries, `corpus/SOURCES.md:97`). **F1 verdict: fails (contract breach, omission).** Append-only fix permitted by rule 2: add
`corpus/knowledge/2026-10-23-r31-sqlite-positive.md` to the cell and log old→new in `corpus/lessons/round-31.md`.

Adjacent, same class (not my row, recorded because it falsifies F2): the refusals entry's `source:` also cites S096 and S097, whose
`used-by` cells (lines 102–103) list only the positive entry.

```
[UTC 2026-10-23T04:32:34Z] $ sed -n '41p' corpus/lessons/round-31.md
Row changes old→new: none to existing rows; S092–S097 new (status `mined`, used-by the two round-31 entries).
exit=0
```
**F2 verdict: fails.** No S092–S097 row lists two entries: S092, S096, S097 list one and each is missing the other citer; S093–S095 are
cited by one entry only. The sentence overstates `used-by` for all six new rows (S093–S095 by claiming a second citer that does not exist).
The row's own Gate decision cell (line 31) does not repeat the claim, so the error is confined to the change log at line 41.

### F. Anchor line references spot-checked (all land on the described code)

Read from the extracted tarball, one batch at `[UTC 2026-10-23T04:33:24Z]`, every command exit 0 (receipt `lines.log`):
- `SqliteDatabaseLimits.js:1-8` — `SQLITE_DATABASE_LIMITS` object, `:4` the quoted `inputBytes`.
- `SqliteDatabaseFailures.js:25-26,104-105` — `sqliteDatabaseFailure` / `ownedCommandFailure`, operation `"inspect_sqlite_database"`.
- `SqliteDatabaseInspection.js:358-367` — `inspectSqliteDatabaseSnapshot`, `new DatabaseSync(snapshotPath, { readOnly: true, allowExtension: false, … })`.
- `SqliteDatabaseProvider.js:18-19,150-169` — provider doc "without source writes" and the snapshot→worker→`safeParse` path.
- `SqliteDatabaseSnapshot.js:104-121,134` — "Freeze a stable offline file set without ever opening the source through SQLite"; `path`, `-wal`, `-journal`;
  combined `inputBytes` budget; WAL artifact capture.
- `SqliteDatabaseWorker.js:11-20` — strict worker request schema and reply.
- `SqliteDatabaseWorkerExecution.js:59-82,94` — owned worker invocation (`--max-old-space-size=256`), timeout/diagnostic limits, `readStableArtifact`.
- `domain/sqlite/sqliteDatabase.js:90-94` — strict output schema ("without arbitrary SQL").
- `artifacts/readStableArtifact.js:29-32` — bounded stable read, regular-file/symlink checks.

### G. `scope` claims are present in the cited code

Observation: input contract/limits (Limits.js:1-8; domain schema:90-94), SQLite/WAL/journal snapshot (Snapshot.js:107-121,132-149; journal
recovery refusal :79-80), bounded read-only worker inspection (Inspection.js:359-362; WorkerExecution.js:79-80), result/error shaping
(Failures.js:25-26,104-105; Provider.js:167+ `safeParse`), and the disclaimer "not observed REA outcomes" is true (the row teaches
implementation only). Scope cell holds.

## Findings

| # | Finding | Label | Verdict |
|---|---|---|---|
| F1 | S092 `used-by` omits `corpus/knowledge/2026-10-23-r31-sqlite-positive.md`, which cites S092 at `:3` and `:51`; contract CORPUS.md:107-108 | observation | **fails** |
| F2 | `lessons/round-31.md:41` says S092–S097 are "used-by the two round-31 entries"; no such row exists (S092/S096/S097 each list one, S093–S095 one) | observation | **fails** |
| F3 | Wave-1 `SrcReaSqlite.md:7` calls the quote "(5 contiguous words)"; it is 6 whitespace tokens (4 alphanumeric) | observation | **fails** (number drift in the wave-1 report only; the Gate table and row carry no count) |
| F4 | `anchor` carries no explicit version/commit/date token; revision is pinned by the tarball SHA-256 and `source`'s "6.5.0" | observation + contract reading | **holds in substance**, minor literal deviation |
| F5 | `source` cell carries member scope and a compared local path beyond "title — canonical URL" | observation | **holds** (S090/S081 precedent; compared path verified identical) |
| F6 | `teaches` has a directive plus a caution; the Gate quote grounds only the "bounded input" clause | inference | **holds in substance**, partial quote-to-teaches grounding |

Not evaluated / unknown: whether the L1 intended `used-by` to be a superset of citers during drafting (motive is not evidence); whether
S096/S097's matching omission is scheduled for a sibling seat (outside this ticket).

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS092/`)

| path | sha256 |
|---|---|
| `dl/rea-agents-6.5.0.tgz` (5,634,033 bytes, fetched 2026-10-23T04:29:48Z) | `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699` |
| `pkg/package/dist/sqlite/SqliteDatabaseLimits.js` (extracted) | `92df76ffd21386dba134051791230e9d143220854a49e3e65e72d51daa074121` |
| `evidence.sh` | `6b9aa49e97c32eaeff241136624bb597a2868381841dc52d7be4d954c3f1f309` |
| `evidence.log` (timestamped receipts A–E) | `fd8409b5f28aecf5db7632bfaf520b3a6eb94f76d958cf470a29d3e5b06a5914` |
| `census.log` (duplicate-id, enum, path-existence receipts) | `9f235b58d0d92baa19fe94b66da61888c44489bfd8417348caf62521830adce7` |
| `lines.log` (anchor line-ref batch + malformed-row census, 04:33:24Z) | `9d008904d950dcb99ac451fb9dba1151176a30677ccedef22815bee17cf0e38a` |
| `evidence-extras.txt` (package.json name/version, NF, positive-entry count) | `c87577c3097a800ab28d398ab130677d3269feee5deac63f95c17537a7b646c7` |
| `pkg/package/**` (full extraction, 9 modules plus the rest of `dist/`) | per-file hashes in the anchor cell above |

Installs/updates: none. No process left running; every command ran under the harness timeout and the last `exit=` is 0.
