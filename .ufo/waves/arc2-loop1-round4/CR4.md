# CR4 (critic) — attack on the background PE run's presence: round-shape and scope rules

Seat CR4, wave `arc2-loop1-round4`, 2026-10-18, observation window 19:04:41Z–19:16:47Z
(`date -u` readings inline). Read-only on the repo, `/var/tmp`, `/proc`, the user journal,
and `~/.npm` logs; **this report is my only write**. HEAD `158a96611f22afdfa723131f3ec27f39138020e8`
at my start, `1692acbe48ce0eac3b7c87698be59d8a04f46a08` ("rule 11", parent, 19:09:10Z) after.
No git mutations, no config edits, no installs, no REA probes, no network fetches by this seat.
The PE run was observed read-only — **never killed, renice'd, signalled, or touched**. No
scratch files were created by this seat (nothing under `/tmp/arc2-l4r4-CR4-*`).

**Pre-pair receipt (my leg):** `.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt`
verified **5/5 rc=0** at ~19:05Z and again at 19:12Z (post-OOM) — §2.3.

## 1. Verdict

**ATTACK NOT SUSTAINED on the round-shape prong; SUSTAINED IN NARROW FORM on one scope
expectation.** Precisely:

1. **One-batched-dispatch discipline — NO violation.** The binding text constrains *L2 subagent
   dispatch*, not host processes: `MISSION.md:55-56` ("Every L1 lane MUST dispatch **at least 8
   L2 subagents per round**, in **one batched AgentSwarm call** … not a sequence of individual
   dispatches"), `PROTOCOL.md:97-98`, `SKILL.md:72`. The run carries no seat identity — no lane
   prompt, no `/skill:godspeed` lead, no report path, no seat file — and was launched by the
   parent's own receipt shell (`pid 4175697`), not by any task/Agent call. It is therefore not
   a second, un-batched dispatch. The rule is also a floor ("at least 8"), not an exclusive
   channel: the parent executing the round's own C2 decisive-run recipe
   (`LOG.md:1094-1095`; `CR2.md:305-316`) as infrastructure is lane work, not an undispatched
   seat. In the observed event nothing was serialized: the wave ran concurrently (seat reports
   landed 19:06Z–19:12Z, §2.6) and the parent committed `1692acbe` at 19:09:10Z while the run
   was dead. ("2h process" is the *form*: 7200 s deadline, no outer kill. In the event it lived
   **4 m 42 s** — the deadline never bound.)

2. **Scope rules — one strict-form deviation, disclosed, minimal.** The brief's "no network
   fetches (npx cache resolution expected offline)" expectation is **falsified**: the run's own
   `npm exec` made one live registry touch — `http fetch GET 200
   https://registry.npmjs.org/rea-agents 48ms (cache revalidated)`
   (`~/.npm/_logs/2026-10-18T19_03_02_856Z-debug-0.log:14`, the file's 14th line — npm's
   own leading counter reads `13`; that log is fd 20 of pid 4175743).
   It is metadata-only — the package resolved from the cached 6.5.0 tree at
   `~/.npm/_npx/ad9a3fdbcad992c6` — and is already disclosed in the wave's own records
   (`.ufo/waves/arc2-loop1-round4/E16.md`, §battery note, "one registry packument revalidation";
   same text in `E22.md`'s draft-diff block). Every other scope
   constraint holds: **no custody-path fd** on any of the three processes; **no repo fd**
   (`grep -c Projects/shokunin` → 0/0/0); `TMPDIR=/var/tmp/arc2-l4r4-pe` (disk, not tmpfs);
   scratch namespaced; no custody path touched.

3. **The run's presence was, in the event, benign and contained — and its outcome is the
   round's decisive C2 datum.** It died by `CONSTRAINT_MEMCG` OOM inside its own scope at
   **19:07:45Z, 4 m 42 s in** — `MemoryPeak == MemoryMax == 7516192768` (7 GiB), swap cap
   reached (1 048 552 kB / 1 048 576 kB) — with **zero host-level OOM kills** in the window,
   custody 5/5 throughout, and a typed negative sealed (`exit=1`, `code: cancelled`,
   `cleanup: complete`). The round-3 CR2 containment recipe worked as designed: the failure
   became a leg-local negative instead of the bystander-kill CR2 predicted for an uncontained
   run (`CR2.md:252-264`).

## 2. Evidence — exact commands with observed output (all this session)

### 2.1 Identity and launch path — infrastructure, not a seat

```console
$ tr '\0' ' ' < /proc/4175733/cmdline; echo
/bin/bash /tmp/arc2-l4r4-pe-launch.sh
$ ps -o pid,ppid,lstart,cmd -p 4175743,4177041,4181543
4175743 4175733 Sun Oct 18 16:03:01 2026  npm exec rea-agents@6.5.0 analyze …/windows_release_arm64.exe
4177041 4175743 Sun Oct 18 16:03:02 2026  node …/.bin/rea analyze …/windows_release_arm64.exe
4181543 4177041 Sun Oct 18 16:03:03 2026  java … -Xmx6G … ghidra.app.util.headless.AnalyzeHeadless …
$ ps -o pid,ppid,cmd -p 4175697
4175697 1539 /bin/bash -c cd '/home/vgpnk/Projects/shokunin/kaidoku-shokunin' && … sha256sum … > .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt && … nohup /tmp/arc2-l4r4-pe-launch.sh > /tmp/arc2-l4r4-pe-launch.out 2>&1 & …
$ readlink /proc/4175743/cwd /proc/4177041/cwd /proc/4181543/cwd
/home/vgpnk/Projects/shokunin/kaidoku-shokunin
/home/vgpnk/Projects/shokunin/kaidoku-shokunin
/home/vgpnk/Projects/shokunin/kaidoku-shokunin
```

The parent launched the run from the **same shell that wrote the pre-pair receipt**
(19:03:02Z), i.e., as declared round infrastructure — no seat prompt or report duty appears
anywhere in the cmdlines. The launcher script (sha256
`8c0450e1dffa7e4fda78deb233b913939813ed6ac4b8acf44ad13e7b99868e69`):

```console
$ cat /tmp/arc2-l4r4-pe-launch.sh
#!/bin/bash
# arc2-loop1-round4: contained decisive 91.6MB PE wall run (CR2 recipe).
# Deadline-only: REA's own 7200s deadline is the only timeout; no outer kill.
mkdir -p /var/tmp/arc2-l4r4-pe
systemd-run --user --scope --quiet \
  -p MemoryMax=7G -p MemorySwapMax=1G -p Description=arc2-pe-wall \
  env REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000 \
      GHIDRA_HEADLESS_MAXMEM=6G \
      TMPDIR=/var/tmp/arc2-l4r4-pe \
      GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC \
      JAVA_HOME=/usr/lib/jvm/java-21-openjdk \
  npx -y rea-agents@6.5.0 analyze …/windows_release_arm64.exe \
  > /var/tmp/arc2-l4r4-pe/stdout.json 2> /var/tmp/arc2-l4r4-pe/stderr.log
echo "exit=$? wall_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > /var/tmp/arc2-l4r4-pe/exit.txt
```

### 2.2 The rule text (read, not recalled)

```console
$ sed -n '55,56p' /home/vgpnk/.kimi-code/skills/shokunin/protocol/MISSION.md
Every L1 lane MUST dispatch **at least 8 L2 subagents per round**, in **one
batched AgentSwarm call** (the Kimi host surface) — one call carrying all lanes,
$ sed -n '97,98p' /home/vgpnk/.kimi-code/skills/shokunin/protocol/PROTOCOL.md
… (ii) the L2 minimum — at least 8 L2 lanes in one batched AgentSwarm call
(the Kimi host surface), a number this file does not own: `MISSION.md` §L2 concurrency is its
$ sed -n '72p' /home/vgpnk/.kimi-code/skills/shokunin/SKILL.md
   dispatch ONE batched AgentSwarm call with ≥8 lanes:
```

Corroborating in-repo statement of the same discipline, `.ufo/rounds/interactive-r1/wave-validation.json:11`
(embedded plan `dispatch.note`): "Issue exactly one batched task call carrying every spawn lane
… Never split a wave into multiple task calls (one-swarm-per-wave)." **None of these texts
constrains parent-run host processes; all constrain seat dispatch.**

### 2.3 Scope sweep

```console
$ for p in 4175743 4177041 4181543; do ls -l /proc/$p/fd | grep -c 'Projects/shokunin'; done
0
0
0
$ for p in 4175743 4177041 4181543; do ls -l /proc/$p/fd | grep -E 'kimi-code|devin|bashrc|\.profile|config\.toml' || echo "  no custody-path fd"; done
PID 4175743: no custody-path fd
PID 4177041: no custody-path fd
PID 4181543: (matches were `comp*` jar names under the Ghidra install — substring false
              positives of the `omp` pattern; no home-config path appeared)
$ tr '\0' '\n' < /proc/4175743/environ | grep -E '^(TMPDIR|GHIDRA|REA_|HOME|PWD)='
PWD=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
HOME=/home/vgpnk
TMPDIR=/var/tmp/arc2-l4r4-pe
$ tail -n +2 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
RC=0        (at ~19:05Z; re-run 19:12Z post-OOM, rc=0 again)
```

Network — the one deviation:

```console
$ grep -n 'http fetch' /home/vgpnk/.npm/_logs/2026-10-18T19_03_02_856Z-debug-0.log
13 http fetch GET 200 https://registry.npmjs.org/rea-agents 48ms (cache revalidated)
$ ss -tnp | grep 4175743
ESTAB 0 0 [2804:…]:48630 [2606:4700::6810:622]:443 users:(("npm exec rea-ag",pid=4175743,fd=22))
```

The npm debug log is fd 20 of pid 4175743 (verified in the fd listing); the fetch is the run's
own, at 19:03:02Z. It is a packument revalidation, not a package download.

Repo-write surface during the run's life (`find <repo> -newermt '2026-10-18 16:03:00' -type f`,
at 19:06Z): only `receipts/config-pre-pair.txt`, `E23.md`, `E4.md`, `e16-table.json` —
parent/seat artifacts; nothing attributable to the run.

### 2.4 Terminal event — contained OOM (measured live)

```console
$ systemctl --user show run-p4175743-i29293759.scope -p Description -p MemoryMax -p MemorySwapMax -p MemoryPeak -p Result
Description=arc2-pe-wall
MemoryMax=7516192768
MemorySwapMax=1073741824
MemoryPeak=7516192768
Result=oom-kill
$ cat /var/tmp/arc2-l4r4-pe/exit.txt
exit=1 wall_utc=2026-10-18T19:07:45Z
$ journalctl --user -u run-p4175743-i29293759.scope --no-pager
Oct 18 16:03:02 … Started arc2-pe-wall.
Oct 18 16:07:45 … The kernel OOM killer killed some processes in this unit.
Oct 18 16:07:45 … Failed with result 'oom-kill'.
Oct 18 16:07:45 … Consumed 9min 2.497s CPU time over 4min 42.603s wall clock time, 7G memory peak, 1G memory swap peak.
$ journalctl -k --since "2026-10-18 16:07:44" --until "2026-10-18 16:07:46" --no-pager | grep -E 'failcnt|constraint|Killed process'
… decompile invoked oom-killer: … oom_score_adj=200
… memory: usage 7340032kB, limit 7340032kB, failcnt 5359
… swap: usage 1048552kB, limit 1048576kB, failcnt 53192
… oom-kill:constraint=CONSTRAINT_MEMCG,… oom_memcg=/user.slice/…/run-p4175743-i29293759.scope,task=java,pid=4181543
… Memory cgroup out of memory: Killed process 4181543 (java) … oom_score_adj:200
$ journalctl -k --since "2026-10-18 16:03" --no-pager | grep -c 'Killed process'
1        (the scoped java only; zero CONSTRAINT_NONE / global_oom lines in the window)
```

Trajectory (my samples): at 19:07:10Z `MemoryCurrent=4397207552`, `MemoryPeak=6552682496`
(4.09 / 6.10 GiB); host `available` 6.6 GiB at 19:04Z, 7.7 GiB at 19:07Z, 12 GiB after the
kill; host swap 9.1 → 10 GiB, never near round-3's 16.5 GiB peak. Typed negative at
`/var/tmp/arc2-l4r4-pe/stdout.json` (20,093 B): `code: cancelled`, `retryable: true`,
`cleanup: complete`, `process_id: 4181543`, `target_sha256: 7a2ccd68…`,
`run_id: 4cd20f34-…`. The Ghidra session dir `/var/tmp/arc2-l4r4-pe/rea-ghidra-1Uwcai/`
existed during the run (442 MB at 19:05Z) and is gone after (2.6 MB left; `cleanup: complete`);
no `/tmp/rea-ghidra-*` residue from this run (TMPDIR was redirected off tmpfs).

### 2.5 Corroboration in sibling records (read this session)

Sibling seat files were rewritten at 16:14–16:16Z while this report was open (their own
work); pointers below are anchored by quoted text, with the line number as observed at my
last read (19:16Z) — the drift class this round's C1 addresses, applied to my own citations.

- `E11.md` (header line and §4): "… **OOM-killed by its own 7 G cgroup cap at 19:07:45Z,
  4 m 42 s in**" (observed at :21-22 and :264); §4 journal lines (:190-207); post-OOM
  custody 5/5 (:230).
- `E22.md`: "`Result=oom-kill`, `MemoryPeak=7516192768` = `MemoryMax`" (observed at :545-546);
  "never killed, reniced, restarted, or signalled — it OOM-killed itself at 19:07:45Z"
  (observed at :613).
- `V3.md:3`, `E4.md:8-9`, `E4.md:314` (observed): observed read-only, never signalled.
- `E16.md` (battery note, observed at :345) and `E22.md` (draft-diff block, observed at
  :438-439): "one registry packument revalidation" — the network caveat is disclosed
  before this report.

### 2.6 Wave liveness during the run

Seat reports landed in the wave dir at 19:06Z (E4), 19:07Z (E23), 19:09Z (SC2), 19:10Z (E13),
19:11Z (E11, E20), 19:12Z (E12, E22, S1, V3); parent commit `1692acbe` ("rule 11") at
19:09:10Z. The run did not serialize the wave or the parent.

## 3. VERBATIM — text the parent may land (round record or LOG)

```text
CR4 (round 4) — background PE run adjudicated. No violation of the one-batched-
dispatch discipline: the run is round infrastructure, not an L2 seat (no seat
prompt/report duty; launched by the parent's own receipt shell at 19:03:02Z;
MISSION.md:55-56 governs seat dispatch, not host processes). One strict-form
scope deviation, disclosed: "npx cache resolution expected offline" was falsified
— the run's npm exec made one registry packument revalidation (GET 200
registry.npmjs.org/rea-agents, 48ms; debug log file line 14), metadata-only,
package served from the cached 6.5.0 tree (already noted in E16's battery note and
E22's draft-diff block, "one registry packument revalidation"). Custody untouched
(no custody-path fd; 5/5 rc=0 before, during,
post-OOM). Outcome: contained CONSTRAINT_MEMCG OOM at 19:07:45Z, 4m42s, peak ==
cap (7516192768 B), zero host-level OOM kills, deadline never bound; typed
negative at /var/tmp/arc2-l4r4-pe/stdout.json (exit=1, code=cancelled,
cleanup:complete). Residue duty: systemctl --user reset-failed
run-p4175743-i29293759.scope.
```

## 4. Conclusions, labeled

**Observations** (ran/read this session): the process chain and its parent shell (receipt
shell, 19:03:02Z); cwd of all three processes = the lane repo; the launcher script's contents
and sha256; `TMPDIR=/var/tmp/arc2-l4r4-pe` in the npm environ; `-Xmx6G` in the JVM cmdline
(heap knob effective); scope properties `MemoryMax=7516192768`, `MemorySwapMax=1073741824`,
`Result=oom-kill`, `MemoryPeak == MemoryMax`; the journal's OOM trio (user unit + kernel
`CONSTRAINT_MEMCG` lines, killed pid 4181543 java, failcnt 5359 memory / 53192 swap); one
`Killed process` line total in the window, zero `global_oom`; `exit.txt` = `exit=1
wall_utc=2026-10-18T19:07:45Z`; the typed negative's fields; the npm fetch line and the ESTAB
socket; zero repo/custody fds; receipt 5/5 at two checks; sibling corroboration (§2.5); the
wave's concurrent landing times and the parent commit; the failed transient unit still listed.

**Inferences:** (1) the one-batched rule, read against its own text, governs seat dispatch and
therefore cannot be violated by a parent-run host process — the run is outside its subject
matter, and the rule is a minimum, not an exclusive channel; (2) the "offline npx" expectation
is falsified by npm's own cache-revalidation behavior under `npx -y`, a metadata-only touch
whose disclosure duty the wave's records already discharged; (3) the OOM at 4 m 42 s means
this configuration's binding constraint is the cgroup memory ceiling (6 G heap + children
inside a 7 G cap), not the deadline — a C2 coverage datum whose interpretation belongs to
E11/E22/the parent; (4) the containment design converted the predicted host-level risk into a
leg-local typed negative.

**Unknowns:** (1) whether the wave dispatch itself was one batched call — no in-repo dispatch
receipt exists to verify (same unknown as round-1 `R5.md:402`); (2) why
`REA_GHIDRA_STARTUP_TIMEOUT_MS` / `GHIDRA_HEADLESS_MAXMEM` did not appear in the npm process's
`/proc/environ` at my 19:06Z read despite the launcher setting them and the JVM cmdline
proving `-Xmx6G` took effect (processes gone; not re-verifiable post-mortem); (3) whether
`--offline` would have suppressed the packument revalidation (not tested); (4) the final C2
disposition of the OOM result (parent/E11's call).

## 5. Scope compliance and residue

- Only write: this report. `git status --porcelain` → wave dir + `e16-table.json` (parent's),
  nothing else touched by me. No git mutations, no config edits, no installs, no network
  fetches, no REA probes, no battery leg. No scratch files created; no other seat's files
  modified. The PE run was never signalled, renice'd, or touched; its scratch was read only.
- Residue for the parent (not mine to clear): the failed transient scope unit
  `run-p4175743-i29293759.scope` (`systemctl --user is-failed` → `failed`) needs
  `systemctl --user reset-failed run-p4175743-i29293759.scope`; the run's typed negative and
  exit stamp remain under `/var/tmp/arc2-l4r4-pe/` as evidence.
