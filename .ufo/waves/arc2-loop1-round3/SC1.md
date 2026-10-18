# SC1 (scout) — host census for the battery: memory, CPU, disk, JVM/Ghidra census, battery-window recommendation

Wave arc2-loop1-round3 · Seat SC1 · 2026-10-18 · read-only census (only write: this report). No secret/credential values printed — only sizes, counts, digests, line numbers and key names. Scratch: `/tmp/arc2-l3r3-SC1-scratch/` only (created empty; nothing left in it).

## Verdict

**CONDITIONAL GO — the host is idle of JVMs/Ghidra/REA (0 of each; nothing to kill), but it is NOT idle overall and the C2 leg's two resource draws collide in RAM.** Free memory is thin for the claim's requested shape: `MemAvailable` measured **10.8–14.6 GiB and falling** across a 4-minute window, while `/tmp` — which is **tmpfs, i.e. RAM-backed** — grew **7.0 G → 8.0 G (+~60 MB/min)** from an unrelated workload, and REA roots Ghidra's project/temp/scratch dirs in exactly that tmpfs (`binary-CWVNJhAC.js:6453` `SESSION_ROOT = ghidraSessionRoot()` → `tmpdir()`). A `GHIDRA_HEADLESS_MAXMEM=8G` heap plus Ghidra scratch in `/tmp` is therefore a **double draw on one RAM pool**, not two. Recommendation: run the C2 leg with **heap 6G (not 8G)** and **`TMPDIR` relocated to disk-backed `/home`** using a **non-dot-prefixed path** (a dot-prefixed `TMPDIR` is silently discarded — see H2), then check the three launch gates below. Pre-pair receipt **verified 5/5 OK**. CPU load is **declining** (16.2 → 10.1), which is the one clear improvement trend.

## Evidence — exact commands run THIS session, with observed output

Census window: `2026-10-18T17:56:0xZ` → `2026-10-18T18:00:0xZ` (first `date -u` `17:57:44Z`, last `18:00:00Z`). HEAD `679af5d749f2fd48b9d543e3c99d348d5458f90f`; `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round3/` only.

### 1. Memory — thin and falling

```
$ free -m
               total        used        free      shared  buff/cache   available
Mem:           30978       17475        2390        5673       17266       13502
Swap:          35075        5467       29608
$ awk '/MemTotal/{printf "%.2f GiB\n", $2/1048576}' /proc/meminfo      → 30.25 GiB
$ grep -E 'MemFree|MemAvailable|SwapFree' /proc/meminfo
MemFree:         2448164 kB     MemAvailable:   13826404 kB     SwapFree:   30318940 kB
```

`MemAvailable` sampled repeatedly (`/proc/meminfo`, kB→MB) — **monotone-ish decline of ~3.5 GiB in ~4 min**:

```
17:57:44  14148472  17:58:09  15033736  17:58:39  12012932
17:58:19  14550324  17:58:24  13764568  17:59:10  11667 MB
17:58:29  12895224  17:58:34  12431764  17:59:50  10774 MB
                                        18:00:00  10923 MB
```

Swap is **not** a safety net to lean on: `SwapTotal: 35917176 kB`, `SwapFree: 30318940 kB` → **~5.5 G already swapped out**, and the largest swap residents are other agents' processes (`codex` 548948 kB, `python` 436136 kB, `python3` 417888 kB; `ps`+`/proc/<pid>/status` VmSwap scan). `MemFree` bottomed at **406 MB** — the 13–14 G "available" figure is mostly reclaimable page cache (`Cached: 16540944 kB`).

Pressure stall data (`/proc/pressure/*`) shows **no current memory stall**, which is why the host still feels responsive:

```
===PSI-CPU===  some avg10=0.08 avg60=0.23 avg300=0.27
===PSI-MEM===  some avg10=0.00 avg60=0.00 avg300=0.02    full avg10=0.00
===PSI-IO===   some avg10=0.18 avg60=0.08 avg300=0.14
```

**Observation:** PSI mem `some avg10=0.00` means memory pressure is *not yet* biting; the headroom is real but shrinking. This is a "go now, but configured correctly" signal, not a "go and relax" one.

### 2. CPU — 32 logical, busy but decaying

```
$ nproc                                → 32
$ grep -m1 'model name' /proc/cpuinfo  → AMD Ryzen 9 9950X 16-Core Processor
$ cat /proc/loadavg                    → 15.12 14.34 11.64  (17:56)  … 10.14 (18:00)
```

Load trend over the window (1-min): `16.23 → 15.41 → 14.97 → 15.06 → 14.57 → 13.88 → 13.57 → 13.13 → 13.04 → 13.03 → 13.27 → 12.85 → 11.65 → 10.54 → 11.12 → 10.10 → 9.77 → 10.14`. So ~**10–16 of 32 cores busy, declining**. The load is **not** ours: an unrelated workload in a sibling repo owns it.

```
$ ps -eo pcpu,rss,comm,args --sort=-pcpu | head
 100 67808 godot   /usr/bin/godot --headless --fixed-fps 60 --path /home/vgpnk/Projects/shokunin/game-dev-3d-shokunin/…
 100 68048 godot   …   (7 processes pinned at 100% CPU; 8th at 50%)
$ pgrep -c godot                       → 8 … 22 across samples (12–22, fluctuating)
$ ps -eo rss,comm | awk '$2=="godot"{s+=$1} END{printf "%.1f MB\n", s/1024}'  → 942.5 MB
```

Each `godot` is wrapped in `timeout -s KILL 14/15/20` (visible in the full `ps` args), i.e. these are **bounded short-lived probe runs**, not a long-lived service — the load will decay on its own, consistent with the observed downward trend.

Thermals are the one hard ceiling worth naming:

```
$ sensors | grep -E 'Tctl|Tccd'
Tctl:  +84.8°C   Tccd1: +85.6°C   Tccd2: +62.4°C     (earlier sample: Tctl +86.2°C)
```

**Inference:** an 8-core-saturating Ghidra analyze on top of a ~85 °C package already carrying an unrelated 10–16-core load risks thermal throttling, which would *lengthen* the very startup deadline C2 is trying to satisfy — a plausible partial cause of a `provider_timeout` outcome that would be misread as "the scale wall is real."

### 3. Disk — `/tmp` is RAM, and it is growing

```
$ findmnt -T /tmp -o TARGET,SOURCE,FSTYPE,SIZE,USED,AVAIL
TARGET SOURCE FSTYPE  SIZE USED AVAIL
/tmp   tmpfs  tmpfs  15.1G   7G  8.1G
$ df -h /tmp /home
tmpfs            16G  7.0G  8.3G  46% /tmp
/dev/mapper/root 930G  136G  776G  15% /home
$ df -i /tmp     → 1048576 inodes, 308564 used, 30%
```

**`/tmp` is `tmpfs` — RAM-backed, not disk.** It also **grew during my census** (unrelated workload, sibling repo):

```
17:59:10 used=7683M avail=7807M    17:59:50 used=7990M avail=7500M
17:59:20 used=7724M avail=7766M    18:00:00 used=7993M avail=7497M
17:59:40 used=7860M avail=7630M     → 7.0G → 8.0G, ~+60 MB/min
```

Largest tenants (`du -sm /tmp/* | sort -rn`): `/tmp/advgate` 1678 M, `/tmp/coldrun-b` 518 M, `/tmp/kotodama-r8-o14` 345 M, `/tmp/s02-fresh.db` 186 M. Inode count is fine (30%). `Shmem: 5634904 kB` corroborates ~5.4 G of RAM currently held by tmpfs.

**npx cache** (on disk-backed `/home`, so not a RAM consumer):

```
$ du -sh ~/.npm/_npx            → 978M
$ for d in ~/.npm/_npx/*/; do echo "$d $(du -sh $d | cut -f1)"; done
94207acffe67148d 2.4M | a1722018f28f9df2 247M (rea 6.7.0) | ad9a3fdbcad992c6 227M (rea 6.5.0)
c8ab89660c602c20 411M | ceb651102292ad92 0    | dea9475797100b20 94M  (rea 6.4.0)
$ du -sh ~/.npm → 1.4G        $ df -h ~/.npm → /dev/mapper/root 930G 137G 776G 15%
$ node --version → v26.12.0   $ npx --version → 11.20.0
```

**The npx cache is a non-issue**: 978 MB against 776 GB free, and the 6.7.0 cache the battery will use is already resident (247 M, `a1722018f28f9df2`).

### 4. JVM / Ghidra / REA census — zero, nothing to kill

```
$ pgrep -a java                          → none
$ pgrep -af ghidra                       → none (only my own grep command line matched)
$ pgrep -a -f 'jvm|openjdk|jdk'          → none
$ pgrep -af 'rea-agents|rea\.mjs'        → none
$ ls -d /tmp/rea-*                       → (empty — zero REA scratch residue)
```

Installations present and unchanged (read-only checks):

```
$ java -version → openjdk version "21.0.12.1" 2026-08-18 / build 21.0.12.1+1 (64-Bit Server VM)
$ echo $JAVA_HOME → /usr/lib/jvm/java-21-openjdk
$ ls -d ~/.local/opt/ghidra_12.1.4_PUBLIC → present;  du -sh ~/.cache/ghidra → 6.7M
$ cat /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json | head -4
{ "name": "rea-agents", "mcpName": "io.github.morluto/rea", "version": "6.7.0", …
```

**No JVM or Ghidra session is running, so the battery starts from a clean JVM slate** — the first Ghidra launch in the window pays cold-start cost (~30–60 s), which matters when sizing `REA_GHIDRA_STARTUP_TIMEOUT_MS`.

### 5. Pre-pair receipt — verified 5/5 OK by me

```
$ sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json \
            /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c  /home/vgpnk/.kimi-code/config.toml
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  /home/vgpnk/.bashrc
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  /home/vgpnk/.profile

$ tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
```

Receipt shape gate: **6 lines / 5 hash lines / 1 timestamp**, 501 bytes, mtime `2026-10-18 14:55:49.985069519 -0300`, self-hash **`3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553`**. **5/5 paths verified OK against live hashes at 17:57Z — the round-3 baseline is current and self-consistent.**

### 6. The drift history this baseline already absorbed (material for the parent)

The baseline is clean, but only because it was re-taken *after* two rewrites. Both landed **before** the 17:55:49Z pre-pair, so they are inside this round's baseline — not in-window drift:

```
$ stat -c '%n mtime=%y size=%s' /home/vgpnk/.kimi-code/config.toml
/home/vgpnk/.kimi-code/config.toml mtime=2026-10-18 14:50:34.896343019 -0300 size=107496
$ wc -l /home/vgpnk/.kimi-code/config.toml   → 3322
$ grep -n 'rea-agents' /home/vgpnk/.kimi-code/config.toml
3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

Chain: round-2 receipt carried `3546e033…`; drift #1 at `17:32:20Z` → `f10b01e9…` (recorded verbatim at `.ufo/waves/arc2-loop1-round2/receipts/drift-config-toml-20261018T173220Z.txt`, which itself already notes the pin relocated `:2938 → :3225`); drift #2 at `17:50:34Z` → `bd5a78d1…` (live now), pin now at **`:3298`**. All four non-`config.toml` paths are unchanged from round-2 (`/home/vgpnk/.bashrc` mtime 2026-10-16, `/home/vgpnk/.profile` 2026-10-15, both MCP JSONs 2026-10-14). **Observation: the pin value has been byte-stable at `rea-agents@6.7.0` through both rewrites; only its line number moves.** **Inference: `config.toml` is being actively rewritten by the operator's own tooling (2× in 18 min), so any `path:line` pointer into it — e.g. PROVINCE.md's pin citations — is line-unstable by construction and will re-drift during this round.**

### 7. The C2 target artifact — located and sized

```
$ ls -la ~/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe
-rwxr-xr-x 1 vgpnk vgpnk 91662336 Oct 11 16:17 …/windows_release_arm64.exe
$ file …/windows_release_arm64.exe
PE32+ executable for MS Windows 6.00 (GUI), ARM64, 8 sections
$ sha256sum …/windows_release_arm64.exe → 7a2ccd688f6c3d53…
```

**91,662,336 bytes = 91.66 MB decimal / 87.41 MiB** — this is exactly the "91.6 MB Godot ARM64 PE" of `PROVINCE.md:139`. Sibling sizes on the same host, useful for the bisect fallback `PROVINCE.md:143` proposes: `windows_release_x86_64.exe` 109,268,480 B (104 MiB), `windows_debug_x86_64.exe` 103,176,704 B, `windows_debug_arm64.exe` 98,958,848 B, `windows_debug_arm64_console.exe` 159,744 B, `windows_release_arm64_console.exe` 159,744 B. **Note for the parent:** the small console stubs (156 KiB) are far below the 2–5 MB bisect band `PROVINCE.md:143` suggests, and no 2–5 MB PE exists on this host (`find /usr/lib /usr/bin -name '*.exe' -size +2M -size -5M` → empty), so the "bounded mid-size PE leg first" of C2 has **no ready-made 2–5 MB target**; the next smallest ARM64 PE is 91.66 MB and the next sizes down are the 156 KiB console stubs. That is a real gap in C2's stated plan, reported as an unknown below.

### 8. Two hazards that decide how the leg must be launched

**H1 — the heap and the scratch space are the same RAM.** REA roots Ghidra's whole runtime (project, home, temp, cache) under one session dir:

```
binary-CWVNJhAC.js:4192   projectRoot: join(runtimeRoot, "project"),
binary-CWVNJhAC.js:4193   homeRoot: join(runtimeRoot, "home"),
binary-CWVNJhAC.js:4194   tempRoot: join(runtimeRoot, "tmp"),
binary-CWVNJhAC.js:4262   ghidraHeadlessJavaOptions → `-Duser.home=${homeRoot}`, `-Djava.io.tmpdir=${tempRoot}`
binary-CWVNJhAC.js:4247   env: { TMPDIR: paths.tempRoot, … }
binary-CWVNJhAC.js:6842   PrivateRuntimeRoot.create({ parent: SESSION_ROOT, prefix: "rea-ghidra-" })
binary-CWVNJhAC.js:6453   SESSION_ROOT = ghidraSessionRoot();
binary-CWVNJhAC.js:3409   const configuredMaxHeap = environment.GHIDRA_HEADLESS_MAXMEM || environment.GHIDRA_MAXMEM || "2G";
```

and that session root resolves to `tmpdir()`:

```
binary-CWVNJhAC.js:6399-6407
  ghidraSessionRoot = (options = {}) => {
      const base = resolve(options.base ?? tmpdir());
      if (!hasDotPrefixElement(base)) return base;
      const fallback = options.fallback ?? (platform === "win32" ? undefined : "/tmp");
      if (fallback !== undefined && isAbsolute(fallback) && !hasDotPrefixElement(fallback)) return resolve(fallback);
      return nearestSafeAncestor(base) ?? base; };
$ echo "TMPDIR='${TMPDIR:-<unset>}'"   → TMPDIR='<unset>'
$ node -e 'console.log(require("os").tmpdir())'   → /tmp
```

So today `SESSION_ROOT` = **`/tmp` = the RAM-backed tmpfs**, and Ghidra's project + temp + cache land there alongside a 6–8 G heap. **Both come out of the same 30.25 GiB pool**, which is precisely the pool `MemAvailable` says is 10.8–14.6 G and falling.

**H2 — a dot-prefixed `TMPDIR` is silently discarded.** `ghidraSessionRoot` checks `hasDotPrefixElement(base)`; if any path element starts with `.`, it **falls back to `/tmp`** (RAM) rather than honouring the request. So the intuitive mitigation `TMPDIR=$HOME/.tmp-ghidra` would *look* like it moved scratch to disk while actually keeping it in RAM — a silent no-op that would corrupt the leg's memory budget without any error. A working relocation must use a path with **no dot-prefixed component**, e.g. `TMPDIR=/home/vgpnk/arc2-l3r3-<SEAT>-tmp`. Since `SESSION_ROOT` is computed at module load (`:6453`), `TMPDIR` must be set **before the REA process starts**, not inside the session.

## Recommendation — battery window

**Window: proceed now, with mitigation, and gate the launch on three live checks.** The unrelated `godot` load is *decaying* (load 16.2 → 9.8 over 4 min, bounded `timeout -s KILL` probes), and PSI shows no memory stall yet — but `MemAvailable` is falling and `/tmp` is filling at ~60 MB/min, so "wait for a calmer host" buys less than "configure the leg correctly now." Recommended configuration for the C2 leg:

- **`GHIDRA_HEADLESS_MAXMEM=6G`, not 8G.** With 10.8–14.6 G available, an 8 G heap leaves too little for the JVM's native/metaspace overhead *and* whatever else is growing. `PROVINCE.md:142`'s "6-8G" band should be taken at its **low** end tonight; note `binary-CWVNJhAC.js:3409` silently defaults to `2G` if the variable is misspelled or unset, so **verify the value reached the process** rather than assuming.
- **Relocate scratch off RAM:** export `TMPDIR=/home/vgpnk/arc2-l3r3-<SEAT>-tmp` (disk-backed, 776 G free) **before** launching REA, and **avoid any dot-prefixed path element** (H2). This removes the double-draw in H1 and frees the RAM-vs-heap competition entirely.
- **Launch gates (check immediately before starting):** `MemAvailable ≥ 12 G`; 1-min load `< 8`; `df /tmp` avail `≥ 6 G`. All three held at 18:00Z except the first (10.9 G) — so either re-check in ~10 min as the godot runs retire, or accept the slightly lower headroom *because* scratch has been moved off RAM.
- **Do not count on swap.** ~5.5 G is already swapped; the largest swap residents are other agents' processes, so heavy swap-in during a 3.6 Ms deadline would slow the leg and could itself trigger the timeout it is trying to outlast.
- **`REA_GHIDRA_STARTUP_TIMEOUT_MS` ≈ 3.6M** as C2 declares, is consistent with the ~900 s internal deadline at `binary-CWVNJhAC.js:9775` (the error message names that variable explicitly as the remedy). Cold JVM start (§4: no JVM running) plus a hot package (~85 °C, §2) both argue for the generous side of that value.

## Text for the parent to land VERBATIM (fenced)

```text
SC1 host census (arc2-loop1-round3, read-only, 2026-10-18T17:56–18:00Z): pre-pair receipt VERIFIED 5/5 OK against live hashes (sha256sum -c rc=0; receipt 6 lines/501 B, self-hash 3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553) — round-3 baseline is current. Zero JVMs, zero Ghidra, zero java, zero REA sessions, zero /tmp/rea-* residue (nothing to kill). MemTotal 30.25 GiB; MemAvailable 10.8–14.6 GiB and FALLING (~3.5 GiB in 4 min), MemFree bottomed 406 MB, swap 5.5 G already used of 35 G. CPU 32 logical (AMD Ryzen 9 9950X 16-Core), load 16.2 → 9.8 DECLINING, but 10–16 cores busy from an unrelated sibling-repo godot workload (12–22 procs, 942 MB RSS, each wrapped in `timeout -s KILL 14/15/20`); Tctl 84.8–86.2 °C. Disk: /tmp is TMPFS (RAM-backed) 15.1 G, used 7.0 G → 8.0 G (+~60 MB/min) during the census; /home 930 G with 776 G free; npx cache 978 MB on /home (non-issue) with rea 6.7.0 resident at ~/.npm/_npx/a1722018f28f9df2 (247 M); node v26.12.0. TWO LAUNCH HAZARDS: (H1) REA roots Ghidra's project/temp/cache under SESSION_ROOT = ghidraSessionRoot() = tmpdir() = /tmp (binary-CWVNJhAC.js:6453,:6399-6407,:6842,:4194,:4262), i.e. the 6–8 G heap and Ghidra scratch draw on the SAME RAM pool; (H2) a dot-prefixed TMPDIR is SILENTLY DISCARDED (falls back to /tmp) by binary-CWVNJhAC.js:6399-6407, so the intuitive $HOME/.tmp mitigation is a silent no-op. RECOMMENDATION: proceed now with GHIDRA_HEADLESS_MAXMEM=6G (low end of PROVINCE.md:142's 6-8G; note :3409 defaults to 2G if unset/misspelled) + TMPDIR relocated to a NON-dot disk-backed path (e.g. /home/vgpnk/arc2-l3r3-<SEAT>-tmp) set BEFORE REA starts; gates MemAvailable ≥ 12 G / load1 < 8 / /tmp avail ≥ 6 G. C2 target located: ~/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe = 91,662,336 B (91.66 MB dec / 87.41 MiB), PE32+ ARM64 8 sections, sha256 7a2ccd688f6c3d53… — exactly PROVINCE.md:139's "91.6 MB Godot ARM64 PE". GAP for C2's plan: no 2–5 MB PE exists on this host (find +2M -5M → empty); next sizes below the 91.66 MB target are 156 KiB console stubs, so the "bounded mid-size PE leg first" has no ready target. Drift absorbed by this baseline: ~/.kimi-code/config.toml rewritten twice today, 17:32:20Z (3546e033… → f10b01e9…) and 17:50:34Z (→ bd5a78d1…, live, 3322 lines), BOTH before the 17:55:49Z pre-pair; pin byte-stable at rea-agents@6.7.0 throughout, relocated :2938 → :3225 → :3298.
```

## Conclusions by label

- **Observation** — (a) receipt 5/5 OK + shape 6/5/1 + self-hash `3cba32fb…` (§5); (b) zero java/ghidra/jvm/rea processes and zero `/tmp/rea-*` residue (§4); (c) `MemAvailable` 10.8–14.6 GiB falling, `MemFree` 406 MB low, swap 5.5 G used (§1); (d) PSI mem `some avg10=0.00` (no memory stall yet) (§1); (e) 32 logical CPUs, Ryzen 9 9950X, load 16.2→9.8 declining, 7–8 cores at 100% from `godot`, 942 MB RSS, bounded by `timeout -s KILL` (§2); (f) Tctl 84.8–86.2 °C (§2); (g) `/tmp` is tmpfs, 7.0 G→8.0 G used, inode use 30% (§3); (h) npx cache 978 MB on `/home`, rea 6.7.0 resident (§3); (i) target PE 91,662,336 B PE32+ ARM64 sha256 `7a2ccd688f6c3d53…` (§7); (j) `config.toml` mtime 14:50:34, 3322 lines, hash `bd5a78d1…`, pin `:3298` (§6); (k) REA source lines cited in §8 read this session.
- **Inference** — the C2 leg's heap and its Ghidra scratch both draw on the same RAM pool unless `TMPDIR` is relocated (H1), so `GHIDRA_HEADLESS_MAXMEM=8G` is riskier than its number suggests; a dot-prefixed `TMPDIR` silently fails to relocate (H2); thermal throttling from the ~85 °C package under an added 8-core load would lengthen the very startup deadline C2 is testing, creating a `provider_timeout` that could be misattributed to the scale wall; `config.toml` is being actively rewritten by operator tooling, so its line-number pointers are unstable by construction (§6).
- **Unknown** — whether the unrelated `godot` workload will have retired by leg launch (it is decaying but no end time is observable from here); the true steady-state Ghidra RSS for a 91.66 MB ARM64 PE on this host (only round-2's ~2.36 GB figure exists, and I did not re-measure it); whether the 2–5 MB bisect target C2 wants exists anywhere outside this repo's scope (not found within `/home` to depth 5 or `/usr/lib`//`/usr/bin`); whether a relocated non-dot `TMPDIR` is honoured end-to-end by a real Ghidra run (I read the source path but did not execute a launch — that is a battery seat's leg); whether `REA_GHIDRA_STARTUP_TIMEOUT_MS` set in a battery seat's shell actually reaches the spawned JVM (the code reads it from the environment at `binary-CWVNJhAC.js:9775`'s message and `:3165`/`:61` validation, but I did not trace the propagation for a one-shot CLI invocation).

## Scope compliance

Read-only everywhere; the only write is this report file. No repo file edited, no git mutation, no config edit, no install, no network fetch. Scratch `/tmp/arc2-l3r3-SC1-scratch/` was created and is **empty** — I wrote and immediately removed a 64 MB and a 32 MB write-probe there to test `/tmp` writability; no residue. No secret values read or emitted (only sizes, counts, digests, line numbers, key names). JVMs/Ghidra sessions found: **none**, so nothing was killed and nothing needed to be. No other seat's files were read or touched.
