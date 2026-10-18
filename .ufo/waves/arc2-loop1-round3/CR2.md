# CR2 (critic) — C2 safety attack: is the 6-8 GB Ghidra run safe alongside a 64-seat wave?

Seat CR2, wave arc2-loop1-round3, read-only on the repo and home. Every command
below was run by this seat this session (2026-10-18, 17:56Z–18:13Z) at HEAD
`679af5e`; `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round3/` only.
This report is my only write. Scratch confined to `/tmp/arc2-l3r3-CR2-*`. No
Ghidra leg was started by me; the live leg measured below belongs to seat E11
(read-only sampling of its `/proc` and its scratch). No config edits, no git
mutations, no installs, no network.

## 1. Verdict

**OBJECTION SUSTAINED — the 8 GB configuration is unsafe-by-margin on this
host as the wave actually runs it; the honest minimal version (deadline-only
retry, heap at 2–4 G, cgroup-contained, disk TMPDIR) is safe and is what C2
should land.**

The failure mode the plan assumes — "worst case, the leg dies" — is not the
failure mode that exists. Measured on the live same-knob leg (E11, running
while this seat sampled): the 8 G JVM peaked at **8.76 GB RSS — above its own
8 GiB `-Xmx` cap** — becoming the **highest-scored killable process on the
host** (oom_score 888 vs kimi parent seats 803–812 and the user's browser
renderers 868–870), while its own GC dips dropped it to **823–848 — below the
renderers**. A global OOM landing at such a dip kills a bystander (the user's
browser tab, a parent kimi seat), not the retryable leg. No isolation prevents
this: the JVM inherits the parent kimi seat's cgroup with `memory.max=max`,
`memory.swap.max=max`, unlimited rlimits, and REA applies no prlimit on the
Ghidra path. The plan's own recorded precondition — "on an idle host"
(`PROVINCE.md:143`, `corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:154`)
— is violated by construction in a 64-seat wave (load 13–20, four kimi seats,
other lanes' blender/godot/chromium resident), and a **global OOM already fired
on this host today at 17:46:17Z, nine minutes before the round-3 pre-pair**.

The plan's other leg — the "bounded mid-size PE first" — has already passed
(E10: 6 G knobs, 2.5 MB PE, exit 0, 44.1 s, peak JVM RSS 1.63 GiB) and shows
neither knob binding. The 8 G variant is therefore the *only* new risk C2 adds,
and it is the one my objection targets.

## 2. What the plan proposes, and its own recorded precondition

- `PROVINCE.md:139-144` (frontier bullet ">90 MB PE scale wall"): "Not OOM
  (RSS ~2.36GB vs -Xmx2G headroom exists). Next: raise
  `REA_GHIDRA_STARTUP_TIMEOUT_MS` to ~3.6Ms + `GHIDRA_HEADLESS_MAXMEM=6-8G`
  **on an idle host**, or bisect with a 2-5MB PE."
- `corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:136-137`: "The PE
  axis boundary at 91.6 MB is the session deadline — `provider_timeout`, **not
  a format, admission, or memory wall.**" Same file `:154`: "the honest next
  probes are a ~2–5 MB PE binary and a re-run at 3600 s **on an idle host**."
- Same file `:76-78`: default run was `-Xmx2G`; RSS peaked ~2.36 GB, "no OOM
  signature in log, process was CPU-bound (~85–96%) not heap-floored when
  killed."

Observation: the recorded wall is **time**, and the 6–8 G heap figure is the
same entry's speculative "and/or", not a measured requirement. The recorded
precondition is an idle host.

## 3. Evidence

### 3.1 Pre-pair receipt verified 5/5 (twice)

```
$ tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -
…/config/devin/mcp_config.json: OK ; omp/agent/mcp.json: OK ; kimi-code/config.toml: OK ; .bashrc: OK ; .profile: OK
RC=0        (re-verified at 18:08Z, same rc=0; receipt self-hash 3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553)
```

### 3.2 Host state at leg start (17:58Z)

```
$ free -g        → total 30, used 16, free 1, buff/cache 17, available 13; swap 34 total / 5 used
$ nproc          → 32
$ uptime         → load average: 14.15, 14.15, 11.59
$ ps aux --sort=-rss | head
  4 × kimi (RSS 0.4–1.1 GB each, VmSwap 95–155 MB each), blender -b (100% CPU, other lane),
  godot --headless (other lane), chromium tree, devin-shim, zcode
```

This is the "not idle" condition, measured at the moment the C2 leg started.

### 3.3 The live C2 leg (seat E11) — exact configuration

`/tmp/arc2-l3r3-E11/run-big.sh` (read this session):

```
export REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000
export GHIDRA_HEADLESS_MAXMEM=8G
PE=/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe
timeout -k 30 1800 npx -y rea-agents@6.7.0 analyze "$PE" --format json
```

Confirmed live in `/proc/2514831/environ`: `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000`,
`GHIDRA_HEADLESS_MAXMEM=8G`, `TMPDIR=/tmp/arc2-l3r3-E11/tmp/…`; in the cmdline:
`-Xmx8G … -import /tmp/arc2-l3r3-E11/tmp/rea-ghidra-QzJOuD/target-7a2ccd688f6c.exe`
— the same 91.6 MB Godot ARM64 PE as r4-12 (sha prefix `7a2ccd68…`,
`r4-12:16-17`). Started 17:58:20Z, `loadavg=13.04` (E11 console log).

### 3.4 Measured trajectory (my samplers, 17:59:44Z–18:12:19Z)

Sampler 1 (40 rows, 10–12 s cadence; `/tmp/arc2-l3r3-CR2-sample.tsv`):

| metric | value | at |
|---|---|---|
| JVM RSS plateau → climb | 3.92 GB → 4.63 → 5.13 → 6.17 → 7.42 GB | 18:00–18:07Z |
| peak JVM RSS (sampler 1) | **7,420,324 kB (7.42 GB)** | 18:07:22Z |
| peak JVM swap-in | **1,525,428 kB (1.53 GB)** | 18:04:33Z |
| JVM oom_score | 838 → 874 | 18:00Z → 18:06:46Z |
| min MemAvailable | 6,322,788 kB (6.32 GB) | 18:04:09Z |
| max host swap used | **16,540,164 kB (16.5 GB)** — from 9.81 GB at leg start | 18:04:33Z |
| max load1 | 19.73 | 18:02:57Z |

Sampler 2 (late; `/tmp/arc2-l3r3-CR2-late.tsv`, 18:10:29–18:15:20Z, 30 rows),
leg still running at sampler close:

```
18:10:29Z  5903376 kB RSS  160284 kB swap  oom_score 859
18:11:39Z  8753868 kB RSS  160200 kB swap  oom_score 888
18:12:49Z  8760584 kB RSS  160200 kB swap  oom_score 888   ← late-sampler peak
18:13:50Z  6582984 kB RSS  160132 kB swap  oom_score 866
18:15:00Z  7048936 kB RSS  152620 kB swap  oom_score 870
18:15:20Z  4116872 kB RSS  152564 kB swap  oom_score 842   ← next GC dip
```

**Peak observed 8,760,584 kB (8.35 GiB) > the 8 GiB `-Xmx8G` heap cap**
(off-heap: metaspace, JIT, GC structures, native decompiler buffers ≈
+0.35 GiB). In the late window alone RSS oscillated 4.12–8.76 GB and
oom_score 842–888 across three GC cycles — the inversion below is a repeating
cycle, not a one-off. The JVM tree also carried 11–12 native
`os/linux_x86_64/decompile` processes (combined RSS 0.66–1.17 GB measured at
two points), so the leg's total resident demand was ≈ 9.9–10 GB. At my final
check (18:15:34Z) the leg was at 1033 s of its 1800 s cap, still in
`ANALYZING all memory and code` (ghidra.log 470+ lines, stdout still 0 bytes,
no evidence sealed) — final outcome not yet observed by this seat. Zero OOM
kills in the leg window (`journalctl -k --since "2026-10-18 18:00"` → 0).

### 3.5 OOM victim ranking — and the inversion

All relevant processes share `oom_score_adj=200` (kimi seats, the JVM) or 300
(chromium renderers). `/proc/<pid>/oom_score` is the kernel's effective badness
(adj already included); measured this session:

```
JVM (8.76 GB, adj=200)          oom_score 888   ← top-ranked killable process on the host
chromium renderer (0.41 GB, adj=300)  oom_score 870
kimi parent seats (0.8–1.1 GB, adj=200)  oom_score 803–812
JVM at its GC dip (2.18 GB)     oom_score 823   ← below the renderers
```

Empirical fit across the adj=200 cluster: score ≈ 601 + 9.9 × RSS_GiB + adj
(±2 points on four adj=200 observations; the adj=300 renderer does not fit the
same line). **Inversion:** at 18:05:34Z and 18:10:49Z the
JVM's RSS dipped (2.18 GB / 4.79 GB) and its score fell to 823/848 — below the
renderers' 870. Had a global OOM fired at either instant, the kernel would have
killed a chromium renderer (the operator's browser) or, at a deeper dip, a
parent kimi seat — not the leg. The margin between the JVM and the parent seats
at dips was ~11 points.

### 3.6 No isolation exists

```
$ sed -n 's/^0:://p' /proc/2514831/cgroup
/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/app-Hyprland-xdg\x2dterminal\x2dexec-1c68de2e.scope
$ cat .../app-Hyprland-xdg\x2dterminal\x2dexec-1c68de2e.scope/memory.max      → max
$ cat .../…/memory.swap.max                                                   → max
$ grep -E "Max address space|Max resident set|Max data size" /proc/2514831/limits
Max data size unlimited / unlimited ; Max resident set unlimited / unlimited ; Max address space unlimited / unlimited
$ grep -rn "LinuxResourceLimits|prlimit" <rea-agents@6.7.0>/dist/ghidra/      → no matches
```

The JVM runs inside the **same cgroup as the parent kimi seat's terminal** with
no memory or swap limit anywhere up the chain (`user.slice/memory.max` = `max`,
`memory.current` 22.95 GB at read time). REA's prlimit wrapper applies only to
Wakaru/firmware/capture providers (`dist/cli-runtime/cli.js:37799`,
`dist/mcp/main-Cx-Z7m_n.js:44070`), never to Ghidra. Mechanism source:
`dist/ghidra/GhidraJavaLaunch.js:114` (`GHIDRA_HEADLESS_MAXMEM || GHIDRA_MAXMEM
|| "2G"`) and `:141` (`-Xmx${configuredMaxHeap}`) — the knob is a plain JVM
heap option with no guard rails; `dist/config/providerStartupTimeout.js:3`
(default 330_000 ms) and `:10/:16` (cap 2³¹−1) bound the deadline knob.

### 3.7 The host is already in an OOM-firing regime

```
$ journalctl -k --since "2026-10-18 00:00" | grep "Out of memory: Killed"
Oct 18 14:46:17 plazir27 kernel: Out of memory: Killed process 746432 (systemd-coredum)
  total-vm:14056kB, anon-rss:4300kB, …, UID:0 pgtables:72kB oom_score_adj:500
  … oom-kill:constraint=CONSTRAINT_NONE,…,global_oom, task_memcg=/system.slice/system-systemd\x2dcoredump.slice/…
```

14:46:17 local (−03) = **17:46:17Z — 9 minutes before the round-3 pre-pair**.
A global (not memcg-constrained) OOM kill of a root process fired under this
multi-lane load. Zero OOM kills after 18:00Z during the leg (checked twice).

### 3.8 Pressure export to other sessions (measured, no kill required)

The leg did not need to OOM to hurt other sessions — it pushed them into swap:

```
kimi seat 2299991 VmSwap: 110 MB (17:58Z) → 390 MB (18:10Z)
kimi seat 2342280 VmSwap: 152 MB → 223 MB
kimi seat 1980565 VmSwap:  78 MB → 179 MB
kimi seat 878959  VmSwap:  95 MB → 136 MB
host swap used: 9.81 GB (leg start) → 16.54 GB peak (18:04:33Z)
```

All four sibling kimi seats' swap residency rose 1.4–3.5× during the leg. The
JVM's own swap peaked at 1.53 GB; the rest of the +6.7 GB host swap came from
reclaiming other sessions' pages.

### 3.9 The tmpfs angle

```
$ findmnt -T /tmp    → tmpfs        (16 GB RAM-backed; df: 16G size, ~7.0G→10.2G used in window)
$ findmnt -T /var/tmp → /dev/mapper/root[/@] btrfs (775 GB free)
/tmp avail: 8.81 GB (17:57Z) → 5.84 GB (18:12Z); E11 project dir grew to ~900 MB
```

Every byte of the Ghidra project lands in RAM (`TMPDIR` was redirected into
`/tmp` by E11's script). Redirecting `TMPDIR` to `/var/tmp` (btrfs) converts
~1–2 GB of RAM consumption per leg into evictable page cache — verified the
session dir follows `TMPDIR` (the session landed at
`/tmp/arc2-l3r3-E11/tmp/rea-ghidra-QzJOuD/`, not `/tmp/rea-ghidra-*`).

### 3.10 The containment primitive works on this host (verified live)

```
$ systemd-run --user --scope -p MemoryMax=268435456 -p MemorySwapMax=0 --quiet -- bash -c '…cat memory.max; cat memory.swap.max'
268435456
0
$ systemd-run --user --scope -p MemoryMax=67108864 -p MemorySwapMax=0 --quiet -- bash -c 'echo in-scope; python3 <400MB alloc>'
in-scope cgroup=/user.slice/…/run-p2866091-i19650632.scope
Killed            (SIGKILL)
SCOPE-EXIT=137    parent shell unaffected
$ systemctl --user list-units --type=scope --all | grep -c run-p   → 0   (self-cleaned)
```

A `systemd-run --user --scope -p MemoryMax=… -p MemorySwapMax=…` envelope is
honored by this kernel (7.2.3-arch1-3, cgroup v2) and confines an
over-allocation kill to the scope. This is the missing guard rail. (The demo
left a `failed (Result: oom-kill)` transient unit, which I removed with
`systemctl --user reset-failed run-p2866091-i19650632.scope` — a scope that
dies by memcg OOM stays visible as a failed unit until reset; plan for that in
the post-run residue sweep.)

### 3.11 The bounded mid-size leg already passed (E10)

`.ufo/waves/arc2-loop1-round3/E10.md:14-18`: `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000
GHIDRA_HEADLESS_MAXMEM=6G` on a 2.5 MB PE → **exit 0, 44.1 s, 7 segments /
6,337 procedures, evidence `ev_92dea347…`**; "peak JVM RSS 1.63 GiB « 6 GiB
heap; 44 s « 3600 s deadline". Neither knob bound. The mid-size leg validates
the recipe syntax, not the 8 G heap demand — only the 91.6 MB target exercises
it.

## 4. Strongest safety objection (condensed)

Under global memory exhaustion the kernel kills the highest-scored process, and
the 8 G JVM's own GC cycle sweeps it across the bystander band: measured
oom_score 823 (dip) ↔ 888 (peak), against parent kimi seats at 803–812 and
browser renderers at 870. The plan's implicit "worst case the leg dies" is
false at every dip below 870: the victim is then the operator's browser or a
parent seat — non-retryable losses — while the leg survives. There is no
cgroup, rlimit, or REA-level guard on the Ghidra path to convert this into a
leg-local failure, and the host demonstrably reaches global OOM in this
workload regime (17:46:17Z today, pre-pair). The plan's own precondition
("idle host") is violated by the wave itself, and the recorded r4-12 wall was
time, not memory — so the 8 G heap is an unpriced, unrequired risk.

## 5. The honest minimal version

1. **Deadline-only retry first.** Keep `GHIDRA_HEADLESS_MAXMEM` at the default
   2 G (or 4 G); raise only `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000`. This is
   the wall r4-12 actually measured (`provider_timeout`, retryable), and it
   costs nothing new on the memory axis. If a typed heap failure appears, step
   to 4 G, then 6 G — each step inside a scope (below).
2. **Contain the leg.** `systemd-run --user --scope -p MemoryMax=7G
   -p MemorySwapMax=1G` — verified honored on this host; a scope-local kill
   (exit 137) becomes the honest negative, not a host-level event.
3. **TMPDIR on disk.** `TMPDIR=/var/tmp/arc2-l3r3-<seat>-tmp` (btrfs, 775 GB
   free) — removes ~1–2 GB of RAM consumption per leg.
4. **Run with other heavy legs closed**, or record the degraded margin
   explicitly in the round record.
5. **Post-run gates:** `journalctl -k` shows zero OOM in the window; JVM peak
   RSS < `MemoryMax`; zero `/tmp/rea-ghidra-*` residue; the scoped memcg kill
   (exit 137, untyped) is an accepted honest-negative form — or the parent
   wires a wrapper converting 137 into a recorded typed negative.

## 6. Verbatim block for the parent (land as-is if used)

```text
C2 safety disposition (round 3, seat CR2; measured 2026-10-18 17:58–18:13Z, HEAD 679af5e):
The 8G configuration as drafted is refused; the honest minimal version below is
cleared. Measured on the live same-knob leg (seat E11:
REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 + GHIDRA_HEADLESS_MAXMEM=8G, target
windows_release_arm64.exe sha 7a2ccd68…): peak JVM RSS 8.76 GB at 18:12Z (above
the 8 GiB -Xmx cap; off-heap ~0.35 GiB), JVM swap-in 1.53 GB, host swap used
9.8 → 16.5 GB, /tmp (16 GB RAM-backed tmpfs) avail 8.8 → 5.8 GB, load 19.7.
The JVM became the host's top OOM candidate (oom_score 888; kimi parent seats
803-812; browser renderers 868-870 at adj=300), and its own GC dips drop it to
823-848 — below the renderers — so a global OOM at a dip kills a bystander
(browser/parent), not the retryable leg. No isolation exists: the JVM inherits
the parent kimi scope (memory.max=max, memory.swap.max=max, rlimits unlimited);
REA applies prlimit only on Wakaru/firmware/capture paths, not Ghidra. The
plan's own precondition "on an idle host" (PROVINCE.md:143; r4-12:154) is
violated by a 64-seat wave, and a global OOM already fired today at 17:46:17Z
(killed systemd-coredump, adj=500) — 9 min before the pre-pair.

Honest minimal (recipe; all primitives verified this session):
1) Deadline-only retry first — r4-12's measured wall was TIME (provider_timeout,
   retryable), not memory; the 6-8G MAXMEM was the same entry's speculative
   "and/or". Keep GHIDRA_HEADLESS_MAXMEM at 2G (or 4G); raise only the deadline.
2) Contain: systemd-run --user --scope -p MemoryMax=7G -p MemorySwapMax=1G
   (read-back verified; over-allocation demo killed inside scope, exit 137,
   parent unaffected).
3) TMPDIR=/var/tmp/arc2-l3r3-<seat>-tmp (disk-backed btrfs; /tmp is RAM).
4) Run with other heavy legs closed, or record the degraded margin.
5) Post-run gates: journalctl -k zero OOM in window; JVM peak < MemoryMax;
   zero /tmp/rea-ghidra-* residue; scoped memcg kill (exit 137, untyped) is an
   accepted honest-negative form.
```

## 7. Conclusions, labeled

**Observations** (ran/read this session): receipt 5/5 rc=0 twice; the E11 leg's
knobs in environ/cmdline and its 17:58:20Z start; the full RSS/swap/score
trajectory (peak 8.76 GB RSS, 1.53 GB JVM swap, score 823–888); cgroup
`memory.max=max`/`memory.swap.max=max` and unlimited rlimits on the JVM;
no prlimit in the Ghidra provider; the 17:46:17Z global OOM line; sibling kimi
seats' swap residency rising 1.4–3.5×; /tmp tmpfs avail 8.8→5.8 GB and E11's
~900 MB project dir; the systemd-run containment demo (exit 137, parent
unaffected, scope self-cleaned); E10's exit-0 6 G result; the source lines in
`GhidraJavaLaunch.js:114,:141`, `providerStartupTimeout.js:3,:10,:16`.

**Inferences:** (1) the 8 G heap is not required — r4-12's wall was time, and
the live leg at 1033 s was still CPU-bound (ghidra.log still appending), not
heap-floored; (2) the OOM inversion is real given ±65-point score movement
across the GC cycle, observed over three cycles in the late window; (3) the
honest minimal would suffice and the mid-size leg already proved the recipe;
(4) the pressure export to sibling seats is systematic, not incidental.

**Unknowns:** (1) the E11 leg's final outcome (still running at my last check
18:15:34Z: 1033 s of 1800 s cap, stdout 0 bytes; whether it completes, and its
final peak); (2) whether a
scoped memcg OOM kill would surface as a typed envelope in REA or as an
untyped SIGKILL (expected untyped; untested); (3) the kernel's exact
oom_badness weighting of shmem/swap at these magnitudes (my score model is an
empirical fit on four adj=200 observations, not kernel-source verified); (4) the
post-pair custody state (SC2's config-churn note is outside this seat's scope).

## 8. Reproduction commands

```bash
git rev-parse HEAD; git status --porcelain
tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -
cat /tmp/arc2-l3r3-E11/run-big.sh
tr '\0' '\n' < /proc/2514831/environ | grep -E 'REA_GHIDRA_STARTUP_TIMEOUT_MS|GHIDRA_HEADLESS_MAXMEM|TMPDIR'
tr '\0' ' ' < /proc/2514831/cmdline | grep -o '\-Xmx[0-9A-Za-z]*'
cat /tmp/arc2-l3r3-CR2-sample.tsv; cat /tmp/arc2-l3r3-CR2-late.tsv
sed -n 's/^0:://p' /proc/2514831/cgroup; grep -E 'Max address space|Max resident set' /proc/2514831/limits
grep -rn 'prlimit' /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/ghidra/   # no matches
journalctl -k --since "2026-10-18 00:00" | grep "Out of memory: Killed"
systemd-run --user --scope -p MemoryMax=268435456 -p MemorySwapMax=0 --quiet -- bash -c 'sed -n "s/^0:://p" /proc/self/cgroup; cat /sys/fs/cgroup$(sed -n "s/^0:://p" /proc/self/cgroup)/memory.max'
```

## 9. Scope compliance and residue

- Only repo write: this report. `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round3/`
  only. No git mutations, no config edits, no installs, no network fetches, no
  Ghidra leg started by this seat.
- Scratch: `/tmp/arc2-l3r3-CR2-sample.tsv`, `/tmp/arc2-l3r3-CR2-late.tsv`,
  `/tmp/arc2-l3r3-CR2-oomdemo.py` (my namespace only; left as evidence).
  Zero Ghidra project dirs in my namespace; the systemd-run demo scope was
  left as a `failed (Result: oom-kill)` transient unit by design and removed
  with `systemctl --user reset-failed` (verified `grep -c run-p` → 0 after);
  no processes of mine remain (both samplers exited; `pgrep -fa
  arc2-l3r3-CR2` → empty). No other seat's files were modified; the E11 leg was
  only read (`/proc`, its scratch logs).
