# SchemaRizin — `debug-with-rizin` help/schema, alias, adjacent ownership

Role: read-only scout (leaf, no delegation, no background jobs). Question: read
`debug-with-rizin --help/--schema` only; report the exact `rizin_debug_command`
alias and adjacent ownership; **no run**. No debugger/Frida execution, no
process attach, no device access, no carrier execution was performed.

Repo revision at report time: `a3c92eb6bc70984e90ae5b895412de978840b2c5`
(`git rev-parse HEAD`). All wave-23 files are untracked; no production file was
touched.

## Findings

### Probe record (observation)

Package identity: `rea-agents@6.5.0`, npx cache root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`. The cached package matches the
already-retained R22 identity: `dist/cliCommandNames.js` SHA-256
`41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3`
(identical to `.ufo/waves/round-22/evidence/sources/cli-aliases.json`).
`package-lock.json` pins
`rea-agents-6.5.0.tgz` integrity
`sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`
(`package-lock.json:1589-1592`, SHA-256
`49ac77275f8ca32fc3da1f03387802a82bcb1cb2bb687546b39f31ea5cc2d2da`).

Environment overrides for every probe below:
`env -u REA_MCP_URL -u REA_RIZIN_COMMAND`. No `REA_RIZIN_COMMAND` was set in the
ambient environment; other `REA_*` variables present were
`REA_ADB_PATH`, `REA_APKTOOL_COMMAND`, `REA_BINWALK_COMMAND`,
`REA_JADX_MCP_JAR`, `REA_PWNTOOLS_PYTHON`, `REA_UNBLOB_COMMAND`,
`REA_WAKARU_COMMAND` (values not read/recorded). Working directory:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

P0 (identity only, not a behavioral probe):
`npx -y rea-agents@6.5.0 --version` → stdout `6.5.0`, exit 0.

P1 (observed, exit 0, no stderr):
`npx -y rea-agents@6.5.0 debug-with-rizin --help --format json --full-output`

```
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

P2 (observed, exit 0, no stderr):
`npx -y rea-agents@6.5.0 debug-with-rizin --schema --format json --full-output`

```json
{
  "args": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "minLength": 1,
        "description": "Path to the local artifact to debug."
      },
      "command": {
        "type": "string",
        "minLength": 1,
        "description": "One unrestricted Rizin debugger command."
      }
    },
    "required": [
      "path",
      "command"
    ],
    "additionalProperties": false
  },
  "options": {
    "type": "object",
    "properties": {
      "inferiorTty": {
        "type": "string",
        "minLength": 1,
        "description": "Caller-selected Linux TTY for inferior stdout and stderr."
      },
      "backend": {
        "description": "Optional Rizin IO debugger backend name.",
        "type": "string",
        "minLength": 1
      }
    },
    "required": [
      "inferiorTty"
    ],
    "additionalProperties": false
  }
}
```

Retained stdout digests (re-run with the same argv/env, piped to `sha256sum`;
producer exit 0 both times):

- P1 stdout: 1046 bytes, SHA-256
  `325bd83f37e4ac92937986c3d985b30d1ee2ad99c9aadc6ae52f5755a0435d81`.
- P2 stdout: 894 bytes, SHA-256
  `d1902d95671c558cac18b5b5e17eb242265568aaba373337cbcf60551423e73b`.

P1 and P2 were invoked with no target path and no command. No
`<path> <command>` invocation occurred, and no retained evidence was produced.
[INFERENCE] Help/schema rendering in the 6.5.0 CLI does not run the command
handler, so these probes cannot start a debugger or hold the T1 verb; that
handler-level non-execution was not separately instrumented.

### 1. Help vs schema: a required option is not marked required in help (observation)

- Help renders `--inferior-tty <string>` under `Options` with no required marker
  (P1).
- The schema makes `inferiorTty` required: `"required": ["inferiorTty"]` (P2).
- Source agrees with the schema: `inferiorTty: z.string().min(1)` with no
  `.optional()` (`dist/cli/reverseEngineeringCommands.js:216-219`), while
  `backend` is explicitly `.optional()` (`:220-223`).
- `path` and `command` are both required (`dist/cli/reverseEngineeringCommands.js:207-214`);
  `command` additionally rejects CR/LF via `.refine((value) => !/[\r\n]/u.test(value))`
  (`:211-213`).

Consequence [INFERENCE]: a caller following only the help text can omit
`--inferior-tty` and receive a CLI argument-validation failure before any
debugger start. The exact error projection was not observed (no run).

`--schema` emits the input contract only; it exposes no output schema (P2).

### 2. Exact alias (observation)

- Alias table: `"debug-with-rizin": ["rizin_debug_command"]`
  (`dist/cliCommandNames.js:178`). The table is introduced as
  “Canonical MCP operations reached by CLI commands with different names.”
  (`dist/cliCommandNames.js:161-162`).
- The CLI's evidence record uses the same operation string:
  `operation: "rizin_debug_command"` and predicate
  `rea.debugger.command-observation`
  (`dist/rizin/RizinDebugSessionManager.js:31-33`).
- The canonical MCP contract named `rizin_debug_command`
  (`dist/contracts/rizinDebugToolContracts.js:38`) takes
  `{ session_id: uuid, command: string }` and no `path`
  (`:43-48`); its `command` also rejects CR/LF (`:45-47`).
- The CLI command instead takes `{ path, command }` plus options
  `{ inferiorTty, backend? }` (`dist/cli/reverseEngineeringCommands.js:205-223`);
  it has no `--session-id` input; the manager mints a UUID per start
  (`dist/rizin/RizinDebugSessionManager.js:201`) and the CLI uses the returned
  id (`dist/cli/reverseEngineeringCommands.js:230-241`).

Observation: the alias is an **operation-name association only**, matching the
scope already recorded in R22 (`cli-aliases.json`: “operation-name association
only, not target execution or dynamic province ownership”).

[INFERENCE] The CLI schema must not be read as the MCP `rizin_debug_command`
schema. The two surfaces share the operation name but not the input contract:
CLI `path` is absent from the MCP tool; MCP `session_id` is absent from the CLI.

Cross-check with the inherited counter (observation, not run):
`count-c1.py` maps the T1 verb to the bound operation as
`"debug-with-rizin": "rizin-debug-command"`
(`.ufo/waves/round-22/tools/count-c1.py:34-35`); `bind()` converts the hyphen
form with `verb.replace('-', '_')` to `rizin_debug_command`
(`.ufo/waves/round-21/tools/verb-coverage.py:85`). That is consistent with the
source operation string above. The counter separately requires the original
envelope's `meta.command == "debug-with-rizin"` (`count-c1.py:79`). **The
`meta.command` value for a successful `debug-with-rizin` envelope was not
observed** because no run was allowed; it remains an untested counter
expectation, not a finding.

### 3. Adjacent ownership (observation + inference)

`debug-with-rizin` is an ephemeral CLI wrapper around the persistent-session
manager: it starts a session, executes exactly one command, then closes the
session in `finally` and calls `closeAll()` as fallback
(`dist/cli/reverseEngineeringCommands.js:226-263`). It is **dynamic debugger
execution**, not static analysis.

| Surface | CLI command | Canonical op | Ownership / boundary | Source |
|---|---|---|---|---|
| `debug-with-rizin` | yes | `rizin_debug_command` | one-shot: start → execute → close → closeAll; evidence operation is `rizin_debug_command` | `reverseEngineeringCommands.js:205,226-263`; `RizinDebugSessionManager.js:33` |
| `start_rizin_debug_session` | none (MCP-only) | `start_rizin_debug_session` | persistent process; `path`, required `inferior_tty`, optional `backend`; Linux only | `cliCommandNames.js:241`; `rizinDebugToolContracts.js:17-33`; `RizinDebugSessionManager.js:172-174` |
| `rizin_debug_session_status` | none (MCP-only) | `rizin_debug_session_status` | lifecycle/readback only; `session_id` | `cliCommandNames.js:242`; `rizinDebugToolContracts.js:61-81` |
| `close_rizin_debug_session` | none (MCP-only) | `close_rizin_debug_session` | verifies detach/absence; output `target_state: "unknown"` | `cliCommandNames.js:243`; `rizinDebugToolContracts.js:83-97`; `RizinDebugSessionManager.js:607-618` |
| `execute-rizin-command` | yes | `execute_rizin_command` | **static** one-shot `rizin -N -q -c <command> <path>`; no `-d`, no inferior TTY | `RizinCommand.js:9-15`; `reverseEngineeringCommands.js:114-127` |
| `cutter-command` | yes | `cutter_command` | live Cutter instance; network/session ownership separate | `cliCommandNames.js:173`; `toolEffects.js:24-33` |
| `debug-with-gdb` | yes | `gdb_console` | parallel ephemeral debugger family | `cliCommandNames.js:177`; `reverseEngineeringCommands.js:128` |

Count fencing: `execute-rizin-command` and `cutter-command` are separate
non-T1 surfaces and are not substitutes for the `debug-with-rizin` T1 verb.
`debug-with-gdb` is its own T1 verb (`claims.json` T1 list), so any evidence
from it must not be double-counted as `debug-with-rizin`.

Debug spawn arguments (observation), used by both the CLI wrapper and the
persistent MCP start:

```
-N -0 -d -R stdout=<resolved TTY> -R stderr=<resolved TTY>
-e dbg.exitkills=false [-D <backend>] <resolved path>
```

(`dist/rizin/RizinDebugSessionManager.js:208-218`). The manager later reads back
`e dbg.exitkills` and refuses detach unless it is `false`
(`dist/rizin/RizinDebugSessionManager.js:831-833`).

Binary selection and platform (observation):
`environment.REA_RIZIN_COMMAND ?? "rizin"` (`RizinDebugSessionManager.js:134`);
the static path uses the same override (`composition/reverseEngineering.js:13`).
The debug manager refuses non-Linux platforms because `/proc` descriptor
readback is required (`RizinDebugSessionManager.js:172`). No rizin version gate
was found in the debug path; provider identity is `{id: "rizin.debugger", name:
"Rizin debugger", version: null}` (`RizinDebugSessionManager.js:25-29`). Host
`rizin` exists at `/usr/bin/rizin`, version `0.8.2`, observed with `rizin -v`
(environment fact only; not executed by REA and not a target run). This does not
establish compatibility with this path.

Effect metadata (observation, `dist/contracts/toolEffects.js`):
- `start_rizin_debug_session`: mutates target/session, launches process,
  executes foreign code, not idempotent (`:53-59`).
- `rizin_debug_command`: mutates target/session, executes foreign code, writes
  filesystem, launches process, accesses network, changes UI state, may discard
  data, not idempotent (`:60-70`).
- `rizin_debug_session_status`: mutates session only (`:71`).
- `close_rizin_debug_session`: mutates session/target, launches process,
  executes foreign code (`:72-78`).
- `execute_rizin_command`: mutates target/session, writes filesystem, launches
  process, accesses network, may discard data, executes foreign code, not
  idempotent (`:85-94`).

### 4. Evidence binding limit (observation)

The command result carried by `rizin_debug_command` has only:
`command`, `output`, `output_scope: "command_and_interleaved_session_output"`,
`output_truncated`, optional `output_invalid_utf8`, `completion_status:
"complete"|"unknown"`, `backend` (`rizinDebugToolContracts.js:5-13`).
Evidence parameters are `session_id`, `command`, `inferior_tty`,
`launch_provenance` (`RizinDebugSessionManager.js:31-50`), where
`launch_provenance` holds only `caller_selected_path` and `resolved_path`
(`:203-206`). There is **no artifact SHA-256 and no target-content binding** in
this evidence; the record says so explicitly:

- limitation: “Launch provenance records the original and resolved startup
  paths; it does not establish the current target after unrestricted debugger
  commands.” (`RizinDebugSessionManager.js:30,50`)
- `subjectUnavailableReason`: “The current debugger target identity is not
  established by the Rizin session identifier.” (`:42`)

By contrast, the static `execute_rizin_command` observation schema carries
`artifact_sha256_after` and `artifact_changed`
(`dist/contracts/reverseEngineeringToolContracts.js:5-17`).

[INFERENCE] Even a future successful `debug-with-rizin` run would not, by
itself, supply the target SHA-256 that this wave's probe contract requires;
an outer wrapper or a separate `execute-rizin-command` observation would be
needed. That is 6.5.0 source behavior, not an observed run.

### 5. No-run / no-count boundary

- P1/P2 are help/schema reads with exit 0. They are not verb execution and
  cannot be used as held evidence for R23-C1.
- No `debug-with-rizin <path> <command>` invocation occurred; no TTY was
  selected; no device or remote connection was touched. No debugger child was
  observed by these probes [INFERENCE from help/schema rendering; not
  process-instrumented].
- This seat adds no counted verb. R23-C1's cumulative `k` is unchanged by this
  report; only L1's counter run establishes the exact numerator. Dynamic
  debugger ownership remains adjacent and unresolved, as declared in the wave
  context.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SchemaRizin.md`
  — self-hash is reported in the final hand-off message, not embedded here
  (embedding it would change the digest).
- No receipts or sandbox outputs were written; all observed stdout is embedded
  above. No production lane files were edited.

Source identity hashes used for the static citations (SHA-256):

```
4d8e5738f9078aa57e7e9c5c6fd21ffc247fd02aac3152a115931ad672999447  dist/contracts/rizinDebugToolContracts.js
d1a90a5557da356650b25f88b87ec43d89a3bfb7048c3c13659f1eacdde7ca68  dist/rizin/RizinDebugSessionManager.js
1b00da263871783dc5754385af2bc7ce71944f3c475e80bfca53cfd15ceada07  dist/rizin/RizinCommand.js
1d12ce7f0ab94c1f2e1caf3903008da318f5dbccb04d102bdc4e8efa3e2814f8  dist/contracts/toolEffects.js
5bfe9d1ae4d10b0ff9239212175a026c31f21035847c961a79f1978f96e3023e  dist/cli/reverseEngineeringCommands.js
41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3  dist/cliCommandNames.js
a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c  package.json
49ac77275f8ca32fc3da1f03387802a82bcb1cb2bb687546b39f31ea5cc2d2da  package-lock.json (npx cache root)
14d5619e384fa6c56e6efb7679faa384d1db19b4765031ac68cf895dd80cf972  package.json (npx cache root)
```

## Installs

None. `npx -y rea-agents@6.5.0` reused the existing npx cache
(`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`, package mtime 2026-10-16); no tool
was installed, upgraded, or configured. No `pacman`, `npm -g`, `uv`, or global
write was performed.

## Open risks / unknowns

1. **`meta.command` unobserved.** A successful CLI `debug-with-rizin` envelope
   was never produced. The inherited counter expects `meta.command ==
   "debug-with-rizin"` (`count-c1.py:79`) and evidence operation
   `rizin_debug_command`; only the latter is source-confirmed. If a future run
   emits a different envelope command key, the counter would reject it.
2. **No version gate found ≠ no version requirement.** The debug path has no
   observed check for the host Rizin version; host `rizin 0.8.2` was only
   version-printed, not exercised against this path. Backend/TTY/detach
   behavior remains untested.
3. **Required-option rendering mismatch.** Help does not mark
   `--inferior-tty` required while the schema and source do. Exact CLI
   argument-error shape/exit code was not observed.
4. **Alias overreading.** `debug-with-rizin` ↔ `rizin_debug_command` is a name
   association; MCP callers still need `session_id` from
   `start_rizin_debug_session`, which has no CLI command. Do not cite the CLI
   schema as the MCP tool schema.
5. **Evidence strength.** The 6.5.0 debugger evidence has no target hash and
   explicitly disclaims current-target identity after unrestricted commands.
   This is why this seat does not treat the verb as held and why dynamic
   ownership remains adjacent.
6. **Host observation provenance.** `/usr/bin/rizin 0.8.2` came from a direct
   `rizin -v` environment check, not from an REA probe and not from target
   execution; it is recorded only as environment context.
7. This report is author-side. It is not outside verification; no execution
   probe was attempted and no proposed work is called verified.
