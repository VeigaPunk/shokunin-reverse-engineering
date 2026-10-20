# Scout — REA Ghidra runtime root, `ghidra.log` lifecycle, and retention knobs

Scope: read-only inspection of `rea-agents@6.5.0` installed dist
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/` (referred to as `dist/`) plus the
installed Ghidra 12.1.4 sources. No REA analyze/search/decompile and no Ghidra run was performed.

**Verdict: CONFIRMED — "no knob retains ghidra.log".** The log is created inside the per-session
private runtime root and is destroyed with that root by `rm -rf` on every normal close. The only ways it
outlives the session are (a) abnormal termination that skips close, and (b) the fail-closed
incomplete-process path, which retains the root only until a later successful close. Neither is a knob.

## 1. Where `/tmp/rea-ghidra-*` is created (observed)

| Step | Anchor |
|---|---|
| Session parent chosen once at module load | `dist/ghidra/GhidraClient.js:32` — `const SESSION_ROOT = ghidraSessionRoot();` |
| Parent resolution, dot-element rule | `dist/ghidra/GhidraSessionRoot.js:28-46` — `resolve(options.base ?? tmpdir())`; if any path element starts with `.`, falls back to `/tmp` (posix) or the nearest dot-free ancestor. Doc comment: Ghidra's `NamingUtilities.checkName` aborts headless on dot-prefixed project-path elements, so an inherited `TMPDIR=~/.cache/...` would fail every operation. |
| Root allocated per start | `dist/ghidra/GhidraClient.js:395-398` inside `#startWithin` — `PrivateRuntimeRoot.create({ parent: SESSION_ROOT, prefix: "rea-ghidra-", platform })`; guarded by `#start` at `:377`. |
| POSIX allocation | `dist/process/PrivateRuntimeRoot.js:35-42` — `mkdtemp(join(parent, "rea-ghidra-"))` (owner-only mode from mkdtemp; no chmod afterwards). Windows uses `WindowsPrivateRuntime.create` in the same method. |
| Layout of the root | `dist/ghidra/GhidraLauncher.js:440-451` — `project/`, `home/`, `tmp/`, `cache/`, `config/`, `data/`, `session.json`, `ownership.json`, `ghidra.log`, `script.log`. |
| All child state pinned inside the root | `dist/ghidra/GhidraLauncher.js:518-534` sets `HOME`, `TMPDIR`, `XDG_CACHE_HOME`/`XDG_CONFIG_HOME`/`XDG_DATA_HOME` (and `TEMP`/`TMP`/`USERPROFILE`/`APPDATA` on win32); `:543` adds `-Duser.home=${homeRoot}` and `-Djava.io.tmpdir=${tempRoot}`. |
| Socket root is separate | `dist/ghidra/GhidraTransport.js:16` — prefix `rea-ghidra-socket-`. |

Observed on this host: `ls -d /tmp/rea-ghidra-*` → no entries (no session open at read time).

## 2. Where `ghidra.log` is configured (observed)

- `dist/ghidra/GhidraLauncher.js:449` — `ghidraLogPath: join(runtimeRoot, "ghidra.log")` (sibling
  `scriptLogPath` at `:450`).
- Injected into the headless argument list at `:119` and emitted as `-log <path>` at `:383`, next to
  `-readOnly` (`:380`), `-deleteProject` (`:381`), `-scriptlog` (`:384`), and the project locator
  `<projectRoot> rea-project` (`:328`).
- Upstream, in the installed Ghidra 12.1.4 `Ghidra/Features/Base/lib/Base-src.zip`:
  - `ghidra/app/util/headless/AnalyzeHeadless.java:53` `LOG("-log", true, "<path to log file>")`,
    `:58` `DELETE_PROJECT("-deleteProject", false)`, `:169` reads the next arg as `logFile`,
    `:184` `HeadlessAnalyzer.getLoggableInstance(logFile, scriptLogFile, true)`.
  - `ghidra/app/util/headless/HeadlessAnalyzer.java:103` `getLoggableInstance`, `:125-126`
    `configuration.setApplicationLogFile(logFile)`, `:134`
    `Msg.setErrorLogger(new HeadlessErrorLogger(logFile))` — so `ghidra.log` is the log4j application
    log and also receives `Msg` output.
- The path is never re-assigned elsewhere: `grep -rn "ghidraLogPath" dist --include=*.js` yields only
  `GhidraLauncher.js:119`, `GhidraLauncher.js:252` (recorded in the partial-launch descriptor) and
  `GhidraDiagnostics.js:33` (path string in diagnostics). Nothing ever reads the file back — the only
  `readFile` in the launcher is `application.properties` at `GhidraLauncher.js:463`.

## 3. Where and when it is deleted (observed)

Two independent deleters; only the second removes `ghidra.log`.

**(a) `-deleteProject` deletes the project only, not the log.**
`GhidraLauncher.js:381` passes the flag unconditionally alongside `-readOnly` (`:380`). Upstream,
`HeadlessAnalyzer.java:432-434` forces `options.deleteProject = true` for any read-only import, and the
`finally` at `:457-459` runs `FileUtilities.deleteDir(locator.getProjectDir())` plus
`locator.getMarkerFile().delete()`. That removes `<runtimeRoot>/project/rea-project*`; `ghidra.log`
lives at the runtime-root level (`GhidraLauncher.js:449`), is not referenced by that block, and is still
open when the project dir is removed.

**(b) The runtime-root `rm` is what removes `ghidra.log`.**
Chain:
`GhidraClient.close()` (`GhidraClient.js:282`, takes no arguments) → `#requestClose(false)` (`:327`) →
`#close` (`:549`) → `#cleanup(forceStop)` (`:563`) → `#removeRuntimeRoots()` (called `:614`, defined
`:638`) → `PrivateRuntimeRoot.close()` (`PrivateRuntimeRoot.js:45-47`) →
`rm(this.path, { recursive: true, force: true })` (`PrivateRuntimeRoot.js:49`) and then
`this.#runtimeRoot = undefined`.

Failure semantics:
- Incomplete JVM stop: `#cleanup` throws at `GhidraClient.js:595-603` **before** the `rm`, with the
  comment "Keep the supervisor and private files available for a later close" (`:601-602`). Root and log
  survive until a later `close()` succeeds — fail-closed retention, not an option.
- `rm` failure: leftovers are reported via `ProviderCleanupError` (`GhidraClient.js:664-670`,
  "it is retained for a later close") and the root handle is kept for retry (`:641-661`).

When the close is triggered:
- **MCP**: `close_binary`/target switch (provider adapter `close` at `GhidraProviderClient.js:608-611`
  → `client.close()`, called by `AnalysisClientCleanup.js:7`) and MCP shutdown
  (`dist/main/shutdown.js:17` `session.close({ retainProviderDocuments: true })` →
  `BinarySession.js:300-321` → `closeAnalysisClient`). `retainDocument` is a Hopper-only detach concept
  (`HopperCleanup.js:16,83`; `HopperClient.js:474`); `GhidraClient.close()` ignores arguments, so it
  cannot retain REA's root.
- **CLI one-shot** (`rea analyze` etc.): the command wrapper's `finish()` → `release()` closes provider
  resources before the process exits (`dist/cli-runtime/cli.js:512-533`), so the root is gone by the time
  the `npx rea-agents` process exits.
- **Startup failure**: `#startupFailure` (`GhidraClient.js:309-325`) and `#startupInterrupted`
  (`:707`) → `#cleanup` also remove it.
- **Signals**: shutdown handlers cover only `SIGINT`, `SIGTERM`, stdin `end`/`close`
  (`dist/main.js:24-28`). `SIGKILL`/crash leaves the directory on disk permanently. That is the only
  durable survival path.

## 4. Claim test: "no knob retains ghidra.log" — CONFIRMED

Exact commands run in `dist/` (all read-only):

```
$ grep -rEn -i "retainRuntime|keepRuntime|preserveRuntime|KEEP_TEMP|REA_TMP|REA_KEEP|REA_LOG_FILE|--log-file|--keep-|retainLog|preserveLog" --include=*.js . | grep -v "\.map"
(no output, exit 1)

$ grep -oE "REA_[A-Z0-9_]+" config/environment.js | sort -u
REA_ANALYSIS_PROVIDER
REA_GHIDRA_COMPILER_SPEC_ID
REA_GHIDRA_DISABLED_ANALYZERS
REA_GHIDRA_LANGUAGE_ID
REA_GHIDRA_NATIVEAOT_JAR
REA_GHIDRA_SEED_FILE
REA_GHIDRA_STARTUP_TIMEOUT_MS
REA_HOPPER_STARTUP_TIMEOUT_MS
REA_IDA_MCP_CONFIG
REA_ILSPY_CMD_PATH
REA_LOG_LEVEL
REA_MCP_INPUT_SCHEMA_PROFILE
REA_MCP_MAX_RESPONSE_BYTES
REA_MCP_OUTPUT_SCHEMA_PROFILE
REA_REFERENCE_SECRET_PATTERNS_JSON
REA_SWIFTC_COMPILE_TIMEOUT_MS

$ grep -rn "ghidra.log" --include=*.js .
./ghidra/GhidraLauncher.js:449
./cli-runtime/binary-BVOr2mgE.js:3949      (bundle copy)
./mcp/main-kBXHZ8S5.js:5775                (bundle copy)

$ grep -rn "rm(" --include=*.js process/ ghidra/
process/PrivateRuntimeRoot.js:49   rm(this.path, { recursive: true, force: true })
process/... (other providers' own roots)
ghidra/GhidraTargetSnapshot.js:52  rm(snapshotPath, { force: true })   (target snapshot file, not the log)
```

Corroborating surfaces (observed):
- Env schema `config/environment.js:25-61` contains no temp-dir, log-path or retention setting; the
  provider knobs are `GHIDRA_INSTALL_DIR`, `JAVA_HOME`, `REA_GHIDRA_*` (NativeAOT jar, startup timeout,
  language id, compiler spec id, disabled analyzers, seed file), `REA_HOPPER_*`, `REA_ILSPY_CMD_PATH`,
  `REA_LOG_LEVEL` (REA's own logger), `REA_REFERENCE_SECRET_PATTERNS_JSON`, `REA_MCP_*`.
- `rea --help` global options (tail of the list) expose only `--filter-output`, `--format`,
  `--full-output`, `--help`, `--llms(-full)`, `--mcp`, `--schema`, `--token-count`, `--token-limit`,
  `--token-offset`, `--update`, `--version` — no log/temp/keep flag. `rea inspect --help` shows only
  `--snapshot`, `--target-format`, `--architecture`, `--entry-point`, `--provider`.
- `rea --llms-full` has no mention of `ghidra.log`, `runtime_root`, or `rea-ghidra`.
- `open` is not a CLI command (`rea open --schema` → `code: COMMAND_NOT_FOUND`,
  `message: 'open' is not a command for 'rea'`, suggesting `open-jeb-project`); it exists only as the MCP
  `open_binary` tool, so there is no per-open CLI option surface either.
- The only environment input that changes *where* the root appears is `TMPDIR` (parent only, through
  `ghidraSessionRoot`), with a `/tmp` fallback; nothing changes *whether* it is removed.

Residual (explicitly not a knob): incomplete-process fail-closed retention until a later close
(`GhidraClient.js:601-603`), and crash/SIGKILL survival. Confidence: high for the POSIX lane; the
Windows `WindowsPrivateRuntime.close()` path was not inspected.

## 5. Calibration for `W/tools/carrier-run.py`

- The contract's caveat ("lines written after the final poll before REA deletes its runtime root can be
  missing") is correct and can be sharpened: deletion is synchronous in the REA process during
  command-end release (`cli.js:512-533`), **before** the `npx rea-agents` child exits. A poller keyed on
  `Popen.poll()` therefore has exactly the window in which the child is alive; a copy started after the
  child exits cannot succeed. Poll fast enough that the tail is small, and record the last copy time and
  byte size (already planned).
- The root exists before `ghidra.log` does: `createGhidraRuntimeDirectories`
  (`GhidraLauncher.js:482-509`) only creates the directories; the log appears when analyzeHeadless
  installs its appender. Polling must tolerate `ENOENT` for both `ghidra.log` and `script.log`.
- Each root holds two logs: `ghidra.log` (`-log`, `:382-383`) and `script.log` (`-scriptlog`, `:384`).
  The planned extraction of both is right; `ghidra.log` also carries `Msg` output
  (`HeadlessAnalyzer.java:134`).
- If the chosen provider is not Ghidra (e.g. Hopper/IDA), no `rea-ghidra-*` root ever appears; the tool
  should record zero new roots rather than poll until timeout.
- Since roots are always deleted at close, "retained" is only ever a copy-out artifact; the receipt's
  `log_capture_limit` wording is accurate and needs no knob.

## 6. Hygiene / remaining unknowns

- Wrote only this report. One scratch extraction of `HeadlessAnalyzer.java` to `/tmp/ha.java` was removed
  (verified absent). No REA analyze/search/decompile, no `analyzeHeadless`, no carrier execution.
  No tool installs or upgrades.
- Unknown: whether log4j flushes buffered lines between the last poll and JVM exit (poller may miss the
  tail — already acknowledged in the contract). Unknown: exact first-write moment of `script.log`.
  Not inspected: Windows runtime-root deletion parity.
