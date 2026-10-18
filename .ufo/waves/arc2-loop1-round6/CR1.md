# CR1 — C1: third attempt at the same wall — persistence or sunk-cost?

**Verdict: SUNK-COST. Stop the 91.6MB binary as the owned coverage claim. Land the honest-negative. Do not re-dispatch this configuration.**

The research chain was persistence (time → outer cap → memory → disable analyzers). This execution is not. It died in 7.554s on an analyzer name that does not exist in Ghidra 12.1.4, before analysis, before `analyzer_preset`, before the memory wall. The round-4 prescription's other half (worker reduction) is absent from the unit. Prior hours on this file are what put it back on the claim, not evidence that this env would clear the wall. That is the sunk-cost test. The service is already terminal — the dispatch brief's "in-flight" clause does not apply. Do not wait. Do not treat a name error as a scale result.

Stopping the big leg must not cancel the 17.7MB mid-rung. That rung is still the unrun information between the held 2.5MB bisect and this unheld file.

## Axes

- **Mechanism novelty:** did this run change the constraint the last failure named?
- **Information per claim-slot:** what new fact about the wall did the run buy?
- **Stop-value:** does stopping improve the record without killing a live hypothesis?
- **Harm-none:** does the stop spare the mid-rung and any run that is actually testing a new mechanism?

Stop improves the first three and harms none: the unit is already dead, and the new mechanism never started.

## Evidence

Observed 2026-10-18T20:45:40Z. HEAD `54bc9dd`. Custody pre-pair **5/5 OK, rc 0** (`sha256sum -c` on `.ufo/waves/arc2-loop1-round6/receipts/config-pre-pair.txt`). No signal sent. Only `arc2-*` unit: `arc2-r6-pe` `loaded failed failed`.

### This attempt — terminal refusal, wall untested

```console
$ systemctl --user show arc2-r6-pe -p ActiveState -p SubState -p Result -p ExecMainStatus -p NRestarts -p MemoryPeak -p MemoryMax -p ExecMainStartTimestamp -p ExecMainExitTimestamp
ActiveState=failed
SubState=failed
Result=exit-code
ExecMainStatus=1
NRestarts=0
MemoryPeak=2208227328
MemoryMax=9663676416
ExecMainStartTimestamp=Sun 2026-10-18 17:40:58 -03
ExecMainExitTimestamp=Sun 2026-10-18 17:41:06 -03
$ journalctl --user -u arc2-r6-pe --no-pager -o short-iso
2026-10-18T17:41:06-03:00 ... Consumed 13.930s CPU time over 7.554s wall clock time, 2G memory peak.
$ systemctl --user show arc2-r6-pe -p Environment
Environment="REA_GHIDRA_DISABLED_ANALYZERS=Decompiler Parameter ID,Decompiler Switch Analysis,Decompiler Parallel Convention Analysis" REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000 GHIDRA_HEADLESS_MAXMEM=6G TMPDIR=/var/tmp/arc2-l6r6-pe GHIDRA_INSTALL_DIR=... JAVA_HOME=...
$ stat -c '%s %y' /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe /var/tmp/arc2-l6r6-pe/stdout.json
91662336 2026-10-11 16:17:46.129033608 -0300
16692 2026-10-18 17:41:06.513410314 -0300
$ sha256sum <target> /var/tmp/arc2-l6r6-pe/stdout.json
7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292
4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7
```

Envelope (`/var/tmp/arc2-l6r6-pe/stdout.json`, not JSON — YAML-ish error doc): `:1-5` `error: Analysis failed` / `code: execution_failure` / `retryable: false` / "repeating the unchanged request is not expected to succeed." `:13` target sha matches. `:31` script argv is the full disabled list, then `Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis` at `ReaGhidraAnalysisOptions.java:22`, `Processing aborted as a result of pre-script.` `:38-39` `failure_kind: process` / `Ghidra exited before bridge startup`. String counts in the 16692 bytes: `analyzer_preset=0`, `evidence_id=0`, `preset=0`.

The throw is unconditional on the first unknown name (`ReaGhidraAnalysisOptions.java:18-22`: `getAnalyzer(name) == null || !options.containsKey(name)`). So the two real names were never set false either.

Name check, read-only, 202 jars under `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`:

```text
Decompiler Parameter ID: 7 hits (incl. DecompilerFunctionAnalyzer.class)
Decompiler Switch Analysis: 1 hit (DecompilerSwitchAnalyzer.class)
Decompiler Parallel Convention Analysis: 0
Parallel Convention: 0
```

`git grep 'Decompiler Parallel Convention' HEAD` → `NO_COMMITTED_HIT`. The three-name list is not in the landed record. `analyzer_preset` is emitted only after the disabled list resolves (`GhidraAnalysisProfile.js:41-45` in the 6.5.0 cache `ad9a3fdbcad992c6`). Absence in the envelope is the expected consequence of the pre-script abort, not a missing log line.

Unit env keys: the five above. No worker-count variable. Round 4's landed next step was both halves: `SCORECARD.md:899-900` "next attempt carries the `REA_GHIDRA_DISABLED_ANALYZERS` lead with worker reduction"; same sentence `LOG.md:1146`. E12 named the env var as the untried footprint lever and did not name these three strings (`.ufo/waves/arc2-loop1-round4/E12.md:621-622`).

### The two prior arc attempts, same file

| # | Where | What was changed | Terminal state | Wall tested? |
|---|---|---|---|---|
| pre-window | r4-12 | default ~900s | `provider_timeout`, still progressing, RSS ~2.36GB, not OOM | time, yes |
| 1 | arc2 round 3 | timeout 3600000 + heap 8G | 30m01.228s, exit 124, typed `cancelled`, deadline untested | no — outer 1800s cap |
| 2 | arc2 round 4 | 7G cgroup, 7200s, disk TMPDIR | OOM at own cap, 4m42s, `CONSTRAINT_MEMCG` | memory, yes |
| 3 | this claim | 9G cap, heap 6G, 7200s, disabled-analyzer list, no worker knob | exit 1 in 7.554s, name error | no |

Pointers: `PROVINCE.md:139-144` (r4-12; its "Next:" is still "raise timeout + heap", which attempts 1–2 already did); `SKILL.md:65` and `SKILL.md:76` still prescribe that same raise; `SCORECARD.md:800-808` and `.ufo/reports/arc2-loop1-round3/kaidoku.md:75-77` (attempt 1; knowledge entry refused as a re-run dressed as a move; coverage stayed 79/79); `SCORECARD.md:894-900` and `.ufo/reports/arc2-loop1-round4/kaidoku.md:43-44` and `.ufo/waves/arc2-loop1-round4/E13.md:234-241` (attempt 2: 10 decompile children, binding wall memory not time). Last measured denominator: command A 79/79 at `3f4a685` (`SCORECARD.md:993`). Mid-rung still named unrun at `LOG.md:1114` and `SCORECARD.md:1020`.

## Steelman: stop

1. **The hypothesis was not tested.** Round 4 said the wall is memory and the next lever is disable-analyzers plus fewer workers. This unit applied a list Ghidra rejects, omitted worker reduction, and exited before auto-analysis. A 7.5s name error does not update the memory-wall posterior. Calling it the decisive retry repeats the move `SCORECARD.md:807-808` already refused.
2. **The tool refuses the identical retry.** `retryable: false` and "repeating the unchanged request is not expected to succeed" (`stdout.json:4-5`). A fourth run of this env is the request REA says not to repeat.
3. **The information to stop is already in hand.** Time wall measured (r4-12). Outer-cap confound measured (round 3). Memory wall measured (round 4, 4m42s, own 7G cap). This run adds only "this analyzer string is not in Ghidra 12.1.4." That fact was available from a jar scan, not a 91.6MB claim.
4. **Claim-slot cost inside 6/10.** Coverage has been 79/79 since the round-3 honest stop. Three arc rounds have now spent the big-PE question (inconclusive, infrastructure OOM, this refusal) without moving the denominator. Four rounds remain. Returning the owned axis to this file because the previous runs were expensive is the sunk-cost error. Persistence would be a *different* configuration, validated cheaply on a small PE (drop the phantom name, confirm the two real names disable, set a worker cap), and it would be infrastructure — not this claim's HELD branch — until that cheap check exists.
5. **The brief is stale.** "In-flight at close = big leg not verified" does not apply. `ActiveState=failed` since 17:41:06-03, observed 20:45:40Z, `NRestarts=0`. Waiting cannot produce an evidence bundle from this unit. The honest-negative verifies the typed-terminal clause. Do not hold the round open for it.
6. **What the stop must not take with it.** The 17.7MB agent-browser rung is carried debt, not this failure. The 2.5MB bisect already held (`SCORECARD.md:797-799`). The mid-rung is the measurement that can still move knowledge without another hour on a file whose binding constraint is already named. I saw no mid-rung unit — only the failed `arc2-r6-pe`.

Persistence steelman, and why it loses: each prior failure did change the constraint, and round 6's *plan* followed the landed next step. Credit the plan. Do not credit the execution. A plan whose first action is an unvalidated name, and whose co-equal lever is missing, is not a third measurement of the wall. It is a sunk claim slot.

## Verbatim-landable

```text
C1 big-leg adjudication (CR1, arc2-loop1-round6): SUNK-COST — stop. Do not re-dispatch arc2-r6-pe's configuration, and do not hold the round for it. The service is terminal failed (exit 1, 7.554s, Mem peak 2G of a 9G cap, NRestarts=0, 17:40:58–17:41:06-03), not in-flight. Envelope /var/tmp/arc2-l6r6-pe/stdout.json (16692 bytes, sha256 4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7) is execution_failure, retryable false, analyzer_preset absent, evidence_id absent. Ghidra aborted in the pre-script: Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis (ReaGhidraAnalysisOptions.java:22). That string has 0 hits in 202 jars of ghidra_12.1.4_PUBLIC and 0 hits in HEAD; the other two names exist but were never applied, because the script throws on the first unknown. The unit set no worker-reduction knob, so SCORECARD.md:899-900's prescribed next attempt (DISABLED_ANALYZERS plus worker reduction) did not run. This is the third arc attempt on windows_release_arm64.exe (91662336 bytes, sha256 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292) after round 3's outer-cap kill and round 4's 4m42s self-OOM; it did not reach the memory wall those runs already measured. Knowledge denominator stays 79 for this leg. Land the honest-negative. A later attempt is persistence only if it is a different configuration, name-validated on a small PE first, and not this claim's HELD branch. Do not cancel the 17.7MB mid-rung — it is still unrun (LOG.md:1114, SCORECARD.md:1020).
```

## Labels

- **Observation:** unit failed, 7.554s, peak 2G / max 9G, exit 1, NRestarts 0; envelope hash and absent keys; script error names `Decompiler Parallel Convention Analysis`; that string is absent from 202 Ghidra jars and from HEAD; unit env has no worker knob; custody 5/5 rc 0; only `arc2-*` unit is this failed service; target 91662336 bytes, sha256 `7a2ccd68…`.
- **Observation:** prior terminals are recorded at `PROVINCE.md:139-144`, `SCORECARD.md:800-808`, `SCORECARD.md:894-900`, round-3 report `:75-77`, round-4 report `:43-44`.
- **Inference:** the disabled-analyzer mechanism did not execute; this run adds no scale information; repeating this env is sunk-cost; the honest-negative verifies the big leg; the dispatch "in-flight" sentence was already false at 20:45:40Z.
- **Inference:** `SKILL.md:65` / `:76` and `PROVINCE.md:142-144` still tell the next reader to raise timeout and heap — the move attempts 1–2 already spent. Leaving that row unchanged invites attempt 4. (Draft only; this seat does not edit.)
- **Unknown:** who chose the three analyzer names. Not in HEAD.
- **Unknown:** whether a sibling seat's 17.7MB leg is running outside `arc2-*` systemd units. Not observed here.
- **Unknown:** whether dropping the phantom name and cutting decompile workers would fit under 9G. Unmeasured, and not a reason to keep this claim open.

## Scope

Only repo write: this file. No git mutation, no config edit, no install, no network, no signal to `arc2-r6-pe`. Scratch unused. Custody paths read as `sha256sum -c` only.
