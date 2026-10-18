# SC1 (scout) — host census: the round's background PE run is dead — OOM-killed at its own 7 GiB cap

Wave arc2-loop1-round4 · Seat SC1 · 2026-10-18, census window 19:04:30Z–19:11:13Z (UTC; host journal prints local −03, UTC = local + 3h) · read-only; only write is this report · HEAD `1692acbe48ce0eac3b7c87698be59d04a46a08` (`git status --porcelain` → `?? .ufo/waves/arc2-loop1-round4/…` only). No secret values printed — sizes, counts, digests, line numbers only. No scratch created. No process was touched, signalled, or reniced.

## Verdict

**RUN IS DEAD — the "live" PE analyze was memcg-OOM-killed at 19:07:45Z, 4m42.603s into its 2h deadline (3.9%), with `MemoryPeak` exactly equal to `MemoryMax` (7 GiB).** Conformance: the cap held — the host was never globally OOM'd; the kernel killed the contained JVM (java pid 4181543) via `CONSTRAINT_MEMCG`, and the scope's own swap cap (1 GiB) was also pegged. Host MemAvailable during coexistence 6.9–9.6 GiB (floor 6926 MiB @19:05:36Z), load1 9.9–12.8; post-kill it recovered to 10.7–14.0 GiB / load1 6.50. JVM count 1 during (java + 10 native `decompile` children), 0 now. The 7.0 GiB was consumed by java 3.20 GiB anon + ten decompile children 3.60 GiB anon + node/npm 0.14 GiB; `-Xmx6G` never bound. No relief is needed now (the kill released everything), but a restart must not reuse `MemoryMax=7G`: either ≥12 GiB — with the trade-off that the host had only ~7.5 GiB MemAvailable at the kill moment — or a smaller workload (fewer decompile workers).

## Evidence — exact commands run THIS session, with observed output

### 1. Scope identity, conformance, runtime

```
$ systemctl --user show run-p4175743-i29293759.scope -p MemoryMax -p MemoryHigh -p MemoryCurrent -p MemoryPeak -p MemorySwapMax -p CPUUsageNSec -p TasksCurrent -p TasksMax -p Description -p ActiveEnterTimestamp
Description=arc2-pe-wall
ActiveEnterTimestamp=Sun 2026-10-18 16:03:02 -03
MemoryCurrent=6361624576      # 19:04:30Z: 5.93 GiB = 84.7% of cap already
MemoryPeak=6552682496         # then; final peak below
MemoryHigh=infinity
MemoryMax=7516192768          # = 7 GiB exactly
MemorySwapMax=1073741824      # = 1 GiB
TasksCurrent=69 ; TasksMax=36852
```

Final state (read after the cgroup disappeared from `/sys/fs/cgroup/…/app.slice/`):

```
$ systemctl --user show run-p4175743-i29293759.scope -p ActiveState -p SubState -p Result -p ExecMainStatus -p ActiveExitTimestamp -p MemoryPeak -p RuntimeMaxUSec
ActiveState=failed  SubState=failed  Result=oom-kill
ActiveExitTimestamp=Sun 2026-10-18 16:07:45 -03
MemoryPeak=7516192768         # peak == max, exactly
RuntimeMaxUSec=infinity       # the 2h deadline was the wrapper's, not systemd's

$ journalctl --user -u run-p4175743-i29293759.scope --no-pager -o short-iso
2026-10-18T16:03:02-03:00 plazir27 systemd[1539]: Started arc2-pe-wall.
2026-10-18T16:07:45-03:00 plazir27 systemd[1539]: run-p4175743-i29293759.scope: The kernel OOM killer killed some processes in this unit.
2026-10-18T16:07:45-03:00 plazir27 systemd[1539]: run-p4175743-i29293759.scope: Failed with result 'oom-kill'.
2026-10-18T16:07:45-03:00 plazir27 systemd[1539]: run-p4175743-i29293759.scope: Consumed 9min 2.497s CPU time over 4min 42.603s wall clock time, 7G memory peak, 1G memory swap peak.
```

Runtime **4m42.603s** vs the 2h deadline = **3.9%**; CPU 9m02.497s over 4m42.6s wall ≈ 1.92 cores average. Wrapper record: `$ cat /var/tmp/arc2-l4r4-pe/exit.txt` → `exit=1 wall_utc=2026-10-18T19:07:45Z` (37 B, mtime 19:07:45.424Z).

### 2. The kill: kernel evidence and the 7.0 GiB decomposition

```
$ journalctl -k --since "2026-10-18 16:07:40" --until "2026-10-18 16:07:50" --no-pager
... decompile invoked oom-killer: gfp_mask=0x100cca(GFP_HIGHUSER_MOVABLE), order=0, oom_score_adj=200
... Memory cgroup stats for /user.slice/user-1000.slice/user@1000.service/app.slice/run-p4175743-i29293759.scope:
... anon 7454068736          # 6.94 GiB anon in the cgroup at kill
... oom-kill:constraint=CONSTRAINT_MEMCG,...,oom_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/run-p4175743-i29293759.scope,task_memcg=…,task=java,pid=4181543,uid=1000
... Memory cgroup out of memory: Killed process 4181543 (java) total-vm:10168632kB, anon-rss:3353140kB, file-rss:5684kB, shmem-rss:16kB, UID:1000 pgtables:8856kB oom_score_adj:200
```

The kernel's own per-task table at kill (pages → GiB):

| task | rss_anon | rss total |
|---|---|---|
| java (4181543) | 838285 p = 3.20 GiB | 3.28 GiB |
| 10 × `decompile` (pids 1776990–1786937) | 945027 p = 3.60 GiB | 3.64 GiB |
| node-MainThread (4177041) | 31250 p = 122 MiB | 137 MiB |
| npm exec (4175743) | 5279 p = 21 MiB | 34 MiB |

→ java 46%, decompile children 52%, node/npm 2% of the 7.0 GiB. **The 6 GiB heap never bound** (java RSS was 3.2–3.6 GiB all session); the native decompile worker pool did. `memory.events` inside the scope (read at 19:04:30Z): `low 0 / high 0 / max 0 / oom 0` — no prior throttling, straight to max.

### 3. Trend during coexistence (my samples, exact)

Scope `memory.current` (MiB) vs host, every 7 s (javaRSS = VmRSS of pid 4181543; dec = `pgrep -c decompile`):

```
19:06:24 scope=3358 avail=7717 swapFree=24844 load=12.52 javaRSS=2604 dec=0
19:06:38 scope=2956 avail=7514 swapFree=24793 load=12.20 javaRSS=2605 dec=0
19:06:52 scope=3900 avail=7976 swapFree=24841 load=11.03 javaRSS=3057 dec=0
19:07:06 scope=4163 avail=8570 swapFree=23910 load=10.06 javaRSS=3249 dec=0
19:07:20 scope=4375 avail=8289 swapFree=23952 load=10.12 javaRSS=3414 dec=7
19:07:27 scope=6526 avail=7676 swapFree=22620 load=10.59 javaRSS=3408 dec=10
19:07:41 scope=7145 avail=7946 swapFree=21593 load=11.73 javaRSS=3409 dec=10
19:07:45 OOM: peak 7168 MiB == cap
```

Peak slope 19:07:20→19:07:27: **+2151 MiB in 7 s (307 MiB/s)**, coincident with the decompile respawn burst 0→10 (kernel OOM was invoked by `decompile`). Earlier the same pattern ran once and survived: within 88 s of start (19:04:30Z) the scope was at 5.93 GiB/85% with the *first* decompile generation (10 workers, 1.73 GiB RSS) + java 3.50 GiB; that generation exited and current fell to 3.28 GiB by 19:06:24 — the second burst is what tipped it.

Host during coexistence: MemAvailable 6.9–9.6 GiB (floor 6926 MiB @19:05:36Z), load1 9.9–12.8 (peak 12.80 @19:06:07), swap used 10.2→13.5 GiB, `MemFree` 267–633 MB (vmstat), heavy swap-in (`si` up to ~123 MB/s), PSI mem avg10 ≤ 0.26. After the kill: MemAvailable 13688→13269 MiB (19:08:35–19:09:00Z), 10665 MiB @19:11:13Z; load1 7.49→6.50; swap used down to 9.0 GiB.

### 4. Post-kill state (19:11:13Z)

`pgrep -a java` → none (rc=1); `pgrep -c decompile` → 0; no `node-MainThread`/`rea` processes; scope cgroup removed from `/sys/fs/cgroup/…/app.slice/`; unit shows failed/failed; `systemctl --user list-units 'run-p*.scope' --all` → only the dead unit. `free -m`: available 10665 MiB, swap used 9036 MiB. `/tmp` tmpfs 12G/16G (77%), inode use 58%; `/var/tmp` is btrfs root disk (929.5G, 772.5G avail) — the round's TMPDIR choice was disk-backed, so round-3's scratch-in-RAM hazard (SC1 r3 §8) was correctly avoided.

### 5. Collateral context (observed, not mine to act on)

- Host OOM history today (`journalctl -k --since today`): global OOM 14:46:17 local = **17:46:17Z** (`CONSTRAINT_NONE`, killed systemd-coredump); sibling memcg OOM 15:06:07 local = **18:06:07Z** (python3, scope run-p2866091-…); this one 16:07:45 local = **19:07:45Z**. `user@1000.service` memory.events: `oom 2 / oom_kill 2`, `max 5424`, `sock_throttled 66135`.
- PID churn: `/proc/loadavg` last-PID 576421 @19:04:30Z → 2155874 @19:08:35Z → 2592755 @19:11:13Z (~2.7–6.4k PIDs/s; `pid_max=4194304`, so the counter wrapped between the scope's start and 19:04 — which is why the OOM table's decompile pids read lower than java's).
- 6 godot SIGABRT coredumps recorded since 16:03 local (`coredumpctl list`); thermal Tctl 82.6 °C / Tccd1 86.8 °C @19:09Z; nproc 32, Ryzen 9 9950X.

### 6. REA error-taxonomy defect (instrument note)

The OOM kill surfaced to REA as a *cancellation*, not a failure — `/var/tmp/arc2-l4r4-pe/stdout.json` (20093 B, mtime 19:07:45.363Z):

```
error: Analysis failed
code: cancelled
category: cancelled
message: Analysis was cancelled. Start it again when ready.
retryable: true
...
failure_kind: cancelled
failure_message: Ghidra startup was cancelled
```

Anyone reading only REA's stdout would conclude the run was deliberately cancelled. The true cause (memcg OOM kill) exists only in systemd/dmesg. **Observation**; **inference**: a future instrument should capture `systemctl show -p Result` (or the wrapper's exit reason) rather than trusting REA's `code:`.

### 7. Pre-pair receipt — verified 5/5 OK

```
$ tail -n +2 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
```

Timestamp line 2026-10-18T19:03:02Z; 5 hash lines, 5/5 OK at 19:08Z.

## Text for the parent to land VERBATIM (fenced)

```text
SC1 host census (arc2-loop1-round4, read-only, 2026-10-18T19:04:30–19:11:13Z): THE BACKGROUND PE RUN IS DEAD. Scope run-p4175743-i29293759.scope ("arc2-pe-wall") reached Result=oom-kill / ActiveState=failed at 19:07:45Z after 4m42.603s wall (3.9% of the 2h deadline), CPU 9m02.497s, killed by kernel CONSTRAINT_MEMCG OOM (dmesg: "Memory cgroup out of memory: Killed process 4181543 (java) ... oom_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/run-p4175743-i29293759.scope"). MemoryMax=7516192768 B (7 GiB) and MemoryPeak=7516192768 B — peak == max exactly, cap fully consumed; MemorySwapMax=1 GiB also pegged ("1G memory swap peak"). Decomposition of the 7.0 GiB at kill: 10 decompile children 3.60 GiB anon (52%), java 3.20 GiB anon (46%; its -Xmx6G never bound), node+npm 0.14 GiB (2%). Final ramp: cgroup memory.current 4.27->6.98 GiB in 21 s (peak slope 307 MiB/s at 19:07:20->19:07:27) coincident with a decompile-worker respawn burst 0->10; the kernel OOM was invoked by "decompile". Host during coexistence: MemAvailable 6.9–9.6 GiB (floor 6926 MiB @19:05:36Z), load1 9.9–12.8, swap used 10.2->13.5 GiB, MemFree 267–633 MB, heavy swap-in (~123 MB/s). Containment held: NO host-wide OOM — the 7 GiB cgroup cap took the kill. Post-kill 19:08:35–19:11:13Z: MemAvailable recovered to 10.7–14.0 GiB, load1 6.50, swap used 9.0 GiB. JVM count: 1 during (java pid 4181543 + 10 native decompile procs), 0 now; no rea/java/node-MainThread processes remain; scope cgroup removed. Host OOM history today: global OOM 17:46:17Z (killed systemd-coredump), sibling memcg OOM 18:06:07Z (python3), this one 19:07:45Z; user@1000.service memory.events oom 2 / oom_kill 2. REA surfaced the kill as code: cancelled / "Ghidra startup was cancelled" (stdout.json 20093 B) — the OOM cause is invisible in REA's error taxonomy; wrapper exit.txt = "exit=1 wall_utc=2026-10-18T19:07:45Z". RELIEF: none needed now (the kill released everything). For any restart: do NOT reuse MemoryMax=7G — observed need was 7.0 GiB at 4m42s and still climbing, so cap >=12 GiB (optionally MemoryHigh=10G to throttle instead of kill, MemorySwapMax 2–4G), BUT note the host had only ~7.5 GiB MemAvailable at the kill moment, so a larger cap draws the host toward a global OOM — alternatively reduce Ghidra decompile-worker parallelism (the 52% consumer; knob name not verified this session). Keep the systemd scope (it demonstrably prevented a global OOM) and keep TMPDIR on disk (/var/tmp/arc2-l4r4-pe is btrfs, 772.5G free — correct; /tmp is tmpfs 77–84% full, 3.1–3.6G free, avoid for scratch). Pre-pair receipt verified 5/5 OK (sha256sum -c rc=0).
```

## Conclusions by label

- **Observation** — (a) scope `run-p4175743-i29293759.scope`, started 19:03:02Z, failed with `Result=oom-kill` at 19:07:45Z after 4m42.603s wall / 9m02.497s CPU (§1); (b) `MemoryMax` = `MemoryPeak` = 7516192768 B exactly, `MemorySwapMax` 1 GiB pegged (§1); (c) kernel `CONSTRAINT_MEMCG` OOM killed java pid 4181543; cgroup anon 7.45 GB; per-task table gives java 3.20 GiB / 10× decompile 3.60 GiB / node+npm 0.14 GiB (§2); (d) scope `memory.current` 4.27→6.98 GiB in 21 s, decompile 0→10 in the same window, `decompile` invoked the oom-killer (§2–3); (e) host MemAvailable 6.9–9.6 GiB and load1 9.9–12.8 during, 10.7–14.0 GiB and 6.50 after (§3–4); (f) JVM count 1 during / 0 after; no orphaned processes (§4); (g) REA reported `code: cancelled` / "Ghidra startup was cancelled"; wrapper `exit=1 wall_utc=2026-10-18T19:07:45Z` (§6); (h) receipt 5/5 OK (§7); (i) three OOM events on this host today, one global (§5); (j) `/tmp` tmpfs 77–84% full, `/var/tmp` on btrfs 772.5G free (§4).
- **Inference** — the 7 GiB cap, not the analysis itself, ended the run: the workload was at 7.0 GiB and climbing at 4m42s, so it cannot fit a 7 GiB cgroup, and a restart needs a larger cap or a smaller worker pool; the binding consumer is the decompile worker pool, not the `-Xmx6G` heap, so heap tuning is not the fix; raising the cap trades the contained kill for a much closer approach to a global OOM (host floor 6.9 GiB MemAvailable) unless the workload shrinks or sibling waves subside; REA's `cancelled` taxonomy will mislabel any future OOM kill as a user cancellation.
- **Unknown** — the Ghidra decompile-parallelism knob name/mechanism (not verified this session); whether a ≥12 GiB cap would let the 91.6 MB PE analyze finish inside 2h (only 4m42s of progress observed, no completion baseline); the steady-state footprint the run would have reached; which sibling workload drives the ~2.7–6.4k PIDs/s churn and the godot SIGABRT coredumps; whether the parent intends to restart the PE leg at all this round.

## Scope compliance

Read-only everywhere; the only write is this report. No repo file edited, no git mutation, no config edit, no install, no network fetch, no scratch directory created. The PE run was never killed, reniced, or touched by me — it died by kernel memcg OOM at 19:07:45Z, before any of my samples after that instant, and all my reads were passive (`systemctl show`, `/proc`, `journalctl`, `free`, `ps`). No other seat's files were read or touched. Secret hygiene: only sizes, counts, digests, line numbers and key names appear above. Per AGENTS.md, the parent should land a LOG.md entry from the verbatim block; I did not touch LOG.md (hard scope).
