# CR4 — service-launch pattern: process or claim?

**Verdict: ATTACK SUSTAINED.** A parent-launched, caller-independent user service is a process. It is not a claim. The line is a close-time seal, in the steered round's receipts, of a typed terminal that matches a pre-accepted branch of that round's claim, bound to `InvocationID` plus envelope hash. A timeout budget, a unit name, a live JVM, or "either way" is not that seal.

This instance is already on the process side of the line. `arc2-r6-pe` is not in-flight and was never a multi-hour run. Its terminal is an instrument-abort (unknown analyzer, before analysis). That does not verify the 91.6MB scale-wall claim either way — same class as round 3's typed-but-unmatched kill (`SCORECARD.md:802-804`). Landing it as the wall's honest-negative would launder an instrument defect into coverage.

## Evidence

Observed 2026-10-18T20:44:40Z and rechecked 2026-10-18T20:52:47Z. Read-only. Service not signaled. Only write: this file. Custody against the pre-pair receipt: 5/5 rc=0.

```sh
date -u +%Y-%m-%dT%H:%M:%SZ
# 2026-10-18T20:44:40Z  (recheck 2026-10-18T20:52:47Z)
systemctl --user show arc2-r6-pe.service -p ActiveState -p SubState -p Result \
  -p ExecMainStatus -p NRestarts -p Type -p Restart -p RemainAfterExit \
  -p InvocationID -p MemoryPeak -p MemoryMax -p ExecMainStartTimestamp \
  -p ExecMainExitTimestamp -p MainPID -p ControlGroup
# ActiveState=failed SubState=failed Result=exit-code ExecMainStatus=1
# NRestarts=0 Type=simple Restart=no RemainAfterExit=no
# InvocationID=31dc1c7f0a5e4f9db082dfc9da37b90d
# MemoryPeak=2208227328 MemoryMax=9663676416
# ExecMainStartTimestamp=Sun 2026-10-18 17:40:58 -03
# ExecMainExitTimestamp=Sun 2026-10-18 17:41:06 -03
# MainPID=0 ControlGroup=   (recheck; unit has no child)
journalctl --user -u arc2-r6-pe.service --no-pager -o cat
# Started … analyze …/windows_release_arm64.exe.
# Main process exited, code=exited, status=1/FAILURE
# Failed with result 'exit-code'.
# Consumed 13.930s CPU time over 7.554s wall clock time, 2G memory peak.
sha256sum /var/tmp/arc2-l6r6-pe/stdout.json
# 4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7
stat -c '%s %y' /var/tmp/arc2-l6r6-pe/stdout.json
# 16692 2026-10-18 17:41:06.513410314 -0300
# same size and mtime at both observations (frozen)
sha256sum /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe
# 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292
stat -c '%s' …/windows_release_arm64.exe
# 91662336
tail -n +2 .ufo/waves/arc2-loop1-round6/receipts/config-pre-pair.txt | sha256sum -c -
# five paths OK; RC=0
```

Unit file `/run/user/1000/systemd/transient/arc2-r6-pe.service:6-12`: `MemoryMax=9663676416`, `StandardOutput=file:/var/tmp/arc2-l6r6-pe/stdout.json`, `REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000`, `ExecStart` is `npx -y rea-agents@6.5.0 analyze` of the 91.6MB PE. The 7200000 ms figure is a ceiling in the unit file, not a measured duration. Journal wall is 7.554s. Pre-pair stamp `.ufo/waves/arc2-loop1-round6/receipts/config-pre-pair.txt:1` is `2026-10-18T20:39:12Z`; the unit started at 17:40:58 -03 (20:40:58Z) and exited at 17:41:06 -03 (20:41:06Z). This `InvocationID` did not cross a round boundary. The pattern is built to (caller-independent, 2 h budget, "across rounds"); this instance did not use that span.

Envelope `/var/tmp/arc2-l6r6-pe/stdout.json` is not JSON (`json.load` raises `Expecting value: line 1 column 1`). It is a 39-line error document:

- `:1-5` — `error: Analysis failed` / `code: execution_failure` / `retryable: false`
- `:13` — `target_sha256` matches the binary hash above
- `:31` — pre-script argv is the disabled-analyzer list, then `Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis` at `ReaGhidraAnalysisOptions.java:22`, `Processing aborted as a result of pre-script`
- `:38-39` — `failure_kind: process` / `failure_message: Ghidra exited before bridge startup`
- string counts in the 16692 bytes: `analyzer_preset=0`, `evidence_id=0`

The throw is the script's own pre-analysis check, not a scale failure: `ReaGhidraAnalysisOptions.java:21-22` throws when `analysis.getAnalyzer(name) == null || !options.containsKey(name)`. Runtime dir named in the envelope (`rea-ghidra-f5rC3Z`) is already gone; only `stdout.json`, empty `stderr.log`, and `node-compile-cache` remain under `/var/tmp/arc2-l6r6-pe`.

Process-identity trap, same minute: `ps` showed a live `AnalyzeHeadless` (pid 2280341, `-Xmx6G`) whose cwd/tmpdir is `/var/tmp/arc2-l6r6-E9-mid/` and whose import is `target-a6a9a3654c41.exe`. That is not `arc2-r6-pe` (`ControlGroup` empty, `MainPID=0`). A live JVM is not this claim's service.

Network, same class as round 4: `~/.npm/_logs/2026-10-18T20_40_59_043Z-debug-0.log:14` — `http fetch GET 200 https://registry.npmjs.org/rea-agents 56ms (cache revalidated)`. Metadata revalidation, not a package download. The process did it; the claim text does not record it.

## Where the line already is, and where this pattern moves it

- A claim is an axis-move with a falsifiable before→after, owned by the steered round only (`PROTOCOL.md:86-87`, `:96-97`). A lane must not claim another round's work.
- Evidence must resolve at closure. A path a later session cannot reach is not evidence; commit the artifact or cite a reproducible command (`PROTOCOL.md:341-343`). `/var/tmp/arc2-l6r6-pe/stdout.json` is a process artifact until its hash and branch label are in the round record. The runtime dir is already gone, so the deleted logs cannot be the seal.
- `held` requires a carrier run this round (`SKILL.md:31-32`; `corpus/QUALITY.md:20`). `>90MB PE` is `measured r4`, not held (`SKILL.md:65`). Sessions are ephemeral (`SKILL.md:39`).
- Round 3 already refused a typed terminal that matched neither pre-accepted branch: outer-cap kill, `cancelled`, `cleanup:complete`, no evidence sealed, "neither HELD nor the pre-accepted typed refusal, so the claim cannot verify" (`SCORECARD.md:800-804`; `.ufo/reports/arc2-loop1-round3/kaidoku.md:112-113`). Coverage stayed 79/79.
- Round 4 ran the same binary as **round infrastructure**, not as the coverage claim. Typed OOM in 4m42s; REA's envelope mislabeled it `cancelled` (`SCORECARD.md:894-901`). Coverage unchanged (`SCORECARD.md:908`). Envelope `code` and systemd `Result` disagreed. Both belong in the seal; neither may be silently preferred.
- Round 5 carried the retry as debt, not as a partial claim (`SCORECARD.md:1018-1020`). The counting lesson is the same defect class: count the artifact, not the intent (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:13-14,21-24`; `SCORECARD.md:976-977`). A 7200000 ms knob is intent. 7.554 s is the process fact. Neither is the claim.
- The dispatch text's "verifies on a typed terminal state … either way" is wider than `SCORECARD.md:802-804`. A typed instrument-abort is a sealed process fact. It is not HELD and not the wall's honest-negative.

One-batched dispatch is not the violation. `PROTOCOL.md:97-98` constrains L2 seat dispatch, not a parent host unit. The attack is claim accounting, not dispatch shape.

## Labels

- **Observation:** unit failed, `Result=exit-code`, `ExecMainStatus=1`, wall 7.554s, peak 2208227328 under cap 9663676416, `NRestarts=0`, `Restart=no`, `InvocationID=31dc1c7f0a5e4f9db082dfc9da37b90d`, envelope frozen at 16692 bytes / sha256 `4a3ebb82…`, no `evidence_id`, no `analyzer_preset`, unknown-analyzer abort at `ReaGhidraAnalysisOptions.java:22`, target hash matches the 91662336-byte PE, custody 5/5, one registry packument revalidation, a different live JVM under `arc2-l6r6-E9-mid`.
- **Inference:** the pattern confuses a process vehicle with a claim. Caller-independence lets a unit outlive the parent turn and the round; without an InvocationID-bound seal at close, a later round can harvest the unit name (restart-laundering: `Type=simple`, a second `systemd-run --unit=arc2-r6-pe` replaces `InvocationID`). "Either way" would count this abort as verifying the scale-wall. It must not. Post-pair taken while a service is still active does not cover that process's remaining life; this instance was already terminal before the 5/5 recheck, so that hole is not instantiated here.
- **Unknown:** the 17.7MB mid-rung (out of seat; the E9 JVM was not inspected). Whether a corrected analyzer name would pass on this binary (not tested). Whether the parent restarts the unit after this report (`NRestarts=0` now). Whether `/var/tmp` still holds the envelope at commit time — if not, an uncommitted hash is not closure evidence (`PROTOCOL.md:341-343`).

## Verbatim-landable

```text
Service-launch line (process vs claim). A parent-launched user service is a process, never a claim. Count the sealed terminal, not the launch intent (corpus/lessons/2026-10-18-wave-dispatch-counting.md:21). A steered round may claim only a terminal sealed into that round's receipts before close (PROTOCOL.md:86-87, :341-343). Required seal: unit name, InvocationID, ExecMainStartTimestamp, ExecMainExitTimestamp, Result, ExecMainStatus, wall duration, MemoryPeak, MemoryMax, envelope byte size, envelope sha256, and one pre-accepted branch label. Branches: HELD (evidence_id and analyzer_preset present); honest-negative-of-the-wall (typed refusal or contained kill after analysis started — provider_timeout, CONSTRAINT_MEMCG/oom-kill, or cancelled at the REA deadline); instrument-abort (pre-analysis failure: unknown analyzer, resolution, import abort) — sealed as a process fact, does not verify the scale-wall claim either way (SCORECARD.md:802-804). In-flight at close = not verified; do not carry the live unit as partial credit. A later round may adopt the same InvocationID only as an audit under its own round number, or launch a new InvocationID. Citing only the unit name is restart-laundering. Envelope code alone is not Result (r4 mislabeled OOM as cancelled, SCORECARD.md:898). Hash the bytes; the filename stdout.json is not a format claim. Post-pair custody is taken after the unit is terminal.

Round-6 instance: arc2-r6-pe InvocationID 31dc1c7f0a5e4f9db082dfc9da37b90d is instrument-abort, not the wall. Result=exit-code, ExecMainStatus=1, wall 7.554s, MemoryPeak=2208227328 (cap 9663676416), envelope sha256 4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7, 16692 bytes, no evidence_id, no analyzer_preset, code execution_failure, retryable false, unknown analyzer "Decompiler Parallel Convention Analysis" (ReaGhidraAnalysisOptions.java:22). Big-leg C1 does not verify on this terminal. Denominator stays 79 for this leg. Residue for the parent, not a seat: systemctl --user reset-failed arc2-r6-pe.service.
```
