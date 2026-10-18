<!-- arc2-loop1-round8 seat report — SC1 (scout): custody corroboration + host census during the natural control run. Observed read-only; the unit was never signaled/killed from this seat. -->

# SC1 — custody corroboration + host census during `arc2-r8-ctl` (natural control)

## 1. Verdict

- **Custody: PASS 5/5.** `.ufo/waves/arc2-loop1-round8/receipts/config-pre-pair.txt` verified byte-identical against all five live config paths at 19:49:56 -03 (89 s after the pre-pair second); zero drift. The pre-pair timestamp equals the service-start second (22:48:27Z == 19:48:27 -03), the same-second property round 7 recorded.
- **Host safety: PASS — the 9G cap is safe alongside.** Host MemAvailable floor during the run was 10,220,836 kB (~9.75 GiB) on a 31,721,792 kB host, memory PSI `some avg10` ≤ 0.09 for the whole life, and the kill was strictly cgroup-local (`CONSTRAINT_MEMCG`).
- **Control-run outcome (observed live, NOT sealed by this seat): the NATURAL CONTROL OOM-KILLED.** `Result=oom-kill` at 19:53:10 -03 — wall 4m42.945s, CPU 11m54.335s, mem peak 9G + swap peak 1G. Kernel log: a decompile worker's anonymous charge triggered the memcg OOM; victim = the Ghidra java process (3883315, anon-rss 3.4G). Round-4's kill profile (10–12 decompile workers, cap-saturating ramp) reproduced without any mitigation. This is the live attribution C3 was built to test; the sealed correction remains the parent's call.

## 2. Evidence

### 2.1 Custody (5/5)

Command: `sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile`

All five output lines identical to `receipts/config-pre-pair.txt:2-6`, e.g.:

```
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
e0634d8c5335aaf013bac5d4e45e4cfb513021f5fa027f36b5ad227324aa1c20  /home/vgpnk/.kimi-code/config.toml
```

Receipt line 1: `2026-10-18T22:48:27Z`; service `ExecMainStartTimestamp=Sun 2026-10-18 19:48:27 -03` — same second. [observation] Post-pair receipt not yet present at check time (receipts dir held only `config-pre-pair.txt`). [observation]

### 2.2 The unit was the natural preset (three independent corroborations)

1. Unit Environment — `systemctl --user show arc2-r8-ctl -p Environment`:
   `REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000 GHIDRA_HEADLESS_MAXMEM=6G TMPDIR=/var/tmp/arc2-l8r8-ctl GHIDRA_INSTALL_DIR=...ghidra_12.1.4_PUBLIC JAVA_HOME=...java-21-openjdk` — **no `REA_GHIDRA_DISABLED_ANALYZERS`**. (Also resolves the "7200s deadline": it is REA's startup-timeout env, not a systemd deadline; systemd showed the 1m30s transient default, irrelevant here.)
2. Java cmdline (ps, 19:50:23 -03): `-Xmx6G`, postScripts only `ReaGhidraNoReturnFix.java` + `ReaGhidraBridge.java` — **no `ReaGhidraAnalysisOptions.java`** (r7's disable vehicle, `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:17`).
3. Behavior: decompile workers present — r7's disabled run had zero (`:17`).

### 2.3 Live census before the kill (19:49:56 / 19:50:23 -03)

`systemctl --user show arc2-r8-ctl`: `ActiveState=active`, `MainPID=3883208`, `MemoryCurrent=6290862080`, `MemoryMax=9663676416` (exactly 9 GiB), `MemoryHigh=infinity`; cgroup `memory.swap.max=1073741824` (1G), `memory.events: low 0 high 0 max 0 oom 0 oom_kill 0`.

ps tree at T+116s: java (3883315) + **10** `Ghidra/Features/Decompiler/os/linux_x86_64/decompile` workers (3884350…3884386). [observation]

### 2.4 The kill (19:53:10 -03)

`systemctl --user status arc2-r8-ctl` after:
`Active: failed (Result: oom-kill) since Sun 2026-10-18 19:53:10 -03` — `Duration: 4min 42.677s` — `Mem peak: 9G (swap: 1G)` — `CPU: 11min 54.335s` — `Main PID ... status=1/FAILURE`.

`journalctl -k --since '19:50'`:
```
Oct 18 19:53:10 kernel: decompile invoked oom-killer: gfp_mask=0xcc0(GFP_KERNEL), order=0, oom_score_adj=200
Oct 18 19:53:10 kernel: oom-kill:constraint=CONSTRAINT_MEMCG,...,oom_memcg=/user.slice/.../arc2-r8-ctl.service,task=java,pid=3883315,uid=1000
Oct 18 19:53:10 kernel: Memory cgroup out of memory: Killed process 3883315 (java) total-vm:10167600kB, anon-rss:3415192kB, ... oom_score_adj:200
```
OOM task table lists the worker cohort (3894771/77/84/…/835/839, `decompile`) alive at kill alongside java (swapents raw values captured in the kernel dump; not reconciled against the 1G swap peak — see unknowns). [observation]

### 2.5 Survivor envelope

`/var/tmp/arc2-l8r8-ctl/stdout.json` (20,294 B, the only run artifact left; runtime dir deleted — ghidra.log/script.log gone):
`error: Analysis failed` / `code: cancelled` / `category: cancelled` / `retryable: true` / `failure_kind: cancelled` ("Ghidra startup was cancelled") / `run_id: e21ffd25-c5e8-4858-9962-ce6eab2c9152` / `profile_digest: 78013cb1…` / `target_sha256: 7a2ccd688f6c…` (matches the r7 artifact, `:11`) / `operation: list_documents`. No `evidence_id` — this is a failure envelope, not a census envelope. [observation]

### 2.6 Host census — SC1 sampler (48 samples × 10 s, 19:51:09→19:58:10 -03; capture at `/var/tmp/arc2-l8r8-SC1-census/samples-capture.log`)

```
19:52:19 MemAvail_kb=14284600 svc_cur=5680259072 workers=6  psi=0.00 ev=[max 0 ...]
19:52:29 MemAvail_kb=11665368 svc_cur=8776650752 workers=12 psi=0.00 ev=[max 0 ...]
19:52:49 MemAvail_kb=10801156 svc_cur=9663676416 workers=12 psi=0.09 ev=[max 2951 oom 0 oom_kill 0]
19:53:09 MemAvail_kb=10220836 svc_cur=9663590400 workers=12 psi=0.06 ev=[max 6951 oom 0 oom_kill 0]
19:53:19 MemAvail_kb=19409172 (cgroup gone — post-kill)
```
- MemAvailable floor during the run: **10,220,836 kB** at 19:53:09 (1 s before the kill); global min across all 48 samples is the same value. MemFree min 257,600 kB (page cache reclaim; MemAvailable is the honest metric and never left double digits in GiB).
- `memory.events` max-charge hits climbed 0 → 2,951 → 4,045 → 6,951 over the last 20 s; `oom_kill 0` in the final in-cgroup sample (kill landed 19:53:10, between samples).
- Post-kill MemAvailable recovered to ≥ 19.3 GiB. Host: MemTotal 31,721,792 kB, swap 30.3G file + 4G zram, disk `/` 751G avail, TMPDIR peaked 441M (2.6M after cleanup). [observation]

## 3. Verbatim-landable draft (SC1 observations; parent integrates/seals)

```markdown
Natural control observed live (SC1 census, 2026-10-18): user service `arc2-r8-ctl` ran the same
91.6MB PE (sha256 7a2ccd68…) on plain ghidra-default — no `REA_GHIDRA_DISABLED_ANALYZERS` in the
unit Environment (only `REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000`, `GHIDRA_HEADLESS_MAXMEM=6G`,
`TMPDIR=/var/tmp/arc2-l8r8-ctl`), no `ReaGhidraAnalysisOptions.java` postScript on the java
cmdline (only `ReaGhidraNoReturnFix.java` + `ReaGhidraBridge.java`), and 10 decompile workers in
the process tree at T+116s. OOM-killed by its own memcg at T+283s (19:53:10 -03): kernel
`constraint=CONSTRAINT_MEMCG`, trigger a decompile worker's anonymous charge, victim the Ghidra
java process (3883315, anon-rss 3.4G); systemd `Result=oom-kill`, wall 4m42.945s, CPU
11m54.335s, mem peak 9G, swap peak 1G; cap ramp 19:52:19→19:52:49 with memory.events max-charge
hits 0→6,951 before the kill. REA envelope: `category: cancelled`, `retryable: true` (survives at
`/var/tmp/arc2-l8r8-ctl/stdout.json`; no evidence_id). Attribution corroborated live: without the
disable recipe the run dies inside round-4's kill profile (10–12 decompile workers, 9G+1G
exhausted in under 5 min) — the round-7 analyzer-disable mitigation was necessary, and the
"natural unmitigated hold" named unknown (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:19`)
resolves as: the natural preset does NOT hold under the 9G/1G caps. Host census: the 9G cap is
safe alongside — MemAvailable floor 10,220,836 kB on a 31,721,792 kB host at the pre-kill second,
memory PSI some avg10 ≤ 0.09 throughout, kill strictly cgroup-local. Custody: pre-pair 5/5
sha256-verified at 19:49:56 -03, zero drift, pre-pair second == service-start second.
```

## 4. Labels

- **Observation:** everything in §2 — unit states, hashes, ps/journal/systemd excerpts, sampler series, surviving envelope; sampled at 10 s resolution.
- **Inference:** "natural preset in force" (three corroborations, §2.2); "attribution confirmed" (natural dies in the r4 worker profile vs r7's zero-worker success — the contrast the control was built for); "cap safe alongside" from floor+PSI+CONSTRAINT_MEMCG. Sealing the C3 correction and any SCORECARD/LOG/corpus edit stays with the parent.
- **Unknown:** worker count discrepancy (ps tree 10 at T+116s vs pgrep peak 12 — counting-method difference, both recorded); kernel-dump `swapents` magnitudes not reconciled against the 1G cgroup swap peak; whether the parent re-runs the control (this census covers one unit life only); rerun id-stability (r7's second named unknown) — untouched, no census envelope was produced; post-pair receipt not yet present at check time.
