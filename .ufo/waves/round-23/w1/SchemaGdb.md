# SchemaGdb — REA 6.5.0 `debug-with-gdb` help/schema and exact `gdb_console` alias

Seat: `KaidokuR23.SchemaGdb` (scout, leaf, read-only). Round 23, W1. This is an author-side
schema/alias read, not outside verification and not an executed-verb claim. Boundary for this
seat: `--help`/`--schema` only; no `debug-with-gdb` command was run, no inferior TTY was
allocated, no GDB process or target was started, and no device/network target was touched.

Probe date: 2026-10-21. Host: Linux 7.2.11-arch1-1 x86_64. Node `v24.21.0`, npx `11.19.0`.
Working directory for every probe: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Env overrides: **none**; this seat set or changed no `REA_*` variable and used no config flag.
Two npx caches exist: `a1722018f28f9df2` holds `rea-agents` 6.7.0; `ad9a3fdbcad992c6` holds
6.5.0 (the only 6.5.0 cache). The version probe printed `6.5.0`, so the package contract below
is the 6.5.0 one. No target artifact exists for these probes; the subject is the installed
package, whose identity hashes are listed in §2/§7.

## Findings

### 1. Probes (observation)

All four probes exited 0 with empty stderr (0 bytes, sha256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). No output was paged,
filtered, or truncated. Exact argv as executed:

| # | argv (cwd `kaidoku-shokunin`) | exit | stdout bytes | stdout sha256 |
|---|---|---|---|---|
| 1 | `npx -y rea-agents@6.5.0 --version` | 0 | 6 | `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00` |
| 2 | `npx -y rea-agents@6.5.0 debug-with-gdb --help` | 0 | 988 | `c62067d16fe2015a03d493e60b277b8c039db65e256e7bc16327c836dfb22647` |
| 3 | `npx -y rea-agents@6.5.0 debug-with-gdb --schema` | 0 | 430 | `e91fc3f98698cec1dfc71141a3758b9fc78f9887fc4640726846cb7cbac8cd57` |
| 4 | `npx -y rea-agents@6.5.0 debug-with-gdb --schema --format json` | 0 | 603 | `da0dad42a59fd65aa65e4a583ea23a1f3fd0518d0dd165cf6392c15d2389cf12` |

Probe 1 stdout verbatim: `6.5.0\n`.

Probe 2 stdout verbatim (988 bytes):

```
rea debug-with-gdb — Run one unrestricted GDB console command in an ephemeral MI session; provide an inferior TTY so a live target can be safely detached

Usage: rea debug-with-gdb <command> [options]

Arguments:
  command  One unrestricted GDB console command.

Options:
  --inferior-tty <string>  Caller-selected durable TTY for output from a live GDB inferior.

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

Probe 3 stdout verbatim (default TOON, 430 bytes):

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

Probe 4 stdout verbatim (JSON, 603 bytes):

```json
{
  "args": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "minLength": 1,
        "description": "One unrestricted GDB console command."
      }
    },
    "required": [
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
        "description": "Caller-selected durable TTY for output from a live GDB inferior."
      }
    },
    "required": [
      "inferiorTty"
    ],
    "additionalProperties": false
  }
}
```

The help presents `--inferior-tty` as an ordinary option with no required marker; the schema
marks `inferiorTty` in `options.required`. That discrepancy is observed in the producer's own
bytes, not inferred. Both `args` and `options` set `additionalProperties: false`. No `globals`
block appeared in either schema rendering.

### 2. Exact alias and producer operation (observation)

Installed package root (source subject):
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.

| File | sha256 |
|---|---|
| `package.json` (name `rea-agents`, version `6.5.0`, engines `^22.19.0 \|\| ^24.11.0 \|\| >=26.0.0`, bin `rea`/`rea-agents` → `scripts/rea.mjs`) | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` |
| `dist/cliCommandNames.js` | `41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3` |
| `dist/cli/reverseEngineeringCommands.js` | `5bfe9d1ae4d10b0ff9239212175a026c31f21035847c961a79f1978f96e3023e` |
| `dist/gdb/GdbSessionManager.js` | `354898e88a81e23ab808fc87c727f88460bccb41a7a6ab870b8c0bf01b159b60` |
| `scripts/rea.mjs` | `526105418604cc6e5a202a6275b700814e27450bfaffd45e7510530ba669de8d` |
| `incur` 0.6.1 `dist/Cli.js` (CLI framework) | `325ea8e8ae28f7a3acc233eb4ac95527330a6fc6347515bcb61e59cc677c061a` |

- `dist/cliCommandNames.js:177` — `"debug-with-gdb": ["gdb_console"],` (line 178 is the
  contrasting `"debug-with-rizin": ["rizin_debug_command"],`). This is the exact CLI-command →
  tool-operation alias. It is `gdb_console` with an **underscore**, not `debug_with_gdb`.
- No second CLI alias is declared for it: `CLI_COMMAND_ALIASES` (line 160) is
  `Object.freeze(["compare-bundles"])`. The three persistent GDB session tools
  (`start_gdb_session`, `gdb_session_status`, `close_gdb_session`) are listed in
  `MCP_TOOLS_WITHOUT_DEDICATED_CLI` (lines 238–240), not as one-shot CLI commands; the
  one-shot CLI verb's only tool mapping is `gdb_console`.
- `dist/cli/reverseEngineeringCommands.js:128` — `cli.command(CLI_COMMANDS.debugWithGdb, …)`.
  `args.command: z.string().min(1)`, `options.inferiorTty: z.string().min(1)` (lines 130–140),
  matching the schema. The pre-spawn refusal at lines 143–151 constructs
  `AnalysisInputError("gdb_console", …)`; the success path returns the provider evidence.
- `dist/gdb/GdbSessionManager.js:582` — successful one-shot console evidence is
  `operation: "gdb_console"` with `predicateType: "rea.debugger.console-observation"` (line
  581). Timeout/exit paths at lines 642 and 1010/1283 use the same operation string.
- `grep -rq "debug_with_gdb" dist scripts` → **no match** (`ABSENT`). No operation string
  `debug_with_gdb` exists in the installed package.

Therefore the exact producer contract is: CLI verb `debug-with-gdb` → operation
`gdb_console`. Any counter that derives the operation as `verb.replace("-", "_")` obtains
`debug_with_gdb` and will not bind a genuine record. This reproduces the round-22 S056
observation (same `cliCommandNames.js` sha256), independently re-read here.

### 3. No-execution boundary (observation + inference)

Observed: probes 2–4 produced only static CLI introspection text, exit 0, empty stderr; no
GDB banner, MI record, session id, evidence id, or target text appeared. Probes 2–4 used no
`command` positional and no `--inferior-tty`, so they cannot enter a session.

Source-observed short-circuit: the CLI framework handles help and schema before command
dispatch. In `incur/dist/Cli.js`, `if (help)` starts at line 877 and returns at 947;
`if (schema)` starts at 950 and returns at 996; command execution follows after the schema
block. Consequently `--help`/`--schema` do not call the `debugWithGdb` `run` handler and
cannot spawn GDB. [INFERENCE] No debugger process was started by these probes; this rests on
the source path plus the static output, not on a process monitor.

Execution boundary that was **not** crossed, recorded for what the verb would mean:

- A real one-shot invocation requires `inferiorTty` per schema, then starts GDB as
  `<REA_GDB_COMMAND|gdb> --nx --quiet --interpreter=mi3` (mi2 fallback)
  (`GdbSessionManager.js:287`); startup sends no target-execution commands, so no inferior
  exists until `execute()` (comment at lines 324–326).
- The handler first rejects commands matching `gdbOneShotCommandMayInvalidateDetachProof`
  (`GdbSessionManager.js:1404–1418`): `source`/`define`/`alias`/`python` prefixes, any
  `<`/`>`/`&>`/`;`/CR/LF, `tty` or `inferior-tty` settings, and `run`/`start`/`starti` with
  redirection. This refusal happens before a manager is created.
- On close, zero thread groups → `-gdb-exit`; live thread groups with a verified durable TTY
  → detach, which may resume target execution; live groups without a verified TTY → refusal
  (`GdbSessionManager.js:735–756`).

This seat did none of that. Dynamic debugger ownership remains adjacent and unresolved, as
the round-23 claim boundary requires.

### 4. Relation to R23-C1 (inference; no count asserted)

This report is schema/alias authority only. It produced no executed `gdb_console` evidence
envelope and must not be counted toward `k/6`; it is not a held-verb witness, and a mere
schema/help mention cannot satisfy R23-C1. Its counting relevance is the identifier: a future
genuine non-refused one-shot record carries `operation: "gdb_console"`.

Whether the round-23 counter aliases that identifier explicitly is **unknown** here:
`.ufo/waves/round-23/tools/count-c1.py` did not exist when probed — `tools/` contained only
`setup-sigrok.py` and `sigrok-cli.sh`. If round-23 reuses the round-21/22
`verb.replace("-", "_")` binding, `debug-with-gdb` remains structurally uncountable at 0
regardless of execution. That is an inference about the counter, not an observation of the
round-23 instrument. Exact `k` and the incomplete count belong to L1.

### 5. Observation / inference / unknown

Observed:
- Exact help/schema bytes and exits in §1; alias at `cliCommandNames.js:177`; producer
  operation `gdb_console`; required `inferiorTty` only in schema; help/schema return before
  dispatch; no `debug_with_gdb` operation string in the package.
- The round-22 W2 `SchemaDebugWithGdb.md` report recorded the same help/schema byte counts
  (988 and 430) and the same body text in its excerpt; it did not record hashes, so the hashes
  in §1 are new receipts here and equality is by length/text excerpt, not a stored digest.

Inference:
- The help/schema probes started no GDB process (source short-circuit + static output; no
  process monitor).
- A counter using hyphen→underscore cannot bind `gdb_console`; its ceiling for this verb is 0
  unless it adds the explicit alias.

Unknown:
- CLI error-envelope shape/exit code for a refused command or a missing `--inferior-tty`
  (not run; this seat was help/schema only).
- MI3 acceptance, timeout/partial-observation behavior, detach behavior, and any real
  `gdb_console` evidence on this host (not run).
- Round-23 counter alias policy (file absent at probe time).
- Why the schema renderings omit a `globals` block (not investigated; no claim depends on it).
- Whether other bundled copies of `CLI_COMMAND_TOOL_ALIASES` disagree (only the canonical
  `dist/cliCommandNames.js` table was read; grep showed copies exist in
  `dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js:934` and
  `dist/mcp/serverIdentity-Cio4iFV3.js:571` but they were not opened or hashed).

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SchemaGdb.md` —
  sha256 `bd07083fc95735ab75e000b7df73d7f3edb8d45e9c6df5cf9b7444fb53c50441` (see note below
  for the digest scope).
  Digest scope: the hash is computed over this file exactly as written here, with the 64 hex
  characters on the preceding line replaced by 64 `0` characters. Inserting the digest changes
  the raw file hash by construction, so a verifier must apply that same normalization; the
  retained probe receipts' raw digests are in §1 and §2.
- No other file was written. A `/tmp` scratch probe JSON was created during data capture and
  removed; no sandbox clone, no evidence file, and no production lane file was touched. `npx`
  used the pre-existing 6.5.0 cache.

## Installs

None. No pacman, uv, cargo, npm-global, or release-binary install/update; no config edits.
`npx -y rea-agents@6.5.0` resolved the pre-existing cache (6.5.0), and the version probe
confirmed it.

## Open risks

- **Alias binding gap.** `gdb_console` ≠ `debug_with_gdb`. Unless the round-23 counter carries
  the S056 alias explicitly, genuine execution cannot be counted for this verb. Do not report
  the verb held on the strength of this report.
- **Help vs schema calibration.** Help shows `--inferior-tty` as optional-looking, while the
  schema requires `inferiorTty`. A caller following help alone will fail argument validation.
- **Cache identity drift.** The source anchors are an npx cache directory. If L1 re-probes
  after a cache refresh, re-check `package.json` version 6.5.0 and the file hashes in §2
  before reusing these claims.
- **No runtime evidence.** Nothing here shows MI3 startup, command execution, timeout, or
  detach behavior; those remain unobserved and cannot be inferred from help/schema.
- **Author-side only.** Single-seat observation, no independent verifier; the report does not
  authenticate the producer or grant dynamic-analysis ownership.
