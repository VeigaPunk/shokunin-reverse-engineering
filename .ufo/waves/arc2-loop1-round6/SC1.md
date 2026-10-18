# SC1 — host census of `arc2-r6-pe` (independent of E1)

Seat SC1, wave arc2-loop1-round6. Samples 2026-10-18T17:44:02-03:00, 17:45:33, 17:46:45, 17:48:04 (`date -Is`). Only write: this file. Read-only elsewhere. No signal, kill, restart. No git mutation. Scratch unused (`/tmp` quota-full; no `/var/tmp/arc2-l6r6-SC1-*` created).

Custody not in scope. E1.md was absent at 17:45:33 and present (9199 B, mtime 17:46) when rechecked; core unit counters below were taken before that read. Later `OOMKills` / kernel-window queries are confirmatory re-runs, not copies.

## 1. Verdict

**CORROBORATES E1 — TERMINAL ANALYZER-NAME REFUSAL, NOT A MEMORY WALL, NOT IN-FLIGHT.** `arc2-r6-pe` was already `failed` / `exit-code` / `ExecMainStatus=1` at first sample. Wall 7.554 s (17:40:58 → 17:41:06 -03). `MemoryPeak=2208227328` (2.0566 GiB, 22.8508% of `MemoryMax=9663676416` = 9 GiB). Headroom 7,455,449,088 B. `MemorySwapPeak=0`. `OOMKills=0`. `CPUUsageNSec=13930953000` (13.931 s). Cgroup directory gone. Decompile workers: **0** (pre-script abort) vs round-4's **10** (`.ufo/waves/arc2-loop1-round4/E19.md:165`, `.ufo/reports/arc2-loop1-round4/kaidoku.md:44`). C1 big leg is a typed terminal refusal, not a hold and not an in-flight close.

## 2. Evidence

### 2.1 Service cgroup (sealed accounting; live cgroup absent)

```sh
systemctl --user show arc2-r6-pe.service -p ActiveState -p SubState -p Result -p ExecMainStatus -p ExecMainPID -p MainPID -p NRestarts -p InvocationID -p MemoryPeak -p MemoryMax -p MemorySwapPeak -p OOMKills -p CPUUsageNSec -p ControlGroup -p TasksCurrent -p MemoryCurrent
systemctl --user status arc2-r6-pe.service --no-pager -l
systemctl --user cat arc2-r6-pe.service
find /sys/fs/cgroup -maxdepth 8 -type d -name 'arc2-r6-pe.service'
```

Observed, stable 17:44:02 through 17:48:04:

```text
ActiveState=failed SubState=failed Result=exit-code ExecMainStatus=1
ExecMainPID=1992927 MainPID=0 NRestarts=0
InvocationID=31dc1c7f0a5e4f9db082dfc9da37b90d
ControlGroup=          # empty; find returned no directory
MemoryCurrent=[not set] TasksCurrent=[not set]
MemoryPeak=2208227328 MemoryMax=9663676416 MemorySwapPeak=0 OOMKills=0
CPUUsageNSec=13930953000
```

Status excerpt (17:44:02): `Duration: 7.554s`, `Mem peak: 2G`, `CPU: 13.930s`, `Process: 1992927 ExecStart=…/npx -y rea-agents@6.5.0 analyze …/windows_release_arm64.exe (code=exited, status=1/FAILURE)`. Journal (4 lines only):

```text
2026-10-18T17:40:58-03:00 Started [systemd-run] … npx -y rea-agents@6.5.0 analyze …/windows_release_arm64.exe.
2026-10-18T17:41:06-03:00 arc2-r6-pe.service: Main process exited, code=exited, status=1/FAILURE
2026-10-18T17:41:06-03:00 arc2-r6-pe.service: Failed with result 'exit-code'.
2026-10-18T17:41:06-03:00 arc2-r6-pe.service: Consumed 13.930s CPU time over 7.554s wall clock time, 2G memory peak.
```

Verbose journal `_SOURCE_REALTIME_TIMESTAMP` 1792356058992859 → 1792356066546922 = 7,554,063 µs. Transient unit `/run/user/1000/systemd/transient/arc2-r6-pe.service`: `MemoryMax=9663676416`, `MemorySwapMax=1073741824`, `OOMScoreAdjust=200`, `OOMPolicy=stop`, `StandardOutput=file:/var/tmp/arc2-l6r6-pe/stdout.json`, `StandardError=file:/var/tmp/arc2-l6r6-pe/stderr.log`. Environment matches the brief, including `REA_GHIDRA_DISABLED_ANALYZERS=Decompiler Parameter ID,Decompiler Switch Analysis,Decompiler Parallel Convention Analysis`, `GHIDRA_HEADLESS_MAXMEM=6G`, `TMPDIR=/var/tmp/arc2-l6r6-pe`.

`MemoryAvailable` is **not** sealed: 9252810752 at 17:48:04 (E1's earlier samples were lower and already moving). `9*1024**3 == 9663676416`. Peak/cap = 0.228508.

Kernel window, independent of E1's cutoff:

```sh
journalctl -k --since '2026-10-18 17:40:00' --until '2026-10-18 17:47:00' --no-pager | grep -E -i 'oom|Killed process|out of memory'
# NO_OOM_LINES
```

### 2.2 Host memory / load (32 CPUs; unit already dead)

| sample | loadavg | MemAvailable kB | MemFree kB | SwapFree kB | Committed_AS kB | CommitLimit kB |
|---|---|---:|---:|---:|---:|---:|
| 17:44:02 | 10.11 8.02 8.77 | 19140720 | 775596 | 17534740 | 52032124 | 51778072 |
| 17:45:33 | 17.75 11.32 9.89 | 15081796 | 407176 | 17994828 | 58421588 | 51778072 |
| 17:46:45 | 19.12 13.02 10.58 | 12474008 | 295708 | 16829668 | 59429576 | (not re-read) |
| 17:48:04 | 24.00 16.45 12.02 | 11735628 | 1877908 | 14775504 | 60213604 | 51778072 |

`MemTotal=31721792 kB`. PSI at 17:48:04: cpu some avg10=3.09 full=0; memory some avg10=0.09 full=0.07; io some avg10=0.13 full=0.04. At 17:44:02 memory full avg10 was 0.50. Committed_AS exceeded CommitLimit at every sample. That pressure is host-wide and **after** this unit exited; the dead cgroup cannot be the source (peak 2.06 GiB, swap peak 0, no live procs).

### 2.3 JVM / decompile decomposition

Target (read-only `stat` + `sha256sum`): `/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe` = **91662336** B, sha256 `7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292` (matches `stdout.json:13`).

Envelope `/var/tmp/arc2-l6r6-pe/stdout.json`: 16692 B, sha256 `4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7`, mtime 17:41:06.513 -03. `stderr.log` is 0 B (mtime 17:40:59). `du -sb` = 1429008 (1.363 MiB apparent); `du -sh` = 2.6M (allocated). `find -type f` = 537, `find -type d` = 3. No `rea-ghidra-f5rC3Z/` left.

Phase order inside the envelope (embedded Ghidra stdout, `stdout.json:31`):

- Class search complete (507 ms); Headless startup complete (1179 ms).
- IMPORT of staged `target-7a2ccd688f6c.exe`; loader Portable Executable (PE); language `AARCH64:LE:64:v8A:windows`.
- Pre-script `ReaGhidraAnalysisOptions.java` argv is the three disabled-analyzer names.
- `IllegalArgumentException: Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis` at `ReaGhidraAnalysisOptions.java:22` (throw is `ReaGhidraAnalysisOptions.java:21-22`; stack in `stdout.json:31`).
- `Processing aborted as a result of pre-script.` Import then discarded (`readOnly`). No `ANALYZING` line. The only `Decompil*` hits are script-path names plus that exception — not decompiler tasks.
- Child `process_id: 1993398` (`stdout.json:23`) `exit_code: 0` (`stdout.json:27`); envelope `failure_kind: process` / `failure_message: Ghidra exited before bridge startup` (`stdout.json:38-39`); `retryable: false` (`stdout.json:5`); `code: execution_failure` (`stdout.json:2`). npx main 1992927 exited 1. Captured JVM banner (`stdout.json:35`): OpenJDK 21.0.12.1, 64-Bit Server VM.

`pgrep -c -x java` was 0 at 17:45:33. At 17:48:04 one JVM existed and is **not** this unit: pid 2280341, etime 03:23, RSS 1700576 kB, `-Xmx6G`, `AnalyzeHeadless` under `/var/tmp/arc2-l6r6-E9-mid/` (E9 mid-rung). `arc2-r6-pe` `MainPID=0`, `ControlGroup` empty, `NRestarts=0`. Do not fold that RSS into this cgroup.

Round-4 baseline, re-read not rewritten: E19.md:165 `10 × decompile workers | 954,961 combined rss pages | 3.643 GiB`; kaidoku.md:44 `memory wall identified: 10 decompile workers + JVM`. This run: **0 vs 10**.

## 3. Verbatim-landable

```text
SC1 host census (independent of E1; samples 17:44:02–17:48:04 -03): arc2-r6-pe was already terminal. ActiveState=failed, Result=exit-code, ExecMainStatus=1, ExecMainPID=1992927, InvocationID=31dc1c7f0a5e4f9db082dfc9da37b90d, NRestarts=0. Wall 7.554 s (17:40:58→17:41:06 -03; journal delta 7,554,063 µs). MemoryPeak=2208227328 B = 2.0566 GiB = 22.8508% of MemoryMax=9663676416 (exactly 9 GiB); headroom 7455449088 B; MemorySwapPeak=0; OOMKills=0; CPUUsageNSec=13930953000. ControlGroup empty (cgroup dir gone). Kernel 17:40–17:47 -03: no oom/Killed-process line. Target 91662336 B sha256 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292. stdout.json 16692 B sha256 4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7. JVM imported the PE (AARCH64:LE:64:v8A:windows) then aborted in pre-script ReaGhidraAnalysisOptions.java:22 — Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis — before auto-analysis. Decompile workers 0 vs round-4's 10 (E19.md:165, kaidoku.md:44). Ghidra child 1993398 exit_code 0; npx 1992927 exit 1; failure_message=Ghidra exited before bridge startup; retryable=false. The 9G cap was not the binding constraint. Not in-flight. Host load rose 10.11→24.00 after the unit died (32 CPUs); Committed_AS > CommitLimit is host-wide, not this cgroup. A later JVM (pid 2280341) is E9's mid-rung under /var/tmp/arc2-l6r6-E9-mid, not arc2-r6-pe.
```

## 4. Labels

- **Observation:** unit counters above are byte-stable across four samples; cgroup dir absent; stdout.json names the unknown analyzer and contains no analysis/decompile phase; kernel window has no OOM line; host MemAvailable and load moved after exit; the only live `java` at 17:48:04 is E9's mid-rung.
- **Inference:** agrees with E1. Binding constraint was the third disabled-analyzer name on this program, not MemoryMax and not the 7,200,000 ms startup timeout. Round-4's 10-worker set was never spawned, which is why peak stayed at 2.0566 GiB. C1's big leg is a typed refusal, not a scale-wall hold.
- **Unknown:** whether dropping or renaming `Decompiler Parallel Convention Analysis` would start analysis and then pressure the 9G cap. This seat did not re-run the service. Host overcommit's other owners were not attributed.
