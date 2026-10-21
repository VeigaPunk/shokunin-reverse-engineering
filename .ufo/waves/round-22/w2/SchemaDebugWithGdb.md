# SchemaDebugWithGdb — REA 6.5.0 `debug-with-gdb` schema authority review (round 22, W2)

Seat: `KaidokuR22R.SchemaDebugWithGdb-6`. This is an author-side schema/source review only, with no outside admission. No target was run or attached, no GDB inferior was started, and no `debug-with-gdb` invocation was executed. It does not claim to be a lost W1 seat returning.

## Verdict (TLDR)

1. **Counter-mapping blocker (high confidence, observed in source).** REA 6.5.0 `debug-with-gdb` returns Evidence with `operation: "gdb_console"`. The R22-C1 counter, both `tools/` and `frozen/`, binds through round-21 `bind()`, which requires `operation == verb.replace('-', '_')`, that is `"debug_with_gdb"`. A genuine, non-refused `debug-with-gdb` record therefore **can never bind**, so `debug-with-gdb` cannot count toward `t1_exercised_count` under the frozen counter. The reachable maximum for this verb is 0. L1 should treat this as a structural ceiling on R22-C1, not as an execution gap.
2. **Input contract.** `command` is required (string, minLength 1). `--inferior-tty` is **required** according to the schema (`required[1]: inferiorTty`), but `--help` and `--llms-full` present it as an ordinary option without marking it required. That is a documentation and calibration discrepancy.
3. **One-shot refusal set.** Before GDB is spawned, the handler refuses any command matching `gdbOneShotCommandMayInvalidateDetachProof`. The refusal is an `AnalysisInputError("gdb_console")` and would be a typed refusal envelope. Under the C1 falsifiers that envelope never counts.

## Commands run (exact argv, exit, stdout/stderr)

Working directory: `/tmp`. Package resolved by npx to `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`package.json` version `6.5.0`). A second npx cache, `a1722018f28f9df2`, holds 6.7.0 and was **not** used.

| argv | exit | stdout | stderr |
|---|---|---|---|
| `npx -y rea-agents@6.5.0 --version` | 0 | `6.5.0` | empty |
| `npx -y rea-agents@6.5.0 debug-with-gdb --help` | 0 | 988 bytes (below) | 0 bytes |
| `npx -y rea-agents@6.5.0 debug-with-gdb --schema` | 0 | 430 bytes, TOON (below) | 0 bytes |
| `npx -y rea-agents@6.5.0 debug-with-gdb --schema --format json` | 0 | JSON schema, same content | merged into stdout |
| `npx -y rea-agents@6.5.0 --llms-full` | 0 | manifest; `debug-with-gdb` section quoted below | merged into stdout |

Host prerequisite probes. These exercise GDB itself only, with no target or inferior:

| argv | exit | output |
|---|---|---|
| `command -v gdb` | 0 | `/usr/bin/gdb` |
| `gdb --version` (first line) | 0 | `GNU gdb (GDB) 18.1` |
| `gdb --nx --batch -ex 'show version'` (first line) | 0 | `GNU gdb (GDB) 18.1` |
| `uname -sr` | 0 | `Linux 7.2.11-arch1-1` |
| `echo ${REA_GDB_COMMAND-<unset>}` | 0 | `<unset>`, so REA would spawn `gdb` from PATH |
| `tty` (agent shell) | 1 | `not a tty`. This agent shell has no controlling TTY to offer as `--inferior-tty`. |

### `--help` stdout (verbatim)

```
rea debug-with-gdb — Run one unrestricted GDB console command in an ephemeral MI session; provide an inferior TTY so a live target can be safely detached

Usage: rea debug-with-gdb <command> [options]

Arguments:
  command  One unrestricted GDB console command.

Options:
  --inferior-tty <string>  Caller-selected durable TTY for output from a live GDB inferior.
```

(followed by the standard Global Options block: `--filter-output`, `--format`, `--full-output`, `--help`, `--llms`, `--schema`, `--token-count`, `--token-limit`, `--token-offset`).

### `--schema` stdout (verbatim)

```
args:
  type: object
  properties:
    command:
      type: string
      minLength: 1
      description: One unrestricted GDB console command.
  required[1]: command
  additionalProperties: false
options:
  type: object
  properties:
    inferiorTty:
      type: string
      minLength: 1
      description: Caller-selected durable TTY for output from a live GDB inferior.
  required[1]: inferiorTty
  additionalProperties: false
```

### `--llms-full` section

The table lists `--inferiorTty | string | (blank default) | Caller-selected durable TTY…`, and the manifest's Options table has no Required column. Only the schema reveals that the option is mandatory.

## Source authority (REA 6.5.0, read-only)

| File | sha256 |
|---|---|
| `dist/cli/reverseEngineeringCommands.js` (registration, lines 128–204) | `5bfe9d1ae4d10b0ff9239212175a026c31f21035847c961a79f1978f96e3023e` |
| `dist/cli-runtime/cli.js` (bundled copy, lines 40947–40996; logic identical) | `168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204` |
| `dist/gdb/GdbSessionManager.js` (provider) | `354898e88a81e23ab808fc87c727f88460bccb41a7a6ab870b8c0bf01b159b60` |
| `dist/domain/evidence.js` (record shape: `evidence_id` `ev_<64hex>`, `operation` string) | (not hashed) |

The `bin` entries `rea` and `rea-agents` both resolve to `scripts/rea.mjs`. Engines: node `^22.19.0 || ^24.11.0 || >=26.0.0`.

### Handler flow (observed)

1. A zod schema gives `command: string.min(1)` and `inferiorTty: string.min(1)`. The option is **not** `.optional()`, so it is required, which matches `--schema`.
2. `gdbOneShotCommandMayInvalidateDetachProof(command)` returns true, and the handler refuses with `AnalysisInputError("gdb_console", path ["command"], "invalid_value", "This command can invalidate the verified inferior output route; use the persistent GDB session workflow.")`. **No GDB process is spawned on this path.**
3. Otherwise it calls `GdbSessionManager.start({ inferiorTty })`, then `execute(sessionId, command)`, then `close(sessionId)`, then `closeAll()`. If cleanup fails, `process.exitCode = 1`.
4. On success it returns `executed.value.evidence`. On failure it returns `projectAnalysisError(...)`.

### Exact input and effect limits

These come from the constants in `GdbSessionManager.js`.

| Limit | Value | Where |
|---|---|---|
| Startup deadline (MI prompt) | 10,000 ms (`STARTUP_TIMEOUT_MS`) | l.12 |
| Per-command timeout | 120,000 ms (`COMMAND_TIMEOUT_MS`) | l.13 |
| Max command output | 16 MiB (`MAX_COMMAND_OUTPUT_BYTES`) | l.14 |
| Max command output records | 16,384 | l.15 |
| Max single MI line | 16 MiB. Exceeding it is a protocol failure. | l.16, l.851–852 |
| Recent-record budget | 64 KiB | l.17 |
| Diagnostic (stderr) capture | 64 KiB | l.18 |
| Max concurrent sessions | 8. Irrelevant for one-shot use, which runs one session. | l.19 |
| Max pending commands per session | 16 | l.20 |
| `inferior_tty` validation at start | non-empty and no NUL. **No existence or char-device check at start.** | l.222–230 |
| Platform | `linux` only. Others get `capability_unavailable`; win32 has a specific message. | l.233–236 |

One-shot refusal set (`gdbOneShotCommandMayInvalidateDetachProof`, l.1404–1416, plus `commandMayChangeInferiorOutput`, l.1418–1433). A command is refused if any of these holds:

- Its first token is a prefix of `source`, `define`, or `alias`, or equals `py`, or is a prefix of `python`.
- It contains `<`, `>`, `<<`, `>>`, `&>`, `;`, CR, or LF anywhere.
- It is `set` or `with` followed by a setting that is a prefix of `inferior-tty`.
- Its first token is a prefix of `tty`.
- It contains `inferior-tty` anywhere.
- It starts with `wit`/`with`, `tty`, `source`, `py…`, or `define`.
- It is `run`, `start`, or `starti` (or a prefix of one) followed by a redirection.

Effects:

- GDB is spawned as `<REA_GDB_COMMAND|gdb> --nx --quiet --interpreter=mi3`, falling back to `mi2` if mi3 startup fails (l.277–287). `--nx` suppresses gdbinit.
- After startup: `-gdb-set auto-load off`. If this is not `^done`, the result is `capability_unavailable` (l.383–386).
- `-inferior-tty-set <tty>`, then `-inferior-tty-show`. The reported `inferior_tty_terminal` must equal the caller's string exactly, otherwise `capability_unavailable` (l.387–401).
- The command runs as `-interpreter-exec console <quoted command>` (l.579). The command is **unrestricted**. The source's own limitation text says it "can access local shell, filesystem, network, and target controls" (l.618).
- On close, `-list-thread-groups --recurse 1` runs first. With zero groups, REA sends `-gdb-exit` (`target_state: "none_observed"`). With live groups and a verified TTY, REA **detaches the inferior, which may resume target execution**. With live groups and no verified TTY, close is refused with `invalid_input` (l.725–754). Before detaching, `verifyGdbInferiorOutputSink` requires the TTY's realpath to be a char device and the inferior's `/proc/<pid>/fd/1` and `fd/2` to point to it, with a stable `/proc/<pid>/stat` start time (l.146–171).

## Output operation binding (observed)

| Path | Evidence `operation` | `predicateType` |
|---|---|---|
| Successful console command | `gdb_console` | `rea.debugger.console-observation` (l.580–620) |
| Command timeout (partial) | `gdb_console`, via `GdbCommandTimeoutError.evidence` | console-observation |
| GDB exited mid-command | `gdb_console` | console-observation (l.640–655) |
| Startup failure partial observation | `start_gdb_session` | `rea.debugger.startup-observation` (l.470–495) |
| One-shot refusal / input errors | error envelope `gdb_console` / `start_gdb_session` / `close_gdb_session` | none (refusal) |

Provider identity is `{ id: "gnu.gdb", name: "GNU GDB", version: null }`. The provider version is **never recorded** in Evidence. Evidence `parameters` are `{ session_id: <randomUUID>, command }`. Because `evidence_id` is a digest over the normalized record (`evidence.js` l.238) and `session_id` is a fresh UUID for each run, **[INFERENCE]** two identical runs yield different `evidence_id`s, so a retained record cannot be reproduced byte-for-byte. `subject` is unavailable ("The active GDB inferior identity is not established by the debugger session identifier.").

**No `debug_with_gdb` operation string exists anywhere in REA 6.5.0 `dist/`.** A grep for `debug_with_gdb|debugWithGdb` matched only the `CLI_COMMANDS.debugWithGdb` key and name strings.

## Comparison to `claims.json` and the counter mapping

- `claims.json` R22-C1 lists `debug-with-gdb` in `t1`. Its `after_target` expects verbs counted only when bound, non-refused Evidence exists.
- The counting path: `frozen/count-c1.py` (sha256 `d7f67075ff17d7fbe2622924219cb804e3848df4a2b3f4371665dbd53e5c04aa`) calls `r21._measure`. `tools/count-c1.py` (sha256 `5fbc68684a1b6d8aa1a29fbd42e3074c9ca6674b69e83d061b0a49d5f947dd61`) adds a round-22 `SOURCES.md` S051+ eligibility filter and its own per-verb loop. **Both** call `r21.bind(blob, verb, evidence_id)` in `.ufo/waves/round-21/tools/verb-coverage.py` (sha256 `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b`).
- `bind()` line 85: `operation = 'inspect_with_objdump' if verb == 'list-objdump-architectures' else verb.replace('-', '_')`. For `debug-with-gdb` that gives `debug_with_gdb`, but the REA record carries `gdb_console`, so the result is always `evidence_unbound` (exit 1). The only alias in `bind()` is the objdump one, and it has no GDB entry.
- `tools/counter-fixtures.py` lists `debug-with-gdb` in T1 but adds no operation alias (grep observed).
- Separately, `bind()`'s `refused()` would not wrongly refuse a real `gdb_console` record. The record has no `exit_code` key (only `process_exit_code` on the exit path), and `completion_status` values `complete`/`unknown` are not in `REFUSALS`. So the alias gap is the **sole** binding obstacle.
- Consequence for calibration: an honest C1 report must give `debug-with-gdb` as `exercised: false` even if a valid GDB run is retained. Claiming it as counted would require changing the counter (`bind()` alias `debug-with-gdb → gdb_console`), which is a frozen-instrument edit and outside this seat. **[INFERENCE]** The same class of mismatch probably affects `debug-with-rizin`, which likely emits a `rizin_debug_command`-style operation. I did not verify this; it belongs to the `SchemaDebugWithRizin` seat.

## Required host and provider prerequisites for a real run (not performed)

1. Linux with `/proc`. Present: Linux 7.2.11.
2. GDB reachable as `REA_GDB_COMMAND` or `gdb` on PATH, accepting `--nx --quiet --interpreter=mi3` (or mi2), `-gdb-set auto-load off`, and `-inferior-tty-set`/`-inferior-tty-show` with an exact string echo. Present: `/usr/bin/gdb`, GDB 18.1. I did not probe MI behaviour, which would need a REA invocation.
3. A caller-selected `--inferior-tty` string. It is mandatory at the CLI even for commands that never create an inferior. **[INFERENCE]** For a no-inferior command such as `show version`, the path is only stored by GDB and not stat'd by REA, so it need not exist. The char-device and `/proc/<pid>/fd` checks run only when a live inferior must be detached on close. This agent shell reports `not a tty`.
4. Node satisfying engines (`^22.19.0 || ^24.11.0 || >=26.0.0`), and npx access to `rea-agents@6.5.0`, which was already cached.
5. The command must avoid the one-shot refusal set, so no `;`, redirections, `source`, `python`, `define`, `alias`, `tty`, `inferior-tty`, or `with`.

## Blockers and unknowns

- **Blocker for R22-C1 counting:** the operation alias gap (`gdb_console` vs `debug_with_gdb`). It is unfixable without modifying the frozen round-21 `bind()`.
- **Unknown:** the shape of the CLI error-envelope projection and its process exit code for the refusal path. I did not invoke it, because my scope was help and schema only. A bounded, no-spawn probe for L1 would be `npx -y rea-agents@6.5.0 debug-with-gdb 'source x' --inferior-tty /dev/null --format json`, which per source returns before GDB spawns.
- **Unknown:** whether `--help` validation rejects a missing `--inferior-tty` before `run()`. The incur zod schema says yes, but I did not observe it.
- **Unknown:** the actual MI3 support in GDB 18.1 under REA (`mi_version` returned). Not executed.

## Tooling

No installs or updates. `rea-agents@6.5.0` was already in the npx cache. No pacman, uv, or binary channel was used.
