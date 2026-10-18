# SC1 (scout) — round-7 config custody 5-path check + service fd scan

## (1) Verdict

**PASS — custody 5/5 HELD; service fd scan CLEAN (no custody/repo fds).** Live service `arc2-r7-pe` observed strictly read-only (no signal, no kill, no write).

## (2) Evidence

Baseline: HEAD `995e6a0799c4dad26942de15bd9058fe7acb676d` (`git rev-parse HEAD`, matches the round claim "995e6a0").

### Custody 5/5

Instrument: `.ufo/waves/arc2-loop1-round7/receipts/config-pre-pair.txt:1-6` — line 1 stamps the pre-pair at `2026-10-18T21:40:26Z`; lines 2-6 are the 5 sha256 rows:

| path | pre-pair == now |
|---|---|
| `/home/vgpnk/.config/devin/mcp_config.json` | 16f496e6… MATCH |
| `/home/vgpnk/.omp/agent/mcp.json` | 38d2a1d0… MATCH |
| `/home/vgpnk/.kimi-code/config.toml` | e0634d8c… MATCH |
| `/home/vgpnk/.bashrc` | 7d2ca28a… MATCH |
| `/home/vgpnk/.profile` | 6c6be761… MATCH |

Command: `diff <(tail -n +2 .ufo/waves/arc2-loop1-round7/receipts/config-pre-pair.txt | sort -k2) <(sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile | sort -k2)`
Observed: empty diff, then `=== CUSTODY 5/5 MATCH ===`. Pairing exactness: `systemctl --user show arc2-r7-pe -p ExecMainStartTimestamp` → `Sun 2026-10-18 18:40:26 -03` = 21:40:26Z, identical to the receipt stamp on line 1.

### Service fd scan (no custody/repo fds)

`systemctl --user show arc2-r7-pe` → ActiveState=active, SubState=running, MainPID=3224316, MemoryCurrent=4302942208 (~4.3G, inside 6G heap / 9G cap). Cgroup `…/user@1000.service/app.slice/arc2-r7-pe.service` holds 3 PIDs: 3224316 (npm exec, 23 fds), 3224356 (node rea analyze, 23 fds), 3224474 (java Ghidra 12.1.4, 165 fds) — **211 fds total**.

Distribution (`readlink /proc/<pid>/fd/* | sort | uniq -c | sort -rn`, top 40 shown): only `anon_inode:[io_uring|eventpoll|eventfd]`, `/dev/null`, `pipe:[…]`, `socket:[…]`, `/var/tmp/arc2-l7r7-pe/**` (stdout.json, stderr.log, script.log, ghidra.log, rea-project.lock~, 2 ghidra caches, 1 deleted felixcache lock), JVM `lib/modules`, npm debug log, and read-only Ghidra processor jars under `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/`.

Custody/repo filter: `… | grep -E '/home/vgpnk/Projects/shokunin/kaidoku-shokunin|/home/vgpnk/\.config/devin/mcp_config\.json|/home/vgpnk/\.omp/agent/mcp\.json|/home/vgpnk/\.kimi-code/config\.toml|/home/vgpnk/\.bashrc|/home/vgpnk/\.profile'` → no match, `NO-CUSTODY-OR-REPO-FDS (grep exit 1)`.

Residual sweep (everything outside the benign prefixes): only `/dev/random`, `/dev/urandom`. Target exe (`…/godot/export_templates/4.7.2.stable/windows_release_arm64.exe`) has no open fd at scan time.

Env cross-check (`tr '\0' '\n' < /proc/3224474/environ | grep -E '^(REA_|TMPDIR=)'`): `REA_GHIDRA_DISABLED_ANALYZERS=Call Convention ID,Decompiler Parameter ID,Decompiler Switch Analysis` (exact validated names), `REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000`, `TMPDIR=/var/tmp/arc2-l7r7-pe/rea-ghidra-tYDK4I/tmp` — matches the briefed launch config; TMPDIR discipline is visible in the fd set (all Ghidra scratch under `/var/tmp/arc2-l7r7-pe/`).

## (3) Verbatim-landable text

```
- Custody 5/5 HELD: pre-pair receipt `.ufo/waves/arc2-loop1-round7/receipts/config-pre-pair.txt` (2026-10-18T21:40:26Z, same instant as `arc2-r7-pe` start 18:40:26 -03) re-verified byte-identical post-launch — sha256sum of devin mcp_config.json, .omp/agent/mcp.json, .kimi-code/config.toml, .bashrc, .profile matches 5/5 (empty diff).
- Service fd scan CLEAN: `arc2-r7-pe` (3 pids — npm wrapper, node rea, java Ghidra; 211 fds) holds zero custody fds and zero repo fds; full fd set = {anon_inode, pipe, socket, /dev/null, /dev/random, /dev/urandom} ∪ `/var/tmp/arc2-l7r7-pe/**` ∪ read-only JVM/Ghidra/npm libs. TMPDIR discipline confirmed in-fd-set (Ghidra scratch only under the designated TMPDIR) and in-env (`REA_GHIDRA_DISABLED_ANALYZERS` exact validated names, 7200000 ms timeout).
```

## (4) Labels

- **Observation:** 5/5 hash match; 211 fds enumerated across 3 PIDs; grep exit 1 on custody/repo patterns; residual sweep = /dev/random + /dev/urandom; env keys as briefed; memory ~4.3G.
- **Inference:** target-exe fd absent ⇒ Ghidra closed it after program import (normal mid-analyze state), not an error; custody held through the service's start and current runtime because hashes taken after launch (now) equal the pre-launch receipt.
- **Unknown:** custody beyond this instant (scan is point-in-time, not continuous — a close-of-round re-check by the integrating seat is still worthwhile if the run outlives this report); final analyze outcome (C1 hold/typed-refusal) is out of this seat's scope and belongs to the WATCH seats.
