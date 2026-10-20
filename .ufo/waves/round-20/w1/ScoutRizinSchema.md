# ScoutRizinSchema — `execute-rizin-command` (rea-agents@6.5.0): schema, argv, deadline, caps, command rules

Read-only scout (leaf; no subagent dispatch). Wrote only this report. Clock at assembly
(`date -Iseconds` read immediately before writing): `2026-10-20T17:56:39-03:00`.
No tool installs or upgrades were performed; the npx cache already held the package.
`D` below = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (rea-agents@6.5.0, dir mtime Oct 16 12:49).
All `D/...` anchors are **observation** from reading the shipped bundle; all exit codes are **observation** from the pasted commands.

## 1. CLI surface as shipped (observed)

```
$ npx -y rea-agents@6.5.0 execute-rizin-command --schema ; echo EXIT=$?
args:
  type: object
  properties:
    path:
      type: string
      minLength: 1
      description: Path to the local artifact to analyze.
    command:
      type: string
      minLength: 1
      description: One caller-selected Rizin command.
  required[2]: path,command
  additionalProperties: false
EXIT=0
```

```
$ npx -y rea-agents@6.5.0 execute-rizin-command --llms-full ; echo EXIT=$?     # 10 lines, 0 stderr
# rea execute-rizin-command

Execute one Rizin command against a local artifact

## Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `string` | yes | Path to the local artifact to analyze. |
| `command` | `string` | yes | One caller-selected Rizin command. |
EXIT=0
```
The `--llms-full` manifest carries **no** timeout, cap, or capability text (10 lines total).

```
$ npx -y rea-agents@6.5.0 execute-rizin-command --help ; echo EXIT=$?
rea execute-rizin-command — Execute one Rizin command against a local artifact
Usage: rea execute-rizin-command <path> <command>
EXIT=0
```

Args are **positional**; global options are only `--filter-output --format --full-output
--help --llms --llms-full --schema --token-count --token-limit --token-offset` (observed in that
same help output). There is no `--timeout`, `--max-output`, or command-filter option.

```
$ npx -y rea-agents@6.5.0 execute-rizin-command --path /usr/bin/true --command iI ; echo EXIT=$?
code: UNKNOWN
message: "Unknown flag: --path"
EXIT=1
```

## 2. Implementation (observed, path:line)

- argv: `D/rizin/RizinCommand.js:8-14`
  `["-N", "-q", "-c", input.command, resolve(input.path)]` — exactly five argv elements, command
  passed as **one** element to `-c`, path `resolve()`d (absolute) as the last element.
- Input schema: `D/domain/reverseEngineering.js:23-30` — `z.object({path: string().min(1), command:
  string().min(1).refine(v => !/[\r\n\u0000]/u.test(v), "A single command line is required")}).strict()`.
  **No allow-list, deny-list, or command-class check.** The only content rule is "one line".
- Service entry: `D/application/reverse/ReverseEngineeringService.js:106-110` and the bundle copy
  `D/cli-runtime/cli.js:38012-38017` (`rizinInputSchema.safeParse` → `#observe(...)`).
- Executable selection: `D/composition/reverseEngineering.js:12-18` —
  `providerExecutable(environment.REA_RIZIN_COMMAND ?? "rizin", …)`; Windows-only rewrapping via
  `resolveWindowsProviderExecutable`. Environment snapshot `{...environment}` at
  `D/composition/reverseEngineering.js:29-31`; **rizin has no `environmentOverrides`** (objdump, by
  contrast, sets `DEBUGINFOD_URLS: ""` at :16).
- argv/env actually emitted are echoed into Evidence: `parameters.command_arguments` (observed below).
- Spawn: `D/cli-runtime/snapshotEnvironment-D_tWyOub.js:441-457` — `shell:false`, stdin `"ignore"`,
  stdout/stderr `"pipe"`, `detached: platform !== "win32"` (:449, own process group, `processGroupId =
  child.pid` :458-464), `cwd` inherited unless supplied (none supplied for this verb), child env =
  `{...hostEnvironment, ...options.env, REA_PROCESS_RUN_ID}` (:415-425).
- Limits: `D/cli-runtime/cli.js:37930-37932`
  `DEFAULT_TIMEOUT_MS = 12e4` (120000 ms), `MAX_COMBINED_OUTPUT_BYTES = 16*1024*1024`,
  `MAX_CONCURRENT_REVERSE_ENGINEERING_OPERATIONS = 8` (per CLI process only).
- Run call: `D/cli-runtime/cli.js:38076-38084` passes `timeout`, `stopSignal: "SIGTERM"`,
  `maxBuffer`; the installed runner `runOwnedCommandOutput` (`cli.js:38296-38310`) **ignores those
  three keys** and hardcodes `timeoutMs: DEFAULT_TIMEOUT_MS`, `diagnosticBytes:
  MAX_COMBINED_OUTPUT_BYTES`, `acceptNonZeroExit: true`. Dead parameters — inference from source,
  corroborated by the observed values matching the hardcoded pair (J and I below).
- Capture/truncation: `cli.js:38103-38114` (failure→capture), `:38163-38190` (classification,
  `exit_code = null` + `completion_status = "unknown"` when killed/unknown), buffer accounting
  `snapshotEnvironment:699` (`remaining = maxDiagnosticBytes − stdout.bytes − stderr.bytes`, i.e.
  **stdout and stderr share one budget**), truncation flag `:699-702`.
- Output-limit mapping: `D/cli-runtime/OwnedCommand-Cj9GhmPR.js:79,86` raise
  `OwnedCommandFailure("output-limit")`; `cli.js:38350` maps it to the sentinel
  `ERR_CHILD_PROCESS_STDIO_MAXBUFFER`; `D/cli-runtime/ExecFileOutput-BEQs-lDD.js:48-52` turns that
  into `outputTruncated: true`.
- Termination ladder: `snapshotEnvironment:403-404` `DEFAULT_TERMINATION_GRACE_MS = 250`,
  `DEFAULT_KILL_GRACE_MS = 1e3`; `:652-659` SIGTERM, wait 250 ms, SIGKILL, wait 1000 ms, else
  `incomplete`.
- Evidence limitations text for this verb: `cli.js:38224-38238`, rizin entry at **`:38229`**:
  "Rizin commands and retained plugins may read files or access network resources outside the
  selected artifact; those external inputs are not bound to Evidence."
- `REA_RIZIN_COMMAND` grep (5 files, 6 hits): `D/composition/reverseEngineering.js:13`,
  `D/cli-runtime/cli.js:38548` (inlined copy of the same composition), `D/rizin/RizinDebugSessionManager.js:134`
  and `D/cli-runtime/cli.js:40064` (the *persistent debug-session* manager, a different verb),
  `D/mcp/main-kBXHZ8S5.js:65387,67772` (bundle copies).
- MCP tool description (`D/cli-runtime/toolContracts-D2FOG_Nb.js:3424-3437`) is far more candid than
  the CLI manifest: 16 MiB shared combined limit, `output_truncated`/`completion_status` semantics,
  and "Rizin commands and retained plugins can execute foreign code, mutate files, access the
  network, and read files outside the selected artifact".
- MCP-only side effect (not CLI): `D/mcp/main-kBXHZ8S5.js:14738-14768` `withAdmittedExternalMutation`
  drains calls, runs the command, then retires/closes the active target; refuses when the active
  route is Ghidra (`:14753`). Registration path `:65417-65444`.

## 3. Runs (each command pasted; exit codes observed)

Harness: `npx -y rea-agents@6.5.0 execute-rizin-command --format json …` from `/tmp`.

| # | argv tail | CLI exit | raw_result (exit_code / signal / truncated / completion) | evidence_id |
|---|---|---|---|---|
| A | `/usr/bin/true iI` | 0 | 0 / null / false / complete | `ev_5970c44a…4238c7` |
| A2 | A re-run | 0 | identical stdout, **identical evidence_id** | `ev_5970c44a…4238c7` |
| B | `/usr/bin/true '!echo REA_RIZIN_SHELL_OK'` | 0 | 0 / null / false / complete | `ev_48b42d64…010cd8` |
| C | `/usr/bin/true $'iI\n?V'` | 1 | error envelope `invalid_request` | — |
| D | `/tmp/does-not-exist-kr20 iI` | 1 | error envelope `invalid_request` | — |
| E | `../../usr/bin/true '?V;?V'` | 0 | 0 / null / false / complete | `ev_c873bb29…51cf57` |
| G | `/usr/bin/true`, `!yes` piped into `head -c 17000000` | 0 | null / **SIGTERM** / false / **unknown** | `ev_1095835e…150337` |
| H | `/usr/bin/true`, `!yes` piped into `head -c 2000000` | 0 | null / SIGTERM / false / unknown | `ev_aa946079…1ee35e7d` |
| I | `/usr/bin/godot 'px 6000000'` (182 MB carrier) | 0 | null / null / **true** / **unknown** | `ev_96e992c3…dd39b35` |
| J | `/usr/bin/true '!sleep 130'` | 1 | error `provider_timeout`, partial obs. | `ev_57703195…3b22508a` |
| K | empty regular file `iI` (mktemp dir) | 0 | 0 / null / false / complete | `ev_d40ed996…bde5fc9` |

Details that matter:

- **A**: `parameters` = `{"path":"/usr/bin/true","command":"iI","provider_executable":"rizin",
  "command_arguments":["-N","-q","-c","iI","/usr/bin/true"]}`; `subject.digest.sha256 =
  8398af7d1f94a88be3303caa083616ad22a12783e4dfee0373298bc61aef0662`, equal to `sha256sum /usr/bin/true`
  (observed); `subject.format = "unknown"`, `architecture: null`, `provider.version: null`;
  `predicate_type = "rea.reverse-engineering.command-observation"`, `confidence: "observed"`,
  `authority: "shipped-artifact"`. stdout 586 chars (`iI` key/value table). Four limitations listed;
  a fifth signal limitation is added only when the provider process is signal-terminated (see G).
- **A/A2 determinism**: two runs produced the **same** `evidence_id` (`ev_5970c44a…`). Observation:
  the id is content-addressed/deterministic for identical inputs, safe to cite in corpus entries.
- **B**: stdout was exactly `"REA_RIZIN_SHELL_OK\n"`, exit 0. Observation: a caller-supplied command
  reaches a shell (`!`) and its output is captured as Evidence. The 38229 limitation string does not
  mention code execution; the MCP description does (toolContracts:3427).
- **C**: `$'iI\n?V'` → exit 1, `{"code":"invalid_request","category":"invalid_input",…}`. The refine
  at `domain/reverseEngineering.js:29` is the enforcement point.
- **D**: nonexistent path → exit 1 `invalid_request` **before spawn**: the digest at
  `cli.js:38373` (stat/hash; call site `:38046-38049`) fails first; EACCES/EPERM would instead be
  `AnalysisAccessDeniedError`, other stat errors `AnalysisInputError` (`cli.js:38050-38059`).
- **E**: `parameters.path` keeps the **raw** caller string `../../usr/bin/true` while
  `command_arguments[4]` is the resolved `/usr/bin/true` (observed). `?V;?V` produced rizin stderr
  `ERROR: core: Error while parsing command: `?V;?V``, **stdout empty, exit_code 0** → REA returned
  a "complete" observation. `;` is **not** a command separator for `-c` in rizin 0.8.2.
- **G/H**: `!yes | head -c N` never produced output; the child was terminated by SIGTERM and REA
  reported `completion_status: "unknown"` with **CLI exit 0** (empty stdout, empty stderr). Controls:
  `rizin -N -q -c '!seq 1 100' /usr/bin/true` → 292 bytes, status 0; `sh -c 'yes | head -c 100'` → 100
  bytes; `timeout 8 rizin -N -q -c '!yes | head -c 100' /usr/bin/true | wc -c` → 0 bytes, status 124
  (still running at the 8 s cap). Reading: rizin's `|` operator intercepts the pipeline, so `!`
  shell pipelines are unreliable. The ~30 s SIGTERM sender in the unwrapped direct run
  (`rizin … | wc -c` → 0 bytes, status **143** after 30.5 s) is **unresolved**; it is not REA's
  deadline, which is 120 s and was separately observed at 120 s (J).
- **I (cap)**: stdout **16,776,256** chars + stderr **960** chars = **16,777,216** = exactly 16 MiB;
  `output_truncated: true`, `exit_code: null`, `signal: null`, `completion_status: "unknown"`,
  limitation "The provider command ended before completion could be confirmed; captured output is
  partial." CLI exit 0. The 960 stderr bytes were rizin's own `bin_file_strings` warnings — stderr is
  charged to the same budget. Emitted JSON was **47,475,458 bytes** because `raw_result` and
  `normalized_result` each carry the full 16.7 MB stdout.
- **J (deadline)**: wall **2m1.2s** (120 s deadline + shutdown), CLI exit 1,
  `{"code":"provider_timeout","category":"timeout",…}`, `details.timeout_ms = 120000`,
  `details.captured_output = {stdout:"", stderr:"", truncated:false, exit_code:null, signal:"SIGKILL"}`,
  and `details.partial_observation` = a full Evidence record (`ev_57703195…`) whose limitations add
  "The provider process terminated by signal SIGKILL" and "…failed with AnalysisTimeoutError:
  Analysis operation timed out after 120000ms". SIGKILL despite the SIGTERM-first ladder is
  **inference** (rizin blocked in the shell wait; SIGTERM not honoured within 250 ms), not proven.
- **K**: a zero-byte regular file still returns rizin exit 0 / `complete`; stderr carried system-magic
  warnings. `-N` does not silence system (`/usr/share/rizin/magic`) loading.
- Non-zero rizin exit was **not** obtained (empty file, parse errors, and `q 5` all exited 0), so the
  "non-zero exit preserved as an observed command result" path is **source-only**: `acceptNonZeroExit:
  true` at `cli.js:38310` + `OwnedCommand:87-88`, then re-thrown as `OwnedOutputFailure`
  (`cli.js:38323`) and converted back to an ok-observation at `cli.js:38103-38114`. Unverified
  by observation.

## 4. Answers to the four questions

1. **argv**: `<REA_RIZIN_COMMAND|rizin> -N -q -c <command> <absolute-resolved-path>`, `shell:false`,
   stdin ignored, stdout/stderr piped, own process group, inherited cwd, full host env + `REA_PROCESS_RUN_ID`.
2. **Timeout**: 120000 ms, hardcoded (`cli.js:37930`, runner `:38308`); not settable from CLI or MCP.
   On expiry: CLI exit 1 / `provider_timeout` / `timeout_ms 120000` / SIGKILL / partial Evidence
   retained (`details.partial_observation`).
3. **Output caps**: 16,777,216 bytes **combined stdout+stderr**, hardcoded (`cli.js:37931`, `:38309`;
   accounting `snapshotEnvironment:699`). Overflow yields CLI exit 0 with `output_truncated:true`,
   `exit_code:null`, `completion_status:"unknown"` and a partial-output limitation — an overflow is
   **not** an error. No override.
4. **Allow/deny**: none. Only `string().min(1)` plus "no CR/LF/NUL" (`domain/reverseEngineering.js:23-30`).
   Observed consequences: `!` shell execution works; `;` does not chain (rizin parse error, exit 0);
   `|` is rizin's own operator and hangs shell pipelines; `resolve()` keeps a POSIX path from being
   parsed as a flag (inference).

## 5. Calibration notes for round-20 C2 evidence runs

- Cite `ev_` ids safely: identical inputs reproduce the identical id (A/A2). Do not cite
  `provider.version` — it is always `null`, so record `rizin 0.8.2 @ linux-x86-64` out-of-band
  (observed via `rizin -v`).
- Gate on `raw_result.output_truncated`, `completion_status`, and `exit_code` — CLI exit 0 covers
  complete, truncated, and hung/killed observations alike (I, G, H, K).
- A hung or killed rizin can look "ok" with empty stdout (G/H). Avoid `|` inside `!`; `!seq`/`!echo`
  are reliable (B, control). Budget 120 s per run and expect SIGKILL on deadline (J).
- Large stdout is duplicated into `raw_result` and `normalized_result` (47 MB JSON for a 16.7 MB
  capture); use `--filter-output`/`--token-limit` when retaining outputs.
- `parameters.path` is the raw caller string; the resolved path is only in `command_arguments` and
  `subject.local_path` (E). Pre-run and post-run digests bracket the call (`artifact_changed`).
- `-N` disables user rc/projects (`/usr/share/man/man1/rizin.1.gz:83-84`) but **not** plugins or
  system magic — `-NN` is the plugin/script kill switch (:85-86). The shipped tool description's
  "suppresses user settings and scripts while retaining plugins" wording is consistent with `-N`, not `-NN`.

## 6. Remaining unknowns

- Non-zero rizin exit preservation: unobserved (see §3 K).
- Sender of SIGTERM at ~30 s in the unwrapped `!yes | head` run: unidentified; not REA's deadline.
- Windows executable resolution (`resolveWindowsProviderExecutable`) untested.
- MCP session-retirement path (`mcp/main:14738`) read, not executed.

Raw captures of every run above (stdout JSON + stderr) were moved under a mkdtemp scratch dir:
`/tmp/kr20-rizinschema.xmVGlg/` (`kr20-rizin-{A,A2,B,C,D,E,G,H,I,J,K}.json`, `kr20-rizin-direct17.err`,
`kr20-rizin-llms-full.txt`). Not retained in the lane; re-run any row with the pasted argv to reproduce.
