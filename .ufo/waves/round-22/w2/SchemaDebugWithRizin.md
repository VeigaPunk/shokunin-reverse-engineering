# SchemaDebugWithRizin — REA 6.5.0 `debug-with-rizin` schema authority review (round 22, wave 2)

Seat: `KaidokuR22R.SchemaDebugWithRizin-6`. Author-side evidence only; not outside admission.
Scope: `--help` / `--schema` of `debug-with-rizin` plus static reading of the installed REA 6.5.0 dist.
**Target never run.** No `debug-with-rizin <path> <command>` invocation, no rizin `-d` launch, no debugger attach, and no install.
Lane HEAD at review: `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`; claims baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`.

## Bottom line

1. **[OBSERVED] Counter blocker for R22-C1.** REA emits Evidence for `debug-with-rizin` with `operation: "rizin_debug_command"`. The r21 `bind` that `count-c1.py` calls expects `verb.replace('-', '_')`, which is `debug_with_rizin`. That means even a genuinely executed, retained, non-refused `debug-with-rizin` record **cannot count** under the frozen or the working C1 counter. `debug-with-gdb` has the same defect, because REA emits `gdb_console` for it. The other four T1 verbs map one-to-one. Without a counter change, the C1 ceiling is **k ≤ 4/6**. This does not falsify C1, since its `after_target` only requires k ≥ 1 reported exactly, but it calibrates what C1 can claim.
2. **[OBSERVED] Running this verb is target execution.** The launch argv includes `rizin -d <path>`, which spawns the artifact as a debuggee. The tool's own effects declare `executesForeignCode`, `launchesProcess`, `accessesNetwork`, `writesFilesystem`, and `mutatesTarget`. Under this wave's contract ("No target execution/debug attach"), a qualifying C1 witness for `debug-with-rizin` cannot be produced in this wave at all.
3. **[OBSERVED] The help output under-states the input limits.** `--inferior-tty` appears under "Options" in `--help`, but `--schema` marks it **required**. The schema also omits a source-level refinement that rejects `\r` and `\n` in `command`.

## Commands and observed exits

| argv (cwd `/tmp`) | exit | stdout | stderr |
|---|---|---|---|
| `npx -y rea-agents@6.5.0 debug-with-rizin --help` (wrapped in bash `time`) | 0 | 1046 B, sha256 `325bd83f37e4ac92937986c3d985b30d1ee2ad99c9aadc6ae52f5755a0435d81` | only the bash `time` lines (`real 0m0.954s`) |
| `npx -y rea-agents@6.5.0 debug-with-rizin --schema` | 0 | 646 B, sha256 `07361c89ac32cbc9fe0038ff523c2c24b5fb28268ecdd540ed4efa96c605982d` | empty |
| `npx -y rea-agents@6.5.0 --version` | 0 | `6.5.0` | — |
| `command -v rizin` | 0 | `/usr/bin/rizin` | — |
| `rizin -v` (version query only, no target) | 0 | `Database must be a file` / `rizin 0.8.2 @ linux-x86-64` (verbatim) | — |
| `pacman -Q rizin` (read-only query) | 0 | `rizin 0.8.2-2` | — |
| `uname -sr` | 0 | `Linux 7.2.11-arch1-1` | — |
| `tty` (agent shell) | 1 | `not a tty` | — |
| synthetic `bind` probe (python3 -I -B, imports `.ufo/waves/round-21/tools/verb-coverage.py` read-only, in-memory strings, no lane writes) | 0 | see "Counter mapping" | — |

Package resolved by npx: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`package.json` version `6.5.0`). `REA_RIZIN_COMMAND` was unset in this agent's environment.

### `--help` stdout (verbatim)

```text
rea debug-with-rizin — Run one unrestricted Rizin debugger command in an ephemeral session

Usage: rea debug-with-rizin <path> <command> [options]

Arguments:
  path     Path to the local artifact to debug.
  command  One unrestricted Rizin debugger command.

Options:
  --inferior-tty <string>  Caller-selected Linux TTY for inferior stdout and stderr.
  --backend <string>       Optional Rizin IO debugger backend name.

Global Options:
  --filter-output <keys>              Filter output by key paths (e.g. foo,bar.baz,a[0,3])
  --format <toon|json|yaml|md|jsonl>  Output format
  --full-output                       Show full output envelope
  --help                              Show help
  --llms, --llms-full                 Print LLM-readable manifest
  --schema                            Show JSON Schema for command
  --token-count                       Print token count of output (instead of output)
  --token-limit <n>                   Limit output to n tokens
  --token-offset <n>                  Skip first n tokens of output
```

### `--schema` stdout (verbatim, TOON format)

```text
args:
  type: object
  properties:
    path:
      type: string
      minLength: 1
      description: Path to the local artifact to debug.
    command:
      type: string
      minLength: 1
      description: One unrestricted Rizin debugger command.
  required[2]: path,command
  additionalProperties: false
options:
  type: object
  properties:
    inferiorTty:
      type: string
      minLength: 1
      description: Caller-selected Linux TTY for inferior stdout and stderr.
    backend:
      description: Optional Rizin IO debugger backend name.
      type: string
      minLength: 1
  required[1]: inferiorTty
  additionalProperties: false
```

## Exact input limits (schema plus source)

All of these are **[OBSERVED]**, from the schema and from source at `dist/cli/reverseEngineeringCommands.js:205-266`, which is mirrored in `dist/cli-runtime/cli.js:40997+`.

- `path`: a string with `minLength` 1. Resolved with `resolve(input.path)` against the caller's cwd. Launch provenance records both the original `caller_selected_path` and the `resolved_path`.
- `command`: a string with `minLength` 1. A zod `.refine(v => !/[\r\n]/u.test(v))` rejects multi-line commands, so exactly one command line is allowed. This refine has **no message** in the CLI and is **not expressed in `--schema`**. The MCP twin (`rizin_debug_command`) carries the message "A single command line is required".
- `--inferior-tty` (`inferiorTty`): **required**, string with `minLength` 1. At start (`cli.js:40097-40115`), REA calls `realpath` on it, opens it `O_RDWR|O_NOCTTY|O_NONBLOCK`, and requires `isatty` to be true and the type to be `S_IFCHR`. If any of these fail, it returns `AnalysisInputError("start_rizin_debug_session")`. All of this happens **before** spawning Rizin.
- `--backend`: optional, string with `minLength` 1. It is passed as `-D <backend>`.
- `additionalProperties: false` applies to both `args` and `options`.

## Effects and runtime limits

All **[OBSERVED]** in `cli.js:39949-40250` and `dist/contracts/toolEffects.js:51-69`.

- **Launch argv:** `${REA_RIZIN_COMMAND ?? "rizin"} -N -0 -d -R stdout=<tty> -R stderr=<tty> -e dbg.exitkills=false [-D <backend>] <resolved_path>`. Here `-d` spawns the target under the debugger, which counts as target execution.
- **CLI lifecycle:** the CLI creates an ephemeral `RizinDebugSessionManager(environment)`, then runs `start`, then `execute(session_id, command)`, then `close`, then `closeAll`. If cleanup fails, it logs an error and sets `process.exitCode = 1` even when the command output was collected.
- **Declared effects of `rizin_debug_command`:** `mutatesTarget`, `mutatesSession`, `executesForeignCode`, `writesFilesystem`, `launchesProcess`, `accessesNetwork`, `changesUiState`, `mayDiscardData`, and `idempotent: false`.
- **Declared effects of `start_rizin_debug_session`:** `mutatesTarget`, `mutatesSession`, `launchesProcess`, `executesForeignCode`, and `idempotent: false`.
- **Limits:**

  | Constant | Value |
  |---|---|
  | `MAX_SESSIONS` | 8 |
  | `MAX_PENDING_COMMANDS` | 16 |
  | `FRAME_TIMEOUT_MS` | 120000 |
  | `STARTUP_TIMEOUT_MS` | 30000 |
  | `CLEANUP_COMMAND_TIMEOUT_MS` | 1000 |
  | `MAX_FRAME_BYTES` | 16 MiB |
  | `MAX_COMMAND_OUTPUT_BYTES` | 16 MiB |
  | `MAX_QUEUED_FRAME_BYTES` | 4 MiB |
  | `MAX_QUEUED_FRAMES` | 4096 |
  | `MAX_COMMAND_FRAMES` | 4096 |
  | `MAX_RECENT_FRAME_BYTES` | 16 KiB |
  | `MAX_DIAGNOSTIC_BYTES` | 64 KiB |
  | `MIN_QUEUED_FRAME_CHARGE_BYTES` | 64 |

- **Output result** (`dist/contracts/rizinDebugToolContracts.js`): a strict object `{command, output, output_scope: "command_and_interleaved_session_output", output_truncated, output_invalid_utf8?: true, completion_status: "complete"|"unknown", backend: string|null}`. If output exceeds the limits or times out, `output_truncated` becomes true, `completion_status` becomes `unknown`, and the session is stopped.
- **Close and detach verification** (`cli.js:40605-40660`): REA runs `olj`, parses the `ptrace://<pid>` rows, and requires exactly one inferior. It reads `/proc/<pid>/stat` to get the start time. It confirms that `e dbg.exitkills` reads back `false`, and that `/proc/<pid>/fd/{1,2}` match the TTY's device, inode, character-device type, and realpath. It then runs `o- <fd>`, re-checks `olj`, and confirms the start time is stable. A detached inferior **may keep running** and write to the TTY.

## Operation binding (the record a successful run would produce)

**[OBSERVED]** in `cli.js:39976-39993` (`createRizinCommandEvidence`):

- `operation: "rizin_debug_command"`
- `predicateType: "rea.debugger.command-observation"`
- provider identity `{id: "rizin.debugger", name: "Rizin debugger", version: null}`
- `parameters: {session_id, command, inferior_tty, launch_provenance}`
- `result` and `rawResult` both hold the commandResult object
- `subjectUnavailableReason: "The current debugger target identity is not established by the Rizin session identifier."`
- the limitations list includes `RIZIN_LAUNCH_PROVENANCE_LIMITATION`

CLI-to-operation map: `dist/cliCommandNames.js:178` `"debug-with-rizin": ["rizin_debug_command"]` (and `:177` `"debug-with-gdb": ["gdb_console"]`).

**[INFERENCE]** Because the subject is unavailable and the provider version is null, such a record would bind to a session, not to an artifact digest. If a witness were ever counted, it would show `pathless: true` in the r21 `bind` result, assuming `subject` serializes as null. This is untested here because no run was made.

## Counter mapping vs `claims.json`

`claims.json` R22-C1 lists `debug-with-rizin` in `t1`, with the move "hold … with executed, retained, bound REA Evidence". `count-c1.py` delegates to `.ufo/waves/round-21/tools/verb-coverage.py::bind`, line 85:

```python
operation = 'inspect_with_objdump' if verb == 'list-objdump-architectures' else verb.replace('-', '_')
```

Synthetic probe, with in-memory records `{"evidence_id": "ev_" + "a"*64, "operation": <op>}`. Output verbatim:

```text
rizin rizin_debug_command ({'finding': 'evidence_unbound', 'bound': False}, 1)
rizin debug_with_rizin ({'finding': 'evidence_bound', 'bound': True, 'pathless': False}, 0)
gdb gdb_console ({'finding': 'evidence_unbound', 'bound': False}, 1)
gdb debug_with_gdb ({'finding': 'evidence_bound', 'bound': True, 'pathless': False}, 0)
```

How each T1 verb's emitted operation compares with what `bind` expects (**[OBSERVED]** by grepping `dist/cli-runtime/cli.js`):

| T1 verb | REA emits | `bind` expects | countable? |
|---|---|---|---|
| identify-flutter-build | `identify_flutter_build` | same | yes |
| inspect-dart-aot | `inspect_dart_aot` | same | yes |
| inspect-signal-decoders | `inspect_signal_decoders` | same | yes |
| decode-signal-recording | `decode_signal_recording` | same | yes |
| debug-with-gdb | `gdb_console` | `debug_with_gdb` | **no** (structural) |
| debug-with-rizin | `rizin_debug_command` | `debug_with_rizin` | **no** (structural) |

Why the selftest stays green despite this: `tools/counter-fixtures.py:46-47` fabricates fixture records with `'operation': verb.replace('-', '_')`. That is an operation name REA never emits for these two verbs, so the fixture matches the counter's assumption instead of REA's real output.

Falsifier cross-check (**[INFERENCE]**): the only way to make `debug-with-rizin` count under the current counter is a record whose `operation` is `debug_with_rizin`. No REA 6.5.0 code path emits that. Such a record would be hand-authored, not "executed, retained, bound REA Evidence". If any round-22 C1 witness for `debug-with-rizin` or `debug-with-gdb` is counted, that witness is suspect by construction.

Counter integrity note (**[OBSERVED]**):

- `frozen/count-c1.py` (sha256 `d7f67075…aa`) and `tools/count-c1.py` (sha256 `5fbc6868…61`) differ. `tools/` adds the S051+ `source:` eligibility gate and `--selftest`.
- Neither file exists at baseline `7787fea`. Both were added in `75f04a4` ("freeze claims declaration and counters") and touched again in `2ee3d9f`.
- `claims.json` `counting_command` names `tools/count-c1.py`.
- Both versions share the same `bind` operation derivation, so the blocker applies to both.

## Required host and provider prerequisites (for a future, admitted run)

- Linux. Any other platform gets `AnalysisCapabilityUnavailableError`: "Persistent Rizin debugger sessions require Linux /proc descriptor readback…". **Host status: Linux 7.2.11. Met.**
- `/proc` readable for `/proc/<pid>/stat` and `/proc/<pid>/fd/{1,2}`. **Host: `/proc/self/fd` present.**
- A Rizin binary on PATH as `rizin`, or `REA_RIZIN_COMMAND`. **Host: `/usr/bin/rizin`, `rizin 0.8.2-2` (pacman), reports `rizin 0.8.2 @ linux-x86-64`.** REA does not pin a Rizin version, and the provider identity has `version: null`. Backend availability depends on the build ([INFERENCE], from the contract text "Backend and target capabilities depend on the installed build").
- A caller-owned **character-device TTY** to use as `--inferior-tty`, for example a dedicated `/dev/pts/N`. **This agent's shell has no TTY (`tty` returned "not a tty").** A future run would need a real pts allocated by the operator. `/dev/null` fails the `isatty` check.
- ptrace permission to debug the spawned child. [INFERENCE] This depends on the host `kernel.yama.ptrace_scope` setting; not inspected.
- Contract admission for target execution, which this wave forbids.

## Source paths

- `dist/cliCommandNames.js:58,178`: verb name and operation map.
- `dist/cli/reverseEngineeringCommands.js:205-266`: CLI args/options zod, newline refine, start/execute/close lifecycle.
- `dist/contracts/rizinDebugToolContracts.js`: MCP contracts for start/command/status, and the result schema.
- `dist/contracts/toolEffects.js:51-69`: effect declarations.
- `dist/cli-runtime/cli.js:39949-40250` (limits, Evidence factory, start/launch argv) and `:40605-40720` (detach and `/proc` verification).
- Lane: `.ufo/waves/round-21/tools/verb-coverage.py:77-101` (`bind`), `.ufo/waves/round-22/tools/count-c1.py`, `.ufo/waves/round-22/frozen/count-c1.py`, `.ufo/waves/round-22/tools/counter-fixtures.py:40-50`.

## Unknowns

- How Rizin 0.8.2 behaves under `-N -0 -d` for any specific artifact, and what the startup frame looks like. Not run.
- The exact CLI exit code when `projectAnalysisError` returns an error envelope. Not exercised.
- The host `ptrace_scope`. Not inspected.

## Blocker statement

No qualifying C1 witness for `debug-with-rizin` is reachable for two independent reasons:

- (a) The wave contract forbids target execution, and the verb always launches the target with `rizin -d`.
- (b) Even with an admitted run, the counter's `bind` would reject REA's genuine `rizin_debug_command` record.

To fix (b), L1 would need a verb-to-operation map in the counter, using `cliCommandNames.js` as the authority: `debug-with-rizin` → `rizin_debug_command` and `debug-with-gdb` → `gdb_console`. That would change a frozen counter after the claims were declared, which is L1's call, not this seat's.

## Installs

None. No tool was installed or updated.
