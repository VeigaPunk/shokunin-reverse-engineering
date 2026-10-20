# SentinelPollRace — round 17 W1 (author-side advisory, read-only)

Scope: the carrier-run.py log poller design, `contract.md:36-41`, plus how its output reaches downstream tools.
`W` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17`.
`R` = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` (rea-agents 6.5.0, the version the contract pins).
Nothing was installed, run, or edited apart from this report. `W/tools/` does not exist yet, so I reviewed the contract text, not code.

## F1 — HIGH (correctness): "NEW dir" is not the same as "this run's dir", so a sibling lane's session log can be retained as this carrier's evidence

**Exploit path (accidental, no attacker needed).**
1. carrier-run takes a baseline glob of `/tmp/rea-ghidra-*` (`contract.md:36`).
2. Any other REA process on the host then opens a Ghidra session before our run ends. The new dir counts as NEW and its `ghidra.log`/`script.log` are copied into `DIR/logs/<dirname>/` (`contract.md:37-38`).
3. The receipt lists that dir under retained logs (`contract.md:44-45`).

**Evidence (observed).**
- Every REA Ghidra session, from the CLI or from the MCP server, uses `mkdtemp(<SESSION_ROOT>/rea-ghidra-XXXXXX)`: `R/ghidra/GhidraClient.js:32,395-399`, `R/process/PrivateRuntimeRoot.js:38`, and the MCP bundle `R/mcp/main-kBXHZ8S5.js:7751-7752`.
- mkdtemp's 0700 mode only separates different users. Every lane on this host runs as `vgpnk`, so foreign dirs are fully readable. That is why contamination is possible.
- A REA producer is live on the host right now: `ps` showed pid 3221 `npm exec rea-agents@6.5.0 mcp` (parent `omp` pid 3092, about 35 min old) with child pid 3234 `node …/.bin/rea mcp`. It can create a session dir whenever its client opens a binary. 170+ peer agents are live.
- The exposure window is the whole REA step. The pilot esbuild session logged 10:18:19 → 10:19:53 (`W/pilot/esbuild-0.25.12-log/ghidra.log:2`, `W/pilot/esbuild-0.25.12-log/script.log`). `--timeout` allows up to 1800 s (`contract.md:32`).

**Nothing downstream catches it (observed).**
- `log-extract.py` parses Go lines only and never checks which target the log belongs to (`contract.md:51-60`).
- `receipt-validate.py` only recomputes sha256 values and pins (`contract.md:106-108`).
- So a foreign log from another Go binary would yield real-looking `go_lines` and flow into `compare.py` (`contract.md:75-78`) and into C2's ">=3 retained runs" count (`claims.json:22`).
- The worst case is a foreign in-range Go carrier: it would give a false match, not an error.

**Sibling variants (observed in source).**
- **a. Glob over-match.** `rea-ghidra-socket-*` dirs also match `rea-ghidra-*` (`R/ghidra/GhidraTransport.js:16-18`). They are created only when the socket path exceeds 107 bytes (`:10-15`) and contain no logs, but they inflate the NEW set.
- **b. TMPDIR redirect.** The session root is `os.tmpdir()` whenever that path has no dot-prefixed element. It falls back to `/tmp` only if it has one (`R/ghidra/GhidraSessionRoot.js:28-38`). If the L1's or a wrapper's environment ever sets `TMPDIR=/var/tmp/x` or similar, our sessions leave `/tmp`. The poller would then see zero dirs of our own and only foreign ones, a fully foreign "retained log". Today `TMPDIR` is empty in this seat (observed); the L1's environment is not observed.
- **c. Baseline scope.** The `--search` steps "same" wording (`contract.md:40`) does not say whether the baseline is re-taken per step. A single baseline lets the analyze step's dir (if it leaked after a kill or timeout) or a search step's dir be attributed to the wrong step.
- **d. Unhandled races.** A foreign session can close between listdir and copy (`rm -rf` at `R/process/PrivateRuntimeRoot.js:49`). `FileNotFoundError` is then a normal event. If it is not caught per dir, a foreign lane can abort our capture (exit 2) or leave a half-recorded entry.
- **e. Cross-lane leak.** Foreign logs copied under `W/runs/` would put another lane's analysis paths into kaidoku's evidence tree (low).

**Pilot calibration (observed).** The pilot used the same "new dir" rule (`W/pilot/README.txt:4`) but is not contaminated:
- `shfmt-log/ghidra.log:2,46`: `/tmp/rea-ghidra-LuPZRm/…`, `IMPORTING …/target-58f765638eed.bin`. This matches the shfmt sha256 prefix at `README.txt:7`.
- `esbuild-0.25.12-log/ghidra.log:2,46`: `/tmp/rea-ghidra-r9xmGu/…`, `target-bab29b2ca7a9.bin`. This matches `README.txt:8`.

So F1 is a latent risk for the measured runs, not an observed defect in the pilot evidence.

## F2 — the two suggested binding keys: one needs care, the other doesn't exist

- **`target-<sha prefix>.bin` is necessary but not sufficient.**
  - The snapshot name is `target-${sha256.slice(0,12)}${ext}`, with `ext=".bin"` when the carrier has no short alphanumeric extension (`R/ghidra/GhidraTargetSnapshot.js:14,76-78`). Both pilot carriers got `.bin`.
  - Two lanes analyzing the same carrier, such as the shared `/usr/bin/shfmt`, produce the same name. The sha12 check alone cannot tell them apart.
  - The file appears only after mkdtemp and endpoint allocation (`R/ghidra/GhidraClient.js:395-420`). A dir found without it is "pending", not "foreign".
- **`session.json` has no pid, and it contains a secret.** It holds `{transport, endpoint_path, token, run_id, target_sha256, …}` (`R/ghidra/GhidraLauncher.js:95-106`; the token is at `:98`). It must never be copied into `DIR`. Reading `target_sha256`/`run_id` from it is fine.
- **The pid lives in `ownership.json`.** It is written right after the JVM spawn: `{run_id, pid: JVM leader, process_group_id, parent_pid: process.pid of the REA node process, created_at}` (`R/ghidra/GhidraLauncher.js:195-206`). This is the process-binding key.
- **Process tree under npx (observed on the live MCP instance).** `npm exec` pid 3221 → `node …/.bin/rea` pid 3234, with the same SID/PGID (3221). That makes `parent_pid` a direct child of the Popen'd `npx`.
  - [INFERENCE] the `analyze` subcommand uses the same `npm exec` spawn path.

## Smallest remediation (contract change for L1; ordered, cumulative)

1. **Isolate by construction.**
   - Create `rt = tempfile.mkdtemp(prefix="kr17-rea-", dir="/tmp")` per carrier-run.
   - Assert that no element of `os.path.realpath(rt)` starts with `.`. Otherwise REA silently falls back to shared `/tmp`, per `GhidraSessionRoot.js:33-37`. `W` itself contains `.ufo`, so `rt` cannot live under `DIR`.
   - Run every REA step with `env={**os.environ, "TMPDIR": rt}` and `start_new_session=True`.
   - Poll only `rt/rea-ghidra-*`, excluding names that start with `rea-ghidra-socket-`.
   - Record `rt` in the receipt and `os.rmdir` it at the end (it fails loudly if REA leaked a dir; record that, don't hide it).
   - Socket path budget: `/tmp/kr17-rea-XXXXXXXX/rea-ghidra-XXXXXX/bridge.sock` is about 50 bytes, under 107.
   - [INFERENCE until the first real run] Node's `os.tmpdir()` honours `TMPDIR` on POSIX. The first run's `ghidra.log` line 2, `Using log file: <rt>/rea-ghidra-…/ghidra.log`, proves or refutes this.
2. **Bind before copying.** Keep this even with step 1, because it also covers a dot-path fallback. A NEW dir is bound to a step only when all of these hold:
   - the basename matches `^rea-ghidra-[A-Za-z0-9]{6}$`;
   - `target-<carrier_sha256[:12]>.bin` exists as a regular file (lstat);
   - `ownership.json` parses, and `/proc/<parent_pid>/stat` field 6 (session id) equals the step's `Popen.pid` while the Popen is alive. Fallback: walk the ppid chain up to `Popen.pid`.
   - Record `run_id`, `parent_pid`, `pid`, and `binding: {target_name, sid_match}` in the receipt.
   - Until bound, the dir is pending: do not copy it. A pending dir that disappears is recorded as `unbound_vanished`.
   - Foreign or unbound dirs get their names recorded in `foreign_new_dirs`; their contents are never copied.
   - Never copy `session.json`.
3. **Cardinality and scope.** Re-take the baseline before each step. Each REA step must end with exactly one bound dir; 0 or more than 1 means exit 2. Catch `FileNotFoundError`/`PermissionError` per dir per poll.
4. **Post-hoc content gate.** Add this to `log-extract.py` output and enforce it in `receipt-validate.py`: the retained `ghidra.log` must contain `Using log file: <session_dir>/ghidra.log` and `IMPORTING: file://<session_dir>/target-<sha12>.bin`, matching the receipt's `session_dir` and the carrier's pinned sha256. Today it would pass both pilot logs (observed above) and reject any foreign or wrong-carrier log, even after the fact.
5. **Optional depth gain** (it also narrows `contract.md:46-47`; [INFERENCE], needs one exercised run).
   - Once a dir is bound, `os.link` its `ghidra.log`/`script.log` into `rt/keep/<dirname>/`. `/tmp` is a single xfs mount (observed), and `fs.protected_hardlinks=1` allows this because we own the files.
   - REA's `rm -rf` (`PrivateRuntimeRoot.js:49`) only unlinks the directory entries. The kept inode then holds the JVM's final bytes, closing the "lines after final poll" gap.
   - This is valid only if Ghidra's `-log` appender (`GhidraLauncher.js:382-385`) never rotates or recreates the file. Verify that the kept inode equals the live one at the last poll, and that nlink was 2.
   - Copy into `DIR` (btrfs, a different fs) after the step ends.

## Searched, no further finding
- REA dist: `rea-ghidra` prefix sites, `GhidraSessionRoot`, `PrivateRuntimeRoot`, `GhidraTargetSnapshot`, `GhidraTransport`, and `GhidraLauncher` runtime paths and descriptors.
- Live `/tmp/rea-ghidra-*`: none at review time.
- REA processes and their tree.
- `W/contract.md`, `W/claims.json`, and `W/pilot/*` (logs, README, SHA256SUMS).

No `REA_GHIDRA_*` knob for keeping the session root was found beyond those `W/pilot/README.txt:5` already lists. Installs: none.
