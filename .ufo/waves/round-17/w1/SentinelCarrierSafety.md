# SentinelCarrierSafety — round 17 w1 (advisory, author-side)

Scope: the planned `W/tools/carrier-run.py` (contract.md:31-49). This is a review of the plan only: at 10:3x
`W/tools/` did not exist (observed: `ls .ufo/waves/round-17/tools`, "No such file or directory"), so no
implementation lines are cited. The evidence comes from the REA 6.5.0 dist in the npx cache
(`R=~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime`), the pilot evidence, and the host state.
Labels: **[OBS]** means observed; **[INF]** means inferred.
Tools installed: none.

## Verdict
Carrier execution: no finding (see "Bounded no-finding" below). Two Medium findings must be fixed in the tool before
L1 runs it:
- F1: run attribution by new-dir set difference.
- F2: orphaned Ghidra after a timeout.

The Low findings are cheap hardening steps or contract fixes. None is a blocker on its own.

## Findings

### F1 — Medium — new-dir set difference captures other sessions' Ghidra roots
- **Exploit/failure path:** contract.md:36-39 attributes every `/tmp/rea-ghidra-*` dir that appears after the
  baseline to "our" analyze. Any other REA session that starts during the window gets copied into `DIR/logs/` and
  recorded as this carrier's log.
- **Evidence:**
  - [OBS] A live REA MCP server is running from the same npx cache: pid 3221 `npm exec rea-agents@6.5.0 mcp`,
    its child 3234 `node …/.bin/rea mcp`, parent omp pid 3092, started 09:57:31.
  - [OBS] Every Ghidra session uses one shared root and prefix: `SESSION_ROOT = ghidraSessionRoot()` →
    `tmpdir()` (`R/binary-BVOr2mgE.js:5578-5585,5624`), plus prefix `rea-ghidra-` (`:5924-5928`).
  - [INF] Any tool call to that server, or to another lane's REA during an L1 run, creates a dir that the set
    difference cannot tell apart from ours.
- **Impact:**
  - Another session's ghidra.log could be attached to the wrong carrier. Its `IMPORTING:` line shows that
    session's target path. log-extract/compare would then report a false match or mismatch against the prediction.
  - Another session's data could land in the lane dir, which gets committed.
- **Smallest remediation:** accept a new dir only when one of these attribution checks passes:
  - (a) Primary: read `ownership.json`, which holds no token (`R/binary-BVOr2mgE.js:3773-3784`: run_id, pid,
    process_group_id, parent_pid, launcher). Accept the dir only if `parent_pid` is the analyze Popen pid or a
    descendant of it (walk `/proc/<pid>/stat` ppid while the run is live).
  - (b) Cheaper fallback: `lstat` existence of `<dir>/target-<carrier_sha256[:12]>.bin`. This is a name check
    only. The pattern was observed at pilot `shfmt-log/ghidra.log:46`
    (`/tmp/rea-ghidra-LuPZRm/target-58f765638eed.bin`).

  Record any unattributed new dirs by name only, under `unattributed_new_dirs`, and never open them.

### F2 — Medium — a timeout kill leaves Ghidra and its runtime root behind
- **Exploit/failure path:** `subprocess` timeout, or a bare `Popen.kill()`, sends SIGKILL only to the `npx`
  (`npm exec`) pid.
- **Evidence:**
  - [OBS] REA starts Ghidra in its own process group: `ownership_kind: "posix-process-group"`,
    `process_group_id` (`R/binary-BVOr2mgE.js:3777-3780`).
  - [OBS] REA removes the runtime root only in `PrivateRuntimeRoot.close()` (`R/PrivateRuntimeRoot-DAy0PiBM.js:248-256`).
  - [OBS] REA aborts cleanly only on SIGINT/SIGTERM delivered to node (`R/DirectAnalysis-BgvAtpN3.js:466-467`).
  - [OBS] Shutdown budget `SHUTDOWN_TIMEOUT_MS = 1e4` (`R/binary-BVOr2mgE.js:5623`).
- **Impact:**
  - [INF] An orphaned java/node keeps analyzing, which breaks "L1 runs every carrier analysis once,
    sequentially".
  - [INF] The `/tmp/rea-ghidra-*` dir stays behind, with `session.json` still holding the bearer token (F3).
  - [INF] The orphan keeps writing logs, and the next step can pick that up.
- **Smallest remediation:**
  1. Start with `Popen(..., start_new_session=True)`.
  2. On timeout, `os.killpg(pgid, SIGTERM)`, then wait ≥ 15 s (more than the 10 s REA shutdown), then
     `killpg(SIGKILL)`.
  3. Afterwards, if the attributed dir still exists, read its `ownership.json` `process_group_id`. Signal that
     group only after `/proc/<pid>/cmdline` contains the dir path.
  4. Record in the receipt: `timed_out`, the signals sent, `runtime_root_removed: bool`, and
     `orphan_pids_remaining`.

### F3 — Low — the contract permits reading other dirs, and `session.json` holds a bearer token
- **Path:** contract.md:39 says "Never touch other dirs' files beyond reading". That permits reading any file in
  any `rea-ghidra-*` dir. A generic implementation (`copytree`, globbing `*`, `os.walk`) would copy
  `session.json` into the lane dir.
- **Evidence:**
  - [OBS] `session.json` contains `token: session.token`, a 32-byte random hex value (`R/binary-BVOr2mgE.js:3693-3702,5956`).
  - [OBS] The pilot logs contain no 64-hex string: `grep -c '[0-9a-f]\{64\}'` returned 0 for all four pilot
    `ghidra.log`/`script.log` files. So the two allowed files did not leak the token in the pilot.
- **Impact:** the token is scoped to a session and dies after close. A same-uid process could already read it in
  `/tmp`. The real harm is a committed secret-shaped value, which violates the review target. Low.
- **Remediation:** amend contract.md:39 to: "open only `ghidra.log`, `script.log`, and (for attribution)
  `ownership.json`, by exact name, in attributed dirs; never open `session.json`, `bridge.sock`, `project/`,
  `home/`, `config/`, `tmp/`". Use an allowlist, never a glob.

### F4 — Low — symlink-following copy from a dir another uid can plant
- **Path:** `/tmp` is `drwxrwxrwt root`. Another uid can create `/tmp/rea-ghidra-x/ghidra.log ->
  /home/vgpnk/.ssh/id_ed25519`. `shutil.copy*` follows the link with vgpnk's rights, which would put a
  credential into `DIR/logs/` and from there into git.
- **Evidence:** [OBS] `fs.protected_symlinks = 1` protects links only inside sticky world-writable dirs. The
  attacker's subdir is not sticky, so it is not covered.
- **Impact:** [OBS] the only login uid ≥ 1000 is vgpnk (`/etc/passwd`), so a cross-uid attacker needs a
  service/sandbox uid. Low.
- **Remediation:**
  - Filter dir names with `^rea-ghidra-[A-Za-z0-9]{6}$` (mkdtemp form, `R/PrivateRuntimeRoot-DAy0PiBM.js:241`).
    This also excludes `rea-ghidra-socket-*`, which the current glob matches (`R/binary-BVOr2mgE.js:5340-5343`).
  - `lstat(dir)`: require `S_ISDIR`, `st_uid == os.getuid()` and `mode & 0o077 == 0`.
  - Open files with `O_RDONLY|O_NOFOLLOW`, then `fstat` and require `S_ISREG`.

### F5 — Low — the watched root silently diverges if `TMPDIR` is set
- **Evidence:**
  - [OBS] The session root is `tmpdir()`. It falls back to `/tmp` only when that path has a dot-prefixed element
    (`R/binary-BVOr2mgE.js:5578-5585`).
  - [OBS] `TMPDIR` is unset in this seat's shell. [INF] L1's environment is unverified.
- **Impact:** with `TMPDIR=/x`, REA writes `/x/rea-ghidra-*` while the tool watches `/tmp`. The result is zero
  retained logs. In the worst case, unrelated `/tmp` dirs get attributed (F1).
- **Remediation:** pass the child an explicit env with `TMPDIR` removed, or set to `/tmp`. Watch that same
  resolved root, and record it in the receipt.

### F6 — Low — `--search NAME` argv form allows option injection into a file-writing flag
- **Evidence:**
  - [OBS] `rea search --help`: "`--pattern <string>` … use `--pattern=<value>` for leading dashes".
  - [OBS] Both `search` and `analyze` accept `--snapshot <string>` ("Load and update a local analysis snapshot"),
    which writes a file.
- **Path:** the two-token form `--pattern NAME` with a NAME like `--snapshot=/some/path` would write outside the
  out dir. NAME comes from L1, so this is trusted input. Low.
- **Remediation:** always emit `--pattern=NAME`. Never pass `--snapshot`/`--provider`. Record the argv as run
  (already in the contract).

### F7 — Low/Info — child writes outside the out dir that cannot be avoided
- **Expected writes:**
  - npm `~/.npm/_logs` and `_cacache` [INF].
  - REA `/tmp/rea-ghidra-*`, deleted at close (`:248-256`).
  - `/tmp/rea-process-token-*` (`R/ProcessOwnership-DXC5-UWt.js:258`).
- **Ghidra user state is redirected:** `HOME`/`XDG_*` point into the runtime root (`R/binary-BVOr2mgE.js:4005-4022`).
  - [OBS] Pilot `shfmt-log/ghidra.log:4` loads preferences from `/tmp/rea-ghidra-LuPZRm/config/...`.
  - [OBS] `~/.config/ghidra` and `~/.cache/ghidra` were last modified 2026-10-12, so the pilot did not touch them.
  - [OBS] Pilot cwd `/tmp/kr17-pilot` holds only the pilot's own files, so REA wrote nothing to cwd.
- **Remediation:** set child cwd to `DIR`. Have the receipt list `external_writes_expected` as a declared
  limitation, not a claim of none.

### F8 — Low — network and supply chain via `npx -y`
- **Evidence:**
  - [OBS] contract.md:7 says "No network", but `npx -y` may resolve from the registry.
  - [OBS] The cached lock pins `rea-agents` 6.5.0, `integrity sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`
    (`~/.npm/_npx/ad9a3fdbcad992c6/package-lock.json`). The live MCP server (F1) shares that cache dir.
- **Remediation:** set child env `npm_config_offline=true`, and record the lock's integrity plus the resolved
  `rea.mjs` sha256 in the receipt.

### F9 — Low — environment passthrough and unbounded untrusted log content
- **Environment:**
  - [OBS] Ghidra gets a scrubbed env: `hostEnvironment: {}` plus the explicit env (`R/binary-BVOr2mgE.js:3768-3769,4005-4022`).
  - [INF] npx/node inherit L1's full env, including any API tokens.
  - Remediation: pass a minimal env (`PATH`, `HOME`, `LANG`, `npm_config_offline`). Never serialize
    `os.environ` into the receipt.
- **Log content:** ghidra.log carries strings derived from the carrier (Go analyzer type/function names).
  - Remediation: cap each copied file (e.g. 64 MiB) and record `truncated`. log-extract should treat the lines
    as data only.

### F10 — Low — carrier path is not constrained
- **Path:** `--carrier PATH` is hashed (pins) and copied by REA to `/tmp/rea-ghidra-*/target-<sha12>.bin`
  (pilot `ghidra.log:46`), and its sha256 is published in the receipt.
- **Impact:** if a credential path were passed by mistake, its hash and a /tmp copy would result.
- **Remediation:** before any step, require ELF magic `\x7fELF` on an `O_NOFOLLOW` open, and refuse paths under
  `~/.ssh`, `~/.gnupg`, `~/.omp` or `~/.config/**/auth*`.
- **Current selection:** [OBS] pilot carriers are `/usr/bin/shfmt` and
  `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/…/bin/esbuild`. Neither is a
  credential path.

## Bounded no-finding: carrier execution
No path to carrier execution was found:
- [OBS] `dist/go/*.js` (GoBinaryProvider, GoElfImage, …) contain no `spawn`/`execFile`/`child_process`, so
  `inspect-go-binary` parses only. [INF] The bundled copy in cli-runtime is the same code.
- [OBS] `analyze` auto-selected the Ghidra provider: pilot `esb.json` `analysis_profile.upstream_analysis_profile.provider.id = "ghidra"`.
- [OBS] Ghidra imports an immutable snapshot copy (`import_mode: "ephemeral-source-immutable"`).
- [OBS] The only scripts run were `ReaGhidraNoReturnFix.java` and `ReaGhidraBridge.java` (pilot
  `shfmt-log/ghidra.log:120-124`).

Residual risk: a future `--provider` or `--target-format` argument could select a different provider. Mitigation:
never pass them, and assert `provider.id == "ghidra"` in the receipt.

Searched:
- In the REA dist: `rea-ghidra-|mkdtemp|ghidra.log|script.log`, `SESSION_ROOT|HOME|XDG|-log|-scriptlog`, SIGINT/SIGTERM/exit
  handlers, and `spawn|execFile|child_process` in `dist/go`.
- `rea analyze --help` and `rea search --help`.
- Pilot `README.txt`, `SHA256SUMS`, both `ghidra.log`/`script.log`, and `esb.json`/`shfmt.json`.
- Host: sysctl `fs.protected_*`, `/etc/passwd` uids, `$TMPDIR`, `/tmp/rea-*`, `~/.config|.cache/ghidra`, running
  `rea`/`ghidra` processes, and `/tmp/kr17-pilot`.

Not searched: the carrier-run.py implementation, which did not exist yet. Re-review once it lands, against F1-F6.
