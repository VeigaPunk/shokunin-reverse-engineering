# SentinelEnvLeak: round-17 w2 environment-leak attack on carrier-run.py and retained artifacts

Scope: `tools/carrier-run.py` as run (lane HEAD `da64646adcb19c1ede7537b799b8c7d283fe43da`, observed with `git rev-parse HEAD`), and all 131 files under `runs/` and `predictions/` (all tracked at da64646: `git ls-files … | wc -l` = 131). Paths are relative to `.ufo/waves/round-17/` unless absolute. Labels: [OBS] observed, [INF] inference. No secret value is printed anywhere in this report.

## Verdict

- **Artifact leak: none found (bounded no-finding, below).** No token, bearer string, API key, or credential-path string occurs in any retained run or prediction file.
- **Exposure: confirmed and broader than w1 stated.** The full L1 environment reaches npx, the REA node process, and the **Ghidra analysis JVM**. The Ghidra half contradicts an [OBS]-labelled w1 claim (F2).

## F1: Low. Full L1 env (OAuth tokens and ssh-agent) is handed to npx, REA, and the Ghidra JVM

- **Code** [OBS]: `tools/carrier-run.py:264-266` sets `child_env = dict(os.environ)` with only `TMPDIR` replaced. `:101-103` passes it as `env=child_env` to every `npx -y rea-agents@6.5.0 …` step (`:308`).
- **What the env holds** [OBS for this seat; INF for L1]:
  - Command: `env | cut -d= -f1 | grep -iE 'token|key|secret|pass|auth|cred|session|bearer|api|…'` (names only).
  - Secret-bearing names found: `OPENAI_CODEX_TOKEN` (1836 B), `XAI_OAUTH_TOKEN` (882 B), `SSH_AUTH_SOCK`, `DBUS_SESSION_BUS_ADDRESS`.
  - This seat and L1 are spawned by the same host process, so [INF] L1's env is the same set. I did not read L1's environ.
- **Where it flows** [OBS, static read of the cached `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` 6.5.0]:
  1. `dist/cli-runtime/cli.js:41787-41789`: `createCli(selectedEnvironment = process.env)` → `createDirectAnalysis(environment)`.
  2. `dist/composition/binary.js:15-18`: `createBinarySession(…, selectedEnvironment)` → `new GhidraProvider(config, logger, environment)`.
  3. `dist/ghidra/GhidraProvider.js:42,222`: `this.environment = snapshotEnvironment(environment)` → launcher `options.environment`.
  4. `dist/ghidra/GhidraLauncher.js:147,518-523`: `ghidraLaunchEnvironment(…, this.options.environment)` spreads `ghidraJavaEnvironment(…)`.
  5. `dist/ghidra/GhidraInstallation.js:290-298`: that function spreads `snapshotEnvironment(environment)`. On POSIX this is a full copy (`dist/process/snapshotEnvironment.js:2-4`: `Object.freeze({ ...environment })`).
  6. `dist/ghidra/GhidraJavaLaunch.js:79-80,109,130`: the JVM's environment again spreads that snapshot. REA's own comment: "The merged environment becomes the analysis JVM's environment".
  7. `GhidraLauncher.js:190-191`: `env: command.environment, hostEnvironment: {}`.
  - Result: only `HOME`, `TMPDIR`, `XDG_*`, `JAVA_HOME`/`PATH` and the `*JAVA_OPTIONS` variables are overridden. Both tokens and `SSH_AUTH_SOCK` reach the JVM that parses untrusted carrier bytes.
- **Exploit path** [INF]:
  - A parser bug in REA's node Go-buildinfo reader or in a Ghidra loader/analyzer, triggered by a hostile carrier, gives code execution inside a process that holds both OAuth tokens and a live ssh-agent socket. It needs no file read.
  - A cold `npx -y` cache would also run `frida`'s install script (`package-lock.json`: `hasInstallScript` = `node_modules/frida`, observed) with the same env.
- **Why only Low** [OBS/INF]:
  - `/proc/sys/kernel/yama/ptrace_scope` = `1` (observed). Yama gates only `PTRACE_MODE_ATTACH`, so [INF] any same-uid code can already read the L1's `/proc/<pid>/environ`. Child inheritance adds convenience, not a new trust boundary.
  - No value was persisted (see the no-finding section).
- **Smallest fix** (one hunk at `carrier-run.py:264`):
  - Build `child_env` from an allowlist instead of `dict(os.environ)`: `PATH`, `HOME`, `LANG`/`LC_*`, `GHIDRA_INSTALL_DIR`, `JAVA_HOME`, `GHIDRA_MAXMEM`, `GHIDRA_HEADLESS_MAXMEM`, `REA_GHIDRA_*`, `REA_LOG_LEVEL`, plus `TMPDIR=private_root`, `npm_config_offline=true` and `npm_config_update_notifier=false`.
  - Record the whole allowlisted dict in the receipt. It is secret-free by construction, which also closes F3.
- **Evidence the fix is behavior-neutral for allowed verbs** [OBS]:
  - Command: `env -i PATH="$PATH" HOME="$HOME" LANG=C.UTF-8 npm_config_offline=true npm_config_update_notifier=false npx -y rea-agents@6.5.0 inspect-go-binary /usr/bin/shfmt --format json > /tmp/sentinel-envleak/shfmt.min.json`
  - Result: exit 0, and the output is **byte-identical** to the retained `runs/calib-shfmt/inspect-go.json` (`cmp` silent; sha256 prefix `a5ddc648011cc743` for both; `evidence_id` and `normalized_result` equal).
  - `--help` under the same env also exits 0, so offline cache resolution works.
  - `analyze` was not run (lane bound). [INF] It needs only the allowlisted Ghidra/Java/REA vars (`dist/config/environment.js:23-41`).

## F2: Medium (calibration). w1 SentinelCarrierSafety F9's "[OBS] Ghidra gets a scrubbed env" is false

- **Target**: `w1/SentinelCarrierSafety.md:138`: "[OBS] Ghidra gets a scrubbed env: `hostEnvironment: {}` plus the explicit env".
- **Evidence**: F1's chain, steps 4-7. `hostEnvironment: {}` (`GhidraLauncher.js:191`) only stops the spawn helper from merging `process.env` a second time. The explicit `env` (`:190`) already is a full snapshot of `process.env`.
- **Impact**: the observation is mislabelled. If integrated, knowledge would claim the analysis JVM is env-isolated when it is not. w1 scoped the token exposure to "npx/node" only (`:139`), so the L1 kept `dict(os.environ)` while integrating w1 F1/F2/F5 (`carrier-run.py:97-100`) but not F9.
- **Smallest fix**: amend `:138` to "[OBS] Ghidra's JVM env = full REA `process.env` snapshot with HOME/TMPDIR/XDG_*/JAVA option overrides (`GhidraJavaLaunch.js:79-80,109`)". Then F9's minimal-env remediation applies to both processes.

## F3: Low (provenance). `rea_ghidra_env` omits variables REA actually reads

- **Code** [OBS]: `carrier-run.py:287-288` records only keys starting `REA_GHIDRA_`.
  - `runs/*/receipt.json:1797` = `{}` in 7 receipts; `runs/pro-op/receipt.json:1797` = `{REA_GHIDRA_STARTUP_TIMEOUT_MS: 900000}`.
- **What REA also reads** [OBS]:
  - `GHIDRA_INSTALL_DIR` and `JAVA_HOME` (`dist/ghidra/…`, `dist/config/parseConfig.js:45-46`; both set in this seat's env).
  - `GHIDRA_HEADLESS_MAXMEM`/`GHIDRA_MAXMEM`, which set the JVM `-Xmx` (`GhidraJavaLaunch.js:134`).
  - `REA_LOG_LEVEL` (`cli.js:41790`).
- **Impact**:
  - The JDK selection and the heap cap (an OOM can change analysis outcomes) are unrecorded.
  - `GHIDRA_INSTALL_DIR` is recoverable only from `ghidra.log` paths.
  - Recording everything is not the fix, because that would serialize the tokens.
- **Smallest fix**: same as F1. Record the allowlisted `child_env` (minus `HOME`/`PATH` if desired) as `child_env_recorded`.

## F4: Info. Private session parents are left in /tmp

- [OBS] All 8 receipts record `session_parent_leftovers: ['node-compile-cache']`, so `carrier-run.py:366-367` never runs `rmdir`.
- 8 dirs `/tmp/kr17-rea-*` remain, each mode `drwx------` and 2.6 MB (`du -sh`). The receipts state this honestly, so it is not a fabrication.
- The contents are a V8 compile cache for REA's JS, not secrets.
- **Smallest fix**: when `leftovers == ['node-compile-cache']`, `shutil.rmtree` that one entry, then `rmdir`. Keep any other leftover for audit.

## Bounded no-finding: what was checked

Every check below covers all 131 files under `runs/` and `predictions/`.

| check | method | result |
|---|---|---|
| keywords `Bearer`, `sk-`, `ghp_`/`gho_`/`ghs_`/`github_pat_`, `xox?-`, `AKIA…`, JWT `eyJ…`, `authorization`, `api_key`, `passw`, `secret`, `credential`, `token`, `.netrc`/`.npmrc`/`.ssh/`/`.aws/`/`.config/gh`/`agent.db`/`auth.json`, `ANTHROPIC`/`OPENAI`/`GH_TOKEN`/`NPM_TOKEN`/`OP_SESSION` | `grep` (case-insensitive, gitignore off) | `token`: 0 hits. Other patterns: 48 hits, all at line 1 of `runs/pro-op/inspect-go.json` and `predictions/pro-op.inspect-go.json` (24 each): carrier build-info module paths (`go.1password.io/…`, `github.com/1Password/…`, `aws-sdk-go-v2/credentials`, `go-libsecret`), i.e. public `/usr/bin/op` metadata |
| 64-hex strings | Python: 205 distinct values, each bound to a real digest | 187 = sha256 of an actual retained, pinned, or carrier file (re-hashed now); 16 = REA `evidence_id`; 2 = REA profile digests (`analyzer_preset.digest`, `workflow_revision.digest`), identical in all 8 `analyze.json`, so per-version constants, not per-session tokens. **0 unexplained** |
| REA bridge token (`session.json`, 64-hex, `GhidraLauncher.js:95-106` per w1) | 64-hex count in every retained `ghidra.log`/`script.log` | 0 in all 16 log files. The only ≥32-hex runs are the carrier `MD5=` in the `Loading file:` line (e.g. `runs/pro-op/logs/rea-ghidra-yRmWqx/ghidra.log:59`) |
| actual env values | Python: every env var whose name looks secret, full value plus 16-byte windows at stride 8 (for values ≥32 B), searched as bytes in all 131 files | `OPENAI_CODEX_TOKEN`, `XAI_OAUTH_TOKEN`, `HL_INITIAL_WORKSPACE_TOKEN`, `STARSHIP_SESSION_KEY`, `__MISE_SESSION`, `SSH_AUTH_SOCK`, `DBUS_SESSION_BUS_ADDRESS`, …: **found_in=none** for all |
| any env value ≥12 B present verbatim | same script | only `GHIDRA_INSTALL_DIR`, `PWD`, `OLDPWD` (= round-17 dir): non-secret paths |
| high-entropy mixed-case tokens ≥24 chars | Shannon entropy >4.2, attributed to their JSON key or log context | all attributed: Ghidra/install paths, Go `h1:` module sums (`sum`), `module_bytes_base64`/`go_version_bytes_base64` (carrier build-info), `session_dir` names |
| home-dir credential paths | regex `/home/vgpnk/…`, 247 distinct paths | none under `.ssh`, `.aws`, `.config`, `.omp`, `.codex`, `.netrc`/`.npmrc`. Present: Ghidra install and typeinfo paths, the npx cache `~/.npm/_npx/ad9a3fdbcad992c6/…/bridge/ghidra`, carriers under `~/.local/bin` and `~/Projects/kimi-code/node_modules/…` (`predictions/carriers.tsv:2,5,8`; another project's name, Info only), lane paths |
| REA Evidence `environment` field | `json.load` of all 8 `analyze.json` and of `runs/pro-op/inspect-go.json` | `environment: null`, `parameters: {}` (analyze); `environment: null` (inspect-go) |
| receipt env serialization | `carrier-run.py:269-288` | only `python`, `orig_argv` (no env content: `--carrier`, `--label`, `--out-dir`, `--pin` paths) and `rea_ghidra_env`; `os.environ` is never dumped |

Limits:
- Value-matching ran against **this seat's** env. [INF] L1's env is the same host-inherited set but was not read.
- `carrier-run.stdout` differs from `receipt.json` only after byte 104630 (`cmp`), and both were scanned in full.
- Nothing was executed except allowed `npx … --help` and `inspect-go-binary` (reads the file only). No REA analyze or Ghidra run, no carrier executed.

## Housekeeping

- Scratch files: `/tmp/sentinel_envleak_scan.py`, `/tmp/sentinel_envleak_envmatch.py`, `/tmp/sentinel-envleak/`. No installs or upgrades.
- Wrote only this report.
