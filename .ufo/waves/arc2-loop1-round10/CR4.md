# CR4 (critic) — the dual-service host load (two 9G caps + 64 seats)

Seat CR4, arc2-loop1-round10. HEAD `c561f00` (`git log --oneline -1`). This report
is this seat's only write; no repo file edited, no git mutation, no config edit, no
install, no network, and **neither live leg was signalled, stopped, or restarted**
(both were observed read-only and both reached terminal states on their own).
Scratch: `/var/tmp/arc2-l10r10-CR4-work/` only. Custody
`.ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt` re-verified **5/5 OK**
(5 hash lines, all `sha256sum` matches) — not required by this scope, run because
the file was already open.

## (1) Verdict

**The seat's premise does not survive contact with the journal, and it fails in
both directions at once.** "Two 9G caps + 64 seats" is not the operative resource,
and the one leg that died did not die of it.

**(a) The load is exculpated for the mid-leg failure — that kill is a spec error.**
`arc2-r10-mid` was killed by `oom-kill:constraint=CONSTRAINT_MEMCG` against **its
own** 9G limit (`memory: usage 9437184kB, limit 9437184kB`), with `anon 9567342592`
reached in **53.602 s**. The r6 recipe it re-ran held for 2479 s only because r6
ran **uncapped** — a plain `node … rea.mjs` process under `timeout(1)`, no
`MemoryMax` anywhere, measured `peak_tree_rss_kb=19149984` = **18.26 GiB** tree RSS.
The r10 rerun kept the r6 params and added the r7 envelope (9G cap + 1G swap cap).
No host state is needed to produce this death: the same envelope on an idle host
yields the same kill. Therefore the r10-mid OOM is **not** evidence about
`ev_8b688ce7…`, and it is **not** a host-load casualty. It is r6-recipe × r7-envelope.

**(b) The load is not exculpated at the host level — the budget never closed.**
Two 9 GiB caps are **59.5 %** of a 30.25 GiB host, and they are not the largest
consumer. `/tmp` is a **16 GiB tmpfs holding 13 GiB** with no size cap, ~all of it
swapped out (resident `Shmem` 4.76–5.25 MB across every one of 240 samples), and
only ~1.6 GiB of it is identifiably this project's. `app.slice` — the cgroup the
wave's services live in — has already recorded **`oom 5 oom_kill 4`** today, with
`memory.peak` **28.21 GiB**, and one of those OOM-kill notices fired at **20:52:36**,
**3 m 50 s before** `arc2-r10-big`'s JVM started (20:56:26). The wave ran on an
already-OOMing host. It got away with it; it did not fit.

**(c) The load's real cost was paid in swap, and it landed on the leg that
survived.** `arc2-r10-big` HELD — and not merely id-equal: its envelope is
**byte-identical** to r7's committed receipt (5204 B, sha256 `a77ebee8…`,
`evidence_id ev_a4aa9b0d…`), so **rerun id stability is CONFIRMED at the 91.6 MB
scale point**. The cost of the concurrent host was **769.1 M memory swap peak
against r7's 53.1 M — ×14.5** — for **+0.94 %** wall time. The cgroup's own
`memory.high=max` and `oom_kill 0` say that swap was driven by host-side global
reclaim, not by the leg's cap.

**Consequence for the round:** do not cite the big leg's hold as validation of the
dual-service plan (it held *despite* the plan, and paid ×14.5 swap), and do not cite
the mid leg's OOM as load-induced. Two unrelated causes were compressed into one
"host load" frame.

## (2) Evidence

All commands read-only. Legs were never signalled.

### 2.1 Big leg — terminal state, held

```text
$ systemctl --user show arc2-r10-big.service -p ActiveState -p SubState -p Result -p ExecMainStatus
ActiveState=inactive
SubState=dead
Result=success
ExecMainStatus=0
# (unit now unloaded: `systemctl --user status arc2-r10-big.service` -> "Unit … could not be found")
```

```text
$ journalctl --since "2026-10-18 21:00:00" --no-pager | grep arc2-r10-big
Oct 18 21:20:23 plazir27 systemd[1539]: arc2-r10-big.service: Consumed 42min 43.809s CPU time
  over 23min 58.082s wall clock time, 7.8G memory peak, 769.1M memory swap peak.
# no failure / OOM / Stopping line
```

```text
$ sha256sum /var/tmp/arc2-l10r10-big/stdout.json
a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a  /var/tmp/arc2-l10r10-big/stdout.json
$ sha256sum .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json
a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a  …/r7-pe-envelope.json
$ diff <(cat .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json) \
       <(cat /var/tmp/arc2-l10r10-big/stdout.json) && echo BYTE-IDENTICAL
BYTE-IDENTICAL
$ head -c 120 /var/tmp/arc2-l10r10-big/stdout.json
evidence_id: ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608
```

The r10 rerun reproduces r7's envelope **to the byte**, not merely to the id. r7's
side of the comparison: `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13`
(9G cap + 1G swap cap, wall 1424.663 s, "7.9G memory peak") and `:20`
(`ev_a4aa9b0d…`); swap figure `.ufo/waves/arc2-loop1-round7/CR3.md:101`
("23min 44.663s wall clock time, 7.9G memory peak, 53.1M memory swap peak").

Own cgroup sampler (`/var/tmp/arc2-l10r10-CR4-work/sample.sh`, 5 s cadence,
240 samples, 21:00–21:20, written to `load-samples.tsv`):

```text
$ cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/arc2-r10-big.service/memory.peak
8456077312                      # 7.874 GiB against the 9663676416 (9 GiB) limit
$ cat …/arc2-r10-big.service/memory.events
low 0
high 0
max 0                           # the cap was never hit
oom 0
oom_kill 0
oom_group_kill 0
```

Delta table (r7 → r10-big), same target, same recipe, same cap:

| metric | r7 (`arc2-r7-pe`) | r10-big | delta |
|---|---|---|---|
| wall | 1424.663 s | 1438.082 s | +13.419 s (**+0.94 %**) |
| CPU | 42 min 35.706 s | 42 min 43.809 s | +8.103 s (+0.32 %) |
| memory peak | 7.9 G | 7.8 G | −0.1 G |
| **swap peak** | **53.1 M** | **769.1 M** | **×14.5** |
| envelope | 5204 B `a77ebee8…` | 5204 B `a77ebee8…` | **identical** |

The ×14.5 swap was front-loaded: the cgroup's `memory.swap.peak` was already
`806506496` (769.1 MiB) at the first cgroup read (~21:00) and did not move again
(`memory.swap.current` 291 MB flat), i.e. it was incurred in the import/startup
phase while host `MemFree` sat at 267 MB–4 MB. `memory.high=max` means no
cgroup-side proactive reclaim was possible, so the reclaim was host-global.

### 2.2 Mid leg — terminal state, OOM-killed at its own cap

```text
$ journalctl --since "2026-10-18 20:56:00" --until "2026-10-18 20:58:00" --no-pager -k
Oct 18 20:57:18 plazir27 kernel: decompile invoked oom-killer: gfp_mask=0x100cca(GFP_HIGHUSER_MOVABLE), order=0, oom_score_adj=200
Oct 18 20:57:18 plazir27 kernel: mem_cgroup_out_of_memory+0xe1/0xf0
Oct 18 20:57:18 plazir27 kernel: memory: usage 9437184kB, limit 9437184kB, failcnt 206682
Oct 18 20:57:18 plazir27 kernel: swap: usage 1048436kB, limit 1048576kB, failcnt 8375
Oct 18 20:57:18 plazir27 kernel: Memory cgroup stats for /user.slice/…/app.slice/arc2-r10-mid.service:
Oct 18 20:57:18 plazir27 kernel: anon 9567342592
Oct 18 20:57:18 plazir27 kernel: file 1318912
Oct 18 20:57:18 plazir27 kernel: oom-kill:constraint=CONSTRAINT_MEMCG,nodemask=(null),cpuset=user.slice,
  mems_allowed=0,oom_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/arc2-r10-mid.service,
  task_memcg=…/arc2-r10-mid.service,task=java,pid=622553,uid=1000
Oct 18 20:57:18 plazir27 kernel: Memory cgroup out of memory: Killed process 622553 (java)
  total-vm:10093312kB, anon-rss:2367976kB, file-rss:22132kB, shmem-rss:16kB, UID:1000
Oct 18 20:57:18 plazir27 systemd[1539]: arc2-r10-mid.service: Main process exited, code=exited, status=1/FAILURE
Oct 18 20:57:18 plazir27 systemd[1539]: arc2-r10-mid.service: Failed with result 'oom-kill'.
Oct 18 20:57:18 plazir27 systemd[1539]: arc2-r10-mid.service: Consumed 4min 14.200s CPU time
  over 53.602s wall clock time, 9G memory peak, 1G memory swap peak.
```

The cgroup's own task table names the driver — ten `decompile` children on top of
the JVM:

```text
[  pid  ]   uid  tgid total_vm      rss rss_anon rss_file rss_shmem … name
[ 622319]  1000 622319   439969    14819      103    14716         0 … npm exec rea-ag
[ 622408]  1000 622408   461963    19045     4958    14087         0 … node-MainThread
[ 622553]  1000 622553  2523328   597531   591994     5533         4 … java
[ 643360]  1000 643360    78064    75164    74164     1000         0 … decompile
[ 643448]  1000 643448    84505    83014    82029      985         0 … decompile
[ 643454]  1000 643454    51748    50405    49393     1012         0 … decompile
[ 643566]  1000 643566   393322   389598   388607      991         0 … decompile
[ 643621]  1000 643621   187617   186237   185256      981         0 … decompile
[ 643708]  1000 643708    45236    43814    42821      993         0 … decompile
[ 643801]  1000 643801   104923   103430   102461      969         0 … decompile
[ 643849]  1000 643849   391642   384455   383471      984         0 … decompile
[ 643901]  1000 643901   186497   185057   184071      986         0 … decompile
[ 644073]  1000 644073   255554   247458   246449    1009         0 … decompile
```

Sum of the ten `decompile` `rss_anon`: 1 738 722 pages = **6.63 GiB**; plus the JVM
2.26 GiB plus node/npm ≈ **8.9 GiB** of the 9.57 GiB cgroup `anon`. This is round-4's
and r8's kill profile reproduced (`decompile invoked oom-killer`, ~10 workers) — but
this time on a **17.7 MB** target, and with the largest worker at 1.48 GiB where r6
saw one at ~4.1 GB, i.e. the cap *truncated* swarm growth before killing it.

The envelope is typed as a cancellation and carries **no `evidence_id`**:

```text
$ head -c 200 /var/tmp/arc2-l10r10-mid/stdout.json
error: Analysis failed
code: cancelled
category: cancelled
message: Analysis was cancelled. Start it again when ready.
$ grep -nE 'failure_|process_id|exit_code|exit_signal|operation:' /var/tmp/arc2-l10r10-mid/stdout.json
23:    process_id: 622553
27:    exit_code: null
28:    exit_signal: null
38:    failure_kind: cancelled
39:    failure_message: Ghidra startup was cancelled
# operation: list_documents
# (315462 B; zero evidence_id)
```

**Mislabel class, third occurrence.** `failure_kind: cancelled` with `exit_code:
null` / `exit_signal: null` is the exact shape of r4's and r8's OOM receipts
(`.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json:2-4,38-39`; adjudicated
at `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:29-33`). Envelope bytes alone
cannot distinguish "user cancelled" from "kernel killed". The receipt **pair**
(envelope + kernel journal) must be cited together.

The r6 baseline that makes the cap the cause rather than the host:

```text
$ cat .ufo/waves/arc2-loop1-round6/receipts/mid-rung-meta.txt
start_utc=2026-10-18T20:46:09Z
exit_code=0
end_utc=2026-10-18T21:27:28Z
stdout_bytes=5660
stderr_bytes=0
peak_tree_rss_kb=19149984        # 18.26 GiB
peak_java_rss_kb=2884192         # 2.75 GiB
wall_s=2479
```

r6's mid run was a bare process (`.ufo/waves/arc2-loop1-round6/E9.md:44-52`); the
only 9G unit in round 6 was `arc2-r6-pe`, the *big* leg (`.ufo/waves/arc2-loop1-round6/C6.md:31`
`MemoryMax=9663676416`). The mid rung had no memcg cap. Two independent lines then
make the mid r10 kill forced: r6's own 18.26 GiB tree peak is **2.03×** the r10 cap,
and the r10 cgroup's own unique-charged `anon 9567342592` (8.91 GiB) hit the 9 GiB
limit in 53.6 s with no host contribution required.

### 2.3 Host budget — it does not close

```text
$ grep -E 'MemTotal|MemFree|MemAvailable|Shmem|SwapTotal|SwapFree|Committed_AS|CommitLimit' /proc/meminfo
MemTotal:       31721792 kB      # 30.25 GiB
MemFree:         1038328 kB
MemAvailable:   11787172 kB
Shmem:              5160 kB
SwapTotal:      35917176 kB      # 34.25 GiB
SwapFree:       16714756 kB      # -> ~19.4 GiB swap in use
Committed_AS:   44644040 kB
CommitLimit:    51778072 kB
$ stat -f -c '%n blocks=%b bfree=%f bsize=%s' /tmp
/tmp blocks=3965224 bfree=797160 bsize=4096      # 16.2 GiB size, 3.26 GiB free -> 13 GiB used
$ du -sh /tmp/* | sort -rh | head -5
1.6G    /tmp/arc2-l3r3-C1-inst
927M    /tmp/seat50
885M    /tmp/seat44-a4b
518M    /tmp/coldrun-b
345M    /tmp/kotodama-r8-o14
```

`/tmp` is tmpfs (`/proc/self/mountinfo: 0:56 / /tmp … tmpfs rw,nosuid,nodev,
nr_inodes=1048576,inode64,huge=advise,usrquota`; `stat -c %D /tmp/s02-fresh.db` →
dev `38` = 0:56, while `/` and `/var/tmp` are dev `1f` btrfs). It has **no size
limit**, is the **largest single consumer on the box**, and ~all of it is swapped
out — resident `Shmem` stayed between 4 760 kB and 5 252 kB across all 240 samples.
Only ~1.6 GiB is this project's; the rest is stale scratch from `arc2-l3r3`
(round 3), `seat50`/`seat44-a4b` (unattributed seats), `coldrun-b`, and
`kotodama-r8-o14`. The wave's own mitigation (disk `TMPDIR`) kept *new* bytes out
of it but could not discharge the 13 GiB already resident.

```text
$ S=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice
$ echo "cur=$(cat $S/memory.current) peak=$(cat $S/memory.peak)"
cur=23673843712 peak=30289674240            # 22.05 GiB current / 28.21 GiB peak
$ grep -E '^(anon|file|kernel|shmem) ' $S/memory.stat
anon 5506408448                             #  5.13 GiB
file 16028536832                            # 14.93 GiB
kernel 2085904384                           #  1.94 GiB
shmem 1884160
$ cat $S/memory.events
low 0
high 0
max 220143                                  # 220,143 limit-hit events
oom 5
oom_kill 4                                  # four OOM kills in this cgroup today
oom_group_kill 0
sock_throttled 166501
```

```text
$ journalctl --since "2026-10-18 20:40:00" --until "2026-10-18 20:56:00" --no-pager | grep -i 'oom killer'
Oct 18 20:52:36 plazir27 systemd[1539]: app.slice: The kernel OOM killer killed some processes in this unit.
Oct 18 20:52:36 plazir27 systemd[1539]: -.slice: The kernel OOM killer killed some processes in this unit.
```

That is **3 m 50 s before** `arc2-r10-big`'s JVM started (`ps -o etime` on pid
622629 read `01:32` at 20:57:58 → start ≈ 20:56:26). The wave launched into a host
that had just OOM-killed. Host-wide OOM notices today: 14:46:17, 15:06:07,
16:07:45, **19:53:10 (`arc2-r8-ctl` — round 8's own control)**,
**20:52:36 (app.slice, pre-launch)**, **20:57:18 (`arc2-r10-mid`)**.

Sampler window (21:00–21:20, 240 × 5 s):

```text
min host MemFree        273816 kB   (267 MB)
min host MemAvailable   12672872 kB (12.08 GiB)
min host SwapFree       16148172 kB (>=19.4 GiB swap in use throughout)
host loadavg range      2.03 .. 11.51   (32 CPUs; CPU was never the binding axis)
max big_cur             8455393280 B (7.874 GiB)
```

Process budget at 21:01 (`ps -eo rss,args | awk '{s+=$1}'`): **12.93 GiB total RSS**,
of which `java` 6.23 GiB (the big leg alone) and `kimi` 4.09 GiB. So at the moment
of peak host pressure the two wave legs + the CLI sessions were ~10.3 GiB of a
12.93 GiB process budget — against 13 GiB of tmpfs that belongs to nobody in
particular.

### 2.4 "64 seats" is a roster count, not a load unit

```text
$ ps -eo comm --no-headers | sort | uniq -c | sort -rn | head -5
     35 bash
     18 sleep
     15 python3
      5 kimi
      5 godot
$ ls /proc | grep -cE '^[0-9]+$'
717
$ for p in $(ls /proc | grep -E '^[0-9]+$'); do readlink /proc/$p/cwd; done | … | sort | uniq -c | sort -rn
     43 /home/vgpnk/Projects/shokunin/kaidoku-shokunin
     31 /home/vgpnk/Projects/shokunin/game-dev-2d-shokunin
     19 /home/vgpnk/Projects/shokunin/souji-shokunin
      8 /home/vgpnk/Projects/shokunin/game-dev-2d-shokunin/corpus/fixtures
      5 /home/vgpnk/Projects/shokunin/game-dev-3d-shokunin
      4 /home/vgpnk/Projects/shokunin/kotodama-shokunin/.scratch/r31-run
      3 /home/vgpnk/Projects/shokunin/kotodama-shokunin
```

The 64-seat wave presents as **5 `kimi` processes**, not 64. Concurrent load comes
from **at least four other shokunin fleets** (`game-dev-2d`, `game-dev-3d`,
`souji`, `kotodama`) plus this one. Any future load model keyed to "seats" is
measuring the wrong quantity: the concurrency unit is the spawned subprocess
(`godot`, `decompile`, `java`), and the memory unit is the tmpfs/anon pair.

Delivery is progressing normally in parallel: `.ufo/waves/arc2-loop1-round10/`
held 0 `.md` reports at E9's census and **31** at 21:59.

## (3) Verbatim-landable text

Draft only — CR4 lands nothing. Artifact A is a corpus/`SCORECARD`-shaped record of
the host envelope and the two outcomes; artifact B is the receipt-pair rule the
third recurrence of the mislabel class justifies.

```text
## 2026-10-18 arc2-loop1-round10 — the dual-service host envelope (91.6MB held, 17.7MB killed)

Two user services ran concurrently on one 30.25 GiB host (`MemTotal 31721792 kB`),
each with a 9 GiB `MemoryMax` (9663676416) and a 1 GiB `MemorySwapMax`
(1073741824) — 18 GiB of caps, 59.5% of RAM. The host also carried a 16 GiB
`/tmp` tmpfs holding 13 GiB (`stat -f`: 3965224 blocks × 4096, 797160 free) with no
size cap, ~all of it swapped out (resident `Shmem` 4760–5252 kB across 240 samples),
and at least four other shokunin fleets. `app.slice` had already recorded
`oom 5 oom_kill 4` and `memory.peak` 28.21 GiB, with an OOM-kill notice at 20:52:36 —
3m50s before the first leg's JVM started. Host swap was ~19.4 GiB in use throughout.

Big leg (`arc2-r10-big`, 91.6 MB Godot ARM64, r7 recipe with the three
registry-validated disabled analyzers): HELD. `Result=success`, exit 0, 23min
58.082s wall, `Consumed 42min 43.809s CPU`, 7.8G memory peak, 769.1M memory swap
peak. Envelope 5204 B sha256 `a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a`,
byte-identical to the committed r7 receipt `.ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json`;
`evidence_id ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608`
re-derives exactly. Rerun id stability is therefore CONFIRMED at the 91.6 MB scale
point, and byte-level, not merely id-level. Cost of the concurrent host: swap peak
769.1M against r7's 53.1M (×14.5) and +0.94% wall (1438.082s vs 1424.663s);
`memory.events` `oom 0 oom_kill 0 max 0`, `memory.high=max`, so that reclaim was
host-global, not cgroup-driven. Correctness and CPU (+0.32%) were untouched.

Mid leg (`arc2-r10-mid`, 17.7 MB agent-browser, r6 recipe — no disabled analyzers):
kernel-OOM-killed at its own 9G cap in 53.602s. `Failed with result 'oom-kill'`,
`ExecMainStatus=1`; kernel `memory: usage 9437184kB, limit 9437184kB, failcnt
206682`, `swap: usage 1048436kB, limit 1048576kB, failcnt 8375`, `anon 9567342592`,
`oom-kill:constraint=CONSTRAINT_MEMCG,…oom_memcg=…/arc2-r10-mid.service`, victim
`java` pid 622553. Task table: JVM `rss_anon` 591994 pages plus ten `decompile`
children summing 1738722 pages (6.63 GiB). Envelope
`/var/tmp/arc2-l10r10-mid/stdout.json` (315462 B) is typed `code: cancelled` /
`failure_kind: cancelled` / `failure_message: Ghidra startup was cancelled` with
`exit_code: null`, `exit_signal: null` and no `evidence_id`. `ev_8b688ce7…` does
NOT re-derive; the r6 unknown (id stability across a rerun) stays UNKNOWN and is a
named debt, not a closure.

Root cause of the mid kill is recipe infidelity, not host load: r6 held only because
it ran uncapped — a bare process with no `MemoryMax`, measured
`peak_tree_rss_kb=19149984` (18.26 GiB) at
`.ufo/waves/arc2-loop1-round6/receipts/mid-rung-meta.txt`. The r10 rerun kept the r6
params and added the r7 envelope (9G + 1G swap), a cap r6 never had. The host is
therefore exculpated for this kill and indicted for the envelope: 2×9G caps plus a
13 GiB uncapped tmpfs do not fit a 30.25 GiB host, and the wave launched onto a host
that had already OOM-killed four times that day.
```

```text
Rule (receipt pair): a REA run envelope's `failure_kind`/`code` is not a terminal
class. `cancelled` with `exit_code: null` and `exit_signal: null` has been produced
by at least three distinct causes on this host — r4's memcg OOM, r8's control memcg
OOM (`.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json:2-4,38-39`), and
r10-mid's memcg OOM at `usage == limit`. Any claim that a leg was "cancelled",
"timed out", or "refused" must cite the kernel journal for the run window alongside
the envelope, or be recorded as UNKNOWN. Corollary: `systemctl show … OOMKills` is
uint64-max when the unit is unloaded and is NOT a count
(`.ufo/waves/arc2-loop1-round7/CR3.md:119-120`); use `memory.events` from the live
cgroup or the journal `Failed with result 'oom-kill'` line.
```

## (4) Observation / inference / unknown

**Observation** — all sealed or from `/proc`/`/sys` this session:
`arc2-r10-big` terminal `Result=success` / exit 0, 23min 58.082s wall, 7.8G peak,
769.1M swap peak (journal 21:20:23); its 5204 B envelope is `diff`-identical to
`.ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json`, sha256 `a77ebee8…`,
`ev_a4aa9b0d…`; cgroup `memory.peak` 8456077312 of 9663676416 with `oom_kill 0`,
`max 0`. `arc2-r10-mid` terminal `Result=oom-kill` / `ExecMainStatus=1`, 53.602s
wall, 9G peak, 1G swap peak, kernel `CONSTRAINT_MEMCG` at `usage == limit`, ten
`decompile` children, envelope typed `cancelled` with no `evidence_id`. r6's
mid-rung meta records `exit_code=0`, `wall_s=2479`, `peak_tree_rss_kb=19149984`.
Host: `MemTotal 31721792 kB`; `/tmp` tmpfs 13 GiB of 16.2 GiB used, resident
`Shmem` 4760–5252 kB; swap ~19.4 GiB in use; `app.slice` `oom 5 oom_kill 4`,
`memory.peak` 30289674240; pre-launch OOM notice 20:52:36; 5 `kimi` processes,
717 tasks, ≥4 concurrent fleets. Custody 5/5 OK.

**Inference** —
(i) The mid kill is fully determined by its envelope; host state is not a necessary
cause, since r6's own uncapped run exceeded the 9G cap by 2.03× on tree RSS and the
r10 cgroup's unique-charged anon independently reached 8.91 GiB in 53.6s.
(ii) The big leg's ×14.5 swap is host-attributable, because `memory.high=max` and
`oom_kill 0` rule out cgroup-side reclaim as the driver while host `MemFree` was
267 MB–4 MB during the startup phase where the swap peak was incurred.
(iii) The dual-service plan's cap arithmetic is not a budget: the 13 GiB uncapped
tmpfs is unowned by any `MemoryMax` and can only be swapped, which is why the host
sits 19.4 GiB into swap with 13 GiB of `/tmp` and 12.93 GiB of process RSS against
30.25 GiB of RAM.
(iv) "64 seats" is not a concurrency or memory unit on this host.

**Unknown** —
- The r10-mid leg's `analyzer_preset` is **not** sealed: the envelope aborted at
  `operation: list_documents` and contains no preset field (`grep -c 'ghidra-default'
  → 0`). "No disabled analyzers" is asserted from the launch recipe in this seat's
  brief, not from the run's own output. The r6 mid receipt (`mid-rung-envelope.json`,
  sha256 `2f39ab66…`, `analyzer_preset: ghidra-default`) is the only sealed evidence
  of the recipe.
- Wall-time discrepancy on the mid leg: the journal `Consumed` line says **53.602 s**;
  `.ufo/waves/arc2-loop1-round10/P2.md` states **53.178 s**. Both are near-identical
  and neither is wrong-class, but the authoritative source should be named in the
  integrated record.
- Which unit was OOM-killed at 20:52:36 is unresolved: systemd reported it at
  `app.slice` / `-.slice` granularity only, no kernel `Killed process` line survives
  in the journal for that second, and the victim's unit was already unloaded. Treated
  as "an app.slice OOM occurred pre-launch", not as a named victim.
- Whether the r6 natural mid-rung footprint is reproducible *at all* on this host is
  open: its 18.26 GiB tree peak plus the big leg's 7.9 GiB peak cannot coexist inside
  30.25 GiB alongside 13 GiB of tmpfs, so a natural mid-rung hold concurrent with the
  big leg is host-infeasible regardless of cap choice. Not measured here — CR4 did
  not launch anything.
- `peak_tree_rss_kb` (sum of tree RSS, double-counts shared pages) is not strictly
  comparable to memcg `anon` (unique-charged). The 2.03× ratio in inference (i) is
  corroborated rather than replaced by the r10 cgroup's own `anon 9567342592`.
