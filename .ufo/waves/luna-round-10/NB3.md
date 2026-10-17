## CLAIM
Independent (pass-2) sentinel-hygiene audit of `/tmp` + processes at 2026-10-16 22:44:03 -0300 replicates lane-A N3: 16 stale round-6/8 `/tmp` roots (1,096,013,272 B) persist with zero live process references, and no luna-round-10 kaidoku scratch or stray fleet process exists. Verdict is a FINDING on the persisting pre-wave leftovers.

## METHOD
Read-only. `/tmp` name scan (`kaidoku|luna-round|rea-ghidra|rea-agent|shokunin|analyzeheadless|\.ufo`), per-root `du -sb` + mtimes; `/proc/*/{fd,cwd,exe}` scan against those roots; `/proc/*/cwd`+`comm` scan for processes attached to the fleet root or the kaidoku repo; zombie scan; `crontab -l` (not installed), `systemctl --user list-timers --all`, `/etc/cron.d` (absent). No deletions, no live probes, no network. Snapshot context: actual HEAD is `c343939` (operator protocol-conformance rollout, +16 LOG / +12 SCORECARD, 0 deletions, committed 22:42:01 during this wave), not the briefed `6e83a20`; `git diff --quiet HEAD` clean.

## FINDINGS
- `candidate_roots:16 TOTAL_BYTES=1096013272` — byte-identical to N3's 22:33 figure; newest candidate mtime `2026-10-16 20:57:13` (~1.5 h before this wave). No round-10-labelled kaidoku entries appeared. Largest: two npm caches (329,808,132 + 329,809,645 B), leg-10 stdout 2,127,950 B, `luna-round-8-leg-6.sqlite` (valid SQLite 3, pages=2).
- Reference scan: `process_refs_to_candidates: []`; deleted-open fds are all desktop noise (Steam/Chromium/gvfs), none fleet.
- Fleet-attached processes = 6: two kimi chains — 2728/2959/3018 (18:47) and 733888/734193/734254 (22:33) — cwd `/home/vgpnk/Projects/shokunin`; no process holds cwd or fds under the kaidoku repo except transient in-flight seat shells (bash + `sleep 15`/`sleep 20`, ppid 2959). No ghidra/java/analyzeheadless/rea-agents/shokunin-watchdog process; no respawn machinery (only unrelated `ai-usage.timer`).
- Zombies: 5 `uwsm-app`/`systemctl` defunct — desktop session, not fleet.
- N3's `npm exec godot-mcp` (666065/666084) is ZCode editor infra (parent zcode-cli 665992, cwd `~/.zcode/workspace/default`), pre-dating the wave.

## THREATS
Name-pattern attribution only; point-in-time snapshot — later seats may add `/tmp` scratch. Shared `/tmp` currently hosts sibling-repo scratch (`/tmp/kumitate-conformance` 22:43:21, `wb3.diff`, wav rerecords) outside my markers and unaudited. A process that started and exited between scans cannot be excluded. N3's open item — config byte/hash identity — remains unverified by me (scope = /tmp + processes).

## VERDICT
FINDING: pass-1 replicated — 16 pre-wave `/tmp` roots (1,096,013,272 B) persist, zero process refs, no round-10 kaidoku scratch or stray fleet process; HEAD drift to c343939 noted.
