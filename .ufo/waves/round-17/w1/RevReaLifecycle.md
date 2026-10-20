# REA 6.5.0 Ghidra session lifecycle — reconstruction (r17 W1, advisory)

Seat: `KaidokuR17.RevReaLifecycle-3`. Date: 2026-10-20. Read-only lane.
Scope: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (rea-agents 6.5.0), the bundled
Ghidra bridge Java, installed Ghidra 12.1.4 headless sources, and the round-17 pilot artifacts already on
disk. No REA analyze/search/decompile, no Ghidra launch, no carrier execution, no file written except this
report. `grep` here is used only for literal location of code; the semantic claims below are each anchored
to the statement that implements them.

Path abbreviations used below:

- `DIST` = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist`
- `PKG`  = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
- `G12`  = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` (sources = `Ghidra/Features/Base/lib/Base-src.zip`,
  log config = `Ghidra/Framework/Generic/lib/Generic.jar`)
- `P`    = `.ufo/waves/round-17/pilot`

Labels: **[obs]** observed (tool output / file bytes), **[inf]** inference from code (stated as such).

---

## 1. Where the session directory comes from

1. Root parent is `ghidraSessionRoot()` evaluated **once at module load**
   (`DIST/ghidra/GhidraClient.js:32` `const SESSION_ROOT = ghidraSessionRoot();`). It returns
   `resolve(tmpdir())`, unless any path element starts with `.`, in which case it falls back to `/tmp`
   (`DIST/ghidra/GhidraSessionRoot.js:28-39`; comment at `:19-27` explains Ghidra's
   `NamingUtilities.checkName` rejects dot-prefixed project path elements). So a `TMPDIR=~/.cache/...`
   does not move the session dir; it is forced to `/tmp`.
2. The runtime root is `mkdtemp(join(parent, "rea-ghidra-"))`
   (`DIST/process/PrivateRuntimeRoot.js:38`), i.e. `/tmp/rea-ghidra-XXXXXX`, mode 0700 by `mkdtemp`
   (`:39-40` comment; no chmod). Allocated at provider start
   (`DIST/ghidra/GhidraClient.js:395-398`, `prefix: "rea-ghidra-"`).
3. A **second** root `/tmp/rea-ghidra-socket-XXXXXX` exists only when the unix-socket path would exceed
   the sockaddr limit (`>107` bytes on Linux): `DIST/ghidra/GhidraTransport.js:9-26`. With the default
   `/tmp` parent the path is `.../bridge.sock`, ~35 bytes, so in practice **one directory per session**.
4. There is **no reaper/sweeper** for stale dirs: the only directory-prefix literals are the two above
   (`grep -rn 'rea-ghidra-' DIST` → `GhidraClient.js:397`, `GhidraTransport.js:18`; the only other match
   is the seed format id `rea-ghidra-seeds-v1`, `GhidraAnalysisSeeds.js:10`, which is not a path).
   Cleanup is exclusively parent-process-driven.

## 2. File inventory (what a copier can see)

Fixed layout: `ghidraRuntimePaths()` at `DIST/ghidra/GhidraLauncher.js:440-451`.

| Entry | Writer | Content / lifetime |
|---|---|---|
| `session.json` | REA, `write-file-atomic`, mode 0600 (`GhidraLauncher.js:95-107`, `:511-517`) | `transport, endpoint_path, token, run_id, target_sha256, provider_version, profile_digest` (+`analysis_extensions`). **Bearer token** = 64 hex chars. Deleted by the *bridge itself* on POSIX at script start (`PKG/bridge/ghidra/ReaGhidraBridge.java:191-197`), i.e. it disappears before the client can issue any request. |
| `ownership.json` | REA, mode 0600 (`GhidraLauncher.js:195-205`) | run_id, transport, endpoint_path, pid, process_group_id, parent_pid, ownership_kind, launcher, headless_script, created_at. Lives until root deletion. |
| `ghidra.log` | Ghidra log4j2 `detail` appender (`-log`, `GhidraLauncher.js:382-383`) | Whole JVM log incl. every analyzer. Line format `%d{yyyy-MM-dd HH:mm:ss} %-5p (%c{1}) %m %ex %n` (`G2 generic.log4j.xml` → `log4j-appender-rolling-file.xml`). |
| `script.log` | Ghidra log4j2 `script` appender (`-scriptlog`, `GhidraLauncher.js:384-385`) | Only `Format:GhidraScript` messages (`log4j-appender-rolling-file-scripts.xml` regex filter). Observed content: one line per script print, e.g. the no-return refit (`P/shfmt-log/script.log:1`). **No Go analyzer diagnostics land here.** |
| `target-<sha12><ext>` | REA copy of the carrier, `open(..., "wx", 0600)`, streamed with SHA-256 verify (`DIST/ghidra/GhidraTargetSnapshot.js:10-14`, `:31`) | name = `target-${sha256.slice(0,12)}${extname if /^\.[A-Za-z0-9]{1,12}$/ else ".bin"}` (`:11`, `:76-79`). Removed on copy failure (`:50-58`); otherwise lives until root deletion. Observed names: `target-58f765638eed.bin`, `target-bab29b2ca7a9.bin` (`P/shfmt-log/ghidra.log:2,119`; `P/esbuild-0.25.12-log/ghidra.log:2,118`). |
| `project/` | Ghidra (`-import <root>/project` + `rea-project`) | Ghidra project; `-readOnly` forces `deleteProject` (`HeadlessOptions.java:376-382`; applied `HeadlessAnalyzer.java:457-459`) so Ghidra deletes it itself before JVM exit. Also falls to the root `rm -rf`. |
| `home/`,`tmp/`,`cache/`,`config/`,`data/` | REA `mkdir(recursive, 0700)` (`GhidraLauncher.js:482-509`) | Ghidra HOME/TMPDIR/XDG roots (`GhidraLauncher.js:518-545`); `config/ghidra/<release>/` pre-created (`:482-509`). Pilot shows `config/vgpnk-ghidra/ghidra_12.1.4_PUBLIC/preferences` (`P/shfmt-log/ghidra.log:4`). |
| `bridge.sock` | bridge Java, `rw-------` (`ReaGhidraBridge.java:261-272`) | Deleted by bridge in its `finally` (`:270-272`), then by `rm -rf`. |
| `seeds/`, `extensions/` | REA, only when configured (`GhidraAnalysisSeeds.js:164-174`, `extensions/GhidraExtensions.js:132-143`) | not present for the r17 carriers. |

## 3. Lifecycle timeline (POSIX, CLI `rea analyze`)

The CLI is deliberately single-shot: *"Open one binary, execute one tool, and always release provider
resources. Unlike MCP mode, every CLI invocation is intentionally isolated"*
(`DIST/application/DirectAnalysis.js:26-30`), enforced by `withSessionCleanup`
(`DIST/application/DirectAnalysisCleanup.js:9-24`; used at `DirectAnalysis.js:94-96`, `:221-232`).

- **T0** allocate root + snapshot target + allocate endpoint (`GhidraClient.js:395-425`).
- **T1** `mkdir` layout, write `session.json`, spawn owned POSIX process group, write `ownership.json`
  (`GhidraLauncher.js:90`, `:95`, `:150-193`, `:195`). Launch is a direct JVM exec of
  `analyzeHeadless`-equivalent arguments (`GhidraLauncher.js:329-438`): `-import`, `-readOnly`,
  `-deleteProject`, `-log`, `-scriptlog`, `-scriptPath`, optional `-preScript`s, then
  `-postScript ReaGhidraNoReturnFix.java`, `-postScript .../ReaGhidraBridge.java <session.json>`
  (`:423`, `:429`, `:433`).
- **T2** JVM opens `ghidra.log` / `script.log` (log4j file appenders). First two observed lines are
  `Using log config file: …generic.log4j.xml` and `Using log file: /tmp/rea-ghidra-XXXXXX/ghidra.log`
  (`P/shfmt-log/ghidra.log:1-2`, `P/esbuild-0.25.12-log/ghidra.log:1-2`). [obs]
- **T3** import + auto-analysis. Go analyzer lines are written here, between
  `ANALYZING all memory and code` and `REPORT: Analysis succeeded for file` (`HeadlessAnalyzer.java:1044`,
  `:1054`/`:1077`). Observed: `P/shfmt-log/ghidra.log:82-89` (go1.27.0 → `Untested Go version`,
  `Missing Go bootstrap type info`), `P/esbuild-0.25.12-log/ghidra.log:62-85` (1.23.12 snapshot, 61
  NoReturn, 2248+2055 signature fixes, 6264 strings, 19 missing type names). [obs]
- **T4** postScripts run **after** analysis (`HeadlessAnalyzer.java:1087-1093`). The bridge deletes
  `session.json`, binds `bridge.sock`, then serves (`ReaGhidraBridge.java:191-197`, `:261-267`).
- **T5** client polls for the endpoint every 50 ms (`DIST/ghidra/GhidraSocketConnection.js:16-48`),
  connects, `ping` handshake (`GhidraClientStartup.js:4-25`). **The socket cannot exist before T4, so a
  successful `open` proves auto-analysis already finished** — the entire analysis-phase log is written
  before the CLI can issue its first request.
- **T6** operation(s) (`binary_overview` for `analyze`, `cli/coreBinaryCommands.js:47-88`).
- **T7** close begins immediately after the operation returns (`DirectAnalysisCleanup.js:20-35`); the CLI
  JSON is emitted only *after* this returns, so **by the time `npx rea analyze` exits the directory is
  already gone**.
- **T8** graceful `shutdown` request, 10 s timeout (`GhidraClient.js:569-584`, `SHUTDOWN_TIMEOUT_MS`
  `:31`); bridge replies `{shutdown:true, project_ephemeral:true}` and returns
  (`ReaGhidraBridge.java:393-399`).
- **T9** `analyzeHeadless` continues: because `-postScript` was used and analysis is enabled (default
  `analyze = true`, `HeadlessOptions.java:137-139`), it immediately runs a **second full analysis pass**:
  `ANALYZING changes made by post scripts` … `REPORT: Post-analysis succeeded for file`
  (`HeadlessAnalyzer.java:1121-1130`). This is *after* the client already got the shutdown ACK.
- **T10** client waits only **500 ms** for the JVM to exit (`GhidraClient.js:591`), then calls
  `stop()` (`:593`). Cleanup for a spawned provider is token-verified group **SIGKILL**
  (`ProviderProcess.js:262-286` → `ProcessOwnership.js:52-97`), then up to 1000 ms exit wait
  (`ProviderProcess.js:4-5`, `:270`); one retry then up to another 1000 ms (`:277-286`).
- **T11** `#lastDiagnostics` snapshot, close snapshot owners, then remove roots
  (`GhidraClient.js:606-616`, `:638-668`) → `rm(root, {recursive:true, force:true})`
  (`PrivateRuntimeRoot.js:49`). If `stop()` reports `incomplete`, cleanup **throws and keeps the files**
  for a later close (`GhidraClient.js:596-604`), reporting `ProviderCleanupError` with `leftover_paths`.
- **T12** CLI prints JSON / exits.

Two kill paths:

- graceful: T8 ACK then T10/T11 as above (normal `close_binary` / command end).
- forced: `forceStop=true` skips the `shutdown` request entirely (`GhidraClient.js:569`) and goes
  straight to kill + rm. It is taken when an **active** bridge request is aborted
  (`GhidraRequestQueue.js:72` `onActiveCancellation` → `GhidraClient.js:335-341` `#stopAfterActiveCancellation`
  → `#requestClose(true)`), e.g. SIGINT/SIGTERM forwarded through `cli/commandCancellation.js:6-16`
  (exit 130/143), or an aborted/timed-out startup (`#startupFailure` → `#cleanup()`).

## 4. Cleanup order, verbatim

`GhidraClient.js:563-624`:

1. `:567` `#requestQueue.failQueued(...)`
2. `:568-584` if not forced and socket live → `shutdown` request (10 s cap); non-ack only logs a warning
3. `:585` `#failAll(...)` (fail in-flight)
4. `:586-590` detach + destroy socket, `#socket = undefined`
5. `:591` `waitForExit(500)`
6. `:592-594` `snapshot()`, `stop()` (SIGKILL group, ≤2×1000 ms)
7. `:596-604` `status === "incomplete"` → emit `cleanup-incomplete`, `throw` (root retained)
8. `:606-608` `#lastDiagnostics = #diagnostics()`; clear `#process`, `#launch`
9. `:609-612` close every `#snapshotOwners` handle
10. `:614-620` `#removeRuntimeRoots()` → `runtimeRoot.close()` then `socketRoot.close()` (`:638-668`);
    a failed root is kept and rethrown as `ProviderCleanupError`
11. `:622-627` clear `#snapshotPath`, `#endpointPath`, `#token`, `#runId`, reset buffer

There is **no per-file ordering**: `ghidra.log` disappears in the same single `rm -rf` as everything else.

## 5. When is the log last written vs deleted

**Write side.** `ghidra.log` is a log4j2 `RollingFile` (`detail` appender, `G2 …/Generic.jar!/generic.log4j.xml`
+ `log4j-appender-rolling-file.xml`). The XML does not disable `immediateFlush`, so it keeps log4j2's
default `immediateFlush=true`: each event is flushed on publish. A fresh `analyzeHeadless` process always
enables log4j (`AnalyzeHeadless.java:184` `getLoggableInstance(logFile, scriptLogFile, true)`, reached
because `Application.isInitialized()` is false at `:180-184`), so the `HeadlessErrorLogger`/`PrintWriter`
path (`HeadlessErrorLogger.java:45`) is unused in REA runs. Consequence:
a copied file never contains bytes that the JVM had not yet flushed; and a SIGKILL cannot un-write earlier
lines.

Writes continue **past** the client's last bridge response: T9's second analysis pass logs
`ANALYZING changes made by post scripts` and later `REPORT: Post-analysis succeeded` on the same file.

**Delete side.** Deletion happens at T11, immediately after the group SIGKILL/exit is verified
(`GhidraClient.js:591-616`, `PrivateRuntimeRoot.js:49`). Nothing sleeps between exit verification and
`rm`; there is no "quiescent but still present" phase.

**Therefore:** the last *possible* write is the JVM's last flush before it is killed or exits; the delete
follows within the same cleanup call. The boundary is not "log last written vs deleted" separated in time —
it is "the log is still being appended at the moment the deleting code path is already running."

**Deterministic tail loss (code, not polling).** Because REA waits only 500 ms (`GhidraClient.js:591`)
after the ACK while Ghidra has just started a full second analysis pass (`HeadlessAnalyzer.java:1121-1130`),
that pass is normally aborted by SIGKILL. `REPORT: Post-analysis succeeded for file` can therefore be
**absent by construction**, independent of the copier. A retained log that lacks it is not evidence that
the copier fell behind.

## 6. Bounding the polling-copy gap

Let `P` = poll period, `t_ack` = client receipt of the shutdown ACK, `t_c` = last successful copy.

- Lines can only be missed from the interval `(t_c, t_kill]`, where
  `t_kill ≤ t_ack + 500 ms` when the JVM is still alive at `t_ack+500 ms`, or `t_kill = t_exit ≤ t_ack + 500 ms`
  when it exits naturally first. So the *time span* of potentially missed content is
  **≤ P + 500 ms** (plus the client's own ACK processing latency, sub-millisecond on a unix socket).
- The classes of content in that span are exactly: the second-analysis-pass lines T9 emits. All analyzer
  diagnostics of interest (Go RTTI/snapshot/symbol/string lines) were written in T3, i.e. **before** the
  bridge existed and hence before any request could be answered (T5). A single copy at any time in
  `[T5, T11]` captures them completely. The observed pilot confirms this: every Go line in
  `P/shfmt-log/ghidra.log:82-89` and `P/esbuild-0.25.12-log/ghidra.log:62-85` is present. [obs]
- Path-level hazards, all bounded:
  - *ENOENT*: a copy that **opens** the file after T11's `rm` fails. A copy that already opened it still
    reads the full inode (POSIX unlink keeps the fd valid), so `rm` itself cannot truncate a copy in flight.
  - *Torn tail*: only from a read racing an in-flight `write(2)`; with per-record flush the window is one
    write syscall. Both pilot logs end on a complete record (`tail -c 120 | xxd`: `…bin  \n` /
    `…/ReaGhidraBridge.java  \n`), including the two trailing spaces of the layout. [obs] Still, a parser
    should tolerate an unterminated final line.
  - *Discovery*: the dir exists for the whole analysis (Ghidra's own totals: 24 s at
    `P/shfmt-log/ghidra.log:116`, 91 s at `P/esbuild-0.25.12-log/ghidra.log:115`; wall clock
    10:17:28→10:17:54 and 10:18:19→10:19:52 per the timestamped first/`Analysis succeeded` lines
    `:1-2`→`:119`/`:118`), so a 0.5–1 s directory listing cannot miss its existence. [obs]
- Ways to obtain the full tail are failure-only, not knobs:
  - `stop()` incomplete → root retained + `leftover_paths` in the error (`GhidraClient.js:596-604`,
    `:638-668`) — requires an unkillable process group.
  - Parent REA killed with SIGKILL → `#cleanup` never runs and no sweeper exists (§1.4), leaving
    `/tmp/rea-ghidra-*` behind. Not a supported contract; just the only way to get a *post-exit* copy.
  - No keep/debug environment variable exists: `DIST/config/environment.js:33-47` admits only
    `REA_GHIDRA_NATIVEAOT_JAR`, `REA_GHIDRA_STARTUP_TIMEOUT_MS`, `REA_GHIDRA_LANGUAGE_ID`,
    `REA_GHIDRA_COMPILER_SPEC_ID`, `REA_GHIDRA_DISABLED_ANALYZERS`, `REA_GHIDRA_SEED_FILE`. The pilot
    README's "no keep knob" claim is confirmed. [obs]

**Empirical calibration of the gap (same code path, two runs, P = 1 s):**

- `P/shfmt-log/ghidra.log:125` (last line) = `ANALYZING changes made by post scripts: …` @ 10:17:56 —
  the copy landed *after* the bridge returned and the second pass had started.
- `P/esbuild-0.25.12-log/ghidra.log:123` (last line) = `SCRIPT: …/ReaGhidraBridge.java` @ 10:19:53 —
  the copy landed *before* that same next line was written.
- Both are exactly the T8→T9 boundary; the two runs differ by one line. That is the polling gap measured
  in situ, and it sits one line inside a window the code bounds at ≈ `P + 500 ms`.

## 7. Divergences / risks for the r17 carrier-run contract

1. **Wrapper timeout vs REA's own deadline.** `carrier-run.py` allows 1800 s, but REA aborts the whole
   import+analysis+handshake at `DEFAULT_GHIDRA_STARTUP_TIMEOUT_MS = 330_000` ms
   (`DIST/config/providerStartupTimeout.js:4`, wired at `config/parseConfig.js:47`) and then cleans up
   (deletes the root) and reports `Ghidra startup deadline elapsed`
   (`GhidraClient.js:309-325`, `:711-716`; `GhidraClientStartup.js:26-31`). A slow carrier yields a deleted log and a
   REA-side failure long before 1800 s. The receipt should record which deadline fired.
2. **Never plan a post-exit copy.** T7/T12: the JSON is printed after cleanup, and by then the root is
   gone. The only in-run handle is the poll. The receipt field
   `log_capture_limit: "polling copy; lines written after the final poll before REA deletes its runtime
   root can be missing"` is accurate but incomplete — it should also state the *structural* absence of the
   post-script analysis tail (§5, `HeadlessAnalyzer.java:1121-1130` + 500 ms wait).
3. **Do not resolve a log path from a failure payload.** Diagnostics retain `ghidra_log_path` /
   `script_log_path` (`DIST/ghidra/GhidraDiagnostics.js:33-34`) *after* those files are deleted; a stale
   path in `details` is expected, not a bug.
4. **Copy both files; expect only `ghidra.log` to carry the payload.** `script.log` is regex-filtered to
   GhidraScript messages (`log4j-appender-rolling-file-scripts.xml`), confirmed by the single-line pilot
   files. The Go diagnostics upstream of C2 live only in `ghidra.log`.
5. **`session.json` is a bearer-token file.** 0600, and it is deleted by the bridge before serving
   (`ReaGhidraBridge.java:191-197`), so it is capturable only in the import/analysis window. Copying the
   whole directory (rather than the two logs) can capture it; never publish or hash-publish its contents.
   The contract's "copy `ghidra.log` and `script.log` only" is also the security-correct scope.
6. **Interrupt policy.** `timeout 900 npx …` sends SIGTERM → abort → `forceStop` kill *if a request is
   active* (`GhidraRequestQueue.js:72`), which skips the graceful shutdown; cleanup and deletion still run
   (`cli/commandCancellation.js:6-16` sets 143). `timeout -s KILL` bypasses cleanup entirely and leaks the
   dir (§6), which would then pollute the "new dirs" set of a later run — the contract's pre-existing-set
   diff already handles that, but the receipt should not treat a leaked dir as belonging to this run
   (match by run_id in `ownership.json` if needed).
7. **MCP runs behave differently.** The single-shot rule is CLI-only (`DirectAnalysis.js:26-30`); an MCP
   session retains the target until `close_binary` (bundled `mcp/*.js` close paths). Out of scope for C2,
   noted so a future `MCP` mode is not assumed to delete on command exit.

## 8. Confidence and residual unknowns

- High confidence (direct code statements, mutually consistent across dist, bridge Java, and Ghidra 12.1.4
  sources): root creation, file inventory and lifetimes, cleanup order 1–11, SIGKILL-not-SIGTERM for the
  REA-spawned group, the 500 ms post-ACK wait, the second analysis pass after postScripts, `rm -rf` of the
  root, and the absence of a keep/sweep mechanism.
- Medium confidence [inf]: that the second pass is *always* aborted. Code allows a natural exit within
  500 ms; on a trivial target it could complete and write `Post-analysis succeeded`. The r17 carriers
  (3 k procedures) make that implausible, but it is not proven for every carrier.
- Not observed: a live REA run in this seat (forbidden), an incomplete-cleanup retention, an MCP-mode
  session, and any post-SIGKILL partial-line write. `/tmp` currently holds **no** `rea-ghidra-*` residue
  after the pilot runs [obs, `ls /tmp` filtered], which is consistent with normal cleanup.
- Searched and found nothing else: an internal reader of `ghidra.log` (only path construction and
  diagnostics), a copy/rotation of the log by REA, a stale-root reaper, or an environment knob that keeps
  the session directory.

No tool installs or upgrades were needed or performed for this lane.
