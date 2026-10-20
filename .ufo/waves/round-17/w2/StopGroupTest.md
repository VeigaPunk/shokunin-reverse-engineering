# StopGroupTest — round 17 w2 (advisory, author-side)

Target: `.ufo/waves/round-17/tools/carrier-run.py` at lane rev `da64646` (file observed again mid-run at
w2-hardened rev; anchors below are that current rev). Harness:
`.ufo/waves/round-17/w2/stopgroup-attack.py`, run as
`python3 -B .ufo/waves/round-17/w2/stopgroup-attack.py` (all state under `/tmp/kr17-stopgroup-*`, exit 0).
W1 basis: `w1/SentinelCarrierSafety.md:45-66` F2 — remediation items 3-4 were "signal the Ghidra
`process_group_id` from `ownership.json`" and "record `orphan_pids_remaining`".
Labels: **[OBS]** = measured; **[INF]** = inferred. Tools installed: none.

## Verdict
Three findings: the w1 F2 fix is partial — it kills only the child's own group, so a grandchild that
holds its own process group (exactly how REA spawns Ghidra: `ownership_kind: "posix-process-group"`,
`w1/SentinelCarrierSafety.md:49-50`) survives a timeout; `run_step`'s timeout path was never hardened at
all; and `run()`'s exit-code logic ignores `timeout`/`stop`, so a timed-out analyze that exits 0 yields a
success receipt. Severity: F1/F2 Medium, F3 Low.

## Findings

### F1 — Medium — `_stop_group` leaves the Ghidra-class grandchild alive
- **Path:** `carrier-run.py:114` `os.killpg(proc.pid, signal.SIGTERM)`, `:116` `proc.wait(timeout=15)`,
  `:119` `os.killpg(proc.pid, signal.SIGKILL)`. The pgid signalled is the child's own group only. A
  descendant that created its own group/session is never addressed — and there is no `ownership.json`
  read or `process_group_id` signalling anywhere in the file (w1 F2 remediation item 3, not landed).
- **Evidence:** [OBS] scenario A — child ignores SIGTERM; grandchild spawned with `start_new_session=True`
  (the documented REA Ghidra shape). Output:
  `"stop": "sigkill", "exit": -9, "wall_s": 16.5, "grandchild_alive_after_stop_group": true`.
  `os.kill(<gc>, 0)` succeeded after `_stop_group` returned; the orphan was reparented and kept running
  until the harness reaped it.
- **Impact:** [INF] on a real timeout the orphaned java/Ghidra keeps analyzing (breaks sequential
  once-per-carrier), keeps writing its `rea-ghidra-*` root, and no receipt field names it: `rec` gets only
  `stop`/`timeout`/`exit` (`carrier-run.py:450-452,481`) — w1 F2's `orphan_pids_remaining` was not landed.
  The new `session_parent_leftovers` gate (`:412-414`) detects the leftover *directory* and returns 2,
  but the *process* stays alive after `run()` exits; nothing terminates it.
- **Smallest remediation:** after `_stop_group`, for each `session_parent_leftovers`/tracked dir read
  `ownership.json` `process_group_id` and signal it (guarded by `/proc/<pid>/cmdline` containing the dir
  path, per w1 F2 item 3); record `orphan_pids_remaining` in the step record.

### F2 — Medium — `run_step` timeout still uses bare `proc.kill()`, not `_stop_group`
- **Path:** `carrier-run.py:159-160` — `except subprocess.TimeoutExpired: proc.kill()`. This is exactly
  the un-hardened code path w1 F2 described; the fix was applied only to `_run_polled`.
- **Evidence:** [OBS] scenario B — inspect-go-binary step on a private-runner child; grandchild placed in
  the *same* process group (a correct `killpg` would reach it). Output:
  `"timeout": true, "exit": null, "grandchild_pgid_same_as_child_group": true,
  "grandchild_alive_after_proc_kill": true`.
- **Impact:** [INF] `inspect-go-binary` is spawned via `_private_runner` (`:103-105`, own session). If it
  hangs and is killed, every same-group descendant — npx→node→rea children — survives with its private
  TMPDIR root, then gets picked up by the next step's poller.
- **Smallest remediation:** call `_stop_group(proc)` in the `run_step` timeout branch instead of
  `proc.kill()`, and record `rec["stop"]`.

### F3 — Low — a timed-out step that exits 0 still yields `run()` exit code 0
- **Path:** `carrier-run.py:405-415` — return-code logic checks `pins_cmp`, `steps["analyze"]["exit"]
  not in (0,)`, and the bound-session count; `rec["timeout"]`/`rec["stop"]` never reach it.
- **Evidence:** [OBS] scenario D — injected runner; analyze times out, child traps SIGTERM and exits 0
  (REA's documented SIGTERM clean-abort path can produce exactly this). Output:
  `"analyze_timeout": true, "analyze_stop": "sigterm", "analyze_exit": 0, "receipt_error": null,
  "run_exit_code": 0`. A receipt asserting success while its own analyze step says `"timeout": true,
  "stop": "sigterm"` is internally contradictory.
- **Impact:** today REA exits nonzero on SIGINT/SIGTERM by observation, so this is latent rather than
  live; the check `"exit" not in (0,)` alone is the only thing standing between a SIGTERM-clean-exit-0
  REA build and a false clean receipt.
- **Smallest remediation:** `if steps["analyze"].get("exit") not in (0,) or
  steps["analyze"].get("timeout")` → return 2.

## Additional observations (not findings)
- **[OBS] Scenario C:** with a runner lacking `start_new_session` (the module's own `_popen`,
  `:95-96`), `killpg(proc.pid)` raises ESRCH and `_stop_group` degrades to `proc.kill()` labelled
  `"stop": "kill"`, while the child shared the *parent's* group (`child_pgid == our_pgid`). Harmless
  here — wrong pgid is a no-op — but the same `"kill"` label also covers the "killed the child alone,
  group signalled nothing" case; the receipt cannot distinguish a real group stop from a degraded one.
  Mild pgid-collision hazard if `proc.pid` ever equals a live unrelated pgid. [INF]
- **[OBS] 15 s blind window:** during `proc.wait(timeout=15)` inside `_stop_group` no `poller.scan()`
  runs; if the runtime root is deleted inside that window the final scan at `:479` sees nothing.
  Bounded: earlier copies are retained; only the tail is lost (already disclaimed by
  `log_capture_limit`, `:40-43` and w1 RevReaLifecycle §6).

## Bounded no-finding
- `_stop_group` correctly reaches "sigkill" and reaps the child for a SIGTERM-ignoring child in its own
  session (A: `exit=-9`, `stop="sigkill"`); `exit_code` after stop is not `None` in this path
  (`:475-478` `proc.wait(timeout=10)` succeeds post-SIGKILL).
- `pgid` non-collision for the private runner is by construction (`start_new_session` makes the child a
  group leader, `:103-105`).
- The new `session_parent_leftovers` gate (`:412-414`) does catch a surviving session dir → exit 2; F1's
  residual gap is the surviving *process* and the absent orphan record, not silent receipt success.

Ran: `python3 -B .ufo/waves/round-17/w2/stopgroup-attack.py` → JSON above, exit 0, 20.6 s wall.
Also read: `tools/carrier-run.py` (current rev), `tools/pins.py`, `w1/SentinelCarrierSafety.md`,
`w1/RevReaLifecycle.md`.
